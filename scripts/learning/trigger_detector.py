#!/usr/bin/env python3
"""
Trigger Detector per CervellaSwarm Continuous Learning.
Rileva automaticamente quando c'è una lezione da documentare.
"""

__version__ = "1.0.0"
__version_date__ = "2026-01-01"

import sqlite3
import json
import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, List, Any

# Costanti
TRIGGER_FIX_AFTER_AGENT = "FIX_AFTER_AGENT"
TRIGGER_PATTERN_THRESHOLD = "PATTERN_THRESHOLD"
TRIGGER_MANUAL_MARK = "MANUAL_MARK"
TRIGGER_CRITICAL_ERROR = "CRITICAL_ERROR"

# Configurazione
FIX_WINDOW_MINUTES = 30  # Finestra per rilevare fix dopo agent
PATTERN_THRESHOLD = 3     # Minimo occorrenze per trigger pattern

def get_db_path() -> Path:
    """Ritorna il path del database."""
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent
    return project_root / "data" / "swarm_memory.db"

def get_db_connection() -> sqlite3.Connection:
    """Ottiene connessione al database."""
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    return conn

class TriggerResult:
    """Risultato di un trigger detection."""
    def __init__(self, trigger_type: str, triggered: bool, data: Dict[str, Any] = None):
        self.trigger_type = trigger_type
        self.triggered = triggered
        self.data = data or {}
        self.timestamp = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> Dict:
        return {
            "trigger_type": self.trigger_type,
            "triggered": self.triggered,
            "data": self.data,
            "timestamp": self.timestamp
        }

def check_fix_after_agent(conn: sqlite3.Connection) -> TriggerResult:
    """
    TRIGGER 1: FIX_AFTER_AGENT
    Rileva se la Regina ha fatto Edit entro 30 minuti da un task agent.
    """
    cursor = conn.cursor()

    # Trova ultimi task degli agent (non orchestrator)
    cutoff = (datetime.now(timezone.utc) - timedelta(minutes=FIX_WINDOW_MINUTES)).isoformat()

    cursor.execute("""
        SELECT agent_name, task_description, timestamp, files_modified
        FROM swarm_events
        WHERE agent_name != 'cervella-orchestrator'
        AND agent_name IS NOT NULL
        AND timestamp > ?
        AND event_type = 'task_complete'
        ORDER BY timestamp DESC
        LIMIT 5
    """, (cutoff,))

    recent_tasks = cursor.fetchall()

    if not recent_tasks:
        return TriggerResult(TRIGGER_FIX_AFTER_AGENT, False)

    # Cerca edit della Regina dopo questi task
    cursor.execute("""
        SELECT COUNT(*) as edit_count, files_modified
        FROM swarm_events
        WHERE agent_name = 'cervella-orchestrator'
        AND event_type = 'tool_use'
        AND task_description LIKE '%Edit%'
        AND timestamp > ?
        ORDER BY timestamp DESC
    """, (cutoff,))

    edits = cursor.fetchone()

    if edits and edits['edit_count'] > 0:
        # Potenziale fix dopo agent!
        return TriggerResult(TRIGGER_FIX_AFTER_AGENT, True, {
            "recent_agent_tasks": [dict(t) for t in recent_tasks],
            "edit_count": edits['edit_count'],
            "suggestion": "La Regina ha fatto edit dopo task agent - possibile lezione!"
        })

    return TriggerResult(TRIGGER_FIX_AFTER_AGENT, False)

def check_pattern_threshold(conn: sqlite3.Connection) -> TriggerResult:
    """
    TRIGGER 2: PATTERN_THRESHOLD
    Rileva se un pattern di errore ha raggiunto la soglia (3+ occorrenze).
    """
    cursor = conn.cursor()

    cursor.execute("""
        SELECT pattern_name, occurrence_count, severity_level, last_seen,
               root_cause_hypothesis, mitigation_applied
        FROM error_patterns
        WHERE occurrence_count >= ?
        AND mitigation_applied = 0
        AND status = 'ACTIVE'
        ORDER BY occurrence_count DESC, severity_level DESC
        LIMIT 5
    """, (PATTERN_THRESHOLD,))

    patterns = cursor.fetchall()

    if patterns:
        return TriggerResult(TRIGGER_PATTERN_THRESHOLD, True, {
            "patterns": [dict(p) for p in patterns],
            "suggestion": f"{len(patterns)} pattern hanno raggiunto la soglia di {PATTERN_THRESHOLD}+ occorrenze"
        })

    return TriggerResult(TRIGGER_PATTERN_THRESHOLD, False)

