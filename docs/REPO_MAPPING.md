# REPO MAPPING - Contesto Intelligente per lo Sciame

> **W2 Tree-sitter - La FAMIGLIA ora capisce il codice!**
> Data: 19 Gennaio 2026 - Sessione 275

---

## Cos'è il Repo Mapping?

```
+================================================================+
|                                                                |
|   PRIMA: Worker riceveva solo il task                         |
|          "Fai una funzione di login"                           |
|          (Non sapeva nulla del progetto!)                      |
|                                                                |
|   DOPO:  Worker riceve task + MAPPA del progetto               |
|          "Fai una funzione di login"                           |
|          + lista funzioni esistenti                            |
|          + classi importanti                                   |
|          + struttura del codice                                |
|                                                                |
+================================================================+
```

Il **Repo Mapping** usa **tree-sitter** (parser AST) e **PageRank** per:
1. Analizzare TUTTO il codice del progetto
2. Estrarre simboli (funzioni, classi, types)
3. Calcolare quali sono i più IMPORTANTI
4. Fornire un riassunto intelligente ai worker

---

## Come Usarlo

### Per la Regina (spawn-workers)

```bash
# Worker CON contesto intelligente (1500 tokens default)
spawn-workers --backend --with-context

# Worker con contesto più ampio (più dettagli)
spawn-workers --backend --context-budget 2000

# Tutti i worker comuni con contesto
spawn-workers --all --with-context

# Worker senza contesto (comportamento vecchio)
spawn-workers --backend
```

### Flag Disponibili

| Flag | Descrizione |
|------|-------------|
| `--with-context` | Abilita contesto intelligente |
| `--no-context` | Disabilita (default) |
| `--context-budget N` | Token budget (default 1500) |

---

## Cosa Riceve il Worker?

Quando usi `--with-context`, il worker riceve:

```markdown
CONTESTO CODEBASE (auto-generato da repo_mapper):

# REPOSITORY MAP

## scripts/utils/auth.py

def login(username: str, password: str) -> bool
def logout(user_id: int) -> None
class AuthService
def validate_token(token: str) -> dict

## scripts/utils/database.py

def get_connection() -> Connection
class DatabasePool
def execute_query(query: str) -> list

---
Usa questo contesto per capire la struttura del progetto.
I simboli sono ordinati per importanza (PageRank).

---

[PROMPT WORKER NORMALE]
Sei CERVELLA-BACKEND...
```

---

## Budget Token Consigliati

| Tipo Progetto | Budget | Uso |
|---------------|--------|-----|
| Piccolo (< 50 file) | 500-1000 | Visione essenziale |
| Medio (50-200 file) | 1500 | Default bilanciato |
| Grande (> 200 file) | 2000-3000 | Più dettagli |

**NOTA:** Budget più alto = più simboli inclusi = più contesto per il worker

---

## Linguaggi Supportati

| Linguaggio | Estensioni | Status |
|------------|------------|--------|
| Python | .py | Completo |
| TypeScript | .ts, .tsx | Completo |
| JavaScript | .js | Completo |
| JSX | .jsx | Parziale (known issue) |

---

## File del Sistema

| File | Scopo |
|------|-------|
| `scripts/utils/treesitter_parser.py` | Parser AST multi-linguaggio |
| `scripts/utils/symbol_extractor.py` | Estrae funzioni/classi/types |
| `scripts/utils/dependency_graph.py` | PageRank per importanza |
| `scripts/utils/repo_mapper.py` | Orchestratore principale |
| `scripts/utils/generate_worker_context.py` | Wrapper per spawn-workers |

---

## Directory Escluse Automaticamente

Il sistema esclude automaticamente:
- `node_modules/`
- `__pycache__/`
- `.git/`
- `dist/`, `build/`
- `.venv/`, `venv/`
- `.pytest_cache/`, `.mypy_cache/`

---

## Debug

Se qualcosa non funziona, controlla:

```bash
# Log errori generazione contesto
cat .swarm/logs/context_generation.log

# Test manuale generazione
python3 scripts/utils/generate_worker_context.py --budget 500 --verbose
```

---

## Per Sviluppatori

### Usare direttamente RepoMapper

```python
from scripts.utils.repo_mapper import RepoMapper

# Genera mappa
mapper = RepoMapper(repo_path=".")
map_text = mapper.build_map(token_budget=2000)
print(map_text)

# Con filtro
map_text = mapper.build_map(
    token_budget=1500,
    filter_pattern="**/*.py"  # Solo Python
)
```

### CLI diretta

```bash
# Genera mappa del progetto corrente
python3 scripts/utils/repo_mapper.py --repo-path . --budget 2000

# Salva su file
python3 scripts/utils/repo_mapper.py --repo-path . --output map.md

# Solo Python con statistiche
python3 scripts/utils/repo_mapper.py --filter "**/*.py" --stats
```

---

## Versioni

| Versione | Data | Novità |
|----------|------|--------|
| spawn-workers v3.7.0 | 2026-01-19 | AUTO-CONTEXT integrato |
| repo_mapper v1.0.0 | 2026-01-19 | Prima release |

---

*"Lo sciame ora CAPISCE il codice prima di lavorarci!"*

*Cervella & Rafa - W2 Tree-sitter*
