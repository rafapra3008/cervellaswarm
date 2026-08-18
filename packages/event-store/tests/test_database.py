# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for cervellaswarm_event_store.database module."""

import sqlite3
from pathlib import Path

import pytest
from cervellaswarm_event_store.database import EventStore
from cervellaswarm_event_store.writer import Event, Lesson


class TestEventStoreInit:
    def test_memory_store_created(self):
        store = EventStore(":memory:")
        assert store.is_open
        store.close()

    def test_file_store_created(self, tmp_path):
        db = tmp_path / "test.db"
        store = EventStore(db)
        assert store.is_open
        assert db.exists()
        store.close()

    def test_creates_parent_dirs(self, tmp_path):
        db = tmp_path / "nested" / "dir" / "test.db"
        store = EventStore(db)
        assert db.exists()
        store.close()

    def test_db_path_property(self):
        store = EventStore(":memory:")
        assert store.db_path == Path(":memory:")
        store.close()

    def test_db_path_absolute_for_file(self, tmp_path):
        db = tmp_path / "test.db"
        store = EventStore(db)
        assert store.db_path.is_absolute() or str(store.db_path) == ":memory:"
        store.close()

    def test_schema_created_on_init(self):
        store = EventStore(":memory:")
        conn = store._conn
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = {row[0] for row in cursor.fetchall()}
        assert "events" in tables
        assert "lessons" in tables
        assert "error_patterns" in tables
        store.close()

    def test_indices_created(self):
        store = EventStore(":memory:")
        conn = store._conn
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name LIKE 'idx_%'")
        indices = [row[0] for row in cursor.fetchall()]
        assert len(indices) >= 8
        store.close()

    def test_wal_mode_active(self):
        store = EventStore(":memory:")
        cursor = store._conn.cursor()
        cursor.execute("PRAGMA journal_mode")
        mode = cursor.fetchone()[0]
        # memory DBs return 'memory' mode, WAL applies to file DBs
        assert mode in ("wal", "memory")
        store.close()


class TestEventStoreContextManager:
    def test_context_manager_closes_on_exit(self):
        with EventStore(":memory:") as store:
            assert store.is_open
        assert not store.is_open

    def test_context_manager_closes_on_exception(self):
        store_ref = None
        try:
            with EventStore(":memory:") as store:
                store_ref = store
                raise ValueError("boom")
        except ValueError:
            pass
        assert store_ref is not None
        assert not store_ref.is_open

    def test_close_is_idempotent(self):
        store = EventStore(":memory:")
        store.close()
        store.close()  # should not raise
        assert not store.is_open

    def test_operations_after_close_raise(self):
        store = EventStore(":memory:")
        store.close()
        with pytest.raises(RuntimeError, match="closed"):
            store.query_events()


class TestEventStoreLogEvent:
    def test_log_event_returns_id(self, event_store, sample_event):
        event_id = event_store.log_event(sample_event)
        assert event_id == sample_event.id
        assert len(event_id) == 36  # UUID format

    def test_log_event_persists(self, event_store, sample_event):
        event_store.log_event(sample_event)
        result = event_store.query_events()
        assert result.total == 1
        assert result.events[0].id == sample_event.id

    def test_log_multiple_events(self, event_store, sample_event):
        for _ in range(5):
            event_store.log_event(
                Event(
                    event_type="task_completed",
                    agent_name="backend",
                    project="proj",
                )
            )
        result = event_store.query_events()
        assert result.total == 5

    def test_log_event_with_files_modified(self, event_store):
        event = Event(
            event_type="task_completed",
            agent_name="backend",
            files_modified=("src/app.py", "tests/test_app.py"),
        )
        event_store.log_event(event)
        result = event_store.query_events()
        assert result.events[0].files_modified == ("src/app.py", "tests/test_app.py")

    def test_log_event_with_tags(self, event_store):
        event = Event(
            event_type="custom",
            tags=("refactor", "backend"),
        )
        event_store.log_event(event)
        result = event_store.query_events()
        assert "refactor" in result.events[0].tags

    def test_log_event_with_metadata(self, event_store):
        event = Event(
            event_type="custom",
            metadata={"key": "value", "count": 42},
        )
        event_store.log_event(event)
        result = event_store.query_events()
        assert result.events[0].metadata == {"key": "value", "count": 42}

    def test_log_failed_event(self, event_store):
        event = Event(
            event_type="task_failed",
            agent_name="backend",
            success=False,
            error_message="DB connection refused",
        )
        event_store.log_event(event)
        result = event_store.query_events(success=False)
        assert result.total == 1
        assert result.events[0].error_message == "DB connection refused"


class TestEventStoreLogLesson:
    def test_log_lesson_returns_id(self, event_store, sample_lesson):
        lesson_id = event_store.log_lesson(sample_lesson)
        assert lesson_id == sample_lesson.id

    def test_log_lesson_persists(self, event_store, sample_lesson):
        event_store.log_lesson(sample_lesson)
        stats = event_store.get_statistics()
        assert stats.total_lessons == 1


