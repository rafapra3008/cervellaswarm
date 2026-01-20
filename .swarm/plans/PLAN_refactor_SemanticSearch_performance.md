# PLAN: Refactor SemanticSearch Class to Improve Performance

> **Architect:** CERVELLA-ARCHITECT
> **Data:** 2026-01-20
> **Task:** Refactor SemanticSearch class to improve performance

---

## Phase 1: Understanding

### 1.1 Cosa Vuole l'Utente

Migliorare le performance della classe `SemanticSearch` che attualmente:
- Scansiona tutti i file del repo all'inizializzazione
- Costruisce un indice di simboli in memoria
- Calcola PageRank per importanza simboli
- Fornisce API per navigazione semantica del codice

### 1.2 Codebase Analysis

#### File Critici Analizzati

| File | Righe | Ruolo |
|------|-------|-------|
| `scripts/utils/semantic_search.py` | 572 | Classe principale SemanticSearch |
| `scripts/utils/symbol_extractor.py` | 1163 | Estrazione simboli da AST |
| `scripts/utils/dependency_graph.py` | 465 | Grafo dipendenze + PageRank |
| `scripts/utils/treesitter_parser.py` | 365 | Parser tree-sitter |

#### Architettura Attuale

```
SemanticSearch.__init__(repo_root)
    |
    +-> TreesitterParser()           # Inizializzazione parser
    +-> SymbolExtractor(parser)      # Inizializzazione extractor
    +-> DependencyGraph()            # Inizializzazione grafo
    |
    +-> _build_index()               # <-- BOTTLENECK PRINCIPALE
            |
            +-> repo_root.rglob("*{ext}")     # Scan tutti i file
            +-> should_exclude(path)          # Filtro esclusioni
            |
            +-> FOR file IN source_files:
            |       extractor.extract_symbols(file)   # Parse ogni file
            |       FOR symbol IN symbols:
            |           symbol_index[name].append(symbol)
            |           graph.add_symbol(symbol)
            |           graph.add_reference(...)
            |
            +-> graph.compute_importance()    # PageRank su tutto il grafo
```

### 1.3 Bottleneck Identificati

#### B1: Scan Completo del Repository (righe 157-163)
```python
for ext in extensions:
    for file_path in self.repo_root.rglob(f"*{ext}"):
        if not should_exclude(file_path.relative_to(self.repo_root)):
            source_files.append(file_path)
```
**Problema:** `rglob` viene chiamato 5 volte (una per estensione), iterando l'intero albero ogni volta.

#### B2: Parsing Sincrono File-by-File (righe 167-187)
```python
for file_path in source_files:
    symbols = self.extractor.extract_symbols(str(file_path))
```
**Problema:** Ogni file viene parsato sequenzialmente. Su repo grandi (100+ file) questo e' lento.

#### B3: PageRank su Tutto il Grafo (riga 191)
```python
self.graph.compute_importance()
```
**Problema:** PageRank viene calcolato subito dopo l'indicizzazione, anche se l'utente potrebbe non usarlo.

#### B4: Nessun Indice Persistente
**Problema:** L'indice viene ricostruito da zero ad ogni istanza. Nessun salvataggio su disco.

#### B5: should_exclude() Chiamato per Ogni File (righe 150-155)
```python
def should_exclude(path: Path) -> bool:
    for part in path.parts:
        if part in exclude_dirs or part.endswith(".egg-info"):
            return True
    return False
```
**Problema:** Itera su tutti i path parts per ogni file. Inefficiente per path profondi.

### 1.4 Metriche Attuali (dai test)

| Operazione | Tempo Target | Tempo Attuale |
|------------|--------------|---------------|
| find_symbol | < 100ms | < 50ms (cached) |
| find_callers | < 500ms | < 1000ms |
| estimate_impact | < 2s | < 2000ms |
| Inizializzazione | N/A | 5-10s (100-1000 file) |

---

## Phase 2: Design

### 2.1 Approach: Ottimizzazione Incrementale

**Strategia:** Ottimizzare senza rompere l'API esistente. Nessun breaking change.

### 2.2 Ottimizzazioni Proposte

#### OPT-1: Single-Pass Glob (Priorita ALTA)

**Attuale:**
```python
for ext in extensions:
    for file_path in self.repo_root.rglob(f"*{ext}"):
```

**Proposto:**
```python
for file_path in self.repo_root.rglob("*"):
    if file_path.suffix in extensions and not should_exclude(...):
        source_files.append(file_path)
```

**Beneficio:** 1 iterazione invece di 5. ~80% reduction in scan time.

#### OPT-2: Early Directory Pruning (Priorita ALTA)

**Attuale:** `rglob` entra comunque in node_modules, .git, etc.

**Proposto:** Usare `os.walk()` con modifica in-place di `dirs`:
```python
for root, dirs, files in os.walk(self.repo_root):
    # Prune excluded directories IN-PLACE (os.walk rispetta questo)
    dirs[:] = [d for d in dirs if d not in exclude_dirs]
    for f in files:
        if Path(f).suffix in extensions:
            yield Path(root) / f
```

**Beneficio:** Non entra mai in directory escluse. Massivo improvement su repo con node_modules.

#### OPT-3: Lazy PageRank (Priorita MEDIA)

**Attuale:** PageRank calcolato sempre in __init__

**Proposto:** Calcolare solo quando serve:
```python
def _ensure_importance_computed(self):
    if not self._importance_computed:
        self.graph.compute_importance()
        self._importance_computed = True

def find_symbol(self, name):
    # ...
    if len(candidates) > 1:
        self._ensure_importance_computed()  # Solo se serve disambiguare
```

