#!/usr/bin/env python3
"""
Hook SessionStart CervellaSwarm - Caricamento Contesto Sciame

Inietta SOLO info essenziali (puntatori, warnings). NON ripete contenuto
gia' presente in CLAUDE.md, MEMORY.md o auto-caricato dal system-reminder.

Versione: 3.1.0
Data: 2026-02-28
Cervella & Rafa

v2.0.0 - Aggiunta COSTITUZIONE obbligatoria!
v2.1.0 - Sessione 299 - SNCP 2.0 Day 5: Warning PROMPT_RIPRESA e handoff
v2.2.0 - Sessione 302 - Aggiornato a 17 membri (con Architect)
v3.0.0 - Sessione 352 - B.3 Smart Loading: rimosso COSTITUZIONE e NORD (-210 righe contesto)
v3.1.0 - Sessione 428 - Output ridotto: solo puntatori + warnings (~600 char, era ~4800)
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
import os

# Path progetto
PROJECT_ROOT = Path(__file__).parent.parent.parent


def check_if_review_day() -> tuple:
    """Verifica se oggi e giorno CODE REVIEW (Lunedi o Venerdi)."""
    now = datetime.now()
    day_num = now.weekday()  # 0=Mon, 4=Fri
    day_names = {0: "Lunedi", 4: "Venerdi"}
    is_review_day = day_num in [0, 4]
    day_name = day_names.get(day_num, now.strftime("%A"))
    return is_review_day, day_name


def check_prompt_ripresa_age(file_path: Path, max_days: int = 7) -> tuple:
    """
    Verifica se PROMPT_RIPRESA e' troppo vecchio.
    SNCP 2.0 - Warning se > 7 giorni senza update.

    Returns: (is_old, days_old)
    """
    try:
        if not file_path.exists():
            return False, 0

        mtime = os.path.getmtime(file_path)
        file_date = datetime.fromtimestamp(mtime)
        days_old = (datetime.now() - file_date).days

        return days_old > max_days, days_old
    except Exception:
        return False, 0


def check_handoff_age(handoff_dir: Path, project_name: str, max_days: int = 3) -> tuple:
    """
    Verifica se ultimo handoff per il progetto e' troppo vecchio.
    SNCP 2.0 - Warning se > 3 giorni senza handoff.

    Returns: (is_old, days_old, last_handoff_name)
    """
    try:
        if not handoff_dir.exists():
            return True, 999, None

        # Cerca handoff per questo progetto
        # Pattern: HANDOFF_*cervellaswarm*.md o HANDOFF_*_S*.md (nuovo formato)
        handoffs = []
        for f in handoff_dir.glob("*.md"):
            name_lower = f.name.lower()
            if project_name.lower() in name_lower or f"_s" in name_lower:
                handoffs.append(f)

        if not handoffs:
            # Fallback: prendi tutti gli handoff recenti
            handoffs = list(handoff_dir.glob("HANDOFF_*.md"))

        if not handoffs:
            return True, 999, None

        # Trova il piu' recente per data modifica
        latest = max(handoffs, key=lambda f: os.path.getmtime(f))
        mtime = os.path.getmtime(latest)
        file_date = datetime.fromtimestamp(mtime)
        days_old = (datetime.now() - file_date).days

        return days_old > max_days, days_old, latest.name
    except Exception:
        return False, 0, None


def main():
    """Entry point hook."""
    try:
        now = datetime.now()
        context_parts = []

        # Header compatto
        context_parts.append("# CERVELLASWARM - Sessione Iniziata")
        context_parts.append(f"*Workspace: CervellaSwarm | {now.strftime('%Y-%m-%d %H:%M')}*")
        context_parts.append("- COSTITUZIONE: `~/.claude/COSTITUZIONE_OPERATIVA.md` | Completa: `~/.claude/COSTITUZIONE.md`")
        context_parts.append("- Stato: leggi `.sncp/progetti/cervellaswarm/PROMPT_RIPRESA_cervellaswarm.md`")
        context_parts.append("- NORD: `~/Developer/CervellaSwarm/NORD.md`")
        context_parts.append("")

        # Warning: CODE REVIEW day (Lunedi o Venerdi)
        is_review_day, day_name = check_if_review_day()
        if is_review_day:
            context_parts.append(f"WARNING CODE REVIEW DAY: Oggi e {day_name} - invocare `cervella-reviewer` per audit?")
            context_parts.append("")

        # Warning: PROMPT_RIPRESA troppo vecchio
        prompt_ripresa_path = PROJECT_ROOT / ".sncp/progetti/cervellaswarm/PROMPT_RIPRESA_cervellaswarm.md"
        is_pr_old, pr_days = check_prompt_ripresa_age(prompt_ripresa_path, max_days=7)
        if is_pr_old:
            context_parts.append(f"WARNING SNCP: PROMPT_RIPRESA non aggiornato da {pr_days} giorni - aggiornare a fine sessione.")
            context_parts.append("")

        # Warning: handoff mancante
        handoff_dir = PROJECT_ROOT / ".swarm/handoff"
        is_handoff_old, handoff_days, last_handoff = check_handoff_age(handoff_dir, "cervellaswarm", max_days=3)
        if is_handoff_old and handoff_days > 0:
            last = f" (ultimo: {last_handoff})" if last_handoff else ""
            context_parts.append(f"WARNING SNCP: Ultimo handoff {handoff_days} giorni fa{last} - creare handoff a fine sessione.")
            context_parts.append("")

        context_md = "\n".join(context_parts)

        result = {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": context_md
            }
        }

        print(json.dumps(result))
        sys.exit(0)

    except Exception as e:
        # Fallback graceful
        error_result = {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": f"Hook Swarm: errore caricamento contesto - {str(e)}"
            }
        }
        print(json.dumps(error_result))
        sys.exit(0)


if __name__ == "__main__":
    main()
