# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for spec.py core: dataclasses, PropertyReport, static checker.

Covers: PropertySpec validation for all 9 kinds, ProtocolSpec validation,
PropertyReport computed properties (all_passed/passed_count/violated_count),
and check_properties() static checker against DelegateTask and ArchitectFlow.
"""

import pytest

from cervellaswarm_lingua_universale.spec import (
    PropertyKind,
    PropertyVerdict,
    PropertySpec,
    ProtocolSpec,
    PropertyResult,
    PropertyReport,
    check_properties,
)
from cervellaswarm_lingua_universale.protocols import (
    DelegateTask,
    ArchitectFlow,
    Protocol,
    ProtocolStep,
    ProtocolChoice,
)
from cervellaswarm_lingua_universale.types import MessageKind


# ============================================================
# PropertySpec - dataclass validation
# ============================================================

class TestPropertySpecValidation:
    """PropertySpec __post_init__ validation by kind."""

    def test_always_terminates_valid(self):
        spec = PropertySpec(kind=PropertyKind.ALWAYS_TERMINATES)
        assert spec.kind == PropertyKind.ALWAYS_TERMINATES
        assert spec.params == ()
        assert spec.threshold == 0.0

    def test_no_deadlock_valid(self):
        spec = PropertySpec(kind=PropertyKind.NO_DEADLOCK)
        assert spec.kind == PropertyKind.NO_DEADLOCK
        assert spec.params == ()

    def test_all_roles_participate_valid(self):
        spec = PropertySpec(kind=PropertyKind.ALL_ROLES_PARTICIPATE)
        assert spec.kind == PropertyKind.ALL_ROLES_PARTICIPATE
        assert spec.params == ()

    def test_ordering_valid_two_params(self):
        spec = PropertySpec(
            kind=PropertyKind.ORDERING,
            params=("task_request", "task_result"),
        )
        assert spec.params == ("task_request", "task_result")

    def test_ordering_requires_exactly_two_params_zero(self):
        with pytest.raises(ValueError, match="ORDERING requires exactly 2 params"):
            PropertySpec(kind=PropertyKind.ORDERING, params=())

    def test_ordering_requires_exactly_two_params_one_given(self):
        with pytest.raises(ValueError, match="ORDERING requires exactly 2 params"):
            PropertySpec(kind=PropertyKind.ORDERING, params=("task_request",))

    def test_ordering_requires_exactly_two_params_three_given(self):
        with pytest.raises(ValueError, match="ORDERING requires exactly 2 params"):
            PropertySpec(
                kind=PropertyKind.ORDERING,
                params=("task_request", "task_result", "audit_request"),
            )

    def test_exclusion_valid_two_params(self):
        spec = PropertySpec(
            kind=PropertyKind.EXCLUSION,
            params=("worker", "audit_request"),
        )
        assert spec.params == ("worker", "audit_request")

    def test_exclusion_requires_exactly_two_params_zero(self):
        with pytest.raises(ValueError, match="EXCLUSION requires exactly 2 params"):
            PropertySpec(kind=PropertyKind.EXCLUSION, params=())

    def test_exclusion_requires_exactly_two_params_one_given(self):
        with pytest.raises(ValueError, match="EXCLUSION requires exactly 2 params"):
            PropertySpec(kind=PropertyKind.EXCLUSION, params=("worker",))

    def test_trust_min_valid_one_param(self):
        spec = PropertySpec(
            kind=PropertyKind.TRUST_MIN,
            params=("trusted",),
        )
        assert spec.params == ("trusted",)

    def test_trust_min_requires_exactly_one_param_zero(self):
        with pytest.raises(ValueError, match="TRUST_MIN requires exactly 1 param"):
            PropertySpec(kind=PropertyKind.TRUST_MIN, params=())

    def test_trust_min_requires_exactly_one_param_two_given(self):
        with pytest.raises(ValueError, match="TRUST_MIN requires exactly 1 param"):
            PropertySpec(
                kind=PropertyKind.TRUST_MIN,
                params=("trusted", "standard"),
            )

    def test_confidence_min_valid_threshold(self):
        spec = PropertySpec(kind=PropertyKind.CONFIDENCE_MIN, threshold=0.8)
        assert spec.threshold == 0.8

    def test_confidence_min_zero_threshold_valid(self):
        spec = PropertySpec(kind=PropertyKind.CONFIDENCE_MIN, threshold=0.0)
        assert spec.threshold == 0.0

    def test_confidence_min_one_threshold_valid(self):
        spec = PropertySpec(kind=PropertyKind.CONFIDENCE_MIN, threshold=1.0)
        assert spec.threshold == 1.0

    def test_confidence_min_threshold_above_one_raises(self):
        with pytest.raises(ValueError, match="CONFIDENCE_MIN threshold must be 0.0-1.0"):
            PropertySpec(kind=PropertyKind.CONFIDENCE_MIN, threshold=1.1)

    def test_confidence_min_threshold_negative_raises(self):
        with pytest.raises(ValueError, match="CONFIDENCE_MIN threshold must be 0.0-1.0"):
            PropertySpec(kind=PropertyKind.CONFIDENCE_MIN, threshold=-0.1)


# ============================================================
# ProtocolSpec - dataclass validation
# ============================================================

class TestProtocolSpecValidation:
    """ProtocolSpec __post_init__ validation."""

    def test_valid_construction(self):
        prop = PropertySpec(kind=PropertyKind.ALWAYS_TERMINATES)
        spec = ProtocolSpec(protocol_name="DelegateTask", properties=(prop,))
        assert spec.protocol_name == "DelegateTask"
        assert len(spec.properties) == 1

    def test_empty_name_raises(self):
        prop = PropertySpec(kind=PropertyKind.ALWAYS_TERMINATES)
        with pytest.raises(ValueError, match="protocol_name cannot be empty"):
            ProtocolSpec(protocol_name="", properties=(prop,))

    def test_empty_properties_raises(self):
        with pytest.raises(ValueError, match="properties cannot be empty"):
            ProtocolSpec(protocol_name="DelegateTask", properties=())


# ============================================================
# PropertyReport - computed properties
# ============================================================

class TestPropertyReport:
    """PropertyReport: all_passed, passed_count, violated_count."""

    def _make_result(self, verdict):
        spec = PropertySpec(kind=PropertyKind.ALWAYS_TERMINATES)
        return PropertyResult(spec=spec, verdict=verdict)

    def test_all_passed_when_all_proved(self):
        r1 = self._make_result(PropertyVerdict.PROVED)
        r2 = self._make_result(PropertyVerdict.PROVED)
        report = PropertyReport(protocol_name="X", results=(r1, r2))
        assert report.all_passed is True

    def test_all_passed_when_satisfied_and_skipped(self):
        r1 = self._make_result(PropertyVerdict.SATISFIED)
        r2 = self._make_result(PropertyVerdict.SKIPPED)
        report = PropertyReport(protocol_name="X", results=(r1, r2))
        assert report.all_passed is True

    def test_all_passed_false_when_violated(self):
        r1 = self._make_result(PropertyVerdict.PROVED)
        r2 = self._make_result(PropertyVerdict.VIOLATED)
        report = PropertyReport(protocol_name="X", results=(r1, r2))
        assert report.all_passed is False

    def test_passed_count_proved_and_satisfied(self):
        r1 = self._make_result(PropertyVerdict.PROVED)
        r2 = self._make_result(PropertyVerdict.SATISFIED)
        r3 = self._make_result(PropertyVerdict.SKIPPED)
        r4 = self._make_result(PropertyVerdict.VIOLATED)
        report = PropertyReport(protocol_name="X", results=(r1, r2, r3, r4))
        assert report.passed_count == 2

    def test_violated_count(self):
        r1 = self._make_result(PropertyVerdict.VIOLATED)
        r2 = self._make_result(PropertyVerdict.VIOLATED)
        r3 = self._make_result(PropertyVerdict.PROVED)
        report = PropertyReport(protocol_name="X", results=(r1, r2, r3))
        assert report.violated_count == 2

    def test_passed_count_zero_when_all_skipped(self):
        r1 = self._make_result(PropertyVerdict.SKIPPED)
        report = PropertyReport(protocol_name="X", results=(r1,))
        assert report.passed_count == 0
        assert report.all_passed is True

    def test_violated_count_zero_when_none_violated(self):
        r1 = self._make_result(PropertyVerdict.PROVED)
        report = PropertyReport(protocol_name="X", results=(r1,))
        assert report.violated_count == 0


# ============================================================
# Static checker: check_properties()
# ============================================================

class TestStaticAlwaysTerminates:
    """ALWAYS_TERMINATES static checks."""

    def test_delegate_task_proved(self):
        spec = ProtocolSpec(
            protocol_name="DelegateTask",
            properties=(PropertySpec(kind=PropertyKind.ALWAYS_TERMINATES),),
        )
        report = check_properties(DelegateTask, spec)
        assert report.results[0].verdict == PropertyVerdict.PROVED

    def test_architect_flow_proved(self):
        spec = ProtocolSpec(
            protocol_name="ArchitectFlow",
            properties=(PropertySpec(kind=PropertyKind.ALWAYS_TERMINATES),),
        )
        report = check_properties(ArchitectFlow, spec)
        assert report.results[0].verdict == PropertyVerdict.PROVED


class TestStaticNoDeadlock:
    """NO_DEADLOCK static checks."""

    def test_delegate_task_proved(self):
        spec = ProtocolSpec(
            protocol_name="DelegateTask",
            properties=(PropertySpec(kind=PropertyKind.NO_DEADLOCK),),
        )
        report = check_properties(DelegateTask, spec)
        assert report.results[0].verdict == PropertyVerdict.PROVED

    def test_architect_flow_proved(self):
        spec = ProtocolSpec(
            protocol_name="ArchitectFlow",
            properties=(PropertySpec(kind=PropertyKind.NO_DEADLOCK),),
        )
        report = check_properties(ArchitectFlow, spec)
        assert report.results[0].verdict == PropertyVerdict.PROVED


class TestStaticOrdering:
    """ORDERING static checks against protocol structure."""

    def test_task_request_before_task_result_delegate_task(self):
        spec = ProtocolSpec(
            protocol_name="DelegateTask",
            properties=(
                PropertySpec(
                    kind=PropertyKind.ORDERING,
                    params=("task_request", "task_result"),
                ),
            ),
        )
        report = check_properties(DelegateTask, spec)
        assert report.results[0].verdict == PropertyVerdict.PROVED

    def test_audit_request_before_audit_verdict_delegate_task(self):
        spec = ProtocolSpec(
            protocol_name="DelegateTask",
            properties=(
                PropertySpec(
                    kind=PropertyKind.ORDERING,
                    params=("audit_request", "audit_verdict"),
                ),
            ),
        )
        report = check_properties(DelegateTask, spec)
        assert report.results[0].verdict == PropertyVerdict.PROVED

    def test_reversed_ordering_violated(self):
        spec = ProtocolSpec(
            protocol_name="DelegateTask",
            properties=(
                PropertySpec(
                    kind=PropertyKind.ORDERING,
                    params=("task_result", "task_request"),
                ),
            ),
        )
        report = check_properties(DelegateTask, spec)
        assert report.results[0].verdict == PropertyVerdict.VIOLATED

    def test_architect_flow_task_request_before_task_result_in_approve(self):
        spec = ProtocolSpec(
            protocol_name="ArchitectFlow",
            properties=(
                PropertySpec(
                    kind=PropertyKind.ORDERING,
                    params=("task_request", "task_result"),
                ),
            ),
        )
        report = check_properties(ArchitectFlow, spec)
        assert report.results[0].verdict == PropertyVerdict.PROVED

    def test_ordering_vacuous_truth_kinds_absent_from_protocol(self):
        spec = ProtocolSpec(
            protocol_name="DelegateTask",
            properties=(
                PropertySpec(
                    kind=PropertyKind.ORDERING,
                    params=("research_query", "research_report"),
                ),
            ),
        )
        report = check_properties(DelegateTask, spec)
        assert report.results[0].verdict == PropertyVerdict.PROVED


class TestStaticExclusion:
    """EXCLUSION static checks."""

    def test_worker_cannot_send_audit_request_proved(self):
        spec = ProtocolSpec(
            protocol_name="DelegateTask",
            properties=(
                PropertySpec(
                    kind=PropertyKind.EXCLUSION,
                    params=("worker", "audit_request"),
                ),
            ),
        )
        report = check_properties(DelegateTask, spec)
        assert report.results[0].verdict == PropertyVerdict.PROVED

    def test_worker_cannot_send_task_result_violated(self):
        # worker DOES send task_result in DelegateTask -> VIOLATED
        spec = ProtocolSpec(
            protocol_name="DelegateTask",
            properties=(
                PropertySpec(
                    kind=PropertyKind.EXCLUSION,
                    params=("worker", "task_result"),
                ),
            ),
        )
        report = check_properties(DelegateTask, spec)
        assert report.results[0].verdict == PropertyVerdict.VIOLATED

    def test_regina_cannot_send_audit_verdict_proved(self):
        spec = ProtocolSpec(
            protocol_name="DelegateTask",
            properties=(
                PropertySpec(
                    kind=PropertyKind.EXCLUSION,
                    params=("regina", "audit_verdict"),
                ),
            ),
        )
        report = check_properties(DelegateTask, spec)
        assert report.results[0].verdict == PropertyVerdict.PROVED


class TestStaticTrustMin:
    """TRUST_MIN static checks."""

    def test_standard_trust_delegate_task_proved(self):
        spec = ProtocolSpec(
            protocol_name="DelegateTask",
            properties=(
                PropertySpec(kind=PropertyKind.TRUST_MIN, params=("standard",)),
            ),
        )
        report = check_properties(DelegateTask, spec)
        assert report.results[0].verdict == PropertyVerdict.PROVED

    def test_untrusted_tier_always_passes(self):
        spec = ProtocolSpec(
            protocol_name="DelegateTask",
            properties=(
                PropertySpec(kind=PropertyKind.TRUST_MIN, params=("untrusted",)),
            ),
        )
        report = check_properties(DelegateTask, spec)
        assert report.results[0].verdict == PropertyVerdict.PROVED


class TestStaticConfidenceMin:
    """CONFIDENCE_MIN is always SKIPPED in static mode."""

    def test_confidence_min_skipped_static(self):
        spec = ProtocolSpec(
            protocol_name="DelegateTask",
            properties=(
                PropertySpec(kind=PropertyKind.CONFIDENCE_MIN, threshold=0.8),
            ),
        )
        report = check_properties(DelegateTask, spec)
        assert report.results[0].verdict == PropertyVerdict.SKIPPED


class TestStaticAllRolesParticipate:
    """ALL_ROLES_PARTICIPATE static checks."""

    def test_delegate_task_all_three_roles_proved(self):
        spec = ProtocolSpec(
            protocol_name="DelegateTask",
            properties=(
                PropertySpec(kind=PropertyKind.ALL_ROLES_PARTICIPATE),
            ),
        )
        report = check_properties(DelegateTask, spec)
        assert report.results[0].verdict == PropertyVerdict.PROVED

    def test_architect_flow_all_four_roles_proved(self):
        spec = ProtocolSpec(
            protocol_name="ArchitectFlow",
            properties=(
                PropertySpec(kind=PropertyKind.ALL_ROLES_PARTICIPATE),
            ),
        )
        report = check_properties(ArchitectFlow, spec)
        assert report.results[0].verdict == PropertyVerdict.PROVED

    def test_protocol_with_unused_declared_role_violated(self):
        phantom_protocol = Protocol(
            name="PhantomTest",
            roles=("regina", "worker", "ghost"),
            elements=(
                ProtocolStep(
                    sender="regina",
                    receiver="worker",
                    message_kind=MessageKind.TASK_REQUEST,
                ),
                ProtocolStep(
                    sender="worker",
                    receiver="regina",
                    message_kind=MessageKind.TASK_RESULT,
                ),
            ),
        )
        spec = ProtocolSpec(
            protocol_name="PhantomTest",
            properties=(
                PropertySpec(kind=PropertyKind.ALL_ROLES_PARTICIPATE),
            ),
        )
        report = check_properties(phantom_protocol, spec)
        assert report.results[0].verdict == PropertyVerdict.VIOLATED
        assert "ghost" in report.results[0].evidence


class TestStaticFullSpec:
    """Full spec with all 9 property types -> PropertyReport correctness."""

    def test_full_spec_delegate_task_report(self):
        spec = ProtocolSpec(
            protocol_name="DelegateTask",
            properties=(
                PropertySpec(kind=PropertyKind.ALWAYS_TERMINATES),
                PropertySpec(kind=PropertyKind.NO_DEADLOCK),
                PropertySpec(
                    kind=PropertyKind.ORDERING,
                    params=("task_request", "task_result"),
                ),
                PropertySpec(
                    kind=PropertyKind.EXCLUSION,
                    params=("worker", "audit_request"),
                ),
                PropertySpec(kind=PropertyKind.CONFIDENCE_MIN, threshold=0.8),
                PropertySpec(kind=PropertyKind.TRUST_MIN, params=("standard",)),
                PropertySpec(kind=PropertyKind.ALL_ROLES_PARTICIPATE),
            ),
        )
        report = check_properties(DelegateTask, spec)
        assert len(report.results) == 7
        assert report.protocol_name == "DelegateTask"
        verdicts = {r.verdict for r in report.results}
        assert PropertyVerdict.VIOLATED not in verdicts
        assert PropertyVerdict.SKIPPED in verdicts
        # 6 PROVED, 1 SKIPPED (CONFIDENCE_MIN)
        assert report.passed_count == 6
        assert report.violated_count == 0
        assert report.all_passed is True


# ============================================================
# F6 fix: EXCLUSION violation in a branch
# F7 fix: direct _collect_all_paths test
# F8 fix: TRUST_MIN VIOLATED test
# ============================================================


class TestGuardianaFixes:
    """Tests added per Guardiana audit F6, F7, F8."""

    def test_exclusion_violation_in_branch(self):
        """F6: EXCLUSION should detect violations inside choice branches."""
        proto = Protocol(
            name="BranchExclusion",
            roles=("regina", "worker", "guardiana"),
            elements=(
                ProtocolStep(
                    sender="regina",
                    receiver="worker",
                    message_kind=MessageKind.TASK_REQUEST,
                ),
                ProtocolChoice(
                    decider="regina",
                    branches={
                        "good": (
                            ProtocolStep(
                                sender="worker",
                                receiver="regina",
                                message_kind=MessageKind.TASK_RESULT,
                            ),
                        ),
                        "bad": (
                            ProtocolStep(
                                sender="worker",
                                receiver="regina",
                                message_kind=MessageKind.AUDIT_VERDICT,
                            ),
                        ),
                    },
                ),
            ),
        )
        spec = ProtocolSpec(
            protocol_name="BranchExclusion",
            properties=(
                PropertySpec(
                    kind=PropertyKind.EXCLUSION,
                    params=("worker", "audit_verdict"),
                ),
            ),
        )
        report = check_properties(proto, spec)
        assert report.results[0].verdict == PropertyVerdict.VIOLATED
        assert "bad" in report.results[0].evidence

    def test_collect_all_paths_branch_count(self):
        """F7: _collect_all_paths returns correct path count for ArchitectFlow."""
        from cervellaswarm_lingua_universale.spec import _collect_all_paths

        paths = _collect_all_paths(ArchitectFlow.elements)
        # ArchitectFlow has 1 choice with 2 branches -> 2 paths
        assert len(paths) == 2
        # Approve path: 2 pre-choice + 5 in branch = 7 steps
        # Reject path: 2 pre-choice + 2 in branch = 4 steps
        path_lengths = sorted(len(p) for p in paths)
        assert path_lengths == [4, 7]

    def test_trust_min_violated_for_insufficient_tier(self):
        """F8: TRUST_MIN VIOLATED when role has lower tier than required."""
        # worker has STANDARD tier; requiring VERIFIED should VIOLATE
        spec = ProtocolSpec(
            protocol_name="DelegateTask",
            properties=(
                PropertySpec(kind=PropertyKind.TRUST_MIN, params=("verified",)),
            ),
        )
        report = check_properties(DelegateTask, spec)
        assert report.results[0].verdict == PropertyVerdict.VIOLATED
        assert "worker" in report.results[0].evidence or "guardiana" in report.results[0].evidence


# ============================================================
# NO_DELETION static checker tests
# ============================================================


class TestStaticNoDeletion:
    """NO_DELETION static checks."""

    def test_no_deletion_proved_on_standard_protocol(self):
        """check_properties with NO_DELETION on a standard Protocol -> PROVED.

        DelegateTask uses no DELETE-related MessageKind (none exist currently).
        """
        spec = ProtocolSpec(
            protocol_name="DelegateTask",
            properties=(PropertySpec(kind=PropertyKind.NO_DELETION),),
        )
        report = check_properties(DelegateTask, spec)
        assert report.results[0].verdict == PropertyVerdict.PROVED

    def test_no_deletion_proved_on_architect_flow(self):
        """ArchitectFlow also has no deletion kinds -> PROVED."""
        spec = ProtocolSpec(
            protocol_name="ArchitectFlow",
            properties=(PropertySpec(kind=PropertyKind.NO_DELETION),),
        )
        report = check_properties(ArchitectFlow, spec)
        assert report.results[0].verdict == PropertyVerdict.PROVED


# ============================================================
# ROLE_EXCLUSIVE static checker tests
# ============================================================


class TestStaticRoleExclusive:
    """ROLE_EXCLUSIVE static checks."""

    def test_role_exclusive_proved(self):
        """Protocol where only role X sends dm -> PROVED."""
        proto = Protocol(
            name="ExclusiveProto",
            roles=("Cuoco", "Pantry"),
            elements=(
                ProtocolStep(
                    sender="Cuoco",
                    receiver="Pantry",
                    message_kind=MessageKind.DM,
                ),
                ProtocolStep(
                    sender="Pantry",
                    receiver="Cuoco",
                    message_kind=MessageKind.TASK_RESULT,
                ),
            ),
        )
        spec = ProtocolSpec(
            protocol_name="ExclusiveProto",
            properties=(
                PropertySpec(
                    kind=PropertyKind.ROLE_EXCLUSIVE,
                    params=("Cuoco", "dm"),
                ),
            ),
        )
        report = check_properties(proto, spec)
        assert report.results[0].verdict == PropertyVerdict.PROVED

    def test_role_exclusive_violated(self):
        """Protocol where role Y also sends dm -> VIOLATED."""
        proto = Protocol(
            name="ViolationProto",
            roles=("Cuoco", "Pantry"),
            elements=(
                ProtocolStep(
                    sender="Cuoco",
                    receiver="Pantry",
                    message_kind=MessageKind.DM,
                ),
                ProtocolStep(
                    sender="Pantry",
                    receiver="Cuoco",
                    message_kind=MessageKind.DM,
                ),
            ),
        )
        spec = ProtocolSpec(
            protocol_name="ViolationProto",
            properties=(
                PropertySpec(
                    kind=PropertyKind.ROLE_EXCLUSIVE,
                    params=("Cuoco", "dm"),
                ),
            ),
        )
        report = check_properties(proto, spec)
        assert report.results[0].verdict == PropertyVerdict.VIOLATED
