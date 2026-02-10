# HARDTESTS APPLE STYLE - Sprint 9.4

> **Data:** 3 Gennaio 2026 - Sessione 72
> **Obiettivo:** Validare che CervellaSwarm sia Apple Style
> **Metodo:** Multi-finestra REALE (spawn-workers.sh) - NO Task tool!

---

## REGOLA FONDAMENTALE

```
+------------------------------------------------------------------+
|                                                                  |
|   QUESTI TEST SI FANNO CON MULTI-FINESTRA REALE!                |
|                                                                  |
|   Comando: ./scripts/swarm/spawn-workers.sh --[worker]          |
|                                                                  |
|   NON usare Task tool!                                          |
|   Task tool = tutto nel contesto Regina = NON e' il NORD!       |
|                                                                  |
|   "Comodo != Giusto" - Lezione Sessione 72                      |
|                                                                  |
+------------------------------------------------------------------+
```

---

## TEST 1: SMOOTH COMMUNICATION

**Scenario:** Regina delega task a 2 worker (backend + tester)

### Setup

```bash
# Finestra 1 (Regina) - gia' aperta
# Tu sei qui!

# Finestra 2 (Backend)
./scripts/swarm/spawn-workers.sh --backend

# Finestra 3 (Tester)
./scripts/swarm/spawn-workers.sh --tester
```

### Azioni

1. **Regina** crea TASK_AS1.md (Apple Style 1):
   ```
   Task: Creare funzione hello_world() in test-orchestrazione/api/hello.py
   Livello: 1 (BASSO)
   Criteri: Funzione esiste, ritorna "Hello CervellaSwarm!"
   ```

2. **Backend worker** (finestra 2):
   - Legge task
   - ACK_RECEIVED
   - ACK_UNDERSTOOD
   - Implementa
   - Scrive output
   - .done

3. **Tester worker** (finestra 3):
   - Regina crea TASK_AS1_TEST.md
   - Tester verifica funzione
   - Scrive risultato

4. **Regina** verifica completamento

### Checklist Verifica

- [ ] Handoff chiaro (worker conferma ricezione)
- [ ] Triple ACK funziona (received, understood, done)
- [ ] Output file creato correttamente
- [ ] Zero ambiguita in tutto il flusso
- [ ] Tempo totale < 10 minuti

### Risultato

| Aspetto | PASS/FAIL | Note |
|---------|-----------|------|
| Handoff chiaro | | |
| Triple ACK | | |
| Output corretto | | |
| Zero ambiguita | | |
| Tempo OK | | |

**ESITO TEST 1:** ____

---

## TEST 2: TRIPLE CHECK AUTOMATICO

**Scenario:** Backend completa feature, Guardiana verifica

### Setup

```bash
# Finestra 1: Regina (tu)
# Finestra 2: Backend
./scripts/swarm/spawn-workers.sh --backend

# Finestra 3: Guardiana Qualita
./scripts/swarm/spawn-workers.sh --guardiana-qualita
```

### Azioni

1. **Regina** crea TASK_AS2.md:
   ```
   Task: Creare funzione validate_name() in test-orchestrazione/api/validators.py
   Livello: 2 (MEDIO) - Richiede Guardiana
   Criteri: Valida che nome non sia vuoto, max 100 char
   ```

2. **Backend** implementa

3. **Regina** crea review request per Guardiana

4. **Guardiana** verifica:
   - Codice funziona
   - Casi edge coperti
   - Approva o rigetta

5. **Se approvato** -> merge

### Checklist Verifica

- [ ] Backend completa con output
- [ ] Regina crea review request
- [ ] Guardiana riceve e verifica
- [ ] .approved o .rejected creato
- [ ] Flusso completo < 15 minuti

### Risultato

| Aspetto | PASS/FAIL | Note |
|---------|-----------|------|
| Backend output | | |
| Review request | | |
| Guardiana verifica | | |
| Approvazione | | |
| Tempo OK | | |

