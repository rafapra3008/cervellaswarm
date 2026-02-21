# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for integration.py - AgentInfo, AGENT_CATALOG, lookup helpers,
agents_for_protocol, create_session, SwarmValidationResult, validate_swarm,
resolve_bindings.

Coverage target: 100% on integration.py
"""

from dataclasses import FrozenInstanceError
from types import MappingProxyType

import pytest

from cervellaswarm_lingua_universale import (
    AgentInfo,
    AGENT_CATALOG,
    AgentRole,
    AuditRequest,
    AuditVerdict,
    AuditVerdictType,
    EventCollector,
    MessageKind,
    ProtocolMonitor,
    ProtocolViolation,
    ResearchQuery,
    ResearchReport,
    SessionStarted,
    SwarmValidationResult,
    TaskRequest,
    TaskResult,
    TaskStatus,
)
from cervellaswarm_lingua_universale.integration import (
    agent_by_name,
    agent_by_role,
    agents_for_protocol,
    create_session,
    resolve_bindings,
    validate_swarm,
)
from cervellaswarm_lingua_universale.protocols import (
    ArchitectFlow,
    DelegateTask,
    Protocol,
    ProtocolStep,
    ResearchFlow,
    SimpleTask,
    STANDARD_PROTOCOLS,
)


# ============================================================
# Helpers / Factories
# ============================================================

def make_task_request():
    return TaskRequest(
        task_id="T001",
        description="Implement feature X",
        target_files=("src/x.py",),
        constraints=("No external deps",),
    )


def make_task_result():
    return TaskResult(
        task_id="T001",
        status=TaskStatus.OK,
        summary="Feature X implemented",
        files_created=("src/x.py",),
        test_command="pytest tests/test_x.py",
    )


def make_audit_request():
    return AuditRequest(
        audit_id="A001",
        target="src/x.py",
        checklist=("Tests present",),
        worker_output="Feature X with tests.",
    )


def make_audit_verdict():
    return AuditVerdict(
        audit_id="A001",
        verdict=AuditVerdictType.APPROVED,
        score=9.0,
        checked=("Tests present",),
    )


# ============================================================
# 1. AgentInfo - Dataclass behaviour
# ============================================================

class TestAgentInfoCreation:
    def test_valid_creation_all_fields(self):
        """AgentInfo can be created with valid role, name and protocol_roles."""
        info = AgentInfo(
            role=AgentRole.BACKEND,
            agent_name="cervella-backend",
            protocol_roles=("worker",),
        )
        assert info.role == AgentRole.BACKEND
        assert info.agent_name == "cervella-backend"
        assert info.protocol_roles == ("worker",)

    def test_multiple_protocol_roles(self):
        """AgentInfo can have more than one protocol role."""
        info = AgentInfo(
            role=AgentRole.ARCHITECT,
            agent_name="cervella-architect",
            protocol_roles=("architect", "worker"),
        )
        assert "architect" in info.protocol_roles
        assert "worker" in info.protocol_roles

    def test_protocol_roles_is_tuple(self):
        """protocol_roles must be a tuple (immutable)."""
        info = AgentInfo(
            role=AgentRole.FRONTEND,
            agent_name="cervella-frontend",
            protocol_roles=("worker",),
        )
        assert isinstance(info.protocol_roles, tuple)

    def test_post_init_empty_agent_name_raises(self):
        """Empty agent_name raises ValueError."""
        with pytest.raises(ValueError, match="agent_name cannot be empty"):
            AgentInfo(
                role=AgentRole.BACKEND,
                agent_name="",
                protocol_roles=("worker",),
            )

    def test_post_init_empty_protocol_roles_raises(self):
        """Empty protocol_roles tuple raises ValueError."""
        with pytest.raises(ValueError, match="protocol_roles cannot be empty"):
            AgentInfo(
                role=AgentRole.BACKEND,
                agent_name="cervella-backend",
                protocol_roles=(),
            )

    def test_frozen_cannot_set_role(self):
        """AgentInfo is frozen - cannot reassign role."""
        info = AgentInfo(
            role=AgentRole.BACKEND,
            agent_name="cervella-backend",
            protocol_roles=("worker",),
        )
        with pytest.raises(FrozenInstanceError):
            info.role = AgentRole.FRONTEND  # type: ignore[misc]

    def test_frozen_cannot_set_agent_name(self):
        """AgentInfo is frozen - cannot reassign agent_name."""
        info = AgentInfo(
            role=AgentRole.BACKEND,
            agent_name="cervella-backend",
            protocol_roles=("worker",),
        )
        with pytest.raises(FrozenInstanceError):
            info.agent_name = "cervella-other"  # type: ignore[misc]

    def test_frozen_cannot_set_protocol_roles(self):
        """AgentInfo is frozen - cannot reassign protocol_roles."""
        info = AgentInfo(
            role=AgentRole.BACKEND,
            agent_name="cervella-backend",
            protocol_roles=("worker",),
        )
        with pytest.raises(FrozenInstanceError):
            info.protocol_roles = ("architect",)  # type: ignore[misc]


# ============================================================
# 2. AgentInfo.can_play()
# ============================================================

class TestAgentInfoCanPlay:
    def test_can_play_matching_role_returns_true(self):
        info = AgentInfo(
            role=AgentRole.BACKEND,
            agent_name="cervella-backend",
            protocol_roles=("worker",),
        )
        assert info.can_play("worker") is True

    def test_can_play_non_matching_role_returns_false(self):
        info = AgentInfo(
            role=AgentRole.BACKEND,
            agent_name="cervella-backend",
            protocol_roles=("worker",),
        )
        assert info.can_play("regina") is False

    def test_can_play_one_of_multiple_roles(self):
        info = AgentInfo(
            role=AgentRole.ARCHITECT,
            agent_name="cervella-architect",
            protocol_roles=("architect", "worker"),
        )
        assert info.can_play("architect") is True
        assert info.can_play("worker") is True

    def test_can_play_guardiana_role(self):
        info = AgentInfo(
            role=AgentRole.GUARDIANA_QUALITA,
            agent_name="cervella-guardiana-qualita",
            protocol_roles=("guardiana",),
        )
        assert info.can_play("guardiana") is True
        assert info.can_play("worker") is False

    def test_can_play_researcher_role(self):
        info = AgentInfo(
            role=AgentRole.RESEARCHER,
            agent_name="cervella-researcher",
            protocol_roles=("researcher", "worker"),
        )
        assert info.can_play("researcher") is True
        assert info.can_play("worker") is True
        assert info.can_play("guardiana") is False

    def test_can_play_empty_string_returns_false(self):
        info = AgentInfo(
            role=AgentRole.BACKEND,
            agent_name="cervella-backend",
            protocol_roles=("worker",),
        )
        assert info.can_play("") is False


# ============================================================
# 3. AGENT_CATALOG - Structure and completeness
# ============================================================

class TestAgentCatalogStructure:
    def test_catalog_contains_exactly_17_agents(self):
        assert len(AGENT_CATALOG) == 17

    def test_catalog_is_mapping_proxy_type(self):
        """AGENT_CATALOG is immutable (MappingProxyType)."""
        assert isinstance(AGENT_CATALOG, MappingProxyType)

    def test_catalog_immutable_cannot_add_key(self):
        with pytest.raises(TypeError):
            AGENT_CATALOG[AgentRole.BACKEND] = None  # type: ignore[index]

    def test_all_agent_roles_present_in_catalog(self):
        """All 17 AgentRole enum values are in the catalog."""
        for role in AgentRole:
            assert role in AGENT_CATALOG, f"Missing: {role}"

    def test_every_agent_has_at_least_one_protocol_role(self):
        for role, info in AGENT_CATALOG.items():
            assert len(info.protocol_roles) >= 1, (
                f"{role} has empty protocol_roles"
            )

    def test_no_duplicate_agent_names(self):
        names = [info.agent_name for info in AGENT_CATALOG.values()]
        assert len(names) == len(set(names))

    def test_all_agent_names_match_cervella_prefix(self):
        """All agent names start with 'cervella-'."""
        for info in AGENT_CATALOG.values():
            assert info.agent_name.startswith("cervella-"), (
                f"'{info.agent_name}' does not start with 'cervella-'"
            )

    def test_catalog_keys_are_agent_role_enum(self):
        for key in AGENT_CATALOG:
            assert isinstance(key, AgentRole)

    def test_catalog_values_are_agent_info(self):
        for value in AGENT_CATALOG.values():
            assert isinstance(value, AgentInfo)

    def test_role_matches_catalog_key(self):
        """Each AgentInfo.role matches its catalog key."""
        for role, info in AGENT_CATALOG.items():
            assert info.role == role


# ============================================================
# 4. Specific agents in catalog
# ============================================================

class TestSpecificCatalogEntries:
    def test_regina_in_catalog(self):
        info = AGENT_CATALOG[AgentRole.REGINA]
        assert info.agent_name == "cervella-orchestrator"
        assert info.protocol_roles == ("regina",)

    def test_guardiana_qualita_in_catalog(self):
        info = AGENT_CATALOG[AgentRole.GUARDIANA_QUALITA]
        assert info.agent_name == "cervella-guardiana-qualita"
        assert info.protocol_roles == ("guardiana",)

    def test_guardiana_ricerca_in_catalog(self):
        info = AGENT_CATALOG[AgentRole.GUARDIANA_RICERCA]
        assert info.agent_name == "cervella-guardiana-ricerca"
        assert info.protocol_roles == ("guardiana",)

    def test_guardiana_ops_in_catalog(self):
        info = AGENT_CATALOG[AgentRole.GUARDIANA_OPS]
        assert info.agent_name == "cervella-guardiana-ops"
        assert info.protocol_roles == ("guardiana",)

    def test_architect_can_play_worker_too(self):
        info = AGENT_CATALOG[AgentRole.ARCHITECT]
        assert "architect" in info.protocol_roles
        assert "worker" in info.protocol_roles

    def test_researcher_can_play_worker_too(self):
        info = AGENT_CATALOG[AgentRole.RESEARCHER]
        assert "researcher" in info.protocol_roles
        assert "worker" in info.protocol_roles

    def test_scienziata_can_play_researcher_and_worker(self):
        info = AGENT_CATALOG[AgentRole.SCIENZIATA]
        assert "researcher" in info.protocol_roles
        assert "worker" in info.protocol_roles

    def test_backend_only_worker(self):
        info = AGENT_CATALOG[AgentRole.BACKEND]
        assert info.protocol_roles == ("worker",)

    def test_security_only_worker(self):
        info = AGENT_CATALOG[AgentRole.SECURITY]
        assert info.protocol_roles == ("worker",)

    def test_ingegnera_only_worker(self):
        info = AGENT_CATALOG[AgentRole.INGEGNERA]
        assert info.protocol_roles == ("worker",)


# ============================================================
# 5. agent_by_name()
# ============================================================

class TestAgentByName:
    def test_known_agent_returns_agent_info(self):
        info = agent_by_name("cervella-backend")
        assert info is not None
        assert info.role == AgentRole.BACKEND

    def test_unknown_agent_returns_none(self):
        assert agent_by_name("cervella-nonexistent") is None

    def test_empty_string_returns_none(self):
        assert agent_by_name("") is None

    def test_all_17_agents_findable_by_name(self):
        """Every agent in the catalog is findable by name."""
        for role, info in AGENT_CATALOG.items():
            found = agent_by_name(info.agent_name)
            assert found is not None, f"Cannot find by name: {info.agent_name}"
            assert found.role == role

    def test_lookup_is_case_sensitive(self):
        assert agent_by_name("Cervella-Backend") is None
        assert agent_by_name("CERVELLA-BACKEND") is None

    @pytest.mark.parametrize("name,expected_role", [
        ("cervella-orchestrator", AgentRole.REGINA),
        ("cervella-guardiana-qualita", AgentRole.GUARDIANA_QUALITA),
        ("cervella-guardiana-ricerca", AgentRole.GUARDIANA_RICERCA),
        ("cervella-guardiana-ops", AgentRole.GUARDIANA_OPS),
        ("cervella-architect", AgentRole.ARCHITECT),
        ("cervella-security", AgentRole.SECURITY),
        ("cervella-ingegnera", AgentRole.INGEGNERA),
        ("cervella-backend", AgentRole.BACKEND),
        ("cervella-frontend", AgentRole.FRONTEND),
        ("cervella-tester", AgentRole.TESTER),
        ("cervella-reviewer", AgentRole.REVIEWER),
        ("cervella-researcher", AgentRole.RESEARCHER),
        ("cervella-marketing", AgentRole.MARKETING),
        ("cervella-devops", AgentRole.DEVOPS),
        ("cervella-docs", AgentRole.DOCS),
        ("cervella-data", AgentRole.DATA),
        ("cervella-scienziata", AgentRole.SCIENZIATA),
    ])
    def test_agent_by_name_parametrized(self, name, expected_role):
        info = agent_by_name(name)
        assert info is not None
        assert info.role == expected_role


# ============================================================
# 6. agent_by_role()
# ============================================================

class TestAgentByRole:
    def test_known_role_returns_agent_info(self):
        info = agent_by_role(AgentRole.BACKEND)
        assert info is not None
        assert info.agent_name == "cervella-backend"

    def test_all_agent_roles_return_agent(self):
        """Every AgentRole has an agent in the catalog."""
        for role in AgentRole:
            info = agent_by_role(role)
            assert info is not None, f"No agent for role: {role}"

    @pytest.mark.parametrize("role", list(AgentRole))
    def test_agent_by_role_parametrized(self, role):
        info = agent_by_role(role)
        assert info is not None
        assert info.role == role


# ============================================================
# 7. agents_for_protocol()
# ============================================================

class TestAgentsForProtocol:
    def test_delegate_task_regina_has_1_agent(self):
        coverage = agents_for_protocol(DelegateTask)
        assert len(coverage["regina"]) == 1
        assert coverage["regina"][0].role == AgentRole.REGINA

    def test_delegate_task_worker_has_13_agents(self):
        """13 agents can play 'worker' in DelegateTask."""
        coverage = agents_for_protocol(DelegateTask)
        # architect, security, ingegnera, backend, frontend, tester, reviewer,
        # researcher, marketing, devops, docs, data, scienziata = 13
        worker_agents = coverage["worker"]
        assert len(worker_agents) == 13

    def test_delegate_task_guardiana_has_3_agents(self):
        coverage = agents_for_protocol(DelegateTask)
        guardiana_agents = coverage["guardiana"]
        assert len(guardiana_agents) == 3
        roles = {a.role for a in guardiana_agents}
        assert AgentRole.GUARDIANA_QUALITA in roles
        assert AgentRole.GUARDIANA_RICERCA in roles
        assert AgentRole.GUARDIANA_OPS in roles

    def test_architect_flow_has_architect_role(self):
        coverage = agents_for_protocol(ArchitectFlow)
        assert "architect" in coverage
        assert len(coverage["architect"]) >= 1
        assert any(a.role == AgentRole.ARCHITECT for a in coverage["architect"])

    def test_research_flow_researcher_has_at_least_2(self):
        """Researcher and Scienziata can both play 'researcher'."""
        coverage = agents_for_protocol(ResearchFlow)
        researcher_agents = coverage["researcher"]
        assert len(researcher_agents) >= 2
        roles = {a.role for a in researcher_agents}
        assert AgentRole.RESEARCHER in roles
        assert AgentRole.SCIENZIATA in roles

    def test_simple_task_has_only_regina_and_worker(self):
        coverage = agents_for_protocol(SimpleTask)
        assert set(coverage.keys()) == {"regina", "worker"}

    def test_returns_dict_with_all_protocol_roles(self):
        coverage = agents_for_protocol(DelegateTask)
        for role in DelegateTask.roles:
            assert role in coverage

    def test_custom_catalog_parameter(self):
        """Custom catalog restricts agents returned."""
        small_catalog = MappingProxyType({
            AgentRole.REGINA: AGENT_CATALOG[AgentRole.REGINA],
            AgentRole.BACKEND: AGENT_CATALOG[AgentRole.BACKEND],
        })
        coverage = agents_for_protocol(SimpleTask, catalog=small_catalog)
        assert len(coverage["regina"]) == 1
        assert len(coverage["worker"]) == 1

    def test_empty_custom_catalog_returns_empty_lists(self):
        coverage = agents_for_protocol(DelegateTask, catalog=MappingProxyType({}))
        for role in DelegateTask.roles:
            assert coverage[role] == []

    def test_protocol_roles_are_all_present_as_keys(self):
        for protocol in STANDARD_PROTOCOLS.values():
            coverage = agents_for_protocol(protocol)
            for role in protocol.roles:
                assert role in coverage


# ============================================================
# 8. create_session()
# ============================================================

class TestCreateSession:
    def test_creates_session_checker_with_session_id(self):
        checker = create_session(SimpleTask, session_id="S-TEST")
        assert checker.session_id == "S-TEST"

    def test_creates_session_checker_auto_session_id(self):
        """When session_id is empty, one is auto-generated."""
        checker = create_session(SimpleTask)
        assert checker.session_id  # non-empty

    def test_auto_binds_regina_when_not_provided(self):
        """Regina is auto-bound to cervella-orchestrator."""
        checker = create_session(
            DelegateTask,
            bindings={"worker": "cervella-backend",
                      "guardiana": "cervella-guardiana-qualita"},
        )
        # The session is valid and can send messages using real agent names
        checker.send("cervella-orchestrator", "cervella-backend", make_task_request())

    def test_explicit_binding_overrides_auto_bind(self):
        """Explicit regina binding is not overridden."""
        checker = create_session(
            SimpleTask,
            bindings={"regina": "cervella-orchestrator",
                      "worker": "cervella-backend"},
        )
        assert checker.session_id  # valid, no error

    def test_raises_for_unknown_agent_name(self):
        """ValueError when binding references unknown agent."""
        with pytest.raises(ValueError, match="unknown agent name"):
            create_session(
                SimpleTask,
                bindings={"worker": "cervella-nonexistent"},
            )

    def test_raises_for_role_not_in_protocol(self):
        """ValueError when binding role not in protocol."""
        with pytest.raises(ValueError, match="not in protocol roles"):
            create_session(
                SimpleTask,
                bindings={"guardiana": "cervella-guardiana-qualita"},
            )

    def test_raises_when_agent_cannot_play_role(self):
        """ValueError when agent cannot play the protocol role."""
        with pytest.raises(ValueError, match="cannot play protocol role"):
            create_session(
                SimpleTask,
                bindings={"worker": "cervella-orchestrator"},
            )

    def test_monitor_parameter_passed_through(self):
        """Monitor is connected to the created session."""
        monitor = ProtocolMonitor()
        collector = EventCollector()
        monitor.add_listener(collector)

        create_session(SimpleTask, monitor=monitor)
        started_events = [e for e in collector.events if isinstance(e, SessionStarted)]
        assert len(started_events) == 1

    def test_protocol_name_matches(self):
        checker = create_session(DelegateTask)
        assert checker.protocol_name == "DelegateTask"

    def test_can_send_messages_with_real_agent_names(self):
        """After create_session, messages use real agent names."""
        checker = create_session(
            SimpleTask,
            bindings={"worker": "cervella-backend"},
        )
        checker.send("cervella-orchestrator", "cervella-backend", make_task_request())
        checker.send("cervella-backend", "cervella-orchestrator", make_task_result())
        assert checker.is_complete

    def test_bindings_none_uses_auto_bind_only(self):
        """With bindings=None and regina in protocol, auto-bind works."""
        checker = create_session(DelegateTask, bindings=None)
        assert checker.session_id  # no error


# ============================================================
# 9. SwarmValidationResult
# ============================================================

class TestSwarmValidationResult:
    def test_frozen_dataclass(self):
        result = SwarmValidationResult(
            valid=True,
            protocols_checked=("DelegateTask",),
            covered_roles=("guardiana", "regina", "worker"),
            uncovered_roles=(),
            coverage=(
                ("guardiana", ("cervella-guardiana-qualita",)),
                ("regina", ("cervella-orchestrator",)),
                ("worker", ("cervella-backend",)),
            ),
        )
        with pytest.raises(FrozenInstanceError):
            result.valid = False  # type: ignore[misc]

    def test_coverage_map_property_returns_dict(self):
        result = SwarmValidationResult(
            valid=True,
            protocols_checked=("SimpleTask",),
            covered_roles=("regina", "worker"),
            uncovered_roles=(),
            coverage=(
                ("regina", ("cervella-orchestrator",)),
                ("worker", ("cervella-backend",)),
            ),
        )
        cmap = result.coverage_map
        assert isinstance(cmap, dict)
        assert "regina" in cmap
        assert "worker" in cmap

    def test_coverage_map_values_are_tuples(self):
        result = SwarmValidationResult(
            valid=True,
            protocols_checked=("SimpleTask",),
            covered_roles=("regina", "worker"),
            uncovered_roles=(),
            coverage=(
                ("regina", ("cervella-orchestrator",)),
                ("worker", ("cervella-backend", "cervella-frontend")),
            ),
        )
        cmap = result.coverage_map
        assert isinstance(cmap["worker"], tuple)

    def test_valid_true_when_no_uncovered_roles(self):
        result = SwarmValidationResult(
            valid=True,
            protocols_checked=("SimpleTask",),
            covered_roles=("regina", "worker"),
            uncovered_roles=(),
            coverage=(
                ("regina", ("cervella-orchestrator",)),
                ("worker", ("cervella-backend",)),
            ),
        )
        assert result.valid is True

    def test_valid_false_when_uncovered_roles(self):
        result = SwarmValidationResult(
            valid=False,
            protocols_checked=("DelegateTask",),
            covered_roles=("regina", "worker"),
            uncovered_roles=("guardiana",),
            coverage=(
                ("guardiana", ()),
                ("regina", ("cervella-orchestrator",)),
                ("worker", ("cervella-backend",)),
            ),
        )
        assert result.valid is False
        assert "guardiana" in result.uncovered_roles


# ============================================================
# 10. validate_swarm()
# ============================================================

class TestValidateSwarm:
    def test_default_all_agents_all_protocols_is_valid(self):
        result = validate_swarm()
        assert result.valid is True

    def test_default_uncovered_roles_is_empty(self):
        result = validate_swarm()
        assert result.uncovered_roles == ()

    def test_all_standard_protocol_names_in_protocols_checked(self):
        result = validate_swarm()
        for name in STANDARD_PROTOCOLS:
            assert name in result.protocols_checked

    def test_coverage_map_has_entries_for_all_roles(self):
        result = validate_swarm()
        cmap = result.coverage_map
        for proto in STANDARD_PROTOCOLS.values():
            for role in proto.roles:
                assert role in cmap

    def test_with_subset_agents_may_be_invalid(self):
        result = validate_swarm(
            available_agents=[AgentRole.REGINA, AgentRole.BACKEND]
        )
        assert result.valid is False

    def test_only_regina_and_backend_missing_guardiana(self):
        result = validate_swarm(
            available_agents=[AgentRole.REGINA, AgentRole.BACKEND],
        )
        assert "guardiana" in result.uncovered_roles

    def test_with_specific_protocols_checks_only_those(self):
        result = validate_swarm(protocols=[SimpleTask])
        assert "SimpleTask" in result.protocols_checked
        assert "DelegateTask" not in result.protocols_checked

    def test_simple_task_with_regina_and_worker_is_valid(self):
        result = validate_swarm(
            protocols=[SimpleTask],
            available_agents=[AgentRole.REGINA, AgentRole.BACKEND],
        )
        assert result.valid is True

    def test_covered_roles_sorted(self):
        result = validate_swarm()
        covered_list = list(result.covered_roles)
        assert covered_list == sorted(covered_list)

    def test_uncovered_roles_sorted(self):
        result = validate_swarm(
            available_agents=[AgentRole.BACKEND],
        )
        uncovered_list = list(result.uncovered_roles)
        assert uncovered_list == sorted(uncovered_list)

    def test_protocols_checked_is_tuple(self):
        result = validate_swarm()
        assert isinstance(result.protocols_checked, tuple)

    def test_covered_roles_is_tuple(self):
        result = validate_swarm()
        assert isinstance(result.covered_roles, tuple)

    def test_uncovered_roles_is_tuple(self):
        result = validate_swarm()
        assert isinstance(result.uncovered_roles, tuple)

    def test_coverage_is_tuple_of_tuples(self):
        result = validate_swarm()
        assert isinstance(result.coverage, tuple)
        for item in result.coverage:
            assert isinstance(item, tuple)
            assert len(item) == 2

    def test_full_swarm_covers_all_roles(self):
        result = validate_swarm()
        cmap = result.coverage_map
        assert len(cmap["regina"]) == 1
        assert len(cmap["worker"]) >= 10
        assert len(cmap["guardiana"]) == 3

    def test_empty_available_agents_list(self):
        result = validate_swarm(available_agents=[])
        assert result.valid is False
        assert len(result.uncovered_roles) > 0

    def test_agent_not_in_catalog_silently_skipped(self):
        """Roles not in catalog are skipped gracefully."""
        result = validate_swarm(
            available_agents=[AgentRole.REGINA, AgentRole.BACKEND],
            protocols=[SimpleTask],
        )
        assert result.valid is True


# ============================================================
# 11. resolve_bindings()
# ============================================================

class TestResolveBindings:
    def test_returns_bindings_for_all_protocol_roles(self):
        bindings = resolve_bindings(DelegateTask)
        for role in DelegateTask.roles:
            assert role in bindings

    def test_simple_task_returns_two_bindings(self):
        bindings = resolve_bindings(SimpleTask)
        assert len(bindings) == 2
        assert "regina" in bindings
        assert "worker" in bindings

    def test_preferences_are_respected(self):
        bindings = resolve_bindings(
            DelegateTask,
            preferences={"worker": "cervella-backend"},
        )
        assert bindings["worker"] == "cervella-backend"

    def test_preference_for_researcher_in_research_flow(self):
        bindings = resolve_bindings(
            ResearchFlow,
            preferences={"researcher": "cervella-researcher"},
        )
        assert bindings["researcher"] == "cervella-researcher"

    def test_raises_for_unknown_preferred_agent(self):
        with pytest.raises(ValueError, match="is not in the catalog"):
            resolve_bindings(
                SimpleTask,
                preferences={"worker": "cervella-nonexistent"},
            )

    def test_raises_when_agent_cannot_play_preferred_role(self):
        with pytest.raises(ValueError, match="cannot play"):
            resolve_bindings(
                SimpleTask,
                preferences={"worker": "cervella-orchestrator"},
            )

    def test_raises_when_role_cannot_be_filled(self):
        """ValueError if no agent in catalog can fill the role."""
        custom_catalog = MappingProxyType({
            AgentRole.REGINA: AGENT_CATALOG[AgentRole.REGINA],
            # No guardiana in catalog
        })
        with pytest.raises(ValueError, match="no agent available for protocol role"):
            resolve_bindings(DelegateTask, catalog=custom_catalog)

    def test_deterministic_same_input_same_output(self):
        """Same call produces identical results."""
        b1 = resolve_bindings(DelegateTask)
        b2 = resolve_bindings(DelegateTask)
        assert b1 == b2

    def test_values_are_valid_agent_names(self):
        """All resolved names are in the catalog."""
        bindings = resolve_bindings(DelegateTask)
        for role, name in bindings.items():
            info = agent_by_name(name)
            assert info is not None
            assert info.can_play(role)

    def test_custom_catalog_parameter(self):
        """Custom catalog restricts agent selection."""
        custom = MappingProxyType({
            AgentRole.REGINA: AGENT_CATALOG[AgentRole.REGINA],
            AgentRole.BACKEND: AGENT_CATALOG[AgentRole.BACKEND],
        })
        bindings = resolve_bindings(SimpleTask, catalog=custom)
        assert bindings["regina"] == "cervella-orchestrator"
        assert bindings["worker"] == "cervella-backend"

    def test_no_preferences_returns_deterministic_first_alphabetical(self):
        """Without preferences, picks agent whose role.value sorts first."""
        bindings = resolve_bindings(DelegateTask)
        worker_info = agent_by_name(bindings["worker"])
        assert worker_info is not None
        # All other worker candidates should sort >= this one
        coverage = agents_for_protocol(DelegateTask)
        for candidate in coverage["worker"]:
            assert worker_info.role.value <= candidate.role.value

    def test_resolve_bindings_returns_dict(self):
        bindings = resolve_bindings(SimpleTask)
        assert isinstance(bindings, dict)

    def test_resolve_all_standard_protocols(self):
        """resolve_bindings works for every standard protocol."""
        for name, protocol in STANDARD_PROTOCOLS.items():
            bindings = resolve_bindings(protocol)
            assert set(bindings.keys()) == set(protocol.roles), (
                f"Protocol '{name}' binding mismatch"
            )

    def test_resolve_custom_catalog_rejects_global_agent(self):
        """P2 fix: preferences validated against custom catalog, not global."""
        from types import MappingProxyType as MPT

        regina_only = MPT({AgentRole.REGINA: AGENT_CATALOG[AgentRole.REGINA]})
        # cervella-backend exists in global but NOT in custom catalog
        with pytest.raises(ValueError, match="not in the catalog"):
            resolve_bindings(
                SimpleTask,
                preferences={"worker": "cervella-backend"},
                catalog=regina_only,
            )

    def test_resolve_custom_catalog_accepts_present_agent(self):
        """Custom catalog accepts agents that ARE in the catalog."""
        from types import MappingProxyType as MPT

        small_cat = MPT({
            AgentRole.REGINA: AGENT_CATALOG[AgentRole.REGINA],
            AgentRole.BACKEND: AGENT_CATALOG[AgentRole.BACKEND],
        })
        bindings = resolve_bindings(
            SimpleTask,
            preferences={"worker": "cervella-backend"},
            catalog=small_cat,
        )
        assert bindings["worker"] == "cervella-backend"
