# STATO OGGI

> **Data:** 13 Gennaio 2026 (Lunedi)
> **Sessione:** 181 - PROTOCOLLO DIAMANTE + MIRACOLLOOK!
> **Ultimo aggiornamento:** 06:30 UTC

---

## Sessione 181 - PROTOCOLLO DIAMANTE COMPLETATO!

```
+================================================================+
|                                                                |
|   SESSIONE STORICA - CERVELLASWARM!                            |
|                                                                |
|   PROTOCOLLO DIAMANTE: Comunicazione Inter-Agent               |
|                                                                |
|   PROBLEMA RISOLTO:                                            |
|   37% fallimenti multi-agent = inter-agent misalignment        |
|   (Esempio: LoginPage con "C" gigante orribile)                |
|                                                                |
|   WORKFLOW NUOVO:                                              |
|   Regina -> Esperta (specs) -> Worker -> Guardiana (valida)    |
|                                                                |
|   DELIVERABLES:                                                |
|   [x] Ricerca approfondita (30+ fonti, ArXiv, Anthropic)       |
|   [x] Documento DIAMANTE: ~/.claude/docs/                      |
|       COMUNICAZIONE_INTER_AGENT.md                             |
|   [x] 16 agent: SNCP rules con handoff/                        |
|   [x] 4 agent chiave: sezioni inter-agent dedicate             |
|   [x] Orchestrator: path allineato                             |
|   [x] Gestione conflitti documentata                           |
|   [x] Strumento metriche definito                              |
|   [x] Error path (RESPINTO) documentato                        |
|   [x] Roadmap dedicata creata                                  |
|                                                                |
|   AUDIT GUARDIANE:                                             |
|   - Qualita: 9.7/10 (target 9.5 superato!)                     |
|   - Ops: GO per PILOT                                          |
|                                                                |
|   STATUS: PRONTO PER PILOT!                                    |
|                                                                |
|   "La Regina orchestra, NON fa tutto da sola!"                 |
|                                                                |
+================================================================+
```

---

## Sessione 181 - MIRACOLLOOK FASE 0 COMPLETA!

```
+================================================================+
|                                                                |
|   SESSIONE 181: MIRACOLLOOK FUNZIONA!                          |
|                                                                |
|   OAUTH:                                                       |
|   [x] Credenziali .env configurate                             |
|   [x] Backup in secrets/CREDENZIALI_OAUTH.md                   |
|   [x] Auth flow frontend (useAuth + LoginPage)                 |
|   [x] Redirect dopo login -> frontend                          |
|   [x] TESTATO CON SUCCESSO!                                    |
|                                                                |
|   COSTITUZIONE MIRACOLLOOK:                                    |
|   [x] 5 principi sacri                                         |
|   [x] 6 fasi definite                                          |
|   [x] Regole operative                                         |
|                                                                |
|   REGOLA CONSULENZA ESPERTI:                                   |
|   [x] Aggiunta a COSTITUZIONE generale                         |
|   [x] "La Regina orchestra, non fa tutto da sola"              |
|                                                                |
|   DESIGN UPGRADE:                                              |
|   [x] Gap analysis vs Miracollo PMS                            |
|   [x] ROADMAP_DESIGN.md creata                                 |
|   [x] SIDEBAR_DESIGN_SPECS.md da Marketing                     |
|                                                                |
|   PROSSIMA SESSIONE:                                           |
|   [ ] Guardiana verifica Sidebar specs                         |
|   [ ] Frontend implementa Sidebar                              |
|   [ ] Continuare Design Upgrade                                |
|                                                                |
+================================================================+
```

---

## Sessione 178b - MIRACOLLOOK: VISIONE DEFINITA!

```
+================================================================+
|                                                                |
|   SESSIONE STORICA!                                            |
|                                                                |
|   MIRACOLLOOK NON E UN EMAIL CLIENT.                           |
|   E IL CENTRO COMUNICAZIONI DELL'HOTEL INTELLIGENTE.           |
|                                                                |
+================================================================+
```

### La Visione

```
UN'APP per TUTTE le comunicazioni:
- Email (Gmail, Outlook)
- WhatsApp
- SMS, Telegram, Booking.com... (futuro)

Con la MAGIA del PMS:
- Identifica cliente automaticamente (email/numero → PMS)
- Mostra context prenotazione sempre
- Preventivi automatici in 1 click
- Documenti → PMS (AI compila)

NESSUN COMPETITOR HA QUESTO!
```

