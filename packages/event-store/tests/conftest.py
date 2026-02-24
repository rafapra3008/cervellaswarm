# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Shared fixtures for cervellaswarm-event-store tests."""

import pytest

from cervellaswarm_event_store.database import EventStore
from cervellaswarm_event_store.writer import Event, Lesson


@pytest.fixture
def event_store():
    """In-memory EventStore instance. Fast, isolated."""
    store = EventStore(":memory:")
    yield store
    store.close()


@pytest.fixture
def sample_event():
    """A minimal valid Event instance."""
    return Event(
        event_type="task_completed",
        agent_name="backend",
        agent_role="Backend Specialist",
        project="test-project",
        description="Implemented endpoint",
        success=True,
        duration_ms=500,
    )


@pytest.fixture
def sample_lesson():
    """A minimal valid Lesson instance."""
    return Lesson(
        context="API design",
        problem="Missing input validation",
        solution="Add pydantic models",
        pattern="always-validate-input",
        severity="high",
        confidence=0.85,
        project="test-project",
    )


@pytest.fixture
def populated_store(event_store, sample_event, sample_lesson):
    """EventStore pre-loaded with sample data."""
    # Three events of different types
    event_store.log_event(sample_event)
    event_store.log_event(
        Event(
            event_type="task_failed",
            agent_name="frontend",
            project="test-project",
            description="CSS rendering bug",
            success=False,
            error_message="Cannot read property 'style' of null",
            duration_ms=100,
        )
    )
    event_store.log_event(
        Event(
            event_type="task_failed",
            agent_name="backend",
            project="other-project",
            description="DB connection failed",
            success=False,
            error_message="Connection timeout after 30s",
            duration_ms=30000,
        )
    )
    event_store.log_event(
        Event(
            event_type="session_started",
            session_id="sess-001",
            project="test-project",
        )
    )
    # One lesson
    event_store.log_lesson(sample_lesson)
    return event_store