**Beneficio:** Utenti che cercano simboli unici non pagano il costo di PageRank.

#### OPT-4: Parallel File Processing (Priorita MEDIA)

**Attuale:** Parsing sequenziale

**Proposto:** Usare `concurrent.futures.ThreadPoolExecutor`:
```python
with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
    futures = {executor.submit(self._process_file, f): f for f in source_files}
    for future in as_completed(futures):
        symbols = future.result()
        # merge into index
```

**Beneficio:** ~2-4x speedup su multi-core.

**Rischio:** Tree-sitter e' thread-safe? Da verificare. Se no, usare ProcessPoolExecutor.

#### OPT-5: Persistent Index Cache (Priorita BASSA)

**Proposto:** Salvare indice su disco in formato pickle/JSON:
```python
CACHE_FILE = ".semantic_cache.pkl"

def _load_cache(self):
    cache_path = self.repo_root / CACHE_FILE
    if cache_path.exists():
        return pickle.load(...)
    return None

def _save_cache(self):
    pickle.dump({
        'mtime_map': {...},
        'symbol_index': self.symbol_index,
        'graph': self.graph
    }, ...)
```

**Beneficio:** Istanziazioni successive quasi istantanee (solo file modificati).

**Rischio:** Invalidazione cache complessa. Da implementare con cura.

### 2.3 Critical Files da Modificare

| File | Modifiche |
|------|-----------|
| `scripts/utils/semantic_search.py` | OPT-1, OPT-2, OPT-3, (OPT-4, OPT-5) |
| `tests/utils/test_semantic_search.py` | Nuovi test performance |

### 2.4 Rischi

| Rischio | Mitigazione |
|---------|-------------|
| Breaking API | Nessuna modifica alle firme pubbliche |
| Race conditions (OPT-4) | Test thread-safety tree-sitter prima |
| Cache stale (OPT-5) | Usare mtime-based invalidation |
| Regression performance | Benchmark prima/dopo |

---

## Phase 3: Review

### 3.1 Assumptions Validate

- [x] SemanticSearch e' il collo di bottiglia (confermato da analisi codice)
- [x] Il caching mtime in SymbolExtractor funziona gia' (v2.2.0)
- [x] PageRank e' opzionale per molte operazioni
- [x] tree-sitter-language-pack usato per parsing (thread-safe da verificare)

### 3.2 Questions Aperte

1. **Thread-safety tree-sitter:** Necessario verificare se tree-sitter Python bindings sono thread-safe prima di OPT-4

2. **Target performance:** Qual e' il target per l'inizializzazione?
   - Attuale: 5-10s per 100-1000 file
   - Ragionevole: < 2s per 100 file, < 5s per 1000 file

3. **Scope OPT-5:** Persistent cache aggiunge complessita'. E' necessaria ora o e' prematura?

### 3.3 Raccomandazione

Implementare in ordine di priorita:
1. **OPT-1 + OPT-2** (Quick wins, no risks)
2. **OPT-3** (Medium effort, good benefit)
3. **OPT-4** (Only after thread-safety verified)
4. **OPT-5** (Future iteration, high complexity)

---

## Phase 4: Final Plan

### 4.1 Execution Order

```
STEP 1: OPT-2 - Early Directory Pruning
   Worker: cervella-backend
   File: scripts/utils/semantic_search.py
   Righe: 131-163
   Descrizione: Sostituire rglob con os.walk + pruning

STEP 2: OPT-1 - Single-Pass Glob
   Worker: cervella-backend
   File: scripts/utils/semantic_search.py
   Righe: 159-163
   Descrizione: Unificare loop estensioni (parte di STEP 1)

STEP 3: OPT-3 - Lazy PageRank
   Worker: cervella-backend
   File: scripts/utils/semantic_search.py
   Righe: 189-191, 239-240
   Descrizione: Aggiungere _ensure_importance_computed()

STEP 4: Test Performance
   Worker: cervella-tester
   File: tests/utils/test_semantic_search.py
   Descrizione: Aggiungere benchmark prima/dopo

STEP 5: (OPTIONAL) OPT-4 - Parallel Processing
   Worker: cervella-researcher (prima) + cervella-backend
   Descrizione: Verificare thread-safety, poi implementare
```

### 4.2 Success Criteria

| Criterio | Metrica |
|----------|---------|
| Nessun breaking change | API pubblica invariata |
| Init speedup | < 3s per 100 file (da 5-10s) |
| find_symbol speed | Invariata o migliorata |
| Test pass | 100% test esistenti passano |

### 4.3 Output Attesi

1. `semantic_search.py` v1.2.0 con ottimizzazioni
2. Test aggiornati con benchmark
3. (Opzionale) Research output su thread-safety tree-sitter

---

## Report Finale

**PIANO COMPLETO**

Ho analizzato la classe `SemanticSearch` e identificato 5 bottleneck principali:

1. **Scan multiplo** - rglob chiamato 5 volte per estensione
2. **No directory pruning** - entra in node_modules, .git, etc.
3. **PageRank eager** - calcolato sempre, anche se non serve
4. **Parsing sequenziale** - file processati uno alla volta
5. **No persistent cache** - indice ricostruito ad ogni istanza

**Raccomandazione:** Implementare OPT-1/2/3 subito (quick wins), OPT-4 dopo verifica thread-safety, OPT-5 in futuro.

**Stima improvement:** 2-4x speedup su inizializzazione senza breaking changes.

---

*CERVELLA-ARCHITECT - Piano prima, codice dopo.*