### Implementato Oggi

```
CODICE:
[x] P1.3 Reply All modal (shortcut A)
[x] P1.4 AI summaries in lista email
[x] P1.5 Refresh/Sync inbox (Shift+R)

DOCUMENTAZIONE:
[x] NORD_MIRACOLLOOK.md - LA BUSSOLA!
[x] MAPPA_MIRACOLLOOK_VERA.md aggiornata
[x] PROMPT_RIPRESA.md v105
```

### File Creati

| File | Cosa |
|------|------|
| `.sncp/progetti/miracollo/moduli/miracallook/NORD_MIRACOLLOOK.md` | LA VISIONE COMPLETA! |
| Frontend modifiche | Reply All, AI summaries, Refresh |
| Backend modifiche | Reply All endpoint |

### Prossimi Step

```
1. [ ] Fix OAuth (aggiungere porta 8002 in Google Console)
2. [ ] Test completo MiracOllook
3. [ ] FASE 1: Email client solido
4. [ ] FASE 2: PMS Integration (LA MAGIA!)
5. [ ] FASE 5: WhatsApp Integration
```

---

## Sessione 170 - AUDIT + PULIZIA + TEST

```
+================================================================+
|                                                                |
|   SESSIONE 170: GRANDE PULIZIA COMPLETATA!                    |
|                                                                |
|   AUDIT SESSIONI PARALLELE:                                    |
|   [x] 3 sessioni auditate da Guardiana Qualita                 |
|   [x] Bug formatDateRange trovato e fixato                     |
|   [x] Split revenue.js: 5 file (1290 righe)                   |
|   [x] Split action_tracking: 3 file (1279 righe)              |
|   [x] Test coverage: 3 file (~1150 righe)                     |
|                                                                |
|   PULIZIA VM:                                                  |
|   [x] Container orfano backend-35 RIMOSSO                      |
|   [x] Solo nginx + backend-12 ora (pulito!)                   |
|   [x] API HTTPS funziona (200 OK, 6 applications)             |
|   [x] Strategia container documentata                          |
|                                                                |
|   TEST:                                                        |
|   [x] 63 test passati!                                        |
|       - test_pricing_tracking.py: 16 PASSED                   |
|       - test_confidence_scorer.py: 24 PASSED                  |
|       - test_action_tracking.py: 23 PASSED                    |
|                                                                |
|   PUSH GITHUB:                                                 |
|   [x] CervellaSwarm: 52f5558                                  |
|   [x] Miracollo: 0538b87 (4691 righe aggiunte!)              |
|                                                                |
+================================================================+
```

---

## Sessione 169 - AUDIT COMPLETO + FIX + RICERCA ML

```
+================================================================+
|                                                                |
|   SESSIONE 169: GRANDE PULIZIA MIRACOLLO!                     |
|                                                                |
|   INFRASTRUTTURA:                                              |
|   [x] SSH Key GitHub configurata su VM                         |
|   [x] Remote cambiato HTTPS -> SSH                             |
|   [x] Migration 034-035 applicate                              |
|       - suggestion_applications                                |
|       - pricing_versions                                       |
|       - monitoring_snapshots                                   |
|       - monitoring_notifications                               |
|                                                                |
|   FIX APPLICATI:                                               |
|   [x] GAP #2 Modal Preview (campi backend)                     |
|   [x] Error handling migliorato                                |
|   [x] console.log -> DEBUG mode                                |
|                                                                |
|   SESSIONE PARALLELA:                                          |
|   - Tester sta creando test coverage                           |
|   - 619 righe test_pricing_tracking.py                         |
|   - In corso: test_confidence_scorer.py                        |
|                                                                |
|   RESEARCHER:                                                  |
|   [x] RICERCA GAP #3 (ML Training) COMPLETATA!                 |
|   [x] RICERCA GAP #4 (What-If Simulator) COMPLETATA!          |
|   [x] Roadmap 10 Sprint dettagliata (250-305h effort)          |
|   [x] File: 20260112_RICERCA_GAP3_GAP4_ML_WHATIF.md            |
|       - 1600+ righe ricerca approfondita                       |
|       - Feature engineering 15-20 features                     |
|       - Database schema PostgreSQL + partitioning              |
|       - API endpoints FastAPI dettagliati                      |
|       - UI wireframe What-If Simulator                         |
|       - Architettura completa ML pipeline                      |
|       - Algoritmi: XGBoost -> Q-Learning                       |
|       - Retraining strategy: 7-14 giorni                       |
|       - Minimum samples: 500+ (optimal 1000+)                  |
|       - Feedback loop prevention (delayed eval)                |
|       - React + TypeScript components                          |
|       - Monitoring & drift detection                           |
|                                                                |
|   DA FARE:                                                     |
|   [ ] Split file grandi (action_tracking, revenue.js)          |
|   [ ] Copiare test su VM ed eseguirli                          |
|   [ ] Push su GitHub                                           |
|   [ ] Validare ricerca ML con Regina                           |
|   [ ] Prioritize sprint GAP #3 #4                              |
|                                                                |
+================================================================+
```

