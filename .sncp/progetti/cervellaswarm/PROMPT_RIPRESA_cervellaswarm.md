# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-02-27 - Sessione 414
> **STATUS:** C2.2 quasi completo! C2.2.1-C2.2.5 DONE. Prossimo: C2.2.6 golden tests.

---

## SESSIONE 414 - Cosa e successo

### 2 sub-step completati, 2 audit Guardiana, 4 P2 fixati

**C2.2.4 - `_compile_agent` (9.5/10)**
- Genera classe Python con `__lu_role__`, `__lu_trust__`, `__lu_accepts__`, `__lu_produces__`
- `process(**kwargs)` con `requires` -> precondition guards, `ensures` -> postcondition guards
- `_contract_expr_to_python()`: compila espressioni contract con `kwargs["name"]` lookup
- `_escape_contract_str()`: escape sicuro per messaggi errore
- Fix P2 Confident[T]: preamble import registrato per GenericType("Confident", ...)
- Fix P2 F1: MethodCallExpr args nei contract ora usano `_contract_expr_to_python` (non `_expr_to_python`)
- 47 test, 99% coverage (1 miss = stub protocol, poi risolto in C2.2.5)

**C2.2.5 - `_compile_protocol` bridge to codegen (9.3/10 -> fix -> ~9.5)**
- Pipeline: ProtocolNode AST -> Protocol runtime object -> PythonGenerator
- `_ast_to_protocol()`: trasforma StepNode -> ProtocolStep, ChoiceNode -> ProtocolChoice
- `_step_to_message_kind()`: euristica keyword-based (asks+verify -> AUDIT_REQUEST, etc.)
- Delega a PythonGenerator individual methods (proto_def, role_classes, session_class)
- Fix P2 F1: class name prefix per evitare collision multi-protocol (`DelegateTaskReginaRole`)
- Fix P2 F2: properties emesse come commenti nel codice generato
- Fix P3: return types corretti con TYPE_CHECKING block, docstring aggiornato
- 43 test (+ 2 regression per P2 fix)

**Coverage _compiler.py: 100%!** (289 statements, 0 miss -- prima volta!)

---

## MAPPA SITUAZIONE

```
LINGUAGGIO CERVELLASWARM (la missione vera):
  FASE A+B: COMPLETE (13 moduli, 1820 test, 9.5+ media)
  FASE C: Il Linguaggio
    C1: La Grammatica    [####################] 100% DONE!
    C2: Il Compilatore   [###############.....] 72%
      C2.1 STUDIO           DONE (S412, 9.3/10)
      C2.2 AST -> Python    5/7 DONE!
        C2.2.1 contracts      DONE (S413, 9.6/10)
        C2.2.2 core scaffold  DONE (S413, 9.5/10)
        C2.2.3 types          DONE (S413, 9.5/10)
        C2.2.4 agents         DONE (S414, 9.5/10)
        C2.2.5 protocols      DONE (S414, 9.3->~9.5)
        C2.2.6 golden tests   TODO  <-- PROSSIMO
        C2.2.7 audit finale   TODO
      C2.3 Python interop   TODO
      C2.4 Constrained gen  TODO
    C3: L'Esperienza     [....................] 0%
```

---

## I NUMERI TOTALI (dopo S414)

| Metrica | Valore |
|---------|--------|
| Test totali | 2427 (+85 da S413) |
| Test passanti | 2427 (100%) |
| Coverage _compiler.py | **100%** (289 stmts, 0 miss) |
| Coverage _contracts.py | 100% |
| Coverage parser | 100% |
| Test compiler totali | 178 (core 88 + agent 47 + protocol 43) |
| File nuovi S414 | 2 test (test_compiler_agent.py, test_compiler_protocol.py) |
| Tempo test suite | 0.57s |
| Regressioni | 0 |

---

## Lezioni Apprese (S414)

### Cosa ha funzionato bene
- "Fix P2 diamante subito" (6a volta, S411-S414): 4 P2 fixati immediatamente in questa sessione. **PROMUOVERE a P21 confermato.**
- "Guardiana dopo ogni step" (17a volta). Ha scovato il P2 della collision multi-protocol.
- "_contract_expr_to_python" separato da "_expr_to_python": design pulito per kwargs-aware contracts.
- Bridge to codegen.py con individual methods: riuso del PythonGenerator senza duplicare logica.

### Cosa non ha funzionato
- La euristica `_step_to_message_kind` puo dare falsi positivi (payload "planning the verification" -> PLAN_REQUEST). Accettabile per ora, ma potrebbe servire un meccanismo di override esplicito in futuro.
- Score C2.2.5 sotto target (9.3): la collision multi-protocol era un rischio reale non previsto.

---

## Prossimi step

1. **C2.2.6** - Golden file tests + round-trip exec per 10 esempi canonici
2. **C2.2.7** - Guardiana audit finale C2.2
3. **C2.3** - Python interop
4. **C2.4** - Constrained generation

---

## File chiave

- `packages/lingua-universale/src/cervellaswarm_lingua_universale/_compiler.py` - 707 LOC, 100% coverage
- `packages/lingua-universale/src/cervellaswarm_lingua_universale/_contracts.py` - ContractViolation
- `packages/lingua-universale/tests/test_compiler_core.py` - 88 test (core + types)
- `packages/lingua-universale/tests/test_compiler_agent.py` - 47 test (C2.2.4)
- `packages/lingua-universale/tests/test_compiler_protocol.py` - 43 test (C2.2.5)
- `.sncp/progetti/cervellaswarm/reports/STUDIO_C2_1_ARCHITETTURA_COMPILATORE.md`

*"La domanda e la risposta nello STESSO linguaggio." - Rafa*
*"Ultrapassar os proprios limites!" - Rafa & Cervella*

---

## AUTO-CHECKPOINT: 2026-02-27 13:20 (auto)

### Stato Git
- **Branch**: main
- **Ultimo commit**: 1398b664 - S413: C2.2.1-C2.2.3 Compilatore - contracts + core + types (3x Guardiana 9.5+)
- **File modificati** (5):
  - coverage
  - .sncp/progetti/cervellaswarm/PROMPT_RIPRESA_cervellaswarm.md
  - .sncp/progetti/contabilita/PROMPT_RIPRESA_contabilita.md
  - .sncp/progetti/miracollo/roadmaps/SUBROADMAP_RECAP_RINASCITA_2026.md
  - packages/lingua-universale/src/cervellaswarm_lingua_universale/_compiler.py

### Note
- Checkpoint automatico generato da hook
- Trigger: auto

---
