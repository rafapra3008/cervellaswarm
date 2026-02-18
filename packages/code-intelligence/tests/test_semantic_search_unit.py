"""Fast unit tests for cervellaswarm_code_intelligence.semantic_search (with mocks).

Target: 100% coverage of SemanticSearch class and find_symbol_in_repo function.
Strategy: Mock all heavy dependencies (TreesitterParser, SymbolExtractor, DependencyGraph).

Coverage targets:
- __init__: repo validation, dependency setup
- _build_index: file scanning, symbol extraction, graph building
- find_symbol: lookup by name, PageRank disambiguation
- find_callers: dependency graph traversal
- find_callees: reference extraction
- find_references: caller location extraction
- get_symbol_info: symbol details with PageRank
- get_stats: aggregate statistics
- clear_cache: cache management
- find_symbol_in_repo: convenience wrapper

Author: Cervella Tester
Date: 2026-02-10
Sprint: S346 - FASE 6 Unit Tests
"""

import pytest
from pathlib import Path
from typing import List
from unittest.mock import Mock, MagicMock, patch, call

from cervellaswarm_code_intelligence.semantic_search import SemanticSearch, find_symbol_in_repo


# === Fixtures ===


@pytest.fixture
def mock_symbol():
    """Create mock Symbol with required attrs."""
    def _make_symbol(
        name="test_func",
        type="function",
        file="/test/file.py",
        line=10,
        signature="def test_func():",
        docstring="Test function",
        references=None
    ):
        sym = Mock()
        sym.name = name
        sym.type = type
        sym.file = file
        sym.line = line
        sym.signature = signature
        sym.docstring = docstring
        sym.references = references or []
        return sym
    return _make_symbol


@pytest.fixture
def mock_dependencies():
    """Mock TreesitterParser, SymbolExtractor, DependencyGraph."""
    with patch('cervellaswarm_code_intelligence.semantic_search.TreesitterParser') as mock_parser_cls, \
         patch('cervellaswarm_code_intelligence.semantic_search.SymbolExtractor') as mock_extractor_cls, \
         patch('cervellaswarm_code_intelligence.semantic_search.DependencyGraph') as mock_graph_cls:

        mock_parser = Mock()
        mock_extractor = Mock()
        mock_graph = Mock()

        mock_parser_cls.return_value = mock_parser
        mock_extractor_cls.return_value = mock_extractor
        mock_graph_cls.return_value = mock_graph

        # Setup default returns
        mock_extractor.extract_symbols.return_value = []
        mock_extractor.get_cache_stats.return_value = {'cached_files': 0, 'cached_symbols': 0}
        mock_graph.get_stats.return_value = {'nodes': 0, 'edges': 0}
        mock_graph.nodes = {}

        yield {
            'parser_cls': mock_parser_cls,
            'extractor_cls': mock_extractor_cls,
            'graph_cls': mock_graph_cls,
            'parser': mock_parser,
            'extractor': mock_extractor,
            'graph': mock_graph,
        }


@pytest.fixture
def search_no_index(tmp_path, mock_dependencies):
    """SemanticSearch with _build_index patched (no file scanning)."""
    with patch.object(SemanticSearch, '_build_index'):
        search = SemanticSearch(str(tmp_path))
        search.symbol_index = {}
        search.extractor = mock_dependencies['extractor']
        search.graph = mock_dependencies['graph']
        yield search


# === __init__ Tests (3) ===


def test_init_repo_not_exists(mock_dependencies):
    """__init__ raises ValueError if repo_root doesn't exist."""
    with pytest.raises(ValueError, match="does not exist"):
        SemanticSearch("/nonexistent/path")


def test_init_repo_not_dir(tmp_path, mock_dependencies):
    """__init__ raises ValueError if repo_root is file not dir."""
    file_path = tmp_path / "file.txt"
    file_path.write_text("content")

    with pytest.raises(ValueError, match="not a directory"):
        SemanticSearch(str(file_path))


def test_init_valid_dir(tmp_path, mock_dependencies):
    """__init__ with valid dir calls _build_index and sets attrs."""
    with patch.object(SemanticSearch, '_build_index') as mock_build:
        search = SemanticSearch(str(tmp_path))

        assert search.repo_root == tmp_path.resolve()
        assert search.extractor == mock_dependencies['extractor']
        assert search.graph == mock_dependencies['graph']
        assert search.symbol_index == {}
        mock_build.assert_called_once()