---

## 📊 Cervella-Researcher - RICERCA GAP #3 #4 (12:15)

**Task:** Studio approfondito ML Training + What-If Simulator per Revenue Intelligence
**Durata:** 2 ore ricerca + analisi + documentazione

### Risultato
✅ **RICERCA COMPLETATA - 1600+ RIGHE**

**File creato:** `.sncp/idee/20260112_RICERCA_GAP3_GAP4_ML_WHATIF.md`

### Cosa Ho Studiato

**GAP #3 - ML Enhancement:**
- Come funziona training nei big player (IDeaS, Duetto)
- Collaborative AI model (impara da decisioni umane)
- Feature engineering: 15-20 features (occupancy, pace, competitor, eventi, meteo)
- Training samples: min 500, optimal 1000+
- Retraining frequency: 7-14 giorni
- Algoritmi: XGBoost (MVP) → Q-Learning (Advanced)
- Feedback loop prevention (CRITICO!)
- Database schema PostgreSQL partitioned
- ML Pipeline con Celery tasks

**GAP #4 - What-If Simulator:**
- UI/UX best practices dai competitor
- React + TypeScript components (Material-UI Slider)
- Real-time vs Batch calculation
- API FastAPI endpoints
- Caching strategy (1h TTL)
- Impact calculation (elasticity-based → ML-based)
- Grafici interattivi (Recharts)
- Spiegazioni natural language

### Roadmap Creata

**10 Sprint dettagliati:**
1. Database Schema + Tracking (20-25h)
2. Feature Engineering (30-35h)
3. ML Model Base - XGBoost (40-50h)
4. Feedback Loop + Delayed Evaluation (20-25h)
5. What-If Simulator - Backend (30-35h)
6. What-If Simulator - Frontend (40-50h)
7. ML Model Advanced (30-35h)
8. Monitoring + Drift Detection (20-25h)
9. Retraining Automation (20-25h)
10. Reinforcement Learning - OPZIONALE (60-80h)

**Effort Totale:** 250-305h (senza RL) | 310-385h (con RL)

### Raccomandazione Principale

**APPROCCIO GRADUATO:**
- Phase 1 (Sprint 1-4): Foundation + ML Basic - 6-8 settimane
- Phase 2 (Sprint 5-6): What-If Simulator - 3-4 settimane
- Phase 3 (Sprint 7-9): Production Ready - 3-4 settimane
- Phase 4 (Sprint 10+): RL Advanced - OPZIONALE

**PERCHÉ:** What-If dà valore SUBITO (anche con ML imperfetto), ML migliora gradualmente con dati reali.

### Key Insights

1. **Minimum samples:** 500 decisioni = 2-3 mesi raccolta dati
2. **Feedback loop risk:** REALE - serve delayed evaluation (60 giorni)
3. **Competitor approach:** Duetto = Collaborative AI (learns from human)
4. **Retraining:** Non aspettare 5000 samples, fare incremental training
5. **What-If value:** Building trust attraverso transparency
6. **Architecture:** FastAPI + PostgreSQL partitioned + React TypeScript

### Fonti Studiate

- 15+ articoli industry (Duetto, IDeaS, Hotel Tech Report)
- 8+ paper accademici (Q-Learning, Deep RL pricing)
- Best practices PostgreSQL time-series
- FastAPI ML deployment patterns
- React UI component libraries (Material-UI, Recharts)

