# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for monitor.py - Event types, MonitorListener, ProtocolMonitor,
MetricsCollector, MetricsSnapshot, LoggingListener, EventCollector.

Coverage target: 96%+ on monitor.py
"""

import logging
import threading
import time
import warnings
from dataclasses import FrozenInstanceError
from types import MappingProxyType

import pytest

from cervellaswarm_lingua_universale.monitor import (
    BranchChosen,
    EventCollector,
    LoggingListener,
    MessageSent,
    MetricsCollector,
    MetricsSnapshot,
    MonitorEvent,
    MonitorListener,
    ProtocolMonitor,
    RepetitionStarted,
    SessionEnded,
    SessionStarted,
    ViolationOccurred,
)
from cervellaswarm_lingua_universale.types import MessageKind


# ============================================================
# Helpers / Factories
# ============================================================

def make_session_started(session_id="S001", protocol_name="TestProto"):
    return SessionStarted(
        session_id=session_id,
        protocol_name=protocol_name,
        timestamp=time.time(),
        roles=("regina", "worker"),
    )


def make_message_sent(session_id="S001", step_index=0, branch=None):
    return MessageSent(
        session_id=session_id,
        protocol_name="TestProto",
        timestamp=time.time(),
        step_index=step_index,
        sender="regina",
        receiver="worker",
        message_kind=MessageKind.TASK_REQUEST,
        duration_ms=1.5,
        branch=branch,
    )


def make_branch_chosen(session_id="S001", auto_detected=True):
    return BranchChosen(
        session_id=session_id,
        protocol_name="TestProto",
        timestamp=time.time(),
        step_index=2,
        branch_name="approve",
        auto_detected=auto_detected,
    )


def make_violation(session_id="S001", step_index=0):
    return ViolationOccurred(
        session_id=session_id,
        protocol_name="TestProto",
        timestamp=time.time(),
        step_index=step_index,
        expected="sender=regina",
        got="sender=worker",
    )


def make_session_ended(session_id="S001", total_messages=4, duration_ms=50.0, repetitions=1):
    return SessionEnded(
        session_id=session_id,
        protocol_name="TestProto",
        timestamp=time.time(),
        total_messages=total_messages,
        duration_ms=duration_ms,
        repetitions=repetitions,
    )


def make_repetition_started(session_id="S001", repetition_number=1):
    return RepetitionStarted(
        session_id=session_id,
        protocol_name="TestProto",
        timestamp=time.time(),
        repetition_number=repetition_number,
    )


# ============================================================
# 1. Event Types - Creation and Fields
# ============================================================

class TestMonitorEvent:
    def test_base_event_has_session_id_protocol_name_timestamp(self):
        ts = time.time()
        # MonitorEvent is a base class; use a concrete subclass
        ev = SessionStarted(
            session_id="S001",
            protocol_name="TestProto",
            timestamp=ts,
            roles=("regina", "worker"),
        )
        assert ev.session_id == "S001"
        assert ev.protocol_name == "TestProto"
        assert ev.timestamp == ts

    def test_session_started_has_roles(self):
        ev = make_session_started()
        assert ev.roles == ("regina", "worker")

    def test_message_sent_all_fields(self):
        ev = make_message_sent(step_index=3, branch="approve")
        assert ev.step_index == 3
        assert ev.sender == "regina"
        assert ev.receiver == "worker"
        assert ev.message_kind == MessageKind.TASK_REQUEST
        assert ev.duration_ms == 1.5
        assert ev.branch == "approve"

    def test_message_sent_branch_default_is_none(self):
        ev = make_message_sent()
        assert ev.branch is None

    def test_branch_chosen_fields(self):
        ev = make_branch_chosen(auto_detected=False)
        assert ev.step_index == 2
        assert ev.branch_name == "approve"
        assert ev.auto_detected is False

    def test_branch_chosen_auto_detected_true(self):
        ev = make_branch_chosen(auto_detected=True)
        assert ev.auto_detected is True

    def test_violation_occurred_fields(self):
        ev = make_violation(step_index=1)
        assert ev.step_index == 1
        assert ev.expected == "sender=regina"
        assert ev.got == "sender=worker"

    def test_session_ended_fields(self):
        ev = make_session_ended(total_messages=4, duration_ms=99.9, repetitions=2)
        assert ev.total_messages == 4
        assert ev.duration_ms == 99.9
        assert ev.repetitions == 2

    def test_repetition_started_fields(self):
        ev = make_repetition_started(repetition_number=2)
        assert ev.repetition_number == 2


# ============================================================
# 2. Event Types - Immutability (frozen dataclass)
# ============================================================

class TestEventImmutability:
    def test_session_started_is_frozen(self):
        ev = make_session_started()
        with pytest.raises(FrozenInstanceError):
            ev.session_id = "S999"  # type: ignore[misc]

    def test_message_sent_is_frozen(self):
        ev = make_message_sent()
        with pytest.raises(FrozenInstanceError):
            ev.step_index = 99  # type: ignore[misc]

    def test_branch_chosen_is_frozen(self):
        ev = make_branch_chosen()
        with pytest.raises(FrozenInstanceError):
            ev.branch_name = "reject"  # type: ignore[misc]

    def test_violation_occurred_is_frozen(self):
        ev = make_violation()
        with pytest.raises(FrozenInstanceError):
            ev.expected = "changed"  # type: ignore[misc]

    def test_session_ended_is_frozen(self):
        ev = make_session_ended()
        with pytest.raises(FrozenInstanceError):
            ev.total_messages = 999  # type: ignore[misc]

    def test_repetition_started_is_frozen(self):
        ev = make_repetition_started()
        with pytest.raises(FrozenInstanceError):
            ev.repetition_number = 99  # type: ignore[misc]


# ============================================================
# 3. Event Types - Inheritance
# ============================================================

class TestEventInheritance:
    def test_session_started_is_monitor_event(self):
        assert isinstance(make_session_started(), MonitorEvent)

    def test_message_sent_is_monitor_event(self):
        assert isinstance(make_message_sent(), MonitorEvent)

    def test_branch_chosen_is_monitor_event(self):
        assert isinstance(make_branch_chosen(), MonitorEvent)

    def test_violation_occurred_is_monitor_event(self):
        assert isinstance(make_violation(), MonitorEvent)

    def test_session_ended_is_monitor_event(self):
        assert isinstance(make_session_ended(), MonitorEvent)

    def test_repetition_started_is_monitor_event(self):
        assert isinstance(make_repetition_started(), MonitorEvent)


# ============================================================
# 4. MonitorListener Protocol
# ============================================================

class TestMonitorListenerProtocol:
    def test_class_with_on_event_is_listener(self):
        class GoodListener:
            def on_event(self, event: MonitorEvent) -> None:
                pass

        assert isinstance(GoodListener(), MonitorListener)

    def test_class_without_on_event_is_not_listener(self):
        class BadListener:
            def handle(self, event):
                pass

        assert not isinstance(BadListener(), MonitorListener)

    def test_event_collector_satisfies_protocol(self):
        collector = EventCollector()
        assert isinstance(collector, MonitorListener)

    def test_logging_listener_satisfies_protocol(self):
        ll = LoggingListener()
        assert isinstance(ll, MonitorListener)


# ============================================================
# 5. ProtocolMonitor - add/remove listener
# ============================================================

class TestProtocolMonitorListeners:
    def test_initial_listener_count_is_zero(self):
        monitor = ProtocolMonitor()
        assert monitor.listener_count == 0

    def test_add_listener_increments_count(self):
        monitor = ProtocolMonitor()
        collector = EventCollector()
        monitor.add_listener(collector)
        assert monitor.listener_count == 1

    def test_add_multiple_listeners(self):
        monitor = ProtocolMonitor()
        monitor.add_listener(EventCollector())
        monitor.add_listener(EventCollector())
        assert monitor.listener_count == 2

    def test_remove_listener_decrements_count(self):
        monitor = ProtocolMonitor()
        collector = EventCollector()
        monitor.add_listener(collector)
        monitor.remove_listener(collector)
        assert monitor.listener_count == 0

    def test_remove_listener_not_present_is_noop(self):
        monitor = ProtocolMonitor()
        collector = EventCollector()
        # Remove without adding - no exception
        monitor.remove_listener(collector)
        assert monitor.listener_count == 0

    def test_remove_only_removes_target_listener(self):
        monitor = ProtocolMonitor()
        c1 = EventCollector()
        c2 = EventCollector()
        monitor.add_listener(c1)
        monitor.add_listener(c2)
        monitor.remove_listener(c1)
        assert monitor.listener_count == 1


# ============================================================
# 6. ProtocolMonitor - emit events
# ============================================================

class TestProtocolMonitorEmit:
    def test_emit_delivers_event_to_listener(self):
        monitor = ProtocolMonitor()
        collector = EventCollector()
        monitor.add_listener(collector)

        ev = make_session_started()
        monitor.emit(ev)

        assert len(collector.events) == 1
        assert collector.events[0] is ev

    def test_emit_delivers_to_all_listeners(self):
        monitor = ProtocolMonitor()
        c1 = EventCollector()
        c2 = EventCollector()
        monitor.add_listener(c1)
        monitor.add_listener(c2)

        ev = make_session_started()
        monitor.emit(ev)

        assert len(c1.events) == 1
        assert len(c2.events) == 1

    def test_emit_no_listeners_no_error(self):
        monitor = ProtocolMonitor()
        monitor.emit(make_session_started())  # No exception

    def test_bad_listener_does_not_break_emit(self):
        monitor = ProtocolMonitor()

        class BrokenListener:
            def on_event(self, event: MonitorEvent) -> None:
                raise RuntimeError("I am broken")

        good = EventCollector()
        monitor.add_listener(BrokenListener())
        monitor.add_listener(good)

        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            monitor.emit(make_session_started())

        # Warning emitted for broken listener
        assert len(caught) == 1
        assert issubclass(caught[0].category, RuntimeWarning)
        assert "BrokenListener" in str(caught[0].message)

        # Good listener still received the event
        assert len(good.events) == 1

    def test_bad_listener_warning_contains_exception_type(self):
        monitor = ProtocolMonitor()

        class ExplodingListener:
            def on_event(self, event: MonitorEvent) -> None:
                raise ValueError("boom")

        monitor.add_listener(ExplodingListener())

        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            monitor.emit(make_message_sent())

        assert len(caught) == 1
        assert "ValueError" in str(caught[0].message)


# ============================================================
# 7. ProtocolMonitor - listening() context manager
# ============================================================

class TestProtocolMonitorListeningContextManager:
    def test_listening_adds_then_removes_listener(self):
        monitor = ProtocolMonitor()
        collector = EventCollector()

        with monitor.listening(collector):
            assert monitor.listener_count == 1
            monitor.emit(make_session_started())

        # After context: removed
        assert monitor.listener_count == 0
        # But the event was received during the block
        assert len(collector.events) == 1

    def test_listening_removes_on_exception(self):
        monitor = ProtocolMonitor()
        collector = EventCollector()

        with pytest.raises(RuntimeError):
            with monitor.listening(collector):
                raise RuntimeError("test error")

        assert monitor.listener_count == 0

    def test_listening_events_not_received_after_exit(self):
        monitor = ProtocolMonitor()
        collector = EventCollector()

        with monitor.listening(collector):
            pass

        monitor.emit(make_message_sent())
        # No events after context exit
        assert len(collector.events) == 0


# ============================================================
# 8. ProtocolMonitor - metrics property
# ============================================================

class TestProtocolMonitorMetrics:
    def test_metrics_returns_snapshot(self):
        monitor = ProtocolMonitor()
        snap = monitor.metrics
        assert isinstance(snap, MetricsSnapshot)

    def test_metrics_initial_all_zero(self):
        monitor = ProtocolMonitor()
        snap = monitor.metrics
        assert snap.sessions_started == 0
        assert snap.total_messages == 0
        assert snap.sessions_completed == 0

    def test_reset_metrics_zeroes_all(self):
        monitor = ProtocolMonitor()
        monitor.emit(make_session_started())
        monitor.emit(make_message_sent())
        monitor.reset_metrics()

        snap = monitor.metrics
        assert snap.sessions_started == 0
        assert snap.total_messages == 0


# ============================================================
# 9. MetricsCollector
# ============================================================

class TestMetricsCollector:
    def test_record_session_started_increments_count(self):
        mc = MetricsCollector()
        mc.record(make_session_started())
        snap = mc.snapshot()
        assert snap.sessions_started == 1

    def test_record_session_started_tracks_per_protocol(self):
        mc = MetricsCollector()
        mc.record(make_session_started(protocol_name="DelegateTask"))
        mc.record(make_session_started(protocol_name="DelegateTask"))
        mc.record(make_session_started(protocol_name="SimpleTask"))
        snap = mc.snapshot()
        assert snap.sessions_per_protocol["DelegateTask"] == 2
        assert snap.sessions_per_protocol["SimpleTask"] == 1

    def test_record_message_sent_increments_total(self):
        mc = MetricsCollector()
        mc.record(make_message_sent())
        mc.record(make_message_sent())
        snap = mc.snapshot()
        assert snap.total_messages == 2

    def test_record_message_sent_tracks_step_duration(self):
        mc = MetricsCollector()
        ev = MessageSent(
            session_id="S001",
            protocol_name="TestProto",
            timestamp=time.time(),
            step_index=0,
            sender="regina",
            receiver="worker",
            message_kind=MessageKind.TASK_REQUEST,
            duration_ms=10.0,
        )
        mc.record(ev)
        snap = mc.snapshot()
        assert snap.avg_step_duration_ms == 10.0

    def test_record_branch_chosen_increments_total(self):
        mc = MetricsCollector()
        mc.record(make_branch_chosen())
        snap = mc.snapshot()
        assert snap.total_branches == 1

    def test_record_branch_chosen_tracks_frequency(self):
        mc = MetricsCollector()
        mc.record(make_branch_chosen())
        mc.record(make_branch_chosen())
        approve_branch = BranchChosen(
            session_id="S002",
            protocol_name="TestProto",
            timestamp=time.time(),
            step_index=2,
            branch_name="reject",
            auto_detected=True,
        )
        mc.record(approve_branch)
        snap = mc.snapshot()
        assert snap.branch_frequency["approve"] == 2
        assert snap.branch_frequency["reject"] == 1

    def test_record_violation_increments_total(self):
        mc = MetricsCollector()
        mc.record(make_violation())
        snap = mc.snapshot()
        assert snap.total_violations == 1

    def test_record_violation_tracks_session_as_violated(self):
        mc = MetricsCollector()
        mc.record(make_violation(session_id="S001"))
        snap = mc.snapshot()
        assert snap.sessions_violated == 1

    def test_multiple_violations_same_session_counted_once(self):
        mc = MetricsCollector()
        mc.record(make_violation(session_id="S001", step_index=0))
        mc.record(make_violation(session_id="S001", step_index=1))
        snap = mc.snapshot()
        assert snap.sessions_violated == 1
        assert snap.total_violations == 2

    def test_violations_different_sessions_counted_separately(self):
        mc = MetricsCollector()
        mc.record(make_violation(session_id="S001"))
        mc.record(make_violation(session_id="S002"))
        snap = mc.snapshot()
        assert snap.sessions_violated == 2

    def test_record_violation_tracks_by_step(self):
        mc = MetricsCollector()
        mc.record(make_violation(step_index=2))
        mc.record(make_violation(step_index=2))
        mc.record(make_violation(step_index=0))
        snap = mc.snapshot()
        assert snap.violation_by_step[2] == 2
        assert snap.violation_by_step[0] == 1

    def test_record_session_ended_increments_completed(self):
        mc = MetricsCollector()
        mc.record(make_session_ended())
        snap = mc.snapshot()
        assert snap.sessions_completed == 1

    def test_record_session_ended_tracks_duration(self):
        mc = MetricsCollector()
        mc.record(make_session_ended(duration_ms=100.0))
        mc.record(make_session_ended(duration_ms=200.0))
        snap = mc.snapshot()
        assert snap.avg_session_duration_ms == 150.0

    def test_avg_session_duration_zero_when_no_sessions(self):
        mc = MetricsCollector()
        snap = mc.snapshot()
        assert snap.avg_session_duration_ms == 0.0

    def test_avg_step_duration_zero_when_no_messages(self):
        mc = MetricsCollector()
        snap = mc.snapshot()
        assert snap.avg_step_duration_ms == 0.0

    def test_avg_step_duration_correct(self):
        mc = MetricsCollector()
        for duration in [10.0, 20.0, 30.0]:
            ev = MessageSent(
                session_id="S001",
                protocol_name="TestProto",
                timestamp=time.time(),
                step_index=0,
                sender="regina",
                receiver="worker",
                message_kind=MessageKind.TASK_REQUEST,
                duration_ms=duration,
            )
            mc.record(ev)
        snap = mc.snapshot()
        assert snap.avg_step_duration_ms == 20.0

    def test_reset_clears_all_counters(self):
        mc = MetricsCollector()
        mc.record(make_session_started())
        mc.record(make_message_sent())
        mc.record(make_violation())
        mc.record(make_session_ended())
        mc.reset()

        snap = mc.snapshot()
        assert snap.sessions_started == 0
        assert snap.total_messages == 0
        assert snap.total_violations == 0
        assert snap.sessions_completed == 0
        assert snap.sessions_violated == 0
        assert snap.total_branches == 0
        assert snap.avg_session_duration_ms == 0.0
        assert snap.avg_step_duration_ms == 0.0

    def test_reset_clears_branch_frequency(self):
        mc = MetricsCollector()
        mc.record(make_branch_chosen())
        mc.reset()
        snap = mc.snapshot()
        assert dict(snap.branch_frequency) == {}

    def test_reset_clears_violation_by_step(self):
        mc = MetricsCollector()
        mc.record(make_violation(step_index=3))
        mc.reset()
        snap = mc.snapshot()
        assert dict(snap.violation_by_step) == {}

    def test_unknown_event_type_is_ignored(self):
        """Unknown MonitorEvent subclasses are silently ignored."""
        mc = MetricsCollector()

        @pytest.mark.skip
        class UnknownEvent(MonitorEvent):
            pass

        ev = UnknownEvent(
            session_id="S001",
            protocol_name="TestProto",
            timestamp=time.time(),
        )
        mc.record(ev)  # No exception
        snap = mc.snapshot()
        assert snap.sessions_started == 0


# ============================================================
# 10. MetricsSnapshot
# ============================================================

class TestMetricsSnapshot:
    def test_default_values_all_zero_or_empty(self):
        snap = MetricsSnapshot()
        assert snap.sessions_started == 0
        assert snap.sessions_completed == 0
        assert snap.sessions_violated == 0
        assert snap.total_messages == 0
        assert snap.total_violations == 0
        assert snap.total_branches == 0
        assert snap.avg_session_duration_ms == 0.0
        assert snap.avg_step_duration_ms == 0.0
        assert dict(snap.violation_by_step) == {}
        assert dict(snap.branch_frequency) == {}
        assert dict(snap.sessions_per_protocol) == {}

    def test_snapshot_is_frozen(self):
        snap = MetricsSnapshot()
        with pytest.raises(FrozenInstanceError):
            snap.sessions_started = 99  # type: ignore[misc]

    def test_mapping_fields_are_mapping_proxy(self):
        snap = MetricsSnapshot()
        assert isinstance(snap.violation_by_step, MappingProxyType)
        assert isinstance(snap.branch_frequency, MappingProxyType)
        assert isinstance(snap.sessions_per_protocol, MappingProxyType)

    def test_snapshot_from_collector_has_immutable_maps(self):
        mc = MetricsCollector()
        mc.record(make_violation(step_index=1))
        mc.record(make_branch_chosen())
        mc.record(make_session_started(protocol_name="DelegateTask"))
        snap = mc.snapshot()

        assert isinstance(snap.violation_by_step, MappingProxyType)
        assert isinstance(snap.branch_frequency, MappingProxyType)
        assert isinstance(snap.sessions_per_protocol, MappingProxyType)

    def test_snapshot_maps_cannot_be_mutated(self):
        mc = MetricsCollector()
        mc.record(make_violation(step_index=1))
        snap = mc.snapshot()

        with pytest.raises(TypeError):
            snap.violation_by_step[1] = 999  # type: ignore[index]


# ============================================================
# 11. LoggingListener
# ============================================================

class TestLoggingListener:
    def _get_listener_and_records(self, logger_name="test.monitor"):
        listener = LoggingListener(logger_name=logger_name)
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)
        records = []

        class CapturingHandler(logging.Handler):
            def emit(self, record):
                records.append(record)

        handler = CapturingHandler()
        logger.addHandler(handler)
        return listener, records, handler, logger

    def test_violation_logged_at_warning(self):
        listener, records, handler, logger = self._get_listener_and_records(
            "test.monitor.violation"
        )
        try:
            listener.on_event(make_violation())
            assert len(records) == 1
            assert records[0].levelno == logging.WARNING
        finally:
            logger.removeHandler(handler)

    def test_session_ended_logged_at_info(self):
        listener, records, handler, logger = self._get_listener_and_records(
            "test.monitor.ended"
        )
        try:
            listener.on_event(make_session_ended())
            assert len(records) == 1
            assert records[0].levelno == logging.INFO
        finally:
            logger.removeHandler(handler)

    def test_session_started_logged_at_info(self):
        listener, records, handler, logger = self._get_listener_and_records(
            "test.monitor.started"
        )
        try:
            listener.on_event(make_session_started())
            assert len(records) == 1
            assert records[0].levelno == logging.INFO
        finally:
            logger.removeHandler(handler)

    def test_message_sent_logged_at_debug(self):
        listener, records, handler, logger = self._get_listener_and_records(
            "test.monitor.message"
        )
        try:
            listener.on_event(make_message_sent())
            assert len(records) == 1
            assert records[0].levelno == logging.DEBUG
        finally:
            logger.removeHandler(handler)

    def test_branch_chosen_logged_at_debug(self):
        listener, records, handler, logger = self._get_listener_and_records(
            "test.monitor.branch"
        )
        try:
            listener.on_event(make_branch_chosen())
            assert len(records) == 1
            assert records[0].levelno == logging.DEBUG
        finally:
            logger.removeHandler(handler)

    def test_repetition_started_logged_at_debug(self):
        listener, records, handler, logger = self._get_listener_and_records(
            "test.monitor.repetition"
        )
        try:
            listener.on_event(make_repetition_started())
            assert len(records) == 1
            assert records[0].levelno == logging.DEBUG
        finally:
            logger.removeHandler(handler)

    def test_default_logger_name(self):
        listener = LoggingListener()
        # Default name used - should not raise
        listener.on_event(make_session_started())

    def test_violation_log_contains_step_info(self):
        listener, records, handler, logger = self._get_listener_and_records(
            "test.monitor.viol2"
        )
        try:
            ev = make_violation(step_index=3)
            listener.on_event(ev)
            msg = records[0].getMessage()
            assert "3" in msg
        finally:
            logger.removeHandler(handler)

    def test_message_sent_log_contains_branch_when_present(self):
        listener, records, handler, logger = self._get_listener_and_records(
            "test.monitor.branch_msg"
        )
        try:
            ev = make_message_sent(branch="approve")
            listener.on_event(ev)
            msg = records[0].getMessage()
            assert "approve" in msg
        finally:
            logger.removeHandler(handler)

    def test_message_sent_no_branch_in_log(self):
        listener, records, handler, logger = self._get_listener_and_records(
            "test.monitor.no_branch"
        )
        try:
            ev = make_message_sent(branch=None)
            listener.on_event(ev)
            msg = records[0].getMessage()
            assert "branch=" not in msg
        finally:
            logger.removeHandler(handler)

    def test_unknown_event_not_logged(self):
        """Unknown event type does not crash and produces no log record."""
        listener, records, handler, logger = self._get_listener_and_records(
            "test.monitor.unknown"
        )
        try:
            # MonitorEvent base directly (no isinstance match in LoggingListener)
            ev = MonitorEvent(
                session_id="S001",
                protocol_name="TestProto",
                timestamp=time.time(),
            )
            listener.on_event(ev)  # Should not raise
            assert len(records) == 0
        finally:
            logger.removeHandler(handler)


# ============================================================
# 12. EventCollector
# ============================================================

class TestEventCollector:
    def test_initial_events_empty(self):
        collector = EventCollector()
        assert collector.events == []

    def test_on_event_appends_to_events(self):
        collector = EventCollector()
        ev = make_session_started()
        collector.on_event(ev)
        assert len(collector.events) == 1
        assert collector.events[0] is ev

    def test_multiple_events_collected_in_order(self):
        collector = EventCollector()
        ev1 = make_session_started()
        ev2 = make_message_sent()
        ev3 = make_session_ended()
        collector.on_event(ev1)
        collector.on_event(ev2)
        collector.on_event(ev3)
        assert collector.events[0] is ev1
        assert collector.events[1] is ev2
        assert collector.events[2] is ev3

    def test_clear_empties_events(self):
        collector = EventCollector()
        collector.on_event(make_session_started())
        collector.on_event(make_message_sent())
        collector.clear()
        assert collector.events == []

    def test_of_type_filters_correctly(self):
        collector = EventCollector()
        collector.on_event(make_session_started())
        collector.on_event(make_message_sent())
        collector.on_event(make_message_sent())
        collector.on_event(make_session_ended())

        messages = collector.of_type(MessageSent)
        assert len(messages) == 2
        assert all(isinstance(e, MessageSent) for e in messages)

    def test_of_type_returns_empty_when_no_match(self):
        collector = EventCollector()
        collector.on_event(make_session_started())
        assert collector.of_type(ViolationOccurred) == []

    def test_of_type_with_violation(self):
        collector = EventCollector()
        collector.on_event(make_violation())
        collector.on_event(make_message_sent())
        violations = collector.of_type(ViolationOccurred)
        assert len(violations) == 1
        assert isinstance(violations[0], ViolationOccurred)

    def test_of_type_with_branch_chosen(self):
        collector = EventCollector()
        collector.on_event(make_branch_chosen())
        branches = collector.of_type(BranchChosen)
        assert len(branches) == 1


# ============================================================
# 13. Thread Safety
# ============================================================

class TestThreadSafety:
    def test_concurrent_emit_no_crash(self):
        """Multiple threads emitting concurrently - no crash, all events recorded."""
        monitor = ProtocolMonitor()
        collector = EventCollector()
        monitor.add_listener(collector)

        n_threads = 10
        n_events_per_thread = 20
        errors = []

        def emit_many():
            try:
                for _ in range(n_events_per_thread):
                    monitor.emit(make_message_sent())
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=emit_many) for _ in range(n_threads)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == [], f"Thread errors: {errors}"
        assert len(collector.events) == n_threads * n_events_per_thread

    def test_concurrent_metrics_recording_no_crash(self):
        """MetricsCollector is thread-safe."""
        mc = MetricsCollector()
        n_threads = 10
        n_per_thread = 20
        errors = []

        def record_many():
            try:
                for _ in range(n_per_thread):
                    mc.record(make_session_started())
                    mc.record(make_message_sent())
                    mc.record(make_violation())
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=record_many) for _ in range(n_threads)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []
        snap = mc.snapshot()
        assert snap.sessions_started == n_threads * n_per_thread
        assert snap.total_messages == n_threads * n_per_thread
        assert snap.total_violations == n_threads * n_per_thread

    def test_add_remove_listener_concurrent(self):
        """Concurrent add/remove - no crash."""
        monitor = ProtocolMonitor()
        errors = []

        def add_and_remove():
            try:
                collector = EventCollector()
                monitor.add_listener(collector)
                monitor.emit(make_session_started())
                monitor.remove_listener(collector)
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=add_and_remove) for _ in range(20)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []
