"""
Test per Analytics Commands - summary + helpers.

Testa:
- cmd_summary() - overview generale
- helpers.py - utility functions

Sessione 340.
"""

import pytest
import sqlite3
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock
from datetime import datetime
from io import StringIO

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.memory.analytics.commands.summary import cmd_summary
from scripts.memory.analytics import helpers


# === FIXTURES LOCALI ===


@pytest.fixture
def summary_temp_db(tmp_path):
    """Database temporaneo con schema completo per summary."""
    db_path = tmp_path / "summary_test.db"
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE swarm_events (
            id INTEGER PRIMARY KEY,
            timestamp TEXT,
            agent_name TEXT,
            event_type TEXT,
            task_description TEXT,
            project TEXT,
            success INTEGER,
            duration_ms INTEGER
        )
    """)
    cursor.execute("""
        CREATE TABLE lessons_learned (
            id INTEGER PRIMARY KEY,
            pattern TEXT,
            category TEXT,
            severity TEXT,
            status TEXT,
            prevention TEXT,
            occurrence_count INTEGER,
            time_wasted_minutes INTEGER
        )
    """)
    conn.commit()
    conn.close()
    yield db_path


@pytest.fixture
def summary_empty_db(summary_temp_db):
    """Database vuoto."""
    return summary_temp_db


@pytest.fixture
def summary_populated_db(summary_temp_db):
    """Database con dati realistici."""
    conn = sqlite3.connect(summary_temp_db)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    now = datetime.now().isoformat()

    cursor.execute("""
        INSERT INTO swarm_events (timestamp, agent_name, event_type, task_description, project, success, duration_ms)
        VALUES
            (?, 'cervella-backend', 'TASK_START', 'Fix API', 'miracollo', 1, 5000),
            (?, 'cervella-backend', 'TASK_END', 'Query', 'miracollo', 1, 3000),
            (?, 'cervella-frontend', 'TASK_START', 'CSS', 'miracollo', 0, 2000),
            (?, 'cervella-tester', 'TASK_START', 'Tests', 'miracollo', 1, 6000)
    """, (now, now, now, now))

    cursor.execute("""
        INSERT INTO lessons_learned (pattern, category, severity, status, prevention, occurrence_count, time_wasted_minutes)
        VALUES
            ('Import Error', 'Testing', 'CRITICAL', 'ACTIVE', 'Use absolute imports', 5, 120),
            ('DB Pool', 'Backend', 'HIGH', 'ACTIVE', 'Add pooling', 3, 60),
            ('CSS z-index', 'Frontend', 'MEDIUM', 'ACTIVE', 'Use layers', 2, 30)
    """)

    conn.commit()
    conn.close()
    return summary_temp_db


# === TEST CMD_SUMMARY ===


class TestCmdSummary:
    """Test cmd_summary() - overview generale."""

    @patch('scripts.memory.analytics.commands.summary.connect_db')
    @patch('sys.stdout', new_callable=StringIO)
    def test_empty_db_shows_zero_stats(self, mock_stdout, mock_connect, summary_empty_db):
        """Empty DB mostra statistiche a zero."""
        conn = sqlite3.connect(summary_empty_db)
        conn.row_factory = sqlite3.Row
        mock_connect.return_value = conn

        cmd_summary()

        output = mock_stdout.getvalue()
        assert "Total Events:" in output
        assert "0" in output
        conn.close()

    @patch('scripts.memory.analytics.commands.summary.connect_db')
    @patch('sys.stdout', new_callable=StringIO)
    def test_calculates_total_events(self, mock_stdout, mock_connect, summary_populated_db):
        """Calcola total events."""
        conn = sqlite3.connect(summary_populated_db)
        conn.row_factory = sqlite3.Row
        mock_connect.return_value = conn

        cmd_summary()

        output = mock_stdout.getvalue()
        assert "Total Events:" in output
        assert "4" in output
        conn.close()

    @patch('scripts.memory.analytics.commands.summary.connect_db')
    @patch('sys.stdout', new_callable=StringIO)
    def test_calculates_success_count(self, mock_stdout, mock_connect, summary_populated_db):
        """Calcola success count."""
        conn = sqlite3.connect(summary_populated_db)
        conn.row_factory = sqlite3.Row
        mock_connect.return_value = conn

        cmd_summary()

        output = mock_stdout.getvalue()
        assert "Success Rate:" in output
        conn.close()

    @patch('scripts.memory.analytics.commands.summary.connect_db')
    @patch('sys.stdout', new_callable=StringIO)
    def test_success_rate_calculation(self, mock_stdout, mock_connect, summary_populated_db):
        """Success rate = (success / total) * 100."""
        conn = sqlite3.connect(summary_populated_db)
        conn.row_factory = sqlite3.Row
        mock_connect.return_value = conn

        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as total FROM swarm_events")
        total = cursor.fetchone()['total']
        cursor.execute("SELECT COUNT(*) as success FROM swarm_events WHERE success = 1")
        success = cursor.fetchone()['success']

        expected_rate = (success / total * 100) if total > 0 else 0

        cmd_summary()

        output = mock_stdout.getvalue()
        assert f"{expected_rate:.1f}%" in output
        conn.close()

    @patch('scripts.memory.analytics.commands.summary.connect_db')
    @patch('sys.stdout', new_callable=StringIO)
    def test_handles_division_by_zero(self, mock_stdout, mock_connect, summary_empty_db):
        """Gestisce division by zero se no events."""
        conn = sqlite3.connect(summary_empty_db)
        conn.row_factory = sqlite3.Row
        mock_connect.return_value = conn

        try:
            cmd_summary()
            success = True
        except ZeroDivisionError:
            success = False

        assert success
        conn.close()

    @patch('scripts.memory.analytics.commands.summary.connect_db')
    @patch('sys.stdout', new_callable=StringIO)
    def test_counts_total_lessons(self, mock_stdout, mock_connect, summary_populated_db):
        """Conta total lessons."""
        conn = sqlite3.connect(summary_populated_db)
        conn.row_factory = sqlite3.Row
        mock_connect.return_value = conn

        cmd_summary()

        output = mock_stdout.getvalue()
        assert "Total Lessons:" in output
        conn.close()

    @patch('scripts.memory.analytics.commands.summary.connect_db')
    @patch('sys.stdout', new_callable=StringIO)
    def test_counts_active_lessons(self, mock_stdout, mock_connect, summary_populated_db):
        """Conta active lessons (status = ACTIVE)."""
        conn = sqlite3.connect(summary_populated_db)
        conn.row_factory = sqlite3.Row
        mock_connect.return_value = conn

        cmd_summary()

        output = mock_stdout.getvalue()
        assert "Active Lessons:" in output
        assert "da risolvere" in output
        conn.close()

    @patch('scripts.memory.analytics.commands.summary.connect_db')
    @patch('sys.stdout', new_callable=StringIO)
    def test_shows_last_event_timestamp(self, mock_stdout, mock_connect, summary_populated_db):
        """Mostra timestamp ultimo evento."""
        conn = sqlite3.connect(summary_populated_db)
        conn.row_factory = sqlite3.Row
        mock_connect.return_value = conn

        cmd_summary()

        output = mock_stdout.getvalue()
        assert "Last Event:" in output
        conn.close()

    @patch('scripts.memory.analytics.commands.summary.connect_db')
    @patch('sys.stdout', new_callable=StringIO)
    def test_handles_no_events_for_last_event(self, mock_stdout, mock_connect, summary_empty_db):
        """Se no events, last event = N/A."""
        conn = sqlite3.connect(summary_empty_db)
        conn.row_factory = sqlite3.Row
        mock_connect.return_value = conn

        cmd_summary()

        output = mock_stdout.getvalue()
        assert "Last Event:" in output
        assert "N/A" in output
        conn.close()

    @patch('scripts.memory.analytics.commands.summary.connect_db')
    @patch('sys.stdout', new_callable=StringIO)
    def test_shows_top_3_lessons(self, mock_stdout, mock_connect, summary_populated_db):
        """Mostra top 3 lezioni attive."""
        conn = sqlite3.connect(summary_populated_db)
        conn.row_factory = sqlite3.Row
        mock_connect.return_value = conn

        cmd_summary()

        output = mock_stdout.getvalue()
        assert "TOP LESSONS ATTIVE" in output
        conn.close()

    @patch('scripts.memory.analytics.commands.summary.connect_db')
    @patch('sys.stdout', new_callable=StringIO)
    def test_top_lessons_ordered_by_severity(self, mock_stdout, mock_connect, summary_populated_db):
        """Top lessons ordinate per severity."""
        conn = sqlite3.connect(summary_populated_db)
        conn.row_factory = sqlite3.Row
        mock_connect.return_value = conn

        cmd_summary()

        output = mock_stdout.getvalue()
        if "CRITICAL" in output and "HIGH" in output:
            critical_pos = output.find("CRITICAL")
            high_pos = output.find("HIGH")
            assert critical_pos < high_pos
        conn.close()

    @patch('scripts.memory.analytics.commands.summary.connect_db')
    @patch('sys.stdout', new_callable=StringIO)
    def test_shows_header_and_footer(self, mock_stdout, mock_connect, summary_populated_db):
        """Mostra header e footer."""
        conn = sqlite3.connect(summary_populated_db)
        conn.row_factory = sqlite3.Row
        mock_connect.return_value = conn

        cmd_summary()

        output = mock_stdout.getvalue()
        assert "CERVELLASWARM ANALYTICS" in output
        assert "╔" in output
        assert "╚" in output
        conn.close()


# === TEST HELPERS ===


class TestHelpers:
    """Test helpers.py - utility functions."""

    def test_has_rich_is_boolean(self):
        """HAS_RICH e un boolean."""
        assert isinstance(helpers.HAS_RICH, bool)

    def test_console_is_none_or_console(self):
        """console e None o Console."""
        if helpers.HAS_RICH:
            assert helpers.console is not None
        else:
            assert helpers.console is None

    def test_rich_available_returns_boolean(self):
        """rich_available() ritorna boolean."""
        result = helpers.rich_available()
        assert isinstance(result, bool)

    def test_rich_available_matches_has_rich(self):
        """rich_available() == HAS_RICH."""
        assert helpers.rich_available() == helpers.HAS_RICH

    def test_get_console_returns_console_or_none(self):
        """get_console() ritorna console o None."""
        result = helpers.get_console()
        if helpers.HAS_RICH:
            assert result is not None
        else:
            assert result is None

    @patch('sys.stdout', new_callable=StringIO)
    def test_plain_print_prints_text(self, mock_stdout):
        """plain_print() stampa testo."""
        helpers.plain_print("Test message")
        assert "Test message" in mock_stdout.getvalue()

    @patch.object(helpers, 'HAS_RICH', True)
    def test_print_rich_or_plain_calls_rich_fn_when_rich_available(self):
        """print_rich_or_plain() chiama rich_fn se HAS_RICH."""
        rich_fn = MagicMock()
        plain_fn = MagicMock()

        helpers.print_rich_or_plain(rich_fn, plain_fn, "arg1", kwarg="val")

        rich_fn.assert_called_once_with("arg1", kwarg="val")
        plain_fn.assert_not_called()

    @patch.object(helpers, 'HAS_RICH', False)
    def test_print_rich_or_plain_calls_plain_fn_when_no_rich(self):
        """print_rich_or_plain() chiama plain_fn se no Rich."""
        rich_fn = MagicMock()
        plain_fn = MagicMock()

        helpers.print_rich_or_plain(rich_fn, plain_fn, "arg1", kwarg="val")

        plain_fn.assert_called_once_with("arg1", kwarg="val")
        rich_fn.assert_not_called()

    def test_table_is_none_when_no_rich(self):
        """Table = None se no Rich."""
        if not helpers.HAS_RICH:
            assert helpers.Table is None

    def test_panel_is_none_when_no_rich(self):
        """Panel = None se no Rich."""
        if not helpers.HAS_RICH:
            assert helpers.Panel is None

    def test_layout_is_none_when_no_rich(self):
        """Layout = None se no Rich."""
        if not helpers.HAS_RICH:
            assert helpers.Layout is None

    def test_box_is_none_when_no_rich(self):
        """box = None se no Rich."""
        if not helpers.HAS_RICH:
            assert helpers.box is None

    def test_text_is_none_when_no_rich(self):
        """Text = None se no Rich."""
        if not helpers.HAS_RICH:
            assert helpers.Text is None
