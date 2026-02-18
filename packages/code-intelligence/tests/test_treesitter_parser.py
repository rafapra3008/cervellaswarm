"""Tests for cervellaswarm_code_intelligence/treesitter_parser.py.

Author: Cervella Tester | Version: 1.0.0 | Date: 2026-02-10
"""

import logging
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch, mock_open
import pytest
from cervellaswarm_code_intelligence.treesitter_parser import TreesitterParser, parse_file


# FIXTURES

@pytest.fixture
def parser():
    return TreesitterParser()

@pytest.fixture
def mock_tree():
    tree = MagicMock()
    tree.root_node.has_error = False
    tree.root_node.type = "module"
    tree.root_node.child_count = 3
    tree.root_node.children = []
    tree.root_node.start_point = (0, 0)
    return tree

@pytest.fixture
def mock_tree_with_errors():
    tree = MagicMock()
    tree.root_node.has_error = True
    tree.root_node.type = "ERROR"
    return tree

@pytest.fixture
def mock_language():
    lang = MagicMock()
    lang.name = "python"
    return lang

@pytest.fixture
def mock_parser_obj():
    return MagicMock()


# INITIALIZATION TESTS (2)

def test_init_empty_caches(parser):
    assert parser.parsers == {}
    assert parser.trees == {}
    assert parser.languages == {}

def test_init_logger_configured(caplog):
    with caplog.at_level(logging.DEBUG):
        TreesitterParser()
    assert "TreesitterParser initialized" in caplog.text


# DETECT_LANGUAGE TESTS (7)

def test_detect_language_python(parser):
    assert parser.detect_language("app.py") == "python"

def test_detect_language_typescript(parser):
    assert parser.detect_language("app.ts") == "typescript"

def test_detect_language_tsx(parser):
    assert parser.detect_language("component.tsx") == "tsx"

def test_detect_language_javascript(parser):
    assert parser.detect_language("script.js") == "javascript"

def test_detect_language_jsx(parser):
    assert parser.detect_language("component.jsx") == "jsx"

def test_detect_language_unsupported_raises(parser):
    with pytest.raises(ValueError) as exc:
        parser.detect_language("App.java")
    assert "Unsupported file extension: .java" in str(exc.value)

def test_detect_language_case_insensitive(parser):
    assert parser.detect_language("APP.PY") == "python"
    assert parser.detect_language("Script.JS") == "javascript"


# GET_LANGUAGE TESTS (4)

@patch("cervellaswarm_code_intelligence.treesitter_parser.get_language")
def test_get_language_creates_on_first_call(mock_get_lang, parser, mock_language):
    mock_get_lang.return_value = mock_language
    result = parser.get_language("python")
    assert result == mock_language
    mock_get_lang.assert_called_once_with("python")
    assert "python" in parser.languages

@patch("cervellaswarm_code_intelligence.treesitter_parser.get_language")
def test_get_language_returns_cached(mock_get_lang, parser, mock_language):
    mock_get_lang.return_value = mock_language
    result1 = parser.get_language("python")
    result2 = parser.get_language("python")
    assert result1 == result2 == mock_language
    mock_get_lang.assert_called_once()

@patch("cervellaswarm_code_intelligence.treesitter_parser.get_language")
def test_get_language_returns_none_on_exception(mock_get_lang, parser):
    mock_get_lang.side_effect = RuntimeError("Language not found")
    assert parser.get_language("python") is None

@patch("cervellaswarm_code_intelligence.treesitter_parser.get_language")
def test_get_language_cache_populated_after_success(mock_get_lang, parser, mock_language):
    mock_get_lang.return_value = mock_language
    parser.get_language("python")
    assert parser.languages["python"] == mock_language
    assert len(parser.languages) == 1


# GET_PARSER TESTS (5)

