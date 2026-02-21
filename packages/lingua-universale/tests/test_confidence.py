# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for confidence.py - Confident[T] and ConfidenceScore."""

import pytest

from cervellaswarm_lingua_universale.confidence import (
    CompositionStrategy,
    Confident,
    ConfidenceScore,
    ConfidenceSource,
    compose_scores,
)


# ── ConfidenceSource ─────────────────────────────────────────────────────────

class TestConfidenceSource:
    def test_all_values_exist(self):
        assert ConfidenceSource.SELF_REPORTED.value == "self_reported"
        assert ConfidenceSource.AUDIT.value == "audit"
        assert ConfidenceSource.COMPUTED.value == "computed"
        assert ConfidenceSource.INHERITED.value == "inherited"
        assert ConfidenceSource.DEFAULT.value == "default"

    def test_five_members(self):
        assert len(ConfidenceSource) == 5


# ── ConfidenceScore creation ─────────────────────────────────────────────────

class TestConfidenceScoreCreation:
    def test_basic_creation(self):
        cs = ConfidenceScore(value=0.9)
        assert cs.value == 0.9
        assert cs.source == ConfidenceSource.DEFAULT
        assert cs.evidence == ()

    def test_creation_with_source(self):
        cs = ConfidenceScore(value=0.7, source=ConfidenceSource.AUDIT)
        assert cs.source == ConfidenceSource.AUDIT

    def test_creation_with_evidence(self):
        cs = ConfidenceScore(value=0.8, evidence=("audit:S386", "audit:S385"))
        assert cs.evidence == ("audit:S386", "audit:S385")

    def test_frozen(self):
        cs = ConfidenceScore(value=0.5)
        with pytest.raises((AttributeError, TypeError)):
            cs.value = 0.9  # type: ignore[misc]

    def test_value_zero(self):
        cs = ConfidenceScore(value=0.0)
        assert cs.value == 0.0

    def test_value_one(self):
        cs = ConfidenceScore(value=1.0)
        assert cs.value == 1.0

    def test_value_midpoint(self):
        cs = ConfidenceScore(value=0.5)
        assert cs.value == 0.5

    def test_value_very_small(self):
        cs = ConfidenceScore(value=1e-10)
        assert cs.value == pytest.approx(1e-10)


# ── ConfidenceScore validation ───────────────────────────────────────────────

class TestConfidenceScoreValidation:
    def test_rejects_negative(self):
        with pytest.raises(ValueError, match="0.0-1.0"):
            ConfidenceScore(value=-0.1)

    def test_rejects_above_one(self):
        with pytest.raises(ValueError, match="0.0-1.0"):
            ConfidenceScore(value=1.001)

    def test_rejects_large_positive(self):
        with pytest.raises(ValueError, match="0.0-1.0"):
            ConfidenceScore(value=10.0)

    def test_rejects_large_negative(self):
        with pytest.raises(ValueError, match="0.0-1.0"):
            ConfidenceScore(value=-100.0)

    def test_boundary_exactly_zero_ok(self):
        cs = ConfidenceScore(value=0.0)
        assert cs.value == 0.0

    def test_boundary_exactly_one_ok(self):
        cs = ConfidenceScore(value=1.0)
        assert cs.value == 1.0


# ── ConfidenceScore.full() and unknown() ─────────────────────────────────────

class TestConfidenceScoreShorthands:
    def test_full_value(self):
        cs = ConfidenceScore.full()
        assert cs.value == 1.0

    def test_full_source_is_default(self):
        cs = ConfidenceScore.full()
        assert cs.source == ConfidenceSource.DEFAULT

    def test_full_evidence_empty(self):
        cs = ConfidenceScore.full()
        assert cs.evidence == ()

    def test_unknown_value(self):
        cs = ConfidenceScore.unknown()
        assert cs.value == 0.5

    def test_unknown_source_is_default(self):
        cs = ConfidenceScore.unknown()
        assert cs.source == ConfidenceSource.DEFAULT

    def test_unknown_evidence_empty(self):
        cs = ConfidenceScore.unknown()
        assert cs.evidence == ()

    def test_full_and_unknown_are_different(self):
        assert ConfidenceScore.full() != ConfidenceScore.unknown()


