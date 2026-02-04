"""
CervellaSwarm Analytics - Auto-Detect Command

Auto-rileva pattern di errori ricorrenti.
"""

__version__ = "2.2.0"
__version_date__ = "2026-02-04"

import sys
from pathlib import Path

# Setup path per import
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from common.colors import RED, GREEN, YELLOW, CYAN, BOLD, RESET
from ..helpers import HAS_RICH, console, Table, box

# Pattern detector import (opzionale)
try:
    from pattern_detector import detect_error_patterns, fetch_recent_errors, save_patterns_to_db
    PATTERN_DETECTOR_AVAILABLE = True
except ImportError:
    PATTERN_DETECTOR_AVAILABLE = False
    detect_error_patterns = None
    fetch_recent_errors = None
    save_patterns_to_db = None


def cmd_auto_detect(days: int = 7):
    """Auto-rileva pattern di errori ricorrenti."""
    if not PATTERN_DETECTOR_AVAILABLE:
        print(f"\n{RED}pattern_detector.py non disponibile!{RESET}")
        print(f"{YELLOW}Suggerimento:{RESET} Verifica che pattern_detector.py sia nella stessa directory\n")
        return

    print(f"\n{CYAN}Auto-detection pattern errori (ultimi {days} giorni)...{RESET}\n")

    # Fetch errori
    errors = fetch_recent_errors(days=days)

    if not errors:
        print(f"{GREEN}Nessun errore trovato! Sistema stabile.{RESET}\n")
        return

    print(f"   Trovati {YELLOW}{len(errors)}{RESET} errori")

    # Rileva pattern
    print(f"\n{CYAN}Rilevamento pattern in corso...{RESET}")
    patterns = detect_error_patterns(
        errors=errors,
        similarity_threshold=0.7,
        min_occurrences=3
    )

    if not patterns:
        print(f"{GREEN}Nessun pattern ricorrente rilevato (soglia: 3+ occorrenze){RESET}\n")
        return

    print(f"   Rilevati {BOLD}{YELLOW}{len(patterns)}{RESET} pattern\n")

    # Salva nel database
    print(f"{CYAN}Salvataggio pattern nel database...{RESET}")
    new, updated = save_patterns_to_db(patterns)
    print(f"   {GREEN}Nuovi: {new} | Aggiornati: {updated}{RESET}\n")

    # Output pattern
    if HAS_RICH:
        _print_patterns_rich(patterns)
    else:
        _print_patterns_plain(patterns)


def _print_patterns_rich(patterns):
    """Output Rich per pattern rilevati."""
    patterns_table = Table(
        title="PATTERN RILEVATI",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold cyan"
    )
    patterns_table.add_column("#", justify="right", style="dim")
    patterns_table.add_column("Severity", justify="center")
    patterns_table.add_column("Pattern Name", style="white")
    patterns_table.add_column("Occorrenze", justify="right", style="yellow")

    for i, pattern in enumerate(patterns, 1):
        severity_color = {
            'CRITICAL': 'red',
            'HIGH': 'yellow',
            'MEDIUM': 'cyan',
            'LOW': 'green'
        }.get(pattern['severity_level'], 'white')

        patterns_table.add_row(
            str(i),
            f"[{severity_color}]{pattern['severity_level']}[/{severity_color}]",
            pattern['pattern_name'][:60],
            str(pattern['occurrence_count'])
        )

    console.print(patterns_table)
    console.print("\n[green]Pattern detection completato![/green]\n")


def _print_patterns_plain(patterns):
    """Output plain text per pattern rilevati."""
    print("\nPATTERN RILEVATI")
    print("-" * 80)
    for i, pattern in enumerate(patterns, 1):
        print(f"{i}. [{pattern['severity_level']}] {pattern['pattern_name'][:60]}")
        print(f"   Occorrenze: {pattern['occurrence_count']}")
    print(f"\n{GREEN}Pattern detection completato!{RESET}\n")
