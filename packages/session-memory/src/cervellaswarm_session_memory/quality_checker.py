# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""
Quality checker for session state files.

Evaluates session state quality on 4 criteria:
- Actionability (30%): Clear TODOs and next steps
- Specificity (30%): Precise info vs vague terms
- Freshness (20%): How recently updated
- Conciseness (20%): Respects line limits

Score target: 8.0/10 by default (configurable).
"""

import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from cervellaswarm_session_memory.config import DEFAULTS, load_config, get_memory_dir

# Patterns that indicate actionable content
ACTIONABILITY_PATTERNS = [
    r"TODO:",
    r"NEXT\b",
    r"\[ \]",
    r"- \[ \]",
    r"\bSTEP\b",
    r"\bACTION\b",
    r"\d+\.\s*\[\s*\]",
]

# Patterns that indicate specific, precise information
SPECIFICITY_GOOD = [
    r"\d{4}-\d{2}-\d{2}",
    r"v\d+\.\d+\.\d+",
    r"\d+\.\d+/10",
    r"\d+/\d+\s+test",
    r":\d{4}",
    r"\d+%",
    r"S\d{3}",
]

# Patterns that indicate vague, imprecise language
SPECIFICITY_BAD = [
    r"\bsoon\b",
    r"\bmaybe\b",
    r"\bprobably\b",
    r"\bsome\b",
    r"\bvarious\b",
    r"\blater\b",
    r"\beventually\b",
]


@dataclass
class QualityResult:
    """Quality check result for a single project."""

    project: str
    file: str
    lines: int
    updated: str
    scores: dict[str, float]
    total: float
    status: str
    warnings: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)


def check_actionability(
    content: str,
    patterns: list[str] | None = None,
) -> float:
    """Check for clear TODOs and next steps.

    Args:
        content: File content to analyze.
        patterns: Custom patterns to look for. Defaults to built-in list.

    Returns:
        Score from 0.0 to 10.0.
    """
    active_patterns = patterns if patterns is not None else ACTIONABILITY_PATTERNS
    lines = content.split("\n")
    total_lines = len(lines)

    if total_lines == 0:
        return 0.0

    action_items = 0
    for pattern in active_patterns:
        action_items += len(re.findall(pattern, content, re.IGNORECASE))

    density = action_items / total_lines
    if density >= 0.10:
        score = 10.0
    elif density >= 0.05:
        score = 8.0
    elif density >= 0.02:
        score = 6.0
    elif density > 0:
        score = 4.0
    else:
        score = 2.0

    # Bonus for explicit NEXT STEPS section
    if re.search(r"NEXT\s+STEPS?", content, re.IGNORECASE):
        score = min(10.0, score + 2.0)

    return score


def check_specificity(
    content: str,
    good_patterns: list[str] | None = None,
    bad_patterns: list[str] | None = None,
) -> float:
    """Check for specific vs vague information.

    Args:
        content: File content to analyze.
        good_patterns: Patterns indicating specificity.
        bad_patterns: Patterns indicating vagueness.

    Returns:
        Score from 0.0 to 10.0.
    """
    good = good_patterns if good_patterns is not None else SPECIFICITY_GOOD
    bad = bad_patterns if bad_patterns is not None else SPECIFICITY_BAD

    total_lines = len(content.split("\n"))
    if total_lines == 0:
        return 0.0

    good_matches = sum(len(re.findall(p, content, re.IGNORECASE)) for p in good)
    bad_matches = sum(len(re.findall(p, content, re.IGNORECASE)) for p in bad)

    good_density = good_matches / total_lines
    bad_density = bad_matches / total_lines

    score = 10.0
    score -= bad_density * 20
    score += good_density * 50

    return max(0.0, min(10.0, score))


def check_freshness(file_path: Path) -> tuple[float, str]:
    """Check how recently the file was updated.

    Args:
        file_path: Path to the file to check.

    Returns:
        Tuple of (score 0-10, last modified date string).
    """
    if not file_path.exists():
        return 0.0, "N/A"

    mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
    now = datetime.now()
    days_old = (now - mtime).days

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


def check_conciseness(
    content: str,
    max_lines: int = 300,
    warning_lines: int = 200,
) -> tuple[float, list[str]]:
    """Check if file respects line limits.

    Args:
        content: File content.
        max_lines: Maximum allowed lines.
        warning_lines: Warning threshold.

    Returns:
        Tuple of (score 0-10, list of warnings).
    """
    line_count = len(content.split("\n"))
    warnings = []

    if line_count < warning_lines:
        score = 10.0
    elif line_count < max_lines:
        score = 8.0
        warnings.append(f"Approaching max lines ({line_count}/{max_lines})")
    elif line_count < max_lines + 50:
        score = 4.0
        warnings.append(f"OVER LIMIT: {line_count} lines (max {max_lines})")
    else:
        score = 0.0
        warnings.append(f"CRITICAL: {line_count} lines (max {max_lines})")

    return score, warnings


def check_quality(
    file_path: Path,
    project_name: str = "",
    weights: dict[str, float] | None = None,
    max_lines: int | None = None,
    warning_lines: int | None = None,
) -> QualityResult:
    """Run a full quality check on a session state file.

    Args:
        file_path: Path to the session state file.
        project_name: Name of the project.
        weights: Custom scoring weights. Defaults to config.
        max_lines: Maximum allowed lines. Defaults to config.
        warning_lines: Warning threshold. Defaults to config.

    Returns:
        QualityResult with scores and suggestions.
    """
    config = load_config()
    quality_config = config.get("quality", DEFAULTS["quality"])

    if weights is None:
        weights = quality_config.get("weights", DEFAULTS["quality"]["weights"])
    if max_lines is None:
        max_lines = config.get("max_lines", DEFAULTS["max_lines"])
    if warning_lines is None:
        warning_lines = config.get("warning_lines", DEFAULTS["warning_lines"])

    if not file_path.exists():
        return QualityResult(
            project=project_name,
            file=str(file_path),
            lines=0,
            updated="N/A",
            scores={},
            total=0.0,
            status="ERROR",
            warnings=[f"File not found: {file_path}"],
        )

    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        return QualityResult(
            project=project_name,
            file=str(file_path),
            lines=0,
            updated="N/A",
            scores={},
            total=0.0,
            status="ERROR",
            warnings=[f"Cannot read file: {e}"],
        )

    actionability_score = check_actionability(content)
    specificity_score = check_specificity(content)
    freshness_score, updated_date = check_freshness(file_path)
    conciseness_score, conciseness_warnings = check_conciseness(content, max_lines, warning_lines)

    total_score = (
        actionability_score * weights.get("actionability", 0.30)
        + specificity_score * weights.get("specificity", 0.30)
        + freshness_score * weights.get("freshness", 0.20)
        + conciseness_score * weights.get("conciseness", 0.20)
    )

    if total_score >= 9.0:
        status = "EXCELLENT"
    elif total_score >= 7.0:
        status = "PASS"
    elif total_score >= 5.0:
        status = "NEEDS_IMPROVEMENT"
    else:
        status = "FAIL"

    suggestions = []
    if actionability_score < 7.0:
        suggestions.append("Add more specific TODO items and NEXT STEPS")
    if specificity_score < 7.0:
        suggestions.append("Replace vague terms (soon, maybe) with specific dates/numbers")
    if freshness_score < 7.0:
        suggestions.append("Update file more frequently (currently stale)")

    return QualityResult(
        project=project_name,
        file=str(file_path),
        lines=len(content.split("\n")),
        updated=updated_date,
        scores={
            "actionability": round(actionability_score, 1),
            "specificity": round(specificity_score, 1),
            "freshness": round(freshness_score, 1),
            "conciseness": round(conciseness_score, 1),
        },
        total=round(total_score, 1),
        status=status,
        warnings=conciseness_warnings,
        suggestions=suggestions,
    )


def check_all_projects(
    base_dir: Path | None = None,
    config: dict | None = None,
) -> list[QualityResult]:
    """Run quality checks on all discovered projects.

    Args:
        base_dir: Base directory. Defaults to CWD.
        config: Pre-loaded config.

    Returns:
        List of QualityResult objects.
    """
    from cervellaswarm_session_memory.project_manager import discover_projects

    projects = discover_projects(base_dir, config)
    return [check_quality(p.state_file, p.name) for p in projects]
