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
    MessageKind,
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
from .checker import SessionChecker, SessionState
from .dsl import (
    parse_protocol,
    parse_protocols,
    render_protocol,
    render_protocols,
    DSLError,
    DSLParseError,
)

__all__ = [
    # Version
    "__version__",
    # Types
    "AgentRole",
    "MessageKind",
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
    "SessionChecker",
    "SessionState",
    # DSL
    "parse_protocol",
    "parse_protocols",
    "render_protocol",
    "render_protocols",
    "DSLError",
    "DSLParseError",
]
