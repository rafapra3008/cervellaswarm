"""
CervellaSwarm Weekly Retrospective - Data Extraction Module

Funzioni per estrarre dati dal database (NO printing, solo return).

SECURITY FIX v2.2.0: Tutte le query SQL ora usano parametrized queries (no f-string).
"""

__version__ = "2.2.0"
__version_date__ = "2026-02-04"

import sqlite3
from typing import Dict, List, Any


def fetch_metrics(conn: sqlite3.Connection, period_start: str) -> Dict[str, Any]:
    """
    Estrae metriche chiave dal periodo specificato.

    Args:
        conn: Connessione database
        period_start: Data inizio periodo (ISO format)

    Returns:
        Dict con total, successes, failures, success_rate
    """
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            COUNT(*) as total,
            SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successes,
            SUM(CASE WHEN success = 0 THEN 1 ELSE 0 END) as failures
        FROM swarm_events
        WHERE datetime(timestamp) >= datetime(?)
    """, (period_start,))

    row = cursor.fetchone()

    total = row['total']
    successes = row['successes']
    failures = row['failures']
    success_rate = (successes / total * 100) if total > 0 else 0

    return {
        'total': total,
        'successes': successes,
        'failures': failures,
        'success_rate': success_rate
    }


def fetch_top_patterns(conn: sqlite3.Connection, limit: int = 3) -> List[Dict[str, Any]]:
    """
    Estrae top N pattern errori attivi, ordinati per severity e count.

    Args:
        conn: Connessione database
        limit: Numero massimo di pattern da ritornare

    Returns:
        Lista di dict con pattern_name, severity_level, occurrence_count
    """
    cursor = conn.cursor()

    cursor.execute("""
        SELECT pattern_name, severity_level, occurrence_count
        FROM error_patterns
        WHERE status = 'ACTIVE'
        ORDER BY
            CASE severity_level
                WHEN 'CRITICAL' THEN 1
                WHEN 'HIGH' THEN 2
                WHEN 'MEDIUM' THEN 3
                WHEN 'LOW' THEN 4
            END,
            occurrence_count DESC
        LIMIT ?
    """, (limit,))

    return [dict(row) for row in cursor.fetchall()]


def fetch_lessons(conn: sqlite3.Connection, period_start: str, limit: int = 5) -> List[Dict[str, Any]]:
    """
    Estrae lezioni apprese nel periodo specificato.

    Args:
        conn: Connessione database
        period_start: Data inizio periodo (ISO format)
        limit: Numero massimo di lezioni da ritornare

    Returns:
        Lista di dict con pattern, severity
    """
    cursor = conn.cursor()

    cursor.execute("""
        SELECT pattern, severity
        FROM lessons_learned
        WHERE datetime(created_at) >= datetime(?)
        ORDER BY
            CASE severity
                WHEN 'CRITICAL' THEN 1
                WHEN 'HIGH' THEN 2
                WHEN 'MEDIUM' THEN 3
                WHEN 'LOW' THEN 4
            END
        LIMIT ?
    """, (period_start, limit))

    return [dict(row) for row in cursor.fetchall()]


def fetch_agent_breakdown(conn: sqlite3.Connection, period_start: str, limit: int = 5) -> List[Dict[str, Any]]:
    """
    Estrae breakdown attività per agente (top N).

    Args:
        conn: Connessione database
        period_start: Data inizio periodo (ISO format)
        limit: Numero massimo di agenti da ritornare

    Returns:
        Lista di dict con agent_name, total, successes, failures, avg_duration
    """
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            agent_name,
            COUNT(*) as total,
            SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successes,
            SUM(CASE WHEN success = 0 THEN 1 ELSE 0 END) as failures,
            ROUND(AVG(duration_ms), 0) as avg_duration
        FROM swarm_events
        WHERE datetime(timestamp) >= datetime(?)
          AND agent_name IS NOT NULL
        GROUP BY agent_name
        ORDER BY total DESC
        LIMIT ?
    """, (period_start, limit))

    return [dict(row) for row in cursor.fetchall()]


def generate_recommendations(metrics: Dict[str, Any], conn: sqlite3.Connection) -> List[str]:
    """
    Genera raccomandazioni automatiche basate su metriche e stato sistema.

    Args:
        metrics: Dict con total, successes, failures, success_rate
        conn: Connessione database

    Returns:
        Lista di raccomandazioni (stringhe con emoji)
    """
    recommendations = []
    cursor = conn.cursor()

    # Success rate basso
    if metrics['success_rate'] < 80:
        recommendations.append("⚠️  Success rate < 80% - Investigare cause degli errori")

    # Alto numero di errori
    if metrics['failures'] > 10:
        recommendations.append("🔍 Alto numero di errori - Eseguire auto-detect per pattern")

    # Lezioni ACTIVE
    cursor.execute("SELECT COUNT(*) as active FROM lessons_learned WHERE status = 'ACTIVE'")
    active_lessons_count = cursor.fetchone()['active']
    if active_lessons_count > 5:
        recommendations.append(f"📚 {active_lessons_count} lezioni ACTIVE - Pianificare fix")

    # Pattern ACTIVE
    cursor.execute("SELECT COUNT(*) as active FROM error_patterns WHERE status = 'ACTIVE'")
    active_patterns_count = cursor.fetchone()['active']
    if active_patterns_count > 3:
        recommendations.append(f"🔴 {active_patterns_count} pattern ACTIVE - Review necessaria")

    # Sistema inattivo
    if metrics['total'] == 0:
        recommendations.append("⚪ Nessun evento in questo periodo - Sistema inattivo")
    elif not recommendations:
        recommendations.append("✅ Sistema stabile - Continuare così!")

    return recommendations


def generate_next_steps(conn: sqlite3.Connection, metrics: Dict[str, Any]) -> List[str]:
    """
    Genera prossimi passi suggeriti basati su stato sistema.

    Args:
        conn: Connessione database
        metrics: Dict con metriche (total, failures)

    Returns:
        Lista di step suggeriti (stringhe)
    """
    next_steps = []
    cursor = conn.cursor()

    # Count pattern attivi
    cursor.execute("SELECT COUNT(*) as active FROM error_patterns WHERE status = 'ACTIVE'")
    active_patterns_count = cursor.fetchone()['active']

    # Count lezioni attive
    cursor.execute("SELECT COUNT(*) as active FROM lessons_learned WHERE status = 'ACTIVE'")
    active_lessons_count = cursor.fetchone()['active']

    if active_patterns_count > 0:
        next_steps.append("1. Review pattern attivi con `analytics.py patterns`")

    if active_lessons_count > 0:
        next_steps.append("2. Review lezioni attive con `analytics.py lessons`")

    if metrics['failures'] > 5:
        next_steps.append("3. Analizzare ultimi errori con `analytics.py events -n 20`")

    if not next_steps:
        next_steps.append("✅ Nessuna azione richiesta - Sistema OK!")

    return next_steps
