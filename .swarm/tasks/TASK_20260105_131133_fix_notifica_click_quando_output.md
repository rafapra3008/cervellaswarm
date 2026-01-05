# Output: FIX NOTIFICA CLICK

**Task:** TASK_20260105_131133_fix_notifica_click_quando
**Worker:** cervella-backend
**Data:** 05 January 2026
**Esito:** COMPLETATO

---

## Problema Risolto

Quando cliccavi sulla notifica del worker terminato, si apriva Console.app con il file `.log`.
Ora invece si apre il file `_output.md` del task completato (molto piu utile!).

---

## Modifiche Apportate

**File:** `scripts/swarm/spawn-workers.sh`

### 1. Versione aggiornata
- Da: 2.4.0
- A: 2.5.0

### 2. Nuova logica per trovare l'output (righe 509-538)

```bash
# v2.5.0: Trova l'ultimo task completato
TASK_OUTPUT_FILE=""

# Metodo 1: Leggi da file .task scritto dal worker
TASK_FILE="${SWARM_DIR}/status/worker_${WORKER_NAME}.task"
if [ -f "$TASK_FILE" ]; then
    TASK_NAME=$(cat "$TASK_FILE")
    POTENTIAL_OUTPUT="${SWARM_DIR}/tasks/${TASK_NAME}_output.md"
    if [ -f "$POTENTIAL_OUTPUT" ]; then
        TASK_OUTPUT_FILE="$POTENTIAL_OUTPUT"
    fi
fi

# Metodo 2 (fallback): Cerca .done piu recente
if [ -z "$TASK_OUTPUT_FILE" ]; then
    LATEST_DONE=$(ls -t "${SWARM_DIR}/tasks/"*.done | head -1)
    # ... deriva output da li
fi

# Metodo 3 (fallback finale): usa il log
if [ -z "$TASK_OUTPUT_FILE" ]; then
    TASK_OUTPUT_FILE="$LOG_FILE"
fi
```

### 3. Aggiornate istruzioni worker (righe 160-168)

Ora i worker devono scrivere il TASK_ID quando prendono un task:
```bash
echo "TASK_123" > .swarm/status/worker_backend.task
```

### 4. Terminal-notifier ora apre l'output

```bash
terminal-notifier \
    -open "file://${TASK_OUTPUT_FILE}"  # Era: ${LOG_FILE}
```

---

## Gerarchia Fallback

1. **Preferito:** File `.swarm/status/worker_NOME.task` scritto dal worker
2. **Fallback:** File `.done` piu recente in `.swarm/tasks/`
3. **Fallback finale:** File `.log` (comportamento precedente)

---

## Come Testare

1. Crea un task per un worker
2. Spawna il worker con `spawn-workers --backend`
3. Aspetta che completi
4. Clicca sulla notifica
5. Dovrebbe aprirsi il file `_output.md` invece di Console.app!

---

## Note

- Il worker deve seguire le nuove regole e scrivere il task ID
- Se il worker non scrive il task ID, il fallback trova comunque l'output dal `.done` piu recente
- Se non esiste nemmeno il `.done`, si apre il log (come prima)

---

*Completato da cervella-backend*
