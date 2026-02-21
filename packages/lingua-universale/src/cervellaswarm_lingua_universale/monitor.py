# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Protocol monitoring and observability for CervellaSwarm sessions.

The ProtocolMonitor observes SessionChecker instances and emits events
for every significant protocol action: messages sent, branches chosen,
violations detected, sessions completed.

This is the EYES of the Lingua Universale.
No more silent protocols. Every action observed, measured, reported.

Research basis: 32 sources including OpenTelemetry GenAI conventions,
PyMOP runtime verification, OpenAI Agents SDK tracing, Google SRE
golden signals, AgentOps session analytics. See report:
.sncp/progetti/cervellaswarm/reports/RESEARCH_20260221_protocol_monitor.md
"""

from __future__ import annotations

import threading
import time
import warnings
from contextlib import contextmanager
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import (
    Iterator,
    Mapping,
    Optional,
    Protocol,
    runtime_checkable,
)

from .types import MessageKind


# ============================================================
# Event types (frozen dataclasses, immutable)
# ============================================================


@dataclass(frozen=True)
class MonitorEvent:
    """Base class for all monitor events.

    Every event carries session_id, protocol_name, and a wall-clock
    timestamp. Subclasses add event-specific fields.
    """

    session_id: str
    protocol_name: str
    timestamp: float  # time.time() wall clock


@dataclass(frozen=True)
class SessionStarted(MonitorEvent):
    """Emitted when a new SessionChecker is created."""

    roles: tuple[str, ...]


@dataclass(frozen=True)
class MessageSent(MonitorEvent):
    """Emitted after a message is successfully validated and recorded."""

    step_index: int
    sender: str
    receiver: str
    message_kind: MessageKind
    duration_ms: float  # time.monotonic() delta for the send() call
    branch: Optional[str] = None


@dataclass(frozen=True)
class BranchChosen(MonitorEvent):
    """Emitted when a protocol branch is selected."""

    step_index: int
    branch_name: str
    auto_detected: bool  # True if auto-detected, False if explicit choose_branch()


@dataclass(frozen=True)
class ViolationOccurred(MonitorEvent):
    """Emitted when a protocol violation is detected.

    Emitted BEFORE the ProtocolViolation exception is raised,
    so the monitor always sees the violation even if the caller
    catches the exception.
    """

    step_index: int
    expected: str
    got: str


@dataclass(frozen=True)
class SessionEnded(MonitorEvent):
    """Emitted when a session reaches completion."""

    total_messages: int
    duration_ms: float  # wall-clock duration from start to completion
    repetitions: int  # how many full protocol cycles completed


@dataclass(frozen=True)
class RepetitionStarted(MonitorEvent):
    """Emitted when a protocol resets for another repetition cycle."""

    repetition_number: int  # 1-based (first repeat after initial = 1)


# ============================================================
# Listener interface (structural typing)
# ============================================================


@runtime_checkable
class MonitorListener(Protocol):
    """Interface for protocol monitor listeners.

    Implement on_event() to receive monitor events.
    Listeners MUST be fast - avoid blocking I/O in on_event().
    If you need I/O, use a queue + worker thread internally.
    """

    def on_event(self, event: MonitorEvent) -> None: ...


# ============================================================
# Metrics
# ============================================================


@dataclass(frozen=True)
class MetricsSnapshot:
    """Immutable snapshot of protocol metrics at a point in time.

    All dict fields use MappingProxyType for true immutability.
    """

    sessions_started: int = 0
    sessions_completed: int = 0
    sessions_violated: int = 0
    total_messages: int = 0
    total_violations: int = 0
    total_branches: int = 0
    avg_session_duration_ms: float = 0.0
    avg_step_duration_ms: float = 0.0
    violation_by_step: Mapping[int, int] = field(
        default_factory=lambda: MappingProxyType({})
    )
    branch_frequency: Mapping[str, int] = field(
        default_factory=lambda: MappingProxyType({})
    )
    sessions_per_protocol: Mapping[str, int] = field(
        default_factory=lambda: MappingProxyType({})
    )


class MetricsCollector:
    """Thread-safe collector for protocol metrics.

    Automatically used by ProtocolMonitor. Tracks counters,
    durations, and distributions. Call snapshot() for an
    immutable view of current state.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._sessions_started = 0
        self._sessions_completed = 0
        self._violated_sessions: set[str] = set()
        self._total_messages = 0
        self._total_violations = 0
        self._total_branches = 0
        self._session_durations: list[float] = []
        self._step_durations: list[float] = []
        self._violation_by_step: dict[int, int] = {}
        self._branch_frequency: dict[str, int] = {}
        self._sessions_per_protocol: dict[str, int] = {}

    def record(self, event: MonitorEvent) -> None:
        """Record an event into metrics. Thread-safe."""
        with self._lock:
            if isinstance(event, SessionStarted):
                self._sessions_started += 1
                self._sessions_per_protocol[event.protocol_name] = (
                    self._sessions_per_protocol.get(event.protocol_name, 0)
                    + 1
                )
            elif isinstance(event, MessageSent):
                self._total_messages += 1
                self._step_durations.append(event.duration_ms)
            elif isinstance(event, BranchChosen):
                self._total_branches += 1
                self._branch_frequency[event.branch_name] = (
                    self._branch_frequency.get(event.branch_name, 0) + 1
                )
            elif isinstance(event, ViolationOccurred):
                self._total_violations += 1
                self._violated_sessions.add(event.session_id)
                self._violation_by_step[event.step_index] = (
                    self._violation_by_step.get(event.step_index, 0) + 1
                )
            elif isinstance(event, SessionEnded):
                self._sessions_completed += 1
                self._session_durations.append(event.duration_ms)

    def snapshot(self) -> MetricsSnapshot:
        """Return an immutable snapshot of current metrics."""
        with self._lock:
            avg_session = (
                sum(self._session_durations) / len(self._session_durations)
                if self._session_durations
                else 0.0
            )
            avg_step = (
                sum(self._step_durations) / len(self._step_durations)
                if self._step_durations
                else 0.0
            )
            return MetricsSnapshot(
                sessions_started=self._sessions_started,
                sessions_completed=self._sessions_completed,
                sessions_violated=len(self._violated_sessions),
                total_messages=self._total_messages,
                total_violations=self._total_violations,
                total_branches=self._total_branches,
                avg_session_duration_ms=avg_session,
                avg_step_duration_ms=avg_step,
                violation_by_step=MappingProxyType(
                    dict(self._violation_by_step)
                ),
                branch_frequency=MappingProxyType(
                    dict(self._branch_frequency)
                ),
                sessions_per_protocol=MappingProxyType(
                    dict(self._sessions_per_protocol)
                ),
            )

    def reset(self) -> None:
        """Reset all metrics to zero. Thread-safe."""
        with self._lock:
            self._sessions_started = 0
            self._sessions_completed = 0
            self._violated_sessions.clear()
            self._total_messages = 0
            self._total_violations = 0
            self._total_branches = 0
            self._session_durations.clear()
            self._step_durations.clear()
            self._violation_by_step.clear()
            self._branch_frequency.clear()
            self._sessions_per_protocol.clear()


