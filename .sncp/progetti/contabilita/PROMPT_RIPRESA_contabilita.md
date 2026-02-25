# PROMPT RIPRESA - Contabilita Antigravity

> **Ultimo aggiornamento:** 25 Febbraio 2026 - Sessione 147
> **Branch attivo:** lab-v3 (sviluppo V3) + lab-v2 (intoccato) + main (produzione)
> **Versione canonica:** `CervellaSwarm/.sncp/progetti/contabilita/PROMPT_RIPRESA_contabilita.md`

---

## Stato Attuale - S147 Pre-Deploy QA COMPLETATA

| Cosa | Stato |
|------|-------|
| **Produzione** | v2.11.0 LIVE su contabilitafamigliapra.it (INTATTA) |
| **V3 VM** | v3.contabilitafamigliapra.it LIVE (main.py v1.13.0 - DA AGGIORNARE) |
| **3 Hotel Agent** | TUTTI v2.0.0 daily_closed. Fix N.2-N.5 locali, deploy in N.6 |
| **Lab v2** | INTOCCATO, frozen S87 |
| **Test** | **1441 portale** + **348 agent** = **1789 PASS** (0 warning) |
| **Round QA** | **110** (+1 questa sessione: Caccia Bug 3 Cervelle R110) |
| **FASE N.1-N.5** | COMPLETATE (S141-S146) - 17 step |
| **S147 Pre-Deploy QA** | COMPLETATA - CR 9.3 + BH PASS + LR 9.1 + 6 fix + Guardiana 9.7/10 |
| **Subroadmap** | `docs/SUBROADMAP_S140_LUCIDATURA.md` (17+6 step fatti, 3 step deploy rimanenti) |

---

## PROSSIMA SESSIONE: FASE N.6 - Deploy VM (3 step)

### Step 18: Deploy PORTALE su VM

**15 file da deployare su v3.contabilitafamigliapra.it:**

| # | File | Cosa cambia | Fase |
|---|------|-------------|------|
| 1 | `backend/main.py` | v1.14.0, AGENT_AUTH_ENDPOINTS, portal regex, assert | N.5+N.6 QA |
| 2 | `backend/routers/auth.py` | hmac.compare_digest, no sanitize code, Field max_length | N.5+QA |
| 3 | `backend/routers/admin.py` | sanitize_update_dict merge, health deep auth | N.3+N.5 |
| 4 | `backend/routers/transactions.py` | DELETE FK 409, debounce cleanup | N.1+N.3 |
| 5 | `backend/database/transactions.py` | FK check 4 tabelle (pareggi_parking_gruppi) | N.1 |
| 6 | `backend/database/seasons.py` | Cross-season filter pre_close + close | N.3 |
| 7 | `backend/processors/ericsoft_transformer.py` | BOO canale BOOKING | N.1 |
| 8 | `frontend/css/style.css` | 11 circuiti colore + bonus lilla | N.1+QA |
| 9 | `frontend/js/annullamenti.js` | undoData safety + restituzione_nome card | N.4+QA |
| 10 | `frontend/js/data.js` | initAnnullamenti catch + DELETE 409 frontend | N.1+N.4 |
| 11 | `frontend/js/selection.js` | batch merge Map + batchedSave | N.1 |

**Metodo deploy portale:**
1. SSH alla VM
2. Backup ogni file: `cp file file.backup_pre_n6_s148`
3. Deploy ogni file con `deploy.sh` oppure `scp` diretto
4. Cache bust frontend (aggiornare `?v=` in index.html)
5. Restart servizio: `sudo systemctl restart contabilita-v3`
6. Verificare: `curl https://v3.contabilitafamigliapra.it/api/health`
7. Rafa verifica: DELETE, colori HP, annullamenti

### Step 19: Deploy AGENT su hotel (Rafa via VPN)

**4 file agent da copiare su NL, SHE, HP:**

| # | File | Cosa cambia |
|---|------|-------------|
| 1 | `agent/agent.py` | HC.io /fail, watermark multi-batch, safety net 90gg, NOLOCK skip |
| 2 | `agent/http_sender.py` | 429 retry + signal HC.io |
| 3 | `agent/reconcile_comparator.py` | watermark window (non global) |
| 4 | `agent/__init__.py` | version bump |

**Metodo deploy agent:**
1. Rafa si collega via VPN a ogni hotel
2. Ferma il Task Scheduler: `schtasks /End /TN "ContabilitaSync-{hotel}"`
3. Copia i 4 file in `C:\contabilita-agent\agent\`
4. Dry-run: `python\python.exe -m agent.agent --hotel {hotel} --dry-run --verbose`
5. Se OK: `schtasks /Run /TN "ContabilitaSync-{hotel}"`
6. Verifica HC.io verde

### Step 20: Guardiana Finale

3 Cervelle + Guardiana consensus post-deploy. Target 9.5+.

---

## S147 - Cosa e' stato fatto (Pre-Deploy QA)

### Caccia Bug 3 Cervelle (Round 110)
- **Code Reviewer**: 9.3/10 - 0 P1, 3 P2, 6 P3
- **Bug Hunter**: PASS - 0 P1, 2 P2, 4 P3
- **Logic Reviewer**: 9.1/10 - 0 P1, 4 P2, 4 P3
- **Consensus**: 0 P1, 1 P2, 5 P3

### 6 Fix applicati + Guardiana R110 (9.7/10 APPROVED)
1. P2: `code`+`portal` Field max_length Pydantic (auth.py)
2. P3: `__version__` 1.14.0 (main.py)
3. P3: CSS bonus colore lilla distinto da visa (style.css)
4. P3: assert `_portal_codes` non vuoto (main.py)
5. P3: `restituzione_nome` nella card annullamenti (annullamenti.js)
6. P3: deprecation warning 422 test (test_auth_api.py)

---

## Lezioni Apprese (Sessione 147)

### Cosa ha funzionato bene
- Pre-deploy QA su TUTTO il diff (N.1-N.5 insieme) prima del deploy: zero sorprese
- Consensus 3 Cervelle: 0 P1 da tutte e 3 = alta confidenza per deploy

### Pattern candidato
- "Caccia Bug COMPLETA pre-deploy su accumulo di fix" - quando si accumulano molti step, una QA sull'insieme trova cose che le singole Guardiane mancano. Evidenza: S146 (2 P1 su singola fase) + S147 (1 P2 su insieme). Azione: PROMUOVERE

---

*S147: Pre-Deploy QA COMPLETATA. 0 P1, 6 fix, Guardiana 9.7/10 APPROVED. 1789 test PASS. 110 round QA. Prossimo: FASE N.6 Deploy VM (sessione dedicata).*
