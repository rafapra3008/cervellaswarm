# SUB-ROADMAP: FASE 0 - Dashboard MAPPA

> **"Prima la MAPPA, poi il VIAGGIO"**
>
> **Creata:** 7 Gennaio 2026 - Sessione 112
> **Obiettivo:** Dashboard visuale per USO NOSTRO
> **Timeline:** 2-4 settimane

---

## PERCHE' QUESTA FASE

```
+------------------------------------------------------------------+
|                                                                  |
|   NON stiamo costruendo un prodotto da vendere.                 |
|   Stiamo costruendo uno STRUMENTO per NOI.                      |
|                                                                  |
|   La Dashboard MAPPA ci serve per:                              |
|   1. Vedere lo sciame in azione (VISIVAMENTE!)                  |
|   2. Navigare i nostri progetti con la MAPPA                    |
|   3. Validare se il concetto VISUAL funziona                    |
|   4. Avere un "proof of concept" da mostrare                    |
|                                                                  |
|   Se funziona per noi, funziona per TUTTI.                      |
|                                                                  |
+------------------------------------------------------------------+
```

---

## STACK TECNICO (dagli studi)

| Componente | Tecnologia | Motivo |
|------------|------------|--------|
| **Backend** | FastAPI (Python) | Gia' lo conosciamo! |
| **Real-time** | SSE (Server-Sent Events) | Piu' semplice di WebSocket |
| **File Watcher** | watchdog (Python) | Cross-platform |
| **Frontend** | React + Vite + TypeScript | Veloce, moderno |
| **Styling** | TailwindCSS | Sviluppo rapido |
| **Markdown** | react-markdown | Per renderizzare .md |

---

## GLI STEP

### STEP 0.1: Backend API Base
**Assegnato a:** cervella-backend
**Stato:** [ ] Da fare

```
Creare:
dashboard/
+-- api/
    +-- main.py              # FastAPI app
    +-- routes/
    |   +-- mappa.py         # GET /api/mappa
    |   +-- tasks.py         # GET /api/tasks
    |   +-- workers.py       # GET /api/workers
    |   +-- events.py        # SSE /api/events
    +-- parsers/
    |   +-- markdown.py      # Parse .md -> JSON
    |   +-- tasks.py         # Parse task files
    +-- watchers/
    |   +-- file_watcher.py  # watchdog setup
    +-- requirements.txt
```

**Endpoints MVP:**
- `GET /api/mappa` → Ritorna NORD + ROADMAP + Steps in JSON
- `GET /api/tasks` → Lista task da .swarm/tasks/
- `GET /api/workers` → Stato worker attivi
- `GET /api/events` → SSE per aggiornamenti real-time

**Output:** Backend funzionante su localhost:8000

---

### STEP 0.2: Frontend Base + Layout
**Assegnato a:** cervella-frontend
**Stato:** [ ] Da fare

```
Creare:
dashboard/
+-- frontend/
    +-- src/
    |   +-- App.tsx
    |   +-- components/
    |   |   +-- Layout.tsx       # Layout principale
    |   |   +-- Header.tsx       # Header con titolo
    |   +-- hooks/
    |   |   +-- useSSE.ts        # Hook per SSE
    |   |   +-- useApi.ts        # Hook per fetch
    |   +-- types/
    |       +-- index.ts         # TypeScript types
    +-- package.json
    +-- vite.config.ts
    +-- tailwind.config.js
```

**Output:** App React base che si connette al backend

---

### STEP 0.3: Widget NORD
**Assegnato a:** cervella-frontend
**Dipende da:** 0.1, 0.2

```
Componente NordWidget:
- Mostra obiettivo finale (da NORD.md)
- Progress bar generale
- Sessione attuale
- Espandibile per dettagli
```

**Wireframe:**
```
+----------------------------------+
|           IL NORD                |
|  +----------------------------+  |
|  |   LIBERTA' GEOGRAFICA      |  |
|  |   Progress: ====----  40%  |  |
|  +----------------------------+  |
|  Sessione: 112                   |
+----------------------------------+
```

---

### STEP 0.4: Widget FAMIGLIA
**Assegnato a:** cervella-frontend
**Dipende da:** 0.1, 0.2

```
Componente FamigliaWidget:
- Mostra i 16 agenti
- Stato: idle/working/done
- Icone colorate per tipo
- Hover per dettagli
```

**Wireframe:**
```
+----------------------------------+
|        LA FAMIGLIA               |
|  Regina  [idle]                  |
|  Guardiane: [G1] [G2] [G3]      |
|  Worker:                         |
|  [FE]  [BE]  [TS]  [RV]         |
|  idle  WORK  idle  idle          |
|  2 attivi | 14 idle              |
+----------------------------------+
```

---

### STEP 0.5: Widget ROADMAP
**Assegnato a:** cervella-frontend
**Dipende da:** 0.1, 0.2

```
Componente RoadmapWidget:
- Timeline orizzontale degli STEP
- Progress bar per ogni step
- Click per espandere substep
- Indicatore "SEI QUI"
```

**Wireframe:**
```
STEP 0        STEP 1        STEP 2        NORD
[====>        [===>          [              [*]
 90%]           35%]           0%]
   |             |              |             |
+------+     +------+      +------+      +------+
|0.1 OK|     |1.1   |      |2.1   |      |  *   |
|0.2 OK|     |1.2 WK|      |2.2   |      | FOTO |
+------+     +------+      +------+      +------+
```

