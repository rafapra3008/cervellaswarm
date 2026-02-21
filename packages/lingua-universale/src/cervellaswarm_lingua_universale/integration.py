# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Integration of Lingua Universale with real CervellaSwarm agents.

This is the BRIDGE between theory and practice.

The other 6 modules define WHAT protocols look like (types, protocols),
HOW to check them (checker), HOW to describe them (dsl), HOW to observe
them (monitor), and HOW to prove them (lean4_bridge).

This module answers: WHO are the real agents, and how do they map to
protocol roles?

It is the first time ANYONE maps session types to real AI agents.

Usage::

    from cervellaswarm_lingua_universale import (
        DelegateTask,
        create_session,
        agents_for_protocol,
        validate_swarm,
    )

    # Which agents can participate in DelegateTask?
    coverage = agents_for_protocol(DelegateTask)
    # {'regina': [AgentInfo(REGINA, ...)],
    #  'worker': [AgentInfo(BACKEND, ...), AgentInfo(FRONTEND, ...), ...],
    #  'guardiana': [AgentInfo(GUARDIANA_QUALITA, ...), ...]}

    # Create a session with real agent bindings
    checker = create_session(
        DelegateTask,
        bindings={"worker": "cervella-backend",
                  "guardiana": "cervella-guardiana-qualita"},
    )
    # Now send messages using real agent names:
    checker.send("regina", "cervella-backend", task_request)

    # Validate swarm completeness
    result = validate_swarm()
    assert result.valid  # All standard protocols are covered
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping, Optional, Sequence

from .checker import SessionChecker
from .monitor import ProtocolMonitor
from .protocols import STANDARD_PROTOCOLS, Protocol
from .types import AgentRole


# ============================================================
# Agent metadata
# ============================================================


@dataclass(frozen=True)
class AgentInfo:
    """Metadata about a real CervellaSwarm agent.

    Each agent has exactly one AgentRole (from types.py) and can play
    one or more protocol roles in different protocols.

    The agent_name is the real identifier used in Claude Code
    (e.g., "cervella-backend"), matching the filename in
    ``~/.claude/agents/cervella-backend.md``.
    """

    role: AgentRole
    agent_name: str
    protocol_roles: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.agent_name:
            raise ValueError("agent_name cannot be empty")
        if not self.protocol_roles:
            raise ValueError("protocol_roles cannot be empty")

    def can_play(self, protocol_role: str) -> bool:
        """Check if this agent can fill a given protocol role."""
        return protocol_role in self.protocol_roles


# ============================================================
# Agent Catalog - The 17 agents of CervellaSwarm
# ============================================================

# Protocol role mapping rationale:
#
# "regina"     - Only the Regina (orchestrator) can play this role.
# "guardiana"  - Any of the 3 Guardiane can play this role, each
#                specializing in different audit types.
# "architect"  - Only the Architect can plan complex implementations.
# "researcher" - Researcher and Scienziata produce research reports.
# "worker"     - All worker-tier agents can execute tasks. Strategic
#                agents (security, ingegnera) can also act as workers
#                for tasks in their domain.

_CATALOG_DATA: tuple[AgentInfo, ...] = (
    # Hub
    AgentInfo(
        role=AgentRole.REGINA,
        agent_name="cervella-orchestrator",
        protocol_roles=("regina",),
    ),
    # Guardiane (opus)
    AgentInfo(
        role=AgentRole.GUARDIANA_QUALITA,
        agent_name="cervella-guardiana-qualita",
        protocol_roles=("guardiana",),
    ),
    AgentInfo(
        role=AgentRole.GUARDIANA_RICERCA,
        agent_name="cervella-guardiana-ricerca",
        protocol_roles=("guardiana",),
    ),
    AgentInfo(
        role=AgentRole.GUARDIANA_OPS,
        agent_name="cervella-guardiana-ops",
        protocol_roles=("guardiana",),
    ),
    # Strategic (opus)
    AgentInfo(
        role=AgentRole.ARCHITECT,
        agent_name="cervella-architect",
        protocol_roles=("architect", "worker"),
    ),
    AgentInfo(
        role=AgentRole.SECURITY,
        agent_name="cervella-security",
        protocol_roles=("worker",),
    ),
    AgentInfo(
        role=AgentRole.INGEGNERA,
        agent_name="cervella-ingegnera",
        protocol_roles=("worker",),
    ),
    # Workers (sonnet)
    AgentInfo(
        role=AgentRole.BACKEND,
        agent_name="cervella-backend",
        protocol_roles=("worker",),
    ),
    AgentInfo(
        role=AgentRole.FRONTEND,
        agent_name="cervella-frontend",
        protocol_roles=("worker",),
    ),
    AgentInfo(
        role=AgentRole.TESTER,
        agent_name="cervella-tester",
        protocol_roles=("worker",),
    ),
    AgentInfo(
        role=AgentRole.REVIEWER,
        agent_name="cervella-reviewer",
        protocol_roles=("worker",),
    ),
    AgentInfo(
        role=AgentRole.RESEARCHER,
        agent_name="cervella-researcher",
        protocol_roles=("researcher", "worker"),
    ),
    AgentInfo(
        role=AgentRole.MARKETING,
        agent_name="cervella-marketing",
        protocol_roles=("worker",),
    ),
    AgentInfo(
        role=AgentRole.DEVOPS,
        agent_name="cervella-devops",
        protocol_roles=("worker",),
    ),
    AgentInfo(
        role=AgentRole.DOCS,
        agent_name="cervella-docs",
        protocol_roles=("worker",),
    ),
    AgentInfo(
        role=AgentRole.DATA,
        agent_name="cervella-data",
        protocol_roles=("worker",),
    ),
    AgentInfo(
        role=AgentRole.SCIENZIATA,
        agent_name="cervella-scienziata",
        protocol_roles=("researcher", "worker"),
    ),
)

