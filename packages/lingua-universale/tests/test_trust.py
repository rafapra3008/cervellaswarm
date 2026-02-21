# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for trust.py - TrustScore and trust chain composition."""

import pytest

from cervellaswarm_lingua_universale.confidence import ConfidenceScore, ConfidenceSource
from cervellaswarm_lingua_universale.trust import (
    TrustTier,
    TrustScore,
    trust_tier_for_role,
    compose_chain,
    chain_confidence,
    _TIER_VALUES,
)
from cervellaswarm_lingua_universale.types import AgentRole


# ── TrustTier ─────────────────────────────────────────────────────────────────

class TestTrustTier:
    def test_verified_value(self):
        assert TrustTier.VERIFIED.value == "verified"

    def test_trusted_value(self):
        assert TrustTier.TRUSTED.value == "trusted"

    def test_standard_value(self):
        assert TrustTier.STANDARD.value == "standard"

    def test_untrusted_value(self):
        assert TrustTier.UNTRUSTED.value == "untrusted"

    def test_four_members(self):
        assert len(TrustTier) == 4

    def test_tier_values_order(self):
        # VERIFIED > TRUSTED > STANDARD > UNTRUSTED
        assert _TIER_VALUES[TrustTier.VERIFIED] > _TIER_VALUES[TrustTier.TRUSTED]
        assert _TIER_VALUES[TrustTier.TRUSTED] > _TIER_VALUES[TrustTier.STANDARD]
        assert _TIER_VALUES[TrustTier.STANDARD] > _TIER_VALUES[TrustTier.UNTRUSTED]

    def test_verified_is_10(self):
        assert _TIER_VALUES[TrustTier.VERIFIED] == 1.0

    def test_trusted_is_09(self):
        assert _TIER_VALUES[TrustTier.TRUSTED] == 0.9

    def test_standard_is_075(self):
        assert _TIER_VALUES[TrustTier.STANDARD] == 0.75

    def test_untrusted_is_05(self):
        assert _TIER_VALUES[TrustTier.UNTRUSTED] == 0.5


# ── trust_tier_for_role ───────────────────────────────────────────────────────

class TestTrustTierForRole:
    def test_hub_is_verified(self):
        assert trust_tier_for_role(AgentRole.REGINA) == TrustTier.VERIFIED

    def test_guardiana_qualita_is_verified(self):
        assert trust_tier_for_role(AgentRole.GUARDIANA_QUALITA) == TrustTier.VERIFIED

    def test_guardiana_ricerca_is_verified(self):
        assert trust_tier_for_role(AgentRole.GUARDIANA_RICERCA) == TrustTier.VERIFIED

    def test_guardiana_ops_is_verified(self):
        assert trust_tier_for_role(AgentRole.GUARDIANA_OPS) == TrustTier.VERIFIED

    def test_architect_is_trusted(self):
        assert trust_tier_for_role(AgentRole.ARCHITECT) == TrustTier.TRUSTED

    def test_security_is_trusted(self):
        assert trust_tier_for_role(AgentRole.SECURITY) == TrustTier.TRUSTED

    def test_ingegnera_is_trusted(self):
        assert trust_tier_for_role(AgentRole.INGEGNERA) == TrustTier.TRUSTED

    def test_backend_is_standard(self):
        assert trust_tier_for_role(AgentRole.BACKEND) == TrustTier.STANDARD

    def test_frontend_is_standard(self):
        assert trust_tier_for_role(AgentRole.FRONTEND) == TrustTier.STANDARD

    def test_tester_is_standard(self):
        assert trust_tier_for_role(AgentRole.TESTER) == TrustTier.STANDARD

    def test_researcher_is_standard(self):
        assert trust_tier_for_role(AgentRole.RESEARCHER) == TrustTier.STANDARD

    def test_devops_is_standard(self):
        assert trust_tier_for_role(AgentRole.DEVOPS) == TrustTier.STANDARD

    def test_docs_is_standard(self):
        assert trust_tier_for_role(AgentRole.DOCS) == TrustTier.STANDARD

    def test_data_is_standard(self):
        assert trust_tier_for_role(AgentRole.DATA) == TrustTier.STANDARD

    def test_marketing_is_standard(self):
        assert trust_tier_for_role(AgentRole.MARKETING) == TrustTier.STANDARD

    def test_scienziata_is_standard(self):
        assert trust_tier_for_role(AgentRole.SCIENZIATA) == TrustTier.STANDARD

    def test_reviewer_is_standard(self):
        assert trust_tier_for_role(AgentRole.REVIEWER) == TrustTier.STANDARD


