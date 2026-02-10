"""Tests for scripts/utils/python_extractor.py.

Tests PythonExtractor for symbol/reference extraction from tree-sitter AST.
Covers: calls, imports, inheritance, annotations, decorators, functions, classes.

Author: Cervella Tester (S342)
Date: 2026-02-10
"""
from unittest.mock import MagicMock
from scripts.utils.python_extractor import PythonExtractor
from scripts.utils.symbol_types import Symbol


def make_node(type_name, text=None, children=None, fields=None, parent=None):
    """Create mock tree-sitter node."""
    node = MagicMock()
    node.type = type_name
    node.text = text.encode() if isinstance(text, str) else text
    node.children = children or []
    node.child_count = len(node.children)
    node.parent = parent
    node.start_point = (0, 0)
    node.child_by_field_name = lambda name: (fields or {}).get(name)
    node.child = lambda i: node.children[i] if 0 <= i < len(node.children) else None
    return node


# 1. extract_python_references - Function calls
def test_extract_references_simple_call():
    """foo() -> ["foo"]."""
    ext = PythonExtractor()
    func_id = make_node("identifier", text="foo")
    call_node = make_node("call", fields={"function": func_id})
    assert ext.extract_python_references(call_node) == ["foo"]


def test_extract_references_builtin_call_filtered():
    """print() -> [] (builtin filtered)."""
    ext = PythonExtractor()
    func_id = make_node("identifier", text="print")
    call_node = make_node("call", fields={"function": func_id})
    assert ext.extract_python_references(call_node) == []


def test_extract_references_method_call():
    """obj.method() -> ["method", "obj"]."""
    ext = PythonExtractor()
    obj_id = make_node("identifier", text="obj")
    method_id = make_node("identifier", text="method")
    attr_node = make_node("attribute", fields={"object": obj_id, "attribute": method_id})
    call_node = make_node("call", fields={"function": attr_node})
    assert ext.extract_python_references(call_node) == ["method", "obj"]


def test_extract_references_method_call_builtin_object():
    """self.method() -> ["method"] (self filtered)."""
    ext = PythonExtractor()
    self_id = make_node("identifier", text="self")
    method_id = make_node("identifier", text="method")
    attr_node = make_node("attribute", fields={"object": self_id, "attribute": method_id})
    call_node = make_node("call", fields={"function": attr_node})
    assert ext.extract_python_references(call_node) == ["method"]


# 2. extract_python_references - Imports
def test_extract_references_import_from():
    """from fastapi import Router -> ["Router", "fastapi"]."""
    ext = PythonExtractor()
    module_node = make_node("dotted_name", text="fastapi")
    imported_node = make_node("dotted_name", text="Router")
    import_stmt = make_node("import_from_statement", children=[module_node, imported_node],
                            fields={"module_name": module_node})
    assert ext.extract_python_references(import_stmt) == ["Router", "fastapi"]


def test_extract_references_import_statement():
    """import os -> ["os"]."""
    ext = PythonExtractor()
    dotted = make_node("dotted_name", text="os")
    import_stmt = make_node("import_statement", children=[dotted])
    assert ext.extract_python_references(import_stmt) == ["os"]


def test_extract_references_import_dotted():
    """import os.path -> ["os"]."""
    ext = PythonExtractor()
    dotted = make_node("dotted_name", text="os.path")
    import_stmt = make_node("import_statement", children=[dotted])
    assert ext.extract_python_references(import_stmt) == ["os"]


def test_extract_references_aliased_import():
    """from X import Y as Z -> extracts Y."""
    ext = PythonExtractor()
    module_node = make_node("dotted_name", text="module")
    name_node = make_node("dotted_name", text="MyClass")
    aliased = make_node("aliased_import", fields={"name": name_node})
    import_stmt = make_node("import_from_statement", children=[module_node, aliased],
                            fields={"module_name": module_node})
    refs = ext.extract_python_references(import_stmt)
    assert "MyClass" in refs and "module" in refs


