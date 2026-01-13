# PIANO COMPLETO MIRACOLLOOK

> **Data:** 13 Gennaio 2026 - Sessione 188
> **Status:** Piano Performance APPROVATO, pronto per implementazione

---

## VISIONE

```
+================================================================+
|                                                                |
|   MIRACOLLOOK                                                  |
|   "Il Centro Comunicazioni dell'Hotel Intelligente"            |
|                                                                |
|   Velocita Superhuman ($30/mese) + Prezzo Gmail (gratis!)      |
|                                                                |
+================================================================+
```

---

## STATO ATTUALE

```
FASE 0 (Fondamenta)     [####################] 100%
FASE 1 (Email Solido)   [###############.....] 75%
>>> FASE PERFORMANCE    [....................] 0% <<< PROSSIMA!
FASE 2 (PMS Integration)[....................] 0%
FASE 3 (Hotel Workflow) [....................] 0%
```

---

## PARTE 1: COSA ABBIAMO STUDIATO (Sessione 188)

### 1.1 Ricerca Performance Email Clients

**File:** `studi/RICERCA_PERFORMANCE_EMAIL_CLIENTS.md` (1700+ righe)

**Cosa abbiamo imparato:**

| Strategia | Come Funziona | Beneficio |
|-----------|---------------|-----------|
| **Prefetching** | Scarica PRIMA che user clicchi | 0ms percepiti |
| **Cache 3-Layer** | Memory + IndexedDB + API | -90% latency |
| **Optimistic UI** | Mostra subito, conferma dopo | <10ms feedback |
| **Virtualizzazione** | Render solo 20-30 visibili | No freeze 1000+ |
| **Background Sync** | Service Workers | Funziona offline |

**Competitors analizzati:**
- Gmail (prefetch + CDN + GZIP)
- Superhuman (100ms rule + local DB + keyboard-first)
- Outlook (optimistic UI + background sync)
- Apple Mail (offline-first)

### 1.2 Ricerca Attachments Performance

**File:** `studi/RICERCA_ATTACHMENTS_PERFORMANCE.md` (660+ righe)

**Problema identificato:**
- Download attachment = 30-40 secondi
- Causa: 2 chiamate API Google per ogni download

**Soluzione studiata:**
- Streaming + GZIP (-40% tempo)
- Redis cache (download ripetuti <1s)
- Eager loading (prefetch in background)

### 1.3 Ricerca Upload Attachments

**File:** `studi/RICERCA_UPLOAD_ATTACHMENTS.md`

**Approccio studiato:**
- multipart/form-data (standard HTTP)
- FastAPI UploadFile
- MIMEMultipart per Gmail API
- Limite 25MB per email

---

## PARTE 2: COSA MANCA DA FARE PRIMA (Bug + Tech Debt)

### 2.1 Bug Noti

| # | Bug | Priorita | Status | Note |
|---|-----|----------|--------|------|
| 1 | **Compose subject** | ALTO | DA INVESTIGARE | Email arrivano senza oggetto |
| 2 | **Download lento** | ALTO | RISOLTO CON PIANO | 30-40s -> piano Performance |

### 2.2 Feature FASE 1 Mancanti (IN PAUSA)

| # | Feature | Priorita | Effort | Status |
|---|---------|----------|--------|--------|
| 1 | **Attachments upload** | CRITICO | 6h | Ricerca fatta, da implementare |
| 2 | **Split gmail/api.py** | CRITICO | 6h | 1391 righe, refactoring |
| 3 | Multi-select | ALTO | 6h | Checkbox + batch actions |
| 4 | Undo actions | ALTO | 4h | Toast con "Undo" |
| 5 | Search avanzata UI | ALTO | 4h | Modal con filtri |

### 2.3 Technical Debt

| # | Debt | Priorita | Effort | Note |
|---|------|----------|--------|------|
| 1 | Testing backend | CRITICO | 12h | 0% -> 70% coverage |
| 2 | Testing frontend | CRITICO | 8h | Vitest setup |
| 3 | Token encryption | ALTO | 4h | DB plaintext |
| 4 | Rate limiting | ALTO | 4h | API protection |
| 5 | Error handling | MEDIO | 6h | Centralizzato |

---

## PARTE 3: PIANO FASE PERFORMANCE (APPROVATO)

### 3.1 Checklist Pre-Implementazione