---

### STEP 0.6: Widget SESSIONE
**Assegnato a:** cervella-frontend
**Dipende da:** 0.1, 0.2

```
Componente SessioneWidget:
- Task attualmente in corso
- Worker che sta lavorando
- Timer tempo trascorso
- Log live (ultimi messaggi)
```

**Wireframe:**
```
+----------------------------------+
|      SESSIONE ATTIVA             |
|  Task: "Studio Dashboard"        |
|  Worker: cervella-backend        |
|  Tempo: 12m 34s                  |
|  Log:                            |
|  > Creando API...                |
|  > Setup routes...               |
|  [Vedi Log] [Ferma]              |
+----------------------------------+
```

---

### STEP 0.7: Real-time con SSE
**Assegnato a:** cervella-backend + cervella-frontend
**Dipende da:** 0.1-0.6

```
Backend:
- File watcher rileva modifiche
- Emette eventi SSE

Frontend:
- useSSE hook ascolta eventi
- Aggiorna UI automaticamente

Eventi:
- task.created
- task.working
- task.done
- worker.heartbeat
- file.changed
```

---

### STEP 0.8: Integrazione e Test
**Assegnato a:** cervella-tester
**Dipende da:** 0.1-0.7

```
Test:
- [ ] Backend risponde correttamente
- [ ] Frontend mostra dati
- [ ] SSE funziona (modifico file, UI si aggiorna)
- [ ] Tutti i widget renderizzano
- [ ] Performance accettabile
```

---

## DIPENDENZE

```
0.1 Backend ─────────────────────────────────────┐
                                                  │
0.2 Frontend Base ───────────────────────────────┤
                                                  │
     ┌────────────────────────────────────────────┘
     │
     ├──> 0.3 Widget NORD
     │
     ├──> 0.4 Widget FAMIGLIA
     │
     ├──> 0.5 Widget ROADMAP
     │
     ├──> 0.6 Widget SESSIONE
     │
     └──> 0.7 Real-time SSE
                │
                v
          0.8 Test
```

---

## CHI FA COSA

| Step | Worker | Dipendenze |
|------|--------|------------|
| 0.1 Backend | cervella-backend | - |
| 0.2 Frontend Base | cervella-frontend | - |
| 0.3 Widget NORD | cervella-frontend | 0.1, 0.2 |
| 0.4 Widget FAMIGLIA | cervella-frontend | 0.1, 0.2 |
| 0.5 Widget ROADMAP | cervella-frontend | 0.1, 0.2 |
| 0.6 Widget SESSIONE | cervella-frontend | 0.1, 0.2 |
| 0.7 Real-time SSE | backend + frontend | 0.1-0.6 |
| 0.8 Test | cervella-tester | 0.1-0.7 |

---

## ORDINE DI ESECUZIONE

```
PARALLELO (Fase 1):
├── cervella-backend  → 0.1 Backend API
└── cervella-frontend → 0.2 Frontend Base

SEQUENZIALE (Fase 2 - dopo che 0.1 e 0.2 sono pronti):
├── cervella-frontend → 0.3 NORD
├── cervella-frontend → 0.4 FAMIGLIA
├── cervella-frontend → 0.5 ROADMAP
└── cervella-frontend → 0.6 SESSIONE

INTEGRAZIONE (Fase 3):
├── cervella-backend + frontend → 0.7 SSE
└── cervella-tester → 0.8 Test
```

---

## OUTPUT FINALE

```
+------------------------------------------------------------------+
|  CERVELLASWARM DASHBOARD                         [Rafa] [?] [x]  |
+------------------------------------------------------------------+
|                                                                  |
|  +------------------------+  +-------------------------------+   |
|  |       IL NORD          |  |        LA FAMIGLIA            |   |
|  |  LIBERTA' GEOGRAFICA   |  |  Regina [idle]                |   |
|  |  Progress: ====  40%   |  |  [FE] [BE] [TS] [RV]         |   |
|  +------------------------+  |  2 attivi | 14 idle           |   |
|                              +-------------------------------+   |
|                                                                  |
|  +------------------------------------------------------------+  |
|  |                    LA ROADMAP                               |  |
|  |  [STEP 0]----[STEP 1]----[STEP 2]----[STEP 3]----[NORD]   |  |
|  |     90%         20%         0%          0%                  |  |
|  +------------------------------------------------------------+  |
|                                                                  |
|  +------------------------------------------------------------+  |
|  |                    SESSIONE ATTIVA                          |  |
|  |  Task: "Dashboard MVP" | Worker: backend | 12m 34s          |  |
|  +------------------------------------------------------------+  |
|                                                                  |
+------------------------------------------------------------------+
```

---

## CRITERI DI SUCCESSO

```
[ ] Posso vedere il NORD del progetto
[ ] Posso vedere i 16 membri della famiglia e il loro stato
[ ] Posso vedere la ROADMAP con gli step
[ ] Posso vedere i task attivi in tempo reale
[ ] Quando un file cambia, la UI si aggiorna
[ ] È utile per ME (Rafa) per capire dove siamo
```

---

*"Prima la MAPPA, poi il VIAGGIO"*

*La Dashboard MAPPA sarà il nostro GPS.*

Cervella & Rafa 💙

---

**Versione:** 1.0.0
**Creata:** 7 Gennaio 2026 - Sessione 112
