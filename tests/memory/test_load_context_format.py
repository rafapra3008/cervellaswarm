"""
Test per Sistema Memoria CervellaSwarm - load_context.py (FORMAT)

Formatting, integration, main: format_lessons_for_agent, get_active_suggestions,
format_context, load_context, main.

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
        assert "LEZIONI RILEVANTI PER QUESTO TASK" in result

    def test_includes_severity_emoji(self):
        """Test emoji per severity."""
        lessons = [
            {"severity": "CRITICAL", "pattern": "Test"},
            {"severity": "HIGH", "pattern": "Test"},
            {"severity": "MEDIUM", "pattern": "Test"},
            {"severity": "LOW", "pattern": "Test"},
        ]
        result = format_lessons_for_agent(lessons)
        assert "\U0001f534" in result  # CRITICAL
        assert "\U0001f7e0" in result  # HIGH
        assert "\U0001f7e1" in result  # MEDIUM
        assert "\U0001f7e2" in result  # LOW

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
        assert "92%" in result
        assert "5x" in result
        assert "75" in result

    def test_handles_missing_fields(self):
        """Test campi mancanti non crashano."""
        lessons = [{"severity": "HIGH", "pattern": "Test"}]
        result = format_lessons_for_agent(lessons)
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
        assert result == []


# === TEST FORMAT_CONTEXT ===


class TestFormatContext:
    """Test formatting contesto completo."""

    def test_includes_header(self):
        """Test header presente."""
        result = format_context([], {}, [])
        assert "CervellaSwarm - Memoria Attiva" in result

    def test_includes_events_section(self):
        """Test sezione eventi."""
        events = [
            {"agent": "test", "project": "test", "task": "test", "success": True},
        ]
        result = format_context(events, {}, [])
        assert "Ultimi Eventi Swarm" in result
        assert "test" in result

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
        assert "Statistiche Agent" in result
        assert "cervella-frontend" in result
        assert "80.0%" in result
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
        assert "Lezioni Apprese" in result
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
        assert "SUGGERIMENTI ATTIVI" in result
        assert "Test Suggestion" in result
        assert "Do this to prevent" in result

    def test_limits_events_to_10(self):
        """Test max 10 eventi mostrati."""
        events = [{"agent": f"test{i}", "project": "test", "task": "test", "success": True} for i in range(20)]
        result = format_context(events, {}, [])
        event_count = result.count("- \u2705")
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
        assert "LEZIONI RILEVANTI" in context or len(context) > 100

    @patch('scripts.memory.load_context.get_db_path')
    def test_handles_db_error_gracefully(self, mock_get_db, temp_db):
        """Test gestione errori DB."""
        mock_get_db.return_value = temp_db

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


# === TEST MAIN() ===


class TestMain:
    """Test main() entry point."""

    def test_main_success(self):
        """main() stampa JSON e esce con 0 su successo."""
        mock_result = {"hookSpecificOutput": {"additionalContext": "test"}}
        with patch('scripts.memory.load_context.load_context', return_value=mock_result):
            with patch('scripts.memory.load_context.sys.exit') as mock_exit:
                from scripts.memory.load_context import main
                main()
                mock_exit.assert_called_once_with(0)

    def test_main_error(self):
        """main() stampa errore su stderr e esce con 1 su eccezione."""
        with patch('scripts.memory.load_context.load_context', side_effect=RuntimeError("boom")):
            with patch('scripts.memory.load_context.sys.exit') as mock_exit:
                from scripts.memory.load_context import main
                main()
                mock_exit.assert_called_once_with(1)
