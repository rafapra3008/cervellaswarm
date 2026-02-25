# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for cervellaswarm_event_store.analytics module."""

import pytest

from cervellaswarm_event_store.writer import Event, Lesson
from cervellaswarm_event_store.analytics import (
    DetectedPattern,
    ScoredLesson,
    _calculate_similarity,
    _infer_severity,
    _get_lessons_scored,
    _detect_patterns,
    _agent_stats,
    get_relevant_lessons,
)


class TestCalculateSimilarity:
    def test_identical_strings(self):
        assert _calculate_similarity("hello", "hello") == 1.0

    def test_empty_strings(self):
        assert _calculate_similarity("", "") == 0.0
        assert _calculate_similarity("hello", "") == 0.0
        assert _calculate_similarity("", "world") == 0.0

    def test_completely_different(self):
        sim = _calculate_similarity("aaaa", "zzzz")
        assert sim == 0.0

    def test_similar_strings(self):
        sim = _calculate_similarity(
            "Connection timeout after 30s",
            "Connection timeout after 31s",
        )
        assert sim > 0.8

    def test_case_insensitive(self):
        sim = _calculate_similarity("ERROR", "error")
        assert sim == 1.0

    def test_whitespace_stripped(self):
        sim = _calculate_similarity("  hello  ", "hello")
        assert sim == 1.0

    def test_partial_similarity(self):
        sim = _calculate_similarity("Cannot read property 'x'", "Cannot read property 'y'")
        assert 0.8 <= sim < 1.0


class TestInferSeverity:
    def test_critical_threshold(self):
        assert _infer_severity(10) == "critical"
        assert _infer_severity(15) == "critical"

    def test_high_threshold(self):
        assert _infer_severity(5) == "high"
        assert _infer_severity(9) == "high"

    def test_medium_threshold(self):
        assert _infer_severity(3) == "medium"
        assert _infer_severity(4) == "medium"

    def test_low_threshold(self):
        assert _infer_severity(1) == "low"
        assert _infer_severity(2) == "low"


class TestScoredLessonDataclass:
    def test_valid_creation(self):
        sl = ScoredLesson(
            id="x",
            context=None,
            problem="p",
            solution="s",
            pattern=None,
            category=None,
            severity="medium",
            root_cause=None,
            prevention=None,
            agents_involved=(),
            project=None,
            confidence=0.8,
            times_applied=2,
            status="active",
            tags=(),
            score=30,
        )
        assert sl.score == 30

    def test_negative_score_raises(self):
        with pytest.raises(ValueError, match="score"):
            ScoredLesson(
                id="x", context=None, problem=None, solution=None, pattern=None,
                category=None, severity="low", root_cause=None, prevention=None,
                agents_involved=(), project=None, confidence=0.5, times_applied=0,
                status="active", tags=(), score=-1,
            )

    def test_frozen(self):
        sl = ScoredLesson(
            id="x", context=None, problem=None, solution=None, pattern=None,
            category=None, severity="low", root_cause=None, prevention=None,
            agents_involved=(), project=None, confidence=0.5, times_applied=0,
            status="active", tags=(), score=0,
        )
        with pytest.raises((AttributeError, TypeError)):
            sl.score = 10  # type: ignore


class TestDetectedPatternDataclass:
    def test_valid_creation(self):
        dp = DetectedPattern(
            pattern_name="DB timeout",
            pattern_type="task_failed",
            severity="high",
            occurrence_count=5,
            first_seen="2026-01-01T00:00:00",
            last_seen="2026-01-07T00:00:00",
            affected_agents=("backend",),
            error_ids=("id1", "id2"),
        )
        assert dp.occurrence_count == 5

    def test_empty_pattern_name_raises(self):
        with pytest.raises(ValueError, match="pattern_name"):
            DetectedPattern(
                pattern_name="   ",
                pattern_type="custom",
                severity="low",
                occurrence_count=3,
                first_seen="t",
                last_seen="t",
                affected_agents=(),
                error_ids=(),
            )

    def test_zero_occurrence_count_raises(self):
        with pytest.raises(ValueError, match="occurrence_count"):
            DetectedPattern(
                pattern_name="test",
                pattern_type="custom",
                severity="low",
                occurrence_count=0,
                first_seen="t",
                last_seen="t",
                affected_agents=(),
                error_ids=(),
            )

    def test_invalid_severity_raises(self):
        with pytest.raises(ValueError, match="severity"):
            DetectedPattern(
                pattern_name="test",
                pattern_type="custom",
                severity="extreme",
                occurrence_count=3,
                first_seen="t",
                last_seen="t",
                affected_agents=(),
                error_ids=(),
            )

    def test_frozen(self):
        dp = DetectedPattern(
            pattern_name="test", pattern_type="custom", severity="low",
            occurrence_count=3, first_seen="t", last_seen="t",
            affected_agents=(), error_ids=(),
        )
        with pytest.raises((AttributeError, TypeError)):
            dp.occurrence_count = 10  # type: ignore


