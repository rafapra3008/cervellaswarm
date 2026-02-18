# PROMPT RIPRESA - Contabilita Antigravity

> **Ultimo aggiornamento:** 17 Febbraio 2026 - Sessione 71
> **Branch:** lab-v2

---

## Stato Attuale - DEPLOY LAB V2 SU VM (FASE A COMPLETATA)

| Cosa | Stato |
|------|-------|
| **Produzione** | v2.11.0 LIVE (pdf_parser v1.12.0 + telegram v1.8.0) |
| **Main** | 278f9f9 - Fix deployati su VM |
| **Lab 2.0** | branch lab-v2 - Verifica Diamante COMPLETATA 8/8 |
| **Test lab-v2** | 1034/1034 PASS (0 warnings) |
| **Database pkg** | v2.15.0 (5 Mixin) |
| **SPRING Stack** | Parser v1.1.0 + Matcher v1.0.0 + Router v1.1.0 + UI v1.2.0 + Analysis v1.0.0 = **261 test** |
| **DB LAB** | DATI PRODUZIONE REALI (sync 16 Feb 2026) |
| **VM** | **e2-medium** (2 vCPU, 4GB RAM, 40GB disco) - upgrade S71 |

---

## Sessione 71 - FASE A Upgrade VM COMPLETATA

### Cosa e stato fatto

1. **Step 1: Pre-flight check** - Raccolti tutti i dati VM (memoria, disco, servizi, DB integrity, health). Creato GCP snapshot `pre-resize-s71-20260217-214922`
2. **Step 2: Resize** - Disco 30->40GB (online, zero downtime) + machine type g1-small -> e2-medium (80 secondi downtime). IP 35.193.39.185 preservato
3. **Step 3: Verifica** - Tutti i check OK: RAM 3913MB, disco 39G, 2 vCPU, servizi attivi, DB integri, health OK interno+esterno
4. **Guardiana audit** - Score 9.5/10, 10 finding documentali (0 P0, 0 P1, 6 P2, 4 P3) tutti fixati

### Scoperta confermata (da S70)

- Produzione usa **systemd + venv** (NON Docker), Uvicorn **1 worker** (non 4 come documentato prima)
- DB produzione alla **version 3** (lab v2 ha v9) - conferma necessita DB separati con migrazioni
- Python 3.10.12 sulla VM

### Decisione di Rafa (da S70)

Lab-v2 sulla VM come **secondo portale** porta 8001. Nessun merge. Transizione graduale:
- v1 resta principale (nessuna modifica)
- v2 gira accanto, dati sincronizzati (UNIDIREZIONALE v1->v2)
- Switch quando Rafa decide

---

## Subroadmap: Deploy Lab v2 su VM

| Step | Cosa | Stato |
|------|------|-------|
| 1 | Pre-flight check + GCP snapshot | **COMPLETATO** (S71) |
| 2 | Resize VM + disco 40GB | **COMPLETATO** (S71) |
| 3 | Verifica post-resize + Guardiana | **COMPLETATO** (S71, 9.5/10) |
| 4 | Deploy codebase (rsync o git clone) | PROSSIMO |
| 5 | Python venv + .env (ENVIRONMENT=production, APP_ENV=lab) | - |
| 6 | Copia DB (sqlite3 .backup) + migrazioni v3->v9 | - |
| 7 | Systemd service (127.0.0.1:8001, 2 worker, hardening) | - |
| 8 | Nginx proxy (bloccare /docs, spring_files/) | - |
| 9 | Test suite 1034 su VM (GO/NO-GO gate) | - |
| 10 | Script sync DB (stop->backup->migrate->start) + alert | - |

**ATTENZIONE Ops (da audit Guardiana S70):**
- Sync cron SOVRASCRIVE migrazioni v9 con schema v3 -> script DEVE fare stop/backup/migrate/start
- Bind 127.0.0.1 OBBLIGATORIO per lab (non esporre porta 8001)
- Test suite su VM = gate GO/NO-GO definitivo
- .env lab: ENVIRONMENT=production (no Swagger) + APP_ENV=lab (no Telegram)

---

## Cosa Fare Prossima Sessione

**FASE B: Setup Lab v2 (Step 4-8)**
1. Deploy codebase lab-v2 sulla VM in /opt/contabilita-lab/
2. Setup venv separato + pip install
3. Copiare DB con sqlite3 .backup + eseguire migrazioni v3->v9
4. Creare systemd service contabilita-lab.service
5. Configurare Nginx proxy per porta 8001
6. Audit Guardiana

**Tutte le operazioni VM eseguite dalla Cervella via Bash tool. Rafa approva, NON esegue comandi.**

---

## Documenti di Riferimento

| Doc | Cosa |
|-----|------|
| `docs/SPRING_REPORT_DIAMANTE.md` | Report definitivo Verifica Diamante |
| `deployment/systemd/contabilita-api.service` | Service systemd produzione (1 worker reale) |
| `deployment/contabilita_nginx_improved.conf` | Config Nginx (versione con security headers) |
| Reports in CervellaSwarm `.sncp/progetti/contabilita/reports/` | Studi S70 |

---

*"Ultrapassar os proprios limites!" - Dal diamante alla produzione!*
