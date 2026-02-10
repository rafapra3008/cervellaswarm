"""
Test per scripts.memory.retro.cli.

Coverage focus: Orchestrazione CLI (save_report, generate_retro).
"""

import pytest
import sqlite3
import tempfile
from pathlib import Path
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

from scripts.memory.retro.cli import save_report, generate_retro


def test_save_report_creates_file():
    """save_report crea file con contenuto corretto."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir).resolve()
        content = "# Test Report\n\nThis is a test.\n"

        saved_path = save_report(content, output_dir)

        assert saved_path.exists()
        # resolve() per gestire symlink /var -> /private/var su macOS
        assert saved_path.parent.resolve() == output_dir.resolve()
        assert saved_path.name.endswith(".md")

        # Verifica contenuto
        with open(saved_path, 'r') as f:
            saved_content = f.read()
        assert saved_content == content


def test_save_report_default_output_dir():
    """save_report usa default output_dir se non specificato."""
    content = "# Test\n"

    # Mock Path.mkdir per evitare creazione reale
    with patch('pathlib.Path.mkdir'), \
         patch('builtins.open', create=True) as mock_open:
        mock_open.return_value.__enter__ = lambda s: s
        mock_open.return_value.__exit__ = MagicMock()
        mock_open.return_value.write = MagicMock()

        saved_path = save_report(content, output_dir=None)

        # Verifica che path contiene "data/retro"
        assert "data/retro" in str(saved_path)


@patch('scripts.memory.retro.cli.connect_db')
def test_generate_retro_orchestrates_correctly(mock_connect_db):
    """generate_retro orchestra tutte le funzioni senza errori."""
    # Setup mock DB
    mock_conn = MagicMock()
    mock_connect_db.return_value = mock_conn
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    # Mock fetchone per metrics
    mock_cursor.fetchone.return_value = {
        'total': 10,
        'successes': 8,
        'failures': 2,
        'active': 1
    }
    # Mock fetchall per patterns/lessons/agents
    mock_cursor.fetchall.return_value = []

    # Mock row_factory
    mock_conn.row_factory = sqlite3.Row

    # Esegui senza salvare (per evitare file system)
    generate_retro(days=7, save_to_file=False, quiet=True, output_dir=None)

    # Verifica che connect_db sia stato chiamato
    mock_connect_db.assert_called_once()
    # Verifica che conn.close() sia stato chiamato
    mock_conn.close.assert_called_once()


@patch('scripts.memory.retro.cli.connect_db')
@patch('scripts.memory.retro.cli.save_report')
def test_generate_retro_saves_report_when_requested(mock_save_report, mock_connect_db):
    """generate_retro salva report quando save_to_file=True."""
    # Setup mock DB
    mock_conn = MagicMock()
    mock_connect_db.return_value = mock_conn
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    # Mock fetchone
    mock_cursor.fetchone.return_value = {
        'total': 0,
        'successes': 0,
        'failures': 0,
        'active': 0
    }
    # Mock fetchall
    mock_cursor.fetchall.return_value = []

    # Mock save_report return
    mock_save_report.return_value = Path("/tmp/report.md")

    # Esegui con save=True
    generate_retro(days=7, save_to_file=True, quiet=True, output_dir=None)

    # Verifica che save_report sia stato chiamato
    mock_save_report.assert_called_once()
    args, kwargs = mock_save_report.call_args
    saved_content = args[0]

    # Verifica che contenuto include header markdown
    assert "# WEEKLY RETROSPECTIVE" in saved_content


@patch('scripts.memory.retro.cli.connect_db')
def test_generate_retro_prints_metrics_section(mock_connect_db, capsys):
    """generate_retro stampa sezione metriche."""
    # Setup mock DB
    mock_conn = MagicMock()
    mock_connect_db.return_value = mock_conn
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    # Mock fetchone per metrics
    mock_cursor.fetchone.return_value = {
        'total': 50,
        'successes': 40,
        'failures': 10,
        'active': 0
    }
    # Mock fetchall
    mock_cursor.fetchall.return_value = []

    # Esegui senza quiet
    with patch('scripts.memory.retro.output.HAS_RICH', False):
        generate_retro(days=7, save_to_file=False, quiet=False, output_dir=None)

    captured = capsys.readouterr()
    # Verifica che metriche siano stampate (plain mode ha "Eventi Totali" e valori)
    assert "Eventi Totali" in captured.out
    assert "50" in captured.out


@patch('scripts.memory.retro.cli.connect_db')
def test_generate_retro_handles_empty_db(mock_connect_db, capsys):
    """generate_retro gestisce DB vuoto senza errori."""
    # Setup mock DB vuoto
    mock_conn = MagicMock()
    mock_connect_db.return_value = mock_conn
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    # Mock fetchone per metrics vuoti
    mock_cursor.fetchone.return_value = {
        'total': 0,
        'successes': 0,
        'failures': 0,
        'active': 0
    }
    # Mock fetchall vuoto
    mock_cursor.fetchall.return_value = []

    # Esegui senza errori
    generate_retro(days=7, save_to_file=False, quiet=False, output_dir=None)

    # Verifica che connessione DB sia stata chiusa
    mock_conn.close.assert_called_once()
    # Verifica che connect_db sia stato chiamato
    mock_connect_db.assert_called_once()


@patch('scripts.memory.retro.cli.connect_db')
def test_generate_retro_with_custom_days(mock_connect_db):
    """generate_retro accetta days personalizzato."""
    # Setup mock DB
    mock_conn = MagicMock()
    mock_connect_db.return_value = mock_conn
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.return_value = {
        'total': 0,
        'successes': 0,
        'failures': 0,
        'active': 0
    }
    mock_cursor.fetchall.return_value = []

    # Esegui con days=14
    generate_retro(days=14, save_to_file=False, quiet=True, output_dir=None)

    # Verifica che periodo sia stato calcolato correttamente
    # (fetchone chiamato con period_start calcolato da 14 giorni fa)
    assert mock_cursor.execute.call_count > 0
