# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""
Git Reminder - Stop Hook for Claude Code.

Sends a discreet notification when there are uncommitted files.
Reminds at most once every 30 minutes to avoid being annoying.

Usage in Claude Code settings.json:
    "Stop": [{
        "matcher": "",
        "hooks": [{"type": "command", "command": "cervella-git-reminder"}]
    }]

Optionally reads interval from hooks.yaml config when pyyaml is available.
macOS notifications via osascript, Linux via notify-send (optional, silent if unavailable).
"""

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

__version__ = "1.0.0"

# State file tracks when last reminder was sent per project
REMINDER_STATE_FILE = Path.home() / ".claude" / "git_reminder_state.json"
DEFAULT_INTERVAL_MINUTES = 30


def _get_interval_minutes() -> int:
    """Get reminder interval from config or default."""
    try:
        from .config import get_hook_config

        cfg = get_hook_config("git_reminder")
        return int(cfg.get("interval_minutes", DEFAULT_INTERVAL_MINUTES))
    except Exception as e:
        print(f"git_reminder: config load failed: {e}", file=sys.stderr)
        return DEFAULT_INTERVAL_MINUTES


def get_uncommitted_count(cwd: str) -> int:
    """Count uncommitted files in the git working tree."""
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0 and result.stdout.strip():
            return len(result.stdout.strip().split("\n"))
        return 0
    except Exception as e:
        print(f"git_reminder: git status failed: {e}", file=sys.stderr)
        return 0


def should_remind(cwd: str) -> bool:
    """Check if we should send a reminder (max once per interval)."""
    try:
        interval = _get_interval_minutes()
        if REMINDER_STATE_FILE.exists():
            with open(REMINDER_STATE_FILE, "r") as f:
                state = json.load(f)

            last_reminder = state.get(cwd)
            if last_reminder:
                last_time = datetime.fromisoformat(last_reminder)
                diff_minutes = (datetime.now() - last_time).total_seconds() / 60
                if diff_minutes < interval:
                    return False
        return True
    except (json.JSONDecodeError, ValueError, OSError) as e:
        print(f"git_reminder: should_remind check failed: {e}", file=sys.stderr)
        return True


MAX_STATE_ENTRIES = 20  # Prune old entries to prevent unbounded growth


def update_reminder_state(cwd: str):
    """Update the timestamp of the last reminder. Prunes old entries."""
    try:
        state = {}
        if REMINDER_STATE_FILE.exists():
            with open(REMINDER_STATE_FILE, "r") as f:
                state = json.load(f)

        state[cwd] = datetime.now().isoformat()

        # Prune: keep only the MAX_STATE_ENTRIES most recent entries
        if len(state) > MAX_STATE_ENTRIES:
            sorted_entries = sorted(state.items(), key=lambda x: x[1], reverse=True)
            state = dict(sorted_entries[:MAX_STATE_ENTRIES])

        REMINDER_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(REMINDER_STATE_FILE, "w") as f:
            json.dump(state, f, indent=2)
    except (json.JSONDecodeError, ValueError, OSError) as e:
        print(f"git_reminder: state update failed: {e}", file=sys.stderr)


def send_notification(count: int):
    """Send a discreet desktop notification (cross-platform)."""
    msg = f"You have {count} uncommitted file{'s' if count != 1 else ''}"

    # macOS: osascript
    try:
        script = (
            f'display notification "{msg}" '
            f'with title "Git Reminder" sound name "Tink"'
        )
        subprocess.run(
            ["osascript", "-e", script], capture_output=True, timeout=5
        )
        return
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"git_reminder: macOS notification failed: {e}", file=sys.stderr)

    # Linux: notify-send (optional)
    try:
        subprocess.run(
            ["notify-send", "Git Reminder", msg],
            capture_output=True,
            timeout=5,
        )
    except Exception as e:
        print(f"git_reminder: Linux notification failed: {e}", file=sys.stderr)


def main():
    """Entry point - reads hook input from stdin, checks for uncommitted files."""
    try:
        input_data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError) as e:
        print(f"git_reminder: stdin parse failed: {e}", file=sys.stderr)
        input_data = {}

    cwd = input_data.get("cwd", os.getcwd())

    count = get_uncommitted_count(cwd)
    if count > 0 and should_remind(cwd):
        send_notification(count)
        update_reminder_state(cwd)

    output = {"continue": True, "suppressOutput": True}
    print(json.dumps(output))
    return 0


if __name__ == "__main__":
    sys.exit(main())
