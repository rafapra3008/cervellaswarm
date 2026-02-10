"""Tests for SymbolExtractor - the ORCHESTRATOR module.

Tests the coordination between TreesitterParser, SymbolCache,
PythonExtractor, and TypeScriptExtractor.

Author: Cervella Tester
Date: 2026-02-10
"""
from pathlib import Path
from unittest.mock import MagicMock, patch
import pytest
from scripts.utils.symbol_extractor import SymbolExtractor, extract_symbols
from scripts.utils.symbol_types import Symbol


# ============================================================================
# Test Fixtures
# ============================================================================

@pytest.fixture
def mock_parser():
    """Create a mock TreesitterParser."""
    return MagicMock()


@pytest.fixture
def extractor_with_mocks(mock_parser):
    """Create SymbolExtractor with mocked internal components."""
    extractor = SymbolExtractor(mock_parser)
    extractor._symbol_cache = MagicMock()
    extractor._python_extractor = MagicMock()
    extractor._ts_extractor = MagicMock()
    return extractor, mock_parser


def make_symbol(name, type_="function", signature=None, references=None):
    """Helper to create Symbol instances."""
    return Symbol(
        name=name, type=type_, signature=signature or f"def {name}()",
        references=references or [], line=1, file="test.py"
    )


# ============================================================================
# 1. Initialization (3 tests)
# ============================================================================

def test_init_creates_components(mock_parser):
    """Extractor creates all required components."""
    extractor = SymbolExtractor(mock_parser)
    assert extractor.parser is mock_parser
    assert extractor._symbol_cache is not None
    assert extractor._python_extractor is not None
    assert extractor._ts_extractor is not None


def test_init_custom_cache_maxsize(mock_parser):
    """Custom cache_maxsize is passed to SymbolCache."""
    with patch("scripts.utils.symbol_extractor.SymbolCache") as mock_cache_cls:
        SymbolExtractor(mock_parser, cache_maxsize=2000)
        mock_cache_cls.assert_called_once_with(maxsize=2000)


def test_init_logs_message(mock_parser, caplog):
    """Initialization logs debug message."""
    with caplog.at_level("DEBUG"):
        SymbolExtractor(mock_parser, cache_maxsize=500)
    assert "SymbolExtractor initialized with cache maxsize=500" in caplog.text


# ============================================================================
# 2. extract_symbols - Cache hit (2 tests)
# ============================================================================

def test_extract_symbols_cache_hit_returns_cached(extractor_with_mocks):
    """Cache hit returns cached symbols without parsing."""
    extractor, mock_parser = extractor_with_mocks
    cached_symbols = [make_symbol("cached_func")]
    extractor._symbol_cache.get.return_value = cached_symbols
    with patch("scripts.utils.symbol_extractor.os.path.getmtime", return_value=123.0):
        with patch("scripts.utils.symbol_extractor.Path") as mock_path_cls:
            mock_path = MagicMock()
            mock_path.resolve.return_value = "/abs/test.py"
            mock_path_cls.return_value = mock_path
            result = extractor.extract_symbols("test.py")
    assert result == cached_symbols
    extractor._symbol_cache.get.assert_called_once_with("/abs/test.py", 123.0)
    mock_parser.parse_file.assert_not_called()


def test_extract_symbols_cache_hit_no_parse(extractor_with_mocks):
    """Cache hit does not call parser.parse_file."""
    extractor, mock_parser = extractor_with_mocks
    extractor._symbol_cache.get.return_value = [make_symbol("func")]
    with patch("scripts.utils.symbol_extractor.os.path.getmtime", return_value=123.0):
        with patch("scripts.utils.symbol_extractor.Path") as mock_path_cls:
            mock_path = MagicMock()
            mock_path.resolve.return_value = "/abs/test.py"
            mock_path_cls.return_value = mock_path
            extractor.extract_symbols("test.py")
    mock_parser.parse_file.assert_not_called()


# ============================================================================
# 3. extract_symbols - Language routing (4 tests)
# ============================================================================

def test_extract_symbols_routes_python(extractor_with_mocks):
    """Python file routes to PythonExtractor."""
    extractor, mock_parser = extractor_with_mocks
    extractor._symbol_cache.get.return_value = None
    mock_tree = MagicMock()
    mock_parser.parse_file.return_value = mock_tree
    mock_parser.detect_language.return_value = "python"
    python_symbols = [make_symbol("py_func")]
    extractor._python_extractor.extract_python_symbols.return_value = python_symbols
    with patch("scripts.utils.symbol_extractor.os.path.getmtime", return_value=123.0):
        with patch("scripts.utils.symbol_extractor.Path") as mock_path_cls:
            mock_path = MagicMock()
            mock_path.resolve.return_value = "/abs/test.py"
            mock_path_cls.return_value = mock_path
            result = extractor.extract_symbols("test.py")
    assert result == python_symbols
    extractor._python_extractor.extract_python_symbols.assert_called_once_with(mock_tree, "test.py")


