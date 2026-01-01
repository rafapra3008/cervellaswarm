#!/usr/bin/env python3
"""
SESSION END SAVE - Cervella & Rafa
Versione: 1.0.0
Data: 1 Gennaio 2026

Salva stato quando la sessione Claude Code viene chiusa.
Funziona per TUTTI i progetti.

Salva:
- JSON snapshot in iCloud REGOLE_GLOBALI
- Log in ~/.claude/session-log.txt
- Notifica macOS
"""

import json
import sys
import os
import subprocess
from datetime import datetime
from pathlib import Path

__version__ = "1.0.0"
__version_date__ = "2026-01-01"

# === CONFIGURAZIONE GLOBALE ===

ICLOUD_REGOLE = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/REGOLE_GLOBALI"
SNAPSHOTS_DIR = ICLOUD_REGOLE / "session_snapshots"
LOG_FILE = Path.home() / ".claude/session-log.txt"

KNOWN_PROJECTS = {
    "ContabilitaAntigravity": {
        "name": "Contabilita",
        "emoji": "💰",
        "ultimo_lavoro": "ULTIMO_LAVORO_CONTABILITA.md"
    },
    "miracollogeminifocus": {
        "name": "Miracollo PMS",
        "emoji": "🏨",
        "ultimo_lavoro": "ULTIMO_LAVORO_MIRACOLLO.md"
    },
    "million-dollar-ideas": {
        "name": "Libertaio",
        "emoji": "💡",
        "ultimo_lavoro": "ULTIMO_LAVORO_LIBERTAIO.md"
    },
    "CervellaSwarm": {
        "name": "CervellaSwarm",
        "emoji": "🐝",
        "ultimo_lavoro": "ULTIMO_LAVORO_CERVELLASWARM.md"
    }
}

# === FUNZIONI ===

def detect_project(cwd: str) -> dict:
    """Rileva il progetto dal path."""
    cwd_path = Path(cwd)

    for folder_name, info in KNOWN_PROJECTS.items():
        if folder_name in cwd:
            return {
                "id": folder_name,
                "name": info["name"],
                "emoji": info["emoji"],
                "ultimo_lavoro": info.get("ultimo_lavoro"),
                "known": True
            }

    folder_name = cwd_path.name if cwd_path.name else "unknown"
    return {
        "id": folder_name,
        "name": folder_name.replace("-", " ").replace("_", " ").title(),
        "emoji": "📁",
        "ultimo_lavoro": None,
        "known": False
    }


def get_git_info(cwd: str) -> dict:
    """Ottiene info git."""
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--pretty=format:%h|%s|%an|%ai"],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            parts = result.stdout.strip().split("|")
            last_commit = {
                "hash": parts[0] if len(parts) > 0 else "",
                "message": parts[1] if len(parts) > 1 else "",
                "author": parts[2] if len(parts) > 2 else "",
                "date": parts[3] if len(parts) > 3 else ""
            }
        else:
            last_commit = None

        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=5
        )
        modified_files = []
        if result.returncode == 0 and result.stdout.strip():
            for line in result.stdout.strip().split("\n"):
                if line:
                    status = line[:2].strip()
                    filename = line[3:].strip()
                    modified_files.append({"status": status, "file": filename})

        result = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=5
        )
        branch = result.stdout.strip() if result.returncode == 0 else "unknown"

        return {
            "last_commit": last_commit,
            "modified_files": modified_files,
            "branch": branch,
            "has_uncommitted": len(modified_files) > 0
        }
    except Exception as e:
        return {"error": str(e)}


def send_notification(title: str, message: str, sound: str = "Glass"):
    """Invia notifica macOS."""
    try:
        script = f'display notification "{message}" with title "{title}" sound name "{sound}"'
        subprocess.run(["osascript", "-e", script], capture_output=True, timeout=5)
    except:
        pass


def save_snapshot(data: dict) -> Path:
    """Salva snapshot JSON in iCloud."""
    SNAPSHOTS_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    project_id = data.get("project", {}).get("id", "unknown")
    filename = f"session_{project_id}_{timestamp}.json"
    filepath = SNAPSHOTS_DIR / filename

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False, default=str)

    return filepath


def log_session(project: dict, event: str, snapshot_path: Path = None):
    """Aggiunge entry al log."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    emoji = project.get("emoji", "📁")
    name = project.get("name", "Unknown")

    snapshot_info = f" → {snapshot_path.name}" if snapshot_path else ""
    log_entry = f"[{timestamp}] {emoji} SESSION {event} - {name}{snapshot_info}\n"

    try:
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except:
        pass


def main():
    """Main function."""
    try:
        input_data = json.load(sys.stdin)
    except:
        input_data = {}

    session_id = input_data.get("session_id", "unknown")
    transcript_path = input_data.get("transcript_path", "")
    cwd = input_data.get("cwd", os.getcwd())

    project = detect_project(cwd)
    git_info = get_git_info(cwd)

    snapshot = {
        "version": __version__,
        "timestamp": datetime.now().isoformat(),
        "event": "session_end",
        "session_id": session_id,
        "project": project,
        "cwd": cwd,
        "git": git_info
    }

    try:
        snapshot_path = save_snapshot(snapshot)
    except Exception as e:
        snapshot_path = None
        snapshot["save_error"] = str(e)

    log_session(project, "END", snapshot_path)

    emoji = project.get("emoji", "📁")
    name = project.get("name", "Unknown")
    uncommitted_count = len(git_info.get("modified_files", []))

    if uncommitted_count > 0:
        message = f"Sessione chiusa! ⚠️ {uncommitted_count} file da committare"
    else:
        message = "Sessione chiusa! ✅ Git pulito"

    send_notification(f"{emoji} {name}", message, "Glass")

    output = {"continue": True, "suppressOutput": True}
    print(json.dumps(output))
    return 0


if __name__ == "__main__":
    sys.exit(main())
