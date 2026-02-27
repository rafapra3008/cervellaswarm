# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Integration tests for the Lingua Universale v0.2 unified parser.

Tests ALL 10 canonical examples from DESIGN_C1_2 end-to-end, verifying
the full AST produced by parse() in detail.

Groups:
    1. TestExample1DelegateTask       - Esempio 1: Protocol base
    2. TestExample2PlanAndBuild       - Esempio 2: Protocol con Choice
    3. TestExample3WorkerAgent        - Esempio 3: Agent declaration
    4. TestExample4AnalysisResult     - Esempio 4: Record type
    5. TestExample5VariantTypes       - Esempio 5: Variant types
    6. TestExample6UsePlusAgent       - Esempio 6: Use + Agent
    7. TestExample7SecureAudit        - Esempio 7: Trust + Exclusion
    8. TestExample8RecipeApp          - Esempio 8: Protocol + Agent
    9. TestExample9DeepResearch       - Esempio 9: Type + Protocol
    10. TestExample10CompleteProgram  - Esempio 10: Multi-declaration program
    11. TestCrossConstruct            - Edge cases e error paths

NOTE: No __init__.py in this directory (Package Shadowing Fix, P17).
"""

from __future__ import annotations

import textwrap

import pytest

from cervellaswarm_lingua_universale._parser import ParseError, parse
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
    IdentExpr,
    Loc,
    MethodCallExpr,
    NoDeadlock,
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


# ===========================================================================
# 1. TestExample1DelegateTask
# ===========================================================================


class TestExample1DelegateTask:
    """Esempio 1: DelegateTask - Protocol base con 3 roles, 4 steps, 4 properties."""

    SOURCE = textwrap.dedent("""\
        protocol DelegateTask:
            roles: regina, worker, guardiana

            regina asks worker to do task
            worker returns result to regina
            regina asks guardiana to verify
            guardiana returns verdict to regina

            properties:
                always terminates
                no deadlock
                task_request before task_result
                all roles participate
    """)

    def test_single_declaration(self) -> None:
        """Esempio 1: il programma ha esattamente 1 declaration."""
        program = parse(self.SOURCE)
        assert isinstance(program, ProgramNode)
        assert len(program.declarations) == 1

    def test_protocol_name_and_type(self) -> None:
        """Esempio 1: la declaration e un ProtocolNode con name=DelegateTask."""
        proto = parse(self.SOURCE).declarations[0]
        assert isinstance(proto, ProtocolNode)
        assert proto.name == "DelegateTask"

    def test_roles(self) -> None:
        """Esempio 1: 3 roles in ordine."""
        proto = parse(self.SOURCE).declarations[0]
        assert isinstance(proto, ProtocolNode)
        assert proto.roles == ("regina", "worker", "guardiana")

    def test_steps_count(self) -> None:
        """Esempio 1: 4 step lineari (nessun choice)."""
        proto = parse(self.SOURCE).declarations[0]
        assert isinstance(proto, ProtocolNode)
        assert len(proto.steps) == 4
        for step in proto.steps:
            assert isinstance(step, StepNode)

    def test_step_details(self) -> None:
        """Esempio 1: sender/action/receiver/payload di ogni step."""
        proto = parse(self.SOURCE).declarations[0]
        assert isinstance(proto, ProtocolNode)
        steps = proto.steps

        assert isinstance(steps[0], StepNode)
        assert steps[0].sender == "regina"
        assert steps[0].action == "asks"
        assert steps[0].receiver == "worker"
        assert steps[0].payload == "do task"

        assert isinstance(steps[1], StepNode)
        assert steps[1].sender == "worker"
        assert steps[1].action == "returns"
        assert steps[1].receiver == "regina"
        assert steps[1].payload == "result"

        assert isinstance(steps[2], StepNode)
        assert steps[2].sender == "regina"
        assert steps[2].action == "asks"
        assert steps[2].receiver == "guardiana"
        assert steps[2].payload == "verify"

        assert isinstance(steps[3], StepNode)
        assert steps[3].sender == "guardiana"
        assert steps[3].action == "returns"
        assert steps[3].receiver == "regina"
        assert steps[3].payload == "verdict"

    def test_properties_count(self) -> None:
        """Esempio 1: 4 properties."""
        proto = parse(self.SOURCE).declarations[0]
        assert isinstance(proto, ProtocolNode)
        assert len(proto.properties) == 4

    def test_properties_types(self) -> None:
        """Esempio 1: AlwaysTerminates, NoDeadlock, OrderingProp, AllParticipate."""
        proto = parse(self.SOURCE).declarations[0]
        assert isinstance(proto, ProtocolNode)
        prop_types = [type(p) for p in proto.properties]
        assert prop_types == [AlwaysTerminates, NoDeadlock, OrderingProp, AllParticipate]

    def test_ordering_prop_values(self) -> None:
        """Esempio 1: task_request before task_result."""
        proto = parse(self.SOURCE).declarations[0]
        assert isinstance(proto, ProtocolNode)
        ordering = next(p for p in proto.properties if isinstance(p, OrderingProp))
        assert ordering.before == "task_request"
        assert ordering.after == "task_result"

    def test_loc_is_set(self) -> None:
        """Esempio 1: loc del ProtocolNode e valida."""
        proto = parse(self.SOURCE).declarations[0]
        assert isinstance(proto, ProtocolNode)
        assert isinstance(proto.loc, Loc)
        assert proto.loc.line >= 1


# ===========================================================================
# 2. TestExample2PlanAndBuild
# ===========================================================================


class TestExample2PlanAndBuild:
    """Esempio 2: PlanAndBuild - Protocol con Choice block."""

    SOURCE = textwrap.dedent("""\
        protocol PlanAndBuild:
            roles: regina, architect, worker, guardiana

            regina asks architect to plan
            architect returns plan to regina

            when regina decides:
                approve:
                    regina tells architect decision
                    regina asks worker to do task
                    worker returns result to regina
                    regina asks guardiana to verify
                    guardiana returns verdict to regina
                reject:
                    regina tells architect decision
                    architect returns plan to regina

            properties:
                always terminates
                no deadlock
                confidence >= high
    """)

    def test_single_declaration(self) -> None:
        """Esempio 2: 1 declaration."""
        assert len(parse(self.SOURCE).declarations) == 1

    def test_protocol_name(self) -> None:
        """Esempio 2: name=PlanAndBuild."""
        proto = parse(self.SOURCE).declarations[0]
        assert isinstance(proto, ProtocolNode)
        assert proto.name == "PlanAndBuild"

    def test_four_roles(self) -> None:
        """Esempio 2: 4 roles."""
        proto = parse(self.SOURCE).declarations[0]
        assert isinstance(proto, ProtocolNode)
        assert proto.roles == ("regina", "architect", "worker", "guardiana")

    def test_steps_include_choice(self) -> None:
        """Esempio 2: 2 StepNode + 1 ChoiceNode = 3 step_or_choice totali."""
        proto = parse(self.SOURCE).declarations[0]
        assert isinstance(proto, ProtocolNode)
        assert len(proto.steps) == 3
        assert isinstance(proto.steps[0], StepNode)
        assert isinstance(proto.steps[1], StepNode)
        assert isinstance(proto.steps[2], ChoiceNode)

    def test_choice_decider(self) -> None:
        """Esempio 2: decider del choice e 'regina'."""
        proto = parse(self.SOURCE).declarations[0]
        assert isinstance(proto, ProtocolNode)
        choice = proto.steps[2]
        assert isinstance(choice, ChoiceNode)
        assert choice.decider == "regina"

    def test_choice_two_branches(self) -> None:
        """Esempio 2: 2 branches (approve, reject)."""
        proto = parse(self.SOURCE).declarations[0]
        assert isinstance(proto, ProtocolNode)
        choice = proto.steps[2]
        assert isinstance(choice, ChoiceNode)
        assert len(choice.branches) == 2
        labels = {b.label for b in choice.branches}
        assert labels == {"approve", "reject"}

    def test_approve_branch_five_steps(self) -> None:
        """Esempio 2: branch 'approve' ha 5 steps."""
        proto = parse(self.SOURCE).declarations[0]
        assert isinstance(proto, ProtocolNode)
        choice = proto.steps[2]
        assert isinstance(choice, ChoiceNode)
        approve = next(b for b in choice.branches if b.label == "approve")
        assert isinstance(approve, BranchNode)
        assert len(approve.steps) == 5

    def test_reject_branch_two_steps(self) -> None:
        """Esempio 2: branch 'reject' ha 2 steps."""
        proto = parse(self.SOURCE).declarations[0]
        assert isinstance(proto, ProtocolNode)
        choice = proto.steps[2]
        assert isinstance(choice, ChoiceNode)
        reject = next(b for b in choice.branches if b.label == "reject")
        assert isinstance(reject, BranchNode)
        assert len(reject.steps) == 2

    def test_three_properties(self) -> None:
        """Esempio 2: 3 properties con ConfidenceProp(high)."""
        proto = parse(self.SOURCE).declarations[0]
        assert isinstance(proto, ProtocolNode)
        assert len(proto.properties) == 3
        conf = next(p for p in proto.properties if isinstance(p, ConfidenceProp))
        assert conf.level == "high"


# ===========================================================================
# 3. TestExample3WorkerAgent
# ===========================================================================


class TestExample3WorkerAgent:
    """Esempio 3: Worker Agent declaration."""

    SOURCE = textwrap.dedent("""\
        agent Worker:
            role: backend
            trust: standard
            accepts: TaskRequest, PlanDecision
            produces: TaskResult
            requires:
                task.well_defined
                context.sufficient
            ensures:
                output.compiles
                tests.pass(80)
    """)

    def test_single_declaration(self) -> None:
        """Esempio 3: 1 declaration AgentNode."""
        program = parse(self.SOURCE)
        assert len(program.declarations) == 1
        assert isinstance(program.declarations[0], AgentNode)

    def test_agent_name(self) -> None:
        """Esempio 3: name=Worker."""
        agent = parse(self.SOURCE).declarations[0]
        assert isinstance(agent, AgentNode)
        assert agent.name == "Worker"

    def test_agent_role(self) -> None:
        """Esempio 3: role=backend."""
        agent = parse(self.SOURCE).declarations[0]
        assert isinstance(agent, AgentNode)
        assert agent.role == "backend"

    def test_agent_trust(self) -> None:
        """Esempio 3: trust=standard."""
        agent = parse(self.SOURCE).declarations[0]
        assert isinstance(agent, AgentNode)
        assert agent.trust == "standard"

    def test_accepts_two_items(self) -> None:
        """Esempio 3: accepts ha 2 items (TaskRequest, PlanDecision)."""
        agent = parse(self.SOURCE).declarations[0]
        assert isinstance(agent, AgentNode)
        assert agent.accepts == ("TaskRequest", "PlanDecision")

    def test_produces_one_item(self) -> None:
        """Esempio 3: produces ha 1 item (TaskResult)."""
        agent = parse(self.SOURCE).declarations[0]
        assert isinstance(agent, AgentNode)
        assert agent.produces == ("TaskResult",)

    def test_requires_two_attr_expr(self) -> None:
        """Esempio 3: requires ha 2 AttrExpr (task.well_defined, context.sufficient)."""
        agent = parse(self.SOURCE).declarations[0]
        assert isinstance(agent, AgentNode)
        assert len(agent.requires) == 2
        req0 = agent.requires[0]
        assert isinstance(req0, AttrExpr)
        assert req0.obj == "task"
        assert req0.attr == "well_defined"
        req1 = agent.requires[1]
        assert isinstance(req1, AttrExpr)
        assert req1.obj == "context"
        assert req1.attr == "sufficient"

    def test_ensures_attr_and_method(self) -> None:
        """Esempio 3: ensures ha AttrExpr + MethodCallExpr."""
        agent = parse(self.SOURCE).declarations[0]
        assert isinstance(agent, AgentNode)
        assert len(agent.ensures) == 2
        ens0 = agent.ensures[0]
        assert isinstance(ens0, AttrExpr)
        assert ens0.obj == "output"
        assert ens0.attr == "compiles"
        ens1 = agent.ensures[1]
        assert isinstance(ens1, MethodCallExpr)
        assert ens1.obj == "tests"
        assert ens1.method == "pass"
        assert len(ens1.args) == 1
        assert isinstance(ens1.args[0], NumberExpr)
        assert ens1.args[0].value == "80"


# ===========================================================================
# 4. TestExample4AnalysisResult
# ===========================================================================


class TestExample4AnalysisResult:
    """Esempio 4: AnalysisResult - Record type con 4 fields."""

    SOURCE = textwrap.dedent("""\
        type AnalysisResult =
            conclusion: String
            confidence: Confident[String]
            evidence: List[String]
            alternative: String?
    """)

    def test_single_record_declaration(self) -> None:
        """Esempio 4: 1 RecordTypeDecl."""
        program = parse(self.SOURCE)
        assert len(program.declarations) == 1
        assert isinstance(program.declarations[0], RecordTypeDecl)

    def test_record_name(self) -> None:
        """Esempio 4: name=AnalysisResult."""
        decl = parse(self.SOURCE).declarations[0]
        assert isinstance(decl, RecordTypeDecl)
        assert decl.name == "AnalysisResult"

    def test_four_fields(self) -> None:
        """Esempio 4: 4 fields."""
        decl = parse(self.SOURCE).declarations[0]
        assert isinstance(decl, RecordTypeDecl)
        assert len(decl.fields) == 4

    def test_field_conclusion(self) -> None:
        """Esempio 4: field 'conclusion' e SimpleType('String', optional=False)."""
        decl = parse(self.SOURCE).declarations[0]
        assert isinstance(decl, RecordTypeDecl)
        field = decl.fields[0]
        assert isinstance(field, FieldNode)
        assert field.name == "conclusion"
        assert isinstance(field.type_expr, SimpleType)
        assert field.type_expr.name == "String"
        assert field.type_expr.optional is False

    def test_field_confidence(self) -> None:
        """Esempio 4: field 'confidence' e GenericType('Confident', SimpleType('String'))."""
        decl = parse(self.SOURCE).declarations[0]
        assert isinstance(decl, RecordTypeDecl)
        field = decl.fields[1]
        assert isinstance(field, FieldNode)
        assert field.name == "confidence"
        assert isinstance(field.type_expr, GenericType)
        assert field.type_expr.name == "Confident"
        assert isinstance(field.type_expr.arg, SimpleType)
        assert field.type_expr.arg.name == "String"
        assert field.type_expr.optional is False

    def test_field_evidence(self) -> None:
        """Esempio 4: field 'evidence' e GenericType('List', SimpleType('String'))."""
        decl = parse(self.SOURCE).declarations[0]
        assert isinstance(decl, RecordTypeDecl)
        field = decl.fields[2]
        assert isinstance(field, FieldNode)
        assert field.name == "evidence"
        assert isinstance(field.type_expr, GenericType)
        assert field.type_expr.name == "List"
        assert isinstance(field.type_expr.arg, SimpleType)
        assert field.type_expr.arg.name == "String"

    def test_field_alternative_optional(self) -> None:
        """Esempio 4: field 'alternative' e SimpleType('String', optional=True)."""
        decl = parse(self.SOURCE).declarations[0]
        assert isinstance(decl, RecordTypeDecl)
        field = decl.fields[3]
        assert isinstance(field, FieldNode)
        assert field.name == "alternative"
        assert isinstance(field.type_expr, SimpleType)
        assert field.type_expr.name == "String"
        assert field.type_expr.optional is True


# ===========================================================================
# 5. TestExample5VariantTypes
# ===========================================================================


class TestExample5VariantTypes:
    """Esempio 5: tre VariantTypeDecl con 3, 3, 4 variants."""

    SOURCE = textwrap.dedent("""\
        type TaskStatus = ok | fail | blocked
        type AuditVerdict = approved | blocked | needs_revision
        type Priority = critical | high | medium | low
    """)

    def test_three_declarations(self) -> None:
        """Esempio 5: 3 VariantTypeDecl."""
        program = parse(self.SOURCE)
        assert len(program.declarations) == 3
        for decl in program.declarations:
            assert isinstance(decl, VariantTypeDecl)

    def test_task_status(self) -> None:
        """Esempio 5: TaskStatus ha 3 variants."""
        decl = parse(self.SOURCE).declarations[0]
        assert isinstance(decl, VariantTypeDecl)
        assert decl.name == "TaskStatus"
        assert decl.variants == ("ok", "fail", "blocked")

    def test_audit_verdict(self) -> None:
        """Esempio 5: AuditVerdict ha 3 variants."""
        decl = parse(self.SOURCE).declarations[1]
        assert isinstance(decl, VariantTypeDecl)
        assert decl.name == "AuditVerdict"
        assert decl.variants == ("approved", "blocked", "needs_revision")

    def test_priority(self) -> None:
        """Esempio 5: Priority ha 4 variants."""
        decl = parse(self.SOURCE).declarations[2]
        assert isinstance(decl, VariantTypeDecl)
        assert decl.name == "Priority"
        assert decl.variants == ("critical", "high", "medium", "low")


# ===========================================================================
# 6. TestExample6UsePlusAgent
# ===========================================================================


class TestExample6UsePlusAgent:
    """Esempio 6: 3 UseNode + 1 AgentNode con espressioni complesse."""

    SOURCE = textwrap.dedent("""\
        use python math
        use python datetime as dt
        use python pandas as pd

        agent DataAnalyst:
            role: data
            trust: standard
            requires:
                pd.version >= "2.0"
            ensures:
                output.format == "dataframe"
    """)

    def test_four_declarations(self) -> None:
        """Esempio 6: 3 UseNode + 1 AgentNode = 4 declarations."""
        program = parse(self.SOURCE)
        assert len(program.declarations) == 4

    def test_use_math_no_alias(self) -> None:
        """Esempio 6: use python math -> module='math', alias=None."""
        node = parse(self.SOURCE).declarations[0]
        assert isinstance(node, UseNode)
        assert node.module == "math"
        assert node.alias is None

    def test_use_datetime_alias(self) -> None:
        """Esempio 6: use python datetime as dt -> alias='dt'."""
        node = parse(self.SOURCE).declarations[1]
        assert isinstance(node, UseNode)
        assert node.module == "datetime"
        assert node.alias == "dt"

    def test_use_pandas_alias(self) -> None:
        """Esempio 6: use python pandas as pd -> alias='pd'."""
        node = parse(self.SOURCE).declarations[2]
        assert isinstance(node, UseNode)
        assert node.module == "pandas"
        assert node.alias == "pd"

    def test_agent_declaration(self) -> None:
        """Esempio 6: quarta declaration e AgentNode con name=DataAnalyst."""
        node = parse(self.SOURCE).declarations[3]
        assert isinstance(node, AgentNode)
        assert node.name == "DataAnalyst"
        assert node.role == "data"
        assert node.trust == "standard"

    def test_agent_requires_binop_gte(self) -> None:
        """Esempio 6: requires: pd.version >= '2.0' -> BinOpExpr(>=, AttrExpr, StringExpr)."""
        agent = parse(self.SOURCE).declarations[3]
        assert isinstance(agent, AgentNode)
        assert len(agent.requires) == 1
        req = agent.requires[0]
        assert isinstance(req, BinOpExpr)
        assert req.op == ">="
        assert isinstance(req.left, AttrExpr)
        assert req.left.obj == "pd"
        assert req.left.attr == "version"
        assert isinstance(req.right, StringExpr)
        assert req.right.value == '"2.0"'

    def test_agent_ensures_binop_eq(self) -> None:
        """Esempio 6: ensures: output.format == 'dataframe' -> BinOpExpr(==, AttrExpr, StringExpr)."""
        agent = parse(self.SOURCE).declarations[3]
        assert isinstance(agent, AgentNode)
        assert len(agent.ensures) == 1
        ens = agent.ensures[0]
        assert isinstance(ens, BinOpExpr)
        assert ens.op == "=="
        assert isinstance(ens.left, AttrExpr)
        assert ens.left.obj == "output"
        assert ens.left.attr == "format"
        assert isinstance(ens.right, StringExpr)
        assert ens.right.value == '"dataframe"'


# ===========================================================================
# 7. TestExample7SecureAudit
# ===========================================================================


class TestExample7SecureAudit:
    """Esempio 7: SecureAudit - Protocol con Trust + Exclusion + Confidence."""

    SOURCE = textwrap.dedent("""\
        protocol SecureAudit:
            roles: regina, guardiana, backend

            regina asks backend to do task
            backend returns result to regina
            regina asks guardiana to verify
            guardiana returns verdict to regina

            properties:
                always terminates
                no deadlock
                trust >= trusted
                backend cannot send audit_verdict
                confidence >= high
    """)

    def test_protocol_name(self) -> None:
        """Esempio 7: name=SecureAudit."""
        proto = parse(self.SOURCE).declarations[0]
        assert isinstance(proto, ProtocolNode)
        assert proto.name == "SecureAudit"

    def test_three_roles(self) -> None:
        """Esempio 7: 3 roles."""
        proto = parse(self.SOURCE).declarations[0]
        assert isinstance(proto, ProtocolNode)
        assert proto.roles == ("regina", "guardiana", "backend")

    def test_four_steps(self) -> None:
        """Esempio 7: 4 steps lineari."""
        proto = parse(self.SOURCE).declarations[0]
        assert isinstance(proto, ProtocolNode)
        assert len(proto.steps) == 4

    def test_five_properties(self) -> None:
        """Esempio 7: 5 properties."""
        proto = parse(self.SOURCE).declarations[0]
        assert isinstance(proto, ProtocolNode)
        assert len(proto.properties) == 5

    def test_always_terminates(self) -> None:
        """Esempio 7: presenza di AlwaysTerminates."""
        proto = parse(self.SOURCE).declarations[0]
        assert isinstance(proto, ProtocolNode)
        assert any(isinstance(p, AlwaysTerminates) for p in proto.properties)

    def test_no_deadlock(self) -> None:
        """Esempio 7: presenza di NoDeadlock."""
        proto = parse(self.SOURCE).declarations[0]
        assert isinstance(proto, ProtocolNode)
        assert any(isinstance(p, NoDeadlock) for p in proto.properties)

    def test_trust_prop_trusted(self) -> None:
        """Esempio 7: TrustProp con tier='trusted'."""
        proto = parse(self.SOURCE).declarations[0]
        assert isinstance(proto, ProtocolNode)
        trust = next(p for p in proto.properties if isinstance(p, TrustProp))
        assert trust.tier == "trusted"

    def test_exclusion_prop_backend(self) -> None:
        """Esempio 7: ExclusionProp backend cannot send audit_verdict."""
        proto = parse(self.SOURCE).declarations[0]
        assert isinstance(proto, ProtocolNode)
        excl = next(p for p in proto.properties if isinstance(p, ExclusionProp))
        assert excl.role == "backend"
        assert excl.message == "audit_verdict"

    def test_confidence_prop_high(self) -> None:
        """Esempio 7: ConfidenceProp con level='high'."""
        proto = parse(self.SOURCE).declarations[0]
        assert isinstance(proto, ProtocolNode)
        conf = next(p for p in proto.properties if isinstance(p, ConfidenceProp))
        assert conf.level == "high"


# ===========================================================================
# 8. TestExample8RecipeApp
# ===========================================================================


class TestExample8RecipeApp:
    """Esempio 8: RecipeApp - Protocol + Agent nella stessa declaration list."""

    SOURCE = textwrap.dedent("""\
        protocol RecipeApp:
            roles: regina, chef, guardiana

            regina asks chef to do task
            chef returns result to regina
            regina asks guardiana to verify
            guardiana returns verdict to regina

            properties:
                always terminates
                no deadlock
                all roles participate

        agent Chef:
            role: backend
            trust: standard
            requires:
                user.authenticated
            ensures:
                no_recipe_deleted_by_accident
                recipes.saved
    """)

    def test_two_declarations(self) -> None:
        """Esempio 8: 2 declarations (ProtocolNode + AgentNode)."""
        program = parse(self.SOURCE)
        assert len(program.declarations) == 2
        assert isinstance(program.declarations[0], ProtocolNode)
        assert isinstance(program.declarations[1], AgentNode)

    def test_protocol_name(self) -> None:
        """Esempio 8: ProtocolNode name=RecipeApp."""
        proto = parse(self.SOURCE).declarations[0]
        assert isinstance(proto, ProtocolNode)
        assert proto.name == "RecipeApp"

    def test_protocol_roles(self) -> None:
        """Esempio 8: 3 roles."""
        proto = parse(self.SOURCE).declarations[0]
        assert isinstance(proto, ProtocolNode)
        assert proto.roles == ("regina", "chef", "guardiana")

    def test_protocol_three_properties(self) -> None:
        """Esempio 8: 3 properties con AllParticipate."""
        proto = parse(self.SOURCE).declarations[0]
        assert isinstance(proto, ProtocolNode)
        assert len(proto.properties) == 3
        assert any(isinstance(p, AllParticipate) for p in proto.properties)

    def test_agent_name_and_clauses(self) -> None:
        """Esempio 8: AgentNode name=Chef, role=backend, trust=standard."""
        agent = parse(self.SOURCE).declarations[1]
        assert isinstance(agent, AgentNode)
        assert agent.name == "Chef"
        assert agent.role == "backend"
        assert agent.trust == "standard"

    def test_agent_requires_one_attr_expr(self) -> None:
        """Esempio 8: requires ha 1 AttrExpr (user.authenticated)."""
        agent = parse(self.SOURCE).declarations[1]
        assert isinstance(agent, AgentNode)
        assert len(agent.requires) == 1
        req = agent.requires[0]
        assert isinstance(req, AttrExpr)
        assert req.obj == "user"
        assert req.attr == "authenticated"

    def test_agent_ensures_two_exprs(self) -> None:
        """Esempio 8: ensures ha IdentExpr + AttrExpr."""
        agent = parse(self.SOURCE).declarations[1]
        assert isinstance(agent, AgentNode)
        assert len(agent.ensures) == 2
        ens0 = agent.ensures[0]
        assert isinstance(ens0, IdentExpr)
        assert ens0.name == "no_recipe_deleted_by_accident"
        ens1 = agent.ensures[1]
        assert isinstance(ens1, AttrExpr)
        assert ens1.obj == "recipes"
        assert ens1.attr == "saved"


# ===========================================================================
# 9. TestExample9DeepResearch
# ===========================================================================


class TestExample9DeepResearch:
    """Esempio 9: DeepResearch - RecordTypeDecl + ProtocolNode."""

    SOURCE = textwrap.dedent("""\
        type ResearchResult =
            findings: Confident[String]
            sources: List[String]
            methodology: String

        protocol DeepResearch:
            roles: regina, researcher, guardiana

            regina asks researcher to research
            researcher returns report to regina
            regina asks guardiana to verify
            guardiana returns verdict to regina

            properties:
                always terminates
                confidence >= medium
                trust >= standard
    """)

    def test_two_declarations(self) -> None:
        """Esempio 9: 2 declarations (RecordTypeDecl + ProtocolNode)."""
        program = parse(self.SOURCE)
        assert len(program.declarations) == 2
        assert isinstance(program.declarations[0], RecordTypeDecl)
        assert isinstance(program.declarations[1], ProtocolNode)

    def test_record_name_and_fields(self) -> None:
        """Esempio 9: RecordTypeDecl name=ResearchResult con 3 fields."""
        decl = parse(self.SOURCE).declarations[0]
        assert isinstance(decl, RecordTypeDecl)
        assert decl.name == "ResearchResult"
        assert len(decl.fields) == 3

    def test_first_field_generic(self) -> None:
        """Esempio 9: primo field e GenericType('Confident', SimpleType('String'))."""
        decl = parse(self.SOURCE).declarations[0]
        assert isinstance(decl, RecordTypeDecl)
        field = decl.fields[0]
        assert isinstance(field, FieldNode)
        assert field.name == "findings"
        assert isinstance(field.type_expr, GenericType)
        assert field.type_expr.name == "Confident"
        assert isinstance(field.type_expr.arg, SimpleType)
        assert field.type_expr.arg.name == "String"

    def test_second_field_list(self) -> None:
        """Esempio 9: secondo field e GenericType('List', SimpleType('String'))."""
        decl = parse(self.SOURCE).declarations[0]
        assert isinstance(decl, RecordTypeDecl)
        field = decl.fields[1]
        assert isinstance(field, FieldNode)
        assert field.name == "sources"
        assert isinstance(field.type_expr, GenericType)
        assert field.type_expr.name == "List"

    def test_third_field_simple(self) -> None:
        """Esempio 9: terzo field e SimpleType('String')."""
        decl = parse(self.SOURCE).declarations[0]
        assert isinstance(decl, RecordTypeDecl)
        field = decl.fields[2]
        assert isinstance(field, FieldNode)
        assert field.name == "methodology"
        assert isinstance(field.type_expr, SimpleType)
        assert field.type_expr.name == "String"

    def test_protocol_name(self) -> None:
        """Esempio 9: ProtocolNode name=DeepResearch."""
        proto = parse(self.SOURCE).declarations[1]
        assert isinstance(proto, ProtocolNode)
        assert proto.name == "DeepResearch"

    def test_protocol_three_properties(self) -> None:
        """Esempio 9: 3 properties: AlwaysTerminates, ConfidenceProp, TrustProp."""
        proto = parse(self.SOURCE).declarations[1]
        assert isinstance(proto, ProtocolNode)
        assert len(proto.properties) == 3
        conf = next(p for p in proto.properties if isinstance(p, ConfidenceProp))
        assert conf.level == "medium"
        trust = next(p for p in proto.properties if isinstance(p, TrustProp))
        assert trust.tier == "standard"


# ===========================================================================
# 10. TestExample10CompleteProgram
# ===========================================================================


class TestExample10CompleteProgram:
    """Esempio 10: programma completo multi-declaration (il test piu importante)."""

    SOURCE = textwrap.dedent("""\
        use python logging

        type Priority = critical | high | medium | low

        type CodeResult =
            code: Confident[String]
            tests_passed: Number
            coverage: Number

        protocol CodeReview:
            roles: regina, backend, tester, guardiana

            regina asks backend to do task
            backend returns result to regina
            regina asks tester to verify
            tester returns verdict to regina
            regina asks guardiana to verify
            guardiana returns verdict to regina

            properties:
                always terminates
                no deadlock
                task_request before task_result
                backend cannot send audit_verdict
                tester cannot send task_result
                trust >= standard
                all roles participate

        agent CodeBackend:
            role: backend
            trust: standard
            accepts: TaskRequest
            produces: TaskResult
            requires:
                task.well_defined
                task.priority != critical or regina.approved
            ensures:
                output.compiles
                tests.pass(80)
                coverage >= 70

        agent CodeTester:
            role: tester
            trust: trusted
            accepts: AuditRequest
            produces: AuditVerdict
            requires:
                code.compiles
            ensures:
                all_tests.executed
                report.complete
    """)

    def _program(self):
        return parse(self.SOURCE)

    def test_six_declarations(self) -> None:
        """Esempio 10: 6 declarations totali (1 Use + 1 Variant + 1 Record + 1 Protocol + 2 Agent)."""
        program = self._program()
        assert len(program.declarations) == 6

    def test_declaration_types_in_order(self) -> None:
        """Esempio 10: UseNode, VariantTypeDecl, RecordTypeDecl, ProtocolNode, AgentNode, AgentNode."""
        program = self._program()
        decls = program.declarations
        assert isinstance(decls[0], UseNode)
        assert isinstance(decls[1], VariantTypeDecl)
        assert isinstance(decls[2], RecordTypeDecl)
        assert isinstance(decls[3], ProtocolNode)
        assert isinstance(decls[4], AgentNode)
        assert isinstance(decls[5], AgentNode)

    def test_use_logging(self) -> None:
        """Esempio 10: UseNode('logging', None)."""
        decl = self._program().declarations[0]
        assert isinstance(decl, UseNode)
        assert decl.module == "logging"
        assert decl.alias is None

    def test_variant_priority(self) -> None:
        """Esempio 10: VariantTypeDecl('Priority', 4 variants)."""
        decl = self._program().declarations[1]
        assert isinstance(decl, VariantTypeDecl)
        assert decl.name == "Priority"
        assert decl.variants == ("critical", "high", "medium", "low")

    def test_record_code_result(self) -> None:
        """Esempio 10: RecordTypeDecl('CodeResult', 3 fields con Confident[String])."""
        decl = self._program().declarations[2]
        assert isinstance(decl, RecordTypeDecl)
        assert decl.name == "CodeResult"
        assert len(decl.fields) == 3
        # primo field: Confident[String]
        field0 = decl.fields[0]
        assert isinstance(field0, FieldNode)
        assert field0.name == "code"
        assert isinstance(field0.type_expr, GenericType)
        assert field0.type_expr.name == "Confident"
        # secondo e terzo: Number
        for field in decl.fields[1:]:
            assert isinstance(field.type_expr, SimpleType)
            assert field.type_expr.name == "Number"

    def test_protocol_code_review(self) -> None:
        """Esempio 10: ProtocolNode('CodeReview', 4 roles, 6 steps, 7 properties)."""
        proto = self._program().declarations[3]
        assert isinstance(proto, ProtocolNode)
        assert proto.name == "CodeReview"
        assert len(proto.roles) == 4
        assert proto.roles == ("regina", "backend", "tester", "guardiana")
        assert len(proto.steps) == 6
        assert len(proto.properties) == 7

    def test_protocol_seven_property_types(self) -> None:
        """Esempio 10: 7 property instances (6 unique types, ExclusionProp x2)."""
        proto = self._program().declarations[3]
        assert isinstance(proto, ProtocolNode)
        prop_types = {type(p) for p in proto.properties}
        assert AlwaysTerminates in prop_types
        assert NoDeadlock in prop_types
        assert OrderingProp in prop_types
        assert ExclusionProp in prop_types
        assert TrustProp in prop_types
        assert AllParticipate in prop_types

    def test_protocol_two_exclusion_props(self) -> None:
        """Esempio 10: 2 ExclusionProp (backend e tester)."""
        proto = self._program().declarations[3]
        assert isinstance(proto, ProtocolNode)
        excl = [p for p in proto.properties if isinstance(p, ExclusionProp)]
        assert len(excl) == 2
        roles = {p.role for p in excl}
        assert roles == {"backend", "tester"}

    def test_agent_code_backend_basic(self) -> None:
        """Esempio 10: AgentNode('CodeBackend') con role, trust, accepts, produces."""
        agent = self._program().declarations[4]
        assert isinstance(agent, AgentNode)
        assert agent.name == "CodeBackend"
        assert agent.role == "backend"
        assert agent.trust == "standard"
        assert agent.accepts == ("TaskRequest",)
        assert agent.produces == ("TaskResult",)

    def test_agent_code_backend_requires(self) -> None:
        """Esempio 10: CodeBackend requires ha 2 exprs (AttrExpr + BinOpExpr con 'or')."""
        agent = self._program().declarations[4]
        assert isinstance(agent, AgentNode)
        assert len(agent.requires) == 2
        # primo: task.well_defined
        req0 = agent.requires[0]
        assert isinstance(req0, AttrExpr)
        assert req0.obj == "task"
        assert req0.attr == "well_defined"
        # secondo: task.priority != critical or regina.approved
        req1 = agent.requires[1]
        assert isinstance(req1, BinOpExpr)
        assert req1.op == "or"

    def test_agent_code_backend_requires_or_structure(self) -> None:
        """Esempio 10: lato sinistro dell'or e BinOpExpr(!=), lato destro e AttrExpr."""
        agent = self._program().declarations[4]
        assert isinstance(agent, AgentNode)
        req1 = agent.requires[1]
        assert isinstance(req1, BinOpExpr)
        assert req1.op == "or"
        left = req1.left
        assert isinstance(left, BinOpExpr)
        assert left.op == "!="
        assert isinstance(left.left, AttrExpr)
        assert left.left.obj == "task"
        assert left.left.attr == "priority"
        assert isinstance(left.right, IdentExpr)
        assert left.right.name == "critical"
        right = req1.right
        assert isinstance(right, AttrExpr)
        assert right.obj == "regina"
        assert right.attr == "approved"

    def test_agent_code_backend_ensures(self) -> None:
        """Esempio 10: CodeBackend ensures ha 3 exprs."""
        agent = self._program().declarations[4]
        assert isinstance(agent, AgentNode)
        assert len(agent.ensures) == 3
        # output.compiles
        ens0 = agent.ensures[0]
        assert isinstance(ens0, AttrExpr)
        assert ens0.obj == "output"
        assert ens0.attr == "compiles"
        # tests.pass(80)
        ens1 = agent.ensures[1]
        assert isinstance(ens1, MethodCallExpr)
        assert ens1.obj == "tests"
        assert ens1.method == "pass"
        # coverage >= 70
        ens2 = agent.ensures[2]
        assert isinstance(ens2, BinOpExpr)
        assert ens2.op == ">="
        assert isinstance(ens2.left, IdentExpr)
        assert ens2.left.name == "coverage"
        assert isinstance(ens2.right, NumberExpr)
        assert ens2.right.value == "70"

    def test_agent_code_tester(self) -> None:
        """Esempio 10: secondo AgentNode e CodeTester con trust=trusted."""
        program = self._program()
        # CodeTester is one of the 6 declarations; find by name
        agents = [d for d in program.declarations if isinstance(d, AgentNode)]
        assert len(agents) == 2
        tester = next(a for a in agents if a.name == "CodeTester")
        assert tester.role == "tester"
        assert tester.trust == "trusted"
        assert tester.accepts == ("AuditRequest",)
        assert tester.produces == ("AuditVerdict",)

    def test_agent_code_tester_requires_ensures(self) -> None:
        """Esempio 10: CodeTester requires 1 expr, ensures 2 exprs."""
        program = self._program()
        agents = [d for d in program.declarations if isinstance(d, AgentNode)]
        tester = next(a for a in agents if a.name == "CodeTester")
        assert len(tester.requires) == 1
        req = tester.requires[0]
        assert isinstance(req, AttrExpr)
        assert req.obj == "code"
        assert req.attr == "compiles"
        assert len(tester.ensures) == 2
        ens0 = tester.ensures[0]
        assert isinstance(ens0, AttrExpr)
        assert ens0.obj == "all_tests"
        assert ens0.attr == "executed"
        ens1 = tester.ensures[1]
        assert isinstance(ens1, AttrExpr)
        assert ens1.obj == "report"
        assert ens1.attr == "complete"