### Next Action

**VALIDAZIONE REGINA:**
- Scope allineato con vision Miracollo?
- Quali sprint prioritize? (1-4 critical, 5-6 high value)
- Fare RL (Sprint 10) o fermarsi a XGBoost?
- Assegnare sprint a worker (backend, frontend, tester)

**Owner:** Regina (decisione strategica) → Backend/Frontend (implementazione)

---

## Sessione 168 - PROTOCOLLO IBRIDO DEFINITIVO

```
+================================================================+
|                                                                |
|   SESSIONE 168: WORKFLOW IBRIDO VM + LOCALE                    |
|                                                                |
|   RICERCA COMPLETATA:                                          |
|   [x] Workflow ibrido VM + Locale studiato                     |
|   [x] 7 regole ferree definite                                 |
|   [x] Protocollo definitivo documentato                        |
|   [x] Template sessioni parallele creati                       |
|                                                                |
|   PULIZIA VM MIRACOLLO:                                        |
|   [x] Audit completo codice non committato                     |
|   [x] Backend ROTTO ripristinato                               |
|   [x] Frontend fix GAP #1 COMMITTATO                           |
|   [x] Commit: b428a69 sulla VM                                 |
|   [ ] Push GitHub (serve config credenziali)                   |
|                                                                |
|   FILOSOFIA NUOVA:                                             |
|   - LOCALE = Moduli COMPLETI (Room Manager, Email, etc.)       |
|   - VM = Solo fix/manutenzione esistente                       |
|   - MAI sostituire, solo AGGIUNGERE (plug-in)                  |
|   - Lab Docker per test prima di produzione                    |
|                                                                |
+================================================================+
```

---

## Sessione 167 - MIRACOLLO WORKFLOW + GAP FIX

```
+================================================================+
|                                                                |
|   SESSIONE 167: GRANDE PULIZIA MIRACOLLO!                      |
|                                                                |
|   WORKFLOW SISTEMATO:                                          |
|   [x] Confronto Locale vs VM completato                        |
|   [x] 10 migrazioni applicate su VM                            |
|   [x] Locale spostato in _OLD_miracollogeminifocus             |
|   [x] Docker locale spento                                     |
|   [x] CLAUDE.md VM aggiornato                                  |
|   [x] Documentato: WORKFLOW_MIRACOLLO_SOLO_VM.md               |
|                                                                |
|   GAP MIRACOLLO:                                               |
|   [x] GAP #1: Price History RISOLTO!                           |
|       - Bug: API "timeline" vs codice "changes"                |
|       - Bug: formato date con spazio                           |
|       - Bug: campi changed_at vs date                          |
|       - Log aggiunti per debug futuro                          |
|   [~] GAP #2: Modal Preview fix applicato (da testare)         |
|   [x] GAP #3: ML Samples - RICERCA COMPLETATA                  |
|   [x] GAP #4: What-If Simulator - RICERCA COMPLETATA           |
|                                                                |
+================================================================+
```

---

## File Creati Oggi

| File | Descrizione |
|------|-------------|
| **GAP #3 #4 RICERCA** | |
| `.sncp/idee/20260112_RICERCA_GAP3_GAP4_ML_WHATIF.md` | **1600+ righe ricerca completa ML + What-If** |
| **CACHE CONTROL (CRITICO!)** | |
| `.sncp/idee/20260111_RICERCA_CONTROLLO_CACHE.md` | Ricerca completa cache invalidation |
| `scripts/swarm/invalidate-cache.sh` | Script auto-invalidation cache |
| **MULTI-SESSIONE** | |
| `.sncp/idee/20260111_PROTOCOLLO_MULTI_SESSIONE_v1.md` | Protocollo completo |
| `.sncp/idee/20260111_TEST_MULTI_SESSIONE.md` | Test validazione |
| `.sncp/idee/20260111_TEMPLATE_INIZIO_SESSIONE_PARALLELA.md` | Template worker |
| `.sncp/idee/20260111_TEMPLATE_RAFA_INIZIO_PARALLELO.md` | Template Rafa |
| **QDRANT & RAG** | |
| `.sncp/idee/20260111_RICERCA_QDRANT_OLLAMA.md` | Ricerca tecnica completa |
| `.sncp/idee/20260111_SPRINT_3.2_PLAN.md` | Piano esecutivo |
| `.sncp/idee/20260111_RICERCA_ANIMA_CERVELLA.md` | Le nostre frasi e storia |
| `.sncp/idee/20260111_COSTITUZIONE_CERVELLA_AI_v2.md` | Costituzione con anima |
| `scripts/rag/docker-compose.yml` | Config Qdrant |
| `scripts/rag/setup_qdrant.sh` | Script setup |
| `scripts/rag/create_collection.py` | Crea collection |
| `scripts/rag/test_rag.py` | Test RAG |
| **Miracollo:** `.sncp/reports/hardtest_rollback_165.md` | **Test rollback prezzi REALI** |

