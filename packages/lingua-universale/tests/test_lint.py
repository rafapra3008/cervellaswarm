# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for the _lint.py module -- Lingua Universale linter.

Covers all 10 rules:
  CORRECTNESS (ERROR):
    LU-W010  duplicate_role
    LU-W011  empty_branch
    LU-W012  self_message
    LU-W013  duplicate_branch_label
    LU-W014  undefined_role_in_step (sender, receiver, choice decider)
  STYLE (WARNING):
    LU-W002  protocol_name_convention
    LU-W005  single_step_protocol
  BEST PRACTICES (WARNING):
    LU-W020  no_properties_declared
    LU-W022  deep_nesting
    LU-W024  agent_no_trust

Also tests: lint_program(), lint_source(), lint_file(), ignore parameter, CLI.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path

import pytest

from cervellaswarm_lingua_universale._ast import (
    AgentNode,
    AlwaysTerminates,
    BranchNode,
    ChoiceNode,
    Loc,
    NoDeadlock,
    ProgramNode,
    ProtocolNode,
    StepNode,
)
from cervellaswarm_lingua_universale._lint import (
    LintCategory,
    LintFinding,
    LintSeverity,
    lint_file,
    lint_program,
    lint_source,
)


# ============================================================
# Helpers
# ============================================================


def _loc(line: int = 1, col: int = 0) -> Loc:
    return Loc(line=line, col=col)


def _step(
    sender: str,
    receiver: str,
    action: str = "asks",
    payload: str = "do task",
    line: int = 1,
) -> StepNode:
    return StepNode(
        sender=sender,
        action=action,
        receiver=receiver,
        payload=payload,
        loc=_loc(line),
    )


def _branch(label: str, steps: tuple, line: int = 2) -> BranchNode:
    return BranchNode(label=label, steps=steps, loc=_loc(line))


def _choice(decider: str, branches: tuple, line: int = 2) -> ChoiceNode:
    return ChoiceNode(decider=decider, branches=branches, loc=_loc(line))


def _protocol(
    name: str,
    roles: tuple,
    steps: tuple,
    properties: tuple = (),
    line: int = 1,
) -> ProtocolNode:
    return ProtocolNode(
        name=name,
        roles=roles,
        steps=steps,
        properties=properties,
        loc=_loc(line),
    )


def _agent(
    name: str,
    trust: str | None = None,
    role: str | None = None,
    line: int = 1,
) -> AgentNode:
    return AgentNode(
        name=name,
        role=role,
        trust=trust,
        accepts=(),
        produces=(),
        requires=(),
        ensures=(),
        loc=_loc(line),
    )


def _program(*declarations) -> ProgramNode:
    return ProgramNode(declarations=tuple(declarations), loc=_loc())


def _codes(findings: list[LintFinding]) -> list[str]:
    """Return the list of finding codes in order."""
    return [f.code for f in findings]


def _find(findings: list[LintFinding], code: str) -> list[LintFinding]:
    """Filter findings by code."""
    return [f for f in findings if f.code == code]


# ============================================================
# TestCorrectness
# ============================================================


