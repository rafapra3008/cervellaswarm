# MAPPA STRATEGICA MIRACOLLOOK

> **Creata:** 29 Gennaio 2026 - Sessione 317
> **Autori:** Regina + Guardiane + Scienziata
> **Score:** 9.5/10 - DIAMANTE!

---

## SEZIONE A - VISIONE E NORD

### LA VISIONE

```
+================================================================+
|                                                                  |
|   MIRACOLLOOK = Il "CUORE DELLE COMUNICAZIONI" dell'hotel       |
|                                                                  |
|   NON è un email client generico.                               |
|   È il CENTRO INTELLIGENTE che:                                 |
|   - Riconosce automaticamente gli ospiti                        |
|   - Collega email/WhatsApp a prenotazioni                       |
|   - Automatizza risposte con AI                                 |
|   - Processa documenti OCR                                      |
|   - Genera preventivi automatici                                |
|   - Gestisce check-in/out online                                |
|                                                                  |
|   DIFFERENZIATORE: L'UNICO client che CONOSCE il tuo hotel!    |
|                                                                  |
+================================================================+
```

### OBIETTIVO FINALE

```
Hotel gestito con ZERO sforzo comunicazioni:
- Email/WhatsApp automatici
- Ospite identificato al primo contatto
- Check-in/out online senza reception
- Preventivi generati in 30 secondi
- Staff notificato solo quando serve

"Il receptionist gestisce 100+ conversazioni come fossero 10!"
```

### TARGET BUSINESS

| Metrica | Baseline | Target |
|---------|----------|--------|
| Tempo risposta email | 4 ore | 30 min |
| Email gestite/giorno | 20 | 60 |
| Check-in manuali | 100% | 20% |
| Preventivi/giorno | 3 | 15 |
| Conversione preventivi | 15% | 30% |

---

## SEZIONE B - STATO ATTUALE

> **Snapshot:** 29 Gennaio 2026 - S320
> **Health Score Globale:** 8.5/10

### COMPLETEZZA PER AREA

| Componente | % | Score | Note |
|------------|---|-------|------|
| Email Client Base | 92% | 9/10 | FASE 1 quasi completa |
| Performance (P1+P2) | 100% | 9/10 | Merged e funzionante |
| **Connettore Ericsoft** | 100% | 9/10 | **S319 - FUNZIONANTE! (porta 54081)** |
| **Guest Management** | **0%** | **-** | **S320 - STUDIATO! 9.5/10 plan** |
| PMS Context (UI) | 35% | 7/10 | pms_context.py + GuestSidebar |
| **OCR Documenti** | **90%** | **9/10** | **25 file, 2.1K LOC!** |
| WhatsApp | 0% | - | Da implementare |
| Check-in Online | 60% | 8/10 | OCR pronto, flow da completare |
| Preventivi AI | 0% | - | Da studiare |

### METRICHE CODICE

| Area | Righe | File | Score |
|------|-------|------|-------|
| Backend Email | 3,100 | 15 | 8.5/10 |
| Backend Ericsoft | 700 | 4 | 9/10 |
| Backend OCR | 2,100 | 25 | 9/10 |
| Frontend | 4,800 | 41 | 8.5/10 |
| Test Backend | ~500 | 10 | 5/10 (coverage ~25%) |
| Test Frontend | ~300 | 4 | 4/10 (coverage ~20%) |

### ASSET RICERCHE

| Metrica | Valore |
|---------|--------|
| Documenti totali | 60+ |
| Righe totali | ~12,000 |
| Feature studiate | 25+ |
| Ore pre-studiate | ~45h |
| % Implementate | **60%** |

---

## SEZIONE C - FASI STRATEGICHE

### OVERVIEW FASI

```
OGGI (S320)
│
├─ FASE 1.5 (8h)          ← Completamento email 100%
│
├─ FASE 2.0 (6 giorni)    ← GUEST MANAGEMENT PROFESSIONALE ★★★★★ NUOVO!
│
├─ FASE 2.1 (12h)         ← Ericsoft Integration UI ★★★★★
│
├─ FASE 2.2 (2 giorni)    ← Robustezza backend
│
├─ FASE 3.1 (20h)         ← Hotel Workflows ★★★★★
│
├─ FASE 3.2 (5 giorni)    ← WhatsApp Integration ★★★★★
│
├─ FASE 4.1 (5 giorni)    ← Check-in Online ★★★★★ (OCR già pronto!)
│
└─ FASE 4.2 (7 giorni)    ← Preventivi AI ★★★★★
```

