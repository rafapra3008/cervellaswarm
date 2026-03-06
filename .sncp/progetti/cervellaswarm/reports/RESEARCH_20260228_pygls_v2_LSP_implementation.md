# pygls v2 - Ricerca Implementazione LSP per D2
> **Data:** 2026-02-28
> **Researcher:** Cervella Researcher
> **Status:** COMPLETA
> **Fonti:** 11 consultate (pygls docs, PyPI, GitHub source, migration guide, pytest-lsp, lsp-devtools, VS Code API)

---

## 1. pygls v2.x - Versione e Dipendenze

**Versione stabile:** `2.0.1` (rilasciata 26 gennaio 2026)
**Python richiesto:** >=3.9
**Dipendenze runtime:**
- `lsprotocol` (strutture dati LSP - inclusa automaticamente)
- opzionale: `ws` extra per WebSocket transport

**ZERO dipendenze di business logic.** pygls + lsprotocol sono tutto.

### pyproject.toml - Come aggiungere al package

```toml
# Opzione A: dipendenza obbligatoria (piu semplice per MVP)
[project.dependencies]
dependencies = ["pygls>=2.0.0"]

# Opzione B (RACCOMANDATA): extras opzionale - mantiene core ZERO deps
[project.optional-dependencies]
lsp = ["pygls>=2.0.0"]
# Install: pip install cervellaswarm-lingua-universale[lsp]
```

---

## 2. pygls v2 API - Import Paths (CAMBIATI dalla v1!)

```python
# v2 - CORRETTO
from pygls.lsp.server import LanguageServer   # <-- NUOVO path
from pygls.cli import start_server             # <-- avvio server
from pygls.workspace import TextDocument       # <-- tipo documento
from lsprotocol import types                   # <-- tutti i tipi LSP
```

**ATTENZIONE:** L'import `from pygls.server import LanguageServer` e v1. In v2 e `pygls.lsp.server`.

---

## 3. Minimal Complete LSP Server (v2, copia-incolla-funzionante)

```python
# packages/lingua-universale/src/cervellaswarm_lingua_universale/_lsp.py

"""Language Server Protocol server for Lingua Universale (D2).

Avvio: lu lsp  (aggiungere a _cli.py)
Trasporto: STDIO (compatibile con VS Code, Neovim, Helix, Zed, qualsiasi editor LSP)
"""

import logging

from lsprotocol import types
from pygls.cli import start_server
from pygls.lsp.server import LanguageServer
from pygls.workspace import TextDocument


class LinguaUniversaleServer(LanguageServer):
    """LSP server per Lingua Universale."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Cache: uri -> (version, [Diagnostic])
        self._diagnostics: dict[str, tuple[int | None, list[types.Diagnostic]]] = {}

    def validate(self, document: TextDocument) -> None:
        """Parsa il documento e produce diagnostics."""
        from ._parser import parse, ParseError
        from ._tokenizer import TokenizeError

        diagnostics: list[types.Diagnostic] = []
        source = document.source

        try:
            parse(source)
            # Parse OK - nessun errore
        except (ParseError, TokenizeError) as exc:
            # I nostri errori hanno gia line e col!
            line = max(0, exc.line - 1)   # LSP usa 0-indexed
            col = max(0, exc.col)

            # Opzionale: arricchisci il messaggio con humanize()
            message = str(exc)
            try:
                from .errors import humanize, format_error
                herr = humanize(exc)
                message = herr.message
                if herr.suggestion:
                    message += f" -- {herr.suggestion}"
            except Exception:
                pass  # Fallback al messaggio raw

            # Determina error code (LU-N001, etc.)
            code: str | None = None
            try:
                from .errors import humanize
                herr = humanize(exc)
                code = herr.code
            except Exception:
                pass

            diagnostics.append(
                types.Diagnostic(
                    message=message,
                    severity=types.DiagnosticSeverity.Error,
                    range=types.Range(
                        start=types.Position(line=line, character=col),
                        end=types.Position(line=line, character=col + 1),
                    ),
                    code=code,           # "LU-N001" etc.
                    source="lingua-universale",
                )
            )
        except Exception as exc:
            # Errori inaspettati - non crashare il server
            diagnostics.append(
                types.Diagnostic(
                    message=f"Internal error: {exc}",
                    severity=types.DiagnosticSeverity.Warning,
                    range=types.Range(
                        start=types.Position(line=0, character=0),
                        end=types.Position(line=0, character=1),
                    ),
                    source="lingua-universale",
                )
            )

        self._diagnostics[document.uri] = (document.version, diagnostics)

    def _publish_all(self) -> None:
        """Invia tutte le diagnostics al client."""
        for uri, (version, diagnostics) in self._diagnostics.items():
            self.text_document_publish_diagnostics(
                types.PublishDiagnosticsParams(
                    uri=uri,
                    version=version,
                    diagnostics=diagnostics,
                )
            )


# Istanza globale del server
lu_server = LinguaUniversaleServer(
    name="lingua-universale-lsp",
    version="0.1.0",
)


@lu_server.feature(types.TEXT_DOCUMENT_DID_OPEN)
def did_open(ls: LinguaUniversaleServer, params: types.DidOpenTextDocumentParams):
    """Parsa il documento all'apertura."""
    doc = ls.workspace.get_text_document(params.text_document.uri)
    ls.validate(doc)
    ls._publish_all()


@lu_server.feature(types.TEXT_DOCUMENT_DID_CHANGE)
def did_change(ls: LinguaUniversaleServer, params: types.DidChangeTextDocumentParams):
    """Re-parsa ad ogni modifica."""
    doc = ls.workspace.get_text_document(params.text_document.uri)
    ls.validate(doc)
    ls._publish_all()


@lu_server.feature(types.TEXT_DOCUMENT_DID_CLOSE)
def did_close(ls: LinguaUniversaleServer, params: types.DidCloseTextDocumentParams):
    """Pulisce le diagnostics alla chiusura del documento."""
    uri = params.text_document.uri
    ls._diagnostics.pop(uri, None)
    # Invia lista vuota per pulire gli errori nell'editor
    ls.text_document_publish_diagnostics(
        types.PublishDiagnosticsParams(uri=uri, diagnostics=[])
    )


def main() -> None:
    """Entry point: lu lsp"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        filename="/tmp/lu-lsp.log",  # Log su file per non sporcare STDIO
    )
    logging.info("Lingua Universale LSP server starting")
    start_server(lu_server)  # Avvia su STDIO (default)


if __name__ == "__main__":
    main()
```

