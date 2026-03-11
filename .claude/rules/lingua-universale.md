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
- `_errors.py` - 74 error codes (LU-E001 a LU-E074)

## LSP Architecture (D2 + D5)
- Pure functions separated from server handlers (testable without LSP client)
- `build_symbol_table()` - AST -> dict[name, SymbolEntry] with regex fallback
- `_hover_info()`, `_goto_definition()`, `_completion_items()` - pure functions
- Coordinate: LU 1-indexed line -> LSP 0-indexed (`lsp_line = lu_line - 1`)

## Convenzioni
- Error codes: `LU-EXXX` con severity (error/warning/info)
- Test: `pytest packages/lingua-universale/tests/` (3179 test)
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
- CLI: `lu chat --lang it|pt|en [--mode guided|nl]`
- NL mode: NLProcessor(Protocol) -> ClaudeNLProcessor (anthropic tool_use)
- TOOL_SCHEMA constrains Claude output: action_key enum, properties enum
- _build_draft() validates all fields with detailed error messages

## Fase Corrente
- FASE E: Per Tutti (IntentBridge) -- IN PROGRESS (E.1 DONE, E.2 DONE 9.5/10, E.3 IN PROGRESS)
- Subroadmap: `.sncp/roadmaps/SUBROADMAP_FASE_E_INTENTBRIDGE.md`
- FASE D: L'Ecosistema -- COMPLETA! D1-D6 DONE (media 9.5/10)
- Test: 3161 (LU), ~5473 (totale)
