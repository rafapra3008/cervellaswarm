# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for new message dataclasses in cervellaswarm_lingua_universale.types.

Covers: DirectMessage, Broadcast, ShutdownRequest, ShutdownAck, ContextInject.
Includes valid creation, validation errors, immutability, KIND field, default
values, and field access.
"""

import pytest

from cervellaswarm_lingua_universale.types import (
    Broadcast,
    ContextInject,
    DirectMessage,
    MessageKind,
    ShutdownAck,
    ShutdownRequest,
)


# ── DirectMessage ─────────────────────────────────────────────────────────────


class TestDirectMessage:
    def test_valid_creation(self):
        msg = DirectMessage(
            sender_role="backend",
            content="Auth module ready for review",
            thread_id="thread-42",
        )
        assert msg.sender_role == "backend"
        assert msg.content == "Auth module ready for review"
        assert msg.thread_id == "thread-42"

    def test_default_thread_id_is_empty(self):
        msg = DirectMessage(sender_role="backend", content="ping")
        assert msg.thread_id == ""

    def test_empty_sender_role_raises(self):
        with pytest.raises(ValueError, match="sender_role cannot be empty"):
            DirectMessage(sender_role="", content="hello")

    def test_empty_content_raises(self):
        with pytest.raises(ValueError, match="content cannot be empty"):
            DirectMessage(sender_role="backend", content="")

    def test_kind_is_dm(self):
        msg = DirectMessage(sender_role="backend", content="ping")
        assert msg.KIND == MessageKind.DM

    def test_frozen_immutable(self):
        msg = DirectMessage(sender_role="backend", content="ping")
        with pytest.raises(Exception):
            msg.sender_role = "changed"  # type: ignore[misc]

    def test_frozen_immutable_content(self):
        msg = DirectMessage(sender_role="backend", content="ping")
        with pytest.raises(Exception):
            msg.content = "changed"  # type: ignore[misc]

    def test_field_access(self):
        msg = DirectMessage(
            sender_role="tester",
            content="All tests pass",
            thread_id="T-review",
        )
        assert msg.sender_role == "tester"
        assert msg.content == "All tests pass"
        assert msg.thread_id == "T-review"
        assert msg.KIND == MessageKind.DM


# ── Broadcast ─────────────────────────────────────────────────────────────────


class TestBroadcast:
    def test_valid_creation_default_priority(self):
        msg = Broadcast(
            sender_role="regina",
            content="Sessione 388 avviata",
        )
        assert msg.sender_role == "regina"
        assert msg.content == "Sessione 388 avviata"
        assert msg.priority == "normal"

    def test_valid_urgent_priority(self):
        msg = Broadcast(
            sender_role="regina",
            content="Deploy imminent",
            priority="urgent",
        )
        assert msg.priority == "urgent"

    def test_valid_critical_priority(self):
        msg = Broadcast(
            sender_role="guardiana-qualita",
            content="Critical bug found",
            priority="critical",
        )
        assert msg.priority == "critical"

    def test_empty_sender_role_raises(self):
        with pytest.raises(ValueError, match="sender_role cannot be empty"):
            Broadcast(sender_role="", content="hello")

    def test_empty_content_raises(self):
        with pytest.raises(ValueError, match="content cannot be empty"):
            Broadcast(sender_role="regina", content="")

    def test_invalid_priority_raises(self):
        with pytest.raises(ValueError, match="priority must be normal/urgent/critical"):
            Broadcast(sender_role="regina", content="msg", priority="low")

    def test_invalid_priority_shows_value(self):
        with pytest.raises(ValueError, match="'high'"):
            Broadcast(sender_role="regina", content="msg", priority="high")

    def test_kind_is_broadcast(self):
        msg = Broadcast(sender_role="regina", content="ping")
        assert msg.KIND == MessageKind.BROADCAST

    def test_frozen_immutable(self):
        msg = Broadcast(sender_role="regina", content="ping")
        with pytest.raises(Exception):
            msg.content = "changed"  # type: ignore[misc]

    def test_field_access(self):
        msg = Broadcast(
            sender_role="architect",
            content="Plan approved",
            priority="urgent",
        )
        assert msg.sender_role == "architect"
        assert msg.content == "Plan approved"
        assert msg.priority == "urgent"
        assert msg.KIND == MessageKind.BROADCAST


# ── ShutdownRequest ───────────────────────────────────────────────────────────


class TestShutdownRequest:
    def test_valid_creation_with_reason(self):
        msg = ShutdownRequest(
            target_role="backend",
            reason="Session ending",
        )
        assert msg.target_role == "backend"
        assert msg.reason == "Session ending"

    def test_valid_creation_without_reason(self):
        msg = ShutdownRequest(target_role="tester")
        assert msg.target_role == "tester"
        assert msg.reason == ""

    def test_default_reason_is_empty(self):
        msg = ShutdownRequest(target_role="frontend")
        assert msg.reason == ""

    def test_empty_target_role_raises(self):
        with pytest.raises(ValueError, match="target_role cannot be empty"):
            ShutdownRequest(target_role="")

    def test_kind_is_shutdown_request(self):
        msg = ShutdownRequest(target_role="backend")
        assert msg.KIND == MessageKind.SHUTDOWN_REQUEST

    def test_frozen_immutable(self):
        msg = ShutdownRequest(target_role="backend")
        with pytest.raises(Exception):
            msg.target_role = "changed"  # type: ignore[misc]

    def test_field_access(self):
        msg = ShutdownRequest(
            target_role="devops",
            reason="Maintenance window",
        )
        assert msg.target_role == "devops"
        assert msg.reason == "Maintenance window"
        assert msg.KIND == MessageKind.SHUTDOWN_REQUEST


# ── ShutdownAck ───────────────────────────────────────────────────────────────


class TestShutdownAck:
    def test_valid_creation_default_acknowledged(self):
        msg = ShutdownAck(target_role="backend")
        assert msg.target_role == "backend"
        assert msg.acknowledged is True

    def test_valid_creation_explicit_acknowledged(self):
        msg = ShutdownAck(target_role="tester", acknowledged=True)
        assert msg.acknowledged is True

    def test_valid_creation_not_acknowledged(self):
        msg = ShutdownAck(target_role="tester", acknowledged=False)
        assert msg.acknowledged is False

    def test_empty_target_role_raises(self):
        with pytest.raises(ValueError, match="target_role cannot be empty"):
            ShutdownAck(target_role="")

    def test_kind_is_shutdown_ack(self):
        msg = ShutdownAck(target_role="backend")
        assert msg.KIND == MessageKind.SHUTDOWN_ACK

    def test_frozen_immutable(self):
        msg = ShutdownAck(target_role="backend")
        with pytest.raises(Exception):
            msg.target_role = "changed"  # type: ignore[misc]

    def test_frozen_immutable_acknowledged(self):
        msg = ShutdownAck(target_role="backend")
        with pytest.raises(Exception):
            msg.acknowledged = False  # type: ignore[misc]

    def test_field_access(self):
        msg = ShutdownAck(target_role="researcher", acknowledged=True)
        assert msg.target_role == "researcher"
        assert msg.acknowledged is True
        assert msg.KIND == MessageKind.SHUTDOWN_ACK


# ── ContextInject ─────────────────────────────────────────────────────────────


class TestContextInject:
    def test_valid_creation_with_source_file(self):
        msg = ContextInject(
            context_type="PROMPT_RIPRESA",
            content="# Sessione 388\nStato: ...",
            source_file=".sncp/progetti/cervellaswarm/PROMPT_RIPRESA_cervellaswarm.md",
        )
        assert msg.context_type == "PROMPT_RIPRESA"
        assert msg.content == "# Sessione 388\nStato: ..."
        assert msg.source_file.endswith("PROMPT_RIPRESA_cervellaswarm.md")

    def test_valid_creation_without_source_file(self):
        msg = ContextInject(
            context_type="FATOS",
            content="## Fatos Confirmados\n...",
        )
        assert msg.context_type == "FATOS"
        assert msg.source_file == ""

    def test_default_source_file_is_empty(self):
        msg = ContextInject(context_type="MEMORY", content="key facts")
        assert msg.source_file == ""

    def test_empty_context_type_raises(self):
        with pytest.raises(ValueError, match="context_type cannot be empty"):
            ContextInject(context_type="", content="some content")

    def test_empty_content_raises(self):
        with pytest.raises(ValueError, match="content cannot be empty"):
            ContextInject(context_type="PROMPT_RIPRESA", content="")

    def test_kind_is_context_inject(self):
        msg = ContextInject(context_type="FATOS", content="facts")
        assert msg.KIND == MessageKind.CONTEXT_INJECT

    def test_frozen_immutable(self):
        msg = ContextInject(context_type="FATOS", content="facts")
        with pytest.raises(Exception):
            msg.content = "changed"  # type: ignore[misc]

    def test_frozen_immutable_context_type(self):
        msg = ContextInject(context_type="FATOS", content="facts")
        with pytest.raises(Exception):
            msg.context_type = "changed"  # type: ignore[misc]

    def test_field_access(self):
        msg = ContextInject(
            context_type="NORD",
            content="## NORD\n...",
            source_file="NORD.md",
        )
        assert msg.context_type == "NORD"
        assert msg.content == "## NORD\n..."
        assert msg.source_file == "NORD.md"
        assert msg.KIND == MessageKind.CONTEXT_INJECT