---

## 4. DiagnosticSeverity - Tutti i Livelli

```python
from lsprotocol import types

types.DiagnosticSeverity.Error       # 1 - Errore bloccante (rosso)
types.DiagnosticSeverity.Warning     # 2 - Warning (giallo)
types.DiagnosticSeverity.Information # 3 - Info (blu)
types.DiagnosticSeverity.Hint        # 4 - Suggerimento (grigio)
```

**Per il nostro caso:**
- `ParseError` / `TokenizeError` -> `Error`
- Futuro: warnings stilistici -> `Warning`
- Futuro: suggerimenti -> `Hint`

---

## 5. Metodi v1 vs v2 - Tabella Comparativa CRITICA

| v1 (SBAGLIATO!) | v2 (CORRETTO) |
|-----------------|---------------|
| `from pygls.server import LanguageServer` | `from pygls.lsp.server import LanguageServer` |
| `ls.publish_diagnostics(uri, diags)` | `ls.text_document_publish_diagnostics(PublishDiagnosticsParams(...))` |
| `ls.workspace.get_document(uri)` | `ls.workspace.get_text_document(uri)` |
| `ls.show_message(msg)` | `ls.window_show_message(ShowMessageParams(...))` |
| `server.start_io()` | `start_server(server)` (via `pygls.cli`) |
| `ls.lsp` | `ls.protocol` |

---

## 6. Integrazione _cli.py

```python
# Aggiungere in _cli.py - subparser "lsp"

def _cmd_lsp(args: argparse.Namespace) -> int:
    """Handle ``lu lsp``."""
    from ._lsp import main as lsp_main
    lsp_main()
    return 0  # Never reached (server runs forever)

# Nel parser:
lsp_parser = subparsers.add_parser("lsp", help="Start the Language Server (STDIO)")
lsp_parser.set_defaults(func=_cmd_lsp)
```

---

## 7. VS Code Extension Client (extension.ts)

Il client TypeScript e ~60 righe. Richiede `vscode-languageclient`:

### package.json - modifiche necessarie

```json
{
  "activationEvents": ["onLanguage:lingua-universale"],
  "main": "./out/extension.js",
  "dependencies": {
    "vscode-languageclient": "^9.0.0"
  },
  "devDependencies": {
    "@types/vscode": "^1.75.0",
    "typescript": "^5.0.0"
  },
  "scripts": {
    "compile": "tsc -p ./"
  }
}
```

**ATTENZIONE:** L'attuale `package.json` dell'extension NON ha `main`, `activationEvents`, o
`dependencies`. Queste vanno aggiunte per supportare il LSP client.

### src/extension.ts - il client completo

