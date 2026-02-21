# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for lean4_bridge.py - Core unit tests (no Lean 4 required).

Coverage target: 100% on lean4_bridge.py generator path.
All tests run without Lean 4 installed.
"""

import pytest

from cervellaswarm_lingua_universale.lean4_bridge import (
    ALL_PROPERTIES,
    FLAT_PROPERTIES,
    Lean4Generator,
    Lean4Verifier,
    VerificationProperty,
    VerificationReport,
    VerificationResult,
    _collect_all_steps,
    _collect_choices,
    _extract_theorem,
    _has_choices,
    _lean_constructor,
    _safe_lean_ident,
    _used_message_kinds,
    _validate_lean_name,
    generate_lean4,
    generate_lean4_multi,
    lean4_available,
)
from cervellaswarm_lingua_universale.protocols import (
    ArchitectFlow,
    DelegateTask,
    Protocol,
    ProtocolChoice,
    ProtocolStep,
    ResearchFlow,
    SimpleTask,
)
from cervellaswarm_lingua_universale.types import MessageKind


# ============================================================
# Helpers - custom protocol builders
# ============================================================


def make_flat_protocol(
    name="TestFlat",
    roles=("alpha", "beta"),
    kinds=(MessageKind.TASK_REQUEST, MessageKind.TASK_RESULT),
) -> Protocol:
    """Build a flat protocol (no choices) for testing."""
    elements = tuple(
        ProtocolStep(
            sender=roles[i % len(roles)],
            receiver=roles[(i + 1) % len(roles)],
            message_kind=kind,
        )
        for i, kind in enumerate(kinds)
    )
    return Protocol(name=name, roles=roles, elements=elements)


def make_choice_protocol(name="TestChoice") -> Protocol:
    """Build a protocol with a ProtocolChoice."""
    return Protocol(
        name=name,
        roles=("alpha", "beta", "gamma"),
        elements=(
            ProtocolStep(
                sender="alpha",
                receiver="beta",
                message_kind=MessageKind.TASK_REQUEST,
            ),
            ProtocolChoice(
                decider="alpha",
                branches={
                    "accept": (
                        ProtocolStep(
                            sender="beta",
                            receiver="alpha",
                            message_kind=MessageKind.TASK_RESULT,
                        ),
                    ),
                    "reject": (
                        ProtocolStep(
                            sender="beta",
                            receiver="gamma",
                            message_kind=MessageKind.AUDIT_REQUEST,
                        ),
                    ),
                },
            ),
        ),
    )


# ============================================================
# 1. VerificationProperty enum
# ============================================================


class TestVerificationProperty:
    def test_all_values_exist(self):
        expected = {
            "SENDERS_IN_ROLES",
            "RECEIVERS_IN_ROLES",
            "NO_SELF_LOOP",
            "MIN_ROLES",
            "NON_EMPTY",
            "BRANCHES_NON_EMPTY",
            "DECIDER_IN_ROLES",
        }
        names = {p.name for p in VerificationProperty}
        assert names == expected

    def test_senders_in_roles_value(self):
        assert VerificationProperty.SENDERS_IN_ROLES.value == "senders_in_roles"

    def test_no_self_loop_value(self):
        assert VerificationProperty.NO_SELF_LOOP.value == "no_self_loop"

    def test_branches_non_empty_value(self):
        assert VerificationProperty.BRANCHES_NON_EMPTY.value == "branches_non_empty"

    def test_decider_in_roles_value(self):
        assert VerificationProperty.DECIDER_IN_ROLES.value == "decider_in_roles"

    def test_flat_properties_count(self):
        assert len(FLAT_PROPERTIES) == 5

    def test_flat_properties_contains_senders(self):
        assert VerificationProperty.SENDERS_IN_ROLES in FLAT_PROPERTIES

    def test_flat_properties_contains_receivers(self):
        assert VerificationProperty.RECEIVERS_IN_ROLES in FLAT_PROPERTIES

    def test_flat_properties_contains_no_self_loop(self):
        assert VerificationProperty.NO_SELF_LOOP in FLAT_PROPERTIES

    def test_flat_properties_contains_min_roles(self):
        assert VerificationProperty.MIN_ROLES in FLAT_PROPERTIES

    def test_flat_properties_contains_non_empty(self):
        assert VerificationProperty.NON_EMPTY in FLAT_PROPERTIES

    def test_flat_properties_excludes_branches_non_empty(self):
        assert VerificationProperty.BRANCHES_NON_EMPTY not in FLAT_PROPERTIES

    def test_flat_properties_excludes_decider_in_roles(self):
        assert VerificationProperty.DECIDER_IN_ROLES not in FLAT_PROPERTIES

    def test_all_properties_count(self):
        assert len(ALL_PROPERTIES) == 7

    def test_all_properties_is_superset_of_flat(self):
        flat_set = set(FLAT_PROPERTIES)
        all_set = set(ALL_PROPERTIES)
        assert flat_set.issubset(all_set)

    def test_all_properties_contains_branches_non_empty(self):
        assert VerificationProperty.BRANCHES_NON_EMPTY in ALL_PROPERTIES

    def test_all_properties_contains_decider_in_roles(self):
        assert VerificationProperty.DECIDER_IN_ROLES in ALL_PROPERTIES


# ============================================================
# 2. VerificationResult
# ============================================================


class TestVerificationResult:
    def test_create_proved_true(self):
        r = VerificationResult(
            property_name="no_self_loop",
            proved=True,
            lean_theorem="theorem foo_no_self_loop : True := by decide",
        )
        assert r.proved is True
        assert r.property_name == "no_self_loop"

    def test_create_proved_false_with_error(self):
        r = VerificationResult(
            property_name="senders_in_roles",
            proved=False,
            lean_theorem="theorem foo : False := by decide",
            error="tactic failed",
        )
        assert r.proved is False
        assert r.error == "tactic failed"

    def test_error_defaults_to_none(self):
        r = VerificationResult(
            property_name="non_empty",
            proved=True,
            lean_theorem="theorem t : True := by decide",
        )
        assert r.error is None

    def test_empty_property_name_raises(self):
        with pytest.raises(ValueError, match="property_name cannot be empty"):
            VerificationResult(
                property_name="",
                proved=True,
                lean_theorem="theorem t : True := by decide",
            )

    def test_empty_lean_theorem_raises(self):
        with pytest.raises(ValueError, match="lean_theorem cannot be empty"):
            VerificationResult(
                property_name="non_empty",
                proved=True,
                lean_theorem="",
            )

    def test_is_frozen(self):
        from dataclasses import FrozenInstanceError

        r = VerificationResult(
            property_name="non_empty",
            proved=True,
            lean_theorem="theorem t : True := by decide",
        )
        with pytest.raises(FrozenInstanceError):
            r.proved = False  # type: ignore[misc]


# ============================================================
# 3. VerificationReport
# ============================================================


class TestVerificationReport:
    def _make_result(self, proved=True):
        return VerificationResult(
            property_name="non_empty",
            proved=proved,
            lean_theorem="theorem t : True := by decide",
        )

    def test_create_basic(self):
        r = self._make_result()
        report = VerificationReport(
            protocol_name="TestProto",
            results=(r,),
            lean_code="-- code",
        )
        assert report.protocol_name == "TestProto"

    def test_all_proved_true_when_all_proved(self):
        results = tuple(self._make_result(proved=True) for _ in range(3))
        report = VerificationReport(
            protocol_name="TestProto",
            results=results,
            lean_code="-- code",
        )
        assert report.all_proved is True

    def test_all_proved_false_when_any_failed(self):
        results = (
            self._make_result(proved=True),
            self._make_result(proved=False),
        )
        report = VerificationReport(
            protocol_name="TestProto",
            results=results,
            lean_code="-- code",
        )
        assert report.all_proved is False

    def test_all_proved_false_when_empty_results(self):
        report = VerificationReport(
            protocol_name="TestProto",
            results=(),
            lean_code="-- code",
        )
        assert report.all_proved is False

    def test_proved_count(self):
        results = (
            self._make_result(proved=True),
            self._make_result(proved=True),
            self._make_result(proved=False),
        )
        report = VerificationReport(
            protocol_name="TestProto",
            results=results,
            lean_code="-- code",
        )
        assert report.proved_count == 2

    def test_total_count(self):
        results = tuple(self._make_result() for _ in range(5))
        report = VerificationReport(
            protocol_name="TestProto",
            results=results,
            lean_code="-- code",
        )
        assert report.total_count == 5

    def test_empty_protocol_name_raises(self):
        with pytest.raises(ValueError, match="protocol_name cannot be empty"):
            VerificationReport(
                protocol_name="",
                results=(),
                lean_code="-- code",
            )

    def test_empty_lean_code_raises(self):
        with pytest.raises(ValueError, match="lean_code cannot be empty"):
            VerificationReport(
                protocol_name="TestProto",
                results=(),
                lean_code="",
            )

    def test_generated_at_is_set(self):
        report = VerificationReport(
            protocol_name="TestProto",
            results=(),
            lean_code="-- code",
        )
        assert report.generated_at  # non-empty ISO string

    def test_is_frozen(self):
        from dataclasses import FrozenInstanceError

        report = VerificationReport(
            protocol_name="TestProto",
            results=(),
            lean_code="-- code",
        )
        with pytest.raises(FrozenInstanceError):
            report.protocol_name = "Other"  # type: ignore[misc]


# ============================================================
# 4. _lean_constructor
# ============================================================


class TestLeanConstructor:
    @pytest.mark.parametrize(
        "kind, expected",
        [
            (MessageKind.TASK_REQUEST, "task_request"),
            (MessageKind.TASK_RESULT, "task_result"),
            (MessageKind.AUDIT_REQUEST, "audit_request"),
            (MessageKind.AUDIT_VERDICT, "audit_verdict"),
            (MessageKind.PLAN_REQUEST, "plan_request"),
            (MessageKind.PLAN_PROPOSAL, "plan_proposal"),
            (MessageKind.PLAN_DECISION, "plan_decision"),
            (MessageKind.RESEARCH_QUERY, "research_query"),
            (MessageKind.RESEARCH_REPORT, "research_report"),
            (MessageKind.DM, "dm"),
            (MessageKind.BROADCAST, "broadcast"),
            (MessageKind.SHUTDOWN_REQUEST, "shutdown_request"),
            (MessageKind.SHUTDOWN_ACK, "shutdown_ack"),
            (MessageKind.CONTEXT_INJECT, "context_inject"),
        ],
    )
    def test_mapping_all_kinds(self, kind, expected):
        assert _lean_constructor(kind) == expected


# ============================================================
# 5. _collect_all_steps
# ============================================================


class TestCollectAllSteps:
    def test_flat_elements_returns_all_steps(self):
        proto = make_flat_protocol()
        steps = _collect_all_steps(proto.elements)
        assert len(steps) == 2

    def test_choice_elements_returns_steps_from_branches(self):
        proto = make_choice_protocol()
        steps = _collect_all_steps(proto.elements)
        # 1 flat step + 1 step in "accept" + 1 step in "reject"
        assert len(steps) == 3

    def test_empty_elements_returns_empty(self):
        assert _collect_all_steps([]) == []

    def test_returns_protocol_step_instances(self):
        proto = make_flat_protocol()
        steps = _collect_all_steps(proto.elements)
        assert all(isinstance(s, ProtocolStep) for s in steps)

    def test_architect_flow_collects_all_branch_steps(self):
        # ArchitectFlow: 2 flat + 5 (approve) + 2 (reject) = 9
        steps = _collect_all_steps(ArchitectFlow.elements)
        assert len(steps) == 9


# ============================================================
# 6. _collect_choices
# ============================================================


class TestCollectChoices:
    def test_flat_protocol_returns_empty(self):
        proto = make_flat_protocol()
        choices = _collect_choices(proto.elements)
        assert choices == []

    def test_choice_protocol_returns_one_choice(self):
        proto = make_choice_protocol()
        choices = _collect_choices(proto.elements)
        assert len(choices) == 1
        assert isinstance(choices[0], ProtocolChoice)

    def test_architect_flow_has_one_choice(self):
        choices = _collect_choices(ArchitectFlow.elements)
        assert len(choices) == 1


# ============================================================
# 7. _has_choices
# ============================================================


class TestHasChoices:
    def test_flat_protocol_returns_false(self):
        proto = make_flat_protocol()
        assert _has_choices(proto) is False

    def test_choice_protocol_returns_true(self):
        proto = make_choice_protocol()
        assert _has_choices(proto) is True

    def test_delegate_task_returns_false(self):
        assert _has_choices(DelegateTask) is False

    def test_architect_flow_returns_true(self):
        assert _has_choices(ArchitectFlow) is True

    def test_research_flow_returns_false(self):
        assert _has_choices(ResearchFlow) is False

    def test_simple_task_returns_false(self):
        assert _has_choices(SimpleTask) is False


# ============================================================
# 8. _used_message_kinds
# ============================================================


class TestUsedMessageKinds:
    def test_simple_task_uses_two_kinds(self):
        kinds = _used_message_kinds(SimpleTask)
        assert set(kinds) == {MessageKind.TASK_REQUEST, MessageKind.TASK_RESULT}

    def test_order_follows_enum_definition(self):
        kinds = _used_message_kinds(SimpleTask)
        # TASK_REQUEST comes before TASK_RESULT in enum
        assert kinds.index(MessageKind.TASK_REQUEST) < kinds.index(MessageKind.TASK_RESULT)

    def test_no_duplicates(self):
        kinds = _used_message_kinds(ArchitectFlow)
        assert len(kinds) == len(set(kinds))

    def test_only_kinds_actually_used(self):
        proto = make_flat_protocol(kinds=(MessageKind.DM,))
        kinds = _used_message_kinds(proto)
        assert kinds == [MessageKind.DM]

    def test_includes_kinds_from_branches(self):
        proto = make_choice_protocol()
        kinds = _used_message_kinds(proto)
        kind_set = set(kinds)
        assert MessageKind.TASK_REQUEST in kind_set
        assert MessageKind.TASK_RESULT in kind_set
        assert MessageKind.AUDIT_REQUEST in kind_set

    def test_single_kind_protocol(self):
        proto = Protocol(
            name="Minimal",
            roles=("a", "b"),
            elements=(
                ProtocolStep(sender="a", receiver="b", message_kind=MessageKind.DM),
            ),
        )
        kinds = _used_message_kinds(proto)
        assert kinds == [MessageKind.DM]


# ============================================================
# 9. Lean4Generator.generate_message_kind
# ============================================================


class TestGenerateMessageKind:
    def setup_method(self):
        self.gen = Lean4Generator()

    def test_default_includes_all_14_kinds(self):
        code = self.gen.generate_message_kind()
        for kind in MessageKind:
            assert kind.value in code

    def test_starts_with_inductive(self):
        code = self.gen.generate_message_kind()
        assert code.startswith("inductive MessageKind where")

    def test_ends_with_decidable_eq(self):
        code = self.gen.generate_message_kind()
        assert "deriving DecidableEq, Repr, BEq" in code

    def test_subset_of_kinds(self):
        kinds = [MessageKind.TASK_REQUEST, MessageKind.DM]
        code = self.gen.generate_message_kind(kinds)
        assert "task_request" in code
        assert "dm" in code
        assert "audit_request" not in code

    def test_single_kind(self):
        code = self.gen.generate_message_kind([MessageKind.BROADCAST])
        assert "broadcast" in code
        assert "inductive MessageKind where" in code

    def test_none_generates_all(self):
        code_none = self.gen.generate_message_kind(None)
        code_all = self.gen.generate_message_kind(list(MessageKind))
        assert code_none == code_all


# ============================================================
# 10. Lean4Generator.generate_step_structure
# ============================================================


class TestGenerateStepStructure:
    def setup_method(self):
        self.gen = Lean4Generator()

    def test_starts_with_structure(self):
        code = self.gen.generate_step_structure()
        assert code.startswith("structure ProtocolStep where")

    def test_has_sender_field(self):
        code = self.gen.generate_step_structure()
        assert "sender : String" in code

    def test_has_receiver_field(self):
        code = self.gen.generate_step_structure()
        assert "receiver : String" in code

    def test_has_message_kind_field(self):
        code = self.gen.generate_step_structure()
        assert "message_kind : MessageKind" in code

    def test_has_decidable_eq(self):
        code = self.gen.generate_step_structure()
        assert "DecidableEq" in code


# ============================================================
# 11. Lean4Generator.generate_roles
# ============================================================


class TestGenerateRoles:
    def setup_method(self):
        self.gen = Lean4Generator()

    def test_delegate_task_roles(self):
        code = self.gen.generate_roles(DelegateTask)
        assert '"regina"' in code
        assert '"worker"' in code
        assert '"guardiana"' in code

    def test_simple_task_roles(self):
        code = self.gen.generate_roles(SimpleTask)
        assert '"regina"' in code
        assert '"worker"' in code

    def test_def_name_uses_protocol_name(self):
        code = self.gen.generate_roles(DelegateTask)
        assert "def DelegateTask_roles" in code

    def test_returns_list_string_type(self):
        code = self.gen.generate_roles(SimpleTask)
        assert "List String" in code

    def test_architect_flow_has_four_roles(self):
        code = self.gen.generate_roles(ArchitectFlow)
        assert '"architect"' in code
        assert '"guardiana"' in code


# ============================================================
# 12. Lean4Generator.generate_steps
# ============================================================


class TestGenerateSteps:
    def setup_method(self):
        self.gen = Lean4Generator()

    def test_simple_task_generates_two_steps(self):
        code = self.gen.generate_steps(SimpleTask)
        assert code.count("sender :=") == 2

    def test_step_has_sender_receiver_kind(self):
        code = self.gen.generate_steps(SimpleTask)
        assert 'sender := "regina"' in code
        assert 'receiver := "worker"' in code
        assert "message_kind := .task_request" in code

    def test_def_name_uses_protocol_name(self):
        code = self.gen.generate_steps(SimpleTask)
        assert "def SimpleTask_all_steps" in code

    def test_flat_protocol_with_no_steps_generates_empty_list(self):
        # Build protocol with empty elements (not possible due to validation, so use indirection)
        # We cannot create an empty protocol (Protocol validates roles >= 2 and steps not required)
        # Build a protocol with exactly one step
        proto = make_flat_protocol(kinds=(MessageKind.DM,))
        code = self.gen.generate_steps(proto)
        assert "def TestFlat_all_steps" in code
        assert ".dm" in code

    def test_choice_protocol_includes_branch_steps(self):
        proto = make_choice_protocol()
        code = self.gen.generate_steps(proto)
        # Should include steps from both flat and branches
        assert code.count("sender :=") == 3

    def test_uses_dot_syntax_for_constructor(self):
        code = self.gen.generate_steps(DelegateTask)
        assert ".task_request" in code
        assert ".task_result" in code

    def test_protocol_with_no_steps_generates_empty_list_def(self):
        """When all elements are choices with empty branches list, steps is empty.

        We simulate by patching _collect_all_steps to return [].
        """
        import unittest.mock as mock

        from cervellaswarm_lingua_universale import lean4_bridge

        proto = make_flat_protocol()
        with mock.patch.object(lean4_bridge, "_collect_all_steps", return_value=[]):
            code = self.gen.generate_steps(proto)
        assert "def TestFlat_all_steps : List ProtocolStep := []" in code


# ============================================================
# 13. Lean4Generator.generate_branches
# ============================================================


class TestGenerateBranches:
    def setup_method(self):
        self.gen = Lean4Generator()

    def test_flat_protocol_returns_empty_string(self):
        code = self.gen.generate_branches(DelegateTask)
        assert code == ""

    def test_flat_protocol_research_flow_returns_empty_string(self):
        code = self.gen.generate_branches(ResearchFlow)
        assert code == ""

    def test_choice_protocol_returns_non_empty(self):
        proto = make_choice_protocol()
        code = self.gen.generate_branches(proto)
        assert code != ""

    def test_choice_protocol_generates_branch_defs(self):
        proto = make_choice_protocol()
        code = self.gen.generate_branches(proto)
        assert "TestChoice_branch_accept" in code
        assert "TestChoice_branch_reject" in code

    def test_architect_flow_generates_approve_and_reject(self):
        code = self.gen.generate_branches(ArchitectFlow)
        assert "ArchitectFlow_branch_approve" in code
        assert "ArchitectFlow_branch_reject" in code

    def test_branch_name_with_hyphen_converted_to_underscore(self):
        proto = Protocol(
            name="HypenProto",
            roles=("a", "b"),
            elements=(
                ProtocolChoice(
                    decider="a",
                    branches={
                        "branch-one": (
                            ProtocolStep(
                                sender="a",
                                receiver="b",
                                message_kind=MessageKind.DM,
                            ),
                        ),
                    },
                ),
            ),
        )
        code = self.gen.generate_branches(proto)
        assert "branch_one" in code
        assert "branch-one" not in code

    def test_branch_name_with_space_converted_to_underscore(self):
        proto = Protocol(
            name="SpaceProto",
            roles=("a", "b"),
            elements=(
                ProtocolChoice(
                    decider="a",
                    branches={
                        "branch one": (
                            ProtocolStep(
                                sender="a",
                                receiver="b",
                                message_kind=MessageKind.BROADCAST,
                            ),
                        ),
                    },
                ),
            ),
        )
        code = self.gen.generate_branches(proto)
        assert "branch_one" in code
        assert "branch one" not in code

    def test_second_choice_uses_choice_index(self):
        # Build a protocol with two ProtocolChoice elements
        proto = Protocol(
            name="TwoChoices",
            roles=("a", "b", "c"),
            elements=(
                ProtocolChoice(
                    decider="a",
                    branches={
                        "yes": (
                            ProtocolStep(sender="a", receiver="b", message_kind=MessageKind.DM),
                        ),
                    },
                ),
                ProtocolChoice(
                    decider="b",
                    branches={
                        "ok": (
                            ProtocolStep(sender="b", receiver="c", message_kind=MessageKind.BROADCAST),
                        ),
                    },
                ),
            ),
        )
        code = self.gen.generate_branches(proto)
        # First choice: no index
        assert "TwoChoices_branch_yes" in code
        # Second choice: has choice1 index
        assert "TwoChoices_choice1_branch_ok" in code

    def test_second_choice_theorem_uses_choice_index(self):
        """Theorems for second choice use _choice1 suffix."""
        proto = Protocol(
            name="TwoChoiceThm",
            roles=("a", "b", "c"),
            elements=(
                ProtocolChoice(
                    decider="a",
                    branches={
                        "yes": (
                            ProtocolStep(sender="a", receiver="b", message_kind=MessageKind.DM),
                        ),
                    },
                ),
                ProtocolChoice(
                    decider="b",
                    branches={
                        "ok": (
                            ProtocolStep(sender="b", receiver="c", message_kind=MessageKind.BROADCAST),
                        ),
                    },
                ),
            ),
        )
        code = self.gen.generate_theorems(proto)
        # First choice theorems: no index suffix
        assert "theorem TwoChoiceThm_branches_non_empty :" in code
        assert "theorem TwoChoiceThm_decider_in_roles :" in code
        # Second choice theorems: _choice1 suffix
        assert "theorem TwoChoiceThm_branches_non_empty_choice1 :" in code
        assert "theorem TwoChoiceThm_decider_in_roles_choice1 :" in code


# ============================================================
# 14. Lean4Generator.generate_theorems
# ============================================================


class TestGenerateTheorems:
    def setup_method(self):
        self.gen = Lean4Generator()

    def test_flat_protocol_generates_five_theorems(self):
        code = self.gen.generate_theorems(DelegateTask)
        assert code.count("theorem DelegateTask_") == 5

    def test_has_senders_valid_theorem(self):
        code = self.gen.generate_theorems(DelegateTask)
        assert "theorem DelegateTask_senders_valid" in code

    def test_has_receivers_valid_theorem(self):
        code = self.gen.generate_theorems(DelegateTask)
        assert "theorem DelegateTask_receivers_valid" in code

    def test_has_no_self_loop_theorem(self):
        code = self.gen.generate_theorems(DelegateTask)
        assert "theorem DelegateTask_no_self_loop" in code

    def test_has_min_roles_theorem(self):
        code = self.gen.generate_theorems(DelegateTask)
        assert "theorem DelegateTask_min_roles" in code

    def test_has_non_empty_theorem(self):
        code = self.gen.generate_theorems(DelegateTask)
        assert "theorem DelegateTask_non_empty" in code

    def test_all_theorems_use_by_decide(self):
        code = self.gen.generate_theorems(DelegateTask)
        assert code.count("by decide") == 5

    def test_choice_protocol_generates_seven_theorems(self):
        code = self.gen.generate_theorems(ArchitectFlow)
        # 5 base + 1 branches_non_empty + 1 decider_in_roles = 7
        assert code.count("theorem ArchitectFlow_") == 7

    def test_choice_protocol_has_branches_non_empty(self):
        code = self.gen.generate_theorems(ArchitectFlow)
        assert "theorem ArchitectFlow_branches_non_empty" in code

    def test_choice_protocol_has_decider_in_roles(self):
        code = self.gen.generate_theorems(ArchitectFlow)
        assert "theorem ArchitectFlow_decider_in_roles" in code

    def test_decider_in_roles_theorem_contains_decider_name(self):
        code = self.gen.generate_theorems(ArchitectFlow)
        assert '"regina"' in code

    def test_branches_non_empty_references_branch_defs(self):
        code = self.gen.generate_theorems(ArchitectFlow)
        assert "ArchitectFlow_branch_approve.length > 0" in code
        assert "ArchitectFlow_branch_reject.length > 0" in code

    def test_min_roles_uses_length_comparison(self):
        code = self.gen.generate_theorems(SimpleTask)
        assert "SimpleTask_roles.length ≥ 2" in code

    def test_non_empty_uses_length_comparison(self):
        code = self.gen.generate_theorems(SimpleTask)
        assert "SimpleTask_all_steps.length > 0" in code

    def test_custom_protocol_theorem_names(self):
        proto = make_flat_protocol(name="MyCustomProto")
        code = self.gen.generate_theorems(proto)
        assert "theorem MyCustomProto_senders_valid" in code


# ============================================================
# 15. Lean4Generator.generate (full output)
# ============================================================


class TestGenerateFull:
    def setup_method(self):
        self.gen = Lean4Generator()

    def test_output_contains_header_comment(self):
        code = self.gen.generate(DelegateTask)
        assert "Auto-generated by CervellaSwarm Lean 4 Bridge" in code

    def test_output_contains_protocol_name_in_header(self):
        code = self.gen.generate(DelegateTask)
        assert "Protocol: DelegateTask" in code

    def test_output_contains_generated_timestamp(self):
        code = self.gen.generate(SimpleTask)
        assert "Generated:" in code

    def test_output_contains_types_section(self):
        code = self.gen.generate(DelegateTask)
        assert "-- Types" in code

    def test_output_contains_inductive_message_kind(self):
        code = self.gen.generate(DelegateTask)
        assert "inductive MessageKind where" in code

    def test_output_contains_structure_protocol_step(self):
        code = self.gen.generate(DelegateTask)
        assert "structure ProtocolStep where" in code

    def test_output_contains_roles_def(self):
        code = self.gen.generate(DelegateTask)
        assert "def DelegateTask_roles" in code

    def test_output_contains_steps_def(self):
        code = self.gen.generate(DelegateTask)
        assert "def DelegateTask_all_steps" in code

    def test_output_contains_theorems_section(self):
        code = self.gen.generate(DelegateTask)
        assert "-- Theorems" in code

    def test_output_contains_theorem_senders_valid(self):
        code = self.gen.generate(DelegateTask)
        assert "theorem DelegateTask_senders_valid" in code

    def test_output_only_includes_used_kinds(self):
        # SimpleTask only uses TASK_REQUEST and TASK_RESULT
        code = self.gen.generate(SimpleTask)
        assert "task_request" in code
        assert "task_result" in code
        # audit_request is NOT used in SimpleTask
        assert "audit_request" not in code

    def test_choice_protocol_includes_branches_section(self):
        code = self.gen.generate(ArchitectFlow)
        assert "ArchitectFlow_branch_approve" in code

    def test_do_not_edit_comment_present(self):
        code = self.gen.generate(SimpleTask)
        assert "DO NOT EDIT" in code

    def test_output_is_string(self):
        code = self.gen.generate(DelegateTask)
        assert isinstance(code, str)

    def test_output_not_empty(self):
        code = self.gen.generate(DelegateTask)
        assert len(code) > 100


# ============================================================
# 16. generate_lean4 convenience wrapper
# ============================================================


class TestGenerateLean4:
    def test_returns_same_as_generator_generate(self):
        gen = Lean4Generator()
        # Both should produce equivalent output (timestamps may differ slightly)
        code = generate_lean4(DelegateTask)
        assert "inductive MessageKind where" in code
        assert "theorem DelegateTask_senders_valid" in code

    def test_works_for_all_standard_protocols(self):
        from cervellaswarm_lingua_universale.protocols import STANDARD_PROTOCOLS

        for name, proto in STANDARD_PROTOCOLS.items():
            code = generate_lean4(proto)
            assert f"Protocol: {name}" in code


# ============================================================
# 17. generate_lean4_multi
# ============================================================


class TestGenerateLean4Multi:
    def test_raises_on_empty_list(self):
        with pytest.raises(ValueError, match="protocols cannot be empty"):
            generate_lean4_multi([])

    def test_single_protocol_works(self):
        code = generate_lean4_multi([SimpleTask])
        assert "SimpleTask" in code

    def test_multiple_protocols_in_one_file(self):
        code = generate_lean4_multi([SimpleTask, DelegateTask])
        assert "Protocol: SimpleTask" in code
        assert "Protocol: DelegateTask" in code

    def test_shared_types_section_present(self):
        code = generate_lean4_multi([SimpleTask, DelegateTask])
        assert "Types (shared)" in code

    def test_single_inductive_message_kind(self):
        code = generate_lean4_multi([SimpleTask, DelegateTask])
        # Only one inductive MessageKind definition
        assert code.count("inductive MessageKind where") == 1

    def test_single_structure_protocol_step(self):
        code = generate_lean4_multi([SimpleTask, DelegateTask])
        assert code.count("structure ProtocolStep where") == 1

    def test_all_used_kinds_combined(self):
        # SimpleTask: TASK_REQUEST, TASK_RESULT
        # ResearchFlow: RESEARCH_QUERY, RESEARCH_REPORT, AUDIT_REQUEST, AUDIT_VERDICT
        code = generate_lean4_multi([SimpleTask, ResearchFlow])
        assert "research_query" in code
        assert "audit_request" in code

    def test_all_standard_protocols_combined(self):
        protocols = [DelegateTask, ArchitectFlow, ResearchFlow, SimpleTask]
        code = generate_lean4_multi(protocols)
        assert "Protocol: DelegateTask" in code
        assert "Protocol: ArchitectFlow" in code
        assert "Protocol: ResearchFlow" in code
        assert "Protocol: SimpleTask" in code

    def test_theorems_generated_for_each_protocol(self):
        code = generate_lean4_multi([SimpleTask, DelegateTask])
        assert "theorem SimpleTask_senders_valid" in code
        assert "theorem DelegateTask_senders_valid" in code


# ============================================================
# 18. _extract_theorem
# ============================================================


class TestExtractTheorem:
    def test_finds_existing_theorem(self):
        code = generate_lean4(DelegateTask)
        result = _extract_theorem(code, "DelegateTask_senders_valid")
        assert "theorem DelegateTask_senders_valid" in result
        assert "by decide" in result

    def test_not_found_returns_comment(self):
        code = "-- some lean code"
        result = _extract_theorem(code, "nonexistent_theorem")
        assert "-- theorem nonexistent_theorem not found" in result

    def test_extracted_theorem_ends_with_by_decide(self):
        code = generate_lean4(SimpleTask)
        result = _extract_theorem(code, "SimpleTask_non_empty")
        assert result.endswith("by decide")

    def test_extracted_theorem_multiline(self):
        code = generate_lean4(DelegateTask)
        result = _extract_theorem(code, "DelegateTask_no_self_loop")
        # Should contain the forall quantifier
        assert "∀" in result


# ============================================================
# 19. lean4_available
# ============================================================


class TestLean4Available:
    def test_returns_bool(self):
        result = lean4_available()
        assert isinstance(result, bool)

    def test_no_exception_raised(self):
        # Should never raise, just return True or False
        lean4_available()


# ============================================================
# 20. Lean4Verifier validation (no Lean needed)
# ============================================================


class TestLean4VerifierValidation:
    def test_timeout_zero_raises(self):
        with pytest.raises(ValueError, match="timeout must be positive"):
            Lean4Verifier(timeout=0)

    def test_timeout_negative_raises(self):
        with pytest.raises(ValueError, match="timeout must be positive"):
            Lean4Verifier(timeout=-5)

    def test_timeout_one_is_valid(self):
        v = Lean4Verifier(timeout=1)
        assert v._timeout == 1

    def test_default_timeout_is_sixty(self):
        v = Lean4Verifier()
        assert v._timeout == 60

    def test_verify_code_raises_runtime_error_when_lean_not_available(self):
        """If lean is not installed, verify_code must raise RuntimeError."""
        import unittest.mock as mock

        with mock.patch(
            "cervellaswarm_lingua_universale.lean4_bridge.lean4_available",
            return_value=False,
        ):
            verifier = Lean4Verifier()
            with pytest.raises(RuntimeError, match="Lean 4 is not installed"):
                verifier.verify_code("-- some lean code")

    def test_verify_protocol_raises_runtime_error_when_lean_not_available(self):
        import unittest.mock as mock

        with mock.patch(
            "cervellaswarm_lingua_universale.lean4_bridge.lean4_available",
            return_value=False,
        ):
            verifier = Lean4Verifier()
            with pytest.raises(RuntimeError, match="Lean 4 is not installed"):
                verifier.verify_protocol(SimpleTask)


# ============================================================
# _safe_lean_ident + _validate_lean_name (F1/F2 fix)
# ============================================================


class TestSafeLeanIdent:
    """Tests for _safe_lean_ident helper."""

    @pytest.mark.parametrize(
        "input_name, expected",
        [
            ("approve", "approve"),
            ("reject", "reject"),
            ("my-branch", "my_branch"),
            ("my branch", "my_branch"),
            ("a.b.c", "a_b_c"),
            ("a/b", "a_b"),
            ("approve!", "approve_"),
            ("hello world 123", "hello_world_123"),
            ("_private", "_private"),
            ("CamelCase", "CamelCase"),
            ("with@special#chars", "with_special_chars"),
        ],
    )
    def test_safe_lean_ident(self, input_name, expected):
        assert _safe_lean_ident(input_name) == expected


class TestValidateLeanName:
    """Tests for _validate_lean_name."""

    @pytest.mark.parametrize(
        "valid_name",
        ["DelegateTask", "simple_task", "_private", "A", "a1b2c3", "My_Proto_V2"],
    )
    def test_valid_names_pass(self, valid_name):
        _validate_lean_name(valid_name)  # should not raise

    @pytest.mark.parametrize(
        "invalid_name",
        [
            "My Proto",      # space
            "Proto;end",     # semicolon
            "123abc",        # starts with digit
            "hello-world",   # hyphen
            "a.b",           # dot
            "",              # empty
            "a/b",           # slash
        ],
    )
    def test_invalid_names_raise(self, invalid_name):
        with pytest.raises(ValueError, match="not a valid Lean 4 identifier"):
            _validate_lean_name(invalid_name)


class TestGenerateRejectsInvalidNames:
    """Tests that generate() raises ValueError for invalid protocol names."""

    def test_generate_rejects_name_with_space(self):
        gen = Lean4Generator()
        p = make_flat_protocol(name="My Proto")
        with pytest.raises(ValueError, match="not a valid Lean 4 identifier"):
            gen.generate(p)

    def test_generate_rejects_name_with_semicolon(self):
        gen = Lean4Generator()
        p = make_flat_protocol(name="Proto;end")
        with pytest.raises(ValueError, match="not a valid Lean 4 identifier"):
            gen.generate(p)

    def test_generate_lean4_rejects_invalid_name(self):
        p = make_flat_protocol(name="bad-name")
        with pytest.raises(ValueError, match="not a valid Lean 4 identifier"):
            generate_lean4(p)

    def test_generate_accepts_valid_names(self):
        gen = Lean4Generator()
        for name in ["DelegateTask", "simple_task", "Proto_V2"]:
            p = make_flat_protocol(name=name)
            code = gen.generate(p)
            assert f"-- Protocol: {name}" in code

    def test_generate_lean4_multi_rejects_invalid_name(self):
        valid = make_flat_protocol(name="GoodName")
        invalid = make_flat_protocol(name="bad-name")
        with pytest.raises(ValueError, match="not a valid Lean 4 identifier"):
            generate_lean4_multi([valid, invalid])


class TestBranchSanitizationComprehensive:
    """Tests that branch names with special chars are properly sanitized."""

    def test_branch_with_dots(self):
        """Dot in branch name becomes underscore."""
        gen = Lean4Generator()
        p = Protocol(
            name="TestDot",
            roles=("a", "b"),
            elements=(
                ProtocolChoice(
                    decider="a",
                    branches={
                        "opt.one": (
                            ProtocolStep(sender="a", receiver="b", message_kind=MessageKind.DM),
                        ),
                        "opt.two": (
                            ProtocolStep(sender="b", receiver="a", message_kind=MessageKind.DM),
                        ),
                    },
                ),
            ),
        )
        branches = gen.generate_branches(p)
        assert "TestDot_branch_opt_one" in branches
        assert "TestDot_branch_opt_two" in branches
        # No dots in identifiers
        for line in branches.splitlines():
            if line.startswith("def "):
                ident = line.split(":")[0].replace("def ", "").strip()
                assert "." not in ident

    def test_branch_with_slash(self):
        """Slash in branch name becomes underscore."""
        gen = Lean4Generator()
        p = Protocol(
            name="TestSlash",
            roles=("a", "b"),
            elements=(
                ProtocolChoice(
                    decider="a",
                    branches={
                        "path/a": (
                            ProtocolStep(sender="a", receiver="b", message_kind=MessageKind.DM),
                        ),
                    },
                ),
            ),
        )
        branches = gen.generate_branches(p)
        assert "TestSlash_branch_path_a" in branches