# ── TrustScore creation ───────────────────────────────────────────────────────

class TestTrustScoreCreation:
    def test_basic_creation(self):
        ts = TrustScore(value=0.8)
        assert ts.value == 0.8
        assert ts.tier == TrustTier.STANDARD
        assert ts.reason == ""

    def test_creation_with_tier(self):
        ts = TrustScore(value=1.0, tier=TrustTier.VERIFIED)
        assert ts.tier == TrustTier.VERIFIED

    def test_creation_with_reason(self):
        ts = TrustScore(value=0.75, reason="audit:S386")
        assert ts.reason == "audit:S386"

    def test_frozen(self):
        ts = TrustScore(value=0.5)
        with pytest.raises((AttributeError, TypeError)):
            ts.value = 0.9  # type: ignore[misc]

    def test_value_zero_ok(self):
        ts = TrustScore(value=0.0)
        assert ts.value == 0.0

    def test_value_one_ok(self):
        ts = TrustScore(value=1.0)
        assert ts.value == 1.0

    def test_value_midpoint(self):
        ts = TrustScore(value=0.5)
        assert ts.value == 0.5


# ── TrustScore validation ─────────────────────────────────────────────────────

class TestTrustScoreValidation:
    def test_rejects_negative(self):
        with pytest.raises(ValueError, match="0.0-1.0"):
            TrustScore(value=-0.1)

    def test_rejects_above_one(self):
        with pytest.raises(ValueError, match="0.0-1.0"):
            TrustScore(value=1.001)

    def test_rejects_large_positive(self):
        with pytest.raises(ValueError, match="0.0-1.0"):
            TrustScore(value=10.0)

    def test_rejects_large_negative(self):
        with pytest.raises(ValueError, match="0.0-1.0"):
            TrustScore(value=-5.0)

    def test_boundary_exactly_zero_ok(self):
        ts = TrustScore(value=0.0)
        assert ts.value == 0.0

    def test_boundary_exactly_one_ok(self):
        ts = TrustScore(value=1.0)
        assert ts.value == 1.0


# ── TrustScore.full() and cold_start() ───────────────────────────────────────

class TestTrustScoreShorthands:
    def test_full_value(self):
        ts = TrustScore.full()
        assert ts.value == 1.0

    def test_full_tier(self):
        ts = TrustScore.full()
        assert ts.tier == TrustTier.VERIFIED

    def test_full_reason(self):
        ts = TrustScore.full()
        assert ts.reason == "full"

    def test_cold_start_value(self):
        ts = TrustScore.cold_start()
        assert ts.value == 0.5

    def test_cold_start_tier(self):
        ts = TrustScore.cold_start()
        assert ts.tier == TrustTier.UNTRUSTED

    def test_cold_start_reason(self):
        ts = TrustScore.cold_start()
        assert ts.reason == "cold_start"

    def test_full_and_cold_start_differ(self):
        assert TrustScore.full() != TrustScore.cold_start()


# ── TrustScore.for_role() ─────────────────────────────────────────────────────

class TestTrustScoreForRole:
    def test_regina_gets_verified_value(self):
        ts = TrustScore.for_role(AgentRole.REGINA)
        assert ts.value == pytest.approx(1.0)

    def test_regina_gets_verified_tier(self):
        ts = TrustScore.for_role(AgentRole.REGINA)
        assert ts.tier == TrustTier.VERIFIED

    def test_guardiana_qualita_gets_verified(self):
        ts = TrustScore.for_role(AgentRole.GUARDIANA_QUALITA)
        assert ts.value == pytest.approx(1.0)
        assert ts.tier == TrustTier.VERIFIED

    def test_architect_gets_trusted_value(self):
        ts = TrustScore.for_role(AgentRole.ARCHITECT)
        assert ts.value == pytest.approx(0.9)

    def test_architect_gets_trusted_tier(self):
        ts = TrustScore.for_role(AgentRole.ARCHITECT)
        assert ts.tier == TrustTier.TRUSTED

    def test_backend_gets_standard_value(self):
        ts = TrustScore.for_role(AgentRole.BACKEND)
        assert ts.value == pytest.approx(0.75)

    def test_backend_gets_standard_tier(self):
        ts = TrustScore.for_role(AgentRole.BACKEND)
        assert ts.tier == TrustTier.STANDARD

    def test_reason_contains_role_value(self):
        ts = TrustScore.for_role(AgentRole.BACKEND)
        assert "backend" in ts.reason

    def test_reason_contains_default_prefix(self):
        ts = TrustScore.for_role(AgentRole.ARCHITECT)
        assert ts.reason.startswith("default(")

    def test_all_worker_roles_get_standard(self):
        workers = [
            AgentRole.BACKEND, AgentRole.FRONTEND, AgentRole.TESTER,
            AgentRole.RESEARCHER, AgentRole.MARKETING, AgentRole.DEVOPS,
            AgentRole.DOCS, AgentRole.DATA, AgentRole.SCIENZIATA,
            AgentRole.REVIEWER,
        ]
        for role in workers:
            ts = TrustScore.for_role(role)
            assert ts.tier == TrustTier.STANDARD, f"{role} should be STANDARD"
            assert ts.value == pytest.approx(0.75), f"{role} value should be 0.75"


