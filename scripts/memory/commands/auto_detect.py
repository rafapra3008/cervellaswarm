"""Analytics auto-detect command - Auto-detect error patterns."""

__version__ = "2.2.0"
__version_date__ = "2026-02-04"

import sys
from pathlib import Path

# Aggiungi path per import
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from common.colors import RED, GREEN, YELLOW, CYAN, BOLD, RESET

# Pattern detector import (opzionale)
try:
    from scripts.memory.pattern_detector import (
        detect_error_patterns,
        fetch_recent_errors,
        save_patterns_to_db
    )
    HAS_PATTERN_DETECTOR = True
except ImportError:
    HAS_PATTERN_DETECTOR = False
    detect_error_patterns = None
    fetch_recent_errors = None
    save_patterns_to_db = None

# Rich import opzionale
try:
    from rich.console import Console
    from rich.table import Table
    from rich import box
    HAS_RICH = True
    console = Console()
except ImportError:
    HAS_RICH = False
    console = None


def cmd_auto_detect(days: int = 7):
    """Auto-rileva pattern di errori ricorrenti."""
    if not HAS_PATTERN_DETECTOR:
        print(f"\n{RED}❌ pattern_detector.py non disponibile!{RESET}")
        print(f"{YELLOW}Suggerimento:{RESET} Verifica che pattern_detector.py sia nella stessa directory\n")
        return

    print(f"\n{CYAN}🔍 Auto-detection pattern errori (ultimi {days} giorni)...{RESET}\n")

    # Fetch errori
    errors = fetch_recent_errors(days=days)

    if not errors:
        print(f"{GREEN}✅ Nessun errore trovato! Sistema stabile.{RESET}\n")
        return

    print(f"   Trovati {YELLOW}{len(errors)}{RESET} errori")

    # Rileva pattern
    print(f"\n{CYAN}🔎 Rilevamento pattern in corso...{RESET}")
    patterns = detect_error_patterns(
        errors=errors,
        similarity_threshold=0.7,
        min_occurrences=3
    )

    if not patterns:
        print(f"{GREEN}✅ Nessun pattern ricorrente rilevato (soglia: 3+ occorrenze){RESET}\n")
        return

    print(f"   Rilevati {BOLD}{YELLOW}{len(patterns)}{RESET} pattern\n")

    # Salva nel database
    print(f"{CYAN}💾 Salvataggio pattern nel database...{RESET}")
    new, updated = save_patterns_to_db(patterns)
    print(f"   {GREEN}✅ Nuovi: {new} | Aggiornati: {updated}{RESET}\n")

    # Pattern rilevati (Rich se disponibile, altrimenti plain text)
    if HAS_RICH:
        patterns_table = Table(
            title="📋 PATTERN RILEVATI",
            box=box.ROUNDED,
            show_header=True,
            header_style="bold cyan"
        )
        patterns_table.add_column("#", justify="right", style="dim")
        patterns_table.add_column("Severity", justify="center")
        patterns_table.add_column("Pattern Name", style="white")
        patterns_table.add_column("Occorrenze", justify="right", style="yellow")

        for i, pattern in enumerate(patterns, 1):
            severity_emoji = {
                'CRITICAL': '🔴',
                'HIGH': '🟠',
                'MEDIUM': '🟡',
                'LOW': '🟢'
            }.get(pattern['severity_level'], '⚪')

            severity_color = {
                'CRITICAL': 'red',
                'HIGH': 'yellow',
                'MEDIUM': 'cyan',
                'LOW': 'green'
            }.get(pattern['severity_level'], 'white')

            patterns_table.add_row(
                str(i),
                f"[{severity_color}]{severity_emoji} {pattern['severity_level']}[/{severity_color}]",
                pattern['pattern_name'][:60],
                str(pattern['occurrence_count'])
            )

        console.print(patterns_table)
        console.print("\n[green]✅ Pattern detection completato![/green]\n")
    else:
        # Plain text fallback
        print("\n📋 PATTERN RILEVATI")
        print("-" * 80)
        for i, pattern in enumerate(patterns, 1):
            severity_emoji = {
                'CRITICAL': '🔴',
                'HIGH': '🟠',
                'MEDIUM': '🟡',
                'LOW': '🟢'
            }.get(pattern['severity_level'], '⚪')

            print(f"{i}. {severity_emoji} [{pattern['severity_level']}] {pattern['pattern_name'][:60]}")
            print(f"   Occorrenze: {pattern['occurrence_count']}")
        print(f"\n{GREEN}✅ Pattern detection completato!{RESET}\n")
