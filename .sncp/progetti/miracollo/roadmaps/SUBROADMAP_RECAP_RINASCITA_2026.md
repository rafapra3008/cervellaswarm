# SUBROADMAP - Recap & Rinascita Miracollo

> **Creata:** 22 Febbraio 2026
> **Trigger:** Rafa vuole recap gigante + mostrare a ditta tedesca
> **Basata su:** 3 audit paralleli (Ingegnera 6.5/10, Guardiana QA 6.5/10, DevOps)
> **Audit subroadmap:** Guardiana 8.8/10 -> correzioni applicate
> **Strategia:** Ogni fase -> Guardiana audit -> target 9.5/10

---

## QUADRO ATTUALE

```
+================================================================+
|   MIRACOLLO - STATO REALE (26 Febbraio 2026)                  |
|                                                                |
|   CODICE:         6.5/10 (3 critici post-fix, 5 alti)         |
|   DOCUMENTAZIONE: 6.5/10 (3 critici, 8 medi, ~250 orfani)    |
|   INFRASTRUTTURA: VM LIVE e2-small, DNS OK, IP statico        |
|   OBIETTIVO:      9.5/10 su tutto                             |
+================================================================+
```

---

## FASE 0 - EMERGENZE (fix subito, prima di tutto)

> **Target:** Eliminare bug attivi e rischi immediati
> **Status:** COMPLETATA (26 Feb 2026) - tutti i task verificati

| # | Task | File | Stato |
|---|------|------|-------|
| 0.1 | ~~Fix BUG create_guest~~ | `backend/routers/guests.py:74-88` | GIA FIXATO: 33 col + 33 ? + 33 valori (corretto) |
| 0.2 | ~~Verificare .env.production nella storia Git~~ | Audit completo Guardiana Ops | VERIFICATO: nessun .env reale, .db o .htpasswd nella storia. 3 secrets minori in file tracked (repo PRIVATO, rischio basso) |
| 0.3 | ~~Aggiungere `reports/` a .gitignore~~ | `.gitignore:57-58` | GIA PRESENTE |
| 0.4 | ~~Fix uptime_seconds~~ | `backend/main.py:483` | GIA FIXATO: usa `_app_start_time` |

**Guardiana audit FASE 0: IN ATTESA (dopo completamento VM resize)**

---

## FASE 1 - DEMO DITTA TEDESCA (rendere Miracollo accessibile)

> **Target:** miracollo.com funzionante e visitabile dall'esterno
> **Status:** COMPLETATA (22 Feb 2026) + VM RESIZE (26 Feb 2026)
> **VM migrata:** n4a-standard-1 ARM64 (~$32/mese) -> e2-small x86 (~$17.51/mese) = -$15/mese

| # | Task | Dettagli | Chi |
|---|------|----------|-----|
| 1.1 | Riattivare VM `miracollo-cervella` | GCP Console, zona us-central1-b | Rafa |
| 1.2 | Riservare IP statico GCP | ~$3.65/mese, assegnare a miracollo-cervella | Rafa/Cervella |
| 1.3 | Aggiornare SSH config | Nuovo IP in `~/.ssh/config` (entry `miracollo-vm`) | Cervella |
| 1.4 | Rimuovere entry `cervellamiracollo` da SSH config | VM gia eliminata su GCP (confermato Rafa) | Cervella |
| 1.5 | Aggiornare DNS miracollo.com | Record A -> nuovo IP statico su **register.it** | Rafa |
| 1.6 | Aggiungere tag `https-server` alla VM GCP | Necessario per traffico HTTPS esterno | Cervella |
| 1.7 | Verificare SSL Let's Encrypt | `certbot renew` sulla VM | Cervella |
| 1.8 | `docker-compose up -d` sulla VM | Rebuild + avvio PMS Core | Cervella |
| 1.9 | Smoke test completo | /health, /api/bookings, planning, ospiti | Cervella |
| 1.10 | Riattivare come **e2-small** (2GB) | ~$16/mese - decisione Rafa 22 Feb | Cervella/Rafa |

