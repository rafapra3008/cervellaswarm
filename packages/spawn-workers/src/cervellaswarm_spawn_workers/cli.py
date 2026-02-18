# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""
CLI entry points for CervellaSwarm Spawn Workers.

Provides the ``cervella-spawn`` command for launching, monitoring,
and managing worker processes.
"""

import argparse
import sys
from pathlib import Path

from cervellaswarm_spawn_workers import __version__
from cervellaswarm_spawn_workers.prompt_builder import SPECIALTIES, build_worker_prompt
from cervellaswarm_spawn_workers.spawner import SpawnManager
from cervellaswarm_spawn_workers.team_loader import load_team


def main(argv: list[str] | None = None) -> None:
    """Main CLI entry point for cervella-spawn."""
    parser = argparse.ArgumentParser(
        prog="cervella-spawn",
        description="Config-driven worker spawning for multi-agent systems.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("--team", type=str, help="Path to team.yaml config file")
    group.add_argument("--worker", type=str, help="Spawn a single worker by name")
    group.add_argument("--status", action="store_true", help="Show worker status")
    group.add_argument("--kill", action="store_true", help="Kill all workers")
    group.add_argument("--list", action="store_true", help="List available specialties")

    parser.add_argument("--specialty", type=str, default="generic",
                        help="Worker specialty (default: generic)")
    parser.add_argument("--prompt", type=str, help="Custom system prompt for the worker")
    parser.add_argument("--tasks-dir", type=str, default=".swarm/tasks",
                        help="Tasks directory (default: .swarm/tasks)")
    parser.add_argument("--logs-dir", type=str, default=".swarm/logs",
                        help="Logs directory (default: .swarm/logs)")
    parser.add_argument("--max-workers", type=int, default=5,
                        help="Max concurrent workers (default: 5)")
    parser.add_argument("--backend", type=str, choices=["tmux", "nohup"],
                        help="Force execution backend (default: auto-detect)")
    parser.add_argument("--claude-bin", type=str, help="Path to claude CLI binary")

    args = parser.parse_args(argv)

    if args.list:
        _cmd_list()
        return

    if args.status:
        _cmd_status(args)
        return

    if args.kill:
        _cmd_kill(args)
        return

    if args.team:
        _cmd_team(args)
        return

    if args.worker:
        _cmd_worker(args)
        return

    parser.print_help()


def _cmd_list() -> None:
    """List available worker specialties."""
    print("\nAvailable worker specialties:\n")
    for name, desc in sorted(SPECIALTIES.items()):
        print(f"  {name:<12} {desc}")
    print()


def _cmd_status(args: argparse.Namespace) -> None:
    """Show status of all tracked workers."""
    manager = _make_manager(args, register_signals=False)

    statuses = manager.get_status()
    if not statuses:
        print("No workers tracked.")
        return

    print(f"\n{'NAME':<16} {'STATUS':<10} {'BACKEND':<8} {'UPTIME':<12} {'SESSION/PID'}")
    print("-" * 70)
    for s in statuses:
        status_str = "ALIVE" if s.alive else "DEAD"
        uptime_str = _format_uptime(s.uptime_seconds) if s.alive else "-"
        id_str = s.session_name or str(s.pid or "-")
        print(f"{s.name:<16} {status_str:<10} {s.backend:<8} {uptime_str:<12} {id_str}")
    print()


def _cmd_kill(args: argparse.Namespace) -> None:
    """Kill all workers."""
    manager = _make_manager(args, register_signals=False)

    killed = manager.kill_all()
    manager.cleanup()
    print(f"Killed {killed} worker(s).")


def _cmd_team(args: argparse.Namespace) -> None:
    """Spawn workers from a team.yaml config."""
    team_path = Path(args.team)
    try:
        team = load_team(team_path)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error loading team config: {e}", file=sys.stderr)
        sys.exit(1)

    manager = _make_manager(args)

    # Apply team spawn config
    if team.spawn.tasks_dir != ".swarm/tasks":
        manager.tasks_dir = Path(team.spawn.tasks_dir)
    if team.spawn.logs_dir != ".swarm/logs":
        manager.logs_dir = Path(team.spawn.logs_dir)
    if team.spawn.max_workers != 5:
        manager.max_workers = team.spawn.max_workers

    result = manager.spawn_team(team)

    print(f"\nSpawned: {result.spawned} worker(s)")
    if result.failed:
        print(f"Failed:  {result.failed} worker(s)")
        for err in result.errors:
            print(f"  - {err}")

    if result.workers:
        print(f"\nWorkers running ({manager.backend} backend):")
        for w in result.workers:
            print(f"  - {w.name} -> {w.session_name or w.pid}")
    print()


def _cmd_worker(args: argparse.Namespace) -> None:
    """Spawn a single worker."""
    manager = _make_manager(args)

    system_prompt = args.prompt
    if system_prompt is None:
        system_prompt = build_worker_prompt(
            args.worker, args.specialty, args.tasks_dir
        )

    try:
        worker = manager.spawn_worker(
            name=args.worker,
            system_prompt=system_prompt,
            specialty=args.specialty,
        )
        print(f"Spawned {worker.name} ({worker.backend})")
        if worker.session_name:
            print(f"  Session: {worker.session_name}")
        if worker.pid:
            print(f"  PID: {worker.pid}")
        if worker.log_file:
            print(f"  Log: {worker.log_file}")
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def _make_manager(args: argparse.Namespace, register_signals: bool = True) -> SpawnManager:
    """Create a SpawnManager from CLI args."""
    return SpawnManager(
        tasks_dir=args.tasks_dir,
        logs_dir=args.logs_dir,
        max_workers=args.max_workers,
        backend=args.backend,
        claude_bin=args.claude_bin,
        register_signals=register_signals,
    )


def _format_uptime(seconds: float) -> str:
    """Format uptime seconds into human-readable string."""
    if seconds < 60:
        return f"{seconds:.0f}s"
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    if minutes < 60:
        return f"{minutes}m {secs}s"
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours}h {mins}m"
