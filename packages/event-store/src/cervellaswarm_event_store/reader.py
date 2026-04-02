# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""
Read functions for cervellaswarm-event-store.

query_events: flexible multi-filter query returning a QueryResult.
get_statistics: aggregated counts / rates returning a Statistics dataclass.

All result types are frozen dataclasses.
"""

import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Optional


@dataclass(frozen=True)
class EventRecord:
    """A single event row returned by a query.

    All fields may be None when the column was NULL in the database.
    """

    id: str
    timestamp: str
    event_type: str
    session_id: Optional[str]
    agent_name: Optional[str]
    agent_role: Optional[str]
    task_id: Optional[str]
    parent_task_id: Optional[str]
    description: Optional[str]
    status: Optional[str]
    duration_ms: Optional[int]
    success: Optional[bool]
    error_message: Optional[str]
    project: Optional[str]
    files_modified: tuple
    tags: tuple
    metadata: Optional[dict]
    created_at: Optional[str]


@dataclass(frozen=True)
class QueryResult:
    """Result of a query_events call.

    Attributes:
        events: Tuple of matching EventRecord objects.
        total: Number of events returned (== len(events)).
        filters_applied: Dict of filters that were active.
    """

    events: tuple
    total: int
    filters_applied: dict

    def __post_init__(self) -> None:
        if self.total < 0:
            raise ValueError("total must be >= 0")
        if len(self.events) != self.total:
            raise ValueError("total must equal len(events)")


@dataclass(frozen=True)
class AgentSummary:
    """Per-agent event summary within Statistics.

    Attributes:
        agent_name: Name of the agent.
        event_count: Total number of events logged.
        success_count: Events with success=True.
        fail_count: Events with success=False.
    """

    agent_name: str
    event_count: int
    success_count: int
    fail_count: int

    def __post_init__(self) -> None:
        if self.event_count < 0:
            raise ValueError("event_count must be >= 0")
        if self.success_count < 0:
            raise ValueError("success_count must be >= 0")
        if self.fail_count < 0:
            raise ValueError("fail_count must be >= 0")


@dataclass(frozen=True)
class Statistics:
    """Aggregated statistics for the event store.

    Attributes:
        total_events: Total number of event rows.
        total_lessons: Total number of lesson rows.
        total_patterns: Total number of error_pattern rows.
        success_count: Events where success=1.
        fail_count: Events where success=0.
        success_rate: success_count / total_events (0.0 if no events).
        by_agent: Tuple of AgentSummary sorted by event_count desc.
        by_project: Dict mapping project -> event count.
        by_event_type: Dict mapping event_type -> count.
        project_filter: The project filter applied, empty string = all.
    """

    total_events: int
    total_lessons: int
    total_patterns: int
    success_count: int
    fail_count: int
    success_rate: float
    by_agent: tuple
    by_project: dict
    by_event_type: dict
    project_filter: str = ""

    def __post_init__(self) -> None:
        if self.total_events < 0:
            raise ValueError("total_events must be >= 0")
        if self.total_lessons < 0:
            raise ValueError("total_lessons must be >= 0")
        if self.total_patterns < 0:
            raise ValueError("total_patterns must be >= 0")
        if not 0.0 <= self.success_rate <= 1.0:
            raise ValueError("success_rate must be between 0.0 and 1.0")


# ------------------------------------------------------------------
# Internal helpers
# ------------------------------------------------------------------


def _parse_json_field(value: Optional[str]) -> tuple:
    """Safely parse a JSON array column to a tuple. Returns empty tuple on error."""
    if not value:
        return ()
    try:
        parsed = json.loads(value)
        if isinstance(parsed, list):
            return tuple(parsed)
        return ()
    except (json.JSONDecodeError, TypeError):
        return ()


def _parse_json_dict(value: Optional[str]) -> Optional[dict]:
    """Safely parse a JSON object column. Returns None on error."""
    if not value:
        return None
    try:
        parsed = json.loads(value)
        if isinstance(parsed, dict):
            return parsed
        return None
    except (json.JSONDecodeError, TypeError):
        return None


def _row_to_event_record(row: sqlite3.Row) -> EventRecord:
    """Convert a sqlite3.Row to an EventRecord."""
    success_val: Optional[bool] = None
    raw_success = row["success"]
    if raw_success is not None:
        success_val = bool(raw_success)

    return EventRecord(
        id=row["id"],
        timestamp=row["timestamp"],
        event_type=row["event_type"],
        session_id=row["session_id"],
        agent_name=row["agent_name"],
        agent_role=row["agent_role"],
        task_id=row["task_id"],
        parent_task_id=row["parent_task_id"],
        description=row["description"],
        status=row["status"],
        duration_ms=row["duration_ms"],
        success=success_val,
        error_message=row["error_message"],
        project=row["project"],
        files_modified=_parse_json_field(row["files_modified"]),
        tags=_parse_json_field(row["tags"]),
        metadata=_parse_json_dict(row["metadata"]),
        created_at=row["created_at"],
    )


# ------------------------------------------------------------------
# Query functions
# ------------------------------------------------------------------


def _query_events(
    conn: sqlite3.Connection,
    *,
    agent: str = "",
    project: str = "",
    event_type: str = "",
    session_id: str = "",
    status: str = "",
    success: Optional[bool] = None,
    days: int = 0,
    limit: int = 50,
) -> QueryResult:
    """Internal implementation of EventStore.query_events."""
    clauses: list[str] = []
    params: list = []
    filters_applied: dict = {}

    if agent:
        clauses.append("agent_name = ?")
        params.append(agent)
        filters_applied["agent"] = agent

    if project:
        clauses.append("project = ?")
        params.append(project)
        filters_applied["project"] = project

    if event_type:
        clauses.append("event_type = ?")
        params.append(event_type)
        filters_applied["event_type"] = event_type

    if session_id:
        clauses.append("session_id = ?")
        params.append(session_id)
        filters_applied["session_id"] = session_id

    if status:
        clauses.append("status = ?")
        params.append(status)
        filters_applied["status"] = status

    if success is not None:
        clauses.append("success = ?")
        params.append(1 if success else 0)
        filters_applied["success"] = success

    if days > 0:
        cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
        clauses.append("timestamp >= ?")
        params.append(cutoff)
        filters_applied["days"] = days

    where_clause = "WHERE " + " AND ".join(clauses) if clauses else ""
    sql = f"""
        SELECT id, timestamp, event_type, session_id,
               agent_name, agent_role,
               task_id, parent_task_id, description, status,
               duration_ms, success, error_message,
               project, files_modified, tags, metadata, created_at
        FROM events
        {where_clause}
        ORDER BY timestamp DESC
        LIMIT ?
    """
    params.append(max(1, limit))

    cursor = conn.cursor()
    cursor.execute(sql, params)
    rows = cursor.fetchall()

    records = tuple(_row_to_event_record(r) for r in rows)
    return QueryResult(events=records, total=len(records), filters_applied=filters_applied)


def _project_filter(project: str) -> tuple[str, list]:
    """Build WHERE/AND clause and params for optional project filter."""
    if project:
        return "WHERE project = ?", [project]
    return "", []


def _count_events(
    cursor: sqlite3.Cursor, project: str, extra_condition: str = ""
) -> int:
    """Count events with optional project filter and extra WHERE condition."""
    where, params = _project_filter(project)
    if extra_condition:
        where = f"{where} AND {extra_condition}" if where else f"WHERE {extra_condition}"
    cursor.execute(f"SELECT COUNT(*) FROM events {where}", params)
    return cursor.fetchone()[0] or 0


_VALID_GROUP_COLUMNS = {"project", "event_type", "agent_name", "status", "session_id"}


def _grouped_counts(
    cursor: sqlite3.Cursor, column: str, project: str, extra_where: str = ""
) -> list:
    """SELECT column, COUNT(*) grouped by column with optional project filter."""
    if column not in _VALID_GROUP_COLUMNS:
        raise ValueError(f"Invalid column for grouping: {column!r}")
    where, params = _project_filter(project)
    if extra_where:
        where = f"{where} AND {extra_where}" if where else f"WHERE {extra_where}"
    cursor.execute(
        f"SELECT {column}, COUNT(*) as cnt FROM events {where} "
        f"GROUP BY {column} ORDER BY cnt DESC",
        params,
    )
    return cursor.fetchall()


def _get_statistics(conn: sqlite3.Connection, project: str = "") -> Statistics:
    """Internal implementation of EventStore.get_statistics."""
    cursor = conn.cursor()

    total_events = _count_events(cursor, project)

    cursor.execute("SELECT COUNT(*) FROM lessons")
    total_lessons: int = cursor.fetchone()[0] or 0

    cursor.execute("SELECT COUNT(*) FROM error_patterns")
    total_patterns: int = cursor.fetchone()[0] or 0

    success_count = _count_events(cursor, project, "success = 1")
    fail_count = _count_events(cursor, project, "success = 0")
    success_rate = success_count / total_events if total_events > 0 else 0.0

    # Per-agent summary
    where, params = _project_filter(project)
    agent_where = f"{where} AND agent_name IS NOT NULL" if where else "WHERE agent_name IS NOT NULL"
    cursor.execute(
        f"""
        SELECT agent_name,
               COUNT(*) as cnt,
               SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as ok,
               SUM(CASE WHEN success = 0 THEN 1 ELSE 0 END) as fail
        FROM events
        {agent_where}
        GROUP BY agent_name
        ORDER BY cnt DESC
        """,
        params,
    )
    by_agent = tuple(
        AgentSummary(
            agent_name=row[0],
            event_count=row[1] or 0,
            success_count=row[2] or 0,
            fail_count=row[3] or 0,
        )
        for row in cursor.fetchall()
    )

    # Per-project counts (always unfiltered)
    by_project = {
        row[0]: row[1] for row in _grouped_counts(cursor, "project", "", "project IS NOT NULL")
    }

    # Per-event-type counts
    by_event_type = {row[0]: row[1] for row in _grouped_counts(cursor, "event_type", project)}

    return Statistics(
        total_events=total_events,
        total_lessons=total_lessons,
        total_patterns=total_patterns,
        success_count=success_count,
        fail_count=fail_count,
        success_rate=success_rate,
        by_agent=by_agent,
        by_project=by_project,
        by_event_type=by_event_type,
        project_filter=project,
    )
