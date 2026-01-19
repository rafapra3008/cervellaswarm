#!/usr/bin/env python3
"""
HARDTEST per W3-B Day 6 - architect_flow.py

Test suite completa per routing, validation e fallback logic.
Verifica REQ-15 (routing), REQ-16 (validation), REQ-17 (fallback).

Author: Cervella Tester
Date: 2026-01-19
"""

import pytest
import sys
from pathlib import Path
from datetime import datetime
import tempfile

# Aggiungo scripts/ al path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

from swarm.architect_flow import (
    route_task,
    validate_plan,
    validate_plan_file,
    handle_plan_rejection,
    should_fallback,
    create_fallback_instruction,
    create_session,
    approve_plan,
    get_plan_path,
    _suggest_workers,
    RoutingDecision,
    PlanValidationResult,
    ArchitectSession,
    PlanStatus,
    WorkerType,
    REQUIRED_PLAN_SECTIONS,
    REQUIRED_METADATA_FIELDS,
    MAX_REVISIONS,
)

from swarm.task_classifier import TaskComplexity


# =============================================================================
# REQ-15: ROUTING - Decision Logic
# =============================================================================

def test_T01_route_complex_task_uses_architect():
    """
    T01: route_task con task complesso -> use_architect=True

    Task 'refactor authentication' e complesso per keywords + impact.
    Risultato atteso: use_architect=True, classification.should_architect=True
    """
    result = route_task("refactor authentication module across multiple files")

    assert isinstance(result, RoutingDecision)
    assert result.use_architect is True
    assert result.classification.should_architect is True
    assert result.classification.complexity.value in ["complex", "critical"]
    assert "refactor" in result.classification.triggers or "multifile_pattern" in result.classification.triggers


def test_T02_route_simple_task_no_architect():
    """
    T02: route_task con task semplice -> use_architect=False

    Task 'fix typo' e semplice per keyword detection.
    Risultato atteso: use_architect=False, suggested_workers non vuoto
    """
    result = route_task("fix typo in README.md")

    assert isinstance(result, RoutingDecision)
    assert result.use_architect is False
    assert result.classification.should_architect is False
    assert result.classification.complexity.value == "simple"
    assert len(result.suggested_workers) > 0  # Deve suggerire worker (docs)


def test_T03_route_force_architect():
    """
    T03: route_task con force_architect=True -> always True

    Anche task semplice deve usare architect se forzato.
    """
    result = route_task("fix typo", force_architect=True)

    assert result.use_architect is True
    assert "forzato" in result.reason.lower() or "force_architect" in result.reason.lower()


def test_T04_route_force_direct():
    """
    T04: route_task con force_direct=True -> always False

    Anche task complesso deve bypassare architect se forzato.
    """
    result = route_task("refactor entire codebase", force_direct=True)

    assert result.use_architect is False
    assert "bypass" in result.reason.lower() or "force_direct" in result.reason.lower()
    assert len(result.suggested_workers) > 0  # Deve suggerire worker anche in bypass


def test_T05_suggest_workers_backend_keywords():
    """
    T05: _suggest_workers con keyword backend -> WorkerType.BACKEND

    Keywords come 'api', 'database', 'python', 'fastapi' -> BACKEND worker.
    """
    test_cases = [
        "create new api endpoint",
        "fix database query bug",
        "implement python service",
        "update fastapi routes",
    ]

    for desc in test_cases:
        workers = _suggest_workers(desc)
        assert WorkerType.BACKEND in workers, f"BACKEND worker not suggested for '{desc}'"


def test_T06_suggest_workers_frontend_keywords():
    """
    T06: _suggest_workers con keyword frontend -> WorkerType.FRONTEND

    Keywords come 'ui', 'react', 'css', 'component' -> FRONTEND worker.
    """
    test_cases = [
        "create new ui component",
        "fix react button bug",
        "update css styles",
        "design landing page",
    ]

    for desc in test_cases:
        workers = _suggest_workers(desc)
        assert WorkerType.FRONTEND in workers, f"FRONTEND worker not suggested for '{desc}'"


