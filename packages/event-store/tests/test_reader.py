# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for cervellaswarm_event_store.reader module."""

import pytest

from cervellaswarm_event_store.writer import Event, Lesson
from cervellaswarm_event_store.reader import (
    AgentSummary,
    EventRecord,
    QueryResult,
    Statistics,
    _parse_json_field,
    _parse_json_dict,
)


class TestParseJsonField:
    def test_empty_string_returns_empty_tuple(self):
        assert _parse_json_field("") == ()

    def test_none_returns_empty_tuple(self):
        assert _parse_json_field(None) == ()

    def test_valid_array(self):
        assert _parse_json_field('["a", "b"]') == ("a", "b")

    def test_non_array_returns_empty(self):
        assert _parse_json_field('{"key": "val"}') == ()

    def test_invalid_json_returns_empty(self):
        assert _parse_json_field("not-json") == ()


class TestParseJsonDict:
    def test_none_returns_none(self):
        assert _parse_json_dict(None) is None

    def test_empty_string_returns_none(self):
        assert _parse_json_dict("") is None

    def test_valid_dict(self):
        result = _parse_json_dict('{"key": "val"}')
        assert result == {"key": "val"}

    def test_non_dict_returns_none(self):
        assert _parse_json_dict('["a"]') is None

    def test_invalid_json_returns_none(self):
        assert _parse_json_dict("not-json") is None


class TestQueryResultDataclass:
    def test_valid_creation(self):
        qr = QueryResult(events=(), total=0, filters_applied={})
        assert qr.total == 0

    def test_negative_total_raises(self):
        with pytest.raises(ValueError, match="total"):
            QueryResult(events=(), total=-1, filters_applied={})

    def test_total_mismatch_raises(self):
        with pytest.raises(ValueError, match="total"):
            QueryResult(events=(1, 2), total=1, filters_applied={})

    def test_frozen(self):
        qr = QueryResult(events=(), total=0, filters_applied={})
        with pytest.raises((AttributeError, TypeError)):
            qr.total = 5  # type: ignore


class TestStatisticsDataclass:
    def test_valid_creation(self):
        stats = Statistics(
            total_events=10,
            total_lessons=2,
            total_patterns=1,
            success_count=8,
            fail_count=2,
            success_rate=0.8,
            by_agent=(),
            by_project={},
            by_event_type={},
        )
        assert stats.success_rate == 0.8

    def test_negative_total_events_raises(self):
        with pytest.raises(ValueError):
            Statistics(
                total_events=-1,
                total_lessons=0,
                total_patterns=0,
                success_count=0,
                fail_count=0,
                success_rate=0.0,
                by_agent=(),
                by_project={},
                by_event_type={},
            )

    def test_invalid_success_rate_raises(self):
        with pytest.raises(ValueError, match="success_rate"):
            Statistics(
                total_events=10,
                total_lessons=0,
                total_patterns=0,
                success_count=5,
                fail_count=5,
                success_rate=1.5,
                by_agent=(),
                by_project={},
                by_event_type={},
            )


class TestAgentSummaryDataclass:
    def test_valid_creation(self):
        s = AgentSummary(agent_name="backend", event_count=10, success_count=8, fail_count=2)
        assert s.agent_name == "backend"

    def test_negative_event_count_raises(self):
        with pytest.raises(ValueError):
            AgentSummary(agent_name="x", event_count=-1, success_count=0, fail_count=0)

    def test_frozen(self):
        s = AgentSummary(agent_name="x", event_count=1, success_count=1, fail_count=0)
        with pytest.raises((AttributeError, TypeError)):
            s.agent_name = "y"  # type: ignore