class TestCorrectness:
    """Tests for ERROR-severity correctness rules."""

    # --- LU-W010: duplicate_role ---

    def test_duplicate_role_triggers_finding(self):
        """LU-W010 fires when the same role is declared twice."""
        proto = _protocol(
            "DupRole",
            roles=("alice", "bob", "alice"),
            steps=(_step("alice", "bob"),),
            properties=(AlwaysTerminates(loc=_loc()),),
        )
        findings = lint_program(_program(proto))
        w010 = _find(findings, "LU-W010")
        assert len(w010) == 1
        assert w010[0].severity == LintSeverity.ERROR
        assert w010[0].category == LintCategory.CORRECTNESS
        assert "alice" in w010[0].message
        assert "DupRole" in w010[0].message

    def test_duplicate_role_multiple_duplicates(self):
        """LU-W010 fires once per extra duplicate occurrence."""
        proto = _protocol(
            "ManyDup",
            roles=("alice", "bob", "alice", "bob"),
            steps=(_step("alice", "bob"),),
            properties=(AlwaysTerminates(loc=_loc()),),
        )
        findings = lint_program(_program(proto))
        w010 = _find(findings, "LU-W010")
        assert len(w010) == 2

    def test_no_duplicate_role_no_finding(self):
        """LU-W010 does NOT fire when all roles are distinct."""
        proto = _protocol(
            "CleanRoles",
            roles=("alice", "bob", "carol"),
            steps=(
                _step("alice", "bob"),
                _step("bob", "carol"),
            ),
            properties=(AlwaysTerminates(loc=_loc()),),
        )
        findings = lint_program(_program(proto))
        assert not _find(findings, "LU-W010")

    # --- LU-W011: empty_branch ---

    def test_empty_branch_triggers_finding(self):
        """LU-W011 fires when a branch has zero steps."""
        empty = _branch("empty_path", steps=(), line=3)
        full = _branch("ok_path", steps=(_step("alice", "bob"),), line=4)
        choice = _choice("alice", branches=(empty, full), line=2)
        proto = _protocol(
            "EmptyBranch",
            roles=("alice", "bob"),
            steps=(choice,),
            properties=(AlwaysTerminates(loc=_loc()),),
        )
        findings = lint_program(_program(proto))
        w011 = _find(findings, "LU-W011")
        assert len(w011) == 1
        assert w011[0].severity == LintSeverity.ERROR
        assert w011[0].category == LintCategory.CORRECTNESS
        assert "empty_path" in w011[0].message
        assert "alice" in w011[0].message

    def test_empty_branch_nested_choice(self):
        """LU-W011 fires for empty branch inside nested choice."""
        inner_empty = _branch("inner_empty", steps=(), line=5)
        inner_full = _branch("inner_full", steps=(_step("bob", "carol"),), line=6)
        inner_choice = _choice("bob", branches=(inner_empty, inner_full), line=4)
        outer_full = _branch(
            "outer_full",
            steps=(_step("alice", "bob"), inner_choice),
            line=3,
        )
        outer_empty = _branch("outer_empty", steps=(), line=7)
        outer_choice = _choice("alice", branches=(outer_full, outer_empty), line=2)
        proto = _protocol(
            "NestedEmpty",
            roles=("alice", "bob", "carol"),
            steps=(outer_choice,),
            properties=(AlwaysTerminates(loc=_loc()),),
        )
        findings = lint_program(_program(proto))
        w011 = _find(findings, "LU-W011")
        assert len(w011) == 2

    def test_no_empty_branch_no_finding(self):
        """LU-W011 does NOT fire when all branches have at least one step."""
        b1 = _branch("yes", steps=(_step("alice", "bob"),), line=3)
        b2 = _branch("no", steps=(_step("bob", "alice"),), line=4)
        choice = _choice("alice", branches=(b1, b2), line=2)
        proto = _protocol(
            "GoodBranches",
            roles=("alice", "bob"),
            steps=(choice,),
            properties=(AlwaysTerminates(loc=_loc()),),
        )
        findings = lint_program(_program(proto))
        assert not _find(findings, "LU-W011")

    # --- LU-W012: self_message ---

    def test_self_message_triggers_finding(self):
        """LU-W012 fires when sender == receiver."""
        proto = _protocol(
            "SelfMsg",
            roles=("alice", "bob"),
            steps=(_step("alice", "alice", line=2),),
            properties=(AlwaysTerminates(loc=_loc()),),
        )
        findings = lint_program(_program(proto))
        w012 = _find(findings, "LU-W012")
        assert len(w012) == 1
        assert w012[0].severity == LintSeverity.ERROR
        assert w012[0].category == LintCategory.CORRECTNESS
        assert "alice" in w012[0].message
        assert w012[0].line == 2

    def test_self_message_inside_branch(self):
        """LU-W012 detects self-message inside a choice branch."""
        bad_step = _step("bob", "bob", line=4)
        b1 = _branch("ok", steps=(bad_step,), line=3)
        b2 = _branch("also_ok", steps=(_step("alice", "bob"),), line=5)
        choice = _choice("alice", branches=(b1, b2), line=2)
        proto = _protocol(
            "BranchSelf",
            roles=("alice", "bob"),
            steps=(choice,),
            properties=(AlwaysTerminates(loc=_loc()),),
        )
        findings = lint_program(_program(proto))
        assert _find(findings, "LU-W012")

    def test_no_self_message_no_finding(self):
        """LU-W012 does NOT fire when sender and receiver are always different."""
        proto = _protocol(
            "NoSelf",
            roles=("alice", "bob"),
            steps=(
                _step("alice", "bob"),
                _step("bob", "alice"),
            ),
            properties=(AlwaysTerminates(loc=_loc()),),
        )
        findings = lint_program(_program(proto))
        assert not _find(findings, "LU-W012")

    # --- LU-W013: duplicate_branch_label ---

    def test_duplicate_branch_label_triggers_finding(self):
        """LU-W013 fires when two branches share the same label."""
        b1 = _branch("approve", steps=(_step("alice", "bob"),), line=3)
        b2 = _branch("approve", steps=(_step("bob", "alice"),), line=4)
        choice = _choice("alice", branches=(b1, b2), line=2)
        proto = _protocol(
            "DupLabel",
            roles=("alice", "bob"),
            steps=(choice,),
            properties=(AlwaysTerminates(loc=_loc()),),
        )
        findings = lint_program(_program(proto))
        w013 = _find(findings, "LU-W013")
        assert len(w013) == 1
        assert w013[0].severity == LintSeverity.ERROR
        assert w013[0].category == LintCategory.CORRECTNESS
        assert "approve" in w013[0].message
        assert "alice" in w013[0].message

    def test_duplicate_branch_label_nested(self):
        """LU-W013 fires for duplicate labels in a nested choice."""
        inner_b1 = _branch("yes", steps=(_step("bob", "carol"),), line=5)
        inner_b2 = _branch("yes", steps=(_step("carol", "bob"),), line=6)
        inner_choice = _choice("bob", branches=(inner_b1, inner_b2), line=4)
        outer_b = _branch("proceed", steps=(_step("alice", "bob"), inner_choice), line=3)
        outer_choice = _choice("alice", branches=(outer_b,), line=2)
        proto = _protocol(
            "NestedDupLabel",
            roles=("alice", "bob", "carol"),
            steps=(outer_choice,),
            properties=(AlwaysTerminates(loc=_loc()),),
        )
        findings = lint_program(_program(proto))
        assert _find(findings, "LU-W013")

    def test_unique_branch_labels_no_finding(self):
        """LU-W013 does NOT fire when all branch labels are distinct."""
        b1 = _branch("approve", steps=(_step("alice", "bob"),), line=3)
        b2 = _branch("reject", steps=(_step("bob", "alice"),), line=4)
        b3 = _branch("defer", steps=(_step("alice", "bob"),), line=5)
        choice = _choice("alice", branches=(b1, b2, b3), line=2)
        proto = _protocol(
            "UniqueLabels",
            roles=("alice", "bob"),
            steps=(choice,),
            properties=(AlwaysTerminates(loc=_loc()),),
        )
        findings = lint_program(_program(proto))
        assert not _find(findings, "LU-W013")

    # --- LU-W014: undefined_role_in_step ---

    def test_undefined_sender_triggers_finding(self):
        """LU-W014 fires when step sender is not in the declared roles."""
        proto = _protocol(
            "BadSender",
            roles=("alice", "bob"),
            steps=(_step("carol", "bob", line=2),),
            properties=(AlwaysTerminates(loc=_loc()),),
        )
        findings = lint_program(_program(proto))
        w014 = _find(findings, "LU-W014")
        assert len(w014) == 1
        assert "carol" in w014[0].message
        assert "sender" in w014[0].message

    def test_undefined_receiver_triggers_finding(self):
        """LU-W014 fires when step receiver is not in the declared roles."""
        proto = _protocol(
            "BadReceiver",
            roles=("alice", "bob"),
            steps=(_step("alice", "carol", line=2),),
            properties=(AlwaysTerminates(loc=_loc()),),
        )
        findings = lint_program(_program(proto))
        w014 = _find(findings, "LU-W014")
        assert len(w014) == 1
        assert "carol" in w014[0].message
        assert "receiver" in w014[0].message

    def test_undefined_choice_decider_triggers_finding(self):
        """LU-W014 fires when choice decider is not in the declared roles."""
        b1 = _branch("yes", steps=(_step("alice", "bob"),), line=3)
        choice = _choice("ghost", branches=(b1,), line=2)
        proto = _protocol(
            "BadDecider",
            roles=("alice", "bob"),
            steps=(choice,),
            properties=(AlwaysTerminates(loc=_loc()),),
        )
        findings = lint_program(_program(proto))
        w014 = _find(findings, "LU-W014")
        assert len(w014) == 1
        assert "ghost" in w014[0].message
        assert "decider" in w014[0].message

    def test_undefined_role_message_shows_declared_roles(self):
        """LU-W014 message lists declared roles to aid fixing."""
        proto = _protocol(
            "ShowDeclared",
            roles=("alice", "bob"),
            steps=(_step("carol", "bob", line=2),),
            properties=(AlwaysTerminates(loc=_loc()),),
        )
        findings = lint_program(_program(proto))
        w014 = _find(findings, "LU-W014")
        assert w014
        # Message should show declared roles
        assert "alice" in w014[0].message or "bob" in w014[0].message

    def test_all_roles_defined_no_finding(self):
        """LU-W014 does NOT fire when all roles in steps are declared."""
        b1 = _branch("yes", steps=(_step("alice", "bob"),), line=3)
        b2 = _branch("no", steps=(_step("bob", "alice"),), line=4)
        choice = _choice("alice", branches=(b1, b2), line=2)
        proto = _protocol(
            "AllDefined",
            roles=("alice", "bob"),
            steps=(choice,),
            properties=(AlwaysTerminates(loc=_loc()),),
        )
        findings = lint_program(_program(proto))
        assert not _find(findings, "LU-W014")

    # --- Clean protocol: zero correctness findings ---

    def test_clean_protocol_no_correctness_findings(self):
        """A well-formed protocol produces zero ERROR findings."""
        b1 = _branch("approve", steps=(_step("bob", "alice"),), line=3)
        b2 = _branch("reject", steps=(_step("bob", "alice", payload="decline"),), line=4)
        choice = _choice("bob", branches=(b1, b2), line=2)
        proto = _protocol(
            "CleanProtocol",
            roles=("alice", "bob"),
            steps=(_step("alice", "bob"), choice),
            properties=(AlwaysTerminates(loc=_loc()), NoDeadlock(loc=_loc())),
        )
        findings = lint_program(_program(proto))
        errors = [f for f in findings if f.severity == LintSeverity.ERROR]
        assert not errors