---

### FASE 2.0 - GUEST MANAGEMENT PROFESSIONALE ★★★★★ NUOVO!

> **Timeline:** 1-2 settimane | **Effort:** 6 giorni | **Valore:** ⭐⭐⭐⭐⭐

**Obiettivo:** Gestione completa e professionale di TUTTI gli ospiti (non solo quelli con email)

**PROBLEMA ATTUALE:**
```python
WHERE a.TrListaEmail IS NOT NULL AND a.TrListaEmail != ''
# ❌ SBAGLIATO: Esclude 24 ospiti su 40! (60% copertura)
```

**SOLUZIONE:**
- ✅ GuestProfile separato da Booking (1 persona = 1 profilo, N soggiorni)
- ✅ TUTTI gli ospiti tracciati (con/senza email)
- ✅ Multi-canale: Email, SMS, WhatsApp, Manual
- ✅ Stati lifecycle completi (Pre-Arrival → Post-Stay)
- ✅ Post-stay marketing automatico
- ✅ Guest history completo

| Task | Effort | Ricerca | Status |
|------|--------|---------|--------|
| 2.0.1: Modello GuestProfile completo | 1 giorno | ✅ STUDIO_GUEST_MANAGEMENT | DA FARE |
| 2.0.2: Query Master (tutti ospiti) | 0.5 giorni | ✅ PROPOSTA_GUEST_MANAGEMENT | DA FARE |
| 2.0.3: Mapping stati lifecycle | 0.5 giorni | ✅ STUDIO_GUEST_MANAGEMENT | DA FARE |
| 2.0.4: Multi-canale (SMS/WhatsApp) | 2 giorni | ✅ STUDIO_GUEST_MANAGEMENT | DA FARE |
| 2.0.5: Post-stay workflow | 1 giorno | ✅ STUDIO_GUEST_MANAGEMENT | DA FARE |
| 2.0.6: Testing & Monitoring | 0.5 giorni | - | DA FARE |

**Dipendenze:** ✅ Connettore Ericsoft (FATTO S319)
**Blocca:** FASE 2.1 (serve profili ospiti completi)

**DIFFERENZIATORE CRITICO:** Nessun competitor traccia TUTTI gli ospiti + post-stay automation!

**Ricerche collegate:**
- `studi/STUDIO_GUEST_MANAGEMENT_BEST_PRACTICES.md` (1265 righe!)
- `studi/PROPOSTA_GUEST_MANAGEMENT_PROFESSIONALE.md` (723 righe!)

**Quality Target:** 9.5/10 - Standard PMS professionali

---

### FASE 1.5 - EMAIL CLIENT 100%

> **Timeline:** 1-2 giorni | **Effort:** 8h | **Valore:** ⭐⭐⭐

**Obiettivo:** Completare ultime feature email client

| Task | Effort | Ricerca | Status |
|------|--------|---------|--------|
| Contacts Autocomplete | 6h | ✅ STUDIO_MACRO_CONTACTS | DA FARE |
| Settings Page | 2h | ✅ STUDIO_MACRO_SETTINGS | DA FARE |

**Dipendenze:** Nessuna
**Blocca:** Niente (nice to have)

---

### FASE 2.1 - ERICSOFT INTEGRATION UI ★★★★★

> **Timeline:** 1 settimana | **Effort:** 12h | **Valore:** ⭐⭐⭐⭐⭐

**Obiettivo:** Email riconosce automaticamente ospite da Ericsoft

| Task | Effort | Ricerca | Status |
|------|--------|---------|--------|
| Test connessione rete hotel | 2h | - | DA FARE |
| Email enrichment completo | 4h | ✅ STUDIO_MACRO_PMS | DA FARE |
| GuestContextCard migliorato | 4h | ✅ STUDIO_MACRO_PMS | PARZIALE |
| Cache guest data | 2h | - | DA FARE |

