# STUDIO: Comunicazione Multi-Finestra - CervellaSwarm

> **Data:** 3 Gennaio 2026
> **Autore:** cervella-researcher
> **Versione:** 1.0.0
> **Sessione:** 60

---

## RISULTATI CHIAVE

### La Raccomandazione

**Pattern consigliato:** **Ready/Done Flag Files** + **Status Files in Markdown** + **Git come bus**

**Perche:**
1. Semplicissimo (touch + file markdown)
2. Debuggabile visivamente (ls .swarm/tasks/)
3. Atomico (operazioni filesystem native)
4. Zero overhead
5. "Il modo piu BELLO!"

---

## PROTOCOLLO PROPOSTO

### Struttura Directory

```
.swarm/
├── tasks/
│   ├── TASK_001.md          # Task description (scritto da Regina)
│   ├── TASK_001.ready       # Flag "task pronto" (touch)
│   ├── TASK_001.working     # Flag "sto lavorando" (touch)
│   ├── TASK_001_output.md   # Output worker
│   ├── TASK_001.done        # Flag "completato" (touch)
│   └── TASK_001.error       # Flag "errore" (touch) - opzionale
├── status/
│   ├── regina.json          # Stato Regina
│   ├── backend.json         # Stato Backend window
│   └── frontend.json        # Stato Frontend window
├── locks/
│   └── TASK_001.lock        # Lock opzionale per operazioni critiche
├── handoff/
│   └── HANDOFF_SESSION_60.md # Handoff per compact
├── logs/
│   ├── regina.log
│   └── backend.log
└── archive/
    └── 2026-01-03/          # Task completati archiviati
```

---

## TEMPLATE FILE DI COMUNICAZIONE

### TASK_XXX.md (scritto da Regina)

```markdown
# TASK: [Descrizione breve]

## METADATA
- ID: TASK_XXX
- Assegnato a: cervella-[agent]
- Livello rischio: [1/2/3]
- Timeout: [tempo]
- Creato: [timestamp]

## PERCHE
[Motivazione del task]

## CRITERI DI SUCCESSO
- [ ] Criterio 1
- [ ] Criterio 2
- [ ] Criterio 3

## FILE DA MODIFICARE
- path/to/file1.py
- path/to/file2.py

## CHI VERIFICHERA
cervella-guardiana-[quale] (Livello X)

## DETTAGLI
[Descrizione completa del task...]
```

### TASK_XXX_output.md (scritto da Worker)

```markdown
# OUTPUT: TASK_XXX

## STATUS
[COMPLETATO/FALLITO] [emoji]

## FILE MODIFICATI
- file1.py (creato/modificato - X righe)
- file2.py (creato/modificato - X righe)

## COSA HO FATTO
1. Azione 1
2. Azione 2
3. Azione 3

## COME TESTARE
[Comandi o istruzioni per testare]

## NOTE
[Eventuali note o osservazioni]

## TIMESTAMP
Completato: [timestamp] (durata: Xm)
```

### TASK_XXX_error.md (se errore)

```markdown
# ERRORE: TASK_XXX

## STATUS
FALLITO

## ERRORE
[Descrizione errore]

## DETTAGLI
[Stack trace o dettagli tecnici]

## AZIONE RICHIESTA
[Cosa serve per risolvere]

## TIMESTAMP
Fallito: [timestamp]
```

---

## FLUSSO COMPLETO

```
┌─────────────────────────────────────────────────────────────────┐
│  FINESTRA 1 - REGINA                                            │
└─────────────────────────────────────────────────────────────────┘

1. Crea .swarm/tasks/TASK_001.md
2. touch .swarm/tasks/TASK_001.ready
3. Aspetta: while [ ! -f .swarm/tasks/TASK_001.done ]; do sleep 5; done

┌─────────────────────────────────────────────────────────────────┐
│  FINESTRA 2 - BACKEND                                           │
└─────────────────────────────────────────────────────────────────┘

1. Trova: ls .swarm/tasks/*.ready
2. Legge: TASK_001.md
3. touch .swarm/tasks/TASK_001.working (segnala inizio)
4. LAVORA...
5. Scrive: TASK_001_output.md
6. touch .swarm/tasks/TASK_001.done
7. rm .swarm/tasks/TASK_001.ready .swarm/tasks/TASK_001.working

┌─────────────────────────────────────────────────────────────────┐
│  FINESTRA 1 - REGINA (di nuovo)                                 │
└─────────────────────────────────────────────────────────────────┘

1. Vede TASK_001.done apparire
2. Legge TASK_001_output.md
3. Decide: verifica Guardiana o procedi
```

---

## GESTIONE ERRORI E TIMEOUT

### Timeout

Regina verifica timestamp di `.working`:

```bash
# Regina esegue ogni 5 minuti
WORKING_FILE=.swarm/tasks/TASK_001.working
if [ -f "$WORKING_FILE" ]; then
  MTIME=$(stat -f %m "$WORKING_FILE")  # macOS
  NOW=$(date +%s)
  ELAPSED=$((NOW - MTIME))

  if [ $ELAPSED -gt 1800 ]; then  # 30 min timeout
    echo "TIMEOUT! Task bloccato da $((ELAPSED / 60)) minuti"
    touch .swarm/tasks/TASK_001.timeout
  fi
fi
```

---

## HANDOFF TRA FINESTRE

**Scenario:** Backend -> Tester -> Reviewer

