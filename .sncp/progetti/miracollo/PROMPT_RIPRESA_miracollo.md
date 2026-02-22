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
  ├── VM accesa via gcloud CLI  ✅ (Cervella ha accesso diretto!)
  ├── IP statico 34.134.72.207  ✅ (nome: miracollo-static-ip)
  └── SSH miracollo-vm           ✅ (chiave cervella_miracollo)
FASE C - Deploy               [####################] 100%
  ├── Git pull (62b6251)         ✅
  ├── Basic Auth .htpasswd       ✅ (user: miracollo)
  ├── Docker rebuild             ✅ (2 bug fixati: tenacity + slowapi)
  ├── CORS aggiornato            ✅ (https://miracollo.com)
  └── DB backup pre-deploy       ✅
FASE D - DNS                  [####################] 100%
  ├── A: miracollo.com -> 34.134.72.207       ✅
  └── CNAME: www -> miracollo.com (pre-esistente) ✅
FASE E - Smoke Test           [####################] 100%
  ├── /health -> 200 (healthy, DB connected)   ✅
  ├── / -> 401 senza auth                      ✅
  └── / -> 200 con auth                        ✅
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
  - SSL: Let's Encrypt valido fino 1 Apr 2026 (auto-renew attivo)
  - Certbot timer: attivo (systemd)

DNS: miracollo.com -> 34.134.72.207 (register.it)
SSH: miracollo-vm (34.134.72.207, chiave cervella_miracollo)
```

### Credenziali
- Basic Auth: user=`miracollo`, pass=[stored in nginx/.htpasswd, NOT in git]

---

## BUG FIX FATTI DURANTE DEPLOY

| Bug | Fix | Commit |
|-----|-----|--------|
| `tenacity` mancante da requirements.txt | Aggiunto `tenacity>=8.2.0` | 496e823 |
| `slowapi` exempt_when non supportato v0.1.9 | Custom key_func per health | 62b6251 |
| CORS con vecchio IP | Aggiornato a https://miracollo.com | (VM .env) |

## BUG CRITICI NOTI (pre-esistenti)

- `guests.py:74-88` - INSERT 22 colonne ma 9 placeholder
- 98% endpoint senza auth app-level (mitigato con Basic Auth Nginx)
- ~411 innerHTML senza escape in 94 file JS (mitigato con CSP-RO)
- Machine type ARM64 vs target e2-small (costo da valutare)

---

## PROSSIMI STEP

1. **Monitorare** miracollo.com nei prossimi giorni
2. **SSL renew** - auto, ma verificare prima del 1 Apr 2026
3. **Bug fix** guests.py INSERT (crash)
4. **Valutare** migrazione a e2-small (costo)
5. **CSP enforce** (da Report-Only a enforce dopo monitoraggio)

## DECISIONI CHIUSE

D1 e2-small target | D2 rimuovere cervellamiracollo | D3 register.it | D4 demo non urgente | D5 Room HW dopo | D6 gcloud CLI (Cervella accesso diretto GCP)

## BRACCI: `bracci/pms-core/`, `bracci/miracallook/`, `bracci/room-hardware/`

## SUBROADMAP: `roadmaps/SUBROADMAP_RECAP_RINASCITA_2026.md` (8.8/10)

---

## Lezioni Apprese (Sessione FASE 1 Online - Deploy)

### Funzionato bene
- **gcloud CLI** - Cervella fa TUTTO senza bloccare Rafa (start VM, IP statico, firewall)
- **Step-by-step con audit** - ogni fase -> Guardiana -> score -> prossima
- **Bug trovati durante deploy** - meglio in staging che in produzione

### Non funzionato
- **requirements.txt incompleto** - tenacity usato ma mai aggiunto
- **slowapi API break** - exempt_when documentato ma non in v0.1.9

### Pattern candidato
- **SEMPRE testare docker build in locale prima del deploy** - avrebbe trovato entrambi i bug
- **gcloud CLI > GCP Console** - piu sicuro, tracciabile, ripetibile

---

*"Lavoriamo in pace! Senza casino! Dipende da noi!"*
*Cervella & Rafa - 22 Febbraio 2026*