AGENT_CATALOG: Mapping[AgentRole, AgentInfo] = MappingProxyType(
    {info.role: info for info in _CATALOG_DATA}
)
"""Immutable registry of all 17 CervellaSwarm agents.

Keyed by AgentRole for O(1) lookup. Use ``agent_by_name()`` to
look up by agent_name string.
"""


# ============================================================
# Lookup helpers
# ============================================================

# Pre-computed reverse index: agent_name -> AgentInfo (O(1) lookup)
_NAME_TO_AGENT: Mapping[str, AgentInfo] = MappingProxyType(
    {info.agent_name: info for info in _CATALOG_DATA}
)


def agent_by_name(name: str) -> Optional[AgentInfo]:
    """Look up an agent by its real name (e.g., "cervella-backend").

    Returns None if the name is not in the catalog.
    """
    return _NAME_TO_AGENT.get(name)


def agent_by_role(role: AgentRole) -> Optional[AgentInfo]:
    """Look up an agent by its AgentRole enum value.

    Returns None if the role is not in the catalog.
    """
    return AGENT_CATALOG.get(role)


# ============================================================
# Protocol-Agent mapping
# ============================================================


def agents_for_protocol(
    protocol: Protocol,
    catalog: Optional[Mapping[AgentRole, AgentInfo]] = None,
) -> dict[str, list[AgentInfo]]:
    """Find which real agents can fill each role in a protocol.

    Returns a dict mapping protocol role names to lists of AgentInfo
    objects that can play that role.

    Example::

        coverage = agents_for_protocol(DelegateTask)
        # coverage["worker"] -> [AgentInfo(BACKEND), AgentInfo(FRONTEND), ...]
        # coverage["guardiana"] -> [AgentInfo(GUARDIANA_QUALITA), ...]
    """
    cat = catalog if catalog is not None else AGENT_CATALOG
    result: dict[str, list[AgentInfo]] = {role: [] for role in protocol.roles}
    for info in cat.values():
        for proto_role in info.protocol_roles:
            if proto_role in result:
                result[proto_role].append(info)
    return result


# ============================================================
# Session factory
# ============================================================


def create_session(
    protocol: Protocol,
    bindings: Optional[dict[str, str]] = None,
    session_id: str = "",
    monitor: Optional[ProtocolMonitor] = None,
) -> SessionChecker:
    """Create a SessionChecker with real agent name bindings.

    The ``bindings`` dict maps protocol roles to real agent names.
    The "regina" role is automatically bound to "cervella-orchestrator"
    if not explicitly provided.

    Example::

        checker = create_session(
            DelegateTask,
            bindings={
                "worker": "cervella-backend",
                "guardiana": "cervella-guardiana-qualita",
            },
        )
        # Now use real agent names in send():
        checker.send("cervella-orchestrator", "cervella-backend", msg)

    Raises ValueError if a binding references an unknown agent name
    or if a binding role is not in the protocol.
    """
    bindings = bindings or {}
    # Auto-bind regina if not provided
    if "regina" in protocol.roles and "regina" not in bindings:
        bindings = {**bindings, "regina": "cervella-orchestrator"}

    # Validate binding roles exist in protocol
    for role in bindings:
        if role not in protocol.roles:
            raise ValueError(
                f"binding role '{role}' not in protocol roles "
                f"{protocol.roles}"
            )

    # Validate binding agent names exist in catalog
    for role, agent_name in bindings.items():
        info = agent_by_name(agent_name)
        if info is None:
            raise ValueError(
                f"unknown agent name '{agent_name}' for role '{role}'. "
                f"Known agents: {sorted(_NAME_TO_AGENT.keys())}"
            )
        if not info.can_play(role):
            raise ValueError(
                f"agent '{agent_name}' (role={info.role.value}) cannot play "
                f"protocol role '{role}'. "
                f"It can play: {info.protocol_roles}"
            )

    return SessionChecker(
        protocol=protocol,
        session_id=session_id,
        role_bindings=bindings,
        monitor=monitor,
    )


