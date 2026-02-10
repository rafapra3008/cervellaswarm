"""
Shared fixtures per tests/memory/.

Sessione 341 - Estratte da test_dashboard_analytics_*.py (DRY).
"""

import pytest
import sqlite3
import tempfile
from pathlib import Path
from datetime import datetime, timedelta


@pytest.fixture
def temp_db():
    """Database temporaneo con schema completo."""
    temp_file = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    db_path = Path(temp_file.name)
    temp_file.close()

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE swarm_events (
            id INTEGER PRIMARY KEY, timestamp TEXT,
            agent_name TEXT, task_description TEXT, project TEXT, success INTEGER
        )
    """)
    cursor.execute("""
        CREATE TABLE error_patterns (
            id INTEGER PRIMARY KEY, pattern_name TEXT, status TEXT, severity_level TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE lessons_learned (
            id INTEGER PRIMARY KEY, trigger TEXT, problem TEXT, solution TEXT, status TEXT
        )
    """)
    conn.commit()
    conn.close()
    yield db_path
    db_path.unlink()


@pytest.fixture
def empty_db(temp_db):
    """Database vuoto (solo schema)."""
    return temp_db


@pytest.fixture
def populated_db(temp_db):
    """Database con dati realistici settimana corrente."""
    conn = sqlite3.connect(temp_db)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    now = datetime.now()
    week_ago = now - timedelta(days=7)
    two_weeks_ago = now - timedelta(days=14)

    events_current_week = [
        (now.isoformat(), "cervella-frontend", "Fix CSS bug", "miracollo", 1),
        ((now - timedelta(days=1)).isoformat(), "cervella-backend", "API endpoint", "miracollo", 1),
        ((now - timedelta(days=2)).isoformat(), "cervella-frontend", "React component", "miracollo", 0),
        ((now - timedelta(days=3)).isoformat(), "cervella-backend", "Database query", "contabilita", 1),
        ((now - timedelta(days=4)).isoformat(), "cervella-tester", "Write tests", "miracollo", 1),
        ((now - timedelta(days=5)).isoformat(), "cervella-frontend", "CSS fix", "miracollo", 1),
        ((now - timedelta(days=6)).isoformat(), "cervella-backend", "API fix", "miracollo", 0),
        ((week_ago + timedelta(hours=1)).isoformat(), "cervella-backend", "Task1", "miracollo", 1),
        ((week_ago + timedelta(hours=2)).isoformat(), "cervella-backend", "Task2", "miracollo", 1),
        ((week_ago + timedelta(hours=3)).isoformat(), "cervella-backend", "Task3", "miracollo", 1),
    ]
    events_old = [
        (two_weeks_ago.isoformat(), "cervella-old", "Old task", "old", 1),
    ]

    for event in events_current_week + events_old:
        cursor.execute("""
            INSERT INTO swarm_events (timestamp, agent_name, task_description, project, success)
            VALUES (?, ?, ?, ?, ?)
        """, event)

    cursor.execute("""
        INSERT INTO error_patterns (pattern_name, status, severity_level)
        VALUES ('Import Error Pattern', 'ACTIVE', 'HIGH'),
               ('DB Connection Pattern', 'ACTIVE', 'CRITICAL'),
               ('Old Pattern', 'RESOLVED', 'LOW')
    """)
    cursor.execute("""
        INSERT INTO lessons_learned (trigger, problem, solution, status)
        VALUES ('Import fail', 'Wrong path', 'Fix import', 'ACTIVE'),
               ('DB error', 'No connection', 'Add pool', 'ACTIVE'),
               ('CSS issue', 'z-index', 'Use layers', 'ACTIVE'),
               ('Old lesson', 'Old', 'Old', 'ARCHIVED')
    """)
    conn.commit()
    conn.close()
    return temp_db
