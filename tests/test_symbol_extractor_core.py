"""Unit tests for SymbolExtractor (CORE).

Python, TypeScript, JavaScript extraction.

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


class TestPythonSymbolExtraction:
    """Test suite for Python symbol extraction."""

    def test_extract_python_function(self, extractor):
        """Test extracting a Python function."""
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
            assert len(symbols) >= 2
            names = [s.name for s in symbols]
            assert "Component" in names
            assert "ClassComponent" in names
        finally:
            Path(jsx_file).unlink()
