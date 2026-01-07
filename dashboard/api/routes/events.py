"""
Route /api/events - Server-Sent Events per real-time updates
"""

import asyncio
import json
from pathlib import Path
from datetime import datetime
from typing import AsyncGenerator

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

router = APIRouter(prefix="/api", tags=["events"])

# Workspace path - configurabile
WORKSPACE = Path("/Users/rafapra/Developer/CervellaSwarm")

# Cache per rilevare cambiamenti
_file_mtimes: dict = {}


async def check_for_changes() -> dict | None:
    """Controlla se ci sono cambiamenti nei file monitorati"""
    global _file_mtimes

    changes = []

    # Files da monitorare
    monitored_files = [
        WORKSPACE / "NORD.md",
        WORKSPACE / "ROADMAP_SACRA.md",
        WORKSPACE / "PROMPT_RIPRESA.md",
    ]

    # Aggiungi file in .swarm/tasks/
    tasks_dir = WORKSPACE / ".swarm" / "tasks"
    if tasks_dir.exists():
        monitored_files.extend(tasks_dir.glob("*.md"))
        monitored_files.extend(tasks_dir.glob("*.ready"))
        monitored_files.extend(tasks_dir.glob("*.working"))
        monitored_files.extend(tasks_dir.glob("*.done"))

    # Aggiungi file in .swarm/status/
    status_dir = WORKSPACE / ".swarm" / "status"
    if status_dir.exists():
        monitored_files.extend(status_dir.glob("*.log"))
        monitored_files.extend(status_dir.glob("*.task"))

    for file_path in monitored_files:
        if not file_path.exists():
            continue

        try:
            mtime = file_path.stat().st_mtime
            file_key = str(file_path)

            if file_key not in _file_mtimes:
                _file_mtimes[file_key] = mtime
            elif mtime > _file_mtimes[file_key]:
                _file_mtimes[file_key] = mtime

                # Determina tipo evento
                event_type = "file.changed"
                if ".swarm/tasks/" in file_key:
                    if file_key.endswith(".ready"):
                        event_type = "task.ready"
                    elif file_key.endswith(".working"):
                        event_type = "task.working"
                    elif file_key.endswith(".done"):
                        event_type = "task.done"
                    else:
                        event_type = "task.updated"
                elif ".swarm/status/" in file_key:
                    if "heartbeat" in file_key:
                        event_type = "worker.heartbeat"
                    else:
                        event_type = "worker.status"

                changes.append({
                    "event_type": event_type,
                    "file_path": file_key,
                    "timestamp": datetime.utcnow().isoformat()
                })
        except Exception:
            continue

    if changes:
        return {"changes": changes}
    return None


async def event_generator() -> AsyncGenerator[str, None]:
    """Genera eventi SSE"""
    # Invia evento iniziale di connessione
    yield f"event: connected\ndata: {json.dumps({'status': 'connected', 'timestamp': datetime.utcnow().isoformat()})}\n\n"

    while True:
        changes = await check_for_changes()
        if changes:
            yield f"event: update\ndata: {json.dumps(changes)}\n\n"

        # Heartbeat ogni 30 secondi per mantenere connessione
        yield f"event: heartbeat\ndata: {json.dumps({'timestamp': datetime.utcnow().isoformat()})}\n\n"

        await asyncio.sleep(2)  # Poll ogni 2 secondi


@router.get("/events")
async def events():
    """
    Server-Sent Events endpoint per real-time updates.

    Eventi:
    - connected: Connessione stabilita
    - update: Cambiamenti rilevati (file.changed, task.*, worker.*)
    - heartbeat: Keep-alive ogni 30s
    """
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # Disabilita buffering nginx
        }
    )
