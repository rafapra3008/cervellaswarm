# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-02-27 - Sessione 418
> **STATUS:** C2.3 COMPLETO! STUDIO C2.4 scritto. Prossimo: C2.4.1 LLM Grammar design.

---

## SESSIONE 418 - Cosa e successo

### C2.3.5 -- Golden interop tests + @dataclass fix (Guardiana 9.5/10)

- 36 end-to-end test (I1-I10), P1 CRITICO `sqrt(4)==2.0` PASSA
- BUG TROVATO: `@dataclass` richiede `sys.modules` -> sentinel save/restore fix
- Guardiana: 0 P0/P1, 1 P2 fixato, 6 P3

### C2.3.6 -- Audit finale (Guardiana 9.5/10)

- `__init__.py` aggiornato con 5 nuove API interop, C2.3 APPROVED

### STUDIO C2.4 -- Constrained Generation Export

- Ricerca 12 fonti: XGrammar, llguidance, Outlines, GBNF, lm-format-enforcer, cloud APIs
- **Decisione:** export GBNF (vLLM/XGrammar/llama.cpp) + Lark (Outlines/llguidance) = 95% ecosistema
- **Problema critico:** INDENT/DEDENT -> risolto con "LLM Grammar" whitespace-lenient
- 4 sub-step pianificati, ~2.5 sessioni stimate, 0 nuove deps runtime

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
      C2.3 Python interop   DONE! 6/6 (S416-S418, media 9.5/10)
      C2.4 Constrained gen  STUDIO DONE, implementazione TODO
        C2.4.1 LLM Grammar design   TODO  <-- PROSSIMO
        C2.4.2 GrammarExporter impl  TODO
        C2.4.3 Validation tests      TODO
        C2.4.4 Guardiana audit        TODO
    C3: L'Esperienza     [....................] 0%
```

---

## I NUMERI TOTALI (dopo S418)

| Metrica | Valore |
|---------|--------|
| Test totali | **2600** |
| Test passanti | 2600 (100%) |
| Coverage _compiler.py | **100%** (305 stmts) |
| Coverage _interop.py | **100%** (70 stmts) |
| Regressioni | 0 |

---

## PIANO C2.4 -- Prossimi step

**Leggi PRIMA:** `.sncp/progetti/cervellaswarm/reports/STUDIO_C2_4_CONSTRAINED_GENERATION.md`

### C2.4.1 -- LLM Grammar design (0.5 sessione, BASSO)
- Scrivere ~50 regole whitespace-lenient (no INDENT/DEDENT)
- Decidere verb/noun: closed list vs open IDENT

### C2.4.2 -- GrammarExporter implementation (1 sessione, MEDIO)
- Nuovo file `_grammar_export.py`, classe `GrammarExporter`
- `to_gbnf() -> str` (XGrammar/vLLM/llama.cpp)
- `to_lark() -> str` (Outlines/llguidance)
- ~200-300 LOC, regole codificate staticamente

### C2.4.3 -- Validation tests (0.5 sessione, BASSO)
- `test_grammar_export.py`, ~15-25 test
- Lark parsability, GBNF structure, round-trip con parser
- Dipendenza test-only: `lark`

### C2.4.4 -- Guardiana audit (0.5 sessione)

**Formati target:**
- **GBNF** = `root ::= program` + regole con `ws` per whitespace
- **Lark** = `start: declaration+` + regole con regex terminali

---

## Lezioni Apprese (S418)

### Cosa ha funzionato bene
- Golden tests trovano bug reali (@dataclass + sys.modules)
- "Guardiana dopo ogni step" (24a volta consecutiva)
- STUDIO prima di implementare: ricerca 12 fonti ha chiarito panorama completo

### Pattern confermato
- **"I golden test scoprono bug che i unit test non vedono"** (S415, S418)

---

## File chiave

- `_compiler.py` ~750 LOC | `_interop.py` ~350 LOC | `_contracts.py` 61 LOC
- `test_interop.py` 58 test | `test_interop_golden.py` 36 test
- `test_compiler_core.py` 119 test | `test_compiler_golden.py` 52 test
- **STUDIO C2.4:** `.sncp/progetti/cervellaswarm/reports/STUDIO_C2_4_CONSTRAINED_GENERATION.md`
- **Grammatica EBNF:** `.sncp/progetti/cervellaswarm/reports/DESIGN_C1_2_SYNTAX_GRAMMAR.md`

*"La domanda e la risposta nello STESSO linguaggio." - Rafa*
*"Ultrapassar os proprios limites!" - Rafa & Cervella*
