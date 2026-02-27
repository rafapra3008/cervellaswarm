# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-02-27 - Sessione 422
> **STATUS:** C3.2 DONE + C3.3 DONE. Prossimo: C3.4 REPL interattivo.

---

## SESSIONE 422 - Cosa e successo

### C3.2 CLI + eval -- COMPLETATO (Guardiana 9.5/10)

**Audit Guardiana:** 9.5/10, 0 P0, 0 P1, 2 P2 fixati.

**Fix applicati:**
- **F1 (P2):** `run_file()` allineato a `check_file()`/`verify_file()` -- stesso pattern DRY: leggi file -> delega a `*_source()`. Rimosso import `compile_file` non piu necessario.
- **F2 (P2):** `_protocol_node_to_lean4()` ora mappa `StepNode.action` al `MessageKind` corretto (`asks`->TASK_REQUEST, `returns`->TASK_RESULT, `sends`->DM, `tells`->BROADCAST, `proposes`->PLAN_PROPOSAL) invece di hardcodare TASK_REQUEST.
- **F8 (P3):** `_cmd_compile()` gestisce `PermissionError`/`OSError` su `-o` output.
- **+4 test:** frozen immutability, stdout check, stdout run, bad compile path.

### C3.3 Error messages -- COMPLETATO (Guardiana 9.3/10)

**Ricerca:** 38 fonti esterne (Rust rustc-dev-guide, Elm "Compiler Errors for Humans", Gleam v1.6, Roc, Python 3.14 PEP 657).
**Gap Analysis:** Ingegnera ha mappato 8 gap (G1-G8). Insight chiave: le info di location (line+col) ESISTONO gia in ogni token e AST node. Il lavoro era di COLLEGAMENTO, non di costruzione.

**Cosa e stato costruito:**
1. **`render_snippet()`** (~50 LOC) -- generatore snippet stile Rust/Elm con numeri riga, gutter, caret `^`, label, context lines
2. **12 codici LU-N001..N012** nel catalogo trilingue (en/it/pt):
   - N001 tab, N002 bad indent, N003 unterminated string, N004 unexpected char, N005 dedent mismatch
   - N006 unknown top-level keyword, N007 generic expected/got, N008 missing colon
   - N009 empty protocol, N010 unknown step action, N011 unknown property, N012 unknown agent clause
3. **`ErrorCategory.SYNTAX`** -- nuova categoria per pipeline C1
4. **`_classify_tokenize_error()`** + **`_classify_parse_error()`** -- classifier pattern-matching
5. **`_parser_similar()`** -- fuzzy matching per N006/N010/N011/N012 (keywords, actions, properties, agent clauses)
6. **`humanize()`** -- nuovi branch per TokenizeError e ParseError (prima di tutti gli altri match)
7. **`format_error(source="")`** -- nuovo parametro opzionale per snippet rendering
8. **`_eval.py` integrato** -- `_parse_and_compile()` ora usa `humanize()` + `format_error(source=source)` con fallback

**Audit Guardiana:** 9.3/10, 0 P0, 0 P1, 2 P2 fixati.
- **F1 (P2):** `_parser_similar` N011 aveva "all messages received" (non esiste) -> corretto con le 7 property reali del parser
- **F2 (P2):** catalogo LU-N011 hint incompleto (4 proprieta su 7) -> corretto con tutte e 7
- **F3-F8 (P3):** docstring humanize aggiornata, docstring test corretta, render_snippet edge case col>len(riga) fixato

**Report ricerca:** `.sncp/progetti/cervellaswarm/reports/RESEARCH_20260227_C3_error_messages_deep.md`

---

## MAPPA SITUAZIONE

```
LINGUAGGIO CERVELLASWARM:
  FASE A+B: COMPLETE (13 moduli, 1820 test, 9.5+ media)
  FASE C: Il Linguaggio
    C1: La Grammatica    [####################] 100% DONE!
    C2: Il Compilatore   [####################] 100% DONE!
    C3: L'Esperienza     [############........] ~50%
      C3.1 STUDIO             DONE (S421, 9.3/10)
      C3.2 CLI + eval         DONE (S422, 9.5/10)
      C3.3 Error messages     DONE (S422, 9.3/10)
      C3.4 REPL interattivo   TODO
      C3.5 File .lu + showcase TODO
      C3.6 Guardiana finale   TODO
```

---

## I NUMERI TOTALI (dopo S422)

| Metrica | Valore |
|---------|--------|
| Test totali | **2724** (+42 da S421) |
| Test passanti | 2724 (100%) |
| Moduli .py nel package | 23 |
| File .lu di esempio | 1 (examples/hello.lu) |
| Codici errore LU | **72** (60 + 12 LU-N) |
| Locali errori | 3 (en, it, pt) |
| Regressioni | 0 |
| Tempo suite | 0.86s |
| Guardiana audit S422 | 2 (C3.2: 9.5/10, C3.3: 9.3/10) |

---

## PROSSIMO: C3.4 REPL interattivo

1. **STUDIO** -- ricerca REPL design (Python, IPython, Elixir IEx, Gleam, Deno)
2. **Implementare `_repl.py`** -- REPLSession class con:
   - `lu repl` subcommand (da aggiungere a _cli.py)
   - Prompt `lu>` con readline/stdin
   - Valutazione incrementale (check, run, verify inline)
   - History + multiline input
   - Colori TTY-aware (riusa _cli.py pattern)
3. **Test** -- pytest con capsys/monkeypatch per stdin
4. **Guardiana audit** -- target 9.5/10

Decisioni architetturali gia prese (STUDIO C3.1 S421):
- D2: stdlib REPL (readline/cmd, ZERO deps)
- D4: REPLSession class stateful

Poi: C3.5 File .lu + showcase v2, C3.6 Guardiana finale

---

## File chiave (C3.2 + C3.3)

- **errors.py** (~1900 righe) -- +12 codici LU-N, render_snippet, humanize per TokenizeError/ParseError
- **_eval.py** (~270 righe) -- integrato con humanize(), run_file DRY fix
- **_cli.py** (~235 righe) -- compile -o error handling
- **test_errors_c33.py** (36 test) -- snippet, codici, integration
- **test_eval.py** (+1 test frozen) -- EvalResult immutability
- **test_cli.py** (+3 test) -- stdout check, stdout run, bad compile path
- **RICERCA C3.3:** `.sncp/progetti/cervellaswarm/reports/RESEARCH_20260227_C3_error_messages_deep.md`

---

## Lezioni Apprese (S422)

### Cosa ha funzionato bene
- **2 Cervelle parallele per STUDIO** (Researcher + Ingegnera) -- completate in 5 min parallelo, output complementari (38 fonti + 8 gap)
- **Audit -> Fix -> Re-audit** ha portato 9.3 -> 9.3 con fix mirati (nessun re-audit necessario, fix erano chirurgici)
- **Classifier pattern in errors.py** -- estendibile senza rompere nulla. Aggiungere TokenizeError/ParseError ha richiesto solo nuovi branch

### Cosa non ha funzionato
- **`_extract_quoted` prendeva la PRIMA** quoted string dal messaggio ParseError, non quella dopo "got". Fix: regex specifico `r"got\s+'([^']+)'"` per N006

### Pattern confermato
- **"Research First + Guardiana dopo step" (28a volta consecutiva)** -- il metodo funziona

---

*"La domanda e la risposta nello STESSO linguaggio." - Rafa*
*"Ultrapassar os proprios limites!" - Rafa & Cervella*
