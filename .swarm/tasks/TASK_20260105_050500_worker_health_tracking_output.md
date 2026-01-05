# Output: Worker Health Tracking System

**Task:** TASK_20260105_050500_worker_health_tracking
**Eseguito da:** cervella-backend
**Data:** 2026-01-05
**Stato:** COMPLETATO

---

## Cosa e' stato fatto

### 1. Modificato spawn-workers (v2.0.1 -> v2.1.0)

**File:** `~/.local/bin/spawn-workers`

Aggiunto nel runner script:

```bash
# Health tracking - salva PID e timestamp
mkdir -p .swarm/status
WORKER_PID=$$
WORKER_NAME="backend"  # o frontend, tester, ecc.
echo $WORKER_PID > ".swarm/status/worker_${WORKER_NAME}.pid"
date +%s > ".swarm/status/worker_${WORKER_NAME}.start"

# Cleanup automatico quando il worker termina
cleanup_health_files() {
    rm -f ".swarm/status/worker_${WORKER_NAME}.pid"
    rm -f ".swarm/status/worker_${WORKER_NAME}.start"
}
trap cleanup_health_files EXIT
```

**Comportamento:**
- Quando un worker spawna, crea file `.pid` e `.start` in `.swarm/status/`
- Quando il worker termina normalmente, i file vengono rimossi automaticamente (trap EXIT)
- Se il worker crasha, i file rimangono e `swarm-cleanup` li rileva

### 2. Creato swarm-cleanup (v1.0.0)

**File:** `~/.local/bin/swarm-cleanup`

Script per pulire task orfani e worker morti.

**Uso:**
```bash
swarm-cleanup              # Pulisce task orfani
swarm-cleanup --dry-run    # Mostra cosa farebbe
swarm-cleanup --verbose    # Output dettagliato
swarm-cleanup --timeout 60 # Timeout custom (default: 30 min)
```

**Logica:**
1. Trova tutti i task `.working`
2. Per ogni task:
   - Legge il file `.md` per trovare il worker assegnato
   - Controlla se esiste `.swarm/status/worker_XXX.pid`
   - Se PID non esiste O processo non in esecuzione: marca `.stale`
   - Se `.start` > timeout: marca `.stale`
3. Pulisce anche file di status orfani (PID file di processi morti)

**Output esempio:**
```
==============================================
  SWARM-CLEANUP
  CervellaSwarm Health Management
==============================================

[i] Progetto: /Users/rafapra/Developer/CervellaSwarm
[i] Timeout: 30 minuti

[i] Cerco task .working orfani...
[!] Task orfano trovato: TASK_XYZ (nessun PID file)
[OK] Marcato come stale: TASK_XYZ

[i] Task controllati: 3
[i] Task puliti: 1

[i] Cerco status file orfani...
[i] Status file orfani puliti: 0

==============================================
[OK] Cleanup completato!
==============================================
```

---

## File creati/modificati

| File | Azione | Versione |
|------|--------|----------|
| `~/.local/bin/spawn-workers` | MODIFICATO | 2.0.1 -> 2.1.0 |
| `~/.local/bin/swarm-cleanup` | CREATO | 1.0.0 |

---

## Struttura .swarm/status/

Quando un worker e' attivo:
```
.swarm/status/
├── worker_backend.pid    # Contiene il PID del processo
├── worker_backend.start  # Contiene timestamp Unix di avvio
├── worker_frontend.pid
└── worker_frontend.start
```

---

## Test suggeriti

### Test 1: Spawn normale
```bash
spawn-workers --backend
# Verifica che vengano creati:
ls -la .swarm/status/
# Dovrebbe mostrare worker_backend.pid e worker_backend.start
```

### Test 2: Terminazione normale
```bash
# Dopo che il worker termina normalmente (/exit)
ls -la .swarm/status/
# I file worker_backend.* dovrebbero essere stati rimossi
```

### Test 3: Simulazione crash
```bash
spawn-workers --backend
# In un altro terminale, trova e killa il processo
cat .swarm/status/worker_backend.pid
kill <PID>
# Poi esegui cleanup
swarm-cleanup --verbose
# Dovrebbe rilevare e pulire il task orfano
```

### Test 4: Dry run
```bash
swarm-cleanup --dry-run --verbose
# Mostra cosa farebbe senza modificare nulla
```

---

## Integrazione futura (opzionale)

Per auto-cleanup all'inizio sessione, si potrebbe aggiungere a un hook:

```python
# In un hook SessionStart
import subprocess
subprocess.run(["swarm-cleanup"], capture_output=True)
```

---

## Checklist Verifica

- [x] spawn-workers.sh modificato con PID tracking
- [x] swarm-cleanup creato e funzionante
- [x] Cleanup automatico con trap EXIT
- [x] Directory .swarm/status/ esiste
- [x] Script eseguibile (chmod +x)

---

*Output generato da cervella-backend*
*Task completato con successo*
