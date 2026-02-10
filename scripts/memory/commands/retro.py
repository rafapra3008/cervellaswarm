"""
Analytics retro command - Re-export from analytics module.

La versione canonica vive in scripts/memory/analytics/commands/retro.py.
Questo file esiste per backward compatibility.

Sessione 341 - Consolidamento duplicazione.
"""

from scripts.memory.analytics.commands.retro import cmd_retro

__all__ = ["cmd_retro"]
