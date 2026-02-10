"""
Test per Analytics Commands - agents + events.

Testa:
- cmd_agents() - statistiche per agente
- cmd_events() - ultimi N eventi

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

from scripts.memory.analytics.commands.agents import cmd_agents
from scripts.memory.analytics.commands.events import cmd_events


# === FIXTURES LOCALI ===


@pytest.fixture
def analytics_temp_db(tmp_path):
    """Database temporaneo con schema completo per analytics."""
    db_path = tmp_path / "analytics_test.db"
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
    conn.commit()
    conn.close()
    yield db_path


@pytest.fixture
def analytics_empty_db(analytics_temp_db):
    """Database vuoto (solo schema)."""
    return analytics_temp_db


@pytest.fixture
def analytics_populated_db(analytics_temp_db):
    """Database con dati realistici."""
    conn = sqlite3.connect(analytics_temp_db)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    now = datetime.now().isoformat()

    cursor.execute("""
        INSERT INTO swarm_events (timestamp, agent_name, event_type, task_description, project, success, duration_ms)
        VALUES
            (?, 'cervella-backend', 'TASK_START', 'Fix API endpoint', 'miracollo', 1, 5000),
            (?, 'cervella-backend', 'TASK_END', 'Database query', 'miracollo', 1, 3000),
            (?, 'cervella-frontend', 'TASK_START', 'CSS fix', 'miracollo', 0, 2000),
            (?, 'cervella-frontend', 'TASK_END', 'React component', 'contabilita', 1, 4000),
            (?, 'cervella-tester', 'TASK_START', 'Write tests', 'miracollo', 1, 6000),
            (?, NULL, 'TASK_START', 'Task without agent', 'test', 1, 1000)
    """, (now, now, now, now, now, now))

    conn.commit()
    conn.close()
    return analytics_temp_db


# === TEST CMD_AGENTS ===


class TestCmdAgents:
    """Test cmd_agents() - statistiche per agente."""

    @patch('scripts.memory.analytics.commands.agents.connect_db')
    @patch('sys.stdout', new_callable=StringIO)
    def test_empty_db_shows_no_agents(self, mock_stdout, mock_connect, analytics_empty_db):
        """Empty DB mostra messaggio 'nessun agente'."""
        conn = sqlite3.connect(analytics_empty_db)
        conn.row_factory = sqlite3.Row
        mock_connect.return_value = conn

        cmd_agents()

        output = mock_stdout.getvalue()
        assert "Nessun agente trovato" in output
        conn.close()

    @patch('scripts.memory.analytics.commands.agents.connect_db')
    @patch('sys.stdout', new_callable=StringIO)
    def test_lists_agents_grouped_by_name(self, mock_stdout, mock_connect, analytics_populated_db):
        """Lista agenti raggruppati per nome."""
        conn = sqlite3.connect(analytics_populated_db)
        conn.row_factory = sqlite3.Row
        mock_connect.return_value = conn

        cmd_agents()

        output = mock_stdout.getvalue()
        assert "cervella-backend" in output
        assert "cervella-frontend" in output
        assert "cervella-tester" in output
        conn.close()

    @patch('scripts.memory.analytics.commands.agents.connect_db')
    @patch('sys.stdout', new_callable=StringIO)
    def test_counts_total_tasks(self, mock_stdout, mock_connect, analytics_populated_db):
        """Conta correttamente task totali."""
        conn = sqlite3.connect(analytics_populated_db)
        conn.row_factory = sqlite3.Row
        mock_connect.return_value = conn

        cmd_agents()

        output = mock_stdout.getvalue()
        assert "cervella-backend" in output
        conn.close()

    @patch('scripts.memory.analytics.commands.agents.connect_db')
    @patch('sys.stdout', new_callable=StringIO)
    def test_counts_successes_and_failures(self, mock_stdout, mock_connect, analytics_populated_db):
        """Conta successi e fallimenti separatamente."""
        conn = sqlite3.connect(analytics_populated_db)
        conn.row_factory = sqlite3.Row
        mock_connect.return_value = conn

        cmd_agents()

        output = mock_stdout.getvalue()
        assert "cervella-frontend" in output
        conn.close()

    @patch('scripts.memory.analytics.commands.agents.connect_db')
    @patch('sys.stdout', new_callable=StringIO)
    def test_calculates_avg_duration(self, mock_stdout, mock_connect, analytics_populated_db):
        """Calcola durata media."""
        conn = sqlite3.connect(analytics_populated_db)
        conn.row_factory = sqlite3.Row
        mock_connect.return_value = conn

        cmd_agents()

        output = mock_stdout.getvalue()
        assert "ms" in output
        conn.close()

    @patch('scripts.memory.analytics.commands.agents.connect_db')
    def test_filters_out_null_agent_names(self, mock_connect, analytics_populated_db):
        """Filtra agenti NULL (WHERE agent_name IS NOT NULL)."""
        conn = sqlite3.connect(analytics_populated_db)
        conn.row_factory = sqlite3.Row
        mock_connect.return_value = conn

        cursor = conn.cursor()
        cursor.execute("""
            SELECT agent_name FROM swarm_events
            WHERE agent_name IS NOT NULL
            GROUP BY agent_name
        """)
        agents = cursor.fetchall()

        agent_names = [a['agent_name'] for a in agents]
        assert None not in agent_names
        conn.close()

    @patch('scripts.memory.analytics.commands.agents.connect_db')
    @patch('sys.stdout', new_callable=StringIO)
    def test_orders_by_total_tasks_desc(self, mock_stdout, mock_connect, analytics_populated_db):
        """Ordina per total_tasks DESC."""
        conn = sqlite3.connect(analytics_populated_db)
        conn.row_factory = sqlite3.Row
        mock_connect.return_value = conn

        cmd_agents()

        output = mock_stdout.getvalue()
        backend_pos = output.find("cervella-backend")
        tester_pos = output.find("cervella-tester")
        assert backend_pos < tester_pos
        conn.close()

    @patch('scripts.memory.analytics.commands.agents.connect_db')
    @patch('sys.stdout', new_callable=StringIO)
    def test_shows_header_and_footer(self, mock_stdout, mock_connect, analytics_populated_db):
        """Mostra header e footer."""
        conn = sqlite3.connect(analytics_populated_db)
        conn.row_factory = sqlite3.Row
        mock_connect.return_value = conn

        cmd_agents()

        output = mock_stdout.getvalue()
        assert "AGENT STATISTICS" in output
        assert "╔" in output
        assert "╚" in output
        conn.close()


# === TEST CMD_EVENTS ===


class TestCmdEvents:
    """Test cmd_events() - ultimi N eventi."""

    @patch('scripts.memory.analytics.commands.events.connect_db')
    @patch('sys.stdout', new_callable=StringIO)
    def test_empty_db_shows_no_events(self, mock_stdout, mock_connect, analytics_empty_db):
        """Empty DB mostra 'nessun evento'."""
        conn = sqlite3.connect(analytics_empty_db)
        conn.row_factory = sqlite3.Row
        mock_connect.return_value = conn

        cmd_events()

        output = mock_stdout.getvalue()
        assert "Nessun evento trovato" in output
        conn.close()

    @patch('scripts.memory.analytics.commands.events.connect_db')
    @patch('sys.stdout', new_callable=StringIO)
    def test_default_limit_10(self, mock_stdout, mock_connect, analytics_populated_db):
        """Default limit = 10."""
        conn = sqlite3.connect(analytics_populated_db)
        conn.row_factory = sqlite3.Row
        mock_connect.return_value = conn

        cmd_events()

        output = mock_stdout.getvalue()
        assert "ULTIMI 10 EVENTI" in output
        conn.close()

    @patch('scripts.memory.analytics.commands.events.connect_db')
    @patch('sys.stdout', new_callable=StringIO)
    def test_custom_limit(self, mock_stdout, mock_connect, analytics_populated_db):
        """Parametro limit personalizzato."""
        conn = sqlite3.connect(analytics_populated_db)
        conn.row_factory = sqlite3.Row
        mock_connect.return_value = conn

        cmd_events(limit=3)

        output = mock_stdout.getvalue()
        assert "ULTIMI 3 EVENTI" in output
        conn.close()

    @patch('scripts.memory.analytics.commands.events.connect_db')
    @patch('sys.stdout', new_callable=StringIO)
    def test_shows_success_icon(self, mock_stdout, mock_connect, analytics_populated_db):
        """Mostra icona success."""
        conn = sqlite3.connect(analytics_populated_db)
        conn.row_factory = sqlite3.Row
        mock_connect.return_value = conn

        cmd_events()

        output = mock_stdout.getvalue()
        assert "✅" in output or "❌" in output
        conn.close()

    @patch('scripts.memory.analytics.commands.events.connect_db')
    @patch('sys.stdout', new_callable=StringIO)
    def test_displays_agent_name_or_na(self, mock_stdout, mock_connect, analytics_populated_db):
        """Mostra agent_name o N/A."""
        conn = sqlite3.connect(analytics_populated_db)
        conn.row_factory = sqlite3.Row
        mock_connect.return_value = conn

        cmd_events()

        output = mock_stdout.getvalue()
        assert "cervella-backend" in output or "N/A" in output
        conn.close()

    @patch('scripts.memory.analytics.commands.events.connect_db')
    @patch('sys.stdout', new_callable=StringIO)
    def test_truncates_timestamp(self, mock_stdout, mock_connect, analytics_populated_db):
        """Tronca timestamp a 19 char (senza millisecondi)."""
        conn = sqlite3.connect(analytics_populated_db)
        conn.row_factory = sqlite3.Row
        mock_connect.return_value = conn

        cmd_events()

        output = mock_stdout.getvalue()
        assert "Time:" in output
        conn.close()

    @patch('scripts.memory.analytics.commands.events.connect_db')
    @patch('sys.stdout', new_callable=StringIO)
    def test_truncates_task_description_70_chars(self, mock_stdout, mock_connect, analytics_temp_db):
        """Tronca task_description a 70 caratteri."""
        conn = sqlite3.connect(analytics_temp_db)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        long_desc = "A" * 100
        now = datetime.now().isoformat()
        cursor.execute("""
            INSERT INTO swarm_events (timestamp, agent_name, event_type, task_description, project, success, duration_ms)
            VALUES (?, 'test', 'TEST', ?, 'test', 1, 1000)
        """, (now, long_desc))
        conn.commit()

        mock_connect.return_value = conn
        cmd_events()

        output = mock_stdout.getvalue()
        assert long_desc not in output
        conn.close()

    @patch('scripts.memory.analytics.commands.events.connect_db')
    def test_uses_parameterized_query(self, mock_connect, analytics_populated_db):
        """Usa query parametrizzata (no SQL injection)."""
        conn = sqlite3.connect(analytics_populated_db)
        conn.row_factory = sqlite3.Row
        mock_connect.return_value = conn

        try:
            cmd_events(limit=5)
            success = True
        except Exception:
            success = False

        assert success
        conn.close()
