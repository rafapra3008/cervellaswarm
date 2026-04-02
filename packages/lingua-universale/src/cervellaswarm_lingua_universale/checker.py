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

from .monitor import (
    BranchChosen,
    MessageSent,
    ProtocolMonitor,
    RepetitionStarted,
    SessionEnded,
    SessionStarted,
    ViolationOccurred,
)
from .protocols import Protocol, ProtocolChoice, ProtocolElement, ProtocolStep
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


@dataclass(frozen=True)
class MessageRecord:
    """A recorded message in the session log.

    ``step_index`` refers to the top-level ``protocol.elements`` position.
    Inside nested branches it stays at the outer ``ProtocolChoice`` index;
    use ``SessionChecker.summary()['branch_path']`` for the full location.
    """

    timestamp: float
    sender: str
    receiver: str
    kind: MessageKind
    step_index: int


@dataclass(frozen=True)
class ChoiceFrame:
    """A single frame in the choice navigation stack (LU 1.2).

    Each frame represents an active branch selection.  Nested choices
    push additional frames; when a branch is exhausted the frame is
    popped and the parent resumes from ``parent_index + 1``.
    """

    choice: ProtocolChoice
    branch_name: str
    parent_index: int  # index in parent element list where this choice sits

    # Mutable step counter stored separately in SessionState._frame_positions


@dataclass
class SessionState:
    """Current state of a protocol session.

    Uses a *choice stack* (LU 1.2) to support arbitrarily nested
    ``ProtocolChoice`` blocks at runtime.  For flat protocols the
    stack is always empty and behaviour is identical to LU 1.1.
    """

    session_id: str
    protocol: Protocol
    step_index: int = 0
    choice_stack: list[ChoiceFrame] = field(default_factory=list)
    _frame_positions: list[int] = field(default_factory=list)
    completed: bool = False
    repetition_count: int = 0
    started_at: float = field(default_factory=time.time)
    started_at_mono: float = field(default_factory=time.monotonic)
    completed_at: Optional[float] = None
    completed_at_mono: Optional[float] = None
    log: list[MessageRecord] = field(default_factory=list)

    # -- backward-compat properties ------------------------------------------

    @property
    def branch(self) -> Optional[str]:
        """Name of the current branch (top of the choice stack)."""
        return self.choice_stack[-1].branch_name if self.choice_stack else None

    @property
    def branch_step_index(self) -> int:
        """Step index within the current branch."""
        return self._frame_positions[-1] if self._frame_positions else 0

    # -- stack navigation helpers --------------------------------------------

    def _current_elements(self) -> tuple[ProtocolElement, ...]:
        """Elements of the current context (top-level or innermost branch)."""
        if not self.choice_stack:
            return self.protocol.elements
        frame = self.choice_stack[-1]
        return frame.choice.branches[frame.branch_name]

    def _current_index(self) -> int:
        """Position within ``_current_elements()``."""
        if not self.choice_stack:
            return self.step_index
        return self._frame_positions[-1]

    def _advance_current(self) -> None:
        """Increment the position in the current context by one."""
        if not self.choice_stack:
            self.step_index += 1
        else:
            self._frame_positions[-1] += 1

    # -- core state logic ----------------------------------------------------

    def peek_next_step(self) -> Optional[ProtocolStep]:
        """Return the expected next step WITHOUT mutating state.

        Returns ``None`` if the protocol is complete or at a choice point.
        Handles multi-level backtrack: when the innermost branch is
        exhausted it looks in the parent context, and so on.
        """
        if self.completed:
            return None
        return self._peek_at(
            self._current_elements(),
            self._current_index(),
            len(self.choice_stack),
        )

    def _peek_at(
        self,
        elements: tuple[ProtocolElement, ...],
        idx: int,
        depth: int,
    ) -> Optional[ProtocolStep]:
        """Recursively peek through stack levels."""
        if idx < len(elements):
            elem = elements[idx]
            if isinstance(elem, ProtocolStep):
                return elem
            # ProtocolChoice -- caller must choose_branch
            return None

        # Elements exhausted at this level -- try parent
        if depth <= 0:
            return None  # top-level exhausted
        parent_depth = depth - 1
        frame = self.choice_stack[parent_depth]
        if parent_depth == 0:
            parent_elements = self.protocol.elements
        else:
            pf = self.choice_stack[parent_depth - 1]
            parent_elements = pf.choice.branches[pf.branch_name]
        return self._peek_at(parent_elements, frame.parent_index + 1, parent_depth)

    def _pop_exhausted_frames(self) -> None:
        """Pop frames whose branch is fully consumed and advance parents."""
        while self.choice_stack:
            frame = self.choice_stack[-1]
            branch_elems = frame.choice.branches[frame.branch_name]
            if self._frame_positions[-1] < len(branch_elems):
                break  # frame still active
            # Frame exhausted -- pop and advance parent
            self.choice_stack.pop()
            self._frame_positions.pop()
            if self.choice_stack:
                self._frame_positions[-1] = frame.parent_index + 1
            else:
                self.step_index = frame.parent_index + 1

    def _check_completion_or_repeat(self) -> None:
        """Check if protocol is complete or should reset for next repetition."""
        self._pop_exhausted_frames()
        if self.choice_stack:
            return  # still inside a branch
        if self.step_index >= len(self.protocol.elements):
            self.repetition_count += 1
            if self.repetition_count >= self.protocol.max_repetitions:
                self.completed = True
                self.completed_at = time.time()
                self.completed_at_mono = time.monotonic()
            else:
                self.step_index = 0
                self.choice_stack.clear()
                self._frame_positions.clear()

    def advance_past_exhausted_branch(self) -> None:
        """Advance state when current branch is exhausted. Called by checker."""
        self._pop_exhausted_frames()
        self._check_completion_or_repeat()

    @property
    def at_choice(self) -> Optional[ProtocolChoice]:
        """Return the ProtocolChoice if we're at a branching point."""
        if self.completed:
            return None
        elements = self._current_elements()
        idx = self._current_index()
        if idx >= len(elements):
            return None
        elem = elements[idx]
        if isinstance(elem, ProtocolChoice):
            return elem
        return None


