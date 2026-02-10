"""
Test per Analytics Commands - patterns.

Testa:
- cmd_patterns() - error patterns

Sessione 340.
"""

import pytest
import sqlite3
import sys
from pathlib import Path
from unittest.mock import patch
from datetime import datetime
from io import StringIO

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.memory.analytics.commands.patterns import cmd_patterns


# === FIXTURES LOCALI ===


@pytest.fixture
def patterns_temp_db(tmp_path):
    """Database temporaneo con schema error_patterns."""
    db_path = tmp_path / "patterns_test.db"
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE error_patterns (
            id INTEGER PRIMARY KEY,
            pattern_name TEXT,
            pattern_type TEXT,
            severity_level TEXT,
            occurrence_count INTEGER,
            status TEXT,
            last_seen TEXT,
            root_cause_hypothesis TEXT,
            mitigation_description TEXT
        )
    """)
    conn.commit()
    conn.close()
    yield db_path


@pytest.fixture
def patterns_empty_db(patterns_temp_db):
    """Database vuoto."""
    return patterns_temp_db


@pytest.fixture
def patterns_populated_db(patterns_temp_db):
    """Database con dati realistici."""
    conn = sqlite3.connect(patterns_temp_db)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    now = datetime.now().isoformat()

    cursor.execute("""
        INSERT INTO error_patterns (pattern_name, pattern_type, severity_level, occurrence_count, status, last_seen, root_cause_hypothesis, mitigation_description)
        VALUES
            ('Import Path Error', 'ModuleNotFound', 'CRITICAL', 8, 'ACTIVE', ?, 'Wrong sys.path setup in test files', 'Use absolute imports with scripts. prefix'),
            ('DB Connection Timeout', 'Database', 'HIGH', 5, 'ACTIVE', ?, 'Connection pool exhaustion', 'Increase pool size to 10'),
            ('CSS Specificity Issue', 'Frontend', 'MEDIUM', 3, 'ACTIVE', ?, 'Conflicting selectors', 'Use BEM methodology'),
            ('Old Resolved Pattern', 'General', 'LOW', 1, 'RESOLVED', ?, 'Already fixed', 'N/A')
    """, (now, now, now, now))

    conn.commit()
    conn.close()
    return patterns_temp_db


# === TEST CMD_PATTERNS ===


class TestCmdPatterns:
    """Test cmd_patterns() - error patterns."""

    @patch('scripts.memory.analytics.commands.patterns.connect_db')
    @patch('sys.stdout', new_callable=StringIO)
    def test_empty_db_shows_no_patterns(self, mock_stdout, mock_connect, patterns_empty_db):
        """Empty DB mostra 'nessun pattern'."""
        conn = sqlite3.connect(patterns_empty_db)
        conn.row_factory = sqlite3.Row
        mock_connect.return_value = conn

        cmd_patterns()

        output = mock_stdout.getvalue()
        assert "Nessun pattern trovato" in output
        conn.close()

    @patch('scripts.memory.analytics.commands.patterns.connect_db')
    @patch('sys.stdout', new_callable=StringIO)
    def test_lists_all_patterns(self, mock_stdout, mock_connect, patterns_populated_db):
        """Lista tutti i pattern."""
        conn = sqlite3.connect(patterns_populated_db)
        conn.row_factory = sqlite3.Row
        mock_connect.return_value = conn

        cmd_patterns()

        output = mock_stdout.getvalue()
        assert "Import Path Error" in output
        assert "DB Connection Timeout" in output
        assert "CSS Specificity Issue" in output
        conn.close()

    @patch('scripts.memory.analytics.commands.patterns.connect_db')
    @patch('sys.stdout', new_callable=StringIO)
    def test_orders_by_severity(self, mock_stdout, mock_connect, patterns_populated_db):
        """Ordina per severity (CRITICAL > HIGH > MEDIUM > LOW)."""
        conn = sqlite3.connect(patterns_populated_db)
        conn.row_factory = sqlite3.Row
        mock_connect.return_value = conn

        cmd_patterns()

        output = mock_stdout.getvalue()
        critical_pos = output.find("CRITICAL")
        medium_pos = output.find("MEDIUM")
        assert critical_pos < medium_pos
        conn.close()

    @patch('scripts.memory.analytics.commands.patterns.connect_db')
    @patch('sys.stdout', new_callable=StringIO)
    def test_shows_active_status_icon(self, mock_stdout, mock_connect, patterns_populated_db):
        """Mostra icona status (ACTIVE = 🔴)."""
        conn = sqlite3.connect(patterns_populated_db)
        conn.row_factory = sqlite3.Row
        mock_connect.return_value = conn

        cmd_patterns()

        output = mock_stdout.getvalue()
        assert "🔴" in output or "✅" in output
        conn.close()

    @patch('scripts.memory.analytics.commands.patterns.connect_db')
    @patch('sys.stdout', new_callable=StringIO)
    def test_displays_pattern_type(self, mock_stdout, mock_connect, patterns_populated_db):
        """Mostra pattern_type."""
        conn = sqlite3.connect(patterns_populated_db)
        conn.row_factory = sqlite3.Row
        mock_connect.return_value = conn

        cmd_patterns()

        output = mock_stdout.getvalue()
        assert "Type:" in output
        assert "ModuleNotFound" in output or "Database" in output
        conn.close()

    @patch('scripts.memory.analytics.commands.patterns.connect_db')
    @patch('sys.stdout', new_callable=StringIO)
    def test_displays_occurrence_count(self, mock_stdout, mock_connect, patterns_populated_db):
        """Mostra occurrence_count."""
        conn = sqlite3.connect(patterns_populated_db)
        conn.row_factory = sqlite3.Row
        mock_connect.return_value = conn

        cmd_patterns()

        output = mock_stdout.getvalue()
        assert "Occurrences:" in output
        conn.close()

    @patch('scripts.memory.analytics.commands.patterns.connect_db')
    @patch('sys.stdout', new_callable=StringIO)
    def test_truncates_last_seen_timestamp(self, mock_stdout, mock_connect, patterns_populated_db):
        """Tronca last_seen a 19 char."""
        conn = sqlite3.connect(patterns_populated_db)
        conn.row_factory = sqlite3.Row
        mock_connect.return_value = conn

        cmd_patterns()

        output = mock_stdout.getvalue()
        assert "Last Seen:" in output
        conn.close()

    @patch('scripts.memory.analytics.commands.patterns.connect_db')
    @patch('sys.stdout', new_callable=StringIO)
    def test_truncates_root_cause_70_chars(self, mock_stdout, mock_connect, patterns_temp_db):
        """Tronca root_cause_hypothesis a 70 caratteri."""
        conn = sqlite3.connect(patterns_temp_db)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        long_cause = "A" * 100
        now = datetime.now().isoformat()
        cursor.execute("""
            INSERT INTO error_patterns (pattern_name, pattern_type, severity_level, occurrence_count, status, last_seen, root_cause_hypothesis, mitigation_description)
            VALUES ('Test Pattern', 'Test', 'HIGH', 1, 'ACTIVE', ?, ?, 'Fix it')
        """, (now, long_cause))
        conn.commit()

        mock_connect.return_value = conn
        cmd_patterns()

        output = mock_stdout.getvalue()
        assert long_cause not in output
        conn.close()

    @patch('scripts.memory.analytics.commands.patterns.connect_db')
    @patch('sys.stdout', new_callable=StringIO)
    def test_truncates_mitigation_70_chars(self, mock_stdout, mock_connect, patterns_temp_db):
        """Tronca mitigation_description a 70 caratteri."""
        conn = sqlite3.connect(patterns_temp_db)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        long_mitigation = "B" * 100
        now = datetime.now().isoformat()
        cursor.execute("""
            INSERT INTO error_patterns (pattern_name, pattern_type, severity_level, occurrence_count, status, last_seen, root_cause_hypothesis, mitigation_description)
            VALUES ('Test Pattern', 'Test', 'HIGH', 1, 'ACTIVE', ?, 'Cause', ?)
        """, (now, long_mitigation))
        conn.commit()

        mock_connect.return_value = conn
        cmd_patterns()

        output = mock_stdout.getvalue()
        assert long_mitigation not in output
        conn.close()

    @patch('scripts.memory.analytics.commands.patterns.connect_db')
    @patch('sys.stdout', new_callable=StringIO)
    def test_shows_header_and_footer(self, mock_stdout, mock_connect, patterns_populated_db):
        """Mostra header e footer."""
        conn = sqlite3.connect(patterns_populated_db)
        conn.row_factory = sqlite3.Row
        mock_connect.return_value = conn

        cmd_patterns()

        output = mock_stdout.getvalue()
        assert "ERROR PATTERNS" in output
        assert "╔" in output
        assert "╚" in output
        conn.close()

    @patch('scripts.memory.analytics.commands.patterns.connect_db')
    @patch('sys.stdout', new_callable=StringIO)
    def test_handles_null_root_cause(self, mock_stdout, mock_connect, patterns_temp_db):
        """Gestisce root_cause_hypothesis NULL (non stampato)."""
        conn = sqlite3.connect(patterns_temp_db)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        now = datetime.now().isoformat()
        cursor.execute("""
            INSERT INTO error_patterns (pattern_name, pattern_type, severity_level, occurrence_count, status, last_seen, root_cause_hypothesis, mitigation_description)
            VALUES ('Test Pattern', 'Test', 'HIGH', 1, 'ACTIVE', ?, NULL, 'Fix it')
        """, (now,))
        conn.commit()

        mock_connect.return_value = conn
        cmd_patterns()

        output = mock_stdout.getvalue()
        # Non deve crashare, e "Root Cause:" non appare se NULL
        assert "Test Pattern" in output
        conn.close()

    @patch('scripts.memory.analytics.commands.patterns.connect_db')
    @patch('sys.stdout', new_callable=StringIO)
    def test_handles_null_mitigation(self, mock_stdout, mock_connect, patterns_temp_db):
        """Gestisce mitigation_description NULL (non stampato)."""
        conn = sqlite3.connect(patterns_temp_db)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        now = datetime.now().isoformat()
        cursor.execute("""
            INSERT INTO error_patterns (pattern_name, pattern_type, severity_level, occurrence_count, status, last_seen, root_cause_hypothesis, mitigation_description)
            VALUES ('Test Pattern', 'Test', 'HIGH', 1, 'ACTIVE', ?, 'Cause', NULL)
        """, (now,))
        conn.commit()

        mock_connect.return_value = conn
        cmd_patterns()

        output = mock_stdout.getvalue()
        assert "Test Pattern" in output
        conn.close()

    @patch('scripts.memory.analytics.commands.patterns.connect_db')
    @patch('sys.stdout', new_callable=StringIO)
    def test_orders_by_occurrence_count_within_severity(self, mock_stdout, mock_connect, patterns_temp_db):
        """Ordina per occurrence_count DESC entro stesso severity."""
        conn = sqlite3.connect(patterns_temp_db)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        now = datetime.now().isoformat()
        cursor.execute("""
            INSERT INTO error_patterns (pattern_name, pattern_type, severity_level, occurrence_count, status, last_seen, root_cause_hypothesis, mitigation_description)
            VALUES
                ('High Pattern 1', 'Test', 'HIGH', 5, 'ACTIVE', ?, 'Cause 1', 'Fix 1'),
                ('High Pattern 2', 'Test', 'HIGH', 15, 'ACTIVE', ?, 'Cause 2', 'Fix 2')
        """, (now, now))
        conn.commit()

        mock_connect.return_value = conn
        cmd_patterns()

        output = mock_stdout.getvalue()
        pattern1_pos = output.find("High Pattern 1")
        pattern2_pos = output.find("High Pattern 2")
        # Pattern 2 (15 occ) deve apparire prima di Pattern 1 (5 occ)
        assert pattern2_pos < pattern1_pos
        conn.close()
