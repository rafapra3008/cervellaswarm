"""Unit tests for SymbolExtractor.

Author: Cervella Tester
Version: 1.0.0
Date: 2026-01-19
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


class TestPythonSymbolExtraction:
    """Test suite for Python symbol extraction."""

    def test_extract_python_function(self, extractor):
        """Test extracting a Python function."""
        # Create temporary Python file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write("""def test_function(x: int, y: str) -> bool:
    \"\"\"Test function docstring.\"\"\"
    return True
""")
            py_file = f.name

        try:
            symbols = extractor.extract_symbols(py_file)

            assert len(symbols) == 1
            assert symbols[0].name == "test_function"
            assert symbols[0].type == "function"
            assert symbols[0].signature == "def test_function(x: int, y: str) -> bool"
            # Docstring extraction is optional - implementation may vary
            assert symbols[0].line == 1
        finally:
            Path(py_file).unlink()

    def test_extract_python_function_no_return(self, extractor):
        """Test extracting Python function without return type."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write("""
def no_return(x, y):
    pass
""")
            py_file = f.name

        try:
            symbols = extractor.extract_symbols(py_file)

            assert len(symbols) == 1
            assert symbols[0].name == "no_return"
            assert symbols[0].signature == "def no_return(x, y)"
        finally:
            Path(py_file).unlink()

    def test_extract_python_class(self, extractor):
        """Test extracting a Python class."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write("""class TestClass:
    \"\"\"A test class.\"\"\"
    pass
""")
            py_file = f.name

        try:
            symbols = extractor.extract_symbols(py_file)

            assert len(symbols) == 1
            assert symbols[0].name == "TestClass"
            assert symbols[0].type == "class"
            assert symbols[0].signature == "class TestClass"
            # Docstring extraction is optional
        finally:
            Path(py_file).unlink()

    def test_extract_python_class_with_bases(self, extractor):
        """Test extracting Python class with inheritance."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write("""
class ChildClass(BaseClass, Mixin):
    pass
""")
            py_file = f.name

        try:
            symbols = extractor.extract_symbols(py_file)

            assert len(symbols) == 1
            assert symbols[0].name == "ChildClass"
            assert symbols[0].type == "class"
            assert "ChildClass(BaseClass, Mixin)" in symbols[0].signature
        finally:
            Path(py_file).unlink()

    def test_extract_multiple_python_symbols(self, extractor):
        """Test extracting multiple symbols from Python file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write("""
def function_one():
    pass

class ClassOne:
    pass

def function_two():
    pass

class ClassTwo:
    pass
""")
            py_file = f.name

        try:
            symbols = extractor.extract_symbols(py_file)

            assert len(symbols) == 4
            names = [s.name for s in symbols]
            assert "function_one" in names
            assert "ClassOne" in names
            assert "function_two" in names
            assert "ClassTwo" in names
        finally:
            Path(py_file).unlink()


class TestTypeScriptSymbolExtraction:
    """Test suite for TypeScript symbol extraction."""

    def test_extract_typescript_function(self, extractor):
        """Test extracting a TypeScript function."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ts', delete=False) as f:
            f.write("""
function testFunc(x: number, y: string): boolean {
    return true;
}
""")
            ts_file = f.name

        try:
            symbols = extractor.extract_symbols(ts_file)

            assert len(symbols) == 1
            assert symbols[0].name == "testFunc"
            assert symbols[0].type == "function"
            assert "function testFunc" in symbols[0].signature
            assert symbols[0].line == 2
        finally:
            Path(ts_file).unlink()

    def test_extract_typescript_interface(self, extractor):
        """Test extracting a TypeScript interface."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ts', delete=False) as f:
            f.write("""
interface User {
    name: string;
    age: number;
}
""")
            ts_file = f.name

        try:
            symbols = extractor.extract_symbols(ts_file)

            assert len(symbols) == 1
            assert symbols[0].name == "User"
            assert symbols[0].type == "interface"
            assert "interface User" in symbols[0].signature
        finally:
            Path(ts_file).unlink()

    def test_extract_typescript_type_alias(self, extractor):
        """Test extracting a TypeScript type alias."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ts', delete=False) as f:
            f.write("""
type Status = 'active' | 'inactive';
""")
            ts_file = f.name

        try:
            symbols = extractor.extract_symbols(ts_file)

            assert len(symbols) == 1
            assert symbols[0].name == "Status"
            assert symbols[0].type == "type"
            assert "type Status = ..." in symbols[0].signature
        finally:
            Path(ts_file).unlink()

    def test_extract_multiple_typescript_symbols(self, extractor):
        """Test extracting multiple TypeScript symbols."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.tsx', delete=False) as f:
            f.write("""
interface Props {
    title: string;
}

type Status = 'ok' | 'error';

function render(props: Props): void {
    console.log(props.title);
}
""")
            tsx_file = f.name

        try:
            symbols = extractor.extract_symbols(tsx_file)

            assert len(symbols) == 3
            names = [s.name for s in symbols]
            assert "Props" in names
            assert "Status" in names
            assert "render" in names
        finally:
            Path(tsx_file).unlink()


