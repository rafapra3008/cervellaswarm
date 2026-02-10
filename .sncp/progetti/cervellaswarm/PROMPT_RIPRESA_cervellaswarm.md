# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-02-10 - Sessione 351
> **STATUS:** FASE A 100% + FASE C iniziata. MAPPA MIGLIORAMENTI 4/11 step FATTI.

---

## SESSIONE 351 - A.3 + C.1

```
+================================================================+
|   S351: 2 STEP COMPLETATI                                       |
|                                                                  |
|   A.3 Persistent Memory Guardiane -> FATTO (9/10)              |
|   C.1 Hook Integrity Check        -> FATTO (9.5/10)            |
|                                                                  |
|   FASE A: 100% (3/3)   FASE C: 33% (1/3)                      |
|   Score medio sessione: 9.25/10                                 |
+================================================================+
```

### Cosa fatto
| # | Azione | Dettaglio |
|---|--------|-----------|
| 1 | A.3: Persistent Memory | `memory: user` aggiunto a 6 file Guardiane (3 main + 3 insiders). Sezione istruzioni per ruolo |
| 2 | C.1: Hook Integrity | Nuovo `verify-hooks.py` + wrapper `.sh`. Controlla 34 hook files, rileva BROKEN/DISABLED/divergenze |
| 3 | Guardiana audit x3 | A.3 (9/10), C.1 primo (8/10 -> fix), C.1 re-audit (9.5/10) |
| 4 | MAPPA aggiornata | A.3 e C.1 marcati FATTO con score |

### Decisioni Prese con PERCHE
- **memory: user (non project)** perche le Guardiane devono ricordare pattern cross-progetto, non solo per CervellaSwarm
- **Script in Python (non bash)** perche JSON parsing nativo e piu robusto di jq/sed
- **Divergenze come INFO (non errore)** perche main e insiders possono avere hook diversi intenzionalmente
- **Type hints + error handling** richiesti dalla Guardiana al primo audit e applicati immediatamente

### File Creati/Modificati
- `~/.claude/agents/cervella-guardiana-{qualita,ops,ricerca}.md` - memory: user + sezione istruzioni (v2.1.0)
- `~/.claude-insiders/agents/cervella-guardiana-{qualita,ops,ricerca}.md` - memory: user + sezione istruzioni (v1.1.0)
- `scripts/sncp/verify-hooks.py` - NUOVO: verifica integrita 34 hook files (224 righe)
- `scripts/sncp/verify-hooks.sh` - NUOVO: wrapper bash
- `.sncp/.../MAPPA_MIGLIORAMENTI_INTERNI.md` - A.3+C.1 marcati FATTO

### Scoperte
- 4 divergenze hook tra main e insiders: 2 solo in main, 2 solo in insiders (non bloccanti ma da monitorare)
- Le Guardiane avranno memory directory in `~/.claude/agent-memory/<nome>/` a partire dalla prossima sessione

---

## PROSSIMA SESSIONE (S352)

**COSA FARE:** B.1 (CLAUDE.md Riduzione)

| Step | Cosa | Tempo |
|------|------|-------|
| B.1 | Audit e Riduzione CLAUDE.md | 4h |

**DOVE:** `.sncp/progetti/cervellaswarm/roadmaps/MAPPA_MIGLIORAMENTI_INTERNI.md`

**NOTA:** Miracollook plist hanno path sbagliati - fixare quando si lavora su quel progetto.

---

## ARCHIVIO

| Sessione | Cosa |
|----------|------|
| S337-S348 | Coverage push 41% -> 95% (968 test) |
| S349 | Audit reale + Pulizia + MAPPA MIGLIORAMENTI |
| S350 | FASE A: A.1 Async Hooks (9/10) + A.2 Bash Validator (9.5/10) |
| S351 | A.3 Persistent Memory (9/10) + C.1 Hook Integrity (9.5/10) |

---

*"Un po' ogni giorno fino al 100000%!"*
*Sessione 351 - Cervella & Rafa*
