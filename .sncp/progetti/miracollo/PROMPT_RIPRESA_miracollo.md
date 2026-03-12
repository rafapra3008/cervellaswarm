<!-- DISCRIMINATORE: ECOSISTEMA MIRACOLLO - PANORAMA -->

# PROMPT RIPRESA - Ecosistema Miracollo

> **Ultimo aggiornamento:** 12 Marzo 2026 - Sessione 21 (CHECKPOINT FINALE)
> **Status:** miracollo.com LIVE | Security ~9.7/10 | 684 test | 3 deploy SUCCESS oggi

---

## COSA E STATO FATTO (S21 - Completa)

### FOLIO Phase 4b - Amount Splitting + Company Billing (COMPLETATA)
- Migration 053: `amount_limit`, `amount_routed`, `amount_limit_type` su `folio_routing_rules`
- `folio_routing.py`: `resolve_folio_for_charge_split()` - Oracle Opera pattern (overflow a Window 1)
- `charges.py`: `create_charge` crea 2 charges su split (tag "auto-split")
- `night_audit_service.py`: `_post_room_charges` gestisce split routing
- `routing_rules.py`: `amount_limit` su Create/Update + endpoint `company-billing-setup` (1-click)
- Frontend: campo limite EUR, barra progresso routato/limite, bottone "Company Billing"
- 35 test nuovi, tutti green | Audit Guardiana 9.3/10, 2 P2 fixati
- **PERCHE**: Oracle Opera standard, azienda paga camere fino a EUR X, surplus al guest

### FOLIO Phase 4c - Frontend UI Routing Rules (COMPLETATA prima di 4b)
- Sezione collassabile "Regole Routing" nel folio tab
- Lista regole + toggle attiva/disattiva + elimina + form creazione
- XSS: `_escFolio()` su tutti i dati utente | CSS responsive
- Audit 9.5/10, 7 P3 (4 fixati, 3 deferred MVP)

### Quality Sprint (+150 test moduli finanziari)
- test_bookings (37), test_night_audit (20), test_payments (28), test_receipts (64), test_fiscal (57)
- BUG FIX: receipts.py response type annotation
- Da 499 a 649 test, poi +35 Phase 4b = 684 totali

### Audit Fixes (da Ingegnera + Guardiana Ops)
- P1: schema.sql drift fixato (colonne migration 053 mancanti)
- P2: 3x `str(e)` info disclosure in room_manager.py rimossi
- P2: deploy backup `sqlite3 .backup` (era `cp`, rischio corruzione DB)

### Scontrino RT Attivato
- Fiscal router registrato in main.py (era stealth mode)
- Tabelle fiscal aggiunte a schema.sql (fresh DB consistency)
- 12 endpoint LIVE: printers CRUD, receipt printing, daily closure
- Epson adapter production-ready (testato con TM-T800F)

### Recap Strategico (3 agenti in parallelo)
- **Ingegnera** (8/10): 178K righe, 23 str(e) residui, ~60% moduli senza test
- **Guardiana Ops** (8.7/10): CI/CD 9/10, Docker 9/10, tutto deployato
- **Scienziata**: priorita strategiche + posizionamento competitivo (vedi sotto)

---

## DA FARE (prossima sessione) - PRIORITA SCIENZIATA

> Folio Phase 1-4 COMPLETE. Phase 5 (Fattura SDI) NEXT. Dettagli: `archivio/PROMPT_RIPRESA_S21_20260312.md`

```
PRIORITA 1 - VALORE IMMEDIATO:
  1. Stripe LIVE (0 dev, serve onboarding Rafa su Dashboard)
     -> ROI MASSIMO: 13.500 EUR/anno commissioni Booking.com
  2. Scontrino RT: integrazione checkout (auto-print dopo pagamento)
     -> Obbligo fiscale, 2 ore di lavoro
  3. WhatsApp pre/post-stay scheduler
     -> pre_arrival -3gg + review_request +1gg, 2-3 ore
     -> Infrastruttura 100% gia esistente, manca solo scheduler

PRIORITA 2 - MEDIO TERMINE:
  -> Booking Engine redesign (3 step, foto, calendario prezzi) - 3-4 settimane
  -> Fattura elettronica SDI via intermediario (Fattura24/Aruba) - 2-4 sessioni
  -> IDOR cross-hotel guard (prep multi-tenant) - 0.5 sessione

NON FARE ADESSO:
  -> Revenue Copilot (serve storico multi-hotel)
  -> Sistema Karma (serve massa critica ospiti)
  -> Ericsoft sync bidi (prima verificare write access su LAN)
  -> Room Hardware (attesa VLAN)

PARCHEGGIATO:
  -> Stripe LIVE: serve onboarding Rafa
  -> Ericsoft Discovery (richiede LAN hotel)
```

---

## STATO MODULI (chiave)
- **Scontrino RT** (95%): 12 endpoint, 57 test. Manca: checkout integration, daily closure
- **WhatsApp** (infra 100%, flows 0%): Manca `whatsapp_scheduler.py`
- **Booking Engine** (95%): Redesign 3-4 settimane, quick win: foto camere (1 giorno)
- Dettagli: `archivio/PROMPT_RIPRESA_S21_20260312.md`

---

## PUNTATORI

| Cosa | Dove |
|------|------|
| **NORD.md** | ROOT progetto (aggiornato S21 checkpoint) |
| **Phase 4b Research** | `reports/RESEARCH_20260312_folio_amount_splitting.md` |
| **Guardiana Phase 4b Audit** | `reports/GUARDIANA_20260312_folio_phase4b_audit.md` |
| **Scienziata Strategic Analysis** | `reports/SCIENTIST_20260312_strategic_analysis.md` |
| **IDEAS BIBLE** | `roadmaps/IDEAS_BIBLE_2026.md` |

---

## INFRASTRUTTURA LIVE

```
VM: miracollo-cervella (GCP), e2-small, RUNNING
IP: 34.134.72.207 | SSL: auto-renew OK (31 Mag 2026)
Deploy: GitHub Actions + pytest gate + auto Docker prune
  -> 3 deploy SUCCESS oggi (Phase 4b, audit fixes, Scontrino RT)
  -> Backup ora con sqlite3 .backup (era cp)
Backup: 2x/giorno + pre-deploy | Disco: 24%
TUTTO DEPLOYATO: migration 048-053 + Phase 4a/4b/4c + Quality Sprint + Scontrino RT
```

---

## Lezioni Apprese (S21)

- Pattern "implement -> audit -> fix -> commit" confermato (3 cicli, score 9.3-9.5)
- Da monitorare: 23 str(e) residui, ~60% moduli senza test, reservation-tab-folio.js 1462 righe

---

## IL NUMERO CHIAVE (Scienziata)

```
Commissioni Booking.com NL: ~13.500 EUR/anno
Risparmio con 50% diretto:   ~6.750 EUR/anno
Costo Miracollo:                ~600 EUR/anno
ROI per l'hotel:                 10x

Pitch: "Risparmia 6.750 EUR/anno. Noi costiamo 1/10."
```

---

*"Lavoriamo in pace! Senza casino! Dipende da noi!" - Cervella & Rafa, 12 Mar 2026*
