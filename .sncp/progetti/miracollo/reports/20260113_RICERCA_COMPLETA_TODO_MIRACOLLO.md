# RICERCA COMPLETA - TODO MIRACOLLO

**Data:** 13 Gennaio 2026
**Researcher:** Cervella Researcher
**Status:** COMPLETATO
**Fonti:** SNCP Miracollo (roadmaps, idee, stato, decisioni)

---

## EXECUTIVE SUMMARY

**Stato Miracollo:** Progetto solido con 3 moduli principali.
- **RateBoard:** 8.5/10 (2 fasi completate, 5 pianificate)
- **Miracollook:** 8.0/10 (MVP funzionante, da completare)
- **Revenue Intelligence:** 7/10 (GAP chiusi, ML in pianificazione)

**TODO Totali Identificati:** 147 task divisi in 3 progetti

---

## PROGETTO 1: RATEBOARD (RMS AI)

### Status Attuale
- **Score:** 8.5/10 → Target 9.5/10
- **Completato:** FASE 1 (Fondamenta), FASE 2 (Transparent AI), FASE 3 (Learning from Actions)
- **In Produzione:** Autopilot, What-If, Heatmap, AI Suggestions

### FASE 1: FONDAMENTA - Da Completare

| Task | Priorità | Effort | Status |
|------|----------|--------|--------|
| Test Autopilot dati reali | CRITICO | 3h | TODO |
| Test Coverage 60% | CRITICO | 12h | TODO |
| Fix Validazione | FATTO | - | ✅ |

**Perché Critico:** Non si costruisce su basi fragili. Test = fiducia.

---

### FASE 4: EXTERNAL DATA - Pianificato

**Obiettivo:** Integrare dati esterni per suggerimenti più intelligenti

| Task | Priorità | Effort | Fonti |
|------|----------|--------|-------|
| API Meteo integration | ALTO | 8h | OpenWeather |
| Eventi locali scraping | ALTO | 10h | Local APIs |
| Calendario festività IT | MEDIO | 4h | Dataset |
| Correlazione prezzi-eventi | MEDIO | 6h | Analytics |

**Vantaggio Competitivo:** IDeaS e Duetto NON hanno questo nativo!

---

### FASE 5: COMPETITOR REAL-TIME - POC Completato!

**Status:** 85% - POC PRONTO per test reali!

| Task | Priorità | Effort | Status |
|------|----------|--------|--------|
| **Integrare Playwright POC** | CRITICO | 4h | TODO |
| **Test con URL Booking reale** | CRITICO | 2h | TODO |
| **Setup CRON settimanale** | ALTO | 2h | TODO |
| Alert variazioni competitor | MEDIO | 4h | TODO |
| Suggerimenti basati competitor | MEDIO | 6h | TODO |

**NOVITÀ SESSIONE 186:**
- ✅ playwright_scraping_client.py creato (GRATIS!)
- ✅ competitor_scraping_service.py (520 righe)
- ✅ API REST completa (5 endpoint)
- ✅ Test Roma: 22 elementi con €

**Strategia:** Scraping ~1x settimana (tendenze), non aggressivo.

---

### FASE 6: MOONSHOT - MESSAGING BOT

**Obiettivo:** WhatsApp/Telegram per gestire Revenue dal telefono!

| Task | Priorità | Effort | Status |
|------|----------|--------|--------|
| Ricerca WhatsApp vs Telegram | MEDIO | 4h | Idea salvata |
| MVP Bot notifiche | MEDIO | 12h | TODO |
| Comandi interattivi | BASSO | 8h | TODO |
| Revenue nel telefono | BASSO | 12h | TODO |

**Vantaggio:** UNICO nel mondo! First mover advantage!

**File:** `.sncp/progetti/miracollo/idee/IDEA_MESSAGING_BOT_20260112.md`

---

### FASE 7: AI PLANNING - Suggerimenti in Planning

**Obiettivo:** Planning oggi gestisce prenotazioni. Domani suggerirà COME ottimizzarle!

| Task | Priorità | Effort | Status |
|------|----------|--------|--------|
| Ricerca AI per planning | MEDIO | 6h | TODO |
| Backend suggerimenti | MEDIO | 10h | TODO |
| Frontend UI planning | MEDIO | 8h | TODO |
| Integrare Transparent AI | MEDIO | 4h | TODO |
| Integrare Learning Loop | MEDIO | 4h | TODO |

