# STUDIO COMUNICAZIONE MULTI-FINESTRA - DEFINITIVO

> **Data:** 3 Gennaio 2026 - Sessione 70
> **Versione:** 1.0.0
> **Stato:** DOCUMENTO DEFINITIVO

---

## EXECUTIVE SUMMARY

```
+------------------------------------------------------------------+
|                                                                  |
|   QUESTO STUDIO RISPONDE ALLE 7 DOMANDE FONDAMENTALI             |
|                                                                  |
|   Consolidando:                                                  |
|   - STUDIO_MULTI_FINESTRA_COMUNICAZIONE.md (401 righe)          |
|   - GUIDA_COMPACT_PROTEZIONE.md (109 righe)                     |
|   - RICERCA_PROTEZIONE_COMPACT.md (146 righe)                   |
|   - GUIDA_COMUNICAZIONE.md (729 righe)                          |
|   - spawn-workers.sh (381 righe)                                |
|   - task_manager.py (376 righe)                                 |
|                                                                  |
|   TOTALE: 2142 righe di conoscenza consolidate!                 |
|                                                                  |
+------------------------------------------------------------------+
```

---

## LE 7 DOMANDE - RISPOSTE COMPLETE

### DOMANDA 1: Quando Regina delega, cosa DEVE sapere il worker?

**RISPOSTA COMPLETA**

Il worker riceve un file `.swarm/tasks/TASK_XXX.md` con:

```markdown
# TASK: [Descrizione breve]

## METADATA
- ID: TASK_XXX
- Assegnato a: cervella-[agent]
- Livello rischio: [1/2/3]
- Timeout: 15 minuti
- Creato: [timestamp]

## PERCHE
[Motivazione del task - IL CUORE!]

## CRITERI DI SUCCESSO
- [ ] Criterio 1
- [ ] Criterio 2
- [ ] Test passato

## FILE DA MODIFICARE
- path/to/file1.py
- path/to/file2.py

## CHI VERIFICHERA
cervella-guardiana-[quale] (Livello X)

## DETTAGLI
[Descrizione completa...]
```

**Perche funziona:**
- PERCHE dice al worker l'obiettivo finale (non solo "cosa fare")
- CRITERI danno misurabilita
- CHI VERIFICHERA mette accountability

---

### DOMANDA 2: Quando worker finisce, cosa DEVE tornare alla Regina?

**RISPOSTA COMPLETA**

Il worker scrive `.swarm/tasks/TASK_XXX_output.md`:

```markdown
# OUTPUT: TASK_XXX

## STATUS
[COMPLETATO/FALLITO]

## FILE MODIFICATI
- file1.py (creato - 150 righe)
- file2.py (modificato - +25 righe)

## COSA HO FATTO
1. Creato funzione validate_email in utils.py
2. Aggiunto endpoint POST /api/users
3. Test scritto (10/10 passati)

## COME TESTARE
python -m pytest tests/test_users.py -v

## NOTE
[Eventuali osservazioni...]

## TIMESTAMP
Completato: 2026-01-03 14:30 (durata: 8m)
```

Poi: `touch .swarm/tasks/TASK_XXX.done`

---

### DOMANDA 3: Se worker ha dubbi, come chiede?

**RISPOSTA COMPLETA** (NUOVO!)

Il worker crea `.swarm/tasks/TASK_XXX_dubbio.md`:

```markdown
# DUBBIO: TASK_XXX

## DA
cervella-backend

## STATO TASK
In lavorazione (50% completato)

## IL DUBBIO
Non sono sicuro se la funzione validate_email debba:
A) Usare regex semplice (veloce ma meno preciso)
B) Usare libreria email-validator (preciso ma dipendenza)

## CONTESTO
Il task richiede "validazione email robusta" ma non specifica
se accettiamo dipendenze esterne.

## COSA HO FATTO FINORA
- Creato struttura base utils.py
- Preparato entrambe le implementazioni
- In attesa di decisione

## PROPOSTA
Suggerisco opzione B (email-validator) perche:
- Gestisce edge cases (unicode, IDN domains)
- Mantenuta attivamente
- 2KB di overhead

## TIMESTAMP
2026-01-03 14:15
```

Poi: `touch .swarm/tasks/TASK_XXX.dubbio`