**DNS attuale:** miracollo.com -> IP da verificare dopo riattivazione VM
**GCP Instance:** miracollo-cervella, zona us-central1-b, internal 10.128.0.7
**NOTA:** IP esterno probabilmente rilasciato (VM in pausa). Servira nuovo IP statico.
**Costo stimato:** ~$16/mese (e2-small + IP statico)

**Guardiana audit FASE 1 dopo completamento.**

---

## FASE 2 - SICUREZZA (blindare il sistema) - COMPLETATA!

> **Target:** Da 5.8% endpoint protetti a 100%
> **Status:** COMPLETATA 27 Febbraio 2026 - Score Guardiana 9.2/10

| # | Task | Stato | Score |
|---|------|-------|-------|
| 2.1 | Auth Middleware globale | ✅ LIVE | 9.5/10 |
| 2.2 | CSP Enforce + Security Headers | ✅ DONE | 9.0/10 |
| 2.3 | escapeHtml centralizzata + XSS fix | ✅ DONE | 9.0/10 |
| 2.4 | DB purge git history (filter-repo) | ✅ DONE | 9.3/10 |
| 2.5 | Rate limiting Nginx granulare (3 zone) | ✅ DONE | 9.2/10 |

**Residuo P2:** security.js incluso in 12/29 HTML (planning.html manca - prossima FASE)

**Guardiana audit FASE 2: COMPLETATO 9.2/10**

---

## FASE 3 - DOCUMENTAZIONE (sync e pulizia) - COMPLETATA!

> **Target:** Da 6.5/10 a 9.5/10 - zero contraddizioni
> **Status:** COMPLETATA 27 Febbraio 2026 - Score Guardiana 9.0/10 -> fix P2 applicati

### 3A. Fix Critici (P1)

| # | Task | Problema |
|---|------|----------|
| 3A.1 | ~~Aggiornare PROMPT_RIPRESA.md nella ROOT~~ | ✅ Gia redirect corretto, data aggiornata |
| 3A.2 | ~~Aggiornare PROMPT_RIPRESA_miracollo.md~~ | ✅ Gia aggiornato sessione FASE 2 |
| 3A.3 | ~~Deprecare .sncp/stato/oggi.md locale~~ | ✅ Sostituito con redirect, hook non attivo |

### 3B. Fix Medi (P2)

| # | Task | Problema |
|---|------|----------|
| 3B.1 | ~~Fix NORD.md~~ | ✅ FASE 3 60%->80%, puntatori CervellaSwarm |
| 3B.2 | ~~Fix NORD_PMS-CORE.md~~ | ✅ :8000->:8001, 85%->90% |
| 3B.3 | ~~Fix stato.md PMS Core~~ | ✅ React->HTML/CSS/JS, 85%->90%, FASE 2 |
| 3B.4 | ~~Fix stato.md Miracollook~~ | ✅ 92%->10/10, READ-ONLY, integration |
| 3B.5 | ~~Standardizzare container name~~ | ✅ FORTEZZA fixato, storici lasciati |
| 3B.6 | ~~Fix CLAUDE.md~~ | ✅ Gia corretto (nessun errore trovato) |

### 3C. Pulizia (P3)

| # | Task | Dettagli |
|---|------|----------|
| 3C.1 | ~~Deprecare .sncp/ locale~~ | ✅ README OBSOLETO + .gitignore + git rm --cached 100 file |
| 3C.2 | ~~Archiviare .checkpoints/~~ | ✅ 49 file eliminati (erano in .gitignore) |
| 3C.3 | ~~Archiviare .swarm/~~ | ✅ 290 file git rm --cached + .gitignore + tasks/handoff eliminati |
| 3C.4 | ~~Archiviare reports/~~ | ✅ 90+ file eliminati (erano in .gitignore) |
| 3C.5 | ~~File orfani ROOT~~ | ✅ BULK_HOUSEKEEPING_OUTPUT + .task_output eliminati |
| 3C.6 | ~~HANDOFF nella .swarm/~~ | ✅ Eliminati con .swarm/ |

