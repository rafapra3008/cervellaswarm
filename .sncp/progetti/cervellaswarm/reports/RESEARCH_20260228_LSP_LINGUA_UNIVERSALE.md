# LSP + Editor Tooling - Ricerca Lingua Universale

> **Data:** 2026-02-28
> **Researcher:** Cervella Researcher
> **Status:** COMPLETA
> **Fonti consultate:** 12 (pygls docs, LSP spec, Gleam LS, VS Code API, Pyodide, tree-sitter HN, Rust Playground GitHub, vscode publishing docs)

---

## 1. LSP - Come Funziona

### Architettura Client-Server

```
Editor (VS Code/Neovim/Zed)          Language Server (nostro _lsp.py)
        |                                      |
   LSP Client  <--- JSON-RPC 2.0 --->   LanguageServer
        |                                      |
   TextDocument                        Parser + AST + Checker
```

- Il server gira come **processo separato** (STDIO o TCP)
- Comunicazione via **JSON-RPC 2.0** - messaggi asincroni
- Il client (editor) ANNUNCIA le sue capabilities, il server risponde con le sue
- Entrambi dichiarano esplicitamente cosa supportano -> **graceful degradation**
- Trasporto: STDIO (il piu semplice), TCP/IP, WebSocket

### Il Lifecycle

```
Client -> initialize(capabilities) -> Server
Server -> InitializeResult(capabilities) -> Client
Client -> initialized() [notifica]
[... normale lavoro ...]
Client -> shutdown() -> Server
Client -> exit() -> Server
```

### Capabilities - Essenziali vs Nice-to-Have

**Tier 1 - ESSENZIALI (implementare subito):**
| Capability | Valore | Note |
|-----------|--------|------|
| `textDocument/didOpen` | Notifica apertura | Triggera parsing |
| `textDocument/didChange` | Notifica modifica | Re-parsing live |
| `textDocument/publishDiagnostics` | Errori/warning | Usiamo gia line/col! |

**Tier 2 - ALTO VALORE (sessione dopo):**
| Capability | Valore | Note |
|-----------|--------|------|
| `textDocument/hover` | Info al cursore | Tipo, doc, valore |
| `textDocument/completion` | Autocomplete | Keywords, agent names |
| `textDocument/definition` | Go-to-definition | Per protocol/agent refs |

**Tier 3 - NICE TO HAVE (futuro):**
| Capability | Valore |
|-----------|--------|
| `textDocument/references` | Find all references |
| `textDocument/rename` | Rename refactoring |
| `textDocument/formatting` | Auto-format |
| `textDocument/semanticTokens` | Syntax highlighting avanzato |

---

## 2. Implementazioni di Riferimento

### pygls - Il Framework Python per LSP

- **PyPI:** `pygls` (open source, OpenLaw Library)
- **Versione attuale:** v2.0.1 (stabile)
- **Python:** 3.9+
- **Caratteristica chiave:** implementazione minima in ~20 righe di codice
- Supporta STDIO, TCP, WebSocket
- Sia sync che async (asyncio)
- **ZERO dipendenze runtime obbligatorie** (solo `lsprotocol` per le strutture dati)
- Supporto sperimentale Pyodide (Python-in-browser!)

**Esempio diagnostics: 70 righe totali** per un server che:
1. Riceve `didOpen` / `didChange`
2. Parsa il documento con regex
3. Emette diagnostics con line/col

Per noi: il nostro parser gia produce `Loc(line, col)` e i nostri errori hanno gia tutto il necessario.

### Gleam Language Server - Il Caso Studio Piu Rilevante

Gleam e il caso piu simile al nostro:
- Linguaggio nuovo, single binary, toolchain unificata
- LSP bundlato nel compilatore: `gleam lsp`
- Implementato in Rust (ma il pattern e lo stesso)
- Funzionalita: diagnostics, hover, completion, go-to-def, rename, 30+ code actions
- Supporta: VS Code, Neovim, Helix, Zed, qualsiasi editor LSP-compatible

**Lezione chiave:** Il LSP NON e un progetto separato. E una capability della CLI esistente.
`lu lsp` -> avvia il language server. Esattamente come `gleam lsp`.

### rust-analyzer e gopls

Troppo grandi per il nostro caso. Sono state scritte da zero, richiedono anni-persona.
**Non sono il modello giusto per noi.**

### Costo Realistico per un Linguaggio Piccolo

