"""
Test per scripts.memory.retro.cli - Helper functions e main().

Coverage focus: _print_and_save_* helpers con dati reali + main() CLI.
Split da test_retro_cli.py per rispettare limite 500 righe.
"""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from scripts.memory.retro.cli import generate_retro


@patch('scripts.memory.retro.cli.connect_db')
@patch('scripts.memory.retro.cli.save_report')
def test_generate_retro_saves_patterns_with_data(mock_save_report, mock_connect_db):
    """_print_and_save_patterns con dati reali (lines 162-169)."""
    mock_conn = MagicMock()
    mock_connect_db.return_value = mock_conn
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.return_value = {
        'total': 10, 'successes': 8, 'failures': 2, 'active': 1
    }

    mock_cursor.fetchall.side_effect = [
        [
            {'severity_level': 'HIGH', 'pattern_name': 'ImportError', 'occurrence_count': 5},
            {'severity_level': 'MEDIUM', 'pattern_name': 'TypeError', 'occurrence_count': 3}
        ],
        [], [], [], [],
    ]

    mock_save_report.return_value = Path("/tmp/report.md")
    generate_retro(days=7, save_to_file=True, quiet=True, output_dir=None)

    args, _ = mock_save_report.call_args
    saved_content = args[0]

    assert "TOP 3 PATTERN ERRORI" in saved_content
    assert "[HIGH]" in saved_content
    assert "ImportError" in saved_content
    assert "Count: 5" in saved_content


@patch('scripts.memory.retro.cli.connect_db')
@patch('scripts.memory.retro.cli.save_report')
def test_generate_retro_saves_lessons_with_data(mock_save_report, mock_connect_db):
    """_print_and_save_lessons con dati reali (lines 180-187)."""
    mock_conn = MagicMock()
    mock_connect_db.return_value = mock_conn
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.return_value = {
        'total': 5, 'successes': 5, 'failures': 0, 'active': 0
    }

    mock_cursor.fetchall.side_effect = [
        [],
        [
            {'severity': 'CRITICAL', 'pattern': 'Never push to main without CI'},
            {'severity': 'HIGH', 'pattern': 'Always validate user input'}
        ],
        [], [], []
    ]

    mock_save_report.return_value = Path("/tmp/report.md")
    generate_retro(days=7, save_to_file=True, quiet=True, output_dir=None)

    args, _ = mock_save_report.call_args
    saved_content = args[0]

    assert "LEZIONI APPRESE (2)" in saved_content
    assert "[CRITICAL]" in saved_content
    assert "Never push to main without CI" in saved_content


@patch('scripts.memory.retro.cli.connect_db')
@patch('scripts.memory.retro.cli.save_report')
def test_generate_retro_saves_agents_with_data(mock_save_report, mock_connect_db):
    """_print_and_save_agents con dati reali (lines 198-208)."""
    mock_conn = MagicMock()
    mock_connect_db.return_value = mock_conn
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.return_value = {
        'total': 20, 'successes': 18, 'failures': 2, 'active': 1
    }

    mock_cursor.fetchall.side_effect = [
        [], [],
        [
            {'agent_name': 'cervella-backend', 'total': 10, 'successes': 9, 'failures': 1, 'avg_duration': 2500.5},
            {'agent_name': 'cervella-frontend', 'total': 8, 'successes': 7, 'failures': 1, 'avg_duration': None}
        ],
        [], []
    ]

    mock_save_report.return_value = Path("/tmp/report.md")
    generate_retro(days=7, save_to_file=True, quiet=True, output_dir=None)

    args, _ = mock_save_report.call_args
    saved_content = args[0]

    assert "BREAKDOWN PER AGENTE (Top 5)" in saved_content
    assert "cervella-backend" in saved_content
    assert "2500ms" in saved_content
    assert "N/A" in saved_content