# ============================================================
# TestStyle
# ============================================================


class TestStyle:
    """Tests for WARNING-severity style rules."""

    # --- LU-W002: protocol_name_convention ---

    def test_snake_case_name_triggers_w002(self):
        """LU-W002 fires for snake_case protocol name."""
        proto = _protocol(
            "bad_name",
            roles=("alice", "bob"),
            steps=(_step("alice", "bob"), _step("bob", "alice")),
            properties=(AlwaysTerminates(loc=_loc()),),
        )
        findings = lint_program(_program(proto))
        w002 = _find(findings, "LU-W002")
        assert len(w002) == 1
        assert w002[0].severity == LintSeverity.WARNING
        assert w002[0].category == LintCategory.STYLE
        assert "bad_name" in w002[0].message
        assert "PascalCase" in w002[0].message

    def test_lowercase_name_triggers_w002(self):
        """LU-W002 fires for all-lowercase protocol name."""
        proto = _protocol(
            "mybadprotocol",
            roles=("alice", "bob"),
            steps=(_step("alice", "bob"), _step("bob", "alice")),
            properties=(AlwaysTerminates(loc=_loc()),),
        )
        findings = lint_program(_program(proto))
        assert _find(findings, "LU-W002")

    def test_camel_case_without_leading_capital_triggers_w002(self):
        """LU-W002 fires for camelCase (not PascalCase)."""
        proto = _protocol(
            "myProtocol",
            roles=("alice", "bob"),
            steps=(_step("alice", "bob"), _step("bob", "alice")),
            properties=(AlwaysTerminates(loc=_loc()),),
        )
        findings = lint_program(_program(proto))
        assert _find(findings, "LU-W002")

    def test_pascal_case_name_no_w002(self):
        """LU-W002 does NOT fire for valid PascalCase names."""
        for name in ("MyProtocol", "OrderRequest", "A", "AB2Protocol"):
            proto = _protocol(
                name,
                roles=("alice", "bob"),
                steps=(_step("alice", "bob"), _step("bob", "alice")),
                properties=(AlwaysTerminates(loc=_loc()),),
            )
            findings = lint_program(_program(proto))
            assert not _find(findings, "LU-W002"), f"False positive for name '{name}'"

    # --- LU-W005: single_step_protocol ---

    def test_single_step_triggers_w005(self):
        """LU-W005 fires when a protocol has exactly one step."""
        proto = _protocol(
            "OneStep",
            roles=("alice", "bob"),
            steps=(_step("alice", "bob"),),
            properties=(AlwaysTerminates(loc=_loc()),),
        )
        findings = lint_program(_program(proto))
        w005 = _find(findings, "LU-W005")
        assert len(w005) == 1
        assert w005[0].severity == LintSeverity.WARNING
        assert w005[0].category == LintCategory.STYLE
        assert "OneStep" in w005[0].message
        assert "1 step" in w005[0].message

    def test_two_steps_no_w005(self):
        """LU-W005 does NOT fire when protocol has two or more steps."""
        proto = _protocol(
            "TwoSteps",
            roles=("alice", "bob"),
            steps=(_step("alice", "bob"), _step("bob", "alice")),
            properties=(AlwaysTerminates(loc=_loc()),),
        )
        findings = lint_program(_program(proto))
        assert not _find(findings, "LU-W005")

    def test_single_step_with_choice_no_w005(self):
        """LU-W005 does NOT fire when the single top-level item is a choice (total steps > 1)."""
        b1 = _branch("yes", steps=(_step("alice", "bob"),), line=3)
        b2 = _branch("no", steps=(_step("bob", "alice"),), line=4)
        choice = _choice("alice", branches=(b1, b2), line=2)
        proto = _protocol(
            "ChoiceProtocol",
            roles=("alice", "bob"),
            steps=(choice,),
            properties=(AlwaysTerminates(loc=_loc()),),
        )
        findings = lint_program(_program(proto))
        # choice with 2 total steps but 1 top-level item: W005 checks
        # len(all_steps)==1 AND len(node.steps)==1, so here all_steps==2
        assert not _find(findings, "LU-W005")


