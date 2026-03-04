# SUBROADMAP - Fase D: L'Ecosistema

> **Creata:** 28 Febbraio 2026 - Sessione 425
> **Fonti:** 3 report di ricerca (46+ fonti), studi su Python/Rust/Go/Gleam/Zig/Roc
> **Prerequisiti:** FASE A+B+C COMPLETE (25 moduli, 2806 test, 0 deps)
> **Score target:** 9.5/10 per ogni step (audit Guardiana)
> **Filosofia:** "Fatto BENE > Fatto VELOCE" | "Un progresso al giorno"

---

## L'INSIGHT DI RAFA (S425)

```
+====================================================================+
|                                                                    |
|   "Hai studiato anche i grossi? Come hanno fatto?                  |
|    Python ha tutto questo, giusto?                                  |
|    Anche l'unico modo di fare crescere! Migliorare!"               |
|                                                                    |
|                                          - Rafa, S425              |
+====================================================================+
```

---

## PERCHE FASE D = ECOSISTEMA (non "Per Tutti")

La Fase D nella MAPPA_LINGUAGGIO originale si chiamava "Per Tutti" (IntentBridge,
voce, multi-lingua). Ma la ricerca sui linguaggi di successo dice:

**Nessun linguaggio e arrivato "per tutti" senza prima avere un ecosistema.**

- Python: 30 anni per #1. I primi 10 anni = solo ecosistema.
- Rust: Cargo + crates.io + playground PRIMA di v1.0 stable.
- Go: gofmt + playground + "A Tour of Go" dal giorno 1.
- Gleam: LSP 2 anni PRIMA di v1.0.

**La ricerca accademica conferma** (Meyerovich, OOPSLA 2013):
"Le feature intrinseche hanno solo importanza secondaria nell'adozione.
L'ecosistema determina il destino di un linguaggio."

Quindi la nostra Fase D diventa: costruire l'ecosistema che permette
al linguaggio di CRESCERE. IntentBridge, voce, multi-lingua vengono DOPO
(diventano Fase E).

---

## I 5 PILASTRI DELL'ECOSISTEMA (dai pattern universali)

```
1. INSTALLAZIONE FACILE       pip install   [GIA FATTO!]
2. PROVARE SENZA INSTALLARE   playground    [DA FARE]
3. ERRORI NEL TUO EDITOR      LSP           [DA FARE]
4. TUTORIAL INTERATTIVO        "A Tour"      [DA FARE]
5. COMMUNITY                   governance    [DA FARE]
```

---

## LA MAPPA -- 6 STEP

```
+================================================================+
|   FASE D1: Syntax Highlighting + VS Code Extension  (1-2 sess) |
|   - TextMate grammar per .lu files                              |
|   - VS Code extension base (colorazione)                        |
|   - Pubblicazione su VS Code Marketplace                        |
|   - Screenshot wow per README                                   |
|                                                                  |
|   FASE D2: LSP Base (lu lsp)                        (2-3 sess) |
|   - pygls (Python Generic Language Server)                      |
|   - Diagnostics in tempo reale (errori LU-N inline)             |
|   - Aggiungere `lu lsp` alla CLI                                |
|   - VS Code extension collegata al server                       |
|                                                                  |
|   FASE D3: Playground Online (Pyodide)              (1-2 sess) |
|   - Monaco Editor + Pyodide (Python in WASM)                    |
|   - micropip.install dal browser                                |
|   - Deploy su GitHub Pages ($0)                                  |
|   - "Try it in 30 seconds" sulla homepage                       |
|                                                                  |
|   FASE D4: "A Tour of LU" (Tutorial Interattivo)   (2-3 sess) |
|   - Ispirato a "A Tour of Go" (il gold standard)               |
|   - Step-by-step: types -> agents -> protocols -> verify        |
|   - Integrato nel playground                                    |
|   - "Build your first verified protocol in 10 minutes"          |
|                                                                  |
|   FASE D5: LSP Avanzato + Hover + Completion        (2-3 sess) |
|   - Hover: mostra tipo e documentazione al passaggio            |
|   - Completion: suggerimenti keyword, nomi ruoli, trust tiers   |
|   - Go-to-definition per types e agents                         |
|                                                                  |
|   FASE D6: Guardiana Audit Finale + Launch           (1 sess)  |
|   - Review cross-cutting tutto il tooling                       |
|   - README update con screenshot e links                        |
|   - Annuncio community                                          |
+================================================================+
```