class SessionChecker:
    """Runtime checker for a single protocol session.

    Tracks state and validates each message against the protocol.

    Supports arbitrarily nested ``ProtocolChoice`` blocks (LU 1.2)
    via a stack-based approach: each ``choose_branch`` call pushes a
    ``ChoiceFrame``; when the branch is exhausted the frame is popped
    and the parent context resumes automatically.

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
        monitor: Optional[ProtocolMonitor] = None,
    ) -> None:
        self._state = SessionState(
            session_id=session_id or f"{protocol.name}_{id(self)}",
            protocol=protocol,
        )
        # role_bindings maps protocol roles to actual agent names
        # e.g., {"worker": "cervella-backend", "guardiana": "cervella-guardiana-qualita"}
        self._role_bindings: dict[str, str] = dict(role_bindings) if role_bindings else {}
        self._monitor = monitor
        # Mark complete immediately if protocol has no elements
        self._state._check_completion_or_repeat()
        # Emit session lifecycle events
        if self._monitor is not None:
            self._monitor.emit(SessionStarted(
                session_id=self._state.session_id,
                protocol_name=protocol.name,
                timestamp=time.time(),
                roles=protocol.roles,
            ))
            if self._state.completed:
                self._monitor.emit(SessionEnded(
                    session_id=self._state.session_id,
                    protocol_name=protocol.name,
                    timestamp=time.time(),
                    total_messages=0,
                    duration_ms=0.0,
                    repetitions=self._state.repetition_count,
                ))

    @property
    def session_id(self) -> str:
        """Return the unique identifier for this session."""
        return self._state.session_id

    @property
    def protocol_name(self) -> str:
        """Return the name of the protocol being checked."""
        return self._state.protocol.name

    @property
    def is_complete(self) -> bool:
        """Return True if all protocol steps have been satisfied."""
        return self._state.completed

    @property
    def step_index(self) -> int:
        """Return the zero-based index of the current protocol step."""
        return self._state.step_index

    @property
    def log(self) -> list[MessageRecord]:
        """Return a copy of all recorded messages in this session."""
        return list(self._state.log)

    @property
    def current_branch(self) -> Optional[str]:
        """Return the active choice branch name, or None if not in a choice."""
        return self._state.branch

    def choose_branch(self, branch_name: str) -> None:
        """Choose a branch at a ProtocolChoice point."""
        choice = self._state.at_choice
        if choice is None:
            self._emit_violation(
                step=self._state.step_index,
                expected="at a choice point",
                got=f"not at a choice point (step_index={self._state.step_index})",
            )
            raise ProtocolViolation(
                protocol=self.protocol_name,
                session_id=self.session_id,
                expected="at a choice point",
                got=f"not at a choice point (step_index={self._state.step_index})",
                step=self._state.step_index,
            )
        if branch_name not in choice.branches:
            valid = list(choice.branches.keys())
            self._emit_violation(
                step=self._state.step_index,
                expected=f"branch in {valid}",
                got=branch_name,
            )
            raise ProtocolViolation(
                protocol=self.protocol_name,
                session_id=self.session_id,
                expected=f"branch in {valid}",
                got=branch_name,
                step=self._state.step_index,
            )
        parent_idx = self._state._current_index()
        self._state.choice_stack.append(
            ChoiceFrame(choice=choice, branch_name=branch_name, parent_index=parent_idx),
        )
        self._state._frame_positions.append(0)
        if self._monitor is not None:
            self._monitor.emit(BranchChosen(
                session_id=self.session_id,
                protocol_name=self.protocol_name,
                timestamp=time.time(),
                step_index=self._state.step_index,
                branch_name=branch_name,
                auto_detected=False,
            ))

    def send(self, sender: str, receiver: str, msg: SwarmMessage) -> None:
        """Record and validate a message in the session.

        Raises ProtocolViolation if the message doesn't match expectations.
        Raises SessionComplete if the protocol is already done.
        """
        _t0 = time.monotonic()

        if self._state.completed:
            raise SessionComplete(self.protocol_name, self.session_id)

        kind = message_kind(msg)
        self._auto_detect_branch(kind, sender, receiver)
        self._validate_next_step(sender, receiver, kind)
        record, current_branch = self._record_and_advance(sender, receiver, kind)
        self._emit_post_send_events(record, current_branch, _t0)

    def _auto_detect_branch(
        self, kind: MessageKind, sender: str, receiver: str,
    ) -> None:
        """Auto-detect and select branch at choice points."""
        choice = self._state.at_choice
        if choice is not None:
            matched_branch = self._detect_branch(choice, sender, receiver, kind)
            if matched_branch is not None:
                parent_idx = self._state._current_index()
                self._state.choice_stack.append(
                    ChoiceFrame(choice=choice, branch_name=matched_branch, parent_index=parent_idx),
                )
                self._state._frame_positions.append(0)
                if self._monitor is not None:
                    self._monitor.emit(BranchChosen(
                        session_id=self.session_id,
                        protocol_name=self.protocol_name,
                        timestamp=time.time(),
                        step_index=self._state.step_index,
                        branch_name=matched_branch,
                        auto_detected=True,
                    ))

        self._state.advance_past_exhausted_branch()
        if self._state.completed:
            raise SessionComplete(self.protocol_name, self.session_id)

    def _validate_next_step(
        self, sender: str, receiver: str, kind: MessageKind,
    ) -> None:
        """Validate that the next expected step matches sender/receiver/kind."""
        expected = self._state.peek_next_step()
        if expected is None:
            if self._state.completed:
                raise SessionComplete(self.protocol_name, self.session_id)
            _expected = "branch selection (call choose_branch first)"
            _got = f"{sender}->{receiver}:{kind.value}"
            self._emit_violation(
                step=self._state.step_index, expected=_expected, got=_got,
            )
            raise ProtocolViolation(
                protocol=self.protocol_name,
                session_id=self.session_id,
                expected=_expected,
                got=_got,
                step=self._state.step_index,
            )

        resolved_sender = self._resolve_role(sender)
        resolved_receiver = self._resolve_role(receiver)

        for field, resolved, exp_val in [
            ("sender", resolved_sender, expected.sender),
            ("receiver", resolved_receiver, expected.receiver),
        ]:
            if resolved != exp_val:
                _expected = f"{field}={exp_val}"
                _got = f"{field}={resolved} (raw: {sender if field == 'sender' else receiver})"
                self._emit_violation(
                    step=self._state.step_index, expected=_expected, got=_got,
                )
                raise ProtocolViolation(
                    protocol=self.protocol_name,
                    session_id=self.session_id,
                    expected=_expected,
                    got=_got,
                    step=self._state.step_index,
                )

        if kind != expected.message_kind:
            _expected = f"message={expected.message_kind.value}"
            _got = f"message={kind.value}"
            self._emit_violation(
                step=self._state.step_index, expected=_expected, got=_got,
            )
            raise ProtocolViolation(
                protocol=self.protocol_name,
                session_id=self.session_id,
                expected=_expected,
                got=_got,
                step=self._state.step_index,
            )

    def _record_and_advance(
        self, sender: str, receiver: str, kind: MessageKind,
    ) -> tuple[MessageRecord, str | None]:
        """Record the message and advance protocol state."""
        record = MessageRecord(
            timestamp=time.time(),
            sender=sender,
            receiver=receiver,
            kind=kind,
            step_index=self._state.step_index,
        )
        self._state.log.append(record)

        current_branch = self._state.branch

        self._state._advance_current()
        self._state._pop_exhausted_frames()

        return record, current_branch

    def _emit_post_send_events(
        self,
        record: MessageRecord,
        current_branch: str | None,
        t0: float,
    ) -> None:
        """Emit MessageSent event and check completion/repetition."""
        if self._monitor is not None:
            _duration_ms = (time.monotonic() - t0) * 1000.0
            self._monitor.emit(MessageSent(
                session_id=self.session_id,
                protocol_name=self.protocol_name,
                timestamp=time.time(),
                step_index=record.step_index,
                sender=record.sender,
                receiver=record.receiver,
                message_kind=record.kind,
                duration_ms=_duration_ms,
                branch=current_branch,
            ))

        prev_rep = self._state.repetition_count
        self._state._check_completion_or_repeat()

        if self._monitor is not None:
            if self._state.completed:
                if self._state.completed_at is None or self._state.completed_at_mono is None:
                    raise RuntimeError("Session marked completed but timestamps are None")
                self._monitor.emit(SessionEnded(
                    session_id=self.session_id,
                    protocol_name=self.protocol_name,
                    timestamp=self._state.completed_at,
                    total_messages=len(self._state.log),
                    duration_ms=(
                        self._state.completed_at_mono
                        - self._state.started_at_mono
                    ) * 1000.0,
                    repetitions=self._state.repetition_count,
                ))
            elif self._state.repetition_count > prev_rep:
                self._monitor.emit(RepetitionStarted(
                    session_id=self.session_id,
                    protocol_name=self.protocol_name,
                    timestamp=time.time(),
                    repetition_number=self._state.repetition_count,
                ))

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
            if steps and isinstance(steps[0], ProtocolStep):
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

    def _emit_violation(
        self, *, step: int, expected: str, got: str,
    ) -> None:
        """Emit a ViolationOccurred event if monitor is attached."""
        if self._monitor is not None:
            self._monitor.emit(ViolationOccurred(
                session_id=self.session_id,
                protocol_name=self.protocol_name,
                timestamp=time.time(),
                step_index=step,
                expected=expected,
                got=got,
            ))

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
            "choice_depth": len(self._state.choice_stack),
            "branch_path": [f.branch_name for f in self._state.choice_stack],
        }
