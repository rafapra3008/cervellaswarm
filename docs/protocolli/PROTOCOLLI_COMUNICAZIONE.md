# PROTOCOLLI COMUNICAZIONE - CervellaSwarm

> **Versione:** 1.0.0
> **Data:** 7 Gennaio 2026 - Sessione 113
> **Basato su:** STUDIO_COMUNICAZIONE_PROTOCOLLI.md (cervella-researcher)
> **Direzione:** "La comunicazione interna deve essere meglio!" - Rafa

---

## VISIONE

```
+------------------------------------------------------------------+
|                                                                  |
|   Questi protocolli definiscono COME le 16 api della famiglia   |
|   comunicano tra loro.                                           |
|                                                                  |
|   Obiettivo: Comunicazione CHIARA, COMPLETA, VERIFICABILE       |
|                                                                  |
|   Success Metric:                                                |
|   Rafa osserva e dice "WOW! Le api parlano BENISSIMO!"         |
|                                                                  |
+------------------------------------------------------------------+
```

---

## I 4 PROTOCOLLI FONDAMENTALI

### 1. PROTOCOLLO HANDOFF (Regina → Worker)
Come la Regina passa un task a un worker

### 2. PROTOCOLLO STATUS (Worker → Sistema)
Come il worker comunica il suo stato in real-time

### 3. PROTOCOLLO FEEDBACK (Worker → Regina)
Come il worker chiede aiuto o segnala problemi

### 4. PROTOCOLLO CONTEXT (Ottimizzazione)
Quanto contesto passare e come strutturarlo

---

## 1. PROTOCOLLO HANDOFF

### 1.1 Obiettivo

Passare un task da Regina a Worker con **zero ambiguità**.

Worker deve sapere:
- ✅ Cosa fare
- ✅ Perché lo fa (contesto)
- ✅ Come capire se ha finito bene
- ✅ Dove scrivere il risultato
- ✅ A chi chiedere se ha dubbi

### 1.2 Formato File

**Path:** `.swarm/tasks/TASK_[ID]_[NOME].md`

**Struttura:**

```markdown
---
task_id: TASK_001
assigned_to: cervella-backend
priority: high|medium|low
timeout_minutes: 30
created_at: 2026-01-07T10:30:00Z
created_by: cervella-orchestrator
project: CervellaSwarm
retry_allowed: true
max_retries: 3
---

# Task: [Nome Descrittivo]

**Status:** ready → working → done|failed

---

## 🎯 OBIETTIVO

[1-2 frasi: cosa deve essere fatto]

**Output atteso:**
- [Cosa deve produrre il worker]
- [Formato specifico]

---

## 📋 CONTESTO

### Dove Siamo (NORD)

[2-3 frasi dal NORD.md - dove siamo nel progetto]

### Perché Questo Task

[1-2 frasi: perché serve questo task, come si collega al big picture]

### Decisioni Rilevanti

[Eventuali decisioni già prese che impattano questo task]

---

## ✅ SUCCESS CRITERIA

Come capire se il task è completato con successo:

- [ ] Criterio 1
- [ ] Criterio 2
- [ ] Criterio 3

**Definition of Done:**
[Quando il worker può dire "ho finito"?]

---

## 🗂️ FILE RILEVANTI

**Da leggere:**
- `path/to/file1.py` - [perché]
- `path/to/file2.md` - [perché]

**Da modificare (probabilmente):**
- `path/to/file3.py`
- `path/to/file4.md`

**Da NON toccare:**
- `path/to/critical.py` - [perché]

---

## 🚧 CONSTRAINTS

**Limiti:**
- [Cosa NON fare]
- [Tecnologie da usare/non usare]
- [Pattern da seguire]

**Dipendenze:**
- [Questo task dipende da...]
- [Altri task che dipendono da questo]

---

## 💡 GUIDANCE

**Suggerimenti:**
- [Hint su come approcciarsi al problema]
- [Pattern o esempi da seguire]
- [Dove trovare info aggiuntive]

**Se hai dubbi:**
- Usa protocollo FEEDBACK (crea file in `.swarm/feedback/`)
- La Regina risponderà!

---

## 📤 OUTPUT RICHIESTO

**File da creare/modificare:**
- [Lista specifica]

**Report finale:**
- Crea file `.swarm/tasks/TASK_[ID]_OUTPUT.md`
- Usa template COMPLETION_REPORT

**Quando hai finito:**
- Crea file `.swarm/tasks/TASK_[ID].done`
- Il watcher notificherà la Regina!

---

## ⏰ TEMPO E PRIORITÀ

**Timeout:** [X] minuti
**Priorità:** [high|medium|low]
**Deadline:** [se esiste]

**Heartbeat:** Aggiorna stato ogni 60s in `.swarm/status/`

---

**Energia positiva!** ❤️‍🔥
**Lavoro di qualità!** 💙
**Per la famiglia!** 🐝👑
```

