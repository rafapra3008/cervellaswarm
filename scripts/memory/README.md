# 🐝 CervellaSwarm - Sistema Memoria

Sistema di memoria persistente per tracciare attività degli agenti CervellaSwarm.

**Versione:** 2.1.0
**Data:** 2026-01-01
**Script totali:** 10 (8 Python + 2 Shell)

---

## 📋 OVERVIEW

Questo sistema traccia:
- Eventi degli agenti (task start/complete/fail)
- Performance e statistiche
- Lezioni apprese dal team
- Pattern di lavoro
- Pattern di errori ricorrenti
- Analytics e reporting
- Suggerimenti automatici

**Database:** SQLite con WAL mode (performance ottimizzate)
**Path:** `data/swarm_memory.db`

---

## 🚀 SETUP

### 1. Inizializzazione

```bash
# Crea database e schema
./scripts/memory/init_db.py
```

Output:
```
✅ Database inizializzato: /path/to/swarm_memory.db
✅ Tabelle create: swarm_events, lessons_learned
✅ Indici creati: 7 totali
✅ WAL mode: attivo
```

### 2. Verifica

```bash
# Controlla statistiche (database vuoto)
./scripts/memory/query_events.py --stats
```

---

## 📊 SCRIPT DISPONIBILI

**Totali: 10 script (8 Python + 2 Shell)**

### 🔹 Core Scripts

#### init_db.py

Inizializza database con schema completo.

**Uso:**
```bash
./scripts/memory/init_db.py
```

**Schema creato:**
- Tabella `swarm_events` (eventi agenti)
- Tabella `lessons_learned` (lezioni apprese)
- 7 indici per query ottimizzate

---

#### log_event.py

Logga evento nel database (chiamato da hook PostToolUse).

**Input:** JSON da stdin (payload hook)

**Output:** JSON con status

**Esempio:**
```bash
echo '{
  "tool": {"name": "cervella-frontend", "input": {"task": "Fix bug"}},
  "result": {"file_path": "/path/to/file.js"},
  "context": {"cwd": "/project", "session_id": "abc123"}
}' | ./scripts/memory/log_event.py
```

**Gestione errori:**
- Exit 0 SEMPRE (non blocca workflow anche in caso di errore)
- Skip silenzioso se database non esiste
- Skip silenzioso se non è agent swarm

---

#### load_context.py

Carica contesto per SessionStart hook.

**Output:** JSON con `hookSpecificOutput.additionalContext`

**Uso:**
```bash
./scripts/memory/load_context.py
```

**Include:**
- Ultimi 10 eventi
- Statistiche per agent
- Lezioni apprese attive
- Suggerimenti automatici basati su pattern

**Versione:** 1.1.0 (aggiornato per supportare suggestions)

---

#### query_events.py

Script utility per interrogare il database.

**Opzioni:**

```bash
# Ultimi N eventi
./scripts/memory/query_events.py --recent 50

# Eventi per agent specifico
./scripts/memory/query_events.py --agent cervella-frontend

# Eventi per progetto
./scripts/memory/query_events.py --project miracollo

# Task falliti
./scripts/memory/query_events.py --failed

# Statistiche generali
./scripts/memory/query_events.py --stats

# Formato output (json o table)
./scripts/memory/query_events.py --stats --format table
```

---

### 🔹 Analytics Scripts

#### analytics.py

CLI completa per analytics con Rich formatting.

**Comandi:**

```bash
# Overview generale
python3 analytics.py summary

# Lista lezioni attive
python3 analytics.py lessons

# Ultimi eventi (default 10)
python3 analytics.py events

# Statistiche per agente
python3 analytics.py agents

# Pattern di errori
python3 analytics.py patterns

# Dashboard live con Rich
python3 analytics.py dashboard

# Auto-rileva pattern errori
python3 analytics.py auto-detect

# Weekly retrospective
python3 analytics.py retro
```

**Opzioni:**

```bash
# Numero eventi (per events)
python3 analytics.py events -n 50

# Giorni da analizzare (per auto-detect)
python3 analytics.py auto-detect -d 30

# Mostra versione
python3 analytics.py --version
```

