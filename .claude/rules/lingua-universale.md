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
- `_errors.py` - 74 error codes (LU-E001 a LU-E074)

## LSP Architecture (D2 + D5)
- Pure functions separated from server handlers (testable without LSP client)
- `build_symbol_table()` - AST -> dict[name, SymbolEntry] with regex fallback
- `_hover_info()`, `_goto_definition()`, `_completion_items()` - pure functions
- Coordinate: LU 1-indexed line -> LSP 0-indexed (`lsp_line = lu_line - 1`)

## Convenzioni
- Error codes: `LU-EXXX` con severity (error/warning/info)
- Test: `pytest packages/lingua-universale/tests/` (2900 test)
- Ogni modifica -> test -> Guardiana audit
- MAI rompere backward compatibility senza versione major

## Fase Corrente
- FASE D: L'Ecosistema -- COMPLETA! D1-D6 DONE (media 9.5/10)
- Subroadmap: `.sncp/roadmaps/SUBROADMAP_FASE_D_ECOSISTEMA.md`
- Test: 2900 (LU), 4887 (totale 9 pkg)