class TestGetLessonsScored:
    def test_empty_store_returns_empty(self, event_store):
        result = _get_lessons_scored(event_store._conn)
        assert result == []

    def test_returns_lessons(self, event_store, sample_lesson):
        event_store.log_lesson(sample_lesson)
        result = _get_lessons_scored(event_store._conn)
        assert len(result) == 1
        assert isinstance(result[0], ScoredLesson)

    def test_agent_match_boosts_score(self, event_store):
        # Lesson with matching agent
        lesson_match = Lesson(
            problem="test",
            agents_involved=("backend",),
            confidence=0.5,
        )
        # Lesson without matching agent
        lesson_no_match = Lesson(
            problem="other test",
            agents_involved=("frontend",),
            confidence=0.5,
        )
        event_store.log_lesson(lesson_match)
        event_store.log_lesson(lesson_no_match)

        result = _get_lessons_scored(event_store._conn, agent="backend")
        # First result should be the matching one
        assert result[0].agents_involved == ("backend",)
        assert result[0].score > result[1].score

    def test_project_match_boosts_score(self, event_store):
        l_match = Lesson(problem="p1", project="my-project", confidence=0.5)
        l_no_match = Lesson(problem="p2", project="other", confidence=0.5)
        event_store.log_lesson(l_match)
        event_store.log_lesson(l_no_match)

        result = _get_lessons_scored(event_store._conn, project="my-project")
        assert result[0].project == "my-project"

    def test_limit_applied(self, event_store):
        for _ in range(10):
            event_store.log_lesson(Lesson(problem="test"))
        result = _get_lessons_scored(event_store._conn, limit=3)
        assert len(result) == 3

    def test_only_active_lessons_returned(self, event_store):
        active = Lesson(problem="active", status="active")
        resolved = Lesson(problem="resolved", status="resolved")
        suppressed = Lesson(problem="suppressed", status="suppressed")
        event_store.log_lesson(active)
        event_store.log_lesson(resolved)
        event_store.log_lesson(suppressed)

        result = _get_lessons_scored(event_store._conn)
        assert len(result) == 1
        assert result[0].problem == "active"

    def test_high_confidence_boosts_score(self, event_store):
        low_conf = Lesson(problem="low", confidence=0.5)
        high_conf = Lesson(problem="high", confidence=0.95)
        event_store.log_lesson(low_conf)
        event_store.log_lesson(high_conf)

        result = _get_lessons_scored(event_store._conn)
        assert result[0].problem == "high"

    def test_severity_affects_score(self, event_store):
        low_sev = Lesson(problem="low", severity="low", confidence=0.5)
        crit_sev = Lesson(problem="crit", severity="critical", confidence=0.5)
        event_store.log_lesson(low_sev)
        event_store.log_lesson(crit_sev)

        result = _get_lessons_scored(event_store._conn)
        assert result[0].severity == "critical"


