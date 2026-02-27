# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-02-27 - Sessione 413
> **STATUS:** C2.2 in corso. C2.2.1-C2.2.3 DONE. Prossimo: C2.2.4 _compile_agent.

---

## SESSIONE 413 - Cosa e successo

### 3 sub-step completati, 3 audit Guardiana, tutti sopra target

**C2.2.1 - `_contracts.py` (9.6/10)**
- `ContractViolation(RuntimeError)` con `condition`, `kind`, `source`
- `kind` keyword-only (evita inversioni), validazione boundary (P12)
- `__slots__` + `__reduce__` per pickling corretto
- 32 test, 100% coverage, 0 P0/P1/P2

**C2.2.2 - `_compiler.py` core scaffold (9.5/10)**
- `CompiledModule` frozen dataclass (result type)
- `ASTCompiler` con `compile()`, `_compile_declaration()` dispatch
- `_expr_to_python()`: tutti 8 tipi Expr con parentesizzazione sempre
- `_type_to_python()`: SimpleType/GenericType, `X | None` per optional (PEP 604)
- `_compile_use()`: UseNode -> import statement con `# [LU:line:col]`
- `_safe_ident()`: keyword escaping (pass -> pass_)
- Fix P2: `Optional[X]` -> `X | None` (zero import necessari nel generato)
- Fix P2: `_LU_GENERIC_MAP` alzato a costante modulo
- 78 test, 96% coverage (4 miss = stubs futuri)

**C2.2.3 - Type compilation (9.5/10)**
- `_compile_variant_type`: `type Status = A | B` -> `Status = Literal["A", "B"]`
- `_compile_record_type`: `type TaskData: ...` -> `@dataclass(frozen=True) class TaskData: ...`
- **Preamble import tracker**: `set[str]` in `compile()`, emette `from typing import Literal` etc.
- Campi opzionali: `str | None`, campi generici: `list[str]`, record vuoto: `pass`
- 93 test (era 78), 98% coverage (2 miss = stubs futuri)

---

## MAPPA SITUAZIONE

```
LINGUAGGIO CERVELLASWARM (la missione vera):
  FASE A+B: COMPLETE (13 moduli, 1820 test, 9.5+ media)
  FASE C: Il Linguaggio
    C1: La Grammatica    [####################] 100% DONE!
    C2: Il Compilatore   [########............] 40%
      C2.1 STUDIO           DONE (S412, 9.3/10)
      C2.2 AST -> Python    IN PROGRESS
        C2.2.1 _contracts.py   DONE (S413, 9.6/10)
        C2.2.2 _compiler core  DONE (S413, 9.5/10)
        C2.2.3 types           DONE (S413, 9.5/10)
        C2.2.4 agents          TODO  <-- PROSSIMO
        C2.2.5 protocols       TODO
        C2.2.6 golden tests    TODO
        C2.2.7 audit finale    TODO
      C2.3 Python interop   TODO
      C2.4 Constrained gen  TODO
    C3: L'Esperienza     [....................] 0%
```

---

## I NUMERI TOTALI (dopo S413)

| Metrica | Valore |
|---------|--------|
| Test totali | 2342 (+125 da S412) |
| Test passanti | 2342 (100%) |
| Coverage _contracts.py | 100% |
| Coverage _compiler.py | 98% |
| Coverage parser | 100% |
| File nuovi S413 | 4 (2 src + 2 test) |
| Tempo test suite | 0.57s |
| Regressioni | 0 |

---

## P2 aperti da risolvere

- **Confident[T] import**: `_LU_GENERIC_MAP` mappa `Confident` -> `Confident` ma nessun preamble import registrato. Serve `from cervellaswarm_lingua_universale.confidence import Confident` quando usato. Risolvere in C2.2.4.

---

## Lezioni Apprese (S413)

### Cosa ha funzionato bene
- "Guardiana dopo ogni step" (15a volta, S403-S413). 3 audit in una sessione, tutti 9.5+.
- "Fix P2 diamante subito" (4a volta): `Optional` -> `X | None` e mapping costante fixati tra C2.2.2 e C2.2.3.
- "Preamble import tracker": design semplice (set + sorted) che scala per C2.2.4-C2.2.5.
- "Pickle round-trip test": ha scovato il bug `__reduce__` subito in C2.2.1.

### Cosa non ha funzionato
- Dopo refactor `_type_to_python` (inline `_LU_GENERIC_MAP.get`), il metodo `_generic_to_python` e diventato dead code. Rilevato solo dal coverage check. Lezione: controllare coverage DOPO ogni refactor.

### Pattern candidato
- "Fix P2/P3 diamante prima di chiudere step" (4a volta, S411-S413): PROMUOVERE a P21? Evidenza: S411, S412x2, S413.

---

## Prossimi step

1. **C2.2.4** - `_compile_agent` (il cuore: contratti runtime + metadata). Include fix Confident[T] import.
2. **C2.2.5** - `_compile_protocol` (bridge a codegen.py)
3. **C2.2.6** - Golden file tests + round-trip exec per 10 esempi canonici
4. **C2.2.7** - Guardiana audit finale C2.2

---

## File chiave

- `packages/lingua-universale/src/cervellaswarm_lingua_universale/_contracts.py` - ContractViolation (C2.2.1)
- `packages/lingua-universale/src/cervellaswarm_lingua_universale/_compiler.py` - ASTCompiler (C2.2.2-C2.2.3)
- `packages/lingua-universale/tests/test_contracts.py` - 32 test
- `packages/lingua-universale/tests/test_compiler_core.py` - 93 test
- `.sncp/roadmaps/SUBROADMAP_FASE_C_LINGUAGGIO.md` - Piano FASE C
- `.sncp/progetti/cervellaswarm/reports/STUDIO_C2_1_ARCHITETTURA_COMPILATORE.md` - Architettura

*"La domanda e la risposta nello STESSO linguaggio." - Rafa*
*"Ultrapassar os proprios limites!" - Rafa & Cervella*