# ============================================================
# TestBestPractices
# ============================================================


class TestBestPractices:
    """Tests for WARNING-severity best practice rules."""

    # --- LU-W020: no_properties_declared ---

    def test_no_properties_triggers_w020(self):
        """LU-W020 fires when a protocol declares no properties."""
        proto = _protocol(
            "NoProp",
            roles=("alice", "bob"),
            steps=(_step("alice", "bob"), _step("bob", "alice")),
            properties=(),
        )
        findings = lint_program(_program(proto))
        w020 = _find(findings, "LU-W020")
        assert len(w020) == 1
        assert w020[0].severity == LintSeverity.WARNING
        assert w020[0].category == LintCategory.BEST_PRACTICES
        assert "NoProp" in w020[0].message
        assert "properties" in w020[0].message

    def test_with_properties_no_w020(self):
        """LU-W020 does NOT fire when at least one property is declared."""
        proto = _protocol(
            "HasProps",
            roles=("alice", "bob"),
            steps=(_step("alice", "bob"), _step("bob", "alice")),
            properties=(AlwaysTerminates(loc=_loc()), NoDeadlock(loc=_loc())),
        )
        findings = lint_program(_program(proto))
        assert not _find(findings, "LU-W020")

    # --- LU-W022: deep_nesting ---

    def test_depth_4_triggers_w022(self):
        """LU-W022 fires when nesting exceeds 3 levels."""
        # Build 4-level nesting: choice > branch > choice > branch > choice > branch > choice
        innermost = _choice(
            "carol",
            branches=(_branch("deep", steps=(_step("carol", "dave"),), line=8),),
            line=7,
        )
        level3_branch = _branch("l3", steps=(_step("carol", "dave"), innermost), line=6)
        level3_choice = _choice("carol", branches=(level3_branch,), line=5)
        level2_branch = _branch("l2", steps=(_step("bob", "carol"), level3_choice), line=4)
        level2_choice = _choice("bob", branches=(level2_branch,), line=3)
        level1_branch = _branch("l1", steps=(_step("alice", "bob"), level2_choice), line=2)
        level1_choice = _choice("alice", branches=(level1_branch,), line=1)
        proto = _protocol(
            "DeepNest",
            roles=("alice", "bob", "carol", "dave"),
            steps=(level1_choice,),
            properties=(AlwaysTerminates(loc=_loc()),),
        )
        findings = lint_program(_program(proto))
        w022 = _find(findings, "LU-W022")
        assert w022
        assert w022[0].severity == LintSeverity.WARNING
        assert w022[0].category == LintCategory.BEST_PRACTICES
        assert "DeepNest" in w022[0].message

    def test_depth_3_no_w022(self):
        """LU-W022 does NOT fire at exactly 3 levels (the allowed max)."""
        inner = _choice(
            "carol",
            branches=(_branch("c", steps=(_step("carol", "bob"),), line=5),),
            line=4,
        )
        mid_branch = _branch("b", steps=(_step("bob", "carol"), inner), line=3)
        mid_choice = _choice("bob", branches=(mid_branch,), line=2)
        outer_branch = _branch("a", steps=(_step("alice", "bob"), mid_choice), line=1)
        outer_choice = _choice("alice", branches=(outer_branch,), line=1)
        proto = _protocol(
            "ThreeLevels",
            roles=("alice", "bob", "carol"),
            steps=(outer_choice,),
            properties=(AlwaysTerminates(loc=_loc()),),
        )
        findings = lint_program(_program(proto))
        assert not _find(findings, "LU-W022")

    def test_flat_protocol_no_w022(self):
        """LU-W022 does NOT fire for protocols with no nesting."""
        proto = _protocol(
            "Flat",
            roles=("alice", "bob"),
            steps=(_step("alice", "bob"), _step("bob", "alice")),
            properties=(AlwaysTerminates(loc=_loc()),),
        )
        findings = lint_program(_program(proto))
        assert not _find(findings, "LU-W022")

    # --- LU-W024: agent_no_trust ---

    def test_agent_without_trust_triggers_w024(self):
        """LU-W024 fires when an agent has no explicit trust tier."""
        agent = _agent("my_worker", trust=None, line=5)
        findings = lint_program(_program(agent))
        w024 = _find(findings, "LU-W024")
        assert len(w024) == 1
        assert w024[0].severity == LintSeverity.WARNING
        assert w024[0].category == LintCategory.BEST_PRACTICES
        assert "my_worker" in w024[0].message
        assert "trust" in w024[0].message

    def test_agent_with_trust_no_w024(self):
        """LU-W024 does NOT fire when agent has an explicit trust tier."""
        for tier in ("verified", "trusted", "standard", "untrusted"):
            agent = _agent("my_worker", trust=tier)
            findings = lint_program(_program(agent))
            assert not _find(findings, "LU-W024"), f"False positive for trust='{tier}'"

    # --- Well-configured protocol: zero best practice warnings ---

    def test_well_configured_protocol_no_best_practice_warnings(self):
        """A fully configured protocol produces zero BEST PRACTICES warnings."""
        b1 = _branch("approve", steps=(_step("bob", "alice"),), line=3)
        b2 = _branch("reject", steps=(_step("bob", "alice", payload="decline"),), line=4)
        choice = _choice("bob", branches=(b1, b2), line=2)
        proto = _protocol(
            "WellConfigured",
            roles=("alice", "bob"),
            steps=(_step("alice", "bob"), choice),
            properties=(AlwaysTerminates(loc=_loc()), NoDeadlock(loc=_loc())),
        )
        findings = lint_program(_program(proto))
        bp_warnings = [
            f for f in findings if f.category == LintCategory.BEST_PRACTICES
        ]
        assert not bp_warnings


