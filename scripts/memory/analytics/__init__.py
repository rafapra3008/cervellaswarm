"""
CervellaSwarm Analytics - Sistema di Reporting Modulare

Analizza il database swarm_memory.db e mostra metriche/statistiche.

Usage:
    python -m scripts.memory.analytics summary
    python -m scripts.memory.analytics dashboard
"""

__version__ = "2.2.0"
__version_date__ = "2026-02-04"

from .commands import (
    cmd_summary,
    cmd_lessons,
    cmd_events,
    cmd_agents,
    cmd_patterns,
    cmd_dashboard,
    cmd_auto_detect,
    cmd_retro,
)

__all__ = [
    "cmd_summary",
    "cmd_lessons",
    "cmd_events",
    "cmd_agents",
    "cmd_patterns",
    "cmd_dashboard",
    "cmd_auto_detect",
    "cmd_retro",
]
