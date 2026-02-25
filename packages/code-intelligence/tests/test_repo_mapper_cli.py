"""Tests for cervellaswarm_code_intelligence/cli/map_cmd.py - Core

Covers CLI argument parsing, output modes, verbose and stats flags.
Error handling and edge cases in test_repo_mapper_cli_errors.py.
"""

import sys
import logging
import pytest
from pathlib import Path
from unittest.mock import Mock, patch, mock_open

from cervellaswarm_code_intelligence.cli.map_cmd import main


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def mock_repo_mapper():
    """Mock RepoMapper class with all methods."""
    with patch('cervellaswarm_code_intelligence.cli.map_cmd.RepoMapper') as MockClass:
        mock_instance = Mock()
        mock_instance.build_map.return_value = "# Repository Map\n\n## Files\n- file1.py\n"
        mock_instance.get_stats.return_value = {
            'symbols': 42,
            'graph_nodes': 38,
            'graph_edges': 15,
            'graph_isolated': 4
        }
        mock_instance._estimate_tokens.return_value = 1500
        MockClass.return_value = mock_instance
        yield MockClass, mock_instance


# ============================================================================
# BASIC CLI TESTS
# ============================================================================

def test_main_no_args_defaults(mock_repo_mapper, capsys):
    """main() with no args uses defaults: repo_path='.', budget=2000."""
    MockClass, mock_instance = mock_repo_mapper

    with patch('sys.argv', ['repo_mapper_cli.py']):
        result = main()

    assert result == 0
    MockClass.assert_called_once_with('.')
    mock_instance.build_map.assert_called_once_with(
        token_budget=2000,
        filter_pattern=None
    )
    output = capsys.readouterr().out
    assert "Generating repository map for: ." in output
    assert "Token budget: 2000" in output


def test_main_custom_repo_path(mock_repo_mapper, capsys):
    """main() with --repo-path /some/path."""
    MockClass, mock_instance = mock_repo_mapper

    with patch('sys.argv', ['repo_mapper_cli.py', '--repo-path', '/some/path']):
        result = main()

    assert result == 0
    MockClass.assert_called_once_with('/some/path')
    output = capsys.readouterr().out
    assert "Generating repository map for: /some/path" in output


def test_main_custom_budget(mock_repo_mapper, capsys):
    """main() with --budget 3000."""
    MockClass, mock_instance = mock_repo_mapper

    with patch('sys.argv', ['repo_mapper_cli.py', '--budget', '3000']):
        result = main()

    assert result == 0
    mock_instance.build_map.assert_called_once_with(
        token_budget=3000,
        filter_pattern=None
    )
    output = capsys.readouterr().out
    assert "Token budget: 3000" in output


def test_main_with_filter(mock_repo_mapper, capsys):
    """main() with --filter '**/*.py'."""
    MockClass, mock_instance = mock_repo_mapper

    with patch('sys.argv', ['repo_mapper_cli.py', '--filter', '**/*.py']):
        result = main()

    assert result == 0
    mock_instance.build_map.assert_called_once_with(
        token_budget=2000,
        filter_pattern='**/*.py'
    )
    output = capsys.readouterr().out
    assert "Filter pattern: **/*.py" in output


def test_main_combined_args(mock_repo_mapper):
    """main() with multiple args combined."""
    MockClass, mock_instance = mock_repo_mapper

    with patch('sys.argv', [
        'repo_mapper_cli.py',
        '--repo-path', '/custom/path',
        '--budget', '5000',
        '--filter', '**/*.ts'
    ]):
        result = main()

    assert result == 0
    MockClass.assert_called_once_with('/custom/path')
    mock_instance.build_map.assert_called_once_with(
        token_budget=5000,
        filter_pattern='**/*.ts'
    )


# ============================================================================
# OUTPUT MODES
# ============================================================================

