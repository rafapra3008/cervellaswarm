"""Shared fixtures for cervellaswarm-lingua-universale tests."""

import pytest

from cervellaswarm_lingua_universale.types import (
    AuditRequest,
    AuditVerdict,
    AuditVerdictType,
    PlanComplexity,
    PlanDecision,
    PlanProposal,
    PlanRequest,
    ResearchQuery,
    ResearchReport,
    TaskRequest,
    TaskResult,
    TaskStatus,
)


# ── TaskRequest fixtures ────────────────────────────────────────────────────

@pytest.fixture
def task_request():
    return TaskRequest(
        task_id="T001",
        description="Implement authentication module",
        target_files=("src/auth.py",),
        constraints=("No external deps",),
    )


@pytest.fixture
def task_result_ok():
    return TaskResult(
        task_id="T001",
        status=TaskStatus.OK,
        summary="Auth module implemented in 80 lines",
        files_created=("src/auth.py",),
        test_command="pytest tests/test_auth.py",
    )


@pytest.fixture
def task_result_blocked():
    return TaskResult(
        task_id="T001",
        status=TaskStatus.BLOCKED,
        summary="Cannot proceed without DB schema",
        blockers="Waiting for DB migration file from backend",
    )


# ── Audit fixtures ──────────────────────────────────────────────────────────

@pytest.fixture
def audit_request():
    return AuditRequest(
        audit_id="A001",
        target="src/auth.py",
        checklist=("Tests present", "No secrets", "Max 300 lines"),
        worker_output="Auth module with 5 tests.",
    )


@pytest.fixture
def audit_verdict_approved():
    return AuditVerdict(
        audit_id="A001",
        verdict=AuditVerdictType.APPROVED,
        score=9.5,
        checked=("Tests present", "No secrets"),
    )


# ── Plan fixtures ───────────────────────────────────────────────────────────

@pytest.fixture
def plan_request():
    return PlanRequest(
        plan_id="P001",
        task_description="Migrate database to PostgreSQL",
        complexity_hint=PlanComplexity.HIGH,
        constraints=("Zero downtime",),
    )


@pytest.fixture
def plan_proposal():
    return PlanProposal(
        plan_id="P001",
        complexity=PlanComplexity.HIGH,
        risk_score=0.6,
        files_affected=12,
        phases=("Phase 1: schema", "Phase 2: data", "Phase 3: cutover"),
        steps=("Create new schema", "Migrate data", "Update env"),
        success_criteria=("All tests pass", "Zero data loss"),
    )


@pytest.fixture
def plan_decision_approved():
    return PlanDecision(plan_id="P001", approved=True)


@pytest.fixture
def plan_decision_rejected():
    return PlanDecision(
        plan_id="P001",
        approved=False,
        feedback="Risk score too high, simplify phase 2",
    )


# ── Research fixtures ───────────────────────────────────────────────────────

@pytest.fixture
def research_query():
    return ResearchQuery(
        query_id="Q001",
        topic="PostgreSQL vs MySQL performance 2026",
        min_sources=5,
        scope=("benchmarks", "community"),
    )


@pytest.fixture
def research_report():
    return ResearchReport(
        query_id="Q001",
        topic="PostgreSQL vs MySQL performance 2026",
        sources_consulted=12,
        key_findings=("PostgreSQL wins on JSON", "MySQL faster on simple reads"),
        report_file=".sncp/reports/TESTER_20260219_db_perf.md",
    )
