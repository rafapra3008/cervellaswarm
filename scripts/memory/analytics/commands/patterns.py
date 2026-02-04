#!/usr/bin/env python3
"""
Command: patterns - Pattern di errori
"""

__version__ = "2.2.0"
__version_date__ = "2026-02-04"

import sys
from pathlib import Path

# Setup path per importare common
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from common.db import connect_db
from common.colors import get_severity_color, RESET, BOLD, DIM


def cmd_patterns():
    """Mostra pattern di errori."""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            pattern_name, pattern_type, severity_level,
            occurrence_count, status, last_seen,
            root_cause_hypothesis, mitigation_description
        FROM error_patterns
        ORDER BY
            CASE severity_level
                WHEN 'CRITICAL' THEN 1
                WHEN 'HIGH' THEN 2
                WHEN 'MEDIUM' THEN 3
                WHEN 'LOW' THEN 4
            END,
            occurrence_count DESC
    """)

    patterns = cursor.fetchall()

    print()
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║  🔍 ERROR PATTERNS                                               ║")
    print("╠══════════════════════════════════════════════════════════════════╣")
    print()

    if not patterns:
        print(f"  {DIM}Nessun pattern trovato.{RESET}")
        print()
    else:
        for i, pattern in enumerate(patterns, 1):
            color = get_severity_color(pattern['severity_level'])
            status_icon = "🔴" if pattern['status'] == 'ACTIVE' else "✅"

            print(f"{BOLD}{i}. {status_icon} {color}[{pattern['severity_level']}]{RESET} {pattern['pattern_name']}")
            print(f"   Type: {pattern['pattern_type']} | Occurrences: {pattern['occurrence_count']}")
            print(f"   Last Seen: {pattern['last_seen'][:19]}")

            if pattern['root_cause_hypothesis']:
                print(f"   Root Cause: {pattern['root_cause_hypothesis'][:70]}")

            if pattern['mitigation_description']:
                print(f"   Mitigation: {pattern['mitigation_description'][:70]}")

            print()

    print("╚══════════════════════════════════════════════════════════════════╝")
    print()

    conn.close()