# ============================================================
# TestLintSource
# ============================================================


class TestLintSource:
    """Tests for lint_source() with real LU source code."""

    def test_lint_source_self_message(self):
        """lint_source detects self-message (LU-W012) in real source."""
        source = textwrap.dedent("""\
            protocol Bad:
                roles: alice, bob
                alice asks alice to do task
                properties:
                    always terminates
        """)
        findings = lint_source(source)
        assert any(f.code == "LU-W012" for f in findings)

    def test_lint_source_non_pascal_name(self):
        """lint_source detects LU-W002 for non-PascalCase protocol name."""
        source = textwrap.dedent("""\
            protocol bad_name:
                roles: alice, bob
                alice asks bob to do task
                bob returns result to alice
                properties:
                    always terminates
        """)
        findings = lint_source(source)
        assert any(f.code == "LU-W002" for f in findings)

    def test_lint_source_no_properties(self):
        """lint_source detects LU-W020 for missing properties block."""
        source = textwrap.dedent("""\
            protocol Simple:
                roles: alice, bob
                alice asks bob to do task
                bob returns result to alice
        """)
        findings = lint_source(source)
        assert any(f.code == "LU-W020" for f in findings)

    def test_lint_source_clean_protocol(self):
        """lint_source returns no ERROR findings for a well-formed protocol."""
        source = textwrap.dedent("""\
            protocol TaskRequest:
                roles: client, server
                client asks server to do task
                server returns result to client
                properties:
                    always terminates
                    no deadlock
        """)
        findings = lint_source(source)
        errors = [f for f in findings if f.severity == LintSeverity.ERROR]
        assert not errors

    def test_lint_source_duplicate_role(self):
        """lint_source detects LU-W010 for duplicate role declaration."""
        source = textwrap.dedent("""\
            protocol DupRole:
                roles: alice, bob, alice
                alice asks bob to do task
                bob returns result to alice
                properties:
                    always terminates
        """)
        findings = lint_source(source)
        assert any(f.code == "LU-W010" for f in findings)

    def test_lint_source_single_step(self):
        """lint_source detects LU-W005 for a protocol with one step."""
        source = textwrap.dedent("""\
            protocol Ping:
                roles: client, server
                client asks server to ping
                properties:
                    always terminates
        """)
        findings = lint_source(source)
        assert any(f.code == "LU-W005" for f in findings)

    def test_lint_source_returns_sorted_findings(self):
        """lint_source results are sorted by (line, col, code)."""
        source = textwrap.dedent("""\
            protocol bad_name:
                roles: alice, bob
                alice asks bob to do task
                bob returns result to alice
        """)
        findings = lint_source(source)
        lines = [f.line for f in findings]
        assert lines == sorted(lines)

    def test_lint_source_source_file_label(self):
        """lint_source passes source_file label into findings context (no error)."""
        source = textwrap.dedent("""\
            protocol Simple:
                roles: alice, bob
                alice asks bob to do task
                bob returns result to alice
        """)
        # Just verifying it doesn't raise; label is on context not findings directly
        findings = lint_source(source, source_file="myfile.lu")
        assert isinstance(findings, list)