**Contraddizioni da risolvere (tabella chiave):**

```
Miracollook:  8.5/10 vs 10/10 vs 92% -> ✅ FIXATO: 10/10 ovunque
PMS Score:    85% vs 90%              -> ✅ FIXATO: 90% ovunque
Pulizia Casa: 2/6 vs 6/6             -> ✅ FIXATO: 6/6 (gia corretto in PROMPT_RIPRESA)
FASE 3:       60% (3/5) vs 80% (4/5) -> ✅ FIXATO: 80% in NORD.md
Container:    -13, -35, -1            -> ✅ FIXATO: FORTEZZA aggiornata, storici OK
Porta PMS:    :8000 vs :8001          -> ✅ FIXATO: :8001 in NORD_PMS-CORE
```

**Guardiana audit FASE 3: COMPLETATO 9.0/10 -> fix P2 applicati (FORTEZZA allineata)**

---

## FASE 4 - QUALITA CODICE (debito tecnico) - COMPLETATA!

> **Target:** Health codice da 6.5/10 a 8.5/10
> **Status:** COMPLETATA 6 Marzo 2026 - Guardiana audit in corso

| # | Task | Stato | Score |
|---|------|-------|-------|
| 4.1 | Specializzare `except Exception` (~130+ catches in 80+ file) | ✅ DONE | 9.3/10 |
| 4.2 | Migrare `on_event("startup")` a `lifespan` | ✅ DONE | 9.6/10 |
| 4.3 | Split `cm_reservation.py` (737L -> 5 file package) | ✅ DONE | 9.7/10 |
| 4.4 | `revenue.js` (1288L) era dead code - RIMOSSO | ✅ DONE | N/A |
| 4.5 | Valutazione file >650L: 10 candidati, nessuno critico | ✅ DONE | N/A |
| 4.6 | async/def: documentare convenzione, NO mass-conversion | ✅ DECISIONE | N/A |
| 4.7 | 22 TODO/FIXME: tutti intenzionali (zero tech debt) | ✅ DONE | N/A |

**Extra fix (6 Mar sessione 1):** P2 security.js 28/29 HTML (97%), sender.py dead code, datetime.utcnow()

**Extra fix (6 Mar sessione 2 - post-RINASCITA):**
- P0: Token Telegram rimosso da git (deploy.sh.DEPRECATED)
- P1: File duplicato subscription.py eliminato
- M1-M3: WhatsApp timing-safe + token no-log + /docs /redoc /openapi.json off in prod
- P2: 22 print() -> logger + 28 console.log debug rimossi
- P2: 22 except Exception specializzati + 25 annotati intenzionali + 1 bare except fixato
- P2: 2 file esempio rimossi (EXAMPLE_USAGE_IN_ROUTER.py, example_integration.py)
- P2: backend/backend/ anomalia rimossa, miracallook/ rimosso (workspace separato)
- Docs: FORTEZZA aggiornata (SSL rinnovato 31 Mag, backup cron, security fix)

**Guardiana audit finale: IN CORSO**

---

## FASE 5 - INFRASTRUTTURA (ordine nella casa) - COMPLETATA!

> **Target:** Setup pulito, riproducibile, documentato
> **Status:** COMPLETATA 6 Marzo 2026

| # | Task | Stato |
|---|------|-------|
| 5.1 | Pulire SSH config | ✅ Rimossa entry cervellamiracollo, fix ARM64->x86 |
| 5.2 | Documentare mappa porte | ✅ Gia in CLAUDE.md (8001/8002/8003) |
| 5.3 | Conflitti porte locali | ✅ Nessun conflitto reale |
| 5.4 | Nginx config VM | ✅ Verificata (3 rate limit zones, SSL, CSP enforce) |
| 5.5 | deploy.sh | ✅ GitHub Actions v4.1.0 lo sostituisce |
| 5.6 | pre_deploy_snapshot | N/A - CI/CD ha rollback automatico |
| 5.7 | rollback.sh | ✅ Gia esistente in scripts/ |
| 5.8 | Cron backup DB | ✅ LIVE (2x/giorno 00:30+12:30 UTC, 7d retention, ~96KB) |
| 5.9 | CI/CD (GitHub Actions) | ✅ GIA LIVE (v4.1.0, test import + rollback) |
| 5.10 | Accessi VM | ✅ SSH OK, Docker healthy (up 6 days) |

