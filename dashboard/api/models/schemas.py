"""
Pydantic models per Dashboard API CervellaSwarm
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


# ============ MAPPA SCHEMAS ============

class ProjectInfo(BaseModel):
    """Info progetto"""
    name: str = "CervellaSwarm"
    claim: str = ""
    objective: str = "LIBERTA GEOGRAFICA"


class SessionInfo(BaseModel):
    """Info sessione attuale"""
    number: int = 0
    date: str = ""
    title: str = ""


class StatoReale(BaseModel):
    """Stato reale di un pezzo"""
    name: str
    status: str


class Pezzo(BaseModel):
    """Pezzo della mappa"""
    name: str
    status: str
    percent: int = 0


class CurrentPhase(BaseModel):
    """Fase corrente roadmap"""
    number: int
    name: str
    status: str


class CompletedPhase(BaseModel):
    """Fase completata"""
    number: int
    name: str
    completed_at: str


class SubStep(BaseModel):
    """Substep di uno step"""
    id: str
    name: str
    status: str  # pending, in_progress, completed


class Step(BaseModel):
    """Step della mappa"""
    number: int
    name: str
    status: str
    substeps: List[SubStep] = Field(default_factory=list)


class NordInfo(BaseModel):
    """Info NORD.md"""
    source_file: str = "NORD.md"
    current_session: Optional[SessionInfo] = None
    stato_reale: List[StatoReale] = Field(default_factory=list)
    pezzi: List[Pezzo] = Field(default_factory=list)


class RoadmapInfo(BaseModel):
    """Info ROADMAP"""
    source_file: str = "ROADMAP_SACRA.md"
    current_phase: Optional[CurrentPhase] = None
    completed_phases: List[CompletedPhase] = Field(default_factory=list)


class MappaResponse(BaseModel):
    """Response completa /api/mappa"""
    version: str = "1.0.0"
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    project: ProjectInfo = Field(default_factory=ProjectInfo)
    nord: NordInfo = Field(default_factory=NordInfo)
    roadmap: RoadmapInfo = Field(default_factory=RoadmapInfo)
    steps: List[Step] = Field(default_factory=list)


# ============ TASK SCHEMAS ============

class TaskAck(BaseModel):
    """Acknowledgment stato task"""
    received: bool = False
    understood: bool = False
    done: bool = False


class TaskMetadata(BaseModel):
    """Metadata task"""
    assegnato_a: str = ""
    rischio: int = 1
    timeout_minuti: int = 30
    creato: Optional[datetime] = None


class TaskFiles(BaseModel):
    """Files associati al task"""
    definition: str
    output: Optional[str] = None
    markers: List[str] = Field(default_factory=list)


class HeartbeatInfo(BaseModel):
    """Info heartbeat"""
    last_update: Optional[datetime] = None
    message: str = ""
    seconds_ago: int = 0


class TaskResponse(BaseModel):
    """Response singolo task"""
    task_id: str
    status: str  # ready, working, done
    ack: TaskAck = Field(default_factory=TaskAck)
    metadata: TaskMetadata = Field(default_factory=TaskMetadata)
    files: TaskFiles
    heartbeat: Optional[HeartbeatInfo] = None


class TaskListResponse(BaseModel):
    """Response lista task"""
    tasks: List[TaskResponse]
    count: int
    by_status: dict = Field(default_factory=dict)


# ============ WORKER SCHEMAS ============

class WorkerHeartbeat(BaseModel):
    """Heartbeat worker"""
    last_timestamp: int = 0
    last_message: str = ""
    time_ago: str = ""


class WorkerResponse(BaseModel):
    """Response singolo worker"""
    worker_name: str
    status: str  # idle, active
    current_task: Optional[str] = None
    pid: Optional[int] = None
    is_alive: bool = False
    heartbeat: Optional[WorkerHeartbeat] = None
    session_start: Optional[datetime] = None


class WorkerListResponse(BaseModel):
    """Response lista worker"""
    workers: List[WorkerResponse]
    active_count: int
    idle_count: int


# ============ EVENT SCHEMAS (SSE) ============

class SSEEvent(BaseModel):
    """Evento SSE"""
    event_type: str  # file.changed, task.created, task.done, worker.heartbeat
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    data: dict = Field(default_factory=dict)
