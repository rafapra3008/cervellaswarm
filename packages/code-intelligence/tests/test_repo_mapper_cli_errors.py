"""Tests for cervellaswarm_code_intelligence/cli/map_cmd.py - Errors & Edge Cases

Error handling, edge cases, and integration tests.
Core CLI tests in test_repo_mapper_cli.py.
"""

import sys
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
# ERROR HANDLING
# ============================================================================

def test_main_file_not_found_error(capsys):
    """main() with FileNotFoundError returns 1."""
    with patch('cervellaswarm_code_intelligence.cli.map_cmd.RepoMapper') as MockClass:
        MockClass.side_effect = FileNotFoundError("Repository not found: /invalid/path")

        with patch('sys.argv', ['repo_mapper_cli.py', '--repo-path', '/invalid/path']):
            result = main()

    assert result == 1
    output = capsys.readouterr().out
    assert "Repository not found: /invalid/path" in output


def test_main_generic_exception(capsys):
    """main() with generic Exception returns 1."""
    with patch('cervellaswarm_code_intelligence.cli.map_cmd.RepoMapper') as MockClass:
        mock_instance = Mock()
        mock_instance.build_map.side_effect = RuntimeError("Something went wrong")
        MockClass.return_value = mock_instance

        with patch('sys.argv', ['repo_mapper_cli.py']):
            result = main()

    assert result == 1
    output = capsys.readouterr().out
    assert "Unexpected error: Something went wrong" in output


def test_main_exception_verbose_traceback(capsys):
    """main() with Exception and --verbose prints traceback."""
    with patch('cervellaswarm_code_intelligence.cli.map_cmd.RepoMapper') as MockClass:
        mock_instance = Mock()
        mock_instance.build_map.side_effect = ValueError("Bad value")
        MockClass.return_value = mock_instance

        with patch('sys.argv', ['repo_mapper_cli.py', '--verbose']), \
             patch('traceback.print_exc') as mock_traceback:
            result = main()

    assert result == 1
    output = capsys.readouterr().out
    assert "Unexpected error: Bad value" in output
    mock_traceback.assert_called_once()


def test_main_exception_no_verbose_no_traceback(capsys):
    """main() with Exception and no --verbose doesn't print traceback."""
    with patch('cervellaswarm_code_intelligence.cli.map_cmd.RepoMapper') as MockClass:
        mock_instance = Mock()
        mock_instance.build_map.side_effect = ValueError("Bad value")
        MockClass.return_value = mock_instance

        with patch('sys.argv', ['repo_mapper_cli.py']), \
             patch('traceback.print_exc') as mock_traceback:
            result = main()

    assert result == 1
    mock_traceback.assert_not_called()


def test_main_build_map_exception(capsys):
    """main() with build_map() raising exception."""
    with patch('cervellaswarm_code_intelligence.cli.map_cmd.RepoMapper') as MockClass:
        mock_instance = Mock()
        mock_instance.build_map.side_effect = Exception("Build map failed")
        MockClass.return_value = mock_instance

        with patch('sys.argv', ['repo_mapper_cli.py']):
            result = main()

    assert result == 1
    output = capsys.readouterr().out
    assert "Unexpected error: Build map failed" in output


def test_main_output_write_exception(mock_repo_mapper, capsys):
    """main() with file write error."""
    MockClass, mock_instance = mock_repo_mapper

    with patch('sys.argv', ['repo_mapper_cli.py', '--output', '/readonly/file.md']), \
         patch('builtins.open', side_effect=PermissionError("Permission denied")):
        result = main()

    assert result == 1
    output = capsys.readouterr().out
    assert "Unexpected error: Permission denied" in output


# ============================================================================
# EDGE CASES
# ============================================================================

def test_main_empty_map_output(capsys):
    """main() with empty map from build_map."""
    with patch('cervellaswarm_code_intelligence.cli.map_cmd.RepoMapper') as MockClass:
        mock_instance = Mock()
        mock_instance.build_map.return_value = ""
        MockClass.return_value = mock_instance

        with patch('sys.argv', ['repo_mapper_cli.py']):
            result = main()

    assert result == 0


