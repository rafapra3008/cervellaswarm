# ANALISI ARCHITETTURALE CERVELLASWARM - 10 Febbraio 2026
## Sessione S340 - Cervella Ingegnera

---

## 1. MAPPA ARCHITETTURALE

```
                    +-----------+
                    | common/   |  <-- HUB CENTRALE (usato da TUTTI)
                    |  paths.py |      47% coverage
                    |  db.py    |      92% coverage
                    |  colors.py|      94% coverage
                    |  config.py|      100% coverage
                    +-----------+
                      /  |  \  \
                     /   |   \  \__________________
                    v    v    v                     v
           +--------+ +--------+ +---------+  +--------+
           | memory/| | swarm/ | | utils/  |  | tools/ |
           | 31 file| | 10 file| | 17 file |  | 2 file |
           +--------+ +--------+ +---------+  +--------+
                            |         |
                            v         v
                    +--------------------+
                    | utils/ PIPELINE    |
                    | treesitter_parser  |
                    |   -> extractors    |
                    |   -> dep_graph     |
                    |   -> repo_mapper   |
                    |   -> semantic_srch |
                    |   -> impact_anlzr  |
                    +--------------------+
```

### Conteggio Moduli (solo .py)
| Package | File | Righe Totali | Avg Righe/File |
|---------|------|-------------|----------------|
| scripts/common/ | 5 | 607 | 121 |
| scripts/memory/ | 31 | ~5500 | 177 |
| scripts/swarm/ | 10 | ~3100 | 310 |
| scripts/utils/ | 17 | ~4500 | 265 |
| scripts/tools/ | 2 | 228 | 114 |
| scripts/compaction/ | 3 | 221 | 74 |
| **TOTALE** | **68** | **~14.150** | - |

### Tests
| Package Test | File | Tests |
|-------------|------|-------|
| tests/common/ | 1 | ~20 |
| tests/compaction/ | 1 | ~15 |
| tests/swarm/ | 8 | ~160 |
| tests/memory/ | 10 | ~200 |
| tests/utils/ | 7 | ~100 |
| tests/tools/ | 1 | ~20 |
| **TOTALE** | **28+** | **525** |

---

## 2. MODULI HUB (Dipendenze Critiche)

### HUB 1: `common/paths.py` (235 righe, 47% cov) - CRITICO
- Importato da: memory/log_event, load_context, query_events, suggestions,
  pattern_detector, init_db, migrate, retro/cli, tools/add_version_headers,
  learning/trigger_detector, learning/wizard
- **12+ dipendenti diretti**
- Gap: 42 righe non testate (funzioni di path discovery)

