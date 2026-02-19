# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-02-19 - Sessione 374
> **STATUS:** CACCIA BUG IN CORSO. Package 1/7 completato. FASE 3 F3.1 DONE.

---

## SESSIONE 374 - CACCIA BUG: code-intelligence (Deep Dive #1)

### Cosa abbiamo fatto
Rafa ha deciso: prima di avanzare con F3.2+, consolidare tutti i 7 packages.
Strategia: uno alla volta, deep dive, Ingegnera analizza + Guardiana verifica.

### code-intelligence: 21 issue trovate, 8 fixate

L'Ingegnera ha analizzato tutti i 14 moduli source (~4.145 LOC). Trovate 5 HIGH, 10 MEDIUM, 8 LOW.

| ID | Sev | Bug | Fix |
|----|-----|-----|-----|
| **H3** | HIGH | `get_top_symbols()` KeyError per nodi fantasma NetworkX | Filtro `if k in self.nodes` |
| **H4** | HIGH | Symbol ID collisione `__init__` in classi diverse | Formato `file:line:name` (era `file:name`) |
| **M6** | MED | `*.egg-info` exclude non funziona in repo_mapper | `endswith(".egg-info")` |
| **M8** | MED | `except Exception` silenziava bug reali in `_build_index()` | Ristretto a 3 eccezioni specifiche |
| **M9** | MED | Docstring falso "Thread-safe" in SymbolCache | Rimosso, aggiunto warning |
| **M3** | MED | `clear_cache()` docstring misleading | Chiarito scope |
| **F1** | P2 | `split(":", 1)` fallback rotto per nuovo formato ID | `rsplit` corretto |
| **F2-3** | P3 | Docstring stale dopo cambio formato | Aggiornate |

**Risultato:** 398 test (era 395, +3 regressione). Guardiana: 9.5/10 + 9.3/10 -> fix P2.

### Issue P2 rimasti (non fixabili senza refactor maggiore)
- **H1**: Stale cache senza mtime (workaround `invalidate_file()` esiste)
- **H2**: Docstring extraction index `[1]` hardcoded (funziona, fragile)
- **H5**: `add_reference()` risolve primo match arbitrario (design limitation)
- **M4**: O(n) edge list (richiede migrazione a Set + adjacency dict)

### Decisioni S374

| Decisione | Perche |
|-----------|--------|
| Deep dive uno alla volta | Rafa: "con calma, chiaro e precisi" |
| Ordine per rischio | code-intelligence (AST) > task-orchestration > spawn-workers > rest |
| H4 refactor subito | Docstring GIA documentava `file:line:name`, implementazione era `file:name` |
| H1/H5 rimandati | Richiedono refactor architetturale, non bug fix chirurgico |

### Lezioni apprese S374
- **NetworkX phantom nodes**: `add_edges_from()` aggiunge nodi impliciti. PageRank li include. SEMPRE filtrare.
- **Symbol ID unicita**: `file:name` NON basta. `__init__` in 2 classi = collisione. Line number obbligatorio.
- **`*.egg-info` in set()**: match esatto non funziona per nomi dinamici. Serve `endswith()`.
- **`except Exception` in loop**: silenzia bug reali. Ristringere SEMPRE alle eccezioni attese.

---

## PROSSIMI STEP

### CACCIA BUG - PACKAGES RIMANENTI (6/7)
Ordine scelto (dal piu rischioso):
1. ~~`code-intelligence`~~ -- FATTO (398 test, 8 bug fix, 9.5/10)
2. **`task-orchestration`** -- PROSSIMO (race condition, atomic ops, 273 test)
3. `spawn-workers` -- (subprocess, signal handling, 171 test)
4. `session-memory` -- (il piu nuovo, 177 test)
5. `agent-hooks` -- (config loading, 227 test)
6. `agent-templates` -- (template rendering, 188 test)
7. CLI + MCP -- (TypeScript)

### DOPO il consolidamento:
- **F3.2:** SQLite Event Database
- **F3.3:** Integration Tools
- **F3.4:** Documentation package
- **F3.5:** Auto-Handoff improvements

---

## ARCHIVIO

| Sessione | Cosa |
|----------|------|
| S337-S348 | Coverage push 41% -> 95% (968 test) |
| S349-S361 | MAPPA MIGLIORAMENTI + SNCP 4.0 + POLISH + ANTI-DOWNGRADE |
| S362-S367 | **FASE 0 COMPLETA** (6/6 step, media 9.4/10) |
| S368-S369 | **FASE 1 COMPLETA** (F1.1-F1.4, PyPI LIVE!) |
| S370-S372 | **FASE 2 COMPLETA** (4/4 packages, media 9.5/10) |
| S373 | **FASE 3: F3.1 Session Memory** (9.6/10) |
| S374 | **CACCIA BUG #1: code-intelligence** (8 fix, 398 test, 9.5/10) |

---

*"Ultrapassar os proprios limites!" - Rafa & Cervella, S374*
