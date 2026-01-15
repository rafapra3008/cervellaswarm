#!/usr/bin/env python3
"""
UPDATE PROMPT_RIPRESA - Cervella & Rafa
Versione: 1.0.0
Data: 1 Gennaio 2026

Aggiorna automaticamente PROMPT_RIPRESA.md con checkpoint.
Chiamato da PreCompact e SessionEnd hooks.
"""

import json
import sys
import os
import subprocess
from datetime import datetime
from pathlib import Path

__version__ = "1.0.0"
__version_date__ = "2026-01-01"

# === CONFIGURAZIONE ===

# NOTA: Context Mesh Pattern - ogni progetto ha il suo PROMPT_RIPRESA in .sncp/
# Tutti i PROMPT_RIPRESA sono centralizzati in CervellaSwarm/.sncp/progetti/
CERVELLASWARM_ROOT = Path.home() / "Developer/CervellaSwarm"

KNOWN_PROJECTS = {
    "ContabilitaAntigravity": {
        "path": Path.home() / "Developer/ContabilitaAntigravity",
        "prompt_ripresa": CERVELLASWARM_ROOT / ".sncp/progetti/contabilita/PROMPT_RIPRESA_contabilita.md"
    },
    "miracollogeminifocus": {
        "path": Path.home() / "Developer/miracollogeminifocus",
        "prompt_ripresa": CERVELLASWARM_ROOT / ".sncp/progetti/miracollo/PROMPT_RIPRESA_miracollo.md"
    },
    "CervellaSwarm": {
        "path": CERVELLASWARM_ROOT,
        "prompt_ripresa": CERVELLASWARM_ROOT / ".sncp/progetti/cervellaswarm/PROMPT_RIPRESA_cervellaswarm.md"
    }
}


def detect_project(cwd: str) -> dict:
    """Rileva il progetto dal path."""
    for folder_name, info in KNOWN_PROJECTS.items():
        if folder_name in cwd:
            return {
                "id": folder_name,
                "path": info["path"],
                "prompt_ripresa": info["prompt_ripresa"],
                "known": True
            }
    return {"known": False}


def get_git_status(cwd: str) -> str:
    """Ottiene git status formattato."""
    try:
        # Branch
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=cwd, capture_output=True, text=True, timeout=5
        )
        branch = result.stdout.strip() if result.returncode == 0 else "unknown"

        # Ultimo commit
        result = subprocess.run(
            ["git", "log", "-1", "--pretty=format:%h - %s"],
            cwd=cwd, capture_output=True, text=True, timeout=5
        )
        last_commit = result.stdout.strip() if result.returncode == 0 else "N/A"

        # File modificati
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=cwd, capture_output=True, text=True, timeout=5
        )
        modified = []
        if result.returncode == 0 and result.stdout.strip():
            for line in result.stdout.strip().split("\n")[:5]:  # Max 5 file
                if line:
                    modified.append(f"  - {line[3:].strip()}")

        status = f"- **Branch**: {branch}\n"
        status += f"- **Ultimo commit**: {last_commit}\n"
        if modified:
            status += f"- **File modificati** ({len(modified)}):\n" + "\n".join(modified)
        else:
            status += "- **File modificati**: Nessuno (git pulito)"

        return status
    except Exception as e:
        return f"- Errore git: {str(e)}"


def update_prompt_ripresa(project: dict, trigger: str, cwd: str) -> bool:
    """Aggiorna PROMPT_RIPRESA_{progetto}.md con checkpoint automatico."""
    if not project.get("known"):
        return False

    # prompt_ripresa ora è già un Path completo (Context Mesh)
    prompt_file = project["prompt_ripresa"]
    if not prompt_file.exists():
        return False

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    git_status = get_git_status(cwd)

    checkpoint_section = f"""

---

## AUTO-CHECKPOINT: {timestamp} ({trigger})

### Stato Git
{git_status}

### Note
- Checkpoint automatico generato da hook
- Trigger: {trigger}

---
"""

    try:
        # Leggi contenuto esistente
        with open(prompt_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Cerca se esiste gia una sezione AUTO-CHECKPOINT recente (ultimi 30 min)
        # Per evitare duplicati, rimuovi vecchi checkpoint auto
        lines = content.split('\n')
        new_lines = []
        skip_until_separator = False

        for line in lines:
            if line.startswith('## AUTO-CHECKPOINT:'):
                skip_until_separator = True
                continue
            if skip_until_separator and line.strip() == '---':
                skip_until_separator = False
                continue
            if not skip_until_separator:
                new_lines.append(line)

        content = '\n'.join(new_lines)

        # Aggiungi nuovo checkpoint alla fine
        content = content.rstrip() + checkpoint_section

        # Scrivi
        with open(prompt_file, 'w', encoding='utf-8') as f:
            f.write(content)

        return True
    except Exception as e:
        return False


def send_notification(message: str):
    """Notifica discreta."""
    try:
        script = f'display notification "{message}" with title "📝 PROMPT_RIPRESA" sound name "Pop"'
        subprocess.run(["osascript", "-e", script], capture_output=True, timeout=5)
    except:
        pass


def main():
    try:
        input_data = json.load(sys.stdin)
    except:
        input_data = {}

    cwd = input_data.get("cwd", os.getcwd())
    trigger = input_data.get("trigger", "unknown")

    project = detect_project(cwd)

    if project.get("known"):
        success = update_prompt_ripresa(project, trigger, cwd)
        if success:
            project_name = project["id"].replace("geminifocus", "").replace("Antigravity", "")
            send_notification(f"Checkpoint: {project_name}")

    output = {"continue": True, "suppressOutput": True}
    print(json.dumps(output))
    return 0


if __name__ == "__main__":
    sys.exit(main())
