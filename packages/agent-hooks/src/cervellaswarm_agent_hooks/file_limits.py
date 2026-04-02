# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""
File Limits Guard - SessionEnd Hook for Claude Code.

Checks file sizes and counts at session end to prevent bloat.
Configurable via hooks.yaml (pattern, max_lines, max_count).

Usage in Claude Code settings.json:
    "SessionEnd": [{
        "matcher": "",
        "hooks": [{"type": "command", "command": "cervella-file-limits"}]
    }]
"""

import glob
import json
import os
import sys
from pathlib import Path

from .config import get_hook_config

__version__ = "1.0.0"


def count_lines(file_path: Path) -> int:
    """Count lines in a file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return sum(1 for _ in f)
    except Exception as e:
        print(f"file_limits: failed to count lines in {file_path}: {e}", file=sys.stderr)
        return 0


def find_project_root(cwd: str) -> Path:
    """Find project root by walking up to the nearest .git directory."""
    current = Path(cwd)
    for parent in [current, *current.parents]:
        if (parent / ".git").exists():
            return parent
    return current


def check_limits(cwd: str) -> list[dict]:
    """Check all configured limits and return violations."""
    config = get_hook_config("file_limits")
    checks = config.get("checks", [])
    project_root = find_project_root(cwd)
    violations = []

    for check in checks:
        pattern = check.get("pattern", "")
        name = check.get("name", pattern)
        max_lines = check.get("max_lines")
        max_count = check.get("max_count")
        action = check.get("action", "Review and clean up")

        # Resolve pattern relative to project root
        full_pattern = str(project_root / pattern)
        matches = glob.glob(full_pattern, recursive=True)

        if max_count is not None and len(matches) > max_count:
            violations.append({
                "file": pattern,
                "name": name,
                "current": len(matches),
                "limit": max_count,
                "type": "count",
                "action": action,
                "severity": "CRITICAL" if len(matches) > max_count * 2 else "WARNING",
            })

        if max_lines is not None:
            for match_path in matches:
                lines = count_lines(Path(match_path))
                if lines > max_lines:
                    rel_path = os.path.relpath(match_path, project_root)
                    violations.append({
                        "file": rel_path,
                        "name": name,
                        "current": lines,
                        "limit": max_lines,
                        "type": "lines",
                        "action": action,
                        "severity": "CRITICAL" if lines > max_lines * 2 else "WARNING",
                    })

    return violations


def format_output(violations: list[dict]) -> str:
    """Format violations for console output."""
    if not violations:
        return ""

    lines = [
        "",
        "=" * 60,
        "  FILE LIMITS GUARD - VIOLATIONS DETECTED!",
        "=" * 60,
    ]

    for v in violations:
        icon = "[!]" if v["severity"] == "CRITICAL" else "[*]"
        unit = "files" if v["type"] == "count" else "lines"
        lines.append(f"\n{icon} {v['severity']}: {v['file']}")
        lines.append(f"    {v['name']}: {v['current']} {unit} (limit: {v['limit']})")
        lines.append(f"    Action: {v['action']}")

    lines.extend([
        "",
        "-" * 60,
        "  Clean up before your next commit!",
        "-" * 60,
        "",
    ])

    return "\n".join(lines)


def main():
    """Entry point."""
    try:
        input_data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        input_data = {}

    cwd = input_data.get("cwd", os.getcwd())
    violations = check_limits(cwd)

    if violations:
        print(format_output(violations), file=sys.stderr)

    # Never block the session, just warn
    print(json.dumps({"result": "File limits check completed"}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