**Possibili Suggerimenti:**
- "Sposta questa prenotazione per ottimizzare occupancy"
- "Proponi upgrade a camera più grande"
- "Guest ricorrente - offri sconto fedeltà"
- "Overbooking risk - considera alternativa"

---

### MODULI RATEBOARD - Completamento Features

#### 2.1 Bulk Edit (95% → 100%)
- [ ] Preview before apply (3h)
- [ ] Undo last operation (4h)
- [ ] Template bulk salvabili (4h)

#### 2.2 AI Suggestions (70% → 85%)
- [ ] Competitor pricing in suggerimenti (4h)
- [ ] Confidence scoring statistico (6h)
- [x] Learning from actions (FATTO!)

#### 2.3 Competitor Monitoring (60% → 80%)
- [ ] UI import batch prezzi (6h)
- [ ] CSV upload con mapping (8h)
- [ ] Alert competitor change (4h)
- [ ] Trend competitor nel tempo (6h)

#### 2.4 Detail Panel (95% → 100%)
- [ ] Historical chart 30 giorni (4h)
- [ ] Suggested price range (2h)

---

## PROGETTO 2: REVENUE INTELLIGENCE

### Status Attuale
- **Score:** 7/10 → Target 10/10
- **GAP #1:** RISOLTO (Price History)
- **GAP #2:** RISOLTO (Modal Preview)
- **GAP #3:** RICERCA OK (ML Enhancement)
- **GAP #4:** RICERCA OK (What-If Simulator)

### ROADMAP: Da 7/10 a 10/10

**File:** `.sncp/progetti/miracollo/roadmaps/20260112_ROADMAP_REVENUE_7_TO_10.md`

---

### FASE 1: IMMEDIATA (Settimana 1)

| Task | Effort | Owner | Status |
|------|--------|-------|--------|
| Test Manuale GAP #2 Modal | 2-3h | tester | FATTO ✅ |
| RateBoard Hard Tests | 4-5h | tester | TODO |
| Fix Bug Trovati | 4-8h | backend+frontend | TODO |
| formatDateRange Verification | 1h | frontend | TODO |

---

### FASE 2: STABILIZZAZIONE (Settimana 2-3)

| Task | Effort | Owner | Priority |
|------|--------|-------|----------|
| docker-compose.prod.yml | 8-10h | backend | CRITICO |
| Monitoring Dashboard | 10-12h | backend | ALTO |
| Error Tracking (Sentry) | 4-6h | backend | ALTO |
| Test Coverage 80%+ | 12-15h | tester | CRITICO |

**Metriche Target:**
- Test Coverage: 0% → 80%
- Uptime: ~95% → 99%
- API Latency p95: ? → <500ms

---

### FASE 3: ENHANCEMENT - What-If Simulator MVP (Settimana 4-6)

**Roadmap dedicata:** `.sncp/progetti/miracollo/roadmaps/ROADMAP_WHATIF_SIMULATOR.md`

**Obiettivo:** Dare valore SUBITO agli utenti!

#### Backend API What-If (30-35h)
- [ ] POST /api/v1/what-if/simulate (8h)
- [ ] Calcolo elasticity-based (6h)
- [ ] Response <300ms uncached (4h)
- [ ] Explanation text generator (4h)
- [ ] Competitor position logic (4h)
- [ ] Test endpoint (4h)

#### Caching What-If (8-10h)
- [ ] Cache PostgreSQL/Redis (6h)
- [ ] TTL 1 ora (2h)
- [ ] Cleanup automatico cron (2h)

#### Frontend What-If UI (40-50h)
- [ ] Componente WhatIfSimulator (12h)
- [ ] Slider prezzo con debounce (8h)
- [ ] Cards KPI (occupancy, revenue, competitor) (10h)
- [ ] Grafico price vs occupancy (12h)
- [ ] Mobile responsive (8h)

#### Test What-If (8-10h)
- [ ] 15 test backend (6h)
- [ ] 10 test frontend E2E (4h)

**Perché PRIMA del ML avanzato:**
1. Valore IMMEDIATO - Utenti vedono subito
2. Funziona con elasticity semplice
3. Costruisce fiducia
4. Base per ML futuro

