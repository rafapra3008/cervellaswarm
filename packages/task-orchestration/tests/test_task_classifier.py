# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for cervellaswarm_task_orchestration.task_classifier."""

import pytest
from cervellaswarm_task_orchestration.task_classifier import (
    ClassificationResult,
    TaskComplexity,
    calculate_keyword_score,
    classify_task,
    estimate_files_affected,
    has_multifile_pattern,
    is_simple_task,
    should_use_architect,
    COMPLEXITY_KEYWORDS,
    SIMPLE_KEYWORDS,
    MULTIFILE_PATTERNS,
)


# =============================================================================
# TaskComplexity enum
# =============================================================================


def test_task_complexity_enum_values():
    assert TaskComplexity.SIMPLE.value == "simple"
    assert TaskComplexity.MEDIUM.value == "medium"
    assert TaskComplexity.COMPLEX.value == "complex"
    assert TaskComplexity.CRITICAL.value == "critical"


def test_task_complexity_enum_members():
    members = {e.value for e in TaskComplexity}
    assert members == {"simple", "medium", "complex", "critical"}


# =============================================================================
# ClassificationResult dataclass
# =============================================================================


def test_classification_result_fields():
    result = ClassificationResult(
        complexity=TaskComplexity.MEDIUM,
        should_architect=False,
        confidence=0.4,
        triggers=["refactor"],
        reasoning="test reasoning",
    )
    assert result.complexity == TaskComplexity.MEDIUM
    assert result.should_architect is False
    assert result.confidence == pytest.approx(0.4)
    assert result.triggers == ["refactor"]
    assert result.reasoning == "test reasoning"


def test_classification_result_confidence_range():
    """Confidence must be 0.0-1.0."""
    result = classify_task("fix typo in README")
    assert 0.0 <= result.confidence <= 1.0


# =============================================================================
# estimate_files_affected
# =============================================================================


@pytest.mark.parametrize("description,expected", [
    ("update 7 files in the repo", 7),
    ("change 1 file only", 1),
    ("fix across 12 files", 12),
])
def test_estimate_files_explicit_number(description, expected):
    assert estimate_files_affected(description) == expected


@pytest.mark.parametrize("description,expected", [
    ("refactor the entire codebase", 10),
    ("update all config files", 10),
    ("change every module", 10),
])
def test_estimate_files_entire_all_every(description, expected):
    assert estimate_files_affected(description) == expected


@pytest.mark.parametrize("description,expected", [
    ("update multiple components", 5),
    ("fix several endpoints", 5),
    ("touch various modules", 5),
])
def test_estimate_files_multiple_several_various(description, expected):
    assert estimate_files_affected(description) == expected


@pytest.mark.parametrize("description,expected", [
    ("fix both auth and db", 2),
    ("update two services", 2),
])
def test_estimate_files_both_two(description, expected):
    assert estimate_files_affected(description) == expected


def test_estimate_files_single_default():
    # "small" contains "all" as a substring which triggers the "all" keyword check.
    # Use a description with no triggering substrings.
    assert estimate_files_affected("fix one specific bug") == 1


def test_estimate_files_empty_string():
    assert estimate_files_affected("") == 1


def test_estimate_files_prefers_number_over_keyword():
    """Explicit number takes priority over 'multiple'."""
    result = estimate_files_affected("update 3 files across multiple modules")
    assert result == 3


# =============================================================================
# calculate_keyword_score
# =============================================================================


def test_calculate_keyword_score_empty():
    score, matched = calculate_keyword_score("")
    assert score == pytest.approx(0.0)
    assert matched == []


def test_calculate_keyword_score_no_match():
    score, matched = calculate_keyword_score("the quick brown fox")
    assert score == pytest.approx(0.0)
    assert matched == []


def test_calculate_keyword_score_architecture():
    score, matched = calculate_keyword_score("redesign the architecture")
    assert "architecture" in matched
    assert "redesign" in matched
    assert score > 0.0


def test_calculate_keyword_score_capped_at_1_5():
    """Score is capped at 1.5 regardless of how many keywords match."""
    many_kw = " ".join(COMPLEXITY_KEYWORDS.keys())
    score, matched = calculate_keyword_score(many_kw)
    assert score <= 1.5


def test_calculate_keyword_score_returns_matched_list():
    score, matched = calculate_keyword_score("refactor and migrate the codebase")
    assert "refactor" in matched
    assert "migrate" in matched


def test_calculate_keyword_score_single_keyword():
    score, matched = calculate_keyword_score("refactor the module")
    assert matched == ["refactor"]
    assert score == pytest.approx(COMPLEXITY_KEYWORDS["refactor"])


def test_calculate_keyword_score_case_insensitive():
    score_lower, _ = calculate_keyword_score("refactor")
    score_upper, _ = calculate_keyword_score("REFACTOR the module")
    assert score_lower == score_upper


# =============================================================================
# is_simple_task
# =============================================================================


@pytest.mark.parametrize("description", [
    "fix typo in config",
    "update comment in utils",
    "change text on button",
    "rename variable x",
    "minor adjustment to margin",
    "small fix in header",
    "quick update to labels",
    "simple bugfix",
    "adjust padding value",
    "tweak the timeout",
])
def test_is_simple_task_keywords(description):
    assert is_simple_task(description) is True


def test_is_simple_task_false_for_complex():
    assert is_simple_task("refactor entire auth module") is False


def test_is_simple_task_empty_string():
    assert is_simple_task("") is False


def test_is_simple_task_case_insensitive():
    assert is_simple_task("QUICK update to config") is True


# =============================================================================
# has_multifile_pattern
# =============================================================================