**Output:**
- Formattazione colorata con Rich
- Tabelle e panel eleganti
- Metriche in tempo reale

**Versione:** 2.0.0 (29KB - CLI completa)

---

#### pattern_detector.py

Algoritmo detection pattern errori con `difflib.SequenceMatcher`.

**Uso come modulo:**

```python
from pattern_detector import detect_error_patterns, fetch_recent_errors, save_patterns_to_db

# Fetch errori recenti
errors = fetch_recent_errors(days=30)

# Rileva pattern
patterns = detect_error_patterns(
    errors,
    similarity_threshold=0.7,
    min_occurrences=3
)

# Salva in database
new, updated = save_patterns_to_db(patterns)
```

**Uso standalone:**

```bash
# Rileva e salva pattern automaticamente
python3 pattern_detector.py
```

**Algoritmo:**
- Similarità con `SequenceMatcher` (Python built-in)
- Soglia default: 70%
- Minimo occorrenze: 3
- Clustering automatico errori simili

**Versione:** 1.0.0 (11KB)

---

#### weekly_retro.py

Report retrospettiva settimanale automatico.

**Uso:**

```bash
# Ultimi 7 giorni
python3 weekly_retro.py

# Ultimi 14 giorni
python3 weekly_retro.py -d 14
```

**Output include:**
- Metriche chiave (eventi, successi, errori)
- Success rate percentuale
- Top 3 pattern errori
- Breakdown per agente
- Lezioni apprese della settimana
- Raccomandazioni automatiche

**Formato:** Rich formatting con panel e tabelle

**Versione:** 1.0.0 (10KB)

---

#### suggestions.py

Suggerimenti automatici basati su lezioni e pattern.

**Uso CLI:**

```bash
# Tutti i suggerimenti
python3 suggestions.py

# Filtro per progetto
python3 suggestions.py -p miracollo

# Filtro per agente
python3 suggestions.py -a frontend

# Limite numero suggerimenti
python3 suggestions.py -l 3

# Output JSON
python3 suggestions.py --json
```

**Uso come modulo:**

```python
from suggestions import get_suggestions

# Suggerimenti generici
suggestions = get_suggestions(limit=5)

# Suggerimenti per progetto specifico
suggestions = get_suggestions(project='miracollo', limit=5)

# Suggerimenti per agente specifico
suggestions = get_suggestions(agent='frontend', limit=3)
```

**Output esempio:**

```
💡 SUGGERIMENTI ATTIVI (1)
────────────────────────────────────────────────────────────
🟡 [MEDIUM] blind-retry (PROCESS)
   → Pattern: 1) Prova 2) Fallisce? STOP 3) Ricerca 4) Prova con info nuove

   Occorrenze: 3 volte
   Prevenzione: UNA VOLTA → RICERCA → MAI ALLA CIECA
```

**Severità:**
- CRITICAL (rosso)
- HIGH (arancione)
- MEDIUM (giallo)
- LOW (verde)

**Versione:** 1.0.0 (9KB)

---

### 🔹 Testing & Utilities

#### test_system.sh

Script di test automatico completo del sistema memoria.

**Uso:**
```bash
./scripts/memory/test_system.sh
```

**Cosa testa:**
1. ✅ **Inizializzazione database** - Crea DB e schema
2. ✅ **Log eventi** - Testa 3 eventi (frontend, backend, tester)
3. ✅ **Query database** - Verifica stats e query recenti
4. ✅ **Load context** - Testa caricamento contesto
5. ✅ **Verifica dati** - Conta eventi e agent nel DB

**Output:**
```
🧪 Test Sistema Memoria CervellaSwarm
======================================

✅ Test 1: Inizializzazione database
   ✓ Database creato
✅ Test 2: Log eventi
   ✓ Evento cervella-frontend loggato
   ✓ Evento cervella-backend loggato
   ✓ Evento cervella-tester loggato
✅ Test 3: Query database
   ✓ Query statistiche funziona
   ✓ Query eventi recenti funziona
✅ Test 4: Caricamento contesto
   ✓ Load context funziona
✅ Test 5: Verifica dati salvati
   ✓ Tutti e 3 gli eventi salvati
   ✓ Tutti e 3 gli agent tracciati

🎉 Tutti i test passati!

✅ Sistema Memoria funzionante al 100%!
```