# ============================================================
# TestLintFile
# ============================================================


class TestLintFile:
    """Tests for lint_file() with a temporary .lu file."""

    def test_lint_file_reads_and_lints(self, tmp_path):
        """lint_file reads the file and returns findings."""
        lu_file = tmp_path / "test.lu"
        lu_file.write_text(
            textwrap.dedent("""\
                protocol Simple:
                    roles: alice, bob
                    alice asks bob to do task
                    bob returns result to alice
            """),
            encoding="utf-8",
        )
        findings = lint_file(lu_file)
        # No properties -> LU-W020 expected
        assert any(f.code == "LU-W020" for f in findings)

    def test_lint_file_with_path_string(self, tmp_path):
        """lint_file accepts a str path, not just Path."""
        lu_file = tmp_path / "str_path.lu"
        lu_file.write_text(
            textwrap.dedent("""\
                protocol Simple:
                    roles: alice, bob
                    alice asks bob to do task
                    bob returns result to alice
            """),
            encoding="utf-8",
        )
        findings = lint_file(str(lu_file))
        assert isinstance(findings, list)

    def test_lint_file_clean_protocol(self, tmp_path):
        """lint_file returns no ERROR findings for a clean file."""
        lu_file = tmp_path / "clean.lu"
        lu_file.write_text(
            textwrap.dedent("""\
                protocol CleanFile:
                    roles: client, server
                    client asks server to do task
                    server returns result to client
                    properties:
                        always terminates
                        no deadlock
            """),
            encoding="utf-8",
        )
        findings = lint_file(lu_file)
        errors = [f for f in findings if f.severity == LintSeverity.ERROR]
        assert not errors