@patch('scripts.memory.retro.cli.connect_db')
@patch('scripts.memory.retro.cli.save_report')
def test_generate_retro_saves_suggestions_with_data(mock_save_report, mock_connect_db):
    """_print_and_save_suggestions con dati reali (lines 231-250)."""
    mock_conn = MagicMock()
    mock_connect_db.return_value = mock_conn
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.return_value = {
        'total': 10, 'successes': 8, 'failures': 2, 'active': 1
    }

    mock_cursor.fetchall.side_effect = [[], [], [], [], []]

    with patch('scripts.memory.retro.cli.suggest_new_lessons') as mock_suggest:
        mock_suggest.return_value = [
            ('pattern', 3, 'Pattern X ripetuto 3 volte'),
            ('agent', 0.5, 'Agent Y ha success rate 50%')
        ]

        mock_save_report.return_value = Path("/tmp/report.md")
        generate_retro(days=7, save_to_file=True, quiet=True, output_dir=None)

    args, _ = mock_save_report.call_args
    saved_content = args[0]

    assert "LEZIONI SUGGERITE" in saved_content
    assert "Pattern ripetuti senza lezione documentata:" in saved_content
    assert "Pattern X ripetuto 3 volte" in saved_content
    assert "Agenti con basso success rate:" in saved_content
    assert "Agent Y ha success rate 50%" in saved_content


@patch('scripts.memory.retro.cli.connect_db')
@patch('scripts.memory.retro.cli.save_report')
def test_save_and_notify_with_rich(mock_save_report, mock_connect_db):
    """_save_and_notify con HAS_RICH=True (line 279)."""
    mock_conn = MagicMock()
    mock_connect_db.return_value = mock_conn
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.return_value = {'total': 0, 'successes': 0, 'failures': 0, 'active': 0}
    mock_cursor.fetchall.return_value = []

    mock_save_report.return_value = Path("/tmp/report.md")

    with patch('scripts.memory.retro.cli.HAS_RICH', True), \
         patch('scripts.memory.retro.cli.console') as mock_console:
        generate_retro(days=7, save_to_file=True, quiet=False, output_dir=None)
        mock_console.print.assert_any_call("[green]\u2705 Report salvato:[/green] /tmp/report.md\n")


@patch('scripts.memory.retro.cli.connect_db')
@patch('scripts.memory.retro.cli.save_report')
def test_save_and_notify_without_rich(mock_save_report, mock_connect_db, capsys):
    """_save_and_notify con HAS_RICH=False (line 281)."""
    mock_conn = MagicMock()
    mock_connect_db.return_value = mock_conn
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.return_value = {'total': 0, 'successes': 0, 'failures': 0, 'active': 0}
    mock_cursor.fetchall.return_value = []

    mock_save_report.return_value = Path("/tmp/report.md")

    with patch('scripts.memory.retro.cli.HAS_RICH', False):
        generate_retro(days=7, save_to_file=True, quiet=False, output_dir=None)

    captured = capsys.readouterr()
    assert "\u2705 Report salvato: /tmp/report.md" in captured.out


# === main() tests ===

@patch('sys.argv', ['cli', '-d', '14'])
@patch('scripts.memory.retro.cli.connect_db')
def test_main_normal_execution(mock_connect_db):
    """main() esegue correttamente con args validi."""
    mock_conn = MagicMock()
    mock_connect_db.return_value = mock_conn
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.return_value = {'total': 0, 'successes': 0, 'failures': 0, 'active': 0}
    mock_cursor.fetchall.return_value = []

    from scripts.memory.retro.cli import main
    main()

    mock_connect_db.assert_called_once()


@patch('sys.argv', ['cli', '-d', '0'])
@patch('scripts.memory.retro.cli.HAS_RICH', True)
@patch('scripts.memory.retro.cli.console')
def test_main_days_validation_error_with_rich(mock_console, capsys):
    """main() con args.days < 1 e HAS_RICH=True (lines 342-343)."""
    from scripts.memory.retro.cli import main

    with pytest.raises(SystemExit) as exc_info:
        main()

    assert exc_info.value.code == 1
    mock_console.print.assert_called_with("[red]\u274c Errore: --days deve essere >= 1[/red]")


@patch('sys.argv', ['cli', '-d', '0'])
@patch('scripts.memory.retro.cli.HAS_RICH', False)
def test_main_days_validation_error_without_rich(capsys):
    """main() con args.days < 1 e HAS_RICH=False (lines 344-345)."""
    from scripts.memory.retro.cli import main

    with pytest.raises(SystemExit) as exc_info:
        main()

    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "\u274c Errore: --days deve essere >= 1" in captured.out


@patch('sys.argv', ['cli', '-d', '400'])
@patch('scripts.memory.retro.cli.HAS_RICH', True)
@patch('scripts.memory.retro.cli.console')
@patch('scripts.memory.retro.cli.connect_db')
def test_main_days_warning_with_rich(mock_connect_db, mock_console):
    """main() con args.days > 365 e HAS_RICH=True (lines 349-350)."""
    mock_conn = MagicMock()
    mock_connect_db.return_value = mock_conn
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = {'total': 0, 'successes': 0, 'failures': 0, 'active': 0}
    mock_cursor.fetchall.return_value = []

    from scripts.memory.retro.cli import main
    main()

    mock_console.print.assert_any_call("[yellow]\u26a0\ufe0f  Attenzione: Analisi > 1 anno potrebbe essere lenta[/yellow]")