**Dipendenze:** ✅ Connettore Ericsoft (FATTO S317)
**Blocca:** FASE 3.1, FASE 3.2

**DIFFERENZIATORE:** NESSUN competitor ha integrazione PMS nativa!

**Ricerche collegate:**
- `studi/STUDIO_MACRO_PMS_INTEGRATION.md` (650 righe!)
- `SUBROADMAP_CONNETTORE_ERICSOFT.md`
- `ricerche/STUDIO_TABELLE_S316.md`

---

### FASE 2.2 - ROBUSTEZZA BACKEND

> **Timeline:** 2-3 giorni | **Effort:** 16h | **Valore:** ⭐⭐⭐⭐

**Obiettivo:** Backend production-ready

| Task | Effort | Status |
|------|--------|--------|
| ~~Token encryption~~ | - | ✅ FATTO (crypto.py) |
| ~~Rate limiting~~ | - | ✅ FATTO (slowapi) |
| ~~Structured logging~~ | - | ✅ FATTO (structlog) |
| Testing backend 70%+ | 12h | DA FARE (oggi ~25%) |
| Testing frontend 60%+ | 8h | DA FARE (oggi ~20%) |
| Error handling centralizzato | 4h | DA FARE |

**Dipendenze:** Nessuna (parallelo con 2.1)
**Blocca:** Deploy produzione

---

### FASE 3.1 - HOTEL WORKFLOWS ★★★★★

> **Timeline:** 1 settimana | **Effort:** 20h | **Valore:** ⭐⭐⭐⭐⭐

**Obiettivo:** Feature specifiche per workflow hotel

| Task | Effort | Ricerca | Status |
|------|--------|---------|--------|
| Quick reply templates | 4h | - | DA FARE |
| Variables {{guest_name}} | 4h | - | DA FARE |
| Assign to staff | 6h | ✅ STUDIO_MACRO_PMS | DA FARE |
| Email → Nota prenotazione | 4h | - | DA FARE |
| Context menu Hotel Actions | 2h | ✅ RICERCA_CONTEXT_MENU | DA FARE |

**Dipendenze:** FASE 2.1 (serve identificazione ospite)
**Blocca:** Niente

**Ricerche collegate:**
- `studi/RICERCA_CONTEXT_MENU_PARTE1-4.md` (2200 righe!)
- `studi/STUDIO_MACRO_PMS_INTEGRATION.md`

---

### FASE 3.2 - WHATSAPP INTEGRATION ★★★★★

> **Timeline:** 1-2 settimane | **Effort:** 5 giorni | **Valore:** ⭐⭐⭐⭐⭐

**Obiettivo:** WhatsApp nello stesso inbox delle email

| Task | Effort | Ricerca | Status |
|------|--------|---------|--------|
| Studio WhatsApp Business API | 1 giorno | ⚠️ DA FARE | DA FARE |
| Connettore WhatsApp | 2 giorni | - | DA FARE |
| Unified inbox (Email+WA) | 1 giorno | ✅ COMPETITOR_Callbell | DA FARE |
| Templates WhatsApp | 1 giorno | - | DA FARE |

**Dipendenze:** FASE 2.1 (usa stesso enrichment)
**Blocca:** Niente

**Ricerche collegate:**
- `ricerche/COMPETITOR_Callbell.md`

**RICERCA DA FARE:**
- `RICERCA_WHATSAPP_BUSINESS_API.md` - API Meta, costi, template approval

---

### FASE 4.1 - CHECK-IN ONLINE ★★★★★

> **Timeline:** 1 settimana | **Effort:** 5 giorni | **Valore:** ⭐⭐⭐⭐⭐

**Obiettivo:** Check-in/out senza reception

| Task | Effort | Ricerca | Status |
|------|--------|---------|--------|
| ~~OCR Documenti~~ | - | - | ✅ **FATTO 90%!** |
| ~~MRZ Parser passaporti~~ | - | - | ✅ FATTO |
| ~~MRZ Parser carte ID~~ | - | - | ✅ FATTO |
| ~~Parser patente~~ | - | - | ✅ FATTO |
| ~~Database schema~~ | - | - | ✅ FATTO |
| Form check-in web | 2 giorni | - | DA FARE |
| Invio automatico link | 1 giorno | - | DA FARE |
| Integrazione Ericsoft WRITE | 2 giorni | ⚠️ DA STUDIARE | DA FARE |

