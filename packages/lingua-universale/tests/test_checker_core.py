"""Tests for SessionChecker core behavior: violations, session state, log, role bindings.

Covers: happy paths (SimpleTask, DelegateTask, ResearchFlow), ProtocolViolation
(wrong sender/receiver/message type), SessionComplete, role_bindings,
summary(), log recording, session ID auto-generation.
"""

import pytest

from cervellaswarm_lingua_universale.checker import (
    MessageRecord,
    ProtocolViolation,
    SessionChecker,
    SessionComplete,
)
from cervellaswarm_lingua_universale.protocols import (
    DelegateTask,
    ResearchFlow,
    SimpleTask,
)
from cervellaswarm_lingua_universale.types import (
    AuditRequest,
    AuditVerdict,
    AuditVerdictType,
    MessageKind,
    ResearchQuery,
    ResearchReport,
    TaskRequest,
    TaskResult,
    TaskStatus,
)


# ── Helpers ───────────────────────────────────────────────────────────────────

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


# ── Happy Path: SimpleTask ────────────────────────────────────────────────────

class TestSimpleTaskHappyPath:
    def test_complete_flow(self):
        checker = SessionChecker(SimpleTask, session_id="S001")
        assert not checker.is_complete

        checker.send("regina", "worker", make_task_request())
        checker.send("worker", "regina", make_task_result())

        assert checker.is_complete

    def test_step_index_advances(self):
        checker = SessionChecker(SimpleTask, session_id="S001")
        assert checker.step_index == 0
        checker.send("regina", "worker", make_task_request())
        assert checker.step_index == 1

    def test_log_has_two_entries(self):
        checker = SessionChecker(SimpleTask, session_id="S001")
        checker.send("regina", "worker", make_task_request())
        checker.send("worker", "regina", make_task_result())

        assert len(checker.log) == 2

    def test_log_first_entry_fields(self):
        checker = SessionChecker(SimpleTask, session_id="S001")
        checker.send("regina", "worker", make_task_request())
        record = checker.log[0]
        assert isinstance(record, MessageRecord)
        assert record.sender == "regina"
        assert record.receiver == "worker"
        assert record.kind == MessageKind.TASK_REQUEST


# ── Happy Path: DelegateTask ──────────────────────────────────────────────────

class TestDelegateTaskHappyPath:
    def test_complete_flow(self):
        checker = SessionChecker(DelegateTask, session_id="S002")
        checker.send("regina", "worker", make_task_request())
        checker.send("worker", "regina", make_task_result())
        checker.send("regina", "guardiana", make_audit_request())
        checker.send("guardiana", "regina", make_audit_verdict())
        assert checker.is_complete

    def test_log_has_four_entries_and_protocol_name(self):
        checker = SessionChecker(DelegateTask, session_id="S002")
        checker.send("regina", "worker", make_task_request())
        checker.send("worker", "regina", make_task_result())
        checker.send("regina", "guardiana", make_audit_request())
        checker.send("guardiana", "regina", make_audit_verdict())
        assert len(checker.log) == 4
        assert checker.protocol_name == "DelegateTask"


# ── Happy Path: ResearchFlow ──────────────────────────────────────────────────

class TestResearchFlowHappyPath:
    def test_complete_flow(self):
        checker = SessionChecker(ResearchFlow, session_id="RF001")
        checker.send(
            "regina", "researcher",
            ResearchQuery(query_id="Q1", topic="AI frameworks", min_sources=5),
        )
        checker.send(
            "researcher", "regina",
            ResearchReport(query_id="Q1", topic="AI frameworks", sources_consulted=8),
        )
        checker.send("regina", "guardiana", make_audit_request())
        checker.send("guardiana", "regina", make_audit_verdict())
        assert checker.is_complete
        assert len(checker.log) == 4


# ── ProtocolViolation: wrong sender ───────────────────────────────────────────

class TestWrongSender:
    def test_wrong_sender_raises_violation_with_metadata(self):
        checker = SessionChecker(SimpleTask, session_id="V001")
        with pytest.raises(ProtocolViolation) as exc_info:
            checker.send("worker", "worker", make_task_request())
        err = exc_info.value
        assert "sender" in err.expected
        assert err.protocol == "SimpleTask"
        assert err.session_id == "V001"
        assert err.step == 0


# ── ProtocolViolation: wrong receiver ────────────────────────────────────────

class TestWrongReceiver:
    def test_wrong_receiver_raises_violation(self):
        checker = SessionChecker(SimpleTask, session_id="V002")
        with pytest.raises(ProtocolViolation) as exc_info:
            checker.send("regina", "guardiana", make_task_request())
        assert "receiver" in exc_info.value.expected


# ── ProtocolViolation: wrong message type ─────────────────────────────────────

