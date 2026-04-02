# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Auto-formatter for Lingua Universale ``.lu`` files (B6).

Zero-config, opinionated formatter inspired by gofmt, elm-format, and buf.
``lu fmt`` enforces a single canonical style for all .lu files.

Architecture (based on research of 6 formatters -- 18 sources):
  - Pre-scan: extract comments with line positions before parse.
  - Parse: standard tokenizer + parser -> ProgramNode AST.
  - Format: recursive AST walk emitting canonical text.
  - Re-inject: comments reinserted by position during format.

Design report:
``.sncp/progetti/cervellaswarm/reports/RESEARCH_20260313_LU_FMT_DESIGN.md``
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

from ._ast import (
    AgentNode,
    AllParticipate,
    AlwaysTerminates,
    ChoiceNode,
    ConfidenceProp,
    ExclusionProp,
    NoDeletionProp,
    NoDeadlock,
    OrderingProp,
    ProgramNode,
    ProtocolNode,
    RecordTypeDecl,
    RoleExclusiveProp,
    SimpleType,
    StepNode,
    TrustProp,
    UseNode,
    VariantTypeDecl,
)

if TYPE_CHECKING:
    from ._ast import (
        Expr,
        Property,
        StepOrChoice,
        TypeExpr,
    )


# ============================================================
# Comment extraction (pre-parse)
# ============================================================


@dataclass(frozen=True)
class _Comment:
    """A source comment with its original line number."""

    line: int   # 1-indexed
    text: str   # full line text including '#', stripped of leading whitespace


def _extract_comments(source: str) -> list[_Comment]:
    """Extract all comment lines from source before parsing."""
    comments: list[_Comment] = []
    for i, raw in enumerate(source.splitlines(), start=1):
        stripped = raw.strip()
        if stripped.startswith("#"):
            comments.append(_Comment(line=i, text=stripped))
    return comments


# ============================================================
# Formatter
# ============================================================

_INDENT = "    "  # 4 spaces, invariant (tokenizer enforces this)


def _property_sort_key(prop: Property) -> tuple[int, str, str]:
    """Canonical ordering for properties block."""
    if isinstance(prop, AlwaysTerminates):
        return (0, "", "")
    if isinstance(prop, NoDeadlock):
        return (1, "", "")
    if isinstance(prop, NoDeletionProp):
        return (2, "", "")
    if isinstance(prop, AllParticipate):
        return (3, "", "")
    if isinstance(prop, ConfidenceProp):
        return (4, prop.level, "")
    if isinstance(prop, TrustProp):
        return (5, prop.tier, "")
    if isinstance(prop, OrderingProp):
        return (6, prop.before, prop.after)
    if isinstance(prop, ExclusionProp):
        return (7, prop.role, prop.message)
    if isinstance(prop, RoleExclusiveProp):
        return (8, prop.role, prop.message)
    return (99, "", "")  # pragma: no cover


def _format_type_expr(te: TypeExpr) -> str:
    """Render a type expression to canonical text."""
    if isinstance(te, SimpleType):
        suffix = "?" if te.optional else ""
        return f"{te.name}{suffix}"
    # GenericType
    suffix = "?" if te.optional else ""
    return f"{te.name}[{_format_type_expr(te.arg)}]{suffix}"


def _format_expr(expr: Expr) -> str:
    """Render an expression to canonical text."""
    from ._ast import (
        AttrExpr,
        BinOpExpr,
        GroupExpr,
        IdentExpr,
        MethodCallExpr,
        NotExpr,
        NumberExpr,
        StringExpr,
    )

    if isinstance(expr, IdentExpr):
        return expr.name
    if isinstance(expr, NumberExpr):
        return expr.value
    if isinstance(expr, StringExpr):
        return expr.value
    if isinstance(expr, AttrExpr):
        return f"{expr.obj}.{expr.attr}"
    if isinstance(expr, MethodCallExpr):
        args = ", ".join(_format_expr(a) for a in expr.args)
        return f"{expr.obj}.{expr.method}({args})"
    if isinstance(expr, BinOpExpr):
        return f"{_format_expr(expr.left)} {expr.op} {_format_expr(expr.right)}"
    if isinstance(expr, NotExpr):
        return f"not {_format_expr(expr.operand)}"
    if isinstance(expr, GroupExpr):
        return f"({_format_expr(expr.inner)})"
    return str(expr)  # pragma: no cover


