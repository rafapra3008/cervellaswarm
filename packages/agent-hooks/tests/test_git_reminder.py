# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for cervellaswarm_agent_hooks.git_reminder."""

import json
import os
from datetime import datetime, timedelta
from io import StringIO
from pathlib import Path
from unittest.mock import MagicMock, call, patch

import pytest

from cervellaswarm_agent_hooks.git_reminder import (
    get_uncommitted_count,
    main,
    send_notification,
    should_remind,
    update_reminder_state,
)


# ---------------------------------------------------------------------------
# get_uncommitted_count
# ---------------------------------------------------------------------------


class TestGetUncommittedCount:
    def test_no_changes_returns_zero(self, tmp_path):
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = ""
        with patch("subprocess.run", return_value=mock_result):
            assert get_uncommitted_count(str(tmp_path)) == 0

    def test_one_changed_file(self, tmp_path):
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = " M README.md\n"
        with patch("subprocess.run", return_value=mock_result):
            assert get_uncommitted_count(str(tmp_path)) == 1

    def test_multiple_changed_files(self, tmp_path):
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = " M README.md\n?? new_file.py\nA  added.py\n"
        with patch("subprocess.run", return_value=mock_result):
            assert get_uncommitted_count(str(tmp_path)) == 3

    def test_non_zero_returncode_returns_zero(self, tmp_path):
        mock_result = MagicMock()
        mock_result.returncode = 128  # not a git repo
        mock_result.stdout = ""
        with patch("subprocess.run", return_value=mock_result):
            assert get_uncommitted_count(str(tmp_path)) == 0

    def test_subprocess_exception_returns_zero(self, tmp_path):
        with patch("subprocess.run", side_effect=Exception("git not found")):
            assert get_uncommitted_count(str(tmp_path)) == 0

    def test_timeout_exception_returns_zero(self, tmp_path):
        import subprocess
        with patch("subprocess.run", side_effect=subprocess.TimeoutExpired("git", 5)):
            assert get_uncommitted_count(str(tmp_path)) == 0


# ---------------------------------------------------------------------------
# should_remind
# ---------------------------------------------------------------------------


class TestShouldRemind:
    def test_no_state_file_returns_true(self, tmp_path):
        with patch(
            "cervellaswarm_agent_hooks.git_reminder.REMINDER_STATE_FILE",
            tmp_path / "nonexistent.json",
        ):
            assert should_remind("/some/project") is True

    def test_first_time_cwd_returns_true(self, tmp_path):
        state_file = tmp_path / "state.json"
        state_file.write_text(json.dumps({"/other/project": datetime.now().isoformat()}))
        with patch(
            "cervellaswarm_agent_hooks.git_reminder.REMINDER_STATE_FILE", state_file
        ):
            assert should_remind("/some/project") is True

    def test_recent_reminder_returns_false(self, tmp_path):
        state_file = tmp_path / "state.json"
        # Recent = 5 minutes ago
        recent = (datetime.now() - timedelta(minutes=5)).isoformat()
        state_file.write_text(json.dumps({"/some/project": recent}))
        with patch(
            "cervellaswarm_agent_hooks.git_reminder.REMINDER_STATE_FILE", state_file
        ):
            assert should_remind("/some/project") is False

    def test_old_reminder_returns_true(self, tmp_path):
        state_file = tmp_path / "state.json"
        # Old = 60 minutes ago (past the 30-min interval)
        old = (datetime.now() - timedelta(minutes=60)).isoformat()
        state_file.write_text(json.dumps({"/some/project": old}))
        with patch(
            "cervellaswarm_agent_hooks.git_reminder.REMINDER_STATE_FILE", state_file
        ):
            assert should_remind("/some/project") is True

    def test_corrupted_state_file_returns_true(self, tmp_path):
        state_file = tmp_path / "state.json"
        state_file.write_text("this is not json")
        with patch(
            "cervellaswarm_agent_hooks.git_reminder.REMINDER_STATE_FILE", state_file
        ):
            assert should_remind("/some/project") is True


# ---------------------------------------------------------------------------
# update_reminder_state
# ---------------------------------------------------------------------------


class TestUpdateReminderState:
    def test_creates_state_file(self, tmp_path):
        state_file = tmp_path / "state.json"
        with patch(
            "cervellaswarm_agent_hooks.git_reminder.REMINDER_STATE_FILE", state_file
        ):
            update_reminder_state("/my/project")
        assert state_file.exists()
        state = json.loads(state_file.read_text())
        assert "/my/project" in state

    def test_updates_existing_entry(self, tmp_path):
        state_file = tmp_path / "state.json"
        old_time = (datetime.now() - timedelta(hours=2)).isoformat()
        state_file.write_text(json.dumps({"/my/project": old_time}))
        with patch(
            "cervellaswarm_agent_hooks.git_reminder.REMINDER_STATE_FILE", state_file
        ):
            update_reminder_state("/my/project")
        state = json.loads(state_file.read_text())
        new_time = datetime.fromisoformat(state["/my/project"])
        assert (datetime.now() - new_time).total_seconds() < 5

    def test_exception_does_not_raise(self, tmp_path):
        # Should fail silently
        with patch(
            "cervellaswarm_agent_hooks.git_reminder.REMINDER_STATE_FILE",
            Path("/nonexistent_root/state.json"),
        ):
            # Should not raise
            update_reminder_state("/my/project")


