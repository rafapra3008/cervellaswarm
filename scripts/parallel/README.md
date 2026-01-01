# 🧠 Task Analyzer - CervellaSwarm

Analizzatore intelligente di task per decidere la strategia di esecuzione ottimale.

## 🎯 Cosa Fa

Analizza un task (lista di file) e decide:
- **Sequential**: 1 agente alla volta (file correlati/dipendenti)
- **Parallel**: 3-5 agenti in parallelo (sweet spot)
- **Worktrees**: Isolamento completo per 6+ file indipendenti

## 📊 Decision Matrix

| File | Domini | Dipendenze | Tempo | → Strategia |
|------|--------|------------|-------|-------------|
| 1-2 | any | any | <30min | SEQUENTIAL |
| 3-5 | diversi | basse | any | PARALLEL |
| 3-5 | stesso | alte | any | SEQUENTIAL |
| 6+ | diversi | basse | >60min | WORKTREES |
| 6+ | diversi | alte | any | SEQUENTIAL + Split |

## 🚀 Uso

### CLI Interattiva

```bash
# Analisi base
./scripts/parallel/task_analyzer.py file1.jsx file2.py file3.md

# Con tempo stimato
./scripts/parallel/task_analyzer.py file1.jsx file2.py --time 60

# Output JSON (per automazione)
./scripts/parallel/task_analyzer.py file1.jsx file2.py --json
```

### Output Esempio

```
╔══════════════════════════════════════════════════════════════════╗
║  🧠 TASK ANALYSIS RESULT                                        ║
╠══════════════════════════════════════════════════════════════════╣
║  🔀 Strategia: PARALLEL
║  📝 Motivo: Sweet spot: 3-5 file, domini diversi, basse dipendenze
║  ⚡ Speedup atteso: 1.36x
║
║  📂 DISTRIBUZIONE DOMINI:
║     • frontend: 1 file
║     • backend: 1 file
║     • docs: 1 file
║
║  🐝 AGENTI SUGGERITI:
║     • cervella-frontend
║     • cervella-backend
║     • cervella-docs
║
║  🔀 GRUPPI PARALLELI:
║     Gruppo 1: App.jsx
║     Gruppo 2: main.py
║     Gruppo 3: README.md
╚══════════════════════════════════════════════════════════════════╝
```

## 🎨 Domini Riconosciuti

| Dominio | Pattern | Agente |
|---------|---------|--------|
| Frontend | `.jsx`, `.tsx`, `.css`, `components/` | cervella-frontend |
| Backend | `.py`, `api/`, `services/` | cervella-backend |
| Database | `.sql`, `migrations/`, `models/` | cervella-data |
| Test | `test_*.py`, `*.test.js`, `__tests__/` | cervella-tester |
| Docs | `.md`, `docs/`, `README` | cervella-docs |
| Config | `.json`, `.yaml`, `.env`, `config/` | cervella-devops |

## ⚡ Speedup Atteso

| Strategia | Speedup Base | Con N Gruppi |
|-----------|--------------|--------------|
| Sequential | 1.0x | - |
| Parallel | 1.36x | 1 + (N-1) × 0.2 |
| Worktrees | 1.5-2.0x | 1 + (N-1) × 0.3 |

## 🔬 Esempio Python

```python
from task_analyzer import analyze_task, ExecutionStrategy

# Analizza task
analysis = analyze_task([
    "src/App.jsx",
    "api/main.py",
    "test_api.py"
], estimated_time=45)

# Controlla strategia
if analysis.strategy == ExecutionStrategy.PARALLEL:
    print(f"Speedup atteso: {analysis.estimated_speedup:.2f}x")
    print(f"Agenti: {', '.join(analysis.suggested_agents)}")
```

## 📝 Note

- **TEST domain ha priorità**: `test_api.py` → TEST (non BACKEND)
- **Dipendenze rilevate**: Analisi import/require automatica
- **JSON output**: Perfetto per integrare con orchestratore

---

**Versione**: 1.0.0
**Data**: 2026-01-01
**Autore**: Cervella Backend 🐝⚙️
