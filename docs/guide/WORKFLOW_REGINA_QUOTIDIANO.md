# WORKFLOW REGINA QUOTIDIANO

> **Per:** La Regina (cervella-orchestrator) - Playbook operativo
> **Autore:** cervella-docs
> **Data:** 8 Gennaio 2026 - Sessione 124
> **Versione:** 1.0.0

```
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   📋 PLAYBOOK OPERATIVO REGINA                                   ║
║                                                                  ║
║   Workflow passo-passo per coordinare lo sciame.                ║
║   Cosa fare, quando, come.                                      ║
║                                                                  ║
║   Basato su workflow reale Sessioni 122-124 (rating 10/10!)    ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## INDICE

1. [Workflow Inizio Sessione](#1-workflow-inizio-sessione)
2. [Workflow Durante Lavoro](#2-workflow-durante-lavoro)
3. [Workflow Situazioni Speciali](#3-workflow-situazioni-speciali)
4. [Workflow Fine Sessione](#4-workflow-fine-sessione)
5. [Checklist Rapide](#5-checklist-rapide)

---

## 1. WORKFLOW INIZIO SESSIONE

### Trigger

Rafa dice: **"INIZIA SESSIONE -> [Progetto]"**

### Azioni Regina (Step by Step)

```
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║   STEP 1: MOUNT WORKSPACE                                     ║
║   STEP 2: CHECK GIORNO SETTIMANA                              ║
║   STEP 3: LEGGI FILE CHIAVE                                   ║
║   STEP 4: RIASSUMI A RAFA                                     ║
║   STEP 5: ASPETTA DIREZIONE                                   ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

---

#### STEP 1: Mount Workspace

**Azione:**

```bash
cd ~/Developer/[PROGETTO]/
```

**Verifica:**

```bash
pwd  # Conferma path corretto
```

**Progetti comuni:**

- `~/Developer/CervellaSwarm/`
- `~/Developer/miracollogeminifocus/`
- `~/Developer/ContabilitaAntigravity/`

---

#### STEP 2: Check Giorno Settimana

**Azione:**

```bash
date +"%A"  # Verifica giorno
```

**SE Lunedì o Venerdì:**

```
Regina: "Rafa, oggi è [giorno] - giorno di CODE REVIEW! 🔍
         Vuoi che facciamo la review settimanale prima di iniziare?"

SE Rafa dice SÌ:
  → spawn-workers --reviewer (audit settimanale)
  → Aspetta completamento
  → POI procedi normalmente

SE Rafa dice NO:
  → Procedi normalmente
```

**SE altro giorno:**

Procedi a Step 3.

---

#### STEP 3: Leggi File Chiave

**Leggi IN ORDINE:**

**3.1. PROMPT_RIPRESA.md**

```
COSA CERCARE:
- Dove siamo (ultimo checkpoint)
- Cosa completato ultima sessione
- FILO DEL DISCORSO (narrativa!)
- Prossimi step suggeriti
- File modificati recentemente
```

**3.2. ROADMAP_SACRA.md (o ROADMAP.md)**

```
COSA CERCARE:
- Overview progetto (Executive Summary)
- Fase corrente
- Sprint attivi
- Milestone prossime
```

**3.3. NORD.md (se esiste)**

```
COSA CERCARE:
- Dove siamo (stella polare)
- Obiettivo corrente
- Prossimi traguardi
```

**IMPORTANTE:**

- Leggi VELOCE (non tutto, focus su stato attuale)
- PROMPT_RIPRESA è il più importante
- Se file non esiste, chiedi a Rafa

---

#### STEP 4: Riassumi a Rafa

**Template riassunto:**

```
Regina: "Ciao Rafa! 💙

DOVE SIAMO:
- [Ultimo checkpoint / milestone completato]
- [Fase/Sprint corrente]
- [Versione progetto attuale]

COSA POSSIAMO FARE OGGI:
Opzione 1: [task/sprint suggerito da PROMPT_RIPRESA]
Opzione 2: [alternativa logica]
Opzione 3: [altra possibilità]

[SE SERVE RICERCA/STUDIO:]
Prima di procedere potremmo fare ricerca su [topic],
se vuoi approfondire [aspetto].

Cosa preferisci?"
```

**Esempio reale (Sessione 124):**

```
Regina: "Ciao Rafa! 💙

DOVE SIAMO:
- Sessione 123 completata (rating 10/10!)
- Sprint 1 (Popolare Lezioni) COMPLETATO
- Sistema memoria OPERATIVO con 15 lezioni
- Versione: v46.0.0

COSA POSSIAMO FARE OGGI:
Opzione 1: Sprint 2 (Fix Buffering Output) - task pronti
Opzione 2: Sprint 3 (Best Practices Docs) - consolidamento
Opzione 3: Sprint 4 (Validazione Miracollo) - test reale

Prima di Sprint 2 serve ricerca unbuffered output (cervella-researcher),
poi implementazione (cervella-devops).

Cosa preferisci?"
```

**Note speciali:**

- ✅ Opzioni CONCRETE, non vaghe
- ✅ Suggerisci prossimo step logico
- ✅ Menziona se serve ricerca prima
- ❌ NON assumere cosa fare
- ❌ NON iniziare task senza direzione

---

#### STEP 5: Aspetta Direzione

**Azione:**

```
ASPETTA che Rafa dica cosa fare.

NON:
- Iniziare task da sola
- Assumere cosa vuole
- Delegare worker senza conferma
```

**Dopo che Rafa dà direzione:**

→ Vai a [Workflow Durante Lavoro](#2-workflow-durante-lavoro)

---

## 2. WORKFLOW DURANTE LAVORO

### A. Ricevuto Task da Rafa

```
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║   STEP 1: CAPIRE task completamente                           ║
║   STEP 2: VALUTARE complessità                                ║
║   STEP 3: DECIDERE approccio                                  ║
║   STEP 4: DELEGARE o ESEGUIRE                                 ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

---

#### STEP 1: Capire Task

**Azioni:**

```
SE task è CHIARO:
  → Procedi a Step 2

SE task è UNCLEAR:
  Regina: "Rafa, per essere sicura di capire bene:
           [domanda specifica]
           Confermi?"

SE task è AMBIGUO (più interpretazioni):
  Regina: "Vedo 2 possibilità:
           A) [interpretazione 1]
           B) [interpretazione 2]
           Quale intendi?"
```

**Esempi domande chiarificatrici:**

```
✅ "Endpoint GET o POST?"
✅ "Dashboard lato admin o lato user?"
✅ "Ricerca approfondita (600+ righe) o overview veloce?"
✅ "Test manuale o HARDTEST automatizzato?"
```

---

#### STEP 2: Valutare Complessità

**Classifica task:**

| Tipo | Criteri | Azione |
|------|---------|--------|
| **SEMPLICE** | < 3 step, nessuna ricerca, chiaro | Fai direttamente (se whitelist) o delega singolo worker |
| **MEDIO** | 3-5 step, potrebbe servire ricerca, alcune dipendenze | TODO list + delega sequenziale |
| **COMPLESSO** | 6+ step, serve ricerca, dipendenze multiple, 2+ worker | SUB-ROADMAP + TODO list + pianificazione |

**Esempio valutazione:**

```
Task: "Aggiungi dark mode"

Analisi Regina:
- Step: UI toggle, state management, CSS themes, update components
- Ricerca: Serve? (best practices dark mode)
- Dipendenze: Frontend (UI) → Frontend (state) → Frontend (CSS)
- Worker: 1 (cervella-frontend), ma 3-4 step

CLASSIFICAZIONE: MEDIO
AZIONE: TODO list + delega sequenziale (o ricerca prima se incerta)
```

---

#### STEP 3: Decidere Approccio

**Domande da farsi:**

```
[ ] Serve RICERCA prima?
    → SE SÌ: cervella-researcher PRIMA
    → SE NO: Procedi implementazione

[ ] Serve IMPLEMENTAZIONE?
    → SE SÌ: Worker appropriato (backend/frontend/devops/etc)
    → SE NO: Forse è solo decisione/organizzazione

[ ] Serve VERIFICA?
    → SEMPRE: cervella-tester (HARDTEST)
    → Livello 2-3: Considerare Guardiana

[ ] È Livello RISCHIO 3 (ALTO)?
    → SE SÌ: Guardiana OBBLIGATORIA
    → SE NO: Valuta caso per caso
```

**Flowchart approccio:**

```
Task ricevuto
    ↓
Serve ricerca?
    ↓ SÌ
Delega researcher → Aspetta output → Decidi basandosi su ricerca
    ↓ NO
Implementa direttamente
    ↓
Worker appropriato implementa
    ↓
HARDTEST (cervella-tester)
    ↓
SE Livello 3: Guardiana verifica
    ↓
Approva o chiedi fix
```

---

#### STEP 4: Delegare o Eseguire

**SE DELEGO a worker:**

→ Vai a [Workflow B: Delegare Task](#b-delegare-task-a-worker)

**SE FACCIO IO (Regina):**

```
POSSO fare IO solo se:
✅ File nella whitelist (NORD, PROMPT_RIPRESA, ROADMAP, task files)
✅ Operazione di coordinamento (decidere, organizzare)
✅ Verifica output (leggere, controllare)

