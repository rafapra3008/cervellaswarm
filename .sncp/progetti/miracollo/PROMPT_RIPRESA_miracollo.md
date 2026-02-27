<!-- DISCRIMINATORE: ECOSISTEMA MIRACOLLO - PANORAMA -->

# PROMPT RIPRESA - Ecosistema Miracollo

> **Ultimo aggiornamento:** 26 Febbraio 2026 - VM Migrata a e2-small + Fix Security
> **Status:** miracollo.com LIVE! VM e2-small x86 | Score Guardiana 9.3/10

---

## I 3 BRACCI

| Braccio | Porta | Score | Focus |
|---------|-------|-------|-------|
| **PMS Core** | 8001 | **LIVE su miracollo.com** | Manutenzione + bug fix |
| **Miracollook** | 8002 | 10/10 | READ-ONLY. Non toccare fino PMS >= 9.0 |
| **Room Hardware** | 8003 | 10% | Bloccato VLAN, DOPO |

---

## FASE 1 ONLINE - COMPLETATA!

```
FASE A - Preparazione         [####################] 100% (9.0/10)
FASE B - VM Online            [####################] 100%
  ├── VM accesa via gcloud CLI  (Cervella ha accesso diretto!)
  ├── IP statico 34.134.72.207  (nome: miracollo-static-ip)
  └── SSH miracollo-vm           (chiave cervella_miracollo)
FASE C - Deploy               [####################] 100%
  ├── Git pull (025ada5)
  ├── Basic Auth .htpasswd       (user: miracollo, pass in nginx/.htpasswd)
  ├── Docker rebuild             (3 bug fixati: tenacity + slowapi + certbot)
  ├── CORS aggiornato            (https://miracollo.com)
  └── DB backup pre-deploy
FASE D - DNS                  [####################] 100%
  ├── A: miracollo.com -> 34.134.72.207
  └── CNAME: www -> miracollo.com (pre-esistente)
FASE E - Smoke Test           [####################] 100%
  ├── /health -> 200 (healthy, DB connected, v1.7.0)
  ├── / -> 401 senza auth
  └── / -> 200 con auth (Rafa ha verificato nel browser!)
FASE F - Audit Guardiana      [####################] 100% (9.1/10)
```

---

## INFRASTRUTTURA LIVE

```
VM miracollo-cervella (GCP us-central1-b):
  - STATO: RUNNING
  - Machine: e2-small, x86_64, 2 vCPU, 2GB RAM (~$16/mese)
  - IP statico: 34.134.72.207
  - Disco: 20G (48% usato)
  - Path repo: /home/rafapra/app
  - Git remote: SSH con deploy key (ed25519)
  - Docker: backend + nginx (healthy)
  - SSL: Let's Encrypt valido fino 1 Apr 2026
  - SSL auto-renew: certbot timer systemd + webroot (dry-run OK!)
  - ACME challenge: /.well-known/acme-challenge/ in nginx port 80
  - SECRET_KEY: 128 char random (aggiornata 26 Feb 2026)
  - MIRACOLLO_API_URL: http://backend:8001/api (rete Docker interna)

DNS: miracollo.com -> 34.134.72.207 (register.it)
SSH: miracollo-vm (34.134.72.207, chiave cervella_miracollo)
gcloud: Cervella ha accesso CLI completo (progetto data-frame-476309-v3)
```

### Credenziali
- Basic Auth: user=`miracollo`, pass=[stored in nginx/.htpasswd, NOT in git]
- Rafa ha le credenziali e ha verificato accesso nel browser

---

## BUG FIX FATTI DURANTE DEPLOY

| Bug | Fix | Commit |
|-----|-----|--------|
| `tenacity` mancante da requirements.txt | Aggiunto `tenacity>=8.2.0` | 496e823 |
| `slowapi` exempt_when non supportato v0.1.9 | Custom key_func per health | 62b6251 |
| CORS con vecchio IP | Aggiornato a https://miracollo.com | (VM .env) |
| Certbot renewal falliva (authenticator=nginx) | Webroot + ACME location | 025ada5 |
| BeSync poller 401 (passava per nginx auth) | MIRACOLLO_API_URL=http://backend:8001/api | d1b14e9 |
| Security headers duplicati nginx/backend | proxy_hide_header in nginx | efc52ee |
| SECRET_KEY="test123" in produzione | Generata key random 128 char | (VM .env) |
| Certbot non installato su nuova VM | apt install certbot + timer OK | (VM) |
| Git pull impossibile (no credentials) | Deploy key SSH ed25519 | (VM) |

## BUG CRITICI NOTI (pre-esistenti)

- ~~`guests.py:74-88` - INSERT 22 colonne ma 9 placeholder~~ FIXATO (33 col + 33 ?)
- 98% endpoint senza auth app-level (mitigato con Basic Auth Nginx)
- ~411 innerHTML senza escape in 94 file JS (mitigato con CSP-RO)

---

## PROSSIMI STEP

1. **Aggiornare GitHub Secrets** per auto-deploy (VM_HOST=34.134.72.207, VM_USER=rafapra, SSH_PRIVATE_KEY)
2. **Monitorare** miracollo.com nei prossimi giorni (uptime, errori, RAM 57%)
3. **CSP enforce** (da Report-Only a enforce dopo monitoraggio)
4. **Auth app-level** (login vero per sostituire Basic Auth nel futuro)
5. **Valutare WORKERS=1** se RAM scende sotto 500M available

## DECISIONI CHIUSE

D1 e2-small target | D2 rimuovere cervellamiracollo | D3 register.it | D4 demo non urgente | D5 Room HW dopo | D6 gcloud CLI | D7 Basic Auth resta | D8 VM migrata a e2-small (risparmio costo, Rafa approvato 26 Feb)

## PUNTATORI

| Cosa | Path |
|------|------|
| **Fortezza (accessi, infra, security)** | `guide/FORTEZZA_MIRACOLLO.md` |
| Bracci | `bracci/pms-core/`, `bracci/miracallook/`, `bracci/room-hardware/` |
| Subroadmap | `roadmaps/SUBROADMAP_RECAP_RINASCITA_2026.md` (8.8/10) |

---

## Lezioni Apprese (Sessione Migrazione VM - 26 Feb 2026)

### Funzionato bene
- **Step-by-step con Guardiana audit** - ogni step -> score -> fix P2 -> avanti
- **Deploy key SSH** - soluzione pulita per git pull sulla VM senza credenziali
- **Rete Docker interna** - MIRACOLLO_API_URL=http://backend:8001/api bypassa nginx auth

### Non funzionato
- **docker compose restart non rilegge .env** - serve down/up per nuove variabili
- **Certbot non migrato** - la nuova VM non aveva certbot installato
- **Default API URL nel codice** - puntava a https://miracollo.com che passa per nginx auth

### Pattern candidato
- **Post-migrazione: verificare SEMPRE certbot, git, secrets** - Evidenza: 3 cose mancanti sulla nuova VM
- **proxy_hide_header per security headers** - nginx e source of truth, backend non deve duplicare
- **docker compose down/up (non restart) per .env changes** - Evidenza: restart non rilegge env_file

---

*"Lavoriamo in pace! Senza casino! Dipende da noi!"*
*Cervella & Rafa - 26 Febbraio 2026*

---