# ── ConfidenceScore.from_audit_score ─────────────────────────────────────────

class TestFromAuditScore:
    def test_score_95_maps_to_095(self):
        cs = ConfidenceScore.from_audit_score(9.5)
        assert cs.value == pytest.approx(0.95)

    def test_score_10_maps_to_1(self):
        cs = ConfidenceScore.from_audit_score(10.0)
        assert cs.value == pytest.approx(1.0)

    def test_score_0_maps_to_0(self):
        cs = ConfidenceScore.from_audit_score(0.0)
        assert cs.value == pytest.approx(0.0)

    def test_score_5_maps_to_05(self):
        cs = ConfidenceScore.from_audit_score(5.0)
        assert cs.value == pytest.approx(0.5)

    def test_source_is_audit(self):
        cs = ConfidenceScore.from_audit_score(8.0)
        assert cs.source == ConfidenceSource.AUDIT

    def test_with_audit_id_in_evidence(self):
        cs = ConfidenceScore.from_audit_score(9.5, audit_id="S386")
        assert "audit:S386" in cs.evidence

    def test_without_audit_id_evidence_empty(self):
        cs = ConfidenceScore.from_audit_score(9.0)
        assert cs.evidence == ()

    def test_rejects_score_above_10(self):
        with pytest.raises(ValueError, match="0.0-10.0"):
            ConfidenceScore.from_audit_score(10.1)

    def test_rejects_negative_score(self):
        with pytest.raises(ValueError, match="0.0-10.0"):
            ConfidenceScore.from_audit_score(-1.0)

    def test_boundary_exactly_10_ok(self):
        cs = ConfidenceScore.from_audit_score(10.0)
        assert cs.value == pytest.approx(1.0)

    def test_boundary_exactly_0_ok(self):
        cs = ConfidenceScore.from_audit_score(0.0)
        assert cs.value == pytest.approx(0.0)


# ── compose_min ───────────────────────────────────────────────────────────────

class TestComposeMin:
    def test_min_takes_lower_value(self):
        a = ConfidenceScore(value=0.9)
        b = ConfidenceScore(value=0.6)
        result = a.compose_min(b)
        assert result.value == pytest.approx(0.6)

    def test_min_symmetric(self):
        a = ConfidenceScore(value=0.9)
        b = ConfidenceScore(value=0.6)
        assert a.compose_min(b).value == b.compose_min(a).value

    def test_min_source_is_computed(self):
        a = ConfidenceScore(value=0.9, source=ConfidenceSource.AUDIT)
        b = ConfidenceScore(value=0.7, source=ConfidenceSource.SELF_REPORTED)
        result = a.compose_min(b)
        assert result.source == ConfidenceSource.COMPUTED

    def test_min_accumulates_evidence(self):
        a = ConfidenceScore(value=0.9, evidence=("audit:S386",))
        b = ConfidenceScore(value=0.7, evidence=("audit:S385",))
        result = a.compose_min(b)
        assert "audit:S386" in result.evidence
        assert "audit:S385" in result.evidence

    def test_min_equal_values(self):
        a = ConfidenceScore(value=0.7)
        b = ConfidenceScore(value=0.7)
        result = a.compose_min(b)
        assert result.value == pytest.approx(0.7)

    def test_min_with_zero(self):
        a = ConfidenceScore(value=0.9)
        b = ConfidenceScore(value=0.0)
        result = a.compose_min(b)
        assert result.value == pytest.approx(0.0)

    def test_min_with_one(self):
        a = ConfidenceScore(value=1.0)
        b = ConfidenceScore(value=0.8)
        result = a.compose_min(b)
        assert result.value == pytest.approx(0.8)

    def test_min_returns_new_object(self):
        a = ConfidenceScore(value=0.9)
        b = ConfidenceScore(value=0.7)
        result = a.compose_min(b)
        assert result is not a
        assert result is not b


# ── compose_product ───────────────────────────────────────────────────────────

