"""Tests for core protocol building blocks in cervellaswarm_lingua_universale.protocols.

Covers: ProtocolStep creation/immutability, ProtocolChoice creation/immutability,
Protocol creation with valid/invalid roles, empty name, single role.
"""

import pytest

from cervellaswarm_lingua_universale.protocols import (
    Protocol,
    ProtocolChoice,
    ProtocolStep,
)
from cervellaswarm_lingua_universale.types import MessageKind


# ── ProtocolStep ─────────────────────────────────────────────────────────────

class TestProtocolStep:
    def test_valid_creation(self):
        step = ProtocolStep(
            sender="regina",
            receiver="worker",
            message_kind=MessageKind.TASK_REQUEST,
            description="Delegate task",
        )
        assert step.sender == "regina"
        assert step.receiver == "worker"
        assert step.message_kind == MessageKind.TASK_REQUEST
        assert step.description == "Delegate task"

    def test_description_optional(self):
        step = ProtocolStep(
            sender="regina",
            receiver="worker",
            message_kind=MessageKind.TASK_REQUEST,
        )
        assert step.description == ""

    def test_frozen_immutable(self):
        step = ProtocolStep(
            sender="regina",
            receiver="worker",
            message_kind=MessageKind.TASK_REQUEST,
        )
        with pytest.raises(Exception):
            step.sender = "changed"  # type: ignore[misc]

    def test_all_message_kinds_accepted(self):
        for kind in MessageKind:
            step = ProtocolStep(sender="a", receiver="b", message_kind=kind)
            assert step.message_kind == kind


# ── ProtocolChoice ────────────────────────────────────────────────────────────

class TestProtocolChoice:
    def test_valid_creation(self):
        approve_step = ProtocolStep(
            sender="regina",
            receiver="architect",
            message_kind=MessageKind.PLAN_DECISION,
        )
        reject_step = ProtocolStep(
            sender="regina",
            receiver="architect",
            message_kind=MessageKind.PLAN_DECISION,
            description="Reject with feedback",
        )
        choice = ProtocolChoice(
            decider="regina",
            branches={
                "approve": (approve_step,),
                "reject": (reject_step,),
            },
            description="Regina decides",
        )
        assert choice.decider == "regina"
        assert "approve" in choice.branches
        assert "reject" in choice.branches
        assert choice.description == "Regina decides"

    def test_description_optional(self):
        step = ProtocolStep(
            sender="a",
            receiver="b",
            message_kind=MessageKind.TASK_REQUEST,
        )
        choice = ProtocolChoice(decider="a", branches={"go": (step,)})
        assert choice.description == ""

    def test_frozen_immutable(self):
        step = ProtocolStep(
            sender="regina",
            receiver="worker",
            message_kind=MessageKind.TASK_REQUEST,
        )
        choice = ProtocolChoice(
            decider="regina",
            branches={"go": (step,)},
        )
        with pytest.raises(Exception):
            choice.decider = "changed"  # type: ignore[misc]


# ── Protocol creation and validation ─────────────────────────────────────────

class TestProtocol:
    def test_valid_two_role_protocol(self):
        proto = Protocol(
            name="MinimalProto",
            roles=("sender_role", "receiver_role"),
            elements=(
                ProtocolStep(
                    sender="sender_role",
                    receiver="receiver_role",
                    message_kind=MessageKind.TASK_REQUEST,
                ),
            ),
        )
        assert proto.name == "MinimalProto"
        assert len(proto.roles) == 2

    def test_empty_elements_allowed(self):
        proto = Protocol(name="Empty", roles=("a", "b"), elements=())
        assert len(proto.elements) == 0

    def test_empty_name_raises(self):
        with pytest.raises(ValueError, match="protocol name cannot be empty"):
            Protocol(name="", roles=("a", "b"), elements=())

    def test_single_role_raises(self):
        with pytest.raises(ValueError, match="at least 2 roles"):
            Protocol(name="Bad", roles=("only_one",), elements=())

    def test_invalid_sender_role_raises(self):
        with pytest.raises(ValueError, match="sender 'unknown' not in protocol roles"):
            Protocol(
                name="Bad",
                roles=("a", "b"),
                elements=(
                    ProtocolStep(
                        sender="unknown",
                        receiver="a",
                        message_kind=MessageKind.TASK_REQUEST,
                    ),
                ),
            )

    def test_invalid_receiver_role_raises(self):
        with pytest.raises(ValueError, match="receiver 'unknown' not in protocol roles"):
            Protocol(
                name="Bad",
                roles=("a", "b"),
                elements=(
                    ProtocolStep(
                        sender="a",
                        receiver="unknown",
                        message_kind=MessageKind.TASK_REQUEST,
                    ),
                ),
            )

    def test_invalid_role_inside_choice_raises(self):
        """Roles inside ProtocolChoice branches are also validated."""
        valid_step = ProtocolStep(
            sender="a",
            receiver="b",
            message_kind=MessageKind.TASK_REQUEST,
        )
        bad_step = ProtocolStep(
            sender="ghost",
            receiver="b",
            message_kind=MessageKind.TASK_RESULT,
        )
        with pytest.raises(ValueError, match="sender 'ghost' not in protocol roles"):
            Protocol(
                name="BadChoice",
                roles=("a", "b"),
                elements=(
                    valid_step,
                    ProtocolChoice(
                        decider="a",
                        branches={"branch1": (bad_step,)},
                    ),
                ),
            )

    def test_max_repetitions_default(self):
        proto = Protocol(name="SimpleProto", roles=("a", "b"), elements=())
        assert proto.max_repetitions == 1

    def test_custom_max_repetitions(self):
        proto = Protocol(name="P", roles=("a", "b"), elements=(), max_repetitions=5)
        assert proto.max_repetitions == 5

    def test_frozen_immutable(self):
        proto = Protocol(name="P", roles=("a", "b"), elements=())
        with pytest.raises(Exception):
            proto.name = "changed"  # type: ignore[misc]

    def test_description_optional(self):
        proto = Protocol(name="P", roles=("a", "b"), elements=())
        assert proto.description == ""