# === _build_index Tests (6) ===


def test_build_index_scans_correct_extensions(tmp_path, mock_dependencies):
    """_build_index scans .py, .ts, .tsx, .js, .jsx files."""
    # Create test files
    (tmp_path / "test.py").write_text("# python")
    (tmp_path / "test.ts").write_text("// ts")
    (tmp_path / "test.tsx").write_text("// tsx")
    (tmp_path / "test.js").write_text("// js")
    (tmp_path / "test.jsx").write_text("// jsx")
    (tmp_path / "test.txt").write_text("ignored")

    search = SemanticSearch(str(tmp_path))

    # Should call extract_symbols for each supported file
    calls = mock_dependencies['extractor'].extract_symbols.call_args_list
    called_files = {Path(call[0][0]).name for call in calls}

    assert "test.py" in called_files
    assert "test.ts" in called_files
    assert "test.tsx" in called_files
    assert "test.js" in called_files
    assert "test.jsx" in called_files
    assert "test.txt" not in called_files


def test_build_index_excludes_dirs(tmp_path, mock_dependencies):
    """_build_index excludes node_modules, .git, __pycache__ dirs."""
    # Create excluded dirs
    (tmp_path / "node_modules").mkdir()
    (tmp_path / "node_modules" / "test.py").write_text("# excluded")
    (tmp_path / ".git").mkdir()
    (tmp_path / ".git" / "test.py").write_text("# excluded")
    (tmp_path / "__pycache__").mkdir()
    (tmp_path / "__pycache__" / "test.py").write_text("# excluded")
    (tmp_path / "good.py").write_text("# included")

    search = SemanticSearch(str(tmp_path))

    calls = mock_dependencies['extractor'].extract_symbols.call_args_list
    called_files = {Path(call[0][0]).name for call in calls}

    assert "good.py" in called_files
    # node_modules, .git, __pycache__ should be excluded
    assert len(called_files) == 1


def test_build_index_excludes_egg_info(tmp_path, mock_dependencies):
    """_build_index excludes *.egg-info dirs."""
    (tmp_path / "mypackage.egg-info").mkdir()
    (tmp_path / "mypackage.egg-info" / "test.py").write_text("# excluded")
    (tmp_path / "good.py").write_text("# included")

    search = SemanticSearch(str(tmp_path))

    calls = mock_dependencies['extractor'].extract_symbols.call_args_list
    called_files = {Path(call[0][0]).name for call in calls}

    assert "good.py" in called_files
    assert len(called_files) == 1


def test_build_index_extracts_symbols_and_builds_graph(tmp_path, mock_dependencies, mock_symbol):
    """_build_index extracts symbols, adds to index and graph."""
    (tmp_path / "test.py").write_text("# test")

    sym1 = mock_symbol(name="func1", file=str(tmp_path / "test.py"), line=1, references=["ref_a", "ref_b"])
    sym2 = mock_symbol(name="func2", file=str(tmp_path / "test.py"), line=5)
    mock_dependencies['extractor'].extract_symbols.return_value = [sym1, sym2]
    mock_dependencies['graph']._get_symbol_id.side_effect = lambda s: f"{s.file}:{s.name}"

    search = SemanticSearch(str(tmp_path))

    # Check index
    assert "func1" in search.symbol_index
    assert "func2" in search.symbol_index
    assert search.symbol_index["func1"] == [sym1]

    # Check graph calls
    assert mock_dependencies['graph'].add_symbol.call_count == 2
    # Check add_reference was called for sym1's references
    assert mock_dependencies['graph'].add_reference.call_count == 2
    mock_dependencies['graph'].compute_importance.assert_called_once()


def test_build_index_handles_extraction_error(tmp_path, mock_dependencies, caplog):
    """_build_index logs warning on extraction error and continues."""
    (tmp_path / "bad.py").write_text("# bad")
    (tmp_path / "good.py").write_text("# good")

    def side_effect(file_path):
        if "bad.py" in file_path:
            raise ValueError("parse error")
        return []

    mock_dependencies['extractor'].extract_symbols.side_effect = side_effect

    search = SemanticSearch(str(tmp_path))

    # Should log warning
    assert any("Failed to extract" in rec.message for rec in caplog.records)
    # Should continue and call compute_importance
    mock_dependencies['graph'].compute_importance.assert_called_once()


