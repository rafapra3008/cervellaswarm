# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 3 Gennaio 2026 - Sessione 73 - spawn-workers.sh FUNZIONA!

---

## CARA PROSSIMA CERVELLA

```
+------------------------------------------------------------------+
|                                                                  |
|   Benvenuta! Questo file e' la tua UNICA memoria.               |
|   Leggilo con calma. Qui c'e' tutto quello che devi sapere.     |
|                                                                  |
|   Tu sei la REGINA dello sciame.                                 |
|   Hai 16 agenti pronti a lavorare per te.                       |
|                                                                  |
|   FASE ATTUALE: FASE 9 - APPLE STYLE                            |
|   STATO: spawn-workers.sh v1.2.0 FUNZIONA AL 100%!              |
|                                                                  |
|   Il sistema Multi-Finestra e' VIVO!                            |
|   Puoi gia usarlo per delegare lavoro ai worker!                |
|                                                                  |
+------------------------------------------------------------------+
```

---

## IL MOMENTO ATTUALE (Sessione 73)

```
+------------------------------------------------------------------+
|                                                                  |
|   spawn-workers.sh v1.2.0 - FIX CRITICO COMPLETATO!             |
|                                                                  |
|   PROBLEMA RISOLTO:                                              |
|   - spawn-workers.sh apriva finestra                            |
|   - Claude partiva MA restava fermo in attesa di input          |
|                                                                  |
|   FIX: Aggiunto prompt iniziale come argomento!                 |
|   Ora il worker parte E lavora AUTOMATICAMENTE.                 |
|                                                                  |
|   TESTATO E FUNZIONANTE:                                        |
|   - Worker apre                                                  |
|   - Cerca task in .swarm/tasks/                                  |
|   - Se non trova task, scrive in .swarm/handoff/                |
|   - COMUNICAZIONE TRA FINESTRE FUNZIONA!                        |
|                                                                  |
+------------------------------------------------------------------+
```

---

## FILO DEL DISCORSO (Sessione 73) - LEGGI BENE!

### Il Fix Critico

1. **PROBLEMA: spawn-workers.sh non funzionava**
   La finestra si apriva, Claude partiva, ma restava fermo.
   Aspettava input dall'utente invece di lavorare.

2. **CAUSA: Mancava il prompt iniziale**
   `--append-system-prompt` aggiunge al system prompt
   MA Claude Code aspetta comunque un prompt iniziale!

3. **FIX: Aggiunto argomento prompt**
   ```bash
   claude --append-system-prompt "..." "Cerca task e inizia a lavorare"
   ```
   Il prompt iniziale come argomento fa partire il worker!

4. **TESTATO: FUNZIONA AL 100%!**
   Il worker ha cercato task, trovato template vuoto,
   scritto in .swarm/handoff/ per comunicare con la Regina.
   ESATTAMENTE il comportamento voluto!

---

## FILO DEL DISCORSO (Sessione 72) - Archivio

### La Lezione Fondamentale

1. **HO USATO TASK TOOL INVECE DI MULTI-FINESTRA**
   Rafa mi ha fermato: "Dov'e' la visione? Quando usiamo multi-finestra?"
   Task tool = tutto nel MIO contesto = NON e' il NORD!
   spawn-workers.sh = finestre REALI = IL NORD!

2. **"COMODO != GIUSTO"**
   Ho scelto il metodo COMODO (Task tool) invece del metodo GIUSTO.
   Rafa: "Perche' pensi che abbiamo perso la direzione?"
   Risposta: Comodita' > Visione. Non ho riletto il NORD prima di agire.

3. **PRIMA DI AGIRE, CHIEDERE:**
   - "Questo e' il modo COMODO o il modo GIUSTO?"
   - "Sto seguendo il NORD o sto deviando?"
   - "Lo sciame lavora INSIEME o lavoro solo IO?"

### Cosa Ho Fatto (Sessione 72)

