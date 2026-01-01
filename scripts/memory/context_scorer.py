#!/usr/bin/env python3
"""
CervellaSwarm Context Scorer - Ranking Lezioni per Rilevanza

Calcola score di rilevanza per ogni lezione basandosi su:
- Match agente (agent_name in agents_involved)
- Match progetto (project match)
- Match keywords (tags match con task description)
- Severity (CRITICAL > HIGH > MEDIUM > LOW)
- Confidence e times_applied

Usage:
    from context_scorer import ContextScorer

    scorer = ContextScorer()
    top_lessons = scorer.rank_lessons(
        lessons,
        agent_name="cervella-frontend",
        project="Miracollo",
        task_keywords=["typescript", "component"]
    )
"""

__version__ = "1.0.0"
__version_date__ = "2026-01-01"

import json
import re
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass


@dataclass
class ScoringWeights:
    """Pesi per il calcolo dello score di rilevanza."""
    agent_match: int = 50           # Massimo contributo se agent in agents_involved
    project_match: int = 30         # Se project == lesson.project
    keyword_match_per_tag: int = 5  # Per ogni tag che matcha (max 20)
    severity_critical: int = 20
    severity_high: int = 15
    severity_medium: int = 10
    severity_low: int = 5
    high_confidence: int = 10       # Se confidence > 0.9
    frequently_applied: int = 10    # Se times_applied > 5


class ContextScorer:
    """Calcola score di rilevanza per lezioni basandosi sul contesto corrente."""

    def __init__(self, weights: ScoringWeights = None):
        """
        Inizializza scorer con pesi configurabili.

        Args:
            weights: Pesi personalizzati, usa defaults se None
        """
        self.weights = weights or ScoringWeights()

    def score_lesson(
        self,
        lesson: dict,
        agent_name: Optional[str] = None,
        project: Optional[str] = None,
        task_keywords: Optional[List[str]] = None
    ) -> int:
        """
        Calcola score 0-100 per una singola lezione.

        Args:
            lesson: Dict con campi lezione (agents_involved, tags, severity, etc)
            agent_name: Nome agente corrente (es. "cervella-frontend")
            project: Progetto corrente (es. "Miracollo")
            task_keywords: Parole chiave del task corrente (lowercase)

        Returns:
            Score 0-100 indicante rilevanza della lezione
        """
        score = 0

        # 1. Agent match (+50)
        if agent_name:
            agents = self._parse_agents(lesson.get('agents_involved', []))
            if agent_name in agents:
                score += self.weights.agent_match

        # 2. Project match (+30)
        if project:
            lesson_project = lesson.get('project', '')
            if lesson_project and lesson_project.lower() == project.lower():
                score += self.weights.project_match

        # 3. Keyword match (+5 per tag, max 20)
        if task_keywords:
            tags = self._parse_tags(lesson.get('tags', []))
            matches = sum(1 for tag in tags if tag.lower() in task_keywords)
            keyword_score = min(
                matches * self.weights.keyword_match_per_tag,
                20  # Cap a 20
            )
            score += keyword_score

        # 4. Severity bonus
        severity = lesson.get('severity', 'MEDIUM')
        severity_scores = {
            'CRITICAL': self.weights.severity_critical,
            'HIGH': self.weights.severity_high,
            'MEDIUM': self.weights.severity_medium,
            'LOW': self.weights.severity_low
        }
        score += severity_scores.get(severity, self.weights.severity_medium)

        # 5. Confidence bonus (+10 se > 0.9)
        confidence = lesson.get('confidence', 0.0)
        if isinstance(confidence, (int, float)) and confidence > 0.9:
            score += self.weights.high_confidence

        # 6. Times applied bonus (+10 se > 5)
        times_applied = lesson.get('times_applied', 0)
        if isinstance(times_applied, int) and times_applied > 5:
            score += self.weights.frequently_applied

        return min(100, score)  # Cap a 100

    def rank_lessons(
        self,
        lessons: List[dict],
        agent_name: Optional[str] = None,
        project: Optional[str] = None,
        task_keywords: Optional[List[str]] = None,
        limit: int = 3
    ) -> List[Tuple[dict, int]]:
        """
        Ordina lezioni per rilevanza e ritorna top N.

        Args:
            lessons: Lista di dict lezioni
            agent_name: Nome agente corrente
            project: Progetto corrente
            task_keywords: Keywords del task
            limit: Numero massimo di lezioni da ritornare

        Returns:
            Lista di (lesson, score) ordinata per score decrescente
            Solo lezioni con score > 0
        """
        # Normalizza keywords a lowercase
        if task_keywords:
            task_keywords = [kw.lower() for kw in task_keywords]

        # Calcola score per ogni lezione
        scored = []
        for lesson in lessons:
            score = self.score_lesson(
                lesson,
                agent_name=agent_name,
                project=project,
                task_keywords=task_keywords
            )
            scored.append((lesson, score))

        # Ordina per score decrescente
        scored.sort(key=lambda x: x[1], reverse=True)

        # Ritorna top N con score > 0
        return [(l, s) for l, s in scored[:limit] if s > 0]

    def _parse_agents(self, agents_field) -> List[str]:
        """
        Parse agents_involved field (può essere lista o stringa JSON).

        Args:
            agents_field: Lista o stringa JSON di agenti

        Returns:
            Lista di nomi agenti
        """
        if isinstance(agents_field, list):
            return agents_field

        if isinstance(agents_field, str):
            if not agents_field.strip():
                return []

            try:
                parsed = json.loads(agents_field)
                return parsed if isinstance(parsed, list) else []
            except json.JSONDecodeError:
                # Prova split per comma
                return [a.strip() for a in agents_field.split(',') if a.strip()]

        return []

    def _parse_tags(self, tags_field) -> List[str]:
        """
        Parse tags field (può essere lista o stringa JSON).

        Args:
            tags_field: Lista o stringa JSON di tags

        Returns:
            Lista di tags
        """
        if isinstance(tags_field, list):
            return tags_field

        if isinstance(tags_field, str):
            if not tags_field.strip():
                return []

            try:
                parsed = json.loads(tags_field)
                return parsed if isinstance(parsed, list) else []
            except json.JSONDecodeError:
                # Prova split per comma
                return [t.strip() for t in tags_field.split(',') if t.strip()]

        return []