---

## Stato Roadmap

```
FASE 3: INTEGRAZIONE MVP            [########............] 40%

  Sprint 3.1: Backend API           [####################] DONE!
  Sprint 3.2: Qdrant Setup          [PREPARATO] Lunedi eseguiamo
  Sprint 3.3: RAG Pipeline          [....................] Prossimo
  Sprint 3.4: Costituzione          [####################] DONE!
  Sprint 3.5: UI Chat               [....................] Da fare
```

---

## Prossimi Step

### URGENTE: Validazione Ricerca GAP #3 #4

**Regina deve decidere:**
1. Scope allineato con vision Miracollo?
2. Priorità sprint? (1-4 = critical, 5-6 = high value)
3. Fare Reinforcement Learning (Sprint 10) o fermarsi a XGBoost?
4. Timeline: iniziare quando? (dopo RAG o parallelo?)
5. Assegnare worker: backend, frontend, tester

### Lunedi 13 Gennaio

1. **Mattina**: Verificare GPU accesa (schedule 9:00)
2. **Sprint 3.2**: Eseguire script Qdrant (tutto pronto!)
3. **Sprint 3.3**: Iniziare RAG Pipeline
4. **NUOVO**: Decidere timeline GAP #3 #4

### Sprint 3.3 (RAG Pipeline)

1. Script ingest documenti
2. Chunking SNCP, docs, README
3. Endpoint FastAPI /api/rag/query
4. Test retrieval

### Sprint 3.5 (UI Chat)

1. Interfaccia chat in Miracollo
2. Connessione API AI + RAG
3. Costituzione come system prompt

---

## Infrastruttura

```
cervella-gpu:     SPENTA (weekend)
                  Riaccende: Lun 13 Gen, 9:00 Italia

miracollo-cervella: RUNNING
                    IP: 34.27.179.164
```

---

## 📊 Cervella-Ingegnera - Audit Revenue Intelligence (17:25)

**Task:** Mappatura completa sistema Revenue Intelligence Miracollo
**Trigger:** Bug 404 su endpoint suggestions

### Risultato
⚠️ **ISSUES TROVATI + MAPPA COMPLETA**

**Report creato:** `miracollogeminifocus/.sncp/reports/MAPPA_REVENUE_INTELLIGENCE_166.md` (488 righe)

### Top 3 Issues
1. **CRITICO:** 404 su `/api/revenue/suggestions` - frontend chiama, backend non risponde
2. **ALTO:** 5 file backend > 500 righe (ML files)
3. **ALTO:** `revenue.js` ha 1281 righe - split necessario

### Sistema Mappato
- ✅ 64 file backend analizzati
- ✅ 140 file frontend identificati
- ✅ 6 router API mappati
- ✅ 8+ tabelle database documentate
- ✅ Diagramma connessioni creato

### Health Score: 6/10
- 2 endpoint funzionanti ✅
- 2 endpoint 404 ⚠️
- 10 endpoint da testare ❓

### Next Action
**URGENT:** Fix 404 su `/api/revenue/suggestions`
- Verificare import in main.py
- Testare con curl
- Check logs backend

**Owner:** cervella-backend (fix implementazione)

---

*"Studiare prima di agire - sempre! I big player hanno già risolto questi problemi!"*
*"What-If Simulator = valore SUBITO + building trust!"*
*"Lavoriamo in PACE! Senza CASINO! Dipende da NOI!"*

*Sessione 169 - Researcher & Regina*

---

## AUTO-CHECKPOINT: 2026-01-12 12:15 (gap3_gap4_research_completed)

