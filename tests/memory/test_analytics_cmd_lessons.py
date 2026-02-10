"""
Test per Analytics Commands - lessons.

Testa:
- cmd_lessons() - lezioni apprese

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

from scripts.memory.analytics.commands.lessons import cmd_lessons


# === FIXTURES LOCALI ===


@pytest.fixture
def lessons_temp_db(tmp_path):
    """Database temporaneo con schema lessons_learned."""
    db_path = tmp_path / "lessons_test.db"
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

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
def lessons_empty_db(lessons_temp_db):
    """Database vuoto."""
    return lessons_temp_db


@pytest.fixture
def lessons_populated_db(lessons_temp_db):
    """Database con dati realistici."""
    conn = sqlite3.connect(lessons_temp_db)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO lessons_learned (pattern, category, severity, status, prevention, occurrence_count, time_wasted_minutes)
        VALUES
            ('Import Error Pattern', 'Testing', 'CRITICAL', 'ACTIVE', 'Use absolute imports', 5, 120),
            ('DB Connection Pool', 'Backend', 'HIGH', 'ACTIVE', 'Add connection pooling', 3, 60),
            ('CSS z-index issue', 'Frontend', 'MEDIUM', 'ACTIVE', 'Use CSS layers', 2, 30),
            ('Old resolved lesson', 'General', 'LOW', 'RESOLVED', 'Already fixed', 1, 10)
    """)

    conn.commit()
    conn.close()
    return lessons_temp_db


# === TEST CMD_LESSONS ===