---

### FASE 4: ENHANCEMENT - ML Database Foundation (Settimana 7-8)

**Obiettivo:** Preparare infrastruttura per ML training

#### Database Schema ML (20-25h)
- [ ] Tabella ai_pricing_decisions (6h)
- [ ] Tabella ml_training_runs (4h)
- [ ] Tabella ml_model_metrics (4h)
- [ ] Partitioning mensile (4h)
- [ ] Migration Alembic (2h)

#### API Tracking Decisioni (15-20h)
- [ ] POST /api/v1/pricing/decide (8h)
- [ ] Track ogni suggerimento ML (6h)
- [ ] Latency <50ms (4h)

#### Feature Engineering Base (30-35h)
- [ ] Funzione build_features() (10h)
- [ ] 8 features MVP (occupancy, pace, competitor, etc.) (15h)
- [ ] Features salvate in JSON (4h)
- [ ] Latency <200ms (4h)

**Features MVP:**
1. occupancy_rate
2. booking_pace_7d
3. lead_time_days
4. day_of_week
5. season (high/low)
6. competitor_avg_price
7. historical_revpar
8. current_price_acceptance_rate

---

### FASE 5: ADVANCED - ML Model Training (Mese 2-3)

**Obiettivo:** Primo modello ML funzionante

#### XGBoost Model Training (40-50h)
- [ ] Training script (15h)
- [ ] Accuracy (R2) >70% su test set (15h)
- [ ] Model versioning (10h)

**Rischio:** Samples insufficienti (<500)
**Mitigazione:** Synthetic data per bootstrap, aspettare dati reali

#### API /pricing/suggest (15-20h)
- [ ] Endpoint suggerimento ML (8h)
- [ ] Confidence score (4h)
- [ ] Explanation generata (4h)
- [ ] Latency <100ms (4h)

#### Feedback Loop Prevention (20-25h)
- [ ] Delayed evaluation 60 giorni (8h)
- [ ] Exploration 15% (6h)
- [ ] Sample weighting (6h)
- [ ] Monitoring feedback loop (4h)

#### Retraining Automatico (20-25h)
- [ ] Celery Beat schedule 14 giorni (8h)
- [ ] Auto-deployment nuovo model (8h)
- [ ] Rollback se peggiora (6h)
- [ ] Alert se fallisce (2h)

#### Drift Monitoring (20-25h)
- [ ] Evidently AI integrato (10h)
- [ ] Daily drift check (6h)
- [ ] Alert drift >30% (4h)
- [ ] Dashboard drift metrics (6h)

---

### TECH DEBT Revenue Intelligence

| Cosa | File | Priorità | Effort |
|------|------|----------|--------|
| File legacy revenue.js | `frontend/revenue.js` (1296 righe) | BASSA | 8h |
| hotelId hardcoded | 4 occorrenze | MEDIA | 2h |
| What-If Apply placeholder | `revenue-suggestions.js:558` | BASSA | 2h |
| Debug logs AI Panel | `rateboard-core.js` | BASSA | 1h |

---

## PROGETTO 3: MIRACOLLOOK

### Status Attuale
- **Score:** 8.0/10
- **FASE 0 (Fondamenta):** 100% ✅
- **FASE 1 (Email Solido):** 75%
- **FASE 2 (PMS Integration):** 0%
- **FASE 3 (Hotel Workflow):** 0%

**File:** `.sncp/progetti/miracollo/moduli/miracallook/ROADMAP_MIRACOLLOOK_MASTER.md`

---

### COMPLETATO (Sessione 187)
- ✅ Layout three-panel
- ✅ Inbox, Archived, Starred, Snoozed, Trash viste
- ✅ Send, Reply, Reply All, Forward
- ✅ Quick Actions (hover + keyboard)
- ✅ Keyboard shortcuts (j/k/e/r/c/f/s)
- ✅ Command Palette (Cmd+K)
- ✅ AI Summarization
- ✅ Smart Bundles
- ✅ Design Salutare (Tailwind v4)
- ✅ **Resize pannelli** (react-resizable-panels v4.4.0)
- ✅ **Attachments view + download** (streaming)

---

### FASE 1 - Email Client Solido (Da Completare)

