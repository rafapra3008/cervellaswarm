#!/usr/bin/env python3
"""
Hook SessionStart CervellaSwarm - Caricamento Contesto Sciame

Carica automaticamente all'avvio sessione:
- COSTITUZIONE.md (chi siamo - PRIMA DI TUTTO!)
- NORD.md (dove siamo)
- PROMPT_RIPRESA.md (stato attuale)
- Check CODE REVIEW day (Lunedi/Venerdi)
- Reminder regole Sciame

Versione: 2.0.0
Data: 2026-01-14
Cervella & Rafa

v2.0.0 - Aggiunta COSTITUZIONE obbligatoria!
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Path progetto
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Path Costituzione (GLOBALE - vale per TUTTI!)
COSTITUZIONE_PATH = Path.home() / ".claude/COSTITUZIONE.md"


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


def main():
    """Entry point hook."""
    try:
        # PRIMA DI TUTTO: COSTITUZIONE! (chi siamo)
        costituzione = load_file_summary(COSTITUZIONE_PATH, max_lines=150)

        # Carica file chiave progetto
        nord = load_file_summary(PROJECT_ROOT / "NORD.md", max_lines=60)
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

        # COSTITUZIONE - PRIMA DI TUTTO!
        context_parts.append("## COSTITUZIONE - Chi Siamo")
        context_parts.append(costituzione)
        context_parts.append("")

        # CODE REVIEW reminder se lunedi/venerdi
        if is_review_day:
            context_parts.append("## CODE REVIEW DAY!")
            context_parts.append(f"**Oggi e {day_name}** - Giorno di Code Review settimanale!")
            context_parts.append("Chiedi a Rafa se vuole invocare `cervella-reviewer` per audit.")
            context_parts.append("")

        # Reminder Sciame
        context_parts.append("## Tu sei la REGINA!")
        context_parts.append("- 16 membri della famiglia pronti")
        context_parts.append("- 3 Guardiane (Opus) + 12 Worker (Sonnet)")
        context_parts.append("- DELEGA sempre, MAI edit diretti!")
        context_parts.append("")
        context_parts.append("## 3 Livelli Rischio")
        context_parts.append("- 1-BASSO (docs) -> vai")
        context_parts.append("- 2-MEDIO (feature) -> Guardiana verifica")
        context_parts.append("- 3-ALTO (deploy/auth) -> Guardiana + Rafa")
        context_parts.append("")

        # NORD (la bussola)
        context_parts.append("## NORD - La Bussola")
        context_parts.append(nord)
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