@patch("cervellaswarm_code_intelligence.treesitter_parser.Parser")
@patch("cervellaswarm_code_intelligence.treesitter_parser.get_language")
def test_get_parser_creates_on_first_call(mock_get_lang, mock_parser_cls, parser, mock_language, mock_parser_obj):
    mock_get_lang.return_value = mock_language
    mock_parser_cls.return_value = mock_parser_obj
    result = parser.get_parser("python")
    assert result == mock_parser_obj
    mock_parser_cls.assert_called_once_with(mock_language)
    assert "python" in parser.parsers

@patch("cervellaswarm_code_intelligence.treesitter_parser.Parser")
@patch("cervellaswarm_code_intelligence.treesitter_parser.get_language")
def test_get_parser_returns_cached(mock_get_lang, mock_parser_cls, parser, mock_language, mock_parser_obj):
    mock_get_lang.return_value = mock_language
    mock_parser_cls.return_value = mock_parser_obj
    result1 = parser.get_parser("python")
    result2 = parser.get_parser("python")
    assert result1 == result2
    mock_parser_cls.assert_called_once()

@patch("cervellaswarm_code_intelligence.treesitter_parser.get_language")
def test_get_parser_returns_none_when_language_fails(mock_get_lang, parser):
    mock_get_lang.side_effect = RuntimeError("Language error")
    assert parser.get_parser("python") is None

@patch("cervellaswarm_code_intelligence.treesitter_parser.get_language")
def test_get_parser_returns_none_when_get_language_returns_none(mock_get_lang, parser):
    mock_get_lang.return_value = None
    parser.get_language = Mock(return_value=None)
    assert parser.get_parser("python") is None

@patch("cervellaswarm_code_intelligence.treesitter_parser.Parser")
@patch("cervellaswarm_code_intelligence.treesitter_parser.get_language")
def test_get_parser_returns_none_on_parser_exception(mock_get_lang, mock_parser_cls, parser, mock_language):
    mock_get_lang.return_value = mock_language
    mock_parser_cls.side_effect = RuntimeError("Parser creation failed")
    assert parser.get_parser("python") is None

@patch("cervellaswarm_code_intelligence.treesitter_parser.Parser")
@patch("cervellaswarm_code_intelligence.treesitter_parser.get_language")
def test_get_parser_cache_populated_after_success(mock_get_lang, mock_parser_cls, parser, mock_language, mock_parser_obj):
    mock_get_lang.return_value = mock_language
    mock_parser_cls.return_value = mock_parser_obj
    parser.get_parser("python")
    assert parser.parsers["python"] == mock_parser_obj
    assert len(parser.parsers) == 1


# PARSE_FILE TESTS (10)

@patch("cervellaswarm_code_intelligence.treesitter_parser.Parser")
@patch("cervellaswarm_code_intelligence.treesitter_parser.get_language")
def test_parse_file_success(mock_get_lang, mock_parser_cls, parser, mock_language, mock_parser_obj, mock_tree, tmp_path):
    mock_get_lang.return_value = mock_language
    mock_parser_cls.return_value = mock_parser_obj
    mock_parser_obj.parse.return_value = mock_tree
    test_file = tmp_path / "test.py"
    test_file.write_text("def foo(): pass")
    result = parser.parse_file(str(test_file))
    assert result == mock_tree
    assert result.root_node.has_error is False
    mock_parser_obj.parse.assert_called_once()

def test_parse_file_missing_file_raises(parser):
    with pytest.raises(FileNotFoundError) as exc:
        parser.parse_file("/nonexistent/file.py")
    assert "File not found" in str(exc.value)

def test_parse_file_unsupported_language_returns_none(parser, tmp_path):
    test_file = tmp_path / "test.java"
    test_file.write_text("class Test {}")
    assert parser.parse_file(str(test_file)) is None