# ============================================================
# Protocol Monitor (core)
# ============================================================


class ProtocolMonitor:
    """Event emitter and metrics aggregator for protocol sessions.

    Thread-safe. ZERO external dependencies (stdlib only).

    Usage::

        monitor = ProtocolMonitor()
        monitor.add_listener(my_listener)

        checker = SessionChecker(DelegateTask, monitor=monitor)
        checker.send("regina", "worker", task_request)
        # -> my_listener.on_event(MessageSent(...)) called

        snap = monitor.metrics
        print(snap.total_messages)  # 1
    """

    def __init__(self) -> None:
        self._listeners: list[MonitorListener] = []
        self._lock = threading.RLock()
        self._collector = MetricsCollector()

    def add_listener(self, listener: MonitorListener) -> None:
        """Register a listener to receive events. Thread-safe."""
        with self._lock:
            self._listeners.append(listener)

    def remove_listener(self, listener: MonitorListener) -> None:
        """Remove a listener. Thread-safe. No-op if not found."""
        with self._lock:
            self._listeners = [
                ll for ll in self._listeners if ll is not listener
            ]

    @contextmanager
    def listening(self, listener: MonitorListener) -> Iterator[None]:
        """Context manager for scoped listener registration.

        Usage::

            with monitor.listening(my_listener):
                checker.send(...)  # my_listener receives events
            # my_listener automatically removed
        """
        self.add_listener(listener)
        try:
            yield
        finally:
            self.remove_listener(listener)

    def emit(self, event: MonitorEvent) -> None:
        """Emit an event to all listeners. Thread-safe.

        Listener exceptions are caught and reported via warnings.warn().
        A failing listener NEVER breaks the protocol checker.
        """
        # Always record metrics (internal collector)
        self._collector.record(event)

        # Snapshot listeners under lock, notify outside lock
        with self._lock:
            listeners = list(self._listeners)

        for listener in listeners:
            try:
                listener.on_event(event)
            except Exception as exc:
                warnings.warn(
                    f"MonitorListener {listener!r} raised "
                    f"{type(exc).__name__}: {exc}",
                    RuntimeWarning,
                    stacklevel=2,
                )

    @property
    def metrics(self) -> MetricsSnapshot:
        """Return an immutable snapshot of current metrics."""
        return self._collector.snapshot()

    def reset_metrics(self) -> None:
        """Reset all metrics to zero. Thread-safe."""
        self._collector.reset()

    @property
    def listener_count(self) -> int:
        """Number of registered listeners."""
        with self._lock:
            return len(self._listeners)