class TestComposeProduct:
    def test_product_multiplies(self):
        a = ConfidenceScore(value=0.9)
        b = ConfidenceScore(value=0.8)
        result = a.compose_product(b)
        assert result.value == pytest.approx(0.72)

    def test_product_source_is_computed(self):
        a = ConfidenceScore(value=0.9)
        b = ConfidenceScore(value=0.8)
        result = a.compose_product(b)
        assert result.source == ConfidenceSource.COMPUTED

    def test_product_accumulates_evidence(self):
        a = ConfidenceScore(value=0.9, evidence=("e1",))
        b = ConfidenceScore(value=0.8, evidence=("e2",))
        result = a.compose_product(b)
        assert "e1" in result.evidence
        assert "e2" in result.evidence

    def test_product_with_one_is_identity(self):
        a = ConfidenceScore(value=0.75)
        b = ConfidenceScore(value=1.0)
        result = a.compose_product(b)
        assert result.value == pytest.approx(0.75)

    def test_product_with_zero_gives_zero(self):
        a = ConfidenceScore(value=0.9)
        b = ConfidenceScore(value=0.0)
        result = a.compose_product(b)
        assert result.value == pytest.approx(0.0)

    def test_product_symmetric(self):
        a = ConfidenceScore(value=0.6)
        b = ConfidenceScore(value=0.8)
        assert a.compose_product(b).value == pytest.approx(b.compose_product(a).value)

    def test_product_very_small(self):
        a = ConfidenceScore(value=0.1)
        b = ConfidenceScore(value=0.1)
        result = a.compose_product(b)
        assert result.value == pytest.approx(0.01)


# ── compose_avg ───────────────────────────────────────────────────────────────

class TestComposeAvg:
    def test_avg_arithmetic_mean(self):
        a = ConfidenceScore(value=0.9)
        b = ConfidenceScore(value=0.7)
        result = a.compose_avg(b)
        assert result.value == pytest.approx(0.8)

    def test_avg_source_is_computed(self):
        a = ConfidenceScore(value=0.9)
        b = ConfidenceScore(value=0.7)
        result = a.compose_avg(b)
        assert result.source == ConfidenceSource.COMPUTED

    def test_avg_accumulates_evidence(self):
        a = ConfidenceScore(value=0.9, evidence=("e1",))
        b = ConfidenceScore(value=0.7, evidence=("e2",))
        result = a.compose_avg(b)
        assert "e1" in result.evidence
        assert "e2" in result.evidence

    def test_avg_symmetric(self):
        a = ConfidenceScore(value=0.3)
        b = ConfidenceScore(value=0.9)
        assert a.compose_avg(b).value == pytest.approx(b.compose_avg(a).value)

    def test_avg_equal_values(self):
        a = ConfidenceScore(value=0.6)
        b = ConfidenceScore(value=0.6)
        result = a.compose_avg(b)
        assert result.value == pytest.approx(0.6)

    def test_avg_zero_and_one(self):
        a = ConfidenceScore(value=0.0)
        b = ConfidenceScore(value=1.0)
        result = a.compose_avg(b)
        assert result.value == pytest.approx(0.5)


# ── Confident[T] creation ─────────────────────────────────────────────────────

class TestConfidentCreation:
    def test_basic_creation_str(self):
        c = Confident(value="bug found", confidence=ConfidenceScore(0.9))
        assert c.value == "bug found"
        assert c.confidence.value == 0.9

    def test_basic_creation_int(self):
        c = Confident(value=42, confidence=ConfidenceScore(0.7))
        assert c.value == 42

    def test_basic_creation_list(self):
        c = Confident(value=[1, 2, 3], confidence=ConfidenceScore(0.5))
        assert c.value == [1, 2, 3]

    def test_default_confidence_is_full(self):
        c = Confident(value="test")
        assert c.confidence.value == 1.0

    def test_frozen(self):
        c = Confident(value="x", confidence=ConfidenceScore(0.5))
        with pytest.raises((AttributeError, TypeError)):
            c.value = "y"  # type: ignore[misc]

    def test_generic_dict(self):
        data = {"key": "value"}
        c = Confident(value=data, confidence=ConfidenceScore(0.8))
        assert c.value == data


# ── Confident.is_high and is_low ─────────────────────────────────────────────

