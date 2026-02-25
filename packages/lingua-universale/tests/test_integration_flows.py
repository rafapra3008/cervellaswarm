# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""End-to-end flow tests for integration.py.

Tests real agent name bindings through complete protocol sessions.
Coverage target: 100% integration.py (complementary to test_integration_core.py)
"""

import pytest

from cervellaswarm_lingua_universale import (
    AgentRole,
    AuditRequest,
    AuditVerdict,
    AuditVerdictType,
    BranchChosen,
    EventCollector,
    MessageSent,
    PlanDecision,
    PlanProposal,
    PlanComplexity,
    PlanRequest,
    ProtocolMonitor,
    ProtocolViolation,
    ResearchQuery,
    ResearchReport,
    SessionEnded,
    SessionStarted,
    TaskRequest,
    TaskResult,
    TaskStatus,
    ViolationOccurred,
)
from cervellaswarm_lingua_universale.integration import (
    AGENT_CATALOG,
    agent_by_name,
    agents_for_protocol,
    create_session,
    resolve_bindings,
    validate_swarm,
)
from cervellaswarm_lingua_universale.protocols import (
    ArchitectFlow,
    DelegateTask,
    ResearchFlow,
    SimpleTask,
)


# ============================================================
# Shared message factories
# ============================================================

def task_req(task_id="T001"):
    return TaskRequest(
        task_id=task_id,
        description="Build feature Y",
        target_files=("src/y.py",),
        constraints=("ZERO deps",),
    )


def task_res(task_id="T001"):
    return TaskResult(
        task_id=task_id,
        status=TaskStatus.OK,
        summary="Feature Y done in 100 lines",
        files_created=("src/y.py",),
        test_command="pytest tests/test_y.py",
    )


def audit_req(audit_id="A001"):
    return AuditRequest(
        audit_id=audit_id,
        target="src/y.py",
        checklist=("Tests present", "No secrets"),
        worker_output="Feature Y with 5 tests.",
    )


def audit_ver(audit_id="A001"):
    return AuditVerdict(
        audit_id=audit_id,
        verdict=AuditVerdictType.APPROVED,
        score=9.5,
        checked=("Tests present",),
    )


def plan_req(plan_id="P001"):
    return PlanRequest(
        plan_id=plan_id,
        task_description="Migrate PostgreSQL",
        complexity_hint=PlanComplexity.HIGH,
    )


def plan_prop(plan_id="P001"):
    return PlanProposal(
        plan_id=plan_id,
        complexity=PlanComplexity.HIGH,
        risk_score=0.5,
        files_affected=5,
        phases=("Phase 1",),
        steps=("Step 1",),
        success_criteria=("All tests pass",),
    )


def plan_dec_approve(plan_id="P001"):
    return PlanDecision(plan_id=plan_id, approved=True)


def plan_dec_reject(plan_id="P001"):
    return PlanDecision(
        plan_id=plan_id, approved=False, feedback="Risk too high"
    )


def research_q(query_id="Q001"):
    return ResearchQuery(
        query_id=query_id,
        topic="Python concurrency 2026",
        min_sources=5,
    )


def research_rep(query_id="Q001"):
    return ResearchReport(
        query_id=query_id,
        topic="Python concurrency 2026",
        sources_consulted=10,
        key_findings=("asyncio wins for IO",),
    )


# ============================================================
# 1. Complete DelegateTask flow with real agent names
# ============================================================

class TestDelegateTaskCompleteFlow:
    def test_full_delegate_task_with_backend(self):
        """DelegateTask: orchestrator -> backend -> orchestrator -> guardiana-qualita."""
        checker = create_session(
            DelegateTask,
            session_id="DT-BACKEND-001",
            bindings={
                "worker": "cervella-backend",
                "guardiana": "cervella-guardiana-qualita",
            },
        )
        checker.send("cervella-orchestrator", "cervella-backend", task_req())
        checker.send("cervella-backend", "cervella-orchestrator", task_res())
        checker.send("cervella-orchestrator", "cervella-guardiana-qualita", audit_req())
        checker.send("cervella-guardiana-qualita", "cervella-orchestrator", audit_ver())
        assert checker.is_complete

    def test_full_delegate_task_with_frontend(self):
        checker = create_session(
            DelegateTask,
            session_id="DT-FRONTEND-001",
            bindings={
                "worker": "cervella-frontend",
                "guardiana": "cervella-guardiana-ricerca",
            },
        )
        checker.send("cervella-orchestrator", "cervella-frontend", task_req())
        checker.send("cervella-frontend", "cervella-orchestrator", task_res())
        checker.send("cervella-orchestrator", "cervella-guardiana-ricerca", audit_req())
        checker.send("cervella-guardiana-ricerca", "cervella-orchestrator", audit_ver())
        assert checker.is_complete

    def test_delegate_task_session_id_set_correctly(self):
        checker = create_session(
            DelegateTask,
            session_id="MY-SESSION",
            bindings={"worker": "cervella-tester",
                      "guardiana": "cervella-guardiana-qualita"},
        )
        assert checker.session_id == "MY-SESSION"

    def test_delegate_task_log_has_four_messages(self):
        checker = create_session(
            DelegateTask,
            bindings={"worker": "cervella-devops",
                      "guardiana": "cervella-guardiana-ops"},
        )
        checker.send("cervella-orchestrator", "cervella-devops", task_req())
        checker.send("cervella-devops", "cervella-orchestrator", task_res())
        checker.send("cervella-orchestrator", "cervella-guardiana-ops", audit_req())
        checker.send("cervella-guardiana-ops", "cervella-orchestrator", audit_ver())
        assert len(checker.log) == 4


# ============================================================
# 2. Complete ResearchFlow with cervella-researcher
# ============================================================

class TestResearchFlowCompleteFlow:
    def test_research_flow_with_researcher(self):
        """ResearchFlow: orchestrator -> researcher -> orchestrator -> guardiana."""
        checker = create_session(
            ResearchFlow,
            session_id="RF-001",
            bindings={
                "researcher": "cervella-researcher",
                "guardiana": "cervella-guardiana-ricerca",
            },
        )
        checker.send("cervella-orchestrator", "cervella-researcher", research_q())
        checker.send("cervella-researcher", "cervella-orchestrator", research_rep())
        checker.send("cervella-orchestrator", "cervella-guardiana-ricerca", audit_req())
        checker.send("cervella-guardiana-ricerca", "cervella-orchestrator", audit_ver())
        assert checker.is_complete

    def test_research_flow_with_scienziata_as_researcher(self):
        """Scienziata can also play the researcher role."""
        checker = create_session(
            ResearchFlow,
            session_id="RF-SCIENZIATA-001",
            bindings={
                "researcher": "cervella-scienziata",
                "guardiana": "cervella-guardiana-ricerca",
            },
        )
        checker.send("cervella-orchestrator", "cervella-scienziata", research_q())
        checker.send("cervella-scienziata", "cervella-orchestrator", research_rep())
        checker.send("cervella-orchestrator", "cervella-guardiana-ricerca", audit_req())
        checker.send("cervella-guardiana-ricerca", "cervella-orchestrator", audit_ver())
        assert checker.is_complete

    def test_research_flow_log_has_four_messages(self):
        checker = create_session(
            ResearchFlow,
            bindings={
                "researcher": "cervella-researcher",
                "guardiana": "cervella-guardiana-qualita",
            },
        )
        checker.send("cervella-orchestrator", "cervella-researcher", research_q())
        checker.send("cervella-researcher", "cervella-orchestrator", research_rep())
        checker.send("cervella-orchestrator", "cervella-guardiana-qualita", audit_req())
        checker.send("cervella-guardiana-qualita", "cervella-orchestrator", audit_ver())
        assert len(checker.log) == 4


# ============================================================
# 3. Complete ArchitectFlow (approve branch) with real names
# ============================================================

class TestArchitectFlowApprove:
    def test_architect_flow_approve_branch_complete(self):
        """ArchitectFlow approve branch: full sequence with real names.

        Both branches start with PLAN_DECISION (ambiguous), so we call
        choose_branch() explicitly before sending the first branch message.
        """
        checker = create_session(
            ArchitectFlow,
            session_id="AF-APPROVE-001",
            bindings={
                "architect": "cervella-architect",
                "worker": "cervella-backend",
                "guardiana": "cervella-guardiana-qualita",
            },
        )
        # Plan phase
        checker.send("cervella-orchestrator", "cervella-architect", plan_req())
        checker.send("cervella-architect", "cervella-orchestrator", plan_prop())
        # Both branches start with PLAN_DECISION - explicit choice needed
        checker.choose_branch("approve")
        checker.send("cervella-orchestrator", "cervella-architect", plan_dec_approve())
        checker.send("cervella-orchestrator", "cervella-backend", task_req())
        checker.send("cervella-backend", "cervella-orchestrator", task_res())
        checker.send("cervella-orchestrator", "cervella-guardiana-qualita", audit_req())
        checker.send("cervella-guardiana-qualita", "cervella-orchestrator", audit_ver())
        assert checker.is_complete

    def test_architect_flow_reject_branch_complete(self):
        """ArchitectFlow reject branch ends after plan revision.

        Both branches start with PLAN_DECISION (ambiguous), so we call
        choose_branch() explicitly.
        """
        checker = create_session(
            ArchitectFlow,
            session_id="AF-REJECT-001",
            bindings={
                "architect": "cervella-architect",
                "worker": "cervella-frontend",
                "guardiana": "cervella-guardiana-ops",
            },
        )
        checker.send("cervella-orchestrator", "cervella-architect", plan_req())
        checker.send("cervella-architect", "cervella-orchestrator", plan_prop())
        # Reject branch: explicit choice required (ambiguous first step)
        checker.choose_branch("reject")
        checker.send("cervella-orchestrator", "cervella-architect", plan_dec_reject())
        checker.send("cervella-architect", "cervella-orchestrator", plan_prop())
        assert checker.is_complete

    def test_architect_flow_current_branch_after_choice(self):
        """After choosing approve branch, current_branch is 'approve'."""
        checker = create_session(
            ArchitectFlow,
            session_id="AF-BRANCH-001",
            bindings={
                "architect": "cervella-architect",
                "worker": "cervella-backend",
                "guardiana": "cervella-guardiana-qualita",
            },
        )
        checker.send("cervella-orchestrator", "cervella-architect", plan_req())
        checker.send("cervella-architect", "cervella-orchestrator", plan_prop())
        checker.choose_branch("approve")
        assert checker.current_branch == "approve"


# ============================================================
# 4. Complete SimpleTask with various workers
# ============================================================

class TestSimpleTaskCompleteFlow:
    def test_simple_task_with_backend(self):
        checker = create_session(
            SimpleTask,
            session_id="ST-BACKEND-001",
            bindings={"worker": "cervella-backend"},
        )
        checker.send("cervella-orchestrator", "cervella-backend", task_req())
        checker.send("cervella-backend", "cervella-orchestrator", task_res())
        assert checker.is_complete

    def test_simple_task_with_docs(self):
        checker = create_session(
            SimpleTask,
            bindings={"worker": "cervella-docs"},
        )
        checker.send("cervella-orchestrator", "cervella-docs", task_req())
        checker.send("cervella-docs", "cervella-orchestrator", task_res())
        assert checker.is_complete

    def test_simple_task_with_data(self):
        checker = create_session(
            SimpleTask,
            bindings={"worker": "cervella-data"},
        )
        checker.send("cervella-orchestrator", "cervella-data", task_req())
        checker.send("cervella-data", "cervella-orchestrator", task_res())
        assert checker.is_complete

    def test_simple_task_log_has_two_messages(self):
        checker = create_session(
            SimpleTask,
            bindings={"worker": "cervella-backend"},
        )
        checker.send("cervella-orchestrator", "cervella-backend", task_req())
        checker.send("cervella-backend", "cervella-orchestrator", task_res())
        assert len(checker.log) == 2


# ============================================================
# 5. All 13 workers can complete a SimpleTask
# ============================================================

WORKER_AGENTS = [
    "cervella-architect",
    "cervella-security",
    "cervella-ingegnera",
    "cervella-backend",
    "cervella-frontend",
    "cervella-tester",
    "cervella-reviewer",
    "cervella-researcher",
    "cervella-marketing",
    "cervella-devops",
    "cervella-docs",
    "cervella-data",
    "cervella-scienziata",
]


class TestAllWorkersSimpleTask:
    @pytest.mark.parametrize("worker_name", WORKER_AGENTS)
    def test_worker_completes_simple_task(self, worker_name):
        """Every worker-capable agent can complete a SimpleTask."""
        checker = create_session(
            SimpleTask,
            session_id=f"ST-{worker_name}",
            bindings={"worker": worker_name},
        )
        checker.send("cervella-orchestrator", worker_name, task_req())
        checker.send(worker_name, "cervella-orchestrator", task_res())
        assert checker.is_complete

    def test_all_13_workers_covered(self):
        """Exactly 13 agents can play 'worker' in SimpleTask."""
        coverage = agents_for_protocol(SimpleTask)
        worker_names = {a.agent_name for a in coverage["worker"]}
        assert worker_names == set(WORKER_AGENTS)


# ============================================================
# 6. All 3 guardiane can complete a DelegateTask audit
# ============================================================

GUARDIANA_AGENTS = [
    "cervella-guardiana-qualita",
    "cervella-guardiana-ricerca",
    "cervella-guardiana-ops",
]


class TestAllGuardianeAuditFlow:
    @pytest.mark.parametrize("guardiana_name", GUARDIANA_AGENTS)
    def test_guardiana_completes_delegate_task(self, guardiana_name):
        """Every guardiana can audit in a DelegateTask."""
        checker = create_session(
            DelegateTask,
            session_id=f"DT-{guardiana_name}",
            bindings={
                "worker": "cervella-backend",
                "guardiana": guardiana_name,
            },
        )
        checker.send("cervella-orchestrator", "cervella-backend", task_req())
        checker.send("cervella-backend", "cervella-orchestrator", task_res())
        checker.send("cervella-orchestrator", guardiana_name, audit_req())
        checker.send(guardiana_name, "cervella-orchestrator", audit_ver())
        assert checker.is_complete

    def test_all_3_guardiane_in_catalog(self):
        coverage = agents_for_protocol(DelegateTask)
        guardiana_names = {a.agent_name for a in coverage["guardiana"]}
        assert guardiana_names == set(GUARDIANA_AGENTS)


# ============================================================
# 7. Protocol violation with wrong agent
# ============================================================

class TestProtocolViolationWithRealNames:
    def test_wrong_sender_raises_violation(self):
        """Sending from wrong agent raises ProtocolViolation."""
        checker = create_session(
            SimpleTask,
            bindings={"worker": "cervella-backend"},
        )
        # First message should be from orchestrator, not backend
        with pytest.raises(ProtocolViolation):
            checker.send("cervella-backend", "cervella-orchestrator", task_req())

    def test_wrong_receiver_raises_violation(self):
        """Sending to wrong agent raises ProtocolViolation."""
        checker = create_session(
            SimpleTask,
            bindings={"worker": "cervella-backend"},
        )
        # Should be orchestrator -> backend, not orchestrator -> frontend
        with pytest.raises(ProtocolViolation):
            checker.send("cervella-orchestrator", "cervella-frontend", task_req())

    def test_wrong_message_kind_raises_violation(self):
        """Sending wrong message kind raises ProtocolViolation."""
        checker = create_session(
            SimpleTask,
            bindings={"worker": "cervella-backend"},
        )
        # First step expects TaskRequest, not TaskResult
        with pytest.raises(ProtocolViolation):
            checker.send("cervella-orchestrator", "cervella-backend", task_res())

    def test_unbound_agent_used_as_sender_raises_violation(self):
        """Using an unbound agent name as sender causes a violation."""
        checker = create_session(
            SimpleTask,
            bindings={"worker": "cervella-backend"},
        )
        # cervella-frontend is not bound to any role - resolves to itself
        # which is not "regina", so violation
        with pytest.raises(ProtocolViolation):
            checker.send("cervella-frontend", "cervella-backend", task_req())


# ============================================================
# 8. Monitor integration - create_session with monitor
# ============================================================

class TestMonitorIntegrationWithRealNames:
    def test_session_started_event_emitted(self):
        monitor = ProtocolMonitor()
        collector = EventCollector()
        monitor.add_listener(collector)

        create_session(SimpleTask, monitor=monitor, session_id="MONITOR-001")

        started = collector.of_type(SessionStarted)
        assert len(started) == 1
        assert started[0].session_id == "MONITOR-001"

    def test_message_sent_event_uses_real_agent_name_as_sender(self):
        """MessageSent events carry real agent names, not protocol roles."""
        monitor = ProtocolMonitor()
        collector = EventCollector()
        monitor.add_listener(collector)

        checker = create_session(
            SimpleTask,
            monitor=monitor,
            session_id="MONITOR-002",
            bindings={"worker": "cervella-backend"},
        )
        checker.send("cervella-orchestrator", "cervella-backend", task_req())

        messages = collector.of_type(MessageSent)
        assert len(messages) == 1
        assert messages[0].sender == "cervella-orchestrator"
        assert messages[0].receiver == "cervella-backend"

    def test_session_ended_event_emitted_after_complete(self):
        monitor = ProtocolMonitor()
        collector = EventCollector()
        monitor.add_listener(collector)

        checker = create_session(
            SimpleTask,
            monitor=monitor,
            bindings={"worker": "cervella-backend"},
        )
        checker.send("cervella-orchestrator", "cervella-backend", task_req())
        checker.send("cervella-backend", "cervella-orchestrator", task_res())

        ended = collector.of_type(SessionEnded)
        assert len(ended) == 1
        assert ended[0].total_messages == 2

    def test_violation_event_emitted_on_protocol_violation(self):
        monitor = ProtocolMonitor()
        collector = EventCollector()
        monitor.add_listener(collector)

        checker = create_session(
            SimpleTask,
            monitor=monitor,
            bindings={"worker": "cervella-backend"},
        )
        with pytest.raises(ProtocolViolation):
            checker.send("cervella-backend", "cervella-orchestrator", task_req())

        violations = collector.of_type(ViolationOccurred)
        assert len(violations) == 1

    def test_branch_chosen_event_emitted_in_architect_flow(self):
        monitor = ProtocolMonitor()
        collector = EventCollector()
        monitor.add_listener(collector)

        checker = create_session(
            ArchitectFlow,
            monitor=monitor,
            bindings={
                "architect": "cervella-architect",
                "worker": "cervella-backend",
                "guardiana": "cervella-guardiana-qualita",
            },
        )
        checker.send("cervella-orchestrator", "cervella-architect", plan_req())
        checker.send("cervella-architect", "cervella-orchestrator", plan_prop())
        # Both branches ambiguous (both start PLAN_DECISION) - explicit choice
        checker.choose_branch("approve")
        checker.send("cervella-orchestrator", "cervella-architect", plan_dec_approve())

        branches = collector.of_type(BranchChosen)
        assert len(branches) == 1
        assert branches[0].branch_name == "approve"

    def test_monitor_collects_all_events_in_delegate_task(self):
        monitor = ProtocolMonitor()
        collector = EventCollector()
        monitor.add_listener(collector)

        checker = create_session(
            DelegateTask,
            monitor=monitor,
            bindings={
                "worker": "cervella-tester",
                "guardiana": "cervella-guardiana-qualita",
            },
        )
        checker.send("cervella-orchestrator", "cervella-tester", task_req())
        checker.send("cervella-tester", "cervella-orchestrator", task_res())
        checker.send("cervella-orchestrator", "cervella-guardiana-qualita", audit_req())
        checker.send("cervella-guardiana-qualita", "cervella-orchestrator", audit_ver())

        # SessionStarted + 4 MessageSent + SessionEnded = 6 events
        assert len(collector.events) == 6


# ============================================================
# 9. Multi-session - different agent bindings
# ============================================================

class TestMultiSession:
    def test_two_concurrent_sessions_different_workers(self):
        """Two sessions with different workers are independent."""
        checker1 = create_session(
            SimpleTask,
            session_id="S1",
            bindings={"worker": "cervella-backend"},
        )
        checker2 = create_session(
            SimpleTask,
            session_id="S2",
            bindings={"worker": "cervella-frontend"},
        )

        checker1.send("cervella-orchestrator", "cervella-backend", task_req("T1"))
        checker2.send("cervella-orchestrator", "cervella-frontend", task_req("T2"))
        checker1.send("cervella-backend", "cervella-orchestrator", task_res("T1"))
        checker2.send("cervella-frontend", "cervella-orchestrator", task_res("T2"))

        assert checker1.is_complete
        assert checker2.is_complete

    def test_sessions_have_different_session_ids(self):
        c1 = create_session(SimpleTask)
        c2 = create_session(SimpleTask)
        assert c1.session_id != c2.session_id

    def test_sessions_do_not_share_log(self):
        c1 = create_session(
            SimpleTask, session_id="SL1",
            bindings={"worker": "cervella-backend"},
        )
        c2 = create_session(
            SimpleTask, session_id="SL2",
            bindings={"worker": "cervella-frontend"},
        )
        c1.send("cervella-orchestrator", "cervella-backend", task_req())
        assert len(c1.log) == 1
        assert len(c2.log) == 0

    def test_three_sessions_with_three_guardiane(self):
        """Each guardiana can run its own DelegateTask session."""
        results = []
        for guardiana_name in GUARDIANA_AGENTS:
            checker = create_session(
                DelegateTask,
                bindings={
                    "worker": "cervella-backend",
                    "guardiana": guardiana_name,
                },
            )
            checker.send("cervella-orchestrator", "cervella-backend", task_req())
            checker.send("cervella-backend", "cervella-orchestrator", task_res())
            checker.send("cervella-orchestrator", guardiana_name, audit_req())
            checker.send(guardiana_name, "cervella-orchestrator", audit_ver())
            results.append(checker.is_complete)

        assert all(results)


# ============================================================
# 10. Scienziata as researcher
# ============================================================

class TestScienziataAsResearcher:
    def test_scienziata_completes_research_flow(self):
        checker = create_session(
            ResearchFlow,
            session_id="RF-SCI-001",
            bindings={
                "researcher": "cervella-scienziata",
                "guardiana": "cervella-guardiana-ricerca",
            },
        )
        checker.send("cervella-orchestrator", "cervella-scienziata", research_q())
        checker.send("cervella-scienziata", "cervella-orchestrator", research_rep())
        checker.send("cervella-orchestrator", "cervella-guardiana-ricerca", audit_req())
        checker.send("cervella-guardiana-ricerca", "cervella-orchestrator", audit_ver())
        assert checker.is_complete

    def test_scienziata_can_also_do_simple_task_as_worker(self):
        """Scienziata has protocol_roles ('researcher', 'worker')."""
        checker = create_session(
            SimpleTask,
            bindings={"worker": "cervella-scienziata"},
        )
        checker.send("cervella-orchestrator", "cervella-scienziata", task_req())
        checker.send("cervella-scienziata", "cervella-orchestrator", task_res())
        assert checker.is_complete


# ============================================================
# 11. Architect as worker in DelegateTask
# ============================================================

class TestArchitectAsWorker:
    def test_architect_can_play_worker_in_delegate_task(self):
        """Architect has protocol_roles ('architect', 'worker')."""
        checker = create_session(
            DelegateTask,
            session_id="DT-ARCH-AS-WORKER",
            bindings={
                "worker": "cervella-architect",
                "guardiana": "cervella-guardiana-qualita",
            },
        )
        checker.send("cervella-orchestrator", "cervella-architect", task_req())
        checker.send("cervella-architect", "cervella-orchestrator", task_res())
        checker.send("cervella-orchestrator", "cervella-guardiana-qualita", audit_req())
        checker.send("cervella-guardiana-qualita", "cervella-orchestrator", audit_ver())
        assert checker.is_complete

    def test_architect_can_play_architect_in_architect_flow(self):
        """Architect plays the 'architect' role in ArchitectFlow."""
        checker = create_session(
            ArchitectFlow,
            session_id="AF-ARCH-001",
            bindings={
                "architect": "cervella-architect",
                "worker": "cervella-backend",
                "guardiana": "cervella-guardiana-qualita",
            },
        )
        checker.send("cervella-orchestrator", "cervella-architect", plan_req())
        checker.send("cervella-architect", "cervella-orchestrator", plan_prop())
        # Ambiguous branch (both start PLAN_DECISION) - explicit choice required
        checker.choose_branch("approve")
        checker.send("cervella-orchestrator", "cervella-architect", plan_dec_approve())
        checker.send("cervella-orchestrator", "cervella-backend", task_req())
        checker.send("cervella-backend", "cervella-orchestrator", task_res())
        checker.send("cervella-orchestrator", "cervella-guardiana-qualita", audit_req())
        checker.send("cervella-guardiana-qualita", "cervella-orchestrator", audit_ver())
        assert checker.is_complete


# ============================================================
# 12. resolve_bindings + create_session round-trip
# ============================================================

class TestResolveBindingsCreateSession:
    def test_resolve_then_create_simple_task(self):
        """resolve_bindings output can be used directly in create_session."""
        bindings = resolve_bindings(SimpleTask)
        checker = create_session(SimpleTask, bindings=bindings)
        # Get the worker name from bindings to use in send()
        worker_name = bindings["worker"]
        checker.send("cervella-orchestrator", worker_name, task_req())
        checker.send(worker_name, "cervella-orchestrator", task_res())
        assert checker.is_complete

    def test_resolve_then_create_delegate_task(self):
        bindings = resolve_bindings(
            DelegateTask,
            preferences={
                "worker": "cervella-backend",
                "guardiana": "cervella-guardiana-qualita",
            },
        )
        checker = create_session(DelegateTask, bindings=bindings)
        checker.send("cervella-orchestrator", "cervella-backend", task_req())
        checker.send("cervella-backend", "cervella-orchestrator", task_res())
        checker.send("cervella-orchestrator", "cervella-guardiana-qualita", audit_req())
        checker.send("cervella-guardiana-qualita", "cervella-orchestrator", audit_ver())
        assert checker.is_complete

    def test_resolve_then_create_research_flow(self):
        bindings = resolve_bindings(
            ResearchFlow,
            preferences={"researcher": "cervella-researcher"},
        )
        checker = create_session(ResearchFlow, bindings=bindings)
        researcher_name = bindings["researcher"]
        guardiana_name = bindings["guardiana"]
        checker.send("cervella-orchestrator", researcher_name, research_q())
        checker.send(researcher_name, "cervella-orchestrator", research_rep())
        checker.send("cervella-orchestrator", guardiana_name, audit_req())
        checker.send(guardiana_name, "cervella-orchestrator", audit_ver())
        assert checker.is_complete


# ============================================================
# 13. validate_swarm end-to-end scenarios
# ============================================================

class TestValidateSwarmEndToEnd:
    def test_full_swarm_is_valid(self):
        result = validate_swarm()
        assert result.valid is True
        assert result.uncovered_roles == ()

    def test_swarm_with_only_tester_missing_guardiana(self):
        result = validate_swarm(
            available_agents=[AgentRole.REGINA, AgentRole.TESTER],
        )
        assert result.valid is False
        assert "guardiana" in result.uncovered_roles

    def test_swarm_coverage_map_contains_orchestrator(self):
        result = validate_swarm()
        cmap = result.coverage_map
        assert "cervella-orchestrator" in cmap["regina"]

    def test_swarm_coverage_map_backend_in_worker(self):
        result = validate_swarm()
        cmap = result.coverage_map
        assert "cervella-backend" in cmap["worker"]

    def test_check_only_simple_task_protocol(self):
        result = validate_swarm(
            protocols=[SimpleTask],
            available_agents=[AgentRole.REGINA, AgentRole.FRONTEND],
        )
        assert result.valid is True
        assert "SimpleTask" in result.protocols_checked
