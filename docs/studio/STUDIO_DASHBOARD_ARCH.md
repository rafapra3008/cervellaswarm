# STUDIO ARCHITETTURA: Dashboard Visuale - Integrazione Regina

> **Data:** 6 Gennaio 2026
> **Autore:** cervella-ingegnera
> **Task:** TASK_STUDIO_DASHBOARD_ARCH

---

## EXECUTIVE SUMMARY

La dashboard deve essere un sistema VIVO che integra:
1. File markdown esistenti (NORD, ROADMAP, MAPPA)
2. Sistema task (.swarm/tasks/)
3. Worker e loro stato (heartbeat, PID)
4. La Regina (tramite API locale)

**Raccomandazione:** Architettura event-driven con FastAPI backend + WebSocket per real-time.

---

## 1. DIAGRAMMA ARCHITETTURA

```
+------------------------------------------------------------------+
|                           DASHBOARD WEB                          |
|                         (React/Next.js)                          |
+------------------------------------------------------------------+
           |                    |                    |
           | HTTP REST          | WebSocket          | Static
           | (CRUD ops)         | (Real-time)        | (Assets)
           v                    v                    v
+------------------------------------------------------------------+
|                        DASHBOARD API                              |
|                       (FastAPI + Python)                          |
|                                                                   |
|  +------------------+  +------------------+  +------------------+ |
|  | /api/mappa       |  | /api/tasks       |  | /api/workers     | |
|  | GET/PUT MAPPA    |  | GET/POST tasks   |  | GET status       | |
|  +------------------+  +------------------+  +------------------+ |
|                                                                   |
|  +------------------+  +------------------+  +------------------+ |
|  | /api/nord        |  | /api/roadmap     |  | /api/heartbeat   | |
|  | GET/PUT NORD     |  | GET/PUT roadmap  |  | WebSocket live   | |
|  +------------------+  +------------------+  +------------------+ |
+------------------------------------------------------------------+
           |                    |                    |
           v                    v                    v
+------------------------------------------------------------------+
|                     FILE SYSTEM + WATCHERS                       |
|                                                                   |
|  +----------------+  +------------------+  +------------------+   |
|  | .md FILES      |  | .swarm/tasks/    |  | .swarm/status/   |   |
|  | NORD.md        |  | TASK_*.md        |  | heartbeat_*.log  |   |
|  | ROADMAP*.md    |  | *.ready          |  | worker_*.task    |   |
|  | MAPPA*.md      |  | *.working        |  | worker_*.pid     |   |
|  +----------------+  | *.done           |  +------------------+   |
|                      +------------------+                         |
+------------------------------------------------------------------+
           |                    |                    |
           v                    v                    v
+------------------------------------------------------------------+
|                      FILE WATCHERS (fswatch)                     |
|                                                                   |
|  watch_md() ---------> on_md_change() --------> broadcast_ws()   |
|  watch_tasks() ------> on_task_change() ------> broadcast_ws()   |
|  watch_status() -----> on_status_change() ----> broadcast_ws()   |
+------------------------------------------------------------------+
```

---

## 2. DATA FLOW

### 2.1 Flusso Lettura (File -> Dashboard)

```
STEP 1: Avvio Dashboard
+------------------+
| Dashboard API    |  -> Legge tutti i .md
| startup()        |  -> Legge tutti i task
+------------------+  -> Legge tutti gli status
         |
         v
STEP 2: Parsing
+------------------+
| MarkdownParser   |  -> Estrae sezioni strutturate
| TaskParser       |  -> Converte in JSON
| StatusParser     |  -> Aggrega heartbeat/PID
+------------------+
         |
         v
STEP 3: Cache
+------------------+
| In-Memory Cache  |  -> Struttura JSON navigabile
| (Redis opzionale)|  -> Aggiornata da watchers
+------------------+
         |
         v
STEP 4: Serve
+------------------+
| REST API         |  -> Client richiede dati
| GET /api/mappa   |  -> Ritorna JSON strutturato
+------------------+
```

### 2.2 Flusso Aggiornamento (Dashboard -> File)

```
STEP 1: User Action
+------------------+
| Dashboard UI     |  -> Utente modifica campo
| "Sposta task"    |  -> Invia PATCH request
+------------------+
         |
         v
STEP 2: API Handler
+------------------+
| PATCH /api/tasks |  -> Valida request
| update_task()    |  -> Aggiorna file .md/.ready
+------------------+
         |
         v
STEP 3: File Update
+------------------+
| FileWriter       |  -> Scrive file atomicamente
| (atomic rename)  |  -> Trigger watcher
+------------------+
         |
         v
STEP 4: Broadcast
+------------------+
| WebSocket        |  -> Notifica tutti i client
| broadcast()      |  -> UI si aggiorna
+------------------+
```

