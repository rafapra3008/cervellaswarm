# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Compiler: Lingua Universale AST -> Python source code (C2).

Translates a ``ProgramNode`` AST (produced by the C1 parser) into executable
Python source.  The generated code includes runtime contract enforcement via
``ContractViolation`` and source annotations ``# [LU:line:col]`` for tracing.

Architecture (STUDIO C2.1, S412):
  - **String emission** -- generates Python source as strings (like codegen.py).
  - **isinstance dispatch** -- visitor pattern via ``_compile_declaration``.
  - **Separate from codegen.py** -- different pipeline (AST vs Protocol objects).
  - **Zero external dependencies** -- stdlib + internal modules only.

Implementation plan (7 sub-steps):
  C2.2.1  _contracts.py                DONE (S413)
  C2.2.2  _compiler.py core scaffold   THIS FILE (S413)
          - CompiledModule, ASTCompiler, compile()
          - _expr_to_python, _type_to_python, _compile_use
  C2.2.3  _compile_variant_type, _compile_record_type     THIS FILE (S413)
  C2.2.4  _compile_agent (contracts + metadata)           TODO
  C2.2.5  _compile_protocol (bridge to codegen.py)        TODO
  C2.2.6  Golden file tests + round-trip exec             TODO
  C2.2.7  Guardiana audit finale C2.2                     TODO