def test_T07_routing_decision_has_all_fields():
    """
    T07: RoutingDecision contiene tutti i campi richiesti

    Verifica che la struttura dati sia completa.
    """
    result = route_task("test task")

    assert hasattr(result, 'use_architect')
    assert hasattr(result, 'classification')
    assert hasattr(result, 'reason')
    assert hasattr(result, 'suggested_workers')
    assert isinstance(result.use_architect, bool)
    assert isinstance(result.reason, str)
    assert isinstance(result.suggested_workers, list)


# =============================================================================
# REQ-16: VALIDATION - Plan Structure
# =============================================================================

def test_T08_validate_plan_valid():
    """
    T08: validate_plan con plan valido -> is_valid=True

    Plan con tutte le sezioni obbligatorie + metadata + success criteria.
    """
    valid_plan = """
# Task Plan

## Metadata
- **Task ID**: TASK_001
- **Complexity**: complex
- **Files Affected**: 3
- **Estimated Time**: 2h

## Phase 1: Understanding
Understanding the requirements...

## Phase 2: Design
Design approach...

## Phase 3: Review
Review considerations...

## Phase 4: Final Plan

### Success Criteria
- [ ] Feature works
- [ ] Tests pass

### Execution Order
1. Modify `file1.py`
2. Update `file2.ts`
3. Test `test_file.py`
"""

    result = validate_plan(valid_plan)

    assert isinstance(result, PlanValidationResult)
    assert result.is_valid is True
    assert len(result.errors) == 0
    assert result.score >= 7.0


def test_T09_validate_plan_missing_section():
    """
    T09: validate_plan senza sezione obbligatoria -> error

    Plan senza "## Phase 2: Design" deve generare errore.
    """
    incomplete_plan = """
## Metadata
- **Task ID**: TASK_001
- **Complexity**: complex
- **Files Affected**: 2

## Phase 1: Understanding
Understanding...

## Phase 3: Review
Review...

## Phase 4: Final Plan
### Success Criteria
- [ ] Done
"""

    result = validate_plan(incomplete_plan)

    assert result.is_valid is False
    assert any("Phase 2" in e for e in result.errors)


def test_T10_validate_plan_missing_metadata():
    """
    T10: validate_plan senza campo metadata -> error

    Metadata deve contenere Task ID, Complexity, Files Affected.
    """
    plan_no_taskid = """
## Metadata
- **Complexity**: complex
- **Files Affected**: 2

## Phase 1: Understanding
...
## Phase 2: Design
...
## Phase 3: Review
...
## Phase 4: Final Plan
### Success Criteria
- [ ] Done
"""

    result = validate_plan(plan_no_taskid)

    assert result.is_valid is False
    assert any("Task ID" in e for e in result.errors)


def test_T11_validate_plan_too_short():
    """
    T11: validate_plan con plan < 500 chars -> warning

    Plan troppo breve genera warning (non error).
    """
    short_plan = """
## Metadata
- **Task ID**: T1
- **Complexity**: simple
- **Files Affected**: 1

## Phase 1: Understanding
Short.

## Phase 2: Design
Short.

## Phase 3: Review
Short.

## Phase 4: Final Plan
### Success Criteria
- [ ] Done
"""

    result = validate_plan(short_plan)

    assert any("breve" in w.lower() or "short" in w.lower() for w in result.warnings)


def test_T12_validate_plan_too_long():
    """
    T12: validate_plan con plan > 10000 chars -> warning

    Plan troppo lungo genera warning.
    """
    long_content = "A" * 5000
    long_plan = f"""
## Metadata
- **Task ID**: TASK_001
- **Complexity**: complex
- **Files Affected**: 10

## Phase 1: Understanding
{long_content}

## Phase 2: Design
{long_content}

## Phase 3: Review
Review...

## Phase 4: Final Plan
### Success Criteria
- [ ] Done

Modify `file.py` here.
"""

    result = validate_plan(long_plan)

    assert any("lungo" in w.lower() or "long" in w.lower() for w in result.warnings)


