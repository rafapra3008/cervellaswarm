"""
Test per Sistema Memoria CervellaSwarm - load_context.py (CORE)

Data extraction: get_recent_events, get_agent_stats, get_lessons_learned,
get_relevant_lessons.

Split da test_load_context.py (665 righe > 500 limite).
Sessione 348.
"""

import pytest
import sqlite3
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch, mock_open
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.memory.load_context import (
    get_recent_events,
    get_agent_stats,
    get_lessons_learned,
    get_relevant_lessons,
)


# === FIXTURES ===


@pytest.fixture
def temp_db():
    """Database temporaneo per test."""
    temp_file = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    db_path = Path(temp_file.name)
    temp_file.close()

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE swarm_events (
            id INTEGER PRIMARY KEY,
            timestamp TEXT,
            agent_name TEXT,
            task_description TEXT,
            project TEXT,
            success INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE lessons_learned (
            id INTEGER PRIMARY KEY,
            trigger TEXT,
            context TEXT,
            problem TEXT,
            root_cause TEXT,
            solution TEXT,
            prevention TEXT,
            example TEXT,
            severity TEXT,
            agents_involved TEXT,
            tags TEXT,
            pattern TEXT,
            confidence REAL,
            times_applied INTEGER,
            project TEXT,
            status TEXT
        )
    """)

    conn.commit()
    conn.close()

    yield db_path

    db_path.unlink()


@pytest.fixture
def populated_db(temp_db):
    """Database con dati di test."""
    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO swarm_events (timestamp, agent_name, task_description, project, success)
        VALUES
            ('2026-01-01 10:00:00', 'cervella-frontend', 'Fix CSS bug', 'miracollo', 1),
            ('2026-01-01 11:00:00', 'cervella-backend', 'API endpoint', 'miracollo', 1),
            ('2026-01-01 12:00:00', 'cervella-frontend', 'React component', 'miracollo', 0),
            ('2026-01-01 13:00:00', 'cervella-backend', 'Database migration', 'contabilita', 1)
    """)

    cursor.execute("""
        INSERT INTO lessons_learned (
            trigger, context, problem, root_cause, solution, prevention, example,
            severity, agents_involved, tags, pattern, confidence, times_applied, project, status
        )
        VALUES
            ('Import error', 'Frontend', 'Wrong import path', 'Bad path', 'Fix path', 'Check imports', 'import from scripts.', 'HIGH', 'cervella-frontend', 'import,frontend', 'Import Pattern', 0.95, 10, 'miracollo', 'ACTIVE'),
            ('DB connection', 'Backend', 'Connection failed', 'No pool', 'Add pool', 'Use pool', 'conn = pool.get()', 'CRITICAL', 'cervella-backend', 'database', 'DB Pattern', 0.92, 5, 'contabilita', 'ACTIVE'),
            ('CSS issue', 'Frontend', 'z-index wrong', 'No hierarchy', 'Use layers', 'Plan z-index', 'z-index: var(--layer-modal)', 'MEDIUM', 'cervella-frontend', 'css', 'CSS Pattern', 0.88, 3, 'miracollo', 'ACTIVE'),
            ('Old lesson', 'Old', 'Deprecated', 'N/A', 'N/A', 'N/A', 'N/A', 'LOW', '', '', 'Old Pattern', 0.5, 1, '', 'ARCHIVED')
    """)

    conn.commit()
    conn.close()

    return temp_db


# === TEST GET_RECENT_EVENTS ===


class TestGetRecentEvents:
    """Test recupero eventi recenti."""

    def test_no_events_returns_empty(self, temp_db):
        """Test con database vuoto."""
        conn = sqlite3.connect(temp_db)
        events = get_recent_events(conn, limit=10)
        conn.close()

        assert events == []

    def test_returns_events_with_limit(self, populated_db):
        """Test limit funziona."""
        conn = sqlite3.connect(populated_db)
        events = get_recent_events(conn, limit=2)
        conn.close()

        assert len(events) == 2
        assert events[0]["agent"] == "cervella-backend"  # 13:00
        assert events[1]["agent"] == "cervella-frontend"  # 12:00

    def test_event_structure(self, populated_db):
        """Test struttura evento."""
        conn = sqlite3.connect(populated_db)
        events = get_recent_events(conn, limit=1)
        conn.close()

        event = events[0]
        assert "timestamp" in event
        assert "agent" in event
        assert "task" in event
        assert "project" in event
        assert "success" in event
        assert isinstance(event["success"], bool)

    def test_task_truncation(self, temp_db):
        """Test task > 100 char viene troncato."""
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        long_task = "A" * 150
        cursor.execute("""
            INSERT INTO swarm_events (timestamp, agent_name, task_description, project, success)
            VALUES ('2026-01-01 10:00:00', 'test', ?, 'test', 1)
        """, (long_task,))
        conn.commit()

        events = get_recent_events(conn, limit=1)
        conn.close()

        assert len(events[0]["task"]) == 100


# === TEST GET_AGENT_STATS ===


