#!/usr/bin/env python3
"""
GIT REMINDER - Cervella & Rafa
Versione: 1.0.0
Data: 1 Gennaio 2026

Reminder discreto per file non committati.
Notifica solo ogni 30 minuti per non essere fastidioso.
"""

import json
import sys
import os
import subprocess
from datetime import datetime
from pathlib import Path

__version__ = "1.0.0"

# File per tracciare ultimo reminder
REMINDER_STATE_FILE = Path.home() / ".claude/git_reminder_state.json"
REMINDER_INTERVAL_MINUTES = 30


def get_uncommitted_count(cwd: str) -> int:
    """Conta file non committati."""
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=cwd, capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0 and result.stdout.strip():
            return len(result.stdout.strip().split("\n"))
        return 0
    except:
        return 0


def should_remind(cwd: str) -> bool:
    """Controlla se dovremmo inviare reminder (ogni 30 min max)."""
    try:
        if REMINDER_STATE_FILE.exists():
            with open(REMINDER_STATE_FILE, 'r') as f:
                state = json.load(f)

            last_reminder = state.get(cwd)
            if last_reminder:
                last_time = datetime.fromisoformat(last_reminder)
                now = datetime.now()
                diff_minutes = (now - last_time).total_seconds() / 60

                if diff_minutes < REMINDER_INTERVAL_MINUTES:
                    return False
        return True
    except:
        return True


def update_reminder_state(cwd: str):
    """Aggiorna timestamp ultimo reminder."""
    try:
        state = {}
        if REMINDER_STATE_FILE.exists():
            with open(REMINDER_STATE_FILE, 'r') as f:
                state = json.load(f)

        state[cwd] = datetime.now().isoformat()

        REMINDER_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(REMINDER_STATE_FILE, 'w') as f:
            json.dump(state, f, indent=2)
    except:
        pass


def send_notification(count: int):
    """Notifica discreta."""
    try:
        if count == 1:
            msg = "Hai 1 file non committato"
        else:
            msg = f"Hai {count} file non committati"

        script = f'display notification "{msg}" with title "⏰ Git Reminder" sound name "Tink"'
        subprocess.run(["osascript", "-e", script], capture_output=True, timeout=5)
    except:
        pass


def main():
    try:
        input_data = json.load(sys.stdin)
    except:
        input_data = {}

    cwd = input_data.get("cwd", os.getcwd())

    # Controlla se ci sono file non committati
    count = get_uncommitted_count(cwd)

    if count > 0 and should_remind(cwd):
        send_notification(count)
        update_reminder_state(cwd)

    output = {"continue": True, "suppressOutput": True}
    print(json.dumps(output))
    return 0


if __name__ == "__main__":
    sys.exit(main())
