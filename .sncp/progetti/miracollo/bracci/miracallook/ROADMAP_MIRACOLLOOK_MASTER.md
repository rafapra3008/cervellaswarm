# ROADMAP MIRACOLLOOK - Master

**Data:** 13 Gennaio 2026 - Sessione 188
**Aggiornato:** 19 Gennaio 2026 - Verifica Codice REALE
**Health Score:** 8.5/10
**Status:** FASE 1 = 92% (verificato dal codice!)

---

## VISIONE

```
MIRACOLLOOK = L'Outlook che CONOSCE il tuo hotel!

NON e un email client generico.
E il CENTRO COMUNICAZIONI dell'hotel intelligente.

LA MAGIA = PMS Integration + Guest Recognition + VELOCITA SUPERHUMAN!
```

---

## DOVE SIAMO (19 Gennaio 2026 - Verificato dal CODICE!)

```
FASE 0 (Fondamenta)     [####################] 100% COMPLETA!
FASE PERFORMANCE P1     [####################] 100% MERGED!
FASE PERFORMANCE P2     [####################] 100% MERGED!
FASE 1 (Email Solido)   [##################..] 92% <- VERIFICATO!
FASE 2 (PMS Integration)[....................] 0%
FASE 3 (Hotel Workflow) [....................] 0%

NOTA: Context Menu e Resizable Panels GIA IMPLEMENTATI!
      Vedi MAPPA_VERITA_20260119.md per dettagli.
```

---

## FASE PERFORMANCE - INSTANT FEEL - COMPLETA!

> **SCOPERTA SESSIONE 188:** I big (Gmail, Superhuman) usano le STESSE tecnologie browser!
> **COMPLETATA SESSIONE 190:** P1 + P2 MERGED in main! v2.0.0!

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

### FASE P1 - FONDAMENTA - COMPLETA!

| Step | Feature | Status |
|------|---------|--------|
| 1 | **IndexedDB Schema** | DONE - db.ts |
| 2 | **Batch API** | DONE - 51→2 API calls |
| 3 | **Skeleton Loading** | DONE - EmailSkeleton.tsx |
| 4 | **Optimistic UI** | DONE - useEmails.ts |

**Risultato:** Inbox ~1s (vs 3s prima!)

### FASE P2 - OTTIMIZZAZIONI - COMPLETA!

| Step | Feature | Status |
|------|---------|--------|
| 5 | **Prefetch Intelligente** | DONE - usePrefetchEmails.ts |
| 6 | **Hover Prefetch** | DONE - useHoverPrefetch.ts |
| 7 | **Service Worker** | DONE - Workbox + vite-plugin-pwa |
| 8 | **Offline Sync** | DONE - useOfflineSync.ts |

**Risultato:** Click email = INSTANT! PWA installabile!

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

## FASE 1 - EMAIL CLIENT SOLIDO (75%) - PROSSIMO STEP!

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
- [x] Performance P1+P2 (Sessione 190)

### Da Fare - FUNZIONI BASE MANCANTI (Sessione 191)

**CRITICHE (~8h):**
| Feature | Effort | Note |
|---------|--------|------|
| **Mark as Read/Unread** | 2h | Gmail API modify labels |
| **Drafts (auto-save)** | 6h | Gmail Drafts API |

**ALTE (~16h):**
| Feature | Effort | Note |
|---------|--------|------|
| **Bulk Actions** | 5h | Checkbox + batch API |
| **Thread View** | 4h | Visualizza conversazione |
| **Labels Custom** | 3h | Crea cartelle |
| **Upload Attachments** | 4h | Compose con file |

**MEDIE (~16h):**
| Feature | Effort | Note |
|---------|--------|------|
| **Contacts Autocomplete** | 6h | Google People API |
| **Settings Page** | 8h | Preferenze utente |
| **Firma email** | 2h | Signature in compose |

**TOTALE: ~40h per email client COMPLETO**

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
