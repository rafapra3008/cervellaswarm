# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Linter for Lingua Universale ``.lu`` files.

Checks style, correctness, and best practices on parsed AST nodes.
Distinct from ``lu check`` (syntax/compile) and ``lu verify`` (formal
properties): ``lu lint`` catches structural issues and convention
violations that are valid LU but likely wrong or suboptimal.

Design based on research of Clippy, Ruff, Go vet, Gleam, Buf/protolint,
and elm-review (14 sources).  See report:
``.sncp/progetti/cervellaswarm/reports/RESEARCH_20260313_LU_LINT_DESIGN.md``

Architecture:
  - Single-pass AST walk (like Ruff visitor pattern).
  - Each rule is a plain function: ``(node, ctx) -> list[LintFinding]``.
  - ``lint_program()`` orchestrates the walk and collects findings.
  - Findings carry severity (ERROR | WARNING) and a human-readable message.
  - Exit code: 1 if any ERROR findings, 0 otherwise.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING

from ._ast import (
    AgentNode,
    BranchNode,
    ChoiceNode,
    ProgramNode,
    ProtocolNode,
    StepNode,
)

if TYPE_CHECKING:
    from ._ast import Loc, StepOrChoice


# ============================================================
# Data types
# ============================================================


class LintSeverity(Enum):
    """Severity of a lint finding."""

    ERROR = "error"      # Correctness -- blocks (exit code 1)
    WARNING = "warning"  # Style / best practice -- advisory


class LintCategory(Enum):
    """Category of a lint rule."""

    CORRECTNESS = "correctness"
    STYLE = "style"
    BEST_PRACTICES = "best_practices"


@dataclass(frozen=True)
class LintFinding:
    """A single lint finding."""

    code: str           # e.g. "LU-W010"
    message: str        # human-readable description
    severity: LintSeverity
    category: LintCategory
    line: int           # 1-indexed source line
    col: int            # 0-indexed column


@dataclass
class LintContext:
    """Mutable context accumulated during the AST walk."""

    source_file: str = "<input>"
    findings: list[LintFinding] = field(default_factory=list)

    def add(self, finding: LintFinding) -> None:
        self.findings.append(finding)


# ============================================================
# Helpers
# ============================================================

_PASCAL_CASE_RE = re.compile(r"^[A-Z][a-zA-Z0-9]*$")


def _collect_steps_recursive(
    items: tuple[StepOrChoice, ...],
) -> list[StepNode]:
    """Flatten all StepNodes from a possibly nested step/choice tree."""
    result: list[StepNode] = []
    for item in items:
        if isinstance(item, StepNode):
            result.append(item)
        elif isinstance(item, ChoiceNode):
            for branch in item.branches:
                result.extend(_collect_steps_recursive(branch.steps))
    return result


def _collect_choices_recursive(
    items: tuple[StepOrChoice, ...],
) -> list[ChoiceNode]:
    """Collect all ChoiceNodes from a possibly nested tree."""
    result: list[ChoiceNode] = []
    for item in items:
        if isinstance(item, ChoiceNode):
            result.append(item)
            for branch in item.branches:
                result.extend(_collect_choices_recursive(branch.steps))
    return result


# ============================================================
# CORRECTNESS rules (severity = ERROR)
# ============================================================


def _check_duplicate_role(node: ProtocolNode, ctx: LintContext) -> None:
    """LU-W010: Same role declared twice in roles list."""
    seen: dict[str, int] = {}
    for role in node.roles:
        if role in seen:
            ctx.add(LintFinding(
                code="LU-W010",
                message=f"duplicate role '{role}' in protocol '{node.name}'",
                severity=LintSeverity.ERROR,
                category=LintCategory.CORRECTNESS,
                line=node.loc.line,
                col=node.loc.col,
            ))
        seen[role] = 1


def _check_empty_branch(node: ProtocolNode, ctx: LintContext) -> None:
    """LU-W011: Branch with zero steps -- protocol is incomplete."""
    for choice in _collect_choices_recursive(node.steps):
        for branch in choice.branches:
            if len(branch.steps) == 0:
                ctx.add(LintFinding(
                    code="LU-W011",
                    message=(
                        f"empty branch '{branch.label}' in choice by "
                        f"'{choice.decider}' (protocol '{node.name}')"
                    ),
                    severity=LintSeverity.ERROR,
                    category=LintCategory.CORRECTNESS,
                    line=branch.loc.line,
                    col=branch.loc.col,
                ))