#### CRITICO
| Feature | Priorità | Effort | Note |
|---------|----------|--------|------|
| **Split gmail/api.py** | CRITICO | 6h | 1391 righe! Serve refactor |
| **Attachments upload** | CRITICO | 6h | Compose con file |

#### ALTO
| Feature | Priorità | Effort | Note |
|---------|----------|--------|------|
| Multi-select | ALTO | 6h | Checkbox + batch actions |
| Undo actions | ALTO | 4h | Toast con "Undo" |
| Search avanzata UI | ALTO | 4h | Modal con filtri |
| Column sorting | MEDIO | 2h | Sort by date/sender |

#### MEDIO
| Feature | Priorità | Effort | Note |
|---------|----------|--------|------|
| Contacts autocomplete | MEDIO | 6h | Google Contacts API |
| Email signatures | MEDIO | 4h | Template footer |
| Custom labels UI | MEDIO | 6h | Create/edit labels |
| Desktop notifications | MEDIO | 4h | Web Notifications API |

---

### FASE 2 - PMS INTEGRATION (LA MAGIA!)

**Obiettivo:** Collegare email ai guest del PMS per context automatico.

#### Features
| Feature | Priorità | Effort | Note |
|---------|----------|--------|------|
| **Guest identification** | CRITICO | 8h | Match email → guest |
| **GuestSidebar reale** | CRITICO | 6h | Dati da PMS |
| **Booking context** | CRITICO | 4h | Prenotazioni attive |
| **Guest history** | ALTO | 6h | Email + booking passati |
| **Link to PMS** | ALTO | 2h | Deep link a scheda guest |

#### API Necessarie (da creare)
```
GET /pms/guest/by-email?email=xxx
GET /pms/guest/{id}/bookings
GET /pms/guest/{id}/history
```

---

### FASE 3 - HOTEL WORKFLOW

#### Assign & Team
| Feature | Priorità | Effort | Note |
|---------|----------|--------|------|
| **Assign to user** | CRITICO | 6h | Custom label |
| **Team inbox** | ALTO | 12h | Shared view |
| **Assignment notifications** | MEDIO | 4h | Alert quando assigned |

#### Templates Risposte
| Feature | Priorità | Effort | Note |
|---------|----------|--------|------|
| **Quick replies** | CRITICO | 4h | Template storage |
| **Template categories** | ALTO | 2h | Check-in, Info, etc |
| **Variables** | ALTO | 4h | {{guest_name}}, {{room}} |
| **Template editor** | MEDIO | 6h | UI creazione |

#### Preventivi Auto
| Feature | Priorità | Effort | Note |
|---------|----------|--------|------|
| **Detect quote request** | ALTO | 8h | AI parsing |
| **Generate quote PDF** | ALTO | 12h | PMS integration |
| **1-click send** | ALTO | 4h | Attach + reply |

---

### TECHNICAL DEBT Miracollook

#### Critico
- [ ] Split gmail/api.py (1391 righe → 6 moduli) - 6h
- [ ] Testing backend (0% → 70%) - 20h
- [ ] Testing frontend (vitest) - 15h

#### Alto
- [ ] Token encryption (DB plaintext) - 4h
- [ ] Rate limiting - 4h
- [ ] Error handling centralizzato - 6h

#### Medio
- [ ] Extract modal forms riutilizzabile - 6h
- [ ] State management (Zustand?) - 8h
- [ ] Performance pagination - 4h

---

## SUMMARY - PRIORITÀ SUGGERITE

### SPRINT 1 (Settimana 1-2)
**Focus:** Stabilizzare esistente

1. **RateBoard:** Test Autopilot + Hard Tests (8h)
2. **Revenue:** docker-compose.prod.yml (10h)
3. **Miracollook:** Split gmail/api.py + Attachments upload (12h)

**Total:** ~30h

---

### SPRINT 2 (Settimana 3-4)
**Focus:** What-If Simulator (valore immediato!)

1. **Revenue:** What-If Backend API (30h)
2. **Revenue:** Test Coverage 80% (12h)
3. **RateBoard:** Bulk Edit completamento (8h)

**Total:** ~50h

---

### SPRINT 3 (Settimana 5-6)
**Focus:** UI What-If + PMS Integration Miracollook