class TestEventStoreGetValidTypes:
    def test_returns_frozenset(self, event_store):
        types = event_store.get_valid_event_types()
        assert isinstance(types, frozenset)

    def test_contains_expected_types(self, event_store):
        types = event_store.get_valid_event_types()
        assert "task_completed" in types
        assert "task_failed" in types
        assert "session_started" in types

    def test_severities_frozenset(self, event_store):
        severities = event_store.get_valid_severities()
        assert isinstance(severities, frozenset)
        assert "critical" in severities


# ---------------------------------------------------------------------------
# Migration Framework Tests (S511)
# ---------------------------------------------------------------------------

class TestMigrationFramework:
    """Tests for SCHEMA_VERSION, PRAGMA user_version, and migration loop."""

    def test_new_db_has_correct_version(self):
        """Fresh DB gets SCHEMA_VERSION set via PRAGMA user_version."""
        from cervellaswarm_event_store.database import SCHEMA_VERSION, EventStore
        es = EventStore(":memory:")
        v = es._conn.execute("PRAGMA user_version").fetchone()[0]
        assert v == SCHEMA_VERSION
        es.close()

    def test_schema_version_is_positive(self):
        """SCHEMA_VERSION must be a positive integer."""
        from cervellaswarm_event_store.database import SCHEMA_VERSION
        assert isinstance(SCHEMA_VERSION, int)
        assert SCHEMA_VERSION >= 1

    def test_busy_timeout_set(self):
        """PRAGMA busy_timeout should be 5000ms."""
        from cervellaswarm_event_store.database import EventStore
        es = EventStore(":memory:")
        bt = es._conn.execute("PRAGMA busy_timeout").fetchone()[0]
        assert bt == 5000
        es.close()

    def test_wal_mode_for_file_db(self, tmp_path):
        """File-based DB uses WAL journal mode."""
        from cervellaswarm_event_store.database import EventStore
        db_path = tmp_path / "test.db"
        es = EventStore(str(db_path))
        jm = es._conn.execute("PRAGMA journal_mode").fetchone()[0]
        assert jm == "wal"
        es.close()

    def test_idempotent_schema_init(self):
        """Opening same DB twice doesn't fail or change version."""
        from cervellaswarm_event_store.database import SCHEMA_VERSION, EventStore
        es1 = EventStore(":memory:")
        # Simulate re-init on same connection
        es1._init_schema()
        v = es1._conn.execute("PRAGMA user_version").fetchone()[0]
        assert v == SCHEMA_VERSION
        es1.close()

    def test_migration_v2_adds_session_columns(self, tmp_path):
        """Migration v1->v2 adds 6 session observability columns."""
        db_path = tmp_path / "migrate.db"
        # Create v1 DB manually (without new columns)
        conn = sqlite3.connect(str(db_path))
        conn.execute("""
            CREATE TABLE IF NOT EXISTS token_usage (
                id TEXT PRIMARY KEY, timestamp TEXT NOT NULL,
                session_id TEXT NOT NULL UNIQUE, project TEXT, model TEXT,
                input_tokens INTEGER DEFAULT 0, output_tokens INTEGER DEFAULT 0,
                cache_read_tokens INTEGER DEFAULT 0, cache_creation_tokens INTEGER DEFAULT 0,
                total_messages INTEGER DEFAULT 0, total_tool_calls INTEGER DEFAULT 0,
                cost_usd REAL DEFAULT 0.0, created_at TEXT DEFAULT (datetime('now'))
            )
        """)
        conn.execute("PRAGMA user_version = 1")
        conn.commit()
        conn.close()

        # Open with EventStore -- migration should apply
        es = EventStore(str(db_path))
        v = es._conn.execute("PRAGMA user_version").fetchone()[0]
        assert v == 2

        # Verify new columns exist by inserting with them
        es._conn.execute(
            "INSERT INTO token_usage (id, timestamp, session_id, start_time, end_time, duration_seconds, agent_names, tasks_completed, errors_count) "
            "VALUES ('t1', '2026-04-05', 's1', '2026-04-05T10:00:00Z', '2026-04-05T11:00:00Z', 3600, '[\"cervella-tester\"]', 5, 1)"
        )
        row = es._conn.execute("SELECT start_time, duration_seconds, agent_names, tasks_completed, errors_count FROM token_usage WHERE id='t1'").fetchone()
        assert row[0] == "2026-04-05T10:00:00Z"
        assert row[1] == 3600
        assert row[2] == '["cervella-tester"]'
        assert row[3] == 5
        assert row[4] == 1
        es.close()

    def test_fresh_db_has_session_columns(self):
        """New DB (no migration needed) has session columns from CREATE TABLE."""
        es = EventStore(":memory:")
        es._conn.execute(
            "INSERT INTO token_usage (id, timestamp, session_id, start_time, duration_seconds) "
            "VALUES ('t2', '2026-04-05', 's2', '2026-04-05T10:00:00Z', 1800)"
        )
        row = es._conn.execute("SELECT start_time, duration_seconds FROM token_usage WHERE id='t2'").fetchone()
        assert row[0] == "2026-04-05T10:00:00Z"
        assert row[1] == 1800
        es.close()
