#!/usr/bin/env python3
"""
CervellaSwarm Dashboard - CLI Entry Point

Entry point principale della dashboard. Gestisce argomenti CLI e
modalità di esecuzione (single shot, watch mode, JSON output).

Usage:
    python -m scripts.swarm.dashboard.cli              # Singola visualizzazione
    python -m scripts.swarm.dashboard.cli --watch      # Refresh continuo
    python -m scripts.swarm.dashboard.cli --json       # Output JSON

Responsabilità:
- Parsing argomenti CLI
- Watch mode con refresh automatico
- Gestione Ctrl+C e cleanup
- Interfaccia utente terminale
"""

__version__ = "2.3.0"
__version_date__ = "2026-02-04"

import sys
import time
import argparse
from pathlib import Path

# Import dal render layer
from .render import render_dashboard, render_json, colorize, Colors

# Import task_manager dal nostro sistema
try:
    from task_manager import list_tasks
except ImportError:
    # Fallback se non siamo nella directory giusta
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from task_manager import list_tasks


def clear_screen():
    """Pulisce lo schermo del terminale."""
    print('\033[2J\033[H', end='')


def main():
    """Entry point principale."""
    parser = argparse.ArgumentParser(
        description='CervellaSwarm Dashboard - Monitoring in tempo reale dello sciame',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s              # Visualizzazione singola
  %(prog)s --watch      # Refresh continuo (2s)
  %(prog)s --json       # Output JSON per script
        """
    )

    parser.add_argument(
        '--watch',
        action='store_true',
        help='Refresh continuo ogni 2 secondi'
    )

    parser.add_argument(
        '--json',
        action='store_true',
        help='Output in formato JSON'
    )

    parser.add_argument(
        '--interval',
        type=int,
        default=2,
        help='Intervallo di refresh in secondi (default: 2)'
    )

    parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s {__version__} ({__version_date__})'
    )

    args = parser.parse_args()

    try:
        if args.watch:
            # Watch mode: refresh continuo
            print(colorize("\n🐝 CervellaSwarm Dashboard - Watch Mode (Ctrl+C per uscire)\n", Colors.BRIGHT_CYAN))

            while True:
                tasks = list_tasks()

                clear_screen()

                if args.json:
                    print(render_json(tasks))
                else:
                    print(render_dashboard(tasks))

                time.sleep(args.interval)
        else:
            # Single shot mode
            tasks = list_tasks()

            if args.json:
                print(render_json(tasks))
            else:
                print(render_dashboard(tasks))

    except KeyboardInterrupt:
        print(colorize("\n\n👋 Dashboard chiusa. Arrivederci!\n", Colors.BRIGHT_CYAN))
        sys.exit(0)

    except Exception as e:
        print(colorize(f"\n❌ Errore: {e}\n", Colors.BRIGHT_RED), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