def test_extract_symbols_routes_typescript(extractor_with_mocks):
    """TypeScript file routes to TypeScriptExtractor.extract_typescript_symbols."""
    extractor, mock_parser = extractor_with_mocks
    extractor._symbol_cache.get.return_value = None
    mock_tree = MagicMock()
    mock_parser.parse_file.return_value = mock_tree
    mock_parser.detect_language.return_value = "typescript"
    ts_symbols = [make_symbol("tsFunc")]
    extractor._ts_extractor.extract_typescript_symbols.return_value = ts_symbols
    with patch("scripts.utils.symbol_extractor.os.path.getmtime", return_value=123.0):
        with patch("scripts.utils.symbol_extractor.Path") as mock_path_cls:
            mock_path = MagicMock()
            mock_path.resolve.return_value = "/abs/test.ts"
            mock_path_cls.return_value = mock_path
            result = extractor.extract_symbols("test.ts")
    assert result == ts_symbols
    extractor._ts_extractor.extract_typescript_symbols.assert_called_once_with(mock_tree, "test.ts")


def test_extract_symbols_routes_javascript(extractor_with_mocks):
    """JavaScript file routes to TypeScriptExtractor.extract_javascript_symbols."""
    extractor, mock_parser = extractor_with_mocks
    extractor._symbol_cache.get.return_value = None
    mock_tree = MagicMock()
    mock_parser.parse_file.return_value = mock_tree
    mock_parser.detect_language.return_value = "javascript"
    js_symbols = [make_symbol("jsFunc")]
    extractor._ts_extractor.extract_javascript_symbols.return_value = js_symbols
    with patch("scripts.utils.symbol_extractor.os.path.getmtime", return_value=123.0):
        with patch("scripts.utils.symbol_extractor.Path") as mock_path_cls:
            mock_path = MagicMock()
            mock_path.resolve.return_value = "/abs/test.js"
            mock_path_cls.return_value = mock_path
            result = extractor.extract_symbols("test.js")
    assert result == js_symbols
    extractor._ts_extractor.extract_javascript_symbols.assert_called_once_with(mock_tree, "test.js")


def test_extract_symbols_routes_tsx(extractor_with_mocks):
    """TSX file routes to TypeScriptExtractor.extract_typescript_symbols."""
    extractor, mock_parser = extractor_with_mocks
    extractor._symbol_cache.get.return_value = None
    mock_tree = MagicMock()
    mock_parser.parse_file.return_value = mock_tree
    mock_parser.detect_language.return_value = "tsx"
    tsx_symbols = [make_symbol("TsxComponent")]
    extractor._ts_extractor.extract_typescript_symbols.return_value = tsx_symbols
    with patch("scripts.utils.symbol_extractor.os.path.getmtime", return_value=123.0):
        with patch("scripts.utils.symbol_extractor.Path") as mock_path_cls:
            mock_path = MagicMock()
            mock_path.resolve.return_value = "/abs/test.tsx"
            mock_path_cls.return_value = mock_path
            result = extractor.extract_symbols("test.tsx")
    assert result == tsx_symbols


# ============================================================================
# 4. extract_symbols - Graceful degradation (4 tests)
# ============================================================================

def test_extract_symbols_file_not_found_returns_empty(extractor_with_mocks):
    """FileNotFoundError from parser returns []."""
    extractor, mock_parser = extractor_with_mocks
    extractor._symbol_cache.get.return_value = None
    mock_parser.parse_file.side_effect = FileNotFoundError("not found")
    with patch("scripts.utils.symbol_extractor.os.path.getmtime", return_value=123.0):
        with patch("scripts.utils.symbol_extractor.Path") as mock_path_cls:
            mock_path = MagicMock()
            mock_path.resolve.return_value = "/abs/missing.py"
            mock_path_cls.return_value = mock_path
            result = extractor.extract_symbols("missing.py")
    assert result == []


def test_extract_symbols_parse_error_returns_empty(extractor_with_mocks):
    """General Exception from parser returns []."""
    extractor, mock_parser = extractor_with_mocks
    extractor._symbol_cache.get.return_value = None
    mock_parser.parse_file.side_effect = RuntimeError("parse error")
    with patch("scripts.utils.symbol_extractor.os.path.getmtime", return_value=123.0):
        with patch("scripts.utils.symbol_extractor.Path") as mock_path_cls:
            mock_path = MagicMock()
            mock_path.resolve.return_value = "/abs/bad.py"
            mock_path_cls.return_value = mock_path
            result = extractor.extract_symbols("bad.py")
    assert result == []


