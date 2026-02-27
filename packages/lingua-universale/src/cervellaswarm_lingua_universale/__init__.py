# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""CervellaSwarm Lingua Universale - Session types for AI agent protocols."""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("cervellaswarm-lingua-universale")
except PackageNotFoundError:
    __version__ = "0.1.1"

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
    DirectMessage,
    Broadcast,
    ShutdownRequest,
    ShutdownAck,
    ContextInject,
    SwarmMessage,
    message_kind,
)
from .protocols import (
    Protocol,
    ProtocolStep,
    ProtocolChoice,
    ProtocolElement,
    STANDARD_PROTOCOLS,
    DelegateTask,
    ArchitectFlow,
    ResearchFlow,
    SimpleTask,
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
from .confidence import (
    ConfidenceScore,
    ConfidenceSource,
    Confident,
    CompositionStrategy,
    compose_scores,
)
from .trust import (
    TrustTier,
    TrustScore,
    trust_tier_for_role,
    compose_chain,
    chain_confidence,
)
from .codegen import (
    GeneratedCode,
    PythonGenerator,
    generate_python,
    generate_python_multi,
)
from .intent import (
    IntentParseResult,
    IntentParseError,
    parse_intent,
    parse_intent_protocol,
)
from .spec import (
    PropertyKind,
    PropertyVerdict,
    PropertySpec,
    ProtocolSpec,
    PropertyResult,
    PropertyReport,
    SpecParseError,
    parse_spec,
    check_properties,
    check_session,
)
from ._contracts import (
    ContractViolation,
)
from ._compiler import (
    ASTCompiler,
    CompiledModule,
)
from ._interop import (
    InteropError,
    compile_file,
    save_module,
    load_module,
    load_file,
)
from ._grammar_export import (
    GrammarExporter,
    GRAMMAR_VERSION,
)
from ._eval import (
    EvalResult,
    check_source,
    check_file,
    verify_source,
    verify_file,
    run_source,
    run_file,
)
from ._cli import main as cli_main
from .errors import (
    ErrorCategory,
    ErrorSeverity,
    ErrorLocation,
    HumanError,
    humanize,
    format_error,
    suggest_similar,
    DEFAULT_LOCALE,
    SUPPORTED_LOCALES,
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
    "DirectMessage",
    "Broadcast",
    "ShutdownRequest",
    "ShutdownAck",
    "ContextInject",
    "SwarmMessage",
    "message_kind",
    # Protocols
    "Protocol",
    "ProtocolStep",
    "ProtocolChoice",
    "ProtocolElement",
    "STANDARD_PROTOCOLS",
    "DelegateTask",
    "ArchitectFlow",
    "ResearchFlow",
    "SimpleTask",
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
    # Confidence
    "ConfidenceScore",
    "ConfidenceSource",
    "Confident",
    "CompositionStrategy",
    "compose_scores",
    # Trust
    "TrustTier",
    "TrustScore",
    "trust_tier_for_role",
    "compose_chain",
    "chain_confidence",
    # Codegen
    "GeneratedCode",
    "PythonGenerator",
    "generate_python",
    "generate_python_multi",
    # Intent
    "IntentParseResult",
    "IntentParseError",
    "parse_intent",
    "parse_intent_protocol",
    # Spec
    "PropertyKind",
    "PropertyVerdict",
    "PropertySpec",
    "ProtocolSpec",
    "PropertyResult",
    "PropertyReport",
    "SpecParseError",
    "parse_spec",
    "check_properties",
    "check_session",
    # Contracts (C2)
    "ContractViolation",
    # Compiler (C2)
    "ASTCompiler",
    "CompiledModule",
    # Interop (C2.3)
    "InteropError",
    "compile_file",
    "save_module",
    "load_module",
    "load_file",
    # Grammar Export (C2.4)
    "GrammarExporter",
    "GRAMMAR_VERSION",
    # Eval (C3.2)
    "EvalResult",
    "check_source",
    "check_file",
    "verify_source",
    "verify_file",
    "run_source",
    "run_file",
    "cli_main",
    # Errors
    "ErrorCategory",
    "ErrorSeverity",
    "ErrorLocation",
    "HumanError",
    "humanize",
    "format_error",
    "suggest_similar",
    "DEFAULT_LOCALE",
    "SUPPORTED_LOCALES",
]
