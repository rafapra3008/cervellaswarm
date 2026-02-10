"""
Test per scripts.swarm.dashboard.cli.

Coverage focus: main() branches, watch mode, error handlers.
"""

import pytest
from unittest.mock import patch


class TestClearScreen:
    """Test clear_screen."""

    def test_clear_screen_prints_escape(self, capsys):
        from scripts.swarm.dashboard.cli import clear_screen
        clear_screen()
        captured = capsys.readouterr()
        assert '\033[2J' in captured.out


class TestMainSingleShot:
    """Test main() in single-shot mode."""

    @patch('scripts.swarm.dashboard.cli.list_tasks')
    @patch('scripts.swarm.dashboard.cli.render_dashboard', return_value="dashboard output")
    def test_main_single_shot_default(self, mock_render, mock_list, capsys):
        mock_list.return_value = []
        from scripts.swarm.dashboard.cli import main
        with patch('sys.argv', ['cli']):
            main()
        mock_list.assert_called_once()
        mock_render.assert_called_once_with([])

    @patch('scripts.swarm.dashboard.cli.list_tasks')
    @patch('scripts.swarm.dashboard.cli.render_json', return_value='{"tasks": []}')
    def test_main_single_shot_json(self, mock_json, mock_list, capsys):
        mock_list.return_value = []
        from scripts.swarm.dashboard.cli import main
        with patch('sys.argv', ['cli', '--json']):
            main()
        mock_json.assert_called_once_with([])


class TestMainWatchMode:
    """Test main() watch mode."""

    @patch('scripts.swarm.dashboard.cli.list_tasks')
    @patch('scripts.swarm.dashboard.cli.render_dashboard', return_value="dash")
    @patch('scripts.swarm.dashboard.cli.clear_screen')
    @patch('scripts.swarm.dashboard.cli.time')
    def test_main_watch_mode(self, mock_time, mock_clear, mock_render, mock_list, capsys):
        mock_list.return_value = []
        # sleep raises KeyboardInterrupt on second call to break loop
        mock_time.sleep.side_effect = [None, KeyboardInterrupt]
        from scripts.swarm.dashboard.cli import main
        with patch('sys.argv', ['cli', '--watch']):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 0

    @patch('scripts.swarm.dashboard.cli.list_tasks')
    @patch('scripts.swarm.dashboard.cli.render_json', return_value='{}')
    @patch('scripts.swarm.dashboard.cli.clear_screen')
    @patch('scripts.swarm.dashboard.cli.time')
    def test_main_watch_json_mode(self, mock_time, mock_clear, mock_json, mock_list, capsys):
        mock_list.return_value = []
        mock_time.sleep.side_effect = KeyboardInterrupt
        from scripts.swarm.dashboard.cli import main
        with patch('sys.argv', ['cli', '--watch', '--json']):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 0


class TestMainErrorHandlers:
    """Test main() error handling."""

    @patch('scripts.swarm.dashboard.cli.list_tasks')
    def test_main_keyboard_interrupt(self, mock_list, capsys):
        mock_list.side_effect = KeyboardInterrupt
        from scripts.swarm.dashboard.cli import main
        with patch('sys.argv', ['cli']):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 0

    @patch('scripts.swarm.dashboard.cli.list_tasks')
    def test_main_generic_exception(self, mock_list, capsys):
        mock_list.side_effect = RuntimeError("DB connection failed")
        from scripts.swarm.dashboard.cli import main
        with patch('sys.argv', ['cli']):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1