class TestConfidentProperties:
    def test_is_high_at_08(self):
        c = Confident(value="x", confidence=ConfidenceScore(0.8))
        assert c.is_high is True

    def test_is_high_above_08(self):
        c = Confident(value="x", confidence=ConfidenceScore(0.95))
        assert c.is_high is True

    def test_is_high_at_1(self):
        c = Confident(value="x", confidence=ConfidenceScore(1.0))
        assert c.is_high is True

    def test_not_is_high_below_08(self):
        c = Confident(value="x", confidence=ConfidenceScore(0.79))
        assert c.is_high is False

    def test_not_is_high_at_zero(self):
        c = Confident(value="x", confidence=ConfidenceScore(0.0))
        assert c.is_high is False

    def test_is_low_below_05(self):
        c = Confident(value="x", confidence=ConfidenceScore(0.4))
        assert c.is_low is True

    def test_is_low_at_zero(self):
        c = Confident(value="x", confidence=ConfidenceScore(0.0))
        assert c.is_low is True

    def test_not_is_low_at_05(self):
        c = Confident(value="x", confidence=ConfidenceScore(0.5))
        assert c.is_low is False

    def test_not_is_low_above_05(self):
        c = Confident(value="x", confidence=ConfidenceScore(0.7))
        assert c.is_low is False

    def test_neither_high_nor_low_in_middle(self):
        c = Confident(value="x", confidence=ConfidenceScore(0.65))
        assert c.is_high is False
        assert c.is_low is False


# ── Confident.map ─────────────────────────────────────────────────────────────

class TestConfidentMap:
    def test_map_transforms_value(self):
        c = Confident(value="hello", confidence=ConfidenceScore(0.9))
        result = c.map(str.upper)
        assert result.value == "HELLO"

    def test_map_preserves_confidence(self):
        c = Confident(value="hello", confidence=ConfidenceScore(0.9))
        result = c.map(str.upper)
        assert result.confidence == c.confidence

    def test_map_type_change_int_to_str(self):
        c = Confident(value=42, confidence=ConfidenceScore(0.7))
        result = c.map(str)
        assert result.value == "42"

    def test_map_with_lambda(self):
        c = Confident(value=10, confidence=ConfidenceScore(0.8))
        result = c.map(lambda x: x * 2)
        assert result.value == 20

    def test_map_returns_new_object(self):
        c = Confident(value="x", confidence=ConfidenceScore(0.5))
        result = c.map(str.upper)
        assert result is not c

    def test_map_chaining(self):
        c = Confident(value="hello", confidence=ConfidenceScore(0.9))
        result = c.map(str.upper).map(lambda s: s + "!")
        assert result.value == "HELLO!"
        assert result.confidence.value == pytest.approx(0.9)

    def test_map_identity(self):
        c = Confident(value="same", confidence=ConfidenceScore(0.6))
        result = c.map(lambda x: x)
        assert result.value == "same"
        assert result.confidence.value == pytest.approx(0.6)

    def test_map_with_list(self):
        c = Confident(value=[1, 2, 3], confidence=ConfidenceScore(0.8))
        result = c.map(len)
        assert result.value == 3


# ── Confident.and_then ────────────────────────────────────────────────────────

