"""
Analytics Commands Package - Modular command handlers.

Comandi disponibili:
- summary: Overview generale del sistema
- lessons: Lista lezioni apprese attive
- events: Ultimi eventi dello sciame
- agents: Statistiche per agente
- patterns: Pattern di errori rilevati
- dashboard: Dashboard live visuale (Rich)
- auto_detect: Auto-rilevamento pattern errori
- retro: Weekly retrospective report
"""

__version__ = "2.2.0"
__version_date__ = "2026-02-04"

from .dashboard import cmd_dashboard
from .auto_detect import cmd_auto_detect
from .retro import cmd_retro

__all__ = [
    "cmd_dashboard",
    "cmd_auto_detect",
    "cmd_retro",
]
