# Analisi Sistema di Logging CervellaSwarm

**Status**: ISSUES  
**Health**: 6/10  
**Analista**: cervella-ingegnera  
**Data**: 14 Gennaio 2026

## Executive Summary

Sistema di logging **PRESENTE ma SOTTOUTILIZZATO**.

**Top 3 Problemi**:
1. MEDIO - Logging strutturato disponibile ma NON usato dai worker
2. MEDIO - Log worker sono plain text, difficili da analizzare
3. BASSO - Accumulazione log senza rotazione automatica (6.1MB totali)

## Sistema Trovato

### 1. Structured Logging (PRESENTE, non usato)

**File**: `src/patterns/structured_logging.py`

```python
class SwarmLogger:
    """JSON logging per CervellaSwarm"""
    # Output: logs/swarm_YYYY-MM-DD.jsonl
    # Formato: {timestamp, level, agent, task_id, message, extra}
```

**Funzionalita**:
- Log in formato JSON Lines
- Separazione console/file
- Filtri per agent/level/task_id
- Supporto campi extra strutturati

**Problema**: Worker NON lo usano! Log worker sono plain text.

### 2. Log Worker (.swarm/logs/)

**Tipo**: Plain text output
**Volume**: ~488KB (156+ file)
**Pattern**: `worker_{agent}_{timestamp}.log`

**Contenuto**: Output sessione worker (brevissimo, 1-5 righe)

```
Esempio:
"L'unico task .ready rimasto e TASK_CODE_REVIEW..."
"WORKER_DONE"
```

**Problema**: 
- Non strutturato
- Difficile analizzare
- Non traccia operazioni dettagliate

### 3. Heartbeat Logs (.swarm/status/)

**Tipo**: Timestamp tracking
**Pattern**: `heartbeat_{agent}.log`

```
1767723755|TASK_STUDIO_MULTI_PROGETTO|Analizzando spawn-workers
1767723779|TASK_STUDIO_MULTI_PROGETTO|Analizzando .swarm structure
```

**Utilita**: ALTA - traccia progresso task in real-time

### 4. Event Logging (Database)

**File**: `scripts/memory/log_event.py`

**Sistema**: SQLite database per eventi swarm
- Integrato con hook PostToolUse
- Traccia: agent, task, file modificati, durata
- Query analytics possibili

**Problema**: NON verificato se database esiste/e usato

### 5. Hook Debug Logs (data/logs/)

**File**: 
- `hook_debug.log` (1.9MB)
- `subagent_stop_debug.log` (3.0MB)

**Contenuto**: Debug hook SubagentStop (JSON payload)

**Problema**: GRANDI, nessuna rotazione, debug noise

### 6. Engineer Reports (reports/)

**Pattern**: `engineer_report_{timestamp}.json`
**Volume**: 260 file in archive/
**Contenuto**: Analisi codebase automatiche (JSON strutturato)

**Utilita**: ALTA - storico analisi qualita codice

### 7. Swarm JSONL Logs (logs/)

**File**: `logs/swarm_2026-01-03.jsonl`
**Contenuto**: Demo structured logging (esempi pattern)

**Problema**: Solo demo, NON log produzione reali

## Cosa Traccia il Sistema

| Sistema | Traccia | Utilita | Problemi |
|---------|---------|---------|----------|
| SwarmLogger | Eventi strutturati JSON | Alta | Non usato |
| Worker logs | Output sessioni | Bassa | Plain text |
| Heartbeat | Progresso task | Alta | OK |
| Event DB | Operazioni agent | Alta | Da verificare |
| Hook debug | Debug hooks | Bassa | Troppo verbose |
| Engineer reports | Qualita codice | Alta | OK |

## Lacune Identificate

### CRITICHE
Nessuna critica

### ALTE
1. **Worker non usano structured logging**
   - Worker scrivono plain text
   - Impossibile analizzare programmaticamente
   - Manca correlazione task/operazioni

2. **Event database non verificato**
   - Sistema esiste ma non verificato se attivo
   - Manca dashboard per visualizzare eventi
   - Potenzialmente ricco di dati non sfruttati

### MEDIE
3. **Log rotation mancante/non automatica**
   - Script `log-rotate.sh` esiste ma NON schedulato
   - 6.1MB log accumulati
   - Hook debug log crescono indefinitamente

4. **Manca aggregazione log multi-worker**
   - Log sparsi in directory diverse
   - Difficile visione d'insieme sessione
   - Nessun tool per correlazione temporale

### BASSE
5. **Reports non consolidati**
   - 260 engineer reports in archive
   - Nessun trend analysis automatico
   - Potenziale spreco di insights

## Raccomandazioni

### Priority 1: ALTA
- [ ] Migrare worker a `SwarmLogger` strutturato
- [ ] Verificare stato Event Database + creare query analytics
- [ ] Schedulare `log-rotate.sh` (cron/launchd)

### Priority 2: MEDIA
- [ ] Creare script aggregazione log sessione
- [ ] Dashboard per visualizzare eventi DB
- [ ] Implementare log retention policy (es: 30 giorni)

### Priority 3: BASSA
- [ ] Trend analysis engineer reports
- [ ] Cleanup hook debug logs (disabilitare in prod?)
- [ ] Documentare log locations per onboarding

## File Chiave da Conoscere

```
LOGGING INFRASTRUCTURE:
src/patterns/structured_logging.py  # SwarmLogger (non usato)
scripts/memory/log_event.py         # Event DB logger
scripts/swarm/log-rotate.sh         # Rotazione (manuale)
scripts/swarm/swarm-logs.sh         # Viewer log worker

LOG LOCATIONS:
.swarm/logs/                        # Worker session output
.swarm/status/heartbeat_*.log       # Progresso task
data/logs/                          # Hook debug (verbose!)
logs/                               # Structured logs (solo demo)
reports/                            # Engineer analysis
reports/archive/                    # Old engineer reports

ANALYSIS TOOLS:
scripts/engineer/analyze_codebase.py  # Auto codebase analysis
dashboard/api/routes/events.py        # SSE per monitoring
```

## Metriche Sistema

```
Total log files: 156+ (.swarm/logs/)
Total size: ~6.1MB
  - .swarm/logs/: 488KB
  - logs/: 60KB  
  - data/logs/: 5.6MB (DEBUG NOISE!)

Retention: Nessuna policy automatica
Rotation: Script esistente ma NON schedulato
Format: Mix (JSON, plain text, structured)
```

## Next Steps

1. **Verificare Event DB**:
   ```bash
   sqlite3 ~/.cervellaswarm/swarm_memory.db "SELECT COUNT(*) FROM swarm_events"
   ```

2. **Test SwarmLogger con worker**:
   - Modificare runner template
   - Provare con 1 worker
   - Validare output JSON

3. **Schedulare rotazione**:
   ```bash
   # Aggiungere a crontab
   0 2 * * * cd ~/Developer/CervellaSwarm && scripts/swarm/log-rotate.sh
   ```

## Conclusioni

Sistema logging **ARCHITETTURA BUONA** ma **IMPLEMENTAZIONE PARZIALE**.

**Punti Forza**:
- Structured logging gia progettato
- Event database per analytics
- Heartbeat tracking efficace
- Engineer reports automatici

**Da Migliorare**:
- Adozione structured logging
- Rotazione automatica
- Consolidamento log locations
- Dashboard visualizzazione

**Verdict**: Sistema promettente, serve completare l'integrazione!

---

*Cervella Ingegnera - 14 Gennaio 2026*  
*"Il logging e la memoria del sistema. Trattiamola bene!"*
