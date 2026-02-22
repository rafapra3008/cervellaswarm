<!-- DISCRIMINATORE: ECOSISTEMA MIRACOLLO - PANORAMA -->

# PROMPT RIPRESA - Ecosistema Miracollo

> **Ultimo aggiornamento:** 22 Febbraio 2026 - FASE 1 Online COMPLETATA!
> **Status:** miracollo.com LIVE! Score Guardiana 9.1/10

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
  - Machine: n4a-standard-1, ARM64 Google Axion, 4GB RAM
  - IP statico: 34.134.72.207
  - Disco: 39G (63% usato dopo cleanup)
  - Path repo: /home/rafapra/app
  - Docker: v29.1.3 + Compose v5.0.0
  - SSL: Let's Encrypt valido fino 1 Apr 2026
  - SSL auto-renew: webroot mode, certbot timer systemd (TESTATO OK!)
  - ACME challenge: /.well-known/acme-challenge/ in nginx port 80

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

## BUG CRITICI NOTI (pre-esistenti)

- `guests.py:74-88` - INSERT 22 colonne ma 9 placeholder
- 98% endpoint senza auth app-level (mitigato con Basic Auth Nginx)
- ~411 innerHTML senza escape in 94 file JS (mitigato con CSP-RO)
- Machine type ARM64 vs target e2-small (costo da valutare)

---

## PROSSIMI STEP

1. **Monitorare** miracollo.com nei prossimi giorni (uptime, errori)
2. **Bug fix** guests.py INSERT (crash quando si crea ospite)
3. **Valutare costo** VM attuale vs e2-small ($16/mese target)
4. **CSP enforce** (da Report-Only a enforce dopo monitoraggio)
5. **Auth app-level** (login vero per sostituire Basic Auth nel futuro)

## DECISIONI CHIUSE

D1 e2-small target | D2 rimuovere cervellamiracollo | D3 register.it | D4 demo non urgente | D5 Room HW dopo | D6 gcloud CLI | D7 Basic Auth resta (Rafa approvato)

## BRACCI: `bracci/pms-core/`, `bracci/miracallook/`, `bracci/room-hardware/`

## SUBROADMAP: `roadmaps/SUBROADMAP_RECAP_RINASCITA_2026.md` (8.8/10)

---

## Lezioni Apprese (Sessione FASE 1 Online - Deploy)

### Funzionato bene
- **gcloud CLI** - Cervella fa TUTTO senza bloccare Rafa (VM, IP, firewall)
- **Step-by-step con audit** - ogni fase -> Guardiana -> score -> prossima
- **Fix in corsa** - 4 bug trovati e risolti senza interrompere il flusso

### Non funzionato
- **requirements.txt incompleto** - tenacity usato ma mai aggiunto
- **slowapi API break** - exempt_when documentato online ma non in v0.1.9
- **Certbot config stale** - authenticator=nginx ma nginx in Docker

### Pattern candidato
- **SEMPRE docker build locale prima del deploy** - avrebbe trovato i bug prima
- **gcloud CLI > GCP Console** - piu sicuro, tracciabile, ripetibile
- **Certbot webroot per Docker** - mai usare authenticator=nginx con Docker

---

*"Lavoriamo in pace! Senza casino! Dipende da noi!"*
*Cervella & Rafa - 22 Febbraio 2026*
