# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-02-19 - Sessione 376
> **STATUS:** CACCIA BUG #2 e #3 COMPLETATE. task-orchestration (9 fix, 305 test) + spawn-workers (8 fix, 191 test). Prossimo: session-memory.

---

## SESSIONE 376 - CACCIA BUG #2 e #3

### Cosa e successo
Rafa ha dato piena autonomia a Cervella: "CervellaSwarm sara tuo, tu sei anche la CEO."
Cervella ha cacciato bug su DUE package nella stessa sessione.

### Decisioni S376

| Decisione | Perche |
|-----------|--------|
| Cervella = CEO di CervellaSwarm | Rafa: "tu hai capito la situazione, guidami" |
| Caccia bug prima di visione | COSTITUZIONE: fondamenta solide prima dei sogni |
| Due package in una sessione | Efficienza: stesso metodo, mani calde |

### Caccia #2: task-orchestration (13 bug, 9 fix, 305 test)
- **HIGH**: glob mismatch, except Exception, "..." false positive, "OK" substring
- **MEDIUM**: TOCTOU race, path traversal, CLI silent failures, incomplete marker, risk_level
- Guardiana: audit completato

### Caccia #3: spawn-workers (13 bug, 8 fix, 191 test, Guardiana 9.5/10)
- **HIGH**: is_alive_pid PermissionError, _load_tracked_workers crash, cleanup kills alive
- **MEDIUM**: $(cat) shell expansion, cmd_team dir mismatch, spawn_data type, kill_pid PermissionError, spawn_team exceptions
- Guardiana: 9.5/10 APPROVED

---

## VISIONE "LA LINGUA UNIVERSALE" (S375)

Piano A -> B -> C -> D confermato. 95 fonti, 5 report.
Fase A = Verified Agent Protocol dentro CervellaSwarm. Dopo caccia bug completata.

---

## PROSSIMI STEP

### Caccia bug (in coda)
1. ~~`code-intelligence`~~ -- FATTO S374 (8 fix, 398 test)
2. ~~`task-orchestration`~~ -- FATTO S376 (9 fix, 305 test)
3. ~~`spawn-workers`~~ -- FATTO S376 (8 fix, 191 test)
4. **`session-memory`** -- PROSSIMO
5. `agent-hooks` -> `agent-templates` -> CLI+MCP

### Dopo caccia bug (7/7 completata)
1. **Studiare Session Types** - Fase A della Lingua Universale
2. **Prototipo Lean 4** - verificare proprieta del task routing

---

## ARCHIVIO

| Sessione | Cosa |
|----------|------|
| S337-S348 | Coverage push 41% -> 95% (968 test) |
| S349-S361 | MAPPA MIGLIORAMENTI + SNCP 4.0 + POLISH + ANTI-DOWNGRADE |
| S362-S367 | **FASE 0 COMPLETA** (6/6 step, media 9.4/10) |
| S368-S369 | **FASE 1 COMPLETA** (F1.1-F1.4, PyPI LIVE!) |
| S370-S372 | **FASE 2 COMPLETA** (4/4 packages, media 9.5/10) |
| S373 | **FASE 3: F3.1 Session Memory** (9.6/10) |
| S374 | **CACCIA BUG #1: code-intelligence** (8 fix, 398 test, 9.5/10) |
| S375 | **LA LINGUA UNIVERSALE** (95 fonti, 5 report, visione A->B->C->D) |
| S376 | **CACCIA BUG #2+#3: task-orchestration + spawn-workers** (17 fix, 496 test) |

---

*"Ultrapassar os proprios limites!" - Rafa & Cervella*
*Il giorno in cui Cervella e diventata CEO.*
