#!/usr/bin/env python3
"""
CervellaSwarm Analytics CLI - Entry Point

Usage:
    python analytics/cli.py summary
    python analytics/cli.py dashboard
    python -m scripts.memory.analytics.cli summary
"""

__version__ = "2.2.0"
__version_date__ = "2026-02-04"

import argparse
import sys

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


def main():
    """Entry point CLI."""
    parser = argparse.ArgumentParser(
        description="CervellaSwarm Analytics - Sistema di Reporting",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Comandi disponibili:
  summary      - Overview generale del sistema
  lessons      - Lista tutte le lezioni apprese
  events       - Mostra ultimi eventi (default: 10)
  agents       - Statistiche per agente
  patterns     - Pattern di errori attivi
  dashboard    - Dashboard live con Rich
  auto-detect  - Auto-rileva pattern errori
  retro        - Weekly retrospective

Esempi:
  python analytics/cli.py summary
  python analytics/cli.py dashboard
  python analytics/cli.py events -n 20
  python analytics/cli.py auto-detect -d 14
        """
    )

    parser.add_argument(
        'command',
        choices=['summary', 'lessons', 'events', 'agents', 'patterns',
                 'dashboard', 'auto-detect', 'retro'],
        help='Comando da eseguire'
    )

    parser.add_argument(
        '-n', '--limit',
        type=int,
        default=10,
        help='Numero di eventi da mostrare (solo per "events")'
    )

    parser.add_argument(
        '-d', '--days',
        type=int,
        default=7,
        help='Numero di giorni da analizzare (solo per "auto-detect")'
    )

    parser.add_argument(
        '-v', '--version',
        action='version',
        version=f'%(prog)s {__version__} ({__version_date__})'
    )

    args = parser.parse_args()

    # Dispatch comando
    dispatch = {
        'summary': cmd_summary,
        'lessons': cmd_lessons,
        'events': lambda: cmd_events(args.limit),
        'agents': cmd_agents,
        'patterns': cmd_patterns,
        'dashboard': cmd_dashboard,
        'auto-detect': lambda: cmd_auto_detect(args.days),
        'retro': cmd_retro,
    }

    dispatch[args.command]()


if __name__ == '__main__':
    main()
