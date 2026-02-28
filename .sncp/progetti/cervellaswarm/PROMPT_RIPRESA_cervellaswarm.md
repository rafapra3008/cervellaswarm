# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-02-28 - Sessione 427
> **STATUS:** BLOCCO SCOPERTO! PyPI v0.1.1 vecchio (14 moduli). Serve v0.2.0 (26 moduli) PRIMA di D3 Playground.

---

## SESSIONE 427 - Cosa e successo

### 1. D3 Playground: Costruito ma BLOCCATO
- **playground/index.html** (2187 righe): Monaco Editor + Pyodide, dark theme, split view
- **playground/examples.js** (205 righe): 4 esempi precaricati (hello, confidence, multiagent, ricette)
- Testato nel browser: layout OK, Pyodide carica OK, Monaco funziona
- **BLOCCANTE:** `check_source()` e `run_source()` (Fase C) NON sono nel package su PyPI
- PyPI v0.1.1 ha solo 14 moduli (Fase A+B). Servono i 26 moduli (Fase A+B+C+D)

### 2. Audit Guardiana Qualita: Score 5.5/10 coerenza PyPI vs locale
- **Report completo:** `.sncp/progetti/cervellaswarm/ricerche/AUDIT_PYPI_COERENZA.md`
- **12 moduli mancanti su PyPI**: tutta Fase C (_tokenizer, _ast, _parser, _contracts, _compiler, _interop, _grammar_export, _eval, _colors, _repl, _cli) + D2 (_lsp)
- **README.md massicciamente stale**: dice "9 moduli, 84 symbols, 1273 test" -- reale: 26 moduli, 124 symbols, 2828 test
- **CHANGELOG.md**: manca TUTTA Fase C
- pyproject.toml description troppo stretta

### 3. Subroadmap "Organizza la Casa" creata
- **Path:** `.sncp/roadmaps/SUBROADMAP_ORGANIZZA_CASA_v020.md`
- 6 step: bump version -> CHANGELOG -> README -> test+build -> publish -> audit
- PREREQUISITO per D3 Playground

### 4. Ricerca PTC (Programmatic Tool Calling) -- background
- **Report:** `.sncp/progetti/cervellaswarm/ricerche/PTC_RESEARCH_REPORT.md`
- PTC di Anthropic: 37-86% riduzione token, GA dal 17 Feb 2026
- **Verdetto: MONITORARE, non implementare** -- Claude Code CLI non supporta PTC (issue #12836)
- Non blocca il nostro lavoro, da rivalutare quando Anthropic lo porta in Claude Code

---

## MAPPA SITUAZIONE

```
LINGUAGGIO CERVELLASWARM:
  FASE A+B: COMPLETE (9.5+ media)
  FASE C: Il Linguaggio -- COMPLETA! (S407-S425)
  FASE D: L'Ecosistema -- IN CORSO (S426+)
    D1: Syntax Highlighting   [####################] DONE! (S426, 9.5/10)
    D2: LSP Base (lu lsp)     [####################] DONE! (S426, 9.5/10)
    D3: Playground Online      [####................] BLOCCATO (serve v0.2.0 PyPI)
    D4: "A Tour of LU"        [....................] TODO
    D5: LSP Avanzato           [....................] TODO
    D6: Guardiana Finale       [....................] TODO

  BLOCCO: Organizza Casa (v0.2.0)
    Step 1: Bump versione      [....................] TODO
    Step 2: CHANGELOG v0.2.0   [....................] TODO
    Step 3: README aggiornato  [....................] TODO
    Step 4: Test + build wheel [....................] TODO
    Step 5: Pubblica su PyPI   [....................] TODO
    Step 6: Guardiana audit    [....................] TODO
```

---

## PROSSIMA SESSIONE: Organizza la Casa (v0.2.0)

**Subroadmap:** `.sncp/roadmaps/SUBROADMAP_ORGANIZZA_CASA_v020.md`

### Step 1-3: Versione + Docs (~30 min)
- `pyproject.toml`: version "0.1.1" -> "0.2.0", description aggiornata, keywords
- `__init__.py`: fallback "0.1.1" -> "0.2.0"
- CHANGELOG.md: sezione [0.2.0] con tutti i moduli Fase C (12 nuovi)
- README.md: numeri reali (26 moduli, 124 symbols, 2828 test)

### Step 4-5: Build + Publish (~10 min)
- pytest: conferma 2828 test
- python -m build: wheel v0.2.0
- Verifica wheel contiene 27 file .py
- Pubblica su PyPI (Trusted Publisher via GitHub Actions)

### Step 6: Audit (~10 min)
- Guardiana conferma score >= 9.5/10 coerenza
- `pip install cervellaswarm-lingua-universale` -> v0.2.0
- `from cervellaswarm_lingua_universale import check_source` -> funziona

### DOPO: D3 Playground RIPRENDE
- Il playground (playground/index.html) e GIA costruito e funzionante
- Serve SOLO che PyPI abbia v0.2.0 con check_source/run_source
- Testare nel browser, Guardiana audit, deploy GitHub Pages

---

## I NUMERI TOTALI

| Metrica | Valore |
|---------|--------|
| Test totali | **2828** |
| Moduli .py | **26** |
| Codici errore LU | **74** (3 lingue) |
| File .lu | **5** |
| Dipendenze core | **ZERO** |
| PyPI version | **0.1.1** (STALE! Serve 0.2.0) |
| PyPI packages LIVE | **9/9** |
| Playground | **costruito** (playground/index.html, bloccato da PyPI) |
| Tempo suite | 0.97s |

---

## FILE NUOVI (S427)

```
playground/
  index.html          # 2187 righe - Monaco + Pyodide, dark theme, split view
  examples.js         # 205 righe - 4 esempi .lu precaricati

.sncp/roadmaps/
  SUBROADMAP_ORGANIZZA_CASA_v020.md   # Piano per release v0.2.0

.sncp/progetti/cervellaswarm/ricerche/
  AUDIT_PYPI_COERENZA.md              # Audit Guardiana (5.5/10)
  PTC_RESEARCH_REPORT.md              # Ricerca Programmatic Tool Calling
```

---

## Lezioni Apprese (S427)

### Cosa ha funzionato bene
- **Audit Guardiana PRIMA di procedere** -- ha scoperto il gap critico PyPI
- **Costituzione riletta** -- "RICERCA prima di implementare", "Su carta != REALE"
- **Ricerca parallela PTC** -- ha girato in background senza bloccare il lavoro

### Cosa non ha funzionato
- **Playground costruito PRIMA di verificare PyPI** -- spreco di effort (il codice e' OK ma non funziona end-to-end)
- Avremmo dovuto verificare il package PyPI PRIMA di costruire il playground

### Pattern candidato
- **"Verifica dipendenze esterne PRIMA di costruire"** -- Evidenza: S427 (playground bloccato da PyPI stale). Azione: MONITORARE

---

*"La casa deve essere in ordine prima di invitare ospiti."*
*"Ultrapassar os proprios limites!" - Rafa & Cervella*
