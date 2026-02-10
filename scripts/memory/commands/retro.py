"""Analytics retro command - Wrapper per weekly retrospective."""

__version__ = "2.2.0"
__version_date__ = "2026-02-04"

import sys
from pathlib import Path

# Aggiungi path per import
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from common.colors import RED, YELLOW, CYAN, RESET

# Import del modulo retro
try:
    from scripts.memory.retro import generate_retro
    HAS_RETRO = True
except ImportError:
    HAS_RETRO = False

# Rich check
try:
    from rich.console import Console
    HAS_RICH = True
except ImportError:
    HAS_RICH = False


def cmd_retro():
    """Genera weekly retrospective report."""
    if not HAS_RETRO:
        print(f"\n{RED}❌ Modulo retro non disponibile!{RESET}")
        print(f"{YELLOW}Suggerimento:{RESET} Usa 'python -m scripts.memory.retro.cli'\n")
        return

    if not HAS_RICH:
        print(f"\n{RED}❌ Comando 'retro' richiede Rich installato!{RESET}")
        print(f"{YELLOW}Suggerimento:{RESET} pip install rich")
        print(f"{CYAN}Alternativa:{RESET} Usa 'python -m scripts.memory.retro.cli' che supporta fallback plain text\n")
        return

    # Genera retrospective usando il modulo dedicato
    generate_retro(days=7, save_to_file=False, quiet=False)
