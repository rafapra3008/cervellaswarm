# Output: TASK_STUDIO_DASHBOARD_ARCH

**Worker:** cervella-ingegnera
**Completato:** 6 Gennaio 2026
**Status:** DONE

---

## Risultato

Creato studio completo: `docs/studio/STUDIO_DASHBOARD_ARCH.md`

## Contenuto (587 righe)

1. **Diagramma Architettura** - ASCII art con 3 layer (Dashboard, API, FileSystem)

2. **Data Flow** - 3 flussi documentati:
   - File -> Dashboard (lettura)
   - Dashboard -> File (scrittura)
   - Eventi -> Dashboard (real-time)

3. **Schema JSON Proposto** - 4 modelli:
   - MappaJSON (struttura completa MAPPA)
   - TaskJSON (singolo task)
   - WorkerJSON (stato worker)
   - GlobalStatusJSON (multi-progetto)

4. **API Endpoints** - 15+ endpoint:
   - /api/mappa, /api/nord, /api/roadmap, /api/steps
   - /api/tasks (CRUD completo)
   - /api/workers, /api/heartbeat (WebSocket)

5. **Sincronizzazione** - Strategia one-way raccomandata (file = source of truth)

6. **Integrazione Worker/Regina** - 3 opzioni:
   - File-based (MVP)
   - Hook-based (futuro)
   - MCP Server (avanzato)

7. **MVP Architettura Minima** - Stack consigliato:
   - FastAPI backend
   - watchdog per file watching
   - React/Alpine.js frontend
   - Struttura files proposta

8. **Sicurezza** - Base per locale, roadmap per produzione

9. **Rischi e Mitigazioni** - 5 rischi mappati

## Dipendenze

- Attende STUDIO_DASHBOARD_TECH (tecnologie)
- Attende STUDIO_DASHBOARD_UX (wireframe)

## Raccomandazione

MVP con FastAPI + WebSocket + One-way sync.
Espandibile dopo validazione.

---

*cervella-ingegnera*