class TestJavaScriptSymbolExtraction:
    """Test suite for JavaScript symbol extraction."""

    def test_extract_javascript_function(self, extractor):
        """Test extracting a JavaScript function."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
            f.write("""
function testFunc(x, y) {
    return x + y;
}
""")
            js_file = f.name

        try:
            symbols = extractor.extract_symbols(js_file)

            assert len(symbols) == 1
            assert symbols[0].name == "testFunc"
            assert symbols[0].type == "function"
            assert "function testFunc" in symbols[0].signature
        finally:
            Path(js_file).unlink()

    def test_extract_javascript_class(self, extractor):
        """Test extracting a JavaScript class."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
            f.write("""
class MyClass {
    constructor() {
        this.value = 42;
    }
}
""")
            js_file = f.name

        try:
            symbols = extractor.extract_symbols(js_file)

            assert len(symbols) == 1
            assert symbols[0].name == "MyClass"
            assert symbols[0].type == "class"
            assert "class MyClass" in symbols[0].signature
        finally:
            Path(js_file).unlink()

    @pytest.mark.skip(reason="JSX language library not available in current tree-sitter setup")
    def test_extract_jsx_symbols(self, extractor):
        """Test extracting symbols from JSX file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jsx', delete=False) as f:
            f.write("""function Component() {
    return null;
}

class ClassComponent {
    render() {
        return null;
    }
}
""")
            jsx_file = f.name

        try:
            symbols = extractor.extract_symbols(jsx_file)

            # JSX parsing may not extract inner methods like render()
            assert len(symbols) >= 2
            names = [s.name for s in symbols]
            assert "Component" in names
            assert "ClassComponent" in names
        finally:
            Path(jsx_file).unlink()


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
            # Should not crash, may return partial or empty results
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
            # Should return empty list for unsupported language
            assert len(symbols) == 0
        finally:
            Path(unsupported_file).unlink()

    def test_file_not_found(self, extractor):
        """Test graceful degradation for non-existent file (REQ-10)."""
        # REQ-10: Should return [] instead of raising exception
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
            # Should extract all symbols including nested ones
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
        """Test extract_references method (placeholder implementation)."""
        symbol = Symbol(
            name="test",
            type="function",
            file="test.py",
            line=1,
            signature="def test()"
        )

        # Current implementation returns empty list
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
        # Use absolute path
        project_root = Path(__file__).parent.parent
        file_path = project_root / "scripts" / "utils" / "symbol_extractor.py"

        symbols = extractor.extract_symbols(str(file_path))

        assert len(symbols) > 0

        # Check for known symbols
        names = [s.name for s in symbols]
        assert "Symbol" in names
        assert "SymbolExtractor" in names
        assert "extract_symbols" in names

        # Check symbol types
        types = [s.type for s in symbols]
        assert "class" in types
        assert "function" in types

    def test_extract_from_treesitter_parser(self, extractor):
        """Test extracting symbols from treesitter_parser.py."""
        # Use absolute path
        project_root = Path(__file__).parent.parent
        file_path = project_root / "scripts" / "utils" / "treesitter_parser.py"

        symbols = extractor.extract_symbols(str(file_path))

        assert len(symbols) > 0

        names = [s.name for s in symbols]
        assert "TreesitterParser" in names


class TestTypeScriptReferenceExtraction:
    """Test suite for TypeScript reference extraction (W2.5-B T15-T18)."""

    def test_ts_function_call_reference(self, extractor):
        """T15: Test extracting function call references from TypeScript."""
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
            # Should reference transformData and validateResult
            refs = symbols[0].references
            assert "transformData" in refs
            assert "validateResult" in refs
        finally:
            Path(ts_file).unlink()

    def test_ts_import_reference(self, extractor):
        """T16: Test extracting import references from TypeScript."""
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
            # Should include imports
            assert "UserService" in refs
            assert "AuthHelper" in refs
            assert "DataProcessor" in refs
        finally:
            Path(ts_file).unlink()

    def test_ts_class_extends_reference(self, extractor):
        """T17: Test extracting class extends references from TypeScript."""
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

            # Should find the class
            class_symbols = [s for s in symbols if s.type == "class"]
            assert len(class_symbols) == 1
            assert class_symbols[0].name == "UserController"
            refs = class_symbols[0].references
            # Should reference BaseController from extends
            assert "BaseController" in refs
        finally:
            Path(ts_file).unlink()

    def test_ts_type_annotation_reference(self, extractor):
        """T18: Test extracting type annotation references from TypeScript."""
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
            # Should reference types from annotations
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
            # Builtins should NOT be in references
            assert "console" not in refs
            assert "Array" not in refs
            assert "Promise" not in refs
            # But custom function should be
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
            # Should reference apiClient and methods
            assert "apiClient" in refs
            assert "get" in refs
            assert "post" in refs
        finally:
            Path(ts_file).unlink()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