class TestConfidentAndThen:
    def test_and_then_chains_value(self):
        c = Confident(value="bug found", confidence=ConfidenceScore(0.9))
        result = c.and_then(
            lambda s: Confident(value=s.upper(), confidence=ConfidenceScore(0.8))
        )
        assert result.value == "BUG FOUND"

    def test_and_then_composes_confidence_via_product(self):
        c = Confident(value="x", confidence=ConfidenceScore(0.9))
        result = c.and_then(
            lambda _: Confident(value="y", confidence=ConfidenceScore(0.8))
        )
        assert result.confidence.value == pytest.approx(0.72)

    def test_and_then_source_is_computed(self):
        c = Confident(value="x", confidence=ConfidenceScore(0.9))
        result = c.and_then(
            lambda _: Confident(value="y", confidence=ConfidenceScore(0.8))
        )
        assert result.confidence.source == ConfidenceSource.COMPUTED

    def test_and_then_with_full_confidence_is_identity_on_confidence(self):
        c = Confident(value=10, confidence=ConfidenceScore(0.7))
        result = c.and_then(
            lambda x: Confident(value=x + 1, confidence=ConfidenceScore(1.0))
        )
        assert result.value == 11
        assert result.confidence.value == pytest.approx(0.7)

    def test_and_then_with_zero_confidence_gives_zero(self):
        c = Confident(value="x", confidence=ConfidenceScore(0.9))
        result = c.and_then(
            lambda _: Confident(value="y", confidence=ConfidenceScore(0.0))
        )
        assert result.confidence.value == pytest.approx(0.0)

    def test_and_then_chaining_decreases_confidence(self):
        c = Confident(value=1, confidence=ConfidenceScore(0.9))
        step = lambda x: Confident(value=x + 1, confidence=ConfidenceScore(0.9))
        result = c.and_then(step).and_then(step)
        # 0.9 * 0.9 * 0.9 = 0.729
        assert result.confidence.value == pytest.approx(0.729, rel=1e-4)

    def test_and_then_accumulates_evidence(self):
        c = Confident(
            value="x",
            confidence=ConfidenceScore(0.9, evidence=("e1",)),
        )
        result = c.and_then(
            lambda _: Confident(
                value="y",
                confidence=ConfidenceScore(0.8, evidence=("e2",)),
            )
        )
        assert "e1" in result.confidence.evidence
        assert "e2" in result.confidence.evidence


# ── CompositionStrategy ───────────────────────────────────────────────────────

class TestCompositionStrategy:
    def test_all_values_exist(self):
        assert CompositionStrategy.MIN.value == "min"
        assert CompositionStrategy.PRODUCT.value == "product"
        assert CompositionStrategy.AVERAGE.value == "average"

    def test_three_members(self):
        assert len(CompositionStrategy) == 3


# ── compose_scores ────────────────────────────────────────────────────────────

class TestComposeScores:
    def test_empty_raises_value_error(self):
        with pytest.raises(ValueError, match="empty"):
            compose_scores(())

    def test_single_returns_same(self):
        cs = ConfidenceScore(value=0.7, source=ConfidenceSource.AUDIT)
        result = compose_scores((cs,))
        assert result is cs

    def test_min_strategy_picks_lowest(self):
        scores = (
            ConfidenceScore(value=0.9),
            ConfidenceScore(value=0.6),
            ConfidenceScore(value=0.8),
        )
        result = compose_scores(scores, CompositionStrategy.MIN)
        assert result.value == pytest.approx(0.6)

    def test_product_strategy_multiplies_all(self):
        scores = (
            ConfidenceScore(value=0.9),
            ConfidenceScore(value=0.8),
            ConfidenceScore(value=0.5),
        )
        result = compose_scores(scores, CompositionStrategy.PRODUCT)
        assert result.value == pytest.approx(0.36)

    def test_average_strategy_arithmetic_mean(self):
        scores = (
            ConfidenceScore(value=0.9),
            ConfidenceScore(value=0.7),
            ConfidenceScore(value=0.5),
        )
        result = compose_scores(scores, CompositionStrategy.AVERAGE)
        assert result.value == pytest.approx(7.0 / 10.0)

    def test_default_strategy_is_min(self):
        scores = (
            ConfidenceScore(value=0.9),
            ConfidenceScore(value=0.4),
        )
        result = compose_scores(scores)
        assert result.value == pytest.approx(0.4)

    def test_result_source_is_computed(self):
        scores = (
            ConfidenceScore(value=0.9, source=ConfidenceSource.AUDIT),
            ConfidenceScore(value=0.7, source=ConfidenceSource.SELF_REPORTED),
        )
        result = compose_scores(scores, CompositionStrategy.MIN)
        assert result.source == ConfidenceSource.COMPUTED

    def test_evidence_accumulates_from_all_scores(self):
        scores = (
            ConfidenceScore(value=0.9, evidence=("audit:S386",)),
            ConfidenceScore(value=0.8, evidence=("audit:S385",)),
            ConfidenceScore(value=0.7, evidence=("audit:S384",)),
        )
        result = compose_scores(scores, CompositionStrategy.MIN)
        assert "audit:S386" in result.evidence
        assert "audit:S385" in result.evidence
        assert "audit:S384" in result.evidence

    def test_evidence_empty_when_all_empty(self):
        scores = (
            ConfidenceScore(value=0.9),
            ConfidenceScore(value=0.8),
        )
        result = compose_scores(scores, CompositionStrategy.PRODUCT)
        assert result.evidence == ()

    def test_min_with_two_scores(self):
        scores = (ConfidenceScore(value=0.3), ConfidenceScore(value=0.9))
        result = compose_scores(scores, CompositionStrategy.MIN)
        assert result.value == pytest.approx(0.3)

    def test_product_with_one_gives_identity(self):
        scores = (ConfidenceScore(value=0.75), ConfidenceScore(value=1.0))
        result = compose_scores(scores, CompositionStrategy.PRODUCT)
        assert result.value == pytest.approx(0.75)

    def test_average_two_values(self):
        scores = (ConfidenceScore(value=0.2), ConfidenceScore(value=0.8))
        result = compose_scores(scores, CompositionStrategy.AVERAGE)
        assert result.value == pytest.approx(0.5)

    def test_product_all_zeros(self):
        scores = (
            ConfidenceScore(value=0.0),
            ConfidenceScore(value=0.9),
        )
        result = compose_scores(scores, CompositionStrategy.PRODUCT)
        assert result.value == pytest.approx(0.0)

    def test_min_all_equal(self):
        scores = (
            ConfidenceScore(value=0.7),
            ConfidenceScore(value=0.7),
            ConfidenceScore(value=0.7),
        )
        result = compose_scores(scores, CompositionStrategy.MIN)
        assert result.value == pytest.approx(0.7)

    def test_average_all_ones(self):
        scores = (
            ConfidenceScore(value=1.0),
            ConfidenceScore(value=1.0),
            ConfidenceScore(value=1.0),
        )
        result = compose_scores(scores, CompositionStrategy.AVERAGE)
        assert result.value == pytest.approx(1.0)