@pytest.mark.parametrize("description", [
    "update multiple files in src",
    "change across modules",
    "fix all test files",
    "update every service",
    "refactor entire module",
    "change 5 files in total",
])
def test_has_multifile_pattern_true(description):
    assert has_multifile_pattern(description) is True


@pytest.mark.parametrize("description", [
    "fix a single function",
    "update one record",
    "add a field",
])
def test_has_multifile_pattern_false(description):
    assert has_multifile_pattern(description) is False


def test_has_multifile_pattern_empty_string():
    assert has_multifile_pattern("") is False


def test_has_multifile_pattern_case_insensitive():
    assert has_multifile_pattern("MULTIPLE files need updating") is True


# =============================================================================
# classify_task - happy paths
# =============================================================================


def test_classify_task_simple_keyword():
    result = classify_task("fix typo in README")
    assert result.complexity == TaskComplexity.SIMPLE
    assert result.should_architect is False
    assert result.confidence == pytest.approx(0.9)
    assert "simple_keyword_detected" in result.triggers


def test_classify_task_critical_refactor():
    result = classify_task("refactor the entire architecture across modules")
    assert result.complexity in (TaskComplexity.COMPLEX, TaskComplexity.CRITICAL)
    assert result.should_architect is True


def test_classify_task_architecture_keyword():
    result = classify_task("redesign the architecture")
    assert result.should_architect is True


def test_classify_task_medium_implement():
    result = classify_task("implement a small feature")
    # implement + small -> simple keyword may override
    assert isinstance(result.complexity, TaskComplexity)


def test_classify_task_no_triggers_returns_no_triggers_label():
    result = classify_task("do the thing")
    assert result.triggers == ["no_triggers"]


def test_classify_task_result_has_reasoning():
    result = classify_task("refactor the module")
    assert len(result.reasoning) > 0


# =============================================================================
# classify_task - force_architect override
# =============================================================================


def test_classify_task_force_architect_true():
    result = classify_task("fix typo", force_architect=True)
    assert result.complexity == TaskComplexity.COMPLEX
    assert result.should_architect is True
    assert result.confidence == pytest.approx(1.0)
    assert "force_architect=True" in result.triggers
    assert result.reasoning == "Architect forced by caller"


def test_classify_task_force_architect_overrides_simple():
    """Even a simple task uses architect when forced."""
    result = classify_task("change text on button", force_architect=True)
    assert result.should_architect is True


# =============================================================================
# classify_task - has_breaking_changes boost
# =============================================================================


def test_classify_task_breaking_changes_adds_trigger():
    result = classify_task("update the API", has_breaking_changes=True)
    assert "breaking_changes" in result.triggers


def test_classify_task_breaking_changes_increases_score():
    without = classify_task("update the API")
    with_bc = classify_task("update the API", has_breaking_changes=True)
    # Breaking changes should push complexity up
    assert with_bc.confidence >= without.confidence


def test_classify_task_breaking_changes_on_simple():
    """Breaking change flag on an otherwise simple task."""
    result = classify_task("fix typo", has_breaking_changes=True)
    # force_architect check happens BEFORE simple check, but
    # breaking_changes is checked AFTER simple check -> simple wins first
    assert result.complexity == TaskComplexity.SIMPLE


# =============================================================================
# classify_task - estimated_files override
# =============================================================================


def test_classify_task_estimated_files_overrides_auto():
    result = classify_task("fix a bug", estimated_files=10)
    assert any("files" in t for t in result.triggers)


def test_classify_task_estimated_files_5_triggers_file_score():
    result = classify_task("do something", estimated_files=5)
    assert any("files>5" in t for t in result.triggers)


def test_classify_task_estimated_files_3_triggers_file_score():
    result = classify_task("do something", estimated_files=3)
    assert any("files>3" in t for t in result.triggers)


def test_classify_task_estimated_files_1_no_file_trigger():
    result = classify_task("do something", estimated_files=1)
    assert not any("files>" in t for t in result.triggers)


# =============================================================================
# classify_task - edge cases
# =============================================================================


def test_classify_task_empty_string():
    result = classify_task("")
    assert isinstance(result.complexity, TaskComplexity)
    assert isinstance(result.should_architect, bool)


def test_classify_task_very_long_string():
    long_desc = "implement " * 500
    result = classify_task(long_desc)
    assert 0.0 <= result.confidence <= 1.0


def test_classify_task_mixed_simple_and_complex_keywords():
    """Simple keyword detected first -> SIMPLE wins."""
    result = classify_task("simple refactor")
    assert result.complexity == TaskComplexity.SIMPLE
    assert result.should_architect is False


def test_classify_task_only_numbers():
    result = classify_task("123 456 789")
    assert isinstance(result, ClassificationResult)


def test_classify_task_special_characters():
    result = classify_task("fix: [bug] in (module) <urgent>")
    assert isinstance(result, ClassificationResult)


# =============================================================================
# should_use_architect
# =============================================================================


def test_should_use_architect_simple_task():
    assert should_use_architect("fix typo in README") is False


def test_should_use_architect_complex_task():
    assert should_use_architect("refactor the entire architecture") is True


def test_should_use_architect_returns_bool():
    result = should_use_architect("do something")
    assert isinstance(result, bool)


def test_should_use_architect_empty():
    result = should_use_architect("")
    assert isinstance(result, bool)


# =============================================================================
# Constants sanity checks
# =============================================================================


def test_complexity_keywords_have_valid_weights():
    for kw, weight in COMPLEXITY_KEYWORDS.items():
        assert 0.0 < weight <= 1.0, f"Bad weight for '{kw}': {weight}"


def test_simple_keywords_non_empty():
    assert len(SIMPLE_KEYWORDS) > 0


def test_multifile_patterns_are_valid_regex():
    import re
    for pattern in MULTIFILE_PATTERNS:
        compiled = re.compile(pattern)
        assert compiled is not None