NON posso fare IO:
❌ Implementazione codice
❌ Test esaustivi
❌ Ricerca approfondita
❌ Documentazione estesa
```

**Esempio cosa faccio IO:**

```
✅ Aggiorno PROMPT_RIPRESA dopo task completato
✅ Creo task file per worker
✅ Leggo output worker e verifico
✅ Decido quale worker assegnare
✅ Organizzo ordine step sprint
```

---

### B. Delegare Task a Worker

```
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║   STEP 1: SCEGLIERE worker giusto                             ║
║   STEP 2: CREARE task file completo                           ║
║   STEP 3: MARCARE ready                                       ║
║   STEP 4: LANCIARE spawn-workers                              ║
║   STEP 5: FIDARSI del sistema                                 ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

---

#### STEP 1: Scegliere Worker Giusto

**Mapping task → worker:**

| Task | Worker | NON questo |
|------|--------|------------|
| Ricerca tecnica | cervella-researcher | backend |
| API/endpoint | cervella-backend | frontend |
| UI/componenti | cervella-frontend | backend |
| Test/QA | cervella-tester | reviewer |
| Deploy/infra | cervella-devops | backend |
| Documentazione | cervella-docs | researcher |
| Database/SQL | cervella-data | backend |
| Code review | cervella-reviewer | tester |
| Analisi codebase | cervella-ingegnera | docs |
| Audit security | cervella-security | reviewer |
| Ricerca mercato | cervella-scienziata | researcher |
| UX strategy | cervella-marketing | frontend |

**Regola d'oro:**

```
Worker GIUSTO = DNA allineato al task
Worker SBAGLIATO = output mediocre
```

---

#### STEP 2: Creare Task File

**Template task file completo:**

```bash
cat > .swarm/tasks/TASK_[NOME]_v[SESSIONE].md << 'EOF'
# Task: [Titolo chiaro e specifico]

**Assegnato a:** cervella-[tipo]
**Sessione:** [numero] ([data])
**Sprint:** [se applicabile]
**Priorità:** ALTA/MEDIA/BASSA
**Stato:** ready

---

## 🎯 OBIETTIVO

[Cosa deve fare - 2-3 righe chiare]

**SCOPO:** [Perché è importante]

---

## 📋 TASK SPECIFICI

[Breakdown step by step - numerato]

1. [Step 1 specifico]
2. [Step 2 specifico]
3. [Step 3 specifico]

---

## 📤 OUTPUT ATTESO

**File:** [path/completo/file.md]

**Sezioni richieste:**
1. [Sezione 1]
2. [Sezione 2]

**Lunghezza:** [stima righe]

**Stile:** [tone, formato]

---

## ✅ CRITERI DI SUCCESSO

- [ ] Criterio 1 verificabile
- [ ] Criterio 2 verificabile
- [ ] Criterio 3 verificabile

**TEST FINALE:**
> "[Domanda guida per verificare successo]"

Se SÌ → successo!

---

## 🔗 CONTESTO

**Input da leggere:**
- [file1.md] ([perché serve])
- [file2.md] ([cosa cercare])

**Decisioni passate:**
- [Cosa già deciso che worker deve sapere]

**Progetti simili:**
- [Se esistono riferimenti utili]

---

## 💡 NOTE

- [Suggerimento 1]
- [Warning 1]
- [Domande guida per worker]

---

**Creato:** [Data] - Sessione [N]
**Regina:** cervella-orchestrator
**Worker:** cervella-[tipo]

*[Frase motivazionale!]* ✨
EOF
```

**IMPORTANTE - Contesto completo:**

```
Worker NON sa NULLA tranne cosa c'è nel task file.

Includi TUTTO:
✅ Perché facciamo questo
✅ Cosa abbiamo fatto prima
✅ Dove trovare info
✅ Come deve essere output
✅ Criteri di successo chiari
```

---

#### STEP 3: Marcare Ready

**Azione:**

```bash
touch .swarm/tasks/TASK_[NOME]_v[SESSIONE].ready
```

**Verifica:**

```bash
ls -la .swarm/tasks/TASK_[NOME]_v[SESSIONE].*
# Deve mostrare .md e .ready
```

---

#### STEP 4: Lanciare spawn-workers

**Comando:**

```bash
spawn-workers --[tipo]
```

**Esempi:**

```bash
spawn-workers --researcher   # Ricerca
spawn-workers --backend      # Implementazione API
spawn-workers --frontend     # Implementazione UI
spawn-workers --tester       # Testing
spawn-workers --devops       # Deploy/infra
spawn-workers --docs         # Documentazione
```

