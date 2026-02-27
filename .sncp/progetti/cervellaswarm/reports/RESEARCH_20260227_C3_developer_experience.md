# Developer Experience per Linguaggi di Programmazione Nuovi
## Ricerca per C3 - L'Esperienza (Lingua Universale)

**Data:** 2026-02-27
**Autrice:** Cervella Researcher
**Status:** COMPLETA
**Fonti:** 42 consultate (web + report interni)
**Contesto:** Fondamento per C3 "L'Esperienza" -- prossimo macro-step dopo C1+C2 completati.

---

## SINTESI ESECUTIVA

C3 "L'Esperienza" e il prossimo macro-step di Lingua Universale dopo:
- C1 Grammatica (DONE) -- grammatica EBNF, parser
- C2 Compilatore (DONE) -- AST->Python, interop, constrained gen

C3 deve costruire il layer che fa dire "wow" a chi prova il linguaggio.
Questa ricerca copre: REPL, error messages, CLI, playground, first-5-minutes.

**La buona notizia:** Il report B6 (2026-02-25) ha gia fatto la ricerca su error messages.
Qui aggiorniamo con dati nuovi e integriamo con REPL + CLI + playground.

---

## SEZIONE 1 - REPL COMPARATIVA

### 1.1 Tabella Comparativa REPL Moderni

| REPL | Linguaggio | Sintassi Highlight | Autocomplete | Multiline | Storia | Unique Feature | Playground Web |
|------|------------|-------------------|--------------|-----------|--------|----------------|----------------|
| **Python 3.13+** | Python | Si (da 3.13) | Tab + context-aware (3.14) | Si + storia | Si | pyrepl: estendibile, F1=help, F2=no-output-history | No nativo |
| **IPython/ptpython** | Python | Si | Jinja2 + oggetti | Si | Si | magic %commands, object inspection con ?, Jupyter kernel | No |
| **evcxr** | Rust | Si | Si (tab x2) | Si | Si | Jupyter kernel, custom HTML display, async/await | No |
| **Gleam shell** | Gleam | Si | Si | Si | Si | Erlang shell integrata (`gleam shell`) | tour.gleam.run (WASM!) |
| **Roc REPL** | Roc | Si | Parziale | Si | Parziale | Browser WASM, compiler-less (no interpreter, usa compiler) | roc-lang.org |
| **UCM (Unison)** | Unison | Si | Si | Si | Si | Watch expressions in .u file (NON REPL tradizionale), hash-based, caching | No |
| **Elm REPL** | Elm | Si | Parziale | Si | Si | Errori didattici con hint, nessun runtime exception | No |
| **`deno repl`** | Deno/TS | Si | Si | Si | Si | TypeScript native, --eval flag, Jupyter kernel | No |

### 1.2 Pattern Comuni nei REPL di Successo

Tutti i REPL moderni condividono questi pattern:

1. **Syntax highlighting mentre si digita** -- non dopo l'invio
2. **Tab completion contestuale** -- non solo parole ma tipi e metodi
3. **Storia persistente** tra sessioni (frecce su/giu)
4. **Multiline editing** -- quando il testo e incompleto, va a capo intelligentemente
5. **Error messages immediati** -- pre-esecuzione (syntax check) + post-esecuzione
6. **"Esci senza punto e virgola"** -- comandi speciali senza sintassi verbosa

### 1.3 Differenziatori dei REPL Migliori

**IPython/ptpython -- Il Gold Standard Python:**
- `?obj` o `obj?` per introspection immediata
- `%run script.py` per caricare file nel namespace
- `%history` per storia filtrata
- `%edit` per aprire editor esterno
- Tab completion che capisce il tipo dell'oggetto (Jedi)
- Tab pages (ptpython): ogni tab ha il suo buffer

**UCM (Unison) -- Il Piu Innovativo:**
- NON e un REPL nel senso tradizionale
- `>expression` in qualsiasi .u file = watch expression
- Caching content-addressed: se le dipendenze non cambiano, NON ricalcola
- Comportamento "spreadsheet": solo le celle cambiate vengono rieseguite
- Nessun package manager separato: tutto dentro UCM