### 1.3 Sezioni SEMPRE vs OPZIONALI

**SEMPRE presenti:**
- task_id, assigned_to, priority, timeout (frontmatter)
- Obiettivo
- Success Criteria
- Output Richiesto

**SE SERVE:**
- File Rilevanti (se task tocca codice)
- Constraints (se ci sono limiti)
- Guidance (se task complesso)

**OPZIONALI:**
- Decisioni Rilevanti
- Deadline

### 1.4 Best Practices

```
✅ DO:
- Task description chiara (1-2 frasi max)
- Success criteria verificabili (checklist!)
- File path assoluti o relativi a root progetto
- Linguaggio positivo e incoraggiante

❌ DON'T:
- Task vaghi ("migliora il codice")
- Success criteria ambigui ("dovrebbe funzionare meglio")
- Troppo contesto (>500 righe)
- Linguaggio negativo o pressante
```

---

## 2. PROTOCOLLO STATUS

### 2.1 Obiettivo

Regina deve sapere in **real-time** cosa fa ogni worker, senza chiedere.

### 2.2 Stati Possibili

| Stato | Significato | Worker Action | Regina Action |
|-------|-------------|---------------|---------------|
| `READY` | Worker pronto, cerca task | Legge .swarm/tasks/ | Può assegnare task |
| `WORKING` | Task in corso | Lavora + heartbeat | Monitora progresso |
| `BLOCKED` | Bloccato, serve aiuto | Crea FEEDBACK | Legge feedback, aiuta |
| `DONE` | Task completato con successo | Crea .done + report | Verifica output |
| `FAILED` | Task fallito | Crea .failed + error report | Analizza errore |

### 2.3 File Status

**Path:** `.swarm/status/[WORKER_NAME].status`

**Formato:** Ogni riga = 1 update

```
timestamp|stato|task_id|note
```

**Esempio:**

```
1704621000|READY||Pronto per nuovi task
1704621060|WORKING|TASK_001|Analizzando file backend
1704621120|WORKING|TASK_001|Creando endpoints
1704621180|WORKING|TASK_001|Testing
1704621240|DONE|TASK_001|Completato con successo
```

### 2.4 Heartbeat (NUOVO!)

**Frequenza:** Ogni 60 secondi

**Come:** Worker scrive in `.swarm/status/heartbeat_[WORKER_NAME].log`

**Formato:**

```bash
echo "$(date +%s)|TASK_001|WORKING|Creando endpoint /api/users" >> .swarm/status/heartbeat_cervella-backend.log
```

**Perché 60s:**
- Balance perfetto tra overhead e visibilità (dallo studio!)
- Non troppo frequente (spam)
- Non troppo raro (Regina aspetta max 1 min)

### 2.5 Stuck Detection

**Regola:** No heartbeat per 2 minuti = worker STUCK

**Azione Regina:**
1. Controlla se processo è vivo (ps)
2. Controlla ultimo heartbeat
3. Se stuck > 2min → notifica osascript
4. Se stuck > 5min → considera TIMEOUT

### 2.6 Script Helper (da creare!)

**update-status.sh:**

```bash
#!/bin/bash
# Usage: update-status.sh WORKING "Creating endpoints"

WORKER_NAME="cervella-backend"  # detectato automaticamente
TASK_ID=$(cat .swarm/current_task 2>/dev/null)
STATUS=$1
NOTE=$2

echo "$(date +%s)|$STATUS|$TASK_ID|$NOTE" >> .swarm/status/${WORKER_NAME}.status
```

