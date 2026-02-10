"""
Tests for scripts/utils/semantic_search_cli.py

Coverage target: 95%+ of main() function (lines 19-125)
Excludes: __main__ block (lines 128-129)
"""
import sys
from unittest.mock import Mock, patch, MagicMock
import pytest
from scripts.utils.semantic_search_cli import main


@pytest.fixture
def mock_stats():
    """Standard stats dict returned by search.get_stats()."""
    return {
        "total_symbols": 150,
        "unique_names": 80,
        "graph_nodes": 120,
        "graph_edges": 200,
    }


@pytest.fixture
def mock_search(mock_stats):
    """Mock SemanticSearch instance with all methods."""
    search = MagicMock()
    search.get_stats.return_value = mock_stats
    return search


# ==============================================================================
# USAGE / ARG VALIDATION
# ==============================================================================


def test_main_too_few_args_exits(capsys):
    """Test that main() exits with usage when < 3 args provided."""
    with patch.object(sys, "argv", ["semantic_search_cli.py"]):
        with pytest.raises(SystemExit) as exc_info:
            main()

    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "Usage:" in captured.out
    assert "Commands:" in captured.out
    assert "Example:" in captured.out


def test_main_two_args_exits(capsys):
    """Test that main() exits with usage when only 2 args provided."""
    with patch.object(sys, "argv", ["semantic_search_cli.py", "/repo"]):
        with pytest.raises(SystemExit) as exc_info:
            main()

    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "Usage:" in captured.out


# ==============================================================================
# FIND COMMAND (default)
# ==============================================================================


def test_main_find_symbol_found(mock_search, mock_stats, capsys):
    """Test find command with symbol found."""
    mock_search.find_symbol.return_value = ("src/auth.py", 42)

    with patch.object(sys, "argv", ["cli.py", "/repo", "login"]):
        with patch("scripts.utils.semantic_search_cli.SemanticSearch", return_value=mock_search):
            main()

    captured = capsys.readouterr()
    assert "Initializing semantic search for: /repo" in captured.out
    assert "Total symbols: 150" in captured.out
    assert "Unique names: 80" in captured.out
    assert "Graph nodes: 120" in captured.out
    assert "Graph edges: 200" in captured.out
    assert "Finding symbol: login" in captured.out
    assert "Found at: src/auth.py:42" in captured.out


def test_main_find_symbol_not_found(mock_search, mock_stats, capsys):
    """Test find command with symbol not found."""
    mock_search.find_symbol.return_value = None

    with patch.object(sys, "argv", ["cli.py", "/repo", "unknown"]):
        with patch("scripts.utils.semantic_search_cli.SemanticSearch", return_value=mock_search):
            main()

    captured = capsys.readouterr()
    assert "Finding symbol: unknown" in captured.out
    assert "Symbol not found: unknown" in captured.out


def test_main_find_explicit_command(mock_search, mock_stats, capsys):
    """Test explicit 'find' command (4th arg)."""
    mock_search.find_symbol.return_value = ("lib.py", 10)

    with patch.object(sys, "argv", ["cli.py", "/repo", "MyClass", "find"]):
        with patch("scripts.utils.semantic_search_cli.SemanticSearch", return_value=mock_search):
            main()

    captured = capsys.readouterr()
    assert "Finding symbol: MyClass" in captured.out
    assert "Found at: lib.py:10" in captured.out


# ==============================================================================
# CALLERS COMMAND
# ==============================================================================


def test_main_callers_found(mock_search, mock_stats, capsys):
    """Test callers command with results."""
    mock_search.find_callers.return_value = [
        ("api.py", 15, "authenticate"),
        ("views.py", 30, "login_view"),
    ]

    with patch.object(sys, "argv", ["cli.py", "/repo", "login", "callers"]):
        with patch("scripts.utils.semantic_search_cli.SemanticSearch", return_value=mock_search):
            main()

    captured = capsys.readouterr()
    assert "Finding callers of: login" in captured.out
    assert "Found 2 callers:" in captured.out
    assert "authenticate at api.py:15" in captured.out
    assert "login_view at views.py:30" in captured.out


def test_main_callers_not_found(mock_search, mock_stats, capsys):
    """Test callers command with no results."""
    mock_search.find_callers.return_value = []

    with patch.object(sys, "argv", ["cli.py", "/repo", "orphan", "callers"]):
        with patch("scripts.utils.semantic_search_cli.SemanticSearch", return_value=mock_search):
            main()

    captured = capsys.readouterr()
    assert "Finding callers of: orphan" in captured.out
    assert "No callers found for: orphan" in captured.out


# ==============================================================================
# CALLEES COMMAND
# ==============================================================================


def test_main_callees_found(mock_search, mock_stats, capsys):
    """Test callees command with results."""
    mock_search.find_callees.return_value = ["validate_user", "generate_token", "log_event"]

    with patch.object(sys, "argv", ["cli.py", "/repo", "login", "callees"]):
        with patch("scripts.utils.semantic_search_cli.SemanticSearch", return_value=mock_search):
            main()

    captured = capsys.readouterr()
    assert "Finding callees of: login" in captured.out
    assert "Found 3 callees:" in captured.out
    assert "validate_user" in captured.out
    assert "generate_token" in captured.out
    assert "log_event" in captured.out


