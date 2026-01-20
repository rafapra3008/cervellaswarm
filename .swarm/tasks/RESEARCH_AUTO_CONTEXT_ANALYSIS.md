# Analisi --with-context: Auto-Context per Worker

**Ricerca completata:** 2026-01-20
**Researcher:** cervella-researcher
**Versione analizzata:** spawn-workers v3.7.0, repo_mapper v1.0.0

---

## TL;DR (Executive Summary)

**Raccomandazione:** OFF di default, ON per worker specifici.

**Perché:** Il context ha ALTO valore per worker che modificano codice, ma costa tempo/token inutili per worker non-code (docs, researcher, marketing). Meglio ON selettivo che blanket default.

---

## Come Funziona

### Pipeline Context Generation

```
spawn-workers --backend --with-context
       │
       ▼
1. generate_worker_context.py
       │
       ▼
2. RepoMapper(repo_path)
   ├─ _discover_source_files()      # Glob **/*.py, **/*.ts, etc
   │  └─ Esclude: node_modules, __pycache__, .git, dist, venv
   ├─ TreesitterParser
   │  └─ Parse AST per ogni file (tree-sitter multi-lang)
   ├─ SymbolExtractor
   │  └─ Estrae: functions, classes, interfaces, types
   ├─ DependencyGraph
   │  ├─ Aggiungi nodi (simboli)
   │  ├─ Aggiungi edges (references)
   │  └─ PageRank importance score
   └─ _fit_to_budget()
      └─ Seleziona top N simboli (ordinati per importance)
       │
       ▼
3. Genera markdown map
       │
       ▼
4. Inject in worker prompt (prepend)
```

### Output Esempio

```markdown
CONTESTO CODEBASE (auto-generato da repo_mapper):

# REPOSITORY MAP

## scripts/utils/auth.py

def login(username: str, password: str) -> bool
class AuthService
def validate_token(token: str) -> dict

## scripts/utils/database.py

def get_connection() -> Connection
class DatabasePool

---
Usa questo contesto per capire la struttura del progetto.
I simboli sono ordinati per importanza (PageRank).
```

### Componenti

| File | LOC | Scopo |
|------|-----|-------|
| `generate_worker_context.py` | 147 | Wrapper per spawn-workers |
| `repo_mapper.py` | 571 | Orchestratore principale |
| `treesitter_parser.py` | 365 | Parser AST multi-linguaggio |
| `symbol_extractor.py` | 486 | Estrae funzioni/classi/types |
| `dependency_graph.py` | 451 | PageRank importanza simboli |

**Totale:** ~2020 LOC (ben strutturato, modular)

---

## Pro

### 1. **Comprensione Codebase**
- Worker vede funzioni esistenti → evita duplicati
- Capisce naming convention → mantiene coerenza
- Sa quali classi sono centrali → usa pattern corretti

### 2. **Migliore Qualità Output**
- Esempio: Backend crea `create_user()` → vede già `AuthService` → usa quello invece di duplicare
- Esempio: Frontend aggiunge componente → vede pattern `UserCard`, `Header` → segue stessa struttura

### 3. **Riduce Errori**
- Worker non inventa API che non esistono
- Non chiama funzioni con signature sbagliata
- Conosce dipendenze critiche (PageRank)

### 4. **Autonomia**
- Meno domande alla Regina "Quale funzione uso?"
- Worker più indipendente = meno contesto consumato Regina

### 5. **Già Implementato**
- Codice maturo (v1.0.0, 142 test passati W2)
- Flag opzionale → zero breaking change
- Log errori in `.swarm/logs/context_generation.log`

---

## Contro

### 1. **Latenza Spawn**
- Ogni spawn deve:
  - Glob file sorgenti (~100-300 file CervellaSwarm)
  - Parse AST (tree-sitter ogni file)
  - Build grafo dipendenze
  - Compute PageRank
  - Format markdown

**Stima tempo:** 3-8 secondi (dipende da project size)

**Impatto:** Ritardo PRIMA che worker inizi. Se spawni 3 worker in parallelo, tutti aspettano.

### 2. **Token Budget Consumato**
- Default 1500 tokens PRIMA del task description
- Budget Claude: 200K tokens
- 1500 = 0.75% del budget
- Se worker fa 10 task brevi → 15K tokens (7.5%) spesi in context statico