```typescript
import * as path from 'path';
import { ExtensionContext, workspace } from 'vscode';
import {
    LanguageClient,
    LanguageClientOptions,
    ServerOptions,
    TransportKind,
} from 'vscode-languageclient/node';

let client: LanguageClient | undefined;

export async function activate(context: ExtensionContext): Promise<void> {
    // Opzione A: usa 'lu' dal PATH (richiede installazione globale)
    const serverOptions: ServerOptions = {
        command: 'lu',
        args: ['lsp'],
        transport: TransportKind.stdio,
    };

    // Opzione B: usa 'python -m ...' con venv (piu robusto)
    // const serverOptions: ServerOptions = {
    //     command: 'python',
    //     args: ['-m', 'cervellaswarm_lingua_universale', 'lsp'],
    //     transport: TransportKind.stdio,
    // };

    const clientOptions: LanguageClientOptions = {
        // Attiva solo per file .lu
        documentSelector: [
            { scheme: 'file', language: 'lingua-universale' }
        ],
        synchronize: {
            // Notifica il server quando cambiano file .lu nel workspace
            fileEvents: workspace.createFileSystemWatcher('**/*.lu'),
        },
    };

    client = new LanguageClient(
        'lingua-universale',          // ID (unico)
        'Lingua Universale LSP',      // Label per UI
        serverOptions,
        clientOptions,
    );

    await client.start();
}

export async function deactivate(): Promise<void> {
    await client?.stop();
    client = undefined;
}
```

### tsconfig.json (necessario per compilare)

```json
{
    "compilerOptions": {
        "module": "commonjs",
        "target": "ES2020",
        "outDir": "out",
        "lib": ["ES2020"],
        "sourceMap": true,
        "rootDir": "src",
        "strict": true
    },
    "include": ["src/**/*"],
    "exclude": ["node_modules", ".vscode-test"]
}
```

---

## 8. Testing - Due Approcci

### Approccio A: Unit test del parser (SUBITO, GIA fattibile)

Non richiede pygls. Testa la logica di _lsp.py separando la validazione:

```python
# tests/test_lsp_validation.py

from cervellaswarm_lingua_universale._lsp import LinguaUniversaleServer
from pygls.workspace import TextDocument

def _make_document(source: str, uri: str = "file:///test.lu") -> TextDocument:
    """Helper: crea un documento fake."""
    return TextDocument(uri=uri, source=source)

def test_valid_document_no_diagnostics():
    server = LinguaUniversaleServer("test", "v0")
    doc = _make_document("agent TestAgent:\n  step foo: send Foo to Bar\n")
    server.validate(doc)
    _, diagnostics = server._diagnostics.get(doc.uri, (None, []))
    assert diagnostics == []

def test_invalid_document_produces_diagnostic():
    server = LinguaUniversaleServer("test", "v0")
    doc = _make_document("INVALID SYNTAX @@@\n")
    server.validate(doc)
    _, diagnostics = server._diagnostics.get(doc.uri, (None, []))
    assert len(diagnostics) >= 1
    assert diagnostics[0].severity.value == 1  # DiagnosticSeverity.Error

def test_diagnostic_has_location():
    server = LinguaUniversaleServer("test", "v0")
    doc = _make_document("agent Good:\n  step s1: @@@\n")
    server.validate(doc)
    _, diagnostics = server._diagnostics.get(doc.uri, (None, []))
    assert len(diagnostics) >= 1
    diag = diagnostics[0]
    # Verifica che la location sia sensata (non 0,0)
    assert diag.range.start.line >= 0
```

### Approccio B: E2E con pytest-lsp (per testing completo)

```bash
pip install pytest-lsp pytest-asyncio
```

```python
# tests/test_lsp_e2e.py
import sys
import pytest
import pytest_lsp
from lsprotocol import types
from pytest_lsp import ClientServerConfig, LanguageClient

@pytest_lsp.fixture(
    scope="module",
    config=ClientServerConfig(
        server_command=[sys.executable, "-m", "cervellaswarm_lingua_universale", "lsp"],
    ),
)
async def client(lsp_client: LanguageClient):
    """Avvia il server e inizializza la sessione."""
    await lsp_client.initialize_session(
        types.InitializeParams(
            capabilities=types.ClientCapabilities(),
            root_uri="file:///tmp/test",
        )
    )
    yield
    await lsp_client.shutdown_session()

@pytest.mark.asyncio(loop_scope="module")
async def test_diagnostics_on_invalid_file(client: LanguageClient):
    """Test E2E: file invalido -> diagnostics."""
    test_uri = "file:///tmp/test/invalid.lu"
    client.text_document_did_open(types.DidOpenTextDocumentParams(
        text_document=types.TextDocumentItem(
            uri=test_uri,
            language_id="lingua-universale",
            version=1,
            text="INVALID @@@\n",
        )
    ))
    # Aspetta le diagnostics (il server le pubblica in modo asincrono)
    await client.wait_for_notification("textDocument/publishDiagnostics")
    assert len(client.diagnostics.get(test_uri, [])) >= 1
```

