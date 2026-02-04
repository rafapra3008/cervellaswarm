#!/usr/bin/env python3
"""
Command: summary - Overview generale del sistema
"""

__version__ = "2.2.0"
__version_date__ = "2026-02-04"

import sys
from pathlib import Path

# Setup path per importare common
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from common.db import connect_db
from common.colors import get_severity_color, RESET

# Import helpers da modulo parent
from ..helpers import HAS_RICH, console


def cmd_summary():
    """Mostra overview generale del sistema."""
    conn = connect_db()
    cursor = conn.cursor()

    # Calcola metriche
    cursor.execute("SELECT COUNT(*) as total FROM swarm_events")
    total_events = cursor.fetchone()['total']

    cursor.execute("SELECT COUNT(*) as success FROM swarm_events WHERE success = 1")
    success_count = cursor.fetchone()['success']

    success_rate = (success_count / total_events * 100) if total_events > 0 else 0

    cursor.execute("SELECT COUNT(*) as total FROM lessons_learned")
    total_lessons = cursor.fetchone()['total']

    cursor.execute("SELECT COUNT(*) as active FROM lessons_learned WHERE status = 'ACTIVE'")
    active_lessons = cursor.fetchone()['active']

    cursor.execute("SELECT timestamp FROM swarm_events ORDER BY timestamp DESC LIMIT 1")
    last_event_row = cursor.fetchone()
    last_event = last_event_row['timestamp'] if last_event_row else "N/A"

    # Top 3 lezioni attive
    cursor.execute("""
        SELECT pattern, category, severity
        FROM lessons_learned
        WHERE status = 'ACTIVE'
        ORDER BY
            CASE severity
                WHEN 'CRITICAL' THEN 1
                WHEN 'HIGH' THEN 2
                WHEN 'MEDIUM' THEN 3
                WHEN 'LOW' THEN 4
            END,
            occurrence_count DESC
        LIMIT 3
    """)
    top_lessons = cursor.fetchall()

    # === OUTPUT ===
    print()
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║  🐝 CERVELLASWARM ANALYTICS                                      ║")
    print("╠══════════════════════════════════════════════════════════════════╣")
    print("║                                                                  ║")
    print("║  📊 OVERVIEW                                                     ║")
    print("║  ────────────────────────────────────────────────────           ║")
    print(f"║  Total Events:     {str(total_events).ljust(45)}║")
    print(f"║  Success Rate:     {f'{success_rate:.1f}%'.ljust(45)}║")
    print(f"║  Total Lessons:    {str(total_lessons).ljust(45)}║")
    print(f"║  Active Lessons:   {f'{active_lessons} (da risolvere)'.ljust(45)}║")
    print(f"║  Last Event:       {last_event[:43].ljust(45)}║")
    print("║                                                                  ║")

    if top_lessons:
        print("║  📚 TOP LESSONS ATTIVE                                          ║")
        print("║  ────────────────────────────────────────────────────           ║")
        for lesson in top_lessons:
            severity = lesson['severity']
            color = get_severity_color(severity)
            pattern = lesson['pattern'][:35]
            category = lesson['category'][:20] if lesson['category'] else 'N/A'

            line = f"  [{severity}] {pattern} ({category})"
            # Padding per allineare
            padding = 66 - len(line)
            print(f"║{color}{line}{RESET}{' ' * padding}║")
        print("║                                                                  ║")

    print("╚══════════════════════════════════════════════════════════════════╝")
    print()

    conn.close()
