# STUDIO C3 - L'Esperienza

> **Data:** 2026-02-27 - Sessione 421
> **Autore:** Cervella Regina (sintesi) + Cervella Researcher (42 fonti) + Cervella Ingegnera (gap analysis)
> **Status:** APPROVED (Guardiana 9.3/10, 0 P0, 0 P1, 3 P2 fixati, 5 P3)
> **Input:** 20 moduli letti (2637 test), 42 fonti esterne, gap analysis completa
> **Zero nuove dipendenze runtime.**

---

## 1. DOVE SIAMO

### La pipeline FUNZIONA gia

```
Source .lu -> tokenize -> parse -> AST -> compile -> Python module -> execute
             (_tokenizer)  (_parser)  (_ast)  (_compiler)  (_interop)

+ _contracts.py     -- requires/ensures enforcement
+ _grammar_export.py -- GBNF/Lark per constrained decoding LLM
+ errors.py          -- 60 codici errore, 3 lingue (en/it/pt)
```

**Le 4 chiamate che fanno tutto:**

```python
ast = parse(source)                          # _parser.py
compiled = ASTCompiler().compile(ast)         # _compiler.py
module = load_module(compiled)               # _interop.py
# oppure one-liner:
module = load_file("example.lu")             # _interop.py
```

### Cosa MANCA per "l'esperienza"

| # | Gap | Stato | Complessita |
|---|-----|-------|-------------|
| G1 | CLI entry point (`lu` command) | MANCA | S |
| G2 | REPL interattivo | MANCA | L |
| G3 | errors.py per eccezioni C1-C2 | PARZIALE | M |
| G4 | File `.lu` di esempio | MANCA | S |
| G5 | Showcase v2 (pipeline C1-C2) | MANCA | M |
| G6 | Funzione `eval()` unificata per REPL | MANCA | S |

---

## 2. COSA INSEGNA LA RICERCA (42 fonti)

### Il Principio: CLI prima, REPL dopo

Tutti i linguaggi di successo hanno lo stesso ordine:
1. **CLI** - il comando che fa tutto (`cargo`, `gleam`, `deno`)
2. **Errori umani** - senza questi il linguaggio e inutilizzabile
3. **REPL** - per esplorare interattivamente
4. **Showcase/Tutorial** - per convincere il mondo

### I 5 Differenziatori Unici di LU (dalla ricerca)

1. **`lu verify`** -- nessun linguaggio pratico ha verifica formale one-command
2. **Errori in italiano/portoghese** -- nessun linguaggio mainstream lo fa
3. **Pannello triplo** -- LU source + Python generato + risultato verify (futuro playground)
4. **Constrained decoding** -- LLM genera codice LU valido per costruzione
5. **ZERO deps** -- `pip install` e basta, niente toolchain

### Pattern CLI dai migliori (Gleam, Cargo, Deno)

```
TIER 1 - Senza questi non esiste:
  lu run <file.lu>     -- compila + esegui
  lu check <file.lu>   -- parse + compile check (veloce)
  lu verify <file.lu>  -- verifica formale Lean 4

TIER 2 - Settimana 1:
  lu repl              -- REPL interattivo
  lu compile <file.lu> -- mostra Python generato (senza eseguire)

TIER 3 - Futuro:
  lu new               -- scaffolding progetto
  lu format            -- formatter opinionato
  lu explain E001      -- spiegazione estesa errore
```

### Pattern REPL (Python 3.14, ptpython, Unison)

- Syntax highlighting mentre si digita
- Multiline editing intelligente
- History persistente
- Tab completion contestuale
- MVP: readline base basta, ptpython e stretch goal

---

## 3. DECISIONI ARCHITETTURALI

### D1: CLI via `__main__.py` + argparse (non click/typer)

**Scelta:** `python -m cervellaswarm_lingua_universale` + argparse stdlib.
**Perche:** ZERO deps (P02). argparse copre TIER 1+2 senza problemi.
**Alternativa scartata:** click/typer (aggiunge deps per qualcosa che argparse fa bene).
**Console script:** `lu = cervellaswarm_lingua_universale.__main__:main` in pyproject.toml.

### D2: REPL con `code.InteractiveConsole` base (non ptpython)

**Scelta:** stdlib `code` module + readline per history/completion.
**Perche:** ZERO deps (P02). Il REPL non deve essere un IDE -- deve essere un modo per provare il linguaggio.
**Stretch goal:** syntax highlighting con escape ANSI se terminale supporta.
**Alternativa scartata:** ptpython (la Researcher lo raccomandava, ma violerebbe P02 ZERO deps; REPL puo evolvere dopo).

### D3: errors.py esteso per eccezioni C1-C2 (non nuovo modulo)

**Scelta:** Aggiungere `ParseError`, `TokenizeError`, `ContractViolation`, `InteropError` al catalogo esistente di `errors.py`.
**Perche:** Pattern consolidato (60 codici gia esistenti). Stessa architettura, stessi 3 locali.
**Nuovi codici:** LU-PA-xxx (parser), LU-TK-xxx (tokenizer), LU-CT-xxx (contracts), LU-IO-xxx (interop).

### D4: Session state per REPL incrementale

**Scelta:** Un `REPLSession` che accumula dichiarazioni (types, agents) tra input successivi.
**Perche:** Senza questo, ogni input nel REPL e isolato -- non puoi definire un type e poi usarlo.
**Come:** `REPLSession` mantiene un `ProgramNode` cumulativo; ogni input viene parsato e le dichiarazioni vengono aggiunte.

