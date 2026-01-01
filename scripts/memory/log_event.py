#!/usr/bin/env python3
"""
Sistema Memoria CervellaSwarm - Log Eventi

Riceve payload da hook PostToolUse e logga eventi nel database.
Gestisce errori gracefully per non bloccare mai il workflow.
"""

__version__ = "1.1.0"
__version_date__ = "2026-01-01"  # Fix: cerca agent in subagent_type + tutti i 14 agent

import json
import sqlite3
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path


def get_db_path() -> Path:
    """Ritorna il path del database."""
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent
    return project_root / "data" / "swarm_memory.db"


def extract_agent_info(payload: dict) -> dict:
    """Estrae informazioni sull'agent dal payload."""
    tool = payload.get("tool", {})
    tool_name = tool.get("name", "")
    tool_input = tool.get("input", {})

    # L'agent è in subagent_type (per Task tool) o nel nome del tool
    subagent_type = tool_input.get("subagent_type", "")
    agent_source = subagent_type if subagent_type else tool_name

    # Mapping COMPLETO di tutti i 14 agent (11 worker + 3 guardiane)
    agent_map = {
        # Worker (Sonnet)
        "cervella-frontend": "Frontend Specialist",
        "cervella-backend": "Backend Specialist",
        "cervella-tester": "Quality Assurance",
        "cervella-reviewer": "Code Reviewer",
        "cervella-researcher": "Research Specialist",
        "cervella-marketing": "Marketing Specialist",
        "cervella-devops": "DevOps Specialist",
        "cervella-docs": "Documentation Specialist",
        "cervella-data": "Data Specialist",
        "cervella-security": "Security Specialist",
        "cervella-orchestrator": "Orchestrator (Regina)",
        # Guardiane (Opus)
        "cervella-guardiana-qualita": "Guardiana Qualità",
        "cervella-guardiana-ricerca": "Guardiana Ricerca",
        "cervella-guardiana-ops": "Guardiana Ops",
    }

    agent_name = None
    agent_role = None

    for name, role in agent_map.items():
        if name in agent_source.lower():
            agent_name = name
            agent_role = role
            break

    return {
        "agent_name": agent_name,
        "agent_role": agent_role,
    }


def extract_task_info(payload: dict) -> dict:
    """Estrae informazioni sul task dal payload."""
    tool_input = payload.get("tool", {}).get("input", {})

    # Cerca descrizione task in vari campi comuni
    task_description = (
        tool_input.get("task") or
        tool_input.get("prompt") or
        tool_input.get("query") or
        tool_input.get("message") or
        str(tool_input)[:200]  # Fallback primi 200 char
    )

    return {
        "task_description": task_description,
        "task_status": "completed",  # PostToolUse = task completato
    }


def extract_files_modified(payload: dict) -> list:
    """Estrae lista file modificati dal payload."""
    files = []
    result = payload.get("result", {})

    # Cerca pattern comuni di file modificati
    if isinstance(result, dict):
        if "file_path" in result:
            files.append(result["file_path"])
        elif "files" in result:
            files.extend(result["files"])

    return files


def extract_project(payload: dict) -> str:
    """Deduce il progetto dal contesto."""
    cwd = payload.get("context", {}).get("cwd", "")

    if "miracollo" in cwd.lower():
        return "miracollo"
    elif "contabilita" in cwd.lower():
        return "contabilita"
    elif "cervellaswarm" in cwd.lower():
        return "cervellaswarm"
    else:
        return "unknown"


def log_event(payload: dict) -> dict:
    """
    Logga evento nel database.

    Args:
        payload: Payload da hook PostToolUse

    Returns:
        Dict con status operazione
    """
    db_path = get_db_path()

    # Se DB non esiste, skip silenzioso (non bloccare workflow)
    if not db_path.exists():
        return {
            "status": "skipped",
            "reason": "database_not_initialized",
        }

    try:
        # Estrai informazioni
        agent_info = extract_agent_info(payload)
        task_info = extract_task_info(payload)
        files_modified = extract_files_modified(payload)
        project = extract_project(payload)

        # Se non è un agent swarm, skip
        if not agent_info["agent_name"]:
            return {
                "status": "skipped",
                "reason": "not_swarm_agent",
            }

        # Prepara evento
        event = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "session_id": payload.get("context", {}).get("session_id"),
            "event_type": "task_complete",

            # Agent
            "agent_name": agent_info["agent_name"],
            "agent_role": agent_info["agent_role"],

            # Task
            "task_id": str(uuid.uuid4()),
            "parent_task_id": None,
            "task_description": task_info["task_description"],
            "task_status": task_info["task_status"],

            # Execution
            "duration_ms": None,  # Non disponibile in PostToolUse
            "success": 1,  # PostToolUse = successo
            "error_message": None,

            # Context
            "project": project,
            "files_modified": json.dumps(files_modified) if files_modified else None,

            # Metadata
            "tags": None,
            "notes": None,
        }

        # Inserisci in DB
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO swarm_events (
                id, timestamp, session_id, event_type,
                agent_name, agent_role,
                task_id, parent_task_id, task_description, task_status,
                duration_ms, success, error_message,
                project, files_modified,
                tags, notes
            ) VALUES (
                :id, :timestamp, :session_id, :event_type,
                :agent_name, :agent_role,
                :task_id, :parent_task_id, :task_description, :task_status,
                :duration_ms, :success, :error_message,
                :project, :files_modified,
                :tags, :notes
            )
        """, event)

        conn.commit()
        conn.close()

        return {
            "status": "success",
            "event_id": event["id"],
            "agent": agent_info["agent_name"],
            "project": project,
        }

    except Exception as e:
        # Log errore ma NON bloccare workflow
        print(f"⚠️ Errore log evento: {e}", file=sys.stderr)
        return {
            "status": "error",
            "error": str(e),
        }


def main():
    """Entry point."""
    try:
        # Leggi payload da stdin
        payload = json.load(sys.stdin)

        # Logga evento
        result = log_event(payload)

        # Output JSON per hook
        print(json.dumps(result))

        # Success anche se skipped (non bloccare workflow)
        sys.exit(0)

    except json.JSONDecodeError:
        print(json.dumps({
            "status": "error",
            "error": "invalid_json_input",
        }))
        sys.exit(0)  # Exit 0 per non bloccare workflow

    except Exception as e:
        print(json.dumps({
            "status": "error",
            "error": str(e),
        }))
        sys.exit(0)  # Exit 0 per non bloccare workflow


if __name__ == "__main__":
    main()