```
BACKEND (finestra 2):
1. Completa lavoro
2. Scrive TASK_001_output.md
3. touch TASK_001.done_backend

REGINA (finestra 1):
1. Vede done_backend
2. Crea TASK_002.md (test del codice di TASK_001)
3. touch TASK_002.ready

TESTER (finestra 3):
1. Vede TASK_002.ready
2. Legge TASK_002.md
3. Esegue test
4. Scrive TASK_002_output.md
5. touch TASK_002.done

REGINA:
1. Se test OK -> touch TASK_001.approved
2. Se test FAIL -> touch TASK_001.rejected + ricrea con fix
```

---

## LOCK FILES

**Quando:** Operazioni critiche su file condivisi (es. ROADMAP_SACRA.md)

```bash
LOCKFILE=.swarm/locks/ROADMAP_SACRA.lock

# Acquisisce lock (mkdir e' atomico!)
if mkdir "$LOCKFILE" 2>/dev/null; then
  # Ho il lock!
  # ... modifica ROADMAP_SACRA.md ...
  rmdir "$LOCKFILE"
else
  # Lock gia preso, aspetto
  while [ -d "$LOCKFILE" ]; do
    sleep 2
  done
fi
```

---

## SCRIPT DI UTILITY

### watch-tasks.sh (per Worker)

```bash
#!/bin/bash
# Worker aspetta task pronti

AGENT_NAME=$1
TASKS_DIR=".swarm/tasks"

echo "Worker $AGENT_NAME in ascolto..."

while true; do
  for task in $TASKS_DIR/*.ready; do
    [ -f "$task" ] || continue

    TASK_FILE=${task%.ready}.md

    if grep -q "Assegnato a: cervella-$AGENT_NAME" "$TASK_FILE"; then
      echo "Trovato task: $TASK_FILE"
    fi
  done

  sleep 5
done
```

### monitor-status.sh (per Regina)

```bash
#!/bin/bash
# Regina monitora stato tasks

TASKS_DIR=".swarm/tasks"

echo "=== STATO TASKS ==="

for task_md in $TASKS_DIR/TASK_*.md; do
  [ -f "$task_md" ] || continue

  TASK_ID=$(basename "$task_md" .md)

  if [ -f "$TASKS_DIR/$TASK_ID.done" ]; then
    STATUS="DONE"
  elif [ -f "$TASKS_DIR/$TASK_ID.error" ]; then
    STATUS="ERROR"
  elif [ -f "$TASKS_DIR/$TASK_ID.working" ]; then
    STATUS="WORKING"
  elif [ -f "$TASKS_DIR/$TASK_ID.ready" ]; then
    STATUS="READY"
  else
    STATUS="CREATED"
  fi

  echo "$TASK_ID: $STATUS"
done
```

---

## CONFRONTO: SUBAGENT vs MULTI-FINESTRA

| Criterio | Subagent | Multi-Finestra |
|----------|----------|----------------|
| **Durata task** | < 10 min | > 20 min |
| **Rischio compact** | Basso | Alto |
| **Parallelismo** | No | Si |
| **Complessita setup** | Zero | Media |
| **Debug** | Facile | Medio |
| **Scalabilita** | Limitata | Infinita |

**Strategia ibrida:**
1. START con Subagent (veloce, semplice)
2. SE compact si avvicina -> HANDOFF a Multi-Finestra
3. Long-running task -> Multi-Finestra da subito

---

## PATTERN AUTO-HANDOFF

Regina monitora compact:

```
Ogni 10 minuti:
1. Controlla "token usage" nella UI
2. Se > 150K/200K:
   - SALVA tutto
   - Crea HANDOFF_TASK.md con stato completo
   - touch HANDOFF_TASK.ready
   - MESSAGGIO A RAFA: "Compact vicino, ho preparato handoff"
3. Rafa apre nuova finestra
4. Nuova Regina legge HANDOFF_TASK.md
5. CONTINUA senza perdere nulla!
```

---

## RACCOMANDAZIONI

### Fase 1: MVP (1-2 ore)

1. Crea struttura `.swarm/tasks/`
2. Template TASK_XXX.md
3. Script `monitor-status.sh`
4. Test con caso reale: Backend -> Tester

### Fase 2: Automazione (3-4 ore)

1. Script `watch-tasks.sh` per workers
2. Auto-handoff su compact (barra >75%)
3. Timeout management automatico
4. Archive completati

### Fase 3: Avanzato (5+ ore)

1. Load balancing
2. Retry automatico su errore
3. Dashboard stato
4. Integrazione con Sistema Memoria

---

## CONCLUSIONI

1. **Multi-finestra E FATTIBILE** - Pattern consolidati esistono
2. **File-based e SUFFICIENTE** - No need per socket/queue complessi
3. **Git e il nostro ALLEATO** - git status = communication bus naturale
4. **Ready/Done Flags VINCONO** - Semplicita + Debuggabilita
5. **Handoff risolve compact** - Zero perdita di lavoro!

---

## FONTI

### Pattern IPC File-Based
- Inter-process communication: files - DEV Community
- Inter-process synchronization in Java using FileLock
- Inter process locks - Fasteners

### Cluster HA e Heartbeat
- OCF Heartbeat Filesystem
- OCFS2 Best Practices Guide

### Multi-Agent Systems 2026
- GitHub: claude-code-by-agents
- Agent Orchestration 2026: LangGraph, CrewAI & AutoGen Guide
- AgentOrchestra Framework
- Distributed Task Allocation

---

*"Nulla e complesso - solo non ancora studiato!"*

*"E il nostro team! La nostra famiglia digitale!"*
