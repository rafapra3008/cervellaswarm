# Changelog

All notable changes to `cervellaswarm-lingua-universale` will be documented in this file.

This project follows [Semantic Versioning](https://semver.org/).

## [0.1.0] - 2026-02-21

### Added

**Core type system**
- 14 `MessageKind` enum values covering task lifecycle, audit, architecture, research, and coordination
- 9 frozen dataclass message types: `TaskRequest`, `TaskResult`, `AuditRequest`, `AuditVerdict`, `PlanRequest`, `PlanProposal`, `PlanDecision`, `ResearchQuery`, `ResearchReport`
- 5 coordination message types: `DirectMessage`, `Broadcast`, `ShutdownRequest`, `ShutdownAck`, `ContextInject`
- 17 `AgentRole` definitions with tier-based hierarchy (hub, guardiana, strategic, worker)

**Protocol definitions**
- `Protocol`, `ProtocolStep`, `ProtocolChoice` for defining communication sequences
- 4 standard protocols: `DelegateTask`, `ArchitectFlow`, `ResearchFlow`, `SimpleTask`
- Immutable protocol structures using `MappingProxyType` for branches

**Runtime checker**
- `SessionChecker` with step-by-step protocol enforcement
- `ProtocolViolation` exception with detailed diagnostics (who, what, expected)
- `SessionComplete` signal when protocol finishes successfully
- `MessageRecord` audit trail for all sent messages

**DSL notation**
- Scribble-inspired syntax: `sender -> receiver : MessageKind;`
- `choice at Role { branch: { ... } }` for branching protocols
- `max_repetitions N;` directive for bounded repetition
- `parse_protocol()` / `render_protocol()` with round-trip fidelity

**Protocol monitor**
- 6 event types: `SessionStarted`, `MessageSent`, `BranchChosen`, `ViolationOccurred`, `SessionEnded`, `RepetitionStarted`
- `ProtocolMonitor` with listener registry (observer pattern)
- `MetricsCollector` with Welford online algorithm (O(1) memory)
- `EventCollector` and `LoggingListener` built-in
- Thread-safe internals (Lock + snapshot copy) for Python 3.13+ free-threading

**Lean 4 bridge**
- `Lean4Generator`: Protocol to Lean 4 code generation (template-based)
- `Lean4Verifier`: optional subprocess verification via `lean --json`
- 7 verification properties: senders valid, receivers valid, no self-loop, minimum roles, non-empty steps, branches non-empty, decider in roles
- All theorems proved `by decide` (decidable, zero manual proofs)

**Confidence types**
- `ConfidenceScore` with value (0.0-1.0), source provenance, and evidence
- `Confident[T]` generic wrapper with `map()` and `and_then()` composition
- 3 composition strategies: MIN (conservative), PRODUCT (multiplicative), AVERAGE

**Trust composition**
- `TrustScore` with tier system: VERIFIED, TRUSTED, STANDARD, UNTRUSTED
- Transitive trust composition (Subjective Logic discounting)
- Privilege attenuation: delegatee cannot exceed delegator's authority
- `compose_chain()` for multi-hop trust propagation
- `chain_confidence()` to combine trust chains with output confidence

**Integration**
- `AgentInfo` catalog for 17 CervellaSwarm agents
- `create_session()` factory with automatic role binding
- `validate_swarm()` completeness check
- `resolve_bindings()` deterministic auto-assignment

### Technical Details

- **Zero external dependencies** -- pure Python standard library
- **Python 3.10+** (including 3.13 free-threaded)
- **1273 tests**, 98% coverage, ~0.3s execution time
- **84 public API symbols** exported via `__init__.py`
- Frozen dataclasses with `__post_init__` validation throughout
- Pre-computed O(1) lookup tables for MessageKind <-> PascalCase conversion

[0.1.0]: https://github.com/rafapra3008/cervellaswarm/releases/tag/lingua-universale-v0.1.0
