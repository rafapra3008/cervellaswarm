# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for cervellaswarm_agent_hooks.bash_validator - validate() and main()."""

import json
from io import StringIO

import pytest

from cervellaswarm_agent_hooks.bash_validator import main, validate


# ---------------------------------------------------------------------------
# VALIDATE (integration)
# ---------------------------------------------------------------------------


class TestValidate:
    def test_empty_command_returns_none(self):
        assert validate("") is None

    def test_whitespace_only_returns_none(self):
        assert validate("   ") is None

    def test_blocked_returns_deny(self):
        result = validate("rm -rf /")
        assert result is not None
        decision = result["hookSpecificOutput"]["permissionDecision"]
        assert decision == "deny"

    def test_blocked_reason_in_message(self):
        result = validate("DROP TABLE users")
        assert result is not None
        reason = result["hookSpecificOutput"]["permissionDecisionReason"]
        assert "BLOCKED" in reason

    def test_risky_returns_ask(self):
        result = validate("git reset --hard HEAD")
        assert result is not None
        decision = result["hookSpecificOutput"]["permissionDecision"]
        assert decision == "ask"

    def test_risky_reason_in_message(self):
        result = validate("git reset --hard HEAD")
        reason = result["hookSpecificOutput"]["permissionDecisionReason"]
        assert "WARNING" in reason

    def test_autofix_returns_allow_with_updated_input(self):
        result = validate("git push origin --force feature-x")
        assert result is not None
        output = result["hookSpecificOutput"]
        assert output["permissionDecision"] == "allow"
        assert "updatedInput" in output
        assert "--force-with-lease" in output["updatedInput"]["command"]

    def test_safe_rm_is_not_risky(self):
        result = validate("rm -rf node_modules")
        assert result is None

    def test_safe_command_returns_none(self):
        assert validate("git status") is None

    def test_git_push_normal_returns_none(self):
        assert validate("git push origin feature") is None

    def test_blocked_takes_priority_over_risky(self):
        result = validate("rm -rf /")
        assert result["hookSpecificOutput"]["permissionDecision"] == "deny"

    def test_autofix_before_risky(self):
        # git push --force on non-main should be auto-fixed, not asked
        result = validate("git push --force feature-branch")
        assert result is not None
        assert result["hookSpecificOutput"]["permissionDecision"] == "allow"

    def test_hook_event_name_set(self):
        result = validate("rm -rf /")
        assert result["hookSpecificOutput"]["hookEventName"] == "PreToolUse"

    def test_rm_rf_pycache_allowed(self):
        result = validate("rm -rf __pycache__")
        assert result is None

    def test_chmod_777_is_risky(self):
        result = validate("chmod 777 /etc/passwd")
        assert result is not None
        assert result["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_kill_9_is_risky(self):
        result = validate("kill -9 999")
        assert result is not None
        assert result["hookSpecificOutput"]["permissionDecision"] == "ask"


# ---------------------------------------------------------------------------
# MAIN (stdin integration)
# ---------------------------------------------------------------------------


class TestMain:
    def test_main_blocked_command(self, monkeypatch, capsys):
        payload = {"tool_input": {"command": "rm -rf /"}}
        monkeypatch.setattr("sys.stdin", StringIO(json.dumps(payload)))
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        output = json.loads(captured.out)
        assert output["hookSpecificOutput"]["permissionDecision"] == "deny"

    def test_main_safe_command_no_output(self, monkeypatch, capsys):
        payload = {"tool_input": {"command": "ls -la"}}
        monkeypatch.setattr("sys.stdin", StringIO(json.dumps(payload)))
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert captured.out.strip() == ""

    def test_main_invalid_json_exits_0(self, monkeypatch):
        monkeypatch.setattr("sys.stdin", StringIO("not-json"))
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0

    def test_main_missing_command_key(self, monkeypatch, capsys):
        payload = {"tool_input": {}}
        monkeypatch.setattr("sys.stdin", StringIO(json.dumps(payload)))
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert captured.out.strip() == ""

    def test_main_autofix_command(self, monkeypatch, capsys):
        payload = {"tool_input": {"command": "git push --force feature-branch"}}
        monkeypatch.setattr("sys.stdin", StringIO(json.dumps(payload)))
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        output = json.loads(captured.out)
        assert output["hookSpecificOutput"]["permissionDecision"] == "allow"

    def test_main_risky_command(self, monkeypatch, capsys):
        payload = {"tool_input": {"command": "git reset --hard HEAD"}}
        monkeypatch.setattr("sys.stdin", StringIO(json.dumps(payload)))
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        output = json.loads(captured.out)
        assert output["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_main_empty_stdin_payload(self, monkeypatch, capsys):
        payload = {}
        monkeypatch.setattr("sys.stdin", StringIO(json.dumps(payload)))
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert captured.out.strip() == ""
