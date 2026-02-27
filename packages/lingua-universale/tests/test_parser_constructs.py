# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for the Lingua Universale v0.2 parser constructs (C1.3.4).

Groups:
    1. TestParseExpr          - expression parser: literals, operators, precedence
    2. TestParseUseDecl       - use declarations with module paths and aliases
    3. TestParseTypeDecl      - variant and record type declarations
    4. TestParseAgentDecl     - agent declarations with all clauses
    5. TestCanonicalExamples  - end-to-end examples from DESIGN_C1_2

NOTE: No __init__.py in this directory (Package Shadowing Fix, S340).
"""

from __future__ import annotations

import textwrap

import pytest

from cervellaswarm_lingua_universale._parser import ParseError, parse
from cervellaswarm_lingua_universale._ast import (
    AgentNode,
    AlwaysTerminates,
    AttrExpr,
    BinOpExpr,
    FieldNode,
    GenericType,
    GroupExpr,
    IdentExpr,
    Loc,
    MethodCallExpr,
    NoDeadlock,
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


# ===========================================================================
# Helpers
# ===========================================================================


def _parse_single_expr(source: str):
    """Parse a single expression by wrapping it in a minimal agent requires clause."""
    wrapped = textwrap.dedent(f"""\
        agent _Test:
            requires: {source}
    """)
    tree = parse(wrapped)
    agent = tree.declarations[0]
    assert isinstance(agent, AgentNode)
    assert len(agent.requires) == 1
    return agent.requires[0]


def _parse_use(source: str) -> UseNode:
    """Parse a single use declaration."""
    tree = parse(source + "\n")
    assert len(tree.declarations) == 1
    node = tree.declarations[0]
    assert isinstance(node, UseNode)
    return node


def _parse_type(source: str) -> VariantTypeDecl | RecordTypeDecl:
    """Parse a single type declaration."""
    tree = parse(source + "\n")
    assert len(tree.declarations) == 1
    node = tree.declarations[0]
    assert isinstance(node, (VariantTypeDecl, RecordTypeDecl))
    return node


def _parse_agent(source: str) -> AgentNode:
    """Parse a single agent declaration."""
    tree = parse(textwrap.dedent(source))
    assert len(tree.declarations) == 1
    node = tree.declarations[0]
    assert isinstance(node, AgentNode)
    return node


# ===========================================================================
# 1. TestParseExpr
# ===========================================================================


class TestParseExpr:
    """Expression parser: literals, attribute access, method calls, operators."""

    def test_bare_identifier(self) -> None:
        expr = _parse_single_expr("x")
        assert isinstance(expr, IdentExpr)
        assert expr.name == "x"

    def test_number_literal(self) -> None:
        expr = _parse_single_expr("42")
        assert isinstance(expr, NumberExpr)
        assert expr.value == "42"

    def test_string_literal(self) -> None:
        expr = _parse_single_expr('"hello"')
        assert isinstance(expr, StringExpr)
        assert expr.value == '"hello"'

    def test_attribute_access(self) -> None:
        expr = _parse_single_expr("task.well_defined")
        assert isinstance(expr, AttrExpr)
        assert expr.obj == "task"
        assert expr.attr == "well_defined"

    def test_method_call_no_args(self) -> None:
        expr = _parse_single_expr("obj.method()")
        assert isinstance(expr, MethodCallExpr)
        assert expr.obj == "obj"
        assert expr.method == "method"
        assert expr.args == ()

    def test_method_call_one_arg(self) -> None:
        expr = _parse_single_expr("tests.pass(80)")
        assert isinstance(expr, MethodCallExpr)
        assert expr.obj == "tests"
        assert expr.method == "pass"
        assert len(expr.args) == 1
        assert isinstance(expr.args[0], NumberExpr)
        assert expr.args[0].value == "80"

    def test_method_call_multi_args(self) -> None:
        expr = _parse_single_expr("obj.method(1, 2)")
        assert isinstance(expr, MethodCallExpr)
        assert len(expr.args) == 2
        assert isinstance(expr.args[0], NumberExpr)
        assert isinstance(expr.args[1], NumberExpr)

    def test_grouped_expr(self) -> None:
        expr = _parse_single_expr("(x)")
        assert isinstance(expr, GroupExpr)
        assert isinstance(expr.inner, IdentExpr)
        assert expr.inner.name == "x"

    def test_comparison_eq(self) -> None:
        expr = _parse_single_expr("x == y")
        assert isinstance(expr, BinOpExpr)
        assert expr.op == "=="
        assert isinstance(expr.left, IdentExpr)
        assert isinstance(expr.right, IdentExpr)

    def test_comparison_neq(self) -> None:
        expr = _parse_single_expr("x != y")
        assert isinstance(expr, BinOpExpr)
        assert expr.op == "!="

    def test_comparison_lt(self) -> None:
        expr = _parse_single_expr("x < y")
        assert isinstance(expr, BinOpExpr)
        assert expr.op == "<"

    def test_comparison_gt(self) -> None:
        expr = _parse_single_expr("x > y")
        assert isinstance(expr, BinOpExpr)
        assert expr.op == ">"

    def test_comparison_lte(self) -> None:
        expr = _parse_single_expr("x <= y")
        assert isinstance(expr, BinOpExpr)
        assert expr.op == "<="

    def test_comparison_gte(self) -> None:
        expr = _parse_single_expr("x >= y")
        assert isinstance(expr, BinOpExpr)
        assert expr.op == ">="

    def test_and_expr(self) -> None:
        expr = _parse_single_expr("x and y")
        assert isinstance(expr, BinOpExpr)
        assert expr.op == "and"
        assert isinstance(expr.left, IdentExpr)
        assert isinstance(expr.right, IdentExpr)

    def test_or_expr(self) -> None:
        expr = _parse_single_expr("x or y")
        assert isinstance(expr, BinOpExpr)
        assert expr.op == "or"

    def test_not_expr(self) -> None:
        expr = _parse_single_expr("not x")
        assert isinstance(expr, NotExpr)
        assert isinstance(expr.operand, IdentExpr)
        assert expr.operand.name == "x"

    def test_precedence_and_before_or(self) -> None:
        # "a and b or c" must parse as "(a and b) or c"
        expr = _parse_single_expr("a and b or c")
        assert isinstance(expr, BinOpExpr)
        assert expr.op == "or"
        assert isinstance(expr.left, BinOpExpr)
        assert expr.left.op == "and"
        assert isinstance(expr.right, IdentExpr)
        assert expr.right.name == "c"

    def test_complex_expr(self) -> None:
        # "task.priority != critical or regina.approved"
        # -> BinOpExpr("or", BinOpExpr("!=", AttrExpr, IdentExpr), AttrExpr)
        expr = _parse_single_expr("task.priority != critical or regina.approved")
        assert isinstance(expr, BinOpExpr)
        assert expr.op == "or"
        assert isinstance(expr.left, BinOpExpr)
        assert expr.left.op == "!="
        assert isinstance(expr.left.left, AttrExpr)
        assert expr.left.left.obj == "task"
        assert expr.left.left.attr == "priority"
        assert isinstance(expr.left.right, IdentExpr)
        assert expr.left.right.name == "critical"
        assert isinstance(expr.right, AttrExpr)
        assert expr.right.obj == "regina"
        assert expr.right.attr == "approved"

    def test_double_negation(self) -> None:
        # F5: not not x -> NotExpr(NotExpr(IdentExpr))
        expr = _parse_single_expr("not not x")
        assert isinstance(expr, NotExpr)
        assert isinstance(expr.operand, NotExpr)
        assert isinstance(expr.operand.operand, IdentExpr)
        assert expr.operand.operand.name == "x"

    def test_expr_loc_is_set(self) -> None:
        expr = _parse_single_expr("x")
        assert isinstance(expr, IdentExpr)
        assert isinstance(expr.loc, Loc)
        assert expr.loc.line >= 1


# ===========================================================================
# 2. TestParseUseDecl
# ===========================================================================


class TestParseUseDecl:
    """use declarations: module paths and aliases."""

    def test_use_simple_module(self) -> None:
        node = _parse_use("use python math")
        assert node.module == "math"
        assert node.alias is None

    def test_use_with_alias(self) -> None:
        node = _parse_use("use python datetime as dt")
        assert node.module == "datetime"
        assert node.alias == "dt"

    def test_use_dotted_module(self) -> None:
        node = _parse_use("use python os.path")
        assert node.module == "os.path"
        assert node.alias is None

    def test_use_dotted_module_with_alias(self) -> None:
        node = _parse_use("use python os.path as osp")
        assert node.module == "os.path"
        assert node.alias == "osp"

    def test_use_missing_python_raises(self) -> None:
        with pytest.raises(ParseError, match="'python'"):
            parse("use math\n")

    def test_use_missing_module_raises(self) -> None:
        with pytest.raises(ParseError):
            parse("use python\n")

    def test_use_loc_is_set(self) -> None:
        node = _parse_use("use python math")
        assert isinstance(node.loc, Loc)
        assert node.loc.line >= 1


# ===========================================================================
# 3. TestParseTypeDecl
# ===========================================================================


class TestParseTypeDecl:
    """type declarations: variant and record forms."""

    def test_variant_three_variants(self) -> None:
        node = _parse_type("type TaskStatus = ok | fail | blocked")
        assert isinstance(node, VariantTypeDecl)
        assert node.name == "TaskStatus"
        assert node.variants == ("ok", "fail", "blocked")

    def test_variant_four_variants(self) -> None:
        node = _parse_type("type Priority = critical | high | medium | low")
        assert isinstance(node, VariantTypeDecl)
        assert node.name == "Priority"
        assert len(node.variants) == 4
        assert node.variants == ("critical", "high", "medium", "low")

    def test_variant_two_variants_minimum(self) -> None:
        node = _parse_type("type Flag = yes | no")
        assert isinstance(node, VariantTypeDecl)
        assert node.variants == ("yes", "no")

    def test_record_simple_fields(self) -> None:
        src = textwrap.dedent("""\
            type AnalysisResult =
                conclusion: String
                confidence: Number
        """)
        node = _parse_type(src)
        assert isinstance(node, RecordTypeDecl)
        assert node.name == "AnalysisResult"
        assert len(node.fields) == 2
        assert node.fields[0].name == "conclusion"
        assert node.fields[1].name == "confidence"

    def test_record_optional_field(self) -> None:
        src = textwrap.dedent("""\
            type Result =
                value: String
                alternative: String?
        """)
        node = _parse_type(src)
        assert isinstance(node, RecordTypeDecl)
        field = node.fields[1]
        assert isinstance(field, FieldNode)
        assert isinstance(field.type_expr, SimpleType)
        assert field.type_expr.optional is True
        assert field.type_expr.name == "String"

    def test_record_generic_field(self) -> None:
        src = textwrap.dedent("""\
            type Result =
                confidence: Confident[String]
        """)
        node = _parse_type(src)
        assert isinstance(node, RecordTypeDecl)
        field = node.fields[0]
        assert isinstance(field.type_expr, GenericType)
        assert field.type_expr.name == "Confident"
        assert isinstance(field.type_expr.arg, SimpleType)
        assert field.type_expr.arg.name == "String"

    def test_record_nested_generic_field(self) -> None:
        src = textwrap.dedent("""\
            type Wrapper =
                items: List[Confident[String]]
        """)
        node = _parse_type(src)
        assert isinstance(node, RecordTypeDecl)
        field = node.fields[0]
        assert isinstance(field.type_expr, GenericType)
        assert field.type_expr.name == "List"
        assert isinstance(field.type_expr.arg, GenericType)
        assert field.type_expr.arg.name == "Confident"

    def test_optional_generic_type(self) -> None:
        # F7: List[String]? -> GenericType with optional=True
        src = textwrap.dedent("""\
            type Result =
                items: List[String]?
        """)
        node = _parse_type(src)
        assert isinstance(node, RecordTypeDecl)
        field = node.fields[0]
        assert isinstance(field.type_expr, GenericType)
        assert field.type_expr.name == "List"
        assert field.type_expr.optional is True
        assert isinstance(field.type_expr.arg, SimpleType)
        assert field.type_expr.arg.name == "String"

    def test_variant_single_variant_raises(self) -> None:
        with pytest.raises(ParseError, match="at least 2 variants"):
            parse("type Solo = only\n")

    def test_record_empty_body_raises(self) -> None:
        # An indented block with no fields should raise ParseError.
        # We simulate an empty body by providing only a blank line inside.
        src = textwrap.dedent("""\
            type Empty =
        """)
        # Without INDENT, tokenizer won't produce an INDENT token,
        # so the parser will raise when expecting INDENT after NEWLINE.
        with pytest.raises(ParseError):
            parse(src)

    def test_type_loc_is_set(self) -> None:
        node = _parse_type("type Status = ok | fail")
        assert isinstance(node.loc, Loc)
        assert node.loc.line >= 1


# ===========================================================================
# 4. TestParseAgentDecl
# ===========================================================================


class TestParseAgentDecl:
    """Agent declarations: all optional clauses."""

    def test_agent_basic_role_and_trust(self) -> None:
        src = """\