class TestDetectPatterns:
    def _make_error(self, store, message: str, agent: str = "backend", count: int = 1):
        for _ in range(count):
            store.log_event(
                Event(
                    event_type="task_failed",
                    agent_name=agent,
                    success=False,
                    error_message=message,
                )
            )

    def test_empty_store_returns_empty(self, event_store):
        result = _detect_patterns(event_store._conn)
        assert result == []

    def test_no_errors_returns_empty(self, event_store):
        event_store.log_event(Event(event_type="task_completed", success=True))
        result = _detect_patterns(event_store._conn)
        assert result == []

    def test_detects_cluster(self, event_store):
        self._make_error(event_store, "Connection timeout after 30s", count=3)
        result = _detect_patterns(event_store._conn, min_occurrences=3)
        assert len(result) == 1

    def test_below_threshold_not_detected(self, event_store):
        self._make_error(event_store, "Connection timeout after 30s", count=2)
        result = _detect_patterns(event_store._conn, min_occurrences=3)
        assert len(result) == 0

    def test_similar_errors_grouped(self, event_store):
        # These should be similar enough to cluster
        self._make_error(event_store, "Cannot read property 'x' of undefined")
        self._make_error(event_store, "Cannot read property 'y' of undefined")
        self._make_error(event_store, "Cannot read property 'z' of undefined")
        result = _detect_patterns(event_store._conn, min_occurrences=3)
        assert len(result) == 1
        assert result[0].occurrence_count == 3

    def test_different_errors_not_grouped(self, event_store):
        # Very different messages - should not cluster
        self._make_error(event_store, "Connection refused at port 5432", count=3)
        self._make_error(event_store, "Import error: module not found", count=3)
        result = _detect_patterns(event_store._conn, min_occurrences=3)
        assert len(result) == 2

    def test_severity_inferred(self, event_store):
        # 10+ occurrences = critical
        self._make_error(event_store, "DB timeout", count=10)
        result = _detect_patterns(event_store._conn, min_occurrences=3)
        assert result[0].severity == "critical"

    def test_affected_agents_collected(self, event_store):
        event_store.log_event(Event(event_type="task_failed", success=False,
                                   error_message="DB error", agent_name="backend"))
        event_store.log_event(Event(event_type="task_failed", success=False,
                                   error_message="DB error", agent_name="frontend"))
        event_store.log_event(Event(event_type="task_failed", success=False,
                                   error_message="DB error", agent_name="tester"))
        result = _detect_patterns(event_store._conn, min_occurrences=3)
        assert len(result) == 1
        assert "backend" in result[0].affected_agents
        assert "frontend" in result[0].affected_agents

    def test_pattern_name_truncated(self, event_store):
        long_msg = "A" * 200
        self._make_error(event_store, long_msg, count=3)
        result = _detect_patterns(event_store._conn, min_occurrences=3)
        assert len(result[0].pattern_name) <= 100

    def test_sorted_by_severity(self, event_store):
        self._make_error(event_store, "Minor issue", count=3)   # medium
        self._make_error(event_store, "Critical system failure", count=10)  # critical
        result = _detect_patterns(event_store._conn, min_occurrences=3)
        assert result[0].severity == "critical"

    def test_days_filter(self, event_store):
        # Recent errors (always within 1 day)
        self._make_error(event_store, "Recent timeout", count=3)
        result = _detect_patterns(event_store._conn, days=1, min_occurrences=3)
        assert len(result) == 1

    def test_returns_detected_pattern_instances(self, event_store):
        self._make_error(event_store, "DB error", count=3)
        result = _detect_patterns(event_store._conn, min_occurrences=3)
        assert isinstance(result[0], DetectedPattern)


class TestAgentStats:
    def test_empty_store(self, event_store):
        result = _agent_stats(event_store._conn)
        assert result == []

    def test_agent_appears_in_stats(self, populated_store):
        result = _agent_stats(populated_store._conn)
        agent_names = [r["agent_name"] for r in result]
        assert "backend" in agent_names

    def test_success_rate_calculation(self, event_store):
        event_store.log_event(Event(event_type="task_completed", agent_name="a", success=True))
        event_store.log_event(Event(event_type="task_failed", agent_name="a", success=False))
        result = _agent_stats(event_store._conn)
        assert len(result) == 1
        assert result[0]["success_rate"] == 0.5
        assert result[0]["total_tasks"] == 2
        assert result[0]["successful_tasks"] == 1
        assert result[0]["failed_tasks"] == 1

    def test_project_filter(self, populated_store):
        result = _agent_stats(populated_store._conn, project="test-project")
        # Only backend and frontend have events in test-project
        agent_names = [r["agent_name"] for r in result]
        assert "backend" in agent_names

    def test_sorted_by_total_tasks_desc(self, event_store):
        for _ in range(5):
            event_store.log_event(Event(event_type="task_completed", agent_name="heavy"))
        event_store.log_event(Event(event_type="task_completed", agent_name="light"))
        result = _agent_stats(event_store._conn)
        assert result[0]["agent_name"] == "heavy"

    def test_avg_duration_ms(self, event_store):
        event_store.log_event(Event(event_type="task_completed", agent_name="a", duration_ms=100))
        event_store.log_event(Event(event_type="task_completed", agent_name="a", duration_ms=200))
        result = _agent_stats(event_store._conn)
        assert result[0]["avg_duration_ms"] == 150.0

    def test_avg_duration_none_when_no_durations(self, event_store):
        event_store.log_event(Event(event_type="task_completed", agent_name="a"))
        result = _agent_stats(event_store._conn)
        assert result[0]["avg_duration_ms"] is None


class TestGetRelevantLessons:
    def test_public_alias_works(self, event_store, sample_lesson):
        event_store.log_lesson(sample_lesson)
        result = get_relevant_lessons(event_store._conn)
        assert len(result) == 1

    def test_accepts_agent_and_project(self, event_store, sample_lesson):
        event_store.log_lesson(sample_lesson)
        result = get_relevant_lessons(event_store._conn, agent="backend", project="test-project")
        assert len(result) == 1
