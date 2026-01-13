# ROADMAP MIRACOLLOOK - Master

**Data:** 13 Gennaio 2026 - Sessione 188
**Health Score:** 8.0/10
**Status:** MVP Funzionante - ORA FASE PERFORMANCE!

---

## VISIONE

```
MIRACOLLOOK = L'Outlook che CONOSCE il tuo hotel!

NON e un email client generico.
E il CENTRO COMUNICAZIONI dell'hotel intelligente.

LA MAGIA = PMS Integration + Guest Recognition + VELOCITA SUPERHUMAN!
```

---

## DOVE SIAMO

```
FASE 0 (Fondamenta)     [####################] 100%
FASE 1 (Email Solido)   [###############.....] 75%
>>> FASE PERFORMANCE    [....................] 0% <<< PRIORITA!
FASE 2 (PMS Integration)[....................] 0%
FASE 3 (Hotel Workflow) [....................] 0%
```

---

## FASE PERFORMANCE - INSTANT FEEL (NUOVA PRIORITA!)

> **SCOPERTA SESSIONE 188:** I big (Gmail, Superhuman) usano le STESSE tecnologie browser!
> Possiamo avere velocita Superhuman ($30/mese) GRATIS!

### Perche Prima di Tutto?

```
+================================================================+
|                                                                |
|   PROBLEMA: Download attachment = 30-40 secondi                |
|   MA il problema e PIU GRANDE - tutta l'app e "lenta"          |
|                                                                |
|   SOLUZIONE: Architettura "Instant Feel" come i big            |
|   - Prefetching (scarica PRIMA che clicchi)                    |
|   - Cache 3-layer (Memory + IndexedDB + API)                   |
|   - Optimistic UI (mostra subito, conferma dopo)               |
|   - Virtualizzazione (render solo visibile)                    |
|   - Background sync (funziona offline!)                        |
|                                                                |
+================================================================+
```

### FASE P1 - FONDAMENTA (Week 1-2) - CRITICO

| Step | Feature | Effort | Impatto |
|------|---------|--------|---------|
| 1 | **IndexedDB Schema** | 2 giorni | Cache locale persistente |
| 2 | **Batch API** | 1 giorno | 50 email in 2 chiamate (non 50) |
| 3 | **Lista Virtualizzata** | 1 giorno | No freeze con 1000+ email |
| 4 | **Skeleton Loading** | 0.5 giorni | Perceived performance |

**Risultato:** Inbox <1s (vs 3s attuale)

### FASE P2 - OTTIMIZZAZIONI (Week 3-4) - ALTO

| Step | Feature | Effort | Impatto |
|------|---------|--------|---------|
| 5 | **Optimistic UI** | 2 giorni | Azioni istantanee |
| 6 | **Prefetch Intelligente** | 1.5 giorni | Top 5 email pronte |
| 7 | **Service Worker** | 2 giorni | Offline capability |

**Risultato:** Compete con Superhuman!

### FASE P3 - POLISH (Week 5-6) - MEDIO

| Step | Feature | Effort | Impatto |
|------|---------|--------|---------|
| 8 | SSE Real-Time | 3 giorni | Notifiche push |
| 9 | Attachment Lazy Loading | 1.5 giorni | Progress bar |
| 10 | Cache Management | 1 giorno | Auto-cleanup |

**Risultato:** Supera competitors!

### Metriche Target Performance

| Metrica | Prima | Dopo |
|---------|-------|------|
| Inbox Load | ~3s | <1s |
| Email Open | 300-500ms | <100ms (top 5) |
| Memoria 1000 email | ~500MB | <100MB |
| API Calls (50 email) | 50+ | 2-3 |
| Offline | No | Si |

### Documentazione

- Decisione: `decisioni/DECISIONE_PERFORMANCE_ARCHITECTURE.md`
- Ricerca completa: `studi/RICERCA_PERFORMANCE_EMAIL_CLIENTS.md`
- Ricerca attachments: `studi/RICERCA_ATTACHMENTS_PERFORMANCE.md`

---

## FASE 1 - EMAIL CLIENT SOLIDO (75% - IN PAUSA)

