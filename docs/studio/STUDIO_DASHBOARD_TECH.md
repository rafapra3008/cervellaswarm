# STUDIO TECNOLOGIE - Dashboard Visuale MAPPA

**Data:** 6 Gennaio 2026
**Autore:** cervella-researcher
**Versione:** 1.0.0

---

## EXECUTIVE SUMMARY

```
+------------------------------------------------------------------+
|                                                                  |
|   RACCOMANDAZIONE FINALE:                                        |
|                                                                  |
|   Frontend:     React + Vite + TypeScript                        |
|   Roadmap:      React Flow + Custom Components                   |
|   Realtime:     Server-Sent Events (SSE)                         |
|   Markdown:     react-markdown + remark/rehype                   |
|   Backend:      FastAPI (che gia' usiamo!)                       |
|   Deploy MVP:   FastAPI serve React build (locale)               |
|   Deploy Prod:  Vercel (frontend) + API separata                 |
|                                                                  |
|   PERCHE'? Stack familiare, performance eccellente,              |
|   ecosistema maturo, pronto per produzione.                      |
|                                                                  |
+------------------------------------------------------------------+
```

---

## 1. FRAMEWORK FRONTEND

### Confronto 2025-2026

| Framework | Performance | Ecosistema | Learning Curve | Bundle Size | Raccomandato |
|-----------|-------------|------------|----------------|-------------|--------------|
| **React** | Buona | Eccellente | Media | ~40KB | SI |
| Vue | Buona | Buono | Facile | ~33KB | Alternativa |
| Svelte | Ottima | Medio | Facile | ~2KB | Futuro |
| SolidJS | Eccellente | Piccolo | Media | ~7KB | No (ecosistema) |

### Analisi Dettagliata

#### React (RACCOMANDATO)
**Pro:**
- Ecosistema piu' grande: migliaia di librerie testate
- Tooling eccellente: Next.js, Vite, Remix
- Hiring pool: facile trovare sviluppatori
- Documentazione: la migliore disponibile
- Stabilita': usato in produzione ovunque

**Contro:**
- Bundle size maggiore di Svelte/Solid
- Virtual DOM ha overhead (ma accettabile)
- Verbosita' rispetto a Svelte

