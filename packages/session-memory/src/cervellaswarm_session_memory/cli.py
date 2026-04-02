# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""
CLI for CervellaSwarm Session Memory.

Provides commands for initializing, checking, auditing, and syncing
session memory across projects.

Usage:
    cervella-session init my-project
    cervella-session check [project] [--json]
    cervella-session audit [path] [--json]
    cervella-session sync [project] [--json]
    cervella-session list [--json]
"""

import argparse
import json
import sys
from pathlib import Path

import importlib.metadata


def _get_version() -> str:
    """Get package version from metadata."""
    try:
        return importlib.metadata.version("cervellaswarm-session-memory")
    except importlib.metadata.PackageNotFoundError:
        return "0.1.0"


def main_init(argv: list[str] | None = None) -> None:
    """Initialize a new project with session memory structure."""
    from cervellaswarm_session_memory.project_manager import init_project

    parser = argparse.ArgumentParser(
        prog="cervella-session init",
        description="Initialize session memory for a project",
    )
    parser.add_argument("name", help="Project name")
    parser.add_argument(
        "--project-root",
        type=Path,
        default=None,
        help="Project root directory (default: current directory)",
    )
    parser.add_argument(
        "--memory-dir",
        default=None,
        help="Memory directory name (default: .session-memory)",
    )
    parser.add_argument(
        "--session",
        type=int,
        default=1,
        help="Starting session number (default: 1)",
    )
    parser.add_argument(
        "--description",
        default="",
        help="Project description for compass file",
    )
    parser.add_argument(
        "--no-compass",
        action="store_true",
        help="Skip creating PROJECT_COMPASS.md",
    )
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args(argv)

    try:
        project = init_project(
            name=args.name,
            project_root=args.project_root,
            memory_dir=args.memory_dir,
            session_number=args.session,
            description=args.description,
            create_compass=not args.no_compass,
        )
    except FileExistsError as e:
        if args.json:
            print(json.dumps({"error": str(e)}))
        else:
            print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(
            json.dumps(
                {
                    "project": project.name,
                    "state_file": str(project.state_file),
                    "compass_file": str(project.compass_file) if project.compass_file else None,
                    "memory_dir": str(project.memory_dir),
                }
            )
        )
    else:
        print(f"Initialized session memory for '{project.name}'")
        print(f"  State file: {project.state_file}")
        if project.compass_file:
            print(f"  Compass:    {project.compass_file}")
        print(f"  Archive:    {project.archive_dir}")


def main_check(argv: list[str] | None = None) -> None:
    """Run quality checks on session state files."""
    from cervellaswarm_session_memory.project_manager import discover_projects, get_project
    from cervellaswarm_session_memory.quality_checker import check_quality

    parser = argparse.ArgumentParser(
        prog="cervella-session check",
        description="Check quality of session state files",
    )
    parser.add_argument("project", nargs="?", help="Project name (default: all)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args(argv)

    if args.project:
        project = get_project(args.project)
        if project is None:
            if args.json:
                print(json.dumps({"error": f"Project '{args.project}' not found"}))
            else:
                print(f"Error: Project '{args.project}' not found", file=sys.stderr)
            sys.exit(1)
        results = [check_quality(project.state_file, project.name)]
    else:
        projects = discover_projects()
        if not projects:
            if args.json:
                print(json.dumps([]))
            else:
                print("No projects found. Run 'cervella-session init <name>' first.")
            return
        results = [check_quality(p.state_file, p.name) for p in projects]

    if args.json:
        output = []
        for r in results:
            output.append(
                {
                    "project": r.project,
                    "file": r.file,
                    "lines": r.lines,
                    "updated": r.updated,
                    "scores": r.scores,
                    "total": r.total,
                    "status": r.status,
                    "warnings": r.warnings,
                    "suggestions": r.suggestions,
                }
            )
        print(json.dumps(output, indent=2))
    else:
        print()
        print("=" * 60)
        print("Session Memory - Quality Check")
        print("=" * 60)

        for r in results:
            print()
            status_marker = {"EXCELLENT": "[+]", "PASS": "[+]", "NEEDS_IMPROVEMENT": "[!]", "FAIL": "[-]"}
            marker = status_marker.get(r.status, "[?]")
            print(f"{marker} {r.project.upper()}")
            print(f"    File: {r.file}")
            print(f"    Lines: {r.lines} | Updated: {r.updated}")
            if r.scores:
                print("    Scores:")
                print(f"      Actionability:  {r.scores.get('actionability', 0)}/10  (30%)")
                print(f"      Specificity:    {r.scores.get('specificity', 0)}/10  (30%)")
                print(f"      Freshness:      {r.scores.get('freshness', 0)}/10  (20%)")
                print(f"      Conciseness:    {r.scores.get('conciseness', 0)}/10  (20%)")
                print(f"    TOTAL: {r.total}/10 [{r.status}]")
            if r.suggestions:
                print("    Suggestions:")
                for s in r.suggestions:
                    print(f"      - {s}")

        if len(results) > 1:
            avg = sum(r.total for r in results) / len(results)
            print()
            print("=" * 60)
            print(f"AVERAGE SCORE: {avg:.1f}/10")
            print("=" * 60)
        print()


def main_audit(argv: list[str] | None = None) -> None:
    """Scan files for accidentally committed secrets."""
    from cervellaswarm_session_memory.secret_auditor import audit_directory

    parser = argparse.ArgumentParser(
        prog="cervella-session audit",
        description="Scan for secrets in session memory files",
    )
    parser.add_argument(
        "path",
        nargs="?",
        type=Path,
        default=Path("."),
        help="Directory to scan (default: current directory)",
    )
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args(argv)

    result = audit_directory(args.path)

    if args.json:
        findings = [
            {
                "severity": f.severity.value,
                "pattern": f.pattern_name,
                "file": f.file,
                "line": f.line_number,
            }
            for f in result.findings
        ]
        print(
            json.dumps(
                {
                    "scanned_files": result.scanned_files,
                    "critical": result.critical_count,
                    "high": result.high_count,
                    "clean": result.clean,
                    "findings": findings,
                }
            )
        )
    else:
        print()
        print("=" * 60)
        print("Session Memory - Secret Audit")
        print("=" * 60)
        print(f"Scanned: {result.scanned_files} files in {args.path}")
        print()

        if result.findings:
            for f in result.findings:
                marker = "[CRITICAL]" if f.severity == f.severity.CRITICAL else "[HIGH]"
                print(f"  {marker} {f.pattern_name}")
                print(f"    File: {f.file}")
                print(f"    Line: {f.line_number}")
                print()

        print(f"CRITICAL: {result.critical_count}")
        print(f"HIGH:     {result.high_count}")
        print()

        if result.clean:
            print("No secrets found. Files are clean.")
        else:
            print("ACTION REQUIRED!")
            print("  1. Remove secrets from files")
            print("  2. Store in .env file")
            print("  3. Replace with: [stored in .env as VAR_NAME]")

        print()

    sys.exit(0 if result.clean else 1)


def main_sync(argv: list[str] | None = None) -> None:
    """Verify session memory freshness and coherence."""
    from cervellaswarm_session_memory.sync_checker import verify_project, verify_all

    parser = argparse.ArgumentParser(
        prog="cervella-session sync",
        description="Verify session memory sync status",
    )
    parser.add_argument("project", nargs="?", help="Project name (default: all)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args(argv)

    if args.project:
        results = [verify_project(args.project)]
    else:
        results = verify_all()
        if not results:
            if args.json:
                print(json.dumps([]))
            else:
                print("No projects found. Run 'cervella-session init <name>' first.")
            return

    if args.json:
        output = []
        for r in results:
            output.append(
                {
                    "project": r.project,
                    "overall": r.overall.value,
                    "checks": {k: v.value for k, v in r.checks.items()},
                    "warnings": r.warnings,
                    "errors": r.errors,
                }
            )
        print(json.dumps(output, indent=2))
    else:
        print()
        print("=" * 60)
        print("Session Memory - Sync Status")
        print("=" * 60)

        for r in results:
            overall = r.overall
            marker = {"ok": "[+]", "warning": "[!]", "error": "[-]"}
            print(f"\n{marker.get(overall.value, '[?]')} {r.project.upper()} ({overall.value})")

            for check_name, status in r.checks.items():
                icon = {"ok": "+", "warning": "!", "error": "-"}
                print(f"    [{icon.get(status.value, '?')}] {check_name}")

            if r.warnings:
                for w in r.warnings:
                    print(f"    ! {w}")
            if r.errors:
                for e in r.errors:
                    print(f"    - {e}")

        print()


def main_list(argv: list[str] | None = None) -> None:
    """List all discovered projects."""
    from cervellaswarm_session_memory.project_manager import discover_projects

    parser = argparse.ArgumentParser(
        prog="cervella-session list",
        description="List discovered session memory projects",
    )
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args(argv)

    projects = discover_projects()

    if args.json:
        output = [
            {
                "name": p.name,
                "state_file": str(p.state_file),
                "compass_file": str(p.compass_file) if p.compass_file else None,
                "memory_dir": str(p.memory_dir),
            }
            for p in projects
        ]
        print(json.dumps(output, indent=2))
    else:
        if not projects:
            print("No projects found. Run 'cervella-session init <name>' first.")
            return

        print(f"\nDiscovered {len(projects)} project(s):\n")
        for p in projects:
            print(f"  {p.name}")
            print(f"    State: {p.state_file}")
            if p.compass_file:
                print(f"    Compass: {p.compass_file}")
        print()


def main(argv: list[str] | None = None) -> None:
    """Main entry point dispatching to subcommands."""
    parser = argparse.ArgumentParser(
        prog="cervella-session",
        description="CervellaSwarm Session Memory - Git-native session continuity",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"cervella-session {_get_version()}",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    subparsers.add_parser("init", help="Initialize a new project")
    subparsers.add_parser("check", help="Quality check session state files")
    subparsers.add_parser("audit", help="Scan for secrets")
    subparsers.add_parser("sync", help="Verify sync status")
    subparsers.add_parser("list", help="List discovered projects")

    args, remaining = parser.parse_known_args(argv)

    commands = {
        "init": main_init,
        "check": main_check,
        "audit": main_audit,
        "sync": main_sync,
        "list": main_list,
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