agent Worker:
    role: backend
    trust: standard
"""
        agent = _parse_agent(src)
        assert agent.name == "Worker"
        assert agent.role == "backend"
        assert agent.trust == "standard"
        assert agent.accepts == ()
        assert agent.produces == ()

    def test_agent_accepts_and_produces(self) -> None:
        src = """\
agent Worker:
    accepts: TaskRequest, PlanRequest
    produces: TaskResult
"""
        agent = _parse_agent(src)
        assert agent.accepts == ("TaskRequest", "PlanRequest")
        assert agent.produces == ("TaskResult",)

    def test_agent_requires_block(self) -> None:
        src = """\
agent Worker:
    requires:
        task.well_defined
        task.priority != critical
"""
        agent = _parse_agent(src)
        assert len(agent.requires) == 2
        assert isinstance(agent.requires[0], AttrExpr)
        assert isinstance(agent.requires[1], BinOpExpr)

    def test_agent_ensures_block(self) -> None:
        src = """\
agent Worker:
    ensures:
        result.complete
        result.verified
"""
        agent = _parse_agent(src)
        assert len(agent.ensures) == 2
        assert isinstance(agent.ensures[0], AttrExpr)

    def test_agent_requires_inline(self) -> None:
        src = """\
agent Checker:
    requires: task.well_defined
