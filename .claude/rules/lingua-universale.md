---
paths:
  - packages/lingua-universale/**
---

# Lingua Universale - Regole Sviluppo

## Architettura
- 3 pilastri: Incertezza come tipo, Fiducia componibile, Protocolli auto-verificanti
- Compilatore: LU source -> Python AST -> exec
- Pipeline: lexer -> parser -> compiler -> runtime
- NORD completo: `packages/lingua-universale/NORD.md`

## Struttura Package
- `_grammar.py` - Grammatica Lark (EBNF)
- `_parser.py` - Parser LU -> AST
- `_compiler.py` - AST -> Python code
- `_runtime.py` - Runtime con UncertainValue, TrustLevel
- `_lsp.py` - Language Server Protocol (diagnostics + hover + completion + go-to-def)
- `_intent_bridge.py` - IntentBridge: guided + NL chat protocol builder (E.2+E.3)
- `_nl_processor.py` - ClaudeNLProcessor: NL -> IntentDraft via tool_use (E.3, optional dep)
- `_voice.py` - VoiceProcessor: mic capture + STT via faster-whisper (E.4, optional dep)
- `_errors.py` - 74 error codes (LU-E001 a LU-E074)
- `spec.py` - 9 PropertyKind (E.5: +NO_DELETION, +ROLE_EXCLUSIVE), static+runtime checkers

## LSP Architecture (D2 + D5)
- Pure functions separated from server handlers (testable without LSP client)
- `build_symbol_table()` - AST -> dict[name, SymbolEntry] with regex fallback
- `_hover_info()`, `_goto_definition()`, `_completion_items()` - pure functions
- Coordinate: LU 1-indexed line -> LSP 0-indexed (`lsp_line = lu_line - 1`)

## Convenzioni
- Error codes: `LU-EXXX` con severity (error/warning/info)
- Test: `pytest packages/lingua-universale/tests/` (3684 test)
- Ogni modifica -> test -> Guardiana audit
- MAI rompere backward compatibility senza versione major

## IntentBridge Architecture (E.2+E.3)
- Two-stage pattern (Req2LTL): guided/NL input -> IntentDraft (IR) -> B.4 source
- ChatSession: mutable state machine with injectable I/O (same as REPLSession)
- render_intent_source(): deterministic IntentDraft -> B.4 intent notation
- Pipeline: guided/NL input -> IntentDraft -> parse_intent() -> check_properties() -> generate_python()
- i18n: 3 locales (en/it/pt) via _STRINGS dict (same pattern as errors.py)
- _SIM_NARRATIVES: narrative descriptions per MessageKind x 3 lingue (simulation output)
- Simulation: shows ALL branches (not just first), narrative in target language
- Violation demo (R20): _render_violation_demo() shows blocked attempts for proved properties
  - Supports NO_DELETION (delete attempt blocked) and ROLE_EXCLUSIVE (wrong role blocked)
  - Output narrativo in 3 lingue, integrated after simulation in pipeline step 5b
- CLI: `lu chat --lang it|pt|en [--mode guided|nl] [--voice] [--voice-model small|turbo|...]`
- NL mode: NLProcessor(Protocol) -> ClaudeNLProcessor (anthropic tool_use)
- TOOL_SCHEMA constrains Claude output: action_key enum, properties enum
- _build_draft() validates all fields with detailed error messages

## Voice Architecture (E.4)
- VoiceProcessor: Callable[[str], str] -- drop-in for input()
- Integration via input_fn injection on ChatSession (ZERO changes to _intent_bridge.py)
- Push-to-talk: ENTER to start, ENTER to stop
- STT: faster-whisper "small" (default), lazy model loading (~466MB download once)
- i18n: recording/transcription messages in 3 locales (en/it/pt)
- Optional dep: `pip install cervellaswarm-lingua-universale[voice]`
- Thread safety: sounddevice callback + threading.Event for push-to-talk flow
- Stream cleanup in try/finally after start()

## Fase Corrente
- FASE E: Per Tutti (IntentBridge) -- IN PROGRESS (E.1-E.5 DONE, E.6 IN PROGRESS)
- E.6 CervellaLang 1.0: T3.1-T3.4 DONE (S444-S445), LU 1.1 Nested Choice DONE (S447)
- LU 1.1: `when X decides:` inside branches. Parser recursive, MAX_CHOICE_DEPTH=32
- LU 1.2: SessionChecker stack-based ChoiceFrame for nested runtime tracking
- `lu demo`: autonomous scripted demo (3 lingue, 3 speed, typewriter effect, injected I/O)
- Subroadmap: `.sncp/roadmaps/SUBROADMAP_FASE_E_INTENTBRIDGE.md`
- Task list dettagliata: `.sncp/roadmaps/SUBROADMAP_E5_E6_FUTURO.md`
- FASE D: L'Ecosistema -- COMPLETA! D1-D6 DONE (media 9.5/10)
- B5 `lu lint`: 10 rules, single-pass AST walk (Ruff/Clippy pattern), LSP+CI integrated
- B6 `lu fmt`: zero-config auto-formatter, gofmt/buf pattern, LSP+CI integrated
- `lu lint/fmt`: multi-path support (nargs="+"), dedup via dict.fromkeys()
- Pre-commit: section 5 checks lu fmt --check + lu lint on staged .lu files
- CI: lint-format job runs before test matrix (fast fail on style)
- Test: 3684 (LU), PyPI v0.3.3 LIVE