class TestWrongMessageType:
    def test_wrong_message_type_raises_violation(self):
        checker = SessionChecker(SimpleTask, session_id="V003")
        with pytest.raises(ProtocolViolation) as exc_info:
            checker.send("regina", "worker", make_audit_request())
        err = exc_info.value
        assert "message" in err.expected
        assert "task_request" in err.expected

    def test_wrong_type_at_second_step(self):
        checker = SessionChecker(SimpleTask, session_id="V003")
        checker.send("regina", "worker", make_task_request())
        with pytest.raises(ProtocolViolation):
            checker.send("worker", "regina", make_task_request())


# ── SessionComplete ───────────────────────────────────────────────────────────

class TestSessionComplete:
    def test_send_after_complete_raises_with_metadata(self):
        checker = SessionChecker(SimpleTask, session_id="SC001")
        checker.send("regina", "worker", make_task_request())
        checker.send("worker", "regina", make_task_result())
        assert checker.is_complete

        with pytest.raises(SessionComplete) as exc_info:
            checker.send("regina", "worker", make_task_request())
        err = exc_info.value
        assert err.protocol == "SimpleTask"
        assert err.session_id == "SC001"
        assert "already complete" in str(err)


# ── role_bindings ─────────────────────────────────────────────────────────────

class TestRoleBindings:
    def test_named_agents_resolve_to_roles(self):
        bindings = {
            "worker": "cervella-backend",
            "guardiana": "cervella-guardiana-qualita",
        }
        checker = SessionChecker(DelegateTask, session_id="RB001", role_bindings=bindings)
        checker.send("regina", "cervella-backend", make_task_request())
        checker.send("cervella-backend", "regina", make_task_result())
        checker.send("regina", "cervella-guardiana-qualita", make_audit_request())
        checker.send("cervella-guardiana-qualita", "regina", make_audit_verdict())
        assert checker.is_complete

    def test_mixed_role_and_name(self):
        bindings = {"worker": "cervella-tester"}
        checker = SessionChecker(SimpleTask, session_id="RB002", role_bindings=bindings)
        checker.send("regina", "cervella-tester", make_task_request())
        checker.send("cervella-tester", "regina", make_task_result())
        assert checker.is_complete

    def test_unbound_name_fails(self):
        checker = SessionChecker(SimpleTask, session_id="RB003")
        with pytest.raises(ProtocolViolation):
            checker.send("anonymous-agent", "worker", make_task_request())


# ── summary() ─────────────────────────────────────────────────────────────────

class TestSummary:
    def test_summary_keys(self):
        checker = SessionChecker(SimpleTask, session_id="SUM001")
        s = checker.summary()
        for key in ("session_id", "protocol", "step", "branch", "completed",
                    "messages", "started_at", "completed_at"):
            assert key in s

    def test_summary_before_complete(self):
        checker = SessionChecker(SimpleTask, session_id="SUM001")
        s = checker.summary()
        assert s["completed"] is False
        assert s["messages"] == 0
        assert s["completed_at"] is None

    def test_summary_after_complete(self):
        checker = SessionChecker(SimpleTask, session_id="SUM001")
        checker.send("regina", "worker", make_task_request())
        checker.send("worker", "regina", make_task_result())
        s = checker.summary()
        assert s["completed"] is True
        assert s["messages"] == 2
        assert s["completed_at"] is not None

    def test_summary_session_id(self):
        checker = SessionChecker(SimpleTask, session_id="MY_SESSION")
        assert checker.summary()["session_id"] == "MY_SESSION"


# ── Log recording ─────────────────────────────────────────────────────────────

class TestLogRecording:
    def test_log_starts_empty(self):
        checker = SessionChecker(SimpleTask, session_id="LOG001")
        assert len(checker.log) == 0

    def test_log_records_sender_receiver_kind(self):
        checker = SessionChecker(SimpleTask, session_id="LOG001")
        checker.send("regina", "worker", make_task_request())
        r = checker.log[0]
        assert r.sender == "regina"
        assert r.receiver == "worker"
        assert r.kind == MessageKind.TASK_REQUEST

    def test_log_has_timestamp(self):
        checker = SessionChecker(SimpleTask, session_id="LOG001")
        checker.send("regina", "worker", make_task_request())
        assert checker.log[0].timestamp > 0

    def test_log_is_copy(self):
        checker = SessionChecker(SimpleTask, session_id="LOG001")
        checker.send("regina", "worker", make_task_request())
        log_copy = checker.log
        log_copy.clear()
        assert len(checker.log) == 1

    def test_log_step_index_recorded(self):
        checker = SessionChecker(DelegateTask, session_id="LOG002")
        checker.send("regina", "worker", make_task_request())
        checker.send("worker", "regina", make_task_result())
        assert checker.log[0].step_index == 0
        assert checker.log[1].step_index == 1


# ── Session ID auto-generation ────────────────────────────────────────────────

class TestSessionId:
    def test_auto_generated_id_contains_protocol_name(self):
        checker = SessionChecker(SimpleTask)
        assert "SimpleTask" in checker.session_id

    def test_explicit_session_id_preserved(self):
        checker = SessionChecker(SimpleTask, session_id="EXPLICIT_ID")
        assert checker.session_id == "EXPLICIT_ID"