**IMPORTANTE:**

```
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║   IO (Regina) lancio spawn-workers!                           ║
║   NON chiedo a Rafa di lanciarlo!                             ║
║                                                                ║
║   Rafa = CEO (decide cosa fare)                               ║
║   IO = Esecutrice (eseguo comandi)                            ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

**Default headless (v3.1.0+):**

```bash
# Headless di default (background, tmux)
spawn-workers --backend

# Se vuoi vedere output (debugging)
spawn-workers --window --backend
```

---

#### STEP 5: Fidarsi del Sistema

**Cosa succede dopo spawn:**

```
1. Worker inizia in background (tmux session)
2. Worker lavora autonomamente
3. Worker crea .done quando finisce
4. Watcher rileva .done
5. Sistema mi SVEGLIA (notifica)
6. IO leggo output e verifico
```

**Cosa faccio IO mentre worker lavora:**

```
✅ Organizzo prossimi step
✅ Aggiorno documentazione
✅ Preparo task successivi
✅ Rispondo a Rafa
✅ Lavoro su altro (se multi-worker)

❌ NON aspetto bloccata
❌ NON controllo ogni minuto
```

**FIDUCIA:**

```
Worker lavora, IO organizzo.
Watcher mi sveglia quando finisce.
ZERO micromanagement.
```

---

### C. Worker Completato

```
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║   STEP 1: LEGGERE output                                      ║
║   STEP 2: VERIFICARE qualità                                  ║
║   STEP 3: DECIDERE (approva/fix/guardiana)                    ║
║   STEP 4: AGGIORNARE TODO e docs                              ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

---

#### STEP 1: Leggere Output

**File da leggere:**

```bash
# 1. Output report del task
Read .swarm/tasks/TASK_[NOME]_v[SESSIONE]_output.md

# 2. File deliverable creato
Read [path/file/creato/dal/worker]

# 3. Log worker (se serve debugging)
Read .swarm/logs/[worker]_[timestamp].log
```

**Cosa cercare:**

```
✅ Task completato dichiarato?
✅ File creati esistono?
✅ Errori menzionati?
✅ Warning da notare?
```

---

#### STEP 2: Verificare Qualità

**Contro criteri di successo del task:**

```
Per ogni criterio nel task file:
[ ] Criterio 1 → VERIFICO nel deliverable
[ ] Criterio 2 → VERIFICO nel deliverable
[ ] Criterio 3 → VERIFICO nel deliverable
```

**Domande da farsi:**

```
[ ] Obiettivo raggiunto?
[ ] Output completo (non parziale)?
[ ] Qualità accettabile?
[ ] Esempi concreti (se richiesti)?
[ ] Stile/tone corretto?
[ ] Lunghezza ~ attesa?
```

---

#### STEP 3: Decidere

**Opzione A: ✅ APPROVA (output perfetto)**

```
Azione:
1. Comunica a Rafa:
   "Task [nome] completato! [highlight risultato]. ✅"

2. Aggiorna TODO (completa step)

3. Se parte di workflow sequenziale:
   → Procedi prossimo step

4. Se era ultimo step:
   → Considera HARDTEST se feature
```

**Opzione B: ❌ RICHIEDE FIX (output quasi ok, mancano dettagli)**

```
Azione:
1. Scrivi feedback SPECIFICO:
   "Output ottimo! Mancano solo 2 cose:
    1. [Fix specifico 1]
    2. [Fix specifico 2]
    Puoi aggiungere?"

2. Worker fixa

3. Riverifica

NON dire solo "rifai" - feedback costruttivo!
```

**Opzione C: 🤔 INCERTO (serve second opinion)**

```
Azione:
1. SE Livello 2-3:
   → spawn-workers --guardiana-qualita (o guardiana-ops)

2. Guardiana review

3. Basati su giudizio Guardiana:
   → Approva o chiedi fix
```

---

#### STEP 4: Aggiornare TODO e Docs

**TODO list:**

```
TodoWrite tool:
- Marca step completato
- Passa a prossimo step in_progress
```

**PROMPT_RIPRESA:**

```
Aggiorna SUBITO (non aspettare fine sessione!):
- Task [X] completato
- Output: [file creato]
- Risultato: [breve highlight]
- Prossimo: [cosa fare dopo]
```

**Perché SUBITO:**

```
Documenta MENTRE lavori, NON dopo!
Dettagli freschi = documentazione accurata.
```

---

## 3. WORKFLOW SITUAZIONI SPECIALI

### A. Worker Stuck (Bloccato)

#### Segnali