# ===========================================================================
# 11. TestCrossConstruct
# ===========================================================================


class TestCrossConstruct:
    """Edge cases e error paths cross-costrutto."""

    def test_empty_program(self) -> None:
        """parse('') -> ProgramNode con 0 declarations."""
        program = parse("")
        assert isinstance(program, ProgramNode)
        assert program.declarations == ()

    def test_mixed_blank_lines(self) -> None:
        """Programma con molte blank lines tra declarations -> parsa correttamente."""
        src = textwrap.dedent("""\
            use python os


            type Status = ok | fail


            protocol Simple:
                roles: a, b

                a asks b to do task
                b returns result to a
        """)
        program = parse(src)
        assert len(program.declarations) == 3
        assert isinstance(program.declarations[0], UseNode)
        assert isinstance(program.declarations[1], VariantTypeDecl)
        assert isinstance(program.declarations[2], ProtocolNode)

    def test_comments_between_declarations(self) -> None:
        """Programma con commenti # tra declarations -> parsa correttamente."""
        src = textwrap.dedent("""\
            # Primo use
            use python sys
            # Tipo di stato
            type MyStatus = active | inactive
        """)
        program = parse(src)
        assert len(program.declarations) == 2
        assert isinstance(program.declarations[0], UseNode)
        assert isinstance(program.declarations[1], VariantTypeDecl)

    def test_error_invalid_declaration_keyword(self) -> None:
        """'foo bar' -> ParseError: keyword non riconosciuto."""
        with pytest.raises(ParseError):
            parse("foo bar\n")

    def test_error_number_as_declaration_start(self) -> None:
        """Numero come inizio declaration -> ParseError."""
        with pytest.raises(ParseError):
            parse("42 foo\n")
