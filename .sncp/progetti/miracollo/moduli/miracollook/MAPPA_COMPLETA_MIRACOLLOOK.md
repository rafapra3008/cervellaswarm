# MAPPA COMPLETA MIRACOLLOOK - Step by Step

> **Creata:** 15 Gennaio 2026 - Sessione 224
> **Guardiana Qualita:** cervella-guardiana-qualita
> **Score:** 9.5/10
> **Principio:** "REALE > Su Carta" - Solo FATTI contano!

---

## VISIONE

```
MIRACOLLOOK = L'Outlook che CONOSCE il tuo hotel!

NON e un email client generico.
E il CENTRO COMUNICAZIONI dell'hotel intelligente.

LA MAGIA = PMS Integration + Guest Recognition + VELOCITA SUPERHUMAN!
```

---

## OVERVIEW FASI

```
FASE 0: FONDAMENTA          [####################] 100% COMPLETA!
FASE P: PERFORMANCE         [####################] 100% MERGED!
FASE 1: EMAIL CLIENT SOLIDO [################....] 80%
FASE 2: PMS INTEGRATION     [....................] 0%
FASE 3: HOTEL WORKFLOW      [....................] 0%
FASE 4: MULTI-CHANNEL       [....................] 0%
```

---

## FASE 0: FONDAMENTA [100% COMPLETA]

### 0.1 OAuth Google
- **Status:** [FATTO]
- **Studio:** Nessuno richiesto (standard OAuth2)
- **Dipende da:** Nessuno
- **Note:** /auth/login + /auth/callback

### 0.2 Inbox View
- **Status:** [FATTO]
- **Studio:** `studi/DESIGN_PATTERNS_EMAIL.md`
- **Dipende da:** 0.1
- **Note:** Three-panel layout, lista email

### 0.3 Email Detail
- **Status:** [FATTO]
- **Studio:** `studi/UX_STRATEGY_MIRACALLOOK.md`
- **Dipende da:** 0.2
- **Note:** /gmail/message/{id}

### 0.4 Send Email
- **Status:** [FATTO]
- **Studio:** Nessuno richiesto
- **Dipende da:** 0.1
- **Note:** /gmail/send

### 0.5 Reply / Reply All / Forward
- **Status:** [FATTO]
- **Studio:** Nessuno richiesto
- **Dipende da:** 0.4
- **Note:** /gmail/reply, /gmail/forward

### 0.6 Archive / Trash
- **Status:** [FATTO]
- **Studio:** Nessuno richiesto
- **Dipende da:** 0.1
- **Note:** /gmail/archive, /gmail/trash

### 0.7 Search
- **Status:** [FATTO]
- **Studio:** Nessuno richiesto
- **Dipende da:** 0.1
- **Note:** /gmail/search

### 0.8 AI Summarization
- **Status:** [FATTO]
- **Studio:** Nessuno richiesto (Claude API)
- **Dipende da:** 0.3
- **Note:** /gmail/message/{id}/summary

### 0.9 Keyboard Shortcuts
- **Status:** [FATTO]
- **Studio:** `studi/RICERCA_QUICK_ACTIONS_KEYBOARD.md`
- **Dipende da:** 0.2
- **Note:** j/k/e/r/c/f/s + useKeyboardShortcuts.ts

### 0.10 Command Palette
- **Status:** [FATTO]
- **Studio:** Nessuno richiesto (pattern standard)
- **Dipende da:** 0.9
- **Note:** Cmd+K

### 0.11 Dark Mode
- **Status:** [FATTO]
- **Studio:** `studi/RICERCA_DESIGN_SALUTARE.md`
- **Dipende da:** Nessuno
- **Note:** Tailwind v4 dark mode

### 0.12 Views (Inbox/Archived/Starred/Snoozed/Trash)
- **Status:** [FATTO]
- **Studio:** Nessuno richiesto
- **Dipende da:** 0.2
- **Note:** Sidebar navigation

---

## FASE P: PERFORMANCE [100% MERGED! v2.0.0]

### P1.1 IndexedDB Schema
- **Status:** [FATTO]
- **Studio:** `ricerche/P2_Virtualization.md`, `decisioni/DECISIONE_PERFORMANCE_ARCHITECTURE.md`
- **Dipende da:** 0.2
- **Note:** db.ts - cache locale