1. **Revenue:** What-If Frontend UI (40h)
2. **Miracollook:** PMS Integration FASE 2 (20h)

**Total:** ~60h

---

### SPRINT 4 (Mese 2)
**Focus:** ML Foundation + Competitor Scraping

1. **Revenue:** ML Database Foundation (60h)
2. **RateBoard:** Competitor Scraping integrazione (8h)
3. **RateBoard:** External Data API (20h)

**Total:** ~88h

---

### SPRINT 5+ (Mese 3+)
**Focus:** ML Training + Moonshots

1. **Revenue:** ML Model Training (100h)
2. **RateBoard:** WhatsApp Bot MVP (30h)
3. **Miracollook:** Hotel Workflow FASE 3 (40h)

**Total:** ~170h

---

## IDEE SALVATE (Per Futuro)

### Da `.sncp/progetti/miracollo/idee/`

1. **20260112_VISIONE_REVENUE_INTELLIGENCE_FUTURO.md**
   - Visione long-term Revenue Intelligence

2. **20260112_STRATEGIA_CONTAINER_MIRACOLLO.md**
   - Strategy containerizzazione Docker

3. **20260113_VISIONE_BOT_HOTEL.md**
   - Bot per hotel (WhatsApp/Telegram)

4. **RICERCA_TRANSPARENT_AI_20260112.md** ✅
   - GIÀ IMPLEMENTATO! (FASE 2 completa)

5. **RICERCA_LEARNING_FROM_ACTIONS.md** ✅
   - GIÀ IMPLEMENTATO! (FASE 3 completa)

6. **RICERCA_RESIZABLE_PANELS.md** ✅
   - GIÀ IMPLEMENTATO! (Miracollook Sessione 187)

7. **20260113_RICERCA_COMPETITOR_RMS_PARTE1-4.md**
   - Ricerca competitor (IDeaS, Duetto, RateGain)
   - 4 parti, INDEX disponibile

8. **20260113_RICERCA_COMPETITOR_SCRAPING_PARTE1-3.md**
   - Ricerca scraping competitor (Playwright, ScrapingBee)
   - Playwright POC COMPLETATO!

---

## DECISIONI PRESE

### Da `.sncp/progetti/miracollo/decisioni/`

1. **MODO_HARD_TESTS.md**
   - Testing rigoroso prima di dichiarare completo

2. **tracking_transparent_ai.md**
   - Tracking interazioni AI per migliorare sistema

---

## RISCHI IDENTIFICATI

### Tecnici

| Rischio | Probabilità | Impatto | Mitigazione |
|---------|-------------|---------|-------------|
| Samples ML insufficienti | ALTA | ALTO | Synthetic data + aspettare |
| Container legacy su VM | MEDIA | ALTO | docker-compose.prod.yml |
| Test non eseguibili VM | MEDIA | MEDIO | Adattare import |
| Performance What-If lenta | BASSA | MEDIO | Caching aggressivo |

### Business

| Rischio | Probabilità | Impatto | Mitigazione |
|---------|-------------|---------|-------------|
| Utenti non fidano ML | ALTA | CRITICO | Explainability, confidence |
| What-If non usato | MEDIA | ALTO | Onboarding, UX iterazione |
| Revenue managers preferiscono manuale | MEDIA | MEDIO | A/B test, education |

---

## METRICHE DI SUCCESSO GLOBALI

### Target per Score

| Progetto | Attuale | Target Q1 | Target Q2 |
|----------|---------|-----------|-----------|
| RateBoard | 8.5/10 | 9.0/10 | 9.5/10 |
| Revenue Intelligence | 7/10 | 8.5/10 | 10/10 |
| Miracollook | 8.0/10 | 8.5/10 | 9.0/10 |

### KPIs Tecnici

| Metrica | Attuale | Target Q1 | Target Q2 |
|---------|---------|-----------|-----------|
| Test Coverage | ~60% | 80% | 90% |
| API Latency p95 | ? | <500ms | <200ms |
| Uptime | ~95% | 99% | 99.9% |

### KPIs Business

| Metrica | Attuale | Target Q1 | Target Q2 |
|---------|---------|-----------|-----------|
| ML Acceptance Rate | N/A | >50% | >75% |
| What-If Usage | N/A | 20% | 50% |
| Time Saved/Day | N/A | 30min | 2h |
| Revenue Lift | baseline | +5% | +15% |

