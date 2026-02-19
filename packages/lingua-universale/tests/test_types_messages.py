"""Tests for message dataclasses in cervellaswarm_lingua_universale.types.

Covers: TaskRequest, TaskResult, AuditRequest, AuditVerdict,
PlanRequest, PlanProposal, PlanDecision, ResearchQuery, ResearchReport.
Includes valid creation, validation errors, immutability, and KIND field.
"""

import pytest

from cervellaswarm_lingua_universale.types import (
    AuditRequest,
    AuditVerdict,
    AuditVerdictType,
    MessageKind,
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


# ── TaskRequest ──────────────────────────────────────────────────────────────

class TestTaskRequest:
    def test_valid_creation(self, task_request):
        assert task_request.task_id == "T001"
        assert task_request.description == "Implement authentication module"
        assert task_request.target_files == ("src/auth.py",)
        assert task_request.constraints == ("No external deps",)
        assert task_request.max_file_lines == 500  # default

    def test_empty_task_id_raises(self):
        with pytest.raises(ValueError, match="task_id cannot be empty"):
            TaskRequest(task_id="", description="Something")

    def test_empty_description_raises(self):
        with pytest.raises(ValueError, match="description cannot be empty"):
            TaskRequest(task_id="T001", description="")

    def test_invalid_max_file_lines_raises(self):
        with pytest.raises(ValueError, match="max_file_lines must be positive"):
            TaskRequest(task_id="T001", description="Do it", max_file_lines=0)

    def test_frozen_immutable(self, task_request):
        with pytest.raises(Exception):
            task_request.task_id = "changed"  # type: ignore[misc]

    def test_kind_is_task_request(self, task_request):
        assert task_request.KIND == MessageKind.TASK_REQUEST


# ── TaskResult ───────────────────────────────────────────────────────────────

class TestTaskResult:
    def test_valid_ok_result(self, task_result_ok):
        assert task_result_ok.status == TaskStatus.OK
        assert task_result_ok.task_id == "T001"
        assert len(task_result_ok.summary) <= 200

    def test_valid_blocked_result(self, task_result_blocked):
        assert task_result_blocked.status == TaskStatus.BLOCKED
        assert task_result_blocked.blockers is not None

    def test_empty_task_id_raises(self):
        with pytest.raises(ValueError, match="task_id cannot be empty"):
            TaskResult(task_id="", status=TaskStatus.OK, summary="done")

    def test_empty_summary_raises(self):
        with pytest.raises(ValueError, match="summary cannot be empty"):
            TaskResult(task_id="T001", status=TaskStatus.OK, summary="")

    def test_summary_too_long_raises(self):
        long_summary = "x" * 201
        with pytest.raises(ValueError, match="summary must be <= 200 characters"):
            TaskResult(task_id="T001", status=TaskStatus.OK, summary=long_summary)

    def test_summary_exactly_200_chars_ok(self):
        summary = "x" * 200
        result = TaskResult(task_id="T001", status=TaskStatus.OK, summary=summary)
        assert len(result.summary) == 200

    def test_blocked_without_blockers_raises(self):
        with pytest.raises(ValueError, match="blockers required"):
            TaskResult(
                task_id="T001",
                status=TaskStatus.BLOCKED,
                summary="Stuck on something",
                blockers=None,
            )

    def test_frozen_immutable(self, task_result_ok):
        with pytest.raises(Exception):
            task_result_ok.status = TaskStatus.FAIL  # type: ignore[misc]

    def test_kind_is_task_result(self, task_result_ok):
        assert task_result_ok.KIND == MessageKind.TASK_RESULT


# ── AuditRequest / AuditVerdict ──────────────────────────────────────────────

class TestAuditRequest:
    def test_valid_creation(self, audit_request):
        assert audit_request.audit_id == "A001"
        assert audit_request.target == "src/auth.py"
        assert len(audit_request.checklist) == 3

    def test_empty_audit_id_raises(self):
        with pytest.raises(ValueError, match="audit_id cannot be empty"):
            AuditRequest(audit_id="", target="file.py")

    def test_empty_target_raises(self):
        with pytest.raises(ValueError, match="target cannot be empty"):
            AuditRequest(audit_id="A001", target="")

    def test_kind_is_audit_request(self, audit_request):
        assert audit_request.KIND == MessageKind.AUDIT_REQUEST


class TestAuditVerdict:
    def test_valid_creation(self, audit_verdict_approved):
        assert audit_verdict_approved.score == 9.5
        assert audit_verdict_approved.verdict == AuditVerdictType.APPROVED

    def test_score_out_of_range_raises(self):
        with pytest.raises(ValueError, match="score must be 0.0-10.0"):
            AuditVerdict(
                audit_id="A001",
                verdict=AuditVerdictType.APPROVED,
                score=10.1,
                checked=("check1",),
            )

    def test_score_negative_raises(self):
        with pytest.raises(ValueError, match="score must be 0.0-10.0"):
            AuditVerdict(
                audit_id="A001",
                verdict=AuditVerdictType.APPROVED,
                score=-0.1,
                checked=("check1",),
            )

    def test_empty_checked_raises(self):
        with pytest.raises(ValueError, match="checked items cannot be empty"):
            AuditVerdict(
                audit_id="A001",
                verdict=AuditVerdictType.APPROVED,
                score=8.0,
                checked=(),
            )

    def test_kind_is_audit_verdict(self, audit_verdict_approved):
        assert audit_verdict_approved.KIND == MessageKind.AUDIT_VERDICT


# ── PlanRequest / PlanProposal / PlanDecision ────────────────────────────────

class TestPlanRequest:
    def test_valid_creation(self, plan_request):
        assert plan_request.plan_id == "P001"
        assert plan_request.complexity_hint == PlanComplexity.HIGH

    def test_empty_plan_id_raises(self):
        with pytest.raises(ValueError, match="plan_id cannot be empty"):
            PlanRequest(plan_id="", task_description="Migrate DB")

    def test_empty_task_description_raises(self):
        with pytest.raises(ValueError, match="task_description cannot be empty"):
            PlanRequest(plan_id="P001", task_description="")

    def test_kind_is_plan_request(self, plan_request):
        assert plan_request.KIND == MessageKind.PLAN_REQUEST


class TestPlanProposal:
    def test_valid_creation(self, plan_proposal):
        assert plan_proposal.risk_score == 0.6
        assert plan_proposal.files_affected == 12

    def test_risk_score_out_of_range_raises(self):
        with pytest.raises(ValueError, match="risk_score must be 0.0-1.0"):
            PlanProposal(
                plan_id="P001",
                complexity=PlanComplexity.LOW,
                risk_score=1.1,
                files_affected=3,
            )

    def test_negative_files_affected_raises(self):
        with pytest.raises(ValueError, match="files_affected cannot be negative"):
            PlanProposal(
                plan_id="P001",
                complexity=PlanComplexity.LOW,
                risk_score=0.1,
                files_affected=-1,
            )

    def test_kind_is_plan_proposal(self, plan_proposal):
        assert plan_proposal.KIND == MessageKind.PLAN_PROPOSAL


class TestPlanDecision:
    def test_approved(self, plan_decision_approved):
        assert plan_decision_approved.approved is True

    def test_rejected_with_feedback(self, plan_decision_rejected):
        assert plan_decision_rejected.approved is False
        assert plan_decision_rejected.feedback != ""

    def test_rejected_without_feedback_raises(self):
        with pytest.raises(ValueError, match="feedback required"):
            PlanDecision(plan_id="P001", approved=False)

    def test_kind_is_plan_decision(self, plan_decision_approved):
        assert plan_decision_approved.KIND == MessageKind.PLAN_DECISION


# ── ResearchQuery / ResearchReport ───────────────────────────────────────────

class TestResearchQuery:
    def test_valid_creation(self, research_query):
        assert research_query.query_id == "Q001"
        assert research_query.min_sources == 5

    def test_empty_query_id_raises(self):
        with pytest.raises(ValueError, match="query_id cannot be empty"):
            ResearchQuery(query_id="", topic="AI trends")

    def test_empty_topic_raises(self):
        with pytest.raises(ValueError, match="topic cannot be empty"):
            ResearchQuery(query_id="Q001", topic="")

    def test_min_sources_zero_raises(self):
        with pytest.raises(ValueError, match="min_sources must be positive"):
            ResearchQuery(query_id="Q001", topic="AI trends", min_sources=0)

    def test_kind_is_research_query(self, research_query):
        assert research_query.KIND == MessageKind.RESEARCH_QUERY


class TestResearchReport:
    def test_valid_creation(self, research_report):
        assert research_report.sources_consulted == 12
        assert len(research_report.key_findings) == 2

    def test_empty_query_id_raises(self):
        with pytest.raises(ValueError, match="query_id cannot be empty"):
            ResearchReport(query_id="", topic="AI", sources_consulted=5)

    def test_negative_sources_raises(self):
        with pytest.raises(ValueError, match="sources_consulted cannot be negative"):
            ResearchReport(query_id="Q001", topic="AI", sources_consulted=-1)

    def test_kind_is_research_report(self, research_report):
        assert research_report.KIND == MessageKind.RESEARCH_REPORT
