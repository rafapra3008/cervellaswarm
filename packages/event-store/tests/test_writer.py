# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for cervellaswarm_event_store.writer module."""

import pytest

from cervellaswarm_event_store.writer import Event, Lesson, _insert_event, _insert_lesson, _utc_now, _new_id


class TestNewId:
    def test_returns_string(self):
        assert isinstance(_new_id(), str)

    def test_uuid_format(self):
        uid = _new_id()
        assert len(uid) == 36
        assert uid.count("-") == 4

    def test_unique(self):
        ids = {_new_id() for _ in range(100)}
        assert len(ids) == 100


class TestUtcNow:
    def test_returns_string(self):
        assert isinstance(_utc_now(), str)

    def test_contains_utc_marker(self):
        ts = _utc_now()
        assert "+" in ts or "Z" in ts or ts.endswith("+00:00")


class TestEvent:
    def test_minimal_creation(self):
        ev = Event(event_type="task_completed")
        assert ev.event_type == "task_completed"
        assert ev.id  # auto-generated
        assert ev.timestamp  # auto-generated

    def test_auto_id_generated(self):
        ev1 = Event(event_type="custom")
        ev2 = Event(event_type="custom")
        assert ev1.id != ev2.id

    def test_auto_timestamp_generated(self):
        ev = Event(event_type="custom")
        assert len(ev.timestamp) > 0

    def test_all_fields(self):
        ev = Event(
            event_type="task_completed",
            id="test-id",
            timestamp="2026-01-01T00:00:00+00:00",
            session_id="sess-1",
            agent_name="backend",
            agent_role="Backend Specialist",
            task_id="task-1",
            parent_task_id="parent-1",
            description="Did something",
            status="completed",
            duration_ms=1000,
            success=True,
            error_message=None,
            project="my-project",
            files_modified=("a.py", "b.py"),
            tags=("fast", "clean"),
            metadata={"key": "val"},
        )
        assert ev.agent_name == "backend"
        assert ev.files_modified == ("a.py", "b.py")

    def test_frozen(self):
        ev = Event(event_type="custom")
        with pytest.raises((AttributeError, TypeError)):
            ev.event_type = "other"  # type: ignore

    def test_invalid_event_type_raises(self):
        with pytest.raises(ValueError, match="event_type"):
            Event(event_type="invalid_type")

    def test_empty_event_type_raises(self):
        with pytest.raises(ValueError):
            Event(event_type="")

    def test_whitespace_event_type_raises(self):
        with pytest.raises(ValueError):
            Event(event_type="   ")

    def test_negative_duration_raises(self):
        with pytest.raises(ValueError, match="duration_ms"):
            Event(event_type="task_completed", duration_ms=-1)

    def test_zero_duration_allowed(self):
        ev = Event(event_type="task_completed", duration_ms=0)
        assert ev.duration_ms == 0

    def test_all_valid_event_types(self):
        for et in ["task_started", "task_completed", "task_failed",
                   "session_started", "session_ended", "message_sent",
                   "violation", "custom"]:
            ev = Event(event_type=et)
            assert ev.event_type == et

    def test_success_bool_preserved(self):
        ev = Event(event_type="task_completed", success=True)
        assert ev.success is True
        ev2 = Event(event_type="task_failed", success=False)
        assert ev2.success is False

    def test_empty_files_modified_default(self):
        ev = Event(event_type="custom")
        assert ev.files_modified == ()

    def test_empty_tags_default(self):
        ev = Event(event_type="custom")
        assert ev.tags == ()

    def test_metadata_none_default(self):
        ev = Event(event_type="custom")
        assert ev.metadata is None