"""
        agent = _parse_agent(src)
        assert len(agent.requires) == 1
        assert isinstance(agent.requires[0], AttrExpr)

    def test_agent_full_all_clauses(self) -> None:
        src = """\
agent FullAgent:
    role: tester
    trust: trusted
    accepts: TaskRequest
    produces: TestResult
    requires: task.well_defined
    ensures: result.verified
"""
        agent = _parse_agent(src)
        assert agent.name == "FullAgent"
        assert agent.role == "tester"
        assert agent.trust == "trusted"
        assert agent.accepts == ("TaskRequest",)
        assert agent.produces == ("TestResult",)
        assert len(agent.requires) == 1
        assert len(agent.ensures) == 1

    def test_agent_unknown_clause_raises(self) -> None:
        src = """\
agent Bad:
    unknown: value
"""
        with pytest.raises(ParseError, match="unknown agent clause"):
            _parse_agent(src)

    def test_agent_invalid_trust_raises(self) -> None:
        src = """\
agent Bad:
    trust: superuser
"""
        with pytest.raises(ParseError, match="invalid trust tier"):
            _parse_agent(src)

    def test_agent_blank_lines_in_body(self) -> None:
        src = """\
agent Worker:
    role: backend

    trust: standard
"""
        agent = _parse_agent(src)
        assert agent.role == "backend"
        assert agent.trust == "standard"

    def test_agent_duplicate_clause_raises(self) -> None:
        # P2/F1: duplicate clauses must raise ParseError
        src = """\