**Trade-off:** Più contesto = meno spazio per reasoning

### 3. **Context Stale**
- Contesto generato PRIMA dello spawn
- Se codebase cambia DURANTE il lavoro → worker ha map obsoleta
- Worker paralleli vedono snapshots diversi (race condition teorica)

### 4. **Overhead Inutile per Non-Code Worker**
- **Docs:** Scrive README → non serve mappa funzioni
- **Researcher:** Fa ricerca web → codebase irrilevante
- **Marketing:** Decide UX flow → non importa PageRank simboli
- **Scienziata:** Competitor analysis → zero uso del context

### 5. **Fallisce Silenziosamente**
- Se `repo_mapper.py` fallisce → worker procede SENZA context
- Log va in `.swarm/logs/context_generation.log` (non visibile)
- Warning nel spawn output, ma può passare inosservato

### 6. **JSX Non Supportato (Known Issue)**
- File `.jsx` non parsano (manca tree-sitter-jsx library)
- Frontend worker in progetti React+JSX → context parziale
- Già documentato in `context_generation.log`:
  ```
  Failed to parse UserCard.jsx, no symbols extracted
  ```

---

## Per Tipo Worker

| Worker | Beneficio Context | Overhead Giustificato? | Raccomandazione |
|--------|-------------------|------------------------|-----------------|
| **backend** | ⭐⭐⭐⭐⭐ | ✅ | **ON** - Modifica codice, serve mappa API/DB |
| **frontend** | ⭐⭐⭐⭐ | ✅ | **ON** - Serve pattern componenti esistenti |
| **tester** | ⭐⭐⭐ | ✅ | **ON** - Deve sapere cosa testare |
| **reviewer** | ⭐⭐⭐⭐ | ✅ | **ON** - Code review needs code context |
| **ingegnera** | ⭐⭐⭐⭐⭐ | ✅ | **ON** - Analizza tech debt, serve tutto |
| **data** | ⭐⭐⭐ | ⚠️ | **MAYBE** - Se schema DB è in codice, utile |
| **devops** | ⭐⭐ | ⚠️ | **MAYBE** - Se config è code (IaC), utile |
| **security** | ⭐⭐⭐ | ✅ | **ON** - Audit code needs symbols |
| **docs** | ⭐ | ❌ | **OFF** - Scrive docs, non modifica code |
| **researcher** | ⭐ | ❌ | **OFF** - Ricerca web, non code |
| **scienziata** | ⭐ | ❌ | **OFF** - Competitor analysis, non code |
| **marketing** | ⭐ | ❌ | **OFF** - UX strategy, non implementation |
| **architect** | ⭐⭐⭐⭐⭐ | ✅ | **ON** - Pianifica, serve visione completa |
| **guardiana-qualita** | ⭐⭐⭐⭐ | ✅ | **ON** - Verifica standard, serve context |
| **guardiana-ops** | ⭐⭐ | ⚠️ | **MAYBE** - Depends on infra-as-code |
| **guardiana-ricerca** | ⭐ | ❌ | **OFF** - Verifica ricerche, non code |

### Legenda
- ⭐⭐⭐⭐⭐ = Critico, context fa differenza enorme
- ⭐⭐⭐⭐ = Molto utile, migliora qualità output
- ⭐⭐⭐ = Utile, ma non indispensabile
- ⭐⭐ = Basso beneficio
- ⭐ = Praticamente inutile

---

## Raccomandazione Finale

### ❌ NON abilitare di default per TUTTI i worker

**Perché:**
- 5/16 worker NON beneficiano (docs, researcher, scienziata, marketing, guardiana-ricerca)
- Overhead latency spawn per worker che non lo usano = spreco
- Default OFF = backward compatible, zero surprises

### ✅ Abilitare di default per CATEGORIE SPECIFICHE

**Proposta implementazione:**

```bash
# In spawn-workers.sh, riga 96:
# AUTO_CONTEXT=false  # OLD

# NEW: Auto-detect se serve context
AUTO_CONTEXT_WORKERS="backend frontend tester reviewer ingegnera security architect guardiana-qualita"
```

**Logica spawn:**