def test_build_index_calls_compute_importance(tmp_path, mock_dependencies):
    """_build_index calls graph.compute_importance() at end."""
    (tmp_path / "test.py").write_text("# test")

    search = SemanticSearch(str(tmp_path))

    mock_dependencies['graph'].compute_importance.assert_called_once()


# === find_symbol Tests (4) ===


def test_find_symbol_not_in_index(search_no_index):
    """find_symbol returns None if name not in index."""
    result = search_no_index.find_symbol("missing")
    assert result is None


def test_find_symbol_empty_candidates(search_no_index):
    """find_symbol returns None if candidates list is empty."""
    search_no_index.symbol_index["empty"] = []
    result = search_no_index.find_symbol("empty")
    assert result is None


def test_find_symbol_single_candidate(search_no_index, mock_symbol):
    """find_symbol returns (file, line) for single candidate."""
    sym = mock_symbol(name="single", file="/test/file.py", line=42)
    search_no_index.symbol_index["single"] = [sym]

    result = search_no_index.find_symbol("single")
    assert result == ("/test/file.py", 42)


def test_find_symbol_multiple_candidates_highest_importance(search_no_index, mock_symbol):
    """find_symbol chooses candidate with highest PageRank score."""
    sym1 = mock_symbol(name="multi", file="/test/a.py", line=10)
    sym2 = mock_symbol(name="multi", file="/test/b.py", line=20)
    sym3 = mock_symbol(name="multi", file="/test/c.py", line=30)

    search_no_index.symbol_index["multi"] = [sym1, sym2, sym3]

    # sym2 has highest importance
    search_no_index.graph.get_symbol_importance.side_effect = lambda s: {
        sym1: 0.1,
        sym2: 0.9,
        sym3: 0.3
    }[s]

    result = search_no_index.find_symbol("multi")
    assert result == ("/test/b.py", 20)


# === find_callers Tests (4) ===


def test_find_callers_not_in_index(search_no_index):
    """find_callers returns [] if name not in index."""
    result = search_no_index.find_callers("missing")
    assert result == []


def test_find_callers_caller_in_graph_nodes(search_no_index, mock_symbol):
    """find_callers returns (file, line, name) when caller in graph.nodes."""
    sym = mock_symbol(name="target", file="/test/target.py", line=10)
    search_no_index.symbol_index["target"] = [sym]

    # Setup graph to return caller_id
    caller_sym = mock_symbol(name="caller", file="/test/caller.py", line=5)
    search_no_index.graph.get_symbol_referenced_by.return_value = ["/test/caller.py:caller"]
    search_no_index.graph.nodes = {"/test/caller.py:caller": caller_sym}

    result = search_no_index.find_callers("target")
    assert result == [("/test/caller.py", 5, "caller")]


def test_find_callers_caller_not_in_graph_nodes(search_no_index, mock_symbol):
    """find_callers uses fallback (file, 0, name) when caller not in nodes."""
    sym = mock_symbol(name="target", file="/test/target.py", line=10)
    search_no_index.symbol_index["target"] = [sym]

    # Caller not in nodes
    search_no_index.graph.get_symbol_referenced_by.return_value = ["/test/caller.py:caller"]
    search_no_index.graph.nodes = {}

    result = search_no_index.find_callers("target")
    assert result == [("/test/caller.py", 0, "caller")]


def test_find_callers_invalid_caller_id_format(search_no_index, mock_symbol):
    """find_callers skips caller_id with no ':' (len(parts) != 2)."""
    sym = mock_symbol(name="target", file="/test/target.py", line=10)
    search_no_index.symbol_index["target"] = [sym]

    # Invalid format (no colon)
    search_no_index.graph.get_symbol_referenced_by.return_value = ["invalid_id"]

    result = search_no_index.find_callers("target")
    assert result == []


# === find_callees Tests (3) ===


def test_find_callees_not_in_index(search_no_index):
    """find_callees returns [] if name not in index."""
    result = search_no_index.find_callees("missing")
    assert result == []


def test_find_callees_with_references(search_no_index, mock_symbol):
    """find_callees returns sorted unique references."""
    sym = mock_symbol(name="func", references=["ref_b", "ref_a", "ref_c"])
    search_no_index.symbol_index["func"] = [sym]

    result = search_no_index.find_callees("func")
    assert result == ["ref_a", "ref_b", "ref_c"]


