"""Tests for enums and message_kind helper in cervellaswarm_lingua_universale.types.

Covers: AgentRole.tier, AgentRole.model, MessageKind completeness,
message_kind() helper for all message types.
"""

from cervellaswarm_lingua_universale.types import (
    AgentRole,
    MessageKind,
    message_kind,
)


# ── AgentRole tier ────────────────────────────────────────────────────────────

class TestAgentRoleTier:
    def test_regina_is_hub_tier(self):
        assert AgentRole.REGINA.tier == "hub"

    def test_guardiane_are_guardiana_tier(self):
        for role in (
            AgentRole.GUARDIANA_QUALITA,
            AgentRole.GUARDIANA_RICERCA,
            AgentRole.GUARDIANA_OPS,
        ):
            assert role.tier == "guardiana", f"{role} should be guardiana tier"

    def test_strategic_roles(self):
        for role in (AgentRole.ARCHITECT, AgentRole.SECURITY, AgentRole.INGEGNERA):
            assert role.tier == "strategic", f"{role} should be strategic tier"

    def test_workers_are_worker_tier(self):
        worker_roles = (
            AgentRole.BACKEND,
            AgentRole.FRONTEND,
            AgentRole.TESTER,
            AgentRole.REVIEWER,
            AgentRole.RESEARCHER,
            AgentRole.MARKETING,
            AgentRole.DEVOPS,
            AgentRole.DOCS,
            AgentRole.DATA,
            AgentRole.SCIENZIATA,
        )
        for role in worker_roles:
            assert role.tier == "worker", f"{role} should be worker tier"


# ── AgentRole model ───────────────────────────────────────────────────────────

class TestAgentRoleModel:
    def test_opus_roles(self):
        opus_roles = (
            AgentRole.REGINA,
            AgentRole.GUARDIANA_QUALITA,
            AgentRole.GUARDIANA_RICERCA,
            AgentRole.GUARDIANA_OPS,
            AgentRole.ARCHITECT,
            AgentRole.SECURITY,
            AgentRole.INGEGNERA,
        )
        for role in opus_roles:
            assert role.model == "opus", f"{role} should use opus model"

    def test_sonnet_roles(self):
        sonnet_roles = (
            AgentRole.BACKEND,
            AgentRole.FRONTEND,
            AgentRole.TESTER,
            AgentRole.REVIEWER,
            AgentRole.RESEARCHER,
            AgentRole.MARKETING,
            AgentRole.DEVOPS,
            AgentRole.DOCS,
            AgentRole.DATA,
            AgentRole.SCIENZIATA,
        )
        for role in sonnet_roles:
            assert role.model == "sonnet", f"{role} should use sonnet model"

    def test_tier_model_consistency(self):
        """Every role's model must be consistent with its tier."""
        for role in AgentRole:
            if role.tier in ("hub", "guardiana", "strategic"):
                assert role.model == "opus"
            else:
                assert role.model == "sonnet"


# ── MessageKind completeness ──────────────────────────────────────────────────

class TestMessageKind:
    def test_all_expected_kinds_exist(self):
        expected = {
            "TASK_REQUEST", "TASK_RESULT",
            "AUDIT_REQUEST", "AUDIT_VERDICT",
            "PLAN_REQUEST", "PLAN_PROPOSAL", "PLAN_DECISION",
            "RESEARCH_QUERY", "RESEARCH_REPORT",
            "DM", "BROADCAST",
            "SHUTDOWN_REQUEST", "SHUTDOWN_ACK",
            "CONTEXT_INJECT",
        }
        actual = {m.name for m in MessageKind}
        assert expected.issubset(actual), f"Missing kinds: {expected - actual}"

    def test_enum_values_are_snake_case_strings(self):
        for kind in MessageKind:
            assert kind.value == kind.value.lower()
            assert " " not in kind.value

    def test_message_kind_helper(self, task_request, task_result_ok):
        assert message_kind(task_request) == MessageKind.TASK_REQUEST
        assert message_kind(task_result_ok) == MessageKind.TASK_RESULT

    def test_message_kind_helper_all_types(
        self,
        task_request,
        task_result_ok,
        audit_request,
        audit_verdict_approved,
        plan_request,
        plan_proposal,
        plan_decision_approved,
        research_query,
        research_report,
    ):
        mapping = {
            task_request: MessageKind.TASK_REQUEST,
            task_result_ok: MessageKind.TASK_RESULT,
            audit_request: MessageKind.AUDIT_REQUEST,
            audit_verdict_approved: MessageKind.AUDIT_VERDICT,
            plan_request: MessageKind.PLAN_REQUEST,
            plan_proposal: MessageKind.PLAN_PROPOSAL,
            plan_decision_approved: MessageKind.PLAN_DECISION,
            research_query: MessageKind.RESEARCH_QUERY,
            research_report: MessageKind.RESEARCH_REPORT,
        }
        for msg, expected_kind in mapping.items():
            assert message_kind(msg) == expected_kind