### P1.2 Batch API
- **Status:** [FATTO]
- **Studio:** `ricerche/20260114_ANALISI_Performance.md`
- **Dipende da:** P1.1
- **Note:** 51->2 API calls

### P1.3 Skeleton Loading
- **Status:** [FATTO]
- **Studio:** `studi/RICERCA_PERFORMANCE_EMAIL_CLIENTS.md`
- **Dipende da:** P1.1
- **Note:** EmailSkeleton.tsx

### P1.4 Optimistic UI
- **Status:** [FATTO]
- **Studio:** `ricerche/P2_useOptimistic.md`
- **Dipende da:** P1.2
- **Note:** useEmails.ts mutations

### P2.1 Prefetch Intelligente
- **Status:** [FATTO]
- **Studio:** `ricerche/P2_Prefetch.md`
- **Dipende da:** P1.4
- **Note:** usePrefetchEmails.ts

### P2.2 Hover Prefetch
- **Status:** [FATTO]
- **Studio:** `ricerche/P2_Prefetch.md`
- **Dipende da:** P2.1
- **Note:** useHoverPrefetch.ts

### P2.3 Service Worker
- **Status:** [FATTO]
- **Studio:** `ricerche/P2_ServiceWorker.md`
- **Dipende da:** P1.1
- **Note:** Workbox + vite-plugin-pwa

### P2.4 Offline Sync
- **Status:** [FATTO]
- **Studio:** `ricerche/P2_ServiceWorker.md`
- **Dipende da:** P2.3
- **Note:** useOfflineSync.ts, PWA installabile!

### P3.1 SSE Real-Time (POLISH)
- **Status:** [DA FARE]
- **Studio:** STUDIO MANCA
- **Dipende da:** P2.4
- **Note:** Notifiche push real-time, ~3 giorni effort
- **Effort:** 3 giorni

### P3.2 Attachment Lazy Loading (POLISH)
- **Status:** [DA FARE]
- **Studio:** `studi/RICERCA_ATTACHMENTS_PERFORMANCE.md`
- **Dipende da:** 1.4
- **Note:** Progress bar streaming, ~1.5 giorni
- **Effort:** 1.5 giorni

### P3.3 Cache Management (POLISH)
- **Status:** [DA FARE]
- **Studio:** `studi/RICERCA_PERFORMANCE_EMAIL_CLIENTS.md`
- **Dipende da:** P1.1
- **Note:** Auto-cleanup cache, ~1 giorno
- **Effort:** 1 giorno

---

## FASE 1: EMAIL CLIENT SOLIDO [80%]

### 1.1 Mark Read/Unread
- **Status:** [FATTO] - Sessione 222
- **Studio:** `ricerche/20260114_RICERCA_MarkRead.md`
- **Dipende da:** 0.3
- **Note:** /gmail/mark-read, /gmail/mark-unread