### 2.3 Flusso Real-Time (Eventi -> Dashboard)

```
EVENTO: Worker crea file .done
         |
         v
+------------------+
| fswatch          |  -> Rileva nuovo file
| (o watchdog)     |
+------------------+
         |
         v
+------------------+
| FileWatcher      |  -> Identifica tipo evento
| on_file_event()  |  -> task_completed
+------------------+
         |
         v
+------------------+
| EventEmitter     |  -> Crea messaggio WS
| emit("task.done")|  -> {type, task_id, timestamp}
+------------------+
         |
         v
+------------------+
| WebSocket        |  -> Invia a tutti i client
| broadcast()      |  -> Dashboard si aggiorna
+------------------+
```

---

## 3. SCHEMA JSON PROPOSTO

### 3.1 MappaJSON - Struttura Completa

```json
{
  "version": "1.0.0",
  "updated_at": "2026-01-06T20:30:00Z",
  "project": {
    "name": "CervellaSwarm",
    "claim": "L'unico IDE che ti aiuta a PENSARE prima di SCRIVERE",
    "objective": "LIBERTA GEOGRAFICA"
  },
  "nord": {
    "source_file": "NORD.md",
    "current_session": {
      "number": 110,
      "date": "2026-01-06",
      "title": "IL CLAIM DELLA LIBERTA"
    },
    "stato_reale": [
      {"name": "16 Agents", "status": "FUNZIONANTE"},
      {"name": "spawn-workers v2.9.0", "status": "AUTO-SVEGLIA OVUNQUE!"}
    ],
    "pezzi": [
      {"name": "ANTI AUTO-COMPACT", "status": "PARCHEGGIATO", "percent": 70},
      {"name": "SISTEMA FEEDBACK", "status": "FATTO", "percent": 100},
      {"name": "ROADMAPS VISUALE", "status": "FATTO", "percent": 100},
      {"name": "TEMPLATE SWARM-INIT", "status": "FATTO", "percent": 100}
    ]
  },
  "roadmap": {
    "source_file": "ROADMAP_SACRA.md",
    "current_phase": {
      "number": 9,
      "name": "Apple Style",
      "status": "IN CORSO"
    },
    "completed_phases": [
      {"number": 0, "name": "Setup Progetto", "completed_at": "2025-12-30"},
      {"number": 8, "name": "La Corte Reale", "completed_at": "2026-01-01"}
    ]
  },
  "steps": [
    {
      "number": 0,
      "name": "Solidificare la Base",
      "status": "in_progress",
      "substeps": [
        {"id": "0.1", "name": "Documentare TUTTO", "status": "pending"},
        {"id": "0.2", "name": "Completare swarm-global-status", "status": "in_progress"},
        {"id": "0.3", "name": "Testare watcher fixato", "status": "pending"}
      ]
    },
    {
      "number": 1,
      "name": "Definire l'Esperienza Utente",
      "status": "pending",
      "substeps": []
    }
  ],
  "studi": {
    "completati": [
      {
        "name": "Architettura IDE",
        "file": "docs/studio/STUDIO_ARCHITETTURA_IDE.md",
        "lines": 345,
        "focus": "Come costruire tecnicamente"
      }
    ],
    "da_fare": [
      {
        "name": "UX Journey Cliente",
        "assignee": "cervella-marketing",
        "focus": "Mappare ogni touchpoint"
      }
    ]
  }
}
```

### 3.2 TaskJSON - Singolo Task

```json
{
  "task_id": "TASK_STUDIO_DASHBOARD_ARCH",
  "status": "working",
  "ack": {
    "received": true,
    "understood": true,
    "done": false
  },
  "metadata": {
    "assegnato_a": "cervella-ingegnera",
    "rischio": 2,
    "timeout_minuti": 15,
    "creato": "2026-01-06T20:10:00Z"
  },
  "files": {
    "definition": ".swarm/tasks/TASK_STUDIO_DASHBOARD_ARCH.md",
    "output": null,
    "markers": [".working"]
  },
  "heartbeat": {
    "last_update": "2026-01-06T20:25:00Z",
    "message": "Scrivendo STUDIO_DASHBOARD_ARCH.md",
    "seconds_ago": 30
  }
}
```

### 3.3 WorkerJSON - Stato Worker

