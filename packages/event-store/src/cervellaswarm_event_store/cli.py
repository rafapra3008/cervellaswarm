# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""
CLI for cervellaswarm-event-store.

Usage:
    cervella-events init
    cervella-events log --type task_completed [--agent X] [--project X]
                        [--description TEXT] [--session-id X] [--success]
                        [--fail] [--duration-ms N] [--json]
    cervella-events query [--agent X] [--project X] [--type X]
                          [--session-id X] [--days N] [--limit N] [--json]
    cervella-events stats [--project X] [--json]
    cervella-events lessons [--agent X] [--project X] [--limit N] [--json]
    cervella-events patterns [--days N] [--min-occurrences N] [--json]
    cervella-events usage [--today] [--days N] [--project X] [--model X] [--json]
    cervella-events budget [--set-daily N] [--set-weekly N] [--set-monthly N]
                           [--check] [--json]
"""

import argparse
import importlib.metadata
import json
import sys
from typing import Optional


def _get_version() -> str:
    """Get package version from metadata."""
    try:
        return importlib.metadata.version("cervellaswarm-event-store")
    except importlib.metadata.PackageNotFoundError:
        return "0.1.0"


def _print_json(obj: object) -> None:
    print(json.dumps(obj, indent=2, default=str))


def _handle_error(e: Exception, json_mode: bool) -> None:
    """Print error and exit. Used by all CLI subcommands."""
    if json_mode:
        _print_json({"status": "error", "error": str(e)})
    else:
        print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)


# ------------------------------------------------------------------
# init
# ------------------------------------------------------------------


def main_init(argv: "list[str] | None" = None) -> None:
    """Initialize (or verify) the event store database."""
    parser = argparse.ArgumentParser(
        prog="cervella-events init",
        description="Initialize the event-store SQLite database",
    )
    parser.add_argument(
        "--db-path",
        default=None,
        help="Explicit path to database file (default: .cervella/event-store.db)",
    )
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args(argv)

    from cervellaswarm_event_store.database import EventStore

    try:
        db_path_arg = args.db_path if args.db_path else None
        store = EventStore(db_path=db_path_arg)
        db_path = str(store.db_path)
        store.close()

        if args.json:
            _print_json({"status": "ok", "db_path": db_path})
        else:
            print(f"Event store initialized: {db_path}")
    except Exception as e:
        _handle_error(e, args.json)


# ------------------------------------------------------------------
# log
# ------------------------------------------------------------------


def main_log(argv: "list[str] | None" = None) -> None:
    """Log a new event to the store."""
    parser = argparse.ArgumentParser(
        prog="cervella-events log",
        description="Log an event to the event store",
    )
    parser.add_argument("--type", dest="event_type", required=True, help="Event type")
    parser.add_argument("--agent", default=None, help="Agent name")
    parser.add_argument("--agent-role", default=None, help="Agent role")
    parser.add_argument("--project", default=None, help="Project name")
    parser.add_argument("--session-id", default=None, help="Session identifier")
    parser.add_argument("--description", default=None, help="Event description")
    parser.add_argument("--task-id", default=None, help="Task identifier")
    parser.add_argument("--status", default=None, help="Task status")
    parser.add_argument("--success", action="store_true", default=False, help="Mark event as successful")
    parser.add_argument("--fail", action="store_true", default=False, help="Mark event as failed")
    parser.add_argument("--duration-ms", type=int, default=None, help="Duration in milliseconds")
    parser.add_argument("--error-message", default=None, help="Error message")
    parser.add_argument("--tags", default=None, help="Comma-separated tags")
    parser.add_argument("--db-path", default=None, help="Explicit database path")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args(argv)

    from cervellaswarm_event_store.database import EventStore
    from cervellaswarm_event_store.writer import Event

    success_val: Optional[bool] = None
    if args.success:
        success_val = True
    elif args.fail:
        success_val = False

    tags_tuple: tuple = ()
    if args.tags:
        tags_tuple = tuple(t.strip() for t in args.tags.split(",") if t.strip())

    try:
        event = Event(
            event_type=args.event_type,
            agent_name=args.agent,
            agent_role=args.agent_role,
            project=args.project,
            session_id=args.session_id,
            description=args.description,
            task_id=args.task_id,
            status=args.status,
            success=success_val,
            duration_ms=args.duration_ms,
            error_message=args.error_message,
            tags=tags_tuple,
        )
    except ValueError as e:
        if args.json:
            _print_json({"status": "error", "error": str(e)})
        else:
            print(f"Validation error: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        with EventStore(db_path=args.db_path) as store:
            event_id = store.log_event(event)

        if args.json:
            _print_json({"status": "ok", "event_id": event_id})
        else:
            print(f"Event logged: {event_id}")
    except Exception as e:
        _handle_error(e, args.json)


# ------------------------------------------------------------------
# query
# ------------------------------------------------------------------


def main_query(argv: "list[str] | None" = None) -> None:
    """Query events from the store."""
    parser = argparse.ArgumentParser(
        prog="cervella-events query",
        description="Query events from the event store",
    )
    parser.add_argument("--agent", default="", help="Filter by agent name")
    parser.add_argument("--project", default="", help="Filter by project")
    parser.add_argument("--type", dest="event_type", default="", help="Filter by event type")
    parser.add_argument("--session-id", default="", help="Filter by session ID")
    parser.add_argument("--status", default="", help="Filter by status")
    parser.add_argument("--days", type=int, default=0, help="Limit to last N days")
    parser.add_argument("--limit", type=int, default=50, help="Maximum results (default: 50)")
    parser.add_argument("--db-path", default=None, help="Explicit database path")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args(argv)

    from cervellaswarm_event_store.database import EventStore

    try:
        with EventStore(db_path=args.db_path) as store:
            result = store.query_events(
                agent=args.agent,
                project=args.project,
                event_type=args.event_type,
                session_id=args.session_id,
                status=args.status,
                days=args.days,
                limit=args.limit,
            )

        if args.json:
            events_out = []
            for ev in result.events:
                events_out.append(
                    {
                        "id": ev.id,
                        "timestamp": ev.timestamp,
                        "event_type": ev.event_type,
                        "agent_name": ev.agent_name,
                        "project": ev.project,
                        "description": ev.description,
                        "status": ev.status,
                        "success": ev.success,
                        "duration_ms": ev.duration_ms,
                        "error_message": ev.error_message,
                        "session_id": ev.session_id,
                        "files_modified": list(ev.files_modified),
                        "tags": list(ev.tags),
                    }
                )
            _print_json({"total": result.total, "filters": result.filters_applied, "events": events_out})
        else:
            print(f"\nEvents ({result.total} found):")
            print("-" * 60)
            for ev in result.events:
                ok = "[ok]" if ev.success is True else "[fail]" if ev.success is False else "    "
                agent_str = ev.agent_name or "-"
                proj_str = ev.project or "-"
                desc = (ev.description or "")[:50]
                print(f"  {ok} {ev.timestamp[:19]}  {agent_str:15}  {proj_str:15}  {desc}")
            print()
    except Exception as e:
        _handle_error(e, args.json)


# ------------------------------------------------------------------
# stats
# ------------------------------------------------------------------


def main_stats(argv: "list[str] | None" = None) -> None:
    """Show aggregated statistics."""
    parser = argparse.ArgumentParser(
        prog="cervella-events stats",
        description="Show event store statistics",
    )
    parser.add_argument("--project", default="", help="Scope to a specific project")
    parser.add_argument("--db-path", default=None, help="Explicit database path")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args(argv)

    from cervellaswarm_event_store.database import EventStore

    try:
        with EventStore(db_path=args.db_path) as store:
            stats = store.get_statistics(project=args.project)

        if args.json:
            _print_json(
                {
                    "total_events": stats.total_events,
                    "total_lessons": stats.total_lessons,
                    "total_patterns": stats.total_patterns,
                    "success_count": stats.success_count,
                    "fail_count": stats.fail_count,
                    "success_rate": round(stats.success_rate, 4),
                    "by_agent": [
                        {
                            "agent_name": a.agent_name,
                            "event_count": a.event_count,
                            "success_count": a.success_count,
                            "fail_count": a.fail_count,
                        }
                        for a in stats.by_agent
                    ],
                    "by_project": stats.by_project,
                    "by_event_type": stats.by_event_type,
                    "project_filter": stats.project_filter,
                }
            )
        else:
            scope = f" (project: {stats.project_filter})" if stats.project_filter else ""
            print(f"\nEvent Store Statistics{scope}")
            print("=" * 60)
            print(f"  Events:          {stats.total_events}")
            print(f"  Lessons:         {stats.total_lessons}")
            print(f"  Error patterns:  {stats.total_patterns}")
            print(f"  Success rate:    {stats.success_rate * 100:.1f}%")
            print(f"  Successful:      {stats.success_count}")
            print(f"  Failed:          {stats.fail_count}")
            if stats.by_agent:
                print()
                print("  By Agent:")
                for a in stats.by_agent:
                    rate = a.success_count / a.event_count * 100 if a.event_count > 0 else 0
                    print(f"    {a.agent_name:20}  {a.event_count:5} events  {rate:.0f}% ok")
            if stats.by_project:
                print()
                print("  By Project:")
                for proj, cnt in stats.by_project.items():
                    print(f"    {proj:20}  {cnt:5} events")
            print()
    except Exception as e:
        _handle_error(e, args.json)


# ------------------------------------------------------------------
# lessons
# ------------------------------------------------------------------


def main_lessons(argv: "list[str] | None" = None) -> None:
    """Show relevant lessons from the store."""
    parser = argparse.ArgumentParser(
        prog="cervella-events lessons",
        description="Show relevant lessons from the event store",
    )
    parser.add_argument("--agent", default="", help="Boost lessons relevant to this agent")
    parser.add_argument("--project", default="", help="Boost lessons relevant to this project")
    parser.add_argument("--limit", type=int, default=10, help="Maximum lessons (default: 10)")
    parser.add_argument("--db-path", default=None, help="Explicit database path")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args(argv)

    from cervellaswarm_event_store.database import EventStore

    try:
        with EventStore(db_path=args.db_path) as store:
            lessons = store.get_lessons(agent=args.agent, project=args.project, limit=args.limit)

        if args.json:
            out = []
            for l in lessons:
                out.append(
                    {
                        "id": l.id,
                        "pattern": l.pattern,
                        "problem": l.problem,
                        "solution": l.solution,
                        "severity": l.severity,
                        "confidence": l.confidence,
                        "times_applied": l.times_applied,
                        "project": l.project,
                        "score": l.score,
                    }
                )
            _print_json({"total": len(out), "lessons": out})
        else:
            print(f"\nLessons ({len(lessons)} found):")
            print("-" * 60)
            for i, l in enumerate(lessons, 1):
                print(f"  {i}. [{l.severity.upper()}] score={l.score}  {l.pattern or '(no pattern)'}")
                if l.problem:
                    print(f"     Problem:  {l.problem[:80]}")
                if l.solution:
                    print(f"     Solution: {l.solution[:80]}")
                print(f"     Confidence: {l.confidence:.2f}  Applied: {l.times_applied}")
                print()
    except Exception as e:
        _handle_error(e, args.json)


# ------------------------------------------------------------------
# patterns
# ------------------------------------------------------------------


def main_patterns(argv: "list[str] | None" = None) -> None:
    """Detect and show recurring error patterns."""
    parser = argparse.ArgumentParser(
        prog="cervella-events patterns",
        description="Detect recurring error patterns",
    )
    parser.add_argument("--days", type=int, default=7, help="Analyse last N days (default: 7)")
    parser.add_argument("--min-occurrences", type=int, default=3, help="Minimum cluster size (default: 3)")
    parser.add_argument("--db-path", default=None, help="Explicit database path")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args(argv)

    from cervellaswarm_event_store.database import EventStore

    try:
        with EventStore(db_path=args.db_path) as store:
            patterns = store.detect_patterns(days=args.days, min_occurrences=args.min_occurrences)

        if args.json:
            out = []
            for p in patterns:
                out.append(
                    {
                        "pattern_name": p.pattern_name,
                        "pattern_type": p.pattern_type,
                        "severity": p.severity,
                        "occurrence_count": p.occurrence_count,
                        "first_seen": p.first_seen,
                        "last_seen": p.last_seen,
                        "affected_agents": list(p.affected_agents),
                    }
                )
            _print_json({"total": len(out), "patterns": out})
        else:
            if not patterns:
                print(f"\nNo recurring patterns found in the last {args.days} day(s).")
                return
            print(f"\nError Patterns ({len(patterns)} found, last {args.days} day(s)):")
            print("-" * 60)
            for i, p in enumerate(patterns, 1):
                print(f"  {i}. [{p.severity.upper()}] {p.pattern_name}")
                print(f"     Occurrences: {p.occurrence_count}  Type: {p.pattern_type}")
                if p.affected_agents:
                    print(f"     Agents: {', '.join(p.affected_agents)}")
                print(f"     Last seen: {p.last_seen[:19]}")
                print()
    except Exception as e:
        _handle_error(e, args.json)


# ------------------------------------------------------------------
# usage
# ------------------------------------------------------------------


def main_usage(argv: "list[str] | None" = None) -> None:
    """Show token usage and cost statistics."""
    parser = argparse.ArgumentParser(
        prog="cervella-events usage",
        description="Show token usage and cost statistics",
    )
    parser.add_argument("--project", default="", help="Filter by project")
    parser.add_argument("--model", default="", help="Filter by model")
    parser.add_argument("--today", action="store_true", help="Show only today's usage")
    parser.add_argument("--days", type=int, default=0, help="Limit to last N days")
    parser.add_argument("--db-path", default=None, help="Explicit database path")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args(argv)

    from cervellaswarm_event_store.database import EventStore

    days = 1 if args.today else args.days

    try:
        with EventStore(db_path=args.db_path) as store:
            summary = store.query_usage(
                project=args.project,
                model=args.model,
                days=days,
            )

        if args.json:
            _print_json(
                {
                    "total_sessions": summary.total_sessions,
                    "total_input_tokens": summary.total_input_tokens,
                    "total_output_tokens": summary.total_output_tokens,
                    "total_cache_read_tokens": summary.total_cache_read_tokens,
                    "total_cache_creation_tokens": summary.total_cache_creation_tokens,
                    "total_cost_usd": summary.total_cost_usd,
                    "by_model": summary.by_model,
                    "by_project": summary.by_project,
                }
            )
        else:
            period = "today" if args.today else f"last {days} days" if days else "all time"
            print(f"\nToken Usage ({period})")
            print("=" * 60)
            print(f"  Sessions:       {summary.total_sessions}")

            total_all = (
                summary.total_input_tokens
                + summary.total_output_tokens
                + summary.total_cache_read_tokens
                + summary.total_cache_creation_tokens
            )
            print(f"  Total tokens:   {total_all:,}")
            print(f"  Input tokens:   {summary.total_input_tokens:,}")
            print(f"  Output tokens:  {summary.total_output_tokens:,}")
            print(f"  Cache read:     {summary.total_cache_read_tokens:,}")
            print(f"  Cache write:    {summary.total_cache_creation_tokens:,}")
            print(f"  Cost (est.):    ${summary.total_cost_usd:.4f}")

            if summary.by_model:
                print()
                print("  By Model:")
                for m, data in summary.by_model.items():
                    print(f"    {m:30}  {data['tokens']:>12,} tok  ${data['cost']:.4f}")

            if summary.by_project:
                print()
                print("  By Project:")
                for p, data in summary.by_project.items():
                    print(f"    {p:30}  {data['tokens']:>12,} tok  ${data['cost']:.4f}")
            print()
    except Exception as e:
        _handle_error(e, args.json)


# ------------------------------------------------------------------
# budget
# ------------------------------------------------------------------


def main_budget(argv: "list[str] | None" = None) -> None:
    """Manage budget thresholds and check spend alerts."""
    parser = argparse.ArgumentParser(
        prog="cervella-events budget",
        description="Budget alerts -- set thresholds and check spend",
    )
    parser.add_argument("--set-daily", type=float, metavar="USD", help="Set daily budget (0=disable)")
    parser.add_argument("--set-weekly", type=float, metavar="USD", help="Set weekly budget (0=disable)")
    parser.add_argument("--set-monthly", type=float, metavar="USD", help="Set monthly budget (0=disable)")
    parser.add_argument("--check", action="store_true", help="Check current spend vs thresholds")
    parser.add_argument("--config-path", default=None, help="Override config file path")
    parser.add_argument("--db-path", default=None, help="Explicit database path")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args(argv)

    from pathlib import Path
    from cervellaswarm_event_store.budget import load_config, save_config, check_budget, BudgetConfig

    config_path = Path(args.config_path) if args.config_path else None

    # Set thresholds if any --set-* flag is given
    if any(x is not None for x in [args.set_daily, args.set_weekly, args.set_monthly]):
        current = load_config(config_path)
        new_config = BudgetConfig(
            daily=args.set_daily if args.set_daily is not None else current.daily,
            weekly=args.set_weekly if args.set_weekly is not None else current.weekly,
            monthly=args.set_monthly if args.set_monthly is not None else current.monthly,
        )
        saved_path = save_config(new_config, config_path)
        if args.json:
            _print_json({"status": "saved", "path": str(saved_path), "config": {
                "daily": new_config.daily, "weekly": new_config.weekly, "monthly": new_config.monthly,
            }})
        else:
            print(f"Budget saved to {saved_path}")
            if new_config.daily > 0:
                print(f"  Daily:   ${new_config.daily:.2f}")
            if new_config.weekly > 0:
                print(f"  Weekly:  ${new_config.weekly:.2f}")
            if new_config.monthly > 0:
                print(f"  Monthly: ${new_config.monthly:.2f}")
        return

    # Check or show
    config = load_config(config_path)

    if args.check or True:  # Default action is check
        from cervellaswarm_event_store.database import EventStore

        try:
            with EventStore(db_path=args.db_path) as store:
                daily = store.query_usage(days=1)
                weekly = store.query_usage(days=7)
                monthly = store.query_usage(days=30)

            status = check_budget(
                daily_cost=daily.total_cost_usd,
                weekly_cost=weekly.total_cost_usd,
                monthly_cost=monthly.total_cost_usd,
                config=config,
            )

            if args.json:
                _print_json({
                    "any_over": status.any_over,
                    "alerts": [
                        {"period": a.period, "threshold": a.threshold,
                         "actual": a.actual, "over": a.over, "percent": a.percent}
                        for a in status.alerts
                    ],
                })
            else:
                if not status.alerts:
                    print("No budget thresholds configured.")
                    print("Set with: cervella-events budget --set-daily 500 --set-weekly 3000")
                    return

                print("\nBudget Status")
                print("=" * 50)
                for a in status.alerts:
                    icon = "OVER" if a.over else "OK"
                    bar_len = min(int(a.percent / 5), 20)
                    bar = "#" * bar_len + "." * (20 - bar_len)
                    print(f"  {a.period:8} [{bar}] {a.percent:5.1f}%  ${a.actual:.2f} / ${a.threshold:.2f}  [{icon}]")

                if status.any_over:
                    print("\n  WARNING: Budget exceeded!")
                print()

        except Exception as e:
            _handle_error(e, args.json)


# ------------------------------------------------------------------
# Main dispatcher
# ------------------------------------------------------------------


def main(argv: "list[str] | None" = None) -> None:
    """Main entry point dispatching to subcommands."""
    parser = argparse.ArgumentParser(
        prog="cervella-events",
        description="CervellaSwarm Event Store - SQLite event tracking for AI agents",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"cervella-events {_get_version()}",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    subparsers.add_parser("init", help="Initialize the event store database")
    subparsers.add_parser("log", help="Log an event")
    subparsers.add_parser("query", help="Query events")
    subparsers.add_parser("stats", help="Show statistics")
    subparsers.add_parser("lessons", help="Show relevant lessons")
    subparsers.add_parser("patterns", help="Detect error patterns")
    subparsers.add_parser("usage", help="Show token usage and cost")
    subparsers.add_parser("budget", help="Budget alerts and thresholds")

    args, remaining = parser.parse_known_args(argv)

    commands = {
        "init": main_init,
        "log": main_log,
        "query": main_query,
        "stats": main_stats,
        "lessons": main_lessons,
        "patterns": main_patterns,
        "usage": main_usage,
        "budget": main_budget,
    }

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    handler = commands.get(args.command)
    if handler:
        handler(remaining)
    else:
        parser.print_help()
        sys.exit(1)
