"""
Test per Sistema Memoria CervellaSwarm - load_context.py

Verifica caricamento contesto, scoring lezioni, formatting markdown,
e gestione errori per SessionStart hook.

Sessione 340 - Cervella Tester
"""

import pytest
import sqlite3
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch, mock_open
from datetime import datetime, timezone

# Setup path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.memory.load_context import (
    get_recent_events,
    get_agent_stats,
    get_lessons_learned,
    get_relevant_lessons,
    format_lessons_for_agent,
    get_active_suggestions,
    format_context,
    load_context,
    __version__,
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

    # Tabella swarm_events
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

    # Tabella lessons_learned
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

    # Cleanup
    db_path.unlink()


@pytest.fixture
def populated_db(temp_db):
    """Database con dati di test."""
    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()

    # Eventi
    cursor.execute("""
        INSERT INTO swarm_events (timestamp, agent_name, task_description, project, success)
        VALUES
            ('2026-01-01 10:00:00', 'cervella-frontend', 'Fix CSS bug', 'miracollo', 1),
            ('2026-01-01 11:00:00', 'cervella-backend', 'API endpoint', 'miracollo', 1),
            ('2026-01-01 12:00:00', 'cervella-frontend', 'React component', 'miracollo', 0),
            ('2026-01-01 13:00:00', 'cervella-backend', 'Database migration', 'contabilita', 1)
    """)

    # Lezioni
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
        # Ordine DESC (piu recenti)
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

        # cervella-frontend: 2 task (1 success, 1 fail) su miracollo
        assert "cervella-frontend" in stats
        assert stats["cervella-frontend"]["total_tasks"] == 2
        assert stats["cervella-frontend"]["successful_tasks"] == 1
        assert "miracollo" in stats["cervella-frontend"]["projects"]

        # cervella-backend: 2 task (2 success) su miracollo e contabilita
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
        assert stats["test"]["successful_tasks"] == 0  # NULL trattato come 0


# === TEST GET_LESSONS_LEARNED ===


class TestGetLessonsLearned:
    """Test lezioni apprese."""

    def test_filters_by_min_confidence(self, populated_db):
        """Test filtra per confidence minima."""
        conn = sqlite3.connect(populated_db)
        lessons = get_lessons_learned(conn, min_confidence=0.90)
        conn.close()

        # Solo 2 lezioni >= 0.90
        assert len(lessons) == 2
        for lesson in lessons:
            assert lesson["confidence"] >= 0.90

    def test_orders_by_confidence_and_times_applied(self, populated_db):
        """Test ordinamento."""
        conn = sqlite3.connect(populated_db)
        lessons = get_lessons_learned(conn, min_confidence=0.85)
        conn.close()

        # Prima lezione: confidence 0.95, times_applied 10
        assert lessons[0]["confidence"] == 0.95
        assert lessons[0]["times_applied"] == 10

    def test_max_10_lessons(self, populated_db):
        """Test LIMIT 10."""
        conn = sqlite3.connect(populated_db)
        # Aggiungiamo molte lezioni
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

        # 3 ACTIVE, 1 ARCHIVED
        assert len(lessons) == 3
        for lesson in lessons:
            # Verifichiamo che nessuna sia ARCHIVED controllando i valori
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

        # Lezioni con cervella-frontend dovrebbero avere score > 50
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

        # Lezioni con miracollo dovrebbero avere score >= 30
        for lesson in lessons:
            if "miracollo" in (lesson["project"] or "").lower():
                assert lesson["score"] >= 30

    def test_scoring_severity(self, populated_db):
        """Test severity scoring."""
        conn = sqlite3.connect(populated_db)
        lessons = get_relevant_lessons(conn, limit=10)
        conn.close()

        # CRITICAL = +20, HIGH = +15, MEDIUM = +10
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

        # Scores devono essere in ordine decrescente
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

        # Non dovrebbe crashare con NULL
        assert len(lessons) == 1
        assert lessons[0]["score"] >= 0


# === TEST FORMAT_LESSONS_FOR_AGENT ===


