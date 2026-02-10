"""
CervellaSwarm Analytics - Retro Command

Wrapper per weekly retrospective - RIUSA il modulo retro/ esistente.
"""

__version__ = "2.2.0"
__version_date__ = "2026-02-04"

import sys
from pathlib import Path

# Setup path per import
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from common.colors import RED, YELLOW, CYAN, RESET
from ..helpers import HAS_RICH

# Import modulo retro (riuso, no duplicazione!)
try:
    from scripts.memory.retro import generate_retro
    RETRO_AVAILABLE = True
except ImportError:
    RETRO_AVAILABLE = False
    generate_retro = None


def cmd_retro():
    """Genera weekly retrospective report."""
    if not HAS_RICH:
        print(f"\n{RED}Comando 'retro' richiede Rich installato!{RESET}")
        print(f"{YELLOW}Suggerimento:{RESET} pip install rich")
        print(f"{CYAN}Alternativa:{RESET} Usa 'python -m scripts.memory.retro.cli' per fallback plain text\n")
        return

    if not RETRO_AVAILABLE:
        print(f"\n{RED}Modulo retro non disponibile!{RESET}")
        print(f"{YELLOW}Suggerimento:{RESET} Usa 'python -m scripts.memory.retro.cli'\n")
        return

    # Riusa il modulo retro/ - NO duplicazione codice!
    generate_retro(days=7, save_to_file=False, quiet=False)
