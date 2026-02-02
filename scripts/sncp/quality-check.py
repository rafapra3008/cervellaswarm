#!/usr/bin/env python3
"""Quality checker for PROMPT_RIPRESA files - SNCP 4.0 FASE 2.

Valuta qualità dei PROMPT_RIPRESA su 4 criteri:
- Actionability (30%): TODO chiari e prossimi step
- Specificity (30%): Info precise vs vaghe
- Freshness (20%): Quanto è recente
- Conciseness (20%): Rispetta limiti di righe

Score target: 9.5/10 per tutti i progetti.

Usage:
    ./scripts/sncp/quality-check.py cervellaswarm
    ./scripts/sncp/quality-check.py miracollo
    ./scripts/sncp/quality-check.py contabilita
    ./scripts/sncp/quality-check.py              # tutti
"""

__version__ = "1.0.0"
__version_date__ = "2026-02-02"

import argparse
import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple

# Costanti
SNCP_BASE = Path(".sncp/progetti")
MAX_LINES = 150
WARNING_LINES = 100
WEIGHTS = {
    "actionability": 0.30,
    "specificity": 0.30,
    "freshness": 0.20,
    "conciseness": 0.20
}

# Pattern per analisi
ACTIONABILITY_PATTERNS = [
    r"TODO:",
    r"PROSSIM[IO]",
    r"\[ \]",
    r"DA FARE",
    r"STEP",
    r"NEXT:",
    r"⬜",
    r"\d+\.\s*\[\s*\]",  # 1. [ ] task
]

SPECIFICITY_GOOD = [
    r"\d{4}-\d{2}-\d{2}",  # date YYYY-MM-DD
    r"\d{1,2}\s+(?:Gennaio|Febbraio|Marzo|Aprile|Maggio|Giugno|Luglio|Agosto|Settembre|Ottobre|Novembre|Dicembre)",
    r"v\d+\.\d+\.\d+",     # versioni
    r"\d+\.\d+/10",         # score numerici
    r"\d+/\d+\s+test",      # N/M test
    r":\d{4}",              # porte :8001
    r"\d+%",                # percentuali
]

SPECIFICITY_BAD = [
    r"\bpresto\b",
    r"\bpoi\b",
    r"\bforse\b",
    r"\bvari[eo]?\b",
    r"\bqualche\b",
    r"\brecente\b",
    r"\bmolto\b",
    r"\bprobabile\b",
]


def check_actionability(content: str) -> float:
    """Controlla presenza di TODO chiari e prossimi step.

    Args:
        content: Contenuto del file

    Returns:
        Score 0-10
    """
    score = 0.0
    lines = content.split('\n')
    total_lines = len(lines)

    # Conta match actionability patterns
    action_items = 0
    for pattern in ACTIONABILITY_PATTERNS:
        action_items += len(re.findall(pattern, content, re.IGNORECASE))

    # Score basato su densità di action items
    if total_lines > 0:
        density = action_items / total_lines
        if density >= 0.1:      # 10%+ righe con action items
            score = 10.0
        elif density >= 0.05:   # 5-10%
            score = 8.0
        elif density >= 0.02:   # 2-5%
            score = 6.0
        elif density > 0:       # almeno qualche action item
            score = 4.0
        else:                   # nessun action item
            score = 2.0

    # Bonus se c'è sezione PROSSIMI STEP o NEXT
    if re.search(r"(?:PROSSIM[IO]|NEXT).*STEP", content, re.IGNORECASE):
        score = min(10.0, score + 2.0)

    return score


def check_specificity(content: str) -> float:
    """Controlla specificità delle informazioni.

    Buoni indicatori: date, versioni, numeri, score
    Cattivi indicatori: "presto", "poi", "forse", "vari"

    Args:
        content: Contenuto del file

    Returns:
        Score 0-10
    """
    good_matches = 0
    for pattern in SPECIFICITY_GOOD:
        good_matches += len(re.findall(pattern, content, re.IGNORECASE))

    bad_matches = 0
    for pattern in SPECIFICITY_BAD:
        bad_matches += len(re.findall(pattern, content, re.IGNORECASE))

    total_lines = len(content.split('\n'))
    if total_lines == 0:
        return 0.0

    # Score basato su ratio good/bad
    good_density = good_matches / total_lines
    bad_density = bad_matches / total_lines

    # Penalizza bad matches
    score = 10.0
    score -= bad_density * 20  # -2 punti per ogni 10% di bad matches
    score += good_density * 50  # +5 punti per ogni 10% di good matches

    return max(0.0, min(10.0, score))


def check_freshness(file_path: Path) -> Tuple[float, str]:
    """Controlla quanto è recente il file.

    Args:
        file_path: Path al file da controllare

    Returns:
        Tuple di (score 0-10, data aggiornamento)
    """
    if not file_path.exists():
        return 0.0, "N/A"

    mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
    now = datetime.now()
    days_old = (now - mtime).days

    # Score basato su età
    if days_old < 7:
        score = 10.0
    elif days_old < 14:
        score = 8.0
    elif days_old < 30:
        score = 5.0
    elif days_old < 60:
        score = 3.0
    else:
        score = 2.0

    return score, mtime.strftime("%Y-%m-%d")


