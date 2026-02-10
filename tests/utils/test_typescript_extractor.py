"""Tests for TypeScript/JavaScript symbol extractor.

Tests for scripts.utils.typescript_extractor.TypeScriptExtractor.
Covers 4 main methods:
- extract_typescript_references (function calls, inheritance, type annotations)
- extract_ts_module_level_references (imports)
- extract_typescript_symbols (function, class, interface, type alias)
- extract_javascript_symbols (function, class)

Author: Cervella Tester
Date: 2026-02-10
"""

from unittest.mock import MagicMock

import pytest

from scripts.utils.typescript_extractor import TypeScriptExtractor
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


# 1. extract_typescript_references - Function calls (4 tests)

def test_extract_typescript_references_simple_call():
    """Simple function call: myFunc() -> ['myFunc']"""
    extractor = TypeScriptExtractor()

    func_id = make_node("identifier", text="myFunc")
    call_expr = make_node("call_expression", fields={"function": func_id})
    root = make_node("program", children=[call_expr])

    result = extractor.extract_typescript_references(root)
    assert result == ["myFunc"]


def test_extract_typescript_references_builtin_call_filtered():
    """Builtin function call filtered: console.log() - console is builtin"""
    extractor = TypeScriptExtractor()

    # console is a builtin, should be filtered
    console_id = make_node("identifier", text="console")
    call_expr = make_node("call_expression", fields={"function": console_id})
    root = make_node("program", children=[call_expr])

    result = extractor.extract_typescript_references(root)
    assert result == []


def test_extract_typescript_references_method_call():
    """Method call: obj.method() -> extract both object and method"""
    extractor = TypeScriptExtractor()

    obj_id = make_node("identifier", text="myObj")
    method_id = make_node("property_identifier", text="doSomething")
    member_expr = make_node(
        "member_expression",
        fields={"object": obj_id, "property": method_id}
    )
    call_expr = make_node("call_expression", fields={"function": member_expr})
    root = make_node("program", children=[call_expr])

    result = extractor.extract_typescript_references(root)
    assert sorted(result) == ["doSomething", "myObj"]


def test_extract_typescript_references_method_with_builtin_object():
    """Method with builtin object: this.method() -> only method extracted"""
    extractor = TypeScriptExtractor()

    # 'this' is a builtin, should be filtered
    this_id = make_node("identifier", text="this")
    method_id = make_node("property_identifier", text="myMethod")
    member_expr = make_node(
        "member_expression",
        fields={"object": this_id, "property": method_id}
    )
    call_expr = make_node("call_expression", fields={"function": member_expr})
    root = make_node("program", children=[call_expr])

    result = extractor.extract_typescript_references(root)
    assert result == ["myMethod"]


# 2. extract_typescript_references - Class inheritance (2 tests)

def test_extract_typescript_references_class_extends():
    """Class inheritance: class Child extends Parent -> ['Parent']"""
    extractor = TypeScriptExtractor()

    parent_id = make_node("identifier", text="BaseClass")
    extends_clause = make_node("extends_clause", children=[parent_id])
    class_heritage = make_node("class_heritage", children=[extends_clause])
    class_decl = make_node("class_declaration", children=[class_heritage])
    root = make_node("program", children=[class_decl])

    result = extractor.extract_typescript_references(root)
    assert result == ["BaseClass"]


def test_extract_typescript_references_class_extends_qualified():
    """Qualified parent: class A extends module.B -> ['B']"""
    extractor = TypeScriptExtractor()

    prop_id = make_node("property_identifier", text="MyClass")
    member_expr = make_node("member_expression", fields={"property": prop_id})
    extends_clause = make_node("extends_clause", children=[member_expr])
    class_heritage = make_node("class_heritage", children=[extends_clause])
    class_decl = make_node("class_declaration", children=[class_heritage])
    root = make_node("program", children=[class_decl])

    result = extractor.extract_typescript_references(root)
    assert result == ["MyClass"]


# 3. extract_typescript_references - Type annotations (3 tests)