def test_main_callees_not_found(mock_search, mock_stats, capsys):
    """Test callees command with no results."""
    mock_search.find_callees.return_value = []

    with patch.object(sys, "argv", ["cli.py", "/repo", "leaf_func", "callees"]):
        with patch("scripts.utils.semantic_search_cli.SemanticSearch", return_value=mock_search):
            main()

    captured = capsys.readouterr()
    assert "Finding callees of: leaf_func" in captured.out
    assert "No callees found for: leaf_func" in captured.out


# ==============================================================================
# REFS COMMAND
# ==============================================================================


def test_main_refs_found(mock_search, mock_stats, capsys):
    """Test refs command with results."""
    mock_search.find_references.return_value = [
        ("api.py", 20),
        ("views.py", 45),
        ("tests.py", 100),
    ]

    with patch.object(sys, "argv", ["cli.py", "/repo", "User", "refs"]):
        with patch("scripts.utils.semantic_search_cli.SemanticSearch", return_value=mock_search):
            main()

    captured = capsys.readouterr()
    assert "Finding references to: User" in captured.out
    assert "Found 3 references:" in captured.out
    assert "api.py:20" in captured.out
    assert "views.py:45" in captured.out
    assert "tests.py:100" in captured.out


def test_main_refs_not_found(mock_search, mock_stats, capsys):
    """Test refs command with no results."""
    mock_search.find_references.return_value = []

    with patch.object(sys, "argv", ["cli.py", "/repo", "unused", "refs"]):
        with patch("scripts.utils.semantic_search_cli.SemanticSearch", return_value=mock_search):
            main()

    captured = capsys.readouterr()
    assert "Finding references to: unused" in captured.out
    assert "No references found for: unused" in captured.out


# ==============================================================================
# INFO COMMAND
# ==============================================================================


def test_main_info_symbol_found_with_docstring(capsys):
    """Test info command with symbol found (with docstring)."""
    # Create symbol mock
    mock_symbol = Mock()
    mock_symbol.name = "login"
    mock_symbol.type = "function"
    mock_symbol.file = "auth.py"
    mock_symbol.line = 42
    mock_symbol.signature = "def login(username: str, password: str) -> bool"
    mock_symbol.docstring = (
        "Authenticate user with username and password. "
        "Returns True if successful, False otherwise. "
        "Extra long docstring to test truncation."
    )
    mock_symbol.references = ["authenticate", "validate"]

    # Create graph mock
    mock_graph = Mock()
    mock_graph.get_symbol_importance.return_value = 0.850123

    # Create search mock
    mock_search = MagicMock()
    mock_search.get_stats.return_value = {
        "total_symbols": 150,
        "unique_names": 80,
        "graph_nodes": 120,
        "graph_edges": 200,
    }
    mock_search.get_symbol_info.return_value = mock_symbol
    mock_search.graph = mock_graph

    with patch.object(sys, "argv", ["cli.py", "/repo", "login", "info"]):
        with patch("scripts.utils.semantic_search_cli.SemanticSearch", return_value=mock_search):
            main()

    captured = capsys.readouterr()
    assert "Symbol info: login" in captured.out
    assert "Symbol found:" in captured.out
    assert "Name: login" in captured.out
    assert "Type: function" in captured.out
    assert "File: auth.py:42" in captured.out
    assert "Signature: def login(username: str, password: str) -> bool" in captured.out
    # Docstring is truncated at 100 chars + "..."
    assert "Docstring: Authenticate user with username and password. Returns True if successful, False otherwise. Extra lon..." in captured.out
    assert "References: 2 symbols" in captured.out
    assert "Importance: 0.850123" in captured.out


def test_main_info_symbol_found_no_docstring(mock_search, mock_stats, capsys):
    """Test info command with symbol found (no docstring)."""
    mock_symbol = Mock()
    mock_symbol.name = "helper"
    mock_symbol.type = "function"
    mock_symbol.file = "utils.py"
    mock_symbol.line = 10
    mock_symbol.signature = "def helper(x)"
    mock_symbol.docstring = None
    mock_symbol.references = []

    mock_graph = Mock()
    mock_graph.get_symbol_importance.return_value = 0.123456

    mock_search.get_symbol_info.return_value = mock_symbol
    mock_search.graph = mock_graph

    with patch.object(sys, "argv", ["cli.py", "/repo", "helper", "info"]):
        with patch("scripts.utils.semantic_search_cli.SemanticSearch", return_value=mock_search):
            main()

    captured = capsys.readouterr()
    assert "Symbol info: helper" in captured.out
    assert "Name: helper" in captured.out
    assert "Type: function" in captured.out
    assert "Signature: def helper(x)" in captured.out
    assert "Docstring:" not in captured.out  # Should not print docstring line
    assert "References: 0 symbols" in captured.out
    assert "Importance: 0.123456" in captured.out


