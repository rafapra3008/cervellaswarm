"""Tests for RepoMapper - Integration, convenience, edge cases.

Tests build_map pipeline, generate_repo_map function,
get_stats, and edge cases.

Author: Cervella Tester
Date: 2026-02-10
"""

import pytest
from unittest.mock import Mock, patch

from cervellaswarm_code_intelligence.repo_mapper import RepoMapper, generate_repo_map
from cervellaswarm_code_intelligence.symbol_types import Symbol


@pytest.fixture
def temp_repo(tmp_path):
    """Create temporary repository structure."""
    (tmp_path / "app.py").write_text(
        "def main():\n    pass\n\nclass App:\n    def run(self):\n        pass\n"
    )
    (tmp_path / "utils.py").write_text(
        "def helper():\n    pass\n"
    )
    (tmp_path / "lib").mkdir()
    (tmp_path / "lib" / "core.py").write_text(
        "class Core:\n    pass\n"
    )
    return tmp_path


@pytest.fixture
def mock_symbols():
    """Create mock symbols for testing."""
    return [
        Symbol(name="main", type="function", signature="def main()",
               file="app.py", line=1, references=[]),
        Symbol(name="App", type="class", signature="class App",
               file="app.py", line=4, references=[]),
        Symbol(name="helper", type="function", signature="def helper()",
               file="utils.py", line=1, references=[]),
    ]


# --- Test get_stats() ---

def test_get_stats_basic(temp_repo):
    """Test get_stats returns expected structure."""
    mapper = RepoMapper(str(temp_repo))
    mapper.graph.get_stats = Mock(return_value={
        'nodes': 10, 'edges': 25, 'isolated': 2
    })
    stats = mapper.get_stats()
    assert 'symbols' in stats
    assert 'graph_nodes' in stats
    assert 'graph_edges' in stats
    assert 'graph_isolated' in stats
    assert stats['symbols'] == 10
    assert stats['graph_edges'] == 25


# --- Test build_map() - Integration ---

@patch('cervellaswarm_code_intelligence.repo_mapper.SymbolExtractor')
def test_build_map_integration(mock_extractor_class, temp_repo, mock_symbols):
    """Test complete build_map pipeline."""
    mock_extractor = Mock()
    mock_extractor.extract_symbols = Mock(return_value=mock_symbols[:2])
    mock_extractor_class.return_value = mock_extractor
    mapper = RepoMapper(str(temp_repo))
    mapper.extractor = mock_extractor
    mapper.graph.get_symbol_importance = Mock(return_value=0.5)
    map_text = mapper.build_map(token_budget=2000)
    assert "# REPOSITORY MAP" in map_text
    assert len(map_text) > 0


def test_build_map_no_files_found(tmp_path):
    """Test build_map when no source files are found."""
    mapper = RepoMapper(str(tmp_path))
    map_text = mapper.build_map(token_budget=2000)
    assert "No source files found" in map_text


@patch('cervellaswarm_code_intelligence.repo_mapper.SymbolExtractor')
def test_build_map_no_symbols_extracted(mock_extractor_class, temp_repo):
    """Test build_map when no symbols can be extracted."""
    mock_extractor = Mock()
    mock_extractor.extract_symbols = Mock(return_value=[])
    mock_extractor_class.return_value = mock_extractor
    mapper = RepoMapper(str(temp_repo))
    mapper.extractor = mock_extractor
    map_text = mapper.build_map(token_budget=2000)
    assert "No symbols found" in map_text


@patch('cervellaswarm_code_intelligence.repo_mapper.SymbolExtractor')
def test_build_map_respects_budget(mock_extractor_class, temp_repo):
    """Test that build_map respects token budget."""
    many_symbols = [
        Symbol(name=f"func_{i}", type="function",
               signature=f"def func_{i}(param1: str, param2: int) -> bool",
               file="test.py", line=i * 5, references=[])
        for i in range(100)
    ]
    mock_extractor = Mock()
    mock_extractor.extract_symbols = Mock(return_value=many_symbols)
    mock_extractor_class.return_value = mock_extractor
    mapper = RepoMapper(str(temp_repo))
    mapper.extractor = mock_extractor
    mapper.graph.get_symbol_importance = Mock(return_value=0.5)
    budget = 1000
    map_text = mapper.build_map(token_budget=budget)
    actual_tokens = mapper._estimate_tokens(map_text)
    assert actual_tokens <= budget


@patch('cervellaswarm_code_intelligence.repo_mapper.SymbolExtractor')
def test_build_map_handles_extraction_errors(mock_extractor_class, temp_repo):
    """Test that build_map handles extraction errors gracefully."""
    mock_extractor = Mock()
    mock_extractor.extract_symbols = Mock(side_effect=Exception("Parse error"))
    mock_extractor_class.return_value = mock_extractor
    mapper = RepoMapper(str(temp_repo))
    mapper.extractor = mock_extractor
    map_text = mapper.build_map(token_budget=2000)
    assert "No symbols found" in map_text or "No source files" in map_text


