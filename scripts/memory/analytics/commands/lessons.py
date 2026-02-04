#!/usr/bin/env python3
"""
Command: lessons - Lista lezioni apprese
"""

__version__ = "2.2.0"
__version_date__ = "2026-02-04"

import sys
from pathlib import Path

# Setup path per importare common
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from common.db import connect_db
from common.colors import get_severity_color, RESET, BOLD, DIM


def cmd_lessons():
    """Lista tutte le lezioni apprese ordinate per severity."""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            pattern, category, severity, status,
            prevention, occurrence_count, time_wasted_minutes
        FROM lessons_learned
        ORDER BY
            CASE severity
                WHEN 'CRITICAL' THEN 1
                WHEN 'HIGH' THEN 2
                WHEN 'MEDIUM' THEN 3
                WHEN 'LOW' THEN 4
            END,
            occurrence_count DESC
    """)

    lessons = cursor.fetchall()

    print()
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║  📚 LESSONS LEARNED                                              ║")
    print("╠══════════════════════════════════════════════════════════════════╣")
    print()

    if not lessons:
        print(f"  {DIM}Nessuna lezione trovata.{RESET}")
        print()
    else:
        for i, lesson in enumerate(lessons, 1):
            color = get_severity_color(lesson['severity'])
            status_icon = "🔴" if lesson['status'] == 'ACTIVE' else "✅"

            print(f"{BOLD}{i}. {status_icon} {color}[{lesson['severity']}]{RESET} {lesson['pattern']}")
            print(f"   Category: {lesson['category'] or 'N/A'}")
            print(f"   Prevention: {lesson['prevention'][:80] or 'N/A'}")
            print(f"   Occurrences: {lesson['occurrence_count']} | Time Wasted: {lesson['time_wasted_minutes'] or 0} min")
            print()

    print("╚══════════════════════════════════════════════════════════════════╝")
    print()

    conn.close()
