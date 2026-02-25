"""Tests for standard protocol definitions in cervellaswarm_lingua_universale.protocols.

Covers: DelegateTask, ArchitectFlow, ResearchFlow, SimpleTask fields,
step sequences, branch structure, and STANDARD_PROTOCOLS registry.
"""

from cervellaswarm_lingua_universale.protocols import (
    ArchitectFlow,
    DelegateTask,
    Protocol,
    ProtocolChoice,
    ResearchFlow,
    SimpleTask,
    STANDARD_PROTOCOLS,
)
from cervellaswarm_lingua_universale.types import MessageKind


# ── DelegateTask ──────────────────────────────────────────────────────────────

class TestDelegateTask:
    def test_name(self):
        assert DelegateTask.name == "DelegateTask"

    def test_roles(self):
        assert "regina" in DelegateTask.roles
        assert "worker" in DelegateTask.roles
        assert "guardiana" in DelegateTask.roles

    def test_has_four_steps(self):
        assert len(DelegateTask.elements) == 4

    def test_step_sequence(self):
        steps = DelegateTask.elements
        assert steps[0].message_kind == MessageKind.TASK_REQUEST
        assert steps[1].message_kind == MessageKind.TASK_RESULT
        assert steps[2].message_kind == MessageKind.AUDIT_REQUEST
        assert steps[3].message_kind == MessageKind.AUDIT_VERDICT

    def test_first_step_regina_to_worker(self):
        step = DelegateTask.elements[0]
        assert step.sender == "regina"
        assert step.receiver == "worker"

    def test_second_step_worker_to_regina(self):
        step = DelegateTask.elements[1]
        assert step.sender == "worker"
        assert step.receiver == "regina"

    def test_third_step_regina_to_guardiana(self):
        step = DelegateTask.elements[2]
        assert step.sender == "regina"
        assert step.receiver == "guardiana"

    def test_last_step_guardiana_to_regina(self):
        step = DelegateTask.elements[3]
        assert step.sender == "guardiana"
        assert step.receiver == "regina"


# ── ArchitectFlow ─────────────────────────────────────────────────────────────

class TestArchitectFlow:
    def test_name(self):
        assert ArchitectFlow.name == "ArchitectFlow"

    def test_roles(self):
        assert "regina" in ArchitectFlow.roles
        assert "architect" in ArchitectFlow.roles
        assert "worker" in ArchitectFlow.roles
        assert "guardiana" in ArchitectFlow.roles

    def test_has_three_elements(self):
        # 2 steps + 1 choice
        assert len(ArchitectFlow.elements) == 3

    def test_first_step_plan_request(self):
        step = ArchitectFlow.elements[0]
        assert step.message_kind == MessageKind.PLAN_REQUEST
        assert step.sender == "regina"
        assert step.receiver == "architect"

    def test_second_step_plan_proposal(self):
        step = ArchitectFlow.elements[1]
        assert step.message_kind == MessageKind.PLAN_PROPOSAL
        assert step.sender == "architect"
        assert step.receiver == "regina"

    def test_third_element_is_choice(self):
        elem = ArchitectFlow.elements[2]
        assert isinstance(elem, ProtocolChoice)

    def test_choice_decider_is_regina(self):
        choice = ArchitectFlow.elements[2]
        assert isinstance(choice, ProtocolChoice)
        assert choice.decider == "regina"

    def test_choice_has_approve_and_reject(self):
        choice = ArchitectFlow.elements[2]
        assert isinstance(choice, ProtocolChoice)
        assert "approve" in choice.branches
        assert "reject" in choice.branches

    def test_approve_branch_has_five_steps(self):
        choice = ArchitectFlow.elements[2]
        assert isinstance(choice, ProtocolChoice)
        assert len(choice.branches["approve"]) == 5

    def test_approve_branch_sequence(self):
        choice = ArchitectFlow.elements[2]
        assert isinstance(choice, ProtocolChoice)
        branch = choice.branches["approve"]
        assert branch[0].message_kind == MessageKind.PLAN_DECISION
        assert branch[1].message_kind == MessageKind.TASK_REQUEST
        assert branch[2].message_kind == MessageKind.TASK_RESULT
        assert branch[3].message_kind == MessageKind.AUDIT_REQUEST
        assert branch[4].message_kind == MessageKind.AUDIT_VERDICT

    def test_reject_branch_has_two_steps(self):
        choice = ArchitectFlow.elements[2]
        assert isinstance(choice, ProtocolChoice)
        assert len(choice.branches["reject"]) == 2

    def test_reject_branch_sequence(self):
        choice = ArchitectFlow.elements[2]
        assert isinstance(choice, ProtocolChoice)
        branch = choice.branches["reject"]
        assert branch[0].message_kind == MessageKind.PLAN_DECISION
        assert branch[1].message_kind == MessageKind.PLAN_PROPOSAL

    def test_max_repetitions_single_pass(self):
        assert ArchitectFlow.max_repetitions == 1