@patch("cervellaswarm_code_intelligence.treesitter_parser.Parser")
@patch("cervellaswarm_code_intelligence.treesitter_parser.get_language")
def test_parse_file_returns_cached_tree(mock_get_lang, mock_parser_cls, parser, mock_language, mock_parser_obj, mock_tree, tmp_path):
    mock_get_lang.return_value = mock_language
    mock_parser_cls.return_value = mock_parser_obj
    mock_parser_obj.parse.return_value = mock_tree
    test_file = tmp_path / "test.py"
    test_file.write_text("def foo(): pass")
    result1 = parser.parse_file(str(test_file))
    result2 = parser.parse_file(str(test_file))
    assert result1 == result2
    mock_parser_obj.parse.assert_called_once()

@patch("cervellaswarm_code_intelligence.treesitter_parser.Parser")
@patch("cervellaswarm_code_intelligence.treesitter_parser.get_language")
def test_parse_file_logs_warning_for_parse_errors(mock_get_lang, mock_parser_cls, parser, mock_language, mock_parser_obj, mock_tree_with_errors, tmp_path, caplog):
    mock_get_lang.return_value = mock_language
    mock_parser_cls.return_value = mock_parser_obj
    mock_parser_obj.parse.return_value = mock_tree_with_errors
    test_file = tmp_path / "test.py"
    test_file.write_text("def foo(: pass")
    with caplog.at_level(logging.WARNING):
        result = parser.parse_file(str(test_file))
    assert result == mock_tree_with_errors
    assert "Parse errors found" in caplog.text

@patch("cervellaswarm_code_intelligence.treesitter_parser.Parser")
@patch("cervellaswarm_code_intelligence.treesitter_parser.get_language")
def test_parse_file_returns_none_on_read_exception(mock_get_lang, mock_parser_cls, parser, mock_language, mock_parser_obj):
    mock_get_lang.return_value = mock_language
    mock_parser_cls.return_value = mock_parser_obj
    with patch.object(Path, "exists", return_value=True):
        with patch("builtins.open", mock_open()) as m:
            m.side_effect = IOError("Permission denied")
            assert parser.parse_file("/tmp/test.py") is None

@patch("cervellaswarm_code_intelligence.treesitter_parser.get_language")
def test_parse_file_returns_none_when_get_parser_fails(mock_get_lang, parser, tmp_path):
    mock_get_lang.side_effect = RuntimeError("Language not found")
    test_file = tmp_path / "test.py"
    test_file.write_text("def foo(): pass")
    assert parser.parse_file(str(test_file)) is None

@patch("cervellaswarm_code_intelligence.treesitter_parser.Parser")
@patch("cervellaswarm_code_intelligence.treesitter_parser.get_language")
def test_parse_file_uses_resolved_path_as_cache_key(mock_get_lang, mock_parser_cls, parser, mock_language, mock_parser_obj, mock_tree, tmp_path):
    mock_get_lang.return_value = mock_language
    mock_parser_cls.return_value = mock_parser_obj
    mock_parser_obj.parse.return_value = mock_tree
    test_file = tmp_path / "test.py"
    test_file.write_text("def foo(): pass")
    parser.parse_file(str(test_file))
    assert str(test_file.resolve()) in parser.trees

@patch("cervellaswarm_code_intelligence.treesitter_parser.Parser")
@patch("cervellaswarm_code_intelligence.treesitter_parser.get_language")
def test_parse_file_real_file_with_content(mock_get_lang, mock_parser_cls, parser, mock_language, mock_parser_obj, mock_tree, tmp_path):
    mock_get_lang.return_value = mock_language
    mock_parser_cls.return_value = mock_parser_obj
    mock_parser_obj.parse.return_value = mock_tree
    test_file = tmp_path / "app.py"
    test_file.write_text('def hello(name: str) -> str:\n    return f"Hello, {name}!"\n')
    result = parser.parse_file(str(test_file))
    assert result == mock_tree
    call_args = mock_parser_obj.parse.call_args
    assert b"def hello" in call_args[0][0]


# CACHE MANAGEMENT TESTS (5)

