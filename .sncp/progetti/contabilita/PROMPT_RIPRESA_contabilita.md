# PROMPT RIPRESA - Contabilita Antigravity

> **Ultimo aggiornamento:** 22 Febbraio 2026 - Sessione 135
> **Branch attivo:** lab-v3 (sviluppo V3) + lab-v2 (intoccato) + main (produzione)
> **Versione canonica:** `CervellaSwarm/.sncp/progetti/contabilita/PROMPT_RIPRESA_contabilita.md`

---

## Stato Attuale - S135 Agent v1.4.0 + DB Sync HP

| Cosa | Stato |
|------|-------|
| **Produzione** | v2.11.0 LIVE su contabilitafamigliapra.it (INTATTA) |
| **V3 VM** | LIVE - EricsoftTransformer v1.5.0 + Agent v1.4.0 + Reconcile v1.0.0 |
| **3 Hotel Agent** | **TUTTI v1.4.0!** NL WM4032, SHE WM21654, HP WM24354 - HC.io+TG 1h |
| **Reconcile** | 3/3 ATTIVI (NL win=30, SHE+HP win=1) |
| **Lab v2** | INTOCCATO, frozen S87 |
| **Test** | **1709 PASS** (1399 portale + 310 agent, 0 fail) |
| **Round QA** | 89 totali |
| **Subroadmap** | `docs/SUBROADMAP_S128_DIAMANTE.md` (FASE N pulizia aggiunta S135) |
| **Prossimo** | **FASE M** SPRING Discovery + monitorare agents |

---

## S135 - Cosa abbiamo fatto

### 1. HP DOWN Fix
- sync_hp.bat cancellato per errore -> ricreato da template repo
- `attrib +R` su TUTTI i .bat (NL, HP, SHE) per protezione futura

### 2. Agent v1.4.0 Deploy (3/3 hotel)
- Version bump __init__.py 1.2.0 -> 1.4.0
- Cambio: stagione chain `checkout > check_in` (S134)
- NL: dry-run OK + real OK + Task Scheduler riavviato
- HP: dry-run OK + Task Scheduler riavviato
- SHE: dry-run OK + HC.io confermato + Task Scheduler riavviato
- Backup: `backup_v1.2.0/` su ogni hotel

### 3. Window Reconcile Verificata
- NL=30 (OK), HP=1 (OK), SHE=1 (OK)
- Piano: =7 il ~28 Feb, =30 il ~21 Mar

### 4. DB Sync HP V3
- HP mancava 19/02 + 20/02: INSERT 12 caparre + 3 giroconti da PROD
- UPDATE checkout_date = check_in per i 12 record PDF
- Backup: `contabilita_hp.db.backup_pre_sync_s135`
- NL e SHE: gia' allineati

### 5. Subroadmap aggiornata
- FASE N: Pulizia file (Mac + Windows)
- FASE O: Sync DB (ex FASE N)

---

## TODO Prossime Sessioni

1. **~28 Feb**: RECONCILE_WINDOW_DAYS=7 su SHE+HP
2. **~21 Mar**: RECONCILE_WINDOW_DAYS=30 su SHE+HP
3. **FASE M**: SPRING Discovery (read-only DB SISTEMI HP)
4. **FASE N**: Pulizia file Mac + Standardizzare Windows
5. **FASE O**: Sync DB (se altri gap trovati)

---

## Mappa Sistema

```
                    PRODUZIONE (INTATTA)
                    contabilitafamigliapra.it:443
                    v2.11.0, porta 8000
                    |
    VM Google Cloud (cervello-contabilita)
    35.193.39.185, e2-medium, $28/mese
                    |
        +-----------+-----------+
        |                       |
    LAB V2                  V3 (lab-v3)
    INTOCCATO               v3.contabilita...
    frozen S87              porta 8003
                            Transformer v1.5.0
                            Reconcile v1.0.0
                            |
                +-----------+-----------+
                |           |           |
            Hotel NL    Hotel SHE   Hotel HP
            SYNC+REC    SYNC+REC    SYNC+REC
            WM 4032     WM 21654    WM 24354
            HC.io+TG    HC.io+TG    HC.io+TG
            1h sync     1h sync     1h sync
            5AM recon   5AM recon   5AM recon
            win=30      win=1       win=1
            agent 1.4   agent 1.4   agent 1.4
```

---

## Lezioni Apprese (Sessione S135)

### Cosa ha funzionato bene
- Procedura deploy hotel: stop task -> backup -> copy -> dry-run -> restart = zero downtime
- `attrib +R` su .bat = protezione semplice ed efficace contro cancellazioni accidentali
- Audit pre-sync DB con Guardiana (piano verificato prima di toccare dati)

### Cosa non ha funzionato
- .bat cancellato per errore senza protezione: ora fixato con +R

### Pattern candidato
- "attrib +R su file critici Windows" -> NUOVO, monitorare nelle prossime sessioni

---

*S135: Agent v1.4.0 su 3/3 hotel + DB HP allineato. "Ultrapassar os proprios limites!"*
