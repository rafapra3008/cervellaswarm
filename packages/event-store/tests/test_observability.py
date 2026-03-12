# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for cervellaswarm_event_store.observability module."""

import pytest

from cervellaswarm_event_store.database import EventStore
from cervellaswarm_event_store.observability import (
    TokenUsage,
    UsageSummary,
    estimate_cost,
    _insert_token_usage,
    _query_usage,
    _MODEL_PRICING,
    _DEFAULT_PRICING,
)


# ------------------------------------------------------------------
# estimate_cost
# ------------------------------------------------------------------


class TestEstimateCost:
    def test_zero_tokens(self):
        assert estimate_cost("claude-opus-4-6", 0, 0) == 0.0

    def test_opus_pricing(self):
        # 1M input tokens at $15/MTok = $15.00
        cost = estimate_cost("claude-opus-4-6", 1_000_000, 0)
        assert cost == 15.0

    def test_opus_output_pricing(self):
        # 1M output tokens at $75/MTok = $75.00
        cost = estimate_cost("claude-opus-4-6", 0, 1_000_000)
        assert cost == 75.0

    def test_sonnet_pricing(self):
        # 1M input at $3 + 1M output at $15 = $18
        cost = estimate_cost("claude-sonnet-4-6", 1_000_000, 1_000_000)
        assert cost == 18.0

    def test_cache_read_pricing(self):
        # 1M cache read tokens at $1.50/MTok for Opus
        cost = estimate_cost("claude-opus-4-6", 0, 0, cache_read_tokens=1_000_000)
        assert cost == 1.5

    def test_cache_creation_pricing(self):
        # 1M cache creation tokens at $18.75/MTok for Opus
        cost = estimate_cost("claude-opus-4-6", 0, 0, cache_creation_tokens=1_000_000)
        assert cost == 18.75

    def test_combined_pricing(self):
        # Realistic: 50K input + 5K output + 100K cache_read + 20K cache_write (Opus)
        cost = estimate_cost(
            "claude-opus-4-6",
            input_tokens=50_000,
            output_tokens=5_000,
            cache_read_tokens=100_000,
            cache_creation_tokens=20_000,
        )
        expected = (50_000 * 15 + 5_000 * 75 + 100_000 * 1.5 + 20_000 * 18.75) / 1_000_000
        assert cost == pytest.approx(expected, abs=0.001)

    def test_unknown_model_uses_default(self):
        cost = estimate_cost("unknown-model-xyz", 1_000_000, 0)
        assert cost == _DEFAULT_PRICING["input"]

    def test_haiku_pricing(self):
        cost = estimate_cost("claude-haiku-4-5-20251001", 1_000_000, 0)
        assert cost == 0.8

    def test_rounding(self):
        # Small tokens should round to 6 decimal places
        cost = estimate_cost("claude-opus-4-6", 100, 10)
        assert isinstance(cost, float)
        assert len(str(cost).split(".")[-1]) <= 6


# ------------------------------------------------------------------
# TokenUsage dataclass
# ------------------------------------------------------------------


