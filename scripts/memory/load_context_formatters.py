"""Formatting functions for load_context.

Extracted from load_context.py (S342) to keep it under 500 lines.
Contains presentation/formatting logic for lessons and context.
"""

from datetime import datetime, timezone


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
    output.append("## \U0001f4da LEZIONI RILEVANTI PER QUESTO TASK\n")
    output.append("*Lezioni apprese da errori passati - APPLICALE!*\n\n")

    for lesson in lessons:
        severity = lesson.get("severity", "MEDIUM")
        emoji = {
            "CRITICAL": "\U0001f534",
            "HIGH": "\U0001f7e0",
            "MEDIUM": "\U0001f7e1",
            "LOW": "\U0001f7e2"
        }.get(severity, "\u26aa")

        pattern = lesson.get("pattern") or "Pattern Unknown"
        output.append(f"### {emoji} {severity} - {pattern}\n")

        trigger = lesson.get("trigger")
        if trigger:
            output.append(f"**Trigger:** {trigger}\n\n")

        problem = lesson.get("problem")
        if problem:
            output.append(f"**Problem:** {problem}\n\n")

        root_cause = lesson.get("root_cause")
        if root_cause:
            output.append(f"**Root Cause:** {root_cause}\n\n")

        solution = lesson.get("solution")
        if solution:
            output.append(f"**Solution:** {solution}\n\n")

        prevention = lesson.get("prevention")
        if prevention:
            output.append(f"**Prevention:** {prevention}\n\n")

        example = lesson.get("example")
        if example:
            output.append(f"**Example:** {example}\n\n")

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
    output.append("# \U0001f41d CervellaSwarm - Memoria Attiva\n")
    output.append(f"*Aggiornato: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC*\n")

    # Eventi recenti
    if events:
        output.append("## \U0001f4ca Ultimi Eventi Swarm\n")
        for evt in events[:10]:
            status = "\u2705" if evt["success"] else "\u274c"
            output.append(
                f"- {status} **{evt['agent']}** ({evt['project']}): {evt['task']}\n"
            )
        output.append("")

    # Suggerimenti attivi
    if suggestions:
        output.append("## \U0001f4a1 SUGGERIMENTI ATTIVI\n")
        output.append("*Basati su lezioni apprese e pattern di errori*\n\n")
        for sug in suggestions:
            severity = sug.get('severity', 'MEDIUM')
            emoji = {'CRITICAL': '\U0001f534', 'HIGH': '\U0001f7e0', 'MEDIUM': '\U0001f7e1', 'LOW': '\U0001f7e2'}.get(severity, '\u26aa')
            pattern = sug.get('pattern', 'Unknown')
            prevention = sug.get('prevention') or sug.get('mitigation') or 'N/A'
            output.append(f"- {emoji} **[{severity}] {pattern}**\n")
            output.append(f"  \u2192 {prevention[:100]}\n")
        output.append("\n")

    # Statistiche
    if stats:
        output.append("## \U0001f3af Statistiche Agent\n")
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
        output.append("## \U0001f4a1 Lezioni Apprese (Alta Confidence)\n")
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
