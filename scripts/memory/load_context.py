#!/usr/bin/env python3
"""
Sistema Memoria CervellaSwarm - Caricamento Contesto

Carica contesto rilevante per SessionStart hook.
Include eventi recenti e lezioni apprese attive.
"""

__version__ = "1.1.0"
__version_date__ = "2026-01-01"

import json
import sqlite3
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Import suggestions (fallback graceful)
try:
    from suggestions import get_suggestions, get_context_aware_suggestions
except ImportError:
    get_suggestions = None
    get_context_aware_suggestions = None


def get_db_path() -> Path:
    """Ritorna il path del database."""
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent
    return project_root / "data" / "swarm_memory.db"


def get_recent_events(conn: sqlite3.Connection, limit: int = 20) -> list:
    """
    Recupera eventi recenti.

    Args:
        conn: Connessione al database
        limit: Numero massimo di eventi

    Returns:
        Lista di eventi
    """
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            timestamp,
            agent_name,
            task_description,
            project,
            success
        FROM swarm_events
        WHERE agent_name IS NOT NULL
        ORDER BY timestamp DESC
        LIMIT ?
    """, (limit,))

    events = []
    for row in cursor.fetchall():
        events.append({
            "timestamp": row[0],
            "agent": row[1],
            "task": row[2][:100] if row[2] else "",  # Max 100 char
            "project": row[3],
            "success": bool(row[4]),
        })

    return events


def get_agent_stats(conn: sqlite3.Connection) -> dict:
    """
    Statistiche per agent.

    Returns:
        Dict con statistiche
    """
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            agent_name,
            COUNT(*) as total_tasks,
            SUM(success) as successful_tasks,
            project
        FROM swarm_events
        WHERE agent_name IS NOT NULL
        GROUP BY agent_name, project
        ORDER BY total_tasks DESC
    """)

    stats = {}
    for row in cursor.fetchall():
        agent = row[0]
        if agent not in stats:
            stats[agent] = {
                "total_tasks": 0,
                "successful_tasks": 0,
                "projects": [],
            }

        stats[agent]["total_tasks"] += row[1]
        stats[agent]["successful_tasks"] += row[2]
        if row[3] and row[3] not in stats[agent]["projects"]:
            stats[agent]["projects"].append(row[3])

    return stats


def get_lessons_learned(conn: sqlite3.Connection, min_confidence: float = 0.7) -> list:
    """
    Recupera lezioni apprese con alta confidence.

    Args:
        conn: Connessione al database
        min_confidence: Confidence minima

    Returns:
        Lista di lezioni
    """
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            context,
            problem,
            solution,
            pattern,
            confidence,
            times_applied
        FROM lessons_learned
        WHERE confidence >= ?
        ORDER BY confidence DESC, times_applied DESC
        LIMIT 10
    """, (min_confidence,))

    lessons = []
    for row in cursor.fetchall():
        lessons.append({
            "context": row[0],
            "problem": row[1],
            "solution": row[2],
            "pattern": row[3],
            "confidence": row[4],
            "times_applied": row[5],
        })

    return lessons


def get_active_suggestions(project: str = None) -> list:
    """
    Recupera suggerimenti attivi.

    Args:
        project: Progetto corrente (opzionale)

    Returns:
        Lista di suggerimenti
    """
    if not get_suggestions:
        return []

    try:
        return get_suggestions(project=project, limit=5)
    except Exception:
        return []


def format_context(events: list, stats: dict, lessons: list, suggestions: list = None) -> str:
    """
    Formatta contesto in markdown per hook.

    Args:
        events: Lista eventi recenti
        stats: Statistiche agent
        lessons: Lezioni apprese
        suggestions: Suggerimenti attivi (opzionale)

    Returns:
        Markdown formattato
    """
    output = []

    # Header
    output.append("# 🐝 CervellaSwarm - Memoria Attiva\n")
    output.append(f"*Aggiornato: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC*\n")

    # Eventi recenti
    if events:
        output.append("## 📊 Ultimi Eventi Swarm\n")
        for evt in events[:10]:  # Max 10
            status = "✅" if evt["success"] else "❌"
            output.append(
                f"- {status} **{evt['agent']}** ({evt['project']}): {evt['task']}\n"
            )
        output.append("")

    # Suggerimenti attivi
    if suggestions:
        output.append("## 💡 SUGGERIMENTI ATTIVI\n")
        output.append("*Basati su lezioni apprese e pattern di errori*\n\n")
        for sug in suggestions:
            severity = sug.get('severity', 'MEDIUM')
            emoji = {'CRITICAL': '🔴', 'HIGH': '🟠', 'MEDIUM': '🟡', 'LOW': '🟢'}.get(severity, '⚪')
            pattern = sug.get('pattern', 'Unknown')
            prevention = sug.get('prevention') or sug.get('mitigation') or 'N/A'
            output.append(f"- {emoji} **[{severity}] {pattern}**\n")
            output.append(f"  → {prevention[:100]}\n")
        output.append("\n")

    # Statistiche
    if stats:
        output.append("## 🎯 Statistiche Agent\n")
        for agent, data in stats.items():
            success_rate = (data["successful_tasks"] / data["total_tasks"] * 100
                          if data["total_tasks"] > 0 else 0)
            projects = ", ".join(data["projects"])
            output.append(
                f"- **{agent}**: {data['total_tasks']} task "
                f"({success_rate:.1f}% successo) - Progetti: {projects}\n"
            )
        output.append("")

    # Lezioni apprese
    if lessons:
        output.append("## 💡 Lezioni Apprese (Alta Confidence)\n")
        for lesson in lessons:
            output.append(f"### {lesson['pattern']}\n")
            output.append(f"- **Problema**: {lesson['problem']}\n")
            output.append(f"- **Soluzione**: {lesson['solution']}\n")
            output.append(
                f"- **Confidence**: {lesson['confidence']:.0%} "
                f"(applicata {lesson['times_applied']} volte)\n"
            )
            output.append("")

    return "".join(output)


def load_context() -> dict:
    """
    Carica contesto per SessionStart hook.

    Returns:
        Dict con hookSpecificOutput
    """
    db_path = get_db_path()

    # Se DB non esiste, ritorna vuoto
    if not db_path.exists():
        return {
            "hookSpecificOutput": {
                "additionalContext": "🐝 Sistema memoria non inizializzato."
            }
        }

    try:
        conn = sqlite3.connect(db_path)

        # Carica dati
        events = get_recent_events(conn)
        stats = get_agent_stats(conn)
        lessons = get_lessons_learned(conn)

        conn.close()

        # Carica suggerimenti attivi
        suggestions = get_active_suggestions()

        # Formatta contesto
        context_md = format_context(events, stats, lessons, suggestions)

        return {
            "hookSpecificOutput": {
                "additionalContext": context_md
            },
            "metadata": {
                "events_count": len(events),
                "agents_count": len(stats),
                "lessons_count": len(lessons),
            }
        }

    except Exception as e:
        # Log errore ma ritorna contesto vuoto
        print(f"⚠️ Errore caricamento contesto: {e}", file=sys.stderr)
        return {
            "hookSpecificOutput": {
                "additionalContext": f"⚠️ Errore caricamento memoria: {str(e)}"
            }
        }


def main():
    """Entry point."""
    try:
        # Carica contesto
        result = load_context()

        # Output JSON per hook
        print(json.dumps(result, indent=2))

        sys.exit(0)

    except Exception as e:
        print(json.dumps({
            "hookSpecificOutput": {
                "additionalContext": f"❌ Errore critico: {str(e)}"
            }
        }), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