def test_T13_validate_plan_file_not_found():
    """
    T13: validate_plan_file con file non esistente -> error

    Deve ritornare is_valid=False con errore specifico.
    """
    non_existent = Path("/tmp/nonexistent_plan_xyz123.md")

    result = validate_plan_file(non_existent)

    assert result.is_valid is False
    assert len(result.errors) > 0
    assert any("non trovato" in e.lower() or "not found" in e.lower() for e in result.errors)
    assert result.score == 0.0


# =============================================================================
# REQ-17: FALLBACK - Rejection Handling
# =============================================================================

def test_T14_handle_rejection_first():
    """
    T14: handle_plan_rejection prima volta -> REVISION_1

    Prima rejection deve portare a status REVISION_1.
    """
    session = create_session("TASK_001", "Test task")
    session, action = handle_plan_rejection(session, "Plan troppo generico")

    assert session.status == PlanStatus.REVISION_1
    assert action == "REQUEST_REVISION"
    assert session.revision_count == 1
    assert len(session.rejection_reasons) == 1


def test_T15_handle_rejection_second():
    """
    T15: handle_plan_rejection seconda volta -> REVISION_2

    Seconda rejection deve portare a status REVISION_2.
    """
    session = create_session("TASK_001", "Test task")
    session, _ = handle_plan_rejection(session, "Reason 1")
    session, action = handle_plan_rejection(session, "Reason 2")

    assert session.status == PlanStatus.REVISION_2
    assert action == "REQUEST_REVISION"
    assert session.revision_count == 2
    assert len(session.rejection_reasons) == 2


def test_T16_handle_rejection_third():
    """
    T16: handle_plan_rejection terza volta -> FALLBACK

    Terza rejection deve attivare fallback mode.
    """
    session = create_session("TASK_001", "Test task")
    session, _ = handle_plan_rejection(session, "Reason 1")
    session, _ = handle_plan_rejection(session, "Reason 2")
    session, action = handle_plan_rejection(session, "Reason 3")

    assert session.status == PlanStatus.FALLBACK
    assert action == "FALLBACK_TO_WORKER"
    assert session.revision_count == 3
    assert len(session.rejection_reasons) == 3


def test_T17_should_fallback_after_max_revisions():
    """
    T17: should_fallback True dopo MAX_REVISIONS (2)

    Dopo 3 rejection (> MAX_REVISIONS) deve ritornare True.
    """
    session = create_session("TASK_001", "Test task")

    # Prima e seconda rejection: no fallback
    session, _ = handle_plan_rejection(session, "Reason 1")
    assert should_fallback(session) is False

    session, _ = handle_plan_rejection(session, "Reason 2")
    assert should_fallback(session) is False

    # Terza rejection: fallback!
    session, _ = handle_plan_rejection(session, "Reason 3")
    assert should_fallback(session) is True


def test_T18_fallback_instruction_contains_task():
    """
    T18: create_fallback_instruction contiene task description

    Istruzioni fallback devono includere task originale e rejection reasons.
    """
    session = create_session("TASK_001", "Implement user authentication")
    session, _ = handle_plan_rejection(session, "Missing security considerations")
    session, _ = handle_plan_rejection(session, "No error handling")
    session, _ = handle_plan_rejection(session, "Incomplete tests")

    instruction = create_fallback_instruction(session)

    assert "TASK_001" in instruction
    assert "Implement user authentication" in instruction
    assert "Missing security considerations" in instruction
    assert "No error handling" in instruction
    assert "Incomplete tests" in instruction
    assert session.revision_count == 3


# =============================================================================
# SESSION MANAGEMENT
# =============================================================================

def test_T19_create_session_valid():
    """
    T19: create_session crea sessione valida

    Verifica che tutti i campi siano inizializzati correttamente.
    """
    session = create_session("TASK_001", "Test task description")

    assert isinstance(session, ArchitectSession)
    assert session.task_id == "TASK_001"
    assert session.task_description == "Test task description"
    assert session.status == PlanStatus.DRAFT
    assert session.revision_count == 0
    assert len(session.rejection_reasons) == 0
    assert session.plan_path is None
    assert session.approved_by is None
    assert isinstance(session.created_at, datetime)