# ── Integration / realistic usage ────────────────────────────────────────────

class TestRealisticUsage:
    def test_audit_pipeline(self):
        """Simulate a Guardiana audit producing a Confident result."""
        audit_score = ConfidenceScore.from_audit_score(9.5, audit_id="S386")
        finding = Confident(value="All 29 bugs addressed", confidence=audit_score)
        assert finding.is_high
        assert not finding.is_low
        assert finding.confidence.value == pytest.approx(0.95)

    def test_chain_two_agents(self):
        """Agent A produces a result, Agent B refines it with lower confidence."""
        agent_a = Confident(
            value="database schema valid",
            confidence=ConfidenceScore(0.9, source=ConfidenceSource.AUDIT),
        )
        agent_b_result = agent_a.and_then(
            lambda finding: Confident(
                value=f"migration safe: {finding}",
                confidence=ConfidenceScore(0.8, source=ConfidenceSource.SELF_REPORTED),
            )
        )
        assert "migration safe" in agent_b_result.value
        assert agent_b_result.confidence.value == pytest.approx(0.72)
        assert agent_b_result.confidence.source == ConfidenceSource.COMPUTED

    def test_swarm_consensus_via_compose(self):
        """Three agents vote, combine with MIN (conservative swarm decision)."""
        scores = (
            ConfidenceScore(value=0.95, evidence=("guardiana:S386",)),
            ConfidenceScore(value=0.88, evidence=("tester:S386",)),
            ConfidenceScore(value=0.72, evidence=("backend:S386",)),
        )
        consensus = compose_scores(scores, CompositionStrategy.MIN)
        assert consensus.value == pytest.approx(0.72)
        assert len(consensus.evidence) == 3

    def test_int_value_confident(self):
        c = Confident(value=997, confidence=ConfidenceScore(1.0))
        doubled = c.map(lambda n: n * 2)
        assert doubled.value == 1994
        assert doubled.confidence.value == pytest.approx(1.0)

    def test_none_value_confident(self):
        c: Confident[None] = Confident(value=None, confidence=ConfidenceScore(0.5))
        assert c.value is None
        assert c.confidence.value == pytest.approx(0.5)