1. Quick Wins creati (MA con Task tool - metodo sbagliato):
   - checklist-pre-merge.sh (4 gates)
   - dashboard.py + dashboard.sh
   - progress_bar.py
   - REPORT_FINALE.md template

2. HARDTESTS creati (16 test!):
   - docs/tests/HARDTESTS_APPLE_STYLE.md
   - 6 test generali + 10 test Quick Wins
   - Pronti per esecuzione con MULTI-FINESTRA

3. Test Quick Wins eseguiti (6 PASSATI):
   - dashboard.py PASS
   - progress_bar.py PASS
   - circuit_breaker.py PASS
   - structured_logging.py PASS
   - spawn-workers.sh --list PASS
   - task_manager.py list PASS

4. Riletto COSTITUZIONE per refresh

### Prossima Sessione - URGENTE!

```
PROBLEMA: spawn-workers.sh NON FUNZIONA!

La finestra si apre ma Claude NON parte.
Abbiamo provato fix con path completo ma non basta.

FOCUS SESSIONE 73:
1. DEBUG spawn-workers.sh - capire perche' non parte
2. Testare manualmente il runner script
3. Fixare finche' funziona
4. SOLO DOPO: HARDTESTS

COMANDI DEBUG:
- cat .swarm/runners/run_backend.sh
- bash -x .swarm/runners/run_backend.sh  (vedi cosa fa)
- Aprire Terminal manualmente e provare il comando

IL PROBLEMA:
osascript apre finestra -> esegue runner -> claude non parte
Forse problema con NVM/PATH nella nuova shell?
```

---

## FILO DEL DISCORSO (Sessione 71) - Archivio

### Cosa e' Successo

1. **AVVIATA SESSIONE CON ENERGIA!**
   Rafa: "Ultrapassar os proprios limites!"
   Ho letto lo STUDIO_COMUNICAZIONE_DEFINITIVO.md (900 righe)
   Sapevo esattamente cosa implementare.

2. **LANCIATO LO SCIAME IN PARALLELO!**
   3 api contemporaneamente:
   - cervella-docs: Template DUBBI e PARTIAL
   - cervella-devops: Spawn Guardiane in spawn-workers.sh
   - cervella-backend: Triple ACK system

3. **IMPLEMENTATO TEMPLATE DUBBI**
   File: `.swarm/tasks/TEMPLATE_DUBBI.md` (62 righe)
   - Con commenti HTML e istruzioni
   - Esempi inline per guidare compilazione
   - Workflow: Pausa -> Review -> Decisione -> Riprendi

4. **IMPLEMENTATO TEMPLATE PARTIAL**
   File: `.swarm/tasks/TEMPLATE_PARTIAL.md` (76 righe)
   - Recovery Plan per chi continua
   - Note Tecniche per dettagli critici
   - Distinzione file COMPLETATI vs IN CORSO

5. **ESTESO SPAWN-WORKERS.SH v1.1.0**
   Aggiunte le 3 Guardiane Opus:
   - `--guardiana-qualita`
   - `--guardiana-ops`
   - `--guardiana-ricerca`
   - `--guardiane` (tutte e 3)
   - Sezione separata PURPLE nella lista

6. **IMPLEMENTATO TRIPLE ACK**
   - `task_manager.py v1.1.0` - metodi ack_received(), ack_understood()
   - `triple-ack.sh v2.0.0` - helper script con colori
   - Colonna ACK nella lista: R/U/D (✓ o -)

7. **TESTATO WORKFLOW COMPLETO**
   - Creato task TEST_FLOW
   - ACK_RECEIVED -> ACK_UNDERSTOOD -> ACK_COMPLETED
   - Tutto funzionante!

8. **DETTAGLIO UTILE (da Rafa)**
   Per chiudere finestre senza popup "Termina":
   -> Fare `exit` nel terminale prima di chiudere
   Da integrare nel Graceful Shutdown Sequence!

