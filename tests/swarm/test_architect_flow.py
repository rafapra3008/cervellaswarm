#!/usr/bin/env python3
"""
HARDTEST per W3-B Day 6 - architect_flow.py - Core

Test suite per routing e validation logic.
Verifica REQ-15 (routing), REQ-16 (validation).
Fallback e session tests in test_architect_flow_extended.py.

Author: Cervella Tester
Date: 2026-01-19
"""

import pytest
import sys
from pathlib import Path
from datetime import datetime
import tempfile
import json

# Aggiungo project root al path (NON scripts/, per evitare conflitto con tests/swarm/)
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.swarm.architect_flow import (
    route_task,
    validate_plan,
    validate_plan_file,
    _suggest_workers,
    RoutingDecision,
    PlanValidationResult,
    WorkerType,
    REQUIRED_PLAN_SECTIONS,
    REQUIRED_METADATA_FIELDS,
)

from scripts.swarm.task_classifier import TaskComplexity


# =============================================================================
# REQ-15: ROUTING - Decision Logic
# =============================================================================

def test_T01_route_complex_task_uses_architect():
    """T01: route_task con task complesso -> use_architect=True"""
    result = route_task("refactor authentication module across multiple files")

    assert isinstance(result, RoutingDecision)
    assert result.use_architect is True
    assert result.classification.should_architect is True
    assert result.classification.complexity.value in ["complex", "critical"]
    assert "refactor" in result.classification.triggers or "multifile_pattern" in result.classification.triggers


def test_T02_route_simple_task_no_architect():
    """T02: route_task con task semplice -> use_architect=False"""
    result = route_task("fix typo in README.md")

    assert isinstance(result, RoutingDecision)
    assert result.use_architect is False
    assert result.classification.should_architect is False
    assert result.classification.complexity.value == "simple"
    assert len(result.suggested_workers) > 0


def test_T03_route_force_architect():
    """T03: route_task con force_architect=True -> always True"""
    result = route_task("fix typo", force_architect=True)

    assert result.use_architect is True
    assert "forzato" in result.reason.lower() or "force_architect" in result.reason.lower()


def test_T04_route_force_direct():
    """T04: route_task con force_direct=True -> always False"""
    result = route_task("refactor entire codebase", force_direct=True)

    assert result.use_architect is False
    assert "bypass" in result.reason.lower() or "force_direct" in result.reason.lower()
    assert len(result.suggested_workers) > 0


def test_T05_suggest_workers_backend_keywords():
    """T05: _suggest_workers con keyword backend -> WorkerType.BACKEND"""
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
    """T06: _suggest_workers con keyword frontend -> WorkerType.FRONTEND"""
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
    """T07: RoutingDecision contiene tutti i campi richiesti"""
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
    """T08: validate_plan con plan valido -> is_valid=True"""
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
    """T09: validate_plan senza sezione obbligatoria -> error"""
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
    """T10: validate_plan senza campo metadata -> error"""
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
    """T11: validate_plan con plan < 500 chars -> warning"""
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
    """T12: validate_plan con plan > 10000 chars -> warning"""
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
    """T13: validate_plan_file con file non esistente -> error"""
    non_existent = Path("/tmp/nonexistent_plan_xyz123.md")

    result = validate_plan_file(non_existent)

    assert result.is_valid is False
    assert len(result.errors) > 0
    assert any("non trovato" in e.lower() or "not found" in e.lower() for e in result.errors)
    assert result.score == 0.0
