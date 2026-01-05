# Task: Implementare Worker Health Tracking System

**Assegnato a:** cervella-backend
**Stato:** ready
**Priorita:** ALTA
**Data:** 05 January 2026
**Creato da:** Regina (Sessione 91)

---

## Obiettivo

Implementare sistema di tracking per sapere se un worker e' vivo o morto, e pulire automaticamente task appesi.

---

## Problema Attuale

1. Worker spawna, inizia task, poi muore (crash, timeout Claude, ecc.)
2. Task rimane `.working` per sempre
3. La Regina non sa cosa e' successo
4. Nessun cleanup automatico

---

## Soluzione da Implementare

### 1. Modificare spawn-workers.sh (righe 379-460 circa)

Nel runner script, PRIMA di eseguire Claude:
```bash
# Salva PID e timestamp
echo $$ > "${SWARM_DIR}/status/worker_${WORKER_NAME}.pid"
date +%s > "${SWARM_DIR}/status/worker_${WORKER_NAME}.start"
```

DOPO che Claude termina (prima di chiudere finestra):
```bash
# Pulisci status
rm -f "${SWARM_DIR}/status/worker_${WORKER_NAME}.pid"
rm -f "${SWARM_DIR}/status/worker_${WORKER_NAME}.start"
```

### 2. Creare script ~/.local/bin/swarm-cleanup

Script che:
1. Trova tutti i task `.working`
2. Per ogni task:
   - Cerca file `.pid` corrispondente
   - Se PID non esiste O processo non in esecuzione → marca `.stale`
   - Se `.start` > 30 minuti fa → marca `.stale`
3. Notifica quanti task puliti

```bash
#!/bin/bash
# swarm-cleanup - Pulisce task orfani

SWARM_DIR=".swarm"
TIMEOUT_MINUTES=30

for working in ${SWARM_DIR}/tasks/*.working; do
    [[ -f "$working" ]] || continue

    task_name=$(basename "$working" .working)

    # Controlla se c'e' un PID attivo
    # Se no, marca come stale
    # ...
done
```

### 3. Integrare in hook SessionStart

In uno degli hook esistenti, chiamare `swarm-cleanup` all'inizio sessione.
Opzione: aggiungere a `~/.claude/hooks/context_check.py`

---

## File da Modificare

1. `~/.local/bin/spawn-workers` - Aggiungere PID/timestamp tracking
2. `~/.local/bin/swarm-cleanup` - NUOVO - Script cleanup
3. (Opzionale) Hook per auto-cleanup

---

## Test

1. Spawna un worker
2. Verifica che `.pid` e `.start` vengono creati in `.swarm/status/`
3. Quando worker termina, verifica che file vengono rimossi
4. Simula crash: `kill` il processo worker
5. Esegui `swarm-cleanup` e verifica che task viene marcato `.stale`

---

## Output

Scrivi risultato in `TASK_20260105_050500_worker_health_tracking_output.md`

---

## Checklist Verifica

- [ ] spawn-workers.sh modificato con PID tracking
- [ ] swarm-cleanup creato e funzionante
- [ ] Test passati (spawn, terminazione normale, simulazione crash)
- [ ] File .done creato

---

*Task creato dalla Regina - Sessione 91*
