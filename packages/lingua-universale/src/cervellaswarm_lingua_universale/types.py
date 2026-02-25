# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Core types for CervellaSwarm agent communication.

Every message in the swarm has exactly one type.
Every type has a schema (dataclass).
No untyped messages. No string blobs.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


# ============================================================
# Enums - The vocabulary of the swarm
# ============================================================


class TaskStatus(Enum):
    """Result status of a worker task."""

    OK = "ok"
    FAIL = "fail"
    BLOCKED = "blocked"


class AuditVerdictType(Enum):
    """Guardiana audit outcome."""

    APPROVED = "approved"
    BLOCKED = "blocked"
    NEEDS_REVISION = "needs_revision"


class PlanComplexity(Enum):
    """Architect plan complexity assessment."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AgentRole(Enum):
    """Every agent in the swarm has exactly one role."""

    # Hub
    REGINA = "regina"

    # Guardiane (opus)
    GUARDIANA_QUALITA = "guardiana-qualita"
    GUARDIANA_RICERCA = "guardiana-ricerca"
    GUARDIANA_OPS = "guardiana-ops"

    # Strategic (opus)
    ARCHITECT = "architect"
    SECURITY = "security"
    INGEGNERA = "ingegnera"

    # Workers (sonnet)
    BACKEND = "backend"
    FRONTEND = "frontend"
    TESTER = "tester"
    REVIEWER = "reviewer"
    RESEARCHER = "researcher"
    MARKETING = "marketing"
    DEVOPS = "devops"
    DOCS = "docs"
    DATA = "data"
    SCIENZIATA = "scienziata"

    @property
    def tier(self) -> str:
        """Return the agent tier: hub, guardiana, strategic, or worker."""
        if self == AgentRole.REGINA:
            return "hub"
        if self.value.startswith("guardiana"):
            return "guardiana"
        if self in (AgentRole.ARCHITECT, AgentRole.SECURITY, AgentRole.INGEGNERA):
            return "strategic"
        return "worker"

    @property
    def model(self) -> str:
        """Return the model tier for this role."""
        if self.tier in ("hub", "guardiana", "strategic"):
            return "opus"
        return "sonnet"


class MessageKind(Enum):
    """Classification of message types in the protocol."""

    TASK_REQUEST = "task_request"
    TASK_RESULT = "task_result"
    AUDIT_REQUEST = "audit_request"
    AUDIT_VERDICT = "audit_verdict"
    PLAN_REQUEST = "plan_request"
    PLAN_PROPOSAL = "plan_proposal"
    PLAN_DECISION = "plan_decision"
    RESEARCH_QUERY = "research_query"
    RESEARCH_REPORT = "research_report"
    DM = "dm"
    BROADCAST = "broadcast"
    SHUTDOWN_REQUEST = "shutdown_request"
    SHUTDOWN_ACK = "shutdown_ack"
    CONTEXT_INJECT = "context_inject"


# ============================================================
# Message Dataclasses - The typed payloads
# ============================================================


@dataclass(frozen=True)
class TaskRequest:
    """Regina -> Worker: delegate a task.

    Every task delegation MUST use this type.
    No more unstructured prompt strings.
    """

    task_id: str
    description: str
    target_files: tuple[str, ...] = ()
    constraints: tuple[str, ...] = ()
    max_file_lines: int = 500

    KIND: MessageKind = field(
        default=MessageKind.TASK_REQUEST, init=False, repr=False
    )

    def __post_init__(self) -> None:
        if not self.task_id:
            raise ValueError("task_id cannot be empty")
        if not self.description:
            raise ValueError("description cannot be empty")
        if self.max_file_lines < 1:
            raise ValueError("max_file_lines must be positive")


@dataclass(frozen=True)
class TaskResult:
    """Worker -> Regina: task completion report.

    Workers MUST return this type. Status MUST be set.
    If BLOCKED, blockers MUST be provided.
    """

    task_id: str
    status: TaskStatus
    summary: str
    files_modified: tuple[str, ...] = ()
    files_created: tuple[str, ...] = ()
    test_command: Optional[str] = None
    next_steps: Optional[str] = None
    blockers: Optional[str] = None

    KIND: MessageKind = field(
        default=MessageKind.TASK_RESULT, init=False, repr=False
    )

    def __post_init__(self) -> None:
        if not self.task_id:
            raise ValueError("task_id cannot be empty")
        if not self.summary:
            raise ValueError("summary cannot be empty")
        if len(self.summary) > 200:
            raise ValueError("summary must be <= 200 characters")
        if self.status == TaskStatus.BLOCKED and not self.blockers:
            raise ValueError("blockers required when status is BLOCKED")


@dataclass(frozen=True)
class AuditRequest:
    """Regina -> Guardiana: request quality audit.

    Every significant output MUST be audited.
    Checklist items define what the Guardiana verifies.
    """

    audit_id: str
    target: str
    checklist: tuple[str, ...] = ()
    worker_output: str = ""

    KIND: MessageKind = field(
        default=MessageKind.AUDIT_REQUEST, init=False, repr=False
    )

    def __post_init__(self) -> None:
        if not self.audit_id:
            raise ValueError("audit_id cannot be empty")
        if not self.target:
            raise ValueError("target cannot be empty")


@dataclass(frozen=True)
class AuditVerdict:
    """Guardiana -> Regina: audit result.

    Score MUST be 0.0-10.0. Checked items MUST be non-empty.
    """

    audit_id: str
    verdict: AuditVerdictType
    score: float
    checked: tuple[str, ...] = ()
    issues: tuple[str, ...] = ()
    action: str = ""

    KIND: MessageKind = field(
        default=MessageKind.AUDIT_VERDICT, init=False, repr=False
    )

    def __post_init__(self) -> None:
        if not self.audit_id:
            raise ValueError("audit_id cannot be empty")
        if not (0.0 <= self.score <= 10.0):
            raise ValueError(f"score must be 0.0-10.0, got {self.score}")
        if not self.checked:
            raise ValueError("checked items cannot be empty")


@dataclass(frozen=True)
class PlanRequest:
    """Regina -> Architect: request an implementation plan."""

    plan_id: str
    task_description: str
    complexity_hint: Optional[PlanComplexity] = None
    constraints: tuple[str, ...] = ()

    KIND: MessageKind = field(
        default=MessageKind.PLAN_REQUEST, init=False, repr=False
    )

    def __post_init__(self) -> None:
        if not self.plan_id:
            raise ValueError("plan_id cannot be empty")
        if not self.task_description:
            raise ValueError("task_description cannot be empty")


@dataclass(frozen=True)
class PlanProposal:
    """Architect -> Regina: the implementation plan.

    Risk score MUST be 0.0-1.0.
    """

    plan_id: str
    complexity: PlanComplexity
    risk_score: float
    files_affected: int
    phases: tuple[str, ...] = ()
    steps: tuple[str, ...] = ()
    success_criteria: tuple[str, ...] = ()
    plan_file: str = ""

    KIND: MessageKind = field(
        default=MessageKind.PLAN_PROPOSAL, init=False, repr=False
    )

    def __post_init__(self) -> None:
        if not self.plan_id:
            raise ValueError("plan_id cannot be empty")
        if not (0.0 <= self.risk_score <= 1.0):
            raise ValueError(f"risk_score must be 0.0-1.0, got {self.risk_score}")
        if self.files_affected < 0:
            raise ValueError("files_affected cannot be negative")


@dataclass(frozen=True)
class PlanDecision:
    """Regina -> Architect: approve or reject a plan."""

    plan_id: str
    approved: bool
    feedback: str = ""

    KIND: MessageKind = field(
        default=MessageKind.PLAN_DECISION, init=False, repr=False
    )

    def __post_init__(self) -> None:
        if not self.plan_id:
            raise ValueError("plan_id cannot be empty")
        if not self.approved and not self.feedback:
            raise ValueError("feedback required when rejecting a plan")


@dataclass(frozen=True)
class ResearchQuery:
    """Regina -> Researcher: research request."""

    query_id: str
    topic: str
    min_sources: int = 10
    scope: tuple[str, ...] = ()

    KIND: MessageKind = field(
        default=MessageKind.RESEARCH_QUERY, init=False, repr=False
    )

    def __post_init__(self) -> None:
        if not self.query_id:
            raise ValueError("query_id cannot be empty")
        if not self.topic:
            raise ValueError("topic cannot be empty")
        if self.min_sources < 1:
            raise ValueError("min_sources must be positive")


@dataclass(frozen=True)
class ResearchReport:
    """Researcher -> Regina: research results."""

    query_id: str
    topic: str
    sources_consulted: int
    key_findings: tuple[str, ...] = ()
    report_file: str = ""

    KIND: MessageKind = field(
        default=MessageKind.RESEARCH_REPORT, init=False, repr=False
    )

    def __post_init__(self) -> None:
        if not self.query_id:
            raise ValueError("query_id cannot be empty")
        if not self.topic:
            raise ValueError("topic cannot be empty")
        if self.sources_consulted < 1:
            raise ValueError("sources_consulted must be at least 1")


@dataclass(frozen=True)
class DirectMessage:
    """Agent -> Agent: direct message between any two agents.

    Used for peer-to-peer communication within the swarm.
    """

    sender_role: str
    content: str
    thread_id: str = ""

    KIND: MessageKind = field(
        default=MessageKind.DM, init=False, repr=False
    )

    def __post_init__(self) -> None:
        if not self.sender_role:
            raise ValueError("sender_role cannot be empty")
        if not self.content:
            raise ValueError("content cannot be empty")


@dataclass(frozen=True)
class Broadcast:
    """Agent -> All: broadcast message to all agents.

    Used for team-wide announcements and critical notifications.
    """

    sender_role: str
    content: str
    priority: str = "normal"

    KIND: MessageKind = field(
        default=MessageKind.BROADCAST, init=False, repr=False
    )

    def __post_init__(self) -> None:
        if not self.sender_role:
            raise ValueError("sender_role cannot be empty")
        if not self.content:
            raise ValueError("content cannot be empty")
        if self.priority not in ("normal", "urgent", "critical"):
            raise ValueError(
                f"priority must be normal/urgent/critical, got {self.priority!r}"
            )


@dataclass(frozen=True)
class ShutdownRequest:
    """Leader -> Agent: request graceful shutdown.

    The agent should finish current work and acknowledge.
    """

    target_role: str
    reason: str = ""

    KIND: MessageKind = field(
        default=MessageKind.SHUTDOWN_REQUEST, init=False, repr=False
    )

    def __post_init__(self) -> None:
        if not self.target_role:
            raise ValueError("target_role cannot be empty")


@dataclass(frozen=True)
class ShutdownAck:
    """Agent -> Leader: acknowledge shutdown request.

    Confirms the agent has received and will comply with shutdown.
    """

    target_role: str
    acknowledged: bool = True

    KIND: MessageKind = field(
        default=MessageKind.SHUTDOWN_ACK, init=False, repr=False
    )

    def __post_init__(self) -> None:
        if not self.target_role:
            raise ValueError("target_role cannot be empty")


@dataclass(frozen=True)
class ContextInject:
    """System -> Agent: inject context into agent session.

    Used by hooks to provide PROMPT_RIPRESA, FATOS, etc.
    """

    context_type: str
    content: str
    source_file: str = ""

    KIND: MessageKind = field(
        default=MessageKind.CONTEXT_INJECT, init=False, repr=False
    )

    def __post_init__(self) -> None:
        if not self.context_type:
            raise ValueError("context_type cannot be empty")
        if not self.content:
            raise ValueError("content cannot be empty")


# Type alias for any swarm message
SwarmMessage = (
    TaskRequest
    | TaskResult
    | AuditRequest
    | AuditVerdict
    | PlanRequest
    | PlanProposal
    | PlanDecision
    | ResearchQuery
    | ResearchReport
    | DirectMessage
    | Broadcast
    | ShutdownRequest
    | ShutdownAck
    | ContextInject
)


def message_kind(msg: SwarmMessage) -> MessageKind:
    """Extract the MessageKind from any swarm message."""
    return msg.KIND
