# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""
CLI entry points for CervellaSwarm Task Orchestration.

Provides individual commands and a unified ``cervella-orchestrate`` CLI
that dispatches to classify, route, validate-plan, validate-output, and task
subcommands.
"""

import argparse
import json
import sys
from pathlib import Path

from cervellaswarm_task_orchestration import __version__
from cervellaswarm_task_orchestration.task_classifier import classify_task
from cervellaswarm_task_orchestration.architect_flow import (
    route_task,
    validate_plan_file,
)
from cervellaswarm_task_orchestration.task_manager import (
    create_task,
    list_tasks,
    mark_ready,
    mark_working,
    mark_done,
    ack_received,
    ack_understood,
    get_task_status,
    get_ack_status,
    cleanup_task,
)
from cervellaswarm_task_orchestration.output_validator import (
    validate_output,
    find_last_output,
    find_task_output,
)


# -------------------------------------------------------------------------
# cervella-classify
# -------------------------------------------------------------------------


def main_classify(argv: list[str] | None = None) -> None:
    """CLI: classify a task description."""
    parser = argparse.ArgumentParser(
        prog="cervella-classify",
        description="Classify task complexity (simple/medium/complex/critical).",
    )
    parser.add_argument("description", nargs="+", help="Task description")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    args = parser.parse_args(argv)

    task = " ".join(args.description)
    result = classify_task(task)

    if args.json:
        print(
            json.dumps(
                {
                    "complexity": result.complexity.value,
                    "should_architect": result.should_architect,
                    "confidence": round(result.confidence, 3),
                    "triggers": result.triggers,
                    "reasoning": result.reasoning,
                }
            )
        )
    else:
        print(f"\nTask: {task}")
        print("=" * 60)
        print(f"Complexity:       {result.complexity.value}")
        print(f"Should Architect: {result.should_architect}")
        print(f"Confidence:       {result.confidence:.2f}")
        print(f"Triggers:         {', '.join(result.triggers)}")
        print(f"Reasoning:        {result.reasoning}")


# -------------------------------------------------------------------------
# cervella-route
# -------------------------------------------------------------------------


def main_route(argv: list[str] | None = None) -> None:
    """CLI: route a task to architect or workers."""
    parser = argparse.ArgumentParser(
        prog="cervella-route",
        description="Route a task: architect planning or direct to workers.",
    )
    parser.add_argument("description", nargs="+", help="Task description")
    parser.add_argument("--force-architect", action="store_true", help="Force architect")
    parser.add_argument("--force-direct", action="store_true", help="Force direct to workers")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    args = parser.parse_args(argv)

    task = " ".join(args.description)
    decision = route_task(
        task,
        force_architect=args.force_architect,
        force_direct=args.force_direct,
    )

    if args.json:
        print(
            json.dumps(
                {
                    "use_architect": decision.use_architect,
                    "complexity": decision.classification.complexity.value,
                    "confidence": round(decision.classification.confidence, 3),
                    "reason": decision.reason,
                    "suggested_workers": [w.value for w in decision.suggested_workers],
                }
            )
        )
    else:
        print(f"\nTask: {task}")
        print("=" * 60)
        print(f"Use Architect:     {decision.use_architect}")
        print(f"Complexity:        {decision.classification.complexity.value}")
        print(f"Confidence:        {decision.classification.confidence:.2f}")
        print(f"Reason:            {decision.reason}")
        if decision.suggested_workers:
            workers = [w.value for w in decision.suggested_workers]
            print(f"Suggested Workers: {', '.join(workers)}")


# -------------------------------------------------------------------------
# cervella-validate-plan
# -------------------------------------------------------------------------


def main_validate_plan(argv: list[str] | None = None) -> None:
    """CLI: validate an architect plan file."""
    parser = argparse.ArgumentParser(
        prog="cervella-validate-plan",
        description="Validate an architect-generated plan file.",
    )
    parser.add_argument("plan_file", help="Path to plan.md file")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    args = parser.parse_args(argv)

    result = validate_plan_file(Path(args.plan_file))

    if args.json:
        print(
            json.dumps(
                {
                    "valid": result.is_valid,
                    "score": round(result.score, 1),
                    "errors": result.errors,
                    "warnings": result.warnings,
                }
            )
        )
    else:
        print(f"\nValidating: {args.plan_file}")
        print("=" * 60)
        print(f"Valid:    {result.is_valid}")
        print(f"Score:    {result.score:.1f}/10")
        if result.errors:
            print("\nErrors:")
            for e in result.errors:
                print(f"  - {e}")
        if result.warnings:
            print("\nWarnings:")
            for w in result.warnings:
                print(f"  - {w}")


# -------------------------------------------------------------------------
# cervella-validate-output
# -------------------------------------------------------------------------


def main_validate_output(argv: list[str] | None = None) -> None:
    """CLI: validate worker output."""
    parser = argparse.ArgumentParser(
        prog="cervella-validate-output",
        description="Validate worker output files for quality and completeness.",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--last-output", action="store_true", help="Validate last output")
    group.add_argument("--file", type=str, help="Validate specific file")
    group.add_argument("--task", type=str, help="Validate output of a task (e.g., TASK_001)")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    args = parser.parse_args(argv)

    output_file = None

    if args.last_output:
        output_file = find_last_output()
        if not output_file:
            print("ERROR: No output found!", file=sys.stderr)
            sys.exit(2)
    elif args.file:
        output_file = Path(args.file)
    elif args.task:
        output_file = find_task_output(args.task)
        if not output_file:
            print(f"ERROR: Output not found for task {args.task}", file=sys.stderr)
            sys.exit(2)

    result = validate_output(output_file)

    if args.json:
        print(
            json.dumps(
                {
                    "valid": result.valid,
                    "score": result.score,
                    "errors": result.errors,
                    "warnings": result.warnings,
                    "retry_needed": result.retry_needed,
                    "retry_context": result.retry_context,
                }
            )
        )
    else:
        status = "VALID" if result.valid else "INVALID"
        print(f"\n{status} - {output_file.name}")
        print(f"Score: {result.score}/100")
        if result.errors:
            print("\nErrors:")
            for e in result.errors:
                print(f"  - {e}")
        if result.warnings:
            print("\nWarnings:")
            for w in result.warnings:
                print(f"  - {w}")
        if result.retry_needed:
            print(f"\nRETRY SUGGESTED")
            if result.retry_context:
                print(f"Context: {result.retry_context}")

    sys.exit(0 if result.valid else 1)


# -------------------------------------------------------------------------
# cervella-task
# -------------------------------------------------------------------------


def main_task(argv: list[str] | None = None) -> None:
    """CLI: manage tasks (create, list, status, transitions)."""
    parser = argparse.ArgumentParser(
        prog="cervella-task",
        description="File-based task management for multi-agent systems.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="command", help="Command")

    # list
    sub.add_parser("list", help="List all tasks")

    # create
    p_create = sub.add_parser("create", help="Create a new task")
    p_create.add_argument("task_id", help="Task ID (e.g., TASK_001)")
    p_create.add_argument("agent", help="Assigned agent name")
    p_create.add_argument("description", help="Task description")
    p_create.add_argument("--risk", type=int, default=1, choices=[1, 2, 3], help="Risk level")

    # status transitions
    for cmd in ["ready", "working", "done", "ack-received", "ack-understood", "status", "cleanup"]:
        p = sub.add_parser(cmd, help=f"Mark task as {cmd}")
        p.add_argument("task_id", help="Task ID")

    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        sys.exit(0)

    if args.command == "list":
        tasks = list_tasks()
        if not tasks:
            print("No tasks found.")
        else:
            print(f"{'TASK_ID':<12} {'STATUS':<10} {'ACK':<7} {'AGENT':<25} {'FILE'}")
            print("-" * 90)
            for t in tasks:
                print(f"{t['task_id']:<12} {t['status']:<10} {t['ack']:<7} {t['agent']:<25} {t['file']}")

    elif args.command == "create":
        try:
            path = create_task(args.task_id, args.agent, args.description, args.risk)
            print(f"Task created: {path}")
        except (ValueError, FileExistsError) as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.command in ("ready", "working", "done", "ack-received", "ack-understood", "status", "cleanup"):
        tid = args.task_id
        if args.command == "ready":
            ok = mark_ready(tid)
            if ok:
                print(f"Task {tid} marked as READY")
            else:
                print(f"ERROR: Failed to mark {tid} as READY (invalid ID or task not found)", file=sys.stderr)
                sys.exit(1)
        elif args.command == "working":
            ok = mark_working(tid)
            if ok:
                print(f"Task {tid} marked as WORKING")
            else:
                print(f"ERROR: Failed to mark {tid} as WORKING (invalid ID, not found, or already claimed)", file=sys.stderr)
                sys.exit(1)
        elif args.command == "done":
            ok = mark_done(tid)
            if ok:
                print(f"Task {tid} marked as DONE")
            else:
                print(f"ERROR: Failed to mark {tid} as DONE (invalid ID or task not found)", file=sys.stderr)
                sys.exit(1)
        elif args.command == "ack-received":
            ok = ack_received(tid)
            if ok:
                print(f"Task {tid} - ACK_RECEIVED confirmed")
            else:
                print(f"ERROR: Failed to ACK_RECEIVED {tid} (invalid ID or task not found)", file=sys.stderr)
                sys.exit(1)
        elif args.command == "ack-understood":
            ok = ack_understood(tid)
            if ok:
                print(f"Task {tid} - ACK_UNDERSTOOD confirmed")
            else:
                print(f"ERROR: Failed to ACK_UNDERSTOOD {tid} (invalid ID or task not found)", file=sys.stderr)
                sys.exit(1)
        elif args.command == "status":
            st = get_task_status(tid)
            ack = get_ack_status(tid)
            print(f"Task {tid}:")
            print(f"  Status: {st.upper()}")
            print(f"  ACK: {ack} (R=Received, U=Understood, D=Done)")
        elif args.command == "cleanup":
            ok = cleanup_task(tid)
            if ok:
                print(f"Marker files for {tid} removed")


# -------------------------------------------------------------------------
# cervella-orchestrate (unified)
# -------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> None:
    """Unified CLI dispatching to all orchestration subcommands."""
    parser = argparse.ArgumentParser(
        prog="cervella-orchestrate",
        description="CervellaSwarm Task Orchestration - classify, route, validate, manage tasks.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="command", help="Subcommand")

    sub.add_parser("classify", help="Classify task complexity")
    sub.add_parser("route", help="Route task to architect or workers")
    sub.add_parser("validate-plan", help="Validate architect plan")
    sub.add_parser("validate-output", help="Validate worker output")
    sub.add_parser("task", help="Manage tasks")

    args, remaining = parser.parse_known_args(argv)

    if not args.command:
        parser.print_help()
        sys.exit(0)

    dispatch = {
        "classify": main_classify,
        "route": main_route,
        "validate-plan": main_validate_plan,
        "validate-output": main_validate_output,
        "task": main_task,
    }

    dispatch[args.command](remaining)