def test_extract_references_import_statement_aliased():
    """import os as myos -> ["os"] via extract_python_references."""
    ext = PythonExtractor()
    name_node = make_node("dotted_name", text="os")
    aliased = make_node("aliased_import", fields={"name": name_node})
    import_stmt = make_node("import_statement", children=[aliased])
    assert ext.extract_python_references(import_stmt) == ["os"]


# 3. extract_python_references - Inheritance
def test_extract_references_inheritance():
    """class A(B) -> ["B"]."""
    ext = PythonExtractor()
    base_id = make_node("identifier", text="B")
    bases_node = make_node("argument_list", children=[base_id])
    class_node = make_node("class_definition", fields={"superclasses": bases_node})
    assert ext.extract_python_references(class_node) == ["B"]


def test_extract_references_inheritance_qualified():
    """class A(module.ClassName) -> ["ClassName"]."""
    ext = PythonExtractor()
    attr_id = make_node("identifier", text="ClassName")
    attr_node = make_node("attribute", fields={"attribute": attr_id})
    bases_node = make_node("argument_list", children=[attr_node])
    class_node = make_node("class_definition", fields={"superclasses": bases_node})
    assert ext.extract_python_references(class_node) == ["ClassName"]


# 4. extract_python_references - Type annotations
def test_extract_references_simple_type():
    """x: MyType -> ["MyType"]."""
    ext = PythonExtractor()
    type_id = make_node("identifier", text="MyType")
    type_node = make_node("type", children=[type_id])
    assert ext.extract_python_references(type_node) == ["MyType"]


def test_extract_references_generic_type():
    """x: List[MyType] -> ["MyType"] (List builtin filtered)."""
    ext = PythonExtractor()
    list_id = make_node("identifier", text="List")
    mytype_id = make_node("identifier", text="MyType")
    inner_type = make_node("type", children=[mytype_id])
    type_args = make_node("type_arguments", children=[inner_type])
    generic = make_node("generic_type", fields={"type": list_id, "type_arguments": type_args})
    type_node = make_node("type", children=[generic])
    assert ext.extract_python_references(type_node) == ["MyType"]


def test_extract_references_builtin_type_filtered():
    """x: str -> [] (str builtin filtered)."""
    ext = PythonExtractor()
    type_id = make_node("identifier", text="str")
    type_node = make_node("type", children=[type_id])
    assert ext.extract_python_references(type_node) == []


def test_extract_references_nonbuiltin_generic_type():
    """MyContainer[MyType] -> ["MyContainer", "MyType"] (non-builtin generic base)."""
    ext = PythonExtractor()
    container_id = make_node("identifier", text="MyContainer")
    mytype_id = make_node("identifier", text="MyType")
    inner_type = make_node("type", children=[mytype_id])
    type_args = make_node("type_arguments", children=[inner_type])
    generic = make_node("generic_type", fields={"type": container_id, "type_arguments": type_args})
    type_node = make_node("type", children=[generic])
    refs = ext.extract_python_references(type_node)
    assert "MyContainer" in refs and "MyType" in refs


# 5. extract_python_references - Decorators
def test_extract_references_decorator():
    """@my_decorator -> ["my_decorator"]."""
    ext = PythonExtractor()
    dec_id = make_node("identifier", text="my_decorator")
    decorator = make_node("decorator", children=[dec_id])
    assert ext.extract_python_references(decorator) == ["my_decorator"]


def test_extract_references_decorator_call():
    """@decorator_call() -> ["decorator_call"]."""
    ext = PythonExtractor()
    func_id = make_node("identifier", text="decorator_call")
    call_node = make_node("call", fields={"function": func_id})
    decorator = make_node("decorator", children=[call_node])
    assert ext.extract_python_references(decorator) == ["decorator_call"]


def test_extract_references_decorator_attribute():
    """@module.decorator -> ["decorator"]."""
    ext = PythonExtractor()
    attr_id = make_node("identifier", text="decorator")
    attr_node = make_node("attribute", fields={"attribute": attr_id})
    decorator = make_node("decorator", children=[attr_node])
    assert ext.extract_python_references(decorator) == ["decorator"]


