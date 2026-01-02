#!/usr/bin/env python3
"""
Sistema Memoria CervellaSwarm - Caricamento Contesto

Carica contesto rilevante per SessionStart hook.
Include eventi recenti e lezioni apprese attive.

v2.0.0 Novità:
- Lesson Injection: lezioni rilevanti iniettate nel contesto
- Context Scoring: ranking lezioni per rilevanza (agent + project + severity)
- Agent Filtering: filtra lezioni per agente specifico
"""

__version__ = "2.0.1"
__version_date__ = "2026-01-01"
# v2.0.1 - Fix: Aggiunto hookEventName a tutti i return (required by Claude Code)

import json
import sqlite3
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Import centralizzato path management
sys.path.insert(0, str(Path(__file__).parent.parent))
from common.paths import get_db_path

# Import suggestions (fallback graceful)
try:
    from suggestions import get_suggestions, get_context_aware_suggestions
except ImportError:
    get_suggestions = None
    get_context_aware_suggestions = None


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

        stats[agent]["total_tasks"] += row[1] or 0
        stats[agent]["successful_tasks"] += row[2] or 0
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


def get_relevant_lessons(
    conn: sqlite3.Connection,
    agent_name: str = None,
    project: str = None,
    limit: int = 3
) -> list:
    """
    Filtra lezioni rilevanti per l'agente corrente con scoring.

    Scoring:
    - agents_involved contiene agent_name: +50
    - project match: +30
    - severity CRITICAL: +20, HIGH: +15, MEDIUM: +10, LOW: +5
    - times_applied > 5: +10
    - confidence > 0.9: +10

    Args:
        conn: Connessione al database
        agent_name: Nome dell'agent (es. cervella-frontend)
        project: Nome progetto corrente
        limit: Numero massimo di lezioni

    Returns:
        Lista di lezioni ordinate per rilevanza
    """
    cursor = conn.cursor()

    # Query completa con tutti i campi necessari
    cursor.execute("""
        SELECT
            trigger,
            context,
            problem,
            root_cause,
            solution,
            prevention,
            example,
            severity,
            agents_involved,
            tags,
            pattern,
            confidence,
            times_applied,
            project
        FROM lessons_learned
        WHERE status = 'ACTIVE'
        ORDER BY confidence DESC, times_applied DESC
    """)

    lessons = []
    for row in cursor.fetchall():
        # Calcola score
        score = 0

        # Agent match (+50 se presente in agents_involved)
        agents_involved = row[8] or ""
        if agent_name and agent_name in agents_involved:
            score += 50

        # Project match (+30)
        lesson_project = row[13] or ""
        if project and lesson_project and project.lower() in lesson_project.lower():
            score += 30

        # Severity
        severity = row[7] or "MEDIUM"
        severity_scores = {
            "CRITICAL": 20,
            "HIGH": 15,
            "MEDIUM": 10,
            "LOW": 5
        }
        score += severity_scores.get(severity, 0)

        # Times applied
        times_applied = row[12] or 0
        if times_applied > 5:
            score += 10

        # High confidence
        confidence = row[11] or 0.5
        if confidence > 0.9:
            score += 10

        lessons.append({
            "trigger": row[0],
            "context": row[1],
            "problem": row[2],
            "root_cause": row[3],
            "solution": row[4],
            "prevention": row[5],
            "example": row[6],
            "severity": severity,
            "agents_involved": agents_involved,
            "tags": row[9],
            "pattern": row[10],
            "confidence": confidence,
            "times_applied": times_applied,
            "project": lesson_project,
            "score": score
        })

    # Ordina per score e prendi top N
    lessons.sort(key=lambda x: x["score"], reverse=True)
    return lessons[:limit]


def format_lessons_for_agent(lessons: list) -> str:
    """
    Formatta lezioni per prompt agent in markdown.

    Args:
        lessons: Lista di lezioni da formattare

    Returns:
        Markdown formattato
    """
    if not lessons:
        return ""

    output = []
    output.append("## 📚 LEZIONI RILEVANTI PER QUESTO TASK\n")
    output.append("*Lezioni apprese da errori passati - APPLICALE!*\n\n")

    for lesson in lessons:
        severity = lesson.get("severity", "MEDIUM")
        emoji = {
            "CRITICAL": "🔴",
            "HIGH": "🟠",
            "MEDIUM": "🟡",
            "LOW": "🟢"
        }.get(severity, "⚪")

        pattern = lesson.get("pattern") or "Pattern Unknown"
        output.append(f"### {emoji} {severity} - {pattern}\n")

        # Trigger
        trigger = lesson.get("trigger")
        if trigger:
            output.append(f"**Trigger:** {trigger}\n\n")

        # Problem
        problem = lesson.get("problem")
        if problem:
            output.append(f"**Problem:** {problem}\n\n")

        # Root Cause
        root_cause = lesson.get("root_cause")
        if root_cause:
            output.append(f"**Root Cause:** {root_cause}\n\n")

        # Solution
        solution = lesson.get("solution")
        if solution:
            output.append(f"**Solution:** {solution}\n\n")

        # Prevention
        prevention = lesson.get("prevention")
        if prevention:
            output.append(f"**Prevention:** {prevention}\n\n")

        # Example
        example = lesson.get("example")
        if example:
            output.append(f"**Example:** {example}\n\n")

        # Metadata
        confidence = lesson.get("confidence", 0)
        times_applied = lesson.get("times_applied", 0)
        score = lesson.get("score", 0)
        output.append(
            f"*Confidence: {confidence:.0%} | "
            f"Applicata {times_applied}x | "
            f"Score: {score}*\n\n"
        )
        output.append("---\n\n")

    return "".join(output)


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


def load_context(agent_name: str = None, project: str = None) -> dict:
    """
    Carica contesto per SessionStart hook.

    Args:
        agent_name: Nome agente (opzionale) - per filtrare lezioni
        project: Nome progetto (opzionale) - per filtrare lezioni

    Returns:
        Dict con hookSpecificOutput
    """
    db_path = get_db_path()

    # Se DB non esiste, ritorna vuoto
    if not db_path.exists():
        return {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": "🐝 Sistema memoria non inizializzato."
            }
        }

    try:
        conn = sqlite3.connect(db_path)

        # Carica dati
        events = get_recent_events(conn)
        stats = get_agent_stats(conn)
        lessons = get_lessons_learned(conn)

        # 🆕 NOVITÀ v2.0.0: Lezioni rilevanti per agent/project
        relevant_lessons = get_relevant_lessons(
            conn,
            agent_name=agent_name,
            project=project,
            limit=3
        )

        conn.close()

        # Carica suggerimenti attivi
        suggestions = get_active_suggestions(project=project)

        # Formatta contesto
        context_md = format_context(events, stats, lessons, suggestions)

        # 🆕 NOVITÀ v2.0.0: Aggiungi lezioni rilevanti formattate
        if relevant_lessons:
            lessons_md = format_lessons_for_agent(relevant_lessons)
            context_md = context_md + "\n" + lessons_md

        return {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": context_md
            },
            "metadata": {
                "events_count": len(events),
                "agents_count": len(stats),
                "lessons_count": len(lessons),
                "relevant_lessons_count": len(relevant_lessons),
            }
        }

    except Exception as e:
        # Log errore ma ritorna contesto vuoto
        print(f"⚠️ Errore caricamento contesto: {e}", file=sys.stderr)
        return {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
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
                "hookEventName": "SessionStart",
                "additionalContext": f"❌ Errore critico: {str(e)}"
            }
        }), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
