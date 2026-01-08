# Task: Workflow Regina Quotidiano

**Assegnato a:** cervella-docs
**Sessione:** 124 (8 Gennaio 2026)
**Sprint:** 3 - Best Practices Documentation
**Priorità:** ALTA
**Stato:** waiting (dipende da Task 3.1 e 3.2)

---

## 🎯 OBIETTIVO

Creare guida **passo-passo** per workflow quotidiano della Regina.

**SCOPO:** Playbook operativo che la Regina segue ogni giorno.

---

## 📋 TASK SPECIFICI

### 1. Workflow Inizio Sessione

**Trigger:** Rafa dice "INIZIA SESSIONE -> [Progetto]"

**Azioni Regina:**
```markdown
1. 📂 MOUNT workspace progetto
2. 📅 CHECK giorno settimana
   - SE lunedì o venerdì → proporre Code Review
3. 📖 LEGGI file chiave:
   - PROMPT_RIPRESA.md (stato + filo discorso)
   - ROADMAP_SACRA.md (overview)
   - NORD.md (dove siamo)
4. 📊 RIASSUMI a Rafa:
   - Dove siamo
   - Cosa possiamo fare
   - Se servono studi
5. ⏳ ASPETTA direzione Rafa
```

**Note speciali:**
- NON assumere cosa fare
- NON iniziare task senza direzione
- SEMPRE riassunto chiaro
- Opzioni concrete, non vaghe

---

### 2. Workflow Durante Lavoro

#### A. Ricevuto Task da Rafa

**Azioni:**
```markdown
1. CAPIRE task completamente
   - Se unclear → chiedere
   - Se ambiguo → proporre opzioni
2. VALUTARE complessità
   - Semplice (< 3 step) → fare direttamente
   - Complesso → TODO list + pianificazione
3. DECIDERE approccio
   - Serve ricerca prima? → cervella-researcher
   - Serve implementazione? → worker appropriate
   - Serve verifica? → considerare Guardiana
4. DELEGARE o ESEGUIRE
   - Se delego → spawn-workers
   - Se faccio io → Read/Edit (solo whitelist!)
```

#### B. Delegare Task a Worker

**Azioni:**
```markdown
1. SCEGLIERE worker giusto
   - Backend → API, database
   - Frontend → UI, components
   - Tester → testing, validation
   - Docs → documentation
   - etc.
2. CREARE task file (.swarm/tasks/)
   - Obiettivo chiaro
   - Contesto completo
   - Output atteso definito
   - Criteri successo espliciti
3. MARCARE ready
   - touch TASK_*.ready
4. LANCIARE worker
   - spawn-workers --[tipo]
   - NON Task tool!
5. FIDARSI del sistema
   - Worker lavora
   - Watcher mi sveglia
   - Io posso organizzare prossimi step
```

#### C. Worker Completato

**Azioni:**
```markdown
1. LEGGERE output
   - File _output.md
   - File deliverable creati
2. VERIFICARE qualità
   - Obiettivo raggiunto?
   - Criteri successo soddisfatti?
3. DECIDERE
   - ✅ APPROVA → continua workflow
   - ❌ RICHIEDE FIX → feedback a worker
   - 🤔 INCERTO → Guardiana verifica
4. AGGIORNARE TODO
   - Marca completato
   - Passa a prossimo
```

---

### 3. Workflow Situazioni Speciali

#### A. Worker Stuck

**Segnali:**
- Notifica watcher "stuck detected"
- Nessun progresso da 10+ minuti
- Sessione tmux attiva ma niente output

**Azioni:**
```markdown
1. CHECK tmux session
   - tmux attach -t swarm_[tipo]_*
2. VALUTARE situazione
   - Sta pensando? → aspetta
   - Errore? → leggi errore
   - Bloccato? → intervieni
3. DECIDERE
   - Aspettare? → imposta reminder
   - Killare e rilanciare? → se bloccato
   - Chiedere a Rafa? → se dubbi
```

#### B. Compact Imminente

**Segnali:**
- Context > 80%
- Token usage alto
- Sento che compatta presto

**Azioni:**
```markdown
1. SALVARE SUBITO
   - Git commit tutto
   - Aggiornare PROMPT_RIPRESA
   - Note prossimi step
2. DELEGARE task rimanenti
   - spawn-workers per continuare
3. HANDOFF se necessario
   - File .swarm/handoff/
```

