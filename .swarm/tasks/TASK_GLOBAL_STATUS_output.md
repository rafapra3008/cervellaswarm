# Output: TASK_GLOBAL_STATUS

**Worker:** cervella-backend
**Data:** 6 Gennaio 2026 20:18
**Stato:** COMPLETATO

---

## Cosa e' stato fatto

### 1. Creato script `swarm-global-status`

**Path:** `scripts/swarm/swarm-global-status`
**Linguaggio:** Python 3
**Linee:** ~320

### 2. Funzionalita' implementate

| Feature | Descrizione |
|---------|-------------|
| Vista standard | Mostra tutti i progetti con task e worker |
| Output JSON | `--json` per integrazione con altri tool |
| Watch mode | `--watch` refresh ogni 5 secondi |
| Help | `--help` documentazione completa |

### 3. Cosa mostra

- **Per ogni progetto:**
  - Nome e path
  - Conteggio task (.ready, .working, .done)
  - Worker attivi con verifica PID
  - Ultimo heartbeat
  - Su cosa sta lavorando ogni worker

- **Totali:**
  - Task ready totali
  - Task working totali
  - Worker attivi totali
  - Progetti attivi

### 4. Legenda colori

```
* (verde)   Progetto attivo (worker in esecuzione)
o (giallo)  Ha task pronti (.ready)
- (blu)     Progetto idle
> (verde)   Worker vivo
x (rosso)   Worker morto (PID non trovato)
```

### 5. Link creato

```bash
~/.local/bin/swarm-global-status -> scripts/swarm/swarm-global-status
```

### 6. Test eseguito con successo

```
$ swarm-global-status

+=======================================================================+
|                         SWARM GLOBAL STATUS                           |
+=======================================================================+

* CervellaSwarm (3 ready, 3 working, 1 worker)
    > backend: TASK_GLOBAL_STATUS (0s fa)

* miracollogeminifocus (0 ready, 0 worker)
    (nessun worker attivo)

- ContabilitaAntigravity (0 ready, 0 worker)
    (nessun worker attivo)

------------------------------------------------------------------------
TOTALE: 3 task ready, 3 working, 1 worker attivi
PROGETTI: 3 attivi
------------------------------------------------------------------------
```

---

## File creati

1. `scripts/swarm/swarm-global-status` (nuovo)
2. `~/.local/bin/swarm-global-status` (symlink)

---

## Come usare

```bash
# Vista standard
swarm-global-status

# Output JSON (per script/integrazione)
swarm-global-status --json

# Monitoraggio continuo (refresh ogni 5s)
swarm-global-status --watch

# Help
swarm-global-status --help
```

---

## Note tecniche

- Legge `~/.swarm/projects.txt` per lista progetti
- Verifica PID worker con `os.kill(pid, 0)`
- Legge heartbeat da `.swarm/status/heartbeat_*.log`
- Supporta path con `~` e variabili d'ambiente
- Compatibile con macOS e Linux

---

*"Prima la MAPPA, poi il VIAGGIO!"*
*"Ultrapassar os proprios limites!"*