### D5: File `.lu` canonici come golden test

**Scelta:** Creare `examples/*.lu` con i 10 esempi canonici di C1.2 come file reali.
**Perche:** Servono per il demo, per i test, e per `lu run` out of the box.
**Double duty:** Sono anche i golden test per il REPL e la CLI.

---

## 4. I SUB-STEP DI C3

```
C3: L'Esperienza
  C3.1 STUDIO (questo documento)           1 sess    <- ORA
  C3.2 CLI + eval (lu run/check/verify)    1-2 sess
  C3.3 Error messages C1-C2                1 sess
  C3.4 REPL interattivo                    2 sess
  C3.5 File .lu canonici + showcase v2     1-2 sess
  C3.6 Guardiana audit finale C3           1 sess

EFFORT TOTALE: ~6-8 sessioni
ORDINE: C3.2 -> C3.3 -> C3.4 -> C3.5 -> C3.6
(errori PRIMA del REPL: senza errori umani il REPL e inutile)
```

### C3.2 -- CLI + eval

**File nuovi:**
- `_cli.py` (~300 LOC) -- argparse, subcommands run/check/verify/compile/repl
- `__main__.py` (~10 LOC) -- entry point `python -m`
- `_eval.py` (~80 LOC) -- funzione `eval_lu(source) -> result` unificata

**Modifica:**
- `pyproject.toml` -- aggiungere `[project.scripts] lu = "..."`

**Criterio:** `lu run examples/hello.lu` funziona. `lu check` segnala errori. `lu verify` chiama Lean 4.
**Test:** 30-40 test (subcommands, errori, output format).

### C3.3 -- Error messages C1-C2

**Modifica:**
- `errors.py` -- nuovi codici LU-PA/TK/CT/IO, import delle eccezioni C1-C2, `humanize()` esteso

**Criterio:** Un `ParseError` produce un messaggio in italiano con riga, colonna, e suggerimento.
**Test:** 20-30 test (1 per codice errore x 3 lingue campione).

### C3.4 -- REPL interattivo

**File nuovi:**
- `_repl.py` (~250-350 LOC) -- `REPLSession`, loop readline, commands (help/exit/load/clear)

**Criterio:** `lu repl` si apre, puoi scrivere codice LU, definire types/agents, errori umani inline.
**Test:** 30-40 test (sessione, accumulo stato, errori, commands).

### C3.5 -- File .lu canonici + showcase v2

**File nuovi:**
- `examples/hello.lu` -- il primo file LU del mondo
- `examples/delegation.lu` -- protocollo base
- `examples/ricette_nonna.lu` -- il demo sacro
- `examples/showcase_v2.py` -- il demo end-to-end con pipeline C1-C2

**Criterio:** `lu run examples/*.lu` funziona. showcase_v2 mostra il flusso completo.
**Test:** 10-15 test (ogni .lu file parsa+compila+esegue).

### C3.6 -- Guardiana audit finale

Audit completo C3. Target 9.5/10. Se sotto 9.0, si rifa.

---

## 5. METRICHE TARGET C3

| Metrica | Target |
|---------|--------|
| `lu run` funziona | Si, end-to-end |
| `lu verify` funziona | Si, Lean 4 bridge |
| REPL interattivo | Si, con stato sessione |
| Error messages per C1-C2 | Tutti i codici, 3 lingue |
| File .lu di esempio | >= 3 canonici |
| Test nuovi | 90-125 |
| Zero nuove deps runtime | Confermato |
| Guardiana score | >= 9.5/10 |

---

## 6. RISCHI

| Rischio | Mitigazione |
|---------|-------------|
| REPL state management complesso | D4: ProgramNode cumulativo, pattern semplice |
| `lu verify` richiede Lean 4 installato | Graceful degradation: messaggio chiaro se Lean 4 non trovato |
| Console script `lu` conflitto nome | Fallback: `lingua-universale` come nome lungo, `lu` come short |
| errors.py troppo grande (gia 1784 LOC) | Pattern P18: se > 2000 LOC, split in `_error_catalog.py` |

---

## 7. COSA NON FA C3

- **Playground online** -- Fase D (servono utenti esterni prima)
- **LSP / editor support** -- Fase D (richiede protocollo separato)
- **Package manager** -- Fase D (`lu install`)
- **`lu new` scaffolding** -- TIER 3, non essenziale ora
- **`lu format`** -- puo venire dopo, non blocca nulla
- **`lu test`** -- i test LU girano con pytest; un wrapper `lu test` e TIER 3
- **`lu explain E001`** -- alto valore, basso costo, ma differito a post-C3

---

## 8. IL PARALLELO

```
C1: La Grammatica    = come il linguaggio APPARE     (sintassi)
C2: Il Compilatore   = come il linguaggio FUNZIONA   (semantica)
C3: L'Esperienza     = come il linguaggio si USA     (pragmatica)
```

Senza C3, il linguaggio esiste ma nessuno lo puo toccare.
Con C3, chiunque puo: `pip install`, `lu run`, e vedere il futuro.

---

*"La domanda e la risposta nello STESSO linguaggio." - Rafa*
*"Ultrapassar os proprios limites!" - Rafa & Cervella*

*Fonti: 42 esterne (Gleam, Elm, Rust, Python 3.14, Unison, Roc, Deno, Cargo) + gap analysis codebase*
*Pattern applicati: P02 (ZERO deps), P06 (Research First), P07 (Guardiana dopo step), P18 (split if big)*
