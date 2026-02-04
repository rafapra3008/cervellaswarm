"""
CervellaSwarm Weekly Retrospective - Suggestions Module

Suggerimento lezioni basate su pattern ripetuti e agenti con basso success rate.
"""

__version__ = "2.2.0"
__version_date__ = "2026-02-04"

import sqlite3
from typing import List, Tuple


def suggest_new_lessons(conn: sqlite3.Connection, period_start: str) -> List[Tuple[str, int, str]]:
    """
    Suggerisce nuove lezioni basandosi su pattern errori ripetuti.

    Analizza:
    1. Pattern errori con count >= 3 senza lezione associata
    2. Agenti con success rate < 80%

    Args:
        conn: Connessione database
        period_start: Data inizio periodo (ISO format)

    Returns:
        Lista di tuple (tipo_suggerimento, valore, descrizione)
    """
    cursor = conn.cursor()
    suggestions = []

    # 1. Pattern ripetuti senza lezione documentata
    cursor.execute("""
        SELECT ep.pattern_name, ep.occurrence_count
        FROM error_patterns ep
        WHERE ep.status = 'ACTIVE'
          AND ep.occurrence_count >= 3
          AND NOT EXISTS (
              SELECT 1 FROM lessons_learned ll
              WHERE ll.pattern LIKE '%' || ep.pattern_name || '%'
          )
        ORDER BY ep.occurrence_count DESC
        LIMIT 5
    """)
    patterns = cursor.fetchall()

    for pattern in patterns:
        suggestions.append((
            'pattern',
            pattern['occurrence_count'],
            f"Pattern '{pattern['pattern_name']}' ripetuto {pattern['occurrence_count']} volte senza lezione"
        ))

    # 2. Agenti con basso success rate
    cursor.execute("""
        SELECT
            agent_name,
            COUNT(*) as total,
            SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successes,
            ROUND(100.0 * SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) / COUNT(*), 1) as success_rate
        FROM swarm_events
        WHERE datetime(timestamp) >= datetime(?)
          AND agent_name IS NOT NULL
        GROUP BY agent_name
        HAVING total >= 5 AND success_rate < 80
        ORDER BY success_rate ASC
        LIMIT 3
    """, (period_start,))
    low_performers = cursor.fetchall()

    for agent in low_performers:
        suggestions.append((
            'agent',
            int(agent['success_rate']),
            f"Agente '{agent['agent_name']}' con {agent['success_rate']}% success rate ({agent['total']} task)"
        ))

    return suggestions
