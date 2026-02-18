# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for cervellaswarm_task_orchestration.output_validator."""

import time
import pytest
from pathlib import Path

from cervellaswarm_task_orchestration.output_validator import (
    validate_output,
    find_last_output,
    find_task_output,
    ValidationResult,
    _check_corresponding_log,
    MIN_OUTPUT_LENGTH,
    ERROR_MARKERS,
    INCOMPLETE_MARKERS,
    SUCCESS_INDICATORS,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

LONG_OK = "This output is complete and valid. " * 10  # >100 chars, no markers


def write_output(path: Path, content: str) -> Path:
    path.write_text(content)
    return path


# ---------------------------------------------------------------------------
# ValidationResult dataclass
# ---------------------------------------------------------------------------


def test_validation_result_defaults():
    r = ValidationResult()
    assert r.valid is True
    assert r.errors == []
    assert r.warnings == []
    assert r.retry_needed is False
    assert r.retry_context == ""
    assert r.score == 100


def test_validation_result_custom_values():
    r = ValidationResult(valid=False, score=30, retry_needed=True)
    assert r.valid is False
    assert r.score == 30
    assert r.retry_needed is True


# ---------------------------------------------------------------------------
# validate_output - file not exists
# ---------------------------------------------------------------------------


def test_validate_output_file_not_exists(tmp_path):
    result = validate_output(tmp_path / "missing.md")
    assert result.valid is False
    assert result.retry_needed is True
    assert result.score == 0
    assert any("does not exist" in e for e in result.errors)


# ---------------------------------------------------------------------------
# validate_output - empty file
# ---------------------------------------------------------------------------


def test_validate_output_empty_file(tmp_path):
    f = tmp_path / "TASK_001_output.md"
    f.write_text("   ")  # only whitespace
    result = validate_output(f)
    assert result.valid is False
    assert result.retry_needed is True
    assert result.score == 0
    assert any("empty" in e.lower() for e in result.errors)


# ---------------------------------------------------------------------------
# validate_output - valid clean output
# ---------------------------------------------------------------------------


def test_validate_output_valid_clean(tmp_path):
    f = write_output(tmp_path / "TASK_001_output.md", LONG_OK)
    result = validate_output(f)
    assert result.valid is True
    assert result.errors == []
    assert result.score >= 90
    assert result.retry_needed is False


def test_validate_output_score_starts_at_100(tmp_path):
    f = write_output(tmp_path / "TASK_001_output.md", LONG_OK)
    result = validate_output(f)
    assert result.score <= 100


# ---------------------------------------------------------------------------
# validate_output - error markers
# ---------------------------------------------------------------------------


def test_validate_output_detects_error_marker_Error(tmp_path):
    content = LONG_OK + "\nError: something went wrong\n"
    f = write_output(tmp_path / "TASK_001_output.md", content)
    result = validate_output(f)
    assert result.valid is False
    assert result.retry_needed is True
    assert result.score <= 60


def test_validate_output_detects_traceback(tmp_path):
    content = LONG_OK + "\nTraceback (most recent call last):\n"
    f = write_output(tmp_path / "TASK_001_output.md", content)
    result = validate_output(f)
    assert result.valid is False
    assert any("Traceback" in e for e in result.errors)


def test_validate_output_detects_FAILED(tmp_path):
    content = LONG_OK + "\nFAILED - tests didn't pass\n"
    f = write_output(tmp_path / "TASK_001_output.md", content)
    result = validate_output(f)
    assert result.valid is False


def test_validate_output_score_reduced_by_error_markers(tmp_path):
    content = LONG_OK + "\nError: oops\n"
    f = write_output(tmp_path / "TASK_001_output.md", content)
    result = validate_output(f)
    assert result.score <= 60  # reduced by at least 40


# ---------------------------------------------------------------------------
# validate_output - incomplete markers
# ---------------------------------------------------------------------------


def test_validate_output_detects_TODO_outside_code_block(tmp_path):
    content = LONG_OK + "\nTODO: finish this section\n"
    f = write_output(tmp_path / "TASK_001_output.md", content)
    result = validate_output(f)
    assert any("TODO:" in w for w in result.warnings)
    assert result.score < 100


def test_validate_output_detects_FIXME_outside_code_block(tmp_path):
    content = LONG_OK + "\nFIXME: this is broken\n"
    f = write_output(tmp_path / "TASK_001_output.md", content)
    result = validate_output(f)
    assert any("FIXME:" in w for w in result.warnings)


def test_validate_output_ignores_incomplete_inside_code_block(tmp_path):
    # TODO: inside a code block - should be ignored
    content = LONG_OK + "\n```python\n# TODO: refactor later\n```\n"
    f = write_output(tmp_path / "TASK_001_output.md", content)
    result = validate_output(f)
    # The TODO inside code block should NOT appear in warnings
    assert not any("TODO:" in w for w in result.warnings)


def test_validate_output_incomplete_inside_closed_code_block(tmp_path):
    # Two code fences before TODO = outside code block
    content = LONG_OK + "\n```\nsome code\n```\nTODO: do this\n"
    f = write_output(tmp_path / "TASK_001_output.md", content)
    result = validate_output(f)
    assert any("TODO:" in w for w in result.warnings)


def test_validate_output_score_reduced_by_incomplete_markers(tmp_path):
    content = LONG_OK + "\nTODO: finish me\n"
    f = write_output(tmp_path / "TASK_001_output.md", content)
    result = validate_output(f)
    assert result.score <= 85  # reduced by at least 15


# ---------------------------------------------------------------------------
# validate_output - minimum length
# ---------------------------------------------------------------------------


def test_validate_output_short_output_warning(tmp_path):
    short = "Short output, not enough."  # < MIN_OUTPUT_LENGTH
    assert len(short) < MIN_OUTPUT_LENGTH
    f = write_output(tmp_path / "TASK_001_output.md", short)
    result = validate_output(f)
    assert any("short" in w.lower() for w in result.warnings)
    assert result.score <= 90


def test_validate_output_exact_min_length_no_warning(tmp_path):
    content = "A" * MIN_OUTPUT_LENGTH
    f = write_output(tmp_path / "TASK_001_output.md", content)
    result = validate_output(f)
    assert not any("short" in w.lower() for w in result.warnings)


# ---------------------------------------------------------------------------
# validate_output - success indicators bonus
# ---------------------------------------------------------------------------


def test_validate_output_success_indicator_DONE(tmp_path):
    content = LONG_OK + " DONE - all checks completed."
    f = write_output(tmp_path / "TASK_001_output.md", content)
    result = validate_output(f)
    # Score should not drop below 100 (or even get bonus up to 100)
    assert result.score >= 95


def test_validate_output_success_indicator_PASSED(tmp_path):
    content = LONG_OK + " PASSED all tests."
    f = write_output(tmp_path / "TASK_001_output.md", content)
    result = validate_output(f)
    assert result.score >= 95


# ---------------------------------------------------------------------------
# validate_output - score and retry_needed
# ---------------------------------------------------------------------------


def test_validate_output_score_perfect_clean(tmp_path):
    f = write_output(tmp_path / "TASK_001_output.md", LONG_OK)
    result = validate_output(f)
    assert result.score >= 90
    assert result.retry_needed is False


def test_validate_output_retry_needed_when_score_below_50(tmp_path):
    # Error marker causes score drop >= 40
    content = LONG_OK + "\nError: bad thing\nTraceback\nFAILED\n"
    f = write_output(tmp_path / "TASK_001_output.md", content)
    result = validate_output(f)
    if result.score < 50:
        assert result.retry_needed is True


def test_validate_output_with_warnings_valid_still_true(tmp_path):
    content = LONG_OK + "\nTODO: minor cleanup later\n"
    f = write_output(tmp_path / "TASK_001_output.md", content)
    result = validate_output(f)
    # Warnings alone don't make it invalid
    assert result.valid is True


# ---------------------------------------------------------------------------
# _check_corresponding_log
# ---------------------------------------------------------------------------


def test_check_log_no_logs_dir(tmp_path):
    output_file = tmp_path / "TASK_001_output.md"
    output_file.write_text(LONG_OK)
    result = _check_corresponding_log(output_file, logs_dir=tmp_path / "nonexistent_logs")
    assert result["has_errors"] is False
    assert result["log_file"] is None


def test_check_log_no_matching_log(tmp_path):
    logs_dir = tmp_path / "logs"
    logs_dir.mkdir()
    # Log exists but does not mention the task
    log = logs_dir / "worker_1.log"
    log.write_text("Everything went fine for TASK_999\n")

    output_file = tmp_path / "TASK_001_output.md"
    output_file.write_text(LONG_OK)
    result = _check_corresponding_log(output_file, logs_dir=logs_dir)
    assert result["has_errors"] is False
    assert result["log_file"] is None


def test_check_log_matching_log_with_errors(tmp_path):
    logs_dir = tmp_path / "logs"
    logs_dir.mkdir()
    log = logs_dir / "worker_1.log"
    log.write_text("Processing TASK_001\nError: something failed\n")

    output_file = tmp_path / "TASK_001_output.md"
    output_file.write_text(LONG_OK)
    result = _check_corresponding_log(output_file, logs_dir=logs_dir)
    assert result["has_errors"] is True
    assert result["log_file"] == log
    assert "error" in result["error_summary"].lower()


def test_check_log_matching_log_no_errors(tmp_path):
    logs_dir = tmp_path / "logs"
    logs_dir.mkdir()
    log = logs_dir / "worker_1.log"
    log.write_text("Processing TASK_001\nAll done successfully.\n")

    output_file = tmp_path / "TASK_001_output.md"
    output_file.write_text(LONG_OK)
    result = _check_corresponding_log(output_file, logs_dir=logs_dir)
    assert result["has_errors"] is False


def test_check_log_picks_latest_when_multiple(tmp_path):
    logs_dir = tmp_path / "logs"
    logs_dir.mkdir()

    old_log = logs_dir / "worker_1.log"
    old_log.write_text("TASK_001 processed - Error: old failure\n")
    time.sleep(0.01)
    new_log = logs_dir / "worker_2.log"
    new_log.write_text("TASK_001 - all OK, no problems\n")

    output_file = tmp_path / "TASK_001_output.md"
    output_file.write_text(LONG_OK)
    result = _check_corresponding_log(output_file, logs_dir=logs_dir)
    # Should pick the newest log (no errors)
    assert result["log_file"] == new_log


# ---------------------------------------------------------------------------
# find_last_output
# ---------------------------------------------------------------------------


def test_find_last_output_no_dir(tmp_path):
    result = find_last_output(tasks_dir=tmp_path / "nonexistent")
    assert result is None


def test_find_last_output_empty_dir(tmp_path):
    result = find_last_output(tasks_dir=tmp_path)
    assert result is None


def test_find_last_output_single_file(tmp_path):
    f = tmp_path / "TASK_001_output.md"
    f.write_text(LONG_OK)
    result = find_last_output(tasks_dir=tmp_path)
    assert result == f


def test_find_last_output_returns_most_recent(tmp_path):
    f1 = tmp_path / "TASK_001_output.md"
    f1.write_text(LONG_OK)
    time.sleep(0.01)
    f2 = tmp_path / "TASK_002_output.md"
    f2.write_text(LONG_OK)
    result = find_last_output(tasks_dir=tmp_path)
    assert result == f2


def test_find_last_output_ignores_non_output_files(tmp_path):
    (tmp_path / "TASK_001.md").write_text("task file")
    (tmp_path / "TASK_001.ready").touch()
    result = find_last_output(tasks_dir=tmp_path)
    assert result is None


# ---------------------------------------------------------------------------
# find_task_output
# ---------------------------------------------------------------------------


def test_find_task_output_found(tmp_path):
    f = tmp_path / "TASK_001_output.md"
    f.write_text(LONG_OK)
    result = find_task_output("TASK_001", tasks_dir=tmp_path)
    assert result == f


def test_find_task_output_not_found(tmp_path):
    result = find_task_output("TASK_999", tasks_dir=tmp_path)
    assert result is None


def test_find_task_output_does_not_confuse_similar_names(tmp_path):
    (tmp_path / "TASK_001_output.md").write_text(LONG_OK)
    result = find_task_output("TASK_00", tasks_dir=tmp_path)
    assert result is None