Basandosi su pygls + il nostro codice esistente:
- **Tier 1 (diagnostics only):** ~200-300 righe Python. **1 sessione.**
- **Tier 1+2 (+ hover + completion):** ~600-800 righe. **2-3 sessioni.**
- **Full MVP (tutti Tier 1+2+3):** ~1500 righe. **5-7 sessioni.**

**Il nostro vantaggio:** Abbiamo gia il parser, AST con Loc, error system con LU-N codes.
Praticamente il "motore" del LSP e gia scritto. pygls e solo il "wrapper di rete".

---

## 3. VS Code Extension

### Struttura

```
lingua-universale-vscode/
  package.json          # manifest extension
  client/
    extension.ts        # LSP client (TypeScript, ~50 righe)
  syntaxes/
    lingua-universale.tmLanguage.json  # syntax highlighting
  language-configuration.json          # brackets, comments
```

### TextMate Grammar (.tmLanguage.json)

- JSON (o YAML convertito a JSON)
- Basato su Oniguruma regex
- Scope names standard: `keyword.control.lu`, `string.quoted.lu`, etc.
- VS Code lo carica nativamente - ZERO codice TypeScript necessario per highlighting

**Esempio scope names per Lingua Universale:**
```json
{
  "name": "Lingua Universale",
  "fileTypes": ["lu"],
  "scopeName": "source.lu",
  "patterns": [
    { "match": "\\b(agent|protocol|step|choice)\\b", "name": "keyword.control.lu" },
    { "match": "\\b(always_terminates|no_deadlock)\\b", "name": "keyword.other.property.lu" },
    { "match": "\"[^\"]*\"", "name": "string.quoted.double.lu" },
    { "match": "//.*$", "name": "comment.line.double-slash.lu" },
    { "match": "\\b[0-9]+(\\.[0-9]+)?\\b", "name": "constant.numeric.lu" }
  ]
}
```

### Collegamento al Language Server

Il client TypeScript e minimalista (~50-80 righe):

```typescript
import { LanguageClient, ServerOptions } from 'vscode-languageclient/node';

const serverOptions: ServerOptions = {
  command: 'lu',
  args: ['lsp']  // lu lsp -> avvia il server su STDIO
};

const client = new LanguageClient('lingua-universale', 'Lingua Universale', serverOptions, clientOptions);
client.start();
```

### Pubblicazione VS Code Marketplace

**Requisiti minimi:**
1. Microsoft Account (gratis)
2. Azure DevOps PAT (Personal Access Token) (gratis)
3. `npm install -g @vscode/vsce` (tool CLI)
4. `vsce package` -> genera `.vsix`
5. `vsce publish` -> pubblica

**Non richiesto:** numero minimo di utenti, review umana obbligatoria per estensioni normali.

**Open VSX Registry:** alternativa open-source per VSCodium, Gitpod, Zed (consigliato pubblicare su entrambi).

---

## 4. tree-sitter vs TextMate Grammar

### Confronto per un Linguaggio Nuovo

| Criterio | TextMate | tree-sitter |
|---------|----------|-------------|
| Complessita setup | BASSA (JSON regex) | ALTA (C/Rust parser, build step) |
| Accuratezza | Media (regex-based) | ALTA (full parse tree) |
| Funzionalita | Syntax only | Syntax + code folding + structural navigation |
| Editor support | VS Code, Atom, Sublime | Neovim, Helix, Zed, Emacs, GitHub |
| VS Code support | Nativo | Parziale (via semantic tokens) |
| Manutenzione | Facile | Complessa |
| Prima implementazione | RAPIDA | Lenta (giorni) |

### Raccomandazione

**Fase D immediata:** TextMate grammar per VS Code. Rapido, sufficiente, funziona subito.
**Fase E futura:** tree-sitter grammar per editor moderni (Neovim, Helix, Zed).

Il tree-sitter e il futuro, ma richiede:
- Una grammar in JavaScript per tree-sitter-cli
- Compilazione a C/WASM
- Binding per ogni editor

Non ha senso farlo prima di avere il LSP funzionante.

---

## 5. Playground Online

### Opzioni per Python-based

**Opzione A: Pyodide (Python in WebAssembly) - CONSIGLIATA**

Pyodide compila CPython a WebAssembly. Il browser esegue Python nativo.

- `micropip.install('cervellaswarm-lingua-universale')` -> installa il nostro package
- ZERO backend necessario - tutto nel browser
- Sicuro per definizione (sandbox WebAssembly)
- pygls stessa ha supporto Pyodide sperimentale
- Ottimo per demo, tutorial, "Try it now"

