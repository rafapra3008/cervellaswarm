# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for _compiler.py (C2.2.2 core + C2.2.3 types + C2.3.1-C2.3.2).

Test structure:
  - _expr_to_python: all 8 Expr types + edge cases
  - _type_to_python: SimpleType, GenericType, optional, unknown
  - _compile_use: with/without alias
  - _loc_comment: format verification
  - _safe_ident: keyword avoidance
  - CompiledModule: frozen dataclass
  - compile(): full program with UseNode declarations
  - Error handling: verify TypeError for unknown decl types
  - _escape_contract_str: hardening with \\n, \\r, alignment with codegen (C2.3.1a)
  - CompiledModule.types: variant + record tracking (C2.3.1b)
  - Module metadata: __lu_version__, __lu_source__ (C2.3.2a)
  - __all__ generation + CompiledModule.exports (C2.3.2b)

Agent compilation tests: see test_compiler_agent.py (C2.2.4).
Protocol compilation tests: see test_compiler_protocol.py (C2.2.5).
"""

from __future__ import annotations

import pytest

from cervellaswarm_lingua_universale._ast import (
    AttrExpr,
    BinOpExpr,
    GenericType,
    GroupExpr,
    IdentExpr,
    Loc,
    MethodCallExpr,
    NotExpr,
    NumberExpr,
    ProgramNode,
    RecordTypeDecl,
    SimpleType,
    StringExpr,
    UseNode,
    VariantTypeDecl,
)
from cervellaswarm_lingua_universale._compiler import ASTCompiler, CompiledModule


@pytest.fixture()
def compiler() -> ASTCompiler:
    return ASTCompiler()


LOC = Loc(line=1, col=0)


# ===================================================================
# _expr_to_python
# ===================================================================


class TestExprToPython:
    """Tests for converting Expr AST nodes to Python expression strings."""

    def test_ident_expr(self, compiler: ASTCompiler) -> None:
        expr = IdentExpr("x", LOC)
        assert compiler._expr_to_python(expr) == "x"

    def test_ident_expr_multi_word(self, compiler: ASTCompiler) -> None:
        expr = IdentExpr("my_variable", LOC)
        assert compiler._expr_to_python(expr) == "my_variable"

    def test_ident_expr_keyword_escaped(self, compiler: ASTCompiler) -> None:
        """Python keyword 'class' -> 'class_'."""
        expr = IdentExpr("class", LOC)
        assert compiler._expr_to_python(expr) == "class_"

    def test_number_expr_integer(self, compiler: ASTCompiler) -> None:
        expr = NumberExpr("42", LOC)
        assert compiler._expr_to_python(expr) == "42"

    def test_number_expr_float(self, compiler: ASTCompiler) -> None:
        expr = NumberExpr("3.14", LOC)
        assert compiler._expr_to_python(expr) == "3.14"

    def test_number_expr_zero(self, compiler: ASTCompiler) -> None:
        expr = NumberExpr("0", LOC)
        assert compiler._expr_to_python(expr) == "0"

    def test_string_expr(self, compiler: ASTCompiler) -> None:
        expr = StringExpr('"hello"', LOC)
        assert compiler._expr_to_python(expr) == '"hello"'

    def test_string_expr_single_quotes(self, compiler: ASTCompiler) -> None:
        expr = StringExpr("'world'", LOC)
        assert compiler._expr_to_python(expr) == "'world'"

    def test_attr_expr(self, compiler: ASTCompiler) -> None:
        expr = AttrExpr("input", "is_valid", LOC)
        assert compiler._expr_to_python(expr) == "input.is_valid"

    def test_attr_expr_keyword_obj(self, compiler: ASTCompiler) -> None:
        """Attribute access on keyword: pass.value -> pass_.value."""
        expr = AttrExpr("pass", "value", LOC)
        assert compiler._expr_to_python(expr) == "pass_.value"

    def test_attr_expr_keyword_attr(self, compiler: ASTCompiler) -> None:
        """Keyword as attribute name: obj.class -> obj.class_."""
        expr = AttrExpr("obj", "class", LOC)
        assert compiler._expr_to_python(expr) == "obj.class_"

    def test_method_call_no_args(self, compiler: ASTCompiler) -> None:
        expr = MethodCallExpr("tests", "run", (), LOC)
        assert compiler._expr_to_python(expr) == "tests.run()"

    def test_method_call_with_args(self, compiler: ASTCompiler) -> None:
        arg1 = IdentExpr("x", LOC)
        arg2 = NumberExpr("5", LOC)
        expr = MethodCallExpr("obj", "check", (arg1, arg2), LOC)
        assert compiler._expr_to_python(expr) == "obj.check(x, 5)"

    def test_method_call_keyword_method(self, compiler: ASTCompiler) -> None:
        """Method name is a keyword: tests.pass() -> tests.pass_()."""
        expr = MethodCallExpr("tests", "pass", (), LOC)
        assert compiler._expr_to_python(expr) == "tests.pass_()"

    def test_method_call_keyword_obj(self, compiler: ASTCompiler) -> None:
        """Object name is a keyword: pass.run() -> pass_.run()."""
        expr = MethodCallExpr("pass", "run", (), LOC)
        assert compiler._expr_to_python(expr) == "pass_.run()"

    def test_string_expr_empty(self, compiler: ASTCompiler) -> None:
        """Empty string literal."""
        expr = StringExpr('""', LOC)
        assert compiler._expr_to_python(expr) == '""'

    def test_string_expr_with_escapes(self, compiler: ASTCompiler) -> None:
        """String with escape sequences (passed through raw)."""
        expr = StringExpr('"hello\\nworld"', LOC)
        assert compiler._expr_to_python(expr) == '"hello\\nworld"'

    def test_binop_and(self, compiler: ASTCompiler) -> None:
        left = IdentExpr("a", LOC)
        right = IdentExpr("b", LOC)
        expr = BinOpExpr(left, "and", right, LOC)
        assert compiler._expr_to_python(expr) == "(a) and (b)"

    def test_binop_or(self, compiler: ASTCompiler) -> None:
        left = IdentExpr("a", LOC)
        right = IdentExpr("b", LOC)
        expr = BinOpExpr(left, "or", right, LOC)
        assert compiler._expr_to_python(expr) == "(a) or (b)"

    def test_binop_comparison(self, compiler: ASTCompiler) -> None:
        left = AttrExpr("result", "quality", LOC)
        right = NumberExpr("0.8", LOC)
        expr = BinOpExpr(left, ">=", right, LOC)
        assert compiler._expr_to_python(expr) == "(result.quality) >= (0.8)"

    def test_binop_equality(self, compiler: ASTCompiler) -> None:
        left = IdentExpr("status", LOC)
        right = StringExpr('"active"', LOC)
        expr = BinOpExpr(left, "==", right, LOC)
        assert compiler._expr_to_python(expr) == '(status) == ("active")'

    def test_binop_nested(self, compiler: ASTCompiler) -> None:
        """Nested binary ops should be fully parenthesized."""
        inner = BinOpExpr(IdentExpr("a", LOC), ">", NumberExpr("0", LOC), LOC)
        outer = BinOpExpr(inner, "and", IdentExpr("b", LOC), LOC)
        result = compiler._expr_to_python(outer)
        assert result == "((a) > (0)) and (b)"

    def test_not_expr(self, compiler: ASTCompiler) -> None:
        expr = NotExpr(IdentExpr("valid", LOC), LOC)
        assert compiler._expr_to_python(expr) == "not (valid)"

    def test_not_expr_nested(self, compiler: ASTCompiler) -> None:
        inner = BinOpExpr(IdentExpr("x", LOC), ">", NumberExpr("0", LOC), LOC)
        expr = NotExpr(inner, LOC)
        assert compiler._expr_to_python(expr) == "not ((x) > (0))"

    def test_group_expr(self, compiler: ASTCompiler) -> None:
        expr = GroupExpr(IdentExpr("x", LOC), LOC)
        assert compiler._expr_to_python(expr) == "(x)"

    def test_group_expr_nested(self, compiler: ASTCompiler) -> None:
        inner = BinOpExpr(IdentExpr("a", LOC), "+", IdentExpr("b", LOC), LOC)
        expr = GroupExpr(inner, LOC)
        assert compiler._expr_to_python(expr) == "((a) + (b))"

    def test_unknown_expr_type_raises(self, compiler: ASTCompiler) -> None:
        """Passing a non-Expr type should raise TypeError."""
        with pytest.raises(TypeError, match="Unknown Expr type"):
            compiler._expr_to_python("not_an_expr")  # type: ignore[arg-type]


# ===================================================================
# _type_to_python
# ===================================================================


class TestTypeToPython:
    """Tests for converting TypeExpr AST nodes to Python type strings."""

    def test_simple_string(self, compiler: ASTCompiler) -> None:
        assert compiler._type_to_python(SimpleType("String", False, LOC)) == "str"

    def test_simple_number(self, compiler: ASTCompiler) -> None:
        assert compiler._type_to_python(SimpleType("Number", False, LOC)) == "float"

    def test_simple_boolean(self, compiler: ASTCompiler) -> None:
        assert compiler._type_to_python(SimpleType("Boolean", False, LOC)) == "bool"

    def test_simple_integer(self, compiler: ASTCompiler) -> None:
        assert compiler._type_to_python(SimpleType("Integer", False, LOC)) == "int"

    def test_simple_any(self, compiler: ASTCompiler) -> None:
        assert compiler._type_to_python(SimpleType("Any", False, LOC)) == "object"

    def test_simple_optional(self, compiler: ASTCompiler) -> None:
        assert compiler._type_to_python(SimpleType("String", True, LOC)) == "str | None"

    def test_simple_optional_number(self, compiler: ASTCompiler) -> None:
        assert compiler._type_to_python(SimpleType("Number", True, LOC)) == "float | None"

    def test_simple_unknown_passthrough(self, compiler: ASTCompiler) -> None:
        """Unknown type names are passed through as-is (user-defined types)."""
        assert compiler._type_to_python(SimpleType("TaskData", False, LOC)) == "TaskData"

    def test_simple_unknown_optional(self, compiler: ASTCompiler) -> None:
        assert compiler._type_to_python(SimpleType("TaskData", True, LOC)) == "TaskData | None"

    def test_generic_list_string(self, compiler: ASTCompiler) -> None:
        inner = SimpleType("String", False, LOC)
        assert compiler._type_to_python(GenericType("List", inner, False, LOC)) == "list[str]"

    def test_generic_list_number(self, compiler: ASTCompiler) -> None:
        inner = SimpleType("Number", False, LOC)
        assert compiler._type_to_python(GenericType("List", inner, False, LOC)) == "list[float]"

    def test_generic_map(self, compiler: ASTCompiler) -> None:
        inner = SimpleType("String", False, LOC)
        assert compiler._type_to_python(GenericType("Map", inner, False, LOC)) == "dict[str]"

    def test_generic_set(self, compiler: ASTCompiler) -> None:
        inner = SimpleType("Number", False, LOC)
        assert compiler._type_to_python(GenericType("Set", inner, False, LOC)) == "set[float]"

    def test_generic_confident(self, compiler: ASTCompiler) -> None:
        inner = SimpleType("Number", False, LOC)
        assert compiler._type_to_python(GenericType("Confident", inner, False, LOC)) == "Confident[float]"

    def test_generic_optional(self, compiler: ASTCompiler) -> None:
        inner = SimpleType("String", False, LOC)
        assert compiler._type_to_python(GenericType("List", inner, True, LOC)) == "list[str] | None"

    def test_generic_unknown_passthrough(self, compiler: ASTCompiler) -> None:
        """Unknown generic names pass through as-is."""
        inner = SimpleType("String", False, LOC)
        assert compiler._type_to_python(GenericType("Future", inner, False, LOC)) == "Future[str]"

    def test_unknown_type_expr_raises(self, compiler: ASTCompiler) -> None:
        with pytest.raises(TypeError, match="Unknown TypeExpr type"):
            compiler._type_to_python("not_a_type")  # type: ignore[arg-type]


# ===================================================================
# _compile_use
# ===================================================================


class TestCompileUse:
    """Tests for UseNode -> import statement compilation."""

    def test_simple_import(self, compiler: ASTCompiler) -> None:
        node = UseNode("math", None, Loc(3, 0))
        lines = compiler._compile_use(node)
        assert lines == ["import math  # [LU:3:0]"]

    def test_import_with_alias(self, compiler: ASTCompiler) -> None:
        node = UseNode("datetime", "dt", Loc(5, 0))
        lines = compiler._compile_use(node)
        assert lines == ["import datetime as dt  # [LU:5:0]"]

    def test_dotted_import(self, compiler: ASTCompiler) -> None:
        node = UseNode("os.path", None, Loc(1, 0))
        lines = compiler._compile_use(node)
        assert lines == ["import os.path  # [LU:1:0]"]

    def test_dotted_import_with_alias(self, compiler: ASTCompiler) -> None:
        node = UseNode("collections.abc", "abc", Loc(2, 4))
        lines = compiler._compile_use(node)
        assert lines == ["import collections.abc as abc  # [LU:2:4]"]


# ===================================================================
# _loc_comment
# ===================================================================


class TestLocComment:
    """Tests for source annotation comments."""

    def test_basic(self, compiler: ASTCompiler) -> None:
        assert compiler._loc_comment(Loc(1, 0)) == "# [LU:1:0]"

    def test_large_line(self, compiler: ASTCompiler) -> None:
        assert compiler._loc_comment(Loc(999, 42)) == "# [LU:999:42]"

    def test_zero_col(self, compiler: ASTCompiler) -> None:
        assert compiler._loc_comment(Loc(5, 0)) == "# [LU:5:0]"


# ===================================================================
# _safe_ident
# ===================================================================


class TestSafeIdent:
    """Tests for Python keyword escaping in identifiers."""

    def test_non_keyword_unchanged(self, compiler: ASTCompiler) -> None:
        assert compiler._safe_ident("hello") == "hello"

    def test_keyword_pass(self, compiler: ASTCompiler) -> None:
        assert compiler._safe_ident("pass") == "pass_"

    def test_keyword_class(self, compiler: ASTCompiler) -> None:
        assert compiler._safe_ident("class") == "class_"

    def test_keyword_return(self, compiler: ASTCompiler) -> None:
        assert compiler._safe_ident("return") == "return_"

    def test_keyword_import(self, compiler: ASTCompiler) -> None:
        assert compiler._safe_ident("import") == "import_"

    def test_soft_keyword_match(self, compiler: ASTCompiler) -> None:
        """Python 3.10+ soft keywords should also be escaped."""
        assert compiler._safe_ident("match") == "match_"

    def test_soft_keyword_case(self, compiler: ASTCompiler) -> None:
        assert compiler._safe_ident("case") == "case_"

    def test_normal_name_not_escaped(self, compiler: ASTCompiler) -> None:
        assert compiler._safe_ident("result") == "result"
        assert compiler._safe_ident("input") == "input"
        assert compiler._safe_ident("quality") == "quality"


# ===================================================================
# CompiledModule
# ===================================================================


class TestCompiledModule:
    """Tests for the CompiledModule result type."""

    def test_frozen(self) -> None:
        mod = CompiledModule(
            source_file="test.lu",
            python_source="x = 1\n",
            agents=(),
            protocols=(),
            imports=(),
        )
        with pytest.raises(AttributeError):
            mod.source_file = "other.lu"  # type: ignore[misc]

    def test_attributes(self) -> None:
        mod = CompiledModule(
            source_file="example.lu",
            python_source="import math\n",
            agents=("Worker",),
            protocols=("DelegateTask",),
            imports=("math",),
        )
        assert mod.source_file == "example.lu"
        assert mod.agents == ("Worker",)
        assert mod.protocols == ("DelegateTask",)
        assert mod.imports == ("math",)

    def test_empty_program(self) -> None:
        mod = CompiledModule(
            source_file="empty.lu",
            python_source="",
            agents=(),
            protocols=(),
            imports=(),
        )
        assert mod.agents == ()
        assert mod.protocols == ()


# ===================================================================
# compile() -- full program
# ===================================================================


class TestCompileProgram:
    """Tests for the compile() method with complete programs."""

    def test_empty_program(self, compiler: ASTCompiler) -> None:
        prog = ProgramNode((), Loc(1, 0))
        result = compiler.compile(prog, source_file="empty.lu")
        assert result.source_file == "empty.lu"
        assert result.agents == ()
        assert result.protocols == ()
        assert result.imports == ()
        assert "Auto-generated from empty.lu" in result.python_source

    def test_single_use(self, compiler: ASTCompiler) -> None:
        prog = ProgramNode(
            (UseNode("math", None, Loc(1, 0)),),
            Loc(1, 0),
        )
        result = compiler.compile(prog, source_file="test.lu")
        assert result.imports == ("math",)
        assert "import math" in result.python_source
        assert "# [LU:1:0]" in result.python_source

    def test_multiple_uses(self, compiler: ASTCompiler) -> None:
        prog = ProgramNode(
            (
                UseNode("math", None, Loc(1, 0)),
                UseNode("datetime", "dt", Loc(2, 0)),
                UseNode("os.path", None, Loc(3, 0)),
            ),
            Loc(1, 0),
        )
        result = compiler.compile(prog, source_file="multi.lu")
        assert result.imports == ("math", "datetime", "os.path")
        assert "import math" in result.python_source
        assert "import datetime as dt" in result.python_source
        assert "import os.path" in result.python_source

    def test_default_source_file(self, compiler: ASTCompiler) -> None:
        prog = ProgramNode((), Loc(1, 0))
        result = compiler.compile(prog)
        assert result.source_file == "<input>"
        assert "Auto-generated from <input>" in result.python_source

    def test_python_source_ends_with_newline(self, compiler: ASTCompiler) -> None:
        prog = ProgramNode(
            (UseNode("math", None, Loc(1, 0)),),
            Loc(1, 0),
        )
        result = compiler.compile(prog, source_file="test.lu")
        assert result.python_source.endswith("\n")

    def test_generated_code_is_valid_python(self, compiler: ASTCompiler) -> None:
        """The generated Python source must be syntactically valid."""
        prog = ProgramNode(
            (
                UseNode("math", None, Loc(1, 0)),
                UseNode("datetime", "dt", Loc(2, 0)),
            ),
            Loc(1, 0),
        )
        result = compiler.compile(prog, source_file="valid.lu")
        # compile() as Python builtin -- validates syntax
        compile(result.python_source, "valid.lu", "exec")


# ===================================================================
# _compile_variant_type (C2.2.3)
# ===================================================================


class TestCompileVariantType:
    """Tests for VariantTypeDecl -> Literal type alias."""

    def test_two_variants(self, compiler: ASTCompiler) -> None:
        node = VariantTypeDecl("Status", ("Active", "Inactive"), Loc(5, 0))
        lines = compiler._compile_variant_type(node)
        assert lines == ['Status = Literal["Active", "Inactive"]  # [LU:5:0]']

    def test_three_variants(self, compiler: ASTCompiler) -> None:
        node = VariantTypeDecl("Priority", ("High", "Medium", "Low"), Loc(1, 0))
        lines = compiler._compile_variant_type(node)
        assert lines == ['Priority = Literal["High", "Medium", "Low"]  # [LU:1:0]']

    def test_registers_literal_import(self, compiler: ASTCompiler) -> None:
        node = VariantTypeDecl("Status", ("A", "B"), LOC)
        compiler._compile_variant_type(node)
        assert "from typing import Literal" in compiler._preamble_imports

    def test_via_dispatch(self, compiler: ASTCompiler) -> None:
        node = VariantTypeDecl("Color", ("Red", "Blue"), Loc(3, 0))
        lines = compiler._compile_declaration(node)
        assert 'Color = Literal["Red", "Blue"]' in lines[0]

    def test_in_full_program(self, compiler: ASTCompiler) -> None:
        prog = ProgramNode(
            (VariantTypeDecl("Status", ("Active", "Inactive"), Loc(1, 0)),),
            Loc(1, 0),
        )
        result = compiler.compile(prog, source_file="types.lu")
        assert "from typing import Literal" in result.python_source
        assert 'Status = Literal["Active", "Inactive"]' in result.python_source

    def test_generated_code_is_valid_python(self, compiler: ASTCompiler) -> None:
        prog = ProgramNode(
            (VariantTypeDecl("Status", ("Active", "Inactive"), LOC),),
            LOC,
        )
        result = compiler.compile(prog, source_file="test.lu")
        compile(result.python_source, "test.lu", "exec")


# ===================================================================
# _compile_record_type (C2.2.3)
# ===================================================================


class TestCompileRecordType:
    """Tests for RecordTypeDecl -> @dataclass(frozen=True) class."""

    def test_single_field(self, compiler: ASTCompiler) -> None:
        from cervellaswarm_lingua_universale._ast import FieldNode
        field = FieldNode("name", SimpleType("String", False, LOC), Loc(3, 4))
        node = RecordTypeDecl("Person", (field,), Loc(2, 0))
        lines = compiler._compile_record_type(node)
        assert lines[0] == "@dataclass(frozen=True)  # [LU:2:0]"
        assert lines[1] == "class Person:"
        assert "name: str  # [LU:3:4]" in lines[3]

    def test_multiple_fields(self, compiler: ASTCompiler) -> None:
        from cervellaswarm_lingua_universale._ast import FieldNode
        fields = (
            FieldNode("name", SimpleType("String", False, LOC), Loc(3, 4)),
            FieldNode("priority", SimpleType("Number", False, LOC), Loc(4, 4)),
            FieldNode("active", SimpleType("Boolean", False, LOC), Loc(5, 4)),
        )
        node = RecordTypeDecl("Task", fields, Loc(2, 0))
        lines = compiler._compile_record_type(node)
        assert len(lines) == 6  # decorator + class + docstring + 3 fields
        assert "name: str" in lines[3]
        assert "priority: float" in lines[4]
        assert "active: bool" in lines[5]

    def test_optional_field(self, compiler: ASTCompiler) -> None:
        from cervellaswarm_lingua_universale._ast import FieldNode
        field = FieldNode("tag", SimpleType("String", True, LOC), Loc(3, 4))
        node = RecordTypeDecl("Item", (field,), Loc(2, 0))
        lines = compiler._compile_record_type(node)
        assert "tag: str | None" in lines[3]

    def test_generic_field(self, compiler: ASTCompiler) -> None:
        from cervellaswarm_lingua_universale._ast import FieldNode
        inner = SimpleType("String", False, LOC)
        field = FieldNode("items", GenericType("List", inner, False, LOC), Loc(3, 4))
        node = RecordTypeDecl("Bag", (field,), Loc(2, 0))
        lines = compiler._compile_record_type(node)
        assert "items: list[str]" in lines[3]

    def test_empty_record(self, compiler: ASTCompiler) -> None:
        node = RecordTypeDecl("Empty", (), Loc(1, 0))
        lines = compiler._compile_record_type(node)
        assert "pass" in lines[3]

    def test_registers_dataclass_import(self, compiler: ASTCompiler) -> None:
        node = RecordTypeDecl("X", (), LOC)
        compiler._compile_record_type(node)
        assert "from dataclasses import dataclass" in compiler._preamble_imports

    def test_in_full_program(self, compiler: ASTCompiler) -> None:
        from cervellaswarm_lingua_universale._ast import FieldNode
        field = FieldNode("name", SimpleType("String", False, LOC), Loc(3, 4))
        prog = ProgramNode(
            (RecordTypeDecl("TaskData", (field,), Loc(2, 0)),),
            Loc(1, 0),
        )
        result = compiler.compile(prog, source_file="types.lu")
        assert "from dataclasses import dataclass" in result.python_source
        assert "@dataclass(frozen=True)" in result.python_source
        assert "class TaskData:" in result.python_source
        assert "name: str" in result.python_source

    def test_generated_code_is_valid_python(self, compiler: ASTCompiler) -> None:
        from cervellaswarm_lingua_universale._ast import FieldNode
        fields = (
            FieldNode("name", SimpleType("String", False, LOC), Loc(3, 4)),
            FieldNode("count", SimpleType("Number", False, LOC), Loc(4, 4)),
        )
        prog = ProgramNode(
            (RecordTypeDecl("Data", fields, Loc(2, 0)),),
            LOC,
        )
        result = compiler.compile(prog, source_file="test.lu")
        compile(result.python_source, "test.lu", "exec")

    def test_mixed_types_program(self, compiler: ASTCompiler) -> None:
        """Program with both variant and record types."""
        from cervellaswarm_lingua_universale._ast import FieldNode
        prog = ProgramNode(
            (
                UseNode("math", None, Loc(1, 0)),
                VariantTypeDecl("Status", ("Active", "Inactive"), Loc(3, 0)),
                RecordTypeDecl("Task", (
                    FieldNode("name", SimpleType("String", False, LOC), Loc(6, 4)),
                ), Loc(5, 0)),
            ),
            Loc(1, 0),
        )
        result = compiler.compile(prog, source_file="mixed.lu")
        assert "from typing import Literal" in result.python_source
        assert "from dataclasses import dataclass" in result.python_source
        assert "import math" in result.python_source
        assert "Status = Literal" in result.python_source
        assert "class Task:" in result.python_source
        assert result.imports == ("math",)
        # Verify syntax
        compile(result.python_source, "mixed.lu", "exec")


# ===================================================================
# Preamble import tracker
# ===================================================================


class TestPreambleImports:
    """Tests for the preamble import tracking mechanism."""

    def test_no_preamble_for_use_only(self, compiler: ASTCompiler) -> None:
        """Programs with only UseNode should have no preamble imports."""
        prog = ProgramNode(
            (UseNode("math", None, LOC),),
            LOC,
        )
        result = compiler.compile(prog)
        assert "from typing" not in result.python_source
        assert "from dataclasses" not in result.python_source

    def test_preamble_sorted(self, compiler: ASTCompiler) -> None:
        """Preamble imports should be sorted alphabetically."""
        from cervellaswarm_lingua_universale._ast import FieldNode
        prog = ProgramNode(
            (
                RecordTypeDecl("R", (
                    FieldNode("x", SimpleType("String", False, LOC), LOC),
                ), LOC),
                VariantTypeDecl("V", ("A", "B"), LOC),
            ),
            LOC,
        )
        result = compiler.compile(prog)
        src = result.python_source
        dc_pos = src.index("from dataclasses")
        lit_pos = src.index("from typing")
        assert dc_pos < lit_pos  # dataclasses before typing (alphabetical)

    def test_preamble_no_duplicates(self, compiler: ASTCompiler) -> None:
        """Multiple variant types should produce only one Literal import."""
        prog = ProgramNode(
            (
                VariantTypeDecl("A", ("X", "Y"), LOC),
                VariantTypeDecl("B", ("P", "Q"), LOC),
            ),
            LOC,
        )
        result = compiler.compile(prog)
        assert result.python_source.count("from typing import Literal") == 1

    def test_preamble_reset_between_compiles(self, compiler: ASTCompiler) -> None:
        """Each compile() call starts with a fresh preamble."""
        # First compile with variant type
        prog1 = ProgramNode(
            (VariantTypeDecl("A", ("X", "Y"), LOC),),
            LOC,
        )
        compiler.compile(prog1)
        # Second compile without variant type
        prog2 = ProgramNode(
            (UseNode("math", None, LOC),),
            LOC,
        )
        result = compiler.compile(prog2)
        assert "from typing" not in result.python_source


# ===================================================================
# Error handling (all declaration types now implemented)
# ===================================================================


class TestCompilerErrors:
    """Verify error handling for invalid inputs."""

    def test_unknown_declaration_raises(self, compiler: ASTCompiler) -> None:
        """Passing an unexpected type to _compile_declaration raises TypeError."""
        with pytest.raises(TypeError, match="Unknown declaration type"):
            compiler._compile_declaration("not_a_decl")  # type: ignore[arg-type]

    def test_unknown_step_type_raises(self, compiler: ASTCompiler) -> None:
        """Passing an unexpected type to _transform_steps raises TypeError."""
        with pytest.raises(TypeError, match="Unknown step type"):
            compiler._transform_steps(("not_a_step",))  # type: ignore[arg-type]


# ===================================================================
# _escape_contract_str hardening (C2.3.1a)
# ===================================================================


class TestEscapeContractStr:
    """Tests for _escape_contract_str edge cases (aligned with codegen._escape_string)."""

    def test_backslash(self, compiler: ASTCompiler) -> None:
        assert compiler._escape_contract_str('a\\b') == 'a\\\\b'

    def test_double_quote(self, compiler: ASTCompiler) -> None:
        assert compiler._escape_contract_str('x == "hello"') == 'x == \\"hello\\"'

    def test_newline(self, compiler: ASTCompiler) -> None:
        assert compiler._escape_contract_str("line1\nline2") == "line1\\nline2"

    def test_carriage_return(self, compiler: ASTCompiler) -> None:
        assert compiler._escape_contract_str("line1\rline2") == "line1\\rline2"

    def test_combined_escapes(self, compiler: ASTCompiler) -> None:
        """All four escape types in one string."""
        raw = 'a\\b\n"c"\rd'
        expected = 'a\\\\b\\n\\"c\\"\\rd'
        assert compiler._escape_contract_str(raw) == expected

    def test_empty_string(self, compiler: ASTCompiler) -> None:
        assert compiler._escape_contract_str("") == ""

    def test_no_special_chars(self, compiler: ASTCompiler) -> None:
        """Plain string passes through unchanged."""
        assert compiler._escape_contract_str("input.is_valid") == "input.is_valid"

    def test_alignment_with_codegen_escape_string(self) -> None:
        """Verify alignment: same output as codegen._escape_string for same input."""
        from cervellaswarm_lingua_universale.codegen import _escape_string

        cases = [
            'hello',
            'a\\b',
            '"quoted"',
            "new\nline",
            "cr\rreturn",
            'all\\four\n"types"\r!',
        ]
        for case in cases:
            assert (
                ASTCompiler._escape_contract_str(case) == _escape_string(case)
            ), f"Mismatch for {case!r}"


# ===================================================================
# CompiledModule.types tracking (C2.3.1b)
# ===================================================================


class TestCompiledModuleTypes:
    """Tests for the new CompiledModule.types field."""

    def test_default_empty(self) -> None:
        mod = CompiledModule(
            source_file="test.lu",
            python_source="x = 1\n",
            agents=(),
            protocols=(),
            imports=(),
        )
        assert mod.types == ()

    def test_variant_tracked(self, compiler: ASTCompiler) -> None:
        prog = ProgramNode(
            (VariantTypeDecl("Status", ("Active", "Inactive"), LOC),),
            LOC,
        )
        result = compiler.compile(prog, source_file="test.lu")
        assert result.types == ("Status",)

    def test_record_tracked(self, compiler: ASTCompiler) -> None:
        from cervellaswarm_lingua_universale._ast import FieldNode
        field = FieldNode("name", SimpleType("String", False, LOC), LOC)
        prog = ProgramNode(
            (RecordTypeDecl("TaskData", (field,), LOC),),
            LOC,
        )
        result = compiler.compile(prog, source_file="test.lu")
        assert result.types == ("TaskData",)

    def test_mixed_types_tracked(self, compiler: ASTCompiler) -> None:
        """Both variant and record types tracked in order."""
        from cervellaswarm_lingua_universale._ast import FieldNode
        field = FieldNode("name", SimpleType("String", False, LOC), LOC)
        prog = ProgramNode(
            (
                VariantTypeDecl("Status", ("Active", "Inactive"), LOC),
                RecordTypeDecl("TaskData", (field,), LOC),
                VariantTypeDecl("Priority", ("High", "Low"), LOC),
            ),
            LOC,
        )
        result = compiler.compile(prog, source_file="test.lu")
        assert result.types == ("Status", "TaskData", "Priority")

    def test_agents_not_in_types(self, compiler: ASTCompiler) -> None:
        """AgentNode names go in agents, not types."""
        from cervellaswarm_lingua_universale._ast import AgentNode
        agent = AgentNode(
            name="Worker", role="worker", trust=None,
            accepts=(), produces=(), requires=(), ensures=(),
            loc=LOC,
        )
        prog = ProgramNode((agent,), LOC)
        result = compiler.compile(prog, source_file="test.lu")
        assert result.types == ()
        assert result.agents == ("Worker",)

    def test_empty_program_no_types(self, compiler: ASTCompiler) -> None:
        prog = ProgramNode((), LOC)
        result = compiler.compile(prog, source_file="test.lu")
        assert result.types == ()


# ===================================================================
# Module metadata: __lu_version__ and __lu_source__ (C2.3.2a)
# ===================================================================


class TestModuleMetadata:
    """Tests for __lu_version__ and __lu_source__ in generated code."""

    def test_lu_version_present(self, compiler: ASTCompiler) -> None:
        prog = ProgramNode((), LOC)
        result = compiler.compile(prog, source_file="test.lu")
        assert '__lu_version__ = "0.2"' in result.python_source

    def test_lu_source_present(self, compiler: ASTCompiler) -> None:
        prog = ProgramNode((), LOC)
        result = compiler.compile(prog, source_file="example.lu")
        assert '__lu_source__ = "example.lu"' in result.python_source

    def test_lu_source_default(self, compiler: ASTCompiler) -> None:
        prog = ProgramNode((), LOC)
        result = compiler.compile(prog)
        assert '__lu_source__ = "<input>"' in result.python_source

    def test_lu_source_with_special_chars(self, compiler: ASTCompiler) -> None:
        """Source file path with quotes is properly escaped."""
        prog = ProgramNode((), LOC)
        result = compiler.compile(prog, source_file='path/"weird".lu')
        assert '__lu_source__ = "path/\\"weird\\".lu"' in result.python_source
        # Exec roundtrip: escaped path is valid Python (F4 fix)
        ns: dict[str, object] = {}
        exec(result.python_source, ns)  # noqa: S102
        assert ns["__lu_source__"] == 'path/"weird".lu'

    def test_metadata_after_docstring(self, compiler: ASTCompiler) -> None:
        """Metadata comes right after the module docstring."""
        prog = ProgramNode((), LOC)
        result = compiler.compile(prog, source_file="test.lu")
        lines = result.python_source.splitlines()
        # Line 0: docstring, Line 1: blank, Line 2: __lu_version__, Line 3: __lu_source__
        assert lines[0].startswith('"""')
        assert lines[2] == '__lu_version__ = "0.2"'
        assert lines[3] == '__lu_source__ = "test.lu"'

    def test_metadata_exec_roundtrip(self, compiler: ASTCompiler) -> None:
        """Metadata is accessible after exec()."""
        prog = ProgramNode(
            (UseNode("math", None, LOC),),
            LOC,
        )
        result = compiler.compile(prog, source_file="meta.lu")
        ns: dict[str, object] = {}
        exec(result.python_source, ns)  # noqa: S102
        assert ns["__lu_version__"] == "0.2"
        assert ns["__lu_source__"] == "meta.lu"

    def test_metadata_before_preamble(self, compiler: ASTCompiler) -> None:
        """Metadata appears before preamble imports."""
        prog = ProgramNode(
            (VariantTypeDecl("Status", ("A", "B"), LOC),),
            LOC,
        )
        result = compiler.compile(prog, source_file="test.lu")
        src = result.python_source
        meta_pos = src.index("__lu_version__")
        import_pos = src.index("from typing import Literal")
        assert meta_pos < import_pos


