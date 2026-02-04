#!/usr/bin/env python3
"""
Command: agents - Statistiche per agente
"""

__version__ = "2.2.0"
__version_date__ = "2026-02-04"

import sys
from pathlib import Path

# Setup path per importare common
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from common.db import connect_db
from common.colors import GREEN, YELLOW, RED, RESET, BOLD, DIM


def cmd_agents():
    """Mostra statistiche per agente."""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            agent_name,
            COUNT(*) as total_tasks,
            SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successes,
            SUM(CASE WHEN success = 0 THEN 1 ELSE 0 END) as failures,
            AVG(duration_ms) as avg_duration
        FROM swarm_events
        WHERE agent_name IS NOT NULL
        GROUP BY agent_name
        ORDER BY total_tasks DESC
    """)

    agents = cursor.fetchall()

    print()
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║  👥 AGENT STATISTICS                                             ║")
    print("╠══════════════════════════════════════════════════════════════════╣")
    print()

    if not agents:
        print(f"  {DIM}Nessun agente trovato.{RESET}")
        print()
    else:
        # Header
        print(f"  {BOLD}{'Agent'.ljust(20)} {'Tasks'.ljust(8)} {'Success'.ljust(10)} {'Failures'.ljust(10)} {'Avg Duration'.ljust(15)}{RESET}")
        print(f"  {'-' * 65}")

        for agent in agents:
            name = (agent['agent_name'] or "N/A")[:20].ljust(20)
            total = str(agent['total_tasks']).ljust(8)
            success = str(agent['successes']).ljust(10)
            failures = str(agent['failures']).ljust(10)

            avg_dur = agent['avg_duration']
            avg_str = f"{int(avg_dur)}ms" if avg_dur else "N/A"
            avg_str = avg_str.ljust(15)

            # Colore successi/fallimenti
            if agent['failures'] == 0:
                color = GREEN
            elif agent['failures'] > agent['successes']:
                color = RED
            else:
                color = YELLOW

            print(f"  {name} {total} {color}{success}{RESET} {color}{failures}{RESET} {avg_str}")

        print()

    print("╚══════════════════════════════════════════════════════════════════╝")
    print()

    conn.close()