agent Bad:
    role: backend
    role: frontend
"""
        with pytest.raises(ParseError, match="duplicate agent clause 'role'"):
            _parse_agent(src)

    def test_agent_duplicate_requires_raises(self) -> None:
        src = """\
agent Bad:
    requires: x.valid
    requires: y.valid
"""
        with pytest.raises(ParseError, match="duplicate agent clause 'requires'"):
            _parse_agent(src)

    def test_agent_loc_is_set(self) -> None:
        src = """\
agent Worker:
    role: backend
"""
        agent = _parse_agent(src)
        assert isinstance(agent.loc, Loc)
        assert agent.loc.line >= 1


# ===========================================================================
# 5. TestCanonicalExamples
# ===========================================================================


class TestCanonicalExamples:
    """End-to-end examples from DESIGN_C1_2_SYNTAX_GRAMMAR.md."""

    def test_example3_worker_agent(self) -> None:
        """Esempio 3: Worker agent with all clauses."""
        src = textwrap.dedent("""\
            agent Worker:
                role: backend
                trust: standard
                accepts: TaskRequest
                produces: TaskResult
                requires: task.well_defined
                ensures: result.complete
        """)
        tree = parse(src)
        assert len(tree.declarations) == 1
        agent = tree.declarations[0]
        assert isinstance(agent, AgentNode)
        assert agent.name == "Worker"
        assert agent.role == "backend"
        assert agent.trust == "standard"
        assert agent.accepts == ("TaskRequest",)
        assert agent.produces == ("TaskResult",)
        assert len(agent.requires) == 1
        assert len(agent.ensures) == 1

    def test_example4_analysis_result_record(self) -> None:
        """Esempio 4: AnalysisResult record type."""
        src = textwrap.dedent("""\
            type AnalysisResult =
                conclusion: String
                confidence: Number
                reasoning: String?
        """)
        tree = parse(src)
        assert len(tree.declarations) == 1
        node = tree.declarations[0]
        assert isinstance(node, RecordTypeDecl)
        assert node.name == "AnalysisResult"
        assert len(node.fields) == 3
        names = [f.name for f in node.fields]
        assert names == ["conclusion", "confidence", "reasoning"]
        # Third field is optional
        assert isinstance(node.fields[2].type_expr, SimpleType)
        assert node.fields[2].type_expr.optional is True

    def test_example5_variant_types(self) -> None:
        """Esempio 5: TaskStatus, AuditVerdict, Priority variants."""
        src = textwrap.dedent("""\
            type TaskStatus = ok | fail | blocked
            type AuditVerdict = approved | rejected | needs_review
            type Priority = critical | high | medium | low
        """)
        tree = parse(src)
        assert len(tree.declarations) == 3

        task_status = tree.declarations[0]
        assert isinstance(task_status, VariantTypeDecl)
        assert task_status.name == "TaskStatus"
        assert task_status.variants == ("ok", "fail", "blocked")

        audit_verdict = tree.declarations[1]
        assert isinstance(audit_verdict, VariantTypeDecl)
        assert audit_verdict.name == "AuditVerdict"
        assert len(audit_verdict.variants) == 3

        priority = tree.declarations[2]
        assert isinstance(priority, VariantTypeDecl)
        assert priority.name == "Priority"
        assert len(priority.variants) == 4

    def test_example6_use_and_agent_with_expressions(self) -> None:
        """Esempio 6: use + agent with requires/ensures using string comparison."""
        src = textwrap.dedent("""\
            use python os.path as osp
            agent FileAgent:
                role: backend
                trust: standard
                requires: path.exists
                ensures: result.saved
        """)
        tree = parse(src)
        assert len(tree.declarations) == 2

        use_node = tree.declarations[0]
        assert isinstance(use_node, UseNode)
        assert use_node.module == "os.path"
        assert use_node.alias == "osp"

        agent = tree.declarations[1]
        assert isinstance(agent, AgentNode)
        assert agent.name == "FileAgent"
        assert len(agent.requires) == 1
        assert isinstance(agent.requires[0], AttrExpr)
        assert agent.requires[0].obj == "path"
        assert agent.requires[0].attr == "exists"

    def test_example8_recipe_app_protocol_and_agent(self) -> None:
        """Esempio 8: RecipeApp protocol + Chef agent."""
        src = textwrap.dedent("""\
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
                requires: user.authenticated
                ensures: recipes.saved
        """)
        tree = parse(src)
        assert len(tree.declarations) == 2

        protocol = tree.declarations[0]
        assert isinstance(protocol, ProtocolNode)
        assert protocol.name == "RecipeApp"
        assert protocol.roles == ("regina", "chef", "guardiana")
        assert len(protocol.steps) == 4
        assert len(protocol.properties) == 3
        assert isinstance(protocol.properties[0], AlwaysTerminates)
        assert isinstance(protocol.properties[1], NoDeadlock)

        agent = tree.declarations[1]
        assert isinstance(agent, AgentNode)
        assert agent.name == "Chef"
        assert agent.role == "backend"
        assert len(agent.requires) == 1
        assert isinstance(agent.requires[0], AttrExpr)
        assert agent.requires[0].obj == "user"
        assert agent.requires[0].attr == "authenticated"
        assert len(agent.ensures) == 1
        assert isinstance(agent.ensures[0], AttrExpr)
        assert agent.ensures[0].obj == "recipes"
        assert agent.ensures[0].attr == "saved"

    def test_example9_deep_research_type_and_protocol(self) -> None:
        """Esempio 9: ResearchResult type + DeepResearch protocol."""
        src = textwrap.dedent("""\
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
        tree = parse(src)
        assert len(tree.declarations) == 2

        record = tree.declarations[0]
        assert isinstance(record, RecordTypeDecl)
        assert record.name == "ResearchResult"
        assert len(record.fields) == 3
        assert isinstance(record.fields[0].type_expr, GenericType)
        assert record.fields[0].type_expr.name == "Confident"

        protocol = tree.declarations[1]
        assert isinstance(protocol, ProtocolNode)
        assert protocol.name == "DeepResearch"
        assert len(protocol.steps) == 4
        assert len(protocol.properties) == 3

    def test_example10_partial_use_type_agent(self) -> None:
        """Esempio 10 partial: program with use + type + agent."""
        src = textwrap.dedent("""\
            use python math
            type Result = ok | fail
            agent Processor:
                role: backend
                trust: trusted
                accepts: TaskRequest
                produces: TaskResult
                requires: task.valid
        """)
        tree = parse(src)
        assert isinstance(tree, ProgramNode)
        assert len(tree.declarations) == 3

        assert isinstance(tree.declarations[0], UseNode)
        assert tree.declarations[0].module == "math"

        assert isinstance(tree.declarations[1], VariantTypeDecl)
        assert tree.declarations[1].name == "Result"

        agent = tree.declarations[2]
        assert isinstance(agent, AgentNode)
        assert agent.name == "Processor"
        assert agent.trust == "trusted"
        assert len(agent.requires) == 1