# ============================================================
# Swarm validation
# ============================================================


@dataclass(frozen=True)
class SwarmValidationResult:
    """Result of ``validate_swarm()``.

    Tells you whether the available agents can cover all roles
    in the requested protocols.
    """

    valid: bool
    protocols_checked: tuple[str, ...]
    covered_roles: tuple[str, ...]
    uncovered_roles: tuple[str, ...]
    coverage: tuple[tuple[str, tuple[str, ...]], ...]
    """Per-role coverage: ((role, (agent_names...)), ...)"""

    @property
    def coverage_map(self) -> dict[str, tuple[str, ...]]:
        """Return coverage as a dict for convenience."""
        return dict(self.coverage)


def validate_swarm(
    protocols: Optional[Sequence[Protocol]] = None,
    available_agents: Optional[Sequence[AgentRole]] = None,
) -> SwarmValidationResult:
    """Validate that the swarm has agents for all protocol roles.

    If ``protocols`` is None, checks all STANDARD_PROTOCOLS.
    If ``available_agents`` is None, uses all agents in AGENT_CATALOG.

    Example::

        result = validate_swarm()
        assert result.valid
        # result.coverage_map shows which agents cover each role

        # Check with a subset of agents
        result = validate_swarm(
            available_agents=[AgentRole.REGINA, AgentRole.BACKEND],
        )
        assert not result.valid  # missing guardiana!
    """
    protos = (
        list(protocols) if protocols is not None
        else list(STANDARD_PROTOCOLS.values())
    )

    # Build subset catalog if available_agents specified
    if available_agents is not None:
        cat: Mapping[AgentRole, AgentInfo] = MappingProxyType(
            {role: AGENT_CATALOG[role] for role in available_agents
             if role in AGENT_CATALOG}
        )
    else:
        cat = AGENT_CATALOG

    # Collect all unique roles across all protocols
    all_roles: set[str] = set()
    for proto in protos:
        all_roles.update(proto.roles)

    # Build coverage
    coverage: dict[str, list[str]] = {role: [] for role in sorted(all_roles)}
    for info in cat.values():
        for proto_role in info.protocol_roles:
            if proto_role in coverage:
                coverage[proto_role].append(info.agent_name)

    covered = tuple(sorted(r for r, agents in coverage.items() if agents))
    uncovered = tuple(sorted(r for r, agents in coverage.items() if not agents))

    return SwarmValidationResult(
        valid=len(uncovered) == 0,
        protocols_checked=tuple(p.name for p in protos),
        covered_roles=covered,
        uncovered_roles=uncovered,
        coverage=tuple(
            (role, tuple(sorted(agents)))
            for role, agents in sorted(coverage.items())
        ),
    )


# ============================================================
# Auto-resolve bindings
# ============================================================


def resolve_bindings(
    protocol: Protocol,
    preferences: Optional[dict[str, str]] = None,
    catalog: Optional[Mapping[AgentRole, AgentInfo]] = None,
) -> dict[str, str]:
    """Auto-resolve protocol roles to agent names.

    For each role in the protocol, picks an agent that can play it.
    If ``preferences`` is provided, those bindings take priority.

    Selection strategy (deterministic):
    - If role has a preference, use it (validated).
    - If exactly one agent can play the role, use it.
    - If multiple agents can play it, pick the one whose AgentRole
      name sorts first (deterministic, reproducible).

    Raises ValueError if any role cannot be filled.

    Example::

        bindings = resolve_bindings(DelegateTask)
        # {'regina': 'cervella-orchestrator',
        #  'worker': 'cervella-architect',  # first alphabetically
        #  'guardiana': 'cervella-guardiana-ops'}  # first alphabetically

        bindings = resolve_bindings(
            DelegateTask,
            preferences={"worker": "cervella-backend"},
        )
        # worker is now cervella-backend as requested
    """
    prefs = preferences or {}
    cat = catalog if catalog is not None else AGENT_CATALOG
    coverage = agents_for_protocol(protocol, catalog=cat)
    bindings: dict[str, str] = {}

    for role in protocol.roles:
        if role in prefs:
            # Validate preference against the active catalog (not global)
            agent_name = prefs[role]
            info = next(
                (i for i in cat.values() if i.agent_name == agent_name),
                None,
            )
            if info is None:
                raise ValueError(
                    f"preferred agent '{agent_name}' for role '{role}' "
                    f"is not in the catalog"
                )
            if not info.can_play(role):
                raise ValueError(
                    f"preferred agent '{agent_name}' cannot play "
                    f"role '{role}'"
                )
            bindings[role] = agent_name
        else:
            candidates = coverage.get(role, [])
            if not candidates:
                raise ValueError(
                    f"no agent available for protocol role '{role}'"
                )
            # Deterministic: sort by AgentRole.value string
            candidates_sorted = sorted(
                candidates, key=lambda a: a.role.value
            )
            bindings[role] = candidates_sorted[0].agent_name

    return bindings
