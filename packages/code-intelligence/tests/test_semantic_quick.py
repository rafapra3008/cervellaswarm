"""Quick smoke tests for semantic_search and impact_analyzer.

These tests verify imports and basic structure without full index build.

Author: Cervella Tester
Date: 2026-01-19
"""

from cervellaswarm_code_intelligence.semantic_search import SemanticSearch
from cervellaswarm_code_intelligence.impact_analyzer import ImpactAnalyzer, ImpactResult


def test_import_semantic_search():
    """Verify semantic_search module can be imported."""
    assert SemanticSearch is not None


def test_import_impact_analyzer():
    """Verify impact_analyzer module can be imported."""
    assert ImpactAnalyzer is not None
    assert ImpactResult is not None


def test_impact_result_structure():
    """Verify ImpactResult dataclass structure."""

    result = ImpactResult(
        symbol_name="test",
        risk_score=0.5,
        risk_level="medium",
        files_affected=3,
        callers_count=5,
        importance_score=0.1,
        reasons=["test reason"],
    )

    assert result.symbol_name == "test"
    assert result.risk_score == 0.5
    assert result.risk_level == "medium"
    assert result.files_affected == 3
    assert result.callers_count == 5
    assert result.importance_score == 0.1
    assert len(result.reasons) == 1


def test_invalid_repo_raises():
    """Verify invalid repo path raises ValueError."""
    import pytest

    with pytest.raises(ValueError):
        SemanticSearch("/invalid/path/xyz123")
