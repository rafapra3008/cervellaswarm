# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""
Content quality scoring for session documents.

Scores content across 4 dimensions:
- Actionability (30%): concrete next steps, decisions, action items
- Specificity (30%): specific names, numbers, file paths (not vague)
- Freshness (20%): dates, session numbers, timestamps
- Conciseness (20%): information density (not bloated with filler)

Each dimension returns 0.0-10.0, weighted sum gives total 0.0-10.0.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class QualityScore:
    """Result of content quality scoring."""

    actionability: float
    specificity: float
    freshness: float
    conciseness: float
    total: float

    def passes(self, min_score: float = 7.0) -> bool:
        """Check if total score meets minimum threshold."""
        return self.total >= min_score


# --- Actionability patterns ---

_ACTION_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"^\s*[-*]\s*\[[ x]\]", re.MULTILINE),  # checklists
    re.compile(r"(?i)\b(TODO|FIXME|HACK|XXX)\b"),
    re.compile(r"(?i)\bnext\s+steps?\b"),
    re.compile(r"(?i)\baction\s+items?\b"),
    re.compile(r"(?i)\b(will|should|must|need\s+to)\b"),
    re.compile(r"(?i)\bprossim[io]\s+step\b"),  # Italian
    re.compile(r"(?i)\bdecisi[oa]n[ei]?\b"),
    re.compile(r"^\s*\d+\.\s+", re.MULTILINE),  # numbered lists
)


def _score_actionability(content: str) -> float:
    """Score how actionable the content is (0.0-10.0)."""
    if not content.strip():
        return 0.0

    hits = sum(1 for pat in _ACTION_PATTERNS if pat.search(content))
    # Scale: 0 hits = 0, 1 = 3, 2 = 5, 3 = 7, 4+ = 8, 6+ = 10
    scale = {0: 0.0, 1: 3.0, 2: 5.0, 3: 7.0, 4: 8.0, 5: 9.0}
    if hits >= len(scale):
        return 10.0
    return scale.get(hits, 10.0)


# --- Specificity patterns ---

_SPECIFICITY_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"[a-zA-Z_]\w*\.(py|js|ts|md|yaml|toml|sh)\b"),  # filenames
    re.compile(r"\b\d+(\.\d+)+\b"),  # version numbers
    re.compile(r"\b(v?\d+\.\d+)\b"),  # short versions
    re.compile(r"\bS\d{2,4}\b"),  # session numbers
    re.compile(r"\b\d+\s*(test|file|modul|line|bug|fix|issue)", re.IGNORECASE),  # counts
    re.compile(r"`[^`]+`"),  # inline code
    re.compile(r"\b[A-Z][a-z]+(?:[A-Z][a-z]+)+\b"),  # CamelCase identifiers
    re.compile(r"\b\w+_\w+\b"),  # snake_case identifiers
)


def _score_specificity(content: str) -> float:
    """Score how specific the content is (0.0-10.0)."""
    if not content.strip():
        return 0.0

    hits = sum(1 for pat in _SPECIFICITY_PATTERNS if pat.search(content))
    scale = {0: 0.0, 1: 2.0, 2: 4.0, 3: 6.0, 4: 7.0, 5: 8.0, 6: 9.0}
    if hits >= len(scale):
        return 10.0
    return scale.get(hits, 10.0)


# --- Freshness patterns ---

_FRESHNESS_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"\b\d{4}-\d{2}-\d{2}\b"),  # ISO dates
    re.compile(r"\b(Sessione|Session)\s+\d+\b", re.IGNORECASE),
    re.compile(r"\bS\d{2,4}\b"),  # S392 style
    re.compile(r"\b(today|yesterday|oggi|ieri)\b", re.IGNORECASE),
    re.compile(r"\b\d{1,2}\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)", re.IGNORECASE),
    re.compile(r"(?i)\b(ultimo|last)\s+aggiornamento\b"),
)


def _score_freshness(content: str) -> float:
    """Score how fresh/dated the content is (0.0-10.0)."""
    if not content.strip():
        return 0.0

    hits = sum(1 for pat in _FRESHNESS_PATTERNS if pat.search(content))
    scale = {0: 0.0, 1: 4.0, 2: 6.0, 3: 8.0, 4: 9.0}
    if hits >= len(scale):
        return 10.0
    return scale.get(hits, 10.0)


# --- Conciseness scoring ---


def _score_conciseness(content: str) -> float:
    """Score information density (0.0-10.0).

    Measures ratio of meaningful lines to total lines.
    Penalizes excessive blank lines, very long documents, and filler.
    """
    if not content.strip():
        return 0.0

    lines = content.split("\n")
    total = len(lines)
    non_blank = sum(1 for line in lines if line.strip())

    if total == 0:
        return 0.0

    # Ratio of non-blank to total
    density = non_blank / total

    # Penalty for very long docs (> 200 lines)
    length_penalty = 0.0
    if total > 300:
        length_penalty = 2.0
    elif total > 200:
        length_penalty = 1.0

    # Base score from density
    if density >= 0.80:
        base = 10.0
    elif density >= 0.70:
        base = 8.0
    elif density >= 0.60:
        base = 6.0
    elif density >= 0.50:
        base = 4.0
    else:
        base = 2.0

    return max(0.0, base - length_penalty)


# --- Public API ---

from types import MappingProxyType

# P04: Immutable global with MappingProxyType
DEFAULT_WEIGHTS: MappingProxyType = MappingProxyType({
    "actionability": 0.30,
    "specificity": 0.30,
    "freshness": 0.20,
    "conciseness": 0.20,
})


def score_content(
    content: str,
    weights: dict[str, float] | None = None,
) -> QualityScore:
    """Score content quality across 4 dimensions.

    Args:
        content: The text content to score.
        weights: Custom weights for each dimension. Keys must sum to ~1.0.
            Defaults: actionability=0.30, specificity=0.30, freshness=0.20, conciseness=0.20.

    Returns:
        QualityScore with individual dimension scores and weighted total.
    """
    w = dict(weights) if weights else dict(DEFAULT_WEIGHTS)  # P11: defensive copy

    weight_sum = sum(w.values())
    if abs(weight_sum - 1.0) > 0.05:
        raise ValueError(f"Weights must sum to ~1.0, got {weight_sum:.2f}")

    actionability = _score_actionability(content)
    specificity = _score_specificity(content)
    freshness = _score_freshness(content)
    conciseness = _score_conciseness(content)

    total = (
        actionability * w.get("actionability", 0.30)
        + specificity * w.get("specificity", 0.30)
        + freshness * w.get("freshness", 0.20)
        + conciseness * w.get("conciseness", 0.20)
    )
    total = max(0.0, min(10.0, total))

    return QualityScore(
        actionability=actionability,
        specificity=specificity,
        freshness=freshness,
        conciseness=conciseness,
        total=total,
    )


def _extract_file_path(line: str) -> str | None:
    """Extract a file path from a line of text.

    Looks for patterns like: path/to/file.py, ./file.md, /absolute/path.yaml
    """
    match = re.search(r"(?:^|\s)((?:\./|/)?(?:[\w.-]+/)*[\w.-]+\.\w{1,10})\b", line)
    return match.group(1) if match else None


def score_file(path: str, weights: dict[str, float] | None = None) -> QualityScore:
    """Score content quality of a file.

    Args:
        path: Path to the file to score.
        weights: Custom weights. See score_content.

    Returns:
        QualityScore for the file's content.

    Raises:
        FileNotFoundError: If path does not exist.
        OSError: If path cannot be read.
    """
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    return score_content(content, weights)
