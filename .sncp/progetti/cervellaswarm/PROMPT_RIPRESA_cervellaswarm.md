# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-02-27 - Sessione 418
> **STATUS:** C2.3.5 DONE! Prossimo: C2.3.6 audit finale (ultimo step C2.3).

---

## SESSIONE 418 - Cosa e successo

### C2.3.5 -- Golden interop tests + @dataclass fix (Guardiana 9.5/10)

- Nuovo file `test_interop_golden.py` -- 35 end-to-end test (I1-I10)
- I1 variant, I2 record, I3 `use python math` (P1 CRITICO: `sqrt(4)==2.0` PASSA!), I4-I6 contracts, I7 protocol, I8 save+import, I9 multi-module, I10 __all__
- **BUG TROVATO:** `@dataclass(frozen=True)` in Python 3.13 richiede `sys.modules[cls.__module__].__dict__` -- `load_module` non registrava in sys.modules, crash su tutti i record type
- **FIX:** Sentinel save/restore pattern: `load_module` registra temporaneamente in sys.modules durante exec(), poi ripristina il valore precedente (safe per nomi che collidono con stdlib)
- Guardiana: 0 P0/P1, 1 P2 (fixato: sentinel restore testato), 6 P3 (F4 fixato: multi-contract violation, F6 fixato: docstring aggiornata)
- +35 test (93 interop totali), 100% coverage su _interop.py (70 stmts)

---

## MAPPA SITUAZIONE

```
LINGUAGGIO CERVELLASWARM:
  FASE A+B: COMPLETE (13 moduli, 1820 test, 9.5+ media)
  FASE C: Il Linguaggio
    C1: La Grammatica    [####################] 100% DONE!
    C2: Il Compilatore   [###################.] 97%
      C2.1 STUDIO           DONE (S412, 9.3/10)
      C2.2 AST -> Python    DONE! 7/7 (S413-S415, media 9.5/10)
      C2.3 Python interop   IN PROGRESS (5/6 done)
        C2.3.1 hardening       DONE (S416, 9.6/10)
        C2.3.2 __all__ + meta  DONE (S416, 9.5/10)
        C2.3.3 compile_file    DONE (S417, 9.5/10)
        C2.3.4 load_module     DONE (S417, 9.5/10)
        C2.3.5 golden interop  DONE (S418, 9.5/10)
        C2.3.6 audit finale    TODO  <-- PROSSIMO
      C2.4 Constrained gen  TODO
    C3: L'Esperienza     [....................] 0%
```

---

## I NUMERI TOTALI (dopo S418)

| Metrica | Valore |
|---------|--------|
| Test totali | 2599 |
| Test passanti | 2599 (100%) |
| Coverage _compiler.py | **100%** (305 stmts) |
| Coverage _interop.py | **100%** (70 stmts) |
| Test compiler+interop | 382 (core 119, agent 43, protocol 43, golden 52, contracts 32, interop 58, interop_golden 35) |
| Regressioni | 0 |

---

## PIANO C2.3 -- Prossimo step

**Prossimo: C2.3.6 -- Audit finale**
- Update `__init__.py` con nuove API interop (InteropError, compile_file, save_module, load_module, load_file)
- Guardiana audit finale su tutto C2.3
- Target: 9.5/10
- **Effort:** 0.5 sessione | **Rischio:** BASSO

**Report completo:** `.sncp/progetti/cervellaswarm/reports/STUDIO_C2_3_PYTHON_INTEROP.md`

---

## Lezioni Apprese (S418)

### Cosa ha funzionato bene
- Golden interop tests hanno trovato un BUG REALE (@dataclass + sys.modules) -- esattamente perche servono: i test unitari non lo scoprivano perche SIMPLE_VARIANT non usa @dataclass. I golden test end-to-end con record types lo hanno esposto.
- "Guardiana dopo ogni step" (24a volta consecutiva): P2 trovato (sentinel restore non testato), fixato subito. Pattern consolidato.
- Fix proattivo dei P3 post-audit: multi-contract violation tests, docstring migliorata. Qualita incrementale.

### Cosa non ha funzionato
- Nessun problema questa sessione. Il piano era chiaro, lo step era BASSO rischio come previsto.

### Pattern candidato
- **"I golden test scoprono bug che i unit test non vedono"** -- Evidenza: S418 (@dataclass), S415 (metadata ordering). Azione: CONFERMATO. Always write golden tests per pipeline end-to-end.

---

## File chiave

- `_compiler.py` - ~750 LOC, 100% coverage, 305 stmts (pure string generation)
- `_interop.py` - ~350 LOC, 100% coverage, 70 stmts (I/O + runtime + sys.modules sentinel)
- `_contracts.py` - 61 LOC, ContractViolation
- `test_interop.py` - 58 test (compile_file, save_module, load_module, load_file)
- `test_interop_golden.py` - 35 test (I1-I10 end-to-end pipeline)
- `test_compiler_core.py` - 119 test (core + hardening + metadata + __all__)
- `test_compiler_golden.py` - 52 golden tests (round-trip + metadata)
- `STUDIO_C2_3_PYTHON_INTEROP.md` - piano completo C2.3

*"La domanda e la risposta nello STESSO linguaggio." - Rafa*
*"Ultrapassar os proprios limites!" - Rafa & Cervella*
