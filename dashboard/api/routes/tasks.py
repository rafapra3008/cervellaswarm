"""
Route /api/tasks - Gestione task swarm
"""

from pathlib import Path
from fastapi import APIRouter, HTTPException

from parsers.tasks import TaskParser
from models.schemas import TaskListResponse, TaskResponse

router = APIRouter(prefix="/api", tags=["tasks"])

# Workspace path - configurabile
WORKSPACE = Path("/Users/rafapra/Developer/CervellaSwarm")


@router.get("/tasks", response_model=TaskListResponse)
async def get_tasks():
    """
    Ritorna lista di tutti i task:
    - task_id, status, metadata
    - Raggruppati per status
    """
    parser = TaskParser(WORKSPACE)

    all_tasks = parser.get_all_tasks()
    by_status = parser.get_tasks_by_status()

    return TaskListResponse(
        tasks=all_tasks,
        count=len(all_tasks),
        by_status={
            "ready": len(by_status.get("ready", [])),
            "working": len(by_status.get("working", [])),
            "done": len(by_status.get("done", []))
        }
    )


@router.get("/tasks/{task_id}")
async def get_task(task_id: str):
    """Ritorna singolo task per ID"""
    parser = TaskParser(WORKSPACE)

    task = parser.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task {task_id} non trovato")

    return task


@router.get("/tasks/status/{status}")
async def get_tasks_by_status(status: str):
    """Ritorna task filtrati per status (ready, working, done)"""
    if status not in ["ready", "working", "done", "pending"]:
        raise HTTPException(status_code=400, detail=f"Status non valido: {status}")

    parser = TaskParser(WORKSPACE)
    by_status = parser.get_tasks_by_status()

    return {
        "status": status,
        "tasks": by_status.get(status, []),
        "count": len(by_status.get(status, []))
    }
