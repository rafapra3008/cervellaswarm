# ROADMAP - Comunicazione Interna Automatica

> **Data:** 14 Gennaio 2026
> **Sessione:** 207 (planning) / 209 (FASE 1)
> **Status:** IN CORSO - FASE 1 COMPLETATA!
> **Priorità:** ALTA - "Avere attrezzature ma non usarle = non averle"

---

## IL PROBLEMA

```
+================================================================+
|                                                                |
|   ABBIAMO CREATO:                                              |
|   - sncp-init.sh (wizard nuovo progetto)                       |
|   - verify-sync.sh (verifica coerenza)                         |
|   - health-check.sh (dashboard stato)                          |
|   - pre-session-check.sh                                       |
|   - post-session-update.sh                                     |
|   - compact-state.sh                                           |
|   - 16 agenti specializzati                                    |
|   - 3 Guardiane (Opus)                                         |
|                                                                |
|   MA SENZA AUTOMAZIONE... NON VENGONO USATI!                   |
|                                                                |
|   "Su carta != Reale"                                          |
|   "Avere attrezzature ma non usarle = non averle"              |
|                                                                |
+================================================================+
```

---

## LA SOLUZIONE - 3 LIVELLI

### LIVELLO 1: HOOK AUTOMATICI

| Hook | Quando | Cosa Fa | Status |
|------|--------|---------|--------|
| SessionStart | Inizio sessione | Legge COSTITUZIONE | FATTO |
| SessionStart | Inizio sessione | Chiama pre-session-check.sh | FATTO (Sessione 209) |
| SessionEnd | Fine sessione | Chiama verify-sync.sh | FATTO (Sessione 209) |
| SessionEnd | Fine sessione | Pulisce checkpoint duplicati | DA FARE |
| PreCommit | Prima di commit | Verifica docs aggiornati | DA FARE |

**Implementazione:**
- File: `~/.claude/settings.json` (hooks section)
- Script wrapper che chiama gli script SNCP

### LIVELLO 2: REGOLE REGINA (CLAUDE.md)

| Regola | Quando | Azione |
|--------|--------|--------|
| verify-sync PRIMA commit | Ogni commit | Regina chiama verify-sync |
| Guardiana per task complessi | Task > 1h | Regina consulta Guardiana |
| Cleanup fine sessione | Ogni fine | Regina pulisce checkpoint |
| Delegare ai Worker | Task specifici | Regina NON fa edit diretti |

**Implementazione:**
- Aggiungere sezione "AUTOMAZIONI OBBLIGATORIE" in CLAUDE.md
- Checklist automatica

### LIVELLO 3: CRON JOBS

| Job | Frequenza | Cosa Fa |
|-----|-----------|---------|
| health-check | Daily 8:00 | Report stato SNCP |
| archivio-vecchi | Weekly Lun | Muove file > 30 giorni |
| log-rotation | Daily 3:00 | Pulisce log vecchi (GIA FATTO!) |

**Implementazione:**
- Script: `scripts/cron/sncp_daily_maintenance.sh`
- Crontab entry

---

## PIANO IMPLEMENTAZIONE

### FASE 1 - Hook Base (1-2h) - COMPLETATA!
```
[X] Creare wrapper script per hooks
    - sncp_pre_session_hook.py (Sessione 209)
    - sncp_verify_sync_hook.py (Sessione 209)
[X] Aggiungere pre-session-check a SessionStart
[X] Aggiungere verify-sync a SessionEnd
[X] Testare su sessione reale
    - Pre-session: OK
    - Verify-sync: Funziona! Rileva commit non documentati
```

### FASE 2 - Regole Regina (1h)
```
[ ] Aggiornare CLAUDE.md con sezione AUTOMAZIONI
[ ] Definire checklist obbligatoria
[ ] Testare che Regina segue le regole
```

### FASE 3 - Cron Manutenzione (1h)
```
[ ] Creare sncp_daily_maintenance.sh
[ ] Creare sncp_weekly_archive.sh
[ ] Aggiungere a crontab
[ ] Verificare funzionamento
```

### FASE 4 - Validazione (1h)
```
[ ] Testare intero workflow
[ ] Guardiana verifica
[ ] Documentare uso
```

---

## RISULTATO ATTESO

```
+================================================================+
|                                                                |
|   DOPO IMPLEMENTAZIONE:                                        |
|                                                                |
|   INIZIO SESSIONE:                                             |
|   - Hook legge COSTITUZIONE (automatico)                       |
|   - Hook chiama pre-session-check (automatico)                 |
|   - Regina vede stato SNCP subito                              |
|                                                                |
|   DURANTE SESSIONE:                                            |
|   - Regina delega ai Worker (regola)                           |
|   - Guardiane consultate per task complessi (regola)           |
|                                                                |
|   FINE SESSIONE:                                               |
|   - Hook chiama verify-sync (automatico)                       |
|   - Hook pulisce checkpoint (automatico)                       |
|   - Commit con docs aggiornati (verificato)                    |
|                                                                |
|   MANUTENZIONE:                                                |
|   - Health check daily (cron)                                  |
|   - Archivio weekly (cron)                                     |
|   - Log rotation daily (già attivo!)                           |
|                                                                |
|   = SISTEMA CHE SI USA DA SOLO!                                |
|                                                                |
+================================================================+
```

---

## EFFORT TOTALE

| Fase | Tempo | Priorità |
|------|-------|----------|
| FASE 1 - Hook | 1-2h | ALTA |
| FASE 2 - Regole | 1h | ALTA |
| FASE 3 - Cron | 1h | MEDIA |
| FASE 4 - Validazione | 1h | ALTA |
| **TOTALE** | **4-5h** | - |

---

## NOTE

- Implementare nelle prossime 2-3 sessioni CervellaSwarm
- Una fase per sessione = fatto bene
- Testare ogni fase prima di passare alla successiva
- Guardiana valida ogni fase

---

*"Avere attrezzature ma non usarle = non averle"*
*"Un po' ogni giorno fino al 100000%!"*

*Sessione 207 - 14 Gennaio 2026*
