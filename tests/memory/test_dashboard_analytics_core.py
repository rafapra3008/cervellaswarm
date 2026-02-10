"""
Test per Dashboard Analytics - Core queries e calcoli.

Verifica: NoRich fallback, DB vuoto, query SQL, success rate.

Split da test_dashboard_analytics.py (670 righe > limite 500).
Sessione 341.
"""

import pytest
import sqlite3
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
from io import StringIO

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.memory.analytics.commands.dashboard import cmd_dashboard, __version__

# Fixtures temp_db, empty_db, populated_db from conftest.py


# === TEST HAS_RICH = False ===


class TestDashboardNoRich:
    """Test dashboard quando Rich non disponibile."""

    @patch('scripts.memory.analytics.commands.dashboard.HAS_RICH', False)
    @patch('sys.stdout', new_callable=StringIO)
    def test_prints_error_message(self, mock_stdout):
        from scripts.memory.analytics.commands.dashboard import cmd_dashboard as _cmd
        _cmd()
        assert "Comando 'dashboard' richiede Rich installato" in mock_stdout.getvalue()

    @patch('scripts.memory.analytics.commands.dashboard.HAS_RICH', False)
    @patch('sys.stdout', new_callable=StringIO)
    def test_suggests_pip_install(self, mock_stdout):
        from scripts.memory.analytics.commands.dashboard import cmd_dashboard as _cmd
        _cmd()
        assert "pip install rich" in mock_stdout.getvalue()

    @patch('scripts.memory.analytics.commands.dashboard.HAS_RICH', False)
    @patch('sys.stdout', new_callable=StringIO)
    def test_suggests_alternative_command(self, mock_stdout):
        from scripts.memory.analytics.commands.dashboard import cmd_dashboard as _cmd
        _cmd()
        assert "analytics.cli summary" in mock_stdout.getvalue()

    @patch('scripts.memory.analytics.commands.dashboard.HAS_RICH', False)
    @patch('scripts.memory.analytics.commands.dashboard.connect_db')
    def test_does_not_call_db_when_no_rich(self, mock_connect):
        from scripts.memory.analytics.commands.dashboard import cmd_dashboard as _cmd
        _cmd()
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