class TestCmdLessons:
    """Test cmd_lessons() - lezioni apprese."""

    @patch('scripts.memory.analytics.commands.lessons.connect_db')
    @patch('sys.stdout', new_callable=StringIO)
    def test_empty_db_shows_no_lessons(self, mock_stdout, mock_connect, lessons_empty_db):
        """Empty DB mostra 'nessuna lezione'."""
        conn = sqlite3.connect(lessons_empty_db)
        conn.row_factory = sqlite3.Row
        mock_connect.return_value = conn

        cmd_lessons()

        output = mock_stdout.getvalue()
        assert "Nessuna lezione trovata" in output
        conn.close()

    @patch('scripts.memory.analytics.commands.lessons.connect_db')
    @patch('sys.stdout', new_callable=StringIO)
    def test_lists_all_lessons(self, mock_stdout, mock_connect, lessons_populated_db):
        """Lista tutte le lezioni."""
        conn = sqlite3.connect(lessons_populated_db)
        conn.row_factory = sqlite3.Row
        mock_connect.return_value = conn

        cmd_lessons()

        output = mock_stdout.getvalue()
        assert "Import Error Pattern" in output
        assert "DB Connection Pool" in output
        assert "CSS z-index issue" in output
        conn.close()

    @patch('scripts.memory.analytics.commands.lessons.connect_db')
    @patch('sys.stdout', new_callable=StringIO)
    def test_orders_by_severity(self, mock_stdout, mock_connect, lessons_populated_db):
        """Ordina per severity (CRITICAL > HIGH > MEDIUM > LOW)."""
        conn = sqlite3.connect(lessons_populated_db)
        conn.row_factory = sqlite3.Row
        mock_connect.return_value = conn

        cmd_lessons()

        output = mock_stdout.getvalue()
        critical_pos = output.find("CRITICAL")
        medium_pos = output.find("MEDIUM")
        assert critical_pos < medium_pos
        conn.close()

    @patch('scripts.memory.analytics.commands.lessons.connect_db')
    @patch('sys.stdout', new_callable=StringIO)
    def test_shows_active_status_icon(self, mock_stdout, mock_connect, lessons_populated_db):
        """Mostra icona status (ACTIVE = 🔴, altro = ✅)."""
        conn = sqlite3.connect(lessons_populated_db)
        conn.row_factory = sqlite3.Row
        mock_connect.return_value = conn

        cmd_lessons()

        output = mock_stdout.getvalue()
        assert "🔴" in output or "✅" in output
        conn.close()

    @patch('scripts.memory.analytics.commands.lessons.connect_db')
    @patch('sys.stdout', new_callable=StringIO)
    def test_displays_category(self, mock_stdout, mock_connect, lessons_populated_db):
        """Mostra category."""
        conn = sqlite3.connect(lessons_populated_db)
        conn.row_factory = sqlite3.Row
        mock_connect.return_value = conn

        cmd_lessons()

        output = mock_stdout.getvalue()
        assert "Category:" in output
        assert "Testing" in output or "Backend" in output
        conn.close()

    @patch('scripts.memory.analytics.commands.lessons.connect_db')
    @patch('sys.stdout', new_callable=StringIO)
    def test_displays_prevention(self, mock_stdout, mock_connect, lessons_populated_db):
        """Mostra prevention (troncato a 80 char)."""
        conn = sqlite3.connect(lessons_populated_db)
        conn.row_factory = sqlite3.Row
        mock_connect.return_value = conn

        cmd_lessons()

        output = mock_stdout.getvalue()
        assert "Prevention:" in output
        assert "Use absolute imports" in output or "Add connection pooling" in output
        conn.close()

    @patch('scripts.memory.analytics.commands.lessons.connect_db')
    @patch('sys.stdout', new_callable=StringIO)
    def test_displays_occurrence_count(self, mock_stdout, mock_connect, lessons_populated_db):
        """Mostra occurrence_count."""
        conn = sqlite3.connect(lessons_populated_db)
        conn.row_factory = sqlite3.Row
        mock_connect.return_value = conn

        cmd_lessons()

        output = mock_stdout.getvalue()
        assert "Occurrences:" in output
        conn.close()

    @patch('scripts.memory.analytics.commands.lessons.connect_db')
    @patch('sys.stdout', new_callable=StringIO)
    def test_displays_time_wasted_minutes(self, mock_stdout, mock_connect, lessons_populated_db):
        """Mostra time_wasted_minutes."""
        conn = sqlite3.connect(lessons_populated_db)
        conn.row_factory = sqlite3.Row
        mock_connect.return_value = conn

        cmd_lessons()

        output = mock_stdout.getvalue()
        assert "Time Wasted:" in output
        assert "min" in output
        conn.close()

    @patch('scripts.memory.analytics.commands.lessons.connect_db')
    @patch('sys.stdout', new_callable=StringIO)
    def test_uses_severity_color(self, mock_stdout, mock_connect, lessons_populated_db):
        """Usa get_severity_color per colorare severity."""
        conn = sqlite3.connect(lessons_populated_db)
        conn.row_factory = sqlite3.Row
        mock_connect.return_value = conn

        cmd_lessons()

        output = mock_stdout.getvalue()
        assert "CRITICAL" in output or "HIGH" in output or "MEDIUM" in output
        conn.close()

    @patch('scripts.memory.analytics.commands.lessons.connect_db')
    @patch('sys.stdout', new_callable=StringIO)
    def test_shows_header_and_footer(self, mock_stdout, mock_connect, lessons_populated_db):
        """Mostra header e footer."""
        conn = sqlite3.connect(lessons_populated_db)
        conn.row_factory = sqlite3.Row
        mock_connect.return_value = conn

        cmd_lessons()

        output = mock_stdout.getvalue()
        assert "LESSONS LEARNED" in output
        assert "╔" in output
        assert "╚" in output
        conn.close()

    @patch('scripts.memory.analytics.commands.lessons.connect_db')
    @patch('sys.stdout', new_callable=StringIO)
    def test_handles_null_category(self, mock_stdout, mock_connect, lessons_temp_db):
        """Gestisce category NULL mostrando N/A."""
        conn = sqlite3.connect(lessons_temp_db)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO lessons_learned (pattern, category, severity, status, prevention, occurrence_count, time_wasted_minutes)
            VALUES ('Test Pattern', NULL, 'HIGH', 'ACTIVE', 'Fix it', 1, 10)
        """)
        conn.commit()

        mock_connect.return_value = conn
        cmd_lessons()

        output = mock_stdout.getvalue()
        assert "N/A" in output
        conn.close()

    @patch('scripts.memory.analytics.commands.lessons.connect_db')
    @patch('sys.stdout', new_callable=StringIO)
    def test_handles_null_time_wasted(self, mock_stdout, mock_connect, lessons_temp_db):
        """Gestisce time_wasted_minutes NULL mostrando 0."""
        conn = sqlite3.connect(lessons_temp_db)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO lessons_learned (pattern, category, severity, status, prevention, occurrence_count, time_wasted_minutes)
            VALUES ('Test Pattern', 'Test', 'HIGH', 'ACTIVE', 'Fix it', 1, NULL)
        """)
        conn.commit()

        mock_connect.return_value = conn
        cmd_lessons()

        output = mock_stdout.getvalue()
        assert "0 min" in output
        conn.close()

    @patch('scripts.memory.analytics.commands.lessons.connect_db')
    @patch('sys.stdout', new_callable=StringIO)
    def test_orders_by_occurrence_count_within_severity(self, mock_stdout, mock_connect, lessons_temp_db):
        """Ordina per occurrence_count DESC entro stesso severity."""
        conn = sqlite3.connect(lessons_temp_db)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO lessons_learned (pattern, category, severity, status, prevention, occurrence_count, time_wasted_minutes)
            VALUES
                ('High Pattern 1', 'Test', 'HIGH', 'ACTIVE', 'Fix 1', 10, 100),
                ('High Pattern 2', 'Test', 'HIGH', 'ACTIVE', 'Fix 2', 20, 200)
        """)
        conn.commit()

        mock_connect.return_value = conn
        cmd_lessons()

        output = mock_stdout.getvalue()
        pattern1_pos = output.find("High Pattern 1")
        pattern2_pos = output.find("High Pattern 2")
        # Pattern 2 (20 occ) deve apparire prima di Pattern 1 (10 occ)
        assert pattern2_pos < pattern1_pos
        conn.close()
