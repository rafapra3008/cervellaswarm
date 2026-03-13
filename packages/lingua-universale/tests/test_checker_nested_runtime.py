# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for SessionChecker nested choice runtime (LU 1.2).

Validates that the stack-based ChoiceFrame approach correctly handles
arbitrarily nested ProtocolChoice blocks at runtime.
"""

from __future__ import annotations

import pytest

from cervellaswarm_lingua_universale.checker import (
    ProtocolViolation,
    SessionChecker,
    SessionComplete,
)
from cervellaswarm_lingua_universale.protocols import (
    Protocol,
    ProtocolChoice,
    ProtocolStep,
)
from cervellaswarm_lingua_universale.types import (
    AuditRequest,
    AuditVerdict,
    AuditVerdictType,
    MessageKind,
    TaskRequest,
    TaskResult,
    TaskStatus,
)


# ── Test Protocols ──────────────────────────────────────────────────

def _saga_order() -> Protocol:
    """SagaOrder with nested choice (payment -> inventory decision)."""
    return Protocol(
        name="SagaOrder",
        roles=("coordinator", "payment", "inventory"),
        elements=(
            ProtocolStep(
                sender="coordinator", receiver="payment",
                message_kind=MessageKind.TASK_REQUEST, description="charge order",
            ),
            ProtocolChoice(
                decider="payment",
                branches={
                    "success": (
                        ProtocolStep(
                            sender="payment", receiver="coordinator",
                            message_kind=MessageKind.TASK_RESULT, description="confirmation",
                        ),
                        ProtocolStep(
                            sender="coordinator", receiver="inventory",
                            message_kind=MessageKind.TASK_REQUEST, description="reserve items",
                        ),
                        ProtocolChoice(
                            decider="inventory",
                            branches={
                                "reserved": (
                                    ProtocolStep(
                                        sender="inventory", receiver="coordinator",
                                        message_kind=MessageKind.TASK_RESULT,
                                        description="reservation",
                                    ),
                                ),
                                "out_of_stock": (
                                    ProtocolStep(
                                        sender="inventory", receiver="coordinator",
                                        message_kind=MessageKind.TASK_RESULT,
                                        description="error",
                                    ),
                                    ProtocolStep(
                                        sender="coordinator", receiver="payment",
                                        message_kind=MessageKind.TASK_REQUEST,
                                        description="refund order",
                                    ),
                                ),
                            },
                        ),
                    ),
                    "failure": (
                        ProtocolStep(
                            sender="payment", receiver="coordinator",
                            message_kind=MessageKind.TASK_RESULT, description="error",
                        ),
                    ),
                },
            ),
        ),
    )


def _triple_nested() -> Protocol:
    """Three levels deep: a -> b choice -> c choice -> d choice."""
    return Protocol(
        name="TripleNested",
        roles=("a", "b", "c"),
        elements=(
            ProtocolStep(
                sender="a", receiver="b",
                message_kind=MessageKind.TASK_REQUEST, description="start",
            ),
            ProtocolChoice(
                decider="a",
                branches={
                    "path1": (
                        ProtocolStep(
                            sender="a", receiver="b",
                            message_kind=MessageKind.TASK_RESULT, description="l1",
                        ),
                        ProtocolChoice(
                            decider="b",
                            branches={
                                "deep1": (
                                    ProtocolStep(
                                        sender="b", receiver="c",
                                        message_kind=MessageKind.TASK_REQUEST,
                                        description="l2",
                                    ),
                                    ProtocolChoice(
                                        decider="c",
                                        branches={
                                            "leaf_a": (
                                                ProtocolStep(
                                                    sender="c", receiver="a",
                                                    message_kind=MessageKind.TASK_RESULT,
                                                    description="done_a",
                                                ),
                                            ),
                                            "leaf_b": (
                                                ProtocolStep(
                                                    sender="c", receiver="a",
                                                    message_kind=MessageKind.AUDIT_REQUEST,
                                                    description="done_b",
                                                ),
                                            ),
                                        },
                                    ),
                                ),
                                "deep2": (
                                    ProtocolStep(
                                        sender="b", receiver="a",
                                        message_kind=MessageKind.TASK_RESULT,
                                        description="shortcut",
                                    ),
                                ),
                            },
                        ),
                    ),
                    "path2": (
                        ProtocolStep(
                            sender="a", receiver="c",
                            message_kind=MessageKind.TASK_RESULT, description="quick",
                        ),
                    ),
                },
            ),
        ),
    )


def _steps_after_nested() -> Protocol:
    """Steps come AFTER a nested choice -- tests frame pop correctly."""
    return Protocol(
        name="StepsAfterNested",
        roles=("a", "b", "c"),
        elements=(
            ProtocolChoice(
                decider="a",
                branches={
                    "go": (
                        ProtocolStep(
                            sender="a", receiver="b",
                            message_kind=MessageKind.TASK_REQUEST, description="begin",
                        ),
                        ProtocolChoice(
                            decider="b",
                            branches={
                                "ok": (
                                    ProtocolStep(
                                        sender="b", receiver="a",
                                        message_kind=MessageKind.TASK_RESULT,
                                        description="ok",
                                    ),
                                ),
                                "fail": (
                                    ProtocolStep(
                                        sender="b", receiver="a",
                                        message_kind=MessageKind.TASK_RESULT,
                                        description="fail",
                                    ),
                                ),
                            },
                        ),
                        ProtocolStep(
                            sender="a", receiver="c",
                            message_kind=MessageKind.TASK_REQUEST,
                            description="after nested",
                        ),
                    ),
                    "skip": (
                        ProtocolStep(
                            sender="a", receiver="c",
                            message_kind=MessageKind.TASK_RESULT, description="skipped",
                        ),
                    ),
                },
            ),
        ),
    )


def _msg(kind_val: str = "task_request"):
    """Create a SwarmMessage of the given kind."""
    if kind_val == "task_request":
        return TaskRequest(task_id="T001", description="test")
    if kind_val == "task_result":
        return TaskResult(task_id="T001", status=TaskStatus.OK, summary="ok")
    if kind_val == "audit_request":
        return AuditRequest(audit_id="A001", target="test")
    if kind_val == "audit_verdict":
        return AuditVerdict(
            audit_id="A001", verdict=AuditVerdictType.APPROVED,
            score=9.5, checked=("test",),
        )
    raise ValueError(f"Unknown kind: {kind_val}")


# ── A: Happy Path -- 2 levels (SagaOrder) ──────────────────────────


class TestNestedTwoLevels:
    """SagaOrder nested choice: payment -> inventory."""

    def test_success_reserved(self):
        c = SessionChecker(_saga_order(), session_id="s1")
        c.send("coordinator", "payment", _msg("task_request"))
        c.choose_branch("success")
        c.send("payment", "coordinator", _msg("task_result"))
        c.send("coordinator", "inventory", _msg("task_request"))
        c.choose_branch("reserved")
        c.send("inventory", "coordinator", _msg("task_result"))
        assert c.is_complete

    def test_success_out_of_stock(self):
        c = SessionChecker(_saga_order(), session_id="s2")
        c.send("coordinator", "payment", _msg("task_request"))
        c.choose_branch("success")
        c.send("payment", "coordinator", _msg("task_result"))
        c.send("coordinator", "inventory", _msg("task_request"))
        c.choose_branch("out_of_stock")
        c.send("inventory", "coordinator", _msg("task_result"))
        c.send("coordinator", "payment", _msg("task_request"))
        assert c.is_complete

    def test_failure_branch(self):
        c = SessionChecker(_saga_order(), session_id="s3")
        c.send("coordinator", "payment", _msg("task_request"))
        c.choose_branch("failure")
        c.send("payment", "coordinator", _msg("task_result"))
        assert c.is_complete

    def test_auto_detect_outer(self):
        c = SessionChecker(_saga_order(), session_id="s4")
        c.send("coordinator", "payment", _msg("task_request"))
        # Auto-detect: payment -> coordinator task_result matches both branches
        # but "success" first step is payment->coordinator:task_result
        # and "failure" first step is payment->coordinator:task_result too
        # So auto-detect should return None (ambiguous) -- need explicit choose
        with pytest.raises(ProtocolViolation, match="branch selection"):
            c.send("payment", "coordinator", _msg("task_result"))

    def test_nested_choose_then_auto_detect_inner(self):
        c = SessionChecker(_saga_order(), session_id="s5")
        c.send("coordinator", "payment", _msg("task_request"))
        c.choose_branch("success")
        c.send("payment", "coordinator", _msg("task_result"))
        c.send("coordinator", "inventory", _msg("task_request"))
        # Inner choice: reserved first = inventory->coordinator:task_result
        #               out_of_stock first = inventory->coordinator:task_result
        # Also ambiguous -- explicit choose needed
        with pytest.raises(ProtocolViolation, match="branch selection"):
            c.send("inventory", "coordinator", _msg("task_result"))


# ── B: Happy Path -- 3 levels (TripleNested) ───────────────────────


class TestTripleNested:
    """Three levels of nested choice."""

    def test_path1_deep1_leaf_a(self):
        c = SessionChecker(_triple_nested(), session_id="t1")
        c.send("a", "b", _msg("task_request"))
        c.choose_branch("path1")
        c.send("a", "b", _msg("task_result"))
        c.choose_branch("deep1")
        c.send("b", "c", _msg("task_request"))
        c.choose_branch("leaf_a")
        c.send("c", "a", _msg("task_result"))
        assert c.is_complete

    def test_path1_deep1_leaf_b(self):
        c = SessionChecker(_triple_nested(), session_id="t2")
        c.send("a", "b", _msg("task_request"))
        c.choose_branch("path1")
        c.send("a", "b", _msg("task_result"))
        c.choose_branch("deep1")
        c.send("b", "c", _msg("task_request"))
        c.choose_branch("leaf_b")
        c.send("c", "a", _msg("audit_request"))
        assert c.is_complete

    def test_path1_deep2(self):
        c = SessionChecker(_triple_nested(), session_id="t3")
        c.send("a", "b", _msg("task_request"))
        c.choose_branch("path1")
        c.send("a", "b", _msg("task_result"))
        c.choose_branch("deep2")
        c.send("b", "a", _msg("task_result"))
        assert c.is_complete

    def test_path2_flat(self):
        c = SessionChecker(_triple_nested(), session_id="t4")
        c.send("a", "b", _msg("task_request"))
        c.choose_branch("path2")
        c.send("a", "c", _msg("task_result"))
        assert c.is_complete


# ── C: Stack Pop ───────────────────────────────────────────────────


class TestStackPop:
    """Frame pop and parent resumption."""

    def test_stack_depth_during_nested(self):
        c = SessionChecker(_saga_order(), session_id="d1")
        assert c.summary()["choice_depth"] == 0
        c.send("coordinator", "payment", _msg("task_request"))
        c.choose_branch("success")
        assert c.summary()["choice_depth"] == 1
        c.send("payment", "coordinator", _msg("task_result"))
        c.send("coordinator", "inventory", _msg("task_request"))
        c.choose_branch("reserved")
        assert c.summary()["choice_depth"] == 2
        c.send("inventory", "coordinator", _msg("task_result"))
        # After completion, stack is empty
        assert c.summary()["choice_depth"] == 0

    def test_branch_path_during_nested(self):
        c = SessionChecker(_saga_order(), session_id="bp1")
        c.send("coordinator", "payment", _msg("task_request"))
        c.choose_branch("success")
        c.send("payment", "coordinator", _msg("task_result"))
        c.send("coordinator", "inventory", _msg("task_request"))
        c.choose_branch("out_of_stock")
        assert c.summary()["branch_path"] == ["success", "out_of_stock"]

    def test_steps_after_nested_choice(self):
        c = SessionChecker(_steps_after_nested(), session_id="an1")
        c.choose_branch("go")
        c.send("a", "b", _msg("task_request"))
        c.choose_branch("ok")
        c.send("b", "a", _msg("task_result"))
        # After inner choice completes, should advance to step AFTER nested
        c.send("a", "c", _msg("task_request"))
        assert c.is_complete

    def test_steps_after_nested_choice_fail_path(self):
        c = SessionChecker(_steps_after_nested(), session_id="an2")
        c.choose_branch("go")
        c.send("a", "b", _msg("task_request"))
        c.choose_branch("fail")
        c.send("b", "a", _msg("task_result"))
        c.send("a", "c", _msg("task_request"))
        assert c.is_complete

    def test_skip_branch_no_nesting(self):
        c = SessionChecker(_steps_after_nested(), session_id="an3")
        c.choose_branch("skip")
        c.send("a", "c", _msg("task_result"))
        assert c.is_complete


# ── D: Violations ──────────────────────────────────────────────────


class TestNestedViolations:
    """Correct violations inside nested branches."""

    def test_wrong_sender_inside_nested(self):
        c = SessionChecker(_saga_order(), session_id="v1")
        c.send("coordinator", "payment", _msg("task_request"))
        c.choose_branch("success")
        c.send("payment", "coordinator", _msg("task_result"))
        c.send("coordinator", "inventory", _msg("task_request"))
        c.choose_branch("reserved")
        with pytest.raises(ProtocolViolation, match="sender"):
            c.send("payment", "coordinator", _msg("task_result"))  # wrong sender

    def test_wrong_kind_inside_nested(self):
        c = SessionChecker(_saga_order(), session_id="v2")
        c.send("coordinator", "payment", _msg("task_request"))
        c.choose_branch("success")
        c.send("payment", "coordinator", _msg("task_result"))
        c.send("coordinator", "inventory", _msg("task_request"))
        c.choose_branch("reserved")
        with pytest.raises(ProtocolViolation, match="message"):
            c.send("inventory", "coordinator", _msg("audit_request"))  # wrong kind

    def test_invalid_nested_branch_name(self):
        c = SessionChecker(_saga_order(), session_id="v3")
        c.send("coordinator", "payment", _msg("task_request"))
        c.choose_branch("success")
        c.send("payment", "coordinator", _msg("task_result"))
        c.send("coordinator", "inventory", _msg("task_request"))
        with pytest.raises(ProtocolViolation, match="branch"):
            c.choose_branch("nonexistent")

    def test_choose_branch_when_not_at_choice(self):
        c = SessionChecker(_saga_order(), session_id="v4")
        c.send("coordinator", "payment", _msg("task_request"))
        c.choose_branch("success")
        # Now at a step, not a choice
        with pytest.raises(ProtocolViolation, match="not at a choice point"):
            c.choose_branch("reserved")

    def test_send_after_nested_complete(self):
        c = SessionChecker(_saga_order(), session_id="v5")
        c.send("coordinator", "payment", _msg("task_request"))
        c.choose_branch("failure")
        c.send("payment", "coordinator", _msg("task_result"))
        assert c.is_complete
        with pytest.raises(SessionComplete):
            c.send("coordinator", "payment", _msg("task_request"))


# ── E: Backward Compatibility ──────────────────────────────────────


class TestBackwardCompat:
    """Flat protocols behave identically to LU 1.1."""

    def _flat_protocol(self) -> Protocol:
        return Protocol(
            name="Flat",
            roles=("a", "b"),
            elements=(
                ProtocolStep(
                    sender="a", receiver="b",
                    message_kind=MessageKind.TASK_REQUEST, description="ask",
                ),
                ProtocolChoice(
                    decider="b",
                    branches={
                        "yes": (
                            ProtocolStep(
                                sender="b", receiver="a",
                                message_kind=MessageKind.TASK_RESULT,
                                description="yes",
                            ),
                        ),
                        "no": (
                            ProtocolStep(
                                sender="b", receiver="a",
                                message_kind=MessageKind.AUDIT_VERDICT,
                                description="no",
                            ),
                        ),
                    },
                ),
            ),
        )

    def test_flat_yes_branch(self):
        c = SessionChecker(self._flat_protocol(), session_id="f1")
        c.send("a", "b", _msg("task_request"))
        c.choose_branch("yes")
        c.send("b", "a", _msg("task_result"))
        assert c.is_complete

    def test_flat_no_branch(self):
        c = SessionChecker(self._flat_protocol(), session_id="f2")
        c.send("a", "b", _msg("task_request"))
        c.choose_branch("no")
        c.send("b", "a", _msg("audit_verdict"))
        assert c.is_complete

    def test_flat_stack_always_empty(self):
        c = SessionChecker(self._flat_protocol(), session_id="f3")
        c.send("a", "b", _msg("task_request"))
        assert c.summary()["choice_depth"] == 0
        c.choose_branch("yes")
        assert c.summary()["choice_depth"] == 1
        c.send("b", "a", _msg("task_result"))
        assert c.summary()["choice_depth"] == 0
        assert c.is_complete

    def test_branch_property_backward_compat(self):
        c = SessionChecker(self._flat_protocol(), session_id="f4")
        assert c.current_branch is None
        c.send("a", "b", _msg("task_request"))
        c.choose_branch("yes")
        assert c.current_branch == "yes"

    def test_summary_has_expected_keys(self):
        c = SessionChecker(self._flat_protocol(), session_id="f5")
        s = c.summary()
        assert "session_id" in s
        assert "branch" in s
        assert "choice_depth" in s
        assert "branch_path" in s


# ── F: Edge Cases ──────────────────────────────────────────────────


class TestEdgeCases:
    """Edge cases: repetition, simple protocols, completion."""

    def test_simple_no_choice_protocol(self):
        p = Protocol(
            name="Simple",
            roles=("a", "b"),
            elements=(
                ProtocolStep(
                    sender="a", receiver="b",
                    message_kind=MessageKind.TASK_REQUEST, description="go",
                ),
                ProtocolStep(
                    sender="b", receiver="a",
                    message_kind=MessageKind.TASK_RESULT, description="done",
                ),
            ),
        )
        c = SessionChecker(p, session_id="e1")
        c.send("a", "b", _msg("task_request"))
        c.send("b", "a", _msg("task_result"))
        assert c.is_complete
        assert c.summary()["choice_depth"] == 0

    def test_repetition_resets_stack(self):
        p = Protocol(
            name="RepeatNested",
            roles=("a", "b"),
            max_repetitions=2,
            elements=(
                ProtocolChoice(
                    decider="a",
                    branches={
                        "go": (
                            ProtocolStep(
                                sender="a", receiver="b",
                                message_kind=MessageKind.TASK_REQUEST, description="x",
                            ),
                        ),
                    },
                ),
            ),
        )
        c = SessionChecker(p, session_id="r1")
        # First repetition
        c.choose_branch("go")
        c.send("a", "b", _msg("task_request"))
        assert not c.is_complete
        # Second repetition
        c.choose_branch("go")
        c.send("a", "b", _msg("task_request"))
        assert c.is_complete

    def test_nested_all_paths_complete(self):
        """All paths through nested choice lead to completion."""
        proto = _saga_order()
        paths = [
            # success -> reserved
            [("coordinator", "payment", "task_request"),
             "success",
             ("payment", "coordinator", "task_result"),
             ("coordinator", "inventory", "task_request"),
             "reserved",
             ("inventory", "coordinator", "task_result")],
            # success -> out_of_stock
            [("coordinator", "payment", "task_request"),
             "success",
             ("payment", "coordinator", "task_result"),
             ("coordinator", "inventory", "task_request"),
             "out_of_stock",
             ("inventory", "coordinator", "task_result"),
             ("coordinator", "payment", "task_request")],
            # failure
            [("coordinator", "payment", "task_request"),
             "failure",
             ("payment", "coordinator", "task_result")],
        ]
        for i, path in enumerate(paths):
            c = SessionChecker(proto, session_id=f"all_{i}")
            for item in path:
                if isinstance(item, str):
                    c.choose_branch(item)
                else:
                    s, r, k = item
                    c.send(s, r, _msg(k))
            assert c.is_complete, f"Path {i} did not complete"
