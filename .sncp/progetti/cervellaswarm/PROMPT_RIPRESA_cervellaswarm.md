# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-02-18 - Sessione 368
> **STATUS:** FASE 1 OPEN SOURCE - F1.1+F1.2+F1.3 COMPLETATE! Prossimo: F1.4 (PyPI publish)

---

## SESSIONE 368 - FASE 1: AST Pipeline Standalone Package

### Contesto
Prima sessione FASE 1. Obiettivo: estrarre il pipeline AST (14 moduli, 396 test) come pacchetto pip standalone `cervellaswarm-code-intelligence`. Metodo: step-by-step con Guardiana audit dopo ogni step (target 9.5/10).

### Cosa abbiamo fatto

**F1.1 - Package skeleton + source files (9.6/10):**
- Creato `packages/code-intelligence/` con layout Hatchling + src/
- Copiato 14 moduli da scripts/utils/ con import normalizzati (relative imports)
- 3 CLI entry points: cervella-search, cervella-impact, cervella-map
- pip install -e . funziona, smoke test OK, wheel build OK
- SPDX headers Apache-2.0 su tutti i 14 file
- Fix: LICENSE "Rafa & Cervella" -> "CervellaSwarm Contributors"
- Fix: __main__ blocks con import corretti dal package

**F1.2 - Test suite standalone (9.5/10):**
- Copiato 20 test files + conftest.py (6774 linee)
- Transformation script bulk: `scripts.utils.xxx` -> `cervellaswarm_code_intelligence.xxx`
- Mock path tutti allineati al package
- File path (real file tests) corretti a `src/cervellaswarm_code_intelligence/`
- Docstring aggiornati (rimossi riferimenti a scripts/utils)
- **396 test raccolti, 395 passed, 1 skipped, 0 failed, 0.47s**

**F1.3 - README killer + CHANGELOG (9.5/10):**
- README 225 righe: architettura ASCII, API reference, limitazioni oneste, CLI examples
- Research pattern tree-sitter (benchmark per dev tools)
- CHANGELOG.md per v0.1.0
- ImpactResult aggiunto a __init__.py exports
- Fix P1 Guardiana: CLI args ordine corretto, --repo-path per cervella-map

### Decisioni S368

| Decisione | Perche |
|-----------|--------|
| Hatchling build backend | PyPA recommended, PEP 639 support |
| Flat layout (no sub-packages) | 14 file non giustificano sub-packages |
| `cervellaswarm_code_intelligence` (underscore) | Python module convention |
| Relative imports | Standard per package standalone, no sys.path hacks |
| Escludere test_generate_worker_context | Non fa parte del pipeline AST |
| Escludere test_semantic_search.py (slow) | Integration test che scansiona tutto il repo |

### Struttura Package

```
packages/code-intelligence/
  pyproject.toml          # Hatchling, PEP 639, Apache-2.0
  README.md               # 225 righe, killer
  CHANGELOG.md            # v0.1.0
  LICENSE + NOTICE
  src/cervellaswarm_code_intelligence/
    __init__.py            # 8 exports (Symbol, ..., ImpactResult, RepoMapper)
    symbol_types.py        # Layer 0: Symbol dataclass
    language_builtins.py   # Layer 0: builtin names
    symbol_cache.py        # Layer 0: LRU cache
    treesitter_parser.py   # Layer 0: AST parsing
    python_extractor.py    # Layer 1: Python symbols
    typescript_extractor.py # Layer 1: TS/JS symbols
    symbol_extractor.py    # Layer 2: orchestrator
    dependency_graph.py    # Layer 3: PageRank graph
    semantic_search.py     # Layer 4: code navigation
    repo_mapper.py         # Layer 4: token-budgeted maps
    impact_analyzer.py     # Layer 4: risk assessment
    cli/                   # 3 CLI entry points
  tests/                   # 20 test files + conftest.py
```

### P3 residui (non bloccanti)
- "Author: Cervella Backend" nei docstring dei moduli (nome agente interno, non personale)
- CHANGELOG minimal (OK per v0.1.0)
- cervellaswarm.com in packages/ (dominio non attivo)
- Hero image da ricreare pulita

---

## PROSSIMI STEP
- **F1.4: PyPI publication** - Trusted Publishing (GitHub Actions workflow)
  - Serve: account PyPI, workflow publish.yml, tag v0.1.0
  - Verificare su macchina pulita prima della pubblicazione
- **Hero image:** Creare immagine/GIF pulita senza riferimenti interni
- **F3 nota:** MCP SNCP KNOWN_PROJECTS hardcoded -> rendere configurabile

---

## ARCHIVIO

| Sessione | Cosa |
|----------|------|
| S337-S348 | Coverage push 41% -> 95% (968 test) |
| S349-S360 | MAPPA MIGLIORAMENTI completata + SNCP 4.0 + POLISH |
| S361 | REGOLA ANTI-DOWNGRADE modelli |
| S362 | OPEN SOURCE STRATEGY! subroadmap 5 fasi |
| S363-S367 | **FASE 0 COMPLETA** (6/6 step, media 9.4/10) |
| S368 | **FASE 1: F1.1+F1.2+F1.3** (9.6+9.5+9.5/10) |

---

*"Ultrapassar os proprios limites!" - Rafa & Cervella, S368*
