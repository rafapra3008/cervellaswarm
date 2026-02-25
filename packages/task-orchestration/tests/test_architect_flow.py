# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for cervellaswarm_task_orchestration.architect_flow."""

import json
import pytest
from pathlib import Path
from cervellaswarm_task_orchestration.architect_flow import (
    ArchitectSession,
    PlanStatus,
    PlanValidationResult,
    RoutingDecision,
    WorkerType,
    _suggest_workers,
    approve_plan,
    create_fallback_instruction,
    create_session,
    get_plan_path,
    handle_plan_rejection,
    route_task,
    save_session_state,
    should_fallback,
    validate_plan,
    validate_plan_file,
    MAX_REVISIONS,
    REQUIRED_PLAN_SECTIONS,
    REQUIRED_METADATA_FIELDS,
)
from cervellaswarm_task_orchestration.task_classifier import TaskComplexity


# =============================================================================
# Helpers & Fixtures
# =============================================================================


def _valid_plan() -> str:
    """Minimal valid plan (all required sections + metadata + > 500 chars)."""
    return (
        "## Metadata\n"
        "Task ID: T001\n"
        "Complexity: complex\n"
        "Files Affected: 5\n"
        "## Phase 1: Understanding\n"
        "Understand the context.\n"
        "## Phase 2: Design\n"
        "Use `module.py` and `config.json`.\n"
        "## Phase 3: Review\n"
        "Review changes.\n"
        "## Phase 4: Final Plan\n"
        "### Success Criteria\n"
        "- All tests pass\n"
        "### Execution Order\n"
        "1. module.py 2. config.yaml\n"
        + "x" * 500
    )


@pytest.fixture
def session():
    return create_session("T001", "Implement new auth module")


@pytest.fixture
def valid_plan_file(tmp_path):
    p = tmp_path / "PLAN_T001.md"
    p.write_text(_valid_plan())
    return p


# =============================================================================
# Enum values
# =============================================================================


def test_plan_status_values():
    expected = {
        "DRAFT": "draft", "WAITING_APPROVAL": "waiting_approval",
        "APPROVED": "approved", "REJECTED": "rejected",
        "REVISION_1": "revision_1", "REVISION_2": "revision_2",
        "FALLBACK": "fallback",
    }
    for name, value in expected.items():
        assert PlanStatus[name].value == value


def test_worker_type_values():
    expected = {
        "BACKEND": "backend", "FRONTEND": "frontend", "TESTER": "tester",
        "DEVOPS": "devops", "DOCS": "docs", "DATA": "data",
        "RESEARCHER": "researcher", "SECURITY": "security",
    }
    for name, value in expected.items():
        assert WorkerType[name].value == value


def test_worker_type_count():
    assert len(list(WorkerType)) == 8


# =============================================================================
# RoutingDecision - automatic routing
# =============================================================================


def test_routing_decision_fields_types():
    decision = route_task("fix typo in README")
    assert isinstance(decision, RoutingDecision)
    assert isinstance(decision.use_architect, bool)
    assert isinstance(decision.reason, str)
    assert isinstance(decision.suggested_workers, list)
    assert isinstance(decision.classification.complexity, TaskComplexity)


def test_route_task_simple_no_architect():
    decision = route_task("fix typo in README")
    assert decision.use_architect is False
    assert len(decision.suggested_workers) > 0


def test_route_task_complex_uses_architect():
    decision = route_task("refactor entire architecture across modules")
    assert decision.use_architect is True
    assert decision.suggested_workers == []


def test_route_task_empty_description_defaults_to_backend():
    decision = route_task("")
    assert WorkerType.BACKEND in decision.suggested_workers


# =============================================================================
# route_task - force_architect / force_direct
# =============================================================================


def test_route_task_force_architect():
    decision = route_task("fix typo", force_architect=True)
    assert decision.use_architect is True
    assert "force_architect=True" in decision.reason
    assert decision.suggested_workers == []


def test_route_task_force_architect_overrides_simple():
    assert route_task("change text on button", force_architect=True).use_architect is True


def test_route_task_force_direct():
    decision = route_task("redesign the architecture", force_direct=True)
    assert decision.use_architect is False
    assert "force_direct=True" in decision.reason
    assert len(decision.suggested_workers) > 0


