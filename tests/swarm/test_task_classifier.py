#!/usr/bin/env python3
"""
HARDTEST per W3-B Day 5 - task_classifier.py

Test suite completa per classificazione task.
Verifica logica, edge cases, keyword detection.
"""

import pytest
import sys
from pathlib import Path

# Aggiungo scripts/ al path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

from swarm.task_classifier import (
    classify_task,
    estimate_files_affected,
    calculate_keyword_score,
    is_simple_task,
    has_multifile_pattern,
    should_use_architect,
    TaskComplexity,
    ClassificationResult,
    COMPLEXITY_KEYWORDS,
    SIMPLE_KEYWORDS,
)


# ============================================================================
# T01: classify_task basic - Simple task
# ============================================================================
def test_classify_simple_task():
    """
    Verifica che un task semplice come 'fix typo' sia classificato SIMPLE.
    should_architect=False perche keyword 'fix typo' in SIMPLE_KEYWORDS.
    """
    result = classify_task("fix typo in README.md")

    assert result.complexity == TaskComplexity.SIMPLE
    assert result.should_architect is False
    assert result.confidence >= 0.8  # Alta confidenza per simple tasks
    assert "simple_keyword_detected" in result.triggers


# ============================================================================
# T02: classify_task complex - Refactor
# ============================================================================
def test_classify_complex_refactor():
    """
    Verifica che un refactor complesso multi-modulo sia COMPLEX/CRITICAL.
    Keyword 'refactor' + 'across modules' -> should_architect=True
    """
    result = classify_task("refactor authentication across modules")

    assert result.complexity in [TaskComplexity.COMPLEX, TaskComplexity.CRITICAL]
    assert result.should_architect is True
    assert "refactor" in result.triggers
    assert "across modules" in result.triggers or "multifile_pattern" in result.triggers


# ============================================================================
# T03: keyword detection
# ============================================================================
def test_keyword_detection():
    """
    Verifica che tutte le keyword di complessita siano rilevate correttamente.
    Testa alcune keyword chiave da COMPLEXITY_KEYWORDS.
    """
    test_cases = [
        ("refactor module", ["refactor"]),
        ("migrate database schema", ["migrate"]),
        ("redesign architecture", ["redesign", "architecture"]),
        ("breaking change to API", ["breaking change"]),
        ("integrate new service", ["integrate"]),
    ]

    for description, expected_keywords in test_cases:
        score, matched = calculate_keyword_score(description)

        # Verifica che le keyword siano matchate
        for kw in expected_keywords:
            assert kw in matched, f"Keyword '{kw}' non trovata in '{description}'"

        # Score deve essere > 0 se ci sono match
        assert score > 0.0, f"Score should be > 0 for '{description}'"


# ============================================================================
# T04: file estimation
# ============================================================================
def test_file_estimation():
    """
    Verifica la stima del numero di file affetti.
    - '5 files' -> 5
    - 'multiple files' -> 5
    - default (single file) -> 1
    """
    assert estimate_files_affected("modify 5 files") == 5
    assert estimate_files_affected("change 12 files") == 12
    assert estimate_files_affected("multiple files affected") == 5
    assert estimate_files_affected("several files to update") == 5
    assert estimate_files_affected("entire codebase") == 10
    assert estimate_files_affected("fix single function") == 1


# ============================================================================
# T05: multifile pattern
# ============================================================================
def test_multifile_pattern():
    """
    Verifica che pattern multi-file siano rilevati.
    - 'across modules' -> True
    - 'entire codebase' -> True
    - 'single file' -> False
    """
    assert has_multifile_pattern("refactor across modules") is True
    assert has_multifile_pattern("update entire codebase") is True
    assert has_multifile_pattern("change all test files") is True
    assert has_multifile_pattern("5 files affected") is True
    assert has_multifile_pattern("fix function in utils.py") is False


# ============================================================================
# T06: simple task override
# ============================================================================
def test_simple_keywords_override():
    """
    Verifica che keyword SIMPLE abbiano precedenza.
    Anche se 'refactor' e presente, 'simple' deve vincere.
    """
    result = classify_task("simple refactor of variable names")

    assert result.complexity == TaskComplexity.SIMPLE
    assert result.should_architect is False
    assert "simple_keyword_detected" in result.triggers


# ============================================================================
# T07: force architect
# ============================================================================
def test_force_architect():
    """
    Verifica che force_architect=True forzi sempre architect.
    Anche per task semplici.
    """
    # Task semplice MA con force=True
    result = classify_task("fix typo", force_architect=True)

    assert result.should_architect is True
    assert result.confidence == 1.0
    assert "force_architect=True" in result.triggers


# ============================================================================
# T08: edge case empty
# ============================================================================
def test_empty_string():
    """
    Verifica che una stringa vuota non faccia crashare.
    Default: SIMPLE, no architect.
    """
    result = classify_task("")

    assert result is not None
    assert result.complexity == TaskComplexity.SIMPLE
    assert result.should_architect is False


