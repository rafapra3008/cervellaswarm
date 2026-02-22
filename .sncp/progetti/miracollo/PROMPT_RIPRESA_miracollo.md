<!-- DISCRIMINATORE: ECOSISTEMA MIRACOLLO - PANORAMA -->

# PROMPT RIPRESA - Ecosistema Miracollo

> **Ultimo aggiornamento:** 22 Febbraio 2026 - Sessione FASE 1 Online
> **Status:** FASE A completata (9.0/10), pronta per FASE B (Rafa accende VM)

---

## I 3 BRACCI

| Braccio | Porta | Score | Focus |
|---------|-------|-------|-------|
| **PMS Core** | 8001 | 90% LIVE | FASE 1 Online (andare live su miracollo.com) |
| **Miracollook** | 8002 | 10/10 | READ-ONLY. Non toccare fino PMS >= 9.0 |
| **Room Hardware** | 8003 | 10% | Bloccato VLAN, DOPO |

---

## FASE 1 ONLINE - STATO

```
FASE A - Preparazione         [####################] 100% COMPLETATA (9.0/10)
  ├── Audit Security+Ops+QA    ✅ 34+ finding trovati -> TUTTI P0 risolti
  ├── Script activate_vm.sh    ✅ 716 righe, 11 step (scripts/activate_vm.sh)
  ├── nginx hardened            ✅ Basic Auth + CSP-RO + Swagger blocked + headers fix
  ├── deploy.sh fixato          ✅ Backup DB + auto-detect path VM
  └── CI/CD fixato              ✅ merge --ff-only (no reset --hard)

FASE B - Rafa attiva VM       [....................] DA FARE (PROSSIMO STEP!)
  └── GCP Console: Start VM -> riserva IP statico -> comunicare IP a Cervella

FASE C - Cervella configura   [....................] DA FARE
  └── ./scripts/activate_vm.sh <NUOVO_IP>

FASE D - Rafa aggiorna DNS    [....................] DA FARE
  └── register.it: Record A miracollo.com + www -> nuovo IP

FASE E - Cervella deploy      [....................] DA FARE
  └── SSL + Docker + Smoke test

FASE F - Audit finale         [....................] DA FARE
```

### Credenziali Basic Auth PMS
- User: `miracollo`, Pass: [stored in nginx/.htpasswd, NOT in git]

### Discrepanza Path VM
4 path nella codebase: `~/app`, `/app/miracollo`, `/opt/miracollo`, `/app`
- deploy.sh + activate_vm.sh: auto-detect al runtime
- **Da unificare** dopo conferma su VM accesa

---

## INFRASTRUTTURA

```
VM miracollo-cervella (GCP us-central1-b):
  - STATO: IN PAUSA
  - Specs attuale: ARM64, 2 vCPU, 4GB RAM
  - Target: e2-small x86_64 (~$16/mese)
  - NOTA: ARM64 vs x86_64 - script verifica e avvisa

DNS: miracollo.com su register.it (Rafa aggiorna record A)
SSH: miracollo-vm (IP vecchio 34.27.179.164, script aggiorna)
```

---

## FILE MODIFICATI (sessione 22 Feb)

| File | Modifica |
|------|----------|
| `nginx/nginx.conf` | Basic Auth, CSP-RO, blocco Swagger, security headers inheritance fix |
| `docker-compose.yml` | Volume .htpasswd per nginx |
| `.gitignore` | .htpasswd escluso |
| `.env.production` | CORS = solo HTTPS miracollo.com |
| `deploy.sh` | Auto-detect path VM + backup DB pre-deploy |
| `.github/workflows/deploy.yml` | merge --ff-only (no reset --hard) |
| `scripts/activate_vm.sh` | **NUOVO** - automazione completa riattivazione VM |

**NOTA: Modifiche NON ancora committate! Fare git commit + push nella prossima sessione.**

---

## BUG CRITICI NOTI (pre-esistenti, non toccati)

- `guests.py:74-88` - INSERT 22 colonne ma 9 placeholder
- 98% endpoint senza auth (mitigato con Basic Auth Nginx)
- ~411 innerHTML senza escape in 94 file JS (mitigato con CSP-RO)

---

## SUBROADMAP: `roadmaps/SUBROADMAP_RECAP_RINASCITA_2026.md` (8.8/10)

## DECISIONI CHIUSE: D1 e2-small | D2 rimuovere cervellamiracollo | D3 register.it | D4 demo non urgente | D5 Room HW dopo

## BRACCI: `bracci/pms-core/`, `bracci/miracallook/`, `bracci/room-hardware/`

---

## Lezioni Apprese (Sessione FASE 1 Online)

### Funzionato bene
- **Swarm parallelo 4 Guardiane** - 34+ finding in ~5 min
- **Step-by-step con audit** - ogni fix verificato prima del successivo
- **Decisione autonoma Regina** - basic auth scelto senza bloccare Rafa

### Non funzionato
- **P0 "falsi"** - Security ha classificato .env.production P0 ma NON era in git
- **Health check non aggiornato** - Dopo basic auth, deploy.sh testava /api/health (401)

### Pattern candidato
- **Nginx add_header inheritance** - SEMPRE re-dichiarare headers in location con add_header
- **Auto-detect path** - Non hardcodare, verificare a runtime

---

*"Lavoriamo in pace! Senza casino! Dipende da noi!"*
*Cervella & Rafa - 22 Febbraio 2026*