**ESITO TEST 2:** ____

---

## TEST 3: ERROR HANDLING GRACEFUL

**Scenario:** Worker incontra errore durante task

### Setup

```bash
# Finestra 1: Regina
# Finestra 2: Backend
./scripts/swarm/spawn-workers.sh --backend
```

### Azioni

1. **Regina** crea TASK_AS3.md:
   ```
   Task: Creare funzione che legge file /path/non/esistente.txt
   Livello: 1
   Nota: Questo task fallira'! Vogliamo vedere come gestisce l'errore.
   ```

2. **Backend** tenta implementazione

3. **Backend** incontra errore (file non esiste)

4. **Backend** dovrebbe:
   - Segnalare errore chiaramente nell'output
   - Proporre alternative/soluzioni
   - NON crashare

### Checklist Verifica

- [ ] Errore segnalato in output (non silenzioso)
- [ ] Messaggio chiaro (cosa e' andato storto)
- [ ] Suggerimento recovery presente
- [ ] Worker NON crasha (graceful)
- [ ] Regina capisce cosa fare

### Risultato

| Aspetto | PASS/FAIL | Note |
|---------|-----------|------|
| Errore segnalato | | |
| Messaggio chiaro | | |
| Recovery suggerito | | |
| No crash | | |
| Regina capisce | | |

**ESITO TEST 3:** ____

---

## TEST 4: CLEAN CLOSURE

**Scenario:** Fine sessione, shutdown pulito

### Setup

Dopo aver completato alcuni task, eseguiamo shutdown.

### Azioni

1. **Regina** esegue:
   ```bash
   ./scripts/swarm/shutdown-sequence.sh
   ```

2. Verifica che:
   - Nessun task attivo
   - File temporanei puliti
   - Report generato
   - Git status pulito (o commit fatto)

### Checklist Verifica

- [ ] Script shutdown-sequence.sh funziona
- [ ] Task attivi verificati (0 o warning)
- [ ] Report in reports/ creato
- [ ] Git status mostrato
- [ ] Messaggio finale chiaro

### Risultato

| Aspetto | PASS/FAIL | Note |
|---------|-----------|------|
| Script funziona | | |
| Task verificati | | |
| Report creato | | |
| Git OK | | |
| Messaggio chiaro | | |

**ESITO TEST 4:** ____

---

## TEST 5: FEEDBACK IN TEMPO REALE

**Scenario:** Task lungo con progress updates

### Setup

```bash
# Finestra 1: Regina
# Finestra 2: Backend
./scripts/swarm/spawn-workers.sh --backend
```

### Azioni

1. **Regina** crea TASK_AS5.md:
   ```
   Task: Creare 5 funzioni helper in test-orchestrazione/api/helpers.py
   - format_date()
   - format_currency()
   - truncate_string()
   - capitalize_words()
   - slugify()
   Livello: 1
   Nota: Task piu' lungo del solito
   ```

2. **Backend** lavora con progress:
   - ACK_RECEIVED
   - ACK_UNDERSTOOD
   - [Opzionale] Update progress ogni funzione

3. **Regina** monitora con:
   ```bash
   python3 scripts/swarm/task_manager.py list
   ```

### Checklist Verifica

- [ ] ACK arrivano in tempo
- [ ] Progress visibile (via task_manager o flag)
- [ ] Completion chiara
- [ ] Tempo totale ragionevole

### Risultato

| Aspetto | PASS/FAIL | Note |
|---------|-----------|------|
| ACK puntuali | | |
| Progress visibile | | |
| Completion chiara | | |
| Tempo OK | | |

**ESITO TEST 5:** ____

---

## TEST 6: ANTI-COMPACT (SIMULATO)

**Scenario:** Simuliamo compact imminente

> **NOTA:** Non possiamo forzare un vero compact, ma possiamo testare lo script.

### Azioni

1. **Regina** esegue anti-compact manualmente:
   ```bash
   ./scripts/swarm/anti-compact.sh --no-spawn --message "Test HARDTEST 6"
   ```

2. Verifica che:
   - PROMPT_RIPRESA.md aggiornato con checkpoint
   - Git commit creato
   - Git push eseguito (se configurato)
   - Messaggio finale chiaro

3. **Verifica PROMPT_RIPRESA.md**:
   ```bash
   tail -30 PROMPT_RIPRESA.md
   ```
   Deve mostrare sezione AUTO-CHECKPOINT

### Checklist Verifica

- [ ] Script anti-compact.sh funziona
- [ ] PROMPT_RIPRESA.md aggiornato
- [ ] Git commit creato
- [ ] Messaggio finale chiaro
- [ ] Nuova sessione potrebbe riprendere da qui

### Risultato

| Aspetto | PASS/FAIL | Note |
|---------|-----------|------|
| Script funziona | | |
| PROMPT aggiornato | | |
| Git commit | | |
| Messaggio chiaro | | |
| Recovery possibile | | |

**ESITO TEST 6:** ____

---

## RIEPILOGO FINALE

| Test | Nome | PASS/FAIL |
|------|------|-----------|
| 1 | Smooth Communication | |
| 2 | Triple Check Automatico | |
| 3 | Error Handling Graceful | |
| 4 | Clean Closure | |
| 5 | Feedback Tempo Reale | |
| 6 | Anti-Compact | |

**TOTALE:** ___/6 PASS

---

## CRITERI DI SUCCESSO

```
6/6 PASS -> MIRACOLLO READY! GO!
5/6 PASS -> Fix minore, poi GO
4/6 PASS -> Review necessaria
<4/6     -> NON READY - Fix richiesti
```

---

## NOTE PER ESECUZIONE

1. **Ogni test in ordine** - Non saltare
2. **Compila risultati subito** - Non dopo
3. **Se FAIL** - Documenta PERCHE' e cosa fixare
4. **Usa multi-finestra** - E' il punto del test!

---

## PARTE 2: TEST MIRATI SUI QUICK WINS

Questi test verificano che ogni tool creato FUNZIONI REALMENTE.

---

## TEST QW1: ANTI-COMPACT SCRIPT

```bash
./scripts/swarm/anti-compact.sh --no-spawn --message "Test QW1"
```

### Checklist

- [ ] Script esegue senza errori
- [ ] PROMPT_RIPRESA.md aggiornato con AUTO-CHECKPOINT
- [ ] Git commit creato (se ci sono modifiche)
- [ ] Messaggio finale chiaro

**ESITO:** ____

---

## TEST QW2: SHUTDOWN SEQUENCE

```bash
./scripts/swarm/shutdown-sequence.sh --no-report
```

### Checklist

- [ ] Script esegue senza errori
- [ ] Verifica task attivi funziona
- [ ] Pulizia file temporanei funziona
- [ ] Messaggio finale chiaro

**ESITO:** ____

---

## TEST QW3: CHECKLIST PRE-MERGE

```bash
./scripts/swarm/checklist-pre-merge.sh --skip-tests
```

### Checklist

- [ ] Script esegue senza errori
- [ ] GATE 1 (Syntax) funziona
- [ ] GATE 2 (Lint) funziona
- [ ] GATE 4 (Human review) chiede conferma
- [ ] Output colorato e chiaro

**ESITO:** ____

---

## TEST QW4: TRIPLE ACK

```bash
# Creare task di test
python3 scripts/swarm/task_manager.py create TEST_ACK cervella-backend "Test ACK" 1

# Testare ACK
./scripts/swarm/triple-ack.sh received TEST_ACK
./scripts/swarm/triple-ack.sh understood TEST_ACK
./scripts/swarm/triple-ack.sh status TEST_ACK
```

### Checklist

- [ ] task_manager.py create funziona
- [ ] triple-ack.sh received funziona
- [ ] triple-ack.sh understood funziona
- [ ] triple-ack.sh status mostra R/U correttamente

**ESITO:** ____

---

## TEST QW5: DASHBOARD

```bash
python3 -m scripts.swarm.dashboard.cli
python3 -m scripts.swarm.dashboard.cli --json
```

### Checklist

- [ ] Dashboard ASCII si visualizza
- [ ] Mostra workers (anche se idle)
- [ ] --json produce output valido
- [ ] Nessun errore Python

**ESITO:** ____

---

## TEST QW6: PROGRESS BAR

```bash
python3 src/patterns/progress_bar.py
```

### Checklist

- [ ] Demo esegue senza errori
- [ ] Progress bar si visualizza
- [ ] 3 livelli (task, sprint, phase) funzionano
- [ ] Output colorato

**ESITO:** ____

---

## TEST QW7: CIRCUIT BREAKER

```bash
python3 src/patterns/example_usage.py
```

### Checklist

- [ ] Import funziona
- [ ] Esempio esegue
- [ ] Pattern circuit breaker dimostrabile

**ESITO:** ____

---

## TEST QW8: STRUCTURED LOGGING

```bash
python3 -c "from src.patterns import SwarmLogger; l = SwarmLogger('test'); l.info('Test message')"
```

### Checklist

- [ ] Import funziona
- [ ] Log in console funziona
- [ ] Formato JSON corretto

**ESITO:** ____

---

## TEST QW9: SPAWN WORKERS

```bash
./scripts/swarm/spawn-workers.sh --list
./scripts/swarm/spawn-workers.sh --backend
```

### Checklist

- [ ] --list mostra tutti i worker
- [ ] --backend apre nuova finestra Terminal
- [ ] Nuovo Claude Code si avvia
- [ ] Prompt worker iniettato

**ESITO:** ____

---

## TEST QW10: TASK MANAGER

```bash
python3 scripts/swarm/task_manager.py list
python3 scripts/swarm/task_manager.py create TEST_TM cervella-docs "Test task manager" 1
python3 scripts/swarm/task_manager.py ready TEST_TM
python3 scripts/swarm/task_manager.py list
```

### Checklist

- [ ] list funziona
- [ ] create crea file TASK
- [ ] ready crea file .ready
- [ ] Status aggiornato correttamente

**ESITO:** ____

---

## RIEPILOGO QUICK WINS

| Test | Tool | PASS/FAIL |
|------|------|-----------|
| QW1 | anti-compact.sh | |
| QW2 | shutdown-sequence.sh | |
| QW3 | checklist-pre-merge.sh | |
| QW4 | triple-ack.sh | |
| QW5 | dashboard.py | |
| QW6 | progress_bar.py | |
| QW7 | circuit_breaker.py | |
| QW8 | structured_logging.py | |
| QW9 | spawn-workers.sh | |
| QW10 | task_manager.py | |

**TOTALE QUICK WINS:** ___/10 PASS

---

## RIEPILOGO TOTALE

| Categoria | Passati | Totale |
|-----------|---------|--------|
| Test Generali (1-6) | | 6 |
| Test Quick Wins (QW1-10) | | 10 |
| **TOTALE** | | **16** |

### Criteri Finali

```
16/16 PASS -> PERFETTO! MIRACOLLO READY!
14-15/16   -> Ottimo, fix minori
12-13/16   -> Buono, review necessaria
<12/16     -> NON READY - Fix richiesti
```

---

*"Vogliamo MAGIA, non debugging!"*

*"Comodo != Giusto" - Lezione Sessione 72*

*"Noi abbiamo il mondo davanti a noi. Dobbiamo vederlo."*

*"SU CARTA != REALE" - Solo le cose REALI contano!*

---

Cervella & Rafa
Sessione 72 - 3 Gennaio 2026
