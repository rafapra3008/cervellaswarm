"""
HARDTEST per architect_flow.py - Extended Tests

Fallback handling, session management, edge cases, coverage gaps.
Split da test_architect_flow.py per rispettare limite 500 righe.
"""

import pytest
import sys
import json
import tempfile
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.swarm.architect_flow import (
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
    _extract_section,
    save_session_state,
    RoutingDecision,
    PlanValidationResult,
    ArchitectSession,
    PlanStatus,
    WorkerType,
    MAX_REVISIONS,
)

from scripts.swarm.task_classifier import TaskComplexity


# =============================================================================
# REQ-17: FALLBACK - Rejection Handling
# =============================================================================

def test_T14_handle_rejection_first():
    """T14: handle_plan_rejection prima volta -> REVISION_1"""
    session = create_session("TASK_001", "Test task")
    session, action = handle_plan_rejection(session, "Plan troppo generico")

    assert session.status == PlanStatus.REVISION_1
    assert action == "REQUEST_REVISION"
    assert session.revision_count == 1
    assert len(session.rejection_reasons) == 1


def test_T15_handle_rejection_second():
    """T15: handle_plan_rejection seconda volta -> REVISION_2"""
    session = create_session("TASK_001", "Test task")
    session, _ = handle_plan_rejection(session, "Reason 1")
    session, action = handle_plan_rejection(session, "Reason 2")

    assert session.status == PlanStatus.REVISION_2
    assert action == "REQUEST_REVISION"
    assert session.revision_count == 2
    assert len(session.rejection_reasons) == 2


def test_T16_handle_rejection_third():
    """T16: handle_plan_rejection terza volta -> FALLBACK"""
    session = create_session("TASK_001", "Test task")
    session, _ = handle_plan_rejection(session, "Reason 1")
    session, _ = handle_plan_rejection(session, "Reason 2")
    session, action = handle_plan_rejection(session, "Reason 3")

    assert session.status == PlanStatus.FALLBACK
    assert action == "FALLBACK_TO_WORKER"
    assert session.revision_count == 3
    assert len(session.rejection_reasons) == 3


def test_T17_should_fallback_after_max_revisions():
    """T17: should_fallback True dopo MAX_REVISIONS (2)"""
    session = create_session("TASK_001", "Test task")

    session, _ = handle_plan_rejection(session, "Reason 1")
    assert should_fallback(session) is False

    session, _ = handle_plan_rejection(session, "Reason 2")
    assert should_fallback(session) is False

    session, _ = handle_plan_rejection(session, "Reason 3")
    assert should_fallback(session) is True


def test_T18_fallback_instruction_contains_task():
    """T18: create_fallback_instruction contiene task description"""
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
    """T19: create_session crea sessione valida"""
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
    """T20: approve_plan setta status APPROVED"""
    session = create_session("TASK_001", "Test task")
    session = approve_plan(session, approved_by="Regina")

    assert session.status == PlanStatus.APPROVED
    assert session.approved_at is not None
    assert isinstance(session.approved_at, datetime)
    assert session.approved_by == "Regina"


def test_T21_get_plan_path_format():
    """T21: get_plan_path ritorna formato corretto"""
    task_id = "TASK_123"
    plan_path = get_plan_path(task_id)

    assert isinstance(plan_path, Path)
    assert str(plan_path) == ".swarm/plans/PLAN_TASK_123.md"
    assert plan_path.suffix == ".md"


# =============================================================================
# EDGE CASES & INTEGRATION
# =============================================================================

def test_route_with_multiple_worker_suggestions():
    """Test che un task possa suggerire piu worker contemporaneamente."""
    result = route_task("test the new API endpoint", force_direct=True)

    workers = result.suggested_workers
    assert WorkerType.BACKEND in workers
    assert WorkerType.TESTER in workers


def test_validation_with_success_criteria_variations():
    """Test che success criteria siano riconosciuti anche con case variations."""
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
    assert not any("Success Criteria" in e for e in result.errors)