---

## COSA DEVI FARE (PROSSIMO STEP)

```
+------------------------------------------------------------------+
|                                                                  |
|   I 4 CRITICI SONO GIA IMPLEMENTATI!                            |
|                                                                  |
|   [x] Template DUBBI - .swarm/tasks/TEMPLATE_DUBBI.md           |
|   [x] Template PARTIAL - .swarm/tasks/TEMPLATE_PARTIAL.md       |
|   [x] Spawn Guardiane - spawn-workers.sh v1.1.0                 |
|   [x] Triple ACK - task_manager.py + triple-ack.sh              |
|                                                                  |
|   ORA PUOI:                                                      |
|                                                                  |
|   1. Implementare Shutdown Sequence script                      |
|      (Graceful close con `exit` automatico)                     |
|                                                                  |
|   2. Creare Quality Gates checklist                             |
|      (4 livelli di verifica automatica)                         |
|                                                                  |
|   3. Test REALE su Miracollo!                                   |
|      (Il sistema e' PRONTO!)                                    |
|                                                                  |
+------------------------------------------------------------------+
```

### PROSSIMA SESSIONE - LA MAPPA!

```
SEGUI LA ROADMAP! docs/roadmap/FASE_9_APPLE_STYLE.md

Sprint 9.2 - Quick Wins rimanenti (~6 ore):
[ ] Checklist pre-merge 4 gate (30 min)
[ ] Shutdown sequence (30 min)
[ ] Structured logging JSON (45 min)
[ ] Anti-compact script - verificare (30 min)
[ ] Circuit breaker decorator (1 ora)
[ ] Retry backoff decorator (30 min)
[ ] Progress bar 3 livelli (1 ora)
[ ] Report finale template (45 min)
[ ] Dashboard minimal ASCII (2 ore)

Sprint 9.4 - HARDTESTS Apple Style (6 test!):
[ ] SMOOTH COMMUNICATION
[ ] TRIPLE CHECK AUTOMATICO
[ ] ERROR HANDLING GRACEFUL
[ ] CLEAN CLOSURE
[ ] FEEDBACK IN TEMPO REALE
[ ] ANTI-COMPACT AUTOMATICO

Sprint 9.5 - MIRACOLLO READY:
[ ] Rafa dice "E' LISCIO!" ✅
```

**NON SALTARE A MIRACOLLO PRIMA DI COMPLETARE FASE 9!**
*"Con la mappa rotta giriamo in torno di noi stessi!"* - Rafa

---

## IL DOCUMENTO DI RIFERIMENTO

```
docs/studio/STUDIO_COMUNICAZIONE_DEFINITIVO.md (870+ righe!)

Contiene TUTTO:
- Le 7 domande con risposte complete
- Template per ogni scenario
- Pattern Apple Style integrati
- 10 Quick Wins prioritizzati
- Architettura completa
- Flusso con compact handling
```

**SE HAI DUBBI -> LEGGI QUEL FILE!**

---

## COSA ESISTE GIA (funziona!)

| Cosa | Status |
|------|--------|
| 16 Agents in ~/.claude/agents/ | FUNZIONANTE |
| Sistema Memoria SQLite | FUNZIONANTE |
| 10 Hooks globali | FUNZIONANTE |
| SWARM_RULES v1.4.0 | FUNZIONANTE |
| Pattern Catalog (3 pattern) | FUNZIONANTE |
| GUIDA_COMUNICAZIONE v2.0 | FUNZIONANTE |
| Flusso Guardiane (3 livelli) | TESTATO! |
| HARDTESTS Comunicazione (3/3) | PASSATI! |
| HARDTESTS Swarm V3 (4/4) | PASSATI! |
| spawn-workers.sh v1.1.0 | LA MAGIA + GUARDIANE! |
| Template DUBBI | NUOVO! |
| Template PARTIAL | NUOVO! |
| Triple ACK system | NUOVO! |
| task_manager.py | FUNZIONANTE |
| .swarm/ struttura | FUNZIONANTE |

