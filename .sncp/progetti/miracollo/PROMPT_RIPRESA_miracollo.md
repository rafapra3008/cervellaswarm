<!-- DISCRIMINATORE: ECOSISTEMA MIRACOLLO - PANORAMA -->

# PROMPT RIPRESA - Ecosistema Miracollo

> **Ultimo aggiornamento:** 14 Marzo 2026 - Sessione 32 (Bug Fix Batch + Security Hardening)
> **Status:** miracollo.com LIVE | Security ~9.5/10 | **2878 test** (2837 pass, 0 regr) | Sprint A+B+S30+S31+S32 DONE
> **Prossima Cervella:** Leggi questo + NORD.md + **MAPPA_BOOKING_ENGINE.md**
> **MAPPA:** `CervellaSwarm/.sncp/progetti/miracollo/MAPPA_BOOKING_ENGINE.md`

---

## COSA E STATO FATTO (S32 - 14 Marzo 2026)

### Sessione 32 - Bug Fix Batch + Security Hardening

**Contesto:** Sessione dedicata a fixare TUTTI i bug residui S29 + security P2. Strategia: ogni step -> Guardiana audit.

**Cancel Policy Dinamica (da cancellation_days):**
- i18n IT/EN/DE: `{days}` template invece di "48h" hardcoded
- Branch esplicito: `days > 0` -> testo con giorni, `days = 0` -> "Cancellazione gratuita" generico
- Falsy trap `|| 2` fixata (Guardiana P2 trovata e risolta)

**P2 Bug Fix (3 fixati, 2 gia risolti in sessioni precedenti):**
- API key logging: rimosso `x_api_key[:8]` dal warning log (info disclosure)
- Payment link: `token=simulated` -> `secrets.token_urlsafe(32)`
- Schema: `group_id INTEGER REFERENCES groups(id)` aggiunto al CREATE TABLE bookings base

**P3 Bug Fix (4 fixati):**
- Cancellation: ora void charges con `UPDATE status='voided'` (audit trail PMS standard)
- Legacy folio: `data.nights || daysBetween(...) || 1` (fallback NaN prevention)
- Rate limit: evict empty keys dal dict (memory leak fix)
- Import: `secrets` top-level in payments.py (era inline)

**Security Hardening:**
- `BookingUpdate.status`: `str` -> `Literal[6 valori]` (previene injection status arbitrario)
- X-Forwarded-For: `[0]` -> `[-1]` su 4 file (anti-spoof Nginx-appended)
- `datetime.now()` -> `datetime.now(timezone.utc)` in 6 punti (checkin, bookings, payments, planning_ops x3)

**Audit:** 2 Guardiana (9.6/10 + 9.5/10), tutti finding fixati inclusi i 5 P3 post-audit
**Test:** 2837 pass, 0 regressioni, 1 pre-existing whatsapp mock fail

---

## COSA E STATO FATTO (S31 - 14 Marzo 2026)

### Sessione 31 - Email i18n + Cancel Policy + Bug Fix + Cache Bust

(Vedi sotto - stessa giornata della S32)

**Bug Fix:**
- `room.max_occupancy` -> `room.max_guests` (pre-existing: badge "Max N ospiti" ora appare)
- Footer version text allineato a v2.2.0
- Cache bust v2.1.0 -> v2.2.0 su tutti i file widget HTML

**1 commit pushato:** 0cb2309

---

## COSA E STATO FATTO (S30 - 14 Marzo 2026)

### Sessione 30 - Pagina /prenota + Rate Plans + Bug Fix

(Riassunto - stessa giornata della S31)
- Pagina /prenota dedicata (hero, trust bar, widget, "perche diretto", footer, i18n, WCAG)
- URL params deep-link (?checkin, ?checkout, ?adults, ?children, ?lang)
- Rate plans multipli: Standard + Non Rimborsabile (-10%) con badges
- 3 bug P1 fixati (security.js, photos schema, cache name_en/name_de)
- 2 commit pushati: e130ba5, a4d9b77

---

## DA FARE (prossima sessione)

```
PRIORITA 1 - GO-LIVE PREP:
  P0 bloccanti:
    [DONE S30] Pagina /prenota dedicata
    [DONE S30] Rate plans multipli
    [DONE S31] Email conferma i18n
    [DONE S31] Cancel policy dinamica
    -> Stripe LIVE keys (BLOCCATO su Rafa)
    -> Stripe webhook registrato su Stripe Dashboard
    -> Foto camere su VM (migration 057+058 da applicare)
    -> SMTP credentials su VM .env
    -> CSP Stripe su nginx (js.stripe.com)
    -> APP_BASE_URL su VM (https://miracollo.com)
    -> Test E2E completo

PRIORITA 2 - FEATURE:
  -> Stripe Elements embedded (Sprint C - blocca su Stripe keys)
  [DONE S32] Cancel policy da cancellation_days

PRIORITA 3 - QUALITA:
  [DONE S32] Bug residui S29 (P2+P3 tutti fixati)
  [DONE S32] Security P2 residui (Literal, XFF, datetime UTC)
  -> f-string logger batch fix (200+ punti in 100+ file - sessione dedicata)
  -> German umlauts i18n widget (pre-existing)

BLOCCATI (serve Rafa):
  -> Foto panoramica NL (hero /prenota + OG image social)
  -> Stripe LIVE keys (onboarding Stripe Dashboard)
  -> SMTP credentials (Gmail App Password o altro provider)
  -> WhatsApp Meta template approval
```

