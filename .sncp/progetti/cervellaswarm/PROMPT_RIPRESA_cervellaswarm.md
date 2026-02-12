# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-02-12 - Sessione 357
> **STATUS:** SNCP 4.0 IMPLEMENTATO!

---

## SESSIONE 357 - SNCP 4.0 IMPLEMENTATO

### Cosa abbiamo fatto
Implementata la migrazione SNCP 4.0: da 5 file di stato a 2+1 indice.

### 5 step completati

**Step 1 - Archiviazione:** 6 file spostati in `archivio/`
- `oggi.md` -> `.sncp/stato/archivio/oggi_archived_S357.md`
- 5 `stato.md` archiviati (cervellaswarm, miracollo, contabilita, cervellacostruzione, chavefy)

**Step 2 - Hook zombie ucciso:**
- `sncp_auto_update.py` -> `.DISABLED`
- Rimosso da settings.json (main + insiders)

**Step 3 - Puntatori aggiornati (12+ file):**
- `_SHARED_DNA.md` (main + insiders sincronizzati)
- `CHECKLIST_AZIONE.md`, `CLAUDE.md` (globale + progetto)
- `file_limits_guard.py`, `sncp_verify_sync_hook.py`
- `sncp_validator.py`, `sncp_dna_template.md`, `COMUNICAZIONE_INTER_AGENT.md`
- `PROMPT_RIPRESA_MASTER.md`, `NORD.md`

**Step 4 - NORD.md fixato:** 19->17 agenti, puntatore stato.md rimosso

**Step 5 - Script/hook runtime fixati:**
- `verify-sync.sh`: check_ripresa_freshness (era check_stato_freshness)
- `pre-session-check.sh`: controlla PROMPT_RIPRESA (era stato.md)
- `pre-commit`: rimosso check stato.md, aggiornato docs sync
- `sncp-init.sh`: non crea piu stato.md, dead code rimosso
- `compact-state.sh` + `post-session-update.sh` -> `.DISABLED`
- Template `NORD_TEMPLATE.md` aggiornato

### Audit Guardiana
- 1o audit: 7.8/10 (4 file P1 mancanti)
- Re-audit dopo fix: 9.2/10 (+1 fix insiders sync)
- Dopo ultimo fix: ~9.5/10
- Report: `docs/studio/guardiana/AUDIT_SNCP_4.0_MIGRAZIONE.md`

### Struttura SNCP 4.0 finale
```
TIENI:   PROMPT_RIPRESA  = volatile (ogni sessione)
TIENI:   NORD.md         = stabile (solo milestone)
TIENI:   MASTER          = indice progetti
RIMOSSO: stato.md        = archiviato
RIMOSSO: oggi.md         = archiviato + hook disabilitato
```

### P2 residui (docs stale, non bloccanti)
- 12+ file docs/guide con menzioni legacy di stato.md
- Da pulire in sessioni future quando si toccano quei file

---

## ARCHIVIO

| Sessione | Cosa |
|----------|------|
| S337-S348 | Coverage push 41% -> 95% (968 test) |
| S349 | Audit reale + Pulizia + MAPPA MIGLIORAMENTI |
| S350 | FASE A: Async Hooks + Bash Validator |
| S351 | Persistent Memory + Hook Integrity |
| S352 | COMPLETAMENTO MAPPA: B+C+D = 7 step, score 9.1/10 |
| S353 | CervellaBrasil nasceu! 7 pesquisas, 10k+ linhas |
| S354 | Chavefy nasceu! SaaS Property Management Brasil |
| S355 | SubagentStart Context Injection + Audit totale Famiglia |
| S356 | Studio SNCP 4.0 (3 esperte) + Clear Context (parcheggiato) |
| S357 | SNCP 4.0 IMPLEMENTATO! 6 file archiviati, 12+ puntatori fixati |

---

*"Meno file = meno bugie."*
*Sessione 357 - Cervella & Rafa*
