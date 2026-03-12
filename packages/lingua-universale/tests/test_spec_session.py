# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for spec.py runtime checker: check_session() against completed sessions.

Covers: ORDERING, EXCLUSION, ALWAYS_TERMINATES, NO_DEADLOCK, NO_DELETION,
ROLE_EXCLUSIVE, TRUST_MIN, CONFIDENCE_MIN, and ALL_ROLES_PARTICIPATE in runtime
mode (SATISFIED/VIOLATED/SKIPPED).
"""

import pytest

from cervellaswarm_lingua_universale.spec import (
    PropertyKind,
    PropertyVerdict,
    PropertySpec,
    ProtocolSpec,
    check_session,
)
from cervellaswarm_lingua_universale.protocols import DelegateTask
from cervellaswarm_lingua_universale.types import (
    MessageKind,
    TaskRequest,
    TaskResult,
    TaskStatus,
    AuditRequest,
    AuditVerdict,
    AuditVerdictType,
)
from cervellaswarm_lingua_universale.checker import MessageRecord, SessionChecker


# ============================================================
# Helpers
# ============================================================

def make_task_request(task_id="T001"):
    return TaskRequest(task_id=task_id, description="Do the work")


def make_task_result(task_id="T001"):
    return TaskResult(task_id=task_id, status=TaskStatus.OK, summary="Done")


def make_audit_request(audit_id="A001"):
    return AuditRequest(audit_id=audit_id, target="output")


def make_audit_verdict(audit_id="A001"):
    return AuditVerdict(
        audit_id=audit_id,
        verdict=AuditVerdictType.APPROVED,
        score=9.0,
        checked=("tests present",),
    )


def run_delegate_task_session():
    """Run a complete DelegateTask session and return the log."""
    checker = SessionChecker(DelegateTask, session_id="spec-session-test")
    checker.send("regina", "worker", make_task_request())
    checker.send("worker", "regina", make_task_result())
    checker.send("regina", "guardiana", make_audit_request())
    checker.send("guardiana", "regina", make_audit_verdict())
    assert checker.is_complete
    return checker.log


def make_record(sender, receiver, kind, step_index=0, timestamp=1.0):
    return MessageRecord(
        timestamp=timestamp,
        sender=sender,
        receiver=receiver,
        kind=kind,
        step_index=step_index,
    )


# ============================================================
# ORDERING - runtime
# ============================================================

class TestCheckSessionOrdering:
    """ORDERING runtime checks on session log."""

    def test_correct_ordering_satisfied(self):
        log = run_delegate_task_session()
        spec = ProtocolSpec(
            protocol_name="DelegateTask",
            properties=(
                PropertySpec(
                    kind=PropertyKind.ORDERING,
                    params=("task_request", "task_result"),
                ),
            ),
        )
        report = check_session(log, spec)
        assert report.results[0].verdict == PropertyVerdict.SATISFIED

    def test_audit_ordering_satisfied(self):
        log = run_delegate_task_session()
        spec = ProtocolSpec(
            protocol_name="DelegateTask",
            properties=(
                PropertySpec(
                    kind=PropertyKind.ORDERING,
                    params=("audit_request", "audit_verdict"),
                ),
            ),
        )
        report = check_session(log, spec)
        assert report.results[0].verdict == PropertyVerdict.SATISFIED

    def test_ordering_vacuous_satisfaction_both_kinds_absent(self):
        log = run_delegate_task_session()
        spec = ProtocolSpec(
            protocol_name="DelegateTask",
            properties=(
                PropertySpec(
                    kind=PropertyKind.ORDERING,
                    params=("research_query", "research_report"),
                ),
            ),
        )
        report = check_session(log, spec)
        assert report.results[0].verdict == PropertyVerdict.SATISFIED

    def test_ordering_vacuous_satisfaction_one_kind_absent(self):
        log = run_delegate_task_session()
        spec = ProtocolSpec(
            protocol_name="DelegateTask",
            properties=(
                PropertySpec(
                    kind=PropertyKind.ORDERING,
                    params=("task_request", "research_query"),
                ),
            ),
        )
        report = check_session(log, spec)
        assert report.results[0].verdict == PropertyVerdict.SATISFIED

    def test_ordering_violated_task_result_before_task_request(self):
        r1 = make_record("worker", "regina", MessageKind.TASK_RESULT, step_index=0)
        r2 = make_record("regina", "worker", MessageKind.TASK_REQUEST, step_index=1, timestamp=2.0)
        log = [r1, r2]
        spec = ProtocolSpec(
            protocol_name="DelegateTask",
            properties=(
                PropertySpec(
                    kind=PropertyKind.ORDERING,
                    params=("task_request", "task_result"),
                ),
            ),
        )
        report = check_session(log, spec)
        assert report.results[0].verdict == PropertyVerdict.VIOLATED

    def test_ordering_evidence_contains_message_indices(self):
        log = run_delegate_task_session()
        spec = ProtocolSpec(
            protocol_name="DelegateTask",
            properties=(
                PropertySpec(
                    kind=PropertyKind.ORDERING,
                    params=("task_request", "task_result"),
                ),
            ),
        )
        report = check_session(log, spec)
        assert "0" in report.results[0].evidence or "1" in report.results[0].evidence


# ============================================================
# EXCLUSION - runtime
# ============================================================

class TestCheckSessionExclusion:
    """EXCLUSION runtime checks on session log."""

    def test_no_violation_satisfied(self):
        log = run_delegate_task_session()
        spec = ProtocolSpec(
            protocol_name="DelegateTask",
            properties=(
                PropertySpec(
                    kind=PropertyKind.EXCLUSION,
                    params=("worker", "audit_request"),
                ),
            ),
        )
        report = check_session(log, spec)
        assert report.results[0].verdict == PropertyVerdict.SATISFIED

    def test_violation_detected_worker_sends_audit_request(self):
        bad = make_record("worker", "guardiana", MessageKind.AUDIT_REQUEST)
        log = [bad]
        spec = ProtocolSpec(
            protocol_name="DelegateTask",
            properties=(
                PropertySpec(
                    kind=PropertyKind.EXCLUSION,
                    params=("worker", "audit_request"),
                ),
            ),
        )
        report = check_session(log, spec)
        assert report.results[0].verdict == PropertyVerdict.VIOLATED

    def test_evidence_contains_message_index(self):
        bad = make_record("worker", "guardiana", MessageKind.AUDIT_REQUEST)
        log = [make_record("regina", "worker", MessageKind.TASK_REQUEST), bad]
        spec = ProtocolSpec(
            protocol_name="DelegateTask",
            properties=(
                PropertySpec(
                    kind=PropertyKind.EXCLUSION,
                    params=("worker", "audit_request"),
                ),
            ),
        )
        report = check_session(log, spec)
        assert report.results[0].verdict == PropertyVerdict.VIOLATED
        assert "1" in report.results[0].evidence


# ============================================================
# ALWAYS_TERMINATES + NO_DEADLOCK - runtime
# ============================================================

class TestCheckSessionTermination:
    """ALWAYS_TERMINATES and NO_DEADLOCK are SATISFIED for completed sessions."""

    def test_always_terminates_satisfied(self):
        log = run_delegate_task_session()
        spec = ProtocolSpec(
            protocol_name="DelegateTask",
            properties=(PropertySpec(kind=PropertyKind.ALWAYS_TERMINATES),),
        )
        report = check_session(log, spec)
        assert report.results[0].verdict == PropertyVerdict.SATISFIED

    def test_no_deadlock_satisfied(self):
        log = run_delegate_task_session()
        spec = ProtocolSpec(
            protocol_name="DelegateTask",
            properties=(PropertySpec(kind=PropertyKind.NO_DEADLOCK),),
        )
        report = check_session(log, spec)
        assert report.results[0].verdict == PropertyVerdict.SATISFIED

    def test_evidence_mentions_message_count(self):
        log = run_delegate_task_session()
        spec = ProtocolSpec(
            protocol_name="DelegateTask",
            properties=(PropertySpec(kind=PropertyKind.ALWAYS_TERMINATES),),
        )
        report = check_session(log, spec)
        assert "4" in report.results[0].evidence


# ============================================================
# SKIPPED properties in runtime
# ============================================================

class TestCheckSessionSkipped:
    """TRUST_MIN and CONFIDENCE_MIN are SKIPPED in runtime."""

    def test_trust_min_skipped(self):
        log = run_delegate_task_session()
        spec = ProtocolSpec(
            protocol_name="DelegateTask",
            properties=(PropertySpec(kind=PropertyKind.TRUST_MIN, params=("standard",)),),
        )
        report = check_session(log, spec)
        assert report.results[0].verdict == PropertyVerdict.SKIPPED

    def test_confidence_min_skipped(self):
        log = run_delegate_task_session()
        spec = ProtocolSpec(
            protocol_name="DelegateTask",
            properties=(PropertySpec(kind=PropertyKind.CONFIDENCE_MIN, threshold=0.8),),
        )
        report = check_session(log, spec)
        assert report.results[0].verdict == PropertyVerdict.SKIPPED


# ============================================================
# ALL_ROLES_PARTICIPATE - runtime
# ============================================================

class TestCheckSessionAllRolesParticipate:
    """ALL_ROLES_PARTICIPATE runtime checks."""

    def test_all_roles_present_satisfied(self):
        log = run_delegate_task_session()
        spec = ProtocolSpec(
            protocol_name="DelegateTask",
            properties=(PropertySpec(kind=PropertyKind.ALL_ROLES_PARTICIPATE),),
        )
        report = check_session(log, spec, protocol=DelegateTask)
        assert report.results[0].verdict == PropertyVerdict.SATISFIED

    def test_missing_role_violated_with_protocol(self):
        # Only regina and worker in log; guardiana is declared but absent
        r1 = make_record("regina", "worker", MessageKind.TASK_REQUEST)
        r2 = make_record("worker", "regina", MessageKind.TASK_RESULT, timestamp=2.0)
        log = [r1, r2]
        spec = ProtocolSpec(
            protocol_name="DelegateTask",
            properties=(PropertySpec(kind=PropertyKind.ALL_ROLES_PARTICIPATE),),
        )
        report = check_session(log, spec, protocol=DelegateTask)
        assert report.results[0].verdict == PropertyVerdict.VIOLATED
        assert "guardiana" in report.results[0].evidence

    def test_without_protocol_uses_log_roles_satisfied(self):
        # Without protocol, all roles in the log are considered declared
        log = run_delegate_task_session()
        spec = ProtocolSpec(
            protocol_name="DelegateTask",
            properties=(PropertySpec(kind=PropertyKind.ALL_ROLES_PARTICIPATE),),
        )
        report = check_session(log, spec, protocol=None)
        assert report.results[0].verdict == PropertyVerdict.SATISFIED

    def test_evidence_lists_all_roles_when_satisfied(self):
        log = run_delegate_task_session()
        spec = ProtocolSpec(
            protocol_name="DelegateTask",
            properties=(PropertySpec(kind=PropertyKind.ALL_ROLES_PARTICIPATE),),
        )
        report = check_session(log, spec, protocol=DelegateTask)
        evidence = report.results[0].evidence
        assert "regina" in evidence
        assert "worker" in evidence
        assert "guardiana" in evidence


# ============================================================
# Report metadata
# ============================================================

class TestCheckSessionReportMetadata:
    """check_session() report protocol_name uses spec name, not protocol name."""

    def test_report_protocol_name_from_spec(self):
        log = run_delegate_task_session()
        spec = ProtocolSpec(
            protocol_name="MySpecName",
            properties=(PropertySpec(kind=PropertyKind.ALWAYS_TERMINATES),),
        )
        report = check_session(log, spec)
        assert report.protocol_name == "MySpecName"

    def test_report_has_one_result_per_property(self):
        log = run_delegate_task_session()
        spec = ProtocolSpec(
            protocol_name="DelegateTask",
            properties=(
                PropertySpec(kind=PropertyKind.ALWAYS_TERMINATES),
                PropertySpec(kind=PropertyKind.NO_DEADLOCK),
                PropertySpec(
                    kind=PropertyKind.ORDERING,
                    params=("task_request", "task_result"),
                ),
            ),
        )
        report = check_session(log, spec)
        assert len(report.results) == 3

    # F5 fix: empty log handling
    def test_empty_log_ordering_vacuously_satisfied(self):
        """check_session with empty log: ORDERING is vacuously satisfied."""
        spec = ProtocolSpec(
            protocol_name="DelegateTask",
            properties=(
                PropertySpec(
                    kind=PropertyKind.ORDERING,
                    params=("task_request", "task_result"),
                ),
            ),
        )
        report = check_session([], spec)
        assert report.results[0].verdict == PropertyVerdict.SATISFIED

    def test_empty_log_exclusion_satisfied(self):
        """check_session with empty log: EXCLUSION is satisfied (no messages)."""
        spec = ProtocolSpec(
            protocol_name="DelegateTask",
            properties=(
                PropertySpec(
                    kind=PropertyKind.EXCLUSION,
                    params=("worker", "audit_verdict"),
                ),
            ),
        )
        report = check_session([], spec)
        assert report.results[0].verdict == PropertyVerdict.SATISFIED

    def test_empty_log_terminates_satisfied(self):
        """check_session with empty log: ALWAYS_TERMINATES is satisfied."""
        spec = ProtocolSpec(
            protocol_name="DelegateTask",
            properties=(
                PropertySpec(kind=PropertyKind.ALWAYS_TERMINATES),
            ),
        )
        report = check_session([], spec)
        assert report.results[0].verdict == PropertyVerdict.SATISFIED


# ============================================================
# NO_DELETION and ROLE_EXCLUSIVE runtime tests
# ============================================================


class TestCheckSessionNoDeletion:
    """NO_DELETION runtime checks."""

    def test_no_deletion_satisfied_runtime(self):
        """check_session with NO_DELETION on a completed session -> SATISFIED."""
        log = run_delegate_task_session()
        spec = ProtocolSpec(
            protocol_name="DelegateTask",
            properties=(PropertySpec(kind=PropertyKind.NO_DELETION),),
        )
        report = check_session(log, spec)
        assert report.results[0].verdict == PropertyVerdict.SATISFIED

    def test_no_deletion_satisfied_empty_log(self):
        """check_session with NO_DELETION on empty log -> SATISFIED."""
        spec = ProtocolSpec(
            protocol_name="DelegateTask",
            properties=(PropertySpec(kind=PropertyKind.NO_DELETION),),
        )
        report = check_session([], spec)
        assert report.results[0].verdict == PropertyVerdict.SATISFIED


class TestCheckSessionRoleExclusive:
    """ROLE_EXCLUSIVE runtime checks."""

    def test_role_exclusive_satisfied_runtime(self):
        """Session where only the correct role sends dm -> SATISFIED."""
        records = [
            make_record("Cuoco", "Pantry", MessageKind.DM, step_index=0),
            make_record("Pantry", "Cuoco", MessageKind.TASK_RESULT, step_index=1, timestamp=2.0),
        ]
        spec = ProtocolSpec(
            protocol_name="CookerProto",
            properties=(
                PropertySpec(
                    kind=PropertyKind.ROLE_EXCLUSIVE,
                    params=("Cuoco", "dm"),
                ),
            ),
        )
        report = check_session(records, spec)
        assert report.results[0].verdict == PropertyVerdict.SATISFIED

    def test_role_exclusive_violated_runtime(self):
        """Session where a wrong role sends dm -> VIOLATED."""
        records = [
            make_record("Cuoco", "Pantry", MessageKind.DM, step_index=0),
            make_record("Pantry", "Cuoco", MessageKind.DM, step_index=1, timestamp=2.0),
        ]
        spec = ProtocolSpec(
            protocol_name="CookerProto",
            properties=(
                PropertySpec(
                    kind=PropertyKind.ROLE_EXCLUSIVE,
                    params=("Cuoco", "dm"),
                ),
            ),
        )
        report = check_session(records, spec)
        assert report.results[0].verdict == PropertyVerdict.VIOLATED
        assert "Pantry" in report.results[0].evidence

    def test_role_exclusive_satisfied_no_dm_in_session(self):
        """Session with no dm messages -> SATISFIED (vacuously)."""
        log = run_delegate_task_session()
        spec = ProtocolSpec(
            protocol_name="DelegateTask",
            properties=(
                PropertySpec(
                    kind=PropertyKind.ROLE_EXCLUSIVE,
                    params=("regina", "dm"),
                ),
            ),
        )
        report = check_session(log, spec)
        assert report.results[0].verdict == PropertyVerdict.SATISFIED