def test_session_workflow_complete():
    """Test workflow completo: create -> reject -> reject -> fallback."""
    session = create_session("TASK_999", "Complex refactor")
    assert session.status == PlanStatus.DRAFT

    session, action = handle_plan_rejection(session, "Needs more detail")
    assert action == "REQUEST_REVISION"
    assert not should_fallback(session)

    session, action = handle_plan_rejection(session, "Still incomplete")
    assert action == "REQUEST_REVISION"
    assert not should_fallback(session)

    session, action = handle_plan_rejection(session, "Missing tests")
    assert action == "FALLBACK_TO_WORKER"
    assert should_fallback(session)
    assert session.status == PlanStatus.FALLBACK

    instruction = create_fallback_instruction(session)
    assert "TASK_999" in instruction
    assert "Complex refactor" in instruction


def test_validate_plan_score_calculation():
    """Verifica che lo score sia calcolato correttamente."""
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
    assert result.score >= 8.0

    bad_plan = "## Metadata\nTask ID: T1\n\nSome text."
    result_bad = validate_plan(bad_plan)
    assert result_bad.score < 7.0


# =============================================================================
# COVERAGE GAPS
# =============================================================================

def test_suggest_workers_default_backend():
    """Test che se nessuna keyword matcha, suggerisca BACKEND come default."""
    workers = _suggest_workers("do something generic")
    assert WorkerType.BACKEND in workers
    assert len(workers) >= 1


def test_suggest_workers_devops_keywords():
    """Line 172: _suggest_workers con 'deploy', 'docker', 'ci' -> DEVOPS"""
    workers = _suggest_workers("deploy the app to production")
    assert WorkerType.DEVOPS in workers

    workers = _suggest_workers("setup docker containers")
    assert WorkerType.DEVOPS in workers


def test_suggest_workers_security_keywords():
    """Line 184: _suggest_workers con 'security', 'auth', 'vulnerability' -> SECURITY"""
    workers = _suggest_workers("fix security vulnerability in auth")
    assert WorkerType.SECURITY in workers

    workers = _suggest_workers("implement authentication layer")
    assert WorkerType.SECURITY in workers


def test_validate_plan_missing_metadata_section():
    """Lines 245-246: validate_plan quando Metadata section non trovata"""
    plan_no_metadata = """
## Phase 1: Understanding
Text
## Phase 2: Design
Text
## Phase 3: Review
Text
## Phase 4: Final Plan
### Success Criteria
- [ ] Done
"""
    result = validate_plan(plan_no_metadata)

    assert result.is_valid is False
    assert any("Metadata" in e for e in result.errors)
    assert result.score <= 8.0


def test_validate_plan_file_reads_content():
    """Lines 301-302: validate_plan_file legge file e chiama validate_plan"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write("""
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
### Success Criteria
- [ ] Done in `file.py`
""")
        temp_path = Path(f.name)

    try:
        result = validate_plan_file(temp_path)
        assert result.is_valid is True
        assert result.score > 0.0
    finally:
        temp_path.unlink()


def test_extract_section_start_not_found():
    """Line 309: _extract_section quando start_marker non trovato -> None"""
    content = "## Section A\nText\n## Section B\nMore text"

    result = _extract_section(content, "## Nonexistent", "## Section B")
    assert result is None


def test_save_session_state():
    """Lines 443-459: save_session_state serializza session a JSON"""
    session = create_session("TASK_TEST", "Test description")
    session.status = PlanStatus.APPROVED
    session.plan_path = Path("/test/plan.md")
    session.approved_by = "Regina"

    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir)
        saved_path = save_session_state(session, output_dir)

        assert saved_path.exists()
        assert saved_path.name == "session_TASK_TEST.json"

        data = json.loads(saved_path.read_text())
        assert data["task_id"] == "TASK_TEST"
        assert data["status"] == "approved"
        assert data["approved_by"] == "Regina"