**La Regina:**
1. Vede `.dubbio` apparire
2. Legge il file
3. Risponde in `.swarm/tasks/TASK_XXX_risposta.md`
4. `touch .swarm/tasks/TASK_XXX.risposta`
5. Worker continua

---

### DOMANDA 4: Se Regina fa compact, come si riprende?

**RISPOSTA COMPLETA**

**Pattern AUTO-HANDOFF:**

```
Ogni 10-15 minuti (o quando context alto):

1. REGINA monitora il proprio context
   - Se > 150K tokens o "sento" compact vicino

2. REGINA crea HANDOFF:
   .swarm/handoff/HANDOFF_SESSION_70.md

3. Contenuto HANDOFF:
```

```markdown
# HANDOFF - Sessione 70

## STATO AL MOMENTO DEL COMPACT
- Data: 2026-01-03 15:00
- Task in corso: TASK_005, TASK_006
- Task completati oggi: TASK_001, TASK_002, TASK_003, TASK_004

## WORKER ATTIVI
- cervella-backend (finestra 2) - working su TASK_005
- cervella-tester (finestra 3) - waiting

## PROSSIMA AZIONE
1. Aspettare TASK_005.done
2. Creare TASK_007 per cervella-tester
3. Far verificare da cervella-guardiana-qualita

## DECISIONI PRESE
- Scelto pattern X per validazione
- Scartato approccio Y (vedi TASK_002_output.md)

## FILE IMPORTANTI
- ROADMAP_SACRA.md (aggiornata)
- .swarm/tasks/ (tutti i task)
- src/utils.py (nuovo!)

## NOTA PER PROSSIMA REGINA
I worker stanno lavorando INDIPENDENTEMENTE.
Non hanno bisogno di te per finire.
Quando torni, controlla .done files e continua.
```

```
4. Regina salva e fa compact (o muore)

5. RAFA apre nuova finestra

6. NUOVA REGINA:
   - Legge HANDOFF_SESSION_70.md
   - Controlla .swarm/tasks/*.done (cosa e' finito)
   - CONTINUA!
```

**Il SEGRETO:** I worker NON dipendono dalla Regina per finire!
La Regina coordina, ma il lavoro continua anche senza lei.

---

### DOMANDA 5: Se worker fa compact, cosa succede?

**RISPOSTA COMPLETA** (NUOVO!)

**Scenario:** cervella-backend sta lavorando su TASK_005 e fa compact.

**Protocollo WORKER-COMPACT:**

```
1. WORKER sente compact vicino

2. WORKER salva stato parziale:
   .swarm/tasks/TASK_005_partial.md

   Contenuto:
   - Cosa ho fatto finora (50%)
   - File modificati
   - Dove mi sono fermato
   - Come continuare

3. WORKER aggiorna flag:
   rm TASK_005.working
   touch TASK_005.interrupted

4. WORKER fa compact (o muore)

5. RAFA vede che finestra worker e' morta

6. OPZIONE A: Rafa spawna nuovo worker
   ./spawn-workers.sh --backend
   Nuovo worker vede TASK_005.interrupted
   Legge TASK_005_partial.md
   CONTINUA dal 50%!

7. OPZIONE B: Regina prende il task
   Regina vede .interrupted
   Decide: ri-assegnare o completare lei
```

**Template TASK_XXX_partial.md:**

```markdown
# PARTIAL: TASK_005

## STATUS
INTERROTTO (compact imminente)

## PROGRESSO
50% completato

## COSA HO FATTO
1. Creato struttura base
2. Implementato funzione A
3. [IN CORSO] Funzione B

## DOVE MI SONO FERMATO
File: src/api/users.py
Riga: 45
Stavo: Implementando validazione input

## COME CONTINUARE
1. Completare validazione in users.py:45
2. Aggiungere error handling
3. Scrivere test

## FILE MODIFICATI (parziali!)
- src/api/users.py (IN CORSO - non committare!)

## TIMESTAMP
Interrotto: 2026-01-03 15:30
```

---

### DOMANDA 6: Come Guardiana verifica da altra finestra?

**RISPOSTA COMPLETA**

**Flusso con Guardiana:**