def extract_keywords(text: str, min_length: int = 3) -> List[str]:
    """
    Estrae keywords rilevanti da un testo.

    Rimuove stopwords comuni, converte a lowercase, tokenizza.

    Args:
        text: Testo da cui estrarre keywords
        min_length: Lunghezza minima per una keyword

    Returns:
        Lista di keywords (lowercase)
    """
    # Stopwords comuni (inglese + italiano base)
    stopwords = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
        'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
        'should', 'could', 'may', 'might', 'must', 'can', 'this', 'that',
        'these', 'those', 'it', 'its', 'they', 'them', 'their',
        'il', 'la', 'i', 'le', 'un', 'una', 'di', 'da', 'in', 'con', 'su',
        'per', 'tra', 'fra', 'e', 'o', 'ma', 'se', 'che', 'non'
    }

    # Lowercase
    text = text.lower()

    # Estrai parole (alfanumeriche + - _ )
    words = re.findall(r'[a-z0-9_-]+', text)

    # Filtra stopwords e parole troppo corte
    keywords = [
        w for w in words
        if len(w) >= min_length and w not in stopwords
    ]

    # Rimuovi duplicati mantenendo ordine
    seen = set()
    unique_keywords = []
    for kw in keywords:
        if kw not in seen:
            seen.add(kw)
            unique_keywords.append(kw)

    return unique_keywords


# CLI per test
def main():
    """CLI per test del context scorer."""
    import argparse

    parser = argparse.ArgumentParser(
        description="CervellaSwarm Context Scorer - Ranking Lezioni per Rilevanza"
    )
    parser.add_argument(
        "--agent", "-a",
        help="Nome agente (es. cervella-frontend)"
    )
    parser.add_argument(
        "--project", "-p",
        help="Nome progetto (es. Miracollo)"
    )
    parser.add_argument(
        "--task", "-t",
        help="Descrizione task"
    )
    parser.add_argument(
        "--test", action="store_true",
        help="Esegui test con dati finti"
    )

    args = parser.parse_args()

    if args.test:
        # Test con dati finti
        print("🧠 CervellaSwarm Context Scorer - Test Mode\n")

        scorer = ContextScorer()

        # Lezioni di esempio
        test_lessons = [
            {
                "pattern": "incomplete-interface",
                "agents_involved": ["cervella-frontend"],
                "project": "Miracollo",
                "severity": "CRITICAL",
                "confidence": 0.95,
                "times_applied": 1,
                "tags": ["typescript", "interface", "frontend"]
            },
            {
                "pattern": "blind-retry",
                "agents_involved": ["cervella-backend", "cervella-frontend"],
                "project": "Contabilità",
                "severity": "MEDIUM",
                "confidence": 0.8,
                "times_applied": 10,
                "tags": ["retry", "error-handling", "backend"]
            },
            {
                "pattern": "missing-validation",
                "agents_involved": ["cervella-backend"],
                "project": "Miracollo",
                "severity": "HIGH",
                "confidence": 0.9,
                "times_applied": 3,
                "tags": ["validation", "api", "typescript"]
            }
        ]

        # Scenario 1: cervella-frontend su Miracollo con TypeScript
        print("📋 Scenario 1: cervella-frontend, Miracollo, typescript component")
        results = scorer.rank_lessons(
            test_lessons,
            agent_name="cervella-frontend",
            project="Miracollo",
            task_keywords=extract_keywords("Creare TypeScript component con interface")
        )

        for lesson, score in results:
            print(f"  ✓ {lesson['pattern']}: {score}/100")
            print(f"    - Severity: {lesson['severity']}")
            print(f"    - Agents: {lesson['agents_involved']}")
            print(f"    - Tags: {lesson['tags']}")

        print()

        # Scenario 2: cervella-backend su Contabilità
        print("📋 Scenario 2: cervella-backend, Contabilità, error handling")
        results = scorer.rank_lessons(
            test_lessons,
            agent_name="cervella-backend",
            project="Contabilità",
            task_keywords=extract_keywords("Implement retry logic with error handling")
        )

        for lesson, score in results:
            print(f"  ✓ {lesson['pattern']}: {score}/100")

        print()

        # Test extract_keywords
        print("📋 Test extract_keywords:")
        text = "Create a TypeScript interface with validation for the API endpoint"
        keywords = extract_keywords(text)
        print(f"  Input: {text}")
        print(f"  Keywords: {keywords}")

    else:
        # Modalità interattiva
        scorer = ContextScorer()

        keywords = extract_keywords(args.task) if args.task else None

        print(f"🧠 Context Scorer Ready")
        print(f"  Agent: {args.agent or 'N/A'}")
        print(f"  Project: {args.project or 'N/A'}")
        print(f"  Task keywords: {keywords or 'N/A'}")
        print()
        print("Use Python API to rank lessons:")
        print("  from context_scorer import ContextScorer")
        print("  scorer = ContextScorer()")
        print("  results = scorer.rank_lessons(lessons, agent_name='...', project='...')")


if __name__ == "__main__":
    main()