```
PRIMA DI INIZIARE:
[ ] Verificare React version (deve essere 19+ per useOptimistic)
[ ] Creare branch feature/performance-phase1
[ ] Setup web-vitals per baseline metrics
[ ] Definire success criteria misurabili
```

### 3.2 FASE P1 - FONDAMENTA (Week 1-2)

| Step | Feature | Effort | Impatto | Status |
|------|---------|--------|---------|--------|
| 1 | **IndexedDB Schema** | 2 giorni | Cache locale persistente | DA FARE |
| 2 | **Batch API Client** | 1 giorno | 50 email in 2 chiamate | DA FARE |
| 3 | **Lista Virtualizzata** | 1 giorno | No freeze 1000+ email | DA FARE |
| 4 | **Skeleton Loading** | 0.5 giorni | Perceived performance | DA FARE |

**Risultato atteso:** Inbox load <1s (vs 3s attuale)

**Dettagli tecnici:**

```
IndexedDB Schema:
- Store: emails (keyPath: clientId, indexes: serverId, folder, threadId, from, updated)
- Store: syncQueue (keyPath: id, autoIncrement)
- Store: attachments (keyPath: attachmentId, indexes: emailId, downloaded)

Batch API:
- 1 chiamata lista (50 email headers)
- 1 chiamata batch (top 5 body completi)
- Totale: 2 chiamate invece di 50+

Virtualizzazione:
- react-window (FixedSizeList)
- itemSize: 80px per row
- Render solo 20-30 visibili

Skeleton:
- EmailRowSkeleton component
- Shimmer animation CSS
- No blank screens mai
```

### 3.3 FASE P2 - OTTIMIZZAZIONI (Week 3-4)

| Step | Feature | Effort | Impatto | Status |
|------|---------|--------|---------|--------|
| 5 | **Optimistic UI** | 2 giorni | Azioni istantanee | DA FARE |
| 6 | **Prefetch Intelligente** | 1.5 giorni | Top 5 email pronte | DA FARE |
| 7 | **Service Worker Sync** | 2 giorni | Offline capability | DA FARE |

**Risultato atteso:** Compete con Superhuman!

**Dettagli tecnici:**

```
Optimistic UI:
- useOptimistic hook (React 19+)
- Send/Archive/Delete immediate feedback
- Rollback on error
- Queue in syncQueue per retry

Prefetch:
- Top 5 email body prefetchate all'apertura
- Prefetch next batch quando scroll 80%
- Smart caching (no duplicati)

Service Worker:
- Background sync per outbox
- Auto-retry quando torna online
- Offline email viewing
```

### 3.4 FASE P3 - POLISH (Week 5-6)

| Step | Feature | Effort | Impatto | Status |
|------|---------|--------|---------|--------|
| 8 | SSE Real-Time | 3 giorni | Notifiche push | DA FARE |
| 9 | Attachment Lazy Loading | 1.5 giorni | Progress bar | DA FARE |
| 10 | Cache Management | 1 giorno | Auto-cleanup | DA FARE |

**Risultato atteso:** Supera competitors!

### 3.5 Metriche Target

| Metrica | Prima | Dopo P1 | Dopo P2 | Dopo P3 |
|---------|-------|---------|---------|---------|
| Inbox Load | ~3s | <1s | <1s | <1s |
| Email Open | 300-500ms | <300ms | <100ms | <100ms |
| Memoria 1000 email | ~500MB | <100MB | <100MB | <100MB |
| API Calls (50 email) | 50+ | 2-3 | 2-3 | 2-3 |
| Offline | No | Parziale | Si | Si |

### 3.6 Rischi Identificati

| # | Rischio | Mitigazione |
|---|---------|-------------|
| 1 | Quota browser | 30gg default + auto-cleanup |
| 2 | Conflict resolution | Last-write-wins |
| 3 | Gmail rate limits | Batch + exponential backoff |
| 4 | IndexedDB Safari | idb library wrapper |
| 5 | Migration user esistenti | Graceful first sync |
| 6 | Token refresh offline | Queue + retry on reconnect |
| 7 | Storage mobile | Detect iOS, reduce retention |

---

## PARTE 4: DOPO FASE PERFORMANCE

### 4.1 Completare FASE 1 (Email Solido)

| # | Feature | Priorita | Note |
|---|---------|----------|------|
| 1 | Attachments upload | CRITICO | Compose con file |
| 2 | Split gmail/api.py | CRITICO | Refactoring |
| 3 | Multi-select | ALTO | Batch actions |
| 4 | Undo actions | ALTO | Toast |
| 5 | Search UI | ALTO | Modal filtri |