# ===================================================================
# __all__ generation (C2.3.2b)
# ===================================================================


class TestAllGeneration:
    """Tests for __all__ list generation in compiled code."""

    def test_empty_program_no_all(self, compiler: ASTCompiler) -> None:
        """Empty program has no __all__ (nothing to export)."""
        prog = ProgramNode((), LOC)
        result = compiler.compile(prog, source_file="test.lu")
        assert "__all__" not in result.python_source
        assert result.exports == ()

    def test_use_only_no_all(self, compiler: ASTCompiler) -> None:
        """Programs with only imports have no __all__."""
        prog = ProgramNode(
            (UseNode("math", None, LOC),),
            LOC,
        )
        result = compiler.compile(prog, source_file="test.lu")
        assert "__all__" not in result.python_source
        assert result.exports == ()

    def test_variant_in_all(self, compiler: ASTCompiler) -> None:
        prog = ProgramNode(
            (VariantTypeDecl("Status", ("Active", "Inactive"), LOC),),
            LOC,
        )
        result = compiler.compile(prog, source_file="test.lu")
        assert '__all__ = ["Status"]' in result.python_source
        assert result.exports == ("Status",)

    def test_record_in_all(self, compiler: ASTCompiler) -> None:
        from cervellaswarm_lingua_universale._ast import FieldNode
        field = FieldNode("name", SimpleType("String", False, LOC), LOC)
        prog = ProgramNode(
            (RecordTypeDecl("TaskData", (field,), LOC),),
            LOC,
        )
        result = compiler.compile(prog, source_file="test.lu")
        assert '__all__ = ["TaskData"]' in result.python_source
        assert result.exports == ("TaskData",)

    def test_agent_in_all(self, compiler: ASTCompiler) -> None:
        from cervellaswarm_lingua_universale._ast import AgentNode
        agent = AgentNode(
            name="Worker", role="worker", trust=None,
            accepts=(), produces=(), requires=(), ensures=(),
            loc=LOC,
        )
        prog = ProgramNode((agent,), LOC)
        result = compiler.compile(prog, source_file="test.lu")
        assert '__all__ = ["Worker"]' in result.python_source
        assert result.exports == ("Worker",)

    def test_protocol_session_in_all(self, compiler: ASTCompiler) -> None:
        """Protocol exports its Session class name."""
        from cervellaswarm_lingua_universale._ast import ProtocolNode, StepNode
        step = StepNode("regina", "asks", "worker", "do task", LOC)
        proto = ProtocolNode(
            name="DelegateTask", roles=("regina", "worker"),
            steps=(step,), properties=(), loc=LOC,
        )
        prog = ProgramNode((proto,), LOC)
        result = compiler.compile(prog, source_file="test.lu")
        assert '"DelegateTaskSession"' in result.python_source
        assert "DelegateTaskSession" in result.exports

    def test_mixed_program_all_order(self, compiler: ASTCompiler) -> None:
        """__all__ order: types first, then agents, then session classes."""
        from cervellaswarm_lingua_universale._ast import (
            AgentNode, FieldNode, ProtocolNode, StepNode,
        )
        step = StepNode("regina", "asks", "worker", "do task", LOC)
        prog = ProgramNode(
            (
                VariantTypeDecl("Status", ("A", "B"), LOC),
                RecordTypeDecl("TaskData", (
                    FieldNode("x", SimpleType("String", False, LOC), LOC),
                ), LOC),
                AgentNode(
                    name="Worker", role="worker", trust=None,
                    accepts=(), produces=(), requires=(), ensures=(),
                    loc=LOC,
                ),
                ProtocolNode(
                    name="SimpleTask", roles=("regina", "worker"),
                    steps=(step,), properties=(), loc=LOC,
                ),
            ),
            LOC,
        )
        result = compiler.compile(prog, source_file="test.lu")
        assert result.exports == ("Status", "TaskData", "Worker", "SimpleTaskSession")
        assert (
            '__all__ = ["Status", "TaskData", "Worker", "SimpleTaskSession"]'
            in result.python_source
        )

    def test_all_at_end_of_source(self, compiler: ASTCompiler) -> None:
        """__all__ appears at the end of the generated source."""
        prog = ProgramNode(
            (VariantTypeDecl("Color", ("Red", "Blue"), LOC),),
            LOC,
        )
        result = compiler.compile(prog, source_file="test.lu")
        lines = result.python_source.rstrip().splitlines()
        # __all__ should be near the end (last non-empty line)
        all_lines = [i for i, l in enumerate(lines) if "__all__" in l]
        assert len(all_lines) == 1
        # Should be in the last 3 lines
        assert all_lines[0] >= len(lines) - 3

    def test_all_exec_roundtrip(self, compiler: ASTCompiler) -> None:
        """__all__ is accessible after exec()."""
        prog = ProgramNode(
            (VariantTypeDecl("Status", ("Active", "Inactive"), LOC),),
            LOC,
        )
        result = compiler.compile(prog, source_file="test.lu")
        ns: dict[str, object] = {}
        exec(result.python_source, ns)  # noqa: S102
        assert ns["__all__"] == ["Status"]

    def test_exports_default_empty(self) -> None:
        """CompiledModule.exports defaults to empty tuple."""
        mod = CompiledModule(
            source_file="test.lu",
            python_source="x = 1\n",
            agents=(),
            protocols=(),
            imports=(),
        )
        assert mod.exports == ()

    def test_two_protocols_in_all(self, compiler: ASTCompiler) -> None:
        """Two protocols produce two Session entries in __all__."""
        from cervellaswarm_lingua_universale._ast import ProtocolNode, StepNode
        step1 = StepNode("a", "asks", "b", "do task", LOC)
        step2 = StepNode("c", "asks", "d", "check result", LOC)
        prog = ProgramNode(
            (
                ProtocolNode(
                    name="Alpha", roles=("a", "b"),
                    steps=(step1,), properties=(), loc=LOC,
                ),
                ProtocolNode(
                    name="Beta", roles=("c", "d"),
                    steps=(step2,), properties=(), loc=LOC,
                ),
            ),
            LOC,
        )
        result = compiler.compile(prog, source_file="test.lu")
        assert result.exports == ("AlphaSession", "BetaSession")
        assert '"AlphaSession"' in result.python_source
        assert '"BetaSession"' in result.python_source