# ── TrustScore.compose() ──────────────────────────────────────────────────────

class TestTrustScoreCompose:
    def test_compose_multiplies_values(self):
        a = TrustScore(value=0.9, tier=TrustTier.VERIFIED)
        b = TrustScore(value=0.8, tier=TrustTier.STANDARD)
        result = a.compose(b)
        assert result.value == pytest.approx(0.72)

    def test_compose_picks_lower_tier(self):
        a = TrustScore(value=1.0, tier=TrustTier.VERIFIED)
        b = TrustScore(value=0.75, tier=TrustTier.STANDARD)
        result = a.compose(b)
        assert result.tier == TrustTier.STANDARD

    def test_compose_picks_lower_tier_reversed(self):
        a = TrustScore(value=0.75, tier=TrustTier.STANDARD)
        b = TrustScore(value=1.0, tier=TrustTier.VERIFIED)
        result = a.compose(b)
        assert result.tier == TrustTier.STANDARD

    def test_compose_equal_tiers_keeps_tier(self):
        a = TrustScore(value=0.9, tier=TrustTier.TRUSTED)
        b = TrustScore(value=0.8, tier=TrustTier.TRUSTED)
        result = a.compose(b)
        assert result.tier == TrustTier.TRUSTED

    def test_compose_reason_includes_both(self):
        a = TrustScore(value=0.9, tier=TrustTier.VERIFIED, reason="alice")
        b = TrustScore(value=0.8, tier=TrustTier.STANDARD, reason="bob")
        result = a.compose(b)
        assert "alice" in result.reason
        assert "bob" in result.reason

    def test_compose_reason_uses_tier_value_when_no_reason(self):
        a = TrustScore(value=0.9, tier=TrustTier.VERIFIED)
        b = TrustScore(value=0.8, tier=TrustTier.STANDARD)
        result = a.compose(b)
        assert "verified" in result.reason
        assert "standard" in result.reason

    def test_compose_reason_starts_with_composed(self):
        a = TrustScore(value=0.9, tier=TrustTier.VERIFIED)
        b = TrustScore(value=0.8, tier=TrustTier.STANDARD)
        result = a.compose(b)
        assert result.reason.startswith("composed(")

    def test_compose_returns_new_object(self):
        a = TrustScore(value=0.9, tier=TrustTier.VERIFIED)
        b = TrustScore(value=0.8, tier=TrustTier.STANDARD)
        result = a.compose(b)
        assert result is not a
        assert result is not b

    def test_compose_with_full_is_identity_on_value(self):
        a = TrustScore(value=0.75, tier=TrustTier.STANDARD)
        full = TrustScore.full()
        result = a.compose(full)
        assert result.value == pytest.approx(0.75)

    def test_compose_with_zero_gives_zero(self):
        a = TrustScore(value=0.9, tier=TrustTier.VERIFIED)
        zero = TrustScore(value=0.0, tier=TrustTier.UNTRUSTED)
        result = a.compose(zero)
        assert result.value == pytest.approx(0.0)

    def test_compose_is_commutative_on_value(self):
        a = TrustScore(value=0.8, tier=TrustTier.TRUSTED)
        b = TrustScore(value=0.6, tier=TrustTier.STANDARD)
        assert a.compose(b).value == pytest.approx(b.compose(a).value)

    def test_compose_tier_untrusted_dominates(self):
        a = TrustScore(value=1.0, tier=TrustTier.VERIFIED)
        b = TrustScore(value=0.5, tier=TrustTier.UNTRUSTED)
        result = a.compose(b)
        assert result.tier == TrustTier.UNTRUSTED

    def test_compose_three_agents_associative(self):
        # (A . B) . C == A . (B . C) for values
        a = TrustScore(value=0.9, tier=TrustTier.VERIFIED)
        b = TrustScore(value=0.8, tier=TrustTier.TRUSTED)
        c = TrustScore(value=0.75, tier=TrustTier.STANDARD)
        left = a.compose(b).compose(c)
        right = a.compose(b.compose(c))
        assert left.value == pytest.approx(right.value)