```
1. WORKER completa task
   touch TASK_005.done

2. REGINA vede .done
   Crea TASK_005_review.md per Guardiana

3. REGINA:
   touch TASK_005.review_ready

4. GUARDIANA (finestra separata o Task tool):
   Vede .review_ready
   Legge TASK_005_review.md
   Verifica codice/output
   Scrive TASK_005_review_result.md

5. GUARDIANA:
   touch TASK_005.approved  (o .rejected)

6. REGINA:
   Se .approved -> merge/continua
   Se .rejected -> crea task di fix
```

**Template TASK_XXX_review.md:**

```markdown
# REVIEW REQUEST: TASK_005

## DA VERIFICARE
- Output: TASK_005_output.md
- File: src/api/users.py, src/utils.py

## PERCHE ORIGINALE
Creare endpoint validato per registrazione utenti

## CRITERI DI SUCCESSO
- [ ] Endpoint funzionante
- [ ] Validazione input robusta
- [ ] Error handling presente
- [ ] Test passati

## LIVELLO RISCHIO
2 - MEDIO (nuovo codice, no auth)

## NOTA
Verificare in particolare la validazione email.
```

**Per SPAWN Guardiane:** Vedi sezione "IMPLEMENTAZIONI MANCANTI"

---

### DOMANDA 7: Come si mantiene il MOMENTUM anche con compact?

**RISPOSTA COMPLETA**

**IL SEGRETO DEL MOMENTUM:**

```
+------------------------------------------------------------------+
|                                                                  |
|   IL MOMENTUM NON DIPENDE DA UNA SINGOLA CERVELLA!              |
|                                                                  |
|   Perche:                                                        |
|   - I WORKER lavorano INDIPENDENTEMENTE                          |
|   - I TASK sono in FILE (non in memoria)                         |
|   - I FLAG (.done, .ready) persistono                           |
|   - GIT salva tutto                                              |
|                                                                  |
|   Se Regina fa compact:                                          |
|   -> Workers continuano                                          |
|   -> Nuova Regina riprende                                       |
|   -> ZERO perdita!                                               |
|                                                                  |
|   Se Worker fa compact:                                          |
|   -> Regina vede .interrupted                                    |
|   -> Spawna nuovo worker                                         |
|   -> Continua dal partial                                        |
|   -> ZERO perdita!                                               |
|                                                                  |
+------------------------------------------------------------------+
```

**Checklist Anti-Perdita:**

1. **Ogni 15 minuti:** git add + commit (automatico via hook?)
2. **Prima di task lungo:** HANDOFF preventivo
3. **Worker sente compact:** Salva partial
4. **Regina sente compact:** Crea HANDOFF

**Pattern "Catena Ininterrotta":**

```
Regina 1 -> compact -> HANDOFF -> Regina 2 (continua)
                                     |
Worker 1 (continua) <----------------+
                                     |
                              (zero interruzione!)
```

---

## IMPLEMENTAZIONI MANCANTI

### 1. Template DUBBI (gia definito sopra)

File: `.swarm/tasks/TASK_XXX_dubbio.md`
Flag: `.dubbio` / `.risposta`

**Azione:** Aggiungere a TEMPLATE_TASK come sezione opzionale.

### 2. Spawn Guardiane

Attualmente `spawn-workers.sh` ha solo worker:
- backend, frontend, tester, docs, reviewer, devops, researcher, data, security

**Mancano:**
- guardiana-qualita
- guardiana-ops
- guardiana-ricerca

**Azione:** Aggiornare spawn-workers.sh con:

```bash
--guardiana-qualita
--guardiana-ops
--guardiana-ricerca
```

### 3. Protocollo Worker Compact (gia definito sopra)

File: `.swarm/tasks/TASK_XXX_partial.md`
Flag: `.interrupted`

**Azione:** Documentare in SWARM_RULES.md

---

## ARCHITETTURA FINALE

