# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""
Task Classifier - Determine whether a task requires architect planning.

Rule-based, deterministic classification with zero LLM calls.
Analyzes task descriptions using keyword matching, multi-file pattern
detection, and file count estimation to produce a complexity score.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional
import re


class TaskComplexity(Enum):
    """Task complexity levels."""

    SIMPLE = "simple"  # No architect needed
    MEDIUM = "medium"  # Consider architect
    COMPLEX = "complex"  # Architect recommended
    CRITICAL = "critical"  # Architect required


@dataclass
class ClassificationResult:
    """Result of task classification."""

    complexity: TaskComplexity
    should_architect: bool
    confidence: float  # 0.0 - 1.0
    triggers: list[str]  # Which criteria matched
    reasoning: str


# Keywords suggesting complex tasks
COMPLEXITY_KEYWORDS: dict[str, float] = {
    # High complexity triggers
    "refactor": 0.8,
    "architecture": 0.9,
    "redesign": 0.8,
    "migrate": 0.7,
    "restructure": 0.8,
    "rewrite": 0.7,
    # Medium complexity triggers
    "complex": 0.6,
    "multiple files": 0.5,
    "across modules": 0.6,
    "cross-cutting": 0.6,
    "breaking change": 0.7,
    # Pattern triggers
    "integrate": 0.5,
    "implement feature": 0.5,
    "implement": 0.4,
    "add new": 0.4,
    "create system": 0.6,
    "dashboard": 0.4,
}

# Keywords suggesting simple tasks
SIMPLE_KEYWORDS: list[str] = [
    "fix typo",
    "update comment",
    "change text",
    "rename",
    "minor",
    "small",
    "quick",
    "simple",
    "adjust",
    "tweak",
]

# Patterns indicating multi-file changes
MULTIFILE_PATTERNS: list[str] = [
    r"multiple\s+files?",
    r"across\s+\w+",
    r"all\s+\w+\s+files?",
    r"every\s+\w+",
    r"entire\s+(module|system|codebase)",
    r"\d+\s+files?",
]


def estimate_files_affected(task_description: str) -> int:
    """
    Estimate how many files will be affected by a task.

    Args:
        task_description: Natural language task description.

    Returns:
        Estimated number of files (1-20+).
    """
    desc_lower = task_description.lower()

    # Look for explicit numbers
    number_match = re.search(r"(\d+)\s+files?", desc_lower)
    if number_match:
        return int(number_match.group(1))

    # Keywords suggesting many files
    if any(kw in desc_lower for kw in ["entire", "all", "every", "codebase"]):
        return 10

    if any(kw in desc_lower for kw in ["multiple", "several", "various"]):
        return 5

    if any(kw in desc_lower for kw in ["both", "two"]):
        return 2

    return 1


def calculate_keyword_score(task_description: str) -> tuple[float, list[str]]:
    """
    Calculate complexity score based on keyword matches.

    Args:
        task_description: Natural language task description.

    Returns:
        Tuple of (score 0.0-1.5, list of matched keywords).
    """
    desc_lower = task_description.lower()
    matched: list[str] = []
    total_score = 0.0

    for keyword, weight in COMPLEXITY_KEYWORDS.items():
        if keyword in desc_lower:
            matched.append(keyword)
            total_score += weight

    # Cap at 1.5 to prevent overflow (final_score divides by 1.5)
    capped = min(total_score, 1.5)
    return capped, matched


def is_simple_task(task_description: str) -> bool:
    """Check whether the task is clearly simple."""
    desc_lower = task_description.lower()
    return any(kw in desc_lower for kw in SIMPLE_KEYWORDS)


def has_multifile_pattern(task_description: str) -> bool:
    """Check whether multi-file patterns are present."""
    desc_lower = task_description.lower()
    return any(re.search(pattern, desc_lower) for pattern in MULTIFILE_PATTERNS)


def classify_task(
    task_description: str,
    estimated_files: Optional[int] = None,
    has_breaking_changes: bool = False,
    force_architect: bool = False,
) -> ClassificationResult:
    """
    Classify a task to determine whether it requires architect planning.

    Uses a deterministic, rule-based approach with zero LLM calls.
    Analyzes keywords, file counts, and multi-file patterns to produce
    a complexity score and routing decision.

    Args:
        task_description: Natural language task description.
        estimated_files: Known file count (auto-estimated if None).
        has_breaking_changes: Whether the task has known breaking changes.
        force_architect: Force architect activation.

    Returns:
        ClassificationResult with complexity, decision, and reasoning.
    """
    triggers: list[str] = []

    # Force override
    if force_architect:
        return ClassificationResult(
            complexity=TaskComplexity.COMPLEX,
            should_architect=True,
            confidence=1.0,
            triggers=["force_architect=True"],
            reasoning="Architect forced by caller",
        )

    # Check for simple task
    if is_simple_task(task_description):
        return ClassificationResult(
            complexity=TaskComplexity.SIMPLE,
            should_architect=False,
            confidence=0.9,
            triggers=["simple_keyword_detected"],
            reasoning="Task contains simple-task keyword",
        )

    # Calculate keyword score
    keyword_score, matched_keywords = calculate_keyword_score(task_description)
    if matched_keywords:
        triggers.extend(matched_keywords)

    # Estimate affected files
    files = estimated_files or estimate_files_affected(task_description)

    # Multi-file pattern check
    if has_multifile_pattern(task_description):
        triggers.append("multifile_pattern")
        files = max(files, 3)

    # Breaking changes
    if has_breaking_changes:
        triggers.append("breaking_changes")
        keyword_score += 0.3

    # File count scoring
    file_score = 0.0
    if files >= 5:
        file_score = 0.8
        triggers.append(f"files>5 ({files})")
    elif files >= 3:
        file_score = 0.5
        triggers.append(f"files>3 ({files})")

    # Final score
    final_score = min((keyword_score + file_score) / 1.5, 1.0)

    # Determine complexity and decision
    if final_score >= 0.7:
        complexity = TaskComplexity.CRITICAL
        should_architect = True
        reasoning = "Critical task - detailed planning required"
    elif final_score >= 0.5:
        complexity = TaskComplexity.COMPLEX
        should_architect = True
        reasoning = "Complex task - architect recommended"
    elif final_score >= 0.3:
        complexity = TaskComplexity.MEDIUM
        should_architect = False
        reasoning = "Medium task - architect optional"
    else:
        complexity = TaskComplexity.SIMPLE
        should_architect = False
        reasoning = "Simple task - proceed directly"

    return ClassificationResult(
        complexity=complexity,
        should_architect=should_architect,
        confidence=final_score,
        triggers=triggers if triggers else ["no_triggers"],
        reasoning=reasoning,
    )


def should_use_architect(task_description: str) -> bool:
    """
    Quick check whether architect planning is recommended.

    Args:
        task_description: Natural language task description.

    Returns:
        True if architect is recommended.
    """
    result = classify_task(task_description)
    return result.should_architect
