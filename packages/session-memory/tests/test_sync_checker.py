# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for cervellaswarm_session_memory.sync_checker."""

import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from cervellaswarm_session_memory.sync_checker import (
    CheckStatus,
    SyncResult,
    check_file_size,
    check_git_uncommitted,
    check_state_freshness,
    check_state_in_git,
    verify_all,
    verify_project,
)


# ---------------------------------------------------------------------------
# CheckStatus enum values
# ---------------------------------------------------------------------------


def test_check_status_values():
    """CheckStatus enum has the correct string values."""
    assert CheckStatus.OK.value == "ok"
    assert CheckStatus.WARNING.value == "warning"
    assert CheckStatus.ERROR.value == "error"


# ---------------------------------------------------------------------------
# SyncResult.overall property
# ---------------------------------------------------------------------------


def test_sync_result_overall_ok():
    """overall is OK when all checks are OK."""
    result = SyncResult(
        project="demo",
        checks={"freshness": CheckStatus.OK, "size": CheckStatus.OK},
    )
    assert result.overall == CheckStatus.OK


def test_sync_result_overall_warning():
    """overall is WARNING when at least one check is WARNING and none are ERROR."""
    result = SyncResult(
        project="demo",
        checks={"freshness": CheckStatus.OK, "size": CheckStatus.WARNING},
    )
    assert result.overall == CheckStatus.WARNING


def test_sync_result_overall_error():
    """overall is ERROR when at least one check is ERROR."""
    result = SyncResult(
        project="demo",
        checks={"freshness": CheckStatus.ERROR, "size": CheckStatus.WARNING},
    )
    assert result.overall == CheckStatus.ERROR


# ---------------------------------------------------------------------------
# check_state_freshness
# ---------------------------------------------------------------------------


def test_freshness_recent(tmp_path):
    """A file modified today returns OK status."""
    f = tmp_path / "state.md"
    f.write_text("# State\n", encoding="utf-8")
    status, msg = check_state_freshness(f)
    assert status == CheckStatus.OK


def test_freshness_warning(tmp_path):
    """A file modified 5 days ago returns WARNING status."""
    f = tmp_path / "state.md"
    f.write_text("# State\n", encoding="utf-8")
    old_time = (datetime.now() - timedelta(days=5)).timestamp()
    import os
    os.utime(f, (old_time, old_time))
    status, msg = check_state_freshness(f)
    assert status == CheckStatus.WARNING


def test_freshness_error(tmp_path):
    """A file modified 10 days ago returns ERROR status."""
    f = tmp_path / "state.md"
    f.write_text("# State\n", encoding="utf-8")
    old_time = (datetime.now() - timedelta(days=10)).timestamp()
    import os
    os.utime(f, (old_time, old_time))
    status, msg = check_state_freshness(f)
    assert status == CheckStatus.ERROR


def test_freshness_custom_thresholds(tmp_path):
    """Custom max_days and warn_days are respected."""
    f = tmp_path / "state.md"
    f.write_text("# State\n", encoding="utf-8")
    old_time = (datetime.now() - timedelta(days=2)).timestamp()
    import os
    os.utime(f, (old_time, old_time))
    # With warn_days=1, a 2-day-old file should be WARNING or ERROR
    status, msg = check_state_freshness(f, max_days=5, warn_days=1)
    assert status in (CheckStatus.WARNING, CheckStatus.ERROR)


def test_freshness_missing():
    """A missing file returns ERROR status."""
    status, msg = check_state_freshness(Path("/nonexistent/state.md"))
    assert status == CheckStatus.ERROR
    assert "not found" in msg.lower()


# ---------------------------------------------------------------------------
# check_file_size
# ---------------------------------------------------------------------------


def test_file_size_ok(tmp_path):
    """A file with 50 lines returns OK status."""
    f = tmp_path / "state.md"
    f.write_text("\n".join(["line"] * 50), encoding="utf-8")
    status, msg = check_file_size(f)
    assert status == CheckStatus.OK


def test_file_size_warning(tmp_path):
    """A file with 250 lines returns WARNING status."""
    f = tmp_path / "state.md"
    f.write_text("\n".join(["line"] * 250), encoding="utf-8")
    status, msg = check_file_size(f)
    assert status == CheckStatus.WARNING


def test_file_size_error(tmp_path):
    """A file with 350 lines returns ERROR status."""
    f = tmp_path / "state.md"
    f.write_text("\n".join(["line"] * 350), encoding="utf-8")
    status, msg = check_file_size(f)
    assert status == CheckStatus.ERROR


def test_file_size_custom_limits(tmp_path):
    """Custom max_lines and warning_lines are respected."""
    f = tmp_path / "state.md"
    f.write_text("\n".join(["line"] * 15), encoding="utf-8")
    # With warning_lines=10, max_lines=20 -> 15 lines should be WARNING
    status, msg = check_file_size(f, max_lines=20, warning_lines=10)
    assert status == CheckStatus.WARNING


def test_file_size_missing():
    """A missing file returns ERROR status."""
    status, msg = check_file_size(Path("/nonexistent/state.md"))
    assert status == CheckStatus.ERROR
    assert "not found" in msg.lower()


# ---------------------------------------------------------------------------
# check_git_uncommitted
# ---------------------------------------------------------------------------


def test_git_uncommitted_clean(tmp_path):
    """A clean git working tree returns OK status."""
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = ""

    with patch("cervellaswarm_session_memory.sync_checker.subprocess.run", return_value=mock_result):
        status, msg = check_git_uncommitted(tmp_path)

    assert status == CheckStatus.OK
    assert "clean" in msg.lower()


