# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for the Lingua Universale AST node definitions (_ast.py).

Groups:
    1. TestLoc              - Loc construction and equality
    2. TestExprNodes        - all Expr node variants
    3. TestPropertyNodes    - all Property node variants
    4. TestStepChoiceNodes  - StepNode, BranchNode, ChoiceNode
    5. TestProtocolNode     - ProtocolNode construction
    6. TestTypeNodes        - TypeExpr, FieldNode, VariantTypeDecl, RecordTypeDecl
    7. TestAgentNode        - AgentNode with optional fields
    8. TestUseNode          - UseNode with and without alias
    9. TestProgramNode      - top-level ProgramNode
    10. TestFrozen          - immutability of every node kind
    11. TestEquality        - structural equality via frozen dataclass
    12. TestNestedProgram   - full ProgramNode mirroring Esempio 10

NOTE: No __init__.py in this directory (Package Shadowing Fix).
"""

import dataclasses

import pytest

from cervellaswarm_lingua_universale._ast import (
    AgentNode,
    AllParticipate,
    AlwaysTerminates,
    AttrExpr,
    BinOpExpr,
    BranchNode,
    ChoiceNode,
    ConfidenceProp,
    ExclusionProp,
    FieldNode,
    GenericType,
    GroupExpr,
    IdentExpr,
    Loc,
    MethodCallExpr,
    NoDeadlock,
    NotExpr,
    NumberExpr,
    OrderingProp,
    ProgramNode,
    ProtocolNode,
    RecordTypeDecl,
    SimpleType,
    StepNode,
    StringExpr,
    TrustProp,
    UseNode,
    VariantTypeDecl,
)


# ---------------------------------------------------------------------------
# Shared fixture
# ---------------------------------------------------------------------------

HERE = Loc(line=1, col=0)


# ===========================================================================
# 1. TestLoc
# ===========================================================================


class TestLoc:
    def test_construction(self):
        loc = Loc(line=5, col=12)
        assert loc.line == 5
        assert loc.col == 12

    def test_equality(self):
        assert Loc(1, 0) == Loc(1, 0)
        assert Loc(1, 0) != Loc(2, 0)

    def test_frozen(self):
        loc = Loc(1, 0)
        with pytest.raises(dataclasses.FrozenInstanceError):
            loc.line = 99  # type: ignore[misc]

    def test_hash(self):
        s = {Loc(1, 0), Loc(1, 0), Loc(2, 4)}
        assert len(s) == 2


# ===========================================================================
# 2. TestExprNodes
# ===========================================================================


class TestExprNodes:
    def test_ident_expr(self):
        n = IdentExpr(name="task", loc=HERE)
        assert n.name == "task"
        assert n.loc is HERE

    def test_number_expr(self):
        n = NumberExpr(value="80", loc=HERE)
        assert n.value == "80"

    def test_string_expr_includes_quotes(self):
        n = StringExpr(value='"hello"', loc=HERE)
        assert n.value == '"hello"'

    def test_attr_expr(self):
        n = AttrExpr(obj="task", attr="well_defined", loc=HERE)
        assert n.obj == "task"
        assert n.attr == "well_defined"

    def test_method_call_expr_no_args(self):
        n = MethodCallExpr(obj="tests", method="pass", args=(), loc=HERE)
        assert n.obj == "tests"
        assert n.method == "pass"
        assert n.args == ()

    def test_method_call_expr_with_args(self):
        arg = NumberExpr(value="80", loc=HERE)
        n = MethodCallExpr(obj="tests", method="pass", args=(arg,), loc=HERE)
        assert len(n.args) == 1
        assert n.args[0] == arg

    def test_bin_op_expr(self):
        left = IdentExpr(name="x", loc=HERE)
        right = NumberExpr(value="70", loc=HERE)
        n = BinOpExpr(left=left, op=">=", right=right, loc=HERE)
        assert n.op == ">="
        assert n.left == left
        assert n.right == right

    def test_not_expr(self):
        inner = IdentExpr(name="blocked", loc=HERE)
        n = NotExpr(operand=inner, loc=HERE)
        assert n.operand == inner

    def test_group_expr(self):
        inner = IdentExpr(name="x", loc=HERE)
        n = GroupExpr(inner=inner, loc=HERE)
        assert n.inner == inner

    def test_frozen_ident(self):
        n = IdentExpr(name="x", loc=HERE)
        with pytest.raises(dataclasses.FrozenInstanceError):
            n.name = "y"  # type: ignore[misc]

    def test_frozen_bin_op(self):
        n = BinOpExpr(
            left=IdentExpr("a", HERE),
            op="and",
            right=IdentExpr("b", HERE),
            loc=HERE,
        )
        with pytest.raises(dataclasses.FrozenInstanceError):
            n.op = "or"  # type: ignore[misc]


# ===========================================================================
# 3. TestPropertyNodes
# ===========================================================================


class TestPropertyNodes:
    def test_always_terminates(self):
        p = AlwaysTerminates(loc=HERE)
        assert p.loc is HERE

    def test_no_deadlock(self):
        p = NoDeadlock(loc=HERE)
        assert p.loc is HERE

    def test_ordering_prop(self):
        p = OrderingProp(before="task_request", after="task_result", loc=HERE)
        assert p.before == "task_request"
        assert p.after == "task_result"

    def test_exclusion_prop(self):
        p = ExclusionProp(role="backend", message="audit_verdict", loc=HERE)
        assert p.role == "backend"
        assert p.message == "audit_verdict"

    def test_confidence_prop(self):
        p = ConfidenceProp(level="high", loc=HERE)
        assert p.level == "high"

    def test_trust_prop(self):
        p = TrustProp(tier="trusted", loc=HERE)
        assert p.tier == "trusted"

    def test_all_participate(self):
        p = AllParticipate(loc=HERE)
        assert p.loc is HERE

    def test_frozen_property(self):
        p = AlwaysTerminates(loc=HERE)
        with pytest.raises(dataclasses.FrozenInstanceError):
            p.loc = Loc(99, 0)  # type: ignore[misc]


# ===========================================================================
# 4. TestStepChoiceNodes
# ===========================================================================


class TestStepChoiceNodes:
    def test_step_node(self):
        s = StepNode(
            sender="regina",
            action="asks",
            receiver="worker",
            payload="do task",
            loc=HERE,
        )
        assert s.sender == "regina"
        assert s.action == "asks"
        assert s.receiver == "worker"
        assert s.payload == "do task"

    def test_step_node_returns(self):
        s = StepNode(
            sender="worker",
            action="returns",
            receiver="regina",
            payload="result",
            loc=HERE,
        )
        assert s.action == "returns"

    def test_branch_node(self):
        step = StepNode("a", "tells", "b", "decision", HERE)
        b = BranchNode(label="approve", steps=(step,), loc=HERE)
        assert b.label == "approve"
        assert len(b.steps) == 1

    def test_choice_node(self):
        step_approve = StepNode("regina", "tells", "architect", "decision", HERE)
        step_reject = StepNode("regina", "tells", "architect", "decision", HERE)
        b1 = BranchNode("approve", (step_approve,), HERE)
        b2 = BranchNode("reject", (step_reject,), HERE)
        c = ChoiceNode(decider="regina", branches=(b1, b2), loc=HERE)
        assert c.decider == "regina"
        assert len(c.branches) == 2

    def test_frozen_step(self):
        s = StepNode("a", "asks", "b", "do task", HERE)
        with pytest.raises(dataclasses.FrozenInstanceError):
            s.sender = "x"  # type: ignore[misc]

    def test_frozen_choice(self):
        b = BranchNode("x", (), HERE)
        c = ChoiceNode("regina", (b,), HERE)
        with pytest.raises(dataclasses.FrozenInstanceError):
            c.decider = "worker"  # type: ignore[misc]


# ===========================================================================
# 5. TestProtocolNode
# ===========================================================================


class TestProtocolNode:
    def test_basic_construction(self):
        step = StepNode("regina", "asks", "worker", "do task", HERE)
        prop = AlwaysTerminates(HERE)
        p = ProtocolNode(
            name="DelegateTask",
            roles=("regina", "worker"),
            steps=(step,),
            properties=(prop,),
            loc=HERE,
        )
        assert p.name == "DelegateTask"
        assert p.roles == ("regina", "worker")
        assert len(p.steps) == 1
        assert len(p.properties) == 1

    def test_empty_properties(self):
        step = StepNode("a", "tells", "b", "message", HERE)
        p = ProtocolNode("P", ("a", "b"), (step,), (), HERE)
        assert p.properties == ()

    def test_frozen(self):
        p = ProtocolNode("P", (), (), (), HERE)
        with pytest.raises(dataclasses.FrozenInstanceError):
            p.name = "Q"  # type: ignore[misc]


# ===========================================================================
# 6. TestTypeNodes
# ===========================================================================


class TestTypeNodes:
    def test_simple_type_not_optional(self):
        t = SimpleType(name="String", optional=False, loc=HERE)
        assert t.name == "String"
        assert t.optional is False

    def test_simple_type_optional(self):
        t = SimpleType(name="String", optional=True, loc=HERE)
        assert t.optional is True

    def test_generic_type(self):
        inner = SimpleType("String", False, HERE)
        t = GenericType(name="List", arg=inner, optional=False, loc=HERE)
        assert t.name == "List"
        assert t.arg == inner

    def test_generic_type_optional(self):
        inner = SimpleType("Code", False, HERE)
        t = GenericType(name="Confident", arg=inner, optional=True, loc=HERE)
        assert t.optional is True

    def test_field_node(self):
        type_expr = SimpleType("String", False, HERE)
        f = FieldNode(name="conclusion", type_expr=type_expr, loc=HERE)
        assert f.name == "conclusion"
        assert f.type_expr == type_expr

    def test_variant_type_decl(self):
        v = VariantTypeDecl(name="TaskStatus", variants=("ok", "fail", "blocked"), loc=HERE)
        assert v.name == "TaskStatus"
        assert v.variants == ("ok", "fail", "blocked")

    def test_record_type_decl(self):
        f1 = FieldNode("code", GenericType("Confident", SimpleType("String", False, HERE), False, HERE), HERE)
        f2 = FieldNode("tests_passed", SimpleType("Number", False, HERE), HERE)
        r = RecordTypeDecl(name="CodeResult", fields=(f1, f2), loc=HERE)
        assert r.name == "CodeResult"
        assert len(r.fields) == 2

    def test_frozen_simple_type(self):
        t = SimpleType("String", False, HERE)
        with pytest.raises(dataclasses.FrozenInstanceError):
            t.name = "Number"  # type: ignore[misc]

    def test_frozen_record(self):
        r = RecordTypeDecl("R", (), HERE)
        with pytest.raises(dataclasses.FrozenInstanceError):
            r.name = "S"  # type: ignore[misc]


# ===========================================================================
# 7. TestAgentNode
# ===========================================================================


class TestAgentNode:
    def test_full_agent(self):
        req1 = AttrExpr("task", "well_defined", HERE)
        ens1 = AttrExpr("output", "compiles", HERE)
        a = AgentNode(
            name="Worker",
            role="backend",
            trust="standard",
            accepts=("TaskRequest",),
            produces=("TaskResult",),
            requires=(req1,),
            ensures=(ens1,),
            loc=HERE,
        )
        assert a.name == "Worker"
        assert a.role == "backend"
        assert a.trust == "standard"
        assert a.accepts == ("TaskRequest",)
        assert a.produces == ("TaskResult",)
        assert len(a.requires) == 1
        assert len(a.ensures) == 1

    def test_optional_fields_none(self):
        a = AgentNode(
            name="MinimalAgent",
            role=None,
            trust=None,
            accepts=(),
            produces=(),
            requires=(),
            ensures=(),
            loc=HERE,
        )
        assert a.role is None
        assert a.trust is None

    def test_frozen(self):
        a = AgentNode("A", None, None, (), (), (), (), HERE)
        with pytest.raises(dataclasses.FrozenInstanceError):
            a.name = "B"  # type: ignore[misc]


# ===========================================================================
# 8. TestUseNode
# ===========================================================================


class TestUseNode:
    def test_use_without_alias(self):
        u = UseNode(module="math", alias=None, loc=HERE)
        assert u.module == "math"
        assert u.alias is None

    def test_use_with_alias(self):
        u = UseNode(module="datetime", alias="dt", loc=HERE)
        assert u.alias == "dt"

    def test_use_dotted_module(self):
        u = UseNode(module="os.path", alias=None, loc=HERE)
        assert u.module == "os.path"

    def test_frozen(self):
        u = UseNode("math", None, HERE)
        with pytest.raises(dataclasses.FrozenInstanceError):
            u.module = "os"  # type: ignore[misc]


# ===========================================================================
# 9. TestProgramNode
# ===========================================================================


class TestProgramNode:
    def test_empty_program(self):
        p = ProgramNode(declarations=(), loc=HERE)
        assert p.declarations == ()

    def test_single_declaration(self):
        use = UseNode("logging", None, HERE)
        p = ProgramNode(declarations=(use,), loc=HERE)
        assert len(p.declarations) == 1
        assert isinstance(p.declarations[0], UseNode)

    def test_frozen(self):
        p = ProgramNode((), HERE)
        with pytest.raises(dataclasses.FrozenInstanceError):
            p.declarations = (UseNode("x", None, HERE),)  # type: ignore[misc]


# ===========================================================================
# 10. TestFrozen  (every node kind verified once more, exhaustively)
# ===========================================================================


class TestFrozen:
    """Exhaustive freeze check for every exported node type."""

    NODES = [
        Loc(1, 0),
        IdentExpr("x", HERE),
        NumberExpr("1", HERE),
        StringExpr('"a"', HERE),
        AttrExpr("a", "b", HERE),
        MethodCallExpr("a", "b", (), HERE),
        BinOpExpr(IdentExpr("a", HERE), "and", IdentExpr("b", HERE), HERE),
        NotExpr(IdentExpr("x", HERE), HERE),
        GroupExpr(IdentExpr("x", HERE), HERE),
        AlwaysTerminates(HERE),
        NoDeadlock(HERE),
        OrderingProp("a", "b", HERE),
        ExclusionProp("a", "b", HERE),
        ConfidenceProp("high", HERE),
        TrustProp("trusted", HERE),
        AllParticipate(HERE),
        StepNode("a", "asks", "b", "do task", HERE),
        BranchNode("x", (), HERE),
        ChoiceNode("a", (), HERE),
        ProtocolNode("P", (), (), (), HERE),
        SimpleType("String", False, HERE),
        GenericType("List", SimpleType("String", False, HERE), False, HERE),
        FieldNode("f", SimpleType("String", False, HERE), HERE),
        VariantTypeDecl("V", ("a", "b"), HERE),
        RecordTypeDecl("R", (), HERE),
        AgentNode("A", None, None, (), (), (), (), HERE),
        UseNode("m", None, HERE),
        ProgramNode((), HERE),
    ]

    @pytest.mark.parametrize("node", NODES)
    def test_node_is_frozen(self, node):
        fields = dataclasses.fields(node)
        assert len(fields) > 0, "node has no fields"
        first_field = fields[0]
        with pytest.raises(dataclasses.FrozenInstanceError):
            setattr(node, first_field.name, None)


# ===========================================================================
# 11. TestEquality
# ===========================================================================


class TestEquality:
    def test_loc_equality(self):
        assert Loc(3, 7) == Loc(3, 7)
        assert Loc(3, 7) != Loc(3, 8)

    def test_ident_expr_equality(self):
        assert IdentExpr("x", Loc(1, 0)) == IdentExpr("x", Loc(1, 0))
        assert IdentExpr("x", Loc(1, 0)) != IdentExpr("y", Loc(1, 0))

    def test_nested_equality(self):
        left = AttrExpr("task", "well_defined", Loc(2, 4))
        right = AttrExpr("task", "well_defined", Loc(2, 4))
        assert left == right

    def test_bin_op_equality(self):
        a = BinOpExpr(IdentExpr("x", HERE), ">=", NumberExpr("70", HERE), HERE)
        b = BinOpExpr(IdentExpr("x", HERE), ">=", NumberExpr("70", HERE), HERE)
        assert a == b

    def test_tuple_field_equality(self):
        v1 = VariantTypeDecl("Status", ("ok", "fail"), HERE)
        v2 = VariantTypeDecl("Status", ("ok", "fail"), HERE)
        assert v1 == v2

    def test_protocol_equality(self):
        step = StepNode("a", "asks", "b", "do task", HERE)
        p1 = ProtocolNode("P", ("a", "b"), (step,), (), HERE)
        p2 = ProtocolNode("P", ("a", "b"), (step,), (), HERE)
        assert p1 == p2


# ===========================================================================
# 12. TestNestedProgram  (mirrors Esempio 10)
# ===========================================================================


class TestNestedProgram:
    """Build a ProgramNode that mirrors Example 10 of the design document.

    Esempio 10 contains:
      - use python logging
      - type Priority = critical | high | medium | low
      - type CodeResult = { code: Confident[String], tests_passed: Number, coverage: Number }
      - protocol CodeReview with 6 steps and 7 properties
      - agent CodeBackend with requires/ensures
      - agent CodeTester with requires/ensures
    """

    def _build(self) -> ProgramNode:
        loc = Loc(1, 0)

        # use python logging
        use_logging = UseNode(module="logging", alias=None, loc=loc)

        # type Priority = critical | high | medium | low
        priority_type = VariantTypeDecl(
            name="Priority",
            variants=("critical", "high", "medium", "low"),
            loc=loc,
        )

        # type CodeResult = ...
        confident_string = GenericType(
            name="Confident",
            arg=SimpleType("String", False, loc),
            optional=False,
            loc=loc,
        )
        f_code = FieldNode("code", confident_string, loc)
        f_tests = FieldNode("tests_passed", SimpleType("Number", False, loc), loc)
        f_coverage = FieldNode("coverage", SimpleType("Number", False, loc), loc)
        code_result_type = RecordTypeDecl(
            name="CodeResult",
            fields=(f_code, f_tests, f_coverage),
            loc=loc,
        )

        # protocol CodeReview steps
        s1 = StepNode("regina", "asks", "backend", "do task", loc)
        s2 = StepNode("backend", "returns", "regina", "result", loc)
        s3 = StepNode("regina", "asks", "tester", "verify", loc)
        s4 = StepNode("tester", "returns", "regina", "verdict", loc)
        s5 = StepNode("regina", "asks", "guardiana", "verify", loc)
        s6 = StepNode("guardiana", "returns", "regina", "verdict", loc)

        # protocol CodeReview properties (7 total)
        props = (
            AlwaysTerminates(loc),
            NoDeadlock(loc),
            OrderingProp("task_request", "task_result", loc),
            ExclusionProp("backend", "audit_verdict", loc),
            ExclusionProp("tester", "task_result", loc),
            TrustProp("standard", loc),
            AllParticipate(loc),
        )

        protocol = ProtocolNode(
            name="CodeReview",
            roles=("regina", "backend", "tester", "guardiana"),
            steps=(s1, s2, s3, s4, s5, s6),
            properties=props,
            loc=loc,
        )

        # agent CodeBackend
        req_task_defined = AttrExpr("task", "well_defined", loc)
        # task.priority != critical or regina.approved
        priority_cmp = BinOpExpr(
            left=AttrExpr("task", "priority", loc),
            op="!=",
            right=IdentExpr("critical", loc),
            loc=loc,
        )
        req_priority = BinOpExpr(
            left=priority_cmp,
            op="or",
            right=AttrExpr("regina", "approved", loc),
            loc=loc,
        )
        ens_compiles = AttrExpr("output", "compiles", loc)
        ens_tests = MethodCallExpr("tests", "pass", (NumberExpr("80", loc),), loc)
        ens_coverage = BinOpExpr(
            left=IdentExpr("coverage", loc),
            op=">=",
            right=NumberExpr("70", loc),
            loc=loc,
        )
        backend_agent = AgentNode(
            name="CodeBackend",
            role="backend",
            trust="standard",
            accepts=("TaskRequest",),
            produces=("TaskResult",),
            requires=(req_task_defined, req_priority),
            ensures=(ens_compiles, ens_tests, ens_coverage),
            loc=loc,
        )

        # agent CodeTester
        req_compiles = AttrExpr("code", "compiles", loc)
        ens_all_executed = AttrExpr("all_tests", "executed", loc)
        ens_report = AttrExpr("report", "complete", loc)
        tester_agent = AgentNode(
            name="CodeTester",
            role="tester",
            trust="trusted",
            accepts=("AuditRequest",),
            produces=("AuditVerdict",),
            requires=(req_compiles,),
            ensures=(ens_all_executed, ens_report),
            loc=loc,
        )

        return ProgramNode(
            declarations=(
                use_logging,
                priority_type,
                code_result_type,
                protocol,
                backend_agent,
                tester_agent,
            ),
            loc=loc,
        )

    def test_program_builds(self):
        prog = self._build()
        assert isinstance(prog, ProgramNode)

    def test_declaration_count(self):
        prog = self._build()
        assert len(prog.declarations) == 6

    def test_use_node(self):
        prog = self._build()
        use = prog.declarations[0]
        assert isinstance(use, UseNode)
        assert use.module == "logging"
        assert use.alias is None

    def test_priority_variant(self):
        prog = self._build()
        variant = prog.declarations[1]
        assert isinstance(variant, VariantTypeDecl)
        assert variant.name == "Priority"
        assert variant.variants == ("critical", "high", "medium", "low")

    def test_code_result_record(self):
        prog = self._build()
        record = prog.declarations[2]
        assert isinstance(record, RecordTypeDecl)
        assert record.name == "CodeResult"
        assert len(record.fields) == 3
        # first field: code: Confident[String]
        f0 = record.fields[0]
        assert f0.name == "code"
        assert isinstance(f0.type_expr, GenericType)
        assert f0.type_expr.name == "Confident"

    def test_protocol_steps_and_properties(self):
        prog = self._build()
        protocol = prog.declarations[3]
        assert isinstance(protocol, ProtocolNode)
        assert protocol.name == "CodeReview"
        assert len(protocol.steps) == 6
        assert len(protocol.properties) == 7

    def test_protocol_roles(self):
        prog = self._build()
        protocol = prog.declarations[3]
        assert isinstance(protocol, ProtocolNode)
        assert "regina" in protocol.roles
        assert "tester" in protocol.roles

    def test_backend_agent_contracts(self):
        prog = self._build()
        agent = prog.declarations[4]
        assert isinstance(agent, AgentNode)
        assert agent.name == "CodeBackend"
        assert agent.role == "backend"
        assert len(agent.requires) == 2
        assert len(agent.ensures) == 3
        # ensures[1] is tests.pass(80)
        ens_tests = agent.ensures[1]
        assert isinstance(ens_tests, MethodCallExpr)
        assert ens_tests.method == "pass"
        assert len(ens_tests.args) == 1

    def test_tester_agent(self):
        prog = self._build()
        agent = prog.declarations[5]
        assert isinstance(agent, AgentNode)
        assert agent.name == "CodeTester"
        assert agent.trust == "trusted"
        assert len(agent.requires) == 1
        assert len(agent.ensures) == 2

    def test_program_is_frozen(self):
        prog = self._build()
        with pytest.raises(dataclasses.FrozenInstanceError):
            prog.declarations = ()  # type: ignore[misc]

    def test_program_equality(self):
        prog1 = self._build()
        prog2 = self._build()
        assert prog1 == prog2
