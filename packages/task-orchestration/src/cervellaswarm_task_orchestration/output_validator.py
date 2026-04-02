# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""
Output Validator - Reflection pattern for multi-agent output quality.

Validates worker output files for completeness, errors, and quality.
Produces a quality score (0-100) and determines whether retry is needed.
Checks for error markers, incomplete placeholders, and corresponding logs.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
import re

# Error markers to search for in output
ERROR_MARKERS: list[str] = [
    "Error:",
    "ERROR:",
    "Traceback",
    "FAILED",
    "Exception:",
    "RuntimeError:",
    "ValueError:",
    "TypeError:",
    "SyntaxError:",
    "fatal:",
]

# Incomplete markers to search for in output
INCOMPLETE_MARKERS: list[str] = [
    "TODO:",
    "FIXME:",
    "XXX:",
    "HACK:",
]

# Minimum valid output length (characters)
MIN_OUTPUT_LENGTH = 100

# Success indicators (bonus score)
SUCCESS_INDICATORS: list[str] = [
    "DONE",
    "Completed",
    "Success",
    "OK",
    "PASSED",
]


@dataclass
class ValidationResult:
    """Result of output validation."""

    valid: bool = True
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    retry_needed: bool = False
    retry_context: str = ""
    score: int = 100


def _find_incomplete_markers(content: str) -> list[str]:
    """Find INCOMPLETE_MARKERS that appear outside code blocks."""
    found = []
    for marker in INCOMPLETE_MARKERS:
        idx = 0
        while True:
            idx = content.find(marker, idx)
            if idx == -1:
                break
            code_blocks = content[:idx].count("```")
            if code_blocks % 2 == 0:  # Even count = outside code block
                found.append(marker)
                break
            idx += len(marker)
    return found


def validate_output(output_file: Path, logs_dir: Optional[Path] = None) -> ValidationResult:
    """
    Validate a worker output file.

    Performs the following checks:
    1. File exists and is not empty
    2. No error markers in content
    3. No incomplete placeholders (outside code blocks)
    4. Minimum length reached
    5. Corresponding log has no errors (if available)
    6. Success indicators (bonus score)

    Args:
        output_file: Path to the output file.
        logs_dir: Directory to search for corresponding logs.

    Returns:
        ValidationResult with validity, errors, warnings, and score.
    """
    result = ValidationResult()

    # CHECK 1: File exists
    if not output_file.exists():
        result.valid = False
        result.errors.append(f"Output file does not exist: {output_file}")
        result.retry_needed = True
        result.retry_context = "Worker did not create output file. Verify task completion."
        result.score = 0
        return result

    # CHECK 2: File readable and not empty
    try:
        content = output_file.read_text()
    except (OSError, PermissionError, UnicodeDecodeError) as e:
        result.valid = False
        result.errors.append(f"Cannot read output: {e}")
        result.retry_needed = True
        result.retry_context = "Output file corrupted or inaccessible."
        result.score = 0
        return result

    if len(content.strip()) == 0:
        result.valid = False
        result.errors.append("Output is empty!")
        result.retry_needed = True
        result.retry_context = "Worker created output file but it is empty. Task not completed?"
        result.score = 0
        return result

    # CHECK 3: Minimum length
    if len(content) < MIN_OUTPUT_LENGTH:
        result.warnings.append(
            f"Output very short ({len(content)} chars < {MIN_OUTPUT_LENGTH})"
        )
        result.score -= 10

    # CHECK 4: Error markers
    error_found = [m for m in ERROR_MARKERS if m in content]
    if error_found:
        result.valid = False
        result.errors.append(f"Error markers found: {', '.join(error_found)}")
        result.retry_needed = True
        result.retry_context = "Output contains error messages. Task failed?"
        result.score -= 40

    # CHECK 5: Incomplete markers (outside code blocks)
    incomplete_found = _find_incomplete_markers(content)
    if incomplete_found:
        result.warnings.append(
            f"Incomplete markers: {', '.join(incomplete_found)}"
        )
        result.score -= 15

    # CHECK 6: Success indicators (bonus) - use word boundary to avoid false positives
    success_count = sum(
        1 for ind in SUCCESS_INDICATORS if re.search(rf"\b{re.escape(ind)}\b", content)
    )
    if success_count > 0:
        result.score = min(100, result.score + 5)

    # CHECK 7: Corresponding log
    log_check = _check_corresponding_log(output_file, logs_dir)
    if log_check["has_errors"]:
        result.warnings.append(f"Log contains errors: {log_check['error_summary']}")
        result.score -= 10

    # Clamp score to 0-100 range
    result.score = max(0, min(100, result.score))

    # Score-based retry decision
    if result.score < 50:
        result.retry_needed = True
        result.retry_context = f"Low output quality (score: {result.score}). Review recommended."

    if result.errors:
        result.valid = False

    return result


def _check_corresponding_log(
    output_file: Path,
    logs_dir: Optional[Path] = None,
) -> dict:
    """
    Search for a corresponding log file and check for errors.

    Args:
        output_file: Path to the output file.
        logs_dir: Directory to search for logs.

    Returns:
        Dict with has_errors, error_summary, log_file.
    """
    check: dict = {
        "has_errors": False,
        "error_summary": "",
        "log_file": None,
    }

    log_path = logs_dir or Path(".swarm/logs")

    # Extract task_id from filename: TASK_123_output.md -> TASK_123
    task_id = output_file.stem.replace("_output", "")

    if not log_path.exists():
        return check

    matching_logs: list[tuple[Path, float]] = []
    for log_file in log_path.glob("worker_*.log"):
        try:
            log_content = log_file.read_text()
            if task_id in log_content:
                matching_logs.append((log_file, log_file.stat().st_mtime))
        except (OSError, PermissionError):
            continue

    if not matching_logs:
        return check

    latest_log = max(matching_logs, key=lambda x: x[1])[0]
    check["log_file"] = latest_log

    try:
        log_content = latest_log.read_text()
        errors_found = [m for m in ERROR_MARKERS if m in log_content]
        if errors_found:
            check["has_errors"] = True
            check["error_summary"] = f"{len(errors_found)} error markers in log"
    except (OSError, PermissionError):
        pass

    return check


def find_last_output(tasks_dir: Optional[Path] = None) -> Optional[Path]:
    """
    Find the most recently modified output file.

    Args:
        tasks_dir: Directory to search.

    Returns:
        Path to the file or None.
    """
    search_dir = tasks_dir or Path(".swarm/tasks")
    if not search_dir.exists():
        return None

    output_files = list(search_dir.glob("*_output.md"))
    if not output_files:
        return None

    output_files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
    return output_files[0]


def find_task_output(task_id: str, tasks_dir: Optional[Path] = None) -> Optional[Path]:
    """
    Find output file for a specific task.

    Args:
        task_id: Task ID (e.g., TASK_001).
        tasks_dir: Directory to search.

    Returns:
        Path to the file or None.
    """
    # Validate task_id to prevent path traversal (e.g. "../../etc")
    if not task_id or ".." in task_id or "/" in task_id or "\\" in task_id:
        return None

    search_dir = tasks_dir or Path(".swarm/tasks")
    output_file = search_dir / f"{task_id}_output.md"
    return output_file if output_file.exists() else None
