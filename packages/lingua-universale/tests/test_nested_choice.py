# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for nested choice support in Lingua Universale (LU 1.1).

Nested choice allows ``when X decides:`` blocks inside branch bodies,
enabling protocols like saga-with-compensation and auth-with-retry.
This is standard in MPST/Scribble and was restricted in LU 1.0.

Covers: parser, AST, compiler, protocols, spec checkers, grammar export.
"""

from __future__ import annotations

import textwrap

import pytest

from cervellaswarm_lingua_universale._ast import (
    BranchNode,
    ChoiceNode,
    StepNode,
)
from cervellaswarm_lingua_universale._compiler import ASTCompiler
from cervellaswarm_lingua_universale._grammar_export import GrammarExporter
from cervellaswarm_lingua_universale._parser import ParseError, parse
from cervellaswarm_lingua_universale.protocols import (
    Protocol,
    ProtocolChoice,
    ProtocolStep,
)
from cervellaswarm_lingua_universale.spec import (
    PropertyKind,
    PropertySpec,
    PropertyVerdict,
    ProtocolSpec,
    _collect_all_paths,
    _collect_all_steps,
    check_properties,
)
from cervellaswarm_lingua_universale.types import MessageKind


# ============================================================
# Shared LU source fixtures
# ============================================================

SAGA_ORDER_LU = textwrap.dedent("""\
    protocol SagaOrder:
        roles: coordinator, payment, inventory

        coordinator asks payment to do task
        when payment decides:
            success:
                payment returns confirmation to coordinator
                coordinator asks inventory to do task
                when inventory decides:
                    reserved:
                        inventory returns reservation to coordinator
                    out_of_stock:
                        inventory returns error to coordinator
                        coordinator tells payment refund order
            failure:
                payment returns error to coordinator
""")

AUTH_RETRY_LU = textwrap.dedent("""\
    protocol AuthRetry:
        roles: client, server

        client sends credentials to server
        when server decides:
            valid:
                server returns token to client
            invalid:
                server returns error to client
                when client decides:
                    retry:
                        client sends credentials to server
                    give_up:
                        client tells server quit session
""")

TRIPLE_NESTED_LU = textwrap.dedent("""\
    protocol TripleNested:
        roles: a, b, c

        a asks b to do task
        when a decides:
            branch1:
                a tells b start level1
                when b decides:
                    inner1:
                        b tells c start level2
                        when c decides:
                            deep1:
                                c returns result to a
                            deep2:
                                c returns error to a
                    inner2:
                        b returns result to a
            branch2:
                a returns result to b
