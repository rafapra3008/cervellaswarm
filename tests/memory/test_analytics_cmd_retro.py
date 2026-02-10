"""
Test per scripts.memory.analytics.commands.retro.

Coverage focus: cmd_retro function con entrambi i branch.
"""

import pytest
from unittest.mock import patch


class TestCmdRetro:
    """Test cmd_retro."""

    @patch('scripts.memory.analytics.commands.retro.HAS_RICH', False)
    def test_cmd_retro_no_rich(self, capsys):
        """cmd_retro stampa errore se Rich non disponibile."""
        from scripts.memory.analytics.commands.retro import cmd_retro
        cmd_retro()
        captured = capsys.readouterr()
        assert "Rich" in captured.out or "rich" in captured.out.lower()

    @patch('scripts.memory.analytics.commands.retro.HAS_RICH', True)
    @patch('scripts.memory.analytics.commands.retro.RETRO_AVAILABLE', False)
    def test_cmd_retro_no_retro_module(self, capsys):
        """cmd_retro stampa errore se modulo retro non disponibile."""
        from scripts.memory.analytics.commands.retro import cmd_retro
        cmd_retro()
        captured = capsys.readouterr()
        assert "retro" in captured.out.lower()

    @patch('scripts.memory.analytics.commands.retro.HAS_RICH', True)
    @patch('scripts.memory.analytics.commands.retro.RETRO_AVAILABLE', True)
    @patch('scripts.memory.analytics.commands.retro.generate_retro')
    def test_cmd_retro_success(self, mock_gen):
        """cmd_retro chiama generate_retro quando tutto disponibile."""
        from scripts.memory.analytics.commands.retro import cmd_retro
        cmd_retro()
        mock_gen.assert_called_once_with(days=7, save_to_file=False, quiet=False)
