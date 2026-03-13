# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Protocol definitions for CervellaSwarm agent communication.

Each protocol is a state machine that defines the valid sequence
of messages between agents. The SessionChecker uses these to verify
that communication follows the protocol.

This is the HEART of the Lingua Universale.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Mapping, Optional

from .types import MessageKind


@dataclass(frozen=True)
class ProtocolStep:
    """A single step in a protocol: sender sends message_kind to receiver."""

    sender: str          # role name (e.g., "regina", "worker", "guardiana")
    receiver: str        # role name
    message_kind: MessageKind
    description: str = ""

    def __post_init__(self) -> None:
        if not self.sender:
            raise ValueError("sender cannot be empty")
        if not self.receiver:
            raise ValueError("receiver cannot be empty")
        if self.sender == self.receiver:
            raise ValueError(
                f"sender and receiver cannot be the same: '{self.sender}'"
            )


@dataclass(frozen=True)
class ProtocolChoice:
    """A branching point in the protocol.

    The decider role chooses which branch to take.
    Each branch is a sequence of ProtocolElements (steps and/or nested choices).

    Branches are made immutable via MappingProxyType in __post_init__
    to guarantee protocol definitions cannot be mutated after creation.
    """

    decider: str
    branches: Mapping[str, tuple[ProtocolElement, ...]]
    description: str = ""

    def __post_init__(self) -> None:
        if not self.decider:
            raise ValueError("decider cannot be empty")
        if not self.branches:
            raise ValueError("branches cannot be empty")
        # Make branches immutable (frozen=True only prevents reassignment,
        # not mutation of mutable containers like dict)
        object.__setattr__(
            self, "branches", MappingProxyType(dict(self.branches))
        )


# A protocol element is either a step or a choice
ProtocolElement = ProtocolStep | ProtocolChoice


@dataclass(frozen=True)
class Protocol:
    """A complete session protocol definition.

    Defines the roles involved and the ordered sequence of
    communication steps (including branches).
    """

    name: str
    roles: tuple[str, ...]
    elements: tuple[ProtocolElement, ...]
    max_repetitions: int = 1
    description: str = ""

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("protocol name cannot be empty")
        if len(self.roles) < 2:
            raise ValueError("protocol must have at least 2 roles")
        if len(self.roles) != len(set(self.roles)):
            seen = set()
            dupes = [r for r in self.roles if r in seen or seen.add(r)]  # type: ignore[func-returns-value]
            raise ValueError(f"duplicate roles: {dupes}")
        if self.max_repetitions < 1:
            raise ValueError(
                f"max_repetitions must be at least 1, got {self.max_repetitions}"
            )
        # Validate all senders/receivers and deciders are declared roles
        self._validate_elements(self.elements)

    def _validate_elements(self, elements: tuple[ProtocolElement, ...]) -> None:
        """Recursively validate roles in protocol elements (supports nested choices)."""
        for elem in elements:
            if isinstance(elem, ProtocolStep):
                self._validate_step_roles(elem)
            elif isinstance(elem, ProtocolChoice):
                if elem.decider not in self.roles:
                    raise ValueError(
                        f"decider '{elem.decider}' not in protocol roles "
                        f"{self.roles}"
                    )
                for branch_elems in elem.branches.values():
                    self._validate_elements(branch_elems)

    def _validate_step_roles(self, step: ProtocolStep) -> None:
        if step.sender not in self.roles:
            raise ValueError(
                f"sender '{step.sender}' not in protocol roles {self.roles}"
            )
        if step.receiver not in self.roles:
            raise ValueError(
                f"receiver '{step.receiver}' not in protocol roles {self.roles}"
            )


# ============================================================
# Standard CervellaSwarm Protocols
# ============================================================


DelegateTask = Protocol(
    name="DelegateTask",
    roles=("regina", "worker", "guardiana"),
    description=(
        "The standard workflow: Regina delegates a task to a Worker, "
        "Worker executes and returns result, Guardiana audits."
    ),
    elements=(
        ProtocolStep(
            sender="regina",
            receiver="worker",
            message_kind=MessageKind.TASK_REQUEST,
            description="Regina delegates task to worker",
        ),
        ProtocolStep(
            sender="worker",
            receiver="regina",
            message_kind=MessageKind.TASK_RESULT,
            description="Worker returns execution result",
        ),
        ProtocolStep(
            sender="regina",
            receiver="guardiana",
            message_kind=MessageKind.AUDIT_REQUEST,
            description="Regina requests quality audit",
        ),
        ProtocolStep(
            sender="guardiana",
            receiver="regina",
            message_kind=MessageKind.AUDIT_VERDICT,
            description="Guardiana returns audit verdict",
        ),
    ),
)