def test_T20_approve_plan_sets_status():
    """
    T20: approve_plan setta status APPROVED

    Dopo approvazione, status deve essere APPROVED e approved_at non None.
    """
    session = create_session("TASK_001", "Test task")
    session = approve_plan(session, approved_by="Regina")

    assert session.status == PlanStatus.APPROVED
    assert session.approved_at is not None
    assert isinstance(session.approved_at, datetime)
    assert session.approved_by == "Regina"


def test_T21_get_plan_path_format():
    """
    T21: get_plan_path ritorna formato corretto

    Path deve essere .swarm/plans/PLAN_{task_id}.md
    """
    task_id = "TASK_123"
    plan_path = get_plan_path(task_id)

    assert isinstance(plan_path, Path)
    assert str(plan_path) == ".swarm/plans/PLAN_TASK_123.md"
    assert plan_path.suffix == ".md"


# =============================================================================
# EDGE CASES & INTEGRATION
# =============================================================================

def test_route_with_multiple_worker_suggestions():
    """
    Test che un task possa suggerire piu worker contemporaneamente.

    Ad esempio "test the new API endpoint" dovrebbe suggerire
    sia BACKEND (api) che TESTER (test).
    """
    result = route_task("test the new API endpoint", force_direct=True)

    workers = result.suggested_workers
    assert WorkerType.BACKEND in workers
    assert WorkerType.TESTER in workers


def test_validation_with_success_criteria_variations():
    """
    Test che success criteria siano riconosciuti anche con case variations.
    """
    plan_lowercase = """
## Metadata
- **Task ID**: T1
- **Complexity**: simple
- **Files Affected**: 1

## Phase 1: Understanding
Text
## Phase 2: Design
Text
## Phase 3: Review
Text
## Phase 4: Final Plan

### success criteria
- [ ] Done
"""

    result = validate_plan(plan_lowercase)
    # Non deve generare errore per success criteria (case insensitive)
    assert not any("Success Criteria" in e for e in result.errors)


def test_session_workflow_complete():
    """
    Test workflow completo: create -> reject -> reject -> fallback.
    """
    # Create
    session = create_session("TASK_999", "Complex refactor")
    assert session.status == PlanStatus.DRAFT

    # First rejection
    session, action = handle_plan_rejection(session, "Needs more detail")
    assert action == "REQUEST_REVISION"
    assert not should_fallback(session)

    # Second rejection
    session, action = handle_plan_rejection(session, "Still incomplete")
    assert action == "REQUEST_REVISION"
    assert not should_fallback(session)

    # Third rejection -> fallback
    session, action = handle_plan_rejection(session, "Missing tests")
    assert action == "FALLBACK_TO_WORKER"
    assert should_fallback(session)
    assert session.status == PlanStatus.FALLBACK

    # Generate fallback instruction
    instruction = create_fallback_instruction(session)
    assert "TASK_999" in instruction
    assert "Complex refactor" in instruction


def test_validate_plan_score_calculation():
    """
    Verifica che lo score sia calcolato correttamente.

    Plan perfetto deve avere score ~10.0
    Plan con errori deve avere score < 7.0
    """
    perfect_plan = """
## Metadata
- **Task ID**: TASK_001
- **Complexity**: complex
- **Files Affected**: 3

## Phase 1: Understanding
Detailed understanding section with context.

## Phase 2: Design
Design approach with architecture decisions.

## Phase 3: Review
Review considerations and risks.

## Phase 4: Final Plan

### Success Criteria
- [ ] Feature implemented in `app.py`
- [ ] Tests pass in `test_app.py`
- [ ] Documentation updated in `README.md`

### Execution Order
1. Modify `app.py`
2. Write tests in `test_app.py`
3. Update docs
"""

    result = validate_plan(perfect_plan)
    assert result.score >= 8.0  # Deve essere alto

    # Plan con molti problemi
    bad_plan = "## Metadata\nTask ID: T1\n\nSome text."
    result_bad = validate_plan(bad_plan)
    assert result_bad.score < 7.0


def test_suggest_workers_default_backend():
    """
    Test che se nessuna keyword matcha, suggerisca BACKEND come default.
    """
    workers = _suggest_workers("do something generic")
    assert WorkerType.BACKEND in workers
    assert len(workers) >= 1  # Almeno backend come fallback


# =============================================================================
# RUN
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