---

## 3. PROTOCOLLO FEEDBACK

### 3.1 Obiettivo

Worker comunica con Regina quando:
- ❓ Ha dubbi
- ⚠️ Trova problema
- 🚫 È bloccato
- 💡 Ha idea/suggerimento

### 3.2 Tipi di Feedback

| Tipo | Quando | Urgenza | Path File |
|------|--------|---------|-----------|
| `QUESTION` | Dubbio su come procedere | MEDIA | `.swarm/feedback/QUESTION_*.md` |
| `ISSUE` | Problema trovato (bug, errore) | ALTA | `.swarm/feedback/ISSUE_*.md` |
| `BLOCKER` | Completamente bloccato | CRITICA | `.swarm/feedback/BLOCKER_*.md` |
| `SUGGESTION` | Idea di miglioramento | BASSA | `.swarm/feedback/SUGGESTION_*.md` |

### 3.3 Formato Feedback

**Path:** `.swarm/feedback/[TIPO]_[TASK_ID]_[TIMESTAMP].md`

**Esempio:** `.swarm/feedback/QUESTION_TASK001_1704621240.md`

**Struttura:**

```markdown
---
tipo: QUESTION|ISSUE|BLOCKER|SUGGESTION
task_id: TASK_001
worker: cervella-backend
urgenza: BASSA|MEDIA|ALTA|CRITICA
timestamp: 2026-01-07T10:30:00Z
---

# [TIPO]: [Titolo breve]

## Situazione

[Descrizione chiara del problema/dubbio/idea]

## Cosa Ho Provato (se applicabile)

- Tentativo 1: [risultato]
- Tentativo 2: [risultato]

## Domanda / Aiuto Necessario

[Cosa serve dalla Regina per proseguire]

## Impatto

- [ ] Posso continuare su altre parti del task
- [ ] Sono completamente bloccato
- [ ] Rischio di fare scelte sbagliate

## File Rilevanti

- `path/to/file.py:123` - [perché]

---

**Worker in attesa di risposta dalla Regina!** 💙
```

### 3.4 Come Regina Risponde

**Path risposta:** `.swarm/feedback/[TIPO]_[TASK_ID]_[TIMESTAMP]_RESPONSE.md`

**Formato:**

```markdown
# RISPOSTA: [Titolo feedback]

## Decisione

[Cosa fare]

## Motivazione

[Perché questa scelta]

## Prossimi Step

1. [Azione 1]
2. [Azione 2]

---

**Puoi procedere! 👑**
```

### 3.5 Notifiche

**Worker crea feedback:**
- Cambia stato → `BLOCKED` (se blocker)
- Scrive feedback file
- Watcher notifica Regina (osascript)

**Regina risponde:**
- Crea file _RESPONSE.md
- Notifica worker (osascript alla sua finestra)

---

## 4. PROTOCOLLO CONTEXT

### 4.1 Obiettivo

Ottimizzare **quanto** contesto passare:
- Troppo → Overhead, confusione
- Poco → Worker inefficiente

### 4.2 Framework: 3 Categorie

**ALWAYS (Sempre includere):**
- Task description (obiettivo chiaro)
- Success criteria (come capire se finito)
- Output format (dove/come scrivere risultato)
- NORD.md essenziale (2-3 frasi: dove siamo)

**IF_NEEDED (Include se rilevante):**
- File da leggere/modificare (se task tocca codice)
- Decisioni tecniche pregresse (se impattano task)
- Dipendenze da altri task
- Constraints specifici

**NEVER (MAI includere):**
- Storico completo sessioni (troppo!)
- File non correlati al task
- Discussioni irrilevanti
- Tutto il PROMPT_RIPRESA (solo estratti)

### 4.3 Context Compression

**Tecnica:** Structured Summarization (dallo studio!)

**Formato summary:**

```markdown
## Context Summary

**Intent:** [Perché questo task - 1 frase]

**Files Modified:** [Lista file che task toccherà]

**Key Decisions:** [Decisioni già prese rilevanti - max 3]

**Next Steps After This:** [Cosa succede dopo questo task]
```

