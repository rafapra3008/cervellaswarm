#!/usr/bin/env python3
"""
Task Classifier - Determina se un task richiede planning (architect)

W3-B REQ-14: Threshold task complesso
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional
import re


class TaskComplexity(Enum):
    """Livelli di complessita task."""
    SIMPLE = "simple"      # No architect needed
    MEDIUM = "medium"      # Consider architect
    COMPLEX = "complex"    # Architect recommended
    CRITICAL = "critical"  # Architect required


@dataclass
class ClassificationResult:
    """Risultato classificazione task."""
    complexity: TaskComplexity
    should_architect: bool
    confidence: float  # 0.0 - 1.0
    triggers: list[str]  # Quali criteri hanno matchato
    reasoning: str


# Keywords che suggeriscono task complesso
COMPLEXITY_KEYWORDS = {
    # High complexity triggers
    "refactor": 0.8,
    "architecture": 0.9,
    "redesign": 0.8,
    "migrate": 0.7,
    "restructure": 0.8,
    "rewrite": 0.7,

    # Medium complexity triggers
    "complex": 0.6,
    "multiple files": 0.5,
    "across modules": 0.6,
    "cross-cutting": 0.6,
    "breaking change": 0.7,

    # Pattern triggers
    "integrate": 0.5,
    "implement feature": 0.5,
    "add new": 0.4,
    "create system": 0.6,
}

# Keywords che suggeriscono task semplice
SIMPLE_KEYWORDS = [
    "fix typo",
    "update comment",
    "change text",
    "rename",
    "minor",
    "small",
    "quick",
    "simple",
    "adjust",
    "tweak",
]

# Patterns che indicano multi-file
MULTIFILE_PATTERNS = [
    r"multiple\s+files?",
    r"across\s+\w+",
    r"all\s+\w+\s+files?",
    r"every\s+\w+",
    r"entire\s+(module|system|codebase)",
    r"\d+\s+files?",  # "5 files"
]


def estimate_files_affected(task_description: str) -> int:
    """
    Stima quanti file saranno affetti dal task.

    Returns:
        Numero stimato di file (1-20+)
    """
    desc_lower = task_description.lower()

    # Cerca numeri espliciti
    number_match = re.search(r"(\d+)\s+files?", desc_lower)
    if number_match:
        return int(number_match.group(1))

    # Keywords che suggeriscono molti file
    if any(kw in desc_lower for kw in ["entire", "all", "every", "codebase"]):
        return 10

    if any(kw in desc_lower for kw in ["multiple", "several", "various"]):
        return 5

    if any(kw in desc_lower for kw in ["both", "two"]):
        return 2

    # Default: 1 file
    return 1


def calculate_keyword_score(task_description: str) -> tuple[float, list[str]]:
    """
    Calcola score basato su keywords trovate.

    Returns:
        (score 0.0-1.0, lista keyword matchate)
    """
    desc_lower = task_description.lower()
    matched = []
    total_score = 0.0

    for keyword, weight in COMPLEXITY_KEYWORDS.items():
        if keyword in desc_lower:
            matched.append(keyword)
            total_score += weight

    # Normalizza score (max 1.0)
    normalized = min(total_score / 2.0, 1.0)

    return normalized, matched


def is_simple_task(task_description: str) -> bool:
    """Verifica se il task e chiaramente semplice."""
    desc_lower = task_description.lower()
    return any(kw in desc_lower for kw in SIMPLE_KEYWORDS)


def has_multifile_pattern(task_description: str) -> bool:
    """Verifica se ci sono pattern multi-file."""
    desc_lower = task_description.lower()
    return any(re.search(pattern, desc_lower) for pattern in MULTIFILE_PATTERNS)


def classify_task(
    task_description: str,
    estimated_files: Optional[int] = None,
    has_breaking_changes: bool = False,
    force_architect: bool = False
) -> ClassificationResult:
    """
    Classifica un task per determinare se richiede planning.

    Args:
        task_description: Descrizione del task
        estimated_files: Numero file (se noto), altrimenti stimato
        has_breaking_changes: Se il task ha breaking changes note
        force_architect: Forza attivazione architect

    Returns:
        ClassificationResult con decisione e reasoning
    """
    triggers = []

    # Force override
    if force_architect:
        return ClassificationResult(
            complexity=TaskComplexity.COMPLEX,
            should_architect=True,
            confidence=1.0,
            triggers=["force_architect=True"],
            reasoning="Architect forzato dall'utente"
        )

    # Check se task semplice
    if is_simple_task(task_description):
        return ClassificationResult(
            complexity=TaskComplexity.SIMPLE,
            should_architect=False,
            confidence=0.9,
            triggers=["simple_keyword_detected"],
            reasoning="Task contiene keyword di task semplice"
        )

    # Calcola score keywords
    keyword_score, matched_keywords = calculate_keyword_score(task_description)
    if matched_keywords:
        triggers.extend(matched_keywords)

    # Stima file affetti
    files = estimated_files or estimate_files_affected(task_description)

    # Multi-file pattern check
    if has_multifile_pattern(task_description):
        triggers.append("multifile_pattern")
        files = max(files, 3)  # Almeno 3 se pattern multi-file

    # Breaking changes
    if has_breaking_changes:
        triggers.append("breaking_changes")
        keyword_score += 0.3

    # File count scoring
    file_score = 0.0
    if files >= 5:
        file_score = 0.8
        triggers.append(f"files>5 ({files})")
    elif files >= 3:
        file_score = 0.5
        triggers.append(f"files>3 ({files})")

    # Calcola score finale
    final_score = min((keyword_score + file_score) / 1.5, 1.0)

    # Determina complexity e decisione
    if final_score >= 0.7:
        complexity = TaskComplexity.CRITICAL
        should_architect = True
        reasoning = "Task critico - richiede planning dettagliato"
    elif final_score >= 0.5:
        complexity = TaskComplexity.COMPLEX
        should_architect = True
        reasoning = "Task complesso - architect raccomandato"
    elif final_score >= 0.3:
        complexity = TaskComplexity.MEDIUM
        should_architect = False  # Opzionale per medium
        reasoning = "Task medio - architect opzionale"
    else:
        complexity = TaskComplexity.SIMPLE
        should_architect = False
        reasoning = "Task semplice - procedi direttamente"

    return ClassificationResult(
        complexity=complexity,
        should_architect=should_architect,
        confidence=final_score,
        triggers=triggers if triggers else ["no_triggers"],
        reasoning=reasoning
    )


def should_use_architect(task_description: str) -> bool:
    """
    Shortcut per check rapido.

    Returns:
        True se architect raccomandato
    """
    result = classify_task(task_description)
    return result.should_architect


# CLI interface
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python task_classifier.py '<task description>'")
        print("\nExamples:")
        print("  python task_classifier.py 'refactor authentication module'")
        print("  python task_classifier.py 'fix typo in README'")
        sys.exit(1)

    task = " ".join(sys.argv[1:])
    result = classify_task(task)

    print(f"\nTask: {task}")
    print(f"{'='*60}")
    print(f"Complexity:      {result.complexity.value}")
    print(f"Should Architect: {result.should_architect}")
    print(f"Confidence:      {result.confidence:.2f}")
    print(f"Triggers:        {', '.join(result.triggers)}")
    print(f"Reasoning:       {result.reasoning}")
