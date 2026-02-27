# PROMPT RIPRESA - Contabilita Antigravity

> **Ultimo aggiornamento:** 27 Febbraio 2026 - Sessione 199
> **Branch attivo:** lab-v3 (sviluppo V3) + lab-v2 (intoccato) + main (produzione)
> **Versione canonica:** `CervellaSwarm/.sncp/progetti/contabilita/PROMPT_RIPRESA_contabilita.md`

---

## Stato Attuale - DEPLOY S199 COMPLETATO

| Cosa | Stato |
|------|-------|
| **Produzione V2** | v2.11.0 LIVE su contabilitafamigliapra.it (INTATTA, verificata post-deploy) |
| **V3 VM** | **main.py v1.16.0** + pdf_parser v1.14.1 + **33 file deployati S199** |
| **V3 locale** | Allineato con VM (MD5 verificati 31/32, index.html sync) |
| **Agent NL/SHE/HP** | v2.1.0 LIVE + reconcile v1.1.0 DEPLOYATO S184 |
| **HC.io** | **11 check** - TUTTI VERDI S184 |
| **Test portale** | **1546 PASS** (0 fail, 7 skipped) |
| **Lab-v2** | INTATTO, frozen da S87, verificato post-deploy |
| **Deps VM** | pydantic **2.12.5** (upgrade da 2.12.1 yanked), fastapi 0.133.1, uvicorn 0.41.0 |
| **Nginx** | 3 config allineate (prod 10 header, lab 11, v3 12), portal routes, proxy_hide_header 7/7 |

---

## S199 - Deploy Fortezza Mode (33 file)

| Fase | Cosa | Stato |
|------|------|-------|
| **0** | GCP Snapshot | `pre-deploy-s199-20260227-151346` |
| **1** | Pre-deploy check | 7/7 PASS (1546 test) |
| **2** | Snapshot applicativo | 75 file + 3 DB + MANIFEST |
| **3** | pip install | 14 pkg + pydantic upgrade 2.12.5 |
| **4** | Deploy 28 file (BE+FE) | `deploy_v3_files.sh` - 28/28 MD5 match |
| **5** | Nginx 3 config | Upload + `nginx -t` OK + reload |
| **6** | Cache bust | 16 JS `?v=202602271526` |
| **7** | Verifica | Health 200, v1.16.0, prod+lab intatti |
| **8** | Guardiana audit | Score 9.3/10, 0 P0, 4 P2 (tutti fixati) |

**Audit Guardiana S199**: 4 P2 (cache bust diverge FIXATO, pydantic yanked FIXATO, PROMPT stale FIXATO, NORD stale FIXATO), 4 P3 (CSS no cache bust, 5 FP script verifica, backup accumulo, app-init posizione).

**Snapshot rollback**: `/opt/backups/contabilita-v3/snapshot_20260227_151531`

---

## TODO prossime sessioni

- P3: Fix `verifica_post_deploy_v3.sh` (5 falsi positivi: auth endpoints + bug parsing log)
- P3: Fix `deploy_v3_files.sh` CSS cache bust (solo JS, non CSS)
- P3: Pulizia doppio .env NL+SHE (agent hotel)
- P3: Pulizia `.backup.*` files sulla VM (accumulano)
- Sessione dedicata: miglioramenti script interni

---

## Dove leggere

| Cosa | File |
|------|------|
| NORD progetto | `NORD.md` (root lab-v3) |
| Mappa deploy | `docs/MAPPA_DEPLOY_VM.md` |
| deploy V3 script | `scripts/deploy_v3_files.sh` (v2.0.0) |
| verifica post-deploy | `scripts/verifica_post_deploy_v3.sh` (v1.0.0) |

---

## Lezioni Apprese (Sessione 199)

### Cosa ha funzionato bene
- **deploy_v3_files.sh v2.0.0**: 12 step automatici, rollback auto, 28 file in un batch
- **Guardiana Ops PRE-deploy**: ha trovato deploy_v3_files.sh (non deploy.sh!), mappato struttura VM
- **Triple check MD5**: conferma 31/32 OK (1 atteso = index.html cache bust)
- **pydantic upgrade immediato**: yanked -> 2.12.5, zero downtime

### Cosa non ha funzionato
- **deploy.sh vs deploy_v3_files.sh**: confusione iniziale, risolta da Guardiana Ops
- **Nginx config path diversi**: prod/lab in sites-enabled (file diretti), v3 in sites-available (symlink)
- **verifica_post_deploy_v3.sh**: 5 falsi positivi che desensibilizzano

### Pattern candidato
- **Guardiana Ops PRIMA di deploy complesso**: mappa struttura, trova script giusto. Evidenza: S199
- **Allinea index.html locale DOPO deploy**: copiare da VM per evitare divergenza cache bust. Evidenza: S199

*S199: Deploy 33 file COMPLETATO. V3 VM = v1.16.0. Tutti i servizi OK.*
