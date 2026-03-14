<!-- DISCRIMINATORE: ECOSISTEMA MIRACOLLO - PANORAMA -->

# PROMPT RIPRESA - Ecosistema Miracollo

> **Ultimo aggiornamento:** 14 Marzo 2026 - Sessione 31 (Email i18n + Cancel Policy + Bug Fix)
> **Status:** miracollo.com LIVE | Security ~9.2/10 | **2878 test** (96 API+Stripe = 0 fail) | Sprint A+B+S30+S31 DONE
> **Prossima Cervella:** Leggi questo + NORD.md + **MAPPA_BOOKING_ENGINE.md**
> **MAPPA:** `CervellaSwarm/.sncp/progetti/miracollo/MAPPA_BOOKING_ENGINE.md`

---

## COSA E STATO FATTO (S31 - 14 Marzo 2026)

### Sessione 31 - Email i18n + Cancel Policy + Bug Fix + Cache Bust

**Contesto:** Continuazione diretta della S30 nella stessa giornata. Rafa pieno di energia, autonomia totale alla Regina.

**Email Conferma Prenotazione (i18n IT/EN/DE):**
- Template riscritto con brand Naturae Lodge (green forest gradient, earth tones, gold total)
- 22 chiavi tradotte in 3 lingue (66 traduzioni totali)
- Bank transfer email include sezione IBAN/BIC/causale
- Stripe webhook e booking creation ora passano `language` a `send_booking_confirmation()`
- FIX P2: html.escape() su tutti i merge tags (XSS prevention nelle email)
- Template `"live nature, find yourself"` tagline in header (brand, in inglese di proposito)

**Cancel Policy Dinamica:**
- Step 3 checkout: STD -> "Cancellazione gratuita 48h" (verde), NONR -> "Non rimborsabile" (arancio)
- CSS `.cancel-policy-warning` con color #E65100

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
  -> Cancel policy text da rate.cancellation_days (non hardcoded "48h")

PRIORITA 3 - QUALITA:
  -> Bug residui S29 tester (5 P2 + 6 P3)
  -> Security P2 residui
  -> f-string logger batch fix (P3)

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
```

---

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