# 6. extract_python_references - Builtins filtering & sorting
def test_extract_references_builtins_filtered():
    """PYTHON_BUILTINS filtered out."""
    ext = PythonExtractor()
    len_id = make_node("identifier", text="len")
    len_call = make_node("call", fields={"function": len_id})
    my_id = make_node("identifier", text="my_func")
    my_call = make_node("call", fields={"function": my_id})
    root = make_node("module", children=[len_call, my_call])
    refs = ext.extract_python_references(root)
    assert "len" not in refs and "my_func" in refs


def test_extract_references_sorted_output():
    """Results are sorted."""
    ext = PythonExtractor()
    zebra_call = make_node("call", fields={"function": make_node("identifier", text="zebra")})
    apple_call = make_node("call", fields={"function": make_node("identifier", text="apple")})
    banana_call = make_node("call", fields={"function": make_node("identifier", text="banana")})
    root = make_node("module", children=[zebra_call, apple_call, banana_call])
    assert ext.extract_python_references(root) == ["apple", "banana", "zebra"]


# 7. extract_module_level_references
def test_extract_module_level_import():
    """import os -> ["os"]."""
    ext = PythonExtractor()
    dotted = make_node("dotted_name", text="os")
    import_stmt = make_node("import_statement", children=[dotted])
    root = make_node("module", children=[import_stmt])
    assert ext.extract_module_level_references(root) == ["os"]


def test_extract_module_level_from_import():
    """from fastapi import Router -> ["Router", "fastapi"]."""
    ext = PythonExtractor()
    module_node = make_node("dotted_name", text="fastapi")
    imported_node = make_node("dotted_name", text="Router")
    import_stmt = make_node("import_from_statement", children=[module_node, imported_node],
                            fields={"module_name": module_node})
    root = make_node("module", children=[import_stmt])
    refs = ext.extract_module_level_references(root)
    assert "fastapi" in refs and "Router" in refs


def test_extract_module_level_aliased():
    """import os as aliased -> ["os"]."""
    ext = PythonExtractor()
    name_node = make_node("dotted_name", text="os")
    aliased = make_node("aliased_import", fields={"name": name_node})
    import_stmt = make_node("import_statement", children=[aliased])
    root = make_node("module", children=[import_stmt])
    assert ext.extract_module_level_references(root) == ["os"]


def test_extract_module_level_relative_import_filtered():
    """from . import something -> [] (relative filtered)."""
    ext = PythonExtractor()
    module_node = make_node("dotted_name", text=".something")
    import_stmt = make_node("import_from_statement", fields={"module_name": module_node})
    root = make_node("module", children=[import_stmt])
    assert ext.extract_module_level_references(root) == []


def test_extract_module_level_from_aliased():
    """from X import Y as Z -> extracts Y via module level."""
    ext = PythonExtractor()
    module_node = make_node("dotted_name", text="fastapi")
    name_node = make_node("dotted_name", text="Router")
    aliased = make_node("aliased_import", fields={"name": name_node})
    import_stmt = make_node("import_from_statement", children=[aliased],
                            fields={"module_name": module_node})
    root = make_node("module", children=[import_stmt])
    refs = ext.extract_module_level_references(root)
    assert "Router" in refs and "fastapi" in refs


# 8. extract_python_symbols - Functions
def test_extract_symbols_simple_function():
    """Simple function: name, type, signature, line."""
    ext = PythonExtractor()
    name_node = make_node("identifier", text="hello")
    name_node.start_point = (5, 0)  # line 6
    params_node = make_node("parameters", text="()")
    body_node = make_node("block", children=[])
    func_node = make_node("function_definition",
                          fields={"name": name_node, "parameters": params_node, "body": body_node})
    func_node.parent = None
    root = make_node("module", children=[func_node])
    tree = MagicMock()
    tree.root_node = root
    symbols = ext.extract_python_symbols(tree, "/test/file.py")
    assert len(symbols) == 1
    sym = symbols[0]
    assert sym.name == "hello" and sym.type == "function"
    assert sym.signature == "def hello()" and sym.line == 6


