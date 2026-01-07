"""
Route /api/mappa - Mappa completa del progetto
"""

from pathlib import Path
from datetime import datetime
from fastapi import APIRouter, HTTPException

from parsers.markdown import MarkdownParser
from models.schemas import (
    MappaResponse,
    ProjectInfo,
    NordInfo,
    RoadmapInfo,
    SessionInfo,
    StatoReale,
    Pezzo,
    CurrentPhase,
    CompletedPhase,
    Step,
    SubStep
)

router = APIRouter(prefix="/api", tags=["mappa"])

# Workspace path - configurabile
WORKSPACE = Path("/Users/rafapra/Developer/CervellaSwarm")


@router.get("/mappa", response_model=MappaResponse)
async def get_mappa():
    """
    Ritorna la mappa completa del progetto:
    - Info progetto
    - NORD (sessione, stato reale, pezzi)
    - Roadmap (fasi)
    - Steps con substeps
    """
    parser = MarkdownParser(WORKSPACE)

    # Parse tutti i componenti
    project_data = parser.get_project_info()
    nord_data = parser.parse_nord()
    roadmap_data = parser.parse_roadmap()
    mappa_data = parser.parse_mappa()

    # Costruisci response
    response = MappaResponse(
        version="1.0.0",
        updated_at=datetime.utcnow(),
        project=ProjectInfo(**project_data),
        nord=NordInfo(
            source_file=nord_data.get("source_file", "NORD.md"),
            current_session=SessionInfo(**nord_data["current_session"]) if nord_data.get("current_session") else None,
            stato_reale=[StatoReale(**s) for s in nord_data.get("stato_reale", [])],
            pezzi=[Pezzo(**p) for p in nord_data.get("pezzi", [])]
        ),
        roadmap=RoadmapInfo(
            source_file=roadmap_data.get("source_file", "ROADMAP_SACRA.md"),
            current_phase=CurrentPhase(**roadmap_data["current_phase"]) if roadmap_data.get("current_phase") else None,
            completed_phases=[CompletedPhase(**p) for p in roadmap_data.get("completed_phases", [])]
        ),
        steps=[
            Step(
                number=s["number"],
                name=s["name"],
                status=s["status"],
                substeps=[SubStep(**sub) for sub in s.get("substeps", [])]
            )
            for s in mappa_data.get("steps", [])
        ]
    )

    return response


@router.get("/nord")
async def get_nord():
    """Ritorna solo la sezione NORD"""
    parser = MarkdownParser(WORKSPACE)
    nord_data = parser.parse_nord()

    return {
        "source_file": nord_data.get("source_file", "NORD.md"),
        "current_session": nord_data.get("current_session"),
        "stato_reale": nord_data.get("stato_reale", []),
        "pezzi": nord_data.get("pezzi", [])
    }


@router.get("/roadmap")
async def get_roadmap():
    """Ritorna solo la sezione ROADMAP"""
    parser = MarkdownParser(WORKSPACE)
    roadmap_data = parser.parse_roadmap()

    return {
        "source_file": roadmap_data.get("source_file", "ROADMAP_SACRA.md"),
        "current_phase": roadmap_data.get("current_phase"),
        "completed_phases": roadmap_data.get("completed_phases", [])
    }


@router.get("/steps")
async def get_steps():
    """Ritorna lista step"""
    parser = MarkdownParser(WORKSPACE)
    mappa_data = parser.parse_mappa()

    return {
        "steps": mappa_data.get("steps", []),
        "count": len(mappa_data.get("steps", []))
    }


@router.get("/steps/{step_number}")
async def get_step(step_number: int):
    """Ritorna singolo step"""
    parser = MarkdownParser(WORKSPACE)
    mappa_data = parser.parse_mappa()

    for step in mappa_data.get("steps", []):
        if step["number"] == step_number:
            return step

    raise HTTPException(status_code=404, detail=f"Step {step_number} non trovato")