# ============================================================
# TestIgnore
# ============================================================


class TestIgnore:
    """Tests that the ignore parameter correctly filters findings."""

    def test_ignore_single_code(self):
        """Passing ignore={code} removes that finding from results."""
        proto = _protocol(
            "bad_name",
            roles=("alice", "bob"),
            steps=(_step("alice", "bob"), _step("bob", "alice")),
            properties=(AlwaysTerminates(loc=_loc()),),
        )
        # Without ignore: W002 is present
        findings_full = lint_program(_program(proto))
        assert _find(findings_full, "LU-W002")

        # With ignore: W002 is absent
        findings_ignored = lint_program(_program(proto), ignore=frozenset({"LU-W002"}))
        assert not _find(findings_ignored, "LU-W002")

    def test_ignore_multiple_codes(self):
        """Passing multiple codes in ignore filters all of them."""
        proto = _protocol(
            "bad_name",
            roles=("alice", "bob"),
            steps=(_step("alice", "bob"),),
            properties=(),
        )
        findings = lint_program(
            _program(proto),
            ignore=frozenset({"LU-W002", "LU-W005", "LU-W020"}),
        )
        remaining_codes = {f.code for f in findings}
        assert "LU-W002" not in remaining_codes
        assert "LU-W005" not in remaining_codes
        assert "LU-W020" not in remaining_codes

    def test_ignore_nonexistent_code_no_error(self):
        """Passing an unknown code in ignore does not raise."""
        proto = _protocol(
            "MyProto",
            roles=("alice", "bob"),
            steps=(_step("alice", "bob"), _step("bob", "alice")),
            properties=(AlwaysTerminates(loc=_loc()),),
        )
        findings = lint_program(_program(proto), ignore=frozenset({"LU-W999"}))
        assert isinstance(findings, list)

    def test_ignore_in_lint_source(self):
        """ignore parameter works in lint_source()."""
        source = textwrap.dedent("""\
            protocol Simple:
                roles: alice, bob
                alice asks bob to do task
                bob returns result to alice
        """)
        # Without ignore: LU-W020 fires (no properties)
        findings_full = lint_source(source)
        assert _find(findings_full, "LU-W020")
        # With ignore: LU-W020 is filtered out
        findings = lint_source(source, ignore=frozenset({"LU-W020"}))
        assert not _find(findings, "LU-W020")

    def test_ignore_in_lint_file(self, tmp_path):
        """ignore parameter works in lint_file()."""
        lu_file = tmp_path / "ignore_test.lu"
        lu_file.write_text(
            textwrap.dedent("""\
                protocol Simple:
                    roles: alice, bob
                    alice asks bob to do task
                    bob returns result to alice
            """),
            encoding="utf-8",
        )
        # Verify LU-W020 fires without ignore
        findings_full = lint_file(lu_file)
        assert _find(findings_full, "LU-W020")
        # With ignore: filtered
        findings = lint_file(lu_file, ignore=frozenset({"LU-W020"}))
        assert not _find(findings, "LU-W020")


