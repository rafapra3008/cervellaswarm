#!/usr/bin/env python3
"""
Command: events - Mostra ultimi eventi
"""

__version__ = "2.2.0"
__version_date__ = "2026-02-04"

import sys
from pathlib import Path

# Setup path per importare common
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from common.db import connect_db
from common.colors import GREEN, RED, RESET, BOLD, DIM


def cmd_events(limit: int = 10):
    """Mostra gli ultimi N eventi."""
    conn = connect_db()
    cursor = conn.cursor()

    # FIX SQL INJECTION: Query parametrizzata
    cursor.execute("""
        SELECT
            agent_name, event_type, project, success,
            timestamp, task_description, duration_ms
        FROM swarm_events
        ORDER BY timestamp DESC
        LIMIT ?
    """, (limit,))

    events = cursor.fetchall()

    print()
    print("╔══════════════════════════════════════════════════════════════════╗")
    print(f"║  📝 ULTIMI {limit} EVENTI                                             ║")
    print("╠══════════════════════════════════════════════════════════════════╣")
    print()

    if not events:
        print(f"  {DIM}Nessun evento trovato.{RESET}")
        print()
    else:
        for i, event in enumerate(events, 1):
            success_icon = f"{GREEN}✅{RESET}" if event['success'] else f"{RED}❌{RESET}"
            agent = event['agent_name'] or "N/A"
            project = event['project'] or "N/A"
            etype = event['event_type']
            timestamp = event['timestamp'][:19]  # Tronca millisecondi
            duration = f"{event['duration_ms']}ms" if event['duration_ms'] else "N/A"

            print(f"{i}. {success_icon} {BOLD}{agent}{RESET} | {etype}")
            print(f"   {DIM}Project:{RESET} {project} | {DIM}Time:{RESET} {timestamp} | {DIM}Duration:{RESET} {duration}")

            if event['task_description']:
                desc = event['task_description'][:70]
                print(f"   {DIM}Task:{RESET} {desc}")
            print()

    print("╚══════════════════════════════════════════════════════════════════╝")
    print()

    conn.close()