def test_extract_symbols_none_tree_returns_empty(extractor_with_mocks):
    """parser.parse_file returns None -> returns []."""
    extractor, mock_parser = extractor_with_mocks
    extractor._symbol_cache.get.return_value = None
    mock_parser.parse_file.return_value = None
    with patch("scripts.utils.symbol_extractor.os.path.getmtime", return_value=123.0):
        with patch("scripts.utils.symbol_extractor.Path") as mock_path_cls:
            mock_path = MagicMock()
            mock_path.resolve.return_value = "/abs/test.py"
            mock_path_cls.return_value = mock_path
            result = extractor.extract_symbols("test.py")
    assert result == []


def test_extract_symbols_unsupported_language_returns_empty(extractor_with_mocks):
    """detect_language raises ValueError -> returns []."""
    extractor, mock_parser = extractor_with_mocks
    extractor._symbol_cache.get.return_value = None
    mock_tree = MagicMock()
    mock_parser.parse_file.return_value = mock_tree
    mock_parser.detect_language.side_effect = ValueError("unsupported")
    with patch("scripts.utils.symbol_extractor.os.path.getmtime", return_value=123.0):
        with patch("scripts.utils.symbol_extractor.Path") as mock_path_cls:
            mock_path = MagicMock()
            mock_path.resolve.return_value = "/abs/test.xyz"
            mock_path_cls.return_value = mock_path
            result = extractor.extract_symbols("test.xyz")
    assert result == []


def test_extract_symbols_unimplemented_language_returns_empty(extractor_with_mocks):
    """Language detected but not implemented (else branch) -> returns []."""
    extractor, mock_parser = extractor_with_mocks
    extractor._symbol_cache.get.return_value = None
    mock_tree = MagicMock()
    mock_parser.parse_file.return_value = mock_tree
    mock_parser.detect_language.return_value = "rust"
    with patch("scripts.utils.symbol_extractor.os.path.getmtime", return_value=123.0):
        with patch("scripts.utils.symbol_extractor.Path") as mock_path_cls:
            mock_path = MagicMock()
            mock_path.resolve.return_value = "/abs/test.rs"
            mock_path_cls.return_value = mock_path
            result = extractor.extract_symbols("test.rs")
    assert result == []


# ============================================================================
# 5. extract_symbols - Caching (2 tests)
# ============================================================================

def test_extract_symbols_caches_result(extractor_with_mocks):
    """Stores symbols in cache after extraction when mtime > 0."""
    extractor, mock_parser = extractor_with_mocks
    extractor._symbol_cache.get.return_value = None
    mock_tree = MagicMock()
    mock_parser.parse_file.return_value = mock_tree
    mock_parser.detect_language.return_value = "python"
    extracted = [make_symbol("func")]
    extractor._python_extractor.extract_python_symbols.return_value = extracted
    with patch("scripts.utils.symbol_extractor.os.path.getmtime", return_value=456.0):
        with patch("scripts.utils.symbol_extractor.Path") as mock_path_cls:
            mock_path = MagicMock()
            mock_path.resolve.return_value = "/abs/test.py"
            mock_path_cls.return_value = mock_path
            extractor.extract_symbols("test.py")
    extractor._symbol_cache.set.assert_called_once_with("/abs/test.py", 456.0, extracted)


def test_extract_symbols_no_cache_when_mtime_zero(extractor_with_mocks):
    """Does not cache when mtime == 0 (OSError on getmtime)."""
    extractor, mock_parser = extractor_with_mocks
    extractor._symbol_cache.get.return_value = None
    mock_tree = MagicMock()
    mock_parser.parse_file.return_value = mock_tree
    mock_parser.detect_language.return_value = "python"
    extractor._python_extractor.extract_python_symbols.return_value = [make_symbol("func")]
    with patch("scripts.utils.symbol_extractor.os.path.getmtime", side_effect=OSError):
        with patch("scripts.utils.symbol_extractor.Path") as mock_path_cls:
            mock_path = MagicMock()
            mock_path.resolve.return_value = "/abs/test.py"
            mock_path_cls.return_value = mock_path
            extractor.extract_symbols("test.py")
    extractor._symbol_cache.set.assert_not_called()


# ============================================================================
# 6. Cache management (3 tests)
# ============================================================================

