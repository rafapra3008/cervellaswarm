# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for cervellaswarm_agent_hooks.session_checkpoint - build_checkpoint() and main()."""

import json
from io import StringIO
from pathlib import Path
from unittest.mock import patch

import pytest

from cervellaswarm_agent_hooks.session_checkpoint import build_checkpoint, main


# ---------------------------------------------------------------------------
# build_checkpoint
# ---------------------------------------------------------------------------


class TestBuildCheckpoint:
    def test_contains_project_name(self, tmp_path):
        config = {
            "include_git_status": False,
            "include_recent_commits": False,
        }
        with patch(
            "cervellaswarm_agent_hooks.session_checkpoint.get_branch",
            return_value="main",
        ):
            result = build_checkpoint(str(tmp_path), config)
        assert tmp_path.name in result

    def test_contains_branch(self, tmp_path):
        config = {
            "include_git_status": False,
            "include_recent_commits": False,
        }
        with patch(
            "cervellaswarm_agent_hooks.session_checkpoint.get_branch",
            return_value="feature-x",
        ):
            result = build_checkpoint(str(tmp_path), config)
        assert "feature-x" in result

    def test_includes_git_status_when_configured(self, tmp_path):
        config = {
            "include_git_status": True,
            "include_recent_commits": False,
        }
        with patch(
            "cervellaswarm_agent_hooks.session_checkpoint.get_git_status",
            return_value="3 modified",
        ):
            with patch(
                "cervellaswarm_agent_hooks.session_checkpoint.get_branch",
                return_value="main",
            ):
                result = build_checkpoint(str(tmp_path), config)
        assert "Git Status" in result
        assert "3 modified" in result

    def test_skips_git_status_when_disabled(self, tmp_path):
        config = {
            "include_git_status": False,
            "include_recent_commits": False,
        }
        with patch(
            "cervellaswarm_agent_hooks.session_checkpoint.get_branch",
            return_value="main",
        ):
            result = build_checkpoint(str(tmp_path), config)
        assert "Git Status" not in result

    def test_includes_recent_commits_when_configured(self, tmp_path):
        config = {
            "include_git_status": False,
            "include_recent_commits": True,
        }
        with patch(
            "cervellaswarm_agent_hooks.session_checkpoint.get_recent_commits",
            return_value="abc123 feat: something",
        ):
            with patch(
                "cervellaswarm_agent_hooks.session_checkpoint.get_branch",
                return_value="main",
            ):
                result = build_checkpoint(str(tmp_path), config)
        assert "Recent Commits" in result
        assert "abc123" in result

    def test_skips_commits_when_disabled(self, tmp_path):
        config = {
            "include_git_status": False,
            "include_recent_commits": False,
        }
        with patch(
            "cervellaswarm_agent_hooks.session_checkpoint.get_branch",
            return_value="main",
        ):
            result = build_checkpoint(str(tmp_path), config)
        assert "Recent Commits" not in result

    def test_contains_current_focus_section(self, tmp_path):
        config = {
            "include_git_status": False,
            "include_recent_commits": False,
        }
        with patch(
            "cervellaswarm_agent_hooks.session_checkpoint.get_branch",
            return_value="main",
        ):
            result = build_checkpoint(str(tmp_path), config)
        assert "Current Focus" in result

    def test_result_is_string(self, tmp_path):
        config = {
            "include_git_status": False,
            "include_recent_commits": False,
        }
        with patch(
            "cervellaswarm_agent_hooks.session_checkpoint.get_branch",
            return_value="main",
        ):
            result = build_checkpoint(str(tmp_path), config)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_contains_timestamp(self, tmp_path):
        config = {
            "include_git_status": False,
            "include_recent_commits": False,
        }
        with patch(
            "cervellaswarm_agent_hooks.session_checkpoint.get_branch",
            return_value="main",
        ):
            result = build_checkpoint(str(tmp_path), config)
        # Timestamp format: YYYY-MM-DD HH:MM
        import re
        assert re.search(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}", result)


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------


class TestMain:
    def test_main_writes_state_file(self, monkeypatch, capsys, tmp_path):
        (tmp_path / ".git").mkdir()
        payload = {"cwd": str(tmp_path)}
        monkeypatch.setattr("sys.stdin", StringIO(json.dumps(payload)))

        config = {
            "state_file": "SESSION_STATE.md",
            "include_git_status": False,
            "include_recent_commits": False,
            "max_lines": 200,
        }
        with patch(
            "cervellaswarm_agent_hooks.session_checkpoint.get_hook_config",
            return_value=config,
        ):
            with patch(
                "cervellaswarm_agent_hooks.session_checkpoint.git_command",
                return_value="",
            ):
                result = main()

        assert result == 0
        state_file = tmp_path / "SESSION_STATE.md"
        assert state_file.exists()
        captured = capsys.readouterr()
        output = json.loads(captured.out)
        assert "result" in output

    def test_main_no_git_repo(self, monkeypatch, capsys, tmp_path):
        payload = {"cwd": str(tmp_path)}
        monkeypatch.setattr("sys.stdin", StringIO(json.dumps(payload)))

        with patch(
            "cervellaswarm_agent_hooks.session_checkpoint.find_project_root",
            return_value=None,
        ):
            result = main()

        assert result == 0
        captured = capsys.readouterr()
        output = json.loads(captured.out)
        assert "Not a git repository" in output["result"]

    def test_main_respects_max_lines(self, monkeypatch, capsys, tmp_path):
        (tmp_path / ".git").mkdir()
        payload = {"cwd": str(tmp_path)}
        monkeypatch.setattr("sys.stdin", StringIO(json.dumps(payload)))

        many_lines = "\n".join(f"line {i}" for i in range(300))

        config = {
            "state_file": "SESSION_STATE.md",
            "include_git_status": False,
            "include_recent_commits": False,
            "max_lines": 10,
        }
        with patch(
            "cervellaswarm_agent_hooks.session_checkpoint.get_hook_config",
            return_value=config,
        ):
            with patch(
                "cervellaswarm_agent_hooks.session_checkpoint.build_checkpoint",
                return_value=many_lines,
            ):
                result = main()

        state_file = tmp_path / "SESSION_STATE.md"
        written = state_file.read_text()
        assert len(written.split("\n")) <= 11  # 10 lines + trailing newline

    def test_main_invalid_json_stdin(self, monkeypatch, capsys, tmp_path):
        monkeypatch.setattr("sys.stdin", StringIO("bad json"))

        with patch(
            "cervellaswarm_agent_hooks.session_checkpoint.find_project_root",
            return_value=None,
        ):
            result = main()

        assert result == 0

    def test_main_result_message_contains_filename(self, monkeypatch, capsys, tmp_path):
        (tmp_path / ".git").mkdir()
        payload = {"cwd": str(tmp_path)}
        monkeypatch.setattr("sys.stdin", StringIO(json.dumps(payload)))

        config = {
            "state_file": "MY_STATE.md",
            "include_git_status": False,
            "include_recent_commits": False,
            "max_lines": 200,
        }
        with patch(
            "cervellaswarm_agent_hooks.session_checkpoint.get_hook_config",
            return_value=config,
        ):
            with patch(
                "cervellaswarm_agent_hooks.session_checkpoint.git_command",
                return_value="",
            ):
                result = main()

        captured = capsys.readouterr()
        output = json.loads(captured.out)
        assert "MY_STATE.md" in output["result"]
