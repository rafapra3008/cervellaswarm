# TASK: Dashboard Backend API

**Assegnato a:** cervella-backend
**Rischio:** 2-MEDIO
**Timeout:** 30 minuti
**Stato:** ready

---

## OBIETTIVO

Creare il backend FastAPI per la Dashboard MAPPA di CervellaSwarm.

---

## CONTESTO

Stiamo costruendo una Dashboard visuale per vedere:
- IL NORD (obiettivo del progetto)
- LA FAMIGLIA (16 agenti e loro stato)
- LA ROADMAP (step del progetto)
- SESSIONE ATTIVA (task in corso)

Tu crei il BACKEND. cervella-frontend crea il FRONTEND.

---

## COSA CREARE

### Struttura

```
/Users/rafapra/Developer/CervellaSwarm/dashboard/
+-- api/
    +-- main.py              # FastAPI app principale
    +-- routes/
    |   +-- __init__.py
    |   +-- mappa.py         # GET /api/mappa
    |   +-- tasks.py         # GET /api/tasks
    |   +-- workers.py       # GET /api/workers
    |   +-- events.py        # SSE /api/events
    +-- parsers/
    |   +-- __init__.py
    |   +-- markdown.py      # Parse .md -> JSON
    |   +-- tasks.py         # Parse task files
    +-- models/
    |   +-- __init__.py
    |   +-- schemas.py       # Pydantic models
    +-- requirements.txt
    +-- run.sh               # Script per avviare
```

### Endpoints

1. **GET /api/mappa**
   - Legge NORD.md, ROADMAP_SACRA.md, MAPPA_CERVELLASWARM_IDE.md
   - Ritorna JSON strutturato con:
     - project.name, project.claim, project.objective
     - nord.current_session, nord.stato_reale
     - steps[] con numero, nome, status, substeps[]

2. **GET /api/tasks**
   - Legge .swarm/tasks/*.md
   - Ritorna lista di task con:
     - task_id, status (ready/working/done)
     - assegnato_a, creato, timeout

3. **GET /api/workers**
   - Legge .swarm/status/ (se esiste) o inferisce da task
   - Ritorna lista worker con:
     - name, status (idle/active), current_task
     - heartbeat info (se disponibile)

4. **GET /api/events (SSE)**
   - Server-Sent Events per real-time
   - Usa watchdog per monitorare file changes
   - Eventi: file.changed, task.created, task.done

### Requirements.txt

```
fastapi>=0.109.0
uvicorn>=0.27.0
python-frontmatter>=1.0.0
watchdog>=3.0.0
pydantic>=2.0.0
```

### run.sh

```bash
#!/bin/bash
cd "$(dirname "$0")"
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

## STUDI DI RIFERIMENTO

Leggi questi file per dettagli architetturali:
- docs/studio/STUDIO_DASHBOARD_ARCH.md (schema JSON completo!)
- docs/studio/STUDIO_DASHBOARD_TECH.md (stack tecnico)

---

## OUTPUT

1. Tutti i file creati nella struttura sopra
2. Backend che parte con `./run.sh`
3. Endpoints funzionanti su http://localhost:8000
4. /docs funzionante (Swagger UI di FastAPI)

---

## NOTE

- CORS: Abilita per localhost:5173 (Vite dev server)
- Il parser markdown deve estrarre sezioni strutturate
- Per MVP: okay se parsing è semplificato, miglioriamo dopo
- Workspace: /Users/rafapra/Developer/CervellaSwarm/

---

*"Prima la MAPPA, poi il VIAGGIO"* - Tu costruisci le fondamenta!