def _format_step(step: StepNode) -> str:
    """Render a step to canonical text, respecting action-specific word order.

    Patterns (from parser grammar)::
        asks:     sender asks receiver to payload
        returns:  sender returns payload to receiver
        tells:    sender tells receiver payload
        proposes: sender proposes payload to receiver
        sends:    sender sends payload to receiver
    """
    if step.action == "asks":
        return f"{step.sender} asks {step.receiver} to {step.payload}"
    if step.action in ("returns", "proposes", "sends"):
        return f"{step.sender} {step.action} {step.payload} to {step.receiver}"
    if step.action == "tells":
        return f"{step.sender} tells {step.receiver} {step.payload}"
    # Fallback for unknown actions
    return f"{step.sender} {step.action} {step.receiver} to {step.payload}"


def _format_property(prop: Property) -> str:
    """Render a single property to canonical text."""
    if isinstance(prop, AlwaysTerminates):
        return "always terminates"
    if isinstance(prop, NoDeadlock):
        return "no deadlock"
    if isinstance(prop, NoDeletionProp):
        return "no deletion"
    if isinstance(prop, AllParticipate):
        return "all roles participate"
    if isinstance(prop, ConfidenceProp):
        return f"confidence >= {prop.level}"
    if isinstance(prop, TrustProp):
        return f"trust >= {prop.tier}"
    if isinstance(prop, OrderingProp):
        return f"{prop.before} before {prop.after}"
    if isinstance(prop, ExclusionProp):
        return f"{prop.role} cannot send {prop.message}"
    if isinstance(prop, RoleExclusiveProp):
        return f"{prop.role} exclusive {prop.message}"
    return str(prop)  # pragma: no cover