def check_conciseness(content: str) -> Tuple[float, List[str]]:
    """Controlla rispetto limiti di righe.

    Args:
        content: Contenuto del file

    Returns:
        Tuple di (score 0-10, lista warnings)
    """
    lines = content.split('\n')
    line_count = len(lines)
    warnings = []

    if line_count < WARNING_LINES:
        score = 10.0
    elif line_count < MAX_LINES:
        score = 8.0
        warnings.append(f"Approaching max lines ({line_count}/{MAX_LINES})")
    elif line_count < MAX_LINES + 50:
        score = 4.0
        warnings.append(f"OVER LIMIT: {line_count} lines (max {MAX_LINES})")
    else:
        score = 0.0
        warnings.append(f"CRITICAL: {line_count} lines (max {MAX_LINES})")

    return score, warnings


def analyze_project(project: str) -> Dict:
    """Analizza un progetto e restituisce risultati.

    Args:
        project: Nome progetto (cervellaswarm, miracollo, contabilita)

    Returns:
        Dizionario con risultati analisi
    """
    file_path = SNCP_BASE / project / f"PROMPT_RIPRESA_{project}.md"

    if not file_path.exists():
        return {
            "project": project,
            "file": str(file_path),
            "status": "ERROR",
            "error": f"File not found: {file_path}"
        }

    # Leggi contenuto
    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception as e:
        return {
            "project": project,
            "file": str(file_path),
            "status": "ERROR",
            "error": f"Cannot read file: {e}"
        }

    # Analisi
    actionability_score = check_actionability(content)
    specificity_score = check_specificity(content)
    freshness_score, updated_date = check_freshness(file_path)
    conciseness_score, warnings = check_conciseness(content)

    # Score totale (media pesata)
    total_score = (
        actionability_score * WEIGHTS["actionability"] +
        specificity_score * WEIGHTS["specificity"] +
        freshness_score * WEIGHTS["freshness"] +
        conciseness_score * WEIGHTS["conciseness"]
    )

    # Determina status
    if total_score >= 9.0:
        status = "EXCELLENT"
    elif total_score >= 7.0:
        status = "PASS"
    elif total_score >= 5.0:
        status = "NEEDS_IMPROVEMENT"
    else:
        status = "FAIL"

    # Suggerimenti
    suggestions = []
    if actionability_score < 7.0:
        suggestions.append("Add more specific TODO items and NEXT steps")
    if specificity_score < 7.0:
        suggestions.append("Replace vague terms (presto, forse) with specific dates/numbers")
    if freshness_score < 7.0:
        suggestions.append("Update file more frequently (currently stale)")
    if warnings:
        suggestions.extend(warnings)

    return {
        "project": project,
        "file": str(file_path),
        "lines": len(content.split('\n')),
        "updated": updated_date,
        "scores": {
            "actionability": round(actionability_score, 1),
            "specificity": round(specificity_score, 1),
            "freshness": round(freshness_score, 1),
            "conciseness": round(conciseness_score, 1)
        },
        "total": round(total_score, 1),
        "status": status,
        "warnings": warnings,
        "suggestions": suggestions
    }


def print_human_readable(results: List[Dict]) -> None:
    """Stampa risultati in formato leggibile.

    Args:
        results: Lista di risultati da stampare
    """
    print("\n" + "="*70)
    print("SNCP 4.0 - PROMPT_RIPRESA Quality Check")
    print("="*70 + "\n")

    for result in results:
        if "error" in result:
            print(f"❌ {result['project']}: {result['error']}\n")
            continue

        # Status emoji
        status_emoji = {
            "EXCELLENT": "🌟",
            "PASS": "✅",
            "NEEDS_IMPROVEMENT": "⚠️",
            "FAIL": "❌"
        }
        emoji = status_emoji.get(result["status"], "❓")

        print(f"{emoji} {result['project'].upper()}")
        print(f"   File: {result['file']}")
        print(f"   Lines: {result['lines']} | Updated: {result['updated']}")
        print(f"\n   Scores:")
        print(f"      Actionability:  {result['scores']['actionability']}/10  (30%)")
        print(f"      Specificity:    {result['scores']['specificity']}/10  (30%)")
        print(f"      Freshness:      {result['scores']['freshness']}/10  (20%)")
        print(f"      Conciseness:    {result['scores']['conciseness']}/10  (20%)")
        print(f"\n   TOTAL: {result['total']}/10 [{result['status']}]")

        if result['suggestions']:
            print(f"\n   Suggestions:")
            for suggestion in result['suggestions']:
                print(f"      • {suggestion}")

        print("\n" + "-"*70 + "\n")


def main():
    """Entry point."""
    parser = argparse.ArgumentParser(
        description="Quality checker for PROMPT_RIPRESA files"
    )
    parser.add_argument(
        "project",
        nargs="?",
        help="Project name (cervellaswarm, miracollo, contabilita). If omitted, checks all."
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output in JSON format"
    )

    args = parser.parse_args()

    # Determina progetti da analizzare
    if args.project:
        projects = [args.project]
    else:
        # Trova tutti i progetti in .sncp/progetti/
        if not SNCP_BASE.exists():
            print(f"ERROR: {SNCP_BASE} not found!", file=sys.stderr)
            sys.exit(1)

        projects = [
            p.name for p in SNCP_BASE.iterdir()
            if p.is_dir() and (p / f"PROMPT_RIPRESA_{p.name}.md").exists()
        ]

    if not projects:
        print("ERROR: No projects found!", file=sys.stderr)
        sys.exit(1)

    # Analizza progetti
    results = [analyze_project(proj) for proj in projects]

    # Output
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print_human_readable(results)

        # Summary
        total_avg = sum(r.get("total", 0) for r in results) / len(results)
        print("="*70)
        print(f"AVERAGE SCORE: {total_avg:.1f}/10")
        print("="*70 + "\n")


if __name__ == "__main__":
    main()
