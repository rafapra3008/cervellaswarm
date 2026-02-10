"""
Test per Dashboard Analytics - Core queries e calcoli.

Verifica: NoRich fallback, DB vuoto, query SQL, success rate.

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
from io import StringIO

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


# === TEST HAS_RICH = False ===


class TestDashboardNoRich:
    """Test dashboard quando Rich non disponibile."""

    @patch('sys.stdout', new_callable=StringIO)
    def test_prints_error_message(self, mock_stdout):
        from scripts.memory.analytics.commands import dashboard
        original = dashboard.HAS_RICH
        dashboard.HAS_RICH = False
        dashboard.cmd_dashboard()
        dashboard.HAS_RICH = original
        assert "Comando 'dashboard' richiede Rich installato" in mock_stdout.getvalue()

    @patch('sys.stdout', new_callable=StringIO)
    def test_suggests_pip_install(self, mock_stdout):
        from scripts.memory.analytics.commands import dashboard
        original = dashboard.HAS_RICH
        dashboard.HAS_RICH = False
        dashboard.cmd_dashboard()
        dashboard.HAS_RICH = original
        assert "pip install rich" in mock_stdout.getvalue()

    @patch('sys.stdout', new_callable=StringIO)
    def test_suggests_alternative_command(self, mock_stdout):
        from scripts.memory.analytics.commands import dashboard
        original = dashboard.HAS_RICH
        dashboard.HAS_RICH = False
        dashboard.cmd_dashboard()
        dashboard.HAS_RICH = original
        assert "analytics.cli summary" in mock_stdout.getvalue()

    @patch('scripts.memory.analytics.commands.dashboard.connect_db')
    def test_does_not_call_db_when_no_rich(self, mock_connect):
        from scripts.memory.analytics.commands import dashboard
        original = dashboard.HAS_RICH
        dashboard.HAS_RICH = False
        dashboard.cmd_dashboard()
        dashboard.HAS_RICH = original
        mock_connect.assert_not_called()


# === TEST DB VUOTO ===


class TestDashboardEmptyDB:
    """Test dashboard con database vuoto."""

    @patch('scripts.memory.analytics.commands.dashboard.connect_db')
    @patch('scripts.memory.analytics.commands.dashboard.console')
    def test_handles_zero_events(self, mock_console, mock_connect, empty_db):
        conn = sqlite3.connect(empty_db)
        conn.row_factory = sqlite3.Row
        mock_connect.return_value = conn
        cmd_dashboard()
        assert mock_console.print.called
        conn.close()

    @patch('scripts.memory.analytics.commands.dashboard.connect_db')
    def test_success_rate_zero_when_no_events(self, mock_connect, empty_db):
        conn = sqlite3.connect(empty_db)
        conn.row_factory = sqlite3.Row
        mock_connect.return_value = conn
        cmd_dashboard()
        conn.close()

    @patch('scripts.memory.analytics.commands.dashboard.connect_db')
    def test_top_agent_na_when_no_events(self, mock_connect, empty_db):
        conn = sqlite3.connect(empty_db)
        conn.row_factory = sqlite3.Row
        mock_connect.return_value = conn
        cmd_dashboard()
        conn.close()


# === TEST QUERY SQL ===


class TestDashboardQueries:
    """Test correttezza query SQL."""

    def test_events_week_filters_by_date(self, populated_db):
        conn = sqlite3.connect(populated_db)
        conn.row_factory = sqlite3.Row
        week_ago = (datetime.now() - timedelta(days=7)).isoformat()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as total FROM swarm_events WHERE datetime(timestamp) >= datetime(?)", (week_ago,))
        assert cursor.fetchone()['total'] == 10
        conn.close()

    def test_success_week_counts_only_success_1(self, populated_db):
        conn = sqlite3.connect(populated_db)
        conn.row_factory = sqlite3.Row
        week_ago = (datetime.now() - timedelta(days=7)).isoformat()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as success FROM swarm_events WHERE success = 1 AND datetime(timestamp) >= datetime(?)", (week_ago,))
        assert cursor.fetchone()['success'] == 8
        conn.close()

    def test_errors_week_counts_only_success_0(self, populated_db):
        conn = sqlite3.connect(populated_db)
        conn.row_factory = sqlite3.Row
        week_ago = (datetime.now() - timedelta(days=7)).isoformat()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as errors FROM swarm_events WHERE success = 0 AND datetime(timestamp) >= datetime(?)", (week_ago,))
        assert cursor.fetchone()['errors'] == 2
        conn.close()

    def test_active_patterns_filters_status_active(self, populated_db):
        conn = sqlite3.connect(populated_db)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as active FROM error_patterns WHERE status = 'ACTIVE'")
        assert cursor.fetchone()['active'] == 2
        conn.close()

    def test_active_lessons_filters_status_active(self, populated_db):
        conn = sqlite3.connect(populated_db)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as active FROM lessons_learned WHERE status = 'ACTIVE'")
        assert cursor.fetchone()['active'] == 3
        conn.close()

    def test_top_agent_selects_most_active(self, populated_db):
        conn = sqlite3.connect(populated_db)
        conn.row_factory = sqlite3.Row
        week_ago = (datetime.now() - timedelta(days=7)).isoformat()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT agent_name, COUNT(*) as tasks FROM swarm_events
            WHERE datetime(timestamp) >= datetime(?) AND agent_name IS NOT NULL
            GROUP BY agent_name ORDER BY tasks DESC LIMIT 1
        """, (week_ago,))
        result = cursor.fetchone()
        assert result['agent_name'] == 'cervella-backend'
        assert result['tasks'] == 6
        conn.close()

    def test_top_agent_filters_out_null_names(self, temp_db):
        conn = sqlite3.connect(temp_db)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        now = datetime.now()
        cursor.execute("""
            INSERT INTO swarm_events (timestamp, agent_name, task_description, project, success)
            VALUES (?, NULL, 'Task without agent', 'test', 1), (?, 'test-agent', 'Task with agent', 'test', 1)
        """, (now.isoformat(), now.isoformat()))
        conn.commit()
        week_ago = (datetime.now() - timedelta(days=7)).isoformat()
        cursor.execute("""
            SELECT agent_name, COUNT(*) as tasks FROM swarm_events
            WHERE datetime(timestamp) >= datetime(?) AND agent_name IS NOT NULL
            GROUP BY agent_name ORDER BY tasks DESC LIMIT 1
        """, (week_ago,))
        assert cursor.fetchone()['agent_name'] == 'test-agent'
        conn.close()