""")


# ============================================================
# Parser tests
# ============================================================


class TestParser:
    """Parser tests for nested choice."""

    def test_nested_choice_parses(self):
        """Two-level nested choice (saga pattern) parses correctly."""
        prog = parse(SAGA_ORDER_LU)
        proto = prog.declarations[0]
        assert proto.name == "SagaOrder"

        # Find the outer choice
        outer_choice = proto.steps[1]
        assert isinstance(outer_choice, ChoiceNode)
        assert outer_choice.decider == "payment"
        assert len(outer_choice.branches) == 2

        # "success" branch has steps + nested choice
        success = outer_choice.branches[0]
        assert success.label == "success"
        assert len(success.steps) == 3  # step, step, nested choice

        # Last item in success branch is nested choice
        inner_choice = success.steps[2]
        assert isinstance(inner_choice, ChoiceNode)
        assert inner_choice.decider == "inventory"
        assert len(inner_choice.branches) == 2

        # "reserved" inner branch
        reserved = inner_choice.branches[0]
        assert reserved.label == "reserved"
        assert len(reserved.steps) == 1
        assert isinstance(reserved.steps[0], StepNode)

        # "out_of_stock" inner branch has 2 steps
        out_of_stock = inner_choice.branches[1]
        assert out_of_stock.label == "out_of_stock"
        assert len(out_of_stock.steps) == 2

        # "failure" branch is flat (no nested choice)
        failure = outer_choice.branches[1]
        assert failure.label == "failure"
        assert len(failure.steps) == 1
        assert isinstance(failure.steps[0], StepNode)

    def test_auth_retry_parses(self):
        """Auth-with-retry pattern: nested choice in 'invalid' branch."""
        prog = parse(AUTH_RETRY_LU)
        proto = prog.declarations[0]
        assert proto.name == "AuthRetry"

        choice = proto.steps[1]
        assert isinstance(choice, ChoiceNode)
        assert choice.decider == "server"

        # "invalid" branch has step + nested choice
        invalid = choice.branches[1]
        assert invalid.label == "invalid"
        assert len(invalid.steps) == 2
        assert isinstance(invalid.steps[0], StepNode)
        assert isinstance(invalid.steps[1], ChoiceNode)
        assert invalid.steps[1].decider == "client"

    def test_triple_nested_parses(self):
        """Three levels of nesting parse correctly."""
        prog = parse(TRIPLE_NESTED_LU)
        proto = prog.declarations[0]
        assert proto.name == "TripleNested"

        # Level 1
        level1 = proto.steps[1]
        assert isinstance(level1, ChoiceNode)
        assert level1.decider == "a"

        # Level 2 (inside branch1)
        branch1 = level1.branches[0]
        level2 = branch1.steps[1]
        assert isinstance(level2, ChoiceNode)
        assert level2.decider == "b"

        # Level 3 (inside inner1)
        inner1 = level2.branches[0]
        level3 = inner1.steps[1]
        assert isinstance(level3, ChoiceNode)
        assert level3.decider == "c"
        assert len(level3.branches) == 2

    def test_mixed_steps_and_nested_choice(self):
        """Branch with steps before AND after a nested choice."""
        src = textwrap.dedent("""\
            protocol Mixed:
                roles: a, b, c

                when a decides:
                    path1:
                        a tells b start phase
                        when b decides:
                            ok:
                                b returns result to a
                            fail:
                                b returns error to a
                        a tells c end phase
                    path2:
                        a returns result to b
        """)
        prog = parse(src)
        proto = prog.declarations[0]
        choice = proto.steps[0]
        path1 = choice.branches[0]

        # 3 items: step, nested choice, step
        assert len(path1.steps) == 3
        assert isinstance(path1.steps[0], StepNode)
        assert isinstance(path1.steps[1], ChoiceNode)
        assert isinstance(path1.steps[2], StepNode)

    def test_empty_nested_branch_rejected(self):
        """Empty nested branch body raises ParseError."""
        src = textwrap.dedent("""\
            protocol Bad:
                roles: a, b

                when a decides:
                    ok:
                        a tells b hello
                        when b decides:
                            inner:
                    fail:
                        a returns error to b
        """)
        with pytest.raises(ParseError):
            parse(src)

    def test_existing_flat_protocols_still_parse(self):
        """Flat protocols (no nested choice) continue to work."""
        src = textwrap.dedent("""\
            protocol Flat:
                roles: a, b

                a asks b to do task
                b returns result to a
        """)
        prog = parse(src)
        proto = prog.declarations[0]
        assert len(proto.steps) == 2
        assert all(isinstance(s, StepNode) for s in proto.steps)


# ============================================================
# Compiler tests
# ============================================================


class TestCompiler:
    """Compiler tests for nested choice -> Protocol runtime object."""

    def test_nested_choice_compiles_to_protocol(self):
        """Nested choice compiles to Protocol with nested ProtocolChoice."""
        prog = parse(SAGA_ORDER_LU)
        compiler = ASTCompiler()
        protocol = compiler._ast_to_protocol(prog.declarations[0])

        assert protocol.name == "SagaOrder"
        assert len(protocol.elements) == 2  # step + outer choice

        outer = protocol.elements[1]
        assert isinstance(outer, ProtocolChoice)
        assert outer.decider == "payment"

        # "success" branch has 2 steps + 1 nested choice
        success_elems = outer.branches["success"]
        assert len(success_elems) == 3

        inner = success_elems[2]
        assert isinstance(inner, ProtocolChoice)
        assert inner.decider == "inventory"
        assert "reserved" in inner.branches
        assert "out_of_stock" in inner.branches

        # "out_of_stock" has 2 steps
        oos = inner.branches["out_of_stock"]
        assert len(oos) == 2
        assert all(isinstance(s, ProtocolStep) for s in oos)

    def test_nested_choice_codegen_produces_python(self):
        """Full codegen pipeline with nested choice produces valid Python."""
        prog = parse(SAGA_ORDER_LU)
        compiler = ASTCompiler()
        result = compiler.compile(prog, source_file="saga.lu")

        assert "SagaOrderSession" in result.python_source
        assert result.protocols == ("SagaOrder",)

        # Verify the Python source is syntactically valid
        compile(result.python_source, "saga.lu", "exec")

    def test_triple_nested_codegen(self):
        """Triple nesting compiles and generates valid Python."""
        prog = parse(TRIPLE_NESTED_LU)
        compiler = ASTCompiler()
        result = compiler.compile(prog, source_file="triple.lu")

        compile(result.python_source, "triple.lu", "exec")


# ============================================================
# Protocol validation tests
# ============================================================


class TestProtocol:
    """Protocol runtime object tests with nested choices."""

    def test_nested_protocol_choice_validates(self):
        """Manually created Protocol with nested ProtocolChoice validates."""
        proto = Protocol(
            name="NestedTest",
            roles=("a", "b", "c"),
            elements=(
                ProtocolStep(
                    sender="a", receiver="b",
                    message_kind=MessageKind.TASK_REQUEST,
                ),
                ProtocolChoice(
                    decider="a",
                    branches={
                        "left": (
                            ProtocolStep(
                                sender="a", receiver="b",
                                message_kind=MessageKind.DM,
                            ),
                            ProtocolChoice(
                                decider="b",
                                branches={
                                    "inner_ok": (
                                        ProtocolStep(
                                            sender="b", receiver="c",
                                            message_kind=MessageKind.TASK_RESULT,
                                        ),
                                    ),
                                    "inner_fail": (
                                        ProtocolStep(
                                            sender="b", receiver="a",
                                            message_kind=MessageKind.TASK_RESULT,
                                        ),
                                    ),
                                },
                            ),
                        ),
                        "right": (
                            ProtocolStep(
                                sender="a", receiver="c",
                                message_kind=MessageKind.TASK_RESULT,
                            ),
                        ),
                    },
                ),
            ),
        )
        assert proto.name == "NestedTest"

    def test_nested_choice_invalid_role_rejected(self):
        """Nested choice with undeclared role raises ValueError."""
        with pytest.raises(ValueError, match="not in protocol roles"):
            Protocol(
                name="BadNested",
                roles=("a", "b"),
                elements=(
                    ProtocolChoice(
                        decider="a",
                        branches={
                            "ok": (
                                ProtocolStep(
                                    sender="a", receiver="b",
                                    message_kind=MessageKind.DM,
                                ),
                                ProtocolChoice(
                                    decider="b",
                                    branches={
                                        "inner": (
                                            ProtocolStep(
                                                sender="c",  # undeclared!
                                                receiver="a",
                                                message_kind=MessageKind.DM,
                                            ),
                                        ),
                                    },
                                ),
                            ),
                        },
                    ),
                ),
            )

    def test_nested_choice_invalid_decider_rejected(self):
        """Nested choice with undeclared decider raises ValueError."""
        with pytest.raises(ValueError, match="not in protocol roles"):
            Protocol(
                name="BadDecider",
                roles=("a", "b"),
                elements=(
                    ProtocolChoice(
                        decider="a",
                        branches={
                            "ok": (
                                ProtocolChoice(
                                    decider="z",  # undeclared!
                                    branches={
                                        "inner": (
                                            ProtocolStep(
                                                sender="a", receiver="b",
                                                message_kind=MessageKind.DM,
                                            ),
                                        ),
                                    },
                                ),
                            ),
                        },
                    ),
                ),
            )


# ============================================================
# spec.py tests
# ============================================================


class TestSpec:
    """Spec checker tests for nested choices."""

    @pytest.fixture()
    def nested_protocol(self):
        """Protocol with nested choice for spec tests."""
        return Protocol(
            name="NestedSpec",
            roles=("coordinator", "payment", "inventory"),
            elements=(
                ProtocolStep(
                    sender="coordinator", receiver="payment",
                    message_kind=MessageKind.TASK_REQUEST,
                ),
                ProtocolChoice(
                    decider="payment",
                    branches={
                        "success": (
                            ProtocolStep(
                                sender="payment", receiver="coordinator",
                                message_kind=MessageKind.TASK_RESULT,
                            ),
                            ProtocolStep(
                                sender="coordinator", receiver="inventory",
                                message_kind=MessageKind.TASK_REQUEST,
                            ),
                            ProtocolChoice(
                                decider="inventory",
                                branches={
                                    "reserved": (
                                        ProtocolStep(
                                            sender="inventory",
                                            receiver="coordinator",
                                            message_kind=MessageKind.TASK_RESULT,
                                        ),
                                    ),
                                    "out_of_stock": (
                                        ProtocolStep(
                                            sender="inventory",
                                            receiver="coordinator",
                                            message_kind=MessageKind.DM,
                                        ),
                                        ProtocolStep(
                                            sender="coordinator",
                                            receiver="payment",
                                            message_kind=MessageKind.DM,
                                            description="refund",
                                        ),
                                    ),
                                },
                            ),
                        ),
                        "failure": (
                            ProtocolStep(
                                sender="payment", receiver="coordinator",
                                message_kind=MessageKind.DM,
                            ),
                        ),
                    },
                ),
            ),
        )

    def test_collect_all_steps_nested(self, nested_protocol):
        """_collect_all_steps includes steps from all nesting levels."""
        steps = _collect_all_steps(nested_protocol.elements)
        # 1 top-level + (2 success branch + 1 reserved + 2 out_of_stock) + 1 failure = 7
        assert len(steps) == 7
        senders = {s.sender for s in steps}
        assert senders == {"coordinator", "payment", "inventory"}

    def test_collect_all_paths_nested(self, nested_protocol):
        """_collect_all_paths expands nested choices into all execution paths."""
        paths = _collect_all_paths(nested_protocol.elements)
        # Paths: success->reserved, success->out_of_stock, failure = 3
        assert len(paths) == 3

        # success->reserved path: 1 + 2 + 1 = 4 steps
        reserved_path = [p for p in paths if len(p) == 4]
        assert len(reserved_path) == 1

        # success->out_of_stock path: 1 + 2 + 2 = 5 steps
        oos_path = [p for p in paths if len(p) == 5]
        assert len(oos_path) == 1

        # failure path: 1 + 1 = 2 steps
        fail_path = [p for p in paths if len(p) == 2]
        assert len(fail_path) == 1

    def test_ordering_across_nested_branches(self, nested_protocol):
        """ORDERING checker works across nested branches."""
        spec = ProtocolSpec(
            protocol_name="NestedSpec",
            properties=(
                PropertySpec(
                    kind=PropertyKind.ORDERING,
                    params=("task_request", "task_result"),
                ),
            ),
        )
        report = check_properties(nested_protocol, spec)
        assert report.results[0].verdict == PropertyVerdict.PROVED

    def test_exclusion_detects_nested_violation(self):
        """EXCLUSION detects violation deep inside nested choice."""
        proto = Protocol(
            name="ExclNested",
            roles=("a", "b", "c"),
            elements=(
                ProtocolChoice(
                    decider="a",
                    branches={
                        "outer_ok": (
                            ProtocolStep(
                                sender="a", receiver="b",
                                message_kind=MessageKind.DM,
                            ),
                            ProtocolChoice(
                                decider="b",
                                branches={
                                    "inner_bad": (
                                        ProtocolStep(
                                            sender="b", receiver="c",
                                            message_kind=MessageKind.AUDIT_VERDICT,
                                        ),
                                    ),
                                },
                            ),
                        ),
                    },
                ),
            ),
        )
        spec = ProtocolSpec(
            protocol_name="ExclNested",
            properties=(
                PropertySpec(
                    kind=PropertyKind.EXCLUSION,
                    params=("b", "audit_verdict"),
                ),
            ),
        )
        report = check_properties(proto, spec)
        assert report.results[0].verdict == PropertyVerdict.VIOLATED
        # Branch context preserved in evidence
        assert "inner_bad" in report.results[0].evidence

    def test_all_roles_participate_nested(self, nested_protocol):
        """ALL_ROLES_PARTICIPATE finds roles in nested branches."""
        spec = ProtocolSpec(
            protocol_name="NestedSpec",
            properties=(
                PropertySpec(kind=PropertyKind.ALL_ROLES_PARTICIPATE),
            ),
        )
        report = check_properties(nested_protocol, spec)
        assert report.results[0].verdict == PropertyVerdict.PROVED

    def test_role_exclusive_nested(self):
        """ROLE_EXCLUSIVE detects violations inside nested choice."""
        proto = Protocol(
            name="RoleExclNested",
            roles=("a", "b", "c"),
            elements=(
                ProtocolChoice(
                    decider="a",
                    branches={
                        "branch1": (
                            ProtocolChoice(
                                decider="b",
                                branches={
                                    "nested_bad": (
                                        ProtocolStep(
                                            sender="c", receiver="a",
                                            message_kind=MessageKind.DM,
                                        ),
                                    ),
                                },
                            ),
                        ),
                    },
                ),
            ),
        )
        spec = ProtocolSpec(
            protocol_name="RoleExclNested",
            properties=(
                PropertySpec(
                    kind=PropertyKind.ROLE_EXCLUSIVE,
                    params=("b", "dm"),
                ),
            ),
        )
        report = check_properties(proto, spec)
        assert report.results[0].verdict == PropertyVerdict.VIOLATED
        assert "nested_bad" in report.results[0].evidence

    def test_no_deletion_nested(self, nested_protocol):
        """NO_DELETION checks all nesting levels."""
        spec = ProtocolSpec(
            protocol_name="NestedSpec",
            properties=(
                PropertySpec(kind=PropertyKind.NO_DELETION),
            ),
        )
        report = check_properties(nested_protocol, spec)
        assert report.results[0].verdict == PropertyVerdict.PROVED

    def test_always_terminates_nested(self, nested_protocol):
        """ALWAYS_TERMINATES holds for nested protocols (finite by construction)."""
        spec = ProtocolSpec(
            protocol_name="NestedSpec",
            properties=(
                PropertySpec(kind=PropertyKind.ALWAYS_TERMINATES),
            ),
        )
        report = check_properties(nested_protocol, spec)
        assert report.results[0].verdict == PropertyVerdict.PROVED

    def test_no_deadlock_nested(self, nested_protocol):
        """NO_DEADLOCK holds for nested protocols (all branches non-empty)."""
        spec = ProtocolSpec(
            protocol_name="NestedSpec",
            properties=(
                PropertySpec(kind=PropertyKind.NO_DEADLOCK),
            ),
        )
        report = check_properties(nested_protocol, spec)
        assert report.results[0].verdict == PropertyVerdict.PROVED

    def test_exclusion_evidence_multi_level_context(self):
        """EXCLUSION evidence includes multi-level branch context with '>' separator."""
        proto = Protocol(
            name="DeepContext",
            roles=("a", "b", "c"),
            elements=(
                ProtocolChoice(
                    decider="a",
                    branches={
                        "outer": (
                            ProtocolChoice(
                                decider="b",
                                branches={
                                    "inner": (
                                        ProtocolStep(
                                            sender="b", receiver="c",
                                            message_kind=MessageKind.AUDIT_VERDICT,
                                        ),
                                    ),
                                },
                            ),
                        ),
                    },
                ),
            ),
        )
        spec = ProtocolSpec(
            protocol_name="DeepContext",
            properties=(
                PropertySpec(
                    kind=PropertyKind.EXCLUSION,
                    params=("b", "audit_verdict"),
                ),
            ),
        )
        report = check_properties(proto, spec)
        assert report.results[0].verdict == PropertyVerdict.VIOLATED
        # Multi-level context: "outer > inner"
        assert "outer" in report.results[0].evidence
        assert "inner" in report.results[0].evidence


# ============================================================
# Parser depth guard tests
# ============================================================


class TestDepthGuard:
    """Tests for the recursion depth guard in the parser."""

    def test_max_depth_exceeded_raises(self):
        """Parser raises ParseError when nesting exceeds MAX_CHOICE_DEPTH."""
        from cervellaswarm_lingua_universale._parser import Parser
        original = Parser.MAX_CHOICE_DEPTH
        try:
            Parser.MAX_CHOICE_DEPTH = 2  # lower limit for testing
            # Triple nesting should fail with depth=2
            with pytest.raises(ParseError, match="nesting depth exceeds"):
                parse(TRIPLE_NESTED_LU)
        finally:
            Parser.MAX_CHOICE_DEPTH = original

    def test_within_depth_limit_ok(self):
        """Double nesting within MAX_CHOICE_DEPTH=32 parses fine."""
        prog = parse(SAGA_ORDER_LU)
        assert prog.declarations[0].name == "SagaOrder"


# ============================================================
# Grammar export tests
# ============================================================


class TestGrammarExport:
    """Grammar export tests for nested choice in branch rule."""

    def test_gbnf_branch_allows_nested_choice(self):
        """GBNF branch rule uses step-or-choice+ (not step+)."""
        gbnf = GrammarExporter.to_gbnf()
        assert "step-or-choice+" in gbnf
        # The branch rule should reference step-or-choice
        for line in gbnf.splitlines():
            stripped = line.strip()
            if stripped.startswith("branch") and "::=" in stripped:
                assert "step-or-choice+" in stripped
                break
        else:
            pytest.fail("branch rule not found in GBNF")

    def test_lark_branch_allows_nested_choice(self):
        """Lark branch rule uses step_or_choice+ (not step+)."""
        lark = GrammarExporter.to_lark()
        assert "step_or_choice+" in lark
        for line in lark.splitlines():
            stripped = line.strip()
            if stripped.startswith("branch") and ":" in stripped:
                assert "step_or_choice+" in stripped
                break
        else:
            pytest.fail("branch rule not found in Lark")


# ============================================================
# End-to-end integration test
# ============================================================


class TestEndToEnd:
    """Full pipeline: LU source -> parse -> compile -> spec check."""

    def test_saga_full_pipeline(self):
        """Saga protocol: parse, compile, spec check all pass."""
        prog = parse(SAGA_ORDER_LU)
        compiler = ASTCompiler()
        protocol = compiler._ast_to_protocol(prog.declarations[0])

        # All 3 execution paths exist
        paths = _collect_all_paths(protocol.elements)
        assert len(paths) == 3

        # Codegen produces valid Python
        result = compiler.compile(prog, source_file="saga.lu")
        compile(result.python_source, "saga.lu", "exec")

    def test_auth_retry_full_pipeline(self):
        """Auth retry: parse, compile, spec check."""
        prog = parse(AUTH_RETRY_LU)
        compiler = ASTCompiler()
        protocol = compiler._ast_to_protocol(prog.declarations[0])

        paths = _collect_all_paths(protocol.elements)
        # valid, invalid->retry, invalid->give_up = 3 paths
        assert len(paths) == 3

        result = compiler.compile(prog, source_file="auth.lu")
        compile(result.python_source, "auth.lu", "exec")