# =============================================================================
# _suggest_workers
# =============================================================================


@pytest.mark.parametrize("description,expected_worker", [
    ("fix the api endpoint in python", WorkerType.BACKEND),
    ("update the react component button", WorkerType.FRONTEND),
    ("write pytest tests for coverage", WorkerType.TESTER),
    ("deploy with docker and kubernetes", WorkerType.DEVOPS),
    ("update the readme documentation", WorkerType.DOCS),
    ("etl data migration report", WorkerType.DATA),
    ("research and analyze competitors", WorkerType.RESEARCHER),
    ("security audit and encrypt passwords", WorkerType.SECURITY),
])
def test_suggest_workers_by_keyword(description, expected_worker):
    assert expected_worker in _suggest_workers(description)


def test_suggest_workers_empty_defaults_to_backend():
    assert _suggest_workers("") == [WorkerType.BACKEND]


def test_suggest_workers_multiple_keywords():
    workers = _suggest_workers("fix bug in api test coverage")
    assert WorkerType.BACKEND in workers
    assert WorkerType.TESTER in workers


# =============================================================================
# validate_plan - valid plan
# =============================================================================


def test_validate_plan_valid():
    result = validate_plan(_valid_plan())
    assert isinstance(result, PlanValidationResult)
    assert result.is_valid is True
    assert result.errors == []
    assert result.score >= 7.0


def test_validate_plan_score_clamped():
    assert 0.0 <= validate_plan("").score <= 10.0


def test_validate_plan_empty_is_invalid():
    result = validate_plan("")
    assert result.is_valid is False
    assert len(result.errors) > 0


# =============================================================================
# validate_plan - missing sections and metadata
# =============================================================================


@pytest.mark.parametrize("missing_section", REQUIRED_PLAN_SECTIONS)
def test_validate_plan_missing_required_section(missing_section):
    content = _valid_plan().replace(missing_section, "## Replaced")
    result = validate_plan(content)
    assert result.is_valid is False
    assert any(missing_section in e for e in result.errors)


@pytest.mark.parametrize("missing_field", REQUIRED_METADATA_FIELDS)
def test_validate_plan_missing_metadata_field(missing_field):
    content = _valid_plan().replace(missing_field, "REMOVED")
    result = validate_plan(content)
    assert result.is_valid is False
    assert any(missing_field in e for e in result.errors)


def test_validate_plan_missing_success_criteria():
    content = _valid_plan().replace("### Success Criteria", "### Done When")
    result = validate_plan(content)
    assert result.is_valid is False
    assert any("Success Criteria" in e for e in result.errors)


def test_validate_plan_short_content_adds_warning():
    short = (
        "## Metadata\nTask ID: T1\nComplexity: c\nFiles Affected: 1\n"
        "## Phase 1: Understanding\n## Phase 2: Design\n"
        "## Phase 3: Review\n## Phase 4: Final Plan\n"
        "### Success Criteria\n- done"
    )
    result = validate_plan(short)
    assert any("short" in w.lower() for w in result.warnings)


# =============================================================================
# validate_plan_file
# =============================================================================


def test_validate_plan_file_not_found(tmp_path):
    result = validate_plan_file(tmp_path / "nonexistent.md")
    assert result.is_valid is False
    assert any("not found" in e.lower() for e in result.errors)
    assert result.score == 0.0


def test_validate_plan_file_valid(valid_plan_file):
    assert validate_plan_file(valid_plan_file).is_valid is True


def test_validate_plan_file_invalid_content(tmp_path):
    bad = tmp_path / "bad.md"
    bad.write_text("# Nothing useful here")
    assert validate_plan_file(bad).is_valid is False


# =============================================================================
# handle_plan_rejection
# =============================================================================


def test_handle_plan_rejection_first(session):
    updated, action = handle_plan_rejection(session, "Plan too vague")
    assert action == "REQUEST_REVISION"
    assert updated.status == PlanStatus.REVISION_1
    assert updated.revision_count == 1
    assert "Plan too vague" in updated.rejection_reasons