---

## DETTAGLIO PER STEP

### D1: Syntax Highlighting + VS Code Extension

**Perche prima:** Screenshot colorate di .lu files = marketing immediato.
Gleam insegna: anche solo syntax highlighting cambia la percezione del linguaggio.

**Struttura extension:**
```
lingua-universale-vscode/
  package.json                               # manifest VS Code
  client/extension.ts                        # ~50 righe, lancia lu lsp
  syntaxes/lingua-universale.tmLanguage.json # TextMate grammar
  language-configuration.json                # brackets, comments, etc.
```

**Keyword da colorare:**
- Tipi: `type`, `record`, `variant`
- Agenti: `agent`, `trust`, `capability`
- Protocolli: `protocol`, `roles`, `choice`, `when`
- Proprieta: `requires`, `ensures`, `confidence`, `property`
- Azioni: `asks`, `returns`, `sends`, `confirms`
- Builtins: `use`, `Confident`, `Certain`, `High`, `Medium`, `Low`

**Criterio completamento:**
- [x] TextMate grammar che colora correttamente i 5 file .lu esempio (47/47 check)
- [x] VS Code extension installabile localmente (cervellaswarm.lingua-universale)
- [ ] Screenshot "wow" per README
- [ ] Pubblicazione su VS Code Marketplace (o Open VSX)
- [x] Guardiana verifica 9.5/10

---

### D2: LSP Base (lu lsp)

**Perche:** Errori in tempo reale nell'editor = vera developer experience.
Il 60-70% del lavoro e GIA fatto (parser, error codes, Loc(line,col)).

**Stack:** pygls v2.0.1 (Python Generic Language Server, stabile, STDIO)

**Architettura:**
```python
# _lsp.py - ~200-300 righe
from pygls.server import LanguageServer

lu_server = LanguageServer("lingua-universale-lsp", "v0.1")

@lu_server.feature(TEXT_DOCUMENT_DID_OPEN)
@lu_server.feature(TEXT_DOCUMENT_DID_CHANGE)
def validate(ls, params):
    # 1. Prende il source dal documento
    # 2. Chiama check_source() (GIA ESISTE!)
    # 3. Converte LU-N errors -> LSP Diagnostics
    # 4. I nostri Loc(line,col) -> LSP Range/Position
    ls.publish_diagnostics(uri, diagnostics)
```

**CLI:** aggiungere `lu lsp` come subcommand.

**Nota importante:** pygls e la PRIMA dipendenza esterna. Va aggiunta come
"optional dependency" (`pip install cervellaswarm-lingua-universale[lsp]`).
Il core resta ZERO DEPS.

**Criterio completamento:**
- [x] `lu lsp` funziona via STDIO (pygls v2.0.1)
- [x] Diagnostics: errori LU-N mostrati inline nell'editor (humanize() bridge)
- [x] VS Code extension collegata al server (extension.ts client)
- [x] Test del language server (22 test, 100% pass)
- [x] Zero regressioni sulla suite esistente (2828 test, 0.97s)
- [x] Guardiana verifica 9.5/10

---

### D3: Playground Online (Pyodide)

**Perche:** "Se puoi provarlo in 30 secondi senza installare, lo proverai."
Il nostro ZERO DEPS e il caso PERFETTO per Pyodide (Python nel browser via WASM).

**Stack:** Monaco Editor + Pyodide + GitHub Pages

**Come funziona:**
```javascript
// 1. Carica Pyodide (26MB, cached dopo primo download)
let pyodide = await loadPyodide();
// 2. Installa il nostro package da PyPI
await pyodide.loadPackage("micropip");
await pyodide.runPython(`
    import micropip
    await micropip.install("cervellaswarm-lingua-universale")