# ---------------------------------------------------------------------------
# send_notification
# ---------------------------------------------------------------------------


class TestSendNotification:
    def test_calls_osascript_on_macos(self):
        mock_result = MagicMock()
        with patch("subprocess.run", return_value=mock_result) as mock_run:
            send_notification(3)
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        assert args[0] == "osascript"

    def test_singular_message_for_one_file(self):
        with patch("subprocess.run") as mock_run:
            send_notification(1)
        call_args = mock_run.call_args[0][0]
        assert "osascript" in call_args[0]
        # Check the script contains "file" not "files"
        script_arg = call_args[2]
        assert "1 uncommitted file" in script_arg
        assert "files" not in script_arg

    def test_plural_message_for_multiple_files(self):
        with patch("subprocess.run") as mock_run:
            send_notification(5)
        call_args = mock_run.call_args[0][0]
        script_arg = call_args[2]
        assert "5 uncommitted files" in script_arg

    def test_falls_back_to_notify_send_on_linux(self):
        calls = []
        def fake_run(cmd, **kwargs):
            calls.append(cmd[0])
            if cmd[0] == "osascript":
                raise FileNotFoundError("osascript not found")
            return MagicMock()

        with patch("subprocess.run", side_effect=fake_run):
            send_notification(2)
        assert "osascript" in calls
        assert "notify-send" in calls

    def test_exception_in_notification_is_silent(self):
        # Both osascript and notify-send raise
        with patch("subprocess.run", side_effect=Exception("no notification")):
            # Should not raise
            send_notification(1)


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------


class TestMain:
    def test_main_with_uncommitted_files(self, monkeypatch, capsys, tmp_path):
        payload = {"cwd": str(tmp_path)}
        monkeypatch.setattr("sys.stdin", StringIO(json.dumps(payload)))

        with patch(
            "cervellaswarm_agent_hooks.git_reminder.get_uncommitted_count",
            return_value=3,
        ):
            with patch(
                "cervellaswarm_agent_hooks.git_reminder.should_remind",
                return_value=True,
            ):
                with patch(
                    "cervellaswarm_agent_hooks.git_reminder.send_notification"
                ) as mock_notify:
                    with patch(
                        "cervellaswarm_agent_hooks.git_reminder.update_reminder_state"
                    ) as mock_update:
                        result = main()

        mock_notify.assert_called_once_with(3)
        mock_update.assert_called_once_with(str(tmp_path))
        assert result == 0
        captured = capsys.readouterr()
        output = json.loads(captured.out)
        assert output["continue"] is True

    def test_main_no_uncommitted_files(self, monkeypatch, capsys, tmp_path):
        payload = {"cwd": str(tmp_path)}
        monkeypatch.setattr("sys.stdin", StringIO(json.dumps(payload)))

        with patch(
            "cervellaswarm_agent_hooks.git_reminder.get_uncommitted_count",
            return_value=0,
        ):
            with patch(
                "cervellaswarm_agent_hooks.git_reminder.send_notification"
            ) as mock_notify:
                result = main()

        mock_notify.assert_not_called()
        assert result == 0

    def test_main_skips_when_cooldown_active(self, monkeypatch, capsys, tmp_path):
        payload = {"cwd": str(tmp_path)}
        monkeypatch.setattr("sys.stdin", StringIO(json.dumps(payload)))

        with patch(
            "cervellaswarm_agent_hooks.git_reminder.get_uncommitted_count",
            return_value=5,
        ):
            with patch(
                "cervellaswarm_agent_hooks.git_reminder.should_remind",
                return_value=False,
            ):
                with patch(
                    "cervellaswarm_agent_hooks.git_reminder.send_notification"
                ) as mock_notify:
                    result = main()

        mock_notify.assert_not_called()

    def test_main_invalid_json_stdin(self, monkeypatch, capsys):
        monkeypatch.setattr("sys.stdin", StringIO("bad json"))
        with patch(
            "cervellaswarm_agent_hooks.git_reminder.get_uncommitted_count",
            return_value=0,
        ):
            result = main()
        assert result == 0
        captured = capsys.readouterr()
        output = json.loads(captured.out)
        assert output["suppressOutput"] is True