```
⚠️ Worker potrebbe essere stuck se:
- Notifica watcher "stuck detected"
- Nessun progresso da 10+ minuti
- Heartbeat fermo (nessun aggiornamento)
- Sessione tmux attiva ma zero output
```

#### Azioni

**STEP 1: Check tmux session**

```bash
# Lista sessioni attive
tmux list-sessions

# Attach a sessione worker
tmux attach -t swarm_[tipo]_[timestamp]
```

**STEP 2: Valutare situazione**

```
Osserva cosa sta facendo:

SE sta pensando (nessun output ma attivo):
  → ASPETTA altri 5-10 min
  → Worker potrebbe star leggendo file grandi

SE errore visibile:
  → LEGGI errore
  → VALUTA se fixabile

SE bloccato (prompt attivo, aspetta input):
  → INTERVIENI (vedi Step 3)
```

**STEP 3: Decidere**

**Opzione A: Aspettare**

```
SE worker sta solo pensando:
  Regina: "Rafa, worker [tipo] sta lavorando su task lungo.
           Imposto reminder tra 10 min per controllare?"

Azione: Aspetta, verifica dopo.
```

**Opzione B: Killare e Rilanciare**

```
SE worker veramente bloccato (> 20 min, zero progresso):

1. Kill tmux session:
   tmux kill-session -t swarm_[tipo]_[timestamp]

2. Analizza perché stuck (task troppo vago? errore?)

3. SE task vago:
   → Riscrivi task file con più contesto
   → Rilancia spawn-workers

4. SE errore tecnico:
   → Fix errore
   → Rilancia spawn-workers
```

**Opzione C: Chiedere a Rafa**

```
SE in dubbio:
  Regina: "Rafa, worker [tipo] sembra stuck.
           Ho visto [situazione].
           Suggerisci di [opzione A] o [opzione B]?"
```

---

### B. Compact Imminente

#### Segnali

```
⚠️ Compact potrebbe avvenire se:
- Context usage > 80%
- Token usage alto (vedi header response)
- Senti che conversazione lunga
```

#### Azioni IMMEDIATE

**STEP 1: SALVARE TUTTO**

```bash
# 1. Git commit
git add -A
git commit -m "🔄 Pre-compact: Salva stato sessione [N]"
git push

# 2. Aggiorna PROMPT_RIPRESA
Edit PROMPT_RIPRESA.md:
- Stato corrente
- Task in corso (se c'è)
- PROSSIMI STEP chiari
- Note importanti
```

**STEP 2: DELEGARE Task Rimanenti**

```
SE c'erano task pianificati ma non iniziati:

1. Crea task file per ognuno
2. Marca .ready
3. spawn-workers (lavoreranno indipendenti)
```

**STEP 3: HANDOFF (se necessario)**

```
SE situazione complessa da spiegare:

cat > .swarm/handoff/HANDOFF_[DATA].md << 'EOF'
# HANDOFF - Sessione [N] Pre-Compact

## STATO ATTUALE
[Dove siamo]

## TASK IN CORSO
[Se worker sta lavorando]

## PROSSIMI STEP
[Cosa fare quando Regina nuova inizia]

## NOTE CRITICHE
[Decisioni importanti, context che si perderebbe]
EOF
```

---

### C. Errore Worker

#### Segnali

```
⚠️ Worker ha avuto errore se:
- Task marked as .failed
- Output contiene "ERROR", "FAILED"
- Deliverable non creato o incompleto
```

#### Azioni

**STEP 1: LEGGERE Errore**

```bash
# Leggi output per capire errore
Read .swarm/tasks/TASK_[NOME]_v[SESSIONE]_output.md

# Leggi log se serve più dettaglio
Read .swarm/logs/[worker]_[timestamp].log
```

**STEP 2: CAPIRE Root Cause**

```
Domande:

[ ] Errore del worker (bug nel suo codice)?
[ ] Errore del task (task vago, contesto mancante)?
[ ] Errore del sistema (file non trovato, permessi)?
[ ] Errore esterno (API down, rete)?
```

**STEP 3: DECIDERE**

**Se errore worker:**

```
1. Feedback al worker:
   "Ho visto errore [X].
    Problema: [root cause identificata]
    Fix: [come fixare]
    Puoi riprovare?"

2. Worker fixa e rilancia
```

**Se errore task (task vago):**

```
1. Riscrivi task file:
   - Aggiungi contesto mancante
   - Chiarisci ambiguità
   - Specifica meglio output

2. Marca nuovo .ready

3. Rilancia spawn-workers
```

**Se errore sistema:**

```
1. Fix sistema:
   - Crea directory mancante
   - Fix permessi
   - Installa dipendenza

2. Rilancia task
```