```
                    ┌─────────────────────────────────────┐
                    │      FINESTRA 1: REGINA             │
                    │  Coordina, crea task, monitora      │
                    │  Se compact: HANDOFF -> nuova Regina│
                    └─────────────────────────────────────┘
                                      │
        ┌──────────────┬──────────────┼──────────────┬──────────────┐
        ▼              ▼              ▼              ▼              ▼
   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐
   │FINESTRA │   │FINESTRA │   │FINESTRA │   │FINESTRA │   │FINESTRA │
   │    2    │   │    3    │   │    4    │   │    5    │   │    6    │
   │ BACKEND │   │FRONTEND │   │ TESTER  │   │GUARDIANA│   │  DOCS   │
   └─────────┘   └─────────┘   └─────────┘   └─────────┘   └─────────┘
        │              │              │              │              │
        └──────────────┴──────────────┴──────────────┴──────────────┘
                                      │
                              ┌───────────────┐
                              │   .swarm/     │
                              │   tasks/      │
                              │   handoff/    │
                              │   status/     │
                              └───────────────┘
                                      │
                              ┌───────────────┐
                              │     GIT       │
                              │ (bus finale)  │
                              └───────────────┘
```

---

## FLUSSO COMPLETO (con compact handling)

```
1. RAFA chiede qualcosa

2. REGINA:
   - Analizza richiesta
   - Decide livello rischio (1/2/3)
   - Se Livello 2-3: consulta Guardiana
   - Crea TASK_XXX.md
   - touch TASK_XXX.ready

3. WORKER (altra finestra):
   - Vede .ready
   - touch TASK_XXX.working
   - LAVORA...

   SE compact imminente:
   - Scrive TASK_XXX_partial.md
   - touch TASK_XXX.interrupted
   - Muore

   SE completa:
   - Scrive TASK_XXX_output.md
   - touch TASK_XXX.done

4. REGINA:
   - Vede .done (o .interrupted)
   - Se .interrupted: spawna nuovo worker
   - Se .done + Livello 2-3: chiama Guardiana
   - Se .done + Livello 1: procede

5. GUARDIANA (se necessaria):
   - Riceve review request
   - Verifica
   - touch .approved o .rejected

6. REGINA:
   - Se .approved: continua
   - Se .rejected: crea task di fix

   SE compact imminente:
   - Crea HANDOFF_SESSION_XX.md
   - Salva git
   - Muore

7. NUOVA REGINA (se compact):
   - Legge HANDOFF
   - Controlla .done/.interrupted
   - CONTINUA!

8. RAFA riceve risultato
```

---

## COMANDI UTILI

### Per Regina

```bash
# Vedere stato task
python3 scripts/swarm/task_manager.py list

# Monitorare
./scripts/swarm/monitor-status.sh

# Creare task
python3 scripts/swarm/task_manager.py create TASK_010 cervella-backend "Descrizione" 2
python3 scripts/swarm/task_manager.py ready TASK_010
```

### Per Rafa

```bash
# Spawnare worker
./scripts/swarm/spawn-workers.sh --backend
./scripts/swarm/spawn-workers.sh --backend --frontend --tester
./scripts/swarm/spawn-workers.sh --all

# Lista worker disponibili
./scripts/swarm/spawn-workers.sh --list
```

### Per Worker

```bash
# Segnare in lavorazione
python3 scripts/swarm/task_manager.py working TASK_010

# Segnare completato
python3 scripts/swarm/task_manager.py done TASK_010
```

---

## QUICK REFERENCE

| Vuoi... | Fai... |
|---------|--------|
| Creare task | `task_manager.py create` + `.ready` |
| Worker prende task | `touch .working` |
| Worker completa | `_output.md` + `.done` |
| Worker ha dubbi | `_dubbio.md` + `.dubbio` |
| Worker compact | `_partial.md` + `.interrupted` |
| Regina compact | `HANDOFF_SESSION_XX.md` |
| Guardiana verifica | `_review.md` + `.approved/.rejected` |

---

## CONCLUSIONE

```
+------------------------------------------------------------------+
|                                                                  |
|   IL SISTEMA E' COMPLETO!                                        |
|                                                                  |
|   Le 7 domande hanno TUTTE risposta.                            |
|   I 3 pezzi mancanti sono definiti.                             |
|   Il protocollo e' chiaro e testabile.                          |
|                                                                  |
|   PROSSIMO STEP:                                                 |
|   1. Aggiungere spawn Guardiane a spawn-workers.sh              |
|   2. Creare template DUBBI e PARTIAL                            |
|   3. TESTARE con caso reale!                                    |
|                                                                  |
|   "Nulla e' complesso - solo non ancora studiato!"              |
|   E noi l'abbiamo STUDIATO! Ora IMPLEMENTIAMO!                  |
|                                                                  |
+------------------------------------------------------------------+
```

