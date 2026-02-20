# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Regression tests for S382 bug hunt fixes.

Each test class corresponds to a confirmed bug from the S382
Code Review + Bug Hunt. Tests verify the FIX is correct.
"""

import pytest

from cervellaswarm_lingua_universale.checker import (
    MessageRecord,
    ProtocolViolation,
    SessionChecker,
    SessionComplete,
)
from cervellaswarm_lingua_universale.protocols import (
    Protocol,
    ProtocolChoice,
    ProtocolStep,
    STANDARD_PROTOCOLS,
)
from cervellaswarm_lingua_universale.types import (
    AuditRequest,
    AuditVerdict,
    AuditVerdictType,
    MessageKind,
    PlanDecision,
    PlanRequest,
    ResearchReport,
    TaskRequest,
    TaskResult,
    TaskStatus,
)


# ── BUG-LU-001: Multi-choice checker fix ────────────────────────────────────


class TestMultiChoiceChecker:
    """Checker must handle protocols with 2+ ProtocolChoice elements."""

    def _make_two_choice_protocol(self):
        step_task = ProtocolStep(
            sender="a", receiver="b", message_kind=MessageKind.TASK_REQUEST,
        )
        step_plan = ProtocolStep(
            sender="a", receiver="c", message_kind=MessageKind.PLAN_REQUEST,
        )
        step_result = ProtocolStep(
            sender="b", receiver="a", message_kind=MessageKind.TASK_RESULT,
        )
        step_audit = ProtocolStep(
            sender="c", receiver="a", message_kind=MessageKind.AUDIT_REQUEST,
        )
        choice1 = ProtocolChoice(
            decider="a",
            branches={"task": (step_task,), "plan": (step_plan,)},
        )
        choice2 = ProtocolChoice(
            decider="a",
            branches={"result": (step_result,), "audit": (step_audit,)},
        )
        return Protocol(
            name="TwoChoices", roles=("a", "b", "c"),
            elements=(choice1, choice2),
        )

    def test_two_choices_both_branches_complete(self):
        proto = self._make_two_choice_protocol()
        checker = SessionChecker(proto, session_id="MC001")
        # First choice: auto-detect "task" (unambiguous by receiver)
        checker.send("a", "b", TaskRequest(task_id="T1", description="X"))
        assert not checker.is_complete
        # Second choice: auto-detect "result" (unambiguous by receiver)
        checker.send("b", "a", TaskResult(
            task_id="T1", status=TaskStatus.OK, summary="Done",
        ))
        assert checker.is_complete

    def test_two_choices_explicit_branch_selection(self):
        proto = self._make_two_choice_protocol()
        checker = SessionChecker(proto, session_id="MC002")
        checker.choose_branch("plan")
        checker.send("a", "c", PlanRequest(plan_id="P1", task_description="X"))
        assert not checker.is_complete
        checker.choose_branch("audit")
        checker.send("c", "a", AuditRequest(audit_id="A1", target="test"))
        assert checker.is_complete

    def test_step_index_advances_past_first_choice(self):
        proto = self._make_two_choice_protocol()
        checker = SessionChecker(proto, session_id="MC003")
        checker.choose_branch("task")
        checker.send("a", "b", TaskRequest(task_id="T1", description="X"))
        # After first choice, step_index should be 1 (at second choice)
        assert checker.step_index == 1


# ── BUG-LU-002: Decider validation ──────────────────────────────────────────


class TestDeciderValidation:
    """ProtocolChoice.decider must be in Protocol.roles."""

    def test_invalid_decider_raises(self):
        step = ProtocolStep(
            sender="a", receiver="b", message_kind=MessageKind.TASK_REQUEST,
        )
        choice = ProtocolChoice(decider="nobody", branches={"go": (step,)})
        with pytest.raises(ValueError, match="decider 'nobody' not in protocol roles"):
            Protocol(name="Bad", roles=("a", "b"), elements=(choice,))

    def test_valid_decider_passes(self):
        step = ProtocolStep(
            sender="a", receiver="b", message_kind=MessageKind.TASK_REQUEST,
        )
        choice = ProtocolChoice(decider="a", branches={"go": (step,)})
        proto = Protocol(name="OK", roles=("a", "b"), elements=(choice,))
        assert proto.name == "OK"


# ── BUG-LU-003: Immutable branches ──────────────────────────────────────────


class TestImmutableBranches:
    """ProtocolChoice.branches must be immutable (MappingProxyType)."""

    def test_cannot_add_branch_after_creation(self):
        step = ProtocolStep(
            sender="a", receiver="b", message_kind=MessageKind.TASK_REQUEST,
        )
        choice = ProtocolChoice(decider="a", branches={"go": (step,)})
        with pytest.raises(TypeError):
            choice.branches["evil"] = (step,)

    def test_cannot_delete_branch_after_creation(self):
        step = ProtocolStep(
            sender="a", receiver="b", message_kind=MessageKind.TASK_REQUEST,
        )
        choice = ProtocolChoice(decider="a", branches={"go": (step,)})
        with pytest.raises(TypeError):
            del choice.branches["go"]

    def test_branches_read_operations_still_work(self):
        step = ProtocolStep(
            sender="a", receiver="b", message_kind=MessageKind.TASK_REQUEST,
        )
        choice = ProtocolChoice(decider="a", branches={"go": (step,)})
        assert "go" in choice.branches
        assert choice.branches.get("go") == (step,)
        assert list(choice.branches.keys()) == ["go"]
        assert len(choice.branches) == 1


# ── BUG-LU-005: Ambiguous branch detection ──────────────────────────────────


class TestAmbiguousBranchDetection:
    """Auto-detect must require explicit choose_branch for ambiguous cases."""

    def test_ambiguous_branches_require_choose_branch(self):
        """Two branches with identical first steps -> ambiguous."""
        step = ProtocolStep(
            sender="a", receiver="b", message_kind=MessageKind.TASK_REQUEST,
        )
        step2 = ProtocolStep(
            sender="b", receiver="a", message_kind=MessageKind.TASK_RESULT,
        )
        choice = ProtocolChoice(
            decider="a",
            branches={
                "path1": (step, step2),
                "path2": (step,),
            },
        )
        proto = Protocol(
            name="Ambiguous", roles=("a", "b"), elements=(choice,),
        )
        checker = SessionChecker(proto, session_id="AMB001")
        with pytest.raises(ProtocolViolation, match="branch selection"):
            checker.send(
                "a", "b",
                TaskRequest(task_id="T1", description="Test"),
            )

    def test_explicit_choose_branch_resolves_ambiguity(self):
        """Explicit choose_branch works even for ambiguous protocols."""
        step = ProtocolStep(
            sender="a", receiver="b", message_kind=MessageKind.TASK_REQUEST,
        )
        choice = ProtocolChoice(
            decider="a",
            branches={"path1": (step,), "path2": (step,)},
        )
        proto = Protocol(
            name="Ambiguous2", roles=("a", "b"), elements=(choice,),
        )
        checker = SessionChecker(proto, session_id="AMB002")
        checker.choose_branch("path2")
        checker.send("a", "b", TaskRequest(task_id="T1", description="Test"))
        assert checker.is_complete


# ── BUG-LU-006: Namespace leak cleanup ──────────────────────────────────────


class TestNamespaceLeak:
    """Loop variables _kind and _name must not leak into dsl module namespace."""

    def test_no_kind_in_dsl_namespace(self):
        from cervellaswarm_lingua_universale import dsl
        assert not hasattr(dsl, "_kind")

    def test_no_name_in_dsl_namespace(self):
        from cervellaswarm_lingua_universale import dsl
        assert not hasattr(dsl, "_name")


# ── BUG-LU-007: Empty protocol initial state ────────────────────────────────


class TestEmptyProtocolState:
    """Protocol with 0 elements should be immediately complete."""

    def test_empty_protocol_is_complete_on_init(self):
        proto = Protocol(name="Empty", roles=("a", "b"), elements=())
        checker = SessionChecker(proto, session_id="E001")
        assert checker.is_complete

    def test_empty_protocol_send_raises_session_complete(self):
        proto = Protocol(name="Empty", roles=("a", "b"), elements=())
        checker = SessionChecker(proto, session_id="E002")
        with pytest.raises(SessionComplete):
            checker.send(
                "a", "b",
                TaskRequest(task_id="T1", description="Test"),
            )


# ── BUG-LU-008: ResearchReport sources >= 1 ─────────────────────────────────


class TestResearchReportSources:
    """ResearchReport.sources_consulted must be >= 1 (consistent with query)."""

    def test_zero_sources_raises(self):
        with pytest.raises(ValueError, match="sources_consulted must be at least 1"):
            ResearchReport(query_id="Q1", topic="AI", sources_consulted=0)

    def test_one_source_valid(self):
        report = ResearchReport(query_id="Q1", topic="AI", sources_consulted=1)
        assert report.sources_consulted == 1


# ── BUG-LU-009: Immutable STANDARD_PROTOCOLS ────────────────────────────────


class TestImmutableRegistry:
    """STANDARD_PROTOCOLS registry must be immutable."""

    def test_cannot_add_to_registry(self):
        with pytest.raises(TypeError):
            STANDARD_PROTOCOLS["Fake"] = None  # type: ignore[index]

    def test_cannot_delete_from_registry(self):
        with pytest.raises(TypeError):
            del STANDARD_PROTOCOLS["DelegateTask"]  # type: ignore[attr-defined]

    def test_registry_has_all_standard_protocols(self):
        assert set(STANDARD_PROTOCOLS.keys()) == {
            "DelegateTask", "ArchitectFlow", "ResearchFlow", "SimpleTask",
        }


# ── BUG-LU-010: Duplicate roles ─────────────────────────────────────────────


class TestDuplicateRoles:
    """Protocol must reject duplicate role names."""

    def test_duplicate_roles_raises(self):
        with pytest.raises(ValueError, match="duplicate roles"):
            Protocol(name="Dup", roles=("a", "a", "b"), elements=())

    def test_unique_roles_pass(self):
        proto = Protocol(name="OK", roles=("a", "b"), elements=())
        assert len(proto.roles) == 2


# ── BUG-LU-011: Self-message validation ─────────────────────────────────────


class TestSelfMessage:
    """ProtocolStep must reject sender == receiver."""

    def test_self_message_raises(self):
        with pytest.raises(ValueError, match="sender and receiver cannot be the same"):
            ProtocolStep(
                sender="a", receiver="a", message_kind=MessageKind.TASK_REQUEST,
            )

    def test_empty_sender_raises(self):
        with pytest.raises(ValueError, match="sender cannot be empty"):
            ProtocolStep(
                sender="", receiver="b", message_kind=MessageKind.TASK_REQUEST,
            )

    def test_empty_receiver_raises(self):
        with pytest.raises(ValueError, match="receiver cannot be empty"):
            ProtocolStep(
                sender="a", receiver="", message_kind=MessageKind.TASK_REQUEST,
            )


# ── BUG-LU-012: max_repetitions validation ──────────────────────────────────


class TestMaxRepetitions:
    """Protocol.max_repetitions must be >= 1."""

    def test_zero_repetitions_raises(self):
        with pytest.raises(ValueError, match="max_repetitions must be at least 1"):
            Protocol(name="P", roles=("a", "b"), elements=(), max_repetitions=0)

    def test_negative_repetitions_raises(self):
        with pytest.raises(ValueError, match="max_repetitions must be at least 1"):
            Protocol(name="P", roles=("a", "b"), elements=(), max_repetitions=-5)


# ── BUG-LU-022: ProtocolChoice validation ───────────────────────────────────


class TestProtocolChoiceValidation:
    """ProtocolChoice must validate decider and branches at construction."""

    def test_empty_branches_raises(self):
        with pytest.raises(ValueError, match="branches cannot be empty"):
            ProtocolChoice(decider="a", branches={})

    def test_empty_decider_raises(self):
        step = ProtocolStep(
            sender="a", receiver="b", message_kind=MessageKind.TASK_REQUEST,
        )
        with pytest.raises(ValueError, match="decider cannot be empty"):
            ProtocolChoice(decider="", branches={"go": (step,)})


# ── API re-exports ──────────────────────────────────────────────────────────


# ── Coverage: max_repetitions > 1 ────────────────────────────────────────────


class TestProtocolRepetitions:
    """Protocol with max_repetitions > 1 should reset and run again."""

    def test_protocol_repeats_twice(self):
        step = ProtocolStep(
            sender="a", receiver="b", message_kind=MessageKind.TASK_REQUEST,
        )
        proto = Protocol(
            name="Repeat", roles=("a", "b"), elements=(step,),
            max_repetitions=2,
        )
        checker = SessionChecker(proto, session_id="R001")
        # First repetition
        checker.send("a", "b", TaskRequest(task_id="T1", description="First"))
        assert not checker.is_complete
        # Second repetition
        checker.send("a", "b", TaskRequest(task_id="T2", description="Second"))
        assert checker.is_complete

    def test_protocol_repeats_three_times(self):
        step = ProtocolStep(
            sender="a", receiver="b", message_kind=MessageKind.TASK_REQUEST,
        )
        proto = Protocol(
            name="Repeat3", roles=("a", "b"), elements=(step,),
            max_repetitions=3,
        )
        checker = SessionChecker(proto, session_id="R002")
        for i in range(3):
            checker.send(
                "a", "b",
                TaskRequest(task_id=f"T{i}", description=f"Rep {i}"),
            )
        assert checker.is_complete
        assert len(checker.log) == 3


# ── Coverage: steps after choice ─────────────────────────────────────────────


class TestStepsAfterChoice:
    """Protocol with steps after a ProtocolChoice element."""

    def test_step_after_choice_is_reached(self):
        """A final audit step after a choice should be executed."""
        step_task = ProtocolStep(
            sender="a", receiver="b", message_kind=MessageKind.TASK_REQUEST,
        )
        step_plan = ProtocolStep(
            sender="a", receiver="c", message_kind=MessageKind.PLAN_REQUEST,
        )
        step_audit = ProtocolStep(
            sender="c", receiver="a", message_kind=MessageKind.AUDIT_REQUEST,
        )
        choice = ProtocolChoice(
            decider="a",
            branches={"task": (step_task,), "plan": (step_plan,)},
        )
        proto = Protocol(
            name="ChoiceThenStep", roles=("a", "b", "c"),
            elements=(choice, step_audit),
        )
        checker = SessionChecker(proto, session_id="CAS001")
        checker.choose_branch("task")
        checker.send("a", "b", TaskRequest(task_id="T1", description="X"))
        assert not checker.is_complete
        # Now the audit step after the choice
        checker.send("c", "a", AuditRequest(audit_id="A1", target="test"))
        assert checker.is_complete

    def test_peek_after_choice_returns_post_choice_step(self):
        step_task = ProtocolStep(
            sender="a", receiver="b", message_kind=MessageKind.TASK_REQUEST,
        )
        step_audit = ProtocolStep(
            sender="b", receiver="a", message_kind=MessageKind.TASK_RESULT,
        )
        choice = ProtocolChoice(
            decider="a", branches={"go": (step_task,)},
        )
        proto = Protocol(
            name="Peek", roles=("a", "b"),
            elements=(choice, step_audit),
        )
        checker = SessionChecker(proto, session_id="CAS002")
        checker.choose_branch("go")
        # peek should return the branch step first
        expected = checker._state.peek_next_step()
        assert expected is not None
        assert expected.message_kind == MessageKind.TASK_REQUEST


# ── API re-exports ──────────────────────────────────────────────────────────


class TestReExports:
    """All public types must be importable from top-level package."""

    def test_enums_importable(self):
        from cervellaswarm_lingua_universale import (
            TaskStatus,
            AuditVerdictType,
            PlanComplexity,
        )
        assert TaskStatus.OK.value == "ok"
        assert AuditVerdictType.APPROVED.value == "approved"
        assert PlanComplexity.LOW.value == "low"

    def test_exceptions_importable(self):
        from cervellaswarm_lingua_universale import (
            ProtocolViolation,
            SessionComplete,
            MessageRecord,
        )
        assert issubclass(ProtocolViolation, Exception)
        assert issubclass(SessionComplete, Exception)