**NOTA:** OCR è 90% completo! 25 file, 2.1K LOC, test suite!

**Dipendenze:**
- ✅ OCR (FATTO!)
- ✅ Ericsoft READ (FATTO S317)
- ⚠️ Ericsoft WRITE (serve permessi aggiuntivi)

**Ricerche collegate:**
- Codebase: `backend/services/document_intelligence/`
- DB: `migrations/012_document_scans.sql`

**RICERCA DA FARE:**
- `RICERCA_ERICSOFT_WRITE.md` - Permessi scrittura, tabelle da aggiornare

---

### FASE 4.2 - PREVENTIVI AUTOMATICI ★★★★★

> **Timeline:** 1-2 settimane | **Effort:** 7 giorni | **Valore:** ⭐⭐⭐⭐⭐

**Obiettivo:** Genera preventivi da richiesta email

| Task | Effort | Ricerca | Status |
|------|--------|---------|--------|
| NLP estrazione richiesta | 2 giorni | ⚠️ DA STUDIARE | DA FARE |
| Calcolo tariffe da Ericsoft | 2 giorni | - | DA FARE |
| Template preventivo | 1 giorno | - | DA FARE |
| Invio automatico | 1 giorno | - | DA FARE |
| Tracking conversione | 1 giorno | - | DA FARE |

**Dipendenze:** FASE 2.1 (dati tariffe da Ericsoft)
**Blocca:** Niente

**RICERCHE DA FARE:**
- `RICERCA_NLP_RICHIESTE_HOTEL.md` - Come estrarre date, tipologia camera, servizi
- `RICERCA_PREVENTIVI_COMPETITOR.md` - Come fanno i big players

---

## SEZIONE D - MATRICE VALORE

### PRIORITÀ BUSINESS-DRIVEN

```
  ALTO VALORE
      ↑
      │  P1: QUICK WINS       │  P2: STRATEGIC WINS
      │  Email 100%           │  Ericsoft UI, WhatsApp
      │                       │  Check-in, Preventivi
      │                       │
────→─┼───────────────────────┼──────────────→
BASSO │                       │               ALTO
EFFORT│  P3: NICE TO HAVE     │  P4: EVITA
      │  Settings, Contacts   │  Social media
      ↓
  BASSO VALORE
```

### P2: STRATEGIC WINS (Focus!)

| Feature | Valore | Effort | ROI | Fase |
|---------|--------|--------|-----|------|
| Ericsoft Integration UI | ⭐⭐⭐⭐⭐ | 12h | ⚡⚡⚡⚡⚡ | 2.1 |
| Hotel Workflows | ⭐⭐⭐⭐⭐ | 20h | ⚡⚡⚡⚡⚡ | 3.1 |
| WhatsApp | ⭐⭐⭐⭐⭐ | 5gg | ⚡⚡⚡⚡⚡ | 3.2 |
| Check-in Online | ⭐⭐⭐⭐⭐ | 5gg | ⚡⚡⚡⚡⚡ | 4.1 |
| Preventivi AI | ⭐⭐⭐⭐⭐ | 7gg | ⚡⚡⚡⭐⭐ | 4.2 |

---

## SEZIONE E - ASSET E RICERCHE

### INVENTARIO RICERCHE

