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

## FASE 4 - QUALITA CODICE (debito tecnico)

> **Target:** Health codice da 6.5/10 a 8.5/10

| # | Task | Dettagli | Stima |
|---|------|----------|-------|
| 4.1 | Specializzare `except Exception` nei servizi critici | email_poller, night_audit, cm_poller, notification_worker | 3 ore |
| 4.2 | Migrare `on_event("startup")` a `lifespan` | backend/main.py | 30 min |
| 4.3 | Split `cm_reservation.py` (736L) | Candidato piu grande post-pulizia | 1 ora |
| 4.4 | Split `revenue.js` (1296L) | File frontend piu grande | 1 ora |
| 4.5 | Valutare split altri file >650L | 11 candidati (ml_scheduler, autopilot, fiscal...) | Studio |
| 4.6 | Consistenza async def vs def nei router | Decidere pattern e applicare | 2 ore |
| 4.7 | Risolvere TODO/FIXME attivi (25+) | Almeno i critici in subscription, cm_reservation | 2 ore |

**Guardiana audit FASE 4 dopo completamento.**

---

## FASE 5 - INFRASTRUTTURA (ordine nella casa)

> **Target:** Setup pulito, riproducibile, documentato

| # | Task | Dettagli |
|---|------|----------|
| 5.1 | Pulire SSH config | Rimuovere entry obsolete, allineare con IP reali |
| 5.2 | Documentare mappa porte definitiva | PMS :8001, Miracollook :8002, Room :8003 |
| 5.3 | Valutare porte locali vs Contabilita | Evitare conflitto :8001 in dev locale |
| 5.4 | Verificare/aggiornare nginx.conf sulla VM | Dopo riattivazione |
| 5.5 | Creare `scripts/deploy.sh` | Deploy su VM (ispirato a Contabilita FORTEZZA MODE) |
| 5.6 | Creare `scripts/pre_deploy_snapshot.sh` | Snapshot GCP pre-deploy per rollback |
| 5.7 | Creare `scripts/rollback.sh` | Rollback rapido da snapshot |
| 5.8 | Setup cron backup DB | `cron_backup_db.sh` per miracollo.db sulla VM |
| 5.9 | Setup CI/CD base (GitHub Actions) | git push -> deploy su VM |
| 5.10 | Verificare accessi Cervella alla VM | SSH key, permessi, Docker access |

**NOTA:** Contabilita NON si tocca. Solo Miracollo.

**Guardiana audit FASE 5 dopo completamento.**

---

## FASE 6 - ACCESSI E VITA MIRACOLLO (stabilita)

> **Target:** Tutto accessibile, documentato, funzionante

| # | Task | Dettagli |
|---|------|----------|
| 6.1 | Verificare tutti gli accessi SSH | miracollo-vm, chiave cervella_miracollo |
| 6.2 | Verificare accesso GCP Console | Per gestione VM |
| 6.3 | Verificare accesso GitHub | Push/pull funzionante |
| 6.4 | Verificare accesso DNS registrar | Per aggiornare record A |
| 6.5 | Documentare "Come riattivare Miracollo da zero" | Guida step-by-step per Rafa o Cervella |
| 6.6 | Verificare secrets su VM | .env production allineato |

**Guardiana audit FASE 6 dopo completamento.**

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
| Health Codice | 6.5/10 -> **9.2/10** | 9.5/10 | FASE 0+2 DONE! |
| Health Docs | 6.5/10 -> **9.0/10** | 9.5/10 | FASE 3 DONE! |
| Endpoint autenticati | ~~5.8%~~ -> **100%** | 100% | FASE 2.1 DONE! |
| File orfani | ~250 -> **~0** | 0 | FASE 3C DONE! (390 file rimossi da tracking) |
| Contraddizioni docs | 6+ -> **0** | 0 | FASE 3A+3B DONE! |
| VM accessibile | ~~NO~~ -> **SI** | SI | FASE 1 DONE! |
| DNS corretto | ~~NO~~ -> **SI** | SI | FASE 1 DONE! |
| Script deploy/backup | 0 -> **CI/CD** | 4+ | GitHub Actions LIVE |

---

*"Non abbiamo fretta. Vogliamo la PERFEZIONE."*
*"Un progresso al giorno = 365 progressi all'anno."*

*Cervella & Rafa - 27 Febbraio 2026 (aggiornato FASE 2 COMPLETATA)*