# ============================================================
# Built-in listeners
# ============================================================


class LoggingListener:
    """Listener that logs events via Python's logging module.

    Usage::

        import logging
        logging.basicConfig(level=logging.DEBUG)
        monitor.add_listener(LoggingListener())
    """

    def __init__(self, logger_name: str = "cervellaswarm.monitor") -> None:
        import logging

        self._logger = logging.getLogger(logger_name)

    def on_event(self, event: MonitorEvent) -> None:
        if isinstance(event, ViolationOccurred):
            self._logger.warning(
                "VIOLATION %s[%s] step %d: expected %s, got %s",
                event.protocol_name,
                event.session_id,
                event.step_index,
                event.expected,
                event.got,
            )
        elif isinstance(event, SessionEnded):
            self._logger.info(
                "SESSION_END %s[%s]: %d msgs in %.1fms (%d reps)",
                event.protocol_name,
                event.session_id,
                event.total_messages,
                event.duration_ms,
                event.repetitions,
            )
        elif isinstance(event, SessionStarted):
            self._logger.info(
                "SESSION_START %s[%s] roles=%s",
                event.protocol_name,
                event.session_id,
                event.roles,
            )
        elif isinstance(event, MessageSent):
            self._logger.debug(
                "MESSAGE %s[%s] step %d: %s -> %s : %s (%.2fms%s)",
                event.protocol_name,
                event.session_id,
                event.step_index,
                event.sender,
                event.receiver,
                event.message_kind.value,
                event.duration_ms,
                f" branch={event.branch}" if event.branch else "",
            )
        elif isinstance(event, BranchChosen):
            self._logger.debug(
                "BRANCH %s[%s] step %d: '%s' (auto=%s)",
                event.protocol_name,
                event.session_id,
                event.step_index,
                event.branch_name,
                event.auto_detected,
            )
        elif isinstance(event, RepetitionStarted):
            self._logger.debug(
                "REPETITION %s[%s]: cycle %d",
                event.protocol_name,
                event.session_id,
                event.repetition_number,
            )


class EventCollector:
    """Simple listener that collects all events into a list.

    Useful for testing and debugging.

    Usage::

        collector = EventCollector()
        monitor.add_listener(collector)
        # ... protocol actions ...
        for event in collector.events:
            print(event)
    """

    def __init__(self) -> None:
        self.events: list[MonitorEvent] = []

    def on_event(self, event: MonitorEvent) -> None:
        self.events.append(event)

    def clear(self) -> None:
        self.events.clear()

    def of_type(self, event_type: type) -> list[MonitorEvent]:
        """Return events of a specific type."""
        return [e for e in self.events if isinstance(e, event_type)]
