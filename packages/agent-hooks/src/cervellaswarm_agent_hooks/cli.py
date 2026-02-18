# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""
CLI for CervellaSwarm Agent Hooks.

Commands:
    cervella-hooks setup     Generate config file and settings.json snippet
    cervella-hooks list      List available hooks
    cervella-hooks version   Show version
"""

import json
import sys
from importlib.resources import files
from pathlib import Path

from . import __version__

HOOKS_INFO = [
    {
        "name": "bash-validator",
        "command": "cervella-bash-validator",
        "event": "PreToolUse",
        "matcher": "Bash",
        "description": "Blocks destructive bash commands, asks for risky ones, auto-fixes where possible",
        "timeout": 5,
    },
    {
        "name": "git-reminder",
        "command": "cervella-git-reminder",
        "event": "Stop",
        "matcher": "",
        "description": "Discreet notification about uncommitted files (max once every 30 min)",
        "timeout": 10,
    },
    {
        "name": "file-limits",
        "command": "cervella-file-limits",
        "event": "SessionEnd",
        "matcher": "",
        "description": "Checks file sizes/counts to prevent bloat (configurable via hooks.yaml)",
        "timeout": 10,
    },
    {
        "name": "context-inject",
        "command": "cervella-context-inject",
        "event": "SubagentStart",
        "matcher": "",
        "description": "Injects project facts and state into all subagents automatically",
        "timeout": 5,
    },
    {
        "name": "session-checkpoint",
        "command": "cervella-session-checkpoint",
        "event": "SessionEnd",
        "matcher": "",
        "description": "Auto-saves project state (git info + focus) at session end",
        "timeout": 15,
    },
]


def cmd_list():
    """List all available hooks."""
    print(f"CervellaSwarm Agent Hooks v{__version__}")
    print(f"{'=' * 60}")
    print()

    for hook in HOOKS_INFO:
        print(f"  {hook['name']}")
        print(f"    Command: {hook['command']}")
        print(f"    Event:   {hook['event']} (matcher: {hook['matcher'] or '*'})")
        print(f"    {hook['description']}")
        print()


def cmd_setup():
    """Generate config file and show settings.json snippet."""
    print(f"CervellaSwarm Agent Hooks v{__version__} - Setup")
    print(f"{'=' * 60}")
    print()

    # Generate hooks.yaml
    config_dir = Path.cwd() / ".cervella"
    config_file = config_dir / "hooks.yaml"

    if config_file.exists():
        print(f"  Config file already exists: {config_file}")
    else:
        config_dir.mkdir(parents=True, exist_ok=True)
        # Use the example config from the package
        example_content = _get_example_config()
        config_file.write_text(example_content, encoding="utf-8")
        print(f"  Created config: {config_file}")
        print(f"  Edit it to customize hook behavior.")

    print()
    print("  Add these hooks to your Claude Code settings.json:")
    print(f"  (File: ~/.claude/settings.json)")
    print()

    # Generate settings.json snippet
    settings = {}
    for hook in HOOKS_INFO:
        event = hook["event"]
        entry = {
            "matcher": hook["matcher"],
            "hooks": [
                {
                    "type": "command",
                    "command": hook["command"],
                    "timeout": hook["timeout"],
                }
            ],
        }

        if event not in settings:
            settings[event] = []
        settings[event].append(entry)

    snippet = json.dumps(settings, indent=2)
    for line in snippet.split("\n"):
        print(f"    {line}")

    print()
    print("  Copy the relevant sections into your settings.json 'hooks' object.")
    print("  You can pick individual hooks - they work independently.")
    print()


def _get_example_config() -> str:
    """Get the example hooks.yaml content."""
    try:
        pkg_files = files("cervellaswarm_agent_hooks")
        # Try to read from package
        example = (pkg_files / ".." / ".." / "examples" / "hooks.yaml").read_text()
        return example
    except Exception:
        pass

    # Fallback: minimal config
    return """# CervellaSwarm Agent Hooks - Configuration
# See: https://github.com/rafapra3008/cervellaswarm/tree/main/packages/agent-hooks

file_limits:
  checks:
    - pattern: "SESSION_STATE.md"
      name: "Session state file"
      max_lines: 300
      action: "Archive old content"

context_inject:
  facts_file: "docs/FACTS.md"
  state_file: "SESSION_STATE.md"
  facts_max_lines: 100
  state_max_lines: 50

session_checkpoint:
  state_file: "SESSION_STATE.md"
  include_git_status: true
  include_recent_commits: true

git_reminder:
  interval_minutes: 30
"""


def cmd_version():
    """Show version."""
    print(f"cervellaswarm-agent-hooks v{__version__}")


def main():
    """CLI entry point."""
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help", "help"):
        print("Usage: cervella-hooks <command>")
        print()
        print("Commands:")
        print("  setup    Generate config file and settings.json snippet")
        print("  list     List available hooks")
        print("  version  Show version")
        return 0

    cmd = args[0]

    if cmd == "setup":
        cmd_setup()
    elif cmd == "list":
        cmd_list()
    elif cmd in ("version", "--version", "-V"):
        cmd_version()
    else:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        print("Run 'cervella-hooks help' for usage.", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