@patch("cervellaswarm_code_intelligence.treesitter_parser.Parser")
@patch("cervellaswarm_code_intelligence.treesitter_parser.get_language")
def test_clear_cache_clears_trees_not_parsers(mock_get_lang, mock_parser_cls, parser, mock_language, mock_parser_obj, mock_tree, tmp_path):
    mock_get_lang.return_value = mock_language
    mock_parser_cls.return_value = mock_parser_obj
    mock_parser_obj.parse.return_value = mock_tree
    test_file = tmp_path / "test.py"
    test_file.write_text("def foo(): pass")
    parser.parse_file(str(test_file))
    assert len(parser.trees) == 1
    assert len(parser.parsers) == 1
    assert len(parser.languages) == 1
    parser.clear_cache()
    assert len(parser.trees) == 0
    assert len(parser.parsers) == 1
    assert len(parser.languages) == 1

@patch("cervellaswarm_code_intelligence.treesitter_parser.Parser")
@patch("cervellaswarm_code_intelligence.treesitter_parser.get_language")
def test_invalidate_file_removes_specific_entry(mock_get_lang, mock_parser_cls, parser, mock_language, mock_parser_obj, mock_tree, tmp_path):
    mock_get_lang.return_value = mock_language
    mock_parser_cls.return_value = mock_parser_obj
    mock_parser_obj.parse.return_value = mock_tree
    file1 = tmp_path / "test1.py"
    file2 = tmp_path / "test2.py"
    file1.write_text("def foo(): pass")
    file2.write_text("def bar(): pass")
    parser.parse_file(str(file1))
    parser.parse_file(str(file2))
    assert len(parser.trees) == 2
    parser.invalidate_file(str(file1))
    assert len(parser.trees) == 1
    assert str(file2.resolve()) in parser.trees
    assert str(file1.resolve()) not in parser.trees

def test_invalidate_file_non_cached_does_nothing(parser):
    parser.invalidate_file("/nonexistent/file.py")
    assert len(parser.trees) == 0

@patch("cervellaswarm_code_intelligence.treesitter_parser.Parser")
@patch("cervellaswarm_code_intelligence.treesitter_parser.get_language")
def test_get_cache_stats_returns_correct_counts(mock_get_lang, mock_parser_cls, parser, mock_language, mock_parser_obj, mock_tree, tmp_path):
    mock_get_lang.return_value = mock_language
    mock_parser_cls.return_value = mock_parser_obj
    mock_parser_obj.parse.return_value = mock_tree
    file1 = tmp_path / "test1.py"
    file2 = tmp_path / "test2.py"
    file1.write_text("def foo(): pass")
    file2.write_text("def bar(): pass")
    parser.parse_file(str(file1))
    parser.parse_file(str(file2))
    stats = parser.get_cache_stats()
    assert stats == {'parsers': 1, 'trees': 2, 'languages': 1}

def test_get_cache_stats_empty_on_init(parser):
    stats = parser.get_cache_stats()
    assert stats == {'parsers': 0, 'trees': 0, 'languages': 0}


# CONVENIENCE FUNCTION TESTS (2)

@patch("cervellaswarm_code_intelligence.treesitter_parser.TreesitterParser")
def test_module_parse_file_creates_parser_and_delegates(mock_parser_cls):
    mock_parser_instance = Mock()
    mock_parser_cls.return_value = mock_parser_instance
    mock_parser_instance.parse_file.return_value = "mock_tree"
    result = parse_file("/path/to/file.py")
    assert result == "mock_tree"
    mock_parser_cls.assert_called_once()
    mock_parser_instance.parse_file.assert_called_once_with("/path/to/file.py")

@patch("cervellaswarm_code_intelligence.treesitter_parser.TreesitterParser")
def test_module_parse_file_returns_none_on_failure(mock_parser_cls):
    mock_parser_instance = Mock()
    mock_parser_cls.return_value = mock_parser_instance
    mock_parser_instance.parse_file.return_value = None
    assert parse_file("/path/to/file.py") is None