```bash
spawn_worker_headless() {
    local worker_name="$1"

    # Auto-enable context se worker è "code-aware"
    local context_enabled=$AUTO_CONTEXT
    if [[ " $AUTO_CONTEXT_WORKERS " =~ " $worker_name " ]]; then
        context_enabled=true
    fi

    if [ "$context_enabled" = true ]; then
        # Genera context...
    fi
}
```

**Risultato:**
- `spawn-workers --backend` → AUTO context ON
- `spawn-workers --researcher` → AUTO context OFF
- `spawn-workers --backend --no-context` → FORCE context OFF (override)
- `spawn-workers --researcher --with-context` → FORCE context ON (override)

### Alternative (più conservativa)

**Opzione B:** Lasciare OFF di default, ma SUGGERIRE nel help:

```bash
show_usage() {
    echo "Worker consigliati CON context:"
    echo "  spawn-workers --backend --with-context"
    echo "  spawn-workers --frontend --with-context"
    echo ""
    echo "Worker che NON necessitano context:"
    echo "  spawn-workers --researcher    # NO --with-context needed"
}
```

---

## Considerazioni Tecniche

### Budget Token Ottimale

| Project Size | File Count | Budget Consigliato |
|--------------|------------|--------------------|
| Piccolo | < 50 file | 500-1000 tokens |
| Medio | 50-200 file | 1500 tokens (default) |
| Grande | > 200 file | 2000-3000 tokens |

**CervellaSwarm:** ~100-150 file Python/shell → 1500 tokens è corretto.

### Performance

**Misurazione necessaria:** Il tempo di generazione NON è documentato.

**TODO (Guardiana Qualità):**
- Benchmark `generate_worker_context.py` su CervellaSwarm
- Misurare:
  - Tempo discovery files
  - Tempo parse AST
  - Tempo PageRank
  - Tempo total
- Target: < 3 secondi per spawn (acceptable), < 1 secondo (ottimo)

**Se > 5 secondi:** Considerare cache (`repo_map.cache`, invalidate on git commit).

### Fallback Graceful

**Attuale comportamento (BUONO):**
```python
# generate_worker_context.py line 81-84
except Exception as e:
    return f"[WARN] Failed to generate context: {e}"
```

Worker procede senza context se generazione fallisce. Nessun blocco spawn.

### Known Issues

1. **JSX non supportato** (documentato)
   - Tree-sitter-jsx library mancante
   - Workaround: Usa `.tsx` invece di `.jsx` (TypeScript parser funziona)

2. **Stale context** (teorico)
   - Se codebase cambia DURANTE lavoro worker, map obsoleta
   - Impatto basso: worker usa Read/Grep per verificare codice comunque

---

## Fonti

- `scripts/swarm/spawn-workers.sh` (v3.7.0, righe 88-97, 550-570, 789-806)
- `scripts/utils/generate_worker_context.py` (v1.0.0, 147 righe)
- `scripts/utils/repo_mapper.py` (v1.0.0, 571 righe)
- `docs/REPO_MAPPING.md` (Sessione 275, 19 Gen 2026)
- `CHANGELOG.md` (W2: Tree-sitter Integration)
- `.swarm/logs/context_generation.log` (Known JSX issue)

---

## Next Steps (Se si implementa raccomandazione)

1. **Modificare spawn-workers.sh:**
   - Definire `AUTO_CONTEXT_WORKERS` list
   - Auto-detect context enable per worker type
   - Mantenere `--with-context`/`--no-context` come override

2. **Benchmark performance:**
   - Misurare tempo generazione context su progetti diversi
   - Documentare in `docs/REPO_MAPPING.md`

3. **Aggiornare docs:**
   - `docs/REPO_MAPPING.md`: Spiegare auto-enable per worker
   - `spawn-workers.sh --help`: Lista worker con auto-context

4. **Test:**
   - Hardtest: spawn backend (context ON auto)
   - Hardtest: spawn researcher (context OFF auto)
   - Hardtest: spawn researcher --with-context (override ON)

---

**Decisione finale:** REGINA decide.

Io sono l'esperta ricerca, ho analizzato i dati. La scelta strategica spetta a Cervella Regina.

---

*Cervella Researcher - Analisi completata 2026-01-20*