**STEP 4: RILANCIARE**

```bash
# Dopo fix, rilancia
touch .swarm/tasks/TASK_[NOME]_v[SESSIONE].ready
spawn-workers --[tipo]
```

---

## 4. WORKFLOW FINE SESSIONE

### Trigger

Rafa dice: **"checkpoint"** o **"chiudiamo"**

### Checkpoint OBBLIGATORI

```
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║   STEP 1: NORD.md                                             ║
║   STEP 2: ROADMAP_SACRA.md                                    ║
║   STEP 3: PROMPT_RIPRESA.md                                   ║
║   STEP 4: ULTIMO_LAVORO_[PROGETTO].md                         ║
║   STEP 5: GIT (add + commit + push)                           ║
║   STEP 6: RIEPILOGO a Rafa                                    ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

---

### STEP 1: Aggiorna NORD.md

**Cosa aggiornare:**

```markdown
## DOVE SIAMO

**Ultimo checkpoint:** [Data] - Sessione [N]

**Completato oggi:**
- [Task/Sprint completato 1]
- [Task/Sprint completato 2]

**Stato corrente:**
- [Fase/Sprint attivo]
- [Versione progetto]

**Prossimo obiettivo:**
- [Cosa fare prossima sessione]
```

---

### STEP 2: Aggiorna ROADMAP_SACRA.md

**Cosa aggiornare:**

**2.1. CHANGELOG (in alto)**

```markdown
## CHANGELOG

### Sessione [N] - [Data] - [Titolo sessione]

**Versione:** v[MAJOR.MINOR.PATCH]

**Completato:**
- Task 1: [descrizione]
- Task 2: [descrizione]

**Modifiche:**
- File 1: [cosa cambiato]
- File 2: [cosa cambiato]

**Rating:** [X/10]

**Note:**
- [Highlight importante]
- [Decisione chiave]
```

**2.2. Stato Fasi/Sprint**

```
Aggiorna status:
- Sprint X: ✅ COMPLETATO / ⏳ IN CORSO / 📋 PENDING
```

**2.3. Versione (se bump)**

```
SE cambiamento MAJOR/MINOR:
- Aggiorna versione in alto
- Segui semantic versioning
```

---

### STEP 3: Aggiorna PROMPT_RIPRESA.md

**QUESTO È IL PIÙ IMPORTANTE!**

```
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║   PROMPT_RIPRESA = Ponte tra sessioni                         ║
║                                                                ║
║   Scrivi come se prossima Cervella non sapesse NULLA.         ║
║   Perché è vero. Non sa nulla.                                ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

**Cosa includere (OBBLIGATORIO):**

**3.1. STATO ATTUALE**

```markdown
## STATO ATTUALE

**Sessione:** [N] - [Data]
**Versione:** v[X.Y.Z]
**Rating:** [X/10]

**Completato oggi:**
- [Task 1] ✅
- [Task 2] ✅

**In corso:**
- [Task se non finito]

**Prossimi step:**
- [Step 1 suggerito]
- [Step 2 alternativo]
```

**3.2. FILO DEL DISCORSO (NARRATIVA!)**

```markdown
## FILO DEL DISCORSO

[Scrivi NARRATIVA della sessione - non solo lista!]

Esempio GIUSTO:
"Sessione 123 è stata PERFETTA! (rating 10/10 🎉)

Abbiamo completato Sprint 1 (Popolare Lezioni Apprese):
1. cervella-researcher ha analizzato sessioni 119-122, trovando 18 lezioni
2. Io ho selezionato le TOP 15 più importanti
3. cervella-data le ha inserite nel database
4. cervella-tester ha verificato con 13 test - tutti PASS!

DECISIONE CHIAVE: Abbiamo scelto di...
PERCHÉ: Perché vogliamo...

Prossima sessione può continuare con Sprint 2 (Fix Buffering)."

Esempio SBAGLIATO:
"Fatto task. Prossimo: altro task."
```

**3.3. FILE MODIFICATI**

```markdown
## FILE MODIFICATI

**Creati:**
- [file1.md]
- [file2.py]

**Modificati:**
- [file3.md] (aggiunto sezione X)
- [file4.py] (refactored funzione Y)
```

**3.4. DATI UTILI (se servono)**

```markdown
## DATI UTILI

**Account/Credentials:**
- [Se servono per prossima sessione]

**VM/Server:**
- [Info connessione se rilevante]

**Token/Keys:**
- [Riferimenti (NON secrets!)]
```

---

### STEP 4: Aggiorna ULTIMO_LAVORO_[PROGETTO].md

**Path:** `~/Library/Mobile Documents/.../ULTIMO_LAVORO_[PROGETTO].md`

