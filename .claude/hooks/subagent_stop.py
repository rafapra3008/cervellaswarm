#!/usr/bin/env python3
"""
Hook SubagentStop - Logga quando un subagent completa.

Riceve dati da stdin in formato JSON.
Salva nel database swarm_memory.db e in file di debug.

Versione: 1.0.0
Data: 2026-01-01
"""

import sys
import json
from datetime import datetime
from pathlib import Path

# Path al progetto CervellaSwarm
SWARM_DIR = Path(__file__).parent.parent.parent
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

        # Log di debug
        debug_file = LOGS_DIR / "subagent_stop_debug.log"
        with open(debug_file, "a") as f:
            f.write(f"\n{'='*60}\n")
            f.write(f"TIMESTAMP: {ts}\n")
            f.write(f"{'='*60}\n")
            f.write(json.dumps(input_data, indent=2))
            f.write(f"\n{'='*60}\n\n")

        # Estrai informazioni disponibili
        session_id = input_data.get("session_id", "unknown")
        transcript_path = input_data.get("transcript_path", "")

        # Determina il progetto dal CWD o transcript_path
        cwd = input_data.get("cwd", "")
        project = "unknown"
        if "CervellaSwarm" in cwd or "CervellaSwarm" in transcript_path:
            project = "cervellaswarm"
        elif "miracollo" in cwd.lower() or "miracollo" in transcript_path.lower():
            project = "miracollo"
        elif "Contabilita" in cwd or "Contabilita" in transcript_path:
            project = "contabilita"

        # Salva evento nel database
        try:
            import sqlite3
            import uuid

            conn = sqlite3.connect(str(DB_PATH))
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO swarm_events (
                    id, session_id, agent_name, event_type, project,
                    task_description, status, created_at, raw_payload
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                str(uuid.uuid4()),
                session_id,
                "subagent",  # Non sappiamo quale agent specifico
                "subagent_stop",
                project,
                "Subagent completed (from SubagentStop hook)",
                "completed",
                ts,
                json.dumps(input_data)
            ))

            conn.commit()
            conn.close()

            # Output successo
            print(json.dumps({
                "status": "logged",
                "timestamp": ts,
                "project": project,
                "session_id": session_id
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
