"""
Route /api/workers - Stato worker swarm
"""

from pathlib import Path
from fastapi import APIRouter, HTTPException

from parsers.tasks import WorkerParser
from models.schemas import WorkerListResponse

router = APIRouter(prefix="/api", tags=["workers"])

# Workspace path - configurabile
WORKSPACE = Path("/Users/rafapra/Developer/CervellaSwarm")


@router.get("/workers", response_model=WorkerListResponse)
async def get_workers():
    """
    Ritorna lista worker:
    - worker_name, status (idle/active)
    - current_task, pid, is_alive
    - heartbeat info
    """
    parser = WorkerParser(WORKSPACE)

    all_workers = parser.get_all_workers()

    active_count = sum(1 for w in all_workers if w.get("status") == "active")
    idle_count = len(all_workers) - active_count

    return WorkerListResponse(
        workers=all_workers,
        active_count=active_count,
        idle_count=idle_count
    )


@router.get("/workers/{worker_name}")
async def get_worker(worker_name: str):
    """Ritorna stato singolo worker"""
    parser = WorkerParser(WORKSPACE)

    all_workers = parser.get_all_workers()

    for worker in all_workers:
        if worker["worker_name"] == worker_name:
            return worker

    raise HTTPException(status_code=404, detail=f"Worker {worker_name} non trovato")
