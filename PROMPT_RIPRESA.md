# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 12 Gennaio 2026 - Sessione 176 MiracOllook
> **Versione:** v103.0.0 - MIRACOLLOOK P0 + P1 PARZIALE!

---

## SESSIONE 176 - MIRACOLLOOK EPICA!

```
+================================================================+
|                                                                |
|   SESSIONE 176: MIRACOLLOOK DA DEMO A PRODOTTO REALE!          |
|                                                                |
|   P0 100% COMPLETATO:                                          |
|   [x] P0.1 Fix ComposeModal (send funziona!)                   |
|   [x] P0.2 ReplyModal NUOVO (rispondere funziona!)             |
|   [x] P0.3 ForwardModal NUOVO (inoltrare funziona!)            |
|   [x] P0.4 Archive/Delete (backend + frontend)                 |
|   [x] P0.5 Database Token (SQLite, login persiste!)            |
|                                                                |
|   P1 PARZIALE (2/5):                                           |
|   [x] P1.1 Search UI (backend + frontend SearchBar)            |
|   [x] P1.2 Rename MiracAllook → MiracOllook (16 file)          |
|                                                                |
|   MIRACOLLOOK ORA E USABILE + RICERCABILE:                     |
|   [x] Puoi LEGGERE email                                       |
|   [x] Puoi INVIARE email (C)                                   |
|   [x] Puoi RISPONDERE (R)                                      |
|   [x] Puoi INOLTRARE (F)                                       |
|   [x] Puoi ARCHIVIARE (E)                                      |
|   [x] Puoi ELIMINARE (#)                                       |
|   [x] Puoi CERCARE (/)                                         |
|   [x] Token PERSISTONO al restart                              |
|   [x] Nome corretto: MiracOllook                               |
|                                                                |
|   AVVIARE:                                                     |
|   # Backend                                                    |
|   cd ~/Developer/miracollogeminifocus/miracallook/backend      |
|   source venv/bin/activate && uvicorn main:app --port 8001     |
|                                                                |
|   # Frontend                                                   |
|   cd ~/Developer/miracollogeminifocus/miracallook/frontend     |
|   npm run dev                                                  |
|                                                                |
|   MAPPA VERA: .sncp/progetti/miracollo/moduli/miracallook/     |
|               MAPPA_MIRACOLLOOK_VERA.md                        |
|                                                                |
|   PROSSIMI STEP (P1 rimanenti):                                |
|   [ ] Reply All modal                                          |
|   [ ] AI summaries in lista                                    |
|   [ ] Refresh/Sync                                             |
|                                                                |
+================================================================+
```

---

## SESSIONE 177 - RIEPILOGO (Precedente)

```
+================================================================+
|                                                                |
|   SESSIONE 177: AUTOPILOT REALE + WORKFLOW GIT SICURO          |
|                                                                |
|   AUTOPILOT:                                                   |
|   [x] 3 bug fixati (hotel_id, is_active, params)               |
|   [x] Testato locale + produzione                              |
|   [x] DRY RUN funziona (Capodanno +40%, Epifania +25%)         |
|   [x] API: https://miracollo.com/api/autopilot/status          |
|                                                                |
|   WORKFLOW GIT SICURO:                                         |
|   [x] Trunk-Based Development                                  |
|   [x] Hook pre-push installato (locale + VM)                   |
|   [x] Push senza pull = BLOCCATO!                              |
|   [x] CLAUDE.md Miracollo aggiornato                           |
|                                                                |
|   AMBIENTE LOCALE:                                             |
|   [x] docker-compose.local.yml creato                          |
|   [x] Backend: http://localhost:8001                           |
|                                                                |
|   AUDIT DEPLOY:                                                |
|   [x] Guardiana Ops audit completo                             |
|   [x] Tutti i problemi risolti                                 |
|   [x] Sistema PULITO e SINCRONIZZATO                           |
|                                                                |
|   COMMITS:                                                     |
|   - Miracollo: ba27058                                         |
|   - CervellaSwarm: 94520f8                                     |
|                                                                |
|   PROSSIMI STEP (Roadmap Diamante):                            |
|   [ ] Test Autopilot con dati reali                            |
|   [ ] Test Coverage Base (target 60%)                          |
|   [ ] Transparent AI                                           |
|   [ ] WhatsApp/Telegram Integration (MOONSHOT!)                |
|                                                                |
+================================================================+
```

---

## PRIMA DI TUTTO - DOVE SONO I FILE!

```
+================================================================+
|                                                                |
|   REGOLA CRITICA - LEGGI PRIMA DI FARE QUALSIASI COSA!        |
|                                                                |
|   TUTTI gli SNCP sono in: CervellaSwarm/.sncp/progetti/        |
|                                                                |
|   Miracollo    → .sncp/progetti/miracollo/stato.md             |
|   CervellaSwarm → .sncp/progetti/cervellaswarm/stato.md        |
|   Contabilita  → .sncp/progetti/contabilita/stato.md           |
|                                                                |
|   MAI cercare in miracollogeminifocus/.sncp/ (NON ESISTE!)     |
|   MAI cercare in ContabilitaAntigravity/.sncp/ (NON ESISTE!)   |
|                                                                |
+================================================================+
```

