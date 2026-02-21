# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""CervellaSwarm Lingua Universale - Session types for AI agent protocols."""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("cervellaswarm-lingua-universale")
except PackageNotFoundError:
    __version__ = "0.1.0"

# Public API re-exports for convenience.
# Users can also import directly from submodules.
from .types import (
    AgentRole,
    AuditVerdictType,
    MessageKind,
    PlanComplexity,
    TaskStatus,
    TaskRequest,
    TaskResult,
    AuditRequest,
    AuditVerdict,
    PlanRequest,
    PlanProposal,
    PlanDecision,
    ResearchQuery,
    ResearchReport,
    SwarmMessage,
    message_kind,
)
from .protocols import (
    Protocol,
    ProtocolStep,
    ProtocolChoice,
    ProtocolElement,
    STANDARD_PROTOCOLS,
)
from .checker import (
    MessageRecord,
    ProtocolViolation,
    SessionChecker,
    SessionComplete,
    SessionState,
)
from .dsl import (
    parse_protocol,
    parse_protocols,
    render_protocol,
    render_protocols,
    DSLError,
    DSLParseError,
)
from .monitor import (
    MonitorEvent,
    SessionStarted,
    MessageSent,
    BranchChosen,
    ViolationOccurred,
    SessionEnded,
    RepetitionStarted,
    MonitorListener,
    MetricsSnapshot,
    MetricsCollector,
    ProtocolMonitor,
    LoggingListener,
    EventCollector,
)
from .lean4_bridge import (
    VerificationProperty,
    VerificationResult,
    VerificationReport,
    Lean4Generator,
    Lean4Verifier,
    lean4_available,
    generate_lean4,
    generate_lean4_multi,
    FLAT_PROPERTIES,
    ALL_PROPERTIES,
)
from .integration import (
    AgentInfo,
    AGENT_CATALOG,
    agent_by_name,
    agent_by_role,
    agents_for_protocol,
    create_session,
    SwarmValidationResult,
    validate_swarm,
    resolve_bindings,
)

__all__ = [
    # Version
    "__version__",
    # Types - enums
    "AgentRole",
    "AuditVerdictType",
    "MessageKind",
    "PlanComplexity",
    "TaskStatus",
    # Types - messages
    "TaskRequest",
    "TaskResult",
    "AuditRequest",
    "AuditVerdict",
    "PlanRequest",
    "PlanProposal",
    "PlanDecision",
    "ResearchQuery",
    "ResearchReport",
    "SwarmMessage",
    "message_kind",
    # Protocols
    "Protocol",
    "ProtocolStep",
    "ProtocolChoice",
    "ProtocolElement",
    "STANDARD_PROTOCOLS",
    # Checker
    "MessageRecord",
    "ProtocolViolation",
    "SessionChecker",
    "SessionComplete",
    "SessionState",
    # DSL
    "parse_protocol",
    "parse_protocols",
    "render_protocol",
    "render_protocols",
    "DSLError",
    "DSLParseError",
    # Monitor
    "MonitorEvent",
    "SessionStarted",
    "MessageSent",
    "BranchChosen",
    "ViolationOccurred",
    "SessionEnded",
    "RepetitionStarted",
    "MonitorListener",
    "MetricsSnapshot",
    "MetricsCollector",
    "ProtocolMonitor",
    "LoggingListener",
    "EventCollector",
    # Lean 4 Bridge
    "VerificationProperty",
    "VerificationResult",
    "VerificationReport",
    "Lean4Generator",
    "Lean4Verifier",
    "lean4_available",
    "generate_lean4",
    "generate_lean4_multi",
    "FLAT_PROPERTIES",
    "ALL_PROPERTIES",
    # Integration
    "AgentInfo",
    "AGENT_CATALOG",
    "agent_by_name",
    "agent_by_role",
    "agents_for_protocol",
    "create_session",
    "SwarmValidationResult",
    "validate_swarm",
    "resolve_bindings",
]
