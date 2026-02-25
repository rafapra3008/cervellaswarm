# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""
CLI for cervellaswarm-quality-gates.

Usage:
    cervella-check quality <file>         Score content quality
    cervella-check hooks <directory>      Validate hooks
    cervella-check sync <source> <target> Compare agent directories
    cervella-check all --project-dir .    Run all checks

Options:
    --json          Output as JSON
    --verbose       Show detailed output
    --min-score N   Minimum quality score (default: 7.0)
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from cervellaswarm_quality_gates.config import load_config, get_section
from cervellaswarm_quality_gates.hooks import validate_hooks, hooks_summary
from cervellaswarm_quality_gates.quality import score_content, score_file
from cervellaswarm_quality_gates.sync import compare_agents


def _cmd_quality(args: argparse.Namespace) -> int:
    """Score content quality of a file."""
    config = load_config()
    quality_cfg = get_section("quality", config)
    weights = quality_cfg.get("weights")
    min_score = args.min_score or quality_cfg.get("min_score", 7.0)

    try:
        result = score_file(args.file, weights=weights)
    except FileNotFoundError:
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        return 1
    except OSError as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        return 1

    if args.json:
        data = {
            "file": args.file,
            "actionability": result.actionability,
            "specificity": result.specificity,
            "freshness": result.freshness,
            "conciseness": result.conciseness,
            "total": round(result.total, 2),
            "passes": result.passes(min_score),
            "min_score": min_score,
        }
        print(json.dumps(data, indent=2))
    else:
        print(f"Quality Score: {args.file}")
        print(f"  Actionability: {result.actionability:.1f}/10 (30%)")
        print(f"  Specificity:   {result.specificity:.1f}/10 (30%)")
        print(f"  Freshness:     {result.freshness:.1f}/10 (20%)")
        print(f"  Conciseness:   {result.conciseness:.1f}/10 (20%)")
        print(f"  Total:         {result.total:.1f}/10")
        status = "PASS" if result.passes(min_score) else "FAIL"
        print(f"  Status:        {status} (min: {min_score:.1f})")

    return 0 if result.passes(min_score) else 1


def _cmd_hooks(args: argparse.Namespace) -> int:
    """Validate hook files."""
    config = load_config()
    hooks_cfg = get_section("hooks", config)
    required = hooks_cfg.get("required_hooks", [])

    reports = validate_hooks(args.directory, required_hooks=required)

    if args.json:
        data = {
            "directory": args.directory,
            "hooks": [
                {
                    "name": r.name,
                    "path": r.path,
                    "status": r.status.value,
                    "issues": list(r.issues),
                    "healthy": r.is_healthy,
                }
                for r in reports
            ],
            "summary": hooks_summary(reports),
        }
        print(json.dumps(data, indent=2))
    else:
        print(f"Hook Validation: {args.directory}")
        if not reports:
            print("  No hooks found.")
        for r in reports:
            marker = "OK" if r.is_healthy else r.status.value
            print(f"  [{marker}] {r.name}")
            if args.verbose and r.issues:
                for issue in r.issues:
                    print(f"       - {issue}")

        summary = hooks_summary(reports)
        print(f"  Summary: {summary}")

    unhealthy = sum(1 for r in reports if not r.is_healthy)
    return 1 if unhealthy > 0 else 0


def _cmd_sync(args: argparse.Namespace) -> int:
    """Compare agent directories."""
    config = load_config()
    sync_cfg = get_section("sync", config)
    ignore = sync_cfg.get("ignore_patterns", [])

    result = compare_agents(args.source, args.target, ignore_patterns=ignore)

    if args.json:
        data = {
            "source": result.source_dir,
            "target": result.target_dir,
            "is_synced": result.is_synced,
            "only_in_source": list(result.only_in_source),
            "only_in_target": list(result.only_in_target),
            "different": list(result.different),
            "identical": list(result.identical),
            "total_files": result.total_files,
        }
        if args.verbose:
            data["diffs"] = [
                {
                    "name": d.name,
                    "action": d.action.value,
                    "reason": d.reason,
                }
                for d in result.diffs
            ]
        print(json.dumps(data, indent=2))
    else:
        status = "IN SYNC" if result.is_synced else "OUT OF SYNC"
        print(f"Agent Sync: {status}")
        print(f"  Source: {result.source_dir}")
        print(f"  Target: {result.target_dir}")
        print(f"  Identical: {len(result.identical)}")
        if result.only_in_source:
            print(f"  Only in source: {', '.join(result.only_in_source)}")
        if result.only_in_target:
            print(f"  Only in target: {', '.join(result.only_in_target)}")
        if result.different:
            print(f"  Different: {', '.join(result.different)}")

    return 0 if result.is_synced else 1