`);
// 3. L'utente scrive .lu nel Monaco Editor
// 4. Click "Run" -> esegue nel browser
await pyodide.runPython(`
    from cervellaswarm_lingua_universale import check_source
    result = check_source(user_code)
`);
```

**Costo:** $0 (GitHub Pages statico, Pyodide via CDN)

**Criterio completamento:**
- [x] Pagina HTML con Monaco Editor + Pyodide (S427)
- [x] Carica e esegue codice .lu nel browser (S429, v0.2.0)
- [x] Mostra errori formattati (S427)
- [x] Deploy su GitHub Pages (S429, deploy-playground.yml)
- [ ] "Try it now" link nella README
- [ ] Guardiana verifica 9.5/10 (audit in corso S430)

---

### D4: "A Tour of LU" (Tutorial Interattivo)

**Perche:** "A Tour of Go" e considerato il miglior tutorial al mondo per un linguaggio.
Nessun developer usera un linguaggio senza un onboarding chiaro.

**Struttura (ispirata a Tour of Go):**
```
Capitolo 1: Tipi (5 step)
  1.1 Il tuo primo tipo: type Color = Red | Green | Blue
  1.2 Record types: record Point { x: int, y: int }
  1.3 Confident[T]: l'incertezza come tipo
  1.4 Esercizio: crea i tuoi tipi

Capitolo 2: Agenti (5 step)
  2.1 Il tuo primo agente: agent Worker
  2.2 Trust tiers: trusted, standard, untrusted
  2.3 Capabilities: can read, can write
  2.4 Esercizio: una squadra di agenti

Capitolo 3: Protocolli (5 step)
  3.1 Il tuo primo protocollo: chi parla con chi
  3.2 Choice: decisioni nel protocollo
  3.3 Properties: requires e ensures
  3.4 Esercizio: il protocollo della nonna

Capitolo 4: Verifica (3 step)
  4.1 lu check: compilazione senza esecuzione
  4.2 lu verify: Lean 4 sotto il cofano
  4.3 La demo finale: "Build your first verified protocol"
```

**Integrato nel playground:** ogni step ha codice editabile e eseguibile.

**Criterio completamento:**
- [ ] 18+ step interattivi
- [ ] Integrato nel playground Pyodide
- [ ] Un non-sviluppatore capisce i primi 2 capitoli
- [ ] Guardiana verifica 9.5/10

---

### D5: LSP Avanzato + Hover + Completion

**Perche:** Dopo diagnostics, hover e completion sono le feature piu richieste.
Rendono il linguaggio "comodo" da usare quotidianamente.

**Hover:** mostra tipo, docstring, trust tier al passaggio del mouse.
**Completion:** suggerisce keyword, nomi ruoli gia definiti, trust tiers, confidence levels.
**Go-to-definition:** click su un tipo -> vai alla definizione.

**Criterio completamento:**
- [ ] Hover mostra info su types, agents, protocols
- [ ] Completion per keyword e nomi definiti
- [ ] Go-to-definition per types e agents
- [ ] Test del language server
- [ ] Guardiana verifica 9.5/10

---

### D6: Guardiana Audit Finale + Launch

**Review cross-cutting di tutto l'ecosistema.**
README aggiornata con screenshot, link al playground, VS Code Marketplace.
Annuncio community.

---

## RIEPILOGO

```
+================================================================+
|   SUBROADMAP FASE D: L'ECOSISTEMA                                |
+================================================================+

FASE D1: Syntax Highlighting         [####################] DONE (S426, 9.5/10)
  TextMate grammar + VS Code ext       1 sessione!
  Pubblicazione Marketplace            (pending publisher account)

FASE D2: LSP Base (lu lsp)           [####################] DONE (S426, 9.5/10)
  pygls + diagnostics in tempo reale   1 sessione! (con D1)
  VS Code collegato al server

FASE D3: Playground Online            [####################] DONE (S429, LIVE!)
  Monaco + Pyodide + GitHub Pages      v0.2.0 su PyPI, deploy automatico
  URL: https://rafapra3008.github.io/cervellaswarm/
  "Try it in 30 seconds"

FASE D4: "A Tour of LU"              [....................] TODO
  Tutorial interattivo 18+ step        2-3 sess
  Integrato nel playground

FASE D5: LSP Avanzato                [....................] TODO
  Hover + Completion + Go-to-def       2-3 sess

FASE D6: Guardiana Finale + Launch   [....................] TODO
  Audit cross-cutting + annuncio       1 sess

EFFORT TOTALE: 10-15 sessioni (~2-3 settimane)
ORDINE: D1 -> D2 -> D3 -> D4 -> D5 -> D6
AUDIT: Guardiana dopo OGNI step
```

