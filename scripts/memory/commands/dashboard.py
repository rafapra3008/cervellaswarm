"""
Analytics dashboard command - Re-export from analytics module.

La versione canonica vive in scripts/memory/analytics/commands/dashboard.py.
Questo file esiste per backward compatibility.

Sessione 341 - Consolidamento duplicazione.
"""

from scripts.memory.analytics.commands.dashboard import cmd_dashboard

__all__ = ["cmd_dashboard"]