---

## 9. File Structure - Cosa Creare per D2

```
packages/lingua-universale/
  src/cervellaswarm_lingua_universale/
    _lsp.py                        # NUOVO: server LSP (~100 righe)
  tests/
    test_lsp_validation.py          # NUOVO: unit tests validation logic

extensions/lingua-universale-vscode/
  src/
    extension.ts                   # NUOVO: client TypeScript
  tsconfig.json                    # NUOVO: configurazione TypeScript
  package.json                     # MODIFICA: aggiungere main, deps, activationEvents
```

---

## 10. Considerazioni Architetturali

### STDIO Transport - Come Funziona

```
VS Code                          lu lsp (processo Python)
  |                                     |
  |  ---> JSON-RPC su stdin  ---------->|
  |                                     |  _lsp.py processa
  |  <--- JSON-RPC su stdout <----------|
  |                                     |
  | Logging NON su stdout!              |  -> /tmp/lu-lsp.log
```

**CRITICO:** Il server DEVE loggare su file, MAI su stdout. stdout e usato per il protocollo.

### Syncronizzazione Documento

pygls gestisce automaticamente il buffer del documento in memoria.
`ls.workspace.get_text_document(uri)` ritorna sempre la versione aggiornata dopo ogni `didChange`.

### Errori Struttura Nostra

Siamo fortunati: `ParseError` e `TokenizeError` hanno gia:
- `exc.line` (1-indexed) -> convertire a 0-indexed per LSP: `exc.line - 1`
- `exc.col` (0-indexed) -> usare direttamente
- Messaggio gia formattato con location

`HumanError` da `humanize()` ha anche:
- `herr.code` (LU-N001, etc.) -> usare come `diagnostic.code`
- `herr.message` + `herr.suggestion` -> concatenare per il messaggio

### Dependency Management

Per mantenere ZERO deps nel core, usare extras:
```toml
[project.optional-dependencies]
lsp = ["pygls>=2.0.0"]
```

Il `__main__.py` dovrebbe fare import lazy di `_lsp.py`:
```python
# In _cli.py cmd_lsp():
try:
    from ._lsp import main as lsp_main
except ImportError:
    print("ERROR: LSP support requires: pip install cervellaswarm-lingua-universale[lsp]")
    sys.exit(1)
lsp_main()
```

---

## 11. Pattern di Gleam LSP (per riferimento)

Gleam usa `gleam lsp` come entry point (esattamente il pattern `lu lsp` che vogliamo).
Key insight da Gleam:
- LSP e parte della CLI principale, NON package separato
- Un binary, tutte le funzionalita
- Diagnostics real-time durante typing
- Go-to-definition usando l'AST esistente (che gia hanno i Loc)

Noi siamo in posizione IDENTICA: `_parser.py` produce gia `Loc(line, col)` su ogni nodo AST.

---

## Raccomandazione Implementazione D2

**Step 1 (2h):** Creare `_lsp.py` con il template sopra, collegare a `_cli.py`
**Step 2 (1h):** Test unitari `test_lsp_validation.py` (unit, no LSP client)
**Step 3 (2h):** Modificare `package.json` extension + creare `extension.ts` + `tsconfig.json`
**Step 4 (30min):** Compilare TypeScript + testare in VS Code locale
**Step 5 (1h):** Test E2E con pytest-lsp (opzionale per MVP)

**Stima totale D2:** 1 sessione (6-7h).
**Pre-requisiti:** `pip install pygls` nel venv del package.

---

## Fonti

- [pygls PyPI v2.0.1](https://pypi.org/project/pygls/)
- [pygls GitHub](https://github.com/openlawlibrary/pygls)
- [pygls Getting Started v2](https://pygls.readthedocs.io/en/latest/servers/getting-started.html)
- [pygls Publish Diagnostics Example](https://pygls.readthedocs.io/en/latest/servers/examples/publish-diagnostics.html)
- [pygls Migration Guide v1->v2](https://pygls.readthedocs.io/en/latest/pygls/howto/migrate-to-v2.html)
- [pytest-lsp PyPI](https://pypi.org/project/pytest-lsp/)
- [LSP Devtools](https://lsp-devtools.readthedocs.io/en/latest/)
- [VS Code Language Server Extension Guide](https://code.visualstudio.com/api/language-extensions/language-server-extension-guide)
- [pygls publish_diagnostics.py source](https://github.com/openlawlibrary/pygls/blob/main/examples/servers/publish_diagnostics.py)
- [pygls json_server.py source](https://github.com/openlawlibrary/pygls/blob/main/examples/servers/json_server.py)
- [pygls Releases](https://github.com/openlawlibrary/pygls/releases)