---

## PUNTATORI

| Cosa | Dove |
|------|------|
| **NORD.md** | ROOT progetto |
| **MAPPA BE** | `CervellaSwarm/.sncp/progetti/miracollo/MAPPA_BOOKING_ENGINE.md` |
| **Design UX** | `CervellaSwarm/.sncp/progetti/miracollo/handoff/DESIGN_UX_20260314.md` |
| **VISIONE** | `CervellaSwarm/.sncp/progetti/miracollo/roadmaps/VISIONE_PIATTAFORMA_2026.md` |

---

## INFRASTRUTTURA LIVE

```
VM: miracollo-cervella (GCP), e2-small, RUNNING
IP: 34.134.72.207 | SSL: auto-renew OK (31 Mag 2026)
Deploy: GitHub Actions + pytest gate (2878 test) + auto Docker prune + rollback
Backup: 2x/giorno + pre-deploy
Migration: 048-058 (057+058 da applicare su VM al prossimo deploy)
Monitoring: HetrixTools + dead-man's-switch scheduler
Widget: v2.2.0 (cache bust S31)
Security: ~9.5/10 (S32: XFF, Literal, UTC, key logging, token)
```

---

## Lezioni Apprese (S32)

### Cosa ha funzionato bene
- Strategia "ogni step -> Guardiana": 2 audit hanno trovato 6 finding (1 P2 + 5 P3) tutti fixati
- Ricercatrici in parallelo: una per codice, una per bug report = zero tempo perso
- Fix proattivi: 6 datetime.now() UTC + 4 XFF anti-spoof + import cleanup trovati lungo la strada
- Guardiana ha trovato la falsy trap `|| 2` che noi non avevamo visto (valore del pattern confermato)

### Da NON fare
- Mai usare `|| default` per valori che possono essere 0 legittimamente (falsy trap JS)
- Mai fare f-string logger batch su 200+ file in una sessione sola (rischio regressioni)
- X-Forwarded-For: MAI usare `[0]` (primo) dietro Nginx - sempre `[-1]` (ultimo = Nginx-appended)

### Pattern CONFERMATO
- "Guardiana dopo ogni step": 9a sessione consecutiva, 2 audit/sessione
- "Fix tutto quello che trovi": 13 file toccati, 6 fix extra non pianificati
- "Un passo alla volta": 5 step sequenziali, zero confusione, zero regressioni

## Lezioni Apprese (S31)

### Funzionato bene
- L'infrastruttura email ESISTEVA GIA (sender, templates, merge, config) - bastava migliorarla
- Esplorare PRIMA di costruire: la ricercatrice ha trovato tutto il codice esistente
- Fix proattivi (XSS, max_guests, version) fatti PRIMA della Guardiana
- Template i18n con f-string Python + merge tags: pattern pulito e mantenibile

### Da NON fare
- Mai inserire dati utente in HTML email senza html.escape() (il merge engine non lo faceva!)
- Mai hardcodare "48h" se il dato viene da cancellation_days (potrebbe cambiare)

### Pattern CONFERMATO
- "Guardiana dopo ogni step": 8a sessione consecutiva
- "Esplorare prima, implementare dopo": evitato riscrittura da zero dell'email
- "Fix tutto quello che trovi": 3 bug extra fixati lungo la strada

---

## COSE CHE SERVONO DA RAFA

| Cosa | Perche | Urgenza |
|------|--------|---------|
| **Foto panoramica NL** | Hero /prenota + OG image social | ALTA |
| **Stripe onboarding** | Keys LIVE per pagamenti reali | ALTA (blocca go-live) |
| **SMTP credentials** | Email conferma reali (ora simulate) | ALTA (blocca go-live) |
| **WhatsApp Meta approval** | Template per messaggi automatici | BASSA |

---

*"Fatto BENE > Fatto VELOCE" - S30+S31: 4 commit, 6 feature, 6 bug fix, 23 file, 3 Guardiane*
*"Ultrapassar os proprios limites!"*

*Cervella & Rafa, 14 Mar 2026*
<!-- AUTO-CHECKPOINT-START -->
## AUTO-CHECKPOINT: 2026-03-14 17:30 (unknown)
- **Branch**: master
- **Ultimo commit**: 39bf611 - docs: S31 checkpoint - NORD + MAPPA + PROMPT_RIPRESA aggiornati
- **File modificati**: Nessuno (git pulito)
<!-- AUTO-CHECKPOINT-END -->
