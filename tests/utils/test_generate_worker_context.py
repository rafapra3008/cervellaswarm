#!/usr/bin/env python3
"""Tests for generate_worker_context.py"""

import sys
from io import StringIO
from unittest.mock import Mock, patch

import pytest

from scripts.utils.generate_worker_context import generate_context, main


# ============================================================================
# GENERATE_CONTEXT TESTS
# ============================================================================

@patch('scripts.utils.generate_worker_context.RepoMapper')
def test_generate_context_with_header(mock_mapper_class):
    """Test generate_context includes header by default."""
    mock_mapper = Mock()
    mock_mapper.build_map.return_value = "# REPO MAP\n\n## file.py\ndef func()"
    mock_mapper_class.return_value = mock_mapper

    result = generate_context(repo_path="/fake/path", token_budget=1500)

    assert "CONTESTO CODEBASE" in result
    assert "auto-generato da repo_mapper" in result
    assert "# REPO MAP" in result
    assert "PageRank" in result
    mock_mapper_class.assert_called_once_with("/fake/path")
    mock_mapper.build_map.assert_called_once_with(
        token_budget=1500,
        filter_pattern=None
    )


@patch('scripts.utils.generate_worker_context.RepoMapper')
def test_generate_context_without_header(mock_mapper_class):
    """Test generate_context without header when include_header=False."""
    mock_mapper = Mock()
    mock_mapper.build_map.return_value = "# REPO MAP\n\n## file.py\ndef func()"
    mock_mapper_class.return_value = mock_mapper

    result = generate_context(
        repo_path="/fake/path",
        token_budget=1500,
        include_header=False
    )

    assert "CONTESTO CODEBASE" not in result
    assert "auto-generato da repo_mapper" not in result
    assert result == "# REPO MAP\n\n## file.py\ndef func()"
    mock_mapper_class.assert_called_once_with("/fake/path")


@patch('scripts.utils.generate_worker_context.RepoMapper')
def test_generate_context_custom_token_budget(mock_mapper_class):
    """Test generate_context passes custom token_budget to build_map."""
    mock_mapper = Mock()
    mock_mapper.build_map.return_value = "map content"
    mock_mapper_class.return_value = mock_mapper

    result = generate_context(repo_path=".", token_budget=3000)

    assert "map content" in result
    mock_mapper.build_map.assert_called_once_with(
        token_budget=3000,
        filter_pattern=None
    )


@patch('scripts.utils.generate_worker_context.RepoMapper')
def test_generate_context_custom_filter_pattern(mock_mapper_class):
    """Test generate_context passes filter_pattern to build_map."""
    mock_mapper = Mock()
    mock_mapper.build_map.return_value = "filtered map"
    mock_mapper_class.return_value = mock_mapper

    result = generate_context(
        repo_path=".",
        token_budget=1500,
        filter_pattern="*.py"
    )

    assert "filtered map" in result
    mock_mapper.build_map.assert_called_once_with(
        token_budget=1500,
        filter_pattern="*.py"
    )


@patch('scripts.utils.generate_worker_context.RepoMapper')
def test_generate_context_all_params(mock_mapper_class):
    """Test generate_context with all parameters customized."""
    mock_mapper = Mock()
    mock_mapper.build_map.return_value = "custom map"
    mock_mapper_class.return_value = mock_mapper

    result = generate_context(
        repo_path="/custom/path",
        token_budget=2500,
        filter_pattern="src/**/*.py",
        include_header=False
    )

    assert result == "custom map"
    mock_mapper_class.assert_called_once_with("/custom/path")
    mock_mapper.build_map.assert_called_once_with(
        token_budget=2500,
        filter_pattern="src/**/*.py"
    )


@patch('scripts.utils.generate_worker_context.RepoMapper')
def test_generate_context_file_not_found(mock_mapper_class):
    """Test generate_context handles FileNotFoundError."""
    mock_mapper_class.side_effect = FileNotFoundError("No such directory")

    result = generate_context(repo_path="/nonexistent")

    assert result.startswith("[WARN]")
    assert "Repository path not found" in result
    assert "/nonexistent" in result


@patch('scripts.utils.generate_worker_context.RepoMapper')
def test_generate_context_generic_exception(mock_mapper_class):
    """Test generate_context handles generic exceptions."""
    mock_mapper = Mock()
    mock_mapper.build_map.side_effect = ValueError("Invalid token budget")
    mock_mapper_class.return_value = mock_mapper

    result = generate_context(repo_path=".")

    assert result.startswith("[WARN]")
    assert "Failed to generate context" in result
    assert "Invalid token budget" in result


@patch('scripts.utils.generate_worker_context.RepoMapper')
def test_generate_context_strips_whitespace(mock_mapper_class):
    """Test generate_context strips leading/trailing whitespace."""
    mock_mapper = Mock()
    mock_mapper.build_map.return_value = "  map content  "
    mock_mapper_class.return_value = mock_mapper

    result = generate_context(repo_path=".", include_header=False)

    assert result == "map content"
    assert not result.startswith(" ")
    assert not result.endswith(" ")


# ============================================================================
# MAIN CLI TESTS
# ============================================================================

