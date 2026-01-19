"""Test suite for repo_mapper.py

Tests RepoMapper class and generate_repo_map convenience function.

Author: Cervella Tester
Date: 2026-01-19
"""

import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pytest
from unittest.mock import Mock, patch, MagicMock

from scripts.utils.repo_mapper import RepoMapper, generate_repo_map
from scripts.utils.symbol_extractor import Symbol


@pytest.fixture
def temp_repo(tmp_path):
    """Create temporary repository structure."""
    # Create source files
    (tmp_path / "app.py").write_text(
        "def main():\n    pass\n\nclass App:\n    def run(self):\n        pass\n"
    )
    (tmp_path / "utils.py").write_text(
        "def helper():\n    pass\n"
    )

    # Create subdirectory
    (tmp_path / "lib").mkdir()
    (tmp_path / "lib" / "core.py").write_text(
        "class Core:\n    pass\n"
    )

    # Create excluded directories (should be ignored)
    (tmp_path / "__pycache__").mkdir()
    (tmp_path / "__pycache__" / "app.cpython-39.pyc").write_text("compiled")

    (tmp_path / "node_modules").mkdir()
    (tmp_path / "node_modules" / "package.js").write_text("module.exports = {}")

    return tmp_path


@pytest.fixture
def mock_symbols():
    """Create mock symbols for testing."""
    symbols = [
        Symbol(
            name="main",
            type="function",
            signature="def main()",
            file="app.py",
            line=1,
            references=[]
        ),
        Symbol(
            name="App",
            type="class",
            signature="class App",
            file="app.py",
            line=4,
            references=[]
        ),
        Symbol(
            name="helper",
            type="function",
            signature="def helper()",
            file="utils.py",
            line=1,
            references=[]
        ),
    ]
    return symbols


# --- Test RepoMapper.__init__() ---

def test_init_valid_path(temp_repo):
    """Test initialization with valid repository path."""
    mapper = RepoMapper(str(temp_repo))

    assert mapper.repo_path == temp_repo.resolve()
    assert mapper.parser is not None
    assert mapper.extractor is not None
    assert mapper.graph is not None


def test_init_relative_path_resolved(temp_repo, monkeypatch):
    """Test that relative paths are resolved to absolute."""
    monkeypatch.chdir(temp_repo.parent)

    mapper = RepoMapper(temp_repo.name)

    assert mapper.repo_path.is_absolute()
    assert mapper.repo_path == temp_repo.resolve()


def test_init_invalid_path():
    """Test initialization with non-existent path."""
    with pytest.raises(FileNotFoundError, match="Repository path not found"):
        RepoMapper("/nonexistent/path/to/repo")


# --- Test _discover_source_files() ---

def test_discover_finds_python_files(temp_repo):
    """Test discovery of Python source files."""
    mapper = RepoMapper(str(temp_repo))

    files = mapper._discover_source_files()
    file_names = {f.name for f in files}

    assert "app.py" in file_names
    assert "utils.py" in file_names
    assert "core.py" in file_names


def test_discover_excludes_pycache(temp_repo):
    """Test that __pycache__ directories are excluded."""
    mapper = RepoMapper(str(temp_repo))

    files = mapper._discover_source_files()

    for file in files:
        assert "__pycache__" not in file.parts
        assert not file.name.endswith(".pyc")


def test_discover_excludes_node_modules(temp_repo):
    """Test that node_modules directories are excluded."""
    mapper = RepoMapper(str(temp_repo))

    files = mapper._discover_source_files()

    for file in files:
        assert "node_modules" not in file.parts


def test_discover_with_filter_pattern(temp_repo):
    """Test file discovery with custom filter pattern."""
    # Add a JS file
    (temp_repo / "script.js").write_text("console.log('test');")

    mapper = RepoMapper(str(temp_repo))

    # Filter only JS files
    files = mapper._discover_source_files(filter_pattern="**/*.js")
    file_names = {f.name for f in files}

    assert "script.js" in file_names
    assert "app.py" not in file_names


def test_discover_empty_repository(tmp_path):
    """Test discovery in empty repository."""
    mapper = RepoMapper(str(tmp_path))

    files = mapper._discover_source_files()

    assert len(files) == 0


# --- Test _estimate_tokens() ---