def check_manual_mark(notes: Optional[str] = None, commit_msg: Optional[str] = None) -> TriggerResult:
    """
    TRIGGER 3: MANUAL_MARK
    Rileva se l'utente ha marcato manualmente una lezione.
    """
    search_texts = [t for t in [notes, commit_msg] if t]

    markers = ["lezione:", "lesson:", "impara:", "learn:", "nota importante:"]

    for text in search_texts:
        text_lower = text.lower()
        for marker in markers:
            if marker in text_lower:
                return TriggerResult(TRIGGER_MANUAL_MARK, True, {
                    "marker_found": marker,
                    "text": text,
                    "suggestion": "Lezione marcata manualmente - apri wizard!"
                })

    return TriggerResult(TRIGGER_MANUAL_MARK, False)

def check_critical_error(conn: sqlite3.Connection) -> TriggerResult:
    """
    TRIGGER 4: CRITICAL_ERROR
    Rileva errori critici recenti che meritano documentazione.
    """
    cursor = conn.cursor()

    # Ultimi errori critici (ultime 24 ore)
    cutoff = (datetime.now(timezone.utc) - timedelta(hours=24)).isoformat()

    cursor.execute("""
        SELECT error_message, agent_name, task_description, timestamp
        FROM swarm_events
        WHERE success = 0
        AND error_message IS NOT NULL
        AND timestamp > ?
        ORDER BY timestamp DESC
        LIMIT 5
    """, (cutoff,))

    errors = cursor.fetchall()

    # Check anche pattern critici
    cursor.execute("""
        SELECT pattern_name, occurrence_count
        FROM error_patterns
        WHERE severity_level = 'CRITICAL'
        AND status = 'ACTIVE'
    """)

    critical_patterns = cursor.fetchall()

    if errors or critical_patterns:
        return TriggerResult(TRIGGER_CRITICAL_ERROR, True, {
            "recent_errors": [dict(e) for e in errors] if errors else [],
            "critical_patterns": [dict(p) for p in critical_patterns] if critical_patterns else [],
            "suggestion": "Errori critici rilevati - considera documentarli!"
        })

    return TriggerResult(TRIGGER_CRITICAL_ERROR, False)

def check_all_triggers(notes: Optional[str] = None, commit_msg: Optional[str] = None) -> List[TriggerResult]:
    """
    Esegue tutti i check dei trigger.

    Returns:
        Lista di TriggerResult (solo quelli attivati)
    """
    conn = get_db_connection()
    triggered = []

    try:
        # Check tutti i trigger
        results = [
            check_fix_after_agent(conn),
            check_pattern_threshold(conn),
            check_manual_mark(notes, commit_msg),
            check_critical_error(conn),
        ]

        triggered = [r for r in results if r.triggered]

    finally:
        conn.close()

    return triggered

def format_trigger_notification(result: TriggerResult) -> str:
    """Formatta notifica per un trigger attivato."""
    icons = {
        TRIGGER_FIX_AFTER_AGENT: "🔧",
        TRIGGER_PATTERN_THRESHOLD: "⚠️",
        TRIGGER_MANUAL_MARK: "📝",
        TRIGGER_CRITICAL_ERROR: "🔴"
    }

    lines = [
        "╔══════════════════════════════════════════════════════════════════╗",
        f"║  {icons.get(result.trigger_type, '📋')} LEZIONE RILEVATA!",
        "╠══════════════════════════════════════════════════════════════════╣",
        f"║  Trigger: {result.trigger_type}",
        f"║  {result.data.get('suggestion', 'Nessun dettaglio')}",
        "║",
        "║  Vuoi documentare questa lezione? [Y/n]",
        "╚══════════════════════════════════════════════════════════════════╝"
    ]

    return "\n".join(lines)

def main():
    """Entry point - CLI per test trigger detection."""
    import argparse

    parser = argparse.ArgumentParser(description="CervellaSwarm Trigger Detector")
    parser.add_argument("--check", "-c", action="store_true", help="Esegui tutti i check")
    parser.add_argument("--notes", "-n", type=str, help="Testo da verificare per manual mark")
    parser.add_argument("--json", "-j", action="store_true", help="Output in JSON")
    args = parser.parse_args()

    print(f"🧠 CervellaSwarm Trigger Detector v{__version__}", file=sys.stderr)
    print("-" * 60, file=sys.stderr)

    if args.check:
        triggered = check_all_triggers(notes=args.notes)

        if not triggered:
            print("✅ Nessun trigger attivato", file=sys.stderr)
            if args.json:
                print(json.dumps({"triggers": [], "count": 0}))
        else:
            print(f"⚠️  {len(triggered)} trigger attivati!", file=sys.stderr)

            if args.json:
                print(json.dumps({
                    "triggers": [t.to_dict() for t in triggered],
                    "count": len(triggered)
                }, indent=2))
            else:
                for result in triggered:
                    print("\n" + format_trigger_notification(result))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