def test_main_stats_zero_values(capsys):
    """main() with --stats when all stats are zero."""
    with patch('cervellaswarm_code_intelligence.cli.map_cmd.RepoMapper') as MockClass:
        mock_instance = Mock()
        mock_instance.build_map.return_value = "# Empty"
        mock_instance.get_stats.return_value = {
            'symbols': 0,
            'graph_nodes': 0,
            'graph_edges': 0,
            'graph_isolated': 0
        }
        mock_instance._estimate_tokens.return_value = 0
        MockClass.return_value = mock_instance

        with patch('sys.argv', ['repo_mapper_cli.py', '--stats']):
            result = main()

    assert result == 0
    output = capsys.readouterr().out
    assert "Total symbols: 0" in output
    assert "Estimated tokens: 0 / 2000" in output


def test_main_filter_no_match(mock_repo_mapper):
    """main() with --filter that matches nothing."""
    MockClass, mock_instance = mock_repo_mapper
    mock_instance.build_map.return_value = "# No files matched\n"

    with patch('sys.argv', ['repo_mapper_cli.py', '--filter', '**/*.nonexistent']):
        result = main()

    assert result == 0
    mock_instance.build_map.assert_called_once_with(
        token_budget=2000,
        filter_pattern='**/*.nonexistent'
    )


def test_main_budget_zero(mock_repo_mapper, capsys):
    """main() with --budget 0."""
    MockClass, mock_instance = mock_repo_mapper

    with patch('sys.argv', ['repo_mapper_cli.py', '--budget', '0']):
        result = main()

    assert result == 0
    mock_instance.build_map.assert_called_once_with(
        token_budget=0,
        filter_pattern=None
    )
    output = capsys.readouterr().out
    assert "Token budget: 0" in output


# ============================================================================
# INTEGRATION-STYLE TESTS
# ============================================================================

def test_main_all_flags_combined(capsys):
    """main() with all flags together."""
    with patch('cervellaswarm_code_intelligence.cli.map_cmd.RepoMapper') as MockClass:
        mock_instance = Mock()
        mock_instance.build_map.return_value = "# Full map\n"
        mock_instance.get_stats.return_value = {
            'symbols': 100,
            'graph_nodes': 95,
            'graph_edges': 50,
            'graph_isolated': 5
        }
        mock_instance._estimate_tokens.return_value = 2500
        MockClass.return_value = mock_instance

        m_open = mock_open()
        with patch('sys.argv', [
            'repo_mapper_cli.py',
            '--repo-path', '/project',
            '--budget', '3000',
            '--filter', '**/*.py',
            '--output', 'full.md',
            '--verbose',
            '--stats'
        ]), patch('builtins.open', m_open):
            result = main()

    assert result == 0
    MockClass.assert_called_once_with('/project')
    mock_instance.build_map.assert_called_once_with(
        token_budget=3000,
        filter_pattern='**/*.py'
    )
    m_open.assert_called_once_with('full.md', 'w')

    output = capsys.readouterr().out
    assert "Generating repository map for: /project" in output
    assert "Token budget: 3000" in output
    assert "Filter pattern: **/*.py" in output
    assert "Map saved to: full.md" in output
    assert "Statistics:" in output
    assert "Total symbols: 100" in output
    assert "Estimated tokens: 2500 / 3000" in output


def test_main_successful_run_prints_initial_messages(mock_repo_mapper, capsys):
    """main() prints initial messages before processing."""
    MockClass, mock_instance = mock_repo_mapper

    with patch('sys.argv', ['repo_mapper_cli.py', '--repo-path', '/myproject']):
        result = main()

    assert result == 0
    output = capsys.readouterr().out
    lines = output.split('\n')
    assert any("Generating repository map for: /myproject" in line for line in lines[:10])
    assert any("Token budget: 2000" in line for line in lines[:10])