@patch('sys.argv', ['cli', '-d', '400'])
@patch('scripts.memory.retro.cli.HAS_RICH', False)
@patch('scripts.memory.retro.cli.connect_db')
def test_main_days_warning_without_rich(mock_connect_db, capsys):
    """main() con args.days > 365 e HAS_RICH=False (lines 351-352)."""
    mock_conn = MagicMock()
    mock_connect_db.return_value = mock_conn
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = {'total': 0, 'successes': 0, 'failures': 0, 'active': 0}
    mock_cursor.fetchall.return_value = []

    from scripts.memory.retro.cli import main
    main()

    captured = capsys.readouterr()
    assert "\u26a0\ufe0f  Attenzione: Analisi > 1 anno potrebbe essere lenta" in captured.out


# === Print-when-not-quiet tests ===

@patch('scripts.memory.retro.cli.connect_db')
def test_generate_retro_prints_patterns_when_not_quiet(mock_connect_db):
    """_print_and_save_patterns chiama print_patterns_section quando not quiet."""
    mock_conn = MagicMock()
    mock_connect_db.return_value = mock_conn
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.return_value = {'total': 10, 'successes': 8, 'failures': 2, 'active': 1}
    mock_cursor.fetchall.side_effect = [
        [{'severity_level': 'HIGH', 'pattern_name': 'TestError', 'occurrence_count': 3}],
        [], [], [], []
    ]

    with patch('scripts.memory.retro.cli.print_patterns_section') as mock_print:
        generate_retro(days=7, save_to_file=False, quiet=False, output_dir=None)
        mock_print.assert_called_once()


@patch('scripts.memory.retro.cli.connect_db')
def test_generate_retro_prints_lessons_when_not_quiet(mock_connect_db):
    """_print_and_save_lessons chiama print_lessons_section quando not quiet."""
    mock_conn = MagicMock()
    mock_connect_db.return_value = mock_conn
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.return_value = {'total': 5, 'successes': 5, 'failures': 0, 'active': 0}
    mock_cursor.fetchall.side_effect = [
        [],
        [{'severity': 'HIGH', 'pattern': 'Test lesson'}],
        [], [], []
    ]

    with patch('scripts.memory.retro.cli.print_lessons_section') as mock_print:
        generate_retro(days=7, save_to_file=False, quiet=False, output_dir=None)
        mock_print.assert_called_once()


@patch('scripts.memory.retro.cli.connect_db')
def test_generate_retro_prints_agents_when_not_quiet(mock_connect_db):
    """_print_and_save_agents chiama print_agents_section quando not quiet."""
    mock_conn = MagicMock()
    mock_connect_db.return_value = mock_conn
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.return_value = {'total': 10, 'successes': 9, 'failures': 1, 'active': 1}
    mock_cursor.fetchall.side_effect = [
        [], [],
        [{'agent_name': 'test-agent', 'total': 5, 'successes': 4, 'failures': 1, 'avg_duration': 1000}],
        [], []
    ]

    with patch('scripts.memory.retro.cli.print_agents_section') as mock_print:
        generate_retro(days=7, save_to_file=False, quiet=False, output_dir=None)
        mock_print.assert_called_once()


@patch('scripts.memory.retro.cli.connect_db')
def test_generate_retro_prints_suggestions_when_not_quiet(mock_connect_db):
    """_print_and_save_suggestions chiama print_suggestions_section quando not quiet."""
    mock_conn = MagicMock()
    mock_connect_db.return_value = mock_conn
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.return_value = {'total': 10, 'successes': 8, 'failures': 2, 'active': 1}
    mock_cursor.fetchall.side_effect = [[], [], [], [], []]

    with patch('scripts.memory.retro.cli.suggest_new_lessons') as mock_suggest, \
         patch('scripts.memory.retro.cli.print_suggestions_section') as mock_print:
        mock_suggest.return_value = [('pattern', 3, 'Test pattern')]

        generate_retro(days=7, save_to_file=False, quiet=False, output_dir=None)
        mock_print.assert_called_once()