class TestLesson:
    def test_minimal_creation(self):
        lesson = Lesson()
        assert lesson.id
        assert lesson.timestamp
        assert lesson.severity == "medium"
        assert lesson.confidence == 0.5
        assert lesson.status == "active"

    def test_all_fields(self):
        lesson = Lesson(
            context="Testing",
            problem="Race condition",
            solution="Use locks",
            pattern="synchronize-access",
            category="concurrency",
            severity="high",
            root_cause="Shared mutable state",
            prevention="Prefer immutable data",
            agents_involved=("backend", "tester"),
            project="my-project",
            confidence=0.9,
            times_applied=3,
            status="active",
            tags=("threading", "python"),
        )
        assert lesson.problem == "Race condition"
        assert lesson.agents_involved == ("backend", "tester")

    def test_frozen(self):
        lesson = Lesson()
        with pytest.raises((AttributeError, TypeError)):
            lesson.confidence = 0.9  # type: ignore

    def test_invalid_severity_raises(self):
        with pytest.raises(ValueError, match="severity"):
            Lesson(severity="EXTREME")

    def test_valid_severities(self):
        for sev in ["low", "medium", "high", "critical"]:
            lesson = Lesson(severity=sev)
            assert lesson.severity == sev

    def test_confidence_out_of_range_raises(self):
        with pytest.raises(ValueError, match="confidence"):
            Lesson(confidence=1.5)

    def test_confidence_negative_raises(self):
        with pytest.raises(ValueError, match="confidence"):
            Lesson(confidence=-0.1)

    def test_confidence_boundaries(self):
        l0 = Lesson(confidence=0.0)
        l1 = Lesson(confidence=1.0)
        assert l0.confidence == 0.0
        assert l1.confidence == 1.0

    def test_invalid_status_raises(self):
        with pytest.raises(ValueError, match="status"):
            Lesson(status="deleted")

    def test_valid_statuses(self):
        for st in ["active", "resolved", "suppressed"]:
            lesson = Lesson(status=st)
            assert lesson.status == st

    def test_negative_times_applied_raises(self):
        with pytest.raises(ValueError, match="times_applied"):
            Lesson(times_applied=-1)

    def test_zero_times_applied_allowed(self):
        lesson = Lesson(times_applied=0)
        assert lesson.times_applied == 0

    def test_auto_id_unique(self):
        ids = {Lesson().id for _ in range(50)}
        assert len(ids) == 50


class TestInsertEvent:
    def test_insert_returns_id(self, event_store):
        ev = Event(event_type="task_completed")
        from cervellaswarm_event_store.writer import _insert_event
        result_id = _insert_event(event_store._conn, ev)
        assert result_id == ev.id

    def test_insert_persists_all_fields(self, event_store):
        ev = Event(
            event_type="task_completed",
            agent_name="backend",
            project="proj",
            success=True,
            duration_ms=100,
            description="Test",
            files_modified=("a.py",),
            tags=("tag1",),
            metadata={"x": 1},
        )
        from cervellaswarm_event_store.writer import _insert_event
        _insert_event(event_store._conn, ev)
        cursor = event_store._conn.cursor()
        cursor.execute("SELECT * FROM events WHERE id = ?", (ev.id,))
        row = cursor.fetchone()
        assert row["agent_name"] == "backend"
        assert row["project"] == "proj"
        assert row["success"] == 1

    def test_insert_failed_event(self, event_store):
        ev = Event(
            event_type="task_failed",
            success=False,
            error_message="Something went wrong",
        )
        from cervellaswarm_event_store.writer import _insert_event
        _insert_event(event_store._conn, ev)
        cursor = event_store._conn.cursor()
        cursor.execute("SELECT success, error_message FROM events WHERE id = ?", (ev.id,))
        row = cursor.fetchone()
        assert row["success"] == 0
        assert row["error_message"] == "Something went wrong"


class TestInsertLesson:
    def test_insert_returns_id(self, event_store):
        lesson = Lesson(problem="test problem")
        from cervellaswarm_event_store.writer import _insert_lesson
        result_id = _insert_lesson(event_store._conn, lesson)
        assert result_id == lesson.id

    def test_insert_persists_fields(self, event_store):
        lesson = Lesson(
            context="ctx",
            problem="prob",
            solution="sol",
            pattern="pat",
            confidence=0.8,
            project="proj",
        )
        from cervellaswarm_event_store.writer import _insert_lesson
        _insert_lesson(event_store._conn, lesson)
        cursor = event_store._conn.cursor()
        cursor.execute("SELECT * FROM lessons WHERE id = ?", (lesson.id,))
        row = cursor.fetchone()
        assert row["problem"] == "prob"
        assert row["confidence"] == 0.8
        assert row["project"] == "proj"