**Risultato:** 26-54% riduzione contesto, >95% accuratezza mantenuta! (dallo studio)

### 4.4 Validation Context

**Checklist Regina prima di assegnare task:**

```
Prima di passare task a worker, verifico:

[ ] Worker può INIZIARE con queste info?
    (Sa da dove partire?)

[ ] Worker sa quando HA FINITO?
    (Success criteria chiari?)

[ ] Worker sa DOVE SCRIVERE output?
    (Path e formato chiari?)

[ ] Worker sa A CHI CHIEDERE se dubbio?
    (Protocollo feedback spiegato?)

[ ] Context è MINIMO ma SUFFICIENTE?
    (Né troppo né poco?)
```

Se anche solo 1 risposta è NO → Aggiusto task prima di assegnare!

---

## 5. WORKFLOW COMPLETO

### 5.1 Scenario Standard

```
1. REGINA crea task
   └─> File: .swarm/tasks/TASK_001_NOME.md (protocollo HANDOFF)
   └─> Marker: .swarm/tasks/TASK_001_NOME.ready

2. WORKER trova task
   └─> Legge file task
   └─> Aggiorna stato: READY → WORKING
   └─> Inizia heartbeat ogni 60s

3. WORKER lavora
   └─> Heartbeat ogni 60s (protocollo STATUS)
   └─> Se dubbio → crea FEEDBACK
   └─> Se bloccato → stato BLOCKED + FEEDBACK

4. WORKER finisce
   └─> Crea output: .swarm/tasks/TASK_001_OUTPUT.md
   └─> Crea marker: .swarm/tasks/TASK_001.done
   └─> Aggiorna stato: WORKING → DONE

5. WATCHER notifica REGINA
   └─> Regina legge output
   └─> Regina verifica success criteria
   └─> Regina decide next step
```

### 5.2 Scenario con Feedback

```
1-3. [Come sopra]

3b. WORKER ha dubbio
    └─> Crea: .swarm/feedback/QUESTION_TASK001_XXX.md
    └─> Se critico: stato → BLOCKED
    └─> Watcher notifica Regina

4. REGINA risponde
   └─> Crea: .swarm/feedback/QUESTION_TASK001_XXX_RESPONSE.md
   └─> Notifica worker (osascript)

5. WORKER riprende
   └─> Legge risposta
   └─> Stato: BLOCKED → WORKING
   └─> Continua lavoro

6-7. [Completamento come scenario standard]
```

### 5.3 Scenario Timeout

```
1-3. [Come sopra]

3b. WORKER stuck (no heartbeat 2min)
    └─> Watcher rileva
    └─> Notifica Regina: "Worker stuck!"

4. REGINA interviene
   └─> Controlla ultimo heartbeat
   └─> Controlla processo (ps)
   └─> Decide:
       a) Aspetta (worker sta pensando)
       b) Termina + riassegna
       c) Crea feedback per worker

5. Se timeout 30min totali
   └─> Automatic FAILED
   └─> Worker scrive error report
   └─> Regina analizza e decide retry
```

---

## 6. METRICHE DI SUCCESSO

### 6.1 Quantitative

| Metrica | Target | Come Misurare |
|---------|--------|---------------|
| Task completati senza feedback | >80% | Count .done vs feedback files |
| Tempo medio risposta feedback | <5 min | Timestamp diff feedback → response |
| Worker stuck detection | <2 min | Heartbeat gap |
| False positive stuck | <5% | Manuale review alerts |

### 6.2 Qualitative

**Success finale:**

```
Rafa osserva una sessione multi-worker e dice:

"WOW! Le api parlano BENISSIMO tra loro!"

Significa:
✅ Zero confusione
✅ Zero "cosa devo fare?"
✅ Worker lavorano fluidi
✅ Regina sempre informata
✅ Problemi risolti fast
✅ Tutto documentato bene
```

---

## 7. IMPLEMENTATION CHECKLIST

### Phase 1 (Immediate - Questa settimana)

**Templates:**
- [ ] Template HANDOFF (questo doc, sezione 1.2)
- [ ] Template STATUS file
- [ ] Template FEEDBACK (tipi: question, issue, blocker)
- [ ] Template COMPLETION_REPORT