# ── ResearchFlow ──────────────────────────────────────────────────────────────

class TestResearchFlow:
    def test_name(self):
        assert ResearchFlow.name == "ResearchFlow"

    def test_roles(self):
        assert "regina" in ResearchFlow.roles
        assert "researcher" in ResearchFlow.roles
        assert "guardiana" in ResearchFlow.roles

    def test_has_four_steps(self):
        assert len(ResearchFlow.elements) == 4

    def test_step_sequence(self):
        steps = ResearchFlow.elements
        assert steps[0].message_kind == MessageKind.RESEARCH_QUERY
        assert steps[1].message_kind == MessageKind.RESEARCH_REPORT
        assert steps[2].message_kind == MessageKind.AUDIT_REQUEST
        assert steps[3].message_kind == MessageKind.AUDIT_VERDICT

    def test_first_step_regina_to_researcher(self):
        step = ResearchFlow.elements[0]
        assert step.sender == "regina"
        assert step.receiver == "researcher"

    def test_second_step_researcher_to_regina(self):
        step = ResearchFlow.elements[1]
        assert step.sender == "researcher"
        assert step.receiver == "regina"


# ── SimpleTask ────────────────────────────────────────────────────────────────

class TestSimpleTask:
    def test_name(self):
        assert SimpleTask.name == "SimpleTask"

    def test_roles(self):
        assert "regina" in SimpleTask.roles
        assert "worker" in SimpleTask.roles

    def test_no_guardiana_in_roles(self):
        assert "guardiana" not in SimpleTask.roles

    def test_has_two_steps(self):
        assert len(SimpleTask.elements) == 2

    def test_step_sequence(self):
        steps = SimpleTask.elements
        assert steps[0].message_kind == MessageKind.TASK_REQUEST
        assert steps[1].message_kind == MessageKind.TASK_RESULT

    def test_first_step_regina_to_worker(self):
        step = SimpleTask.elements[0]
        assert step.sender == "regina"
        assert step.receiver == "worker"


# ── STANDARD_PROTOCOLS registry ───────────────────────────────────────────────

class TestStandardProtocolsRegistry:
    def test_all_four_present(self):
        assert set(STANDARD_PROTOCOLS.keys()) == {
            "DelegateTask",
            "ArchitectFlow",
            "ResearchFlow",
            "SimpleTask",
        }

    def test_values_are_protocol_instances(self):
        for name, proto in STANDARD_PROTOCOLS.items():
            assert isinstance(proto, Protocol), f"{name} is not a Protocol"

    def test_names_match_keys(self):
        for key, proto in STANDARD_PROTOCOLS.items():
            assert proto.name == key, f"Key '{key}' != protocol name '{proto.name}'"

    def test_all_have_at_least_two_roles(self):
        for name, proto in STANDARD_PROTOCOLS.items():
            assert len(proto.roles) >= 2, f"{name} has fewer than 2 roles"
