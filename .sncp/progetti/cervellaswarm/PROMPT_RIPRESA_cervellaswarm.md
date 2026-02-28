# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-02-28 - Sessione 426
> **STATUS:** FASE D IN CORSO! D1 + D2 COMPLETATI (9.5/10 entrambi). Prossimo: D3 Playground.

---

## SESSIONE 426 - Cosa e successo

### 1. D1: Syntax Highlighting + VS Code Extension -- COMPLETATO (9.5/10)
- **TextMate grammar** (`lingua-universale.tmLanguage.json`): 33 costrutti, 100% copertura
- **VS Code extension**: package.json, language-configuration, icon 128x128, README
- **Test**: 47/47 check su 5 file .lu
- **Guardiana**: 2 P2 fixati (Confident scope, confidence levels lowercase)
- ID: `cervellaswarm.lingua-universale`

### 2. D2: LSP Base (lu lsp) -- COMPLETATO (9.5/10)
- **_lsp.py**: language server con pygls v2 (STDIO), ~200 righe
  - didOpen + didChange + didSave -> parse() -> diagnostics
  - humanize() per errori ricchi: code LU-N + message + suggestion
  - Coordinate: LU 1-indexed -> LSP 0-indexed
  - didClose pulisce diagnostics
  - `_source_diagnostics()` separata per testabilita
- **CLI**: `lu lsp` subcommand (lazy import, zero impatto su altri comandi)
- **pyproject.toml**: `[lsp]` extra con `pygls>=2.0`. Core resta ZERO DEPS
- **VS Code client**: `extension.ts` lancia `lu lsp` via STDIO
  - Configurazione `lingua-universale.luPath` per path custom
  - Gestione graceful se `lu` non trovato
- **Test**: 22 nuovi test (valid, tokenize errors, parse errors, structure, edge cases)
- **Guardiana**: 2 P2 fixati (__version__ in server, dead import)

### 3. Numeri aggiornati
- **2828 test** (2806 + 22 LSP), 0 regressioni, 0.97s
- **26 moduli .py** (25 + _lsp.py)

---

## MAPPA SITUAZIONE

```
LINGUAGGIO CERVELLASWARM:
  FASE A+B: COMPLETE (9.5+ media)
  FASE C: Il Linguaggio -- COMPLETA! (S407-S425)
  FASE D: L'Ecosistema -- IN CORSO (S426+)
    D1: Syntax Highlighting   [####################] DONE! (S426, 9.5/10)
    D2: LSP Base (lu lsp)     [####################] DONE! (S426, 9.5/10)
    D3: Playground Online      [....................] PROSSIMO
    D4: "A Tour of LU"        [....................] TODO
    D5: LSP Avanzato           [....................] TODO
    D6: Guardiana Finale       [....................] TODO
```

---

## I NUMERI TOTALI

| Metrica | Valore |
|---------|--------|
| Test totali | **2828** |
| Moduli .py | **26** |
| Codici errore LU | **74** (3 lingue) |
| File .lu | **5** |
| Dipendenze core | **ZERO** |
| Dipendenze LSP (optional) | **pygls>=2.0** |
| PyPI packages LIVE | **9/9** |
| VS Code extension | **installabile** (.vsix) |
| LSP server | **funzionante** (lu lsp, STDIO) |
| Tempo suite | 0.97s |

---

## STRUTTURA FILE NUOVI (D1 + D2)

```
extensions/lingua-universale-vscode/    # VS Code extension
  package.json                          # v0.2.0 con LSP client
  language-configuration.json           # brackets, comments, folding
  syntaxes/lingua-universale.tmLanguage.json  # TextMate grammar
  src/extension.ts                      # LSP client (lancia lu lsp)
  tsconfig.json                         # TypeScript config
  tests/test_grammar_coverage.py        # 47/47 grammar check
  README.md, CHANGELOG.md, LICENSE, icon.png

packages/lingua-universale/
  src/.../                              # Package
    _lsp.py                             # NUOVO: LSP server (~200 righe)
    _cli.py                             # AGGIORNATO: +lu lsp subcommand
  pyproject.toml                        # AGGIORNATO: +[lsp] optional dep
  tests/test_lsp.py                     # NUOVO: 22 test LSP
```

---

## PROSSIMO: D3 -- Playground Online (Pyodide)

**Subroadmap completa:** `.sncp/roadmaps/SUBROADMAP_FASE_D_ECOSISTEMA.md`

**D3 in breve:**
- Monaco Editor + Pyodide (Python in WASM) + GitHub Pages
- `micropip.install("cervellaswarm-lingua-universale")` nel browser
- "Try it in 30 seconds" senza installare nulla
- Costo: $0 (statico su GitHub Pages)
- 1-2 sessioni, rischio BASSO

**Decisioni gia prese:**
- Stack: Pyodide (WASM) + Monaco Editor (come VS Code)
- Deploy: GitHub Pages ($0)
- Il nostro ZERO DEPS e' il caso PERFETTO per Pyodide

---

## Fix documentazione ancora da fare

| Doc | Problema | Priorita |
|-----|----------|----------|
| MAPPA_LINGUAGGIO | Numeri fermi a S398 | P2 |
| NORD LU | Numeri fermi a S380 | P2 |
| README.md pubblico | Numeri stale | P3 |
| VS Code Marketplace | Pubblicazione (serve Azure DevOps publisher) | P3 |

---

## Lezioni Apprese (S426)

### Cosa ha funzionato bene
- **2 step in 1 sessione** -- D1 + D2 completati insieme (entrambi 9.5/10)
- **Ricerca parallela** -- Explorer + Researcher in parallelo, poi build mirato
- **_source_diagnostics() separata** -- testabile senza server = 22 test unit puri
- **humanize() bridge** -- errori LU-N con code + suggestion nel LSP diagnostic

### Pattern confermato
- **"Step + Guardiana audit"** (33a e 34a volta) -- il metodo funziona SEMPRE

---

*"La domanda e la risposta nello STESSO linguaggio." - Rafa*
*"Ultrapassar os proprios limites!" - Rafa & Cervella*