### Completato
- [x] Layout three-panel
- [x] Inbox, Archived, Starred, Snoozed, Trash viste
- [x] Send, Reply, Reply All, Forward
- [x] Quick Actions (hover + keyboard)
- [x] Keyboard shortcuts (j/k/e/r/c/f/s)
- [x] Command Palette (Cmd+K)
- [x] AI Summarization
- [x] Smart Bundles (categorizzazione auto)
- [x] Design Salutare (Tailwind v4)
- [x] Resize pannelli (react-resizable-panels v4.4.0)
- [x] Attachments view (lista allegati)
- [x] Attachments download (streaming)

### Da Fare (DOPO Fase Performance)
| Feature | Priorita | Effort | Note |
|---------|----------|--------|------|
| **Attachments upload** | CRITICO | 6h | Compose con file |
| **Split gmail/api.py** | CRITICO | 6h | 1391 righe |
| Multi-select | ALTO | 6h | Checkbox + batch |
| Undo actions | ALTO | 4h | Toast con "Undo" |
| Search avanzata UI | ALTO | 4h | Modal con filtri |

---

## FASE 2 - PMS INTEGRATION (LA MAGIA!)

### Obiettivo
Collegare email ai guest del PMS Miracollo per context automatico.

### Features
| Feature | Priorita | Effort | Note |
|---------|----------|--------|------|
| **Guest identification** | CRITICO | 8h | Match email -> guest |
| **GuestSidebar reale** | CRITICO | 6h | Dati da PMS |
| **Booking context** | CRITICO | 4h | Prenotazioni attive |
| **Guest history** | ALTO | 6h | Email + booking passati |

---

## FASE 3 - HOTEL WORKFLOW

### Assign & Team
| Feature | Priorita | Effort | Note |
|---------|----------|--------|------|
| **Assign to user** | CRITICO | 6h | Custom label |
| **Team inbox** | ALTO | 12h | Shared view |

### Templates Risposte
| Feature | Priorita | Effort | Note |
|---------|----------|--------|------|
| **Quick replies** | CRITICO | 4h | Template storage |
| **Variables** | ALTO | 4h | {{guest_name}} |

---

## TECHNICAL DEBT

### Critico (DOPO Fase Performance)
- [ ] Split gmail/api.py (1391 righe -> 6 moduli)
- [ ] Testing backend (0% -> 70%)
- [ ] Testing frontend (vitest)

### Alto
- [ ] Token encryption (DB plaintext)
- [ ] Rate limiting
- [ ] Error handling centralizzato

---

## NEXT STEPS

### PRIORITA IMMEDIATA: FASE PERFORMANCE

```
+================================================================+
|                                                                |
|   SETTIMANA 1-2: FONDAMENTA                                    |
|   [ ] IndexedDB schema setup                                   |
|   [ ] Batch API client                                         |
|   [ ] react-window virtualizzazione                            |
|   [ ] Skeleton loading components                              |
|                                                                |
|   SETTIMANA 3-4: OTTIMIZZAZIONI                                |
|   [ ] Optimistic UI (useOptimistic hook)                       |
|   [ ] Prefetch intelligente top 5                              |
|   [ ] Service Worker sync                                      |
|                                                                |
+================================================================+
```

### DOPO Fase Performance
1. [ ] Attachments upload
2. [ ] Split gmail/api.py
3. [ ] Testing suite
4. [ ] PMS Integration

---

## METRICHE TARGET

| Metrica | Attuale | Target | Note |
|---------|---------|--------|------|
| Health Score | 8.0/10 | 9.5/10 | Post-performance |
| Inbox Load | ~3s | <1s | Fase P1 |
| Email Open | 500ms | <100ms | Fase P2 |
| Test Coverage | 0% | 70% | Post-tech debt |
| Offline | No | Si | Fase P2 |

---

*"Il Centro Comunicazioni dell'Hotel Intelligente"*
*"Velocita Superhuman. Prezzo Gmail. MIRACOLLOOK!"*
*"Non esistono cose difficili, esistono cose non studiate!"*
