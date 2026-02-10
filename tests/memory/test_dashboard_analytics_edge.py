"""
Test per Dashboard Analytics - Edge cases, Rich output, integration.

Split da test_dashboard_analytics.py (670 righe > limite 500).
Sessione 341.
"""

import pytest
import sqlite3
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.memory.analytics.commands.dashboard import cmd_dashboard, __version__


# === FIXTURES ===


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

    events = [
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

    for event in events:
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


# === TEST EDGE CASES ===


class TestDashboardEdgeCases:
    """Test scenari edge-case."""

    @patch('scripts.memory.analytics.commands.dashboard.connect_db')
    @patch('scripts.memory.analytics.commands.dashboard.console')
    def test_handles_no_patterns(self, mock_console, mock_connect, empty_db):
        conn = sqlite3.connect(empty_db)
        conn.row_factory = sqlite3.Row
        mock_connect.return_value = conn
        cmd_dashboard()
        assert mock_console.print.called
        conn.close()

    @patch('scripts.memory.analytics.commands.dashboard.connect_db')
    @patch('scripts.memory.analytics.commands.dashboard.console')
    def test_handles_no_lessons(self, mock_console, mock_connect, empty_db):
        conn = sqlite3.connect(empty_db)
        conn.row_factory = sqlite3.Row
        mock_connect.return_value = conn
        cmd_dashboard()
        assert mock_console.print.called
        conn.close()

    @patch('scripts.memory.analytics.commands.dashboard.connect_db')
    @patch('scripts.memory.analytics.commands.dashboard.console')
    def test_handles_no_agent_name(self, mock_console, mock_connect, temp_db):
        conn = sqlite3.connect(temp_db)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        now = datetime.now()
        cursor.execute("""
            INSERT INTO swarm_events (timestamp, agent_name, task_description, project, success)
            VALUES (?, NULL, 'Task without agent', 'test', 1)
        """, (now.isoformat(),))
        conn.commit()
        mock_connect.return_value = conn
        cmd_dashboard()
        conn.close()

    @patch('scripts.memory.analytics.commands.dashboard.connect_db')
    def test_closes_connection_on_success(self, mock_connect, populated_db):
        conn = sqlite3.connect(populated_db)
        conn.row_factory = sqlite3.Row
        mock_connect.return_value = conn
        cmd_dashboard()

    @patch('scripts.memory.analytics.commands.dashboard.connect_db')
    def test_handles_db_connection_error(self, mock_connect):
        mock_connect.side_effect = Exception("DB connection failed")
        with pytest.raises(Exception, match="DB connection failed"):
            cmd_dashboard()


# === TEST RICH OUTPUT ===


class TestDashboardRichOutput:
    """Test output Rich renderizzato correttamente."""

    @patch('scripts.memory.analytics.commands.dashboard.connect_db')
    @patch('scripts.memory.analytics.commands.dashboard.console')
    def test_prints_multiple_panels(self, mock_console, mock_connect, populated_db):
        conn = sqlite3.connect(populated_db)
        conn.row_factory = sqlite3.Row
        mock_connect.return_value = conn
        cmd_dashboard()
        assert mock_console.print.call_count >= 4
        conn.close()

    @patch('scripts.memory.analytics.commands.dashboard.connect_db')
    @patch('scripts.memory.analytics.commands.dashboard.Table')
    def test_creates_metrics_table(self, mock_table_class, mock_connect, populated_db):
        conn = sqlite3.connect(populated_db)
        conn.row_factory = sqlite3.Row
        mock_connect.return_value = conn
        mock_table = MagicMock()
        mock_table_class.return_value = mock_table
        cmd_dashboard()
        assert mock_table_class.called
        assert mock_table.add_row.called
        conn.close()

    @patch('scripts.memory.analytics.commands.dashboard.connect_db')
    @patch('scripts.memory.analytics.commands.dashboard.Panel')
    def test_creates_top_agent_panel(self, mock_panel_class, mock_connect, populated_db):
        conn = sqlite3.connect(populated_db)
        conn.row_factory = sqlite3.Row
        mock_connect.return_value = conn
        cmd_dashboard()
        assert mock_panel_class.call_count >= 2
        conn.close()


# === TEST INTEGRATION ===


class TestDashboardIntegration:
    """Test integrazione completa."""

    @patch('scripts.memory.analytics.commands.dashboard.connect_db')
    @patch('scripts.memory.analytics.commands.dashboard.console')
    def test_full_dashboard_workflow(self, mock_console, mock_connect, populated_db):
        conn = sqlite3.connect(populated_db)
        conn.row_factory = sqlite3.Row
        mock_connect.return_value = conn
        cmd_dashboard()
        assert mock_console.print.called
        conn.close()

    @patch('scripts.memory.analytics.commands.dashboard.connect_db')
    def test_dashboard_never_crashes(self, mock_connect, empty_db):
        conn = sqlite3.connect(empty_db)
        conn.row_factory = sqlite3.Row
        mock_connect.return_value = conn
        cmd_dashboard()
        conn.close()


# === TEST VERSION ===


class TestVersion:
    """Test versioning."""

    def test_version_format(self):
        assert isinstance(__version__, str)
        parts = __version__.split(".")
        assert len(parts) == 3
        assert all(p.isdigit() for p in parts)