### HUB 2: `common/db.py` (93 righe, 92% cov)
- Importato da: memory/suggestions, pattern_detector, retro/cli,
  analytics/commands/* (7 file)
- **10+ dipendenti diretti**
- Gap minimo: solo 2 righe

### HUB 3: `common/colors.py` (149 righe, 94% cov)
- Importato da: swarm/dashboard/render, memory/analytics/commands/* (7 file),
  memory/suggestions
- **9+ dipendenti diretti**

### HUB 4: `utils/treesitter_parser.py` (364 righe, 16% cov) - CRITICO
- Base dell'intera pipeline AST
- Usato da: symbol_extractor -> python/typescript_extractor ->
  dependency_graph -> repo_mapper -> generate_worker_context
- **Pipeline critica: 6 moduli dipendono a cascata**

---

## 3. TOP 5 MODULI CRITICI NON TESTATI

| # | Modulo | Righe | Cov | Perche e Critico |
|---|--------|-------|-----|------------------|
| 1 | `treesitter_parser.py` | 364 | 16% | BASE dell'intera pipeline AST. Se fallisce, falliscono 6 moduli a cascata. |
| 2 | `python_extractor.py` | 399 | 7% | Estrae simboli Python - core del repo mapping per TUTTI i nostri file .py |
| 3 | `typescript_extractor.py` | 422 | 8% | Estrae simboli TS - necessario per analisi Miracollo frontend |
| 4 | `repo_mapper.py` | 448 | 0% | Orchestratore pipeline (parser+extractor+graph). Usato da generate_worker_context |
| 5 | `symbol_extractor.py` | 392 | 25% | Facade che coordina python/typescript extractors. Hub intermedio |

**Nota:** I _cli.py (0%) e generate_worker_context (0%) sono meno critici perche sono thin wrapper. measure_context_tokens (0%) e uno utility di debug. convert_agents_to_agent_hq.py (0%) sembra legacy.

---

## 4. RISCHI ARCHITETTURALI

### R1: IMPORT FRAGILI (Severita: ALTO)
Molti moduli usano try/except per import:
```python
try:
    from dependency_graph import DependencyGraph
except ImportError:
    from scripts.utils.dependency_graph import DependencyGraph
```
Questo pattern e presente in: repo_mapper, generate_worker_context, dependency_graph,
python_extractor, typescript_extractor, symbol_extractor, load_context.
**Rischio:** Nasconde errori reali di import. Se un modulo e rinominato, il fallback
silenzioso rende il debug difficile.

### R2: PIPELINE AST NON TESTATA (Severita: CRITICO)
La pipeline treesitter -> extractors -> dep_graph -> repo_mapper ha 0-16% coverage.
E il cuore del sistema di context generation per i worker.
**Rischio:** Regressioni invisibili. Un cambio in treesitter_parser rompe 6 moduli.

### R3: common/paths.py al 47% (Severita: MEDIO)
E l'hub piu usato (12+ dipendenti) ma ha quasi meta delle funzioni non testate.
**Rischio:** Path errati su macchine diverse o dopo refactoring.

### R4: memory/retro/ a coverage variabile (Severita: BASSO)
retro/cli.py 63%, retro/output.py 74%. Non e bloccante ma il modulo retro
e usato per generare retrospettive che guidano decisioni.

### R5: Dual import pattern (common vs scripts.common)
I moduli in memory/ usano `from common.paths import ...` (path relativo via sys.path)
I moduli in swarm/ usano `from scripts.swarm.task_classifier import ...` (absolute)
**Rischio:** Inconsistenza. Se sys.path cambia, i memory/ import si rompono.

---

## 5. PROPOSTA FASE 5: "FONDAMENTA SOLIDE"

### Principio Guida
> "Il codice pulito e un regalo per il te stesso di domani."

Priorita basata su: IMPATTO BUSINESS x RISCHIO x EFFORT

### Step 5.1: Test Pipeline AST Core (Effort: M = 2-3 sessioni)
**Cosa:** Test per treesitter_parser + python_extractor + typescript_extractor
**Perche:** E la fondazione di tutto il context system. Senza test, ogni modifica e rischiosa.
**Target:** Da 7-16% a 80%+ coverage su questi 3 file
**Come:**
- Sessione A: treesitter_parser (16% -> 80%): test parse_file, language detection, error handling
- Sessione B: python_extractor (7% -> 80%): test extract functions/classes/references
- Sessione C: typescript_extractor (8% -> 80%): test extract interfaces/types/functions

### Step 5.2: Test repo_mapper + symbol_extractor (Effort: M = 2 sessioni)
**Cosa:** Test per repo_mapper (0%) e symbol_extractor (25%)
**Perche:** Questi orchestrano la pipeline. Se funzionano, il worker context funziona.
**Target:** 0% -> 70%+ per repo_mapper, 25% -> 80%+ per symbol_extractor
**Come:**
- Sessione A: symbol_extractor facade tests (composition pattern, extract_symbols, cache)
- Sessione B: repo_mapper (build_map, token budget, file filtering, output format)

### Step 5.3: Solidificare common/paths.py (Effort: S = 1 sessione)
**Cosa:** Portare paths.py da 47% a 90%+
**Perche:** E l'hub con piu dipendenti. 42 righe non testate = 12+ moduli a rischio.
**Come:** Test path discovery, env var override, fallback logic

### Step 5.4: Standardizzare Import Pattern (Effort: S = 1 sessione)
**Cosa:** Unificare gli import a un pattern unico (preferibilmente `from scripts.X import Y`)
**Perche:** Elimina i try/except fragili. Rende il codebase consistente.
**Come:** Refactoring guidato - un modulo alla volta, test dopo ogni cambio.

### Step 5.5: Pulizia File Legacy (Effort: S = 1 sessione)
**Cosa:** Valutare/rimuovere convert_agents_to_agent_hq.py (0%, 76 righe),
  measure_context_tokens.py (0%, debug utility), CLI thin wrappers non usati.
**Perche:** Codice morto = confusione. Meno file = meno manutenzione.
**Come:** Verificare usage con grep, archiviare o rimuovere.

---

## 6. RIEPILOGO EFFORT

| Step | Descrizione | Effort | Impatto Coverage |
|------|-------------|--------|-----------------|
| 5.1 | Pipeline AST Core | M (2-3 sess) | +8% (60% -> 68%) |
| 5.2 | repo_mapper + symbol_extractor | M (2 sess) | +4% (68% -> 72%) |
| 5.3 | common/paths.py | S (1 sess) | +1% (72% -> 73%) |
| 5.4 | Standardizzare import | S (1 sess) | +0% (qualita) |
| 5.5 | Pulizia legacy | S (1 sess) | +1% (meno codice) |
| **TOTALE** | | **7-8 sessioni** | **60% -> ~74%** |

### Coverage Proiezione Post-FASE 5
```
PRIMA (S340):  60% coverage, 525 test
DOPO (FASE 5): ~74% coverage, ~650+ test (stima)

Gap residuo: retro/output, retro/cli, semantic_search,
  analytics/auto_detect, CLI wrappers
```

---

## 7. RACCOMANDAZIONE STRATEGICA

**La mia raccomandazione come Ingegnera:**

Iniziare da Step 5.1 (Pipeline AST). Motivo:
1. E la fondazione su cui poggia TUTTO il context system
2. Ha il rischio piu alto (6 moduli in cascata senza test)
3. Una volta solida la base, i test di repo_mapper (5.2) saranno molto piu semplici
4. Sblocca la possibilita di fare refactoring sicuri su tutto il pipeline

**NON consiglio** di inseguire il 70% coverage come numero fine a se stesso.
Consiglio di testare cio che ha IMPATTO REALE. I file della pipeline AST
sono usati attivamente dai worker. I CLI wrapper a 0% possono aspettare.

> "Fatto BENE > Fatto VELOCE"

---

*Report generato da Cervella Ingegnera - 10 Febbraio 2026*
*"Il debito tecnico si paga con gli interessi."*
