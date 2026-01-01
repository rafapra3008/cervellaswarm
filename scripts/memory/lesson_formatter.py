#!/usr/bin/env python3
"""
CervellaSwarm Lesson Formatter - Formato Lezioni per Agenti

Formatta lezioni dal database in markdown ottimizzato per prompt injection.
Supporta diversi formati: full, compact, minimal.
"""

__version__ = "1.0.0"
__version_date__ = "2026-01-01"

from typing import List, Dict, Tuple
from enum import Enum


class FormatStyle(Enum):
    """Stili di formattazione disponibili."""
    FULL = "full"        # Tutti i campi
    COMPACT = "compact"  # Solo essenziali
    MINIMAL = "minimal"  # Una riga


class LessonFormatter:
    """Formatta lezioni per prompt injection."""

    SEVERITY_EMOJI = {
        'CRITICAL': '🔴',
        'HIGH': '🟠',
        'MEDIUM': '🟡',
        'LOW': '🟢'
    }

    def format_single(
        self,
        lesson: dict,
        style: FormatStyle = FormatStyle.COMPACT
    ) -> str:
        """
        Formatta una singola lezione.

        Args:
            lesson: Dict con campi lezione
            style: Stile di formattazione

        Returns:
            Stringa markdown formattata
        """
        if style == FormatStyle.FULL:
            return self._format_full(lesson)
        elif style == FormatStyle.COMPACT:
            return self._format_compact(lesson)
        else:
            return self._format_minimal(lesson)

    def _format_full(self, lesson: dict) -> str:
        """
        Formato completo con tutti i campi.

        Args:
            lesson: Dict con campi lezione

        Returns:
            Stringa markdown formattata
        """
        severity = lesson.get('severity', 'MEDIUM')
        emoji = self.SEVERITY_EMOJI.get(severity, '⚪')
        pattern = lesson.get('pattern', 'Unknown')

        return f"""### {emoji} [{severity}] {pattern}

**Trigger:** {lesson.get('trigger', 'N/A')}

**Context:** {lesson.get('context', 'N/A')}

**Problem:** {lesson.get('problem', 'N/A')}

**Root Cause:** {lesson.get('root_cause', 'N/A')}

**Solution:** {lesson.get('solution', 'N/A')}

**Prevention:** {lesson.get('prevention', 'N/A')}

**Example:** {lesson.get('example', 'N/A')}

*Confidence: {lesson.get('confidence', 0):.0%} | Applied: {lesson.get('times_applied', 0)} times*

---"""

    def _format_compact(self, lesson: dict) -> str:
        """
        Formato compatto - solo campi essenziali.

        Args:
            lesson: Dict con campi lezione

        Returns:
            Stringa markdown formattata
        """
        severity = lesson.get('severity', 'MEDIUM')
        emoji = self.SEVERITY_EMOJI.get(severity, '⚪')
        pattern = lesson.get('pattern', 'Unknown')

        return f"""### {emoji} [{severity}] {pattern}
**Trigger:** {lesson.get('trigger', 'N/A')}
**Problem:** {lesson.get('problem', 'N/A')}
**Solution:** {lesson.get('solution', 'N/A')}
**Prevention:** {lesson.get('prevention', 'N/A')}
"""

    def _format_minimal(self, lesson: dict) -> str:
        """
        Formato minimo - una riga.

        Args:
            lesson: Dict con campi lezione

        Returns:
            Stringa markdown formattata
        """
        severity = lesson.get('severity', 'MEDIUM')
        emoji = self.SEVERITY_EMOJI.get(severity, '⚪')
        pattern = lesson.get('pattern', 'Unknown')
        solution = lesson.get('solution', 'N/A')[:100]

        return f"- {emoji} **{pattern}**: {solution}"

    def format_multiple(
        self,
        lessons: List[Tuple[dict, float]],
        style: FormatStyle = FormatStyle.COMPACT,
        header: bool = True
    ) -> str:
        """
        Formatta multiple lezioni con header.

        Args:
            lessons: Lista di tuple (lesson_dict, score)
            style: Stile di formattazione
            header: Se includere header sezione

        Returns:
            Stringa markdown completa
        """
        if not lessons:
            return ""

        parts = []

        if header:
            parts.append("## 📚 LEZIONI RILEVANTI PER QUESTO TASK\n")
            parts.append("*Queste lezioni derivano da errori reali del team. Prendile SERIAMENTE!*\n")

        for lesson, score in lessons:
            parts.append(self.format_single(lesson, style))
            parts.append("")  # Riga vuota tra lezioni

        if header:
            parts.append("---")
            min_score = min(score for _, score in lessons)
            max_score = max(score for _, score in lessons)
            parts.append(f"*{len(lessons)} lezioni caricate | Score range: {min_score:.0f}-{max_score:.0f}/100*")

        return "\n".join(parts)


def main():
    """CLI per test."""
    import argparse

    parser = argparse.ArgumentParser(description="CervellaSwarm Lesson Formatter")
    parser.add_argument(
        "--style", "-s",
        choices=["full", "compact", "minimal"],
        default="compact",
        help="Stile di formattazione (default: compact)"
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Test con dati finti"
    )

    args = parser.parse_args()

    if args.test:
        formatter = LessonFormatter()

        test_lesson = {
            "pattern": "incomplete-interface",
            "trigger": "Quando lavori su componenti TypeScript",
            "context": "Task: Countdown component",
            "problem": "Interfaccia dichiarata ma non implementata completamente",
            "root_cause": "Agent ha interpretato interfaccia come documentazione",
            "solution": "Implementare TUTTA l'interfaccia PRIMA della logica",
            "prevention": "Checklist: ogni metodo dichiarato = implementato",
            "example": "Countdown: mancavano onExpire, reset, pause",
            "severity": "CRITICAL",
            "confidence": 0.95,
            "times_applied": 1
        }

        style = FormatStyle(args.style)
        print(f"\n🎨 Format Style: {style.value}\n")
        print(formatter.format_single(test_lesson, style))

        # Test formato multiplo
        print("\n" + "="*60)
        print("TEST FORMATO MULTIPLO:")
        print("="*60 + "\n")

        test_lessons = [
            (test_lesson, 95),
            ({
                "pattern": "missing-validation",
                "trigger": "Quando ricevi input utente",
                "problem": "Nessuna validazione input",
                "solution": "SEMPRE validare PRIMA di usare",
                "prevention": "Checklist: ogni input = validato",
                "severity": "HIGH",
                "confidence": 0.90,
                "times_applied": 3
            }, 87)
        ]

        print(formatter.format_multiple(test_lessons, style))


if __name__ == "__main__":
    main()
