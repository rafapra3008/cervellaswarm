# RICERCA: Background Agent Execution Patterns 2025-2026

> **Ricerca:** Cugino #3 (cervella-researcher)
> **Data:** 1 Gennaio 2026
> **Contesto:** PoC Cugini - Ricerca Parallela

---

## EXECUTIVE SUMMARY

L'esecuzione di agenti in background nel 2025-2026 si basa su pattern **async-first** con progress reporting standardizzato. Claude Code supporta `run_in_background=true` per Bash, mentre il Task tool richiede pattern alternativi (parallel execution). MCP Tasks (Nov 2025) introduce il protocollo **call-now-fetch-later** rivoluzionario. Best practices: timeout espliciti, error handling robusto, checkpoint frequenti, e human-in-the-loop per azioni irreversibili. Per CervellaSwarm: continuare con parallel execution (già funziona!), valutare webhook hub per trigger automatici.

---

## 1. STATE OF THE ART

### Claude Code Background Execution

```
┌─────────────────────────────────────────────────────────────────┐
│  CLAUDE CODE BACKGROUND SUPPORT (2025)                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  BASH TOOL:                                                     │
│  ✅ run_in_background: true  → FUNZIONA!                       │
│  ✅ TaskOutput per recupero risultati                          │
│  ✅ Timeout configurabile (600s max)                           │
│                                                                 │
│  TASK TOOL:                                                     │
│  🔴 run_in_background: true  → Feature Request #9905           │
│  ✅ Parallel execution (multiple Tasks in 1 message)           │
│  ✅ Blocking call (aspetta completamento)                      │
│                                                                 │
│  WORKAROUND ATTUALE:                                            │
│  → Usa parallel Task calls (come abbiamo fatto nel PoC!)       │
│  → Tutti partono insieme, risultati arrivano quando pronti     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### MCP Tasks Protocol (Nov 2025)

```
┌─────────────────────────────────────────────────────────────────┐
│  MCP TASKS - CALL NOW, FETCH LATER                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Client → tasks/create → Server                             │
│     (riceve task_id immediatamente)                            │
│                                                                 │
│  2. Client continua a lavorare...                              │
│                                                                 │
│  3. Client → tasks/get(task_id) → Check progress               │
│     (running/completed/failed/cancelled)                        │
│                                                                 │
│  4. Quando completed → recupera risultato                      │
│                                                                 │
│  VANTAGGI:                                                      │
│  ✅ Non-blocking                                                │
│  ✅ Progress reporting standardizzato                          │
│  ✅ Cross-request state machine                                │
│  ✅ Cancellation support                                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. PATTERN PRINCIPALI

### Pattern 1: Webhooks > Polling

```
POLLING (Evitare):
┌─────────────────────────────────────────────────────────────────┐
│  while True:                                                    │
│      status = check_status()  # 💰 Costa ogni volta!           │
│      if status == "done":                                       │
│          break                                                  │
│      sleep(5)                                                   │
│                                                                 │
│  PROBLEMA: 0 eventi = comunque 1000 check = 💸                 │
└─────────────────────────────────────────────────────────────────┘

WEBHOOK (Preferire):
┌─────────────────────────────────────────────────────────────────┐
│  register_webhook(on_complete=callback)                         │
│  # Vai a fare altro...                                          │
│  # Webhook chiama callback quando pronto                        │
│                                                                 │
│  VANTAGGIO: 0 eventi = 0 costi!                                │
└─────────────────────────────────────────────────────────────────┘
```

### Pattern 2: Progress Reporting

```python
# Pattern raccomandato
class BackgroundTask:
    def __init__(self):
        self.progress = 0
        self.status = "running"
        self.checkpoint_file = "task_progress.md"

    def update_progress(self, percent, message):
        self.progress = percent
        # Scrivi checkpoint per recovery
        with open(self.checkpoint_file, 'w') as f:
            f.write(f"Progress: {percent}%\n{message}")

    def run(self):
        self.update_progress(0, "Starting...")
        # ... lavoro ...
        self.update_progress(50, "Halfway done")
        # ... altro lavoro ...
        self.update_progress(100, "Complete!")
        self.status = "completed"
```

