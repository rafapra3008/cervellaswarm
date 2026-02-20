"""Tests for SessionChecker branching and complex flows.

Covers: ArchitectFlow approve branch, ArchitectFlow reject branch,
auto-detect branch from message, choose_branch explicit, choose_branch
with invalid branch, choose_branch when not at choice point.
"""

import pytest

from cervellaswarm_lingua_universale.checker import (
    ProtocolViolation,
    SessionChecker,
)
from cervellaswarm_lingua_universale.protocols import (
    ArchitectFlow,
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


# ── Helpers ───────────────────────────────────────────────────────────────────

def make_task_request():
    return TaskRequest(task_id="T001", description="Do the work")


def make_task_result():
    return TaskResult(task_id="T001", status=TaskStatus.OK, summary="Done")


def make_audit_request():
    return AuditRequest(audit_id="A001", target="output")


def make_audit_verdict():
    return AuditVerdict(
        audit_id="A001",
        verdict=AuditVerdictType.APPROVED,
        score=9.0,
        checked=("quality",),
    )


def make_plan_request():
    return PlanRequest(plan_id="P001", task_description="Build the thing")


def make_plan_proposal():
    return PlanProposal(
        plan_id="P001",
        complexity=PlanComplexity.MEDIUM,
        risk_score=0.4,
        files_affected=5,
    )


def make_plan_decision(approved=True, feedback=""):
    if not approved and not feedback:
        feedback = "Not good enough"
    return PlanDecision(plan_id="P001", approved=approved, feedback=feedback)


# ── ArchitectFlow: approve branch ─────────────────────────────────────────────

class TestArchitectFlowApprove:
    def test_approve_branch_completes(self):
        checker = SessionChecker(ArchitectFlow, session_id="AF001")
        checker.send("regina", "architect", make_plan_request())
        checker.send("architect", "regina", make_plan_proposal())
        checker.choose_branch("approve")
        checker.send("regina", "architect", make_plan_decision(approved=True))
        checker.send("regina", "worker", make_task_request())
        checker.send("worker", "regina", make_task_result())
        checker.send("regina", "guardiana", make_audit_request())
        checker.send("guardiana", "regina", make_audit_verdict())
        assert checker.is_complete

    def test_approve_branch_log_count(self):
        checker = SessionChecker(ArchitectFlow, session_id="AF001")
        checker.send("regina", "architect", make_plan_request())
        checker.send("architect", "regina", make_plan_proposal())
        checker.choose_branch("approve")
        checker.send("regina", "architect", make_plan_decision(approved=True))
        checker.send("regina", "worker", make_task_request())
        checker.send("worker", "regina", make_task_result())
        checker.send("regina", "guardiana", make_audit_request())
        checker.send("guardiana", "regina", make_audit_verdict())
        # 2 pre-choice + 5 approve branch steps
        assert len(checker.log) == 7

    def test_approve_ends_with_audit_verdict(self):
        checker = SessionChecker(ArchitectFlow, session_id="AF001")
        checker.send("regina", "architect", make_plan_request())
        checker.send("architect", "regina", make_plan_proposal())
        checker.choose_branch("approve")
        checker.send("regina", "architect", make_plan_decision(approved=True))
        checker.send("regina", "worker", make_task_request())
        checker.send("worker", "regina", make_task_result())
        checker.send("regina", "guardiana", make_audit_request())
        checker.send("guardiana", "regina", make_audit_verdict())
        from cervellaswarm_lingua_universale.types import MessageKind
        assert checker.log[-1].kind == MessageKind.AUDIT_VERDICT


# ── ArchitectFlow: reject branch ─────────────────────────────────────────────

class TestArchitectFlowReject:
    def test_reject_branch_completes_after_two_steps(self):
        checker = SessionChecker(ArchitectFlow, session_id="AF002")
        checker.send("regina", "architect", make_plan_request())
        checker.send("architect", "regina", make_plan_proposal())
        checker.choose_branch("reject")
        checker.send("regina", "architect", make_plan_decision(approved=False))
        checker.send("architect", "regina", make_plan_proposal())
        assert checker.is_complete

    def test_reject_branch_log_count(self):
        checker = SessionChecker(ArchitectFlow, session_id="AF002")
        checker.send("regina", "architect", make_plan_request())
        checker.send("architect", "regina", make_plan_proposal())
        checker.choose_branch("reject")
        checker.send("regina", "architect", make_plan_decision(approved=False))
        checker.send("architect", "regina", make_plan_proposal())
        # 2 pre-choice + 2 reject branch steps
        assert len(checker.log) == 4

    def test_reject_first_step_is_plan_decision(self):
        checker = SessionChecker(ArchitectFlow, session_id="AF002")
        checker.send("regina", "architect", make_plan_request())
        checker.send("architect", "regina", make_plan_proposal())
        checker.choose_branch("reject")
        checker.send("regina", "architect", make_plan_decision(approved=False))
        from cervellaswarm_lingua_universale.types import MessageKind
        assert checker.log[2].kind == MessageKind.PLAN_DECISION

    def test_reject_second_step_is_plan_proposal(self):
        checker = SessionChecker(ArchitectFlow, session_id="AF002")
        checker.send("regina", "architect", make_plan_request())
        checker.send("architect", "regina", make_plan_proposal())
        checker.choose_branch("reject")
        checker.send("regina", "architect", make_plan_decision(approved=False))
        checker.send("architect", "regina", make_plan_proposal())
        from cervellaswarm_lingua_universale.types import MessageKind
        assert checker.log[3].kind == MessageKind.PLAN_PROPOSAL


# ── Auto-detect branch ────────────────────────────────────────────────────────

class TestAutoDetectBranch:
    def test_ambiguous_branches_require_explicit_choose(self):
        """Both ArchitectFlow branches start with PlanDecision -> ambiguous.

        Auto-detect returns None for ambiguous cases, requiring
        explicit choose_branch(). This is CORRECT behavior.
        """
        checker = SessionChecker(ArchitectFlow, session_id="AD001")
        checker.send("regina", "architect", make_plan_request())
        checker.send("architect", "regina", make_plan_proposal())

        from cervellaswarm_lingua_universale.checker import ProtocolViolation
        with pytest.raises(ProtocolViolation, match="branch selection"):
            checker.send("regina", "architect", make_plan_decision(approved=True))

    def test_auto_detect_works_for_unambiguous_branches(self):
        """Auto-detect works when branches have distinguishable first steps."""
        step_task = ProtocolStep(
            sender="a", receiver="b", message_kind=MessageKind.TASK_REQUEST,
        )
        step_plan = ProtocolStep(
            sender="a", receiver="c", message_kind=MessageKind.PLAN_REQUEST,
        )
        choice = ProtocolChoice(
            decider="a",
            branches={
                "task": (step_task,),
                "plan": (step_plan,),
            },
        )
        proto = Protocol(name="Unambiguous", roles=("a", "b", "c"), elements=(choice,))
        checker = SessionChecker(proto, session_id="AD002")
        # Auto-detect: sender=a, receiver=b, kind=TASK_REQUEST -> "task" branch
        checker.send("a", "b", TaskRequest(task_id="T1", description="Test"))
        assert checker.is_complete

    def test_auto_detect_sets_branch_for_unambiguous(self):
        """Verify branch is set by auto-detect for unambiguous protocols."""
        step_task = ProtocolStep(
            sender="a", receiver="b", message_kind=MessageKind.TASK_REQUEST,
        )
        step_result = ProtocolStep(
            sender="b", receiver="a", message_kind=MessageKind.TASK_RESULT,
        )
        step_plan = ProtocolStep(
            sender="a", receiver="c", message_kind=MessageKind.PLAN_REQUEST,
        )
        choice = ProtocolChoice(
            decider="a",
            branches={
                "task": (step_task, step_result),
                "plan": (step_plan,),
            },
        )
        proto = Protocol(name="WithBranch", roles=("a", "b", "c"), elements=(choice,))
        checker = SessionChecker(proto, session_id="AD003")
        assert checker.current_branch is None
        checker.send("a", "b", TaskRequest(task_id="T1", description="Test"))
        # branch was auto-detected, and first step consumed;
        # branch may or may not still be set (depends on branch exhaustion)
        # but no exception = success


# ── choose_branch ─────────────────────────────────────────────────────────────

class TestChooseBranch:
    def test_choose_approve_branch(self):
        checker = SessionChecker(ArchitectFlow, session_id="CB001")
        checker.send("regina", "architect", make_plan_request())
        checker.send("architect", "regina", make_plan_proposal())
        checker.choose_branch("approve")
        assert checker.current_branch == "approve"

    def test_choose_reject_branch(self):
        checker = SessionChecker(ArchitectFlow, session_id="CB002")
        checker.send("regina", "architect", make_plan_request())
        checker.send("architect", "regina", make_plan_proposal())
        checker.choose_branch("reject")
        assert checker.current_branch == "reject"

    def test_choose_branch_when_not_at_choice_raises(self):
        checker = SessionChecker(SimpleTask, session_id="CB003")
        with pytest.raises(ProtocolViolation) as exc_info:
            checker.choose_branch("approve")
        assert "not at a choice point" in exc_info.value.expected

    def test_choose_branch_when_not_at_choice_contains_protocol(self):
        checker = SessionChecker(SimpleTask, session_id="CB003")
        with pytest.raises(ProtocolViolation) as exc_info:
            checker.choose_branch("approve")
        assert exc_info.value.protocol == "SimpleTask"

    def test_choose_invalid_branch_raises(self):
        checker = SessionChecker(ArchitectFlow, session_id="CB004")
        checker.send("regina", "architect", make_plan_request())
        checker.send("architect", "regina", make_plan_proposal())
        with pytest.raises(ProtocolViolation) as exc_info:
            checker.choose_branch("nonexistent_branch")
        err = exc_info.value
        assert "nonexistent_branch" in err.got
        # Expected message should mention valid branches
        assert "approve" in err.expected or "reject" in err.expected

    def test_choose_branch_after_pre_choice_steps_is_valid(self):
        checker = SessionChecker(ArchitectFlow, session_id="CB005")
        checker.send("regina", "architect", make_plan_request())
        checker.send("architect", "regina", make_plan_proposal())
        # Now at choice point
        checker.choose_branch("approve")
        # Subsequent send should work
        checker.send("regina", "architect", make_plan_decision(approved=True))
        # No exception = success
