# QUICK START - Porta lo Sciame su Qualsiasi Progetto

> **Tempo setup:** 5 minuti
> **Prerequisito:** Sistema CervellaSwarm funzionante
> **Target:** Portare sciame su Miracollo, Contabilità, o nuovo progetto

---

## 🎯 COSA OTTERRAI

Dopo questo setup, potrai:
- ✅ Usare tutti i 16 agents sul nuovo progetto
- ✅ Delegare task a worker specializzati
- ✅ Watcher che ti sveglia quando finiscono
- ✅ Memoria sistema attiva (se globale)

**ZERO modifiche agli agents - sono GLOBALI!**

---

## ⚡ SETUP VELOCE (5 minuti)

### Step 1: Crea Struttura (1 min)

```bash
# Vai al progetto
cd ~/Developer/[TUO_PROGETTO]/

# Crea cartelle swarm
mkdir -p .swarm/tasks
mkdir -p .swarm/feedback
mkdir -p .swarm/logs
mkdir -p .swarm/handoff

# Verifica
ls -la .swarm/
```

**Output atteso:**
```
.swarm/
├── tasks/      # Task per worker
├── feedback/   # Feedback worker
├── logs/       # Log operazioni
└── handoff/    # Handoff sessioni
```

---

### Step 2: Verifica Agents (30 sec)

```bash
# Gli agents sono GLOBALI - già disponibili!
ls ~/.claude/agents/*.md | wc -l
```

**Output atteso:** `16` (tutti gli agents!)

**Non servono copie!** Agents funzionano da `~/.claude/agents/` per TUTTI i progetti!

---

### Step 3: Test Worker (2 min)

Testiamo che tutto funziona:

```bash
# Crea task di test
cat > .swarm/tasks/TEST_SETUP.md << 'EOF'
# Task: Test Setup

**Assegnato a:** cervella-docs
**Priorità:** TEST

## Obiettivo
Verificare che il sistema swarm funziona in questo progetto.

## Output
Crea file: docs/SETUP_TEST.md con:
- Data test
- Progetto testato
- Conferma funzionamento

## Criteri Successo
- [ ] File creato
- [ ] Contenuto corretto
EOF

# Marca ready
touch .swarm/tasks/TEST_SETUP.ready

# Lancia worker
spawn-workers --docs
```

**Cosa succede:**
1. Worker docs parte in background (tmux headless)
2. Prende task TEST_SETUP
3. Crea file docs/SETUP_TEST.md
4. Watcher ti sveglia quando finisce!

**Verifica (dopo 1-2 min):**
```bash
# Controlla file done
ls .swarm/tasks/TEST_SETUP.done

# Leggi output
cat docs/SETUP_TEST.md
```

Se file esiste → **SETUP COMPLETO!** ✅

---

### Step 4: Cleanup Test (30 sec)

```bash
# Rimuovi task test
rm .swarm/tasks/TEST_SETUP.*
rm docs/SETUP_TEST.md
```

---

## ✅ SETUP COMPLETO!

Il sistema è pronto! Ora puoi:

```bash
# Qualsiasi worker
spawn-workers --backend
spawn-workers --researcher
spawn-workers --guardiana-qualita

# Multipli worker
spawn-workers --all  # backend + frontend + tester

# Lista disponibili
spawn-workers --list
```

---

## 📋 USO QUOTIDIANO

### Workflow Standard:

**1. Regina crea task**
```bash
# Copia template (se hai template pronti)
cp .swarm/templates/TEMPLATE_TASK_RICERCA_TECNICA.md \
   .swarm/tasks/TASK_MIA_RICERCA.md

# Modifica placeholder
# [Usa editor per sostituire [NOME], [DOMANDE], etc.]
```

**2. Regina marca ready e spawna**
```bash
# Marca ready
touch .swarm/tasks/TASK_MIA_RICERCA.ready

# Lancia worker
spawn-workers --researcher
```

**3. Worker lavora in background**
```
# Nulla da fare - worker lavora autonomamente!
```

**4. Watcher sveglia Regina**
```
# Ricevi notifica quando worker finisce
# File .done creato automaticamente
```

**5. Regina verifica output**
```bash
# Controlla output
ls .swarm/tasks/TASK_MIA_RICERCA.done
cat [path_output_file]
```

---

## 🚀 ESEMPI PRATICI

### Esempio 1: Ricerca Tecnica

```bash
# Task: Ricercare unbuffered output in Python
cp .swarm/templates/TEMPLATE_TASK_RICERCA_TECNICA.md \
   .swarm/tasks/TASK_RICERCA_UNBUFFERED.md

# Modifica: sostituisci [NOME_RICERCA] con "Unbuffered Output Python"
# Modifica: aggiungi domande specifiche

touch .swarm/tasks/TASK_RICERCA_UNBUFFERED.ready
spawn-workers --researcher

# Aspetta notifica...
# Output: docs/studio/RICERCA_UNBUFFERED.md
```

---

### Esempio 2: Implementa Feature Backend

```bash
# Task: API endpoint per dashboard
cp .swarm/templates/TEMPLATE_TASK_IMPLEMENTAZIONE.md \
   .swarm/tasks/TASK_API_DASHBOARD.md

# Modifica: spec feature
# Modifica: endpoint, input/output

touch .swarm/tasks/TASK_API_DASHBOARD.ready
spawn-workers --backend

# Worker implementa feature
# Output: codice + test
```