def test_estimate_tokens_basic():
    """Test token estimation with basic text."""
    mapper = RepoMapper(".")

    # 4 characters ≈ 1 token
    text = "a" * 40  # 40 characters = ~10 tokens
    tokens = mapper._estimate_tokens(text)

    assert tokens == 10


def test_estimate_tokens_empty():
    """Test token estimation with empty string."""
    mapper = RepoMapper(".")

    tokens = mapper._estimate_tokens("")

    assert tokens == 0


def test_estimate_tokens_signature():
    """Test token estimation for function signature."""
    mapper = RepoMapper(".")

    signature = "def login(username: str, password: str) -> bool"
    tokens = mapper._estimate_tokens(signature)

    # 47 characters / 4 = 11 tokens
    assert tokens == 11


# --- Test _fit_to_budget() ---

def test_fit_to_budget_respects_limit(temp_repo, mock_symbols):
    """Test that _fit_to_budget respects token budget."""
    mapper = RepoMapper(str(temp_repo))

    # Mock graph to return importance scores
    mapper.graph.get_symbol_importance = Mock(return_value=0.5)

    # Very small budget - should select only few symbols
    budget = 250  # Header overhead ~200, leaves ~50 for symbols
    selected = mapper._fit_to_budget(mock_symbols, budget)

    # Calculate total tokens used
    total_tokens = sum(mapper._estimate_tokens(s.signature) for s in selected)

    # Should be within budget (minus header overhead)
    assert total_tokens <= (budget - 200)


def test_fit_to_budget_sorts_by_importance(temp_repo, mock_symbols):
    """Test that symbols are sorted by importance score."""
    mapper = RepoMapper(str(temp_repo))

    # Mock graph to return different importance scores
    importance_map = {
        "main": 0.8,    # Highest
        "App": 0.5,     # Medium
        "helper": 0.2   # Lowest
    }
    mapper.graph.get_symbol_importance = lambda s: importance_map[s.name]

    # Large budget to fit all symbols
    selected = mapper._fit_to_budget(mock_symbols, budget=5000)

    # Verify "main" comes first (highest importance)
    assert selected[0].name == "main"


def test_fit_to_budget_empty_symbols(temp_repo):
    """Test _fit_to_budget with empty symbol list."""
    mapper = RepoMapper(str(temp_repo))

    selected = mapper._fit_to_budget([], budget=2000)

    assert selected == []


# --- Test _format_map() ---

def test_format_map_basic_structure(temp_repo, mock_symbols):
    """Test basic markdown structure of formatted map."""
    mapper = RepoMapper(str(temp_repo))

    map_text = mapper._format_map(mock_symbols)

    assert "# REPOSITORY MAP" in map_text
    assert "## app.py" in map_text or "##" in map_text  # File headers
    assert "def main()" in map_text
    assert "class App" in map_text


def test_format_map_groups_by_file(temp_repo, mock_symbols):
    """Test that symbols are grouped by file."""
    mapper = RepoMapper(str(temp_repo))

    map_text = mapper._format_map(mock_symbols)

    # Should have separate sections for app.py and utils.py
    lines = map_text.split("\n")
    file_headers = [line for line in lines if line.startswith("##")]

    assert len(file_headers) >= 2  # At least 2 files


def test_format_map_relative_paths(temp_repo, mock_symbols):
    """Test that file paths are relative to repo root."""
    mapper = RepoMapper(str(temp_repo))

    # Update symbols to use absolute paths
    for symbol in mock_symbols:
        symbol.file = str(temp_repo / symbol.file)

    map_text = mapper._format_map(mock_symbols)

    # Should show relative paths, not absolute
    assert str(temp_repo) not in map_text
    assert "app.py" in map_text or "/" in map_text


def test_format_map_empty_symbols(temp_repo):
    """Test formatting with no symbols."""
    mapper = RepoMapper(str(temp_repo))

    map_text = mapper._format_map([])

    assert "# REPOSITORY MAP" in map_text
    assert "No symbols selected" in map_text


def test_format_map_sorts_by_line_number(temp_repo):
    """Test that symbols within a file are sorted by line number."""
    mapper = RepoMapper(str(temp_repo))

    # Create symbols in reverse order
    symbols = [
        Symbol(name="bar", type="function", signature="def bar()",
               file="test.py", line=20, references=[]),
        Symbol(name="foo", type="function", signature="def foo()",
               file="test.py", line=5, references=[]),
    ]

    map_text = mapper._format_map(symbols)
    lines = map_text.split("\n")

    # Find positions of symbols
    foo_pos = next(i for i, line in enumerate(lines) if "def foo()" in line)
    bar_pos = next(i for i, line in enumerate(lines) if "def bar()" in line)

    # foo (line 5) should appear before bar (line 20)
    assert foo_pos < bar_pos