@patch('scripts.utils.generate_worker_context.RepoMapper')
def test_main_successful_run(mock_mapper_class, capsys, monkeypatch):
    """Test main() prints to stdout and exits 0 on success."""
    mock_mapper = Mock()
    mock_mapper.build_map.return_value = "# SUCCESS MAP"
    mock_mapper_class.return_value = mock_mapper

    monkeypatch.setattr(sys, 'argv', ['generate_worker_context.py'])

    with pytest.raises(SystemExit) as exc_info:
        main()

    assert exc_info.value.code == 0
    captured = capsys.readouterr()
    assert "CONTESTO CODEBASE" in captured.out
    assert "# SUCCESS MAP" in captured.out
    assert captured.err == ""


@patch('scripts.utils.generate_worker_context.RepoMapper')
def test_main_with_custom_repo_path(mock_mapper_class, capsys, monkeypatch):
    """Test main() with --repo-path argument."""
    mock_mapper = Mock()
    mock_mapper.build_map.return_value = "custom repo map"
    mock_mapper_class.return_value = mock_mapper

    monkeypatch.setattr(
        sys,
        'argv',
        ['generate_worker_context.py', '--repo-path', '/custom/path']
    )

    with pytest.raises(SystemExit) as exc_info:
        main()

    assert exc_info.value.code == 0
    mock_mapper_class.assert_called_once_with('/custom/path')


@patch('scripts.utils.generate_worker_context.RepoMapper')
def test_main_with_custom_budget(mock_mapper_class, capsys, monkeypatch):
    """Test main() with --budget argument."""
    mock_mapper = Mock()
    mock_mapper.build_map.return_value = "map"
    mock_mapper_class.return_value = mock_mapper

    monkeypatch.setattr(
        sys,
        'argv',
        ['generate_worker_context.py', '--budget', '3000']
    )

    with pytest.raises(SystemExit) as exc_info:
        main()

    assert exc_info.value.code == 0
    mock_mapper.build_map.assert_called_once_with(
        token_budget=3000,
        filter_pattern=None
    )


@patch('scripts.utils.generate_worker_context.RepoMapper')
def test_main_with_filter_pattern(mock_mapper_class, capsys, monkeypatch):
    """Test main() with --filter argument."""
    mock_mapper = Mock()
    mock_mapper.build_map.return_value = "filtered"
    mock_mapper_class.return_value = mock_mapper

    monkeypatch.setattr(
        sys,
        'argv',
        ['generate_worker_context.py', '--filter', '*.py']
    )

    with pytest.raises(SystemExit) as exc_info:
        main()

    assert exc_info.value.code == 0
    mock_mapper.build_map.assert_called_once_with(
        token_budget=1500,
        filter_pattern='*.py'
    )


@patch('scripts.utils.generate_worker_context.RepoMapper')
def test_main_with_no_header(mock_mapper_class, capsys, monkeypatch):
    """Test main() with --no-header flag."""
    mock_mapper = Mock()
    mock_mapper.build_map.return_value = "just the map"
    mock_mapper_class.return_value = mock_mapper

    monkeypatch.setattr(
        sys,
        'argv',
        ['generate_worker_context.py', '--no-header']
    )

    with pytest.raises(SystemExit) as exc_info:
        main()

    assert exc_info.value.code == 0
    captured = capsys.readouterr()
    assert "CONTESTO CODEBASE" not in captured.out
    assert "just the map" in captured.out


@patch('scripts.utils.generate_worker_context.RepoMapper')
def test_main_warning_prints_to_stderr(mock_mapper_class, capsys, monkeypatch):
    """Test main() prints warnings to stderr and exits 1."""
    mock_mapper_class.side_effect = FileNotFoundError("No such directory")

    monkeypatch.setattr(
        sys,
        'argv',
        ['generate_worker_context.py', '--repo-path', '/nonexistent']
    )

    with pytest.raises(SystemExit) as exc_info:
        main()

    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "[WARN]" in captured.err
    assert "Repository path not found" in captured.err
    assert "/nonexistent" in captured.err


@patch('scripts.utils.generate_worker_context.RepoMapper')
def test_main_quiet_flag_suppresses_stderr(mock_mapper_class, capsys, monkeypatch):
    """Test main() with --quiet suppresses stderr output."""
    mock_mapper_class.side_effect = FileNotFoundError("No such directory")

    monkeypatch.setattr(
        sys,
        'argv',
        ['generate_worker_context.py', '--repo-path', '/bad', '--quiet']
    )

    with pytest.raises(SystemExit) as exc_info:
        main()

    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""


@patch('scripts.utils.generate_worker_context.RepoMapper')
def test_main_all_options_combined(mock_mapper_class, capsys, monkeypatch):
    """Test main() with multiple CLI options."""
    mock_mapper = Mock()
    mock_mapper.build_map.return_value = "complete map"
    mock_mapper_class.return_value = mock_mapper

    monkeypatch.setattr(
        sys,
        'argv',
        [
            'generate_worker_context.py',
            '--repo-path', '/project',
            '--budget', '2000',
            '--filter', 'src/**/*.py',
            '--no-header'
        ]
    )

    with pytest.raises(SystemExit) as exc_info:
        main()

    assert exc_info.value.code == 0
    mock_mapper_class.assert_called_once_with('/project')
    mock_mapper.build_map.assert_called_once_with(
        token_budget=2000,
        filter_pattern='src/**/*.py'
    )
    captured = capsys.readouterr()
    assert "CONTESTO CODEBASE" not in captured.out
    assert "complete map" in captured.out