class TestTokenUsage:
    def test_create_minimal(self):
        usage = TokenUsage(session_id="test-123")
        assert usage.session_id == "test-123"
        assert usage.input_tokens == 0
        assert usage.output_tokens == 0
        assert usage.cost_usd == 0.0
        assert usage.id  # auto-generated UUID

    def test_create_full(self):
        usage = TokenUsage(
            session_id="sess-1",
            project="cervellaswarm",
            model="claude-opus-4-6",
            input_tokens=50_000,
            output_tokens=5_000,
            cache_read_tokens=100_000,
            cache_creation_tokens=20_000,
            total_messages=42,
            total_tool_calls=15,
            cost_usd=1.2345,
        )
        assert usage.project == "cervellaswarm"
        assert usage.model == "claude-opus-4-6"
        assert usage.total_messages == 42

    def test_frozen(self):
        usage = TokenUsage(session_id="test-123")
        with pytest.raises(AttributeError):
            usage.input_tokens = 999

    def test_empty_session_id_raises(self):
        with pytest.raises(ValueError, match="session_id"):
            TokenUsage(session_id="")

    def test_whitespace_session_id_raises(self):
        with pytest.raises(ValueError, match="session_id"):
            TokenUsage(session_id="   ")

    def test_negative_tokens_raises(self):
        with pytest.raises(ValueError, match="input_tokens"):
            TokenUsage(session_id="test", input_tokens=-1)

    def test_negative_output_raises(self):
        with pytest.raises(ValueError, match="output_tokens"):
            TokenUsage(session_id="test", output_tokens=-1)

    def test_negative_cache_read_raises(self):
        with pytest.raises(ValueError, match="cache_read_tokens"):
            TokenUsage(session_id="test", cache_read_tokens=-1)

    def test_negative_cache_creation_raises(self):
        with pytest.raises(ValueError, match="cache_creation_tokens"):
            TokenUsage(session_id="test", cache_creation_tokens=-1)

    def test_negative_messages_raises(self):
        with pytest.raises(ValueError, match="total_messages"):
            TokenUsage(session_id="test", total_messages=-1)

    def test_negative_tool_calls_raises(self):
        with pytest.raises(ValueError, match="total_tool_calls"):
            TokenUsage(session_id="test", total_tool_calls=-1)

    def test_negative_cost_raises(self):
        with pytest.raises(ValueError, match="cost_usd"):
            TokenUsage(session_id="test", cost_usd=-0.01)


# ------------------------------------------------------------------
# UsageSummary dataclass
# ------------------------------------------------------------------


class TestUsageSummary:
    def test_defaults(self):
        summary = UsageSummary()
        assert summary.total_sessions == 0
        assert summary.total_cost_usd == 0.0
        assert summary.by_model == {}
        assert summary.by_project == {}


# ------------------------------------------------------------------
# Database write/query
# ------------------------------------------------------------------