def _check_self_message(node: ProtocolNode, ctx: LintContext) -> None:
    """LU-W012: sender == receiver in a step -- invalid in MPST."""
    for step in _collect_steps_recursive(node.steps):
        if step.sender == step.receiver:
            ctx.add(LintFinding(
                code="LU-W012",
                message=(
                    f"self-message: '{step.sender}' sends to itself "
                    f"(protocol '{node.name}')"
                ),
                severity=LintSeverity.ERROR,
                category=LintCategory.CORRECTNESS,
                line=step.loc.line,
                col=step.loc.col,
            ))


def _check_duplicate_branch_label(
    node: ProtocolNode, ctx: LintContext,
) -> None:
    """LU-W013: Two branches with same label -- second is unreachable."""
    for choice in _collect_choices_recursive(node.steps):
        seen: dict[str, int] = {}
        for branch in choice.branches:
            if branch.label in seen:
                ctx.add(LintFinding(
                    code="LU-W013",
                    message=(
                        f"duplicate branch label '{branch.label}' in choice "
                        f"by '{choice.decider}' (protocol '{node.name}')"
                    ),
                    severity=LintSeverity.ERROR,
                    category=LintCategory.CORRECTNESS,
                    line=branch.loc.line,
                    col=branch.loc.col,
                ))
            seen[branch.label] = 1


def _check_undefined_role_in_step(
    node: ProtocolNode, ctx: LintContext,
) -> None:
    """LU-W014: Role used in step but not declared in roles list."""
    declared = set(node.roles)
    for step in _collect_steps_recursive(node.steps):
        for role_name, label in [
            (step.sender, "sender"),
            (step.receiver, "receiver"),
        ]:
            if role_name not in declared:
                ctx.add(LintFinding(
                    code="LU-W014",
                    message=(
                        f"undefined role '{role_name}' used as {label} "
                        f"(protocol '{node.name}', declared: "
                        f"{', '.join(sorted(declared))})"
                    ),
                    severity=LintSeverity.ERROR,
                    category=LintCategory.CORRECTNESS,
                    line=step.loc.line,
                    col=step.loc.col,
                ))
    # Also check choice deciders
    for choice in _collect_choices_recursive(node.steps):
        if choice.decider not in declared:
            ctx.add(LintFinding(
                code="LU-W014",
                message=(
                    f"undefined role '{choice.decider}' used as choice "
                    f"decider (protocol '{node.name}', declared: "
                    f"{', '.join(sorted(declared))})"
                ),
                severity=LintSeverity.ERROR,
                category=LintCategory.CORRECTNESS,
                line=choice.loc.line,
                col=choice.loc.col,
            ))


# ============================================================
# STYLE rules (severity = WARNING)
# ============================================================


def _check_protocol_name_convention(
    node: ProtocolNode, ctx: LintContext,
) -> None:
    """LU-W002: Protocol name should be PascalCase."""
    if not _PASCAL_CASE_RE.match(node.name):
        ctx.add(LintFinding(
            code="LU-W002",
            message=(
                f"protocol name '{node.name}' is not PascalCase "
                f"(suggestion: convert to PascalCase)"
            ),
            severity=LintSeverity.WARNING,
            category=LintCategory.STYLE,
            line=node.loc.line,
            col=node.loc.col,
        ))


def _check_single_step_protocol(
    node: ProtocolNode, ctx: LintContext,
) -> None:
    """LU-W005: Protocol with a single step -- possible over-engineering."""
    all_steps = _collect_steps_recursive(node.steps)
    if len(all_steps) == 1 and len(node.steps) == 1:
        ctx.add(LintFinding(
            code="LU-W005",
            message=(
                f"protocol '{node.name}' has only 1 step -- "
                f"consider if a protocol is needed"
            ),
            severity=LintSeverity.WARNING,
            category=LintCategory.STYLE,
            line=node.loc.line,
            col=node.loc.col,
        ))


# ============================================================
# BEST PRACTICES rules (severity = WARNING)
# ============================================================