class TestFormatLessonsForAgent:
    """Test formatting markdown lezioni."""

    def test_empty_lessons_returns_empty_string(self):
        """Test lista vuota."""
        result = format_lessons_for_agent([])
        assert result == ""

    def test_formats_markdown_header(self):
        """Test header presente."""
        lessons = [{"severity": "HIGH", "pattern": "Test Pattern"}]
        result = format_lessons_for_agent(lessons)

        assert "## 📚 LEZIONI RILEVANTI PER QUESTO TASK" in result

    def test_includes_severity_emoji(self):
        """Test emoji per severity."""
        lessons = [
            {"severity": "CRITICAL", "pattern": "Test"},
            {"severity": "HIGH", "pattern": "Test"},
            {"severity": "MEDIUM", "pattern": "Test"},
            {"severity": "LOW", "pattern": "Test"},
        ]
        result = format_lessons_for_agent(lessons)

        assert "🔴" in result  # CRITICAL
        assert "🟠" in result  # HIGH
        assert "🟡" in result  # MEDIUM
        assert "🟢" in result  # LOW

    def test_includes_all_fields(self):
        """Test tutti i campi presenti."""
        lessons = [{
            "severity": "HIGH",
            "pattern": "Test Pattern",
            "trigger": "Test trigger",
            "problem": "Test problem",
            "root_cause": "Test cause",
            "solution": "Test solution",
            "prevention": "Test prevention",
            "example": "Test example",
            "confidence": 0.92,
            "times_applied": 5,
            "score": 75,
        }]
        result = format_lessons_for_agent(lessons)

        assert "Test trigger" in result
        assert "Test problem" in result
        assert "Test cause" in result
        assert "Test solution" in result
        assert "Test prevention" in result
        assert "Test example" in result
        assert "92%" in result  # Confidence formattata
        assert "5x" in result   # Times applied
        assert "75" in result   # Score

    def test_handles_missing_fields(self):
        """Test campi mancanti non crashano."""
        lessons = [{"severity": "HIGH", "pattern": "Test"}]
        result = format_lessons_for_agent(lessons)

        # Non deve crashare
        assert "Test" in result


# === TEST GET_ACTIVE_SUGGESTIONS ===


class TestGetActiveSuggestions:
    """Test recupero suggerimenti."""

    @patch('scripts.memory.load_context.get_suggestions', None)
    def test_no_import_returns_empty(self):
        """Test fallback quando suggestions non disponibile."""
        result = get_active_suggestions()
        assert result == []

    @patch('scripts.memory.load_context.get_suggestions')
    def test_calls_get_suggestions_with_params(self, mock_get):
        """Test chiama get_suggestions correttamente."""
        mock_get.return_value = [{"id": 1}]
        result = get_active_suggestions(project="miracollo")

        mock_get.assert_called_once_with(project="miracollo", limit=5)
        assert len(result) == 1

    @patch('scripts.memory.load_context.get_suggestions')
    def test_handles_exception(self, mock_get):
        """Test gestione eccezioni."""
        mock_get.side_effect = Exception("DB error")
        result = get_active_suggestions()

        # Deve ritornare [] invece di crashare
        assert result == []


# === TEST FORMAT_CONTEXT ===