#### C. Errore Worker

**Segnali:**
- Task failed
- Output con errori
- Risultato inaspettato

**Azioni:**
```markdown
1. LEGGERE errore
   - Capire root cause
2. DECIDERE
   - Errore worker? → feedback chiaro
   - Errore task? → riscrivere task
   - Problema sistema? → fix sistema
3. RILANCIARE
   - Dopo fix, riprova
```

---

### 4. Workflow Fine Sessione

#### A. Trigger: "checkpoint" / "chiudiamo"

**Azioni:**
```markdown
1. 📍 AGGIORNA NORD.md
   - Dove siamo ora
   - Cosa completato oggi
   - Prossimo obiettivo
2. 🗺️ AGGIORNA ROADMAP_SACRA.md
   - CHANGELOG + versione + data
   - Stato fasi
3. 📝 AGGIORNA PROMPT_RIPRESA.md
   - Stato attuale + rating
   - FILO DEL DISCORSO (narrativa!)
   - Prossimi step chiari
   - File modificati
4. 📂 AGGIORNA ULTIMO_LAVORO_[PROGETTO].md
5. 💾 GIT
   - git add -A
   - git commit -m "[emoji] Descrizione"
   - git push
6. ✅ RIEPILOGO a Rafa
   - Cosa fatto
   - Cosa salvato
   - Prossimi step
```

**IMPORTANTE PROMPT_RIPRESA:**
- Scrivi FILO DEL DISCORSO (non solo facts!)
- Spiega PERCHÉ decisioni prese
- Contesto COMPLETO per prossima Cervella
- Rating onesto (X/10)

---

### 5. Checklist Rapide

#### Checklist Pre-Delega
```
[ ] Ho capito cosa serve?
[ ] Ho scelto worker giusto?
[ ] Task file è chiaro e completo?
[ ] Output atteso definito?
[ ] Criteri successo espliciti?
```

#### Checklist Post-Worker
```
[ ] Output letto completamente?
[ ] Obiettivo raggiunto?
[ ] Qualità accettabile?
[ ] TODO aggiornata?
[ ] Prossimo step chiaro?
```

#### Checklist Fine Sessione
```
[ ] NORD aggiornato?
[ ] ROADMAP aggiornata?
[ ] PROMPT_RIPRESA completo?
[ ] ULTIMO_LAVORO aggiornato?
[ ] Git commit + push?
[ ] Riepilogo dato a Rafa?
```

---

## 📤 OUTPUT ATTESO

**File:** `docs/guide/WORKFLOW_REGINA_QUOTIDIANO.md`

**Caratteristiche:**
- **Lunghezza:** 600-900 righe
- **Stile:** Passo-passo, actionable
- **Formato:** Checklist, flowchart, esempi
- **Tone:** Chiaro, pratico

**Sezioni:** Tutte quelle sopra (1-5)

---

## ✅ CRITERI DI SUCCESSO

- [x] Workflow inizio sessione chiaro
- [x] Workflow durante lavoro dettagliato
- [x] Situazioni speciali coperte
- [x] Workflow fine sessione completo
- [x] 3 checklist rapide incluse
- [x] Basato su workflow reale Regina
- [x] Actionable immediatamente

**TEST FINALE:**
> "Regina può seguire questo workflow e coordinare efficacemente?"

---

## 🔗 CONTESTO

**Input da leggere:**
- `docs/analisi/ANALISI_PATTERN_REGINA_v124.md`
- `docs/guide/GUIDA_BEST_PRACTICES_SWARM.md`
- `~/.claude/CLAUDE.md` (trigger sessione)
- `~/.claude/CHECKLIST_AZIONE.md` (checklist esistenti)

**Workflow reali da documentare:**
- Sessioni 122-124 (esempi recenti)
- Pattern identificati da ingegnera
- Best practices da guida

---

## 💡 NOTE

- **ASPETTA** task 3.1 e 3.2 completati!
- Workflow **reale**, non ideale teorico
- Basato su **come lavora veramente** la Regina
- **Pratico** > perfetto
- Pensa a **nuova Cervella** che non sa nulla

---

**Creato:** 8 Gennaio 2026 - Sessione 124
**Regina:** Cervella Orchestratrice
**Worker:** cervella-docs

*"Workflow chiaro = Regina efficace!"* 📋⚙️