# --- Test get_stats() ---

def test_get_stats_basic(temp_repo):
    """Test get_stats returns expected structure."""
    mapper = RepoMapper(str(temp_repo))

    # Mock graph stats
    mapper.graph.get_stats = Mock(return_value={
        'nodes': 10,
        'edges': 25,
        'isolated': 2
    })

    stats = mapper.get_stats()

    assert 'symbols' in stats
    assert 'graph_nodes' in stats
    assert 'graph_edges' in stats
    assert 'graph_isolated' in stats
    assert stats['symbols'] == 10
    assert stats['graph_edges'] == 25


# --- Test build_map() - Integration ---

@patch('scripts.utils.repo_mapper.SymbolExtractor')
def test_build_map_integration(mock_extractor_class, temp_repo, mock_symbols):
    """Test complete build_map pipeline."""
    # Mock symbol extraction
    mock_extractor = Mock()
    mock_extractor.extract_symbols = Mock(return_value=mock_symbols[:2])
    mock_extractor_class.return_value = mock_extractor

    mapper = RepoMapper(str(temp_repo))
    mapper.extractor = mock_extractor

    # Mock graph importance
    mapper.graph.get_symbol_importance = Mock(return_value=0.5)

    map_text = mapper.build_map(token_budget=2000)

    # Verify structure
    assert "# REPOSITORY MAP" in map_text
    assert len(map_text) > 0


def test_build_map_no_files_found(tmp_path):
    """Test build_map when no source files are found."""
    mapper = RepoMapper(str(tmp_path))

    map_text = mapper.build_map(token_budget=2000)

    assert "No source files found" in map_text


@patch('scripts.utils.repo_mapper.SymbolExtractor')
def test_build_map_no_symbols_extracted(mock_extractor_class, temp_repo):
    """Test build_map when no symbols can be extracted."""
    # Mock symbol extraction to return empty list
    mock_extractor = Mock()
    mock_extractor.extract_symbols = Mock(return_value=[])
    mock_extractor_class.return_value = mock_extractor

    mapper = RepoMapper(str(temp_repo))
    mapper.extractor = mock_extractor

    map_text = mapper.build_map(token_budget=2000)

    assert "No symbols found" in map_text


@patch('scripts.utils.repo_mapper.SymbolExtractor')
def test_build_map_respects_budget(mock_extractor_class, temp_repo, mock_symbols):
    """Test that build_map respects token budget."""
    # Create many symbols
    many_symbols = []
    for i in range(100):
        many_symbols.append(
            Symbol(
                name=f"func_{i}",
                type="function",
                signature=f"def func_{i}(param1: str, param2: int) -> bool",
                file="test.py",
                line=i * 5,
                references=[]
            )
        )

    mock_extractor = Mock()
    mock_extractor.extract_symbols = Mock(return_value=many_symbols)
    mock_extractor_class.return_value = mock_extractor

    mapper = RepoMapper(str(temp_repo))
    mapper.extractor = mock_extractor
    mapper.graph.get_symbol_importance = Mock(return_value=0.5)

    budget = 1000
    map_text = mapper.build_map(token_budget=budget)

    # Verify total tokens don't exceed budget
    actual_tokens = mapper._estimate_tokens(map_text)
    assert actual_tokens <= budget


@patch('scripts.utils.repo_mapper.SymbolExtractor')
def test_build_map_handles_extraction_errors(mock_extractor_class, temp_repo):
    """Test that build_map handles extraction errors gracefully."""
    mock_extractor = Mock()
    mock_extractor.extract_symbols = Mock(side_effect=Exception("Parse error"))
    mock_extractor_class.return_value = mock_extractor

    mapper = RepoMapper(str(temp_repo))
    mapper.extractor = mock_extractor

    # Should not raise, should return message about no symbols
    map_text = mapper.build_map(token_budget=2000)

    assert "No symbols found" in map_text or "No source files" in map_text


