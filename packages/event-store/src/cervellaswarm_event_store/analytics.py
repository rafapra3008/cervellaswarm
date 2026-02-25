# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""
Analytics for cervellaswarm-event-store.

detect_patterns: cluster similar error messages using SequenceMatcher.
get_relevant_lessons: rank lessons by contextual relevance score.
agent_stats: per-agent aggregated view.

All result types are frozen dataclasses.
"""

import json
import sqlite3
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from difflib import SequenceMatcher
from typing import Optional

_SEVERITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}
_SEVERITY_SCORES = {"critical": 20, "high": 15, "medium": 10, "low": 5}


# ------------------------------------------------------------------
# Result dataclasses
# ------------------------------------------------------------------


@dataclass(frozen=True)
class ScoredLesson:
    """A lesson enriched with a relevance score.

    Attributes:
        id: Lesson UUID.
        context: Situation in which the lesson was learned.
        problem: What went wrong.
        solution: What resolved the problem.
        pattern: Short reusable pattern name.
        category: Optional category.
        severity: low | medium | high | critical.
        root_cause: Underlying root cause.
        prevention: How to prevent recurrence.
        agents_involved: Agents mentioned.
        project: Project name.
        confidence: 0.0-1.0 confidence.
        times_applied: Application count.
        status: active | resolved | suppressed.
        tags: String tags.
        score: Computed relevance score (higher = more relevant).
    """

    id: str
    context: Optional[str]
    problem: Optional[str]
    solution: Optional[str]
    pattern: Optional[str]
    category: Optional[str]
    severity: str
    root_cause: Optional[str]
    prevention: Optional[str]
    agents_involved: tuple
    project: Optional[str]
    confidence: float
    times_applied: int
    status: str
    tags: tuple
    score: int

    def __post_init__(self) -> None:
        if self.score < 0:
            raise ValueError("score must be >= 0")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0.0 and 1.0")
        if self.times_applied < 0:
            raise ValueError("times_applied must be >= 0")


@dataclass(frozen=True)
class DetectedPattern:
    """A recurring error pattern detected by similarity clustering.

    Attributes:
        pattern_name: Representative error message (truncated to 100 chars).
        pattern_type: Most common event_type in the cluster.
        severity: Inferred from occurrence_count.
        occurrence_count: Number of errors in the cluster.
        first_seen: Earliest timestamp in the cluster.
        last_seen: Latest timestamp in the cluster.
        affected_agents: Agents that produced errors in this cluster.
        error_ids: IDs of the constituent error events.
    """

    pattern_name: str
    pattern_type: str
    severity: str
    occurrence_count: int
    first_seen: str
    last_seen: str
    affected_agents: tuple
    error_ids: tuple

    def __post_init__(self) -> None:
        if not self.pattern_name.strip():
            raise ValueError("pattern_name must be non-empty")
        if self.occurrence_count < 1:
            raise ValueError("occurrence_count must be >= 1")
        if self.severity not in _SEVERITY_ORDER:
            raise ValueError(f"severity must be one of {sorted(_SEVERITY_ORDER)}")


# ------------------------------------------------------------------
# Scoring helpers
# ------------------------------------------------------------------


def _calculate_similarity(text1: str, text2: str) -> float:
    """Return similarity ratio between two strings using SequenceMatcher."""
    if not text1 or not text2:
        return 0.0
    t1 = text1.lower().strip()
    t2 = text2.lower().strip()
    return SequenceMatcher(None, t1, t2).ratio()


def _infer_severity(occurrence_count: int) -> str:
    """Infer severity from number of occurrences."""
    if occurrence_count >= 10:
        return "critical"
    if occurrence_count >= 5:
        return "high"
    if occurrence_count >= 3:
        return "medium"
    return "low"


def _score_lesson(
    row: sqlite3.Row,
    agent: str,
    project: str,
) -> int:
    """Compute relevance score for a lesson row.

    Scoring:
    - agents_involved contains agent: +50
    - project match: +30
    - severity (critical/high/medium/low): +20/+15/+10/+5
    - times_applied > 5: +10
    - confidence > 0.9: +10
    """
    score = 0

    agents_involved = row["agents_involved"] or ""
    if agent and agent.lower() in agents_involved.lower():
        score += 50

    lesson_project = row["project"] or ""
    if project and lesson_project and project.lower() in lesson_project.lower():
        score += 30

    severity = (row["severity"] or "medium").lower()
    score += _SEVERITY_SCORES.get(severity, 0)

    times_applied = row["times_applied"] or 0
    if times_applied > 5:
        score += 10

    confidence = row["confidence"] or 0.5
    if confidence > 0.9:
        score += 10

    return score


from cervellaswarm_event_store.reader import _parse_json_field as _parse_json_tuple


# ------------------------------------------------------------------
# Internal implementations
# ------------------------------------------------------------------


def _get_lessons_scored(
    conn: sqlite3.Connection,
    agent: str = "",
    project: str = "",
    limit: int = 10,
) -> list:
    """Fetch active lessons and rank by relevance score."""
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, context, problem, solution, pattern,
               category, severity, root_cause, prevention,
               agents_involved, project, confidence,
               times_applied, status, tags
        FROM lessons
        WHERE status = 'active'
        ORDER BY confidence DESC, times_applied DESC
        """
    )
    rows = cursor.fetchall()

    scored: list[ScoredLesson] = []
    for row in rows:
        score = _score_lesson(row, agent, project)
        scored.append(
            ScoredLesson(
                id=row["id"],
                context=row["context"],
                problem=row["problem"],
                solution=row["solution"],
                pattern=row["pattern"],
                category=row["category"],
                severity=(row["severity"] or "medium").lower(),
                root_cause=row["root_cause"],
                prevention=row["prevention"],
                agents_involved=_parse_json_tuple(row["agents_involved"]),
                project=row["project"],
                confidence=row["confidence"] or 0.5,
                times_applied=row["times_applied"] or 0,
                status=row["status"] or "active",
                tags=_parse_json_tuple(row["tags"]),
                score=score,
            )
        )

    scored.sort(key=lambda x: x.score, reverse=True)
    return scored[:limit]


