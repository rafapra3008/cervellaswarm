# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Trust composition for multi-agent protocol chains.

Models how trust propagates when agents delegate to other agents.
Based on Subjective Logic (Josang 2016) and DeepMind's Intelligent
AI Delegation (2026) principles:
- Privilege Attenuation: B cannot give C more authority than A gave B
- Transitive Accountability: every link in the chain is accountable
- Graduated Authority: lower trust = stricter constraints

ZERO external dependencies. Uses confidence.py for score integration.
"""

from __future__ import annotations

from enum import Enum
from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from .confidence import ConfidenceScore, ConfidenceSource
from .types import AgentRole


class TrustTier(Enum):
    """Trust tiers mapped to agent capability levels.

    Values are default trust scores for cold-start.
    """

    VERIFIED = "verified"    # Guardiana-audited, full authority
    TRUSTED = "trusted"      # Opus agents, domain expertise
    STANDARD = "standard"    # Sonnet workers, task execution
    UNTRUSTED = "untrusted"  # Unknown/new agents, probation


# Default trust by agent tier (from AgentRole.tier)
_TIER_TRUST: Mapping[str, TrustTier] = MappingProxyType({
    "hub": TrustTier.VERIFIED,
    "guardiana": TrustTier.VERIFIED,
    "strategic": TrustTier.TRUSTED,
    "worker": TrustTier.STANDARD,
})


def trust_tier_for_role(role: AgentRole) -> TrustTier:
    """Determine trust tier from an agent's role."""
    return _TIER_TRUST.get(role.tier, TrustTier.UNTRUSTED)


# Default numeric values for each trust tier
_TIER_VALUES: Mapping[TrustTier, float] = MappingProxyType({
    TrustTier.VERIFIED: 1.0,
    TrustTier.TRUSTED: 0.9,
    TrustTier.STANDARD: 0.75,
    TrustTier.UNTRUSTED: 0.5,
})


@dataclass(frozen=True)
class TrustScore:
    """A trust value with provenance.

    value is always 0.0 to 1.0.
    tier tracks the categorical trust level.
    reason documents why this trust level was assigned.
    """

    value: float
    tier: TrustTier = TrustTier.STANDARD
    reason: str = ""

    def __post_init__(self) -> None:
        if not (0.0 <= self.value <= 1.0):
            raise ValueError(f"trust must be 0.0-1.0, got {self.value}")

    def compose(self, other: TrustScore) -> TrustScore:
        """Compose trust transitively: A trusts B, B trusts C -> A trusts C.

        Uses multiplicative composition (Subjective Logic discounting).
        Result tier is the LOWER of the two (lower value = lower tier).
        """
        composed_value = self.value * other.value
        # Lower tier = lower _TIER_VALUES numeric
        if _TIER_VALUES[self.tier] <= _TIER_VALUES[other.tier]:
            composed_tier = self.tier
        else:
            composed_tier = other.tier
        return TrustScore(
            value=composed_value,
            tier=composed_tier,
            reason=f"composed({self.reason or self.tier.value}, {other.reason or other.tier.value})",
        )

    def attenuate(self, factor: float) -> TrustScore:
        """Attenuate trust by a factor (Privilege Attenuation).

        factor must be 0.0-1.0. The result is always <= original.
        """
        if not (0.0 <= factor <= 1.0):
            raise ValueError(f"attenuation factor must be 0.0-1.0, got {factor}")
        return TrustScore(
            value=self.value * factor,
            tier=self.tier,
            reason=f"attenuated({self.reason or self.tier.value}, {factor})",
        )

    def to_confidence(self) -> ConfidenceScore:
        """Convert trust score to confidence score."""
        return ConfidenceScore(
            value=self.value,
            source=ConfidenceSource.INHERITED,
            evidence=(f"trust:{self.tier.value}",),
        )

    @staticmethod
    def for_role(role: AgentRole) -> TrustScore:
        """Create default trust score for an agent role."""
        tier = trust_tier_for_role(role)
        return TrustScore(
            value=_TIER_VALUES[tier],
            tier=tier,
            reason=f"default({role.value})",
        )

    @staticmethod
    def full() -> TrustScore:
        """Full trust (1.0, VERIFIED)."""
        return TrustScore(value=1.0, tier=TrustTier.VERIFIED, reason="full")

    @staticmethod
    def cold_start() -> TrustScore:
        """Cold start trust for unknown agents (0.5, UNTRUSTED)."""
        return TrustScore(value=0.5, tier=TrustTier.UNTRUSTED, reason="cold_start")


def compose_chain(scores: tuple[TrustScore, ...]) -> TrustScore:
    """Compose a chain of trust scores (A -> B -> C -> ...).

    Uses multiplicative composition. The chain result is the
    product of all individual trust scores.

    Raises ValueError if scores is empty.
    """
    if not scores:
        raise ValueError("cannot compose empty trust chain")
    result = scores[0]
    for score in scores[1:]:
        result = result.compose(score)
    return result


def chain_confidence(
    trust_chain: tuple[TrustScore, ...],
    output_confidence: ConfidenceScore,
) -> ConfidenceScore:
    """Combine a trust chain with output confidence.

    The final confidence is: chain_trust * output_confidence.
    This gives the "real" confidence accounting for trust in each agent.
    """
    if not trust_chain:
        return output_confidence
    chain = compose_chain(trust_chain)
    return chain.to_confidence().compose_product(output_confidence)