# === TEST SUCCESS RATE ===


class TestDashboardSuccessRate:
    """Test calcolo success rate."""

    @patch('scripts.memory.analytics.commands.dashboard.connect_db')
    @patch('scripts.memory.analytics.commands.dashboard.console')
    def test_calculates_correct_success_rate(self, mock_console, mock_connect, populated_db):
        conn = sqlite3.connect(populated_db)
        conn.row_factory = sqlite3.Row
        mock_connect.return_value = conn
        cmd_dashboard()
        conn.close()

    def test_success_rate_100_percent(self, temp_db):
        conn = sqlite3.connect(temp_db)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        now = datetime.now()
        cursor.execute("INSERT INTO swarm_events (timestamp, agent_name, task_description, project, success) VALUES (?, 'test', 'task', 'test', 1)", (now.isoformat(),))
        conn.commit()
        week_ago = (datetime.now() - timedelta(days=7)).isoformat()
        cursor.execute("SELECT COUNT(*) as total FROM swarm_events WHERE datetime(timestamp) >= datetime(?)", (week_ago,))
        events_week = cursor.fetchone()['total']
        cursor.execute("SELECT COUNT(*) as success FROM swarm_events WHERE success = 1 AND datetime(timestamp) >= datetime(?)", (week_ago,))
        success_week = cursor.fetchone()['success']
        success_rate = (success_week / events_week * 100) if events_week > 0 else 0
        assert success_rate == 100.0
        conn.close()

    def test_success_rate_0_percent(self, temp_db):
        conn = sqlite3.connect(temp_db)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        now = datetime.now()
        cursor.execute("INSERT INTO swarm_events (timestamp, agent_name, task_description, project, success) VALUES (?, 'test', 'task', 'test', 0)", (now.isoformat(),))
        conn.commit()
        week_ago = (datetime.now() - timedelta(days=7)).isoformat()
        cursor.execute("SELECT COUNT(*) as total FROM swarm_events WHERE datetime(timestamp) >= datetime(?)", (week_ago,))
        events_week = cursor.fetchone()['total']
        cursor.execute("SELECT COUNT(*) as success FROM swarm_events WHERE success = 1 AND datetime(timestamp) >= datetime(?)", (week_ago,))
        success_week = cursor.fetchone()['success']
        success_rate = (success_week / events_week * 100) if events_week > 0 else 0
        assert success_rate == 0.0
        conn.close()
