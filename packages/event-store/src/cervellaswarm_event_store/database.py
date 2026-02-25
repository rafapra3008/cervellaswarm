# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""
Core EventStore class - SQLite backend for agent event tracking.

Provides a context-manager-aware class that owns a single SQLite connection.
Uses WAL mode for concurrent reads and fast writes.

Supports ':memory:' path for fast in-process testing.
"""

import sqlite3
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cervellaswarm_event_store.writer import Event, Lesson
    from cervellaswarm_event_store.reader import QueryResult, Statistics
    from cervellaswarm_event_store.analytics import DetectedPattern, ScoredLesson


_CREATE_EVENTS = """
CREATE TABLE IF NOT EXISTS events (
    id TEXT PRIMARY KEY,
    timestamp TEXT NOT NULL,
    session_id TEXT,
    event_type TEXT NOT NULL,
    agent_name TEXT,
    agent_role TEXT,
    task_id TEXT,
    parent_task_id TEXT,
    description TEXT,
    status TEXT,
    duration_ms INTEGER,
    success INTEGER,
    error_message TEXT,
    project TEXT,
    files_modified TEXT,
    tags TEXT,
    metadata TEXT,
    created_at TEXT DEFAULT (datetime('now'))
)
"""

_CREATE_LESSONS = """
CREATE TABLE IF NOT EXISTS lessons (
    id TEXT PRIMARY KEY,
    timestamp TEXT NOT NULL,
    context TEXT,
    problem TEXT,
    solution TEXT,
    pattern TEXT,
    category TEXT,
    severity TEXT DEFAULT 'medium',
    root_cause TEXT,
    prevention TEXT,
    agents_involved TEXT,
    project TEXT,
    confidence REAL DEFAULT 0.5,
    times_applied INTEGER DEFAULT 0,
    status TEXT DEFAULT 'active',
    tags TEXT,
    created_at TEXT DEFAULT (datetime('now'))
)
"""

_CREATE_ERROR_PATTERNS = """
CREATE TABLE IF NOT EXISTS error_patterns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pattern_name TEXT UNIQUE NOT NULL,
    pattern_type TEXT NOT NULL,
    first_seen TEXT NOT NULL,
    last_seen TEXT NOT NULL,
    occurrence_count INTEGER DEFAULT 1,
    severity TEXT DEFAULT 'medium',
    error_signature TEXT,
    affected_agents TEXT,
    root_cause TEXT,
    mitigation_applied INTEGER DEFAULT 0,
    mitigation_description TEXT,
    status TEXT DEFAULT 'active'
)
"""

_INDICES = [
    "CREATE INDEX IF NOT EXISTS idx_events_timestamp ON events(timestamp DESC)",
    "CREATE INDEX IF NOT EXISTS idx_events_agent ON events(agent_name)",
    "CREATE INDEX IF NOT EXISTS idx_events_project ON events(project)",
    "CREATE INDEX IF NOT EXISTS idx_events_session ON events(session_id)",
    "CREATE INDEX IF NOT EXISTS idx_events_type ON events(event_type)",
    "CREATE INDEX IF NOT EXISTS idx_events_status ON events(status)",
    "CREATE INDEX IF NOT EXISTS idx_lessons_confidence ON lessons(confidence DESC)",
    "CREATE INDEX IF NOT EXISTS idx_lessons_status ON lessons(status)",
    "CREATE INDEX IF NOT EXISTS idx_lessons_project ON lessons(project)",
    "CREATE INDEX IF NOT EXISTS idx_patterns_severity ON error_patterns(severity)",
    "CREATE INDEX IF NOT EXISTS idx_patterns_status ON error_patterns(status)",
]

from cervellaswarm_event_store.writer import _VALID_EVENT_TYPES, _VALID_SEVERITIES


class EventStore:
    """SQLite-backed event store for AI agent session tracking.

    Owns a single database connection. Use as a context manager for automatic
    cleanup, or call close() explicitly.

    Args:
        db_path: Path to SQLite file, or ':memory:' for in-process testing.
                 If None, resolves from config / env var.

    Example::

        with EventStore(':memory:') as store:
            store.log_event(event)
            result = store.query_events(project='demo')
    """

    def __init__(self, db_path: "Path | str | None" = None) -> None:
        if db_path is None:
            from cervellaswarm_event_store.config import get_db_path

            resolved = get_db_path()
        elif isinstance(db_path, str) and db_path == ":memory:":
            resolved = Path(":memory:")
        else:
            resolved = Path(db_path)

        self._db_path = resolved
        self._conn: "sqlite3.Connection | None" = None
        self._connect()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _connect(self) -> None:
        """Open connection and initialize schema."""
        db_path_str = str(self._db_path)

        if db_path_str != ":memory:":
            # Ensure parent directory exists
            self._db_path.parent.mkdir(parents=True, exist_ok=True)

        conn = sqlite3.connect(db_path_str)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=NORMAL")
        conn.execute("PRAGMA foreign_keys=ON")

        self._conn = conn
        self._init_schema()

    def _init_schema(self) -> None:
        """Create tables and indices if they do not exist."""
        if self._conn is None:
            raise RuntimeError("Cannot initialize schema: connection is None")
        cursor = self._conn.cursor()
        cursor.execute(_CREATE_EVENTS)
        cursor.execute(_CREATE_LESSONS)
        cursor.execute(_CREATE_ERROR_PATTERNS)
        for idx in _INDICES:
            cursor.execute(idx)
        self._conn.commit()

    def _require_conn(self) -> sqlite3.Connection:
        """Return the active connection, raising if closed."""
        if self._conn is None:
            raise RuntimeError("EventStore is closed. Use as context manager or open a new instance.")
        return self._conn

    # ------------------------------------------------------------------
    # Context manager
    # ------------------------------------------------------------------

    def __enter__(self) -> "EventStore":
        return self

    def __exit__(self, exc_type: object, exc_val: object, exc_tb: object) -> None:
        self.close()

    def close(self) -> None:
        """Close the database connection."""
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    # ------------------------------------------------------------------
    # Public write API (delegates to writer module)
    # ------------------------------------------------------------------

    def log_event(self, event: "Event") -> str:
        """Insert an event record and return its id.

        Args:
            event: Event dataclass instance (frozen).

        Returns:
            The event id string (UUID).
        """
        from cervellaswarm_event_store.writer import _insert_event

        return _insert_event(self._require_conn(), event)

    def log_lesson(self, lesson: "Lesson") -> str:
        """Insert a lesson record and return its id.

        Args:
            lesson: Lesson dataclass instance (frozen).

        Returns:
            The lesson id string (UUID).
        """
        from cervellaswarm_event_store.writer import _insert_lesson

        return _insert_lesson(self._require_conn(), lesson)

    # ------------------------------------------------------------------
    # Public read API (delegates to reader module)
    # ------------------------------------------------------------------

    def query_events(
        self,
        *,
        agent: str = "",
        project: str = "",
        event_type: str = "",
        session_id: str = "",
        status: str = "",
        success: "bool | None" = None,
        days: int = 0,
        limit: int = 50,
    ) -> "QueryResult":
        """Query events with optional filters.

        Args:
            agent: Filter by agent_name (exact match).
            project: Filter by project (exact match).
            event_type: Filter by event_type (exact match).
            session_id: Filter by session_id (exact match).
            status: Filter by status field (exact match).
            success: Filter by success flag. None = no filter.
            days: Only return events from the last N days. 0 = no limit.
            limit: Maximum number of rows to return (default 50).

        Returns:
            QueryResult frozen dataclass.
        """
        from cervellaswarm_event_store.reader import _query_events

        return _query_events(
            self._require_conn(),
            agent=agent,
            project=project,
            event_type=event_type,
            session_id=session_id,
            status=status,
            success=success,
            days=days,
            limit=limit,
        )

    def get_statistics(self, project: str = "") -> "Statistics":
        """Return aggregated statistics.

        Args:
            project: If non-empty, scope stats to this project.

        Returns:
            Statistics frozen dataclass.
        """
        from cervellaswarm_event_store.reader import _get_statistics

        return _get_statistics(self._require_conn(), project=project)

    def get_lessons(
        self,
        agent: str = "",
        project: str = "",
        limit: int = 10,
    ) -> "list[ScoredLesson]":
        """Return lessons sorted by relevance score.

        Args:
            agent: Boost lessons that mention this agent.
            project: Boost lessons linked to this project.
            limit: Maximum number of lessons to return.

        Returns:
            List of ScoredLesson sorted by score desc.
        """
        from cervellaswarm_event_store.analytics import _get_lessons_scored

        return _get_lessons_scored(self._require_conn(), agent=agent, project=project, limit=limit)

    # ------------------------------------------------------------------
    # Analytics API (delegates to analytics module)
    # ------------------------------------------------------------------

    def detect_patterns(
        self,
        days: int = 7,
        min_occurrences: int = 3,
        similarity_threshold: float = 0.7,
    ) -> "list[DetectedPattern]":
        """Detect recurring error patterns using similarity clustering.

        Args:
            days: Analyse errors from the last N days.
            min_occurrences: Minimum cluster size to report.
            similarity_threshold: Minimum SequenceMatcher ratio to cluster (0.0-1.0).

        Returns:
            List of DetectedPattern sorted by severity then occurrence_count.
        """
        from cervellaswarm_event_store.analytics import _detect_patterns

        return _detect_patterns(
            self._require_conn(),
            days=days,
            min_occurrences=min_occurrences,
            similarity_threshold=similarity_threshold,
        )

    def agent_stats(self, project: str = "") -> "list[dict]":
        """Return per-agent aggregated statistics.

        Args:
            project: Scope to a specific project. Empty = all projects.

        Returns:
            List of dicts with keys: agent_name, total_tasks, successful_tasks,
            failed_tasks, success_rate, avg_duration_ms, projects.
        """
        from cervellaswarm_event_store.analytics import _agent_stats

        return _agent_stats(self._require_conn(), project=project)

    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------

    @property
    def db_path(self) -> Path:
        """Return the database path."""
        return self._db_path

    @property
    def is_open(self) -> bool:
        """Return True if the connection is open."""
        return self._conn is not None

    def get_valid_event_types(self) -> frozenset:
        """Return the set of recognised event type strings."""
        return _VALID_EVENT_TYPES

    def get_valid_severities(self) -> frozenset:
        """Return the set of recognised severity strings."""
        return _VALID_SEVERITIES
