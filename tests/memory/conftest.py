"""
Shared fixtures per tests/memory/.

Sessione 341 - Estratte da test_dashboard_analytics_*.py (DRY).
Sessione 342 - Aggiunto retro_db con schema completo per modulo retro.
Sessione 345 - Schema canonico unificato (match init_db.py).
"""

import pytest
import sqlite3
import tempfile
from pathlib import Path
from datetime import datetime, timedelta


# =============================================================================
# SCHEMA CANONICO - Match scripts/memory/init_db.py
#
# Divergenze intenzionali rispetto a init_db.py:
# - ID: INTEGER AUTOINCREMENT (test) vs TEXT (produzione) - semplifica insert
# - NOT NULL rilassati: pattern_type, first_seen, last_seen, timestamp(lessons)
#   perche i test inseriscono subset di colonne
# - UNIQUE rimosso da pattern_name (test possono inserire duplicati)
# - DEFAULT aggiunti: event_type='task', duration_ms=0, success=0
#   perche i test spesso non specificano questi campi
# =============================================================================

CANONICAL_SWARM_EVENTS = """
    CREATE TABLE IF NOT EXISTS swarm_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        session_id TEXT,
        event_type TEXT DEFAULT 'task',
        agent_name TEXT,
        agent_role TEXT,
        task_id TEXT,
        parent_task_id TEXT,
        task_description TEXT,
        task_status TEXT,
        duration_ms INTEGER DEFAULT 0,
        success INTEGER DEFAULT 0,
        error_message TEXT,
        project TEXT,
        files_modified TEXT,
        tags TEXT,
        notes TEXT,
        created_at TEXT DEFAULT (datetime('now'))
    )
"""

CANONICAL_ERROR_PATTERNS = """
    CREATE TABLE IF NOT EXISTS error_patterns (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pattern_name TEXT NOT NULL,
        pattern_type TEXT,
        first_seen TEXT,
        last_seen TEXT,
        occurrence_count INTEGER DEFAULT 1,
        severity_level TEXT DEFAULT 'MEDIUM',
        error_signature TEXT,
        affected_agents TEXT,
        affected_files TEXT,
        root_cause_hypothesis TEXT,
        mitigation_applied INTEGER DEFAULT 0,
        mitigation_description TEXT,
        status TEXT DEFAULT 'ACTIVE'
    )
"""

CANONICAL_LESSONS_LEARNED = """
    CREATE TABLE IF NOT EXISTS lessons_learned (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        context TEXT,
        problem TEXT,
        solution TEXT,
        pattern TEXT,
        agents_involved TEXT,
        confidence REAL DEFAULT 0.5,
        times_applied INTEGER DEFAULT 0,
        created_at TEXT DEFAULT (datetime('now')),
        category TEXT,
        severity TEXT DEFAULT 'MEDIUM',
        root_cause TEXT,
        prevention TEXT,
        time_wasted_minutes INTEGER,
        occurrence_count INTEGER DEFAULT 1,
        status TEXT DEFAULT 'ACTIVE',
        related_pattern_id INTEGER,
        project TEXT,
        trigger TEXT,
        example TEXT,
        tags TEXT,
        related_patterns TEXT,
        auto_generated INTEGER DEFAULT 0,
        last_applied TEXT
    )
"""


def _create_canonical_db(db_path: Path):
    """Crea database con schema canonico completo."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(CANONICAL_SWARM_EVENTS)
    cursor.execute(CANONICAL_ERROR_PATTERNS)
    cursor.execute(CANONICAL_LESSONS_LEARNED)
    conn.commit()
    conn.close()


@pytest.fixture
def temp_db():
    """Database temporaneo con schema canonico completo."""
    temp_file = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    db_path = Path(temp_file.name)
    temp_file.close()
    _create_canonical_db(db_path)
    yield db_path
    db_path.unlink()


@pytest.fixture
def retro_db():
    """Database per modulo retro (stesso schema canonico di temp_db)."""
    temp_file = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    db_path = Path(temp_file.name)
    temp_file.close()
    _create_canonical_db(db_path)
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


@pytest.fixture
def populated_retro_db(retro_db):
    """Database popolato per modulo retro con dati test."""
    conn = sqlite3.connect(retro_db)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    now = datetime.now()
    week_ago = now - timedelta(days=7)

    # Eventi misti (success/fail) con duration_ms
    events = [
        (now.isoformat(), "cervella-frontend", "CSS fix", "miracollo", 1, "task", 1200),
        ((now - timedelta(days=1)).isoformat(), "cervella-backend", "API endpoint", "miracollo", 1, "task", 2500),
        ((now - timedelta(days=2)).isoformat(), "cervella-frontend", "Component", "miracollo", 0, "task", 800),
        ((now - timedelta(days=3)).isoformat(), "cervella-backend", "DB query", "contabilita", 1, "task", 3000),
        ((now - timedelta(days=4)).isoformat(), "cervella-tester", "Tests", "miracollo", 0, "task", 1500),
        ((now - timedelta(days=5)).isoformat(), "cervella-backend", "Fix bug", "miracollo", 1, "task", 2000),
        ((week_ago + timedelta(hours=1)).isoformat(), "cervella-backend", "Task", "miracollo", 1, "task", 1800),
    ]

    for event in events:
        cursor.execute("""
            INSERT INTO swarm_events (timestamp, agent_name, task_description, project, success, event_type, duration_ms)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, event)

    # Pattern errori (diversi severity + count)
    patterns = [
        ("Import Error", "CRITICAL", 5, "ACTIVE"),
        ("DB Connection", "HIGH", 3, "ACTIVE"),
        ("CSS z-index", "MEDIUM", 2, "ACTIVE"),
        ("Old Pattern", "LOW", 1, "RESOLVED"),
    ]

    for pattern in patterns:
        cursor.execute("""
            INSERT INTO error_patterns (pattern_name, severity_level, occurrence_count, status)
            VALUES (?, ?, ?, ?)
        """, pattern)

    # Lezioni apprese (diversi severity)
    lessons = [
        ("Import Error lesson", "CRITICAL", now.isoformat()),
        ("DB Connection lesson", "HIGH", now.isoformat()),
        ("CSS lesson", "MEDIUM", (now - timedelta(days=2)).isoformat()),
    ]

    for lesson in lessons:
        cursor.execute("""
            INSERT INTO lessons_learned (pattern, severity, created_at, status)
            VALUES (?, ?, ?, 'ACTIVE')
        """, lesson)

    conn.commit()
    conn.close()
    return retro_db
