#!/usr/bin/env python3
"""
PRE-COMPACT SAVE - Cervella & Rafa
Versione: 2.0.0
Data: 29 Dicembre 2025

SOLUZIONE GLOBALE per salvare stato prima di compact.
Funziona per TUTTI i progetti (presenti e futuri).

Salva:
- JSON snapshot in iCloud REGOLE_GLOBALI
- Log in ~/.claude/compact-log.txt
- Notifica macOS

Uso:
- Chiamato automaticamente da PreCompact hook
- Riceve JSON da stdin con session_id, transcript_path, trigger, cwd
"""

import json
import sys
import os
import subprocess
from datetime import datetime
from pathlib import Path

__version__ = "2.0.0"
__version_date__ = "2025-12-29"

# === CONFIGURAZIONE GLOBALE ===

# Dove salvare gli snapshot (iCloud per persistenza)
ICLOUD_REGOLE = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/REGOLE_GLOBALI"
SNAPSHOTS_DIR = ICLOUD_REGOLE / "compact_snapshots"

# Log file
LOG_FILE = Path.home() / ".claude/compact-log.txt"

# Progetti conosciuti (si auto-espande con nuovi progetti)
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
    """Rileva il progetto dal path. Funziona anche per progetti futuri."""
    cwd_path = Path(cwd)

    # Cerca nei progetti conosciuti
    for folder_name, info in KNOWN_PROJECTS.items():
        if folder_name in cwd:
            return {
                "id": folder_name,
                "name": info["name"],
                "emoji": info["emoji"],
                "ultimo_lavoro": info.get("ultimo_lavoro"),
                "known": True
            }

    # Progetto sconosciuto - usa nome cartella
    folder_name = cwd_path.name if cwd_path.name else "unknown"
    return {
        "id": folder_name,
        "name": folder_name.replace("-", " ").replace("_", " ").title(),
        "emoji": "📁",
        "ultimo_lavoro": None,
        "known": False
    }


def get_git_info(cwd: str) -> dict:
    """Ottiene info git (ultimo commit, file modificati)."""
    try:
        # Ultimo commit
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

        # File modificati (non committati)
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

        # Branch corrente
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


def read_transcript_summary(transcript_path: str, max_messages: int = 5) -> list:
    """Legge ultime N messaggi dal transcript (se accessibile)."""
    try:
        path = Path(transcript_path).expanduser()
        if not path.exists():
            return []

        messages = []
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    msg = json.loads(line.strip())
                    # Estrai solo info essenziali
                    if msg.get("role") in ["user", "assistant"]:
                        content = msg.get("content", "")
                        if isinstance(content, list):
                            # Estrai testo da content blocks
                            text_parts = []
                            for block in content:
                                if isinstance(block, dict) and block.get("type") == "text":
                                    text_parts.append(block.get("text", "")[:200])
                            content = " ".join(text_parts)
                        elif isinstance(content, str):
                            content = content[:200]

                        messages.append({
                            "role": msg.get("role"),
                            "preview": content[:200] + "..." if len(content) > 200 else content
                        })
                except:
                    continue

        # Ritorna ultimi N messaggi
        return messages[-max_messages:] if messages else []
    except Exception as e:
        return [{"error": str(e)}]


def send_notification(title: str, message: str, sound: str = "Ping"):
    """Invia notifica macOS."""
    try:
        script = f'display notification "{message}" with title "{title}" sound name "{sound}"'
        subprocess.run(["osascript", "-e", script], capture_output=True, timeout=5)
    except:
        pass


def save_snapshot(data: dict) -> Path:
    """Salva snapshot JSON in iCloud."""
    # Crea directory se non esiste
    SNAPSHOTS_DIR.mkdir(parents=True, exist_ok=True)

    # Nome file con timestamp e progetto
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    project_id = data.get("project", {}).get("id", "unknown")
    filename = f"compact_{project_id}_{timestamp}.json"
    filepath = SNAPSHOTS_DIR / filename

    # Salva JSON
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False, default=str)

    return filepath


def log_compact(project: dict, trigger: str, snapshot_path: Path = None):
    """Aggiunge entry al log."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    emoji = project.get("emoji", "📁")
    name = project.get("name", "Unknown")

    snapshot_info = f" → {snapshot_path.name}" if snapshot_path else ""
    log_entry = f"[{timestamp}] {emoji} COMPACT ({trigger}) - {name}{snapshot_info}\n"

    try:
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except:
        pass


def main():
    """Main function - chiamata dal PreCompact hook."""
    # Leggi input JSON da stdin
    try:
        input_data = json.load(sys.stdin)
    except:
        input_data = {}

    # Estrai dati
    session_id = input_data.get("session_id", "unknown")
    transcript_path = input_data.get("transcript_path", "")
    trigger = input_data.get("trigger", "unknown")
    cwd = input_data.get("cwd", os.getcwd())
    custom_instructions = input_data.get("custom_instructions", "")

    # Rileva progetto
    project = detect_project(cwd)

    # Raccogli info git
    git_info = get_git_info(cwd)

    # Leggi ultimi messaggi dal transcript
    last_messages = read_transcript_summary(transcript_path, max_messages=5)

    # Crea snapshot
    snapshot = {
        "version": __version__,
        "timestamp": datetime.now().isoformat(),
        "trigger": trigger,
        "session_id": session_id,
        "project": project,
        "cwd": cwd,
        "git": git_info,
        "last_messages": last_messages,
        "custom_instructions": custom_instructions if custom_instructions else None
    }

    # Salva snapshot
    try:
        snapshot_path = save_snapshot(snapshot)
    except Exception as e:
        snapshot_path = None
        snapshot["save_error"] = str(e)

    # Log
    log_compact(project, trigger, snapshot_path)

    # Notifica macOS
    emoji = project.get("emoji", "📁")
    name = project.get("name", "Unknown")
    uncommitted = "⚠️ File non committati!" if git_info.get("has_uncommitted") else "✅ Git pulito"

    send_notification(
        f"{emoji} {name}",
        f"Compact {trigger}! {uncommitted}",
        "Ping"
    )

    # Output per Claude (opzionale)
    output = {
        "continue": True,
        "suppressOutput": True
    }

    # Se ci sono file non committati, avvisa
    if git_info.get("has_uncommitted"):
        output["systemMessage"] = f"⚠️ {len(git_info.get('modified_files', []))} file non committati!"
        output["suppressOutput"] = False

    print(json.dumps(output))
    return 0


if __name__ == "__main__":
    sys.exit(main())