**Gleam tour.gleam.run -- Il Piu Accessibile:**
- Compilatore Rust compilato in WASM che gira nel browser
- Web Workers per non bloccare la UI
- GitHub Pages (hosting gratuito, zero server)
- Precompila stdlib on-demand
- Zero round-trip al server

**Python 3.13/3.14 -- La Tendenza dell'Industria:**
- Il REPL di default ora ha colori, multiline, F1/F2
- PEP 762 (in progress): riscrittura completa del REPL
- Python 3.14: syntax highlight mentre digiti + import autocomplete

### 1.4 REPL per Lingua Universale: Raccomandazione

**Opzione A (MVP rapido):** REPL Python-based con `ptpython` come base
- Zero nuovo codice di infrastruttura
- Aggiunge LU syntax highlighting via pygments custom lexer
- Integra il compilatore LU -> Python esistente
- Stima: 1-2 settimane

**Opzione B (Differenziatore):** REPL con watch expressions stile Unison
- Il .lu file ha `>` prefix per espressioni valutate live
- Ricalcola solo quando dipendenze cambiano
- Integra con il constraint checker esistente
- Stima: 3-4 settimane

**Raccomandazione: Opzione A prima, Opzione B come stretch goal C3.**

---

## SEZIONE 2 - ERROR MESSAGES PER UMANI

> NOTA: Il report B6 (RESEARCH_20260225_error_messages_b6.md) ha 27 fonti
> e copertura completa. Questa sezione aggiunge solo nuovi dati 2024-2026.

### 2.1 Top 10 Pattern (Consolidato B6 + Nuova Ricerca)

| # | Pattern | Esempio | Linguaggio Fonte |
|---|---------|---------|-----------------|
| 1 | **"Forse intendevi X?"** | `audit_verdct` -> suggerisce `audit_verdict` | Elm, Rust, Lean 4 |
| 2 | **Context-aware errors** | Usa i nomi del programmatore, non quelli interni del compiler | Gleam v1.6.0 (2024) |
| 3 | **Codice dell'utente al centro** | Mostra la riga esatta con highlighting, non stack trace | Rust, Elm |
| 4 | **Hint actionable** | "Aggiungi `trust >= high` prima di questa riga" | Elm, Rust |
| 5 | **Codice errore univoco** | `E0308`, `E001` -- link a spiegazione estesa | Rust (`rustc --explain`) |
| 6 | **Level chiaro** | error / warning / note (non tutto e "error") | Rust, miette |
| 7 | **Lowercase, no punto finale** | `type mismatch` non `Type Mismatch.` | Rust style guide |
| 8 | **Witness/Counterexample** | "La proprieta e violata perche: step 3 -> step 5 fuori ordine" | Alloy, TLA+, FizzBee |
| 9 | **Multi-lingua** | Stesso errore in IT e EN | Lingua Universale (unica) |
| 10 | **`explain` command** | `lu explain E001` -> spiegazione lunga con esempi | Rust (`rustc --explain`) |

### 2.2 Novita 2024: Gleam Context-Aware Compilation

Gleam v1.6.0 (novembre 2024) ha introdotto context-aware compilation:
- I type error usano i **nomi e la sintassi che il programmatore usa in quel contesto**
- Non piu "expected `Int`, got `String`" generico
- Ma "expected `user_id` (type `Int`), got `name` (type `String`)"
- Anche i **hover tips** nel LSP sono context-aware

**Applicazione per LU:** Quando il compilatore LU genera errori, usare
il nome del protocollo e i tipi del dominio (es: `trust_tier`, non `str`).

### 2.3 Novita 2024: Gleam Code Actions

Gleam ha introdotto "code actions" -- suggerimenti che l'LSP applica automaticamente:
- Aggiunta automatica di import mancanti
- Conversione tra tipi compatibili
- Fix automatici per deprecazioni (`gleam fix` CLI command)

**Applicazione per LU:** `lu fix` per auto-correggere errori comuni
(typo in message kind, ordine parametri sbagliato, ecc.).