---

## DIPENDENZE

```
FASE A+B+C (COMPLETE - 25 moduli, 2806 test)
   |
   v
D1 (Syntax Highlighting - standalone)
   |
   v
D2 (LSP - dipende da D1 per extension, aggiunge pygls)
   |
   v
D3 (Playground - puo partire in parallelo a D2)
   |
   v
D4 (Tour - dipende da D3 per playground interattivo)
   |
   v
D5 (LSP Avanzato - dipende da D2)
   |
   v
D6 (Launch - dipende da tutto)
```

D1 e D3 sono INDIPENDENTI e possono partire in parallelo.
D2 e D4 hanno dipendenze lineari.

---

## METRICHE TARGET

| Metrica | Target |
|---------|--------|
| VS Code extension installazioni | 100+ primo mese |
| Playground visite | 500+ primo mese |
| Tutorial completamenti | 50+ primo mese |
| LSP diagnostics latency | < 200ms |
| Test totali (fine D6) | 3000+ |
| Zero dependencies (core) | MANTENUTE |
| pygls come optional dep | `[lsp]` extra |

---

## SUCCESS CRITERIA

- [ ] Un developer trova il repo e in 30 secondi sta provando nel browser
- [ ] Un developer installa la VS Code extension e vede errori inline
- [ ] Un non-developer completa il tutorial e capisce "types + agents + protocols"
- [ ] Il playground funziona senza backend ($0 costo)
- [ ] Il core package resta ZERO DEPS
- [ ] Guardiana 9.5/10 su ogni step

---

## IL PARALLELO STORICO

```
1991: Python nasce. Guido dice: "codice leggibile per gli umani."
      Non ha LSP, non ha IDE, non ha playground.
      Ha solo: la visione + una REPL + un tutorial.
      E bastato.

2015: Rust 1.0. Ha: Cargo, crates.io, playground, The Rust Book.
      L'ecosistema era pronto DAL GIORNO 1.
      Lezione: preparati PRIMA di lanciare.

2024: Gleam 1.0. Ha: LSP nel binary, formatter, pkg manager, playground WASM.
      TUTTO in un singolo comando. Zero configurazione.
      Lezione: less is more, ma quel "less" deve funzionare PERFETTAMENTE.

2026: Lingua Universale. Ha: 25 moduli, 2806 test, ZERO deps, CLI, REPL.
      Manca: l'ecosistema che porta il mondo dentro.
      Fase D: costruiamolo.
```

---

## NOTA SULL'IDEA DELLA VM

La Researcher ha analizzato 4 opzioni. Il verdetto:
- **Pyodide nel browser**: PERFETTO per playground pubblico ($0)
- **Dev VM per il team**: NON ORA. Suite 0.91s, GH Actions sufficiente.
- **Se/quando arrivano utenti reali**: aggiungere Fly.io backend per salvataggio/condivisione.

La "VM attiva" ha SENSO come playground Pyodide: una pagina web dove
il linguaggio VIVE e chiunque puo provarlo. Non come server di sviluppo.

---

> "Se nessuno l'ha fatto prima, e perche aspettavano noi."
> "Fatto BENE > Fatto VELOCE."
> "Ultrapassar os proprios limites!"

*Cervella Regina - CervellaSwarm S425*
*Fonti: 3 report Researcher (46+ fonti), studi Python/Rust/Go/Gleam/Zig/Roc*
