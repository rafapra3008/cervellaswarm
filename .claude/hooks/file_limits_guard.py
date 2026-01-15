#!/usr/bin/env python3
"""
Hook SessionEnd - File Limits Guard

Verifica che i file critici non superino i limiti:
- PROMPT_RIPRESA_*.md: max 150 righe
- oggi.md: max 60 righe
- stato.md: max 500 righe

Se superati, genera WARNING per archiviazione.

Versione: 1.0.0
Data: 2026-01-15
Cervella & Rafa

Sessione 216 - Context Mesh Implementation
"""

import json
import sys
from pathlib import Path

# Path progetto
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Limiti OBBLIGATORI
LIMITS = {
    "PROMPT_RIPRESA": 150,
    "oggi.md": 60,
    "stato.md": 500
}

# File da controllare
FILES_TO_CHECK = [
    # PROMPT_RIPRESA per progetto
    (PROJECT_ROOT / ".sncp/progetti/cervellaswarm/PROMPT_RIPRESA_cervellaswarm.md", "PROMPT_RIPRESA"),
    (PROJECT_ROOT / ".sncp/progetti/miracollo/PROMPT_RIPRESA_miracollo.md", "PROMPT_RIPRESA"),
    (PROJECT_ROOT / ".sncp/progetti/contabilita/PROMPT_RIPRESA_contabilita.md", "PROMPT_RIPRESA"),
    # oggi.md globale
    (PROJECT_ROOT / ".sncp/stato/oggi.md", "oggi.md"),
    # stato.md per progetto
    (PROJECT_ROOT / ".sncp/progetti/cervellaswarm/stato.md", "stato.md"),
    (PROJECT_ROOT / ".sncp/progetti/miracollo/stato.md", "stato.md"),
    (PROJECT_ROOT / ".sncp/progetti/contabilita/stato.md", "stato.md"),
]


def count_lines(file_path: Path) -> int:
    """Conta righe di un file."""
    try:
        if file_path.exists():
            return len(file_path.read_text(encoding='utf-8').split('\n'))
        return 0
    except Exception:
        return 0


def check_limits() -> list:
    """Verifica limiti file. Ritorna lista di warning."""
    warnings = []

    for file_path, limit_type in FILES_TO_CHECK:
        if not file_path.exists():
            continue

        lines = count_lines(file_path)
        limit = LIMITS[limit_type]

        if lines > limit:
            warnings.append({
                "file": str(file_path.relative_to(PROJECT_ROOT)),
                "lines": lines,
                "limit": limit,
                "over": lines - limit
            })
        elif lines > limit * 0.9:  # Warning al 90%
            warnings.append({
                "file": str(file_path.relative_to(PROJECT_ROOT)),
                "lines": lines,
                "limit": limit,
                "warning": "quasi al limite"
            })

    return warnings


def main():
    """Entry point hook."""
    try:
        warnings = check_limits()

        if warnings:
            # Formatta warning
            warning_lines = ["## FILE LIMITS WARNING"]
            warning_lines.append("")

            for w in warnings:
                if "over" in w:
                    warning_lines.append(f"- **{w['file']}**: {w['lines']} righe (LIMITE {w['limit']}!) - ARCHIVIARE!")
                else:
                    warning_lines.append(f"- {w['file']}: {w['lines']}/{w['limit']} righe (90% limite)")

            warning_lines.append("")
            warning_lines.append("**AZIONE:** Archivia sessioni vecchie in `.sncp/progetti/*/archivio/`")

            context_md = "\n".join(warning_lines)
        else:
            context_md = "File Limits OK - tutti i file sotto il limite."

        result = {
            "hookSpecificOutput": {
                "hookEventName": "SessionEnd",
                "additionalContext": context_md
            }
        }

        print(json.dumps(result))
        sys.exit(0)

    except Exception as e:
        error_result = {
            "hookSpecificOutput": {
                "hookEventName": "SessionEnd",
                "additionalContext": f"File Limits Guard: errore - {str(e)}"
            }
        }
        print(json.dumps(error_result))
        sys.exit(0)


if __name__ == "__main__":
    main()