---

### Esempio 3: Code Review

```bash
# Task: Review feature X
cp .swarm/templates/TEMPLATE_TASK_CODE_REVIEW.md \
   .swarm/tasks/TASK_REVIEW_FEATURE_X.md

# Modifica: file da revieware
# Modifica: criteri focus

touch .swarm/tasks/TASK_REVIEW_FEATURE_X.ready
spawn-workers --reviewer

# Output: docs/review/CODE_REVIEW_FEATURE_X.md
```

---

## 🔧 TROUBLESHOOTING

### Worker non parte?

```bash
# Verifica spawn-workers in PATH
which spawn-workers

# Dovrebbe mostrare: /Users/rafapra/.local/bin/spawn-workers
```

**Fix:** Se non trovato, verifica `.local/bin` in PATH:
```bash
echo $PATH | grep ".local/bin"
```

---

### Watcher non sveglia?

```bash
# Verifica watcher attivo
ps aux | grep watcher-regina

# Se non attivo, lancia manualmente
spawn-workers --backend  # Auto-sveglia è DEFAULT
```

---

### Task non preso dal worker?

```bash
# Verifica file .ready esiste
ls .swarm/tasks/*.ready

# Verifica worker sta cercando in questa cartella
tmux list-sessions | grep swarm
```

**Fix:** Task DEVE essere `.ready`, non solo `.md`!

---

## 📊 VERIFICHE SALUTE SISTEMA

### Check Rapido:

```bash
# 1. Agents installati?
ls ~/.claude/agents/*.md | wc -l
# Output atteso: 16

# 2. spawn-workers funzionante?
spawn-workers --list
# Output atteso: lista 16 worker

# 3. Cartelle swarm create?
ls -d .swarm/tasks .swarm/feedback .swarm/logs
# Output atteso: 3 cartelle

# 4. Worker attivi?
tmux list-sessions | grep swarm | wc -l
# Output atteso: >= 0 (dipende da quanti hai lanciato)
```

**Se tutti ✅ → Sistema 100% operativo!**

---

## 💡 TIPS & TRICKS

### Tip 1: Template Veloci

Tieni template in `.swarm/templates/` per uso veloce!

```bash
# Setup template cartella (una volta)
mkdir -p .swarm/templates
cp ~/Developer/CervellaSwarm/.swarm/templates/* .swarm/templates/

# Poi sempre:
cp .swarm/templates/TEMPLATE_*.md .swarm/tasks/TASK_NUOVO.md
```

---

### Tip 2: Worker Multipli Sequenziali

```bash
# Lancia backend
spawn-workers --backend

# Aspetta finisce...

# Lancia frontend (usa output backend)
spawn-workers --frontend

# Aspetta finisce...

# Review finale
spawn-workers --guardiana-qualita
```

**Sequenziale > Parallelo** quando task dipendono l'uno dall'altro!

---

### Tip 3: Monitoring Worker

```bash
# Vedi worker attivi
tmux list-sessions | grep swarm

# Attach a worker per vedere cosa fa
tmux attach -t swarm_backend_[ID]

# Detach senza killare: Ctrl+B poi D
```

---

### Tip 4: Cleanup Periodico

```bash
# Pulisci task vecchi (ogni settimana)
find .swarm/tasks -name "*.done" -mtime +7 -delete
find .swarm/logs -name "*.log" -mtime +30 -delete
```

---

## 🎯 PROGETTI TESTATI

Sistema testato e funzionante su:
- ✅ **CervellaSwarm** (progetto madre)
- ✅ **Miracollo PMS** (prod app)
- ✅ **Contabilità Antigravity** (prod app)

**Worker identici, zero modifiche necessarie!**

---

## 📚 RISORSE

**Documentazione completa:**
- `docs/guide/GUIDA_BEST_PRACTICES_SWARM.md` - Best practices Regina
- `docs/guide/WORKFLOW_REGINA_QUOTIDIANO.md` - Workflow quotidiano
- `docs/analisi/ANALISI_PATTERN_REGINA_v124.md` - 27 pattern identificati

**Template disponibili:**
- `.swarm/templates/TEMPLATE_TASK_RICERCA_TECNICA.md`
- `.swarm/templates/TEMPLATE_TASK_IMPLEMENTAZIONE.md`
- `.swarm/templates/TEMPLATE_TASK_BUG_FIX.md`
- `.swarm/templates/TEMPLATE_TASK_CODE_REVIEW.md`
- `.swarm/templates/TEMPLATE_TASK_DOCUMENTAZIONE.md`
- `.swarm/templates/TEMPLATE_TASK_HARDTEST.md`

---

## 🚀 PROSSIMI STEP

Dopo setup:
1. **Familiarizza** - Lancia 2-3 task test
2. **Studia pattern** - Leggi GUIDA_BEST_PRACTICES
3. **Usa intensamente** - Delega task reali
4. **Impara workflow** - Ogni progetto è leggermente diverso

**Il sistema migliora con l'uso!** 💙

---

**Setup completato:** [DATA]
**Progetto:** [NOME_PROGETTO]
**Rating:** 10/10 - Pronto per uso intenso! 🎉

---

*Tempo totale: 5 minuti. Ritorno investimento: INFINITO!* ✨
