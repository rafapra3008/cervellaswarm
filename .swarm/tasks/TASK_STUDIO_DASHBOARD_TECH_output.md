# OUTPUT: TASK_STUDIO_DASHBOARD_TECH

**Data completamento:** 6 Gennaio 2026
**Worker:** cervella-researcher

---

## RISULTATO

Studio completo scritto in: `docs/studio/STUDIO_DASHBOARD_TECH.md`

## RACCOMANDAZIONE FINALE

```
+------------------------------------------------------------------+
|                                                                  |
|   Stack Raccomandato per Dashboard Visuale MAPPA:                |
|                                                                  |
|   Frontend:     React + Vite + TypeScript                        |
|   Roadmap:      React Flow + Custom Components                   |
|   Realtime:     Server-Sent Events (SSE)                         |
|   Markdown:     react-markdown + remark/rehype                   |
|   Backend:      FastAPI (gia' in uso!)                           |
|   Deploy MVP:   FastAPI serve React build (locale)               |
|   Deploy Prod:  Vercel (frontend) + API separata                 |
|                                                                  |
+------------------------------------------------------------------+
```

## PERCHE' QUESTO STACK

1. **FAMILIARE**: React e FastAPI li conosciamo gia'
2. **MATURO**: Ecosistema stabile, documentazione eccellente
3. **VELOCE**: Vite + SSE = feedback istantaneo
4. **SCALABILE**: Da locale a produzione senza riscrivere
5. **PRAGMATICO**: MVP in 1-2 giorni, poi iteriamo

## CONTENUTI STUDIO (490+ righe)

1. Executive Summary con raccomandazione chiara
2. Confronto Framework Frontend (React vs Vue vs Svelte vs SolidJS)
3. Librerie Visualizzazione (React Flow, Mermaid, vis.js, D3.js, GoJS)
4. Tempo Reale (SSE vs WebSocket) - SSE raccomandato
5. Markdown Rendering (react-markdown + plugins)
6. Hosting/Deploy (MVP locale vs Produzione cloud)
7. Architettura MVP dettagliata (1-2 giorni)
8. Risorse e link documentazione

## MVP IN 1-2 GIORNI

**Giorno 1:**
- Setup Vite + React + TypeScript
- Componente MarkdownViewer
- FastAPI endpoint base
- UI con TailwindCSS

**Giorno 2:**
- Parser MAPPA.md -> JSON
- SSE per aggiornamenti live
- File watcher (watchdog)
- Navigazione documenti

## ALTERNATIVA MINIMALISTA

Se serve ancora piu' semplice:
```
Python + Streamlit = Dashboard in ore invece che giorni
```

---

**STATUS: COMPLETATO**
