# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Confidence types for typed agent output certainty.

The first Python package with generic confidence types for AI agents.
No competitor (CrewAI, AutoGen, LangGraph, PydanticAI) has Confident[T]
with automatic composition. ZERO external dependencies.

Research basis: 28 sources including PydanticAI, uncertainties,
llm-confidence, SparkCo confidence scoring.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Generic, Optional, TypeVar

T = TypeVar("T")
U = TypeVar("U")


class ConfidenceSource(Enum):
    """How the confidence score was determined."""

    SELF_REPORTED = "self_reported"  # Agent reported its own confidence
    AUDIT = "audit"                  # Guardiana audit score (most reliable)
    COMPUTED = "computed"            # Derived from composition rules
    INHERITED = "inherited"          # Passed along from upstream agent
    DEFAULT = "default"              # No confidence information (1.0 assumed)


@dataclass(frozen=True)
class ConfidenceScore:
    """A confidence value with provenance.

    value is always 0.0 to 1.0.
    source tracks HOW it was determined.
    evidence is an optional tuple of session/audit references.
    """

    value: float
    source: ConfidenceSource = ConfidenceSource.DEFAULT
    evidence: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not (0.0 <= self.value <= 1.0):
            raise ValueError(f"confidence must be 0.0-1.0, got {self.value}")

    def compose_min(self, other: ConfidenceScore) -> ConfidenceScore:
        """Compose with another score using minimum rule (conservative)."""
        return ConfidenceScore(
            value=min(self.value, other.value),
            source=ConfidenceSource.COMPUTED,
            evidence=self.evidence + other.evidence,
        )

    def compose_product(self, other: ConfidenceScore) -> ConfidenceScore:
        """Compose with another score using product rule (multiplicative)."""
        return ConfidenceScore(
            value=self.value * other.value,
            source=ConfidenceSource.COMPUTED,
            evidence=self.evidence + other.evidence,
        )

    def compose_avg(self, other: ConfidenceScore) -> ConfidenceScore:
        """Compose with another score using arithmetic mean."""
        return ConfidenceScore(
            value=(self.value + other.value) / 2.0,
            source=ConfidenceSource.COMPUTED,
            evidence=self.evidence + other.evidence,
        )

    @staticmethod
    def from_audit_score(score: float, audit_id: str = "") -> ConfidenceScore:
        """Create from a Guardiana audit score (0.0-10.0 -> 0.0-1.0)."""
        if not (0.0 <= score <= 10.0):
            raise ValueError(f"audit score must be 0.0-10.0, got {score}")
        evidence = (f"audit:{audit_id}",) if audit_id else ()
        return ConfidenceScore(
            value=score / 10.0,
            source=ConfidenceSource.AUDIT,
            evidence=evidence,
        )

    @staticmethod
    def full() -> ConfidenceScore:
        """Shorthand for full confidence (1.0)."""
        return ConfidenceScore(value=1.0)

    @staticmethod
    def unknown() -> ConfidenceScore:
        """Shorthand for unknown confidence (0.5)."""
        return ConfidenceScore(value=0.5, source=ConfidenceSource.DEFAULT)


@dataclass(frozen=True)
class Confident(Generic[T]):
    """A value paired with its confidence score.

    This is the core type: wraps any value T with a ConfidenceScore.
    Supports functional composition via map() and and_then().

    Usage::

        result = Confident(value="bug found", confidence=ConfidenceScore(0.9))
        mapped = result.map(str.upper)  # Confident("BUG FOUND", 0.9)
    """

    value: T
    confidence: ConfidenceScore = field(default_factory=ConfidenceScore.full)

    def map(self, fn: Callable[[T], U]) -> Confident[U]:
        """Apply a function to the value, preserving confidence."""
        return Confident(value=fn(self.value), confidence=self.confidence)

    def and_then(self, fn: Callable[[T], Confident[U]]) -> Confident[U]:
        """Chain with another confident computation, composing confidence via product."""
        result = fn(self.value)
        return Confident(
            value=result.value,
            confidence=self.confidence.compose_product(result.confidence),
        )

    @property
    def is_high(self) -> bool:
        """True if confidence >= 0.8."""
        return self.confidence.value >= 0.8

    @property
    def is_low(self) -> bool:
        """True if confidence < 0.5."""
        return self.confidence.value < 0.5


class CompositionStrategy(Enum):
    """How to compose multiple confidence scores."""

    MIN = "min"          # Conservative: take the lowest
    PRODUCT = "product"  # Multiplicative: multiply all
    AVERAGE = "average"  # Balanced: arithmetic mean


def compose_scores(
    scores: tuple[ConfidenceScore, ...],
    strategy: CompositionStrategy = CompositionStrategy.MIN,
) -> ConfidenceScore:
    """Compose multiple confidence scores into one.

    Raises ValueError if scores is empty.
    """
    if not scores:
        raise ValueError("cannot compose empty scores")
    if len(scores) == 1:
        return scores[0]

    if strategy == CompositionStrategy.MIN:
        value = min(s.value for s in scores)
    elif strategy == CompositionStrategy.PRODUCT:
        value = 1.0
        for s in scores:
            value *= s.value
    elif strategy == CompositionStrategy.AVERAGE:
        value = sum(s.value for s in scores) / len(scores)
    else:
        raise ValueError(f"unknown strategy: {strategy}")

    all_evidence: tuple[str, ...] = ()
    for s in scores:
        all_evidence = all_evidence + s.evidence

    return ConfidenceScore(
        value=value,
        source=ConfidenceSource.COMPUTED,
        evidence=all_evidence,
    )
