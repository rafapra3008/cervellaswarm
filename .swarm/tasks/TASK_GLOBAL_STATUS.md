# Task: Implementare swarm-global-status

**Assegnato a:** cervella-backend
**Stato:** ready
**Priorita:** ALTA
**Data:** 6 Gennaio 2026

---

## Obiettivo

Creare il comando `swarm-global-status` che mostra una vista aggregata di TUTTI i progetti CervellaSwarm.

---

## Contesto

Lo studio e' gia' completo: `docs/studio/STUDIO_MULTI_PROGETTO.md`

Leggi la sezione "5. QUICK WIN: swarm-global-status" per:
- Specifiche complete
- Pseudocodice Python
- Formato output atteso

---

## Specifiche

### Input
- `~/.swarm/projects.txt` - Lista progetti (gia' esiste!)
- Ogni progetto ha `.swarm/tasks/` e `.swarm/status/`

### Output Atteso
```
=== SWARM GLOBAL STATUS ===

CervellaSwarm (3 task ready, 2 worker attivi)
  - backend: TASK_123 (working 5m)
  - researcher: TASK_456 (working 2m)

Miracollo (1 task ready, 0 worker attivi)
  - (nessun worker)

Contabilita (0 task, 0 worker)
  - (progetto idle)

TOTALE: 4 task ready, 2 worker attivi
```

### Requisiti
1. Script Python o Bash
2. Legge `~/.swarm/projects.txt`
3. Per ogni progetto conta: .ready, .working, .done
4. Mostra worker attivi (verifica PID ancora vivo)
5. Output colorato (verde/giallo/rosso)
6. Installabile in `~/.local/bin/`

---

## File da Creare

```
scripts/swarm/swarm-global-status
```

Poi linkare: `ln -sf .../swarm-global-status ~/.local/bin/`

---

## Pattern da Seguire

Guarda come sono fatti:
- `scripts/swarm/swarm-status.sh` (singolo progetto)
- `scripts/swarm/swarm-roadmaps.sh` (multi-progetto esistente)

---

## Output Task

1. Script funzionante in `scripts/swarm/`
2. Link creato in `~/.local/bin/`
3. Test con `swarm-global-status`
4. Scrivi risultato in `_output.md`

---

"Prima la MAPPA, poi il VIAGGIO!"
"Ultrapassar os proprios limites!"
