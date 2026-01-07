"""
Dashboard API CervellaSwarm

FastAPI backend per la Dashboard MAPPA che visualizza:
- IL NORD (obiettivo del progetto)
- LA FAMIGLIA (16 agenti e loro stato)
- LA ROADMAP (step del progetto)
- SESSIONE ATTIVA (task in corso)

PORTA DEDICATA: 8100 (Contabilita' usa 8000, NON toccare!)

Avvia con: uvicorn main:app --reload --host 0.0.0.0 --port 8100
Docs: http://localhost:8100/docs
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import mappa_router, tasks_router, workers_router, events_router

# ============ APP ============

app = FastAPI(
    title="CervellaSwarm Dashboard API",
    description="API per la Dashboard MAPPA di CervellaSwarm",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# ============ CORS ============

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",  # Altro dev server
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============ ROUTES ============

app.include_router(mappa_router)
app.include_router(tasks_router)
app.include_router(workers_router)
app.include_router(events_router)


# ============ ROOT ============

@app.get("/")
async def root():
    """Root endpoint con info API"""
    return {
        "name": "CervellaSwarm Dashboard API",
        "version": "1.0.0",
        "endpoints": {
            "mappa": "/api/mappa",
            "nord": "/api/nord",
            "roadmap": "/api/roadmap",
            "steps": "/api/steps",
            "tasks": "/api/tasks",
            "workers": "/api/workers",
            "events": "/api/events (SSE)"
        },
        "docs": "/docs"
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}


# ============ STARTUP ============

@app.on_event("startup")
async def startup_event():
    """Evento startup - inizializzazioni"""
    print("=" * 50)
    print("CervellaSwarm Dashboard API")
    print("=" * 50)
    print("Endpoints disponibili:")
    print("  - GET /api/mappa      -> Mappa completa")
    print("  - GET /api/tasks      -> Lista task")
    print("  - GET /api/workers    -> Stato worker")
    print("  - GET /api/events     -> SSE real-time")
    print("=" * 50)
    print("Docs: http://localhost:8100/docs")
    print("PORTA DEDICATA: 8100 (8000 = Contabilita')")
    print("=" * 50)