ArchitectFlow = Protocol(
    name="ArchitectFlow",
    roles=("regina", "architect", "worker", "guardiana"),
    description=(
        "For complex tasks: Architect plans, Regina approves, "
        "Worker implements, Guardiana verifies."
    ),
    elements=(
        ProtocolStep(
            sender="regina",
            receiver="architect",
            message_kind=MessageKind.PLAN_REQUEST,
            description="Regina requests implementation plan",
        ),
        ProtocolStep(
            sender="architect",
            receiver="regina",
            message_kind=MessageKind.PLAN_PROPOSAL,
            description="Architect proposes plan",
        ),
        ProtocolChoice(
            decider="regina",
            description="Regina approves or rejects the plan",
            branches={
                "approve": (
                    ProtocolStep(
                        sender="regina",
                        receiver="architect",
                        message_kind=MessageKind.PLAN_DECISION,
                        description="Regina approves plan",
                    ),
                    ProtocolStep(
                        sender="regina",
                        receiver="worker",
                        message_kind=MessageKind.TASK_REQUEST,
                        description="Regina delegates implementation",
                    ),
                    ProtocolStep(
                        sender="worker",
                        receiver="regina",
                        message_kind=MessageKind.TASK_RESULT,
                        description="Worker returns result",
                    ),
                    ProtocolStep(
                        sender="regina",
                        receiver="guardiana",
                        message_kind=MessageKind.AUDIT_REQUEST,
                        description="Regina requests audit",
                    ),
                    ProtocolStep(
                        sender="guardiana",
                        receiver="regina",
                        message_kind=MessageKind.AUDIT_VERDICT,
                        description="Guardiana verifies",
                    ),
                ),
                "reject": (
                    ProtocolStep(
                        sender="regina",
                        receiver="architect",
                        message_kind=MessageKind.PLAN_DECISION,
                        description="Regina rejects plan with feedback",
                    ),
                    ProtocolStep(
                        sender="architect",
                        receiver="regina",
                        message_kind=MessageKind.PLAN_PROPOSAL,
                        description="Architect revises plan",
                    ),
                ),
            },
        ),
    ),
    # NOTE: Repetition for reject-then-retry cycles requires recursive
    # protocol elements (planned for Fase B). For now, single pass.
    max_repetitions=1,
)


ResearchFlow = Protocol(
    name="ResearchFlow",
    roles=("regina", "researcher", "guardiana"),
    description=(
        "Research with quality gate: Regina queries, Researcher reports, "
        "Guardiana Ricerca reviews."
    ),
    elements=(
        ProtocolStep(
            sender="regina",
            receiver="researcher",
            message_kind=MessageKind.RESEARCH_QUERY,
            description="Regina sends research query",
        ),
        ProtocolStep(
            sender="researcher",
            receiver="regina",
            message_kind=MessageKind.RESEARCH_REPORT,
            description="Researcher returns report",
        ),
        ProtocolStep(
            sender="regina",
            receiver="guardiana",
            message_kind=MessageKind.AUDIT_REQUEST,
            description="Regina requests research quality review",
        ),
        ProtocolStep(
            sender="guardiana",
            receiver="regina",
            message_kind=MessageKind.AUDIT_VERDICT,
            description="Guardiana reviews research quality",
        ),
    ),
)


SimpleTask = Protocol(
    name="SimpleTask",
    roles=("regina", "worker"),
    description="Quick task without audit. For low-risk, reversible actions.",
    elements=(
        ProtocolStep(
            sender="regina",
            receiver="worker",
            message_kind=MessageKind.TASK_REQUEST,
            description="Regina delegates simple task",
        ),
        ProtocolStep(
            sender="worker",
            receiver="regina",
            message_kind=MessageKind.TASK_RESULT,
            description="Worker returns result",
        ),
    ),
)


# Registry of all standard protocols (immutable)
STANDARD_PROTOCOLS: Mapping[str, Protocol] = MappingProxyType({
    "DelegateTask": DelegateTask,
    "ArchitectFlow": ArchitectFlow,
    "ResearchFlow": ResearchFlow,
    "SimpleTask": SimpleTask,
})