def test_main_stdout_output(mock_repo_mapper, capsys):
    """main() without --output prints to stdout."""
    MockClass, mock_instance = mock_repo_mapper

    with patch('sys.argv', ['repo_mapper_cli.py']):
        result = main()

    assert result == 0
    output = capsys.readouterr().out
    assert "# Repository Map" in output


def test_main_file_output(mock_repo_mapper, capsys):
    """main() with --output writes to file."""
    MockClass, mock_instance = mock_repo_mapper

    m_open = mock_open()
    with patch('sys.argv', ['repo_mapper_cli.py', '--output', '/tmp/map.md']), \
         patch('builtins.open', m_open):
        result = main()

    assert result == 0
    m_open.assert_called_once_with('/tmp/map.md', 'w')
    handle = m_open()
    handle.write.assert_called_once_with("# Repository Map\n\n## Files\n- file1.py\n")
    output = capsys.readouterr().out
    assert "Map saved to: /tmp/map.md" in output


def test_main_no_filter_no_filter_message(mock_repo_mapper, capsys):
    """main() without --filter doesn't print filter message."""
    MockClass, mock_instance = mock_repo_mapper

    with patch('sys.argv', ['repo_mapper_cli.py']):
        result = main()

    assert result == 0
    output = capsys.readouterr().out
    assert "Filter pattern:" not in output


# ============================================================================
# VERBOSE MODE
# ============================================================================

def test_main_verbose_flag(mock_repo_mapper):
    """main() with --verbose sets DEBUG logging."""
    MockClass, mock_instance = mock_repo_mapper

    with patch('sys.argv', ['repo_mapper_cli.py', '--verbose']), \
         patch('logging.basicConfig') as mock_logging:
        result = main()

    assert result == 0
    mock_logging.assert_called_once()
    call_kwargs = mock_logging.call_args[1]
    assert call_kwargs['level'] == logging.DEBUG


def test_main_no_verbose_flag(mock_repo_mapper):
    """main() without --verbose sets INFO logging."""
    MockClass, mock_instance = mock_repo_mapper

    with patch('sys.argv', ['repo_mapper_cli.py']), \
         patch('logging.basicConfig') as mock_logging:
        result = main()

    assert result == 0
    mock_logging.assert_called_once()
    call_kwargs = mock_logging.call_args[1]
    assert call_kwargs['level'] == logging.INFO


# ============================================================================
# STATS MODE
# ============================================================================

def test_main_stats_flag(mock_repo_mapper, capsys):
    """main() with --stats displays statistics."""
    MockClass, mock_instance = mock_repo_mapper

    with patch('sys.argv', ['repo_mapper_cli.py', '--stats']):
        result = main()

    assert result == 0
    mock_instance.get_stats.assert_called_once()
    mock_instance._estimate_tokens.assert_called_once()

    output = capsys.readouterr().out
    assert "Statistics:" in output
    assert "Total symbols: 42" in output
    assert "Graph nodes: 38" in output
    assert "Graph edges: 15" in output
    assert "Isolated symbols: 4" in output
    assert "Estimated tokens: 1500 / 2000" in output


def test_main_stats_with_custom_budget(mock_repo_mapper, capsys):
    """main() with --stats and --budget shows correct budget."""
    MockClass, mock_instance = mock_repo_mapper

    with patch('sys.argv', ['repo_mapper_cli.py', '--stats', '--budget', '3000']):
        result = main()

    assert result == 0
    output = capsys.readouterr().out
    assert "Estimated tokens: 1500 / 3000" in output


def test_main_no_stats_flag(mock_repo_mapper, capsys):
    """main() without --stats doesn't call get_stats."""
    MockClass, mock_instance = mock_repo_mapper

    with patch('sys.argv', ['repo_mapper_cli.py']):
        result = main()

    assert result == 0
    mock_instance.get_stats.assert_not_called()
    mock_instance._estimate_tokens.assert_not_called()
    output = capsys.readouterr().out
    assert "Statistics:" not in output