# ── TrustScore.attenuate() ────────────────────────────────────────────────────

class TestTrustScoreAttenuate:
    def test_attenuate_reduces_value(self):
        ts = TrustScore(value=0.8, tier=TrustTier.VERIFIED)
        result = ts.attenuate(0.5)
        assert result.value == pytest.approx(0.4)

    def test_attenuate_preserves_tier(self):
        ts = TrustScore(value=0.8, tier=TrustTier.VERIFIED)
        result = ts.attenuate(0.5)
        assert result.tier == TrustTier.VERIFIED

    def test_attenuate_with_one_is_identity(self):
        ts = TrustScore(value=0.75, tier=TrustTier.STANDARD)
        result = ts.attenuate(1.0)
        assert result.value == pytest.approx(0.75)

    def test_attenuate_with_zero_gives_zero(self):
        ts = TrustScore(value=0.9, tier=TrustTier.TRUSTED)
        result = ts.attenuate(0.0)
        assert result.value == pytest.approx(0.0)

    def test_attenuate_reason_includes_original_reason(self):
        ts = TrustScore(value=0.8, tier=TrustTier.TRUSTED, reason="alice")
        result = ts.attenuate(0.5)
        assert "alice" in result.reason

    def test_attenuate_reason_includes_factor(self):
        ts = TrustScore(value=0.8, tier=TrustTier.TRUSTED)
        result = ts.attenuate(0.5)
        assert "0.5" in result.reason

    def test_attenuate_reason_starts_with_attenuated(self):
        ts = TrustScore(value=0.8, tier=TrustTier.TRUSTED)
        result = ts.attenuate(0.5)
        assert result.reason.startswith("attenuated(")

    def test_attenuate_returns_new_object(self):
        ts = TrustScore(value=0.8, tier=TrustTier.STANDARD)
        result = ts.attenuate(0.9)
        assert result is not ts

    def test_attenuate_result_always_le_original(self):
        ts = TrustScore(value=0.9, tier=TrustTier.VERIFIED)
        for factor in [0.0, 0.1, 0.5, 0.9, 1.0]:
            result = ts.attenuate(factor)
            assert result.value <= ts.value + 1e-10

    def test_attenuate_rejects_negative_factor(self):
        ts = TrustScore(value=0.8, tier=TrustTier.STANDARD)
        with pytest.raises(ValueError, match="0.0-1.0"):
            ts.attenuate(-0.1)

    def test_attenuate_rejects_factor_above_one(self):
        ts = TrustScore(value=0.8, tier=TrustTier.STANDARD)
        with pytest.raises(ValueError, match="0.0-1.0"):
            ts.attenuate(1.001)

    def test_attenuate_reason_uses_tier_when_no_reason(self):
        ts = TrustScore(value=0.8, tier=TrustTier.STANDARD)
        result = ts.attenuate(0.5)
        assert "standard" in result.reason


# ── TrustScore.to_confidence() ────────────────────────────────────────────────

