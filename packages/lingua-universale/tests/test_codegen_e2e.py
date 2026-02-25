# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""End-to-end tests for code generation: generate -> exec -> use.

These tests verify the generated code actually works at runtime:
- Sessions complete correctly
- Protocol violations are caught
- Role methods enforce type safety
- Branched protocols handle choice correctly
"""

import pytest

from cervellaswarm_lingua_universale.codegen import (
    PythonGenerator,
    generate_python,
    generate_python_multi,
)
from cervellaswarm_lingua_universale.protocols import (
    ArchitectFlow,
    DelegateTask,
    Protocol,
    ProtocolChoice,
    ProtocolStep,
    ResearchFlow,
    SimpleTask,
)
from cervellaswarm_lingua_universale.types import (
    AuditRequest,
    AuditVerdict,
    AuditVerdictType,
    MessageKind,
    PlanComplexity,
    PlanDecision,
    PlanProposal,
    PlanRequest,
    ResearchQuery,
    ResearchReport,
    TaskRequest,
    TaskResult,
    TaskStatus,
)


def _exec_generated(protocol: Protocol) -> dict:
    """Helper: generate code, exec it, return the namespace."""
    code = generate_python(protocol)
    ns: dict = {}
    exec(code, ns)
    return ns


# ============================================================
# DelegateTask E2E
# ============================================================


class TestDelegateTaskE2E:
    """End-to-end tests with DelegateTask protocol."""

    def test_complete_flow(self):
        ns = _exec_generated(DelegateTask)
        session = ns["ProtocolSession"](session_id="E2E-001")
        assert not session.is_complete

        session.regina.send_task_request(
            TaskRequest(task_id="T1", description="test")
        )
        session.worker.send_task_result(
            TaskResult(task_id="T1", status=TaskStatus.OK, summary="done")
        )
        session.regina.send_audit_request(
            AuditRequest(audit_id="A1", target="test")
        )
        session.guardiana.send_audit_verdict(
            AuditVerdict(
                audit_id="A1",
                verdict=AuditVerdictType.APPROVED,
                score=9.5,
                checked=("code",),
            )
        )
        assert session.is_complete

    def test_wrong_sender_raises(self):
        ns = _exec_generated(DelegateTask)
        session = ns["ProtocolSession"](session_id="E2E-002")

        # Worker tries to send first (should be regina)
        with pytest.raises(Exception, match="sender"):
            session.worker.send_task_result(
                TaskResult(task_id="T1", status=TaskStatus.OK, summary="done")
            )

    def test_session_id_propagated(self):
        ns = _exec_generated(DelegateTask)
        session = ns["ProtocolSession"](session_id="MY-SESSION")
        assert session.session_id == "MY-SESSION"

    def test_checker_accessible(self):
        ns = _exec_generated(DelegateTask)
        session = ns["ProtocolSession"](session_id="E2E-003")
        assert session.checker is not None
        assert session.checker.protocol_name == "DelegateTask"

    def test_role_bindings(self):
        ns = _exec_generated(DelegateTask)
        session = ns["ProtocolSession"](
            session_id="E2E-004",
            role_bindings={
                "worker": "cervella-backend",
                "guardiana": "cervella-guardiana-qualita",
            },
        )
        # Use bound names
        session.send("regina", "cervella-backend",
            TaskRequest(task_id="T1", description="test"))
        session.send("cervella-backend", "regina",
            TaskResult(task_id="T1", status=TaskStatus.OK, summary="done"))
        session.send("regina", "cervella-guardiana-qualita",
            AuditRequest(audit_id="A1", target="test"))
        session.send("cervella-guardiana-qualita", "regina",
            AuditVerdict(
                audit_id="A1", verdict=AuditVerdictType.APPROVED,
                score=9.5, checked=("code",),
            ))
        assert session.is_complete


# ============================================================
# SimpleTask E2E
# ============================================================


class TestSimpleTaskE2E:
    """End-to-end tests with SimpleTask protocol."""

    def test_complete_flow(self):
        ns = _exec_generated(SimpleTask)
        session = ns["ProtocolSession"](session_id="ST-001")

        session.regina.send_task_request(
            TaskRequest(task_id="T1", description="quick fix")
        )
        session.worker.send_task_result(
            TaskResult(task_id="T1", status=TaskStatus.OK, summary="fixed")
        )
        assert session.is_complete

    def test_no_guardiana_role(self):
        ns = _exec_generated(SimpleTask)
        session = ns["ProtocolSession"](session_id="ST-002")
        assert not hasattr(session, "guardiana")

    def test_send_after_complete_raises(self):
        ns = _exec_generated(SimpleTask)
        session = ns["ProtocolSession"](session_id="ST-003")

        session.regina.send_task_request(
            TaskRequest(task_id="T1", description="test")
        )
        session.worker.send_task_result(
            TaskResult(task_id="T1", status=TaskStatus.OK, summary="done")
        )
        assert session.is_complete

        with pytest.raises(Exception, match="complete"):
            session.regina.send_task_request(
                TaskRequest(task_id="T2", description="extra")
            )


# ============================================================
# ResearchFlow E2E
# ============================================================


class TestResearchFlowE2E:
    """End-to-end tests with ResearchFlow protocol."""

    def test_complete_flow(self):
        ns = _exec_generated(ResearchFlow)
        session = ns["ProtocolSession"](session_id="RF-001")

        session.regina.send_research_query(
            ResearchQuery(query_id="Q1", topic="AI safety")
        )
        session.researcher.send_research_report(
            ResearchReport(
                query_id="Q1", topic="AI safety", sources_consulted=10
            )
        )
        session.regina.send_audit_request(
            AuditRequest(audit_id="A1", target="research")
        )
        session.guardiana.send_audit_verdict(
            AuditVerdict(
                audit_id="A1",
                verdict=AuditVerdictType.APPROVED,
                score=9.0,
                checked=("sources",),
            )
        )
        assert session.is_complete

    def test_has_researcher_role(self):
        ns = _exec_generated(ResearchFlow)
        session = ns["ProtocolSession"](session_id="RF-002")
        assert hasattr(session, "researcher")


# ============================================================
# ArchitectFlow E2E (branched protocol)
# ============================================================


class TestArchitectFlowE2E:
    """End-to-end tests with ArchitectFlow (branched protocol)."""

    def test_approve_branch_complete(self):
        ns = _exec_generated(ArchitectFlow)
        session = ns["ProtocolSession"](session_id="AF-001")

        # Flat steps before choice
        session.regina.send_plan_request(
            PlanRequest(plan_id="P1", task_description="migrate DB")
        )
        session.architect.send_plan_proposal(
            PlanProposal(
                plan_id="P1", complexity=PlanComplexity.HIGH,
                risk_score=0.5, files_affected=10,
            )
        )

        # Choose approve branch
        session.choose_branch("approve")
        session.regina.send_plan_decision(
            PlanDecision(plan_id="P1", approved=True)
        )
        session.regina.send_task_request(
            TaskRequest(task_id="T1", description="implement migration")
        )
        session.worker.send_task_result(
            TaskResult(task_id="T1", status=TaskStatus.OK, summary="done")
        )
        session.regina.send_audit_request(
            AuditRequest(audit_id="A1", target="migration")
        )
        session.guardiana.send_audit_verdict(
            AuditVerdict(
                audit_id="A1", verdict=AuditVerdictType.APPROVED,
                score=9.5, checked=("code", "tests"),
            )
        )
        assert session.is_complete

    def test_reject_branch_complete(self):
        ns = _exec_generated(ArchitectFlow)
        session = ns["ProtocolSession"](session_id="AF-002")

        session.regina.send_plan_request(
            PlanRequest(plan_id="P1", task_description="migrate DB")
        )
        session.architect.send_plan_proposal(
            PlanProposal(
                plan_id="P1", complexity=PlanComplexity.HIGH,
                risk_score=0.8, files_affected=20,
            )
        )

        # Choose reject branch
        session.choose_branch("reject")
        session.regina.send_plan_decision(
            PlanDecision(plan_id="P1", approved=False, feedback="too risky")
        )
        session.architect.send_plan_proposal(
            PlanProposal(
                plan_id="P1", complexity=PlanComplexity.MEDIUM,
                risk_score=0.3, files_affected=5,
            )
        )
        assert session.is_complete

    def test_has_choose_branch_method(self):
        ns = _exec_generated(ArchitectFlow)
        session = ns["ProtocolSession"](session_id="AF-003")
        assert hasattr(session, "choose_branch")

    def test_has_architect_role(self):
        ns = _exec_generated(ArchitectFlow)
        session = ns["ProtocolSession"](session_id="AF-004")
        assert hasattr(session, "architect")


# ============================================================
# Custom protocol E2E
# ============================================================


class TestCustomProtocolE2E:
    """Tests with custom-defined protocols."""

    def test_minimal_protocol(self):
        """Two roles, one step."""
        proto = Protocol(
            name="MinimalProto",
            roles=("sender", "receiver"),
            elements=(
                ProtocolStep(
                    sender="sender",
                    receiver="receiver",
                    message_kind=MessageKind.DM,
                ),
            ),
        )
        code = generate_python(proto)
        compile(code, "MinimalProto.py", "exec")
        ns: dict = {}
        exec(code, ns)
        session = ns["ProtocolSession"](session_id="CUSTOM-001")
        assert hasattr(session, "sender")
        assert hasattr(session, "receiver")

    def test_protocol_with_description(self):
        proto = Protocol(
            name="DescProto",
            roles=("a", "b"),
            description='A protocol with "special" characters',
            elements=(
                ProtocolStep(
                    sender="a", receiver="b",
                    message_kind=MessageKind.DM,
                    description='Step with "quotes"',
                ),
            ),
        )
        code = generate_python(proto)
        compile(code, "DescProto.py", "exec")


# ============================================================
# generate_python_multi
# ============================================================


class TestGeneratePythonMulti:
    """Tests for multi-protocol generation."""

    def test_empty_raises(self):
        with pytest.raises(ValueError, match="cannot be empty"):
            generate_python_multi([])

    def test_duplicate_names_raises(self):
        with pytest.raises(ValueError, match="duplicate protocol names"):
            generate_python_multi([DelegateTask, DelegateTask])

    def test_two_protocols_compile(self):
        code = generate_python_multi([DelegateTask, SimpleTask])
        compile(code, "multi.py", "exec")

    def test_two_protocols_have_separate_sessions(self):
        code = generate_python_multi([DelegateTask, SimpleTask])
        ns: dict = {}
        exec(code, ns)
        assert "DelegateTaskSession" in ns
        assert "SimpleTaskSession" in ns

    def test_all_four_protocols(self):
        code = generate_python_multi(
            [DelegateTask, SimpleTask, ResearchFlow, ArchitectFlow]
        )
        compile(code, "all_four.py", "exec")
        ns: dict = {}
        exec(code, ns)
        assert "DelegateTaskSession" in ns
        assert "SimpleTaskSession" in ns
        assert "ResearchFlowSession" in ns
        assert "ArchitectFlowSession" in ns

    def test_multi_session_works_e2e(self):
        code = generate_python_multi([SimpleTask])
        ns: dict = {}
        exec(code, ns)
        session = ns["SimpleTaskSession"](session_id="MULTI-001")
        session.send("regina", "worker",
            TaskRequest(task_id="T1", description="test"))
        session.send("worker", "regina",
            TaskResult(task_id="T1", status=TaskStatus.OK, summary="done"))
        assert session.is_complete

    def test_multi_contains_shared_imports(self):
        code = generate_python_multi([DelegateTask, SimpleTask])
        # Should only have one import block, not duplicated
        assert code.count("from cervellaswarm_lingua_universale.checker import") == 1


# ============================================================
# Edge cases and regressions
# ============================================================


class TestCodegenEdgeCases:
    """Edge cases and potential regression tests."""

    def test_generated_code_has_no_syntax_errors(self):
        """All 4 standard protocols must compile."""
        for proto in [DelegateTask, ArchitectFlow, ResearchFlow, SimpleTask]:
            code = generate_python(proto)
            compile(code, f"{proto.name}.py", "exec")

    def test_generated_code_exec_no_exceptions(self):
        """All 4 standard protocols must exec without errors."""
        for proto in [DelegateTask, ArchitectFlow, ResearchFlow, SimpleTask]:
            code = generate_python(proto)
            ns: dict = {}
            exec(code, ns)  # Should not raise
            assert "ProtocolSession" in ns

    def test_all_roles_have_methods_or_receive_note(self):
        """Every role class should have send methods or a receive note."""
        gen = PythonGenerator()
        code = gen.generate_role_classes(DelegateTask)
        # Guardiana only receives from regina in DelegateTask,
        # but also sends audit_verdict back
        assert "send_audit_verdict" in code

    def test_convenience_function_matches_generator(self):
        """generate_python() should produce same structure as PythonGenerator."""
        gen = PythonGenerator()
        code_gen = gen.generate(DelegateTask)
        code_conv = generate_python(DelegateTask)
        # Both should compile
        compile(code_gen, "gen.py", "exec")
        compile(code_conv, "conv.py", "exec")
        # Both should have ProtocolSession
        ns1: dict = {}
        ns2: dict = {}
        exec(code_gen, ns1)
        exec(code_conv, ns2)
        assert "ProtocolSession" in ns1
        assert "ProtocolSession" in ns2
