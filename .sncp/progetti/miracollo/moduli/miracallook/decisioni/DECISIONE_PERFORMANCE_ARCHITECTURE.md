# DECISIONE - Architettura Performance Miracollook

> **Data:** 13 Gennaio 2026 - Sessione 188
> **Decisione:** Implementare architettura "Instant Feel" come i big players
> **Status:** APPROVATA

---

## IL PROBLEMA

```
Download attachments: 30-40 secondi
Perche? Ogni click = 2 chiamate Google API + transfer

Ma il VERO problema e piu grande:
- Non solo attachments
- TUTTA l'app sembra lenta
- I big (Gmail, Superhuman, Outlook) sembrano istantanei
```

---

## LA SCOPERTA

```
+================================================================+
|                                                                |
|   I BIG NON SONO MAGICI!                                       |
|                                                                |
|   Usano le STESSE tecnologie browser:                          |
|   - IndexedDB (disponibile a tutti)                            |
|   - Service Workers (disponibile a tutti)                      |
|   - Optimistic UI (pattern, non tecnologia)                    |
|                                                                |
|   DIFFERENZA: Architettura + attenzione ai dettagli            |
|                                                                |
+================================================================+
```

---

## LE 5 STRATEGIE DEI BIG

| # | Strategia | Come Funziona | Effetto |
|---|-----------|---------------|---------|
| 1 | **Prefetching** | Scaricano PRIMA che clicchi | 0ms percepiti |
| 2 | **Cache 3-Layer** | Memory + IndexedDB + API | -90% latency |
| 3 | **Optimistic UI** | Mostrano subito, confermano dopo | <10ms feedback |
| 4 | **Virtualizzazione** | Render solo 20-30 visibili | No freeze 1000+ |
| 5 | **Background Sync** | Service Workers in background | Funziona offline |

---

## LA DECISIONE

**Implementare architettura "Instant Feel" in 3 fasi:**

### FASE 1 - FONDAMENTA (Week 1-2) - PRIORITA ALTA

1. **IndexedDB Schema** - Cache locale persistente
2. **Batch API** - 50 email in 2 chiamate (non 50)
3. **Lista Virtualizzata** - react-window
4. **Skeleton Loading** - Perceived performance

**Risultato atteso:** Da 3s a <1s inbox load

### FASE 2 - OTTIMIZZAZIONI (Week 3-4)

5. **Optimistic UI** - Azioni istantanee
6. **Prefetch Intelligente** - Top 5 email pronte
7. **Service Worker** - Offline capability

**Risultato atteso:** Compete con Superhuman

### FASE 3 - POLISH (Week 5-6)

8. **SSE Real-Time** - Notifiche push
9. **Attachment Lazy Loading** - Progress bar
10. **Cache Management** - Auto-cleanup

**Risultato atteso:** Supera competitors

---

## METRICHE TARGET

| Metrica | Prima | Dopo |
|---------|-------|------|
| Inbox Load | ~3s | <1s |
| Email Open | 300-500ms | <100ms (top 5) |
| Memoria 1000 email | ~500MB | <100MB |
| API Calls (50 email) | 50+ | 2-3 |
| Offline | No | Si |

---

## PERCHE QUESTA DECISIONE

1. **Superhuman costa $30/mese** - Noi possiamo avere stesso livello GRATIS
2. **Stesse tecnologie browser** - Non serve nulla di speciale
3. **User experience** - 30-40s e inaccettabile per utenti moderni
4. **Scalabilita** - Con 1000+ email non possiamo freezare

---

## TRADE-OFFS ACCETTATI

| Trade-off | Scelta | Perche |
|-----------|--------|--------|
| API calls vs Speed | Prefetch top 5 | 80% user apre recenti |
| Storage | 30 giorni default | Balance quota vs UX |
| Complexity | Offline-first | Zero latency > sempre-online |

---

## FILE DI RIFERIMENTO

- Ricerca completa: `studi/RICERCA_PERFORMANCE_EMAIL_CLIENTS.md`
- Ricerca attachments: `studi/RICERCA_ATTACHMENTS_PERFORMANCE.md`

---

## PROSSIMI STEP

1. [x] Ricerca completata
2. [x] Decisione documentata
3. [ ] Guardiana Qualita valida il piano
4. [ ] Iniziare FASE 1

---

*"Non esistono cose difficili, esistono cose non studiate!"*
*Abbiamo studiato. Ora implementiamo!*