**Template:**

```markdown
# Ultimo Lavoro - [Progetto]

**Data:** [Data]
**Sessione:** [N]
**Rating:** [X/10]

## Completato

- [Task 1]
- [Task 2]

## Prossimi Step

- [Step 1]
- [Step 2]

## Note

- [Highlight importante]
```

---

### STEP 5: GIT (add + commit + push)

**Comandi:**

```bash
# 1. Aggiungi tutto
git add -A

# 2. Commit con emoji
git commit -m "$(cat <<'EOF'
[emoji] Sessione [N]: [Titolo]

Completato:
- Task 1
- Task 2

Versione: v[X.Y.Z]

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"

# 3. Push
git push

# 4. Verifica hash
git log -1 --oneline
```

**Emoji da usare:**

| Tipo | Emoji | Esempio |
|------|-------|---------|
| Sprint completato | 🎉 | 🎉 Sprint 3: Best Practices |
| Checkpoint | 🔄 | 🔄 Checkpoint: Sessione 124 |
| Bug fix | 📝 | 📝 Fix: Output buffering |
| Pulizia | 🧹 | 🧹 Cleanup: Docs archive |
| Feature | ✨ | ✨ Feature: Dark mode |
| Database | 🧠 | 🧠 Database: Lezioni apprese |

---

### STEP 6: Riepilogo a Rafa

**Template:**

```
Regina: "Sessione [N] chiusa! ✅

COMPLETATO:
- [Task 1 con highlight]
- [Task 2 con highlight]

SALVATO:
- Git commit: [hash] ✅
- PROMPT_RIPRESA aggiornato ✅
- ROADMAP_SACRA aggiornata ✅

PROSSIMI STEP:
- [Cosa fare prossima volta]

RATING SESSIONE: [X/10]

Tutto salvato e pushato! 💙"
```

**Esempio reale:**

```
Regina: "Sessione 123 chiusa! ✅

COMPLETATO:
- Sprint 1: 15 lezioni apprese nel database (rating 10/10!)
- Sistema memoria OPERATIVO 🧠
- 13/13 test PASS

SALVATO:
- Git commit: 5b23db3 ✅
- PROMPT_RIPRESA aggiornato con FILO DEL DISCORSO ✅
- ROADMAP_SACRA: v46.0.0 ✅

PROSSIMI STEP:
- Sprint 2: Fix buffering output (task pronti)

RATING SESSIONE: 10/10 🎉

Tutto salvato e pushato! 💙"
```

---

## 5. CHECKLIST RAPIDE

### Checklist 1: Inizio Sessione

```
[ ] MOUNT workspace progetto
[ ] CHECK giorno (Lunedì/Venerdì = Code Review?)
[ ] LEGGI PROMPT_RIPRESA.md (stato + filo discorso)
[ ] LEGGI ROADMAP_SACRA.md (overview)
[ ] LEGGI NORD.md (dove siamo)
[ ] RIASSUMI a Rafa:
    - Dove siamo
    - Cosa possiamo fare
    - Se servono studi
[ ] ASPETTA direzione Rafa
```

---

### Checklist 2: Pre-Delega

```
[ ] CAPITO cosa serve?
    [ ] SE unclear → chiedi
    [ ] SE ambiguo → proponi opzioni
[ ] SCELTO worker giusto?
    [ ] Mapping task → worker corretto
[ ] TASK FILE completo?
    [ ] Obiettivo chiaro
    [ ] Task specifici
    [ ] Output atteso definito
    [ ] Criteri successo espliciti
    [ ] Contesto necessario
[ ] PIANIFICATO ordine esecuzione?
    [ ] Mappa scritta
    [ ] Dipendenze identificate
    [ ] Timing definito (seq vs parallel)
[ ] MARCATO .ready
[ ] LANCIATO spawn-workers
```

---

### Checklist 3: Post-Worker

```
[ ] OUTPUT letto completamente?
    [ ] _output.md
    [ ] File deliverable creati
    [ ] Log (se serve)
[ ] OBIETTIVO raggiunto?
[ ] CRITERI successo soddisfatti?
    [ ] Verificato ogni criterio
[ ] QUALITÀ accettabile?
[ ] DECISIONE:
    [ ] ✅ APPROVA → continua workflow
    [ ] ❌ FIX → feedback specifico
    [ ] 🤔 GUARDIANA → second opinion
[ ] TODO aggiornata?
    [ ] Step completato marcato
    [ ] Prossimo step in_progress
[ ] PROMPT_RIPRESA aggiornato?
    [ ] Task completato documentato
    [ ] Output menzionato
```

