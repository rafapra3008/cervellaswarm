# FAQ CervellaSwarm

> *"Uno sciame di Cervelle. Una sola missione."* 🐝

**Versione:** 1.0.0
**Data:** 8 Gennaio 2026
**Sessione:** 124

---

## 📚 INDICE

1. [Cos'è CervellaSwarm?](#1-cosè-cervellaswarm)
2. [Come funziona spawn-workers?](#2-come-funziona-spawn-workers)
3. [Come creare un task?](#3-come-creare-un-task)
4. [Come monitorare i worker?](#4-come-monitorare-i-worker)
5. [Troubleshooting Comune](#5-troubleshooting-comune)

---

## 1. Cos'è CervellaSwarm?

### 🐝 La Spiegazione Semplice

CervellaSwarm è un sistema di orchestrazione multi-agente che permette a multiple istanze di Claude (chiamate "Cervelle") di lavorare in parallelo su task differenti, coordinate da un'Orchestratrice centrale (la "Regina").

Immagina uno sciame di api: ogni ape ha un compito specifico (raccogliere polline, costruire celle, nutrire le larve), ma tutte lavorano verso lo stesso obiettivo finale. Allo stesso modo, CervellaSwarm ha agenti specializzati:

- **cervella-frontend** 🎨 si occupa di UI/UX e React
- **cervella-backend** ⚙️ gestisce API e database
- **cervella-tester** 🧪 esegue test e QA
- **cervella-researcher** 🔬 fa ricerche tecniche approfondite
- **cervella-docs** 📝 scrive documentazione
- ...e altri 11 membri della famiglia!

### 💪 Benefici Principali

**Parallelizzazione reale:** Invece di fare un task alla volta, puoi avere 3-4-5 agenti che lavorano contemporaneamente su aspetti diversi dello stesso progetto. Questo moltiplica la produttività da 1x a 20x, 50x, potenzialmente 100x e oltre.

**Specializzazione:** Ogni agente è esperto nel suo dominio. Il frontend non deve preoccuparsi del database, il backend non deve pensare al CSS. Ognuno fa ciò che sa fare meglio.

**Zero conflitti:** Grazie a sistemi di isolamento (worktrees Git, task assegnati, comunicazione via filesystem), gli agenti non si pestano i piedi a vicenda. Niente merge hell, niente sovrapposizioni.

**Scalabilità:** Vuoi aggiungere un nuovo tipo di agente? Basta creare il DNA in `~/.claude/agents/` e sarà disponibile immediatamente in tutti i progetti.

---

## 2. Come funziona spawn-workers?

### 🚀 Il Cuore dello Sciame

`spawn-workers` è lo script shell che lancia i worker in sessioni tmux separate. È il comando che trasforma la teoria dello sciame in realtà operativa.

**Posizione:** `scripts/swarm/spawn-workers`
**Versione attuale:** v3.2.0 (unbuffered output)

### 📦 Comandi Base

```bash
# Spawna un singolo worker
spawn-workers --backend        # Lancia cervella-backend
spawn-workers --frontend       # Lancia cervella-frontend
spawn-workers --tester         # Lancia cervella-tester
spawn-workers --docs           # Lancia cervella-docs
spawn-workers --researcher     # Lancia cervella-researcher

# Spawna worker multipli contemporaneamente
spawn-workers --backend --frontend --tester

# Lancia tutti i worker principali
spawn-workers --all            # backend + frontend + tester

# Lista tutti i worker disponibili
spawn-workers --list

# Guardiane (agenti Opus per supervisione)
spawn-workers --guardiana-qualita
spawn-workers --guardiana-ops
spawn-workers --guardiana-ricerca
```

### 🪟 Modalità: Headless vs Window

**Headless (DEFAULT da v3.1.0):**
```bash
spawn-workers --backend
# Nessuna finestra visibile
# Worker lavora in background via tmux
# Output salvato in .swarm/logs/
```

**Window Mode (quando serve vedere l'agente lavorare):**
```bash
spawn-workers --backend --window
# Apre finestra Terminal.app
# Utile per debug o demo
# Stessa funzionalità, solo visuale
```

La modalità headless è preferita perché:
- Non ingombra lo schermo
- Permette di lanciare 10+ worker senza casino
- Output sempre catturabile via tmux
- "La magia è nascosta" (filosofia v3.1.0)

### 🔧 Come Funziona Internamente

1. **Check task ready:** Cerca file `.ready` in `.swarm/tasks/`
2. **Carica contesto:** Usa `load_context.py` per ottimizzare prompt
3. **Crea sessione tmux:** Nome formato `swarm_WORKER_TIMESTAMP`
4. **Lancia Claude:** Con `stdbuf -oL` per output realtime
5. **Monitora completamento:** watcher-regina rileva `.done`

### 🎯 Worker Disponibili (16 totali!)

| Flag | Worker | Specializzazione |
|------|--------|------------------|
| `--orchestrator` | cervella-orchestrator | Regina - coordina tutto |
| `--backend` | cervella-backend | Python, FastAPI, DB |
| `--frontend` | cervella-frontend | React, CSS, UI/UX |
| `--tester` | cervella-tester | Testing, QA, Debug |
| `--researcher` | cervella-researcher | Ricerca tecnica |
| `--scienziata` | cervella-scienziata | Ricerca strategica |
| `--reviewer` | cervella-reviewer | Code review |
| `--docs` | cervella-docs | Documentazione |
| `--devops` | cervella-devops | Deploy, CI/CD |
| `--data` | cervella-data | SQL, Analytics |
| `--security` | cervella-security | Audit sicurezza |
| `--marketing` | cervella-marketing | UX strategy |
| `--ingegnera` | cervella-ingegnera | Tech debt analysis |
| `--guardiana-qualita` | cervella-guardiana-qualita | Supervisione (Opus) |
| `--guardiana-ops` | cervella-guardiana-ops | Supervisione ops (Opus) |
| `--guardiana-ricerca` | cervella-guardiana-ricerca | Supervisione ricerca (Opus) |

---

## 3. Come creare un task?

### 📝 Il Formato Standard

Un task è composto da 2 file in `.swarm/tasks/`:

1. **`TASK_NOME.md`** - Descrizione completa del task
2. **`TASK_NOME.ready`** - Flag vuoto che segnala "task pronto"

### 🎯 Struttura del File Task

```markdown
# Task: [Titolo chiaro e conciso]

**Assegnato a:** cervella-WORKER
**Sessione:** 124
**Priorità:** ALTA/MEDIA/BASSA
**Stato:** ready

---

## 🎯 OBIETTIVO

[Cosa deve fare il worker - 2-3 righe chiare]

---

## 📋 TASK SPECIFICI

### 1. Primo step
- [ ] Azione specifica
- [ ] Altra azione

### 2. Secondo step
- [ ] Azione specifica

---

## 📤 OUTPUT RICHIESTO

**File da creare/modificare:**
- `path/to/file1.md`
- `path/to/file2.py`

**Formato output:**
[Descrizione di cosa ci aspettiamo]

---

## ✅ CRITERI DI SUCCESSO

- [x] Criterio 1
- [x] Criterio 2
- [x] Criterio 3

---

## 🔗 CONTESTO

**File da leggere prima:**
- `docs/ROADMAP_SACRA.md`
- `docs/studio/FILE_RILEVANTE.md`

**Riferimenti:**
- Link a documentazione
- Riferimenti esterni

---

**Creato:** [Data - Sessione]
**Regina:** Cervella Orchestratrice
**Worker:** cervella-WORKER

*"Motto motivazionale del worker!"* 🚀
```

### 🚦 Naming Convention

**Pattern:** `TASK_[DESCRIZIONE]_[VERSIONE].md`

**Esempi:**
- `TASK_HARDTEST_REALTIME_v124.md`
- `TASK_IMPLEMENTA_UNBUFFERED_v124.md`
- `TASK_RICERCA_PERFORMANCE_v123.md`
- `TASK_FIX_LOGIN_BUG_v125.md`

**Regole:**
- TASK_ sempre in maiuscolo
- Descrizione separata da underscore
- Versione = numero sessione o sprint
- Stesso nome per .md e .ready

### ✅ Marcare Task Come Ready

```bash
# Dopo aver creato TASK_NOME.md
touch .swarm/tasks/TASK_NOME.ready

# Il worker può ora prendere il task!
```

### 🔄 Ciclo di Vita del Task

```
.md creato → .ready aggiunto → worker lo vede
            ↓
    worker prende task (.working creato)
            ↓
    worker lavora (heartbeat ogni 60s)
            ↓
    worker finisce (.done creato, _output.md scritto)
            ↓
    watcher notifica Regina
            ↓
    Regina verifica output
            ↓
    Task archiviato o riassegnato
```

---

## 4. Come monitorare i worker?

### 👀 Vedere Cosa Sta Facendo un Worker

**Metodo 1: Attach alla sessione tmux**
```bash
# Lista tutte le sessioni swarm attive
tmux list-sessions | grep swarm

# Output esempio:
# swarm_backend_20260108_131045: 1 windows (created Wed Jan  8 13:10:45 2026)
# swarm_frontend_20260108_131052: 1 windows (created Wed Jan  8 13:10:52 2026)

# Attacca alla sessione per vedere in tempo reale
tmux attach -t swarm_backend_20260108_131045

# Per uscire SENZA chiudere la sessione: Ctrl+B poi D (detach)
```

**Metodo 2: Capture pane (senza attach)**
```bash
# Cattura le ultime 20 righe
tmux capture-pane -t swarm_backend_20260108_131045 -p | tail -20

# Cattura TUTTO l'output dall'inizio
tmux capture-pane -t swarm_backend_20260108_131045 -p -S -

# Salva in file per analisi
tmux capture-pane -t swarm_backend_20260108_131045 -p -S - > debug_output.log
```

### 📂 Log Files

**Heartbeat (progresso worker):**
```bash
cat .swarm/status/heartbeat_backend.log

# Output esempio:
# 1736339445|TASK_API_ENDPOINTS|Leggendo schema database
# 1736339505|TASK_API_ENDPOINTS|Scrivendo endpoint /hotels
# 1736339565|TASK_API_ENDPOINTS|Testing endpoint con curl
```

**Task corrente:**
```bash
cat .swarm/status/worker_backend.task

# Output: TASK_API_ENDPOINTS_v124
```

**Output finale del task:**
```bash
cat .swarm/tasks/TASK_API_ENDPOINTS_v124_output.md
```

### ⏰ Watcher Regina (Auto-Sveglia)

Il sistema include uno script `watcher-regina.sh` che monitora automaticamente il completamento dei task e notifica la Regina.

**Come funziona:**
1. Monitora `.swarm/tasks/` per file `.done`
2. Quando rileva completamento, scrive messaggio nel background bash della Regina
3. Regina riceve notifica system-reminder con "Background bash has new output"
4. Regina legge output e verifica risultato

**Attivazione manuale (se non già attivo):**
```bash
# Check se watcher è attivo
ps aux | grep watcher-regina

# Avvia watcher in background
nohup ./scripts/swarm/watcher-regina.sh > .swarm/logs/watcher.log 2>&1 &

# Stoppa watcher
pkill -f watcher-regina.sh
```

### 📊 Dashboard Rapido

```bash
# Crea script di monitoring veloce
cat > monitor-swarm.sh << 'EOF'
#!/bin/bash
clear
echo "=== CERVELLASWARM STATUS ==="
echo ""
echo "📋 TASK READY:"
ls -1 .swarm/tasks/*.ready 2>/dev/null | wc -l
echo ""
echo "⚙️  WORKER ATTIVI:"
tmux list-sessions | grep swarm | wc -l
echo ""
echo "✅ TASK COMPLETATI (ultimi 5):"
ls -1t .swarm/tasks/*.done 2>/dev/null | head -5 | xargs -n1 basename
echo ""
echo "🔄 WORKER CORRENTI:"
for worker in backend frontend tester docs researcher; do
  if [ -f ".swarm/status/worker_${worker}.task" ]; then
    task=$(cat .swarm/status/worker_${worker}.task)
    echo "  $worker: $task"
  fi
done
EOF

chmod +x monitor-swarm.sh
./monitor-swarm.sh
```

---

## 5. Troubleshooting Comune

### ❌ Problema: Worker non parte

**Sintomo:** `spawn-workers --backend` non fa nulla o dà errore.

**Diagnosi:**
```bash
# 1. Verifica che spawn-workers sia eseguibile
ls -la scripts/swarm/spawn-workers
# Se non ha permesso x: chmod +x scripts/swarm/spawn-workers

# 2. Verifica che tmux sia installato
which tmux
# Se non trovato: brew install tmux

# 3. Verifica che ci sia almeno un task .ready
ls -la .swarm/tasks/*.ready
# Se vuoto: crea un task!

# 4. Verifica che l'agent esista
ls -la ~/.claude/agents/cervella-backend.md
# Se mancante: copia da CervellaSwarm/agents/
```

**Soluzione:**
- Installa dipendenze mancanti (tmux, coreutils)
- Verifica permessi esecuzione script
- Assicurati che ci sia almeno un task .ready assegnato al worker

### 📭 Problema: Output non visibile

**Sintomo:** Worker sembra lavorare ma non vedo output in tmux.

**Diagnosi:**
```bash
# 1. Verifica che sessione tmux esista
tmux list-sessions | grep swarm

# 2. Prova capture completo
tmux capture-pane -t swarm_backend_[TIMESTAMP] -p -S -

# 3. Verifica versione spawn-workers
head -20 scripts/swarm/spawn-workers | grep VERSION
# Dovrebbe essere v3.2.0 con unbuffered output
```

**Soluzione:**
- Se versione < v3.2.0: aggiorna spawn-workers per output realtime
- Se output comunque ritardato: verifica che `stdbuf` o `gstdbuf` sia installato
  ```bash
  brew install coreutils  # Installa gstdbuf su macOS
  ```

### ⏸️ Problema: Task non completato

**Sintomo:** Worker sembra bloccato, nessun file `.done` creato.

**Diagnosi:**
```bash
# 1. Attacca alla sessione per vedere cosa sta facendo
tmux attach -t swarm_backend_[TIMESTAMP]

# 2. Controlla heartbeat (dovrebbe aggiornarsi ogni 60s)
tail -f .swarm/status/heartbeat_backend.log

# 3. Verifica se ha generato errori
tmux capture-pane -t swarm_backend_[TIMESTAMP] -p | grep -i error
```

**Soluzioni comuni:**

**A. Worker aspetta input utente**
- Attach alla sessione, vedi cosa chiede
- Se servono decisioni, rispondi nel terminale tmux

**B. Worker ha finito ma non ha creato .done**
- Crea manualmente:
  ```bash
  touch .swarm/tasks/TASK_NOME.done
  ```
- Estrai output:
  ```bash
  tmux capture-pane -t swarm_backend_[TIMESTAMP] -p -S - > \
      .swarm/tasks/TASK_NOME_output.md
  ```

**C. Task troppo grande/complesso**
- Spezza in sub-task più piccoli
- Ogni task dovrebbe richiedere 15-45 minuti massimo

**D. Worker crashato**
- Check se sessione tmux esiste ancora: `tmux list-sessions | grep swarm`
- Se sessione morta, rilancia: `spawn-workers --backend`
- Analizza log in `.swarm/logs/` per capire causa

### 🔄 Problema: Multipli worker in conflitto

**Sintomo:** Due worker modificano lo stesso file.

**Prevenzione (ZERO CASINO rule):**
- Assegna file diversi a worker diversi
- Frontend → `frontend/`, `components/`
- Backend → `backend/`, `api/`
- Usa worktrees Git per isolamento totale

**Soluzione se succede:**
```bash
# 1. Ferma immediatamente i worker
tmux kill-session -t swarm_backend_[TIMESTAMP]
tmux kill-session -t swarm_frontend_[TIMESTAMP]

# 2. Verifica stato Git
git status

# 3. Decidi quale output tenere o mergea manualmente
# 4. Riassegna task con scope più chiaro
```

### 🆘 Comando Panic: Reset Completo

Se tutto è andato storto e vuoi ricominciare da zero:

```bash
#!/bin/bash
# ATTENZIONE: Questo ferma TUTTO e pulisce lo stato

# 1. Ferma tutti i worker
tmux kill-server

# 2. Pulisci file .working e .done
rm -f .swarm/tasks/*.working
rm -f .swarm/tasks/*.done

# 3. Reset heartbeat
rm -f .swarm/status/heartbeat_*.log
rm -f .swarm/status/worker_*.task

# 4. Backup output importanti
mkdir -p .swarm/backup_$(date +%Y%m%d_%H%M%S)
cp .swarm/tasks/*_output.md .swarm/backup_*/ 2>/dev/null

# 5. Pronto per ricominciare!
echo "✅ Sistema resettato. Puoi rilanciare spawn-workers."
```

---

## 🎓 Risorse Aggiuntive

**Documentazione principale:**
- `CLAUDE.md` - Overview progetto
- `NORD.md` - Bussola e direzione
- `ROADMAP_SACRA.md` - Fasi e sprint
- `PROMPT_RIPRESA.md` - Stato attuale

**Guide approfondite:**
- `docs/studio/STUDIO_SUBAGENTS.md` - Architettura agenti
- `docs/guide/GUIDA_WORKTREES.md` - Isolamento Git
- `docs/architettura/ARCHITETTURA_SISTEMA.md` - Design completo

**Script utili:**
- `scripts/swarm/spawn-workers` - Launcher principale
- `scripts/swarm/watcher-regina.sh` - Monitoring automatico
- `scripts/swarm/task_manager.py` - Gestione task

---

## ❓ Domande Non Coperte?

Questa FAQ viene aggiornata continuamente. Se hai domande non coperte qui:

1. Controlla `PROMPT_RIPRESA.md` per lo stato attuale del sistema
2. Leggi `docs/studio/` per studi approfonditi
3. Chiedi alla Regina (cervella-orchestrator) via handoff:
   ```bash
   cat > .swarm/handoff/DOMANDA_[TOPIC].md << 'EOF'
   # Domanda per la Regina

   [La tua domanda qui]
   EOF
   ```

---

**Creato:** 8 Gennaio 2026 - Sessione 124
**Worker:** cervella-docs 📝
**Rating:** Test Output Realtime

*"La documentazione è il ponte tra idea e realtà!"* 📚✨