# ============================================================
# TestCLI
# ============================================================


class TestCLI:
    """Tests for the lu lint CLI command."""

    def _run_lu(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, "-m", "cervellaswarm_lingua_universale", *args],
            capture_output=True,
            text=True,
        )

    def test_cli_lint_clean_file_exit_0(self, tmp_path):
        """lu lint on a clean file exits with code 0."""
        lu_file = tmp_path / "clean.lu"
        lu_file.write_text(
            textwrap.dedent("""\
                protocol CleanCli:
                    roles: client, server
                    client asks server to do task
                    server returns result to client
                    properties:
                        always terminates
                        no deadlock
            """),
            encoding="utf-8",
        )
        result = self._run_lu("lint", str(lu_file))
        assert result.returncode == 0

    def test_cli_lint_error_file_exit_1(self, tmp_path):
        """lu lint on a file with ERROR findings exits with code 1."""
        lu_file = tmp_path / "bad.lu"
        lu_file.write_text(
            textwrap.dedent("""\
                protocol SelfMsg:
                    roles: alice, bob
                    alice asks alice to do task
                    properties:
                        always terminates
            """),
            encoding="utf-8",
        )
        result = self._run_lu("lint", str(lu_file))
        assert result.returncode == 1

    def test_cli_lint_output_contains_code(self, tmp_path):
        """lu lint output prints the finding code."""
        lu_file = tmp_path / "code_output.lu"
        lu_file.write_text(
            textwrap.dedent("""\
                protocol SelfMsg:
                    roles: alice, bob
                    alice asks alice to do task
                    properties:
                        always terminates
            """),
            encoding="utf-8",
        )
        result = self._run_lu("lint", str(lu_file))
        output = result.stdout + result.stderr
        assert "LU-W012" in output

    def test_cli_lint_warnings_only_exit_0(self, tmp_path):
        """lu lint exits 0 when only WARNING findings are present (no ERRORs)."""
        lu_file = tmp_path / "warnings_only.lu"
        lu_file.write_text(
            textwrap.dedent("""\
                protocol Simple:
                    roles: alice, bob
                    alice asks bob to do task
                    bob returns result to alice
            """),
            encoding="utf-8",
        )
        result = self._run_lu("lint", str(lu_file))
        # LU-W020 (no properties) is WARNING; exit should be 0
        assert result.returncode == 0