"""

from __future__ import annotations

import keyword
from dataclasses import dataclass
from typing import TYPE_CHECKING

from ._ast import (
    AgentNode,
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
    ProtocolNode,
    RecordTypeDecl,
    SimpleType,
    StringExpr,
    UseNode,
    VariantTypeDecl,
)

if TYPE_CHECKING:
    from ._ast import Declaration, Expr, TypeExpr


# ============================================================
# LU -> Python type mapping
# ============================================================

_LU_TYPE_MAP: dict[str, str] = {
    "String": "str",
    "Number": "float",
    "Boolean": "bool",
    "Integer": "int",
    "Any": "object",
}

_LU_GENERIC_MAP: dict[str, str] = {
    "List": "list",
    "Map": "dict",
    "Set": "set",
    "Confident": "Confident",
}

# Python keywords that need a trailing underscore when used as identifiers
# in generated code (e.g. method name "pass" -> "pass_").
_PYTHON_KEYWORDS: frozenset[str] = frozenset(keyword.kwlist) | frozenset(
    keyword.softkwlist
)


# ============================================================
# Result type
# ============================================================


@dataclass(frozen=True)
class CompiledModule:
    """Result of compiling a ProgramNode to Python source."""

    source_file: str
    python_source: str
    agents: tuple[str, ...]
    protocols: tuple[str, ...]
    imports: tuple[str, ...]


# ============================================================
# Compiler
# ============================================================


class ASTCompiler:
    """Compiles a ``ProgramNode`` AST to Python source code.

    Architecture: isinstance-based visitor dispatch, string emission.
    Each declaration type has a dedicated ``_compile_*`` method.

    Usage::

        compiler = ASTCompiler()
        result = compiler.compile(program, source_file="example.lu")
        print(result.python_source)
    """

    def __init__(self) -> None:
        # Preamble import tracker: declaration compilers add lines here.
        # Reset at the start of each compile() call.
        self._preamble_imports: set[str] = set()

    # ----------------------------------------------------------
    # Public API
    # ----------------------------------------------------------

    def compile(
        self, program: ProgramNode, *, source_file: str = "<input>"
    ) -> CompiledModule:
        """Compile a full program AST to Python source."""
        # Reset preamble for this compilation
        self._preamble_imports = set()

        body_lines: list[str] = []

        agents: list[str] = []
        protocols: list[str] = []
        imports: list[str] = []

        for decl in program.declarations:
            decl_lines = self._compile_declaration(decl)
            body_lines.extend(decl_lines)
            body_lines.append("")  # blank separator between declarations

            # Track metadata
            if isinstance(decl, UseNode):
                imports.append(decl.module)
            elif isinstance(decl, AgentNode):
                agents.append(decl.name)
            elif isinstance(decl, ProtocolNode):
                protocols.append(decl.name)

        # Assemble: docstring + preamble imports + body
        lines: list[str] = [
            f'"""Auto-generated from {source_file} by Lingua Universale compiler."""',
        ]
        if self._preamble_imports:
            lines.append("")
            lines.extend(sorted(self._preamble_imports))
        lines.append("")
        lines.extend(body_lines)

        python_source = "\n".join(lines).rstrip("\n") + "\n"

        return CompiledModule(
            source_file=source_file,
            python_source=python_source,
            agents=tuple(agents),
            protocols=tuple(protocols),
            imports=tuple(imports),
        )

    # ----------------------------------------------------------
    # Declaration dispatch
    # ----------------------------------------------------------

    def _compile_declaration(self, decl: Declaration) -> list[str]:
        """Dispatch a top-level declaration to its compiler method."""
        if isinstance(decl, UseNode):
            return self._compile_use(decl)
        if isinstance(decl, VariantTypeDecl):
            return self._compile_variant_type(decl)
        if isinstance(decl, RecordTypeDecl):
            return self._compile_record_type(decl)
        if isinstance(decl, AgentNode):
            return self._compile_agent(decl)
        if isinstance(decl, ProtocolNode):
            return self._compile_protocol(decl)
        raise TypeError(f"Unknown declaration type: {type(decl).__name__}")

    # ----------------------------------------------------------
    # UseNode -> import statement
    # ----------------------------------------------------------

    def _compile_use(self, node: UseNode) -> list[str]:
        """Compile ``use math`` or ``use datetime as dt`` to Python import."""
        loc = self._loc_comment(node.loc)
        if node.alias:
            return [f"import {node.module} as {node.alias}  {loc}"]
        return [f"import {node.module}  {loc}"]

    # ----------------------------------------------------------
    # Type declarations (C2.2.3)
    # ----------------------------------------------------------

    def _compile_variant_type(self, node: VariantTypeDecl) -> list[str]:
        """Compile ``type Status = Active | Inactive`` to Python.

        Generates ``Status = Literal["Active", "Inactive"]`` and registers
        ``from typing import Literal`` in the preamble imports.
        """
        self._preamble_imports.add("from typing import Literal")
        loc = self._loc_comment(node.loc)
        variants = ", ".join(f'"{v}"' for v in node.variants)
        return [f"{node.name} = Literal[{variants}]  {loc}"]

    def _compile_record_type(self, node: RecordTypeDecl) -> list[str]:
        """Compile ``type TaskData: name: String ...`` to Python.

        Generates a ``@dataclass(frozen=True)`` class with typed fields.
        Registers ``from dataclasses import dataclass`` in the preamble.
        """
        self._preamble_imports.add("from dataclasses import dataclass")
        loc = self._loc_comment(node.loc)
        lines = [
            f"@dataclass(frozen=True)  {loc}",
            f"class {node.name}:",
            f'    """Record type \'{node.name}\' -- compiled from Lingua Universale."""',
        ]
        if not node.fields:
            lines.append("    pass")
        else:
            for field in node.fields:
                type_str = self._type_to_python(field.type_expr)
                field_loc = self._loc_comment(field.loc)
                lines.append(f"    {field.name}: {type_str}  {field_loc}")
        return lines

    # ----------------------------------------------------------
    # Agent (stub -- C2.2.4)
    # ----------------------------------------------------------

    def _compile_agent(self, node: AgentNode) -> list[str]:
        """Compile agent declaration. Full implementation in C2.2.4."""
        raise NotImplementedError(
            f"AgentNode compilation not yet implemented: {node.name}"
        )

    # ----------------------------------------------------------
    # Protocol (stub -- C2.2.5)
    # ----------------------------------------------------------

    def _compile_protocol(self, node: ProtocolNode) -> list[str]:
        """Compile protocol declaration. Full implementation in C2.2.5."""
        raise NotImplementedError(
            f"ProtocolNode compilation not yet implemented: {node.name}"
        )

    # ----------------------------------------------------------
    # Expr -> Python expression string
    # ----------------------------------------------------------

    def _expr_to_python(self, expr: Expr) -> str:
        """Convert any Expr AST node to a Python expression string.

        Always parenthesises binary sub-expressions to avoid precedence issues
        (STUDIO C2.1 risk mitigation).
        """
        if isinstance(expr, IdentExpr):
            return self._safe_ident(expr.name)

        if isinstance(expr, NumberExpr):
            return expr.value

        if isinstance(expr, StringExpr):
            # StringExpr.value already includes surrounding quotes
            return expr.value

        if isinstance(expr, AttrExpr):
            return f"{self._safe_ident(expr.obj)}.{self._safe_ident(expr.attr)}"

        if isinstance(expr, MethodCallExpr):
            obj = self._safe_ident(expr.obj)
            method = self._safe_ident(expr.method)
            args = ", ".join(self._expr_to_python(a) for a in expr.args)
            return f"{obj}.{method}({args})"

        if isinstance(expr, BinOpExpr):
            left = self._expr_to_python(expr.left)
            right = self._expr_to_python(expr.right)
            return f"({left}) {expr.op} ({right})"

        if isinstance(expr, NotExpr):
            operand = self._expr_to_python(expr.operand)
            return f"not ({operand})"

        if isinstance(expr, GroupExpr):
            inner = self._expr_to_python(expr.inner)
            return f"({inner})"

        raise TypeError(f"Unknown Expr type: {type(expr).__name__}")

    # ----------------------------------------------------------
    # TypeExpr -> Python type hint string
    # ----------------------------------------------------------

    def _type_to_python(self, tex: TypeExpr) -> str:
        """Convert a TypeExpr AST node to a Python type annotation string.

        Uses ``X | None`` (PEP 604, Python 3.10+) for optional types instead
        of ``Optional[X]``, avoiding the need to track ``from typing import
        Optional`` in the generated output.
        """
        if isinstance(tex, SimpleType):
            base = _LU_TYPE_MAP.get(tex.name, tex.name)
            if tex.optional:
                return f"{base} | None"
            return base

        if isinstance(tex, GenericType):
            base = _LU_GENERIC_MAP.get(tex.name, tex.name)
            arg = self._type_to_python(tex.arg)
            inner = f"{base}[{arg}]"
            if tex.optional:
                return f"{inner} | None"
            return inner

        raise TypeError(f"Unknown TypeExpr type: {type(tex).__name__}")

    # ----------------------------------------------------------
    # Helpers
    # ----------------------------------------------------------

    @staticmethod
    def _loc_comment(loc: Loc) -> str:
        """Build a source-annotation comment ``# [LU:line:col]``."""
        return f"# [LU:{loc.line}:{loc.col}]"

    @staticmethod
    def _safe_ident(name: str) -> str:
        """Append trailing ``_`` if *name* is a Python keyword.

        Handles e.g. method name ``pass`` -> ``pass_``, ``class`` -> ``class_``.
        """
        if name in _PYTHON_KEYWORDS:
            return f"{name}_"
        return name

