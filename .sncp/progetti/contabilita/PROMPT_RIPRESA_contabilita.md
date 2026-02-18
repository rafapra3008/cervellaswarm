# PROMPT RIPRESA - Contabilita Antigravity

> **Ultimo aggiornamento:** 18 Febbraio 2026 - Sessione 76
> **Branch:** lab-v2

---

## Stato Attuale - Subroadmap "Perfezione Pre-Merge" Step 5 COMPLETATO

| Cosa | Stato |
|------|-------|
| **Produzione** | v2.11.0 LIVE su contabilitafamigliapra.it (INTATTA, zero modifiche) |
| **Lab v2 VM** | v1.13.0 LIVE su lab.contabilitafamigliapra.it (HTTPS, 12 headers) |
| **Main** | 278f9f9 - Fix deployati su VM |
| **Test lab-v2** | 1036/1036 PASS locale (0 warnings) |
| **VM** | e2-medium (2 vCPU, 4GB RAM, 40GB disco) |
| **Migrations VM** | v10 su tutti e 3 i DB (NL, HP, SHE) |

---

## Sessione 76 - Step 5 Deploy VM COMPLETATO

### Subroadmap 6 Step

| Step | Cosa | Score | Stato |
|------|------|-------|-------|
| 1 | Auth Fix (config.js v1.3.0) | 9.5/10 | COMPLETATO S75 |
| 2 | Migration v10 + Fatto | 9.5/10 | COMPLETATO S75 |
| 3 | Sync Script v1.2.0 | 9.7/10 | COMPLETATO S75 |
| 4 | Review VM (3 Cervelle + Fix P2) | 9.6/10 | COMPLETATO S75 |
| 5 | Deploy VM + Sync DB | 9.5/10 | **COMPLETATO S76** |
| **6** | **Prova Reale Chiusura Stagione** | - | **PROSSIMO** |

### Step 5: Cosa e stato fatto

**Triple Check pre-deploy** (3 Guardiane parallelo):
- Guardiana Qualita: 9.6/10 (0 P0, 0 P1, 0 P2, 9 P3) - GO
- Guardiana Ops: 8.8/10 (1 P2 deploy.sh branch guard) - GO
- Security: 9.2/10 (0 P0, 0 P1, 0 P2, 2 P3) - GO

**Deploy 5 fasi:**
1. Pre-flight: SSH, disco 21GB, RAM 13%, health prod+lab OK, DB prod=v3, lab=v9
2. Deploy codebase: rsync 7 file, fix permessi migrations.py 600->644
3. Restart service: contabilita-lab restart pulito, zero errori
4. Sync DB: 2 bug trovati e fixati nel sync script (v1.2.0->v1.3.0):
   - Bug 1: `mktemp` crea file 600 (root), www-data non legge -> `chmod 644`
   - Bug 2: Python sys.path non include CWD per script assoluto -> `PYTHONPATH=$LAB_DIR`
   - Rollback automatico funzionato perfettamente nei 2 tentativi falliti
   - Terzo tentativo: SUCCESSO! 3/3 DB v3->v10, 7 migrazioni applicate
5. Verification: prod INTATTA (v3), lab v10, zero errori log

### DB Lab VM aggiornati (sync 18 Feb 2026)

| DB | Versione | Caparre | GIR |
|----|----------|---------|-----|
| NL | v10 | 4,909 | 2,532 |
| HP | v10 | 2,342 | 1,146 |
| SHE | v10 | 2,638 | 1,278 |

### Architettura VM

```
VM cervello-contabilita (e2-medium, 35.193.39.185)
+-- Nginx (80/443)
|   +-- contabilitafamigliapra.it     -> contabilita-api (:8000) [PROD]
|   +-- lab.contabilitafamigliapra.it -> contabilita-lab (:8001) [LAB]
+-- /opt/contabilita-system/  [PROD - NON TOCCARE] DB v3
+-- /opt/contabilita-lab/     [LAB v2] DB v10, sync_db v1.3.0
+-- Cron root 3AM: cron_backup_db.sh v2.0.0 (solo prod)
```

---

## Cosa Fare Prossima Sessione (Step 6)

### Step 6: Prova Reale Chiusura Stagione
1. Rafa apre https://lab.contabilitafamigliapra.it/nl/ (codice portale NL: 2024)
2. Verifica: login popup appare, dati caricano, colonne "fatto" normalizzate
3. Wizard chiusura stagione: pre-close stats, conferma, celebrazione
4. Post-chiusura: carry-forward, read-only, faldone storico, export Excel
5. Zero errori nel journalctl

### Dopo Step 6
- Se tutto OK: Subroadmap Perfezione COMPLETATA, valutare merge
- Se trovati bug: fixare e re-deployare

---

*"Ultrapassar os proprios limites!" - Step 5 REALE, non su carta!*