**Perche' sceglierlo:**
> "React remains the most popular and battle-tested, especially with Next.js leading the edge rendering era."
> -- [FrontendTools 2025](https://www.frontendtools.tech/blog/best-frontend-frameworks-2025-comparison)

#### Vue
Ottima alternativa se si preferisce un approccio piu' "opinionated".
Documentazione eccezionale, Single File Components eleganti.

#### Svelte
Il futuro? Compila a JavaScript puro, niente virtual DOM.
Svelte 5 con "Runes" molto promettente ma ecosistema ancora piccolo.

> "Svelte ranks highest in developer satisfaction (72.8% admired)"
> -- Stack Overflow 2024

#### SolidJS
Performance migliore in assoluto ma ecosistema troppo piccolo per produzione.

### VERDETTO: React + Vite

```
npm create vite@latest dashboard -- --template react-ts
```

Con Vite:
- Startup < 1 secondo
- HMR istantaneo
- Build ottimizzato per produzione
- Supporto TypeScript nativo

---

## 2. LIBRERIE VISUALIZZAZIONE ROADMAP/TIMELINE

### Opzioni Analizzate

| Libreria | Tipo | Pro | Contro | Prezzo |
|----------|------|-----|--------|--------|
| **React Flow** | Nodi/Grafi | Perfetto per flowchart, React-native | Richiede customizzazione | Free/Pro |
| D3.js | Low-level | Massima flessibilita' | Curva di apprendimento ripida | Free |
| Mermaid | Text-to-diagram | Semplice, integrato ovunque | Limitata interattivita' | Free |
| GoJS | Enterprise | Features avanzate | Costoso, licenza | $$$$ |
| vis.js Timeline | Timeline | Ottimo per timeline | Stile datato | Free |
| TimelineJS | Storytelling | Bello per presentazioni | Non interattivo | Free |

### Analisi Dettagliata

#### React Flow (RACCOMANDATO per grafi)

```
npm install reactflow
```

**Pro:**
- Integrazione nativa con React
- Nodi e edge customizzabili al 100%
- Minimap, controlli zoom, pan
- Ottimizzato per grafi complessi
- Community attiva

**Uso per MAPPA:**
Ogni STEP della roadmap = un nodo
Dipendenze = edge connettori
Stato (fatto/in_progress/todo) = colore nodo

#### Mermaid (RACCOMANDATO per markdown)

```
npm install mermaid
```

**Pro:**
- Diagrammi da testo markdown-like
- 1.2M+ download settimanali npm
- Integrato in GitHub, GitLab, Notion
- Perfetto per documentazione

**Uso per MAPPA:**
Renderizzare diagrammi inline nei file .md

#### vis.js Timeline (RACCOMANDATO per timeline)

```
npm install vis-timeline vis-data
```

**Pro:**
- Timeline interattive drag & drop
- Zoom temporale
- Gruppi e cluster
- Performance con migliaia di items

**Uso per MAPPA:**
Timeline temporale degli STEP con milestone

### ARCHITETTURA PROPOSTA

```
+------------------------------------------------------------------+
|                      DASHBOARD MAPPA                              |
+------------------------------------------------------------------+
|                                                                  |
|   +------------------+  +----------------------------------+     |
|   |                  |  |                                  |     |
|   |   ROADMAP        |  |   DETTAGLIO STEP                 |     |
|   |   (React Flow)   |  |   (react-markdown)               |     |
|   |                  |  |                                  |     |
|   |   [STEP 1]-->    |  |   ## Step 3: Dashboard           |     |
|   |   [STEP 2]-->    |  |   - [ ] Task 1                   |     |
|   |   [STEP 3]       |  |   - [x] Task 2                   |     |
|   |                  |  |   - [ ] Task 3                   |     |
|   +------------------+  +----------------------------------+     |
|                                                                  |
|   +----------------------------------------------------------+   |
|   |              TIMELINE (vis.js)                            |   |
|   |   Jan 2026 -------- Feb 2026 -------- Mar 2026           |   |
|   |      [S1]            [S2][S3]            [S4]             |   |
|   +----------------------------------------------------------+   |
|                                                                  |
+------------------------------------------------------------------+
```

---

## 3. STATO IN TEMPO REALE

### WebSocket vs Server-Sent Events (SSE)

| Criterio | WebSocket | SSE |
|----------|-----------|-----|
| Direzione | Bidirezionale | Server -> Client |
| Setup | Piu' complesso | Semplice (HTTP) |
| Reconnection | Manuale | Automatica |
| Overhead | 2 bytes/frame | 5 bytes/messaggio |
| Browser Support | Eccellente | Eccellente |
| Per Dashboard | Overkill | PERFETTO |

### RACCOMANDAZIONE: SSE

> "For 90% of dashboards, crypto prices, stock tickers, notifications - SSE is better and simpler."
> -- [Ably Blog](https://ably.com/blog/websockets-vs-sse)

**Perche' SSE per la Dashboard MAPPA:**

1. **Unidirezionale**: I file .md cambiano sul server, la UI si aggiorna
2. **HTTP nativo**: Nessuna libreria extra, funziona ovunque
3. **Auto-reconnect**: EventSource riconnette automaticamente
4. **Semplice**: Poche righe di codice

### Implementazione Backend (FastAPI)

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio

app = FastAPI()

async def file_watcher():
    """Genera eventi quando i file cambiano"""
    while True:
        # Controlla modifiche ai file
        changes = check_for_changes()  # Implementare
        if changes:
            yield f"data: {json.dumps(changes)}\n\n"
        await asyncio.sleep(1)  # Poll ogni secondo

@app.get("/events")
async def events():
    return StreamingResponse(
        file_watcher(),
        media_type="text/event-stream"
    )
```

### Implementazione Frontend (React)

```typescript
useEffect(() => {
  const eventSource = new EventSource('/api/events');

  eventSource.onmessage = (event) => {
    const data = JSON.parse(event.data);
    // Aggiorna stato React
    setRoadmapData(data);
  };

  eventSource.onerror = () => {
    // Auto-reconnect gestito dal browser
    console.log('Reconnecting...');
  };

  return () => eventSource.close();
}, []);
```

### File Watcher (Backend)

Opzioni per monitorare file .md:

| Libreria | OS | Pro |
|----------|-----|-----|
| watchdog (Python) | Cross-platform | Maturo, affidabile |
| inotify | Linux | Nativo, efficiente |
| FSEvents | macOS | Nativo per Mac |
| chokidar (Node) | Cross-platform | Se backend Node |

**Per FastAPI: watchdog**

```bash
pip install watchdog
```

```python
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MarkdownHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('.md'):
            # Notifica SSE
            notify_clients(event.src_path)
```

---

## 4. MARKDOWN RENDERING

### react-markdown (RACCOMANDATO)

```bash
npm install react-markdown remark-gfm rehype-highlight rehype-slug
```

**Pipeline:**
```
markdown -> remark -> mdast -> remark plugins -> remark-rehype -> hast -> rehype plugins -> React components
```

**Pro:**
- Sicuro: no `dangerouslySetInnerHTML`
- Plugin ecosystem: remark + rehype
- GitHub Flavored Markdown: tabelle, task list, strikethrough
- Syntax highlighting: rehype-highlight
- Link ancorati: rehype-slug

### Esempio Implementazione

```tsx
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeHighlight from 'rehype-highlight';
import rehypeSlug from 'rehype-slug';

function MarkdownViewer({ content }: { content: string }) {
  return (
    <ReactMarkdown
      remarkPlugins={[remarkGfm]}
      rehypePlugins={[rehypeHighlight, rehypeSlug]}
      components={{
        // Custom rendering per link
        a: ({ href, children }) => (
          <a
            href={href}
            onClick={(e) => handleInternalLink(e, href)}
            className="text-blue-600 hover:underline"
          >
            {children}
          </a>
        ),
        // Custom rendering per checkbox
        input: ({ checked }) => (
          <input
            type="checkbox"
            checked={checked}
            readOnly
            className="mr-2"
          />
        )
      }}
    >
      {content}
    </ReactMarkdown>
  );
}
```

### Navigazione tra Documenti

Per link clickabili che navigano tra .md:

```tsx
function handleInternalLink(e: React.MouseEvent, href: string) {
  if (href?.endsWith('.md')) {
    e.preventDefault();
    // Carica il nuovo documento
    loadMarkdownFile(href);
  }
}
```

---

## 5. HOSTING/DEPLOY

### Opzioni Analizzate

| Opzione | Pro | Contro | Costo | MVP? |
|---------|-----|--------|-------|------|
| FastAPI serve build | Semplice, tutto insieme | Un solo server | Free | SI |
| Vite dev server | HMR, sviluppo | Solo dev | Free | SI |
| Vercel | Edge, veloce, CI/CD | Vendor lock-in | Free tier | Prod |
| Netlify | Semplice, form handling | Meno edge | Free tier | Prod |
| GitHub Pages | Gratis, integrato | Solo static | Free | No (serve API) |

### MVP: FastAPI Serve Build

Per sviluppo e primi test, la cosa piu' semplice:

```python
# main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse

app = FastAPI()

# API endpoints
@app.get("/api/roadmap")
async def get_roadmap():
    # Parse MAPPA.md e ritorna JSON
    return parse_roadmap()

@app.get("/api/events")
async def events():
    # SSE per aggiornamenti
    return StreamingResponse(...)

# Serve React build
@app.get("/")
async def index():
    return FileResponse("frontend/dist/index.html")

app.mount("/", StaticFiles(directory="frontend/dist"), name="static")
```

**Workflow:**

```bash
# 1. Build frontend
cd frontend && npm run build

# 2. Run server
cd .. && uvicorn main:app --reload

# 3. Apri http://localhost:8000
```

### Produzione: Vercel + FastAPI

```
                    +------------------+
                    |      Vercel      |
                    |  (React build)   |
                    +--------+---------+
                             |
                             | API calls
                             v
                    +------------------+
                    |    FastAPI       |
                    | (Railway/Render) |
                    +------------------+
                             |
                             v
                    +------------------+
                    |   File System    |
                    |   (.md files)    |
                    +------------------+
```

---

## 6. ARCHITETTURA MVP (1-2 GIORNI)

### Stack Minimo

```
Frontend:
  - React + Vite + TypeScript
  - react-markdown (rendering .md)
  - TailwindCSS (styling veloce)

Backend:
  - FastAPI (gia' lo conosciamo!)
  - watchdog (file watcher)
  - SSE per aggiornamenti

Nessuna libreria grafica complessa per MVP!
Prima funziona, poi si abbellisce.
```

### Struttura Progetto

```
cervellaswarm-dashboard/
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── components/
│   │   │   ├── RoadmapView.tsx      # Mostra step MAPPA
│   │   │   ├── MarkdownViewer.tsx   # Render .md
│   │   │   └── StatusBadge.tsx      # Stato worker
│   │   ├── hooks/
│   │   │   └── useSSE.ts            # Hook per SSE
│   │   └── types/
│   │       └── roadmap.ts           # TypeScript types
│   ├── package.json
│   └── vite.config.ts
│
├── backend/
│   ├── main.py                      # FastAPI app
│   ├── parsers/
│   │   └── markdown_parser.py       # Parse MAPPA.md -> JSON
│   ├── watchers/
│   │   └── file_watcher.py          # watchdog setup
│   └── requirements.txt
│
└── README.md
```

### Fasi MVP

**Giorno 1:**
1. Setup Vite + React + TypeScript
2. Componente MarkdownViewer funzionante
3. FastAPI endpoint che legge un .md
4. UI base con TailwindCSS

**Giorno 2:**
1. Parser per MAPPA.md -> struttura JSON
2. SSE per aggiornamenti live
3. File watcher con watchdog
4. Navigazione tra documenti

### Cosa NON fare nel MVP

```
NO: React Flow complesso (troppo tempo)
NO: Timeline grafica (aggiungiamo dopo)
NO: Animazioni elaborate
NO: Deploy su cloud
NO: Autenticazione

SI: Funziona
SI: Mostra i dati
SI: Si aggiorna quando i file cambiano
SI: E' usabile localmente
```

---

## 7. RISORSE E DOCUMENTAZIONE

### Framework e Tools

- [Vite Getting Started](https://vite.dev/guide/)
- [React Documentation](https://react.dev/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [TailwindCSS](https://tailwindcss.com/docs)

### Visualizzazione

- [React Flow Documentation](https://reactflow.dev/)
- [vis.js Timeline](https://visjs.github.io/vis-timeline/docs/timeline/)
- [Mermaid Live Editor](https://mermaid.live/)

### Markdown

- [react-markdown GitHub](https://github.com/remarkjs/react-markdown)
- [remark plugins](https://github.com/remarkjs/remark/blob/main/doc/plugins.md)
- [rehype plugins](https://github.com/rehypejs/rehype/blob/main/doc/plugins.md)

### Backend

- [FastAPI Static Files](https://fastapi.tiangolo.com/tutorial/static-files/)
- [SSE with FastAPI](https://devdojo.com/bobbyiliev/how-to-use-server-sent-events-sse-with-fastapi)
- [watchdog Documentation](https://python-watchdog.readthedocs.io/)

### Deploy

- [Vercel Deployment Guide](https://vercel.com/docs)
- [Netlify React Deploy](https://www.netlify.com/with/react/)

---

## 8. CONCLUSIONI

### Perche' questo stack?

```
+------------------------------------------------------------------+
|                                                                  |
|   1. FAMILIARE: React e FastAPI li conosciamo gia'              |
|   2. MATURO: Ecosistema stabile, documentazione eccellente      |
|   3. VELOCE: Vite + SSE = feedback istantaneo                   |
|   4. SCALABILE: Da locale a produzione senza riscrivere         |
|   5. PRAGMATICO: MVP in 1-2 giorni, poi iteriamo                |
|                                                                  |
+------------------------------------------------------------------+
```

### Prossimi Passi

1. **Approvazione**: La Regina decide se procedere con questo stack
2. **Setup Progetto**: Creare struttura base
3. **MVP Sprint**: 2 giorni per prototipo funzionante
4. **Iterazione**: Aggiungere features basate su feedback

### Alternativa Minimalista

Se vogliamo qualcosa di ANCORA piu' semplice:

```
Solo Python + Streamlit

pip install streamlit
streamlit run dashboard.py
```

Pro: Una sola tecnologia, deployment istantaneo
Contro: Meno controllo, UX limitata

---

*"Prima la MAPPA, poi il VIAGGIO!"*

*"Fatto BENE > Fatto VELOCE"*

---

**Fonti Principali:**

- [FrontendTools - Framework Comparison 2025](https://www.frontendtools.tech/blog/best-frontend-frameworks-2025-comparison)
- [DEV Community - Frontend Frameworks 2025](https://dev.to/kouta222/the-next-big-things-in-frontend-svelte-astro-qwik-solid-2025-edition-2fnf)
- [Best of JS - Mermaid](https://bestofjs.org/projects/mermaid)
- [Synergy Codes - React Flow Guide](https://www.synergycodes.com/blog/react-flow-everything-you-need-to-know)
- [Ably - WebSockets vs SSE](https://ably.com/blog/websockets-vs-sse)
- [FreeCodeCamp - SSE vs WebSockets](https://www.freecodecamp.org/news/server-sent-events-vs-websockets/)
- [Strapi - React Markdown Guide](https://strapi.io/blog/react-markdown-complete-guide-security-styling)
- [CodeParrot - Vite + React 2025](https://codeparrot.ai/blogs/advanced-guide-to-using-vite-with-react-in-2025)
- [FastAPI - Static Files](https://fastapi.tiangolo.com/tutorial/static-files/)
- [Northflank - Vercel vs Netlify 2025](https://northflank.com/blog/vercel-vs-netlify-choosing-the-deployment-platform-in-2025)