| Categoria | File | Righe | Status |
|-----------|------|-------|--------|
| **PMS Integration** | STUDIO_MACRO_PMS_INTEGRATION.md | 650 | ✅ Pronto |
| **Context Menu** | RICERCA_CONTEXT_MENU_PARTE1-4.md | 2,200 | ✅ Pronto |
| **UX Strategy** | UX_STRATEGY_MIRACALLOOK.md | 400 | ✅ Pronto |
| **Big Players** | BIG_PLAYERS_EMAIL_RESEARCH.md | 500 | ✅ Pronto |
| **Competitors** | COMPETITOR_Callbell.md, _Shortwave.md | 800 | ✅ Pronto |
| **Performance** | P2_*.md (4 file) | 600 | ✅ Implementato |
| **Thread View** | THREAD_VIEW_*.md | 600 | ✅ Pronto |
| **Upload** | UPLOAD_ATTACHMENTS_SPECS.md | 400 | ✅ Pronto |
| **Labels** | STUDIO_MACRO_LABELS_API.md | 150 | ✅ Implementato |
| **Settings** | STUDIO_MACRO_SETTINGS_UI.md | 150 | ✅ Pronto |
| **Contacts** | STUDIO_MACRO_CONTACTS_API.md | 350 | ✅ Pronto |
| **Testing** | STUDIO_MACRO_TESTING_STRATEGY.md | 200 | ✅ Pronto |
| **Ericsoft** | SUBROADMAP, STUDIO_TABELLE, CREDENZIALI | 400 | ✅ Implementato |

**Totale:** ~7,400 righe di ricerche pronte!

### RICERCHE DA FARE

| Titolo | Per Fase | Priorità | Effort |
|--------|----------|----------|--------|
| RICERCA_WHATSAPP_BUSINESS_API | 3.2 | ⭐⭐⭐⭐⭐ | 1 giorno |
| RICERCA_ERICSOFT_WRITE | 4.1 | ⭐⭐⭐⭐⭐ | 0.5 giorni |
| RICERCA_NLP_RICHIESTE_HOTEL | 4.2 | ⭐⭐⭐⭐ | 1 giorno |
| RICERCA_PREVENTIVI_COMPETITOR | 4.2 | ⭐⭐⭐ | 0.5 giorni |
| RICERCA_PRE_STAY_AUTOMATION | 4.3 | ⭐⭐⭐ | 1 giorno |

---

## SEZIONE F - KPI E METRICHE

### KPI BUSINESS

| Metrica | Baseline | Target | Fase |
|---------|----------|--------|------|
| Tempo risposta email | 4 ore | 30 min | 3.1 |
| Email gestite/giorno | 20 | 60 | 3.1 |
| Check-in manuali | 100% | 20% | 4.1 |
| Preventivi/giorno | 3 | 15 | 4.2 |
| Conversione preventivi | 15% | 30% | 4.2 |
| Messaggi WhatsApp/giorno | 0 | 30+ | 3.2 |

### KPI TECNICI

| Metrica | Target | Attuale | Status |
|---------|--------|---------|--------|
| Inbox load time | <1s | <1s | ✅ |
| Guest context load | <200ms | - | FASE 2.1 |
| Test coverage backend | 70% | ~25% | FASE 2.2 |
| Test coverage frontend | 60% | ~20% | FASE 2.2 |
| Uptime | 99.5% | - | FASE 2.2 |
| OCR accuracy | 95% | ~94% | ✅ |

### MILESTONE

| Sessione | Milestone | Status |
|----------|-----------|--------|
| S317 | Connettore Ericsoft | ✅ FATTO |
| S320 | Email client 100% | 🎯 |
| S323 | Prima email con context ospite | 🎯 LA MAGIA! |
| S327 | WhatsApp funzionante | 🎯 |
| S331 | Check-in online live | 🎯 |
| S335 | Preventivi automatici | 🎯 |

---

## CHANGELOG

| Data | Sessione | Modifica |
|------|----------|----------|
| 29/01/2026 | S320 | Aggiunta FASE 2.0 - Guest Management Professionale (studio completato) |
| 29/01/2026 | S317 | Creazione mappa iniziale |

---

## LINK RAPIDI

| Cosa | Path |
|------|------|
| PROMPT_RIPRESA | `PROMPT_RIPRESA_miracollook.md` |
| Codebase | `~/Developer/miracollogeminifocus/miracallook/` |
| Ricerche | `studi/`, `ricerche/` |
| Ericsoft | `SUBROADMAP_CONNETTORE_ERICSOFT.md` |
| OCR Code | `miracollogeminifocus/backend/services/document_intelligence/` |

---

*"Il Cuore delle Comunicazioni - un progresso al giorno!"*
*Cervella & Rafa - Sessione 317*