def _detect_patterns(
    conn: sqlite3.Connection,
    days: int = 7,
    min_occurrences: int = 3,
    similarity_threshold: float = 0.7,
) -> list:
    """Detect recurring error patterns via SequenceMatcher clustering."""
    cursor = conn.cursor()
    cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()

    cursor.execute(
        """
        SELECT id, event_type, error_message, timestamp, agent_name, project
        FROM events
        WHERE success = 0
          AND error_message IS NOT NULL
          AND timestamp >= ?
        ORDER BY timestamp DESC
        """,
        (cutoff,),
    )
    rows = cursor.fetchall()
    errors = [dict(row) for row in rows]

    if not errors:
        return []

    # Cluster by similarity
    processed: set[int] = set()
    clusters: list[list[dict]] = []

    for i, err in enumerate(errors):
        if i in processed:
            continue
        cluster = [err]
        processed.add(i)
        for j, other in enumerate(errors):
            if j in processed or j <= i:
                continue
            sim = _calculate_similarity(
                err.get("error_message", ""),
                other.get("error_message", ""),
            )
            if sim >= similarity_threshold:
                cluster.append(other)
                processed.add(j)
        clusters.append(cluster)

    # Build DetectedPattern for clusters that meet min_occurrences
    patterns: list[DetectedPattern] = []
    for cluster in clusters:
        count = len(cluster)
        if count < min_occurrences:
            continue

        # Representative name
        representative = cluster[0].get("error_message", "Unknown Error")
        if len(representative) > 100:
            representative = representative[:97] + "..."

        # Pattern type (most common event_type)
        types = [e.get("event_type", "custom") for e in cluster]
        pattern_type = max(set(types), key=types.count)

        # Timestamps
        timestamps = [e["timestamp"] for e in cluster if e.get("timestamp")]
        first_seen = min(timestamps) if timestamps else datetime.now(timezone.utc).isoformat()
        last_seen = max(timestamps) if timestamps else first_seen

        # Affected agents
        agents_set = {e["agent_name"] for e in cluster if e.get("agent_name")}
        affected_agents = tuple(sorted(agents_set))

        # Error IDs
        error_ids = tuple(e["id"] for e in cluster if e.get("id"))

        patterns.append(
            DetectedPattern(
                pattern_name=representative,
                pattern_type=pattern_type,
                severity=_infer_severity(count),
                occurrence_count=count,
                first_seen=first_seen,
                last_seen=last_seen,
                affected_agents=affected_agents,
                error_ids=error_ids,
            )
        )

    # Sort: severity asc (critical first), then occurrence_count desc
    patterns.sort(
        key=lambda p: (_SEVERITY_ORDER.get(p.severity, 4), -p.occurrence_count)
    )
    return patterns


def _agent_stats(conn: sqlite3.Connection, project: str = "") -> list:
    """Return per-agent aggregated statistics as a list of dicts."""
    cursor = conn.cursor()

    project_clause = "AND project = ?" if project else ""
    params = [project] if project else []

    cursor.execute(
        f"""
        SELECT
            agent_name,
            COUNT(*) as total,
            SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as ok,
            SUM(CASE WHEN success = 0 THEN 1 ELSE 0 END) as fail,
            AVG(CASE WHEN duration_ms IS NOT NULL THEN duration_ms END) as avg_ms
        FROM events
        WHERE agent_name IS NOT NULL
        {project_clause}
        GROUP BY agent_name
        ORDER BY total DESC
        """,
        params,
    )

    result = []
    for row in cursor.fetchall():
        total = row[1] or 0
        ok = row[2] or 0
        fail = row[3] or 0
        avg_ms = row[4]

        result.append(
            {
                "agent_name": row[0],
                "total_tasks": total,
                "successful_tasks": ok,
                "failed_tasks": fail,
                "success_rate": ok / total if total > 0 else 0.0,
                "avg_duration_ms": round(avg_ms, 1) if avg_ms is not None else None,
            }
        )

    return result


def get_relevant_lessons(
    conn: sqlite3.Connection,
    agent: str = "",
    project: str = "",
    limit: int = 3,
) -> list:
    """Public alias for _get_lessons_scored used in context loading."""
    return _get_lessons_scored(conn, agent=agent, project=project, limit=limit)