**NOTA:** Contabilita NON si tocca. Solo Miracollo.

**FORTEZZA aggiornata:** 6 Marzo 2026 - FASE 4 + deploy status corretti

---

## FASE 6 - ACCESSI E VITA MIRACOLLO (stabilita) - COMPLETATA!

> **Target:** Tutto accessibile, documentato, funzionante
> **Status:** COMPLETATA 6 Marzo 2026

| # | Task | Stato |
|---|------|-------|
| 6.1 | SSH | ✅ miracollo-vm OK, VM up 1 week |
| 6.2 | GCP Console | ✅ RUNNING, gcloud CLI funzionante |
| 6.3 | GitHub | ✅ push/pull OK |
| 6.4 | DNS registrar | ✅ miracollo.com LIVE (Rafa gestisce register.it) |
| 6.5 | Guida riattivazione | ✅ FORTEZZA_MIRACOLLO.md e la guida completa |
| 6.6 | Secrets su VM | ✅ 72 variabili in .env, tutti presenti |

**Tutti gli accessi verificati e funzionanti.**

---

## PRIORITA E ORDINE

```
URGENTE (per demo ditta tedesca):
  FASE 0 -> FASE 1 -> FASE 2 (almeno 2.1 auth)

IMPORTANTE (qualita sistema):
  FASE 3 -> FASE 4

STABILITA (lungo termine):
  FASE 5 -> FASE 6
```

---

## DECISIONI CHIUSE (22 Feb 2026 - Rafa)

| # | Decisione | Risposta Rafa |
|---|-----------|---------------|
| D1 | VM size | **e2-small** (~$16/mese) - piu economica per ora |
| D2 | `cervellamiracollo` SSH | VM probabilmente gia eliminata su GCP. Rimuovere entry da SSH config |
| D3 | DNS miracollo.com | **register.it** - Rafa cambia il record A quando serve |
| D4 | Demo ditta tedesca | NON urgente - "sistemiamo piano piano, nostro modo, con calma" |
| D5 | Room Hardware VLAN | DOPO - non preoccuparsi ora |

---

## METRICHE

| Metrica | Attuale | Target | Come |
|---------|---------|--------|------|
| Health Codice | 6.5/10 -> 9.2 -> **audit in corso** | 9.5/10 | FASE 0+2+4 + post-RINASCITA |
| Health Docs | 6.5/10 -> **9.0/10** | 9.5/10 | FASE 3 DONE! |
| Security | 5.8% -> 100% -> **M1-M3 fixati** | 9.5/10 | Auth + timing-safe + docs off |
| File orfani | ~250 -> **~0** | 0 | 390+157+8 file rimossi da tracking |
| Contraddizioni docs | 6+ -> **0** | 0 | FASE 3A+3B DONE! |
| VM accessibile | ~~NO~~ -> **SI** | SI | FASE 1 DONE! |
| DNS corretto | ~~NO~~ -> **SI** | SI | FASE 1 DONE! |
| SSL | scadeva 1 Apr -> **rinnovato 31 Mag** | auto | certbot auto-renew CONFERMATO |
| Script deploy/backup | 0 -> **CI/CD + cron 2x/day** | 4+ | FASE 5 DONE! |

---

*"Non abbiamo fretta. Vogliamo la PERFEZIONE."*
*"Un progresso al giorno = 365 progressi all'anno."*

*Cervella & Rafa - 6 Marzo 2026 (post-RINASCITA, sessione pulizia profonda)*
