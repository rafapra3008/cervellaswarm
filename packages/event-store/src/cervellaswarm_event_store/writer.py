# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""
Event and Lesson dataclasses with write functions.

All dataclasses are frozen (immutable) with __post_init__ validation.
The private _insert_* functions operate on an existing sqlite3.Connection;
callers should use EventStore.log_event / EventStore.log_lesson instead.
"""

import json
import sqlite3
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

_VALID_EVENT_TYPES = frozenset(
    {
        "task_started",
        "task_completed",
        "task_failed",
        "session_started",
        "session_ended",
        "message_sent",
        "violation",
        "custom",
    }
)

_VALID_SEVERITIES = frozenset({"low", "medium", "high", "critical"})
_VALID_STATUSES = frozenset({"active", "resolved", "suppressed"})


def _utc_now() -> str:
    """Return current UTC time as ISO 8601 string."""
    return datetime.now(timezone.utc).isoformat()


def _new_id() -> str:
    """Return a new UUID4 string."""
    return str(uuid.uuid4())


def _validate_nonempty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")


def _validate_in_set(value: str, valid: frozenset, field_name: str) -> None:
    normalised = value.lower().strip()
    if normalised not in valid:
        raise ValueError(f"{field_name} must be one of {sorted(valid)}, got {value!r}")


@dataclass(frozen=True)
class Event:
    """Represents a single agent event to be stored.

    Required fields:
        event_type: One of the recognised event types.

    Optional fields default to None / sensible values.

    Attributes:
        id: UUID string. Auto-generated if empty.
        timestamp: ISO 8601 UTC string. Auto-generated if empty.
        event_type: task_started | task_completed | task_failed |
                    session_started | session_ended | message_sent |
                    violation | custom
        session_id: Identifier for the agent session.
        agent_name: Name of the agent (e.g. 'backend').
        agent_role: Human-readable role (e.g. 'Backend Specialist').
        task_id: Identifier for the task.
        parent_task_id: Parent task identifier for sub-tasks.
        description: Human-readable description of what happened.
        status: Task status string (e.g. 'completed', 'failed').
        duration_ms: Elapsed time in milliseconds.
        success: True if the operation succeeded, False if it failed.
        error_message: Error description when success is False.
        project: Project name / identifier.
        files_modified: List of file paths modified by this event.
        tags: Arbitrary string tags for filtering.
        metadata: Arbitrary key-value metadata dict.
    """

    event_type: str
    id: str = field(default_factory=_new_id)
    timestamp: str = field(default_factory=_utc_now)
    session_id: Optional[str] = None
    agent_name: Optional[str] = None
    agent_role: Optional[str] = None
    task_id: Optional[str] = None
    parent_task_id: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    duration_ms: Optional[int] = None
    success: Optional[bool] = None
    error_message: Optional[str] = None
    project: Optional[str] = None
    files_modified: tuple = field(default_factory=tuple)
    tags: tuple = field(default_factory=tuple)
    metadata: Optional[dict] = None

    def __post_init__(self) -> None:
        _validate_nonempty(self.event_type, "event_type")
        _validate_in_set(self.event_type, _VALID_EVENT_TYPES, "event_type")
        if self.duration_ms is not None and self.duration_ms < 0:
            raise ValueError("duration_ms must be >= 0")
        if self.id and not self.id.strip():
            raise ValueError("id must be non-empty when provided")
        if self.timestamp and not self.timestamp.strip():
            raise ValueError("timestamp must be non-empty when provided")


@dataclass(frozen=True)
class Lesson:
    """Represents a lesson learned to be stored.

    Attributes:
        id: UUID string. Auto-generated if empty.
        timestamp: ISO 8601 UTC string. Auto-generated if empty.
        context: Situation in which the lesson was learned.
        problem: What went wrong or what was the challenge.
        solution: What resolved the problem.
        pattern: Short, reusable pattern name.
        category: Optional category (e.g. 'testing', 'security').
        severity: low | medium | high | critical (default: medium).
        root_cause: Underlying root cause.
        prevention: How to prevent recurrence.
        agents_involved: Names of agents involved.
        project: Project name.
        confidence: Float 0.0-1.0. Confidence in this lesson.
        times_applied: How many times this lesson was applied.
        status: active | resolved | suppressed (default: active).
        tags: Arbitrary string tags.
    """

    id: str = field(default_factory=_new_id)
    timestamp: str = field(default_factory=_utc_now)
    context: Optional[str] = None
    problem: Optional[str] = None
    solution: Optional[str] = None
    pattern: Optional[str] = None
    category: Optional[str] = None
    severity: str = "medium"
    root_cause: Optional[str] = None
    prevention: Optional[str] = None
    agents_involved: tuple = field(default_factory=tuple)
    project: Optional[str] = None
    confidence: float = 0.5
    times_applied: int = 0
    status: str = "active"
    tags: tuple = field(default_factory=tuple)

    def __post_init__(self) -> None:
        _validate_in_set(self.severity, _VALID_SEVERITIES, "severity")
        _validate_in_set(self.status, _VALID_STATUSES, "status")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(f"confidence must be between 0.0 and 1.0, got {self.confidence}")
        if self.times_applied < 0:
            raise ValueError("times_applied must be >= 0")
        if self.id and not self.id.strip():
            raise ValueError("id must be non-empty when provided")


# ------------------------------------------------------------------
# Internal write functions
# ------------------------------------------------------------------


def _insert_event(conn: sqlite3.Connection, event: Event) -> str:
    """Insert an Event into the database. Returns the event id."""
    files_json = json.dumps(list(event.files_modified)) if event.files_modified else None
    tags_json = json.dumps(list(event.tags)) if event.tags else None
    meta_json = json.dumps(event.metadata) if event.metadata else None

    success_int: Optional[int] = None
    if event.success is not None:
        success_int = 1 if event.success else 0

    conn.execute(
        """
        INSERT INTO events (
            id, timestamp, session_id, event_type,
            agent_name, agent_role,
            task_id, parent_task_id, description, status,
            duration_ms, success, error_message,
            project, files_modified,
            tags, metadata
        ) VALUES (
            :id, :timestamp, :session_id, :event_type,
            :agent_name, :agent_role,
            :task_id, :parent_task_id, :description, :status,
            :duration_ms, :success, :error_message,
            :project, :files_modified,
            :tags, :metadata
        )
        """,
        {
            "id": event.id,
            "timestamp": event.timestamp,
            "session_id": event.session_id,
            "event_type": event.event_type,
            "agent_name": event.agent_name,
            "agent_role": event.agent_role,
            "task_id": event.task_id,
            "parent_task_id": event.parent_task_id,
            "description": event.description,
            "status": event.status,
            "duration_ms": event.duration_ms,
            "success": success_int,
            "error_message": event.error_message,
            "project": event.project,
            "files_modified": files_json,
            "tags": tags_json,
            "metadata": meta_json,
        },
    )
    conn.commit()
    return event.id


def _insert_lesson(conn: sqlite3.Connection, lesson: Lesson) -> str:
    """Insert a Lesson into the database. Returns the lesson id."""
    agents_json = json.dumps(list(lesson.agents_involved)) if lesson.agents_involved else None
    tags_json = json.dumps(list(lesson.tags)) if lesson.tags else None

    conn.execute(
        """
        INSERT INTO lessons (
            id, timestamp,
            context, problem, solution, pattern,
            category, severity, root_cause, prevention,
            agents_involved, project,
            confidence, times_applied, status, tags
        ) VALUES (
            :id, :timestamp,
            :context, :problem, :solution, :pattern,
            :category, :severity, :root_cause, :prevention,
            :agents_involved, :project,
            :confidence, :times_applied, :status, :tags
        )
        """,
        {
            "id": lesson.id,
            "timestamp": lesson.timestamp,
            "context": lesson.context,
            "problem": lesson.problem,
            "solution": lesson.solution,
            "pattern": lesson.pattern,
            "category": lesson.category,
            "severity": lesson.severity,
            "root_cause": lesson.root_cause,
            "prevention": lesson.prevention,
            "agents_involved": agents_json,
            "project": lesson.project,
            "confidence": lesson.confidence,
            "times_applied": lesson.times_applied,
            "status": lesson.status,
            "tags": tags_json,
        },
    )
    conn.commit()
    return lesson.id