def _check_no_properties_declared(
    node: ProtocolNode, ctx: LintContext,
) -> None:
    """LU-W020: Protocol without properties loses LU's key value."""
    if not node.properties:
        ctx.add(LintFinding(
            code="LU-W020",
            message=(
                f"protocol '{node.name}' has no properties declared -- "
                f"consider adding 'properties for {node.name}:' with "
                f"at least 'always_terminates' and 'no_deadlock'"
            ),
            severity=LintSeverity.WARNING,
            category=LintCategory.BEST_PRACTICES,
            line=node.loc.line,
            col=node.loc.col,
        ))


def _check_deep_nesting(
    node: ProtocolNode, ctx: LintContext,
    *, max_depth: int = 3,
) -> None:
    """LU-W022: Nested choice deeper than max_depth levels."""

    def _walk(items: tuple[StepOrChoice, ...], depth: int) -> None:
        for item in items:
            if isinstance(item, ChoiceNode):
                if depth + 1 > max_depth:
                    ctx.add(LintFinding(
                        code="LU-W022",
                        message=(
                            f"choice nesting depth {depth + 1} exceeds "
                            f"recommended max {max_depth} "
                            f"(protocol '{node.name}')"
                        ),
                        severity=LintSeverity.WARNING,
                        category=LintCategory.BEST_PRACTICES,
                        line=item.loc.line,
                        col=item.loc.col,
                    ))
                for branch in item.branches:
                    _walk(branch.steps, depth + 1)

    _walk(node.steps, 0)


def _check_agent_no_trust(node: AgentNode, ctx: LintContext) -> None:
    """LU-W024: Agent without explicit trust tier."""
    if node.trust is None:
        ctx.add(LintFinding(
            code="LU-W024",
            message=(
                f"agent '{node.name}' has no explicit trust tier -- "
                f"consider adding 'trust: standard' or appropriate tier"
            ),
            severity=LintSeverity.WARNING,
            category=LintCategory.BEST_PRACTICES,
            line=node.loc.line,
            col=node.loc.col,
        ))


# ============================================================
# Main entry point
# ============================================================

# All protocol-level rules
_PROTOCOL_RULES = [
    _check_duplicate_role,
    _check_empty_branch,
    _check_self_message,
    _check_duplicate_branch_label,
    _check_undefined_role_in_step,
    _check_protocol_name_convention,
    _check_single_step_protocol,
    _check_no_properties_declared,
    _check_deep_nesting,
]

# All agent-level rules
_AGENT_RULES = [
    _check_agent_no_trust,
]


def lint_program(
    program: ProgramNode,
    *,
    source_file: str = "<input>",
    ignore: frozenset[str] = frozenset(),
) -> list[LintFinding]:
    """Lint a parsed LU program.

    Args:
        program: The parsed AST root.
        source_file: Label for error messages.
        ignore: Set of rule codes to skip (e.g. ``{"LU-W002", "LU-W020"}``).

    Returns:
        List of findings sorted by (line, col, code).
    """
    ctx = LintContext(source_file=source_file)

    for decl in program.declarations:
        if isinstance(decl, ProtocolNode):
            for rule_fn in _PROTOCOL_RULES:
                rule_fn(decl, ctx)
        elif isinstance(decl, AgentNode):
            for rule_fn in _AGENT_RULES:
                rule_fn(decl, ctx)

    # Filter ignored rules and sort
    findings = [f for f in ctx.findings if f.code not in ignore]
    findings.sort(key=lambda f: (f.line, f.col, f.code))
    return findings


def lint_source(
    source: str,
    *,
    source_file: str = "<input>",
    ignore: frozenset[str] = frozenset(),
) -> list[LintFinding]:
    """Parse and lint LU source code.

    Returns findings or raises on parse error.
    """
    from ._parser import parse

    program = parse(source)
    return lint_program(program, source_file=source_file, ignore=ignore)


def lint_file(
    path: str | Path,
    *,
    ignore: frozenset[str] = frozenset(),
) -> list[LintFinding]:
    """Parse and lint a ``.lu`` file."""
    file_path = Path(path)
    source = file_path.read_text(encoding="utf-8")
    return lint_source(source, source_file=str(file_path), ignore=ignore)
