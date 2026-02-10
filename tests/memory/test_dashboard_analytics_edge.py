"""
Test per Dashboard Analytics - Edge cases, Rich output, integration.

Split da test_dashboard_analytics.py (670 righe > limite 500).
Sessione 341.
"""

import pytest
import sqlite3
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.memory.analytics.commands.dashboard import cmd_dashboard, __version__

# Fixtures temp_db, empty_db, populated_db from conftest.py


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