---

## LO SCIAME (16 membri)

```
TU SEI LA REGINA (Opus) - Coordina, DELEGA, MAI edit diretti!

3 GUARDIANE (Opus):
- cervella-guardiana-qualita
- cervella-guardiana-ops
- cervella-guardiana-ricerca

12 WORKER (Sonnet):
- frontend, backend, tester, reviewer
- researcher, scienziata, ingegnera
- marketing, devops, docs, data, security
```

---

## FILE IMPORTANTI

| File | Cosa Contiene |
|------|---------------|
| `docs/studio/STUDIO_COMUNICAZIONE_DEFINITIVO.md` | **IL RIFERIMENTO!** 870+ righe |
| `docs/studio/STUDIO_APPLE_STYLE.md` | 8 Domande Sacre + Quick Wins |
| `NORD.md` | Dove siamo, prossimo obiettivo |
| `docs/roadmap/FASE_9_APPLE_STYLE.md` | ROADMAP completa FASE 9 |
| `.swarm/README.md` | Come funziona il sistema multi-finestra |
| `scripts/swarm/spawn-workers.sh` | LA MAGIA! Apre finestre worker |
| `SWARM_RULES.md` | Le 12 regole dello sciame |

---

## GIT

```
Branch:   main
Versione: v27.5.0
Stato:    FASE 9 - 45% (Quick Wins parziali, HARDTESTS da fare!)
```

---

## LE NOSTRE FRASI

```
"Lavoriamo in pace! Senza casino! Dipende da noi!"

"Nulla e' complesso - solo non ancora studiato!"

"L'abbiamo STUDIATO! L'abbiamo IMPLEMENTATO! Ora USIAMOLO!"

"Ultrapassar os proprios limites!" - Rafa

"Fatto BENE > Fatto VELOCE"

"E' il nostro team! La nostra famiglia digitale!"
```

---

## LA STORIA (come siamo arrivati qui)

| Sessione | Cosa | Risultato |
|----------|------|-----------|
| 60 | LA SCOPERTA | N finestre = N contesti! |
| 61 | MVP Multi-Finestra | .swarm/ funzionante |
| 62 | CODE REVIEW | 8.5/10 OTTIMO! |
| 63 | INSIGHT CERVELLO | Studio neuroscientifico |
| 64 | HARDTESTS CREATI | 1256 righe di test |
| 65 | HARDTESTS PASSATI | 4/4 PASS! |
| 66 | LA MAGIA! | spawn-workers.sh |
| 67 | CODE REVIEW + ROADMAP | 9.0/10 + FASE 9! |
| 68 | SPRINT 9.1 RICERCA | 8 Domande RISPOSTE! |
| 69 | INSIGHT COMUNICAZIONE | Task tool vs Multi-finestra! |
| 70 | STUDIO COMPLETATO! | BLEND fatto! 870+ righe! |
| **71** | **4 CRITICI IMPLEMENTATI!** | **Sciame parallelo! Tutto testato!** |

---

```
+------------------------------------------------------------------+
|                                                                  |
|   CARA PROSSIMA CERVELLA                                         |
|                                                                  |
|   I 4 CRITICI sono GIA IMPLEMENTATI!                            |
|   [x] Template DUBBI                                              |
|   [x] Template PARTIAL                                            |
|   [x] Spawn Guardiane                                             |
|   [x] Triple ACK                                                  |
|                                                                  |
|   MA NON ANDARE SU MIRACOLLO!                                   |
|   Prima devi completare FASE 9:                                  |
|                                                                  |
|   [ ] Quick Wins rimanenti (~6 ore)                             |
|   [ ] HARDTESTS Apple Style (6 test!)                           |
|   [ ] Checklist MIRACOLLO READY                                 |
|                                                                  |
|   LEGGI: docs/roadmap/FASE_9_APPLE_STYLE.md                     |
|                                                                  |
|   "Con la mappa rotta giriamo in torno di noi stessi!"          |
|                                                                  |
+------------------------------------------------------------------+
```

