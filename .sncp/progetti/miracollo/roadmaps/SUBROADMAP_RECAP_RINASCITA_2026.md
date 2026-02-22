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
|   MIRACOLLO - STATO REALE (22 Febbraio 2026)                  |
|                                                                |
|   CODICE:         6.5/10 (4 critici, 5 alti)                  |
|   DOCUMENTAZIONE: 6.5/10 (3 critici, 8 medi, ~250 orfani)    |
|   INFRASTRUTTURA: VM spenta, DNS sbagliato, IP non fisso      |
|   OBIETTIVO:      9.5/10 su tutto                             |
+================================================================+
```

---

## FASE 0 - EMERGENZE (fix subito, prima di tutto)

> **Target:** Eliminare bug attivi e rischi immediati

| # | Task | File | Stima | Prio |
|---|------|------|-------|------|
| 0.1 | Fix BUG create_guest (22 colonne, 9 placeholder) | `backend/routers/guests.py:74-88` | 10 min | CRITICO |
| 0.2 | Verificare .env.production NON sia nella storia Git | `git log -- .env.production` (gia coperto da `.env.*` in .gitignore) | 5 min | CRITICO |
| 0.3 | Aggiungere `reports/` a .gitignore | `.gitignore` (*.backup gia coperto) | 5 min | ALTO |
| 0.4 | Fix uptime_seconds (psutil.boot_time -> app start) | `backend/main.py:479` | 5 min | BASSO |

**Guardiana audit FASE 0 dopo completamento.**

---

## FASE 1 - DEMO DITTA TEDESCA (rendere Miracollo accessibile)

> **Target:** miracollo.com funzionante e visitabile dall'esterno
> **Prerequisito:** Rafa riattiva VM da Google Cloud Console

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

## FASE 2 - SICUREZZA (blindare il sistema)

> **Target:** Da 5.8% endpoint protetti a 100%

| # | Task | Dettagli | Stima |
|---|------|----------|-------|
| 2.1 | Autenticazione globale su TUTTI gli endpoint admin | Middleware o dependency injection su 396 route in 83 file. Whitelist: /health, /public/*. Richiede triage + test. | 1-2 giorni |
| 2.2 | Aggiungere `Content-Security-Policy` header | `backend/middleware/security.py` | 1 ora |
| 2.3 | Triage + fix XSS: `escapeHtml()` globale nel frontend | ~362 innerHTML assignments in 82 file JS (16 file hanno gia sanitize parziale). Serve triage prima, poi fix. | 1-2 giorni |
| 2.4 | Rimuovere DB backup dalla storia Git | `git filter-repo` per eliminare dati GDPR | 30 min |
| 2.5 | Valutare rate limiting con Redis o single-worker | Attuale in-memory non funziona con 5 workers | Studio |

**NOTA SICUREZZA:**
- 373 endpoint senza auth = chiunque puo modificare prenotazioni, tariffe, pagamenti
- ~362 innerHTML senza escape in 82 file JS = rischio XSS stored
- DB backup nella storia Git = dati personali esposti
- NOTA: Score NORD.md diceva 9.5/10 ma era pre-audit dettagliato. Il 6.5/10 e il risultato del nuovo audit approfondito (85 tool calls, 83 file analizzati)

**Guardiana audit FASE 2 dopo completamento.**

---

## FASE 3 - DOCUMENTAZIONE (sync e pulizia)

> **Target:** Da 6.5/10 a 9.5/10 - zero contraddizioni

### 3A. Fix Critici (P1)

| # | Task | Problema |
|---|------|----------|
| 3A.1 | Aggiornare o rimuovere `PROMPT_RIPRESA.md` nella ROOT | Fossile S167, dice "locale non esiste" (FALSO) |
| 3A.2 | Aggiornare `PROMPT_RIPRESA_miracollo.md` (ecosistema) | Fermo S300, dice Pulizia 2/6 (e 6/6), Miracollook 8.5 (e 10) |
| 3A.3 | Deprecare `.sncp/stato/oggi.md` locale | Fermo S167, hook ancora ci scrive |

### 3B. Fix Medi (P2)

| # | Task | Problema |
|---|------|----------|
| 3B.1 | Fix NORD.md | FASE 3: 60% -> 80%, path Room Manager rotto, sessione stale |
| 3B.2 | Fix NORD_PMS-CORE.md | Porta :8000 -> :8001, score 85% -> 90% |
| 3B.3 | Fix stato.md PMS Core | "React" -> "HTML/CSS/JS", score 85% -> 90% |
| 3B.4 | Aggiornare stato.md Miracollook | 92% -> 10/10, decisione READ-ONLY |
| 3B.5 | Standardizzare container name in docs | -13, -35, -1 -> verificare nome reale su VM |
| 3B.6 | Fix CLAUDE.md: container name, IP VM | Allineare con realta |

### 3C. Pulizia (P3)

| # | Task | Dettagli |
|---|------|----------|
| 3C.1 | Deprecare formalmente `.sncp/` locale | README "OBSOLETO - usa CervellaSwarm" |
| 3C.2 | Archiviare `.checkpoints/` | 49 file Dic 2025, peso morto |
| 3C.3 | Archiviare `.swarm/tasks/` | 100+ file task Gen 2026 |
| 3C.4 | Archiviare/rimuovere `reports/` | 82 JSON + 6.5MB |
| 3C.5 | Spostare file orfani dalla ROOT | BULK_HOUSEKEEPING_OUTPUT.md, .task_output_* |
| 3C.6 | Archiviare HANDOFF S170/S171 | Dalla root SNCP a archivio |

**Contraddizioni da risolvere (tabella chiave):**

```
Miracollook:  8.5/10 vs 10/10 vs 92% -> REALE: 10/10
PMS Score:    85% vs 90%              -> REALE: 90%
Pulizia Casa: 2/6 vs 6/6             -> REALE: 6/6 completata
FASE 3:       60% (3/5) vs 80% (4/5) -> REALE: 80% (4/5)
Container:    -13, -35, -1            -> VERIFICARE su VM
Porta PMS:    :8000 vs :8001          -> REALE: :8001
```

**Guardiana audit FASE 3 dopo completamento.**

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
| Health Codice | 6.5/10 | 9.5/10 | FASE 0+2+4 |
| Health Docs | 6.5/10 | 9.5/10 | FASE 3 |
| Endpoint autenticati | 5.8% | 100% | FASE 2.1 |
| File orfani | ~250 | 0 | FASE 3C |
| Contraddizioni docs | 6+ | 0 | FASE 3A+3B |
| VM accessibile | NO | SI | FASE 1 |
| DNS corretto | NO | SI | FASE 1.5 |
| Script deploy/backup | 0 | 4+ | FASE 5.5-5.8 |

---

*"Non abbiamo fretta. Vogliamo la PERFEZIONE."*
*"Un progresso al giorno = 365 progressi all'anno."*

*Cervella & Rafa - 22 Febbraio 2026*
