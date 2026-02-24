# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Integration tests for cervellaswarm-event-store."""

import pytest

from cervellaswarm_event_store import (
    EventStore,
    Event,
    Lesson,
    QueryResult,
    Statistics,
    DetectedPattern,
    ScoredLesson,
)


class TestFullWorkflow:
    """End-to-end workflow: log -> query -> stats -> lessons -> patterns."""

    def test_complete_workflow(self):
        with EventStore(":memory:") as store:
            # Log several events
            ids = []
            for i in range(5):
                ev = Event(
                    event_type="task_completed",
                    agent_name="backend",
                    project="web-app",
                    description=f"Task {i}",
                    success=True,
                    duration_ms=100 * (i + 1),
                )
                ids.append(store.log_event(ev))

            store.log_event(Event(
                event_type="task_failed",
                agent_name="backend",
                project="web-app",
                success=False,
                error_message="Database connection refused",
            ))

            # Log a lesson
            lesson_id = store.log_lesson(Lesson(
                problem="DB connection refused",
                solution="Use connection pooling",
                pattern="connection-pooling",
                confidence=0.9,
                project="web-app",
            ))

            # Query
            result = store.query_events(agent="backend")
            assert isinstance(result, QueryResult)
            assert result.total == 6

            # Stats
            stats = store.get_statistics()
            assert isinstance(stats, Statistics)
            assert stats.total_events == 6
            assert stats.total_lessons == 1
            assert stats.success_count == 5
            assert stats.fail_count == 1
            assert abs(stats.success_rate - 5 / 6) < 0.01

            # Lessons
            lessons = store.get_lessons(project="web-app")
            assert len(lessons) == 1
            assert isinstance(lessons[0], ScoredLesson)

    def test_multi_project_isolation(self):
        with EventStore(":memory:") as store:
            for proj in ["proj-a", "proj-b", "proj-c"]:
                for _ in range(3):
                    store.log_event(Event(
                        event_type="task_completed",
                        agent_name="backend",
                        project=proj,
                        success=True,
                    ))

            a = store.query_events(project="proj-a")
            assert a.total == 3

            stats_b = store.get_statistics(project="proj-b")
            assert stats_b.total_events == 3

            stats_all = store.get_statistics()
            assert stats_all.total_events == 9

    def test_context_manager_cleanup(self):
        store = EventStore(":memory:")
        assert store.is_open
        with store:
            store.log_event(Event(event_type="custom"))
        assert not store.is_open

    def test_file_persistence(self, tmp_path):
        db = tmp_path / "persist.db"

        with EventStore(db) as store:
            store.log_event(Event(event_type="task_completed", project="test"))
            store.log_lesson(Lesson(problem="stored", confidence=0.9))

        # Re-open and verify data persisted
        with EventStore(db) as store2:
            result = store2.query_events()
            stats = store2.get_statistics()
            assert result.total == 1
            assert stats.total_lessons == 1


class TestPatternDetectionIntegration:
    def test_repeated_errors_create_pattern(self):
        with EventStore(":memory:") as store:
            for i in range(5):
                store.log_event(Event(
                    event_type="task_failed",
                    agent_name="backend",
                    success=False,
                    error_message="JWT token verification failed: invalid signature",
                ))

            patterns = store.detect_patterns(days=1, min_occurrences=3)
            assert len(patterns) == 1
            assert patterns[0].occurrence_count == 5
            assert patterns[0].severity == "high"
            assert isinstance(patterns[0], DetectedPattern)

    def test_pattern_severity_escalates(self):
        with EventStore(":memory:") as store:
            for _ in range(10):
                store.log_event(Event(
                    event_type="task_failed",
                    success=False,
                    error_message="Out of memory error",
                ))
            patterns = store.detect_patterns(min_occurrences=3)
            assert patterns[0].severity == "critical"


class TestLessonRelevanceIntegration:
    def test_agent_and_project_matching(self):
        with EventStore(":memory:") as store:
            # High relevance: agent + project match
            store.log_lesson(Lesson(
                problem="Backend timeout",
                solution="Use async",
                agents_involved=("backend",),
                project="my-proj",
                confidence=0.7,
            ))
            # Low relevance: different agent + project
            store.log_lesson(Lesson(
                problem="CSS bug",
                solution="Fix selector",
                agents_involved=("frontend",),
                project="other-proj",
                confidence=0.9,
            ))

            lessons = store.get_lessons(agent="backend", project="my-proj")
            # Most relevant should be first
            assert lessons[0].agents_involved == ("backend",)