**Limitazione:** Start lento (~3-5 secondi per caricare CPython-WASM). Poi velocissimo.
**Soluzione:** Loading screen con messaggio "Preparing Lingua Universale..." (come fanno tutti).

**Opzione B: Server-side con Docker sandbox**

Come fa Rust Playground:
- React frontend -> Iron/FastAPI backend -> Docker container isolato
- Container: no network, limite CPU/memoria, timeout esecuzione
- Piu veloce di Pyodide, piu flessibile
- Ma richiede infrastruttura (server, Docker, gestione costi)

**Opzione C: Hybrid**

- Pyodide per il playground base (free, no backend)
- Docker per funzionalita avanzate (share code, persistenza)

### Architettura Consigliata per il Playground

```
Browser (HTML + JS)
  |
  +-- Monaco Editor (stesso editor di VS Code, free)
  |     - syntax highlighting via TextMate grammar
  |     - editor professionale
  |
  +-- Pyodide (CPython-WASM)
        - carica cervellaswarm-lingua-universale
        - lu run / lu check / lu verify
        - output nel pannello risultati
```

**Stack:** Monaco Editor + Pyodide + HTML statico = deployable su GitHub Pages. **GRATIS.**

---

## 6. Architettura Raccomandata per il Nostro LSP

### Il Piano "lu lsp"

```python
# packages/lingua-universale/src/cervellaswarm_lingua_universale/_lsp.py

from pygls.server import LanguageServer
from lsprotocol import types
from ._parser import Parser
from ._tokenizer import Tokenizer
from .errors import humanize

lu_server = LanguageServer("lingua-universale-lsp", "v0.1")

@lu_server.feature(types.TEXT_DOCUMENT_DID_OPEN)
def did_open(ls, params):
    _validate(ls, params.text_document)

@lu_server.feature(types.TEXT_DOCUMENT_DID_CHANGE)
def did_change(ls, params):
    _validate(ls, params.text_document)

def _validate(ls, text_document):
    text = ls.workspace.get_document(text_document.uri).source
    try:
        tokens = Tokenizer(text).tokenize()
        Parser(tokens).parse()
        ls.publish_diagnostics(text_document.uri, [])  # no errors
    except SyntaxError as e:
        diag = types.Diagnostic(
            range=types.Range(
                start=types.Position(line=e.line-1, character=e.col),
                end=types.Position(line=e.line-1, character=e.col+1)
            ),
            message=str(e),
            severity=types.DiagnosticSeverity.Error,
            code=e.code  # LU-N001, etc.
        )
        ls.publish_diagnostics(text_document.uri, [diag])

def main():
    lu_server.start_io()
```

**Integrazione CLI:** aggiungere `lu lsp` in `_cli.py`:
```python
elif command == "lsp":
    from ._lsp import main as lsp_main
    lsp_main()
```

### Dipendenze Necessarie

```toml
# pyproject.toml - aggiungere a [project.dependencies]
dependencies = [
    "pygls>=2.0.0",
    "lsprotocol",
]
```

ATTENZIONE: questo introduce 2 dipendenze esterne per la prima volta nel package.
La filosofia "ZERO deps" vale per il core. Il LSP e un modulo opzionale.
Soluzione: `extras_require = {"lsp": ["pygls", "lsprotocol"]}` -> `pip install lingua-universale[lsp]`

---

## 7. Ordine di Implementazione Consigliato (Timeline)

### Fase D1: Foundation Visiva (1 sessione)

**Step D1.1: TextMate Grammar + VS Code Extension base**
- `lingua-universale.tmLanguage.json` (keywords, strings, comments, numbers)
- `package.json` extension manifest
- `language-configuration.json` (brackets, indentation)
- Test: apri un `.lu` file in VS Code -> colori corretti
- Effort: ~100 righe JSON, niente Python

**Deliverable:** `.vsix` installabile localmente

### Fase D2: Language Server Minimo (1-2 sessioni)

**Step D2.1: `lu lsp` - Diagnostics Only**
- `_lsp.py` (~200 righe)
- Integrazione con `_cli.py`
- `did_open` + `did_change` -> parser -> diagnostics
- I nostri LU-N codes come diagnostic codes
- Test: VS Code mostra errori di sintassi nei file `.lu`

**Deliverable:** `lu lsp` funzionante, integrato con VS Code extension

### Fase D3: LSP Ricco (2-3 sessioni)

**Step D3.1: Hover**
- Su `agent MyAgent` -> mostra tipo e proprietà
- Su `step foo` -> mostra step definition
- Su errore -> mostra spiegazione human-friendly (usiamo `errors.py`!)

