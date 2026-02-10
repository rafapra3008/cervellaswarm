"""
Test suite for auto_detect command and helpers module.

Tests:
- auto_detect.py: cmd_auto_detect, _print_patterns_rich, _print_patterns_plain
- helpers.py: print_rich_or_plain, plain_print, get_console, rich_available
"""

from unittest.mock import patch, MagicMock, call
import pytest

from scripts.memory.analytics.commands.auto_detect import (
    cmd_auto_detect,
    _print_patterns_rich,
    _print_patterns_plain
)
from scripts.memory.analytics.helpers import (
    print_rich_or_plain,
    plain_print,
    get_console,
    rich_available
)


# ============================================================================
# TEST: auto_detect.py - cmd_auto_detect
# ============================================================================

class TestCmdAutoDetect:
    """Test cmd_auto_detect con tutti i branch."""

    @patch('scripts.memory.analytics.commands.auto_detect.PATTERN_DETECTOR_AVAILABLE', False)
    def test_pattern_detector_not_available(self, capsys):
        """Branch 1: pattern_detector non disponibile."""
        cmd_auto_detect(days=7)

        captured = capsys.readouterr()
        assert "pattern_detector.py non disponibile!" in captured.out
        assert "Suggerimento:" in captured.out

    @patch('scripts.memory.analytics.commands.auto_detect.PATTERN_DETECTOR_AVAILABLE', True)
    @patch('scripts.memory.analytics.commands.auto_detect.fetch_recent_errors')
    def test_no_errors_found(self, mock_fetch, capsys):
        """Branch 2: Nessun errore trovato."""
        mock_fetch.return_value = []

        cmd_auto_detect(days=7)

        captured = capsys.readouterr()
        assert "Nessun errore trovato! Sistema stabile." in captured.out
        mock_fetch.assert_called_once_with(days=7)

    @patch('scripts.memory.analytics.commands.auto_detect.PATTERN_DETECTOR_AVAILABLE', True)
    @patch('scripts.memory.analytics.commands.auto_detect.fetch_recent_errors')
    @patch('scripts.memory.analytics.commands.auto_detect.detect_error_patterns')
    def test_errors_found_no_patterns(self, mock_detect, mock_fetch, capsys):
        """Branch 3: Errori trovati ma nessun pattern."""
        mock_fetch.return_value = [
            {'error_message': 'Error 1'},
            {'error_message': 'Error 2'}
        ]
        mock_detect.return_value = []

        cmd_auto_detect(days=7)

        captured = capsys.readouterr()
        assert "Trovati" in captured.out and "2" in captured.out
        assert "Nessun pattern ricorrente rilevato" in captured.out
        mock_detect.assert_called_once()

    @patch('scripts.memory.analytics.commands.auto_detect.PATTERN_DETECTOR_AVAILABLE', True)
    @patch('scripts.memory.analytics.commands.auto_detect.fetch_recent_errors')
    @patch('scripts.memory.analytics.commands.auto_detect.detect_error_patterns')
    @patch('scripts.memory.analytics.commands.auto_detect.save_patterns_to_db')
    @patch('scripts.memory.analytics.commands.auto_detect.HAS_RICH', False)
    @patch('scripts.memory.analytics.commands.auto_detect._print_patterns_plain')
    def test_patterns_found_plain_output(self, mock_print_plain, mock_save, mock_detect, mock_fetch, capsys):
        """Branch 4: Pattern trovati, output plain."""
        errors = [
            {'error_message': 'Error 1'},
            {'error_message': 'Error 2'},
            {'error_message': 'Error 3'}
        ]
        patterns = [
            {
                'pattern_name': 'DB Connection Timeout',
                'severity_level': 'HIGH',
                'occurrence_count': 5
            }
        ]

        mock_fetch.return_value = errors
        mock_detect.return_value = patterns
        mock_save.return_value = (1, 0)  # 1 nuovo, 0 aggiornati

        cmd_auto_detect(days=7)

        captured = capsys.readouterr()
        assert "Trovati" in captured.out and "3" in captured.out
        assert "Rilevati" in captured.out and "1" in captured.out
        assert "Salvataggio pattern nel database..." in captured.out
        assert "Nuovi: 1" in captured.out and "Aggiornati: 0" in captured.out

        mock_save.assert_called_once_with(patterns)
        mock_print_plain.assert_called_once_with(patterns)

    @patch('scripts.memory.analytics.commands.auto_detect.PATTERN_DETECTOR_AVAILABLE', True)
    @patch('scripts.memory.analytics.commands.auto_detect.fetch_recent_errors')
    @patch('scripts.memory.analytics.commands.auto_detect.detect_error_patterns')
    @patch('scripts.memory.analytics.commands.auto_detect.save_patterns_to_db')
    @patch('scripts.memory.analytics.commands.auto_detect.HAS_RICH', True)
    @patch('scripts.memory.analytics.commands.auto_detect._print_patterns_rich')
    def test_patterns_found_rich_output(self, mock_print_rich, mock_save, mock_detect, mock_fetch, capsys):
        """Branch 5: Pattern trovati, output Rich."""
        errors = [
            {'error_message': 'Error 1'},
            {'error_message': 'Error 2'}
        ]
        patterns = [
            {
                'pattern_name': 'Network Timeout',
                'severity_level': 'CRITICAL',
                'occurrence_count': 10
            },
            {
                'pattern_name': 'File Not Found',
                'severity_level': 'MEDIUM',
                'occurrence_count': 3
            }
        ]

        mock_fetch.return_value = errors
        mock_detect.return_value = patterns
        mock_save.return_value = (0, 2)  # 0 nuovi, 2 aggiornati

        cmd_auto_detect(days=14)

        captured = capsys.readouterr()
        assert "Rilevati" in captured.out and "2" in captured.out
        assert "Nuovi: 0" in captured.out and "Aggiornati: 2" in captured.out

        mock_save.assert_called_once_with(patterns)
        mock_print_rich.assert_called_once_with(patterns)