class TestQueryEvents:
    def test_query_all(self, populated_store):
        result = populated_store.query_events()
        assert result.total == 4

    def test_query_by_agent(self, populated_store):
        result = populated_store.query_events(agent="backend")
        assert result.total == 2
        for ev in result.events:
            assert ev.agent_name == "backend"

    def test_query_by_project(self, populated_store):
        result = populated_store.query_events(project="test-project")
        assert result.total == 3

    def test_query_by_event_type(self, populated_store):
        result = populated_store.query_events(event_type="task_failed")
        assert result.total == 2

    def test_query_by_success(self, populated_store):
        result = populated_store.query_events(success=True)
        assert result.total == 1

    def test_query_by_failure(self, populated_store):
        result = populated_store.query_events(success=False)
        assert result.total == 2

    def test_query_by_session_id(self, populated_store):
        result = populated_store.query_events(session_id="sess-001")
        assert result.total == 1

    def test_query_limit(self, populated_store):
        result = populated_store.query_events(limit=2)
        assert result.total == 2

    def test_query_sorted_desc(self, populated_store):
        result = populated_store.query_events()
        timestamps = [ev.timestamp for ev in result.events]
        assert timestamps == sorted(timestamps, reverse=True)

    def test_query_empty_store(self, event_store):
        result = event_store.query_events()
        assert result.total == 0
        assert result.events == ()

    def test_filters_applied_recorded(self, populated_store):
        result = populated_store.query_events(agent="backend", project="test-project")
        assert result.filters_applied["agent"] == "backend"
        assert result.filters_applied["project"] == "test-project"

    def test_no_filters_applied_empty_dict(self, populated_store):
        result = populated_store.query_events()
        assert result.filters_applied == {}

    def test_event_record_types(self, event_store, sample_event):
        event_store.log_event(sample_event)
        result = event_store.query_events()
        ev = result.events[0]
        assert isinstance(ev, EventRecord)
        assert isinstance(ev.files_modified, tuple)
        assert isinstance(ev.tags, tuple)

    def test_query_days_filter(self, event_store):
        # Insert a recent event - should appear in last 1 day
        recent = Event(event_type="task_completed", project="fresh")
        event_store.log_event(recent)
        result = event_store.query_events(days=1)
        assert result.total == 1

    def test_combined_filters(self, populated_store):
        result = populated_store.query_events(
            agent="backend", project="test-project", event_type="task_completed"
        )
        assert result.total == 1

    def test_limit_one(self, populated_store):
        result = populated_store.query_events(limit=1)
        assert result.total == 1

    def test_success_none_returns_all(self, populated_store):
        result = populated_store.query_events(success=None)
        # All events including those with NULL success
        assert result.total == 4


class TestGetStatistics:
    def test_empty_store(self, event_store):
        stats = event_store.get_statistics()
        assert stats.total_events == 0
        assert stats.total_lessons == 0
        assert stats.success_rate == 0.0

    def test_counts_events(self, populated_store):
        stats = populated_store.get_statistics()
        assert stats.total_events == 4

    def test_counts_lessons(self, populated_store):
        stats = populated_store.get_statistics()
        assert stats.total_lessons == 1

    def test_success_rate(self, event_store):
        event_store.log_event(Event(event_type="task_completed", success=True))
        event_store.log_event(Event(event_type="task_failed", success=False))
        stats = event_store.get_statistics()
        assert stats.success_count == 1
        assert stats.fail_count == 1
        assert stats.success_rate == 0.5

    def test_by_agent(self, populated_store):
        stats = populated_store.get_statistics()
        agent_names = [a.agent_name for a in stats.by_agent]
        assert "backend" in agent_names

    def test_by_project(self, populated_store):
        stats = populated_store.get_statistics()
        assert "test-project" in stats.by_project

    def test_by_event_type(self, populated_store):
        stats = populated_store.get_statistics()
        assert "task_completed" in stats.by_event_type
        assert "task_failed" in stats.by_event_type

    def test_project_filter(self, populated_store):
        stats = populated_store.get_statistics(project="test-project")
        assert stats.project_filter == "test-project"
        # other-project events should not be counted
        assert stats.total_events == 3

    def test_returns_statistics_dataclass(self, event_store):
        result = event_store.get_statistics()
        assert isinstance(result, Statistics)

    def test_success_rate_no_events(self, event_store):
        stats = event_store.get_statistics()
        assert stats.success_rate == 0.0