class TestAgentStatsIntegration:
    def test_agent_stats_comprehensive(self):
        with EventStore(":memory:") as store:
            # backend: 3 success, 1 fail
            for _ in range(3):
                store.log_event(Event(event_type="task_completed",
                                      agent_name="backend", success=True, duration_ms=100))
            store.log_event(Event(event_type="task_failed",
                                  agent_name="backend", success=False, duration_ms=50))
            # frontend: 2 success
            for _ in range(2):
                store.log_event(Event(event_type="task_completed",
                                      agent_name="frontend", success=True))

            stats_list = store.agent_stats()
            assert len(stats_list) == 2

            backend = next(s for s in stats_list if s["agent_name"] == "backend")
            assert backend["total_tasks"] == 4
            assert backend["successful_tasks"] == 3
            assert backend["failed_tasks"] == 1
            assert abs(backend["success_rate"] - 0.75) < 0.01
            assert backend["avg_duration_ms"] == 87.5


class TestPublicAPICompleteness:
    """Verify __init__.py exports all expected symbols."""

    def test_event_store_exported(self):
        from cervellaswarm_event_store import EventStore
        assert EventStore is not None

    def test_event_exported(self):
        from cervellaswarm_event_store import Event
        assert Event is not None

    def test_lesson_exported(self):
        from cervellaswarm_event_store import Lesson
        assert Lesson is not None

    def test_query_result_exported(self):
        from cervellaswarm_event_store import QueryResult
        assert QueryResult is not None

    def test_statistics_exported(self):
        from cervellaswarm_event_store import Statistics
        assert Statistics is not None

    def test_detected_pattern_exported(self):
        from cervellaswarm_event_store import DetectedPattern
        assert DetectedPattern is not None

    def test_scored_lesson_exported(self):
        from cervellaswarm_event_store import ScoredLesson
        assert ScoredLesson is not None

    def test_config_functions_exported(self):
        from cervellaswarm_event_store import load_config, get_db_path, get_section
        assert load_config is not None
        assert get_db_path is not None
        assert get_section is not None

    def test_get_relevant_lessons_exported(self):
        from cervellaswarm_event_store import get_relevant_lessons
        assert get_relevant_lessons is not None

    def test_agent_summary_exported(self):
        from cervellaswarm_event_store import AgentSummary
        assert AgentSummary is not None

    def test_event_record_exported(self):
        from cervellaswarm_event_store import EventRecord
        assert EventRecord is not None


class TestEdgeCases:
    def test_event_with_no_optional_fields(self):
        with EventStore(":memory:") as store:
            ev = Event(event_type="custom")
            event_id = store.log_event(ev)
            result = store.query_events()
            r = result.events[0]
            assert r.agent_name is None
            assert r.project is None
            assert r.files_modified == ()
            assert r.tags == ()
            assert r.metadata is None

    def test_lesson_with_no_optional_fields(self):
        with EventStore(":memory:") as store:
            l = Lesson()
            store.log_lesson(l)
            stats = store.get_statistics()
            assert stats.total_lessons == 1

    def test_many_events_performance(self):
        with EventStore(":memory:") as store:
            for i in range(500):
                store.log_event(Event(
                    event_type="task_completed",
                    agent_name=f"agent-{i % 5}",
                    project=f"proj-{i % 3}",
                    success=True,
                ))
            result = store.query_events(limit=500)
            assert result.total == 500
            stats = store.get_statistics()
            assert stats.total_events == 500

    def test_unicode_in_fields(self):
        with EventStore(":memory:") as store:
            ev = Event(
                event_type="custom",
                description="Unicode test: cafe, resume, naïve",
                project="unicode-proj",
            )
            store.log_event(ev)
            result = store.query_events()
            assert "cafe" in result.events[0].description

    def test_session_tracking(self):
        with EventStore(":memory:") as store:
            session = "session-abc-123"
            store.log_event(Event(event_type="session_started", session_id=session))
            for i in range(3):
                store.log_event(Event(
                    event_type="task_completed",
                    session_id=session,
                    agent_name="backend",
                ))
            store.log_event(Event(event_type="session_ended", session_id=session))

            result = store.query_events(session_id=session)
            assert result.total == 5

    def test_concurrent_reopen(self, tmp_path):
        db = tmp_path / "shared.db"
        with EventStore(db) as s1:
            s1.log_event(Event(event_type="custom"))

        with EventStore(db) as s2:
            result = s2.query_events()
            assert result.total == 1