---

## SEZIONE 3 - CLI PER LINGUAGGI: PATTERN E SUBCOMMANDS

### 3.1 Tabella Comparativa CLI

| Subcommand | Gleam | Cargo (Rust) | Deno | Roc | Lingua Universale? |
|------------|-------|--------------|------|-----|-------------------|
| `new` / `init` | `gleam new` | `cargo new` | `deno init` | `roc new` | `lu new` |
| `build` / `check` | `gleam build` + `gleam check` | `cargo build` + `cargo check` | `deno check` | `roc check` | `lu check` |
| `run` | `gleam run` | `cargo run` | `deno run` | `roc run` | `lu run` |
| `test` | `gleam test` | `cargo test` | `deno test` | `roc test` | `lu test` |
| `repl` | `gleam shell` | (evcxr separato) | `deno repl` | `roc repl` | `lu repl` |
| `format` | `gleam format` | `cargo fmt` | `deno fmt` | `roc format` | `lu format` |
| `docs` | `gleam docs` | `cargo doc` | `deno doc` | - | `lu docs` |
| `publish` | `gleam publish` | `cargo publish` | `deno publish` | - | - (futuro) |
| `add`/`remove` | `gleam add` / `gleam remove` | - | `deno add` / `deno remove` | - | - |
| `upgrade` | `gleam update` | `cargo update` | `deno upgrade` | - | - |
| `lsp` | `gleam lsp` | `rust-analyzer` sep. | `deno lsp` | - | `lu lsp` |
| `fix` | `gleam fix` | `cargo fix` | - | - | `lu fix` |
| `explain` | - | `rustc --explain E0308` | - | - | `lu explain E001` |
| `verify` | - | - | - | - | `lu verify` (UNICO!) |

### 3.2 Core Subcommands Essenziali (il Minimo Vitale)

Per un linguaggio nuovo, i subcommand **assolutamente essenziali** nei primi 6 mesi:

```
TIER 1 - DAY ONE (senza questi non esiste il linguaggio):
  {lang} new       -- crea progetto scaffolding
  {lang} run       -- compila e esegue
  {lang} check     -- type check senza eseguire (fast feedback)
  {lang} test      -- esegue i test

TIER 2 - WEEK ONE (senza questi non si usa il linguaggio):
  {lang} repl      -- interattivita
  {lang} format    -- code formatting (opinionato, non configurabile)
  {lang} docs      -- genera documentazione

TIER 3 - MONTH ONE (per adozione seria):
  {lang} lsp       -- integrazione editor
  {lang} fix       -- auto-fix errori comuni
  {lang} explain   -- spiegazione errori estesa
```

### 3.3 Principi di Design CLI (da Gleam + Cargo + Deno)

1. **Un solo nome, nessuna abbreviazione**: `gleam new` non `gleam n`
2. **Errori di CLI utili**: `gleam bluid` -> "did you mean `build`?"
3. **Extensibilita**: cargo permette `cargo-xxx` binari nel PATH come subcommand
4. **`--watch` su quasi tutto**: `gleam run --watch`, `deno run --watch`
5. **Output strutturato opzionale**: `--json` per integrazioni CI/CD
6. **Self-documenting**: `{lang} help {subcommand}` sempre disponibile
7. **Zero config di default**: nessuna configurazione richiesta per iniziare

### 3.4 Novita Deno 2024: CLI come Full Developer Suite

Deno 2.0 (2024) ha aggiunto 10+ subcommand nuovi in un anno.
Filosofia: **la CLI e il prodotto**, non solo un wrapper al compiler.
Deno ha `deno bench`, `deno audit`, `deno jupyter`, `deno deploy`.

**Insegnamento per LU:** `lu verify` (verifica formale con Lean 4)
e il differenziatore che nessun altro ha. E un subcommand Tier 1 per noi,
non Tier 3.

```
TIER 1 LINGUA UNIVERSALE (proposta):
  lu new        -- crea progetto
  lu run        -- compila LU -> Python -> esegui
  lu check      -- parse + type check + property check (veloce)
  lu verify     -- verifica formale Lean 4 (lento, ma unico al mondo)
  lu test       -- esegui test suite
  lu repl       -- REPL interattivo
```