---

## PROMPT_RIPRESA 10000%!

```
+------------------------------------------------------------------+
|                                                                  |
|   Questo file e' scritto con CURA.                              |
|                                                                  |
|   La prossima Cervella non sa NULLA.                            |
|   Questo file e' la sua UNICA memoria.                          |
|                                                                  |
|   Per questo:                                                    |
|   - FILO DEL DISCORSO (perche', non solo cosa)                  |
|   - LE FRASI DI RAFA (le sue parole esatte!)                    |
|   - DECISIONI PRESE (cosa abbiamo scelto e perche')             |
|   - PROSSIMI STEP (cosa fare dopo)                              |
|   - FILE IMPORTANTI (dove trovare tutto)                        |
|                                                                  |
|   L'insight di questa sessione (71):                            |
|   "Ultrapassar os proprios limites!" - Rafa                     |
|   Lo sciame ha lavorato in PARALLELO (3 api insieme!)           |
|                                                                  |
|   IMPORTANTE - Rafa ci ha fermato:                              |
|   "vedere la mapa.. e' l'unico modo di arrivare al tessouro"   |
|   NON saltare a Miracollo! Prima completare FASE 9!             |
|                                                                  |
|   Prossimo: Quick Wins rimanenti + HARDTESTS                    |
|                                                                  |
|   "Non e' sempre come immaginiamo...                            |
|    ma alla fine e' il 100000%!"                                 |
|                                                                  |
+------------------------------------------------------------------+
```

---

*Scritto con CURA e PRECISIONE.*

*"Nulla e' complesso - solo non ancora studiato!"*

*E noi l'abbiamo STUDIATO!*

Cervella & Rafa

---

**VERSIONE:** v27.5.0
**SESSIONE:** 71
**DATA:** 3 Gennaio 2026

---

## CHECKPOINT SESSIONE 71

### Stato Git
- **Branch**: main
- **Ultimo commit**: 0390a70 - docs: Aggiornata ROADMAP FASE 9 + PROMPT_RIPRESA 10000%
- **Versione**: v27.5.0

### File Creati/Modificati Sessione 71
- `.swarm/tasks/TEMPLATE_DUBBI.md` (62 righe) - NUOVO
- `.swarm/tasks/TEMPLATE_PARTIAL.md` (76 righe) - NUOVO
- `scripts/swarm/spawn-workers.sh` v1.1.0 - Guardiane aggiunte
- `scripts/swarm/task_manager.py` v1.1.0 - Triple ACK
- `scripts/swarm/triple-ack.sh` v2.0.0 - NUOVO
- `docs/roadmap/FASE_9_APPLE_STYLE.md` v1.1.0 - Aggiornata

### Insight Sessione 71
- Lo sciame ha lavorato in PARALLELO (3 api insieme!)
- Rafa: "vedere la mapa.. e' l'unico modo di arrivare al tessouro"
- FASE 9 al 45% - Quick Wins e HARDTESTS da fare prima di Miracollo

---

---

---

---

---

## AUTO-CHECKPOINT: 2026-01-03 22:48 (unknown)

### Stato Git
- **Branch**: main
- **Ultimo commit**: 0f70041 - docs: PROMPT_RIPRESA - spawn-workers.sh non funziona, debug prossima sessione
- **File modificati** (5):
  - swarm/runners/run_backend.sh
  - PROMPT_RIPRESA.md
  - reports/scientist_prompt_20260103.md
  - scripts/swarm/spawn-workers.sh
  - .swarm/handoff/

### Note
- Checkpoint automatico generato da hook
- Trigger: unknown

---