**Step D3.2: Completion**
- Keywords del linguaggio: `agent`, `protocol`, `step`, `choice`, `use`
- Property names: `always_terminates`, `no_deadlock`, etc.
- Agent/protocol names usati nel file corrente

**Step D3.3: Go-to-Definition**
- Click su `agent MyAgent` usato in un `step` -> vai alla definizione

### Fase D4: Playground Online (1-2 sessioni)

**Step D4.1: Monaco + Pyodide**
- HTML singolo file con Monaco Editor embedded
- Pyodide che carica `cervellaswarm-lingua-universale` via micropip
- Output panel con risultati di `lu run`
- Deploy su GitHub Pages

**Step D4.2: Publish**
- VS Code Marketplace
- Open VSX Registry

---

## 8. Stima Effort Totale

| Fase | Effort | Valore |
|------|--------|--------|
| D1 TextMate + Extension base | 1 sessione | ALTO - visibilita immediata |
| D2 LSP diagnostics | 1-2 sessioni | ALTISSIMO - developer experience |
| D3 Hover + Completion | 2-3 sessioni | ALTO - produttivita |
| D3 Go-to-def + refactoring | 2-3 sessioni | MEDIO - comfort |
| D4 Playground online | 1-2 sessioni | ALTISSIMO - acquisizione utenti |
| tree-sitter grammar | 2-3 sessioni | MEDIO - dopo MVP |

**MVP realistico (D1+D2+D4):** 3-5 sessioni. Alta visibilita, basso sforzo.

---

## 9. Vantaggi Esistenti del Nostro Codebase

Il nostro parser e GIA ottimizzato per il LSP senza saperlo:

| Cosa abbiamo | Come si usa nel LSP |
|-------------|---------------------|
| `Loc(line, col)` in ogni AST node | Diagnostics precise, hover positioning |
| LU-N error codes (74 codici) | Diagnostic codes linkabili alla docs |
| Error messages Rust-style con context | Diagnostic messages gia pronti |
| `lu check` cmd esistente | Base per `_validate()` nel server |
| `_parser.py` pure Python | Riusabile direttamente, nessun porting |
| 3 locali (en, it, pt) | Diagnostics localizzate! |
| `errors.py` con `humanize()` | Trasformazione automatica errori -> messaggi |

**Stimiamo che il 60-70% del lavoro "pesante" del LSP sia gia fatto.**

---

## 10. Raccomandazione Finale

**Ordine consigliato per massimo impatto/effort:**

```
1. SUBITO: TextMate grammar + VS Code extension (1 sessione) -> Screenshot wow
2. DOPO:   lu lsp + diagnostics (1-2 sessioni) -> Developer experience reale
3. DOPO:   Playground online con Pyodide (1-2 sessioni) -> Acquisizione utenti
4. POI:    Hover + Completion (2-3 sessioni) -> Produttivita completa
5. FUTURO: tree-sitter grammar (quando community cresce)
```

**Stack raccomandato:**
- Python LSP: `pygls` v2.0.1 (dependency opzionale via extras)
- VS Code client: TypeScript (50 righe, template esistente)
- Syntax: TextMate grammar JSON (oggi), tree-sitter (futuro)
- Playground: Monaco Editor + Pyodide (deploy gratuito GitHub Pages)
- Publishing: vsce + Open VSX Registry (entrambi gratis)

---

## Fonti

- [pygls GitHub](https://github.com/openlawlibrary/pygls)
- [pygls Documentation v2.0.1](https://pygls.readthedocs.io/en/stable/index.html)
- [LSP Official Spec 3.17](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/)
- [LSP Overview - Microsoft](https://microsoft.github.io/language-server-protocol/overviews/lsp/overview/)
- [Gleam Language Server](https://gleam.run/language-server/)
- [VS Code Language Server Extension Guide](https://code.visualstudio.com/api/language-extensions/language-server-extension-guide)
- [VS Code Syntax Highlight Guide](https://code.visualstudio.com/api/language-extensions/syntax-highlight-guide)
- [VS Code Publishing Extensions](https://code.visualstudio.com/api/working-with-extensions/publishing-extension)
- [Pyodide - Python in WebAssembly](https://pyodide.org/)
- [Rust Playground Source](https://github.com/rust-lang/rust-playground)
- [tree-sitter vs TextMate HN Discussion](https://news.ycombinator.com/item?id=35770913)
- [pygls Publish Diagnostics Example](https://pygls.readthedocs.io/en/latest/servers/examples/publish-diagnostics.html)