def test_git_uncommitted_changes(tmp_path):
    """A dirty git working tree returns WARNING status."""
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = " M file.md\n M other.md\n"

    with patch("cervellaswarm_session_memory.sync_checker.subprocess.run", return_value=mock_result):
        status, msg = check_git_uncommitted(tmp_path)

    assert status == CheckStatus.WARNING
    assert "2" in msg


def test_git_not_available(tmp_path):
    """FileNotFoundError (git not installed) returns WARNING."""
    with patch(
        "cervellaswarm_session_memory.sync_checker.subprocess.run",
        side_effect=FileNotFoundError,
    ):
        status, msg = check_git_uncommitted(tmp_path)

    assert status == CheckStatus.WARNING
    assert "not available" in msg.lower()


def test_git_timeout(tmp_path):
    """subprocess.TimeoutExpired returns WARNING."""
    with patch(
        "cervellaswarm_session_memory.sync_checker.subprocess.run",
        side_effect=subprocess.TimeoutExpired(cmd="git", timeout=10),
    ):
        status, msg = check_git_uncommitted(tmp_path)

    assert status == CheckStatus.WARNING
    assert "timed out" in msg.lower()


def test_git_not_repo(tmp_path):
    """A non-zero returncode (not a git repo) returns WARNING."""
    mock_result = MagicMock()
    mock_result.returncode = 128
    mock_result.stdout = ""

    with patch("cervellaswarm_session_memory.sync_checker.subprocess.run", return_value=mock_result):
        status, msg = check_git_uncommitted(tmp_path)

    assert status == CheckStatus.WARNING
    assert "repository" in msg.lower()


# ---------------------------------------------------------------------------
# check_state_in_git
# ---------------------------------------------------------------------------


def test_state_in_git_tracked(tmp_path):
    """A tracked state file returns OK status."""
    f = tmp_path / "state.md"
    f.write_text("# State\n", encoding="utf-8")

    mock_result = MagicMock()
    mock_result.returncode = 0

    with patch("cervellaswarm_session_memory.sync_checker.subprocess.run", return_value=mock_result):
        status, msg = check_state_in_git(f, tmp_path)

    assert status == CheckStatus.OK
    assert "tracked" in msg.lower()


def test_state_in_git_untracked(tmp_path):
    """An untracked state file returns WARNING status."""
    f = tmp_path / "state.md"
    f.write_text("# State\n", encoding="utf-8")

    mock_result = MagicMock()
    mock_result.returncode = 1

    with patch("cervellaswarm_session_memory.sync_checker.subprocess.run", return_value=mock_result):
        status, msg = check_state_in_git(f, tmp_path)

    assert status == CheckStatus.WARNING
    assert "not tracked" in msg.lower()


def test_state_in_git_no_git(tmp_path):
    """FileNotFoundError (git not installed) returns WARNING."""
    f = tmp_path / "state.md"
    f.write_text("# State\n", encoding="utf-8")

    with patch(
        "cervellaswarm_session_memory.sync_checker.subprocess.run",
        side_effect=FileNotFoundError,
    ):
        status, msg = check_state_in_git(f, tmp_path)

    assert status == CheckStatus.WARNING


def test_state_in_git_missing_file(tmp_path):
    """A missing state file returns ERROR status without calling git."""
    f = tmp_path / "nonexistent_state.md"
    status, msg = check_state_in_git(f, tmp_path)
    assert status == CheckStatus.ERROR
    assert "does not exist" in msg.lower()


# ---------------------------------------------------------------------------
# verify_project
# ---------------------------------------------------------------------------


def test_verify_project_not_found(tmp_path):
    """A project that does not exist returns ERROR status."""
    result = verify_project("ghost-project", base_dir=tmp_path)
    assert result.checks.get("exists") == CheckStatus.ERROR
    assert result.overall == CheckStatus.ERROR
    assert any("not found" in e for e in result.errors)


def test_verify_project_all_ok(tmp_path, monkeypatch):
    """A freshly initialized project passes all checks (with mocked git)."""
    from cervellaswarm_session_memory.project_manager import init_project

    monkeypatch.chdir(tmp_path)

    # Initialize a real project so discover_projects works
    init_project(name="my-project", project_root=tmp_path)

    # Mock both git calls to return clean/tracked
    clean_mock = MagicMock()
    clean_mock.returncode = 0
    clean_mock.stdout = ""

    with patch(
        "cervellaswarm_session_memory.sync_checker.subprocess.run", return_value=clean_mock
    ):
        result = verify_project("my-project", base_dir=tmp_path)

    assert result.checks.get("exists") == CheckStatus.OK
    assert result.overall in (CheckStatus.OK, CheckStatus.WARNING)


# ---------------------------------------------------------------------------
# verify_all
# ---------------------------------------------------------------------------


def test_verify_all_empty(tmp_path, monkeypatch):
    """verify_all returns an empty list when there are no projects."""
    monkeypatch.chdir(tmp_path)
    results = verify_all(base_dir=tmp_path)
    assert results == []


def test_verify_all_multiple(tmp_path, monkeypatch):
    """verify_all returns one SyncResult per discovered project."""
    from cervellaswarm_session_memory.project_manager import init_project

    monkeypatch.chdir(tmp_path)
    init_project(name="alpha", project_root=tmp_path)
    init_project(name="beta", project_root=tmp_path)

    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = ""

    with patch(
        "cervellaswarm_session_memory.sync_checker.subprocess.run", return_value=mock_result
    ):
        results = verify_all(base_dir=tmp_path)

    project_names = {r.project for r in results}
    assert "alpha" in project_names
    assert "beta" in project_names
    assert len(results) == 2