def test_clear_cache_delegates(extractor_with_mocks):
    """clear_cache delegates to _symbol_cache.clear()."""
    extractor, _ = extractor_with_mocks
    extractor.clear_cache()
    extractor._symbol_cache.clear.assert_called_once()


def test_invalidate_cache_delegates(extractor_with_mocks):
    """invalidate_cache delegates to _symbol_cache.invalidate()."""
    extractor, _ = extractor_with_mocks
    extractor._symbol_cache.invalidate.return_value = True
    with patch("scripts.utils.symbol_extractor.Path") as mock_path_cls:
        mock_path = MagicMock()
        mock_path.resolve.return_value = "/abs/test.py"
        mock_path_cls.return_value = mock_path
        extractor.invalidate_cache("test.py")
    extractor._symbol_cache.invalidate.assert_called_once_with("/abs/test.py")


def test_get_cache_stats_delegates(extractor_with_mocks):
    """get_cache_stats delegates to _symbol_cache.get_stats()."""
    extractor, _ = extractor_with_mocks
    stats = {"cached_files": 5, "cached_symbols": 42}
    extractor._symbol_cache.get_stats.return_value = stats
    result = extractor.get_cache_stats()
    assert result == stats
    extractor._symbol_cache.get_stats.assert_called_once()


# ============================================================================
# 7. Simple methods (2 tests)
# ============================================================================

def test_extract_signature_returns_symbol_signature():
    """extract_signature returns symbol.signature."""
    symbol = make_symbol("func", signature="def func() -> int")
    extractor = SymbolExtractor(MagicMock())
    result = extractor.extract_signature(symbol)
    assert result == "def func() -> int"


def test_extract_references_returns_symbol_references():
    """extract_references returns symbol.references."""
    symbol = make_symbol("func", references=["other_func", "third_func"])
    extractor = SymbolExtractor(MagicMock())
    result = extractor.extract_references(symbol)
    assert result == ["other_func", "third_func"]


# ============================================================================
# 8. Backward compat delegates (2 tests)
# ============================================================================

def test_extract_python_references_delegates(extractor_with_mocks):
    """_extract_python_references delegates to _python_extractor."""
    extractor, _ = extractor_with_mocks
    mock_node = MagicMock()
    refs = ["func1", "func2"]
    extractor._python_extractor.extract_python_references.return_value = refs
    result = extractor._extract_python_references(mock_node)
    assert result == refs
    extractor._python_extractor.extract_python_references.assert_called_once_with(mock_node)


def test_extract_typescript_references_delegates(extractor_with_mocks):
    """_extract_typescript_references delegates to _ts_extractor."""
    extractor, _ = extractor_with_mocks
    mock_node = MagicMock()
    refs = ["tsFunc1", "tsFunc2"]
    extractor._ts_extractor.extract_typescript_references.return_value = refs
    result = extractor._extract_typescript_references(mock_node)
    assert result == refs
    extractor._ts_extractor.extract_typescript_references.assert_called_once_with(mock_node)


def test_extract_module_level_references_delegates(extractor_with_mocks):
    """_extract_module_level_references delegates to _python_extractor."""
    extractor, _ = extractor_with_mocks
    mock_node = MagicMock()
    refs = ["os", "sys"]
    extractor._python_extractor.extract_module_level_references.return_value = refs
    result = extractor._extract_module_level_references(mock_node)
    assert result == refs


def test_extract_ts_module_level_references_delegates(extractor_with_mocks):
    """_extract_ts_module_level_references delegates to _ts_extractor."""
    extractor, _ = extractor_with_mocks
    mock_node = MagicMock()
    refs = ["axios"]
    extractor._ts_extractor.extract_ts_module_level_references.return_value = refs
    result = extractor._extract_ts_module_level_references(mock_node)
    assert result == refs


# ============================================================================
# 9. Convenience function (1 test)
# ============================================================================

def test_module_extract_symbols_creates_parser_and_extractor():
    """Module-level extract_symbols creates parser+extractor and delegates."""
    with patch("scripts.utils.symbol_extractor.TreesitterParser") as mock_parser_cls:
        with patch("scripts.utils.symbol_extractor.SymbolExtractor") as mock_extractor_cls:
            mock_parser = MagicMock()
            mock_parser_cls.return_value = mock_parser
            mock_extractor = MagicMock()
            mock_extractor_cls.return_value = mock_extractor
            expected = [make_symbol("func")]
            mock_extractor.extract_symbols.return_value = expected
            result = extract_symbols("test.py")
    assert result == expected
    mock_parser_cls.assert_called_once()
    mock_extractor_cls.assert_called_once_with(mock_parser)
    mock_extractor.extract_symbols.assert_called_once_with("test.py")