def test_extract_symbols_function_with_return_type():
    """def foo() -> str signature includes return type."""
    ext = PythonExtractor()
    name_node = make_node("identifier", text="foo")
    name_node.start_point = (0, 0)
    params_node = make_node("parameters", text="()")
    return_node = make_node("type", text="str")
    body_node = make_node("block", children=[])
    func_node = make_node("function_definition",
                          fields={"name": name_node, "parameters": params_node,
                                  "return_type": return_node, "body": body_node})
    func_node.parent = None
    root = make_node("module", children=[func_node])
    tree = MagicMock()
    tree.root_node = root
    symbols = ext.extract_python_symbols(tree, "/test/file.py")
    assert symbols[0].signature == "def foo() -> str"


def test_extract_symbols_function_with_docstring():
    """Function with docstring extracts it."""
    ext = PythonExtractor()
    name_node = make_node("identifier", text="greet")
    name_node.start_point = (0, 0)
    params_node = make_node("parameters", text="()")
    string_node = make_node("string", text='"""Say hello."""')
    expr_stmt = make_node("expression_statement")
    expr_stmt.child = lambda i: string_node if i == 0 else None
    colon = make_node(":", text=":")
    body_node = make_node("block", children=[colon, expr_stmt])
    func_node = make_node("function_definition",
                          fields={"name": name_node, "parameters": params_node, "body": body_node})
    func_node.parent = None
    root = make_node("module", children=[func_node])
    tree = MagicMock()
    tree.root_node = root
    symbols = ext.extract_python_symbols(tree, "/test/file.py")
    assert symbols[0].docstring == "Say hello."


def test_extract_symbols_function_without_docstring():
    """Function without docstring has empty docstring."""
    ext = PythonExtractor()
    name_node = make_node("identifier", text="simple")
    name_node.start_point = (0, 0)
    params_node = make_node("parameters", text="()")
    colon = make_node(":", text=":")
    pass_stmt = make_node("pass_statement")
    body_node = make_node("block", children=[colon, pass_stmt])
    func_node = make_node("function_definition",
                          fields={"name": name_node, "parameters": params_node, "body": body_node})
    func_node.parent = None
    root = make_node("module", children=[func_node])
    tree = MagicMock()
    tree.root_node = root
    symbols = ext.extract_python_symbols(tree, "/test/file.py")
    assert symbols[0].docstring == ""


# 9. extract_python_symbols - Classes
def test_extract_symbols_simple_class():
    """Simple class: name, type, signature, line."""
    ext = PythonExtractor()
    name_node = make_node("identifier", text="MyClass")
    name_node.start_point = (10, 0)  # line 11
    body_node = make_node("block", children=[])
    class_node = make_node("class_definition", fields={"name": name_node, "body": body_node})
    class_node.parent = None
    root = make_node("module", children=[class_node])
    tree = MagicMock()
    tree.root_node = root
    symbols = ext.extract_python_symbols(tree, "/test/file.py")
    assert len(symbols) == 1
    sym = symbols[0]
    assert sym.name == "MyClass" and sym.type == "class"
    assert sym.signature == "class MyClass" and sym.line == 11


def test_extract_symbols_class_with_bases():
    """class A(B) signature includes bases."""
    ext = PythonExtractor()
    name_node = make_node("identifier", text="A")
    name_node.start_point = (0, 0)
    bases_node = make_node("argument_list", text="(B)")
    body_node = make_node("block", children=[])
    class_node = make_node("class_definition",
                           fields={"name": name_node, "superclasses": bases_node, "body": body_node})
    class_node.parent = None
    root = make_node("module", children=[class_node])
    tree = MagicMock()
    tree.root_node = root
    symbols = ext.extract_python_symbols(tree, "/test/file.py")
    assert symbols[0].signature == "class A(B)"


