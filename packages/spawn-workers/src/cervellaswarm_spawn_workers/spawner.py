# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""
Core spawn logic for multi-agent worker management.

Provides SpawnManager for launching, monitoring, and killing worker
processes across tmux and nohup backends with signal handling.
"""

import atexit
import logging
import os
import shlex
import shutil
import signal
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from cervellaswarm_spawn_workers.backend import (
    ProcessInfo,
    detect_backend,
    is_alive_pid,
    is_alive_tmux,
    kill_pid,
    kill_tmux,
    launch_nohup,
    launch_tmux,
)
from cervellaswarm_spawn_workers.prompt_builder import build_worker_prompt
from cervellaswarm_spawn_workers.team_loader import AgentConfig, TeamConfig, get_spawnables

logger = logging.getLogger(__name__)


@dataclass
class WorkerInfo:
    """Information about a spawned worker."""

    name: str
    backend: str
    session_name: Optional[str] = None
    pid: Optional[int] = None
    log_file: Optional[Path] = None
    start_time: float = field(default_factory=time.time)


@dataclass
class WorkerStatus:
    """Current status of a worker."""

    name: str
    alive: bool
    backend: str
    pid: Optional[int] = None
    session_name: Optional[str] = None
    uptime_seconds: float = 0.0


@dataclass
class SpawnResult:
    """Result of a spawn operation."""

    spawned: int = 0
    failed: int = 0
    workers: list[WorkerInfo] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


class SpawnManager:
    """Manages the lifecycle of spawned worker processes.

    Handles spawning, monitoring, and cleanup of workers across
    tmux and nohup backends. Registers signal handlers for
    graceful shutdown on SIGINT/SIGTERM.

    Args:
        tasks_dir: Directory for task files.
        logs_dir: Directory for worker log files.
        status_dir: Directory for PID/session tracking files.
        max_workers: Maximum number of concurrent workers.
        backend: Execution backend ("tmux", "nohup", or None for auto-detect).
        claude_bin: Path to claude CLI binary.
        register_signals: Whether to register signal handlers (default True).
    """

    def __init__(
        self,
        tasks_dir: str = ".swarm/tasks",
        logs_dir: str = ".swarm/logs",
        status_dir: str = ".swarm/status",
        max_workers: int = 5,
        backend: Optional[str] = None,
        claude_bin: Optional[str] = None,
        register_signals: bool = True,
    ):
        self.tasks_dir = Path(tasks_dir)
        self.logs_dir = Path(logs_dir)
        self.status_dir = Path(status_dir)
        self.max_workers = max_workers
        self.backend = backend or detect_backend()
        self.claude_bin = claude_bin or shutil.which("claude") or "claude"
        self.workers: list[WorkerInfo] = []

        if register_signals:
            signal.signal(signal.SIGINT, self._signal_handler)
            signal.signal(signal.SIGTERM, self._signal_handler)
            atexit.register(self.cleanup)

        # Load existing workers from status directory (for --status/--kill)
        self._load_tracked_workers()

    def _load_tracked_workers(self) -> None:
        """Load previously tracked workers from status directory files."""
        if not self.status_dir.exists():
            return

        # Find all worker start files to discover tracked workers
        for start_file in self.status_dir.glob("worker_*.start"):
            name = start_file.stem.removeprefix("worker_")

            session_file = self.status_dir / f"worker_{name}.session"
            pid_file = self.status_dir / f"worker_{name}.pid"

            session_name = None
            pid = None

            try:
                start_time = float(start_file.read_text().strip())
            except (ValueError, OSError) as e:
                logger.warning("Cannot read start file %s: %s", start_file, e)
                continue

            try:
                if session_file.exists():
                    session_name = session_file.read_text().strip()
            except OSError as e:
                logger.warning("Cannot read session file %s: %s", session_file, e)

            if pid_file.exists():
                try:
                    pid = int(pid_file.read_text().strip())
                except (ValueError, OSError):
                    pass

            backend = "tmux" if session_name else "nohup"

            worker = WorkerInfo(
                name=name,
                backend=backend,
                session_name=session_name,
                pid=pid,
                start_time=start_time,
            )
            self.workers.append(worker)

    def _signal_handler(self, signum: int, frame: object) -> None:
        """Handle SIGINT/SIGTERM by killing all workers."""
        logger.info("Signal %d received, shutting down workers...", signum)
        self.kill_all()
        raise SystemExit(128 + signum)

    def spawn_worker(
        self,
        name: str,
        system_prompt: Optional[str] = None,
        initial_prompt: Optional[str] = None,
        specialty: str = "generic",
        cwd: Optional[Path] = None,
    ) -> WorkerInfo:
        """Spawn a single worker process.

        Args:
            name: Worker name (used in session name and tracking).
            system_prompt: Custom system prompt. If None, auto-generated from specialty.
            initial_prompt: Initial user message for the worker.
            specialty: Worker specialty for auto-generated prompt.
            cwd: Working directory for the worker.

        Returns:
            WorkerInfo for the spawned worker.

        Raises:
            RuntimeError: If max_workers limit reached or spawn fails.
        """
        alive_count = sum(1 for w in self.get_status() if w.alive)
        if alive_count >= self.max_workers:
            raise RuntimeError(
                f"Max workers limit reached ({self.max_workers}). "
                f"Kill existing workers first."
            )

        if system_prompt is None:
            system_prompt = build_worker_prompt(
                name, specialty, str(self.tasks_dir)
            )

        if initial_prompt is None:
            initial_prompt = (
                f"Check {self.tasks_dir}/ for .ready tasks assigned to you "
                f"and start working. If no tasks found, terminate."
            )

        # Ensure directories exist
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        self.status_dir.mkdir(parents=True, exist_ok=True)

        # Write prompt to file
        prompts_dir = self.logs_dir.parent / "prompts"
        prompts_dir.mkdir(parents=True, exist_ok=True)
        prompt_file = prompts_dir / f"worker_{name}.txt"
        prompt_file.write_text(system_prompt)

        # Build claude command (shlex.quote for shell injection safety)
        # Use shlex.quote for prompt content instead of $(cat file) to prevent
        # shell interpretation of $, `, " characters in the prompt
        command = (
            f'CERVELLASWARM_WORKER=1 '
            f'{shlex.quote(self.claude_bin)} -p '
            f'--append-system-prompt {shlex.quote(system_prompt)} '
            f'{shlex.quote(initial_prompt)}'
        )

        timestamp = int(time.time())
        session_name = f"swarm_{name}_{timestamp}"
        log_file = self.logs_dir / f"worker_{name}_{timestamp}.log"

        env = {"CERVELLASWARM_WORKER": "1"}

        if self.backend == "tmux":
            info = launch_tmux(session_name, command, log_file, cwd=cwd, env=env)
        else:
            info = launch_nohup(command, log_file, cwd=cwd, env=env)

        worker = WorkerInfo(
            name=name,
            backend=info.backend,
            session_name=info.session_name,
            pid=info.pid,
            log_file=info.log_file,
            start_time=info.start_time,
        )
        self.workers.append(worker)

        # Write tracking files
        if info.session_name:
            (self.status_dir / f"worker_{name}.session").write_text(info.session_name)
        if info.pid:
            (self.status_dir / f"worker_{name}.pid").write_text(str(info.pid))
        (self.status_dir / f"worker_{name}.start").write_text(str(timestamp))

        logger.info("Spawned %s (%s): session=%s pid=%s",
                     name, self.backend, info.session_name, info.pid)

        return worker

    def spawn_team(self, team: TeamConfig) -> SpawnResult:
        """Spawn all workers defined in a team configuration.

        Args:
            team: TeamConfig with agents to spawn.

        Returns:
            SpawnResult with counts and worker info.
        """
        result = SpawnResult()
        agents = get_spawnables(team)

        for agent in agents:
            try:
                worker = self.spawn_worker(
                    name=agent.name,
                    system_prompt=agent.system_prompt,
                    specialty=agent.specialty,
                )
                result.workers.append(worker)
                result.spawned += 1
            except (RuntimeError, OSError) as e:
                result.errors.append(f"{agent.name}: {e}")
                result.failed += 1
                logger.error("Failed to spawn %s: %s", agent.name, e)

        return result

    def get_status(self) -> list[WorkerStatus]:
        """Get the current status of all tracked workers.

        Returns:
            List of WorkerStatus for each worker.
        """
        statuses = []
        now = time.time()

        for worker in self.workers:
            alive = False
            if worker.backend == "tmux" and worker.session_name:
                alive = is_alive_tmux(worker.session_name)
            elif worker.pid:
                alive = is_alive_pid(worker.pid)

            statuses.append(
                WorkerStatus(
                    name=worker.name,
                    alive=alive,
                    backend=worker.backend,
                    pid=worker.pid,
                    session_name=worker.session_name,
                    uptime_seconds=now - worker.start_time if alive else 0.0,
                )
            )

        return statuses

    def kill_all(self, graceful_timeout: float = 5.0) -> int:
        """Kill all tracked workers.

        Args:
            graceful_timeout: Seconds to wait after SIGTERM before SIGKILL.

        Returns:
            Number of workers killed.
        """
        killed = 0
        for worker in self.workers:
            if worker.backend == "tmux" and worker.session_name:
                if kill_tmux(worker.session_name):
                    killed += 1
            elif worker.pid:
                if kill_pid(worker.pid, graceful_timeout):
                    killed += 1

        logger.info("Killed %d/%d workers", killed, len(self.workers))
        return killed

    def kill_worker(self, name: str) -> bool:
        """Kill a specific worker by name.

        Args:
            name: Worker name.

        Returns:
            True if worker was found and killed.
        """
        for worker in self.workers:
            if worker.name == name:
                if worker.backend == "tmux" and worker.session_name:
                    return kill_tmux(worker.session_name)
                elif worker.pid:
                    return kill_pid(worker.pid)
        return False

    def cleanup(self) -> None:
        """Remove tracking files only for dead workers (not alive ones)."""
        if not self.status_dir.exists():
            return

        # Determine which workers are alive so we don't orphan them
        alive_names: set[str] = set()
        for status in self.get_status():
            if status.alive:
                alive_names.add(status.name)

        for pattern in ("worker_*.pid", "worker_*.session", "worker_*.start"):
            for f in self.status_dir.glob(pattern):
                # Extract worker name: worker_myname.pid -> myname
                stem = f.stem  # worker_myname
                suffix_map = {".pid": ".pid", ".session": ".session", ".start": ".start"}
                worker_name = stem.removeprefix("worker_")
                if worker_name in alive_names:
                    continue
                try:
                    f.unlink()
                except OSError:
                    pass