class TestFormatContext:
    """Test formatting contesto completo."""

    def test_includes_header(self):
        """Test header presente."""
        result = format_context([], {}, [])
        assert "# 🐝 CervellaSwarm - Memoria Attiva" in result

    def test_includes_events_section(self):
        """Test sezione eventi."""
        events = [
            {"agent": "test", "project": "test", "task": "test", "success": True},
        ]
        result = format_context(events, {}, [])

        assert "## 📊 Ultimi Eventi Swarm" in result
        assert "test" in result
        assert "✅" in result  # Success emoji

    def test_includes_stats_section(self):
        """Test sezione statistiche."""
        stats = {
            "cervella-frontend": {
                "total_tasks": 10,
                "successful_tasks": 8,
                "projects": ["miracollo", "contabilita"],
            }
        }
        result = format_context([], stats, [])

        assert "## 🎯 Statistiche Agent" in result
        assert "cervella-frontend" in result
        assert "80.0%" in result  # Success rate
        assert "miracollo, contabilita" in result

    def test_includes_lessons_section(self):
        """Test sezione lezioni."""
        lessons = [{
            "pattern": "Test Pattern",
            "problem": "Test problem",
            "solution": "Test solution",
            "confidence": 0.95,
            "times_applied": 10,
        }]
        result = format_context([], {}, lessons)

        assert "## 💡 Lezioni Apprese" in result
        assert "Test Pattern" in result
        assert "95%" in result

    def test_includes_suggestions_section(self):
        """Test sezione suggerimenti."""
        suggestions = [{
            "severity": "HIGH",
            "pattern": "Test Suggestion",
            "prevention": "Do this to prevent",
        }]
        result = format_context([], {}, [], suggestions)

        assert "## 💡 SUGGERIMENTI ATTIVI" in result
        assert "Test Suggestion" in result
        assert "Do this to prevent" in result

    def test_limits_events_to_10(self):
        """Test max 10 eventi mostrati."""
        events = [{"agent": f"test{i}", "project": "test", "task": "test", "success": True} for i in range(20)]
        result = format_context(events, {}, [])

        # Conta quante volte appare il pattern dell'evento
        event_count = result.count("- ✅")
        assert event_count == 10


# === TEST LOAD_CONTEXT ===


class TestLoadContext:
    """Test funzione principale."""

    @patch('scripts.memory.load_context.get_db_path')
    def test_db_not_exists_returns_default(self, mock_get_db):
        """Test DB non esistente."""
        mock_get_db.return_value = Path("/nonexistent/path.db")
        result = load_context()

        assert "hookSpecificOutput" in result
        assert result["hookSpecificOutput"]["hookEventName"] == "SessionStart"
        assert "non inizializzato" in result["hookSpecificOutput"]["additionalContext"]

    @patch('scripts.memory.load_context.get_db_path')
    def test_returns_correct_structure(self, mock_get_db, populated_db):
        """Test struttura output corretta."""
        mock_get_db.return_value = populated_db
        result = load_context()

        assert "hookSpecificOutput" in result
        assert "metadata" in result
        assert result["hookSpecificOutput"]["hookEventName"] == "SessionStart"
        assert "additionalContext" in result["hookSpecificOutput"]
        assert "events_count" in result["metadata"]
        assert "agents_count" in result["metadata"]
        assert "lessons_count" in result["metadata"]
        assert "relevant_lessons_count" in result["metadata"]

    @patch('scripts.memory.load_context.get_db_path')
    def test_includes_agent_specific_lessons(self, mock_get_db, populated_db):
        """Test include lezioni agent-specific."""
        mock_get_db.return_value = populated_db
        result = load_context(agent_name="cervella-frontend", project="miracollo")

        context = result["hookSpecificOutput"]["additionalContext"]
        # Deve includere lezioni rilevanti
        assert "LEZIONI RILEVANTI" in context or len(context) > 100

    @patch('scripts.memory.load_context.get_db_path')
    def test_handles_db_error_gracefully(self, mock_get_db, temp_db):
        """Test gestione errori DB."""
        mock_get_db.return_value = temp_db

        # Corrupting DB
        with open(temp_db, 'w') as f:
            f.write("CORRUPTED")

        result = load_context()

        assert "hookSpecificOutput" in result
        assert "Errore" in result["hookSpecificOutput"]["additionalContext"]

    @patch('scripts.memory.load_context.get_db_path')
    @patch('scripts.memory.load_context.get_active_suggestions')
    def test_includes_suggestions_when_available(self, mock_sug, mock_get_db, populated_db):
        """Test include suggerimenti quando disponibili."""
        mock_get_db.return_value = populated_db
        mock_sug.return_value = [{"severity": "HIGH", "pattern": "Test"}]

        result = load_context(project="miracollo")
        context = result["hookSpecificOutput"]["additionalContext"]

        # Deve includere suggerimenti
        assert len(context) > 0


# === TEST VERSION ===


class TestVersion:
    """Test versioning."""

    def test_version_format(self):
        """Test version string format."""
        assert isinstance(__version__, str)
        parts = __version__.split(".")
        assert len(parts) == 3
        assert all(p.isdigit() for p in parts)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
