# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""CLI for CervellaSwarm Agent Templates.

Usage:
    cervella-agent init <type> [--name NAME] [--team TEAM] [--specialty SPEC] [--output DIR]
    cervella-agent init-team <preset> [--name TEAM] [--output DIR]
    cervella-agent list
    cervella-agent validate <file> [<file> ...]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from cervellaswarm_agent_templates import __version__
from cervellaswarm_agent_templates.scaffold import (
    TEAM_PRESETS,
    TEMPLATE_TYPES,
    WORKER_SPECIALTIES,
    create_agent,
    create_shared_dna,
    create_team,
    create_team_config,
    list_templates,
)
from cervellaswarm_agent_templates.validator import validate_agent


def _cmd_init(args: argparse.Namespace) -> int:
    """Handle the 'init' command - create a single agent."""
    try:
        path = create_agent(
            agent_type=args.type,
            name=args.name,
            output_dir=args.output,
            team_name=args.team,
            specialty=args.specialty,
        )
        print(f"Created: {path}")

        # Also create shared DNA if it doesn't exist
        dna_path = Path(args.output) / "_shared_dna.md"
        if not dna_path.exists():
            dna = create_shared_dna(args.output, args.team)
            print(f"Created: {dna}")

        return 0
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def _cmd_init_team(args: argparse.Namespace) -> int:
    """Handle the 'init-team' command - create a complete team."""
    try:
        files = create_team(
            preset=args.preset,
            output_dir=args.output,
            team_name=args.name,
        )
        print(f"Created {len(files)} files in {args.output}/:")
        for f in files:
            print(f"  {f.name}")
        return 0
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def _cmd_list(args: argparse.Namespace) -> int:
    """Handle the 'list' command - show available templates."""
    info = list_templates()

    print("Agent Types:")
    for key, display in info["types"].items():
        print(f"  {key:20s} {display}")

    print("\nWorker Specialties:")
    for key, desc in info["specialties"].items():
        print(f"  {key:20s} {desc}")

    print("\nTeam Presets:")
    for key, desc in info["team_presets"].items():
        print(f"  {key:20s} {desc}")

    return 0


def _cmd_validate(args: argparse.Namespace) -> int:
    """Handle the 'validate' command - check agent files."""
    all_valid = True

    for filepath in args.files:
        result = validate_agent(filepath)
        status = "VALID" if result.valid else "INVALID"
        print(f"\n{filepath}: {status}")

        if result.frontmatter:
            name = result.frontmatter.get("name", "unknown")
            model = result.frontmatter.get("model", "unknown")
            role = result.frontmatter.get("role", "-")
            print(f"  name={name}  model={model}  role={role}")

        for issue in result.issues:
            prefix = {"error": "ERROR", "warning": "WARN", "info": "INFO"}[
                issue.level
            ]
            print(f"  [{prefix}] {issue.field}: {issue.message}")

        if not result.valid:
            all_valid = False

    return 0 if all_valid else 1


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser."""
    parser = argparse.ArgumentParser(
        prog="cervella-agent",
        description="CervellaSwarm Agent Templates - scaffold and validate agent definitions",
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # init
    init_parser = subparsers.add_parser(
        "init", help="Create a single agent from a template"
    )
    init_parser.add_argument(
        "type",
        choices=sorted(TEMPLATE_TYPES),
        help="Agent type to create",
    )
    init_parser.add_argument(
        "--name", "-n", default=None, help="Agent name (default: type name)"
    )
    init_parser.add_argument(
        "--team", "-t", default="my-team", help="Team name (default: my-team)"
    )
    init_parser.add_argument(
        "--specialty",
        "-s",
        default="generic",
        choices=sorted(WORKER_SPECIALTIES),
        help="Worker specialty (only for worker type, default: generic)",
    )
    init_parser.add_argument(
        "--output", "-o", default=".", help="Output directory (default: current)"
    )

    # init-team
    team_parser = subparsers.add_parser(
        "init-team", help="Create a complete team from a preset"
    )
    team_parser.add_argument(
        "preset",
        choices=sorted(TEAM_PRESETS),
        help="Team preset to use",
    )
    team_parser.add_argument(
        "--name", "-n", default="my-team", help="Team name (default: my-team)"
    )
    team_parser.add_argument(
        "--output", "-o", default=".", help="Output directory (default: current)"
    )

    # list
    subparsers.add_parser("list", help="List available templates and specialties")

    # validate
    validate_parser = subparsers.add_parser(
        "validate", help="Validate agent definition files"
    )
    validate_parser.add_argument(
        "files", nargs="+", help="Agent files to validate (.md)"
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    """CLI entry point."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        return 0

    handlers = {
        "init": _cmd_init,
        "init-team": _cmd_init_team,
        "list": _cmd_list,
        "validate": _cmd_validate,
    }

    return handlers[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
