# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Integration tests for monitor.py + SessionChecker.

Tests that the monitor receives correct events when SessionChecker
runs real protocols: DelegateTask, SimpleTask, ArchitectFlow.
Also covers edge cases: empty protocol, violations, backward compat
(monitor=None), repetitions, and explicit vs auto branch selection.
"""

import pytest

from cervellaswarm_lingua_universale.checker import (
    ProtocolViolation,
    SessionChecker,
    SessionComplete,
)
from cervellaswarm_lingua_universale.monitor import (
    BranchChosen,
    EventCollector,
    MessageSent,
    MetricsSnapshot,
    MonitorEvent,
    ProtocolMonitor,
    RepetitionStarted,
    SessionEnded,
    SessionStarted,
    ViolationOccurred,
)
from cervellaswarm_lingua_universale.protocols import (
    ArchitectFlow,
    DelegateTask,
    Protocol,
    ProtocolChoice,
    ProtocolStep,
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
    TaskRequest,
    TaskResult,
    TaskStatus,
)


# ============================================================
# Helpers
# ============================================================

def make_task_request(task_id="T001"):
    return TaskRequest(task_id=task_id, description="Do the work")


def make_task_result(task_id="T001"):
    return TaskResult(task_id=task_id, status=TaskStatus.OK, summary="Done successfully")


def make_audit_request(audit_id="A001"):
    return AuditRequest(audit_id=audit_id, target="output")


def make_audit_verdict(audit_id="A001"):
    return AuditVerdict(
        audit_id=audit_id,
        verdict=AuditVerdictType.APPROVED,
        score=9.0,
        checked=("quality check",),
    )


def make_plan_request(plan_id="P001"):
    return PlanRequest(plan_id=plan_id, task_description="Build the thing")


def make_plan_proposal(plan_id="P001"):
    return PlanProposal(
        plan_id=plan_id,
        complexity=PlanComplexity.MEDIUM,
        risk_score=0.3,
        files_affected=5,
    )


def make_plan_decision_approve(plan_id="P001"):
    return PlanDecision(plan_id=plan_id, approved=True)


def make_plan_decision_reject(plan_id="P001"):
    return PlanDecision(plan_id=plan_id, approved=False, feedback="Too risky")


# ============================================================
# 1. Session lifecycle events
# ============================================================

class TestSessionStartedEvent:
    def test_session_started_emitted_on_init(self):
        monitor = ProtocolMonitor()
        collector = EventCollector()
        monitor.add_listener(collector)

        SessionChecker(DelegateTask, session_id="S001", monitor=monitor)

        started = collector.of_type(SessionStarted)
        assert len(started) == 1
        assert started[0].session_id == "S001"
        assert started[0].protocol_name == "DelegateTask"

    def test_session_started_carries_roles(self):
        monitor = ProtocolMonitor()
        collector = EventCollector()
        monitor.add_listener(collector)

        SessionChecker(DelegateTask, session_id="S001", monitor=monitor)

        started = collector.of_type(SessionStarted)
        assert started[0].roles == DelegateTask.roles

    def test_session_started_timestamp_is_recent(self):
        import time
        before = time.time()
        monitor = ProtocolMonitor()
        collector = EventCollector()
        monitor.add_listener(collector)

        SessionChecker(SimpleTask, session_id="S001", monitor=monitor)

        after = time.time()
        started = collector.of_type(SessionStarted)
        assert before <= started[0].timestamp <= after


class TestSessionEndedEvent:
    def test_session_ended_emitted_after_last_message(self):
        monitor = ProtocolMonitor()
        collector = EventCollector()
        monitor.add_listener(collector)

        checker = SessionChecker(SimpleTask, session_id="S001", monitor=monitor)
        checker.send("regina", "worker", make_task_request())
        checker.send("worker", "regina", make_task_result())

        ended = collector.of_type(SessionEnded)
        assert len(ended) == 1
        assert ended[0].session_id == "S001"
        assert ended[0].total_messages == 2
        assert ended[0].repetitions == 1

    def test_session_ended_duration_is_positive(self):
        monitor = ProtocolMonitor()
        collector = EventCollector()
        monitor.add_listener(collector)

        checker = SessionChecker(SimpleTask, session_id="S001", monitor=monitor)
        checker.send("regina", "worker", make_task_request())
        checker.send("worker", "regina", make_task_result())

        ended = collector.of_type(SessionEnded)
        assert ended[0].duration_ms >= 0.0

    def test_session_ended_not_emitted_before_complete(self):
        monitor = ProtocolMonitor()
        collector = EventCollector()
        monitor.add_listener(collector)

        checker = SessionChecker(SimpleTask, session_id="S001", monitor=monitor)
        checker.send("regina", "worker", make_task_request())
        # Not complete yet - only 1 of 2 steps done

        assert len(collector.of_type(SessionEnded)) == 0


# ============================================================
# 2. MessageSent events
# ============================================================

class TestMessageSentEvent:
    def test_message_sent_emitted_on_valid_send(self):
        monitor = ProtocolMonitor()
        collector = EventCollector()
        monitor.add_listener(collector)

        checker = SessionChecker(SimpleTask, session_id="S001", monitor=monitor)
        checker.send("regina", "worker", make_task_request())

        messages = collector.of_type(MessageSent)
        assert len(messages) == 1

    def test_message_sent_carries_correct_fields(self):
        monitor = ProtocolMonitor()
        collector = EventCollector()
        monitor.add_listener(collector)

        checker = SessionChecker(SimpleTask, session_id="S001", monitor=monitor)
        checker.send("regina", "worker", make_task_request())

        msg = collector.of_type(MessageSent)[0]
        assert msg.session_id == "S001"
        assert msg.sender == "regina"
        assert msg.receiver == "worker"
        assert msg.message_kind == MessageKind.TASK_REQUEST
        assert msg.step_index == 0

    def test_message_sent_duration_ms_is_positive(self):
        monitor = ProtocolMonitor()
        collector = EventCollector()
        monitor.add_listener(collector)

        checker = SessionChecker(SimpleTask, session_id="S001", monitor=monitor)
        checker.send("regina", "worker", make_task_request())

        msg = collector.of_type(MessageSent)[0]
        assert msg.duration_ms >= 0.0

    def test_message_sent_branch_none_for_linear_protocol(self):
        monitor = ProtocolMonitor()
        collector = EventCollector()
        monitor.add_listener(collector)

        checker = SessionChecker(SimpleTask, session_id="S001", monitor=monitor)
        checker.send("regina", "worker", make_task_request())

        msg = collector.of_type(MessageSent)[0]
        assert msg.branch is None

    def test_four_messages_emitted_for_delegate_task(self):
        monitor = ProtocolMonitor()
        collector = EventCollector()
        monitor.add_listener(collector)

        checker = SessionChecker(DelegateTask, session_id="S001", monitor=monitor)
        checker.send("regina", "worker", make_task_request())
        checker.send("worker", "regina", make_task_result())
        checker.send("regina", "guardiana", make_audit_request())
        checker.send("guardiana", "regina", make_audit_verdict())

        assert len(collector.of_type(MessageSent)) == 4


# ============================================================
# 3. ViolationOccurred events
# ============================================================

class TestViolationOccurredEvent:
    def test_violation_emitted_before_exception_raised(self):
        monitor = ProtocolMonitor()
        collector = EventCollector()
        monitor.add_listener(collector)

        checker = SessionChecker(SimpleTask, session_id="S001", monitor=monitor)
        with pytest.raises(ProtocolViolation):
            # Wrong sender
            checker.send("worker", "regina", make_task_request())

        violations = collector.of_type(ViolationOccurred)
        assert len(violations) == 1

    def test_violation_contains_expected_and_got(self):
        monitor = ProtocolMonitor()
        collector = EventCollector()
        monitor.add_listener(collector)

        checker = SessionChecker(SimpleTask, session_id="S001", monitor=monitor)
        with pytest.raises(ProtocolViolation):
            checker.send("worker", "regina", make_task_request())

        v = collector.of_type(ViolationOccurred)[0]
        assert "sender=regina" in v.expected
        assert "worker" in v.got

    def test_violation_has_correct_step_index(self):
        monitor = ProtocolMonitor()
        collector = EventCollector()
        monitor.add_listener(collector)

        checker = SessionChecker(SimpleTask, session_id="S001", monitor=monitor)
        with pytest.raises(ProtocolViolation):
            checker.send("worker", "regina", make_task_request())

        v = collector.of_type(ViolationOccurred)[0]
        assert v.step_index == 0

    def test_violation_not_emitted_on_valid_send(self):
        monitor = ProtocolMonitor()
        collector = EventCollector()
        monitor.add_listener(collector)

        checker = SessionChecker(SimpleTask, session_id="S001", monitor=monitor)
        checker.send("regina", "worker", make_task_request())

        assert len(collector.of_type(ViolationOccurred)) == 0

    def test_violation_emitted_on_wrong_receiver(self):
        monitor = ProtocolMonitor()
        collector = EventCollector()
        monitor.add_listener(collector)

        checker = SessionChecker(SimpleTask, session_id="S001", monitor=monitor)
        with pytest.raises(ProtocolViolation):
            # Wrong receiver: worker should send to regina, not to worker
            checker.send("regina", "regina", make_task_request())

        assert len(collector.of_type(ViolationOccurred)) == 1

    def test_violation_emitted_on_wrong_message_kind(self):
        monitor = ProtocolMonitor()
        collector = EventCollector()
        monitor.add_listener(collector)

        checker = SessionChecker(SimpleTask, session_id="S001", monitor=monitor)
        with pytest.raises(ProtocolViolation):
            # Wrong kind: expected TASK_REQUEST, sending TASK_RESULT
            checker.send("regina", "worker", make_task_result())

        assert len(collector.of_type(ViolationOccurred)) == 1

    def test_multiple_violations_same_session(self):
        monitor = ProtocolMonitor()
        collector = EventCollector()
        monitor.add_listener(collector)

        checker = SessionChecker(SimpleTask, session_id="S001", monitor=monitor)
        for _ in range(3):
            with pytest.raises(ProtocolViolation):
                checker.send("worker", "regina", make_task_request())

        assert len(collector.of_type(ViolationOccurred)) == 3


# ============================================================
# 4. BranchChosen events
# ============================================================

class TestBranchChosenEvent:
    def test_explicit_choose_branch_emits_branch_chosen(self):
        monitor = ProtocolMonitor()
        collector = EventCollector()
        monitor.add_listener(collector)

        checker = SessionChecker(ArchitectFlow, session_id="AF001", monitor=monitor)
        checker.send("regina", "architect", make_plan_request())
        checker.send("architect", "regina", make_plan_proposal())

        # Explicitly choose branch
        checker.choose_branch("reject")

        branches = collector.of_type(BranchChosen)
        assert len(branches) == 1
        assert branches[0].branch_name == "reject"
        assert branches[0].auto_detected is False

    def test_explicit_choose_approve_branch(self):
        monitor = ProtocolMonitor()
        collector = EventCollector()
        monitor.add_listener(collector)

        checker = SessionChecker(ArchitectFlow, session_id="AF001", monitor=monitor)
        checker.send("regina", "architect", make_plan_request())
        checker.send("architect", "regina", make_plan_proposal())

        checker.choose_branch("approve")

        branches = collector.of_type(BranchChosen)
        assert len(branches) == 1
        assert branches[0].branch_name == "approve"
        assert branches[0].auto_detected is False

    def test_branch_chosen_has_correct_step_index(self):
        monitor = ProtocolMonitor()
        collector = EventCollector()
        monitor.add_listener(collector)

        checker = SessionChecker(ArchitectFlow, session_id="AF001", monitor=monitor)
        checker.send("regina", "architect", make_plan_request())
        checker.send("architect", "regina", make_plan_proposal())
        checker.choose_branch("approve")

        branch_ev = collector.of_type(BranchChosen)[0]
        assert branch_ev.step_index == 2  # Choice is at index 2

    def test_message_sent_carries_branch_name_when_in_branch(self):
        monitor = ProtocolMonitor()
        collector = EventCollector()
        monitor.add_listener(collector)

        checker = SessionChecker(ArchitectFlow, session_id="AF001", monitor=monitor)
        checker.send("regina", "architect", make_plan_request())
        checker.send("architect", "regina", make_plan_proposal())
        checker.choose_branch("reject")
        checker.send("regina", "architect", make_plan_decision_reject())

        # The message inside the branch should carry branch name
        branch_messages = [
            e for e in collector.of_type(MessageSent)
            if e.branch == "reject"
        ]
        assert len(branch_messages) >= 1


# ============================================================
# 5. Empty protocol events
# ============================================================

class TestEmptyProtocolEvents:
    def test_empty_protocol_emits_session_started_and_ended(self):
        monitor = ProtocolMonitor()
        collector = EventCollector()
        monitor.add_listener(collector)

        empty_proto = Protocol(
            name="Empty",
            roles=("a", "b"),
            elements=(),
        )
        SessionChecker(empty_proto, session_id="EMPTY001", monitor=monitor)

        assert len(collector.of_type(SessionStarted)) == 1
        assert len(collector.of_type(SessionEnded)) == 1
        assert len(collector.of_type(MessageSent)) == 0

    def test_empty_protocol_session_ended_has_zero_messages(self):
        monitor = ProtocolMonitor()
        collector = EventCollector()
        monitor.add_listener(collector)

        empty_proto = Protocol(
            name="Empty",
            roles=("a", "b"),
            elements=(),
        )
        SessionChecker(empty_proto, session_id="EMPTY001", monitor=monitor)

        ended = collector.of_type(SessionEnded)[0]
        assert ended.total_messages == 0


# ============================================================
# 6. Monitor=None backward compatibility
# ============================================================

class TestMonitorNoneBackwardCompat:
    def test_no_monitor_no_error_on_init(self):
        checker = SessionChecker(SimpleTask, session_id="S001")
        assert not checker.is_complete  # No exception

    def test_no_monitor_no_error_on_valid_send(self):
        checker = SessionChecker(SimpleTask, session_id="S001")
        checker.send("regina", "worker", make_task_request())
        checker.send("worker", "regina", make_task_result())
        assert checker.is_complete

    def test_no_monitor_no_error_on_violation(self):
        checker = SessionChecker(SimpleTask, session_id="S001")
        with pytest.raises(ProtocolViolation):
            checker.send("worker", "regina", make_task_request())
        # No crash - violation handled without monitor

    def test_no_monitor_no_error_on_choose_branch(self):
        checker = SessionChecker(ArchitectFlow, session_id="AF001")
        checker.send("regina", "architect", make_plan_request())
        checker.send("architect", "regina", make_plan_proposal())
        checker.choose_branch("approve")  # No crash without monitor


# ============================================================
# 7. Full DelegateTask flow - metrics validation
# ============================================================

class TestDelegateTaskMetrics:
    def test_full_delegate_task_metrics(self):
        monitor = ProtocolMonitor()
        collector = EventCollector()
        monitor.add_listener(collector)

        checker = SessionChecker(DelegateTask, session_id="DT001", monitor=monitor)
        checker.send("regina", "worker", make_task_request())
        checker.send("worker", "regina", make_task_result())
        checker.send("regina", "guardiana", make_audit_request())
        checker.send("guardiana", "regina", make_audit_verdict())

        snap = monitor.metrics
        assert snap.sessions_started == 1
        assert snap.sessions_completed == 1
        assert snap.total_messages == 4
        assert snap.total_violations == 0
        assert snap.sessions_violated == 0
        assert snap.avg_step_duration_ms > 0.0
        assert snap.avg_session_duration_ms > 0.0

    def test_full_delegate_task_event_sequence(self):
        monitor = ProtocolMonitor()
        collector = EventCollector()
        monitor.add_listener(collector)

        checker = SessionChecker(DelegateTask, session_id="DT001", monitor=monitor)
        checker.send("regina", "worker", make_task_request())
        checker.send("worker", "regina", make_task_result())
        checker.send("regina", "guardiana", make_audit_request())
        checker.send("guardiana", "regina", make_audit_verdict())

        event_types = [type(e).__name__ for e in collector.events]
        assert event_types[0] == "SessionStarted"
        assert event_types[-1] == "SessionEnded"
        message_types = [t for t in event_types if t == "MessageSent"]
        assert len(message_types) == 4

    def test_metrics_sessions_per_protocol(self):
        monitor = ProtocolMonitor()

        checker = SessionChecker(DelegateTask, session_id="DT001", monitor=monitor)
        checker.send("regina", "worker", make_task_request())
        checker.send("worker", "regina", make_task_result())
        checker.send("regina", "guardiana", make_audit_request())
        checker.send("guardiana", "regina", make_audit_verdict())

        snap = monitor.metrics
        assert snap.sessions_per_protocol["DelegateTask"] == 1


# ============================================================
# 8. Violation + metrics integration
# ============================================================

class TestViolationMetricsIntegration:
    def test_violation_increments_sessions_violated_once(self):
        monitor = ProtocolMonitor()
        collector = EventCollector()
        monitor.add_listener(collector)

        checker = SessionChecker(SimpleTask, session_id="S001", monitor=monitor)
        for _ in range(3):
            with pytest.raises(ProtocolViolation):
                checker.send("worker", "regina", make_task_request())

        snap = monitor.metrics
        assert snap.sessions_violated == 1  # same session
        assert snap.total_violations == 3

    def test_two_sessions_with_violations_counted_separately(self):
        monitor = ProtocolMonitor()

        for sid in ["S001", "S002"]:
            checker = SessionChecker(SimpleTask, session_id=sid, monitor=monitor)
            with pytest.raises(ProtocolViolation):
                checker.send("worker", "regina", make_task_request())

        snap = monitor.metrics
        assert snap.sessions_violated == 2

    def test_violation_by_step_tracked_correctly(self):
        monitor = ProtocolMonitor()

        checker = SessionChecker(SimpleTask, session_id="S001", monitor=monitor)
        with pytest.raises(ProtocolViolation):
            checker.send("worker", "worker", make_task_request())  # Step 0

        snap = monitor.metrics
        assert snap.violation_by_step[0] == 1


# ============================================================
# 9. ArchitectFlow approve branch - full flow
# ============================================================

class TestArchitectFlowApprove:
    def test_approve_branch_full_flow_events(self):
        monitor = ProtocolMonitor()
        collector = EventCollector()
        monitor.add_listener(collector)

        checker = SessionChecker(ArchitectFlow, session_id="AF001", monitor=monitor)
        checker.send("regina", "architect", make_plan_request())
        checker.send("architect", "regina", make_plan_proposal())
        checker.choose_branch("approve")
        checker.send("regina", "architect", make_plan_decision_approve())
        checker.send("regina", "worker", make_task_request())
        checker.send("worker", "regina", make_task_result())
        checker.send("regina", "guardiana", make_audit_request())
        checker.send("guardiana", "regina", make_audit_verdict())

        assert checker.is_complete
        assert len(collector.of_type(SessionStarted)) == 1
        assert len(collector.of_type(SessionEnded)) == 1
        assert len(collector.of_type(BranchChosen)) == 1
        assert collector.of_type(BranchChosen)[0].branch_name == "approve"
        assert collector.of_type(BranchChosen)[0].auto_detected is False
        assert len(collector.of_type(MessageSent)) == 7


# ============================================================
# 10. ArchitectFlow reject branch - auto-detection
# ============================================================

class TestArchitectFlowRejectAutoDetect:
    def test_reject_branch_auto_detected(self):
        monitor = ProtocolMonitor()
        collector = EventCollector()
        monitor.add_listener(collector)

        checker = SessionChecker(ArchitectFlow, session_id="AF002", monitor=monitor)
        checker.send("regina", "architect", make_plan_request())
        checker.send("architect", "regina", make_plan_proposal())
        # Auto-detect: both "approve" and "reject" start with PLAN_DECISION from regina to architect
        # Since both branches start identically, auto-detection returns None (ambiguous)
        # We need explicit choose_branch for ArchitectFlow
        checker.choose_branch("reject")
        checker.send("regina", "architect", make_plan_decision_reject())
        checker.send("architect", "regina", make_plan_proposal())

        assert checker.is_complete
        branches = collector.of_type(BranchChosen)
        assert len(branches) == 1
        assert branches[0].branch_name == "reject"
        assert branches[0].auto_detected is False


# ============================================================
# 11. Custom protocol with auto-detectable branches
# ============================================================

class TestAutoDetectUnambiguousBranch:
    def _make_protocol_with_unique_branches(self):
        """Protocol where branches start with DIFFERENT message kinds -> auto-detectable."""
        return Protocol(
            name="UniqueChoice",
            roles=("regina", "worker"),
            elements=(
                ProtocolChoice(
                    decider="regina",
                    branches={
                        "fast": (
                            ProtocolStep(
                                sender="regina",
                                receiver="worker",
                                message_kind=MessageKind.TASK_REQUEST,
                            ),
                        ),
                        "research": (
                            ProtocolStep(
                                sender="regina",
                                receiver="worker",
                                message_kind=MessageKind.RESEARCH_QUERY,
                            ),
                        ),
                    },
                ),
            ),
        )

    def test_auto_detect_emits_branch_chosen_with_auto_true(self):
        monitor = ProtocolMonitor()
        collector = EventCollector()
        monitor.add_listener(collector)

        proto = self._make_protocol_with_unique_branches()
        checker = SessionChecker(proto, session_id="UC001", monitor=monitor)

        from cervellaswarm_lingua_universale.types import ResearchQuery
        checker.send(
            "regina",
            "worker",
            ResearchQuery(query_id="Q001", topic="test topic"),
        )

        branches = collector.of_type(BranchChosen)
        assert len(branches) == 1
        assert branches[0].branch_name == "research"
        assert branches[0].auto_detected is True


# ============================================================
# 12. Repetition events (max_repetitions > 1)
# ============================================================

class TestRepetitionStartedEvent:
    def _make_repeating_protocol(self, max_repetitions=2):
        return Protocol(
            name="Repeating",
            roles=("a", "b"),
            elements=(
                ProtocolStep(
                    sender="a",
                    receiver="b",
                    message_kind=MessageKind.TASK_REQUEST,
                ),
                ProtocolStep(
                    sender="b",
                    receiver="a",
                    message_kind=MessageKind.TASK_RESULT,
                ),
            ),
            max_repetitions=max_repetitions,
        )

    def _make_simple_request():
        return TaskRequest(task_id="T001", description="Do it")

    def _make_simple_result():
        return TaskResult(task_id="T001", status=TaskStatus.OK, summary="Done it")

    def test_repetition_started_emitted_between_cycles(self):
        monitor = ProtocolMonitor()
        collector = EventCollector()
        monitor.add_listener(collector)

        proto = self._make_repeating_protocol(max_repetitions=2)
        checker = SessionChecker(proto, session_id="R001", monitor=monitor)

        req = TaskRequest(task_id="T001", description="Do it")
        res = TaskResult(task_id="T001", status=TaskStatus.OK, summary="Done it")

        # First cycle
        checker.send("a", "b", req)
        checker.send("b", "a", res)
        # Second cycle (repetition)
        checker.send("a", "b", req)
        checker.send("b", "a", res)

        assert checker.is_complete
        reps = collector.of_type(RepetitionStarted)
        assert len(reps) == 1
        assert reps[0].repetition_number == 1

    def test_no_repetition_event_for_max_repetitions_1(self):
        monitor = ProtocolMonitor()
        collector = EventCollector()
        monitor.add_listener(collector)

        checker = SessionChecker(SimpleTask, session_id="S001", monitor=monitor)
        checker.send("regina", "worker", TaskRequest(task_id="T001", description="work"))
        checker.send("worker", "regina", TaskResult(task_id="T001", status=TaskStatus.OK, summary="done"))

        assert len(collector.of_type(RepetitionStarted)) == 0

    def test_repetition_number_increments_correctly(self):
        monitor = ProtocolMonitor()
        collector = EventCollector()
        monitor.add_listener(collector)

        proto = self._make_repeating_protocol(max_repetitions=3)
        checker = SessionChecker(proto, session_id="R001", monitor=monitor)

        req = TaskRequest(task_id="T001", description="Do it")
        res = TaskResult(task_id="T001", status=TaskStatus.OK, summary="Done it")

        for _ in range(3):
            checker.send("a", "b", req)
            checker.send("b", "a", res)

        reps = collector.of_type(RepetitionStarted)
        assert len(reps) == 2
        assert reps[0].repetition_number == 1
        assert reps[1].repetition_number == 2


# ============================================================
# 13. Listener added during emit does not receive current event
# ============================================================

class TestListenerAddedDuringEmit:
    def test_listener_added_during_emit_not_notified_for_current_event(self):
        monitor = ProtocolMonitor()
        late_collector = EventCollector()

        class AddingListener:
            def on_event(self, event: MonitorEvent) -> None:
                # Add another listener mid-emit
                monitor.add_listener(late_collector)

        monitor.add_listener(AddingListener())
        monitor.emit(
            SessionStarted(
                session_id="S001",
                protocol_name="TestProto",
                timestamp=0.0,
                roles=("a", "b"),
            )
        )

        # late_collector was added DURING emit, so it should not have received
        # the event that triggered the add (snapshot was taken before notification)
        assert len(late_collector.events) == 0


# ============================================================
# 14. Listener removed during emit still receives current event
# ============================================================

class TestListenerRemovedDuringEmit:
    def test_listener_removed_during_emit_still_receives_current(self):
        monitor = ProtocolMonitor()
        victim = EventCollector()
        bystander = EventCollector()

        class RemovingListener:
            def on_event(self, event: MonitorEvent) -> None:
                monitor.remove_listener(victim)

        monitor.add_listener(RemovingListener())
        monitor.add_listener(victim)
        monitor.add_listener(bystander)

        ev = SessionStarted(
            session_id="S001",
            protocol_name="TestProto",
            timestamp=0.0,
            roles=("a", "b"),
        )
        monitor.emit(ev)

        # victim WAS in the snapshot taken at the start of emit,
        # so it SHOULD have received the event
        assert len(victim.events) == 1
        assert len(bystander.events) == 1
        # After emit, victim is removed
        assert monitor.listener_count == 2  # RemovingListener + bystander


# ============================================================
# 15. choose_branch violation emits ViolationOccurred
# ============================================================

class TestChooseBranchViolation:
    def test_choose_branch_when_not_at_choice_emits_violation(self):
        monitor = ProtocolMonitor()
        collector = EventCollector()
        monitor.add_listener(collector)

        checker = SessionChecker(SimpleTask, session_id="S001", monitor=monitor)
        with pytest.raises(ProtocolViolation):
            checker.choose_branch("any")

        assert len(collector.of_type(ViolationOccurred)) == 1

    def test_choose_invalid_branch_emits_violation(self):
        monitor = ProtocolMonitor()
        collector = EventCollector()
        monitor.add_listener(collector)

        checker = SessionChecker(ArchitectFlow, session_id="AF001", monitor=monitor)
        checker.send("regina", "architect", make_plan_request())
        checker.send("architect", "regina", make_plan_proposal())

        with pytest.raises(ProtocolViolation):
            checker.choose_branch("nonexistent_branch")

        assert len(collector.of_type(ViolationOccurred)) == 1


# ============================================================
# 16. Full flow with monitor reset
# ============================================================

class TestMonitorReset:
    def test_reset_metrics_clears_after_full_flow(self):
        monitor = ProtocolMonitor()
        collector = EventCollector()
        monitor.add_listener(collector)

        checker = SessionChecker(SimpleTask, session_id="S001", monitor=monitor)
        checker.send("regina", "worker", make_task_request())
        checker.send("worker", "regina", make_task_result())

        # Before reset
        snap = monitor.metrics
        assert snap.sessions_started == 1
        assert snap.total_messages == 2

        monitor.reset_metrics()

        # After reset
        snap = monitor.metrics
        assert snap.sessions_started == 0
        assert snap.total_messages == 0
        assert snap.sessions_completed == 0

        # Collector still has events (it's independent)
        assert len(collector.events) > 0