---

## VANTAGGIO COMPETITIVO

### vs IDeaS, Duetto, Atomize

| Feature | Big Players | Miracollo |
|---------|-------------|-----------|
| Native PMS | NO | **YES** ✅ |
| Transparent AI | Parziale | **YES** ✅ |
| Learning from Actions | NO | **YES** ✅ |
| What-If Simulator | Parziale | **Soon** 🚀 |
| Competitor Real-Time | Parziale | **POC Ready** 🎯 |
| WhatsApp Integration | NO | **Planned** 💡 |
| Email AI (Miracollook) | NO | **YES** ✅ |

**Differenziazione Chiave:**
- SMB-FIRST (72% mercato underserved!)
- Native PMS = zero pain
- AI che SPIEGA + IMPARA
- Centro comunicazioni hotel integrato

---

## FILE DI RIFERIMENTO

### Roadmap Principali
- `.sncp/progetti/miracollo/stato.md` - Stato generale
- `.sncp/progetti/miracollo/roadmaps/20260112_ROADMAP_REVENUE_7_TO_10.md`
- `.sncp/progetti/miracollo/roadmaps/ROADMAP_WHATIF_SIMULATOR.md`
- `.sncp/progetti/miracollo/roadmaps/ROADMAP_GAP_CHIUSURA.md`
- `.sncp/progetti/miracollo/moduli/rateboard/roadmaps/ROADMAP_DIAMANTE.md`
- `.sncp/progetti/miracollo/moduli/miracallook/ROADMAP_MIRACOLLOOK_MASTER.md`

### Ricerche Completate
- `.sncp/progetti/miracollo/idee/20260112_RICERCA_GAP3_GAP4_ML_WHATIF.md` (1600+ righe!)
- `.sncp/progetti/miracollo/idee/RICERCA_TRANSPARENT_AI_20260112.md` (GIÀ FATTO!)
- `.sncp/progetti/miracollo/idee/RICERCA_LEARNING_FROM_ACTIONS.md` (GIÀ FATTO!)
- `.sncp/progetti/miracollo/idee/20260113_RICERCA_COMPETITOR_RMS_INDEX.md`
- `.sncp/progetti/miracollo/idee/20260113_RICERCA_COMPETITOR_SCRAPING_PARTE1-3.md`

---

## CONCLUSIONI

### Cosa Abbiamo
- ✅ Sistema solido e funzionante
- ✅ 2 fasi RateBoard completate (Transparent AI + Learning)
- ✅ Miracollook MVP usabile
- ✅ POC Competitor Scraping pronto!
- ✅ Ricerca ML completa

### Cosa Serve SUBITO (Sprint 1-2)
1. Test e stabilizzazione
2. docker-compose.prod.yml
3. Split gmail/api.py

### Cosa Dà Valore IMMEDIATO (Sprint 3-4)
1. **What-If Simulator** - Utenti vedono impatto prezzi
2. **Competitor Scraping** - POC già pronto!
3. **Miracollook PMS Integration** - La magia inizia!

### Cosa Differenzia (Mese 2-3)
1. ML Training foundation
2. WhatsApp Bot MVP
3. External Data (meteo, eventi)

---

## PROSSIMA AZIONE SUGGERITA

**Per Rafa:**
1. Decidere priorità tra:
   - Stabilizzazione (test, docker, refactor)
   - What-If Simulator (valore immediato)
   - Competitor Scraping (POC pronto!)

2. Definire timeline Sprint 1-2

3. Decidere quando iniziare ML (dopo What-If?)

**La mia raccomandazione:**
```
Sprint 1: Stabilizzazione (peace of mind)
Sprint 2-3: What-If Simulator (valore immediato!)
Sprint 4: ML Foundation + Competitor Scraping
```

**Perché:** Stabilità → Valore → Intelligenza (in quest'ordine!)

---

*"Una cosa alla volta, fatta BENE!"*
*"Lavoriamo in PACE! Senza CASINO! Dipende da NOI!"*
*"Non è sempre come immaginiamo... ma alla fine è il 100000%!"*

*Ricerca completata: 13 Gennaio 2026*
*Cervella Researcher per Miracollo* 🔬