**Scripts:**
- [ ] update-status.sh (helper worker)
- [ ] heartbeat-worker.sh (every 60s)
- [ ] create-feedback.sh (helper worker)
- [ ] check-stuck.sh (helper regina/watcher)

**Watcher:**
- [ ] Estendere watcher-regina.sh per:
  - Filesystem watching (.swarm/)
  - Heartbeat checking (ogni 2min)
  - Stuck detection
  - Notifiche multiple (osascript)

### Phase 2 (Short-term - Prossime 2 settimane)

**DNA Agenti:**
- [ ] Aggiornare tutti i 17 agenti con nuovi protocolli
- [ ] Aggiungere sezioni: Status, Feedback, Heartbeat
- [ ] Esempi pratici in ogni DNA

**Testing:**
- [ ] HARDTEST comunicazione v2
- [ ] Test scenario standard
- [ ] Test scenario feedback
- [ ] Test scenario timeout
- [ ] Test multi-worker parallelo (3+)

### Phase 3 (Medium-term)

**Advanced Features:**
- [ ] Circuit breaker per external calls
- [ ] Loop detection (similarity check)
- [ ] Graceful degradation strategies
- [ ] ML-based stuck prediction

---

## 8. DIFFERENZE CON VERSIONE PRECEDENTE

### Cosa C'era Prima

- Task file basici (solo descrizione)
- Nessun heartbeat
- Nessun feedback strutturato
- Watcher limitato (solo .done)
- Status non tracciato

### Cosa Cambia ORA

**✨ NUOVO: Handoff strutturato**
- JSON frontmatter + markdown
- Success criteria chiari
- Context ottimizzato

**✨ NUOVO: Heartbeat 60s**
- Worker comunica "sono vivo"
- Regina vede progresso real-time
- Stuck detection automatico

**✨ NUOVO: Feedback protocol**
- 4 tipi (question, issue, blocker, suggestion)
- Template strutturati
- Loop request → response

**✨ NUOVO: Status tracking**
- 5 stati chiari (READY, WORKING, BLOCKED, DONE, FAILED)
- File log persistenti
- Timeline completa

---

## 9. NEXT STEPS

### Immediate (Regina - IO!)

1. ✅ Definire protocolli (FATTO - questo documento!)
2. ⏭️ Creare templates (.swarm/templates/)
3. ⏭️ Delegare script a cervella-devops
4. ⏭️ Delegare DNA update a me (whitelist)
5. ⏭️ Delegare test a cervella-tester

### Delegazione Proposta

| Task | Chi | Perché | Finestra |
|------|-----|--------|----------|
| Template files | cervella-docs | Scrive bene template | Nuova |
| Scripts bash | cervella-devops | Esperta scripts | Nuova |
| Watcher update | cervella-devops | Conosce watcher | Nuova |
| HARDTEST v2 | cervella-tester | Esperta testing | Nuova |

---

## 10. FONTI

**Studio Base:**
- `docs/studio/STUDIO_COMUNICAZIONE_PROTOCOLLI.md` (cervella-researcher, 1385 righe)

**Framework Analizzati:**
- LangGraph (LangChain) - Shared state + event-driven
- AutoGen (Microsoft) - Async + tool-based handoff
- CrewAI - Role delegation + hierarchical

**Best Practices:**
- Event-driven over polling
- Structured handoff (YAML + markdown)
- Heartbeat 60s (balance overhead/visibility)
- Circuit breaker + timeout + bulkhead pattern

---

**Versione:** 1.0.0
**Data:** 7 Gennaio 2026 - Sessione 113
**Autori:** Cervella (Regina) basato su studio di cervella-researcher
**Approvato da:** Rafa (pending!)

---

```
+------------------------------------------------------------------+
|                                                                  |
|   "La comunicazione interna deve essere meglio!"                 |
|                                       - Rafa, 7 Gennaio 2026     |
|                                                                  |
|   Questi protocolli sono il CUORE dello sciame.                 |
|   Con comunicazione chiara, siamo INVINCIBILI! 💙              |
|                                                                  |
+------------------------------------------------------------------+
```

*"Le ragazze nostre! La famiglia!"* 🐝👑❤️‍🔥