class TestTokenUsageDatabase:
    @pytest.fixture
    def store(self):
        with EventStore(":memory:") as s:
            yield s

    def test_log_and_query(self, store):
        usage = TokenUsage(
            session_id="sess-1",
            project="cervellaswarm",
            model="claude-opus-4-6",
            input_tokens=10_000,
            output_tokens=2_000,
            cache_read_tokens=50_000,
            cache_creation_tokens=5_000,
            total_messages=20,
            total_tool_calls=8,
            cost_usd=0.56,
        )
        record_id = store.log_token_usage(usage)
        assert record_id == usage.id

        summary = store.query_usage()
        assert summary.total_sessions == 1
        assert summary.total_input_tokens == 10_000
        assert summary.total_output_tokens == 2_000
        assert summary.total_cache_read_tokens == 50_000
        assert summary.total_cache_creation_tokens == 5_000
        assert summary.total_cost_usd == 0.56

    def test_multiple_sessions(self, store):
        for i in range(3):
            store.log_token_usage(
                TokenUsage(
                    session_id=f"sess-{i}",
                    project="cervellaswarm",
                    model="claude-opus-4-6",
                    input_tokens=10_000,
                    output_tokens=1_000,
                    cost_usd=0.50,
                )
            )
        summary = store.query_usage()
        assert summary.total_sessions == 3
        assert summary.total_input_tokens == 30_000
        assert summary.total_output_tokens == 3_000
        assert summary.total_cost_usd == 1.50

    def test_filter_by_project(self, store):
        store.log_token_usage(
            TokenUsage(session_id="s1", project="cervellaswarm", input_tokens=100, cost_usd=0.10)
        )
        store.log_token_usage(
            TokenUsage(session_id="s2", project="contabilita", input_tokens=200, cost_usd=0.20)
        )

        cs_summary = store.query_usage(project="cervellaswarm")
        assert cs_summary.total_sessions == 1
        assert cs_summary.total_input_tokens == 100

        ct_summary = store.query_usage(project="contabilita")
        assert ct_summary.total_sessions == 1
        assert ct_summary.total_input_tokens == 200

    def test_filter_by_model(self, store):
        store.log_token_usage(
            TokenUsage(session_id="s1", model="claude-opus-4-6", output_tokens=1000, cost_usd=0.50)
        )
        store.log_token_usage(
            TokenUsage(session_id="s2", model="claude-sonnet-4-6", output_tokens=2000, cost_usd=0.10)
        )

        opus_summary = store.query_usage(model="claude-opus-4-6")
        assert opus_summary.total_sessions == 1
        assert opus_summary.total_output_tokens == 1000

    def test_filter_by_days(self, store):
        from datetime import datetime, timezone, timedelta

        old_ts = (datetime.now(timezone.utc) - timedelta(days=10)).isoformat()
        recent_ts = datetime.now(timezone.utc).isoformat()

        store.log_token_usage(
            TokenUsage(session_id="old", timestamp=old_ts, input_tokens=100, cost_usd=0.10)
        )
        store.log_token_usage(
            TokenUsage(session_id="new", timestamp=recent_ts, input_tokens=200, cost_usd=0.20)
        )

        recent = store.query_usage(days=7)
        assert recent.total_sessions == 1
        assert recent.total_input_tokens == 200

        all_time = store.query_usage()
        assert all_time.total_sessions == 2

    def test_by_model_breakdown(self, store):
        store.log_token_usage(
            TokenUsage(session_id="s1", model="claude-opus-4-6", input_tokens=100, cost_usd=0.50)
        )
        store.log_token_usage(
            TokenUsage(session_id="s2", model="claude-sonnet-4-6", input_tokens=200, cost_usd=0.10)
        )

        summary = store.query_usage()
        assert "claude-opus-4-6" in summary.by_model
        assert "claude-sonnet-4-6" in summary.by_model
        assert summary.by_model["claude-opus-4-6"]["cost"] == 0.50

    def test_by_project_breakdown(self, store):
        store.log_token_usage(
            TokenUsage(session_id="s1", project="cervellaswarm", cost_usd=0.50)
        )
        store.log_token_usage(
            TokenUsage(session_id="s2", project="miracollo", cost_usd=0.30)
        )

        summary = store.query_usage()
        assert "cervellaswarm" in summary.by_project
        assert "miracollo" in summary.by_project

    def test_empty_database(self, store):
        summary = store.query_usage()
        assert summary.total_sessions == 0
        assert summary.total_cost_usd == 0.0
        assert summary.by_model == {}
        assert summary.by_project == {}

    def test_token_usage_table_created(self, store):
        """Verify token_usage table exists in schema."""
        conn = store._require_conn()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='token_usage'"
        )
        assert cursor.fetchone() is not None


# ------------------------------------------------------------------
# Model pricing
# ------------------------------------------------------------------


class TestModelPricing:
    def test_all_models_have_required_keys(self):
        for model, pricing in _MODEL_PRICING.items():
            assert "input" in pricing, f"{model} missing 'input'"
            assert "output" in pricing, f"{model} missing 'output'"
            assert "cache_read" in pricing, f"{model} missing 'cache_read'"
            assert "cache_write" in pricing, f"{model} missing 'cache_write'"

    def test_prices_are_positive(self):
        for model, pricing in _MODEL_PRICING.items():
            for key, val in pricing.items():
                assert val > 0, f"{model}.{key} must be positive"

    def test_opus_more_expensive_than_sonnet(self):
        opus = _MODEL_PRICING["claude-opus-4-6"]
        sonnet = _MODEL_PRICING["claude-sonnet-4-6"]
        assert opus["input"] > sonnet["input"]
        assert opus["output"] > sonnet["output"]
