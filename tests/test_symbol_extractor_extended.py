"""Unit tests for SymbolExtractor (EXTENDED).

Edge cases, methods, convenience function, real files, TS references.

Split da test_symbol_extractor.py (662 righe > 500 limite).
Sessione 348.
"""

import pytest
import tempfile
from pathlib import Path

from scripts.utils.symbol_extractor import (
    SymbolExtractor,
    Symbol,
    extract_symbols,
)
from scripts.utils.treesitter_parser import TreesitterParser


@pytest.fixture
def parser():
    """Create a TreesitterParser instance."""
    return TreesitterParser()


@pytest.fixture
def extractor(parser):
    """Create a SymbolExtractor instance."""
    return SymbolExtractor(parser)


class TestEdgeCases:
    """Test suite for edge cases and error handling."""

    def test_empty_file(self, extractor):
        """Test extracting symbols from empty file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write("")
            empty_file = f.name

        try:
            symbols = extractor.extract_symbols(empty_file)
            assert len(symbols) == 0
        finally:
            Path(empty_file).unlink()

    def test_file_with_no_symbols(self, extractor):
        """Test file with code but no extractable symbols."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write("""
# Just a comment
x = 42
print(x)
""")
            no_symbols_file = f.name

        try:
            symbols = extractor.extract_symbols(no_symbols_file)
            assert len(symbols) == 0
        finally:
            Path(no_symbols_file).unlink()

    def test_malformed_code(self, extractor):
        """Test extracting from malformed code."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write("""
