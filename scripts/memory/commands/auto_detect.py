"""
Analytics auto-detect command - Re-export from analytics module.

La versione canonica vive in scripts/memory/analytics/commands/auto_detect.py.
Questo file esiste per backward compatibility.

Sessione 341 - Consolidamento duplicazione.
"""

from scripts.memory.analytics.commands.auto_detect import cmd_auto_detect

__all__ = ["cmd_auto_detect"]
