# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""
Observability module for cervellaswarm-event-store.

Tracks token usage per session from Claude Code conversation transcripts.
Stores aggregated data in SQLite for cost analysis and trend tracking.

Usage data is extracted from JSONL transcripts (assistant messages contain
Anthropic API usage metadata: input_tokens, output_tokens, cache tokens).
"""

import sqlite3
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Optional

from cervellaswarm_event_store.writer import _new_id, _utc_now

# ------------------------------------------------------------------
# Pricing (per million tokens, USD)
# Updated: March 2026 -- adjust when pricing changes
# ------------------------------------------------------------------

_MODEL_PRICING: dict[str, dict[str, float]] = {
    "claude-opus-4-6": {
        "input": 15.0,
        "output": 75.0,
        "cache_read": 1.50,
        "cache_write": 18.75,
    },
    "claude-sonnet-4-6": {
        "input": 3.0,
        "output": 15.0,
        "cache_read": 0.30,
        "cache_write": 3.75,
    },
    "claude-haiku-4-5-20251001": {
        "input": 0.80,
        "output": 4.0,
        "cache_read": 0.08,
        "cache_write": 1.0,
    },
}

# Aliases for model names that may appear without date suffix
_MODEL_PRICING["claude-haiku-4-5"] = _MODEL_PRICING["claude-haiku-4-5-20251001"]

# Fallback for unknown models (use Sonnet pricing as safe middle ground)
_DEFAULT_PRICING = _MODEL_PRICING["claude-sonnet-4-6"]


def estimate_cost(
    model: str,
    input_tokens: int,
    output_tokens: int,
    cache_read_tokens: int = 0,
    cache_creation_tokens: int = 0,
) -> float:
    """Estimate cost in USD for a set of token counts.

    Args:
        model: Model identifier (e.g. 'claude-opus-4-6').
        input_tokens: Non-cached input tokens.
        output_tokens: Output tokens.
        cache_read_tokens: Tokens read from cache.
        cache_creation_tokens: Tokens written to cache.

    Returns:
        Estimated cost in USD.
    """
    pricing = _MODEL_PRICING.get(model, _DEFAULT_PRICING)
    cost = (
        input_tokens * pricing["input"]
        + output_tokens * pricing["output"]
        + cache_read_tokens * pricing["cache_read"]
        + cache_creation_tokens * pricing["cache_write"]
    ) / 1_000_000
    return round(cost, 6)


# ------------------------------------------------------------------
# Dataclasses
# ------------------------------------------------------------------


@dataclass(frozen=True)
class TokenUsage:
    """Aggregated token usage for a single session.

    Attributes:
        id: UUID string. Auto-generated if empty.
        timestamp: ISO 8601 UTC string. Auto-generated if empty.
        session_id: Claude Code session identifier.
        project: Project name.
        model: Primary model used (most tokens).
        input_tokens: Total non-cached input tokens.
        output_tokens: Total output tokens.
        cache_read_tokens: Total cache read tokens.
        cache_creation_tokens: Total cache creation tokens.
        total_messages: Number of assistant messages in the session.
        total_tool_calls: Number of tool calls in the session.
        cost_usd: Estimated cost in USD.
    """

    session_id: str
    id: str = field(default_factory=_new_id)
    timestamp: str = field(default_factory=_utc_now)
    project: Optional[str] = None
    model: Optional[str] = None
    input_tokens: int = 0
    output_tokens: int = 0
    cache_read_tokens: int = 0
    cache_creation_tokens: int = 0
    total_messages: int = 0
    total_tool_calls: int = 0
    cost_usd: float = 0.0

    def __post_init__(self) -> None:
        if not self.session_id or not self.session_id.strip():
            raise ValueError("session_id must be a non-empty string")
        for attr in ("input_tokens", "output_tokens", "cache_read_tokens",
                      "cache_creation_tokens", "total_messages", "total_tool_calls"):
            if getattr(self, attr) < 0:
                raise ValueError(f"{attr} must be >= 0")
        if self.cost_usd < 0:
            raise ValueError("cost_usd must be >= 0")


@dataclass(frozen=True)
class UsageSummary:
    """Aggregated usage summary across sessions.

    Attributes:
        total_sessions: Number of sessions.
        total_input_tokens: Sum of input tokens.
        total_output_tokens: Sum of output tokens.
        total_cache_read_tokens: Sum of cache read tokens.
        total_cache_creation_tokens: Sum of cache creation tokens.
        total_cost_usd: Sum of estimated cost.
        by_model: Dict of model -> {tokens, cost}.
        by_project: Dict of project -> {tokens, cost}.
    """

    total_sessions: int = 0
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    total_cache_read_tokens: int = 0
    total_cache_creation_tokens: int = 0
    total_cost_usd: float = 0.0
    by_model: dict = field(default_factory=dict)
    by_project: dict = field(default_factory=dict)


# ------------------------------------------------------------------
# Write functions
# ------------------------------------------------------------------


def _insert_token_usage(conn: sqlite3.Connection, usage: TokenUsage) -> str:
    """Insert a TokenUsage record. Returns the id."""
    conn.execute(
        """
        INSERT INTO token_usage (
            id, timestamp, session_id, project, model,
            input_tokens, output_tokens,
            cache_read_tokens, cache_creation_tokens,
            total_messages, total_tool_calls, cost_usd
        ) VALUES (
            :id, :timestamp, :session_id, :project, :model,
            :input_tokens, :output_tokens,
            :cache_read_tokens, :cache_creation_tokens,
            :total_messages, :total_tool_calls, :cost_usd
        )
        """,
        {
            "id": usage.id,
            "timestamp": usage.timestamp,
            "session_id": usage.session_id,
            "project": usage.project,
            "model": usage.model,
            "input_tokens": usage.input_tokens,
            "output_tokens": usage.output_tokens,
            "cache_read_tokens": usage.cache_read_tokens,
            "cache_creation_tokens": usage.cache_creation_tokens,
            "total_messages": usage.total_messages,
            "total_tool_calls": usage.total_tool_calls,
            "cost_usd": usage.cost_usd,
        },
    )
    conn.commit()
    return usage.id


# ------------------------------------------------------------------
# Query functions
# ------------------------------------------------------------------


def _query_usage(
    conn: sqlite3.Connection,
    *,
    project: str = "",
    model: str = "",
    days: int = 0,
) -> UsageSummary:
    """Query aggregated usage statistics.

    Args:
        project: Filter by project (exact match).
        model: Filter by model (exact match).
        days: Only include data from the last N days. 0 = no limit.

    Returns:
        UsageSummary with aggregated data.
    """
    where_clauses: list[str] = []
    params: list = []

    if project:
        where_clauses.append("project = ?")
        params.append(project)
    if model:
        where_clauses.append("model = ?")
        params.append(model)
    if days > 0:
        cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
        where_clauses.append("timestamp >= ?")
        params.append(cutoff)

    where_sql = "WHERE " + " AND ".join(where_clauses) if where_clauses else ""

    cursor = conn.cursor()

    # Totals
    cursor.execute(
        f"""
        SELECT
            COUNT(*) as sessions,
            COALESCE(SUM(input_tokens), 0) as inp,
            COALESCE(SUM(output_tokens), 0) as out,
            COALESCE(SUM(cache_read_tokens), 0) as cr,
            COALESCE(SUM(cache_creation_tokens), 0) as cc,
            COALESCE(SUM(cost_usd), 0) as cost
        FROM token_usage
        {where_sql}
        """,
        params,
    )
    row = cursor.fetchone()

    # By model
    cursor.execute(
        f"""
        SELECT
            model,
            SUM(input_tokens + output_tokens + cache_read_tokens + cache_creation_tokens) as tokens,
            SUM(cost_usd) as cost
        FROM token_usage
        {where_sql}
        GROUP BY model
        ORDER BY cost DESC
        """,
        params,
    )
    by_model = {
        r["model"] or "unknown": {"tokens": r["tokens"], "cost": round(r["cost"], 4)}
        for r in cursor.fetchall()
    }

    # By project
    cursor.execute(
        f"""
        SELECT
            project,
            SUM(input_tokens + output_tokens + cache_read_tokens + cache_creation_tokens) as tokens,
            SUM(cost_usd) as cost
        FROM token_usage
        {where_sql}
        GROUP BY project
        ORDER BY cost DESC
        """,
        params,
    )
    by_project = {
        r["project"] or "unknown": {"tokens": r["tokens"], "cost": round(r["cost"], 4)}
        for r in cursor.fetchall()
    }

    return UsageSummary(
        total_sessions=row["sessions"],
        total_input_tokens=row["inp"],
        total_output_tokens=row["out"],
        total_cache_read_tokens=row["cr"],
        total_cache_creation_tokens=row["cc"],
        total_cost_usd=round(row["cost"], 4),
        by_model=by_model,
        by_project=by_project,
    )