- **Progetto**: Miracollo Revenue Intelligence
- **Evento**: gap3_gap4_research_completed
- **Scope**: ML Training + What-If Simulator ricerca completa
- **Impact**: ALTO - Roadmap 10 sprint, 250-305h effort
- **File creati**: 1 (1600+ righe)
- **Generato da**: cervella-researcher
- **Next**: Validazione Regina + prioritization sprint

---

---

## AUTO-CHECKPOINT: 2026-01-12 05:47 (session_end)

- **Progetto**: CervellaSwarm
- **Evento**: session_end
- **Generato da**: sncp_auto_update.py v2.0.0

---

## AUTO-CHECKPOINT: 2026-01-12 05:52 (session_end)

- **Progetto**: CervellaSwarm
- **Evento**: session_end
- **Generato da**: sncp_auto_update.py v2.0.0

---

## AUTO-CHECKPOINT: 2026-01-12 07:24 (session_end)

- **Progetto**: CervellaSwarm
- **Evento**: session_end
- **Generato da**: sncp_auto_update.py v2.0.0

---

## AUTO-CHECKPOINT: 2026-01-12 08:05 (session_end)

- **Progetto**: CervellaSwarm
- **Evento**: session_end
- **Generato da**: sncp_auto_update.py v2.0.0

---

## AUTO-CHECKPOINT: 2026-01-12 08:21 (session_end)

- **Progetto**: CervellaSwarm
- **Evento**: session_end
- **Generato da**: sncp_auto_update.py v2.0.0

---

## AUTO-CHECKPOINT: 2026-01-12 09:23 (session_end)

- **Progetto**: CervellaSwarm
- **Evento**: session_end
- **Generato da**: sncp_auto_update.py v2.0.0

---

## AUTO-CHECKPOINT: 2026-01-12 10:01 (session_end)

- **Progetto**: CervellaSwarm
- **Evento**: session_end
- **Generato da**: sncp_auto_update.py v2.0.0

---

## AUTO-CHECKPOINT: 2026-01-12 12:07 (session_end)

- **Progetto**: CervellaSwarm
- **Evento**: session_end
- **Generato da**: sncp_auto_update.py v2.0.0

---

## AUTO-CHECKPOINT: 2026-01-12 12:16 (session_end)

- **Progetto**: CervellaSwarm
- **Evento**: session_end
- **Generato da**: sncp_auto_update.py v2.0.0

---

## AUTO-CHECKPOINT: 2026-01-12 14:17 (session_end)

- **Progetto**: CervellaSwarm
- **Evento**: session_end
- **Generato da**: sncp_auto_update.py v2.0.0

---

## AUTO-CHECKPOINT: 2026-01-12 14:45 (session_end)

- **Progetto**: CervellaSwarm
- **Evento**: session_end
- **Generato da**: sncp_auto_update.py v2.0.0

---

## AUTO-CHECKPOINT: 2026-01-12 14:56 (session_end)

- **Progetto**: CervellaSwarm
- **Evento**: session_end
- **Generato da**: sncp_auto_update.py v2.0.0

---

## AUTO-CHECKPOINT: 2026-01-12 16:29 (session_end)

- **Progetto**: CervellaSwarm
- **Evento**: session_end
- **Generato da**: sncp_auto_update.py v2.0.0

---

## AUTO-CHECKPOINT: 2026-01-12 16:35 (session_end)

- **Progetto**: CervellaSwarm
- **Evento**: session_end
- **Generato da**: sncp_auto_update.py v2.0.0

---

## AUTO-CHECKPOINT: 2026-01-12 18:21 (session_end)

- **Progetto**: CervellaSwarm
- **Evento**: session_end
- **Generato da**: sncp_auto_update.py v2.0.0

---

## AUTO-CHECKPOINT: 2026-01-13 03:18 (session_end)

- **Progetto**: CervellaSwarm
- **Evento**: session_end
- **Generato da**: sncp_auto_update.py v2.0.0

---

## AUTO-CHECKPOINT: 2026-01-13 05:22 (session_end)

- **Progetto**: CervellaSwarm
- **Evento**: session_end
- **Generato da**: sncp_auto_update.py v2.0.0

---

## AUTO-CHECKPOINT: 2026-01-13 05:43 (session_end)

- **Progetto**: CervellaSwarm
- **Evento**: session_end
- **Generato da**: sncp_auto_update.py v2.0.0