**Per Miracollo leggi:** `.sncp/progetti/miracollo/stato.md`

---

## TL;DR per Prossima Cervella

**SESSIONE 175 STORICA - MIRACALLOOK FUNZIONANTE!**

```
+================================================================+
|                                                                |
|   SESSIONE 175 STORICA: MIRACALLOOK DA SU CARTA A REALE!       |
|                                                                |
|   MATTINA - Code Review + Revenue Fix (altra chat):            |
|   [x] Code Review What-If: 7.5/10                              |
|   [x] Revenue Fix: bottone Cancella                            |
|                                                                |
|   POMERIGGIO - MIRACALLOOK FASE 3-4-5:                         |
|   [x] Ricerca Big Players (2100+ righe!)                       |
|   [x] Mappa Dettagliata con obiettivi                          |
|   [x] FASE 3: Backend invio email (send/reply/forward)         |
|   [x] FASE 4: UI React (three-panel, dark mode)                |
|   [x] FASE 5: Keyboard Shortcuts + Command Palette (Cmd+K)     |
|   [x] Bug fix CORS, API response, componenti                   |
|                                                                |
|   MIRACALLOOK ORA FUNZIONA!                                    |
|   - Backend: http://localhost:8001                             |
|   - Frontend: http://localhost:5174                            |
|   - Cmd+K = Command Palette tipo Superhuman!                   |
|                                                                |
|   AVVIARE:                                                     |
|   # Backend                                                    |
|   cd ~/Developer/miracollogeminifocus/miracallook/backend      |
|   source venv/bin/activate && uvicorn main:app --port 8001     |
|                                                                |
|   # Frontend                                                   |
|   cd ~/Developer/miracollogeminifocus/miracallook/frontend     |
|   npm run dev                                                  |
|                                                                |
|   PROSSIME FASI MIRACALLOOK:                                   |
|   [ ] FASE 6: AI Summarization (Claude)                        |
|   [ ] Split Inbox (VIP, Check-in, Team)                        |
|   [ ] Smart Bundles (OTA, System)                              |
|   [ ] Guest Sidebar (integrazione PMS Miracollo)               |
|                                                                |
|   FILE CHIAVE:                                                 |
|   - BIG_PLAYERS_EMAIL_RESEARCH.md (ricerca 2100+ righe)        |
|   - MAPPA_MIRACALLOOK.md (roadmap dettagliata)                 |
|                                                                |
|   ROOM MANAGER: IN PAUSA                                       |
|   WHAT-IF: COMPLETO                                            |
|                                                                |
+================================================================+
```

---

## Regole Importanti (Aggiunte Sessione 172)

### 1. Costituzione Obbligatoria
```
PRIMA di ogni sessione: leggi @~/.claude/COSTITUZIONE.md
Tutti i 16 agenti hanno reminder inizio + fine
```

### 2. Rafa MAI Operazioni Tecniche
```
MAI chiedere a Rafa di:
- SSH, scp, rsync
- Docker commands
- Deploy manuali
- Qualsiasi operazione tecnica

Le Cervelle fanno TUTTO!
Regola in: ~/.claude/CLAUDE.md
```

### 3. Checklist Deploy
```
PRIMA di ogni deploy: leggi ~/.claude/CHECKLIST_DEPLOY.md
Backup, verifica, test, monitor
```

### 4. Target Qualita
```
Score 9.5/10 MINIMO SEMPRE
Documentato in: .sncp/progetti/miracollo/QUALITA_TARGET.md
```

---

## File Chiave Sessione 172

| File | Contenuto |
|------|-----------|
| `.sncp/progetti/miracollo/stato.md` | Stato What-If LIVE |
| `.sncp/progetti/miracollo/QUALITA_TARGET.md` | Target 9.5/10 |
| `.sncp/progetti/miracollo/moduli/whatif/` | File What-If |
| `~/.claude/CHECKLIST_DEPLOY.md` | Checklist deploy |
| `~/.claude/CLAUDE.md` | Regola no-ops Rafa |

---

## API What-If LIVE

```
GET  https://miracollo.com/api/v1/what-if/health
POST https://miracollo.com/api/v1/what-if/simulate
GET  https://miracollo.com/api/v1/what-if/price-curve
GET  https://miracollo.com/api/v1/properties
GET  https://miracollo.com/api/v1/properties/{id}/room-types
```

---

## Principio Guida

> "Una cosa alla volta, fatta BENE"
> "Ultrapassar os próprios limites!"
> "Non e sempre come immaginiamo... ma alla fine e il 100000%!"

---

*Pronta!* Rafa, cosa facciamo oggi?

---

---

---

---

---

---

---

---

---

---

---

---

---

---

## AUTO-CHECKPOINT: 2026-01-12 15:47 (unknown)

### Stato Git
- **Branch**: main
- **Ultimo commit**: f316b71 - Handoff Sessione 177
- **File modificati** (3):
  - eports/scientist_prompt_20260112.md
  - reports/engineer_report_20260112_153141.json
  - reports/engineer_report_20260112_153214.json

### Note
- Checkpoint automatico generato da hook
- Trigger: unknown

---