**Quando usarlo:**
- Dopo setup iniziale (verifica che tutto funzioni)
- Prima di deploy (regression test)
- Dopo modifiche al sistema memoria

---

#### example_usage.sh

Guida interattiva con esempi pratici.

**Uso:**
```bash
./scripts/memory/example_usage.sh
```

**Cosa mostra:**
1. **Step 1:** Comando inizializzazione
2. **Step 2:** Esempio log evento
3. **Step 3:** Query database con esempi live
4. **Step 4:** Load contesto

**Output:**
```
🐝 CervellaSwarm - Esempio Utilizzo Sistema Memoria
======================================================

📋 Step 1: Inizializzazione (se non già fatto)
   ./scripts/memory/init_db.py

📋 Step 2: Log evento (automatico da PostToolUse hook)
   echo '{...payload...}' | ./scripts/memory/log_event.py

📋 Step 3: Query database
   🔹 Ultimi 10 eventi:
   [output live dal DB]

   🔹 Statistiche generali:
   [statistiche live dal DB]

📋 Step 4: Load contesto (automatico da SessionStart hook)
   ./scripts/memory/load_context.py

✅ Per documentazione completa: cat scripts/memory/README.md
```

**Quando usarlo:**
- Prima volta che usi il sistema (per capire come funziona)
- Per vedere esempi concreti di query
- Per verificare che il DB contenga dati

---

## 📦 SCHEMA DATABASE

### Tabella: swarm_events

| Campo | Tipo | Descrizione |
|-------|------|-------------|
| id | TEXT | UUID evento |
| timestamp | TEXT | ISO8601 |
| session_id | TEXT | ID sessione Claude |
| event_type | TEXT | task_start, task_complete, task_failed |
| agent_name | TEXT | cervella-frontend, backend, etc. |
| agent_role | TEXT | Ruolo agent |
| task_id | TEXT | UUID task |
| parent_task_id | TEXT | Per task annidati |
| task_description | TEXT | Descrizione task |
| task_status | TEXT | started, completed, failed |
| duration_ms | INTEGER | Tempo esecuzione |
| success | INTEGER | 1/0 |
| error_message | TEXT | Messaggio errore |
| project | TEXT | miracollo, contabilita, etc. |
| files_modified | TEXT | JSON array file |
| tags | TEXT | JSON array tag |
| notes | TEXT | Note libere |
| created_at | TEXT | Timestamp creazione |

**Indici:**
- idx_events_timestamp
- idx_events_agent
- idx_events_project
- idx_events_task_status
- idx_events_session

---

### Tabella: lessons_learned

| Campo | Tipo | Descrizione |
|-------|------|-------------|
| id | TEXT | UUID |
| timestamp | TEXT | ISO8601 |
| context | TEXT | Contesto problema |
| problem | TEXT | Problema riscontrato |
| solution | TEXT | Soluzione trovata |
| pattern | TEXT | Pattern identificato |
| agents_involved | TEXT | JSON array agenti |
| confidence | REAL | 0-1 |
| times_applied | INTEGER | Volte applicata |
| created_at | TEXT | Timestamp creazione |

**Indici:**
- idx_lessons_confidence
- idx_lessons_pattern

---

### Tabella: error_patterns

| Campo | Tipo | Descrizione |
|-------|------|-------------|
| id | TEXT | UUID |
| pattern_name | TEXT | Nome pattern (es. "blind-retry") |
| pattern_type | TEXT | Tipo pattern (es. "PROCESS") |
| severity_level | TEXT | CRITICAL, HIGH, MEDIUM, LOW |
| occurrence_count | INTEGER | Numero occorrenze rilevate |
| status | TEXT | ACTIVE, RESOLVED, ARCHIVED |
| last_seen | TEXT | Ultima volta visto (ISO8601) |
| root_cause_hypothesis | TEXT | Ipotesi causa root |
| mitigation_description | TEXT | Come mitigare/prevenire |
| created_at | TEXT | Timestamp creazione |