### Pattern 3: Timeout e Retry

```
┌─────────────────────────────────────────────────────────────────┐
│  TIMEOUT STRATEGY                                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  TIER 1: Quick tasks (< 30s)                                   │
│  → Timeout: 60s                                                 │
│  → Retry: 2x con backoff                                        │
│                                                                 │
│  TIER 2: Medium tasks (30s - 5min)                             │
│  → Timeout: 10min                                               │
│  → Retry: 1x                                                    │
│  → Checkpoint ogni 1min                                         │
│                                                                 │
│  TIER 3: Long tasks (> 5min)                                   │
│  → Timeout: 30min (max)                                         │
│  → No retry (troppo costoso)                                    │
│  → Checkpoint ogni 30s                                          │
│  → Human notification se fallisce                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. BEST PRACTICES

### Do's

| Practice | Perché | Come |
|----------|--------|------|
| **Checkpoint frequenti** | Recovery da crash | File .md con stato |
| **Timeout espliciti** | Evita task zombie | Config per tier |
| **Error categorization** | Retry intelligente | Transient vs Fatal |
| **Progress reporting** | Visibility | Percentuale + messaggio |
| **Graceful degradation** | Resilienza | Fallback a sequential |

### Don'ts

| Anti-pattern | Problema | Alternativa |
|--------------|----------|-------------|
| **Fire and forget** | Lost tasks | Always track |
| **Infinite timeout** | Resource leak | Max 30min |
| **Retry everything** | Waste | Categorize errors |
| **No progress** | Black box | Report ogni step |

---

## 4. CLAUDE CODE SPECIFICO

### Pattern Attuale (Funzionante)

```
┌─────────────────────────────────────────────────────────────────┐
│  PARALLEL TASK EXECUTION (Come nel PoC!)                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  // Un solo messaggio, 3 Task tool calls                       │
│  // Tutti partono "insieme", risultati arrivano quando pronti  │
│                                                                 │
│  VANTAGGI:                                                      │
│  ✅ Funziona OGGI (no feature request)                         │
│  ✅ Parallel reale (non finto)                                  │
│  ✅ Risultati aggregati                                         │
│                                                                 │
│  LIMITAZIONI:                                                   │
│  🔴 Blocking (Regina aspetta tutti)                            │
│  🔴 No progress mid-execution                                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 5. APPLICABILITA CERVELLASWARM

### Cosa Funziona Oggi

| Feature | Stato | Come |
|---------|-------|------|
| **Parallel Tasks** | ✅ FUNZIONA | Multiple Task calls in 1 message |
| **Bash Background** | ✅ FUNZIONA | run_in_background: true |
| **TaskOutput** | ✅ FUNZIONA | Recupera risultati Bash |

### Cosa Manca

| Feature | Stato | Workaround |
|---------|-------|------------|
| **Task Background** | 🔴 Non supportato | Usa parallel calls |
| **Progress Reporting** | 🔴 Non supportato | Checkpoint in file |
| **Cancellation** | 🔴 Non supportato | Kill manual |

### Raccomandazioni

1. **Continuare con Parallel Execution** - Funziona benissimo!
2. **Checkpoint via file** - Progress reporting manuale
3. **Valutare Webhook Hub** - Per trigger automatici (code review Lun/Ven)
4. **Monitorare MCP Tasks** - Quando disponibile, adottare

---

## FONTI

1. Claude Code Documentation (run_in_background)
2. MCP Tasks Specification (Nov 2025)
3. Google ADK Background Execution
4. Microsoft Agent Framework Async Patterns
5. Anthropic Context Engineering Guide
6. LangGraph Async Execution
7. Temporal Workflow Engine Patterns

---

*"Non reinventiamo la ruota - studiamo chi l'ha già fatta!"* 🔬

*Ricerca completata da Cugino #3 - PoC Parallelizzazione* 🐝