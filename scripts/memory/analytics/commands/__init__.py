"""
CervellaSwarm Analytics - Commands Module

Tutti i comandi CLI disponibili.
"""

from .summary import cmd_summary
from .lessons import cmd_lessons
from .events import cmd_events
from .agents import cmd_agents
from .patterns import cmd_patterns
from .dashboard import cmd_dashboard
from .auto_detect import cmd_auto_detect
from .retro import cmd_retro

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
