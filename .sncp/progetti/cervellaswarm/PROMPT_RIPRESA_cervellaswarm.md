# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-02-27 - Sessione 421
> **STATUS:** C3.1 STUDIO DONE + C3.2 CLI+eval IN PROGRESS (implementazione completa, Guardiana audit pending).

---

## SESSIONE 421 - Cosa e successo

### C3.1 STUDIO -- L'Esperienza (Guardiana 9.3/10)

- **Ricerca:** 42 fonti esterne (Gleam, Elm, Rust, Python 3.14, Unison, Roc, Deno, Cargo)
- **Gap analysis:** Ingegnera ha mappato 6 gap (G1-G6) con complessita S/M/L
- **Insight chiave:** la pipeline parse -> compile -> execute GIA FUNZIONA
- **5 decisioni architetturali:** D1 argparse, D2 stdlib REPL, D3 errors.py esteso, D4 REPLSession, D5 .lu canonici
- **Guardiana:** 9.3/10, 0 P0, 0 P1, 3 P2 (tutti fixati: conteggio codici 35->60, SUBROADMAP/MAPPA allineate)
- **Report:** `.sncp/progetti/cervellaswarm/reports/STUDIO_C3_LESPERIENZA.md`
- **Ricerca:** `.sncp/progetti/cervellaswarm/reports/RESEARCH_20260227_C3_developer_experience.md`
- **Documenti satellite aggiornati:** SUBROADMAP C2->DONE C3 riallineata, MAPPA nota Fase C

### C3.2 CLI + eval -- IN PROGRESS (codice scritto, test passanti, audit pending)

**4 file nuovi creati:**
- `_eval.py` (~100 LOC) -- `check_source/file()`, `verify_source/file()`, `run_source/file()`, `EvalResult`
- `_cli.py` (~105 LOC) -- argparse con 5 subcommand: check, run, verify, compile, version
- `__main__.py` (~10 LOC) -- entry point `python -m cervellaswarm_lingua_universale`
- `examples/hello.lu` -- primo file `.lu` del mondo (type + agent + protocol + properties)

**2 file modificati:**
- `pyproject.toml` -- aggiunto `[project.scripts] lu = "cervellaswarm_lingua_universale._cli:main"`
- `__init__.py` -- aggiunto export EvalResult, check/verify/run_source/file, cli_main

**Test nuovi:** 45 (27 test_eval.py + 18 test_cli.py)

**Stato funzionale:**
- `lu check examples/hello.lu` -> OK, 1 agent, 1 protocol, 1 type
- `lu run examples/hello.lu` -> OK, modulo Python live con 21 export
- `lu verify examples/hello.lu` -> OK, Lean 4 source generated (1791 chars)
- `lu compile examples/hello.lu` -> stampa Python generato
- `lu version` -> "Lingua Universale v0.1.0"
- Errori gestiti: file not found (exit 1), syntax error (exit 1 + messaggio)
- Coverage _eval.py: 90%, Coverage _cli.py: 90%

**MANCA per completare C3.2:**
- Guardiana audit C3.2 (target 9.5/10)
- Fix eventuali P1/P2 dall'audit

---

## MAPPA SITUAZIONE

```
LINGUAGGIO CERVELLASWARM:
  FASE A+B: COMPLETE (13 moduli, 1820 test, 9.5+ media)
  FASE C: Il Linguaggio
    C1: La Grammatica    [####################] 100% DONE!
    C2: Il Compilatore   [####################] 100% DONE!
    C3: L'Esperienza     [#####...............] ~25%
      C3.1 STUDIO             DONE (S421, 9.3/10)
      C3.2 CLI + eval         IN PROGRESS (codice+test ok, audit pending)
      C3.3 Error messages     TODO
      C3.4 REPL interattivo   TODO
      C3.5 File .lu + showcase TODO
      C3.6 Guardiana finale   TODO
```

---

## I NUMERI TOTALI (dopo S421)

| Metrica | Valore |
|---------|--------|
| Test totali | **2682** (+45 da S420) |
| Test passanti | 2682 (100%) |
| Moduli .py nel package | 23 (20 + _eval.py, _cli.py, __main__.py) |
| File .lu di esempio | 1 (examples/hello.lu) |
| Regressioni | 0 |
| Guardiana audit S421 | 1 (C3.1 STUDIO 9.3/10) |

---

## PROSSIMO: Completare C3.2

1. **Guardiana audit C3.2** -- audit `_eval.py` + `_cli.py` + `test_eval.py` + `test_cli.py`
2. **Fix P1/P2** dall'audit
3. **Commit** con tutti i file C3.2

Poi: C3.3 Error messages C1-C2 (estendere errors.py per ParseError, TokenizeError, etc.)

---

## File chiave

- **STUDIO C3:** `.sncp/progetti/cervellaswarm/reports/STUDIO_C3_LESPERIENZA.md`
- **RICERCA C3:** `.sncp/progetti/cervellaswarm/reports/RESEARCH_20260227_C3_developer_experience.md`
- **Nuovi:** `_eval.py`, `_cli.py`, `__main__.py`, `examples/hello.lu`
- **Modificati:** `pyproject.toml` (console script), `__init__.py` (export)
- **Test nuovi:** `test_eval.py` (27 test), `test_cli.py` (18 test)

---

## Lezioni Apprese (S421)

### Cosa ha funzionato bene
- 2 agenti in parallelo (Researcher + Ingegnera) per ricerca e gap analysis
- Bug trovati SUBITO durante test manuale: `MessageKind.REQUEST` (non esiste), `steps` vs `elements`, `message_type` vs `message_kind`. Testare a mano PRIMA dei test automatici salva tempo
- Refactor `_parse_and_compile()` helper ha eliminato duplicazione parse in verify_source

### Cosa non ha funzionato
- 3 fix consecutivi in `_protocol_node_to_lean4()` per campi sbagliati. Lezione: leggere SEMPRE la signature del target dataclass PRIMA di costruire l'oggetto

### Pattern confermato
- **"Research First + Guardiana dopo step" (27a volta consecutiva)** -- il metodo e solido

---

*"La domanda e la risposta nello STESSO linguaggio." - Rafa*
*"Ultrapassar os proprios limites!" - Rafa & Cervella*
