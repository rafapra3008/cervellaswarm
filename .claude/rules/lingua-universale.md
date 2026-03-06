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
- `_lsp.py` - Language Server Protocol
- `_errors.py` - 74 error codes (LU-E001 a LU-E074)
- `_symbols.py` - 131 symbols table

## Convenzioni
- Error codes: `LU-EXXX` con severity (error/warning/info)
- Test: `pytest packages/lingua-universale/tests/` (2856 test)
- Ogni modifica -> test -> Guardiana audit
- MAI rompere backward compatibility senza versione major

## Fase Corrente
- FASE D: L'Ecosistema (D1-D4 DONE, D5 LSP Avanzato PROSSIMO)
- Subroadmap: `.sncp/roadmaps/SUBROADMAP_FASE_D_ECOSISTEMA.md`