def test_handle_plan_rejection_second(session):
    handle_plan_rejection(session, "R1")
    updated, action = handle_plan_rejection(session, "R2")
    assert action == "REQUEST_REVISION"
    assert updated.status == PlanStatus.REVISION_2
    assert updated.revision_count == 2


def test_handle_plan_rejection_third_triggers_fallback(session):
    handle_plan_rejection(session, "R1")
    handle_plan_rejection(session, "R2")
    updated, action = handle_plan_rejection(session, "R3")
    assert action == "FALLBACK_TO_WORKER"
    assert updated.status == PlanStatus.FALLBACK
    assert updated.revision_count == 3


def test_handle_plan_rejection_accumulates_reasons(session):
    handle_plan_rejection(session, "reason one")
    handle_plan_rejection(session, "reason two")
    assert "reason one" in session.rejection_reasons
    assert "reason two" in session.rejection_reasons


# =============================================================================
# should_fallback
# =============================================================================


def test_should_fallback_false_initially(session):
    assert should_fallback(session) is False


def test_should_fallback_boundary(session):
    session.revision_count = MAX_REVISIONS
    assert should_fallback(session) is False


def test_should_fallback_true_after_exceeding_max(session):
    session.revision_count = MAX_REVISIONS + 1
    assert should_fallback(session) is True


# =============================================================================
# create_fallback_instruction
# =============================================================================


def test_create_fallback_instruction_structure(session):
    session.rejection_reasons = ["reason alpha", "reason beta"]
    instruction = create_fallback_instruction(session)
    assert instruction.startswith("#")
    assert session.task_id in instruction
    assert session.task_description in instruction
    assert "reason alpha" in instruction
    assert "reason beta" in instruction
    assert "WARNING" in instruction or "Fallback" in instruction


# =============================================================================
# create_session
# =============================================================================


def test_create_session_defaults():
    s = create_session("T999", "Do something")
    assert isinstance(s, ArchitectSession)
    assert s.task_id == "T999"
    assert s.task_description == "Do something"
    assert s.status == PlanStatus.DRAFT
    assert s.revision_count == 0
    assert s.plan_path is None
    assert s.rejection_reasons == []


# =============================================================================
# approve_plan
# =============================================================================


def test_approve_plan(session):
    updated = approve_plan(session)
    assert updated.status == PlanStatus.APPROVED
    assert updated.approved_at is not None
    assert updated.approved_by == "coordinator"


def test_approve_plan_custom_approver(session):
    updated = approve_plan(session, approved_by="supervisor")
    assert updated.approved_by == "supervisor"


# =============================================================================
# get_plan_path
# =============================================================================


def test_get_plan_path_default_dir():
    assert get_plan_path("T001") == Path(".swarm/plans/PLAN_T001.md")


def test_get_plan_path_custom_dir(tmp_path):
    assert get_plan_path("T123", base_dir=tmp_path) == tmp_path / "PLAN_T123.md"


# =============================================================================
# save_session_state
# =============================================================================


def test_save_session_state_creates_valid_json(session, tmp_path):
    output = save_session_state(session, output_dir=tmp_path)
    assert output.exists()
    data = json.loads(output.read_text())
    assert data["task_id"] == session.task_id
    assert data["task_description"] == session.task_description
    assert data["status"] == PlanStatus.DRAFT.value
    assert data["plan_path"] is None
    assert data["approved_at"] is None
    assert "T001" in output.name


def test_save_session_state_with_plan_path(session, tmp_path):
    session.plan_path = Path("/tmp/plan.md")
    output = save_session_state(session, output_dir=tmp_path)
    data = json.loads(output.read_text())
    assert data["plan_path"] == "/tmp/plan.md"


def test_save_session_state_creates_directory(tmp_path):
    s = create_session("T777", "task")
    out_dir = tmp_path / "nested" / "sessions"
    save_session_state(s, output_dir=out_dir)
    assert out_dir.exists()


def test_save_session_state_after_approval(session, tmp_path):
    approve_plan(session)
    output = save_session_state(session, output_dir=tmp_path)
    data = json.loads(output.read_text())
    assert data["approved_at"] is not None
    assert data["approved_by"] == "coordinator"