class TestTrustScoreToConfidence:
    def test_to_confidence_preserves_value(self):
        ts = TrustScore(value=0.9, tier=TrustTier.VERIFIED)
        cs = ts.to_confidence()
        assert cs.value == pytest.approx(0.9)

    def test_to_confidence_source_is_inherited(self):
        ts = TrustScore(value=0.9, tier=TrustTier.VERIFIED)
        cs = ts.to_confidence()
        assert cs.source == ConfidenceSource.INHERITED

    def test_to_confidence_evidence_includes_tier(self):
        ts = TrustScore(value=1.0, tier=TrustTier.VERIFIED)
        cs = ts.to_confidence()
        assert "trust:verified" in cs.evidence

    def test_to_confidence_trusted_tier_evidence(self):
        ts = TrustScore(value=0.9, tier=TrustTier.TRUSTED)
        cs = ts.to_confidence()
        assert "trust:trusted" in cs.evidence

    def test_to_confidence_standard_tier_evidence(self):
        ts = TrustScore(value=0.75, tier=TrustTier.STANDARD)
        cs = ts.to_confidence()
        assert "trust:standard" in cs.evidence

    def test_to_confidence_untrusted_tier_evidence(self):
        ts = TrustScore(value=0.5, tier=TrustTier.UNTRUSTED)
        cs = ts.to_confidence()
        assert "trust:untrusted" in cs.evidence

    def test_to_confidence_returns_confidence_score_instance(self):
        ts = TrustScore(value=0.8, tier=TrustTier.TRUSTED)
        cs = ts.to_confidence()
        assert isinstance(cs, ConfidenceScore)

    def test_to_confidence_zero_value(self):
        ts = TrustScore(value=0.0, tier=TrustTier.UNTRUSTED)
        cs = ts.to_confidence()
        assert cs.value == pytest.approx(0.0)

    def test_to_confidence_full_value(self):
        ts = TrustScore.full()
        cs = ts.to_confidence()
        assert cs.value == pytest.approx(1.0)


# ── compose_chain() ───────────────────────────────────────────────────────────

class TestComposeChain:
    def test_empty_raises_value_error(self):
        with pytest.raises(ValueError, match="empty"):
            compose_chain(())

    def test_single_returns_same(self):
        ts = TrustScore(value=0.9, tier=TrustTier.VERIFIED)
        result = compose_chain((ts,))
        assert result is ts

    def test_two_agents_multiplicative(self):
        a = TrustScore(value=0.9, tier=TrustTier.VERIFIED)
        b = TrustScore(value=0.8, tier=TrustTier.STANDARD)
        result = compose_chain((a, b))
        assert result.value == pytest.approx(0.72)

    def test_two_agents_lower_tier(self):
        a = TrustScore(value=1.0, tier=TrustTier.VERIFIED)
        b = TrustScore(value=0.75, tier=TrustTier.STANDARD)
        result = compose_chain((a, b))
        assert result.tier == TrustTier.STANDARD

    def test_three_agents_product(self):
        a = TrustScore(value=1.0, tier=TrustTier.VERIFIED)
        b = TrustScore(value=0.9, tier=TrustTier.TRUSTED)
        c = TrustScore(value=0.75, tier=TrustTier.STANDARD)
        result = compose_chain((a, b, c))
        assert result.value == pytest.approx(1.0 * 0.9 * 0.75)

    def test_three_agents_lowest_tier(self):
        a = TrustScore(value=1.0, tier=TrustTier.VERIFIED)
        b = TrustScore(value=0.9, tier=TrustTier.TRUSTED)
        c = TrustScore(value=0.75, tier=TrustTier.STANDARD)
        result = compose_chain((a, b, c))
        assert result.tier == TrustTier.STANDARD

    def test_chain_with_cold_start_gives_low_trust(self):
        a = TrustScore.full()
        b = TrustScore.cold_start()
        result = compose_chain((a, b))
        assert result.value == pytest.approx(0.5)

    def test_chain_attenuates_trust(self):
        # Each hop reduces trust
        ts = TrustScore(value=0.9, tier=TrustTier.VERIFIED)
        chain = (ts, ts, ts)
        result = compose_chain(chain)
        assert result.value == pytest.approx(0.9 ** 3)

    def test_chain_with_zero_gives_zero(self):
        a = TrustScore.full()
        b = TrustScore(value=0.0, tier=TrustTier.UNTRUSTED)
        c = TrustScore.full()
        result = compose_chain((a, b, c))
        assert result.value == pytest.approx(0.0)

    def test_chain_order_does_not_change_product(self):
        a = TrustScore(value=0.9, tier=TrustTier.VERIFIED)
        b = TrustScore(value=0.8, tier=TrustTier.TRUSTED)
        c = TrustScore(value=0.7, tier=TrustTier.STANDARD)
        abc = compose_chain((a, b, c))
        bca = compose_chain((b, c, a))
        assert abc.value == pytest.approx(bca.value)


# ── chain_confidence() ────────────────────────────────────────────────────────

