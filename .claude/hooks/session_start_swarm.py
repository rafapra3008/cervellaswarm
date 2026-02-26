#!/usr/bin/env python3
"""
Hook SessionStart CervellaSwarm - Caricamento Contesto Sciame

Carica automaticamente all'avvio sessione:
- PROMPT_RIPRESA.md (stato attuale)
- Check CODE REVIEW day (Lunedi/Venerdi)
- Reminder regole Sciame
- Warning se PROMPT_RIPRESA > 7 giorni vecchio (SNCP 2.0)
- Warning se ultimo handoff > 3 giorni (SNCP 2.0)

NON carica (B.3 Smart Loading - S352):
- COSTITUZIONE_OPERATIVA.md -> caricata dagli agenti via _SHARED_DNA (AZIONE #1). Completa via "mi sento persa".
- NORD.md -> disponibile via /swarm-context skill (carica NORD + PROMPT_RIPRESA on-demand)

Versione: 3.0.0
Data: 2026-02-10
Cervella & Rafa

v2.0.0 - Aggiunta COSTITUZIONE obbligatoria!
v2.1.0 - Sessione 299 - SNCP 2.0 Day 5: Warning PROMPT_RIPRESA e handoff
v2.2.0 - Sessione 302 - Aggiornato a 17 membri (con Architect)
v3.0.0 - Sessione 352 - B.3 Smart Loading: rimosso COSTITUZIONE e NORD (-210 righe contesto)
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
import os

# Path progetto
PROJECT_ROOT = Path(__file__).parent.parent.parent


def load_file_summary(file_path: Path, max_lines: int = 100) -> str:
    """Carica file con limite righe."""
    try:
        if file_path.exists():
            content = file_path.read_text(encoding='utf-8')
            lines = content.split('\n')
            if len(lines) > max_lines:
                return '\n'.join(lines[:max_lines]) + f"\n\n... (altre {len(lines) - max_lines} righe)"
            return content
        else:
            return f"File non trovato: {file_path.name}"
    except Exception as e:
        return f"Errore lettura {file_path.name}: {e}"


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
        # PROMPT_RIPRESA specifico per CervellaSwarm (Context Mesh pattern)
        prompt_ripresa = load_file_summary(
            PROJECT_ROOT / ".sncp/progetti/cervellaswarm/PROMPT_RIPRESA_cervellaswarm.md",
            max_lines=100
        )

        # Check code review day
        is_review_day, day_name = check_if_review_day()

        # Formatta contesto
        context_parts = []

        # Header
        context_parts.append("# CERVELLASWARM - Sessione Iniziata")
        context_parts.append(f"*Workspace: CervellaSwarm | {datetime.now().strftime('%Y-%m-%d %H:%M')}*")
        context_parts.append("")

        # CODE REVIEW reminder se lunedi/venerdi
        if is_review_day:
            context_parts.append("## CODE REVIEW DAY!")
            context_parts.append(f"**Oggi e {day_name}** - Giorno di Code Review settimanale!")
            context_parts.append("Chiedi a Rafa se vuole invocare `cervella-reviewer` per audit.")
            context_parts.append("")

        # SNCP 2.0 - Warning se PROMPT_RIPRESA troppo vecchio
        prompt_ripresa_path = PROJECT_ROOT / ".sncp/progetti/cervellaswarm/PROMPT_RIPRESA_cervellaswarm.md"
        is_pr_old, pr_days = check_prompt_ripresa_age(prompt_ripresa_path, max_days=7)
        if is_pr_old:
            context_parts.append("## SNCP WARNING - PROMPT_RIPRESA VECCHIO!")
            context_parts.append(f"**PROMPT_RIPRESA non aggiornato da {pr_days} giorni!**")
            context_parts.append("Aggiornare a fine sessione con stato attuale.")
            context_parts.append("")

        # SNCP 2.0 - Warning se ultimo handoff troppo vecchio
        handoff_dir = PROJECT_ROOT / ".swarm/handoff"
        is_handoff_old, handoff_days, last_handoff = check_handoff_age(handoff_dir, "cervellaswarm", max_days=3)
        if is_handoff_old and handoff_days > 0:
            context_parts.append("## SNCP WARNING - HANDOFF MANCANTE!")
            context_parts.append(f"**Ultimo handoff: {handoff_days} giorni fa**")
            if last_handoff:
                context_parts.append(f"Ultimo: `{last_handoff}`")
            context_parts.append("Creare handoff a fine sessione (template 6-sezioni).")
            context_parts.append("")

        # Reminder Sciame
        context_parts.append("## Tu sei la REGINA!")
        context_parts.append("- 17 membri della famiglia pronti")
        context_parts.append("- 3 Guardiane (Opus) + 1 Architect (Opus) + 2 Analiste (Opus) + 10 Worker (Sonnet)")
        context_parts.append("- DELEGA sempre, MAI edit diretti!")
        context_parts.append("- COSTITUZIONE: agenti leggono OPERATIVA via _SHARED_DNA. Completa: `Read ~/.claude/COSTITUZIONE.md`")
        context_parts.append("- NORD + Contesto: usa `/swarm-context` per caricare on-demand")
        context_parts.append("")
        context_parts.append("## 3 Livelli Rischio")
        context_parts.append("- 1-BASSO (docs) -> vai")
        context_parts.append("- 2-MEDIO (feature) -> Guardiana verifica")
        context_parts.append("- 3-ALTO (deploy/auth) -> Guardiana + Rafa")
        context_parts.append("")

        # PROMPT_RIPRESA (stato attuale)
        context_parts.append("## PROMPT RIPRESA - Stato Attuale")
        context_parts.append(prompt_ripresa)
        context_parts.append("")

        # Footer
        context_parts.append("---")
        context_parts.append("**Pronta!** Rafa, cosa facciamo oggi?")

        context_md = "\n".join(context_parts)

        # Output JSON per hook
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