def test_extract_typescript_references_simple_type():
    """Simple type annotation: param: MyType -> ['MyType']"""
    extractor = TypeScriptExtractor()

    type_id = make_node("type_identifier", text="CustomType")
    type_ann = make_node("type_annotation", children=[type_id])
    root = make_node("program", children=[type_ann])

    result = extractor.extract_typescript_references(root)
    assert result == ["CustomType"]


def test_extract_typescript_references_generic_type():
    """Generic type: Array<MyType> -> ['Array', 'MyType']"""
    extractor = TypeScriptExtractor()

    container_id = make_node("type_identifier", text="Container")
    arg_id = make_node("type_identifier", text="MyData")
    type_args = make_node("type_arguments", children=[arg_id])
    generic_type = make_node(
        "generic_type",
        fields={"name": container_id, "type_arguments": type_args}
    )
    type_ann = make_node("type_annotation", children=[generic_type])
    root = make_node("program", children=[type_ann])

    result = extractor.extract_typescript_references(root)
    assert sorted(result) == ["Container", "MyData"]


def test_extract_typescript_references_standalone_type_identifier():
    """Standalone type_identifier node -> extracts name (non-builtin only)"""
    extractor = TypeScriptExtractor()

    type_id = make_node("type_identifier", text="MyCustomType")
    root = make_node("program", children=[type_id])
    result = extractor.extract_typescript_references(root)
    assert result == ["MyCustomType"]


# 4. extract_ts_module_level_references (4 tests)

def test_extract_ts_module_level_references_default_import():
    """Default import: import axios from 'axios' -> ['axios']"""
    extractor = TypeScriptExtractor()

    name_id = make_node("identifier", text="axios")
    import_clause = make_node("import_clause", children=[name_id])
    import_stmt = make_node("import_statement", children=[import_clause])
    root = make_node("program", children=[import_stmt])

    result = extractor.extract_ts_module_level_references(root)
    assert result == ["axios"]


def test_extract_ts_module_level_references_named_imports():
    """Named imports: import { Router, Request } from 'express' -> ['Router']"""
    extractor = TypeScriptExtractor()

    # Request is builtin, Router is not
    router_spec = make_node(
        "import_specifier",
        fields={"name": make_node("identifier", text="Router")}
    )
    request_spec = make_node(
        "import_specifier",
        fields={"name": make_node("identifier", text="Request")}
    )
    named_imports = make_node("named_imports", children=[router_spec, request_spec])
    import_clause = make_node("import_clause", children=[named_imports])
    import_stmt = make_node("import_statement", children=[import_clause])
    root = make_node("program", children=[import_stmt])

    result = extractor.extract_ts_module_level_references(root)
    assert result == ["Router"]


def test_extract_ts_module_level_references_namespace_import():
    """Namespace import: import * as lib from 'lib' -> ['lib']"""
    extractor = TypeScriptExtractor()

    lib_id = make_node("identifier", text="myLib")
    namespace_import = make_node("namespace_import", children=[lib_id])
    import_clause = make_node("import_clause", children=[namespace_import])
    import_stmt = make_node("import_statement", children=[import_clause])
    root = make_node("program", children=[import_stmt])

    result = extractor.extract_ts_module_level_references(root)
    assert result == ["myLib"]


def test_extract_ts_module_level_references_import_specifier_no_name():
    """Import specifier without name field -> fallback to children"""
    extractor = TypeScriptExtractor()

    child_id = make_node("identifier", text="MyService")
    import_spec = make_node("import_specifier", children=[child_id])
    named_imports = make_node("named_imports", children=[import_spec])
    import_clause = make_node("import_clause", children=[named_imports])
    import_stmt = make_node("import_statement", children=[import_clause])
    root = make_node("program", children=[import_stmt])

    result = extractor.extract_ts_module_level_references(root)
    assert result == ["MyService"]


# 5. extract_typescript_symbols (4 tests)