class TestChainConfidence:
    def test_empty_chain_returns_output_confidence_unchanged(self):
        output = ConfidenceScore(value=0.9, source=ConfidenceSource.AUDIT)
        result = chain_confidence((), output)
        assert result is output

    def test_single_agent_full_trust_is_identity_on_confidence(self):
        trust_chain = (TrustScore.full(),)
        output = ConfidenceScore(value=0.8)
        result = chain_confidence(trust_chain, output)
        assert result.value == pytest.approx(0.8)

    def test_single_agent_partial_trust_reduces_confidence(self):
        trust_chain = (TrustScore(value=0.9, tier=TrustTier.TRUSTED),)
        output = ConfidenceScore(value=0.8)
        result = chain_confidence(trust_chain, output)
        assert result.value == pytest.approx(0.72)

    def test_two_agents_trust_times_confidence(self):
        a = TrustScore(value=0.9, tier=TrustTier.VERIFIED)
        b = TrustScore(value=0.8, tier=TrustTier.STANDARD)
        output = ConfidenceScore(value=0.9)
        # chain trust = 0.72, final = 0.72 * 0.9
        result = chain_confidence((a, b), output)
        assert result.value == pytest.approx(0.72 * 0.9)

    def test_result_source_is_computed(self):
        trust_chain = (TrustScore(value=0.9, tier=TrustTier.TRUSTED),)
        output = ConfidenceScore(value=0.8, source=ConfidenceSource.AUDIT)
        result = chain_confidence(trust_chain, output)
        assert result.source == ConfidenceSource.COMPUTED

    def test_cold_start_agent_sharply_reduces_confidence(self):
        trust_chain = (TrustScore.cold_start(),)
        output = ConfidenceScore(value=0.9)
        result = chain_confidence(trust_chain, output)
        assert result.value == pytest.approx(0.45)

    def test_chain_accumulates_evidence(self):
        trust_chain = (TrustScore(value=0.9, tier=TrustTier.VERIFIED),)
        output = ConfidenceScore(value=0.8, evidence=("audit:S386",))
        result = chain_confidence(trust_chain, output)
        assert "trust:verified" in result.evidence
        assert "audit:S386" in result.evidence

    def test_zero_trust_in_chain_gives_zero_confidence(self):
        trust_chain = (TrustScore(value=0.0, tier=TrustTier.UNTRUSTED),)
        output = ConfidenceScore(value=1.0)
        result = chain_confidence(trust_chain, output)
        assert result.value == pytest.approx(0.0)

    def test_three_agents_in_chain(self):
        a = TrustScore(value=1.0, tier=TrustTier.VERIFIED)
        b = TrustScore(value=0.9, tier=TrustTier.TRUSTED)
        c = TrustScore(value=0.75, tier=TrustTier.STANDARD)
        output = ConfidenceScore(value=0.9)
        chain_trust = 1.0 * 0.9 * 0.75
        result = chain_confidence((a, b, c), output)
        assert result.value == pytest.approx(chain_trust * 0.9)


# ── Edge cases ────────────────────────────────────────────────────────────────

class TestEdgeCases:
    def test_trust_score_equality_same_values(self):
        a = TrustScore(value=0.9, tier=TrustTier.VERIFIED, reason="x")
        b = TrustScore(value=0.9, tier=TrustTier.VERIFIED, reason="x")
        assert a == b

    def test_trust_score_inequality_different_tier(self):
        a = TrustScore(value=0.9, tier=TrustTier.VERIFIED)
        b = TrustScore(value=0.9, tier=TrustTier.TRUSTED)
        assert a != b

    def test_compose_verified_with_untrusted(self):
        verified = TrustScore.full()
        untrusted = TrustScore.cold_start()
        result = verified.compose(untrusted)
        assert result.tier == TrustTier.UNTRUSTED
        assert result.value == pytest.approx(0.5)

    def test_attenuate_zero_from_one_gives_zero(self):
        ts = TrustScore.full()
        result = ts.attenuate(0.0)
        assert result.value == pytest.approx(0.0)
        assert result.tier == TrustTier.VERIFIED

    def test_to_confidence_compose_product_valid(self):
        ts = TrustScore(value=0.9, tier=TrustTier.TRUSTED)
        cs = ts.to_confidence()
        other = ConfidenceScore(value=0.8)
        combined = cs.compose_product(other)
        assert combined.value == pytest.approx(0.72)

    def test_for_role_returns_frozen(self):
        ts = TrustScore.for_role(AgentRole.BACKEND)
        with pytest.raises((AttributeError, TypeError)):
            ts.value = 0.9  # type: ignore[misc]

    def test_chain_confidence_empty_with_zero_confidence(self):
        output = ConfidenceScore(value=0.0)
        result = chain_confidence((), output)
        assert result.value == pytest.approx(0.0)