**Indici:**
- idx_patterns_status
- idx_patterns_severity

**Note:**
- Popolata automaticamente da `pattern_detector.py`
- Usata da `suggestions.py` per generare suggerimenti
- Aggiornata da `analytics.py auto-detect`

---

## 🔗 INTEGRAZIONE CON HOOK

### PostToolUse Hook

```json
{
  "hookName": "PostToolUse",
  "executable": "./scripts/memory/log_event.py"
}
```

**Comportamento:**
- Riceve payload hook via stdin
- Logga evento se è agent swarm
- Skip silenzioso altrimenti
- Exit 0 SEMPRE (non blocca workflow)

---

### SessionStart Hook

```json
{
  "hookName": "SessionStart",
  "executable": "./scripts/memory/load_context.py"
}
```

**Comportamento:**
- Carica contesto memoria
- Output JSON con additionalContext
- Include ultimi eventi + statistiche + lezioni

---

## 📊 ESEMPI

### Verificare Attività Agent

```bash
# Tutti gli eventi di cervella-frontend
./scripts/memory/query_events.py --agent cervella-frontend

# Ultimi 100 eventi
./scripts/memory/query_events.py --recent 100

# Eventi solo progetto Miracollo
./scripts/memory/query_events.py --project miracollo
```

### Analizzare Performance

```bash
# Statistiche generali
./scripts/memory/query_events.py --stats

# Task falliti
./scripts/memory/query_events.py --failed

# Dashboard live con Rich
python3 analytics.py dashboard

# Report settimanale
python3 weekly_retro.py
```

### Pattern e Suggerimenti

```bash
# Rileva pattern errori automaticamente
python3 pattern_detector.py

# Mostra pattern rilevati
python3 analytics.py patterns

# Suggerimenti per evitare errori
python3 suggestions.py

# Suggerimenti per progetto specifico
python3 suggestions.py -p miracollo
```

### Debug

```bash
# Output tabella (più leggibile)
./scripts/memory/query_events.py --recent 10 --format table

# Eventi con dettagli completi
python3 analytics.py events -n 20
```

---

## 🛠️ MANUTENZIONE

### Backup Database

```bash
# Copia database
cp data/swarm_memory.db data/swarm_memory.db.backup
```

### Reset Database

```bash
# Elimina e ricrea
rm data/swarm_memory.db
./scripts/memory/init_db.py
```

### Ottimizzazione

```bash
# SQLite VACUUM (compatta database)
sqlite3 data/swarm_memory.db "VACUUM;"
```

---

## ⚠️ NOTE IMPORTANTI

1. **Gestione Errori:**
   - Tutti gli script gestiscono errori gracefully
   - Exit 0 anche in caso di errore (non bloccare workflow)
   - Log errori su stderr

2. **Performance:**
   - WAL mode per scritture concorrenti
   - Indici su campi più usati
   - Database separato (non interferisce con progetti)

3. **Privacy:**
   - Task description limitata a 200 char
   - Solo path file (non contenuto)
   - Session ID opzionale

---

## 🎯 ROADMAP FUTURA

- [x] ~~Pattern detection automatico~~ (v2.0.0 - COMPLETATO)
- [x] ~~Analytics e reporting~~ (v2.0.0 - COMPLETATO)
- [x] ~~Suggerimenti automatici~~ (v2.0.0 - COMPLETATO)
- [x] ~~Weekly retrospective~~ (v2.0.0 - COMPLETATO)
- [ ] Web UI per visualizzare statistiche
- [ ] Grafici performance agenti
- [ ] Machine learning avanzato per predizioni
- [ ] Export report PDF
- [ ] Integrazione Telegram notifiche eventi critici

---

**Creato:** 2026-01-01
**Ultimo Aggiornamento:** 2026-01-01 (v2.1.0 - Documentazione script shell completa)
**Parte di:** CervellaSwarm v1.0.0

💙🐝 *Cervella Docs - La Documentatrice dello Sciame*
