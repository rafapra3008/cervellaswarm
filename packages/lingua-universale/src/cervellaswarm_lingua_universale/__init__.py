# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""CervellaSwarm Lingua Universale - Session types for AI agent protocols."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("cervellaswarm-lingua-universale")
except PackageNotFoundError:
    __version__ = "0.5.0"

# Public API re-exports for convenience.
# Users can also import directly from submodules.
from ._cli import main as cli_main
from ._compiler import (
    ASTCompiler,
    CompiledModule,
)
from ._contracts import (
    ContractViolation,
)
from ._eval import (
    EvalResult,
    check_file,
    check_source,
    run_file,
    run_source,
    verify_file,
    verify_source,
)
from ._fmt import format_source as format_source
from ._generate import (
    GenerateResult,
    generate_from_file,
    generate_from_source,
)
from ._grammar_export import (
    GRAMMAR_VERSION,
    GrammarExporter,
)
from ._intent_bridge import (
    ChatPhase,
    ChatResult,
    ChatSession,
    DraftChoice,
    DraftMessage,
    IntentDraft,
    NLClarificationNeeded,
    NLProcessor,
    Turn,
    render_intent_source,
)
from ._interop import (
    InteropError,
    compile_file,
    load_file,
    load_module,
    save_module,
)
from ._lint import (
    LintCategory as LintCategory,
)
from ._lint import (
    LintFinding as LintFinding,
)
from ._lint import (
    LintSeverity as LintSeverity,
)
from ._lint import (
    lint_source as lint_source,
)
from ._mcp_audit import (
    AnnotationFinding,
    AuditReport,
    InferredProtocol,
    ToolDefinition,
    audit_tools,
    check_annotations,
    load_manifest,
)
from ._mcp_audit import (
    render_json as render_audit_json,
)
from ._mcp_audit import (
    render_terminal as render_audit_terminal,
)
from ._nl_processor import (
    TOOL_SCHEMA as _NL_TOOL_SCHEMA,
)
from ._nl_processor import (  # anthropic imported lazily at instantiation
    ClaudeNLProcessor as ClaudeNLProcessor,
)
from ._nl_processor import (
    NLProcessorError as NLProcessorError,
)
from ._repl import REPLSession
from ._voice import (  # faster-whisper+sounddevice imported lazily at instantiation
    VoiceProcessor as VoiceProcessor,
)
from ._voice import (
    VoiceProcessorError as VoiceProcessorError,
)
from .checker import (
    MessageRecord,
    ProtocolViolation,
    SessionChecker,
    SessionComplete,
    SessionState,
)
from .codegen import (
    GeneratedCode,
    PythonGenerator,
    generate_python,
    generate_python_multi,
)
from .codegen_json import (
    JSONSchemaGenerator,
    generate_json_schema,
)
from .codegen_ts import (
    TypeScriptGenerator,
    generate_typescript,
)
from .confidence import (
    CompositionStrategy,
    ConfidenceScore,
    ConfidenceSource,
    Confident,
    compose_scores,
)
from .dsl import (
    DSLError,
    DSLParseError,
    parse_protocol,
    parse_protocols,
    render_protocol,
    render_protocols,
)
from .errors import (
    DEFAULT_LOCALE,
    SUPPORTED_LOCALES,
    ErrorCategory,
    ErrorLocation,
    ErrorSeverity,
    HumanError,
    format_error,
    humanize,
    render_snippet,
    suggest_similar,
)
from .integration import (
    AGENT_CATALOG,
    AgentInfo,
    SwarmValidationResult,
    agent_by_name,
    agent_by_role,
    agents_for_protocol,
    create_session,
    resolve_bindings,
    validate_swarm,
)
from .intent import (
    IntentParseError,
    IntentParseResult,
    parse_intent,
    parse_intent_protocol,
)
from .lean4_bridge import (
    ALL_PROPERTIES,
    FLAT_PROPERTIES,
    Lean4Generator,
    Lean4Verifier,
    VerificationProperty,
    VerificationReport,
    VerificationResult,
    generate_lean4,
    generate_lean4_multi,
    lean4_available,
)
from .monitor import (
    BranchChosen,
    EventCollector,
    LoggingListener,
    MessageSent,
    MetricsCollector,
    MetricsSnapshot,
    MonitorEvent,
    MonitorListener,
    ProtocolMonitor,
    RepetitionStarted,
    SessionEnded,
    SessionStarted,
    ViolationOccurred,
)
from .protocols import (
    STANDARD_PROTOCOLS,
    ArchitectFlow,
    DelegateTask,
    Protocol,
    ProtocolChoice,
    ProtocolElement,
    ProtocolStep,
    ResearchFlow,
    SimpleTask,
)
from .spec import (
    PropertyKind,
    PropertyReport,
    PropertyResult,
    PropertySpec,
    PropertyVerdict,
    ProtocolSpec,
    SpecParseError,
    check_properties,
    check_session,
    parse_spec,
)
from .trust import (
    TrustScore,
    TrustTier,
    chain_confidence,
    compose_chain,
    trust_tier_for_role,
)
from .types import (
    AgentRole,
    AuditRequest,
    AuditVerdict,
    AuditVerdictType,
    Broadcast,
    ContextInject,
    DirectMessage,
    MessageKind,
    PlanComplexity,
    PlanDecision,
    PlanProposal,
    PlanRequest,
    ResearchQuery,
    ResearchReport,
    ShutdownAck,
    ShutdownRequest,
    SwarmMessage,
    TaskRequest,
    TaskResult,
    TaskStatus,
    message_kind,
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
    "TypeScriptGenerator",
    "generate_typescript",
    "JSONSchemaGenerator",
    "generate_json_schema",
    # Generate bridge
    "GenerateResult",
    "generate_from_file",
    "generate_from_source",
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
    # Lint (B5)
    "lint_source",
    "LintFinding",
    "LintSeverity",
    "LintCategory",
    # Format (B6)
    "format_source",
    # IntentBridge (E.2+E.3)
    "ChatPhase",
    "ChatResult",
    "ChatSession",
    "DraftChoice",
    "DraftMessage",
    "IntentDraft",
    "NLClarificationNeeded",
    "NLProcessor",
    "Turn",
    "render_intent_source",
    # REPL (C3.4)
    "REPLSession",
    # Errors
    "ErrorCategory",
    "ErrorSeverity",
    "ErrorLocation",
    "HumanError",
    "humanize",
    "format_error",
    "render_snippet",
    "suggest_similar",
    "DEFAULT_LOCALE",
    "SUPPORTED_LOCALES",
    # MCP Audit
    "AnnotationFinding",
    "AuditReport",
    "InferredProtocol",
    "ToolDefinition",
    "audit_tools",
    "check_annotations",
    "load_manifest",
    "render_audit_json",
    "render_audit_terminal",
    # NL Processor (E.3, optional dep -- `pip install ...[nl]`)
    "ClaudeNLProcessor",
    "NLProcessorError",
    # Voice Processor (E.4, optional dep -- `pip install ...[voice]`)
    "VoiceProcessor",
    "VoiceProcessorError",
]