---

## SEZIONE 4 - PLAYGROUND ONLINE

### 4.1 Architettura dei Playground Esistenti

**Rust Playground (play.rust-lang.org):**
- Frontend: React con Monaco editor
- Backend: Axum (Rust)
- Isolamento: Docker containers (no network, limiti memoria/CPU/tempo)
- Multi-versione: stable, beta, nightly
- Lezione: **Docker e il modo industriale, ma richiede infrastruttura**

**Gleam Tour (tour.gleam.run):**
- Stack: compiler Rust -> WASM, CodeFlask editor, GitHub Pages
- Esecuzione: 100% client-side, zero server
- Threading: Web Workers (UI non si blocca)
- Stdlib: scaricata on-demand, precompilata
- Hosting: GitHub Pages (GRATIS, zero infrastruttura)
- Lezione: **WASM + GitHub Pages = playground zero-cost per piccoli team**

**Go Playground (go.dev/play):**
- Backend: server Google, sandboxato con gVisor
- Multi-snippet: condivisione via URL
- Formato automatico
- Lezione: **condivisione via URL e fondamentale per il marketing**

**Roc REPL (roc-lang.org):**
- Compiler compilato in WASM
- Gira nel browser, zero server
- Lezione: **anche un linguaggio alpha puo avere playground WASM**

### 4.2 Requisiti Minimi per un Playground

```
MUST HAVE (MVP):
  - Editor con syntax highlighting (Monaco o CodeMirror)
  - Esecuzione sandboxata (WASM client-side o Docker server-side)
  - Output visibile
  - Almeno 3-5 esempi precaricati
  - Condivisione via URL (permalink)

SHOULD HAVE:
  - Errori con highlighting nel codice
  - "Resetta a esempio originale" button
  - Mobile-friendly (anche solo lettura, non editing)
  - Keyboard shortcuts (Ctrl+Enter = run)

NICE TO HAVE:
  - Multi-file support
  - Import dipendenze
  - Output formattato (non solo plain text)
  - Integrazione con docs (link da errore a documentazione)
```

### 4.3 Raccomandazione per Lingua Universale

**Approccio: WASM client-side (stile Gleam tour)**

Motivo: il nostro compilatore LU -> Python esiste gia.
Il percorso e:
1. Compilare il compiler LU in WASM (o usare Pyodide per Python nel browser)
2. Editor con syntax highlighting custom per LU
3. Esegui il Python generato in Pyodide
4. Hosting: GitHub Pages (zero costo)

**Alternativa piu semplice (MVP in 2 settimane):**
- Backend FastAPI/Docker su Fly.io (free tier)
- Frontend: Monaco editor + un file HTML
- Limit: 5 secondi, nessuna rete, memoria limitata

**Differenziatore unico:** il playground mostra sia:
- Il codice LU che si sta scrivendo
- Il Python generato (pannello affiancato)
- Il risultato della verifica formale (check/verify)

Questo e educativo E dimostrativo del valore del linguaggio.

---

## SEZIONE 5 - "FIRST 5 MINUTES" EXPERIENCE

### 5.1 Cosa Fanno i Migliori (Pattern Consolidati)

