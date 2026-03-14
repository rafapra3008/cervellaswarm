#!/usr/bin/env python3
"""
Hook SubagentStop - Logga quando un subagent completa.

Riceve dati da stdin in formato JSON.
Salva nel database swarm_memory.db e in file di debug.

Versione: 2.1.0
Data: 2026-03-14
v2.1.0 - S454: DRY fix - project detection via cervella_hooks_common (was inline mapping)
Upgrade v2: Legge agent_type, agent_id, agent_transcript_path, last_assistant_message
             (campi disponibili da Claude Code v2.1.49+, prima ignorati)
"""

import sys
import json
import sqlite3
import uuid
from datetime import datetime
from pathlib import Path

# Import project detection from single source of truth (DRY - S454)
sys.path.insert(0, str(Path.home() / ".claude" / "hooks"))
from cervella_hooks_common import detect_project_name as _detect_project_name

# Path ASSOLUTO al database centrale CervellaSwarm
# Questo garantisce che lo script funzioni anche quando eseguito da altri progetti
# (es. Miracollo, Contabilità) - tutti scrivono nello STESSO DB centrale!
SWARM_DIR = Path.home() / "Developer" / "CervellaSwarm"
DATA_DIR = SWARM_DIR / "data"
LOGS_DIR = DATA_DIR / "logs"
DB_PATH = DATA_DIR / "swarm_memory.db"

def main():
    # Assicura che le directory esistano
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    try:
        # Leggi dati da stdin
        input_data = json.load(sys.stdin)

        # Timestamp
        ts = datetime.now().isoformat()

        # Log di debug (con rotazione: max 1000 righe)
        debug_file = LOGS_DIR / "subagent_stop_debug.log"
        # Rotazione: se > 1000 righe, tieni solo le ultime 500
        if debug_file.exists():
            try:
                lines = debug_file.read_text().splitlines()
                if len(lines) > 1000:
                    debug_file.write_text("\n".join(lines[-500:]) + "\n")
            except Exception:
                pass
        with open(debug_file, "a") as f:
            f.write(f"\n{'='*60}\n")
            f.write(f"TIMESTAMP: {ts}\n")
            f.write(f"{'='*60}\n")
            f.write(json.dumps(input_data, indent=2))
            f.write(f"\n{'='*60}\n\n")

        # Estrai informazioni disponibili (v2: campi agent_* da Claude Code v2.1.49+)
        session_id = input_data.get("session_id", "unknown")
        agent_type = input_data.get("agent_type", "subagent")
        agent_id = input_data.get("agent_id", "")
        transcript_path = input_data.get("agent_transcript_path", input_data.get("transcript_path", ""))
        last_message = input_data.get("last_assistant_message", "")

        # Determina il progetto dal CWD (DRY - S454: usa cervella_hooks_common)
        cwd = input_data.get("cwd", "")
        project = _detect_project_name(cwd) or "unknown"

        # Salva evento nel database
        try:
            summary = last_message[:500] if last_message else ""
            notes_data = {
                "agent_id": agent_id,
                "transcript_path": transcript_path,
                "summary": summary,
            }

            with sqlite3.connect(str(DB_PATH), timeout=10) as conn:
                conn.execute("PRAGMA journal_mode=WAL")
                cursor = conn.cursor()

                # Auto-create tabella se non esiste (P1 fix)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS swarm_events (
                        id TEXT PRIMARY KEY,
                        timestamp TEXT NOT NULL,
                        session_id TEXT,
                        agent_name TEXT,
                        event_type TEXT,
                        project TEXT,
                        task_description TEXT,
                        task_status TEXT,
                        notes TEXT
                    )
                """)

                cursor.execute("""
                    INSERT INTO swarm_events (
                        id, timestamp, session_id, agent_name, event_type, project,
                        task_description, task_status, notes
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    str(uuid.uuid4()),
                    ts,
                    session_id,
                    agent_type,
                    "subagent_stop",
                    project,
                    f"Agent '{agent_type}' completed",
                    "completed",
                    json.dumps(notes_data),
                ))

                conn.commit()

            print(json.dumps({
                "status": "logged",
                "timestamp": ts,
                "project": project,
                "agent_type": agent_type,
                "session_id": session_id,
            }))

        except Exception as db_error:
            # Log errore DB ma non fallire
            with open(LOGS_DIR / "subagent_stop_errors.log", "a") as f:
                f.write(f"{ts}: DB Error: {db_error}\n")

            print(json.dumps({
                "status": "debug_only",
                "error": str(db_error)
            }))

        sys.exit(0)

    except Exception as e:
        # Log errore
        error_file = LOGS_DIR / "subagent_stop_errors.log"
        with open(error_file, "a") as f:
            f.write(f"{datetime.now().isoformat()}: {str(e)}\n")

        print(json.dumps({"status": "error", "error": str(e)}))
        sys.exit(0)  # Non fallire per non bloccare Claude

if __name__ == "__main__":
    main()
