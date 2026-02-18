"""Tests for RepoMapper - Core operations.

Tests initialization, file discovery, token estimation,
budget fitting, and map formatting.

Author: Cervella Tester
Date: 2026-02-10
"""

import pytest
from unittest.mock import Mock

from cervellaswarm_code_intelligence.repo_mapper import RepoMapper
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
    (tmp_path / "__pycache__").mkdir()
    (tmp_path / "__pycache__" / "app.cpython-39.pyc").write_text("compiled")
    (tmp_path / "node_modules").mkdir()
    (tmp_path / "node_modules" / "package.js").write_text("module.exports = {}")
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
    (temp_repo / "script.js").write_text("console.log('test');")
    mapper = RepoMapper(str(temp_repo))
    files = mapper._discover_source_files(filter_pattern="**/*.js")
    file_names = {f.name for f in files}
    assert "script.js" in file_names
    assert "app.py" not in file_names


def test_discover_empty_repository(tmp_path):
    """Test discovery in empty repository."""
    mapper = RepoMapper(str(tmp_path))
    files = mapper._discover_source_files()
    assert len(files) == 0


def test_discover_skips_non_files(temp_repo):
    """Test that directories matching glob patterns are skipped (line 244)."""
    # Create a directory with .py extension (unusual but possible)
    (temp_repo / "fake_module.py").mkdir()
    mapper = RepoMapper(str(temp_repo))
    files = mapper._discover_source_files()
    # All results must be actual files
    for f in files:
        assert f.is_file()
    # The fake directory should not appear
    assert "fake_module.py" not in {f.name for f in files}


# --- Test _estimate_tokens() ---

def test_estimate_tokens_basic():
    """Test token estimation with basic text."""
    mapper = RepoMapper(".")
    text = "a" * 40  # 40 characters = ~10 tokens
    assert mapper._estimate_tokens(text) == 10


def test_estimate_tokens_empty():
    """Test token estimation with empty string."""
    mapper = RepoMapper(".")
    assert mapper._estimate_tokens("") == 0


def test_estimate_tokens_signature():
    """Test token estimation for function signature."""
    mapper = RepoMapper(".")
    signature = "def login(username: str, password: str) -> bool"
    assert mapper._estimate_tokens(signature) == 11


# --- Test _fit_to_budget() ---

def test_fit_to_budget_respects_limit(temp_repo, mock_symbols):
    """Test that _fit_to_budget respects token budget."""
    mapper = RepoMapper(str(temp_repo))
    mapper.graph.get_symbol_importance = Mock(return_value=0.5)
    budget = 250
    selected = mapper._fit_to_budget(mock_symbols, budget)
    total_tokens = sum(mapper._estimate_tokens(s.signature) for s in selected)
    assert total_tokens <= (budget - 200)


def test_fit_to_budget_sorts_by_importance(temp_repo, mock_symbols):
    """Test that symbols are sorted by importance score."""
    mapper = RepoMapper(str(temp_repo))
    importance_map = {"main": 0.8, "App": 0.5, "helper": 0.2}
    mapper.graph.get_symbol_importance = lambda s: importance_map[s.name]
    selected = mapper._fit_to_budget(mock_symbols, budget=5000)
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
    assert "def main()" in map_text
    assert "class App" in map_text


def test_format_map_groups_by_file(temp_repo, mock_symbols):
    """Test that symbols are grouped by file."""
    mapper = RepoMapper(str(temp_repo))
    map_text = mapper._format_map(mock_symbols)
    lines = map_text.split("\n")
    file_headers = [line for line in lines if line.startswith("##")]
    assert len(file_headers) >= 2


def test_format_map_relative_paths(temp_repo, mock_symbols):
    """Test that file paths are relative to repo root."""
    mapper = RepoMapper(str(temp_repo))
    for symbol in mock_symbols:
        symbol.file = str(temp_repo / symbol.file)
    map_text = mapper._format_map(mock_symbols)
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
    symbols = [
        Symbol(name="bar", type="function", signature="def bar()",
               file="test.py", line=20, references=[]),
        Symbol(name="foo", type="function", signature="def foo()",
               file="test.py", line=5, references=[]),
    ]
    map_text = mapper._format_map(symbols)
    lines = map_text.split("\n")
    foo_pos = next(i for i, line in enumerate(lines) if "def foo()" in line)
    bar_pos = next(i for i, line in enumerate(lines) if "def bar()" in line)
    assert foo_pos < bar_pos