@dataclass
class LUFormatter:
    """Formats a parsed LU program to canonical style."""

    _comments: list[_Comment] = field(default_factory=list)
    _comment_idx: int = field(default=0, init=False)

    def format_program(self, program: ProgramNode) -> str:
        """Format an entire program to canonical string."""
        self._comment_idx = 0
        parts: list[str] = []

        # Emit file-level leading comments (before first declaration)
        first_decl_line = (
            program.declarations[0].loc.line
            if program.declarations
            else 999999
        )
        header = self._drain_comments_before(first_decl_line)
        if header:
            parts.append(header)
            parts.append("")  # blank line after header comments

        # Group declarations by type for ordering:
        # use -> types -> agents -> protocols (preserve order within groups)
        uses: list[UseNode] = []
        types: list[VariantTypeDecl | RecordTypeDecl] = []
        agents: list[AgentNode] = []
        protocols: list[ProtocolNode] = []

        for decl in program.declarations:
            if isinstance(decl, UseNode):
                uses.append(decl)
            elif isinstance(decl, (VariantTypeDecl, RecordTypeDecl)):
                types.append(decl)
            elif isinstance(decl, AgentNode):
                agents.append(decl)
            elif isinstance(decl, ProtocolNode):
                protocols.append(decl)

        # Sort uses alphabetically by module name
        uses.sort(key=lambda u: u.module)

        sections: list[list[str]] = []

        # Uses don't need blank lines between them
        if uses:
            section: list[str] = []
            for use in uses:
                leading = self._drain_comments_before(use.loc.line)
                if leading:
                    section.append(leading)
                section.append(self._format_use(use))
            sections.append(section)

        for group, formatter in [
            (types, self._format_type),
            (agents, self._format_agent),
            (protocols, self._format_protocol),
        ]:
            if group:
                sections.append(self._format_decl_group(group, formatter))

        # Join sections with blank lines
        for i, sec in enumerate(sections):
            parts.extend(sec)
            if i < len(sections) - 1:
                parts.append("")

        # Trailing comments (after all declarations)
        trailing = self._drain_remaining_comments()
        if trailing:
            parts.append("")
            parts.append(trailing)

        # Ensure single trailing newline
        result = "\n".join(parts)
        if not result.endswith("\n"):
            result += "\n"
        return result

    def _format_decl_group(self, items: list, formatter) -> list[str]:
        """Format a group of declarations with leading comments and blank lines."""
        section: list[str] = []
        for i, item in enumerate(items):
            leading = self._drain_comments_before(item.loc.line)
            if leading:
                section.append(leading)
            section.append(formatter(item))
            if i < len(items) - 1:
                section.append("")
        return section

    def _drain_comments_before(self, line: int) -> str:
        """Return all comments with line < `line`, advance index."""
        lines: list[str] = []
        while (
            self._comment_idx < len(self._comments)
            and self._comments[self._comment_idx].line < line
        ):
            lines.append(self._comments[self._comment_idx].text)
            self._comment_idx += 1
        return "\n".join(lines)

    def _drain_remaining_comments(self) -> str:
        """Return all remaining comments."""
        lines: list[str] = []
        while self._comment_idx < len(self._comments):
            lines.append(self._comments[self._comment_idx].text)
            self._comment_idx += 1
        return "\n".join(lines)

    def _format_use(self, node: UseNode) -> str:
        if node.alias:
            return f"use python {node.module} as {node.alias}"
        return f"use python {node.module}"

    def _format_type(self, node: VariantTypeDecl | RecordTypeDecl) -> str:
        if isinstance(node, VariantTypeDecl):
            variants = " | ".join(node.variants)
            return f"type {node.name} = {variants}"
        # RecordTypeDecl
        lines = [f"type {node.name} ="]
        for f in node.fields:
            lines.append(f"{_INDENT}{f.name}: {_format_type_expr(f.type_expr)}")
        return "\n".join(lines)

    def _format_agent(self, node: AgentNode) -> str:
        lines = [f"agent {node.name}:"]
        # Canonical clause order: role, trust, accepts, produces, requires, ensures
        if node.role is not None:
            lines.append(f"{_INDENT}role: {node.role}")
        if node.trust is not None:
            lines.append(f"{_INDENT}trust: {node.trust}")
        if node.accepts:
            lines.append(f"{_INDENT}accepts: {', '.join(node.accepts)}")
        if node.produces:
            lines.append(f"{_INDENT}produces: {', '.join(node.produces)}")
        if node.requires:
            if len(node.requires) == 1:
                lines.append(f"{_INDENT}requires: {_format_expr(node.requires[0])}")
            else:
                lines.append(f"{_INDENT}requires:")
                for expr in node.requires:
                    lines.append(f"{_INDENT}{_INDENT}{_format_expr(expr)}")
        if node.ensures:
            if len(node.ensures) == 1:
                lines.append(f"{_INDENT}ensures: {_format_expr(node.ensures[0])}")
            else:
                lines.append(f"{_INDENT}ensures:")
                for expr in node.ensures:
                    lines.append(f"{_INDENT}{_INDENT}{_format_expr(expr)}")
        return "\n".join(lines)

    def _format_protocol(self, node: ProtocolNode) -> str:
        lines = [f"protocol {node.name}:"]
        lines.append(f"{_INDENT}roles: {', '.join(node.roles)}")
        lines.append("")  # blank line after roles

        # Steps and choices
        self._format_steps(node.steps, depth=1, lines=lines)

        # Properties block
        if node.properties:
            lines.append("")  # blank line before properties
            lines.append(f"{_INDENT}properties:")
            sorted_props = sorted(node.properties, key=_property_sort_key)
            for prop in sorted_props:
                lines.append(f"{_INDENT}{_INDENT}{_format_property(prop)}")

        return "\n".join(lines)

    def _format_steps(
        self,
        items: tuple[StepOrChoice, ...],
        depth: int,
        lines: list[str],
    ) -> None:
        """Format steps and choices at a given indentation depth."""
        indent = _INDENT * depth
        prev_was_choice = False

        for i, item in enumerate(items):
            if isinstance(item, StepNode):
                if prev_was_choice and i > 0:
                    lines.append("")  # blank line after choice block
                lines.append(f"{indent}{_format_step(item)}")
                prev_was_choice = False
            elif isinstance(item, ChoiceNode):
                if i > 0:
                    lines.append("")  # blank line before choice
                lines.append(f"{indent}when {item.decider} decides:")
                for j, branch in enumerate(item.branches):
                    if j > 0:
                        lines.append("")  # blank line between branches
                    branch_indent = _INDENT * (depth + 1)
                    lines.append(f"{branch_indent}{branch.label}:")
                    self._format_steps(
                        branch.steps, depth + 2, lines,
                    )
                prev_was_choice = True


# ============================================================
# Public API
# ============================================================


def format_source(
    source: str,
    *,
    source_file: str = "<input>",
) -> str:
    """Parse and format LU source code to canonical style.

    Returns the formatted source string.
    Raises on parse error.
    """
    from ._parser import parse

    comments = _extract_comments(source)
    program = parse(source)
    formatter = LUFormatter(_comments=comments)
    return formatter.format_program(program)


def format_file(
    path: str | Path,
) -> tuple[str, bool]:
    """Format a .lu file.

    Returns (formatted_source, changed) where changed is True if the
    formatted output differs from the original source.
    """
    file_path = Path(path)
    source = file_path.read_text(encoding="utf-8")
    formatted = format_source(source, source_file=str(file_path))
    changed = formatted != source
    return formatted, changed