```json
{
  "worker_name": "ingegnera",
  "status": "active",
  "current_task": "TASK_STUDIO_DASHBOARD_ARCH",
  "pid": 12345,
  "is_alive": true,
  "heartbeat": {
    "last_timestamp": 1736192700,
    "last_message": "Scrivendo STUDIO_DASHBOARD_ARCH.md",
    "time_ago": "30s fa"
  },
  "session_start": "2026-01-06T20:10:00Z"
}
```

### 3.4 GlobalStatusJSON (Multi-Progetto)

```json
{
  "timestamp": "2026-01-06T20:30:00Z",
  "projects": [
    {
      "name": "CervellaSwarm",
      "path": "~/Developer/CervellaSwarm",
      "exists": true,
      "tasks": {
        "ready": 5,
        "working": 1,
        "done": 0
      },
      "workers": [
        {
          "name": "ingegnera",
          "task": "TASK_STUDIO_DASHBOARD_ARCH",
          "alive": true,
          "heartbeat": "30s fa"
        }
      ],
      "last_heartbeat": "30s fa"
    }
  ],
  "totals": {
    "ready": 5,
    "working": 1,
    "done": 0,
    "workers_active": 1
  }
}
```

---

## 4. API ENDPOINTS NECESSARI

### 4.1 MAPPA & Documenti

| Metodo | Endpoint | Descrizione |
|--------|----------|-------------|
| GET | `/api/mappa` | Ritorna MappaJSON completa |
| GET | `/api/nord` | Ritorna sezione NORD |
| GET | `/api/roadmap` | Ritorna sezione ROADMAP |
| GET | `/api/steps` | Ritorna lista step |
| GET | `/api/steps/{n}` | Ritorna step specifico |
| PATCH | `/api/steps/{n}/substeps/{id}` | Aggiorna stato substep |

### 4.2 Tasks

| Metodo | Endpoint | Descrizione |
|--------|----------|-------------|
| GET | `/api/tasks` | Lista tutti i task |
| GET | `/api/tasks/{id}` | Dettaglio task |
| POST | `/api/tasks` | Crea nuovo task |
| PATCH | `/api/tasks/{id}` | Aggiorna task (status, etc.) |
| DELETE | `/api/tasks/{id}` | Cancella task |
| POST | `/api/tasks/{id}/ready` | Marca come ready |
| POST | `/api/tasks/{id}/working` | Marca come working |
| POST | `/api/tasks/{id}/done` | Marca come done |

### 4.3 Workers & Status

| Metodo | Endpoint | Descrizione |
|--------|----------|-------------|
| GET | `/api/workers` | Lista worker attivi |
| GET | `/api/workers/{name}` | Dettaglio worker |
| GET | `/api/heartbeat` | WebSocket per eventi live |
| GET | `/api/global-status` | Status multi-progetto |

### 4.4 WebSocket Events

| Evento | Payload | Quando |
|--------|---------|--------|
| `task.created` | TaskJSON | Nuovo task creato |
| `task.ready` | {task_id} | Task marcato ready |
| `task.working` | {task_id, worker} | Worker ha preso task |
| `task.done` | {task_id, output_file} | Task completato |
| `worker.heartbeat` | WorkerJSON | Heartbeat ricevuto |
| `worker.started` | {worker_name, pid} | Worker avviato |
| `worker.stopped` | {worker_name} | Worker terminato |
| `file.changed` | {file_path, type} | File .md modificato |

---

## 5. SINCRONIZZAZIONE

### 5.1 Strategia: One-Way vs Two-Way

```
+------------------------------------------------------------------+
|                                                                  |
|   RACCOMANDAZIONE: ONE-WAY SYNC (File -> Dashboard)              |
|                                                                  |
|   PERCHE?                                                         |
|   1. I file .md sono "source of truth"                           |
|   2. La Regina e i worker scrivono direttamente nei file         |
|   3. Two-way sync e' complesso e causa conflitti                 |
|                                                                   |
|   ECCEZIONE: Task status                                          |
|   - Dashboard puo' creare/modificare task                        |
|   - Ma scrive DIRETTAMENTE nei file (non in cache)               |
|   - I file restano source of truth                               |
|                                                                   |
+------------------------------------------------------------------+
```

### 5.2 Conflict Resolution

Se file cambia mentre dashboard modifica:

1. **Detect**: Watcher rileva cambio esterno
2. **Compare**: Confronta timestamp
3. **Strategy**:
   - Se cambio esterno piu' recente -> ricarica da file
   - Se cambio dashboard piu' recente -> scrivi file (overwrite)
   - Se contemporaneo -> notifica utente, chiedi scelta

### 5.3 Caching