def test_extract_typescript_symbols_function():
    """TypeScript function: name, type='function', signature"""
    extractor = TypeScriptExtractor()

    name_node = make_node("identifier", text="calculateSum")
    params_node = make_node("parameters", text="(a, b)")
    func_decl = make_node(
        "function_declaration",
        fields={"name": name_node, "parameters": params_node},
        children=[]
    )

    tree = MagicMock()
    tree.root_node = make_node("program", children=[func_decl])

    result = extractor.extract_typescript_symbols(tree, "test.ts")

    assert len(result) == 1
    assert result[0].name == "calculateSum"
    assert result[0].type == "function"
    assert result[0].signature == "function calculateSum(a, b)"
    assert result[0].file == "test.ts"
    assert result[0].line == 1


def test_extract_typescript_symbols_class_with_heritage():
    """TypeScript class with heritage: signature includes extends"""
    extractor = TypeScriptExtractor()

    name_node = make_node("identifier", text="MyComponent")
    heritage_node = make_node("class_heritage", text="extends Base")
    class_decl = make_node(
        "class_declaration",
        fields={"name": name_node},
        children=[heritage_node]
    )

    tree = MagicMock()
    tree.root_node = make_node("program", children=[class_decl])

    result = extractor.extract_typescript_symbols(tree, "test.tsx")

    assert len(result) == 1
    assert result[0].name == "MyComponent"
    assert result[0].type == "class"
    assert result[0].signature == "class MyComponent extends Base"




def test_extract_typescript_symbols_interface():
    """TypeScript interface: signature with body"""
    extractor = TypeScriptExtractor()

    name_node = make_node("identifier", text="User")
    body_node = make_node("interface_body", text="{ id: number }")
    interface_decl = make_node(
        "interface_declaration",
        fields={"name": name_node, "body": body_node}
    )

    tree = MagicMock()
    tree.root_node = make_node("program", children=[interface_decl])

    result = extractor.extract_typescript_symbols(tree, "types.ts")

    assert len(result) == 1
    assert result[0].name == "User"
    assert result[0].type == "interface"
    assert result[0].signature == "interface User { id: number }"




def test_extract_typescript_symbols_interface_long_body():
    """Interface with body > 100 chars truncated to '{ ... }'."""
    extractor = TypeScriptExtractor()
    name_node = make_node("identifier", text="BigInterface")
    long_body = "{ " + "; ".join(f"field{i}: string" for i in range(20)) + " }"
    body_node = make_node("interface_body", text=long_body)
    interface_decl = make_node(
        "interface_declaration",
        fields={"name": name_node, "body": body_node}
    )
    tree = MagicMock()
    tree.root_node = make_node("program", children=[interface_decl])
    result = extractor.extract_typescript_symbols(tree, "types.ts")
    assert result[0].signature == "interface BigInterface { ... }"


def test_extract_typescript_symbols_no_name_node():
    """Node without name field is skipped (guard clause)."""
    extractor = TypeScriptExtractor()
    func_decl = make_node("function_declaration", fields={"name": None})
    tree = MagicMock()
    tree.root_node = make_node("program", children=[func_decl])
    result = extractor.extract_typescript_symbols(tree, "test.ts")
    assert result == []


def test_extract_typescript_references_class_without_declaration():
    """node.type == 'class' (not 'class_declaration') also extracts inheritance."""
    extractor = TypeScriptExtractor()
    base_id = make_node("identifier", text="Parent")
    extends_clause = make_node("extends_clause", children=[base_id])
    heritage = make_node("class_heritage", children=[extends_clause])
    class_node = make_node("class", children=[heritage])
    refs = extractor.extract_typescript_references(class_node)
    assert refs == ["Parent"]


def test_extract_typescript_symbols_type_alias():
    """TypeScript type alias: signature is 'type Name = ...'"""
    extractor = TypeScriptExtractor()

    name_node = make_node("identifier", text="Status")
    type_alias = make_node("type_alias_declaration", fields={"name": name_node})

    tree = MagicMock()
    tree.root_node = make_node("program", children=[type_alias])

    result = extractor.extract_typescript_symbols(tree, "enums.ts")

    assert len(result) == 1
    assert result[0].name == "Status"
    assert result[0].type == "type"
    assert result[0].signature == "type Status = ..."