def test_build_map_with_custom_files(temp_repo, mock_symbols):
    """Test build_map with custom file list."""
    mapper = RepoMapper(str(temp_repo))
    mapper.extractor.extract_symbols = Mock(return_value=mock_symbols[:1])
    mapper.graph.get_symbol_importance = Mock(return_value=0.5)
    custom_files = [str(temp_repo / "app.py")]
    map_text = mapper.build_map(relevant_files=custom_files, token_budget=2000)
    assert "# REPOSITORY MAP" in map_text
    mapper.extractor.extract_symbols.assert_called()


@patch('cervellaswarm_code_intelligence.repo_mapper.SymbolExtractor')
def test_build_map_with_symbol_references(mock_extractor_class, temp_repo):
    """Test build_map processes symbol references (covers line 163)."""
    symbols_with_refs = [
        Symbol(name="caller", type="function", signature="def caller()",
               file="app.py", line=1, references=["callee"]),
        Symbol(name="callee", type="function", signature="def callee()",
               file="app.py", line=10, references=[]),
    ]
    mock_extractor = Mock()
    mock_extractor.extract_symbols = Mock(return_value=symbols_with_refs)
    mock_extractor_class.return_value = mock_extractor
    mapper = RepoMapper(str(temp_repo))
    mapper.extractor = mock_extractor
    map_text = mapper.build_map(token_budget=2000)
    assert "# REPOSITORY MAP" in map_text
    # Verify graph has edges from references
    assert len(mapper.graph.edges) > 0


# --- Test generate_repo_map() Convenience Function ---

@patch('cervellaswarm_code_intelligence.repo_mapper.RepoMapper')
def test_generate_repo_map_basic(mock_mapper_class, temp_repo):
    """Test convenience function generate_repo_map."""
    mock_mapper = Mock()
    mock_mapper.build_map = Mock(return_value="# REPOSITORY MAP\n\ntest content")
    mock_mapper_class.return_value = mock_mapper
    result = generate_repo_map(str(temp_repo), token_budget=2000)
    mock_mapper_class.assert_called_once_with(str(temp_repo))
    mock_mapper.build_map.assert_called_once_with(
        token_budget=2000, filter_pattern=None
    )
    assert result == "# REPOSITORY MAP\n\ntest content"


@patch('cervellaswarm_code_intelligence.repo_mapper.RepoMapper')
def test_generate_repo_map_with_output_file(mock_mapper_class, temp_repo, tmp_path):
    """Test generate_repo_map with output file."""
    mock_mapper = Mock()
    mock_mapper.build_map = Mock(return_value="# MAP CONTENT")
    mock_mapper_class.return_value = mock_mapper
    output_file = tmp_path / "output.md"
    result = generate_repo_map(
        str(temp_repo), token_budget=1500, output_file=str(output_file)
    )
    assert output_file.exists()
    assert output_file.read_text() == "# MAP CONTENT"
    assert result == "# MAP CONTENT"


@patch('cervellaswarm_code_intelligence.repo_mapper.RepoMapper')
def test_generate_repo_map_with_filter(mock_mapper_class, temp_repo):
    """Test generate_repo_map with filter pattern."""
    mock_mapper = Mock()
    mock_mapper.build_map = Mock(return_value="# MAP")
    mock_mapper_class.return_value = mock_mapper
    generate_repo_map(str(temp_repo), token_budget=2000, filter_pattern="**/*.py")
    mock_mapper.build_map.assert_called_once_with(
        token_budget=2000, filter_pattern="**/*.py"
    )


# --- Edge Cases ---

def test_edge_case_null_symbol_signature(temp_repo):
    """Test handling of symbol with empty signature."""
    mapper = RepoMapper(str(temp_repo))
    symbols = [
        Symbol(name="test", type="function", signature="",
               file="test.py", line=1, references=[])
    ]
    map_text = mapper._format_map(symbols)
    assert "# REPOSITORY MAP" in map_text


def test_edge_case_very_long_signature(temp_repo):
    """Test handling of symbol with very long signature."""
    mapper = RepoMapper(str(temp_repo))
    long_sig = "def function(" + ", ".join([f"param{i}: str" for i in range(50)]) + ")"
    symbols = [
        Symbol(name="func", type="function", signature=long_sig,
               file="test.py", line=1, references=[])
    ]
    tokens = mapper._estimate_tokens(long_sig)
    assert tokens > 100
    map_text = mapper._format_map(symbols)
    assert long_sig in map_text


def test_edge_case_zero_budget(temp_repo, mock_symbols):
    """Test _fit_to_budget with zero budget."""
    mapper = RepoMapper(str(temp_repo))
    mapper.graph.get_symbol_importance = Mock(return_value=0.5)
    selected = mapper._fit_to_budget(mock_symbols, budget=0)
    assert len(selected) == 0


def test_edge_case_negative_budget(temp_repo, mock_symbols):
    """Test _fit_to_budget with negative budget."""
    mapper = RepoMapper(str(temp_repo))
    mapper.graph.get_symbol_importance = Mock(return_value=0.5)
    selected = mapper._fit_to_budget(mock_symbols, budget=-100)
    assert len(selected) == 0