```python
class MappaCache:
    def __init__(self):
        self.data: dict = {}
        self.last_modified: dict = {}  # file -> timestamp

    def get(self, file_path: str) -> dict:
        current_mtime = os.path.getmtime(file_path)
        if file_path not in self.last_modified or \
           current_mtime > self.last_modified[file_path]:
            self.reload(file_path)
        return self.data.get(file_path)

    def reload(self, file_path: str):
        content = Path(file_path).read_text()
        self.data[file_path] = parse_markdown(content)
        self.last_modified[file_path] = os.path.getmtime(file_path)
```

---

## 6. INTEGRAZIONE WORKER E REGINA

### 6.1 Worker Monitoring

```python
class WorkerMonitor:
    """Monitora tutti i worker attivi"""

    def __init__(self, status_dir: Path):
        self.status_dir = status_dir

    def get_active_workers(self) -> List[WorkerStatus]:
        workers = []
        for task_file in self.status_dir.glob("worker_*.task"):
            worker_name = task_file.stem.replace("worker_", "")
            workers.append(self._get_worker_status(worker_name))
        return workers

    def _get_worker_status(self, name: str) -> WorkerStatus:
        task_id = self._read_task(name)
        pid = self._read_pid(name)
        heartbeat = self._read_heartbeat(name)

        return WorkerStatus(
            name=name,
            task_id=task_id,
            pid=pid,
            is_alive=self._is_process_alive(pid),
            heartbeat=heartbeat
        )

    def _is_process_alive(self, pid: int) -> bool:
        try:
            os.kill(pid, 0)
            return True
        except (OSError, ProcessLookupError):
            return False
```

### 6.2 Integrazione Regina (Claude API Interna)

```
+------------------------------------------------------------------+
|                                                                  |
|   NOTA: La Regina e' un processo Claude Code separato            |
|                                                                  |
|   OPZIONI INTEGRAZIONE:                                          |
|                                                                   |
|   A) File-based (RACCOMANDATO per MVP)                           |
|      - Regina scrive in .swarm/handoff/                          |
|      - Dashboard legge/scrive nello stesso folder                |
|      - Semplice, funziona subito                                 |
|                                                                   |
|   B) Hook-based (Futuro)                                         |
|      - Hook invia eventi a Dashboard API                         |
|      - Richiede modifiche agli hooks esistenti                   |
|                                                                   |
|   C) MCP Server (Avanzato)                                       |
|      - Dashboard espone MCP server                               |
|      - Regina usa tool dedicati                                  |
|      - Massima integrazione                                       |
|                                                                   |
+------------------------------------------------------------------+
```

### 6.3 Checkpoint Notifications

Quando Regina fa checkpoint:

1. **Hook SessionEnd**: Scrive in `.swarm/events/checkpoint_{timestamp}.json`
2. **Watcher Dashboard**: Rileva nuovo file
3. **Dashboard**: Notifica UI "Checkpoint salvato!"
4. **UI**: Aggiorna tutti i dati dalla nuova versione file

```json
// .swarm/events/checkpoint_20260106_203000.json
{
  "type": "checkpoint",
  "timestamp": "2026-01-06T20:30:00Z",
  "session": 110,
  "files_updated": [
    "NORD.md",
    "PROMPT_RIPRESA.md",
    "ROADMAP_SACRA.md"
  ],
  "git_commit": "abc123"
}
```

---

## 7. MVP: ARCHITETTURA MINIMA

### 7.1 Cosa Serve per Prototipo (1-2 giorni)

```
BACKEND (FastAPI):
[x] Server FastAPI base
[x] GET /api/mappa - Legge e parsa NORD.md + MAPPA*.md
[x] GET /api/tasks - Legge .swarm/tasks/
[x] GET /api/workers - Legge .swarm/status/
[x] WebSocket /api/heartbeat - Broadcast eventi
[x] FileWatcher con watchdog

FRONTEND (qualsiasi):
[x] Pagina unica con sezioni
[x] Fetch iniziale dati
[x] WebSocket per aggiornamenti
[x] Visualizzazione step/substep con checkbox
[x] Lista task con colori per stato
[x] Lista worker con heartbeat

OPZIONALE:
[ ] Autenticazione (non serve per MVP locale)
[ ] PATCH endpoints (solo read per MVP)
[ ] Two-way sync (solo one-way per MVP)
```

### 7.2 Stack Consigliato MVP

| Componente | Tecnologia | Motivo |
|------------|------------|--------|
| Backend | FastAPI (Python) | Gia' usato in task_manager.py |
| File Watching | watchdog (Python) | Cross-platform, asincrono |
| WebSocket | FastAPI WebSocket | Integrato |
| Frontend | React + Tailwind | O anche solo HTML + Alpine.js |
| Markdown Parser | python-markdown + frontmatter | Parsing .md strutturato |