### 4.2 FASE 2 - PMS Integration

| # | Feature | Priorita | Note |
|---|---------|----------|------|
| 1 | Guest identification | CRITICO | Match email -> guest |
| 2 | GuestSidebar reale | CRITICO | Dati da PMS |
| 3 | Booking context | CRITICO | Prenotazioni attive |
| 4 | Guest history | ALTO | Email + booking passati |

### 4.3 FASE 3 - Hotel Workflow

| # | Feature | Priorita | Note |
|---|---------|----------|------|
| 1 | Assign to user | CRITICO | Custom label |
| 2 | Team inbox | ALTO | Shared view |
| 3 | Quick replies | CRITICO | Template storage |
| 4 | Variables | ALTO | {{guest_name}} |

---

## PARTE 5: DOCUMENTAZIONE

### File SNCP Creati/Aggiornati (Sessione 188)

```
.sncp/progetti/miracollo/moduli/miracallook/
├── studi/
│   ├── RICERCA_PERFORMANCE_EMAIL_CLIENTS.md     (1700+ righe) NEW!
│   ├── RICERCA_ATTACHMENTS_PERFORMANCE.md       (660+ righe) NEW!
│   └── RICERCA_UPLOAD_ATTACHMENTS.md            NEW!
├── decisioni/
│   └── DECISIONE_PERFORMANCE_ARCHITECTURE.md    NEW!
├── reports/
│   └── VALIDAZIONE_PIANO_PERFORMANCE.md         NEW!
├── ROADMAP_MIRACOLLOOK_MASTER.md                UPDATED!
├── PIANO_COMPLETO_MIRACOLLOOK.md                NEW! (questo file)
└── stato.md                                     UPDATED!
```

### Validazione

```
GUARDIANA QUALITA: APPROVATO 8.5/10

PASS: Fattibilita Tecnica (9/10)
PASS: Effort Stimati (8/10) - buffer +20%
PASS: Ordine Fasi (9/10)
PASS: Rischi (7/10) - +3 rischi aggiunti
PASS: Priorita (9/10)
PASS: Trade-offs (9/10)
```

---

## PARTE 6: TIMELINE SUGGERITA

```
+================================================================+
|                                                                |
|   GENNAIO 2026 (Settimane 3-4)                                 |
|   [====] FASE P1 - Fondamenta                                  |
|         IndexedDB + Batch API + Virtualizzazione + Skeleton    |
|                                                                |
|   FEBBRAIO 2026 (Settimane 1-2)                                |
|   [====] FASE P2 - Ottimizzazioni                              |
|         Optimistic UI + Prefetch + Service Worker              |
|                                                                |
|   FEBBRAIO 2026 (Settimane 3-4)                                |
|   [====] FASE P3 - Polish                                      |
|         SSE + Attachment Lazy + Cache Management               |
|                                                                |
|   MARZO 2026                                                   |
|   [====] Completare FASE 1 + Tech Debt                         |
|         Upload + Split api.py + Testing                        |
|                                                                |
|   APRILE 2026                                                  |
|   [====] FASE 2 - PMS Integration                              |
|         Guest recognition + Booking context                    |
|                                                                |
+================================================================+
```

---

## CONCLUSIONE

```
+================================================================+
|                                                                |
|   MIRACOLLOOK - IL PIANO E CHIARO!                             |
|                                                                |
|   STUDIATO:                                                    |
|   [x] Come fanno i big (Gmail, Superhuman, Outlook)            |
|   [x] 5 strategie performance (prefetch, cache, optimistic)    |
|   [x] Architettura "Instant Feel"                              |
|   [x] Upload attachments (multipart/form-data)                 |
|                                                                |
|   DA FARE PRIMA:                                               |
|   [ ] Bug compose subject                                      |
|   [ ] Verifica React 19+                                       |
|   [ ] Setup branch + web-vitals                                |
|                                                                |
|   PROSSIMO:                                                    |
|   [ ] FASE P1 - IndexedDB + Batch + Virtualizzazione           |
|                                                                |
|   "Non esistono cose difficili, esistono cose non studiate!"   |
|   ABBIAMO STUDIATO. ORA IMPLEMENTIAMO!                         |
|                                                                |
+================================================================+
```

---

*Creato: 13 Gennaio 2026 - Sessione 188*
*"Velocita Superhuman. Prezzo Gmail. MIRACOLLOOK!"*