# ============================================================================
# TEST: auto_detect.py - _print_patterns_rich
# ============================================================================

class TestPrintPatternsRich:
    """Test _print_patterns_rich."""

    @patch('scripts.memory.analytics.commands.auto_detect.console')
    @patch('scripts.memory.analytics.commands.auto_detect.Table')
    def test_rich_output_patterns(self, mock_table_class, mock_console):
        """Test output Rich con pattern multipli e troncamento."""
        mock_table = MagicMock()
        mock_table_class.return_value = mock_table

        patterns = [
            {'pattern_name': 'DB Timeout', 'severity_level': 'CRITICAL', 'occurrence_count': 15},
            {'pattern_name': 'API Rate Limit', 'severity_level': 'HIGH', 'occurrence_count': 8},
            {'pattern_name': 'Very long pattern name that exceeds sixty characters limit for display',
             'severity_level': 'MEDIUM', 'occurrence_count': 5}
        ]

        _print_patterns_rich(patterns)

        # Verifica Table creata con 4 colonne
        mock_table_class.assert_called_once()
        assert mock_table.add_column.call_count == 4

        # Verifica 3 righe aggiunte
        assert mock_table.add_row.call_count == 3

        # Verifica colori severity
        calls = mock_table.add_row.call_args_list
        assert '[red]CRITICAL[/red]' in calls[0][0][1]
        assert '[yellow]HIGH[/yellow]' in calls[1][0][1]

        # Verifica troncamento pattern lungo a 60 char
        assert len(calls[2][0][2]) == 60

        # Verifica console.print chiamato 2 volte
        assert mock_console.print.call_count == 2


# ============================================================================
# TEST: auto_detect.py - _print_patterns_plain
# ============================================================================

class TestPrintPatternsPlain:
    """Test _print_patterns_plain."""

    def test_plain_output_patterns(self, capsys):
        """Test output plain con pattern multipli e troncamento."""
        patterns = [
            {
                'pattern_name': 'DB Connection Timeout',
                'severity_level': 'CRITICAL',
                'occurrence_count': 15
            },
            {
                'pattern_name': 'Very long pattern name that definitely exceeds sixty characters limit',
                'severity_level': 'LOW',
                'occurrence_count': 2
            }
        ]

        _print_patterns_plain(patterns)

        captured = capsys.readouterr()
        assert "PATTERN RILEVATI" in captured.out
        assert "1. [CRITICAL] DB Connection Timeout" in captured.out
        assert "Occorrenze: 15" in captured.out
        # Secondo pattern troncato a 60 char
        assert "Very long pattern name that definitely exceeds sixty cha" in captured.out
        assert "Pattern detection completato!" in captured.out


# ============================================================================
# TEST: helpers.py
# ============================================================================

class TestHelpers:
    """Test helpers module."""

    def test_print_rich_or_plain_both_modes(self):
        """Test print_rich_or_plain con HAS_RICH True/False."""
        rich_fn = MagicMock()
        plain_fn = MagicMock()

        # Rich available
        with patch('scripts.memory.analytics.helpers.HAS_RICH', True):
            print_rich_or_plain(rich_fn, plain_fn, "arg1", key="value")
        rich_fn.assert_called_once_with("arg1", key="value")
        plain_fn.assert_not_called()

        # Rich not available
        rich_fn.reset_mock()
        plain_fn.reset_mock()
        with patch('scripts.memory.analytics.helpers.HAS_RICH', False):
            print_rich_or_plain(rich_fn, plain_fn, "arg1", key="value")
        plain_fn.assert_called_once_with("arg1", key="value")
        rich_fn.assert_not_called()

    def test_helpers_output_functions(self, capsys):
        """Test plain_print, get_console, rich_available."""
        # plain_print
        plain_print("Test message")
        captured = capsys.readouterr()
        assert captured.out == "Test message\n"

        # get_console (Rich installed)
        assert get_console() is not None

        # rich_available (Rich installed)
        assert rich_available() is True