# 6. extract_javascript_symbols (4 tests)

def test_extract_javascript_symbols_function():
    """JavaScript function: same structure as TypeScript"""
    extractor = TypeScriptExtractor()

    name_node = make_node("identifier", text="initApp")
    params_node = make_node("parameters", text="(config)")
    func_decl = make_node(
        "function_declaration",
        fields={"name": name_node, "parameters": params_node},
        children=[]
    )

    tree = MagicMock()
    tree.root_node = make_node("program", children=[func_decl])

    result = extractor.extract_javascript_symbols(tree, "app.js")

    assert len(result) == 1
    assert result[0].name == "initApp"
    assert result[0].type == "function"
    assert result[0].signature == "function initApp(config)"


def test_extract_javascript_symbols_class_with_heritage():
    """JavaScript class with extends"""
    extractor = TypeScriptExtractor()

    name_node = make_node("identifier", text="CustomError")
    heritage_node = make_node("class_heritage", text="extends Error")
    class_decl = make_node(
        "class_declaration",
        fields={"name": name_node},
        children=[heritage_node]
    )

    tree = MagicMock()
    tree.root_node = make_node("program", children=[class_decl])

    result = extractor.extract_javascript_symbols(tree, "errors.js")

    assert len(result) == 1
    assert result[0].name == "CustomError"
    assert result[0].type == "class"
    assert result[0].signature == "class CustomError extends Error"


def test_extract_javascript_symbols_class_no_heritage():
    """JavaScript class without extends"""
    extractor = TypeScriptExtractor()

    name_node = make_node("identifier", text="Controller")
    class_decl = make_node(
        "class_declaration",
        fields={"name": name_node},
        children=[]
    )

    tree = MagicMock()
    tree.root_node = make_node("program", children=[class_decl])

    result = extractor.extract_javascript_symbols(tree, "controller.js")

    assert len(result) == 1
    assert result[0].name == "Controller"
    assert result[0].type == "class"
    assert result[0].signature == "class Controller"


# 7. Integration tests (2 tests)

def test_typescript_symbols_combine_body_and_module_refs():
    """Symbol references = body refs + module imports (sorted)"""
    extractor = TypeScriptExtractor()

    # Import statement: import axios from 'axios'
    axios_id = make_node("identifier", text="axios")
    import_clause = make_node("import_clause", children=[axios_id])
    import_stmt = make_node("import_statement", children=[import_clause])

    # Function that calls 'validate'
    validate_id = make_node("identifier", text="validate")
    call_expr = make_node("call_expression", fields={"function": validate_id})
    func_name = make_node("identifier", text="processData")
    func_params = make_node("parameters", text="(data)")
    func_decl = make_node(
        "function_declaration",
        fields={"name": func_name, "parameters": func_params},
        children=[call_expr]
    )

    tree = MagicMock()
    tree.root_node = make_node("program", children=[import_stmt, func_decl])

    result = extractor.extract_typescript_symbols(tree, "service.ts")

    assert len(result) == 1
    sym = result[0]
    # Should have both 'axios' (module import) and 'validate' (body ref)
    assert sorted(sym.references) == ["axios", "validate"]


def test_references_sorted():
    """References in symbols are sorted"""
    extractor = TypeScriptExtractor()

    # Function with two calls: zzz(), aaa()
    zzz_call = make_node("call_expression", fields={"function": make_node("identifier", text="zzz")})
    aaa_call = make_node("call_expression", fields={"function": make_node("identifier", text="aaa")})
    func_name = make_node("identifier", text="test")
    func_decl = make_node(
        "function_declaration",
        fields={"name": func_name},
        children=[zzz_call, aaa_call]
    )

    tree = MagicMock()
    tree.root_node = make_node("program", children=[func_decl])

    result = extractor.extract_typescript_symbols(tree, "utils.ts")

    assert len(result) == 1
    assert result[0].references == ["aaa", "zzz"]
