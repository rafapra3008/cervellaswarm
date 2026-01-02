#!/usr/bin/env python3
"""
Sistema Memoria CervellaSwarm - Log Eventi

Riceve payload da hook PostToolUse e logga eventi nel database.
Gestisce errori gracefully per non bloccare mai il workflow.
"""

__version__ = "1.2.0"
__version_date__ = "2026-01-01"  # Fix: supporta formato PostToolUse hook (tool_name, tool_input, cwd, session_id a root level)

import json
import sqlite3
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

# Import centralizzato path management
sys.path.insert(0, str(Path(__file__).parent.parent))
from common.paths import get_db_path


def extract_agent_info(payload: dict) -> dict:
    """Estrae informazioni sull'agent dal payload."""
    # Formato PostToolUse hook: tool_name e tool_input sono a root level
    tool_name = payload.get("tool_name", "")
    tool_input = payload.get("tool_input", {})

    # Fallback per formato vecchio (tool.name, tool.input)
    if not tool_name:
        tool = payload.get("tool", {})
        tool_name = tool.get("name", "")
        tool_input = tool.get("input", {})

    # L'agent è in subagent O subagent_type
    subagent = tool_input.get("subagent", "") or tool_input.get("subagent_type", "")
    agent_source = subagent if subagent else tool_name

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
    # Formato PostToolUse hook: tool_input è a root level
    tool_input = payload.get("tool_input", {})

    # Fallback per formato vecchio
    if not tool_input:
        tool_input = payload.get("tool", {}).get("input", {})

    # Cerca descrizione task in vari campi comuni
    task_description = (
        tool_input.get("task") or
        tool_input.get("prompt") or
        tool_input.get("description") or
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
    # Formato PostToolUse hook: cwd è a root level
    cwd = payload.get("cwd", "")

    # Fallback per formato vecchio
    if not cwd:
        cwd = payload.get("context", {}).get("cwd", "")

    cwd_lower = cwd.lower()
    if "miracollo" in cwd_lower:
        return "miracollo"
    elif "contabilita" in cwd_lower:
        return "contabilita"
    elif "cervellaswarm" in cwd_lower:
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
        # session_id può essere a root level o in context
        session_id = payload.get("session_id") or payload.get("context", {}).get("session_id")

        event = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "session_id": session_id,
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
