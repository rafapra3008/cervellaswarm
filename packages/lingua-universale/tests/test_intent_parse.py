# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Core tests for the intent parser (B.4).

Tests the happy path: valid intent notation -> Protocol objects.
Covers all 14 MessageKind mappings, standard protocols, branching,
and integration with downstream modules.
"""

import pytest

from cervellaswarm_lingua_universale.intent import (
    IntentParseError,
    IntentParseResult,
    parse_intent,
    parse_intent_protocol,
)
from cervellaswarm_lingua_universale.protocols import (
    Protocol,
    ProtocolChoice,
    ProtocolStep,
)
from cervellaswarm_lingua_universale.types import MessageKind


# ============================================================
# Basic parsing
# ============================================================


class TestBasicParsing:
    """Test fundamental parsing of intent notation."""

    def test_simple_two_step(self):
        p = parse_intent_protocol("""
            protocol SimpleTask:
                roles: regina, worker

                regina asks worker to do task
                worker returns result to regina
        """)
        assert p.name == "SimpleTask"
        assert p.roles == ("regina", "worker")
        assert len(p.elements) == 2

    def test_four_step_with_audit(self):
        p = parse_intent_protocol("""
            protocol DelegateTask:
                roles: regina, worker, guardiana

                regina asks worker to do task
                worker returns result to regina
                regina asks guardiana to verify
                guardiana returns verdict to regina
        """)
        assert p.name == "DelegateTask"
        assert p.roles == ("regina", "worker", "guardiana")
        assert len(p.elements) == 4

    def test_research_flow(self):
        p = parse_intent_protocol("""
            protocol ResearchFlow:
                roles: regina, researcher, guardiana

                regina asks researcher to research
                researcher returns report to regina
                regina asks guardiana to verify
                guardiana returns verdict to regina
        """)
        assert p.name == "ResearchFlow"
        assert p.roles == ("regina", "researcher", "guardiana")
        assert len(p.elements) == 4

    def test_parse_intent_returns_result(self):
        result = parse_intent("""
            protocol Test:
                roles: a, b

                a asks b to do task
                b returns result to a
        """)
        assert isinstance(result, IntentParseResult)
        assert isinstance(result.protocol, Protocol)
        assert result.source_text.strip().startswith("protocol")
        assert result.warnings == ()

    def test_protocol_name_preserved(self):
        p = parse_intent_protocol("""
            protocol MyCustomFlow:
                roles: leader, worker

                leader asks worker to do task
                worker returns result to leader
        """)
        assert p.name == "MyCustomFlow"

    def test_custom_role_names(self):
        p = parse_intent_protocol("""
            protocol CustomRoles:
                roles: manager, developer, reviewer

                manager asks developer to do task
                developer returns result to manager
                manager asks reviewer to verify
                reviewer returns verdict to manager
        """)
        assert p.roles == ("manager", "developer", "reviewer")


# ============================================================
# All 14 MessageKind mappings
# ============================================================


class TestAllMessageKinds:
    """Verify each of the 14 MessageKind values can be produced."""

    def test_task_request(self):
        p = parse_intent_protocol("""
            protocol T:
                roles: a, b
                a asks b to do task
                b returns result to a
        """)
        step = p.elements[0]
        assert isinstance(step, ProtocolStep)
        assert step.message_kind == MessageKind.TASK_REQUEST

    def test_task_result(self):
        p = parse_intent_protocol("""
            protocol T:
                roles: a, b
                a asks b to do task
                b returns result to a
        """)
        step = p.elements[1]
        assert isinstance(step, ProtocolStep)
        assert step.message_kind == MessageKind.TASK_RESULT

    def test_audit_request(self):
        p = parse_intent_protocol("""
            protocol T:
                roles: a, b
                a asks b to verify
                b returns verdict to a
        """)
        assert p.elements[0].message_kind == MessageKind.AUDIT_REQUEST

    def test_audit_verdict(self):
        p = parse_intent_protocol("""
            protocol T:
                roles: a, b
                a asks b to verify
                b returns verdict to a
        """)
        assert p.elements[1].message_kind == MessageKind.AUDIT_VERDICT

    def test_plan_request(self):
        p = parse_intent_protocol("""
            protocol T:
                roles: a, b
                a asks b to plan
                b proposes plan to a
        """)
        assert p.elements[0].message_kind == MessageKind.PLAN_REQUEST

    def test_plan_proposal(self):
        p = parse_intent_protocol("""
            protocol T:
                roles: a, b
                a asks b to plan
                b proposes plan to a
        """)
        assert p.elements[1].message_kind == MessageKind.PLAN_PROPOSAL

    def test_plan_decision(self):
        p = parse_intent_protocol("""
            protocol T:
                roles: a, b
                a asks b to plan
                b proposes plan to a
                a tells b decision
                b returns result to a
        """)
        assert p.elements[2].message_kind == MessageKind.PLAN_DECISION

    def test_research_query(self):
        p = parse_intent_protocol("""
            protocol T:
                roles: a, b
                a asks b to research
                b returns report to a
        """)
        assert p.elements[0].message_kind == MessageKind.RESEARCH_QUERY

    def test_research_report(self):
        p = parse_intent_protocol("""
            protocol T:
                roles: a, b
                a asks b to research
                b returns report to a
        """)
        assert p.elements[1].message_kind == MessageKind.RESEARCH_REPORT

    def test_dm(self):
        p = parse_intent_protocol("""
            protocol T:
                roles: a, b
                a sends message to b
                b returns result to a
        """)
        assert p.elements[0].message_kind == MessageKind.DM

    def test_broadcast(self):
        p = parse_intent_protocol("""
            protocol T:
                roles: a, b
                a sends broadcast to b
                b returns result to a
        """)
        assert p.elements[0].message_kind == MessageKind.BROADCAST

    def test_shutdown_request(self):
        p = parse_intent_protocol("""
            protocol T:
                roles: a, b
                a sends shutdown to b
                b sends ack to a
        """)
        assert p.elements[0].message_kind == MessageKind.SHUTDOWN_REQUEST

    def test_shutdown_ack(self):
        p = parse_intent_protocol("""
            protocol T:
                roles: a, b
                a sends shutdown to b
                b sends ack to a
        """)
        assert p.elements[1].message_kind == MessageKind.SHUTDOWN_ACK

    def test_context_inject(self):
        p = parse_intent_protocol("""
            protocol T:
                roles: a, b
                a sends context to b
                b returns result to a
        """)
        assert p.elements[0].message_kind == MessageKind.CONTEXT_INJECT


# ============================================================
# Sender/receiver extraction
# ============================================================


class TestSenderReceiver:
    """Verify correct sender/receiver extraction from action phrases."""

    def test_asks_to_do_task(self):
        p = parse_intent_protocol("""
            protocol T:
                roles: alpha, beta
                alpha asks beta to do task
                beta returns result to alpha
        """)
        step = p.elements[0]
        assert step.sender == "alpha"
        assert step.receiver == "beta"

    def test_returns_result_to(self):
        p = parse_intent_protocol("""
            protocol T:
                roles: alpha, beta
                alpha asks beta to do task
                beta returns result to alpha
        """)
        step = p.elements[1]
        assert step.sender == "beta"
        assert step.receiver == "alpha"

    def test_tells_decision(self):
        p = parse_intent_protocol("""
            protocol T:
                roles: leader, planner
                leader asks planner to plan
                planner proposes plan to leader
                leader tells planner decision
                planner returns result to leader
        """)
        step = p.elements[2]
        assert step.sender == "leader"
        assert step.receiver == "planner"

    def test_proposes_plan_to(self):
        p = parse_intent_protocol("""
            protocol T:
                roles: boss, architect
                boss asks architect to plan
                architect proposes plan to boss
        """)
        step = p.elements[1]
        assert step.sender == "architect"
        assert step.receiver == "boss"


# ============================================================
# Branching (choice)
# ============================================================


class TestBranching:
    """Test choice/branching in intent notation."""

    def test_simple_choice(self):
        p = parse_intent_protocol("""
            protocol ChoiceFlow:
                roles: leader, worker

                when leader decides:
                    go:
                        leader asks worker to do task
                        worker returns result to leader
                    stop:
                        leader sends shutdown to worker
                        worker sends ack to leader
        """)
        assert len(p.elements) == 1
        choice = p.elements[0]
        assert isinstance(choice, ProtocolChoice)
        assert choice.decider == "leader"
        assert "go" in choice.branches
        assert "stop" in choice.branches
        assert len(choice.branches["go"]) == 2
        assert len(choice.branches["stop"]) == 2

    def test_architect_flow_with_choice(self):
        p = parse_intent_protocol("""
            protocol ArchitectFlow:
                roles: regina, architect, worker, guardiana

                regina asks architect to plan
                architect proposes plan to regina

                when regina decides:
                    approve:
                        regina tells architect decision
                        regina asks worker to do task
                        worker returns result to regina
                        regina asks guardiana to verify
                        guardiana returns verdict to regina
                    reject:
                        regina tells architect decision
                        architect proposes plan to regina
        """)
        assert p.name == "ArchitectFlow"
        assert len(p.elements) == 3  # 2 steps + 1 choice
        assert isinstance(p.elements[0], ProtocolStep)
        assert isinstance(p.elements[1], ProtocolStep)
        assert isinstance(p.elements[2], ProtocolChoice)

        choice = p.elements[2]
        assert choice.decider == "regina"
        assert len(choice.branches["approve"]) == 5
        assert len(choice.branches["reject"]) == 2

    def test_three_branches(self):
        p = parse_intent_protocol("""
            protocol TripleChoice:
                roles: manager, dev, qa

                when manager decides:
                    build:
                        manager asks dev to do task
                        dev returns result to manager
                    test:
                        manager asks qa to verify
                        qa returns verdict to manager
                    research:
                        manager asks dev to research
                        dev returns report to manager
        """)
        choice = p.elements[0]
        assert len(choice.branches) == 3

    def test_choice_branch_message_kinds(self):
        p = parse_intent_protocol("""
            protocol T:
                roles: a, b

                when a decides:
                    yes:
                        a asks b to do task
                        b returns result to a
                    no:
                        a sends shutdown to b
                        b sends ack to a
        """)
        choice = p.elements[0]
        assert choice.branches["yes"][0].message_kind == MessageKind.TASK_REQUEST
        assert choice.branches["no"][0].message_kind == MessageKind.SHUTDOWN_REQUEST


# ============================================================
# Comments and whitespace
# ============================================================


class TestCommentsAndWhitespace:
    """Test handling of comments and blank lines."""

    def test_comments_ignored(self):
        p = parse_intent_protocol("""
            # This is a comment
            protocol Test:
                roles: a, b

                # Another comment
                a asks b to do task
                b returns result to a
                # Final comment
        """)
        assert p.name == "Test"
        assert len(p.elements) == 2

    def test_blank_lines_between_steps(self):
        p = parse_intent_protocol("""
            protocol Test:
                roles: a, b

                a asks b to do task

                b returns result to a
        """)
        assert len(p.elements) == 2

    def test_leading_trailing_whitespace(self):
        p = parse_intent_protocol("""

            protocol Test:
                roles: a, b

                a asks b to do task
                b returns result to a

        """)
        assert p.name == "Test"


# ============================================================
# Integration with downstream modules
# ============================================================


class TestDownstreamIntegration:
    """Verify parsed protocols work with SessionChecker, Lean4, CodeGen."""

    def test_session_checker_accepts_parsed_protocol(self):
        from cervellaswarm_lingua_universale.checker import SessionChecker
        from cervellaswarm_lingua_universale.types import (
            TaskRequest,
            TaskResult,
            TaskStatus,
        )

        p = parse_intent_protocol("""
            protocol Test:
                roles: regina, worker

                regina asks worker to do task
                worker returns result to regina
        """)
        session = SessionChecker(p)
        session.send(
            "regina", "worker",
            TaskRequest(task_id="t1", description="test"),
        )
        session.send(
            "worker", "regina",
            TaskResult(task_id="t1", status=TaskStatus.OK, summary="ok"),
        )
        assert session.is_complete

    def test_lean4_generates_for_parsed_protocol(self):
        from cervellaswarm_lingua_universale.lean4_bridge import generate_lean4

        p = parse_intent_protocol("""
            protocol LeanTest:
                roles: a, b

                a asks b to do task
                b returns result to a
        """)
        code = generate_lean4(p)
        assert "LeanTest" in code
        assert len(code) > 100

    def test_codegen_generates_for_parsed_protocol(self):
        from cervellaswarm_lingua_universale.codegen import generate_python

        p = parse_intent_protocol("""
            protocol CodeGenTest:
                roles: a, b

                a asks b to do task
                b returns result to a
        """)
        code = generate_python(p)
        assert "CodeGenTest" in code
        assert len(code) > 100

    def test_dsl_render_of_parsed_protocol(self):
        from cervellaswarm_lingua_universale.dsl import render_protocol

        p = parse_intent_protocol("""
            protocol RenderTest:
                roles: a, b

                a asks b to verify
                b returns verdict to a
        """)
        dsl_text = render_protocol(p)
        assert "protocol RenderTest" in dsl_text
        assert "AuditRequest" in dsl_text
        assert "AuditVerdict" in dsl_text

    def test_full_roundtrip_intent_to_dsl(self):
        """Intent -> Protocol -> DSL -> Protocol (roundtrip via DSL)."""
        from cervellaswarm_lingua_universale.dsl import (
            parse_protocol,
            render_protocol,
        )

        p1 = parse_intent_protocol("""
            protocol Roundtrip:
                roles: x, y

                x asks y to do task
                y returns result to x
        """)
        dsl_text = render_protocol(p1)
        p2 = parse_protocol(dsl_text)

        assert p1.name == p2.name
        assert p1.roles == p2.roles
        assert len(p1.elements) == len(p2.elements)
        for e1, e2 in zip(p1.elements, p2.elements):
            assert isinstance(e1, ProtocolStep)
            assert isinstance(e2, ProtocolStep)
            assert e1.sender == e2.sender
            assert e1.receiver == e2.receiver
            assert e1.message_kind == e2.message_kind