class TestGetAgentStats:
    """Test statistiche agent."""

    def test_no_events_returns_empty(self, temp_db):
        """Test con database vuoto."""
        conn = sqlite3.connect(temp_db)
        stats = get_agent_stats(conn)
        conn.close()

        assert stats == {}

    def test_aggregates_by_agent_and_project(self, populated_db):
        """Test aggregazione per agent e project."""
        conn = sqlite3.connect(populated_db)
        stats = get_agent_stats(conn)
        conn.close()

        assert "cervella-frontend" in stats
        assert stats["cervella-frontend"]["total_tasks"] == 2
        assert stats["cervella-frontend"]["successful_tasks"] == 1
        assert "miracollo" in stats["cervella-frontend"]["projects"]

        assert "cervella-backend" in stats
        assert stats["cervella-backend"]["total_tasks"] == 2
        assert stats["cervella-backend"]["successful_tasks"] == 2
        assert len(stats["cervella-backend"]["projects"]) == 2

    def test_handles_null_success(self, temp_db):
        """Test gestione success NULL."""
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO swarm_events (timestamp, agent_name, task_description, project, success)
            VALUES ('2026-01-01 10:00:00', 'test', 'task', 'test', NULL)
        """)
        conn.commit()

        stats = get_agent_stats(conn)
        conn.close()

        assert stats["test"]["total_tasks"] == 1
        assert stats["test"]["successful_tasks"] == 0


# === TEST GET_LESSONS_LEARNED ===


class TestGetLessonsLearned:
    """Test lezioni apprese."""

    def test_filters_by_min_confidence(self, populated_db):
        """Test filtra per confidence minima."""
        conn = sqlite3.connect(populated_db)
        lessons = get_lessons_learned(conn, min_confidence=0.90)
        conn.close()

        assert len(lessons) == 2
        for lesson in lessons:
            assert lesson["confidence"] >= 0.90

    def test_orders_by_confidence_and_times_applied(self, populated_db):
        """Test ordinamento."""
        conn = sqlite3.connect(populated_db)
        lessons = get_lessons_learned(conn, min_confidence=0.85)
        conn.close()

        assert lessons[0]["confidence"] == 0.95
        assert lessons[0]["times_applied"] == 10

    def test_max_10_lessons(self, populated_db):
        """Test LIMIT 10."""
        conn = sqlite3.connect(populated_db)
        cursor = conn.cursor()
        for i in range(15):
            cursor.execute("""
                INSERT INTO lessons_learned (
                    context, problem, solution, pattern, confidence, times_applied
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (f"ctx{i}", f"prob{i}", f"sol{i}", f"pat{i}", 0.8, i))
        conn.commit()

        lessons = get_lessons_learned(conn, min_confidence=0.7)
        conn.close()

        assert len(lessons) <= 10


# === TEST GET_RELEVANT_LESSONS ===


class TestGetRelevantLessons:
    """Test scoring e filtering lezioni."""

    def test_filters_active_only(self, populated_db):
        """Test filtra solo status=ACTIVE."""
        conn = sqlite3.connect(populated_db)
        lessons = get_relevant_lessons(conn, limit=10)
        conn.close()

        assert len(lessons) == 3
        for lesson in lessons:
            assert lesson["pattern"] != "Old Pattern"

    def test_scoring_agent_match(self, populated_db):
        """Test +50 score per agent match."""
        conn = sqlite3.connect(populated_db)
        lessons = get_relevant_lessons(
            conn,
            agent_name="cervella-frontend",
            limit=10
        )
        conn.close()

        for lesson in lessons:
            if "cervella-frontend" in lesson["agents_involved"]:
                assert lesson["score"] >= 50

    def test_scoring_project_match(self, populated_db):
        """Test +30 score per project match."""
        conn = sqlite3.connect(populated_db)
        lessons = get_relevant_lessons(
            conn,
            project="miracollo",
            limit=10
        )
        conn.close()

        for lesson in lessons:
            if "miracollo" in (lesson["project"] or "").lower():
                assert lesson["score"] >= 30

    def test_scoring_severity(self, populated_db):
        """Test severity scoring."""
        conn = sqlite3.connect(populated_db)
        lessons = get_relevant_lessons(conn, limit=10)
        conn.close()

        for lesson in lessons:
            if lesson["severity"] == "CRITICAL":
                assert lesson["score"] >= 20
            elif lesson["severity"] == "HIGH":
                assert lesson["score"] >= 15

    def test_respects_limit(self, populated_db):
        """Test limit funziona."""
        conn = sqlite3.connect(populated_db)
        lessons = get_relevant_lessons(conn, limit=2)
        conn.close()

        assert len(lessons) == 2

    def test_orders_by_score_desc(self, populated_db):
        """Test ordinamento per score DESC."""
        conn = sqlite3.connect(populated_db)
        lessons = get_relevant_lessons(
            conn,
            agent_name="cervella-frontend",
            project="miracollo",
            limit=10
        )
        conn.close()

        scores = [l["score"] for l in lessons]
        assert scores == sorted(scores, reverse=True)

    def test_handles_null_fields(self, temp_db):
        """Test gestione campi NULL."""
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO lessons_learned (
                trigger, context, problem, solution, pattern, confidence, times_applied, status
            )
            VALUES ('test', 'test', 'test', 'test', 'test', 0.8, 2, 'ACTIVE')
        """)
        conn.commit()

        lessons = get_relevant_lessons(conn, agent_name="test", limit=10)
        conn.close()

        assert len(lessons) == 1
        assert lessons[0]["score"] >= 0