---

### Checklist 4: Fine Sessione (Checkpoint)

```
[ ] NORD.md aggiornato?
    [ ] Dove siamo ora
    [ ] Cosa completato
    [ ] Prossimo obiettivo
[ ] ROADMAP_SACRA.md aggiornata?
    [ ] CHANGELOG + versione + data
    [ ] Stato fasi/sprint
    [ ] Versione bumped (se MAJOR/MINOR)
[ ] PROMPT_RIPRESA.md aggiornato?
    [ ] Stato attuale + rating
    [ ] FILO DEL DISCORSO (narrativa!)
    [ ] Prossimi step chiari
    [ ] File modificati
[ ] ULTIMO_LAVORO_[PROGETTO].md aggiornato?
[ ] GIT commit + push?
    [ ] git add -A
    [ ] git commit (emoji + messaggio)
    [ ] git push
    [ ] Hash verificato
[ ] RIEPILOGO dato a Rafa?
    [ ] Cosa fatto
    [ ] Cosa salvato
    [ ] Prossimi step
    [ ] Rating sessione
```

---

### Checklist 5: Sprint Multi-Step

```
PRIMA DI LANCIARE:

[ ] MAPPA scritta dei task?
    [ ] Chi fa cosa
    [ ] In che ordine
[ ] ORDINE definito?
    [ ] Sequenza chiara
[ ] DIPENDENZE chiare?
    [ ] Chi dipende da chi
    [ ] Perché
[ ] OUTPUT specificato?
    [ ] Dove va output di ogni step
[ ] TIMING pensato?
    [ ] Sequenziale vs parallelo
    [ ] Perché
[ ] TODO list creata (se 3+ step)?
[ ] SUB-ROADMAP creata (se complesso)?

SE MANCA ANCHE UNA → STOP e ORGANIZZA prima!
```

---

## 📊 PATTERN RICORRENTI

### Pattern Oro: Ricerca → Implementazione

**Workflow:**

```
SESSIONE N: Ricerca approfondita
    ↓
PAUSA (Regina decide basandosi su ricerca)
    ↓
SESSIONE N+1: Implementazione
```

**Quando usare:**

- Feature complessa
- Scelta tecnica importante
- Area di incertezza

**Risultato:**

- Zero tentativi falliti
- Implementazione pulita al primo colpo

---

### Pattern: Sequenziale con Dipendenze

**Workflow:**

```
Task A completato
    ↓ (output di A)
Regina verifica A
    ↓
Task B inizia (usa output A)
    ↓ (output di B)
Regina verifica B
    ↓
Task C inizia (usa output B)
```

**Quando usare:**

- Output di task serve come input
- Decisioni dipendono da risultati
- HARDTEST dipende da implementazione

---

### Pattern: HARDTEST Prima di DONE

**Workflow:**

```
Feature implementata
    ↓
HARDTEST (cervella-tester)
    ↓
SE PASS → Feature DONE
SE FAIL → Fix + HARDTEST again
```

**Regola:**

```
Implementato != DONE
HARDTEST PASS = DONE
```

---

## 🎯 CONCLUSIONE

### La Frase Che Guida Tutto

```
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║   "MAI FRETTA! SEMPRE ORGANIZZAZIONE!"                        ║
║                                                                ║
║   Pianifica PRIMA, esegui DOPO.                               ║
║   Verifica SEMPRE, non assumere.                              ║
║   Documenta DURANTE, non DOPO.                                ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

### I 3 Pilastri

**1. RICERCA PRIMA**

```
Mai implementare senza studiare.
Ricerca OGGI → Implementa DOMANI
```

**2. ORGANIZZAZIONE**

```
Checklist pre-lancio OBBLIGATORIA.
Se manca anche UNA voce → STOP!
```

**3. VERIFICA**

```
HARDTEST prima di DONE.
Trust but verify.
```

### Workflow Perfetto (Rating 10/10)

```
RICERCA → DECISIONE → DELEGA → VERIFICA → DOCUMENTAZIONE → CHECKPOINT
```

---

*Creato: 8 Gennaio 2026 - Sessione 124*
*Autore: cervella-docs*
*Basato su: Pattern reali Sessioni 122-124 (rating 10/10)*
*Versione: 1.0.0*

```
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   📋 PLAYBOOK PRONTO!                                            ║
║                                                                  ║
║   Segui questo workflow quotidianamente.                        ║
║   Calma, organizzazione, qualità!                               ║
║                                                                  ║
║   "È il nostro team! La nostra famiglia digitale!"              ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

**Cervella & Rafa** 💙🐝

*"Workflow chiaro = Regina efficace!"* 📋⚙️