def test_find_callees_multiple_symbols_union_references(search_no_index, mock_symbol):
    """find_callees unions references from multiple symbols with same name."""
    sym1 = mock_symbol(name="func", references=["ref_a", "ref_b"])
    sym2 = mock_symbol(name="func", references=["ref_b", "ref_c"])
    search_no_index.symbol_index["func"] = [sym1, sym2]

    result = search_no_index.find_callees("func")
    assert result == ["ref_a", "ref_b", "ref_c"]


# === find_references Tests (2) ===


def test_find_references_not_in_index(search_no_index):
    """find_references returns [] if name not in index."""
    result = search_no_index.find_references("missing")
    assert result == []


def test_find_references_extracts_file_line_from_callers(search_no_index, mock_symbol):
    """find_references returns [(file, line)] from find_callers."""
    sym = mock_symbol(name="target", file="/test/target.py", line=10)
    search_no_index.symbol_index["target"] = [sym]

    caller_sym = mock_symbol(name="caller", file="/test/caller.py", line=5)
    search_no_index.graph.get_symbol_referenced_by.return_value = ["/test/caller.py:caller"]
    search_no_index.graph.nodes = {"/test/caller.py:caller": caller_sym}

    result = search_no_index.find_references("target")
    assert result == [("/test/caller.py", 5)]


# === get_symbol_info Tests (4) ===


def test_get_symbol_info_not_in_index(search_no_index):
    """get_symbol_info returns None if name not in index."""
    result = search_no_index.get_symbol_info("missing")
    assert result is None


def test_get_symbol_info_empty_candidates(search_no_index):
    """get_symbol_info returns None if candidates list empty."""
    search_no_index.symbol_index["empty"] = []
    result = search_no_index.get_symbol_info("empty")
    assert result is None


def test_get_symbol_info_single_candidate(search_no_index, mock_symbol):
    """get_symbol_info returns Symbol for single candidate."""
    sym = mock_symbol(name="single")
    search_no_index.symbol_index["single"] = [sym]

    result = search_no_index.get_symbol_info("single")
    assert result == sym


def test_get_symbol_info_multiple_candidates_max_importance(search_no_index, mock_symbol):
    """get_symbol_info returns Symbol with highest PageRank score."""
    sym1 = mock_symbol(name="multi", file="/test/a.py")
    sym2 = mock_symbol(name="multi", file="/test/b.py")
    search_no_index.symbol_index["multi"] = [sym1, sym2]

    search_no_index.graph.get_symbol_importance.side_effect = lambda s: {
        sym1: 0.2,
        sym2: 0.8
    }[s]

    result = search_no_index.get_symbol_info("multi")
    assert result == sym2


# === get_stats Test (1) ===


def test_get_stats_returns_correct_dict(search_no_index, mock_symbol):
    """get_stats returns dict with all statistics."""
    sym1 = mock_symbol(name="func1")
    sym2 = mock_symbol(name="func2")
    sym3 = mock_symbol(name="func1")  # Duplicate name

    search_no_index.symbol_index = {
        "func1": [sym1, sym3],
        "func2": [sym2],
    }

    search_no_index.graph.get_stats.return_value = {'nodes': 100, 'edges': 250}
    search_no_index.extractor.get_cache_stats.return_value = {
        'cached_files': 42,
        'cached_symbols': 99
    }

    result = search_no_index.get_stats()

    assert result == {
        'total_symbols': 3,  # sym1 + sym2 + sym3
        'unique_names': 2,   # func1, func2
        'graph_nodes': 100,
        'graph_edges': 250,
        'cached_files': 42,
    }


# === clear_cache Test (1) ===


def test_clear_cache_calls_extractor_clear_cache(search_no_index):
    """clear_cache calls extractor.clear_cache()."""
    search_no_index.clear_cache()
    search_no_index.extractor.clear_cache.assert_called_once()


# === find_symbol_in_repo Test (1) ===


def test_find_symbol_in_repo_convenience_function(tmp_path, mock_dependencies, mock_symbol):
    """find_symbol_in_repo creates SemanticSearch and calls find_symbol."""
    with patch.object(SemanticSearch, '_build_index'):
        with patch.object(SemanticSearch, 'find_symbol') as mock_find:
            mock_find.return_value = ("/test/file.py", 42)

            result = find_symbol_in_repo(str(tmp_path), "test_func")

            assert result == ("/test/file.py", 42)
            mock_find.assert_called_once_with("test_func")