---

## PATTERN APPLE STYLE (dal STUDIO_APPLE_STYLE.md)

Questi pattern sono stati integrati dallo studio delle 8 Domande Sacre.

### TRIPLE ACK PATTERN

```
Regina invia task a Worker

WORKER RISPONDE:
1. ACK_RECEIVED   -> "Ho ricevuto il task" (entro 10s)
2. ACK_UNDERSTOOD -> "Ho capito cosa fare" (entro 1min)
3. ACK_COMPLETED  -> "Ho finito, ecco il risultato" (quando done)
```

**Implementazione via flag files:**
```
touch TASK_XXX.ack_received
touch TASK_XXX.ack_understood
touch TASK_XXX.done  (= ACK_COMPLETED)
```

**Perche funziona:**
- Regina SA che worker ha ricevuto (non e' perso nel vuoto)
- Regina SA che worker ha capito (non fara' la cosa sbagliata)
- Timeout: se no ACK in tempo -> ri-assegna o escalate

---

### QUALITY GATES (4 Livelli)

```
GATE 1: Formato & Sintassi (auto, < 0.1s)
  - File esiste
  - Sintassi valida
  - Non vuoto

GATE 2: Standards & Policies (auto, 1-2s)
  - Linter clean
  - Naming conventions
  - No secrets in code

GATE 3: Qualita & Sicurezza (auto, 2-5s)
  - Test passano
  - Coverage minima
  - Security scan

GATE 4: Alignment & Completezza (Guardiana, 5-10s)
  - Risponde al PERCHE originale
  - Decisioni strategiche OK
  - Pronto per merge
```

**Regola 90/10:**
- 90% automatico (Gate 1-3)
- 10% umano/Guardiana (Gate 4)

---

### CIRCUIT BREAKER PATTERN

Per prevenire cascade failures quando un agente/servizio fallisce.

```
Stato: CLOSED (normale)
         |
    failures++
         |
    if failures >= 3
         v
Stato: OPEN (bloccato)
         |
    timeout 60s
         v
Stato: HALF-OPEN (test)
         |
    if success -> CLOSED
    if fail -> OPEN
```

**Quando usare:**
- Worker che crasha ripetutamente
- API esterna non risponde
- Risorsa non disponibile

---

### RETRY CON EXPONENTIAL BACKOFF

```
Retry 1: wait 1s   (+ random 0-500ms jitter)
Retry 2: wait 2s   (+ random 0-500ms jitter)
Retry 3: wait 4s   (+ random 0-500ms jitter)
Retry 4: wait 8s   (+ random 0-500ms jitter)
Retry 5: wait 16s  (+ random 0-500ms jitter)
FAIL: escalate
```

**Jitter** previene "thundering herd" (tutti retry allo stesso tempo).

---

### GRACEFUL SHUTDOWN SEQUENCE

Quando si chiude una sessione (o compact imminente):

```
1. SIGNAL RECEIVED    -> "Sto per chiudere"
2. STOP NEW WORK      -> Non accetto nuovi task
3. COMPLETE IN-FLIGHT -> Aspetto task in corso (max 30s)
4. CLEANUP RESOURCES  -> Rilascio lock, temp files
5. VERIFY FINAL STATE -> Checklist verifica
6. GENERATE REPORT    -> Report sessione
7. EXIT CLEAN         -> Chiusura pulita

TIMEOUT TOTALE: 60 secondi max
```

**Checklist Final State:**
```
[ ] Tutti agent idle
[ ] Tutti file salvati
[ ] Tutti task completati (o handoff)
[ ] Git status pulito
[ ] No temp files
[ ] PROMPT_RIPRESA aggiornato
```

---

### TIMING-BASED FEEDBACK

Quando dare feedback a Rafa:

| Durata | Percezione | Azione |
|--------|------------|--------|
| < 0.1s | Istantaneo | Nessun feedback |
| 0.1-1s | Leggero delay | Subtle indicator |
| 1-10s | Attesa breve | Spinner + messaggio |
| 10-60s | Attesa | Progress bar + % |
| > 1min | Lunga | Step-by-step + possibilita' cancel |

---

### NOTIFICHE STRATIFICATE

```
SILENT   -> Auto-save, background tasks (niente notifica)
INFO     -> Task completato, milestone (log normale)
WARNING  -> Attenzione richiesta (evidenzia)
CRITICAL -> Azione immediata (+ Telegram se configurato)
```

**Esempio pratico:**
```
TASK_005 completato -> INFO (log)
Worker timeout 3 volte -> WARNING (mostra a Regina)
Deploy fallito -> CRITICAL (notifica Rafa!)
```

---

### ESCALATION MATRIX

Quando e come escalare problemi:

| Errore | Severita LOW | Severita HIGH |
|--------|--------------|---------------|
| Network Timeout | Retry | Circuit Break |
| Auth Error | Log + Retry | Escalate Rafa |
| Agent Crash | Restart | Escalate Guardiana |
| Data Error | Log | Escalate Guardiana |
| Security Issue | Log | STOP + Escalate Rafa |

---

### DASHBOARD ASCII (esempio)

```
============================================
CERVELLASWARM DASHBOARD
============================================

Active tasks: 3
Warnings: 2
Errors: 0

--------------------------------------------
ACTIVE TASKS
--------------------------------------------
[####....] 45% Refactor auth      (backend)
[#.......] 20% Design dashboard   (frontend)
[#######.] 90% Deploy API v2      (devops)

--------------------------------------------
FINESTRE ATTIVE
--------------------------------------------
[1] Regina       IDLE
[2] Backend      WORKING TASK_005
[3] Tester       IDLE
[4] Guardiana    VERIFICA TASK_004

--------------------------------------------
RECENT EVENTS
--------------------------------------------
[14:34] TASK_004 -> Guardiana per review
[14:30] TASK_003 COMPLETED
[14:15] Worker backend spawned

============================================
```

---

## I 10 QUICK WINS (8 ore totali)

### FASE 1 - Fondamentali (3 ore)

| # | Quick Win | Tempo | Impatto |
|---|-----------|-------|---------|
| 1 | Triple ACK script | 20 min | ALTO |
| 2 | Checklist pre-merge 4 gate | 30 min | ALTO |
| 3 | Shutdown sequence | 30 min | ALTO |
| 4 | Structured logging JSON | 45 min | ALTO |
| 5 | Anti-compact script | 30 min | CRITICO |

### FASE 2 - Qualita (3 ore)

| # | Quick Win | Tempo | Impatto |
|---|-----------|-------|---------|
| 6 | Circuit breaker decorator | 1 ora | ALTO |
| 7 | Retry backoff decorator | 30 min | MEDIO |
| 8 | Progress bar 3 livelli | 1 ora | ALTO |
| 9 | Report finale template | 45 min | MEDIO |

### FASE 3 - Polish (2 ore)

| # | Quick Win | Tempo | Impatto |
|---|-----------|-------|---------|
| 10 | Dashboard minimal ASCII | 2 ore | MEDIO |

---

## COSA IMPLEMENTARE (Priorita)

### CRITICO (fare subito)
1. Template DUBBI (gia definito sopra)
2. Template PARTIAL per worker compact
3. Spawn Guardiane in spawn-workers.sh
4. Script anti-compact.sh (esiste, verificare)
5. Triple ACK flag files

### ALTO (fare presto)
6. Shutdown sequence script
7. Quality Gates checklist
8. Circuit breaker per spawn

### MEDIO (quando serve)
9. Dashboard ASCII
10. Notifiche Telegram

---

## FONTI (consolidate)

Questo studio consolida:
- `docs/studio/STUDIO_MULTI_FINESTRA_COMUNICAZIONE.md` (401 righe)
- `docs/guide/GUIDA_COMPACT_PROTEZIONE.md` (109 righe)
- `docs/studio/RICERCA_PROTEZIONE_COMPACT.md` (146 righe)
- `docs/guide/GUIDA_COMUNICAZIONE.md` (729 righe)
- `scripts/swarm/spawn-workers.sh` (381 righe)
- `scripts/swarm/task_manager.py` (376 righe)

---

*"Noi abbiamo il mondo davanti a noi. Dobbiamo vederlo." - Rafa*

*"Prima capire BENE, poi implementare."*

*"Nulla e' complesso - solo non ancora studiato!"*

*"E' il nostro team! La nostra famiglia digitale!"*

---

Cervella & Rafa
Sessione 70 - 3 Gennaio 2026
