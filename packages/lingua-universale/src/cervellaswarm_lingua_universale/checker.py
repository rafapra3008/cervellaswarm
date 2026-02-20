# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Runtime session type checker for CervellaSwarm protocols.

The SessionChecker tracks the state of a protocol session and
validates that each message follows the expected sequence.

This is the RUNTIME ENFORCEMENT of session types.
No more "the protocol says X but the agent did Y."
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Optional

from .protocols import Protocol, ProtocolChoice, ProtocolStep
from .types import MessageKind, SwarmMessage, message_kind


class ProtocolViolation(Exception):
    """Raised when a message violates the session protocol."""

    def __init__(
        self,
        protocol: str,
        session_id: str,
        expected: str,
        got: str,
        step: int,
    ) -> None:
        self.protocol = protocol
        self.session_id = session_id
        self.expected = expected
        self.got = got
        self.step = step
        super().__init__(
            f"Protocol '{protocol}' violation in session '{session_id}' "
            f"at step {step}: expected {expected}, got {got}"
        )


class SessionComplete(Exception):
    """Raised when trying to send a message after protocol completion."""

    def __init__(self, protocol: str, session_id: str) -> None:
        self.protocol = protocol
        self.session_id = session_id
        super().__init__(
            f"Protocol '{protocol}' session '{session_id}' is already complete"
        )


@dataclass
class MessageRecord:
    """A recorded message in the session log."""

    timestamp: float
    sender: str
    receiver: str
    kind: MessageKind
    step_index: int


@dataclass
class SessionState:
    """Current state of a protocol session."""

    session_id: str
    protocol: Protocol
    step_index: int = 0
    branch: Optional[str] = None
    branch_step_index: int = 0
    completed: bool = False
    repetition_count: int = 0
    started_at: float = field(default_factory=time.time)
    completed_at: Optional[float] = None
    log: list[MessageRecord] = field(default_factory=list)

    def peek_next_step(self) -> Optional[ProtocolStep]:
        """Return the expected next step WITHOUT mutating state.

        Returns None if protocol is complete or at a choice point.
        """
        if self.completed:
            return None

        elements = self.protocol.elements

        # If we're in a branch, look up current branch step
        # using step_index to find the CORRECT ProtocolChoice
        if self.branch is not None:
            if self.step_index >= len(elements):
                return None
            elem = elements[self.step_index]
            if isinstance(elem, ProtocolChoice):
                branch_steps = elem.branches.get(self.branch, ())
                if self.branch_step_index < len(branch_steps):
                    return branch_steps[self.branch_step_index]
                # Branch exhausted - next element is after the choice
                next_idx = self.step_index + 1
                if next_idx >= len(elements):
                    return None  # protocol will complete
                next_elem = elements[next_idx]
                if isinstance(next_elem, ProtocolStep):
                    return next_elem
                return None
            return None

        if self.step_index >= len(elements):
            return None  # protocol complete

        elem = elements[self.step_index]
        if isinstance(elem, ProtocolStep):
            return elem
        # ProtocolChoice - return None to signal "choice needed"
        return None

    def _check_completion_or_repeat(self) -> None:
        """Check if protocol is complete or should reset for next repetition."""
        if self.step_index >= len(self.protocol.elements):
            self.repetition_count += 1
            if self.repetition_count >= self.protocol.max_repetitions:
                self.completed = True
                self.completed_at = time.time()
            else:
                self.step_index = 0
                self.branch = None
                self.branch_step_index = 0

    def advance_past_exhausted_branch(self) -> None:
        """Advance state when current branch is exhausted. Called by checker."""
        if self.branch is not None:
            if self.step_index < len(self.protocol.elements):
                elem = self.protocol.elements[self.step_index]
                if isinstance(elem, ProtocolChoice):
                    branch_steps = elem.branches.get(self.branch, ())
                    if self.branch_step_index >= len(branch_steps):
                        self.branch = None
                        self.branch_step_index = 0
                        self.step_index += 1
        self._check_completion_or_repeat()

    @property
    def at_choice(self) -> Optional[ProtocolChoice]:
        """Return the ProtocolChoice if we're at a branching point."""
        if self.completed or self.branch is not None:
            return None
        if self.step_index >= len(self.protocol.elements):
            return None
        elem = self.protocol.elements[self.step_index]
        if isinstance(elem, ProtocolChoice):
            return elem
        return None