def test_extract_symbols_class_with_docstring():
    """Class with docstring extracts it."""
    ext = PythonExtractor()
    name_node = make_node("identifier", text="MyClass")
    name_node.start_point = (0, 0)
    string_node = make_node("string", text='"""A test class."""')
    expr_stmt = make_node("expression_statement")
    expr_stmt.child = lambda i: string_node if i == 0 else None
    colon = make_node(":", text=":")
    body_node = make_node("block", children=[colon, expr_stmt])
    class_node = make_node("class_definition", fields={"name": name_node, "body": body_node})
    class_node.parent = None
    root = make_node("module", children=[class_node])
    tree = MagicMock()
    tree.root_node = root
    symbols = ext.extract_python_symbols(tree, "/test/file.py")
    assert symbols[0].docstring == "A test class."


# 10. extract_python_symbols - References integration
def test_extract_symbols_function_with_references():
    """Function symbol has refs from body + module imports + decorators."""
    ext = PythonExtractor()
    module_node = make_node("dotted_name", text="fastapi")
    imported_node = make_node("dotted_name", text="Router")
    import_stmt = make_node("import_from_statement", children=[module_node, imported_node],
                            fields={"module_name": module_node})
    dec_id = make_node("identifier", text="my_decorator")
    decorator = make_node("decorator", children=[dec_id])
    name_node = make_node("identifier", text="my_func")
    name_node.start_point = (5, 0)
    params_node = make_node("parameters", text="()")
    helper_id = make_node("identifier", text="helper")
    helper_call = make_node("call", children=[helper_id], fields={"function": helper_id})
    expr_stmt = make_node("expression_statement", children=[helper_call])
    colon = make_node(":", text=":")
    body_node = make_node("block", children=[colon, expr_stmt])
    func_node = make_node("function_definition", children=[name_node, params_node, body_node],
                          fields={"name": name_node, "parameters": params_node, "body": body_node})
    decorated = make_node("decorated_definition", children=[decorator, func_node])
    func_node.parent = decorated
    root = make_node("module", children=[import_stmt, decorated])
    tree = MagicMock()
    tree.root_node = root
    symbols = ext.extract_python_symbols(tree, "/test/file.py")
    sym = symbols[0]
    assert all(x in sym.references for x in ["Router", "fastapi", "helper", "my_decorator"])
    assert sym.references == sorted(sym.references)


def test_extract_symbols_decorated_call():
    """Function with @decorator() in decorated_definition."""
    ext = PythonExtractor()
    func_id = make_node("identifier", text="app_route")
    call_node = make_node("call", fields={"function": func_id})
    decorator = make_node("decorator", children=[call_node])
    name_node = make_node("identifier", text="handler")
    name_node.start_point = (3, 0)
    params_node = make_node("parameters", text="()")
    body_node = make_node("block", children=[])
    func_node = make_node("function_definition", children=[name_node, params_node, body_node],
                          fields={"name": name_node, "parameters": params_node, "body": body_node})
    decorated = make_node("decorated_definition", children=[decorator, func_node])
    func_node.parent = decorated
    root = make_node("module", children=[decorated])
    tree = MagicMock()
    tree.root_node = root
    symbols = ext.extract_python_symbols(tree, "/test/file.py")
    assert "app_route" in symbols[0].references


def test_extract_symbols_decorated_attribute():
    """Function with @module.deco in decorated_definition."""
    ext = PythonExtractor()
    attr_id = make_node("identifier", text="route")
    attr_node = make_node("attribute", fields={"attribute": attr_id})
    decorator = make_node("decorator", children=[attr_node])
    name_node = make_node("identifier", text="handler")
    name_node.start_point = (3, 0)
    params_node = make_node("parameters", text="()")
    body_node = make_node("block", children=[])
    func_node = make_node("function_definition", children=[name_node, params_node, body_node],
                          fields={"name": name_node, "parameters": params_node, "body": body_node})
    decorated = make_node("decorated_definition", children=[decorator, func_node])
    func_node.parent = decorated
    root = make_node("module", children=[decorated])
    tree = MagicMock()
    tree.root_node = root
    symbols = ext.extract_python_symbols(tree, "/test/file.py")
    assert "route" in symbols[0].references


def test_extract_symbols_empty_tree():
    """Empty tree returns empty list."""
    ext = PythonExtractor()
    root = make_node("module", children=[])
    tree = MagicMock()
    tree.root_node = root
    assert ext.extract_python_symbols(tree, "/test/file.py") == []