def incomplete_function(
    # Missing closing parenthesis
""")
            broken_file = f.name

        try:
            symbols = extractor.extract_symbols(broken_file)
            assert isinstance(symbols, list)
        finally:
            Path(broken_file).unlink()

    def test_unsupported_language(self, extractor):
        """Test file with unsupported extension."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.xyz', delete=False) as f:
            f.write("some content")
            unsupported_file = f.name

        try:
            symbols = extractor.extract_symbols(unsupported_file)
            assert len(symbols) == 0
        finally:
            Path(unsupported_file).unlink()

    def test_file_not_found(self, extractor):
        """Test graceful degradation for non-existent file."""
        result = extractor.extract_symbols("/nonexistent/file.py")
        assert result == []

    def test_nested_classes_and_functions(self, extractor):
        """Test extracting nested symbols."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write("""
class Outer:
    def inner_method(self):
        pass

    class Inner:
        def nested_method(self):
            pass
""")
            nested_file = f.name

        try:
            symbols = extractor.extract_symbols(nested_file)
            assert len(symbols) >= 1
            names = [s.name for s in symbols]
            assert "Outer" in names
        finally:
            Path(nested_file).unlink()


class TestSymbolMethods:
    """Test suite for Symbol class and extractor methods."""

    def test_symbol_repr(self):
        """Test Symbol __repr__ method."""
        symbol = Symbol(
            name="test_func",
            type="function",
            file="test.py",
            line=10,
            signature="def test_func()"
        )
        repr_str = repr(symbol)
        assert "Symbol" in repr_str
        assert "test_func" in repr_str
        assert "test.py:10" in repr_str

    def test_extract_signature(self, extractor):
        """Test extract_signature method."""
        symbol = Symbol(
            name="test",
            type="function",
            file="test.py",
            line=1,
            signature="def test(x: int) -> bool"
        )
        signature = extractor.extract_signature(symbol)
        assert signature == "def test(x: int) -> bool"

    def test_extract_references(self, extractor):
        """Test extract_references method."""
        symbol = Symbol(
            name="test",
            type="function",
            file="test.py",
            line=1,
            signature="def test()"
        )
        refs = extractor.extract_references(symbol, None)
        assert isinstance(refs, list)
        assert len(refs) == 0


class TestConvenienceFunction:
    """Test suite for convenience extract_symbols function."""

    def test_convenience_function(self):
        """Test standalone extract_symbols function."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write("""
def convenience_test():
    pass
""")
            py_file = f.name

        try:
            symbols = extract_symbols(py_file)
            assert len(symbols) == 1
            assert symbols[0].name == "convenience_test"
        finally:
            Path(py_file).unlink()


class TestRealFiles:
    """Test suite using actual project files."""

    def test_extract_from_symbol_extractor(self, extractor):
        """Test extracting symbols from symbol_extractor.py itself."""
        project_root = Path(__file__).parent.parent
        file_path = project_root / "scripts" / "utils" / "symbol_extractor.py"

        symbols = extractor.extract_symbols(str(file_path))

        assert len(symbols) > 0
        names = [s.name for s in symbols]
        assert "SymbolExtractor" in names
        assert "extract_symbols" in names

        types = [s.type for s in symbols]
        assert "class" in types
        assert "function" in types

    def test_extract_from_treesitter_parser(self, extractor):
        """Test extracting symbols from treesitter_parser.py."""
        project_root = Path(__file__).parent.parent
        file_path = project_root / "scripts" / "utils" / "treesitter_parser.py"

        symbols = extractor.extract_symbols(str(file_path))

        assert len(symbols) > 0
        names = [s.name for s in symbols]
        assert "TreesitterParser" in names


class TestTypeScriptReferenceExtraction:
    """Test suite for TypeScript reference extraction."""

    def test_ts_function_call_reference(self, extractor):
        """Test extracting function call references from TypeScript."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ts', delete=False) as f:
            f.write("""
function processData(data: string): void {
    const result = transformData(data);
    validateResult(result);
}
""")
            ts_file = f.name

        try:
            symbols = extractor.extract_symbols(ts_file)
            assert len(symbols) == 1
            assert symbols[0].name == "processData"
            refs = symbols[0].references
            assert "transformData" in refs
            assert "validateResult" in refs
        finally:
            Path(ts_file).unlink()

    def test_ts_import_reference(self, extractor):
        """Test extracting import references from TypeScript."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ts', delete=False) as f:
            f.write("""
import { UserService, AuthHelper } from './services';
import DataProcessor from './utils';

function handleUser(): void {
    const service = new UserService();
}
""")
            ts_file = f.name

        try:
            symbols = extractor.extract_symbols(ts_file)
            assert len(symbols) == 1
            assert symbols[0].name == "handleUser"
            refs = symbols[0].references
            assert "UserService" in refs
            assert "AuthHelper" in refs
            assert "DataProcessor" in refs
        finally:
            Path(ts_file).unlink()

    def test_ts_class_extends_reference(self, extractor):
        """Test extracting class extends references from TypeScript."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ts', delete=False) as f:
            f.write("""
import { BaseController } from './base';

class UserController extends BaseController {
    handleRequest(): void {
        this.process();
    }
}
""")
            ts_file = f.name

        try:
            symbols = extractor.extract_symbols(ts_file)
            class_symbols = [s for s in symbols if s.type == "class"]
            assert len(class_symbols) == 1
            assert class_symbols[0].name == "UserController"
            refs = class_symbols[0].references
            assert "BaseController" in refs
        finally:
            Path(ts_file).unlink()

    def test_ts_type_annotation_reference(self, extractor):
        """Test extracting type annotation references from TypeScript."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ts', delete=False) as f:
            f.write("""
import { UserData, ConfigOptions } from './types';

function processUser(user: UserData, config: ConfigOptions): ProcessResult {
    return new ProcessResult();
}
""")
            ts_file = f.name

        try:
            symbols = extractor.extract_symbols(ts_file)
            assert len(symbols) == 1
            assert symbols[0].name == "processUser"
            refs = symbols[0].references
            assert "UserData" in refs
            assert "ConfigOptions" in refs
            assert "ProcessResult" in refs
        finally:
            Path(ts_file).unlink()

    def test_ts_builtin_filtered(self, extractor):
        """Test that TypeScript builtins are filtered out."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ts', delete=False) as f:
            f.write("""
function logData(data: string): void {
    console.log(data);
    const arr = new Array<number>();
    const promise = new Promise(() => {});
    customFunction(data);
}
""")
            ts_file = f.name

        try:
            symbols = extractor.extract_symbols(ts_file)
            assert len(symbols) == 1
            refs = symbols[0].references
            assert "console" not in refs
            assert "Array" not in refs
            assert "Promise" not in refs
            assert "customFunction" in refs
        finally:
            Path(ts_file).unlink()

    def test_ts_method_call_reference(self, extractor):
        """Test extracting method call references from TypeScript."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ts', delete=False) as f:
            f.write("""
import { apiClient } from './api';

function fetchData(): void {
    apiClient.get('/users');
    apiClient.post('/data', {});
}
""")
            ts_file = f.name

        try:
            symbols = extractor.extract_symbols(ts_file)
            assert len(symbols) == 1
            refs = symbols[0].references
            assert "apiClient" in refs
            assert "get" in refs
            assert "post" in refs
        finally:
            Path(ts_file).unlink()
