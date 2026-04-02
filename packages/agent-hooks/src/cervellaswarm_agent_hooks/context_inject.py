# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""
Context Injection - SubagentStart Hook for Claude Code.

Injects project-specific context into ALL subagents automatically:
- Facts file: verified facts that agents should never contradict
- State file: current project state (session resume summary)

Lightweight (<0.5s), fail-graceful (never blocks agent startup).

Usage in Claude Code settings.json:
    "SubagentStart": [{
        "matcher": "",
        "hooks": [{"type": "command", "command": "cervella-context-inject"}]
    }]
"""

import json
import os
import sys
from pathlib import Path

from .config import get_hook_config

__version__ = "1.0.0"


def find_project_root(cwd: str) -> Path | None:
    """Find project root by walking up to the nearest .git directory."""
    current = Path(cwd)
    for parent in [current, *current.parents]:
        if (parent / ".git").exists():
            return parent
    return None


def safe_read(path: Path, max_lines: int = 0) -> str | None:
    """Read file safely with optional line limit."""
    try:
        if not path.exists():
            return None
        content = path.read_text(encoding="utf-8")
        if max_lines > 0:
            lines = content.split("\n")
            if len(lines) > max_lines:
                content = "\n".join(lines[:max_lines])
                content += f"\n\n... ({len(lines) - max_lines} more lines)"
        return content
    except Exception as e:
        print(f"context_inject: failed to read {path}: {e}", file=sys.stderr)
        return None


def build_context(project_root: Path, config: dict) -> str | None:
    """Build the additionalContext markdown string."""
    parts = []
    project_name = project_root.name
    parts.append(f"# PROJECT CONTEXT: {project_name}")
    parts.append("")

    has_content = False

    # Facts file
    facts_file = config.get("facts_file", "docs/FACTS.md")
    facts_max = config.get("facts_max_lines", 100)
    facts_path = project_root / facts_file
    facts = safe_read(facts_path, max_lines=facts_max)
    if facts:
        parts.append("## CONFIRMED FACTS (DO NOT contradict!)")
        parts.append(facts)
        parts.append("")
        has_content = True

    # State file
    state_file = config.get("state_file", "SESSION_STATE.md")
    state_max = config.get("state_max_lines", 50)
    state_path = project_root / state_file
    state = safe_read(state_path, max_lines=state_max)
    if state:
        parts.append("## CURRENT STATE")
        parts.append(state)
        parts.append("")
        has_content = True

    if not has_content:
        return None

    parts.append("---")
    parts.append(
        "RULE: If your research contradicts a CONFIRMED FACT, "
        "STOP and report the contradiction."
    )

    return "\n".join(parts)


def main():
    """Entry point."""
    try:
        try:
            input_data = json.load(sys.stdin)
        except (json.JSONDecodeError, ValueError):
            input_data = {}

        cwd = input_data.get("cwd", os.getcwd())
        project_root = find_project_root(cwd)

        if not project_root:
            print(json.dumps({}))
            return

        config = get_hook_config("context_inject")
        context_md = build_context(project_root, config)

        if not context_md:
            print(json.dumps({}))
            return

        result = {
            "hookSpecificOutput": {
                "hookEventName": "SubagentStart",
                "additionalContext": context_md,
            }
        }
        print(json.dumps(result))

    except Exception as e:
        print(f"context_inject: {e}", file=sys.stderr)
        print(json.dumps({}))


if __name__ == "__main__":
    main()
