# Changelog

All notable changes to `cervellaswarm-lingua-universale` will be documented in this file.

This project follows [Semantic Versioning](https://semver.org/).

## [0.2.0] - 2026-02-28

### Added

**The Language - Phase C: Parsing Pipeline (C1)**
- `_tokenizer.py`: Unified lexer for Lingua Universale v0.2. Replaces the two inline tokenizers in `intent.py` and `spec.py`. 62-production EBNF grammar support, explicit INDENT/DEDENT tokens, paren-depth tracking for line continuation, 4-space indent enforcement, `textwrap.dedent` pre-processing. Zero external dependencies.
- `_ast.py`: Immutable frozen-dataclass AST node hierarchy for the 62-production grammar. Node families: `Expr` (8 types), `Property` (7 types), `Step/Choice` (3 types), `Protocol`, `Agent`, `Type` (5 types), `Use`, `Program`. All collections use `tuple` for hashability.
- `_parser.py`: Recursive descent parser. Converts token list from `_tokenizer` into `ProgramNode` AST. LL(1) with targeted LL(3) lookahead for method-call disambiguation. Public API: `parse(source) -> ProgramNode`, `ParseError`.

**The Language - Phase C: Compiler Pipeline (C2)**
- `_contracts.py`: Runtime contract enforcement for compiled LU programs. `ContractViolation(RuntimeError)` with `condition`, `kind` (`requires`/`ensures`), and `source` attributes. Raised unconditionally (not disabled with `-O`).
- `_compiler.py`: LU AST to Python source compiler. `ASTCompiler` visitor pattern via `isinstance` dispatch. Emits `ContractViolation` guards for every `requires`/`ensures` clause. Source annotations `# [LU:line:col]` for traceability. `CompiledModule` result type. Public API: `compile(ast) -> CompiledModule`.
- `_interop.py`: File I/O and runtime layer on top of `_compiler`. `compile_file(path)`, `save_module(module, path)`, `load_module(module)`, `load_file(path)`. `load_module`/`load_file` execute generated Python via `exec()` into a live module object. `InteropError` exception type.
- `_grammar_export.py`: Grammar exporter for constrained LLM decoding (C2.4). Exports two formats: **GBNF** (for XGrammar, vLLM, llama.cpp) and **Lark EBNF** (for Outlines, llguidance). Whitespace-lenient variant of the grammar (INDENT/DEDENT replaced by free whitespace). Closed lists for `verb` (5 entries) and `noun` (9 entries) to prevent hallucination. Zero external dependencies; rules statically encoded.

**The Language - Phase C: Evaluation Engine (C3)**
- `_eval.py`: Unified evaluation engine with three levels of evaluation: `check_source()`/`check_file()` (parse + compile, no execution), `verify_source()`/`verify_file()` (parse + compile + Lean 4 formal verification), `run_source()`/`run_file()` (parse + compile + execute). All functions return typed `EvalResult` objects and never raise -- errors are captured in the result.
- `_repl.py`: Interactive REPL session (`lu repl`). `REPLSession` class with stateful multiline input, colon-prefixed commands (`:help`, `:quit`, `:reset`, `:history`, `:check`), readline integration (stdlib, zero deps). Supports `NO_COLOR`/`FORCE_COLOR` via `_colors`.
- `_cli.py`: CLI entry point `lu`. Subcommands: `run <file.lu>`, `check <file.lu>`, `verify <file.lu>`, `compile <file.lu>`, `repl`, `lsp`, `version`. Built on `argparse` (stdlib, zero deps). Console script: `lu = cervellaswarm_lingua_universale._cli:main`.

**Ecosystem - Phase D: Language Server Protocol (D2)**
- `_lsp.py`: LSP server for Lingua Universale. Real-time diagnostics in editors via `textDocument/didOpen`, `didChange`, `didSave`. Converts `TokenizeError`/`ParseError` to LSP `Diagnostic` objects via `humanize()`. STDIO transport, launched via `lu lsp`. Optional dependency: `pygls` (`pip install cervellaswarm-lingua-universale[lsp]`).

**Developer Experience**
- `errors.py`: Human-friendly error messages (already shipped in v0.1.1; error codes now extended to cover the C1 pipeline). New error code range `LU-N` for `_tokenizer`/`_parser` syntax errors.
- `_colors.py`: Shared ANSI terminal color state for CLI and REPL. Respects `NO_COLOR`, `FORCE_COLOR`, and `CLICOLOR_FORCE` environment variables. `init_colors()` / `colors` singleton. Zero external dependencies.

### Changed

- **Module count**: 14 -> 26 modules
- **Public symbols**: 110 -> 131 symbols exported via `__init__.py`
- **Test count**: 1820 -> 2828 tests, 98% coverage maintained
- **Package description**: updated from "session types library" to reflect the full programming language (tokenizer, parser, compiler, REPL, CLI, LSP)
- **Keywords**: added `programming-language`, `compiler`, `vericoding`, `constrained-decoding`
- **CLI entry point**: new `lu` console script added to `pyproject.toml`

## [0.1.1] - 2026-02-25

### Added

**Error messages (errors.py)**
- `humanize()`: convert `ProtocolViolation` to human-readable `HumanError`
- `format_error()`: Elm/Rust-style error formatting with suggestions
- `SUPPORTED_LOCALES`: multi-language support (en, it, pt)
- Verbose mode with contextual suggestions for fixing violations

**Spec language (spec.py)**
- `parse_spec()`: natural language property specification parser
- `check_properties()`: static structural verification of protocols
- `PropertyVerdict`: PROVED / VIOLATED / UNKNOWN verdicts with evidence
- Properties: `always_terminates`, `no_deadlock`, `all_roles_participate`

**Code generation (codegen.py)**
- `generate_python()`: Protocol to Python stub generation
- `generate_python_multi()`: batch generation for multiple protocols

**Intent parser (intent.py)**
- `parse_intent()`: natural language to Protocol conversion
- Pattern matching for common protocol descriptions

### Changed

- Expanded `__init__.py` re-exports: 84 -> 110 public symbols
- Updated test count: 1273 -> 1820 tests, 98% coverage maintained

### Fixed

- Colab notebook compatibility: all 14 modules now importable from PyPI

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

[0.2.0]: https://github.com/rafapra3008/cervellaswarm/releases/tag/lingua-universale-v0.2.0
[0.1.1]: https://github.com/rafapra3008/cervellaswarm/releases/tag/lingua-universale-v0.1.1
[0.1.0]: https://github.com/rafapra3008/cervellaswarm/releases/tag/lingua-universale-v0.1.0