### 7.3 Struttura Files MVP

```
dashboard/
+-- api/
|   +-- main.py              # FastAPI app
|   +-- routes/
|   |   +-- mappa.py         # GET /api/mappa
|   |   +-- tasks.py         # GET /api/tasks
|   |   +-- workers.py       # GET /api/workers
|   |   +-- websocket.py     # WebSocket handler
|   +-- parsers/
|   |   +-- markdown.py      # Parse .md to JSON
|   |   +-- tasks.py         # Parse task files
|   |   +-- status.py        # Parse worker status
|   +-- watchers/
|   |   +-- file_watcher.py  # watchdog integration
|   +-- models/
|       +-- schemas.py       # Pydantic models
|
+-- frontend/
|   +-- index.html
|   +-- app.js
|   +-- styles.css
|
+-- requirements.txt
+-- run.sh                   # Avvia tutto
```

---

## 8. SICUREZZA (Base)

### 8.1 Per MVP (Locale)

```
+------------------------------------------------------------------+
|                                                                  |
|   MVP = SOLO LOCALE                                               |
|                                                                   |
|   - Server su localhost:8000                                     |
|   - Niente autenticazione                                        |
|   - Niente HTTPS                                                  |
|   - Niente rate limiting                                          |
|                                                                   |
|   SUFFICIENTE per prototipo su macchina locale!                  |
|                                                                   |
+------------------------------------------------------------------+
```

### 8.2 Per Produzione (Futuro)

| Aspetto | Soluzione |
|---------|-----------|
| Autenticazione | JWT tokens, OAuth |
| HTTPS | Let's Encrypt, nginx reverse proxy |
| Rate Limiting | FastAPI middleware |
| Input Validation | Pydantic strict mode |
| Path Traversal | Validate task_id (gia' in task_manager.py) |
| Multi-tenant | Separate database/files per utente |

### 8.3 Multi-Utente (Futuro Lontano)

```
SCENARIO: Dashboard SaaS per clienti CervellaSwarm IDE

ARCHITETTURA:
- Ogni cliente ha workspace isolato
- File salvati in /workspaces/{client_id}/
- Database separato per ogni cliente
- Auth con team/org support

NON NECESSARIO per MVP!
```

---

## 9. RISCHI E MITIGAZIONI

| Rischio | Probabilita | Impatto | Mitigazione |
|---------|-------------|---------|-------------|
| Race condition file | Media | Alto | Atomic writes, lock files |
| Parser fallisce su .md malformato | Media | Medio | Try/except, fallback a raw text |
| Worker crash non rilevato | Bassa | Medio | Timeout heartbeat, PID check |
| Performance con molti file | Bassa | Basso | Caching aggressivo |
| WebSocket disconnection | Media | Basso | Auto-reconnect client-side |

---

## 10. CONCLUSIONI

### Raccomandazione Finale

```
+------------------------------------------------------------------+
|                                                                  |
|   PER IL MVP:                                                     |
|                                                                   |
|   1. Backend FastAPI con 3 endpoint READ-ONLY                    |
|   2. WebSocket per real-time                                     |
|   3. File watcher con watchdog                                   |
|   4. Frontend semplice (anche solo HTML + fetch)                 |
|   5. One-way sync (file -> dashboard)                            |
|                                                                   |
|   DOPO MVP:                                                       |
|   - Aggiungere PATCH per modifiche                               |
|   - Integrazione hook per eventi Regina                          |
|   - UI piu' sofisticata con drag & drop                          |
|                                                                   |
+------------------------------------------------------------------+
```

### Dipendenze da Altri Studi

| Questo Studio | Dipende Da | Per |
|---------------|------------|-----|
| STUDIO_DASHBOARD_ARCH | STUDIO_DASHBOARD_TECH | Framework frontend |
| STUDIO_DASHBOARD_ARCH | STUDIO_DASHBOARD_UX | Wireframe UI |

### Prossimi Step

1. Attendere STUDIO_DASHBOARD_TECH (tecnologie frontend)
2. Attendere STUDIO_DASHBOARD_UX (wireframe)
3. Combinare i 3 studi in decisione finale
4. Implementare MVP con cervella-backend + cervella-frontend

---

## FIRMA

```
+------------------------------------------------------------------+
|                                                                  |
|   "Il sistema deve essere REALE, non su carta!"                  |
|                                                                   |
|   Analizzato da cervella-ingegnera                               |
|   6 Gennaio 2026                                                  |
|                                                                   |
+------------------------------------------------------------------+
```

---

*"Prima la MAPPA, poi il VIAGGIO"*

*Cervella & Rafa*