def _cmd_all(args: argparse.Namespace) -> int:
    """Run all checks on a project directory."""
    project_dir = Path(args.project_dir)
    config = load_config()
    exit_code = 0
    results: dict = {}

    # Quality check on common session files
    quality_cfg = get_section("quality", config)
    min_score = args.min_score or quality_cfg.get("min_score", 7.0)
    weights = quality_cfg.get("weights")

    quality_files = []
    seen: set[Path] = set()
    for md_file in project_dir.glob("**/*.md"):
        if md_file in seen:
            continue
        name = md_file.name.upper()
        if any(kw in name for kw in ("PROMPT_RIPRESA", "NORD", "SESSION", "STATE")):
            quality_files.append(md_file)
            seen.add(md_file)

    quality_results = []
    for qf in quality_files[:10]:  # limit to 10 files
        try:
            score = score_file(str(qf), weights=weights)
            quality_results.append({
                "file": str(qf.relative_to(project_dir)),
                "total": round(score.total, 2),
                "passes": score.passes(min_score),
            })
            if not score.passes(min_score):
                exit_code = 1
        except OSError:
            pass

    results["quality"] = {"files": quality_results, "min_score": min_score}

    # Hook validation
    hooks_cfg = get_section("hooks", config)
    hooks_dir_str = hooks_cfg.get("directory", ".claude/hooks/")
    hooks_dir = project_dir / hooks_dir_str
    required = hooks_cfg.get("required_hooks", [])

    if hooks_dir.is_dir():
        reports = validate_hooks(str(hooks_dir), required_hooks=required)
        summary = hooks_summary(reports)
        results["hooks"] = {
            "directory": str(hooks_dir),
            "summary": summary,
            "total": len(reports),
        }
        if any(not r.is_healthy for r in reports):
            exit_code = 1
    else:
        results["hooks"] = {"directory": str(hooks_dir), "summary": {}, "total": 0}

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print("=== Quality Gates: All Checks ===")
        print(f"\nProject: {project_dir}")

        print(f"\n--- Quality ({len(quality_results)} files) ---")
        for qr in quality_results:
            status = "PASS" if qr["passes"] else "FAIL"
            print(f"  [{status}] {qr['file']}: {qr['total']}/10")

        print(f"\n--- Hooks ---")
        hooks_info = results["hooks"]
        if hooks_info["total"] > 0:
            for status_name, count in hooks_info["summary"].items():
                print(f"  {status_name}: {count}")
        else:
            print("  No hooks directory found")

        print(f"\nExit code: {exit_code}")

    return exit_code


def _build_parser() -> argparse.ArgumentParser:
    """Build the argument parser."""
    parser = argparse.ArgumentParser(
        prog="cervella-check",
        description="Quality gates for AI agent swarms",
    )
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--verbose", action="store_true", help="Detailed output")

    subparsers = parser.add_subparsers(dest="command", help="Subcommand")

    # quality
    p_quality = subparsers.add_parser("quality", help="Score content quality")
    p_quality.add_argument("file", help="Path to file to score")
    p_quality.add_argument("--min-score", type=float, help="Minimum passing score")

    # hooks
    p_hooks = subparsers.add_parser("hooks", help="Validate hook files")
    p_hooks.add_argument("directory", help="Path to hooks directory")

    # sync
    p_sync = subparsers.add_parser("sync", help="Compare agent directories")
    p_sync.add_argument("source", help="Source agent directory")
    p_sync.add_argument("target", help="Target agent directory")

    # all
    p_all = subparsers.add_parser("all", help="Run all checks")
    p_all.add_argument("--project-dir", default=".", help="Project root directory")
    p_all.add_argument("--min-score", type=float, help="Minimum passing score")

    return parser


def main(argv: list[str] | None = None) -> int:
    """Main entry point for cervella-check CLI."""
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        return 0

    handlers = {
        "quality": _cmd_quality,
        "hooks": _cmd_hooks,
        "sync": _cmd_sync,
        "all": _cmd_all,
    }

    handler = handlers.get(args.command)
    if handler is None:
        parser.print_help()
        return 1

    return handler(args)


if __name__ == "__main__":
    sys.exit(main())