def test_build_map_with_custom_files(temp_repo, mock_symbols):
    """Test build_map with custom file list."""
    mapper = RepoMapper(str(temp_repo))
    mapper.extractor.extract_symbols = Mock(return_value=mock_symbols[:1])
    mapper.graph.get_symbol_importance = Mock(return_value=0.5)

    custom_files = [str(temp_repo / "app.py")]
    map_text = mapper.build_map(
        relevant_files=custom_files,
        token_budget=2000
    )

    assert "# REPOSITORY MAP" in map_text
    mapper.extractor.extract_symbols.assert_called()


# --- Test generate_repo_map() Convenience Function ---

@patch('scripts.utils.repo_mapper.RepoMapper')
def test_generate_repo_map_basic(mock_mapper_class, temp_repo):
    """Test convenience function generate_repo_map."""
    mock_mapper = Mock()
    mock_mapper.build_map = Mock(return_value="# REPOSITORY MAP\n\ntest content")
    mock_mapper_class.return_value = mock_mapper

    result = generate_repo_map(str(temp_repo), token_budget=2000)

    mock_mapper_class.assert_called_once_with(str(temp_repo))
    mock_mapper.build_map.assert_called_once_with(
        token_budget=2000,
        filter_pattern=None
    )
    assert result == "# REPOSITORY MAP\n\ntest content"


@patch('scripts.utils.repo_mapper.RepoMapper')
def test_generate_repo_map_with_output_file(mock_mapper_class, temp_repo, tmp_path):
    """Test generate_repo_map with output file."""
    mock_mapper = Mock()
    mock_mapper.build_map = Mock(return_value="# MAP CONTENT")
    mock_mapper_class.return_value = mock_mapper

    output_file = tmp_path / "output.md"
    result = generate_repo_map(
        str(temp_repo),
        token_budget=1500,
        output_file=str(output_file)
    )

    # Should write to file
    assert output_file.exists()
    assert output_file.read_text() == "# MAP CONTENT"
    assert result == "# MAP CONTENT"


@patch('scripts.utils.repo_mapper.RepoMapper')
def test_generate_repo_map_with_filter(mock_mapper_class, temp_repo):
    """Test generate_repo_map with filter pattern."""
    mock_mapper = Mock()
    mock_mapper.build_map = Mock(return_value="# MAP")
    mock_mapper_class.return_value = mock_mapper

    generate_repo_map(
        str(temp_repo),
        token_budget=2000,
        filter_pattern="**/*.py"
    )

    mock_mapper.build_map.assert_called_once_with(
        token_budget=2000,
        filter_pattern="**/*.py"
    )


# --- Edge Cases ---

def test_edge_case_null_symbol_signature(temp_repo):
    """Test handling of symbol with empty signature."""
    mapper = RepoMapper(str(temp_repo))

    symbols = [
        Symbol(name="test", type="function", signature="",
               file="test.py", line=1, references=[])
    ]

    # Should not crash
    map_text = mapper._format_map(symbols)
    assert "# REPOSITORY MAP" in map_text


def test_edge_case_very_long_signature(temp_repo):
    """Test handling of symbol with very long signature."""
    mapper = RepoMapper(str(temp_repo))

    # Create symbol with 500 character signature
    long_sig = "def function(" + ", ".join([f"param{i}: str" for i in range(50)]) + ")"
    symbols = [
        Symbol(name="func", type="function", signature=long_sig,
               file="test.py", line=1, references=[])
    ]

    # Should handle without issues
    tokens = mapper._estimate_tokens(long_sig)
    assert tokens > 100

    map_text = mapper._format_map(symbols)
    assert long_sig in map_text


def test_edge_case_zero_budget(temp_repo, mock_symbols):
    """Test _fit_to_budget with zero budget."""
    mapper = RepoMapper(str(temp_repo))
    mapper.graph.get_symbol_importance = Mock(return_value=0.5)

    selected = mapper._fit_to_budget(mock_symbols, budget=0)

    # Should return empty list (no symbols fit)
    assert len(selected) == 0


def test_edge_case_negative_budget(temp_repo, mock_symbols):
    """Test _fit_to_budget with negative budget."""
    mapper = RepoMapper(str(temp_repo))
    mapper.graph.get_symbol_importance = Mock(return_value=0.5)

    selected = mapper._fit_to_budget(mock_symbols, budget=-100)

    # Should return empty list
    assert len(selected) == 0