def test_main_info_symbol_not_found(mock_search, mock_stats, capsys):
    """Test info command with symbol not found."""
    mock_search.get_symbol_info.return_value = None

    with patch.object(sys, "argv", ["cli.py", "/repo", "missing", "info"]):
        with patch("scripts.utils.semantic_search_cli.SemanticSearch", return_value=mock_search):
            main()

    captured = capsys.readouterr()
    assert "Symbol info: missing" in captured.out
    assert "Symbol not found: missing" in captured.out


# ==============================================================================
# STATS COMMAND
# ==============================================================================


def test_main_stats_command(mock_search, mock_stats, capsys):
    """Test stats command (only prints stats, no extra output)."""
    with patch.object(sys, "argv", ["cli.py", "/repo", "dummy", "stats"]):
        with patch("scripts.utils.semantic_search_cli.SemanticSearch", return_value=mock_search):
            main()

    captured = capsys.readouterr()
    assert "Repository Statistics:" in captured.out
    assert "Total symbols: 150" in captured.out
    # Should NOT print any symbol-specific info
    assert "Finding" not in captured.out


# ==============================================================================
# UNKNOWN COMMAND
# ==============================================================================


def test_main_unknown_command(mock_search, mock_stats, capsys):
    """Test unknown command exits with error."""
    with patch.object(sys, "argv", ["cli.py", "/repo", "login", "invalid"]):
        with patch("scripts.utils.semantic_search_cli.SemanticSearch", return_value=mock_search):
            with pytest.raises(SystemExit) as exc_info:
                main()

    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "Unknown command: invalid" in captured.out


# ==============================================================================
# EXCEPTION HANDLING
# ==============================================================================


def test_main_valueerror_exception(capsys):
    """Test ValueError is caught and exits with error message."""
    with patch.object(sys, "argv", ["cli.py", "/repo", "symbol"]):
        with patch(
            "scripts.utils.semantic_search_cli.SemanticSearch",
            side_effect=ValueError("Invalid repository path"),
        ):
            with pytest.raises(SystemExit) as exc_info:
                main()

    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "Invalid repository path" in captured.out


def test_main_general_exception(capsys):
    """Test general Exception is caught and prints traceback."""
    with patch.object(sys, "argv", ["cli.py", "/repo", "symbol"]):
        with patch(
            "scripts.utils.semantic_search_cli.SemanticSearch",
            side_effect=RuntimeError("Database connection failed"),
        ):
            with pytest.raises(SystemExit) as exc_info:
                main()

    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "Unexpected error: Database connection failed" in captured.out
    # Traceback should be printed
    assert "Traceback" in captured.err


# ==============================================================================
# EDGE CASES
# ==============================================================================


def test_main_info_empty_docstring(mock_search, mock_stats, capsys):
    """Test info command with empty string docstring."""
    mock_symbol = Mock()
    mock_symbol.name = "func"
    mock_symbol.type = "function"
    mock_symbol.file = "test.py"
    mock_symbol.line = 5
    mock_symbol.signature = "def func()"
    mock_symbol.docstring = ""  # Empty string (falsy)
    mock_symbol.references = []

    mock_graph = Mock()
    mock_graph.get_symbol_importance.return_value = 0.0

    mock_search.get_symbol_info.return_value = mock_symbol
    mock_search.graph = mock_graph

    with patch.object(sys, "argv", ["cli.py", "/repo", "func", "info"]):
        with patch("scripts.utils.semantic_search_cli.SemanticSearch", return_value=mock_search):
            main()

    captured = capsys.readouterr()
    assert "Docstring:" not in captured.out  # Empty string is falsy


def test_main_callers_single_result(mock_search, mock_stats, capsys):
    """Test callers with single result (singular 'caller' vs 'callers')."""
    mock_search.find_callers.return_value = [("file.py", 10, "caller1")]

    with patch.object(sys, "argv", ["cli.py", "/repo", "func", "callers"]):
        with patch("scripts.utils.semantic_search_cli.SemanticSearch", return_value=mock_search):
            main()

    captured = capsys.readouterr()
    assert "Found 1 callers:" in captured.out  # Code uses plural even for 1


def test_main_refs_single_result(mock_search, mock_stats, capsys):
    """Test refs with single result."""
    mock_search.find_references.return_value = [("file.py", 20)]

    with patch.object(sys, "argv", ["cli.py", "/repo", "var", "refs"]):
        with patch("scripts.utils.semantic_search_cli.SemanticSearch", return_value=mock_search):
            main()

    captured = capsys.readouterr()
    assert "Found 1 references:" in captured.out


def test_main_logging_configured(mock_search, mock_stats):
    """Test that logging is configured when main() runs."""
    mock_search.find_symbol.return_value = ("file.py", 10)

    with patch.object(sys, "argv", ["cli.py", "/repo", "symbol"]):
        with patch("scripts.utils.semantic_search_cli.SemanticSearch", return_value=mock_search):
            with patch("logging.basicConfig") as mock_config:
                main()

    mock_config.assert_called_once()
    call_kwargs = mock_config.call_args[1]
    assert call_kwargs["level"] == 20  # logging.INFO
    assert "asctime" in call_kwargs["format"]
