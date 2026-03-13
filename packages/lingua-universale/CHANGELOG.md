# Changelog

All notable changes to `cervellaswarm-lingua-universale` will be documented in this file.

This project follows [Semantic Versioning](https://semver.org/).

## [0.3.2] - 2026-03-13

### Added

**LU 1.1 - Nested Choice (Parser/Compiler/Spec) (S447)**
- `when X decides:` inside branches of another `when Y decides:` -- arbitrarily deep nesting.
- Standard MPST/Scribble (Honda/Yoshida POPL 2008). Additive choice, zero breaking changes.
- Parser: `_parse_choice()` recursive, `MAX_CHOICE_DEPTH = 32`.
- Compiler: `_convert_elements()` recursive for ChoiceNode in codegen and _eval.
- Spec: `_collect_all_steps`, `_find_violating_steps`, `_collect_all_paths` all recursive.
- 29 new parser/compiler/spec tests.

**LU 1.2 - Nested Runtime (SessionChecker) (S447)**
- Stack-based `ChoiceFrame` in `SessionChecker` replaces flat `branch` + `branch_step_index`.
- `_current_elements()` returns elements from top-of-stack frame.
- `_peek_at()` recursive multi-level lookahead through choice stack.
- `_pop_exhausted_frames()` cascading frame pop with `while` loop.
- `summary()` exposes `choice_depth` and `branch_path`.
- Backward compatible: flat protocols = empty stack = identical behavior.
- 27 new runtime tests (2-level, 3-level, stack pop, violations, edge cases).

### Changed

- **Test count**: 3436 -> 3494 tests
- `saga_order.lu` stdlib: uses real nested choice (payment -> inventory decision).

### Fixed

- **P1**: `_eval.py:_protocol_node_to_runtime()` crashed on nested `.lu` files (`ChoiceNode` has no `.sender`). Fixed with recursive `_convert_elements()`.
- `_detect_branch()`: added `isinstance(steps[0], ProtocolStep)` check for nested-first branches.

## [0.3.1] - 2026-03-13

### Added

**IntentBridge - Phase E.5: "Per Tutti" (S438-S443)**
- `_intent_bridge.py`: ChatSession with 11-phase guided protocol builder. IntentDraft frozen IR. 3 locales (en/it/pt).
- `_nl_processor.py`: ClaudeNLProcessor -- NL to IntentDraft via Claude tool_use. TOOL_SCHEMA constrains output. Optional dep: `pip install ...[nl]`.
- `_voice.py`: VoiceProcessor -- push-to-talk mic capture + STT via faster-whisper. Optional dep: `pip install ...[voice]`.
- `lu chat` command: `--lang it|pt|en`, `--mode guided|nl`, `--voice`, `--voice-model`.
- `lu demo` command: autonomous scripted demo with typewriter effect, 3 speeds, 3 languages.
- Violation demo (R20): `_render_violation_demo()` shows blocked NO_DELETION and ROLE_EXCLUSIVE attempts.
- 2 new PropertyKind: `NO_DELETION` (no destructive operations), `ROLE_EXCLUSIVE` (only role X can send Y).
- Property explanation i18n: human-readable descriptions in 3 languages.
- Pipeline smoke tests: 3 classes, 6 tests covering flat/branched/4-property scenarios.

**CervellaLang 1.0 - Phase E.6 (S444-S445)**
- Grammar 1.0 RFC: 64 EBNF productions frozen. 32 hard + 10 soft keywords.
- Parser aligned to 9/9 PropertyKind (`NoDeletionProp`, `RoleExclusiveProp` AST nodes).
- Grammar export (GBNF + Lark) updated for 9 PropertyKind.
- `lu verify`: standalone CLI verification with colored per-property output (GREEN/RED/YELLOW).
- `lu init --template <name>`: scaffold project from stdlib template.
- `lu init --list-templates`: show 20 available stdlib templates.
- **Standard Library**: 20 verified protocols in 5 categories:
  - Communication (5): request_response, ping_pong, pub_sub, scatter_gather, pipeline
  - Data (3): crud_safe, data_sync, cache_invalidation
  - Business (4): two_buyer (MPST canonical), approval_workflow, auction, saga_order
  - AI/ML (5): rag_pipeline, agent_delegation, tool_calling, human_in_loop, consensus
  - Security (3): auth_handshake, mutual_tls, rate_limited_api
- All 9 PropertyKind covered across stdlib protocols.

### Changed

- **Module count**: 25 -> 29 modules
- **CLI commands**: 7 -> 10 (+ `chat`, `demo`, `verify` as standalone)
- **Test count**: 2909 -> 3436 tests
- **stdlib moved inside package**: `stdlib/` relocated from package root to `src/cervellaswarm_lingua_universale/stdlib/` for correct wheel distribution. Templates now work after `pip install`.
- Test stdlib files use `_STDLIB_DIR` import instead of fragile relative paths (DRY).

### Fixed

- **P1**: spec format was `spec NAME:` (wrong) instead of `properties for NAME:` (correct). Broken since S438, masked by silent try/except.
- **P1**: `result.property_name` attribute did not exist -- fixed to `result.spec.kind.value`.
- **P1**: stdlib `.lu` files were NOT included in PyPI wheel (path was outside `src/`).
- **P1**: `.gitignore` `data/` pattern blocked `stdlib/data/*.lu` files (negation pattern updated).
- Parser: `NoDeletionProp` and `RoleExclusiveProp` AST nodes added for 9/9 PropertyKind alignment.
- `_init_project.py`: `_find_template()` and `list_templates()` path resolution fixed for installed packages.

## [0.3.0] - 2026-03-06

### Added

**Ecosystem - Phase D: LSP Advanced (D5)**
- `_lsp.py`: Hover support — shows type, docstring, and trust tier on mouse hover. Markdown-formatted hover content.
- `_lsp.py`: Completion — context-aware suggestions for keywords, defined names, trust tiers, confidence levels. 7 completion contexts.
- `_lsp.py`: Go-to-definition — click on a type or agent name to jump to its definition. Symbol table with line/column tracking.
- `_lsp.py`: `build_symbol_table()` — AST-based symbol table with regex fallback for robustness.

**Testing**
- `test_colors.py`: 9 tests covering `_ColorState`, `init_colors()`, `reset_colors()`, and singleton behavior. Closes last test coverage gap.

### Changed

- **Refactoring**: `checker.send()` split from 168 lines into 4 private helpers (16-line orchestrator)
- **Refactoring**: `codegen.generate_python_multi()` split from 171 lines into 3 private helpers (43-line orchestrator)
- **Test count**: 2828 -> 2909 tests

### Fixed

- Tour: trust tiers corrected from "three" to "four", added `untrusted` tier
- SPDX license headers added to playground JS files
- VS Code extension README/CHANGELOG updated for D5 LSP features
- Stale test counts fixed across 5 documentation files (2806 -> 2900)

## [0.2.0] - 2026-02-28

### Added

**The Language - Phase C: Parsing Pipeline (C1)**
- `_tokenizer.py`: Unified lexer for Lingua Universale v0.2. Replaces the two inline tokenizers in `intent.py` and `spec.py`. 64-production EBNF grammar support, explicit INDENT/DEDENT tokens, paren-depth tracking for line continuation, 4-space indent enforcement, `textwrap.dedent` pre-processing. Zero external dependencies.
- `_ast.py`: Immutable frozen-dataclass AST node hierarchy for the 64-production grammar. Node families: `Expr` (8 types), `Property` (9 types), `Step/Choice` (3 types), `Protocol`, `Agent`, `Type` (5 types), `Use`, `Program`. All collections use `tuple` for hashability.
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

- **Module count**: 14 -> 25 modules
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

[0.3.2]: https://github.com/rafapra3008/cervellaswarm/releases/tag/lingua-universale-v0.3.2
[0.3.1]: https://github.com/rafapra3008/cervellaswarm/releases/tag/lingua-universale-v0.3.1
[0.3.0]: https://github.com/rafapra3008/cervellaswarm/releases/tag/lingua-universale-v0.3.0
[0.2.0]: https://github.com/rafapra3008/cervellaswarm/releases/tag/lingua-universale-v0.2.0
[0.1.1]: https://github.com/rafapra3008/cervellaswarm/releases/tag/lingua-universale-v0.1.1
[0.1.0]: https://github.com/rafapra3008/cervellaswarm/releases/tag/lingua-universale-v0.1.0