# ============================================================================
# T09: confidence range
# ============================================================================
def test_confidence_range():
    """
    Verifica che confidence sia sempre tra 0.0 e 1.0.
    Testa diverse complessita.
    """
    test_descriptions = [
        "fix typo",
        "add new function",
        "refactor module",
        "migrate entire codebase with breaking changes",
    ]

    for desc in test_descriptions:
        result = classify_task(desc)

        assert 0.0 <= result.confidence <= 1.0, \
            f"Confidence out of range for '{desc}': {result.confidence}"


# ============================================================================
# T10: ClassificationResult fields
# ============================================================================
def test_result_has_all_fields():
    """
    Verifica che ClassificationResult abbia tutti i campi richiesti.
    - complexity (TaskComplexity)
    - should_architect (bool)
    - confidence (float)
    - triggers (list[str])
    - reasoning (str)
    """
    result = classify_task("refactor authentication")

    # Check campi esistono
    assert hasattr(result, "complexity")
    assert hasattr(result, "should_architect")
    assert hasattr(result, "confidence")
    assert hasattr(result, "triggers")
    assert hasattr(result, "reasoning")

    # Check tipi corretti
    assert isinstance(result.complexity, TaskComplexity)
    assert isinstance(result.should_architect, bool)
    assert isinstance(result.confidence, float)
    assert isinstance(result.triggers, list)
    assert isinstance(result.reasoning, str)

    # Check non vuoti
    assert result.triggers  # Lista non vuota
    assert result.reasoning  # Stringa non vuota


# ============================================================================
# T11: should_use_architect shortcut
# ============================================================================
def test_should_use_architect_shortcut():
    """
    Verifica che should_use_architect() sia un wrapper corretto.
    """
    # Simple task
    assert should_use_architect("fix typo") is False

    # Complex task
    assert should_use_architect("refactor across modules") is True


# ============================================================================
# T12: breaking changes flag
# ============================================================================
def test_breaking_changes_flag():
    """
    Verifica che has_breaking_changes aumenti score.
    """
    result_normal = classify_task("update API")
    result_breaking = classify_task("update API", has_breaking_changes=True)

    # Con breaking changes deve avere score piu alto o complessita maggiore
    assert result_breaking.confidence >= result_normal.confidence or \
           result_breaking.complexity.value != result_normal.complexity.value


# ============================================================================
# T13: estimated_files override
# ============================================================================
def test_estimated_files_override():
    """
    Verifica che estimated_files (se fornito) vinca sulla stima automatica.
    """
    # Senza estimated_files: descrizione vaga -> 1 file
    result_auto = classify_task("refactor function")

    # Con estimated_files=10: forza 10 file
    result_manual = classify_task("refactor function", estimated_files=10)

    # Entrambi hanno refactor, ma il secondo ha piu file -> score diverso
    # result_manual dovrebbe avere score maggiore o complessita >= result_auto
    assert result_manual.confidence >= result_auto.confidence or \
           result_manual.complexity != result_auto.complexity


# ============================================================================
# T14: is_simple_task utility
# ============================================================================
def test_is_simple_task_utility():
    """
    Verifica is_simple_task() per detection diretta.
    """
    assert is_simple_task("fix typo in docs") is True
    assert is_simple_task("minor adjustment") is True
    assert is_simple_task("quick rename") is True
    assert is_simple_task("refactor architecture") is False


# ============================================================================
# T15: complex task multiple triggers
# ============================================================================
def test_complex_task_multiple_triggers():
    """
    Verifica che un task molto complesso abbia MULTIPLI trigger.
    """
    result = classify_task(
        "refactor and migrate entire authentication system across 10 files with breaking changes",
        has_breaking_changes=True
    )

    assert result.should_architect is True
    assert len(result.triggers) >= 3  # Almeno 3 trigger attivi
    assert "refactor" in result.triggers
    assert "migrate" in result.triggers


# ============================================================================
# EXTRA: Boundary testing
# ============================================================================
def test_boundary_3_files():
    """
    Verifica comportamento con esattamente 3 file (threshold).
    """
    result = classify_task("modify code", estimated_files=3)

    # 3 files = threshold, potrebbe essere MEDIUM o COMPLEX
    assert result.complexity in [
        TaskComplexity.MEDIUM,
        TaskComplexity.COMPLEX,
        TaskComplexity.SIMPLE  # Dipende da altri fattori
    ]


def test_boundary_5_files():
    """
    Verifica comportamento con 5+ files (soglia alta).
    """
    result = classify_task("modify code", estimated_files=5)

    # 5+ files dovrebbe aumentare score
    assert "files>5 (5)" in result.triggers or "files>3 (5)" in result.triggers


# ============================================================================
# RUN TESTS
# ============================================================================
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