**Go (il Benchmark dell'Industria):**
1. `brew install go` -> funziona in 30 secondi
2. `go.dev/tour` -> tutorial interattivo nel browser (nessuna installazione)
3. Primo programma: `hello world` in 3 righe
4. `go run hello.go` -> esecuzione immediata
5. Go Playground per condividere senza installare

**Gleam (il Piu Curato, 2024):**
1. `brew install gleam` (o asdf/mise)
2. `gleam new myapp && cd myapp && gleam run` -> funziona!
3. tour.gleam.run per esplorare senza installare
4. Progetto scaffolding include: src/, test/, README.md, gleam.toml, GitHub Actions
5. Errori colorati con contesto immediati

**Deno (Fastest First Run):**
1. `curl -fsSL https://deno.land/install.sh | sh` (un solo comando)
2. `deno run https://deno.land/std/examples/welcome.ts` (no install!)
3. Nessun `package.json`, nessun `node_modules`
4. TypeScript di default (no config)

**Rust (Piu Lungo ma Vale la Pena):**
1. `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`
2. `cargo new hello && cd hello && cargo run`
3. Rust book online + playground
4. Il "wow" arriva dopo: borrow checker che SPIEGA come fixare

### 5.2 Checklist "First 5 Minutes" per Lingua Universale

```
MINUTO 0-1 - INSTALLAZIONE:
  [ ] Un solo comando: `pip install lingua-universale` (ZERO deps)
  [ ] O: playground online senza installazione
  [ ] Verifica: `lu --version` stampa versione + tagline

MINUTO 1-2 - HELLO WORLD:
  [ ] `lu new mioprotocollo`
  [ ] Progetto scaffolding con esempio funzionante
  [ ] `lu run` -> output visibile immediatamente

MINUTO 2-3 - PRIMO ERRORE:
  [ ] Introduci un typo deliberato
  [ ] Vedi un errore user-friendly con "forse intendevi X?"
  [ ] Fix immediato, ri-esegui

MINUTO 3-4 - IL DIFFERENZIATORE:
  [ ] `lu verify` -> "Protocollo verificato formalmente in 0.3s"
  [ ] Oppure: introduci violazione ORDERING -> errore con witness
  [ ] Il momento "wow": nessun altro linguaggio fa questo

MINUTO 4-5 - ESPLORA:
  [ ] `lu repl` per giocare interattivamente
  [ ] Link al tour interattivo online
  [ ] Link al playground
  [ ] Link a 3 esempi: semplice, medio, avanzato
```

### 5.3 Il Momento "Wow" per LU (Analisi)

Per **developer Python:**
- "Genero codice Python verificato formalmente? Senza deps esterne?"
- Il wow arriva quando `lu verify` prova la correttezza automaticamente

Per **developer sistemisti:**
- "Session types con verifica Lean 4 in un DSL semplice?"
- Il wow arriva quando una violazione di protocollo viene catturata PRIMA dell'esecuzione

Per **non-developer (target secondario):**
- "Scrivo quello che voglio che succeda, e il sistema lo verifica?"
- Il wow arriva quando l'errore spiega cosa correggere in italiano

**La domanda chiave:** quale dei tre e il target C3?
Per il lancio pubblico (Show HN, Reddit), il target e **developer Python**.

### 5.4 Template README per "First 5 Minutes"

I migliori linguaggi hanno tutti questa struttura nel README:

```markdown
## Quick Start

# Installa
pip install lingua-universale

# Crea primo progetto
lu new myprotocol && cd myprotocol

# Esegui
lu run

# Verifica formalmente
lu verify
```

Seguito immediatamente da un esempio che mostra il valore unico.
Non "hello world" generico, ma il caso d'uso che giustifica l'esistenza del linguaggio.

---

## SEZIONE 6 - RACCOMANDAZIONI SPECIFICHE PER C3

### 6.1 Priorita Proposte per C3

```
C3.1 - CLI Base (Tier 1 commands)
  lu new / lu run / lu check / lu verify / lu test
  Stima: 2 settimane

C3.2 - Error Messages Layer (gia progettato in B6!)
  Translator layer su eccezioni esistenti
  Stima: 1 settimana (design gia fatto)

C3.3 - REPL Interattivo
  ptpython-based con LU syntax highlighting
  Stima: 1-2 settimane

C3.4 - Playground Online
  WASM o FastAPI backend su Fly.io
  Stima: 2-3 settimane

C3.5 - Interactive Tour
  5-10 step guidati, stile tour.gleam.run
  Stima: 2 settimane
```

### 6.2 Differenziatori Unici che LU Puo Avere

Analisi dei competitori: nessuno ha questi.

1. **`lu verify`** -- verifica formale come subcommand di prima classe
   - Cargo, Gleam, Deno non hanno niente di simile
   - "Il primo linguaggio con verifica formale one-command"

2. **Error con witness formale** -- quando una proprieta e violata,
   mostrare la traccia di esecuzione che prova la violazione
   - Alloy lo fa per model checking, nessun linguaggio pratico lo fa

3. **REPL con session type checking** -- ogni espressione nel REPL
   viene verificata contro il protocollo definito
   - Unico al mondo per i session types interattivi

4. **Errori in italiano** -- errori localizzati in italiano per utenti italiani
   - Nessun linguaggio mainstream lo fa (B6 ha gia il design)

5. **Playground che mostra Python generato** -- panello affiancato
   LU + Python + risultato verifica = trasparenza totale del compilatore

### 6.3 Cosa NON Fare (Anti-Pattern da Evitare)

1. **NON aspettare il playground perfetto per lanciare**
   - Gleam ha lanciato con playground semplice, poi migliorato
   - Un playground grezzo con 3 esempi e meglio di nessun playground

2. **NON creare un REPL da zero se ptpython basta**
   - "Non reinventare, studia come fanno i big" (nostro mantra)
   - ptpython si embeds in 50 righe di Python

3. **NON separare il formatter dal linter**
   - `lu format` e `lu check` devono essere entrambi o zero
   - I developer si aspettano entrambi se hai uno

4. **NON usare differenti convention per i messaggi di errore**
   - Una sola voice/tone nei messaggi (B6 ha il design)
   - Mixing italiano/inglese nello stesso messaggio = confusione

5. **NON dimenticare `lu explain`**
   - `rustc --explain E0308` e uno dei feature piu amati di Rust
   - Costa poco da implementare, valore altissimo per l'utente

---

## SEZIONE 7 - FONTI COMPLETE

### Fonti Web Principali

1. [Elm - Delightful language for reliable web applications](https://elm-lang.org/)
2. [Why is Elm such a delightful programming language? - DEV Community](https://dev.to/marciofrayze/why-is-elm-such-a-delightful-programming-language-2em8)
3. [ptpython - A better Python REPL - GitHub](https://github.com/prompt-toolkit/ptpython)
4. [Boost Your Coding Productivity with Ptpython - Real Python](https://realpython.com/ptpython-shell/)
5. [The new REPL in Python 3.13 - Trey Hunner](https://treyhunner.com/2024/05/my-favorite-python-3-dot-13-feature/)
6. [Python 3.14: REPL Autocompletion and Highlighting - Real Python](https://realpython.com/python-repl-autocompletion-highlighting/)
7. [Python 3.14 REPL Gets Smarter - Medium/PyZilla](https://medium.com/pyzilla/python-3-14-repl-autocompletion-syntax-highlighting-eef9f419c17c)
8. [evcxr - Rust REPL and Jupyter Kernel - GitHub](https://github.com/evcxr/evcxr)
9. [Interactive Rust in a REPL and Jupyter Notebook with EVCXR - Depth-First](https://depth-first.com/articles/2020/09/21/interactive-rust-in-a-repl-and-jupyter-notebook-with-evcxr/)
10. [Gleam Command Line Reference](https://gleam.run/command-line-reference/)
11. [CLI Commands - Gleam DeepWiki](https://deepwiki.com/gleam-lang/gleam/5-cli-commands)
12. [Gleam's new interactive language tour](https://gleam.run/news/gleams-new-interactive-language-tour/)
13. [Welcome to the Gleam Language Tour - tour.gleam.run](https://tour.gleam.run/)
14. [Gleam context-aware compilation](https://gleam.run/news/context-aware-compilation/)
15. [Convenient code actions - Gleam](https://gleam.run/news/convenient-code-actions/)
16. [Gleam programming language - Wikipedia](https://en.wikipedia.org/wiki/Gleam_(programming_language))
17. [The Roc Programming Language](https://www.roc-lang.org/)
18. [Roc Language Tutorial](https://www.roc-lang.org/tutorial)
19. [Understanding Roc: Functional and separate from the runtime - TechTarget](https://www.techtarget.com/searchapparchitecture/tip/Understanding-Roc-Functional-and-separate-from-the-runtime)
20. [Unison docs - Tour](https://www.unison-lang.org/docs/tour/)
21. [Unison docs - UCM Commands](https://www.unison-lang.org/docs/ucm-commands/)
22. [What is so unique about Unison? - Galaxy brain](https://etorreborre.blog/what-is-so-unique-about-unison)
23. [Unison - A friendly programming language from the future - GitHub](https://github.com/unisonweb/unison)
24. [Rust Playground - play.rust-lang.org](https://play.rust-lang.org/)
25. [Rust Playground - GitHub rust-lang/rust-playground](https://github.com/rust-lang/rust-playground)
26. [Gleam Playground - GitHub NicklasXYZ](https://github.com/NicklasXYZ/gleam_playground)
27. [A Tour of Go - go.dev](https://go.dev/tour/)
28. [Gleam Language Tour - GitHub gleam-lang/language-tour](https://github.com/gleam-lang/language-tour)
29. [Deno CLI Subcommands Reference](https://docs.deno.com/runtime/reference/cli/)
30. [Deno in 2024 - deno.com blog](https://deno.com/blog/deno-in-2024)
31. [deno compile, standalone executables](https://docs.deno.com/runtime/reference/cli/compile/)
32. [Cargo - The Rust Package Manager - GitHub](https://github.com/rust-lang/cargo)
33. [Top Cargo Subcommands For Rust Development - Zero To Mastery](https://zerotomastery.io/blog/top-cargo-subcommands-for-rust-development/)
34. [Extending Cargo with Custom Commands - The Rust Book](https://doc.rust-lang.org/book/ch14-05-extending-cargo.html)
35. [IPython Tutorial - ipython.readthedocs.io](https://ipython.readthedocs.io/en/stable/interactive/tutorial.html)
36. [IPython: Modern Python Developer's Toolkit - pycon.switowski.com](https://pycon.switowski.com/05-repl/ipython/)
37. [Introduction to Gleam - The New Stack](https://thenewstack.io/introduction-to-gleam-a-new-functional-programming-language/)
38. [Gleam - "gleam new" project structure - dev.to](https://dev.to/sharsha315/introduction-to-gleam-programming-language-1c7n)
39. [Zig Getting Started - ziglang.org](https://ziglang.org/learn/getting-started/)
40. [PEP 762 - REPL-acing the default REPL](https://peps.python.org/pep-0762/)

### Report Interni Utilizzati

41. [RESEARCH_20260225_error_messages_b6.md] - Ricerca completa su error messages (27 fonti)
42. [RESEARCH_20260224_come_si_crea_un_linguaggio.md] - Come si crea un linguaggio (28 fonti)

---

## OUTPUT FORMAT (Riepilogo per Regina)

```
## Developer Experience per Linguaggi Nuovi - Ricerca C3
**Status**: COMPLETA
**Fonti**: 42 consultate
**Sintesi**:
  - REPL: ptpython-based e il MVP piu veloce; Unison watch expressions sono il differenziatore
  - Error messages: B6 gia coperto; aggiungere Gleam context-aware + code actions
  - CLI: Tier 1 = new/run/check/verify/test; `lu verify` e il nostro differenziatore unico
  - Playground: WASM (stile Gleam) o FastAPI+Fly.io; mostrare LU + Python + verify risultato
  - First 5 minutes: pip install -> lu new -> lu run -> lu verify (il wow) -> lu repl
**Raccomandazione**: C3 nell'ordine C3.1 CLI > C3.2 Errors > C3.3 REPL > C3.4 Playground > C3.5 Tour
**Report**: .sncp/progetti/cervellaswarm/reports/RESEARCH_20260227_C3_developer_experience.md
```

---

*Cervella Researcher - CervellaSwarm*
*"Ricerca PRIMA di implementare."*
*"Non inventare, studia come fanno i big."*
*2026-02-27*

COSTITUZIONE-APPLIED: SI
Principio: "Ricerca PRIMA di implementare" + "Fatto BENE > Fatto VELOCE"