class SessionChecker:
    """Runtime checker for a single protocol session.

    Tracks state and validates each message against the protocol.

    Usage:
        checker = SessionChecker(DelegateTask, session_id="S001")
        checker.send("regina", "worker", task_request)
        checker.send("worker", "regina", task_result)
        checker.send("regina", "guardiana", audit_request)
        checker.send("guardiana", "regina", audit_verdict)
        assert checker.is_complete
    """

    def __init__(
        self,
        protocol: Protocol,
        session_id: str = "",
        role_bindings: Optional[dict[str, str]] = None,
    ) -> None:
        self._state = SessionState(
            session_id=session_id or f"{protocol.name}_{id(self)}",
            protocol=protocol,
        )
        # role_bindings maps protocol roles to actual agent names
        # e.g., {"worker": "cervella-backend", "guardiana": "cervella-guardiana-qualita"}
        self._role_bindings: dict[str, str] = role_bindings or {}
        # Mark complete immediately if protocol has no elements
        self._state._check_completion_or_repeat()

    @property
    def session_id(self) -> str:
        return self._state.session_id

    @property
    def protocol_name(self) -> str:
        return self._state.protocol.name

    @property
    def is_complete(self) -> bool:
        return self._state.completed

    @property
    def step_index(self) -> int:
        return self._state.step_index

    @property
    def log(self) -> list[MessageRecord]:
        return list(self._state.log)

    @property
    def current_branch(self) -> Optional[str]:
        return self._state.branch

    def choose_branch(self, branch_name: str) -> None:
        """Choose a branch at a ProtocolChoice point."""
        choice = self._state.at_choice
        if choice is None:
            raise ProtocolViolation(
                protocol=self.protocol_name,
                session_id=self.session_id,
                expected="not at a choice point",
                got=f"choose_branch('{branch_name}')",
                step=self._state.step_index,
            )
        if branch_name not in choice.branches:
            valid = list(choice.branches.keys())
            raise ProtocolViolation(
                protocol=self.protocol_name,
                session_id=self.session_id,
                expected=f"branch in {valid}",
                got=branch_name,
                step=self._state.step_index,
            )
        self._state.branch = branch_name
        self._state.branch_step_index = 0

    def send(self, sender: str, receiver: str, msg: SwarmMessage) -> None:
        """Record and validate a message in the session.

        Raises ProtocolViolation if the message doesn't match expectations.
        Raises SessionComplete if the protocol is already done.
        """
        if self._state.completed:
            raise SessionComplete(self.protocol_name, self.session_id)

        kind = message_kind(msg)

        # If at a choice point, auto-detect branch from message kind
        choice = self._state.at_choice
        if choice is not None and self._state.branch is None:
            matched_branch = self._detect_branch(choice, sender, receiver, kind)
            if matched_branch is not None:
                self._state.branch = matched_branch
                self._state.branch_step_index = 0

        # Advance past exhausted branch if needed (explicit mutation)
        self._state.advance_past_exhausted_branch()
        if self._state.completed:
            raise SessionComplete(self.protocol_name, self.session_id)

        expected = self._state.peek_next_step()
        if expected is None:
            if self._state.completed:
                raise SessionComplete(self.protocol_name, self.session_id)
            # Still at an unresolved choice
            raise ProtocolViolation(
                protocol=self.protocol_name,
                session_id=self.session_id,
                expected="branch selection (call choose_branch first)",
                got=f"{sender}->{receiver}:{kind.value}",
                step=self._state.step_index,
            )

        # Validate sender role
        resolved_sender = self._resolve_role(sender)
        resolved_receiver = self._resolve_role(receiver)

        if resolved_sender != expected.sender:
            raise ProtocolViolation(
                protocol=self.protocol_name,
                session_id=self.session_id,
                expected=f"sender={expected.sender}",
                got=f"sender={resolved_sender} (raw: {sender})",
                step=self._state.step_index,
            )

        if resolved_receiver != expected.receiver:
            raise ProtocolViolation(
                protocol=self.protocol_name,
                session_id=self.session_id,
                expected=f"receiver={expected.receiver}",
                got=f"receiver={resolved_receiver} (raw: {receiver})",
                step=self._state.step_index,
            )

        if kind != expected.message_kind:
            raise ProtocolViolation(
                protocol=self.protocol_name,
                session_id=self.session_id,
                expected=f"message={expected.message_kind.value}",
                got=f"message={kind.value}",
                step=self._state.step_index,
            )

        # Record the message
        record = MessageRecord(
            timestamp=time.time(),
            sender=sender,
            receiver=receiver,
            kind=kind,
            step_index=self._state.step_index,
        )
        self._state.log.append(record)

        # Advance state
        if self._state.branch is not None:
            self._state.branch_step_index += 1
            # Check if branch is exhausted using step_index (not iterating)
            elem = self._state.protocol.elements[self._state.step_index]
            if isinstance(elem, ProtocolChoice):
                branch_steps = elem.branches.get(self._state.branch, ())
                if self._state.branch_step_index >= len(branch_steps):
                    self._state.branch = None
                    self._state.branch_step_index = 0
                    self._state.step_index += 1
        else:
            self._state.step_index += 1

        self._state._check_completion_or_repeat()

    def _resolve_role(self, agent_name: str) -> str:
        """Resolve an agent name to a protocol role.

        If agent_name is already a protocol role, return it directly.
        Otherwise look up in role_bindings.
        """
        if agent_name in self._state.protocol.roles:
            return agent_name
        # Reverse lookup in bindings
        for role, bound_name in self._role_bindings.items():
            if bound_name == agent_name:
                return role
        return agent_name

    def _detect_branch(
        self,
        choice: ProtocolChoice,
        sender: str,
        receiver: str,
        kind: MessageKind,
    ) -> Optional[str]:
        """Auto-detect which branch matches the incoming message.

        Returns the branch name ONLY if exactly one branch matches.
        Returns None if zero or multiple branches match (ambiguous),
        requiring an explicit choose_branch() call.
        """
        resolved_sender = self._resolve_role(sender)
        resolved_receiver = self._resolve_role(receiver)

        matches: list[str] = []
        for branch_name, steps in choice.branches.items():
            if steps:
                first = steps[0]
                if (
                    first.sender == resolved_sender
                    and first.receiver == resolved_receiver
                    and first.message_kind == kind
                ):
                    matches.append(branch_name)
        if len(matches) == 1:
            return matches[0]
        # Ambiguous or no match - require explicit choose_branch
        return None

    def summary(self) -> dict:
        """Return a summary of the session state."""
        return {
            "session_id": self.session_id,
            "protocol": self.protocol_name,
            "step": self._state.step_index,
            "branch": self._state.branch,
            "completed": self._state.completed,
            "messages": len(self._state.log),
            "started_at": self._state.started_at,
            "completed_at": self._state.completed_at,
        }
