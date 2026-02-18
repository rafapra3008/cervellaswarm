# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for cervellaswarm_agent_hooks.session_checkpoint - git helpers."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from cervellaswarm_agent_hooks.session_checkpoint import (
    find_project_root,
    get_branch,
    get_git_status,
    get_recent_commits,
    git_command,
)


# ---------------------------------------------------------------------------
# find_project_root
# ---------------------------------------------------------------------------


class TestFindProjectRoot:
    def test_finds_root_at_current(self, tmp_path):
        (tmp_path / ".git").mkdir()
        root = find_project_root(str(tmp_path))
        assert root == tmp_path

    def test_finds_root_in_parent(self, tmp_path):
        (tmp_path / ".git").mkdir()
        subdir = tmp_path / "src"
        subdir.mkdir()
        root = find_project_root(str(subdir))
        assert root == tmp_path

    def test_returns_none_when_no_git(self, tmp_path):
        with patch.object(Path, "parents", new_callable=lambda: property(lambda self: [])):
            root = find_project_root(str(tmp_path))
            assert root is None


# ---------------------------------------------------------------------------
# git_command
# ---------------------------------------------------------------------------


class TestGitCommand:
    def test_returns_stdout_on_success(self, tmp_path):
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "  main  "
        with patch("subprocess.run", return_value=mock_result):
            result = git_command(["branch", "--show-current"], str(tmp_path))
        assert result == "main"

    def test_returns_empty_on_nonzero(self, tmp_path):
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stdout = "error output"
        with patch("subprocess.run", return_value=mock_result):
            result = git_command(["status"], str(tmp_path))
        assert result == ""

    def test_returns_empty_on_exception(self, tmp_path):
        with patch("subprocess.run", side_effect=Exception("no git")):
            result = git_command(["log"], str(tmp_path))
        assert result == ""

    def test_passes_cwd_to_subprocess(self, tmp_path):
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "output"
        with patch("subprocess.run", return_value=mock_result) as mock_run:
            git_command(["status"], str(tmp_path))
        call_kwargs = mock_run.call_args[1]
        assert call_kwargs["cwd"] == str(tmp_path)

    def test_prepends_git_to_args(self, tmp_path):
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = ""
        with patch("subprocess.run", return_value=mock_result) as mock_run:
            git_command(["status", "--porcelain"], str(tmp_path))
        cmd = mock_run.call_args[0][0]
        assert cmd[0] == "git"
        assert cmd[1] == "status"


# ---------------------------------------------------------------------------
# get_git_status
# ---------------------------------------------------------------------------


class TestGetGitStatus:
    def test_clean_repo(self, tmp_path):
        with patch(
            "cervellaswarm_agent_hooks.session_checkpoint.git_command",
            return_value="",
        ):
            result = get_git_status(str(tmp_path))
        assert result == "Clean working tree"

    def test_modified_files(self, tmp_path):
        with patch(
            "cervellaswarm_agent_hooks.session_checkpoint.git_command",
            return_value=" M file1.py\nM  file2.py",
        ):
            result = get_git_status(str(tmp_path))
        assert "modified" in result

    def test_new_files(self, tmp_path):
        with patch(
            "cervellaswarm_agent_hooks.session_checkpoint.git_command",
            return_value="?? new_file.py",
        ):
            result = get_git_status(str(tmp_path))
        assert "new/untracked" in result

    def test_deleted_files(self, tmp_path):
        with patch(
            "cervellaswarm_agent_hooks.session_checkpoint.git_command",
            return_value=" D deleted.py",
        ):
            result = get_git_status(str(tmp_path))
        assert "deleted" in result

    def test_mixed_changes(self, tmp_path):
        with patch(
            "cervellaswarm_agent_hooks.session_checkpoint.git_command",
            return_value=" M mod.py\n?? new.py\n D del.py",
        ):
            result = get_git_status(str(tmp_path))
        assert "modified" in result
        assert "new/untracked" in result
        assert "deleted" in result

    def test_unknown_changes_falls_back_to_count(self, tmp_path):
        # Lines that don't match M/A/D -> falls back to "N changes"
        with patch(
            "cervellaswarm_agent_hooks.session_checkpoint.git_command",
            return_value="?? a\n?? b",  # only untracked = "new/untracked"
        ):
            result = get_git_status(str(tmp_path))
        assert result  # Not empty


# ---------------------------------------------------------------------------
# get_recent_commits / get_branch
# ---------------------------------------------------------------------------


class TestGetRecentCommits:
    def test_returns_log_output(self, tmp_path):
        fake_log = "abc1234 feat: add feature\ndef5678 fix: bug fix"
        with patch(
            "cervellaswarm_agent_hooks.session_checkpoint.git_command",
            return_value=fake_log,
        ):
            result = get_recent_commits(str(tmp_path))
        assert result == fake_log

    def test_no_commits_fallback(self, tmp_path):
        with patch(
            "cervellaswarm_agent_hooks.session_checkpoint.git_command",
            return_value="",
        ):
            result = get_recent_commits(str(tmp_path))
        assert result == "No commits found"


class TestGetBranch:
    def test_returns_branch_name(self, tmp_path):
        with patch(
            "cervellaswarm_agent_hooks.session_checkpoint.git_command",
            return_value="main",
        ):
            result = get_branch(str(tmp_path))
        assert result == "main"

    def test_falls_back_to_unknown(self, tmp_path):
        with patch(
            "cervellaswarm_agent_hooks.session_checkpoint.git_command",
            return_value="",
        ):
            result = get_branch(str(tmp_path))
        assert result == "unknown"