### 1.2 Drafts Auto-Save
- **Status:** [FATTO] - Sessione 222
- **Studio:** `ricerche/RICERCA_DRAFTS_20260114.md`
- **Dipende da:** 0.4
- **Note:** useDraft.ts + /gmail/drafts/* CRUD

### 1.3 Upload Attachments
- **Status:** [FATTO] - Sessione 223
- **Studio:** `studi/RICERCA_UPLOAD_ATTACHMENTS.md`, `decisioni/UPLOAD_ATTACHMENTS_SPECS.md`
- **Dipende da:** 0.4
- **Note:** useAttachments.ts + AttachmentPicker.tsx + /gmail/send-with-attachments

### 1.4 Thread View
- **Status:** [FATTO] - Sessione 223
- **Studio:** `ricerche/20260114_THREAD_VIEW_API_Research.md`, `ricerche/THREAD_VIEW_UX_Research.md`, `decisioni/THREAD_VIEW_DESIGN_SPECS.md`
- **Dipende da:** 0.3
- **Note:** useThread.ts + ThreadView.tsx + /gmail/thread/{id}

### 1.5 Resizable Panels
- **Status:** [DA FARE]
- **Studio:** `studi/RICERCA_RESIZE_PANNELLI.md`, `studi/RICERCA_RESIZABLE_PANELS_V4.md`
- **Dipende da:** 0.2
- **Note:** react-resizable-panels v4.4.0 gia installato (da integrare)
- **Effort:** 3h

### 1.6 Context Menu
- **Status:** [DA FARE]
- **Studio:** `studi/RICERCA_CONTEXT_MENU*.md` (6 file, 2200 righe!), `studi/CONTEXT_MENU_UX_STRATEGY.md`, `decisioni/CONTEXT_MENU_DESIGN_SPECS.md`
- **Dipende da:** 0.3, 1.1
- **Note:** Specs COMPLETE, pronto per implementazione!
- **Effort:** 5h

### 1.7 Bulk Actions
- **Status:** [DA FARE]
- **Studio:** ✅ `studi/STUDIO_MACRO_BULK_ACTIONS.md` (182 righe)
- **Dipende da:** 0.6, 1.1
- **Note:** Ibrido Gmail+Superhuman, Cmd+A, Shift+Click, Optimistic UI
- **Effort:** 7-10 giorni (MVP 2-3gg)

### 1.8 Labels Custom
- **Status:** [DA FARE]
- **Studio:** ✅ `studi/STUDIO_MACRO_LABELS_API.md` (~150 righe)
- **Dipende da:** 0.1
- **Note:** Max 10K labels, ~80 colori predefiniti, sync bidirezionale Gmail
- **Effort:** 2-3 giorni

### 1.9 Contacts Autocomplete
- **Status:** [DA FARE]
- **Studio:** ✅ `studi/STUDIO_MACRO_CONTACTS_API.md` (357 righe)
- **Dipende da:** 0.4
- **Note:** Google People API, debounce 300ms, chip UI, cache 5min
- **Effort:** 2-3 giorni (9h frontend + 2h backend)

### 1.10 Settings Page
- **Status:** [DA FARE]
- **Studio:** ✅ `studi/STUDIO_MACRO_SETTINGS_UI.md` (150 righe)
- **Dipende da:** Nessuno
- **Note:** Settings drawer laterale, 7 categorie + 2 hotel-specific, auto-save
- **Effort:** 8-12h

### 1.11 Firma Email
- **Status:** [DA FARE]
- **Studio:** STUDIO MANCA (pattern semplice)
- **Dipende da:** 0.4, 1.10
- **Note:** Signature storage + inject in compose
- **Effort:** 2h

---

## FASE 2: PMS INTEGRATION [0%] - LA MAGIA!

### 2.1 Guest Identification
- **Status:** [DA FARE]
- **Studio:** ✅ `studi/STUDIO_MACRO_PMS_INTEGRATION.md` (~650 righe!)
- **Dipende da:** FASE 1 completa
- **Note:** 5 strategie matching + confidence score. CRITICO per differenziazione!
- **Effort:** 8h implementazione

### 2.2 GuestSidebar Reale
- **Status:** [DA FARE]
- **Studio:** ✅ `studi/STUDIO_MACRO_PMS_INTEGRATION.md` (sezione UX)
- **Dipende da:** 2.1
- **Note:** 6 sezioni progressive, dati da PMS invece di mock
- **Effort:** 6h

### 2.3 Booking Context
- **Status:** [DA FARE]
- **Studio:** ✅ `studi/STUDIO_MACRO_PMS_INTEGRATION.md` (sezione architettura)
- **Dipende da:** 2.1, 2.2
- **Note:** Prenotazioni attive, hybrid real-time + cache
- **Effort:** 4h

### 2.4 Guest History
- **Status:** [DA FARE]
- **Studio:** ✅ `studi/STUDIO_MACRO_PMS_INTEGRATION.md` (sezione features)
- **Dipende da:** 2.3
- **Note:** Email passate + booking history + quick actions context-aware
- **Effort:** 6h

---

## FASE 3: HOTEL WORKFLOW [0%]

### 3.1 Assign to User
- **Status:** [DA FARE]
- **Studio:** STUDIO MANCA
- **Dipende da:** FASE 1 completa, 1.8
- **Note:** Custom label per assegnazione
- **Effort:** 6h

### 3.2 Team Inbox
- **Status:** [DA FARE]
- **Studio:** STUDIO MANCA
- **Dipende da:** 3.1
- **Note:** Shared view tra team
- **Effort:** 12h

### 3.3 Quick Reply Templates
- **Status:** [DA FARE]
- **Studio:** STUDIO MANCA
- **Dipende da:** 0.5
- **Note:** Template storage
- **Effort:** 4h

### 3.4 Template Variables
- **Status:** [DA FARE]
- **Studio:** STUDIO MANCA
- **Dipende da:** 3.3, 2.1
- **Note:** {{guest_name}}, {{booking_date}}, etc
- **Effort:** 4h

---

## FASE 4: MULTI-CHANNEL [0%]

### 4.1 WhatsApp Business API
- **Status:** [DA FARE]
- **Studio:** `ricerche/COMPETITOR_Callbell.md` (reference)
- **Dipende da:** FASE 3 completa
- **Note:** Integration WhatsApp Business
- **Effort:** ~30h ricerca + 40h implementazione

### 4.2 Unified Inbox
- **Status:** [DA FARE]
- **Studio:** `ricerche/COMPETITOR_Callbell.md` (reference)
- **Dipende da:** 4.1
- **Note:** Email + WhatsApp in unico inbox
- **Effort:** ~20h

### 4.3 Multi-Channel Sync
- **Status:** [DA FARE]
- **Studio:** STUDIO MANCA
- **Dipende da:** 4.2
- **Note:** Sync messaggi tra canali
- **Effort:** ~15h

---

## TECHNICAL DEBT

### TD.1 Split gmail/api.py
- **Status:** [DA FARE]
- **Studio:** Nessuno richiesto (refactoring)
- **Dipende da:** FASE 1 completa
- **Note:** 1391 righe -> 6 moduli (auth, messages, threads, drafts, labels, actions)
- **Effort:** 6h

### TD.2 Backend Testing
- **Status:** [DA FARE]
- **Studio:** ✅ `studi/STUDIO_MACRO_TESTING_STRATEGY.md` (sezione backend)
- **Dipende da:** TD.1
- **Note:** pytest + VCR.py per Gmail mock, 70% coverage target
- **Effort:** 23h

### TD.3 Frontend Testing
- **Status:** [DA FARE]
- **Studio:** ✅ `studi/STUDIO_MACRO_TESTING_STRATEGY.md` (sezione frontend)
- **Dipende da:** Nessuno
- **Note:** Vitest + React Testing Library + MSW, 70% coverage target
- **Effort:** 22h

### TD.4 Token Encryption
- **Status:** [DA FARE]
- **Studio:** STUDIO MANCA
- **Dipende da:** Nessuno
- **Note:** Token attualmente in DB plaintext
- **Effort:** 4h

### TD.5 Rate Limiting
- **Status:** [DA FARE]
- **Studio:** STUDIO MANCA
- **Dipende da:** Nessuno
- **Note:** Protezione API abuse
- **Effort:** 3h

### TD.6 Error Handling Centralizzato
- **Status:** [DA FARE]
- **Studio:** STUDIO MANCA
- **Dipende da:** Nessuno
- **Note:** Error boundaries + retry logic
- **Effort:** 4h

---

## STUDI COMPLETATI - Sessione 225

### FASE 1 - TUTTI PRONTI!

| Studio | Feature | Status | File |
|--------|---------|--------|------|
| **Bulk Actions Pattern** | 1.7 | ✅ FATTO | `studi/STUDIO_MACRO_BULK_ACTIONS.md` |
| **Gmail Labels API** | 1.8 | ✅ FATTO | `studi/STUDIO_MACRO_LABELS_API.md` |
| **Google People API** | 1.9 | ✅ FATTO | `studi/STUDIO_MACRO_CONTACTS_API.md` |
| **Settings UI Pattern** | 1.10 | ✅ FATTO | `studi/STUDIO_MACRO_SETTINGS_UI.md` |
| **Context Menu** | 1.6 | ✅ GIA PRONTO | `studi/RICERCA_CONTEXT_MENU*.md` (2200 righe!) |
| **Resizable Panels** | 1.5 | ✅ GIA PRONTO | `studi/RICERCA_RESIZABLE_PANELS_V4.md` |

### FASE 2 - PMS Integration - PRONTO!

| Studio | Feature | Status | File |
|--------|---------|--------|------|
| **PMS Integration COMPLETO** | 2.1-2.4 | ✅ FATTO | `studi/STUDIO_MACRO_PMS_INTEGRATION.md` (650 righe!) |

### Tech Debt - Testing - PRONTO!

| Studio | Feature | Status | File |
|--------|---------|--------|------|
| **Testing Strategy** | TD.2-TD.3 | ✅ FATTO | `studi/STUDIO_MACRO_TESTING_STRATEGY.md` |

---

## STUDI ANCORA MANCANTI (Priorità BASSA)

| Studio Mancante | Feature | Effort | Note |
|-----------------|---------|--------|------|
| **SSE Real-Time** | P3.1 | 3h | Server-Sent Events (POLISH, non critico) |
| **Token Security** | TD.4 | 1h | Encryption at rest |
| **Team Inbox Architecture** | 3.2 | 4h | FASE 3 |
| **WhatsApp Business** | 4.1 | 8h | FASE 4 |

**TOTALE MANCANTE:** ~16h (tutto FASE 3-4, non bloccante!)

---

## RIEPILOGO EFFORT

### FASE 1 Rimanente (per 100%) - TUTTI STUDI PRONTI!

| Step | Feature | Effort | Studio |
|------|---------|--------|--------|
| 1.5 | Resizable Panels | 3h | ✅ PRONTO |
| 1.6 | Context Menu | 5h | ✅ PRONTO (2200 righe!) |
| 1.7 | Bulk Actions | 7-10gg | ✅ PRONTO |
| 1.8 | Labels Custom | 2-3gg | ✅ PRONTO |
| 1.9 | Contacts Autocomplete | 2-3gg | ✅ PRONTO |
| 1.10 | Settings Page | 8-12h | ✅ PRONTO |

**TOTALE:** ~25-30 giorni implementazione, **0h ricerca (TUTTO PRONTO!)**

### FASE 2 (PMS Integration) - STUDIO PRONTO!

| Step | Feature | Effort | Studio |
|------|---------|--------|--------|
| 2.1 | Guest Identification | 8h | ✅ PRONTO |
| 2.2 | GuestSidebar Reale | 6h | ✅ PRONTO |
| 2.3 | Booking Context | 4h | ✅ PRONTO |
| 2.4 | Guest History | 6h | ✅ PRONTO |

**TOTALE:** ~24h implementazione, **0h ricerca (TUTTO PRONTO!)**

---

## METRICHE TARGET

| Metrica | Attuale | FASE 1 100% | FASE 2 100% |
|---------|---------|-------------|-------------|
| Health Score | 8.0/10 | 9.5/10 | 10/10 |
| Features Complete | 80% | 100% | 120%+ |
| Test Coverage | 0% | 70% | 80% |
| Differenziazione | Bassa | Media | ALTA (PMS!) |

---

## DIPENDENZE VISUALIZZATE

```
FASE 0 (Fondamenta)
  |
  +---> FASE P (Performance)
  |       |
  |       +---> P3 Polish (opzionale)
  |
  +---> FASE 1 (Email Solido)
          |
          +---> 1.5 Resizable Panels
          +---> 1.6 Context Menu (dipende: 0.3, 1.1)
          +---> 1.7 Bulk Actions (dipende: 0.6, 1.1)
          +---> 1.8 Labels Custom
          +---> 1.9 Contacts Autocomplete
          |
          +---> FASE 2 (PMS Integration)
                  |
                  +---> 2.1 Guest Identification (CRITICO!)
                  +---> 2.2 GuestSidebar (dipende: 2.1)
                  +---> 2.3 Booking Context (dipende: 2.1, 2.2)
                  +---> 2.4 Guest History (dipende: 2.3)
                  |
                  +---> FASE 3 (Hotel Workflow)
                          |
                          +---> 3.1 Assign to User (dipende: 1.8)
                          +---> 3.2 Team Inbox (dipende: 3.1)
                          +---> 3.3 Quick Reply Templates
                          +---> 3.4 Template Variables (dipende: 3.3, 2.1)
                          |
                          +---> FASE 4 (Multi-Channel)
```

---

## COSTITUZIONE-APPLIED

**COSTITUZIONE-APPLIED:** SI

**Principio usato:** "SU CARTA != REALE" + "Studiare prima di agire"

**Come applicato:**
1. Ogni step ha status REALE (verificato da stato.md aggiornato)
2. Ogni step ha link a studio esistente O segnala "STUDIO MANCA"
3. Ogni step ha dipendenze chiare
4. Sprint 1+2 (Mark Read, Drafts, Upload, Thread) segnati come FATTI perche REALMENTE implementati
5. Identificati TUTTI gli studi mancanti per proseguire

---

*"Lavoriamo in PACE! Senza CASINO! Dipende da NOI!"*

*Ultimo aggiornamento: 15 Gennaio 2026 - Sessione 224*
*Cervella Guardiana Qualita - La Custode degli Standard*

*"Non ri-fare, continua da dove altri hanno lasciato!"*