# ── Realistic scenarios ───────────────────────────────────────────────────────

class TestRealisticScenarios:
    def test_regina_to_guardiana_to_worker_chain(self):
        """Regina delegates to Guardiana, who delegates to Backend worker."""
        regina = TrustScore.for_role(AgentRole.REGINA)
        guardiana = TrustScore.for_role(AgentRole.GUARDIANA_QUALITA)
        backend = TrustScore.for_role(AgentRole.BACKEND)

        chain = compose_chain((regina, guardiana, backend))
        # 1.0 * 1.0 * 0.75 = 0.75
        assert chain.value == pytest.approx(0.75)
        assert chain.tier == TrustTier.STANDARD

    def test_audit_verdict_with_trust_chain(self):
        """Audit score combined with trust chain to get real confidence."""
        audit_confidence = ConfidenceScore.from_audit_score(9.5, audit_id="S387")
        trust_chain = (
            TrustScore.for_role(AgentRole.REGINA),
            TrustScore.for_role(AgentRole.GUARDIANA_QUALITA),
        )
        # chain trust = 1.0 * 1.0 = 1.0, result = 1.0 * 0.95 = 0.95
        result = chain_confidence(trust_chain, audit_confidence)
        assert result.value == pytest.approx(0.95)

    def test_cold_start_agent_in_chain_reduces_trust_significantly(self):
        """A new unknown agent in the chain reduces overall trust."""
        regina = TrustScore.for_role(AgentRole.REGINA)
        unknown = TrustScore.cold_start()
        backend = TrustScore.for_role(AgentRole.BACKEND)

        chain = compose_chain((regina, unknown, backend))
        # 1.0 * 0.5 * 0.75 = 0.375
        assert chain.value == pytest.approx(0.375)
        assert chain.tier == TrustTier.UNTRUSTED

    def test_privilege_attenuation_cannot_exceed_original(self):
        """B cannot grant C more authority than A gave B."""
        a_to_b = TrustScore(value=0.6, tier=TrustTier.STANDARD, reason="A->B")
        # B tries to give C full trust (1.0), but compose attenuates
        b_to_c = TrustScore(value=1.0, tier=TrustTier.VERIFIED, reason="B->C")
        result = a_to_b.compose(b_to_c)
        assert result.value <= a_to_b.value + 1e-10

    def test_architect_to_worker_workflow(self):
        """Architect plans, Backend executes with trust chain."""
        architect = TrustScore.for_role(AgentRole.ARCHITECT)
        backend = TrustScore.for_role(AgentRole.BACKEND)
        output = ConfidenceScore(value=0.95, source=ConfidenceSource.SELF_REPORTED)

        result = chain_confidence((architect, backend), output)
        # 0.9 * 0.75 * 0.95
        assert result.value == pytest.approx(0.9 * 0.75 * 0.95)

    def test_trust_attenuation_before_delegation(self):
        """Regina attenuates trust before giving to worker (Privilege Attenuation)."""
        regina = TrustScore.for_role(AgentRole.REGINA)
        attenuated = regina.attenuate(0.8)
        worker = TrustScore.for_role(AgentRole.BACKEND)
        chain = compose_chain((attenuated, worker))
        # 0.8 * 0.75 = 0.6
        assert chain.value == pytest.approx(0.8 * 0.75)

    def test_full_guardiana_pipeline(self):
        """Guardiana audits a backend output with trust fully applied."""
        # Guardiana has VERIFIED trust
        guardiana_trust = TrustScore.for_role(AgentRole.GUARDIANA_QUALITA)
        # Backend result scored 9.3/10 by Guardiana
        audit_score = ConfidenceScore.from_audit_score(9.3, audit_id="S387")
        result = chain_confidence((guardiana_trust,), audit_score)
        # 1.0 * 0.93 = 0.93
        assert result.value == pytest.approx(0.93)
        assert "trust:verified" in result.evidence
        assert "audit:S387" in result.evidence
