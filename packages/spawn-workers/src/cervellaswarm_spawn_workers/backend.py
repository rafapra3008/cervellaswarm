# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""
Execution backends for worker processes.

Supports tmux (preferred) and nohup (universal fallback).
Auto-detects the best available backend.
"""

import logging
import os
import shutil
import signal
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class ProcessInfo:
    """Information about a launched worker process."""

    pid: Optional[int] = None
    session_name: Optional[str] = None
    backend: str = "unknown"
    log_file: Optional[Path] = None
    start_time: float = field(default_factory=time.time)


def detect_backend() -> str:
    """Auto-detect the best available execution backend.

    Returns:
        "tmux" if tmux is installed, otherwise "nohup".
    """
    if shutil.which("tmux"):
        return "tmux"
    return "nohup"


def launch_tmux(
    session_name: str,
    command: str,
    log_file: Path,
    cwd: Optional[Path] = None,
    env: Optional[dict] = None,
) -> ProcessInfo:
    """Launch a command in a detached tmux session.

    Args:
        session_name: Unique tmux session name.
        command: Shell command to execute.
        log_file: Path to write stdout/stderr.
        cwd: Working directory for the command.
        env: Additional environment variables.

    Returns:
        ProcessInfo with session details.

    Raises:
        RuntimeError: If tmux session creation fails.
    """
    log_file.parent.mkdir(parents=True, exist_ok=True)

    full_command = f"{command} 2>&1 | tee \"{log_file}\""

    run_env = os.environ.copy()
    if env:
        run_env.update(env)

    result = subprocess.run(
        ["tmux", "new-session", "-d", "-s", session_name, full_command],
        cwd=str(cwd) if cwd else None,
        env=run_env,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"Failed to create tmux session '{session_name}': {result.stderr.strip()}"
        )

    # Set remain-on-exit to preserve output after process ends
    subprocess.run(
        ["tmux", "set-option", "-t", session_name, "remain-on-exit", "on"],
        capture_output=True,
    )

    return ProcessInfo(
        session_name=session_name,
        backend="tmux",
        log_file=log_file,
    )


def launch_nohup(
    command: str,
    log_file: Path,
    cwd: Optional[Path] = None,
    env: Optional[dict] = None,
) -> ProcessInfo:
    """Launch a command as a background process using nohup-style detach.

    Args:
        command: Shell command to execute.
        log_file: Path to write stdout/stderr.
        cwd: Working directory for the command.
        env: Additional environment variables.

    Returns:
        ProcessInfo with PID.
    """
    log_file.parent.mkdir(parents=True, exist_ok=True)

    run_env = os.environ.copy()
    if env:
        run_env.update(env)

    with open(log_file, "w") as log_fh:
        proc = subprocess.Popen(
            command,
            shell=True,  # nosec: command is built internally by spawner with shlex.quote
            stdout=log_fh,
            stderr=subprocess.STDOUT,
            cwd=str(cwd) if cwd else None,
            env=run_env,
            start_new_session=True,
        )

    return ProcessInfo(
        pid=proc.pid,
        backend="nohup",
        log_file=log_file,
    )


def is_alive_tmux(session_name: str) -> bool:
    """Check if a tmux session is still running."""
    result = subprocess.run(
        ["tmux", "has-session", "-t", session_name],
        capture_output=True,
    )
    return result.returncode == 0


def is_alive_pid(pid: int) -> bool:
    """Check if a process with the given PID is still running."""
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        # PermissionError means the process EXISTS but we can't signal it
        return True


def kill_tmux(session_name: str) -> bool:
    """Kill a tmux session.

    Returns:
        True if session was killed, False if it didn't exist.
    """
    result = subprocess.run(
        ["tmux", "kill-session", "-t", session_name],
        capture_output=True,
    )
    return result.returncode == 0


def kill_pid(pid: int, graceful_timeout: float = 3.0) -> bool:
    """Kill a process by PID with graceful shutdown.

    Sends SIGTERM first, then SIGKILL after timeout.

    Args:
        pid: Process ID to kill.
        graceful_timeout: Seconds to wait after SIGTERM before SIGKILL.

    Returns:
        True if process was killed, False if it didn't exist.
    """
    try:
        os.kill(pid, signal.SIGTERM)
    except ProcessLookupError:
        return False
    except PermissionError:
        logger.warning("No permission to SIGTERM PID %d", pid)
        return False

    deadline = time.time() + graceful_timeout
    while time.time() < deadline:
        if not is_alive_pid(pid):
            return True
        time.sleep(0.1)

    # Force kill
    try:
        os.kill(pid, signal.SIGKILL)
        return True
    except (ProcessLookupError, PermissionError):
        return not is_alive_pid(pid)


def list_tmux_sessions(prefix: str = "swarm_") -> list[str]:
    """List tmux sessions matching the given prefix.

    Args:
        prefix: Session name prefix to filter by.

    Returns:
        List of matching session names.
    """
    result = subprocess.run(
        ["tmux", "list-sessions", "-F", "#{session_name}"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return []

    return [
        name.strip()
        for name in result.stdout.splitlines()
        if name.strip().startswith(prefix)
    ]
