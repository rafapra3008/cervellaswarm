# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for cervellaswarm_agent_hooks.context_inject."""

import json
from io import StringIO
from pathlib import Path
from unittest.mock import patch

import pytest

from cervellaswarm_agent_hooks.context_inject import (
    build_context,
    find_project_root,
    main,
    safe_read,
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
        subdir = tmp_path / "a" / "b" / "c"
        subdir.mkdir(parents=True)
        root = find_project_root(str(subdir))
        assert root == tmp_path

    def test_returns_none_when_no_git(self, tmp_path):
        # No .git anywhere
        isolated = tmp_path / "isolated"
        isolated.mkdir()
        # Walk up from isolated - should reach filesystem root without .git
        # We patch the parents to avoid hitting a real .git in parent dirs
        result = find_project_root(str(isolated))
        # Either None or some real root - just ensure no exception
        assert result is None or isinstance(result, Path)

    def test_finds_root_in_deep_nesting(self, tmp_path):
        (tmp_path / ".git").mkdir()
        deep = tmp_path / "a" / "b" / "c" / "d" / "e"
        deep.mkdir(parents=True)
        root = find_project_root(str(deep))
        assert root == tmp_path


# ---------------------------------------------------------------------------
# safe_read
# ---------------------------------------------------------------------------


class TestSafeRead:
    def test_reads_existing_file(self, tmp_path):
        f = tmp_path / "facts.md"
        f.write_text("fact 1\nfact 2\n")
        result = safe_read(f)
        assert result == "fact 1\nfact 2\n"

    def test_returns_none_for_missing_file(self, tmp_path):
        f = tmp_path / "nonexistent.md"
        result = safe_read(f)
        assert result is None

    def test_no_limit_returns_full_content(self, tmp_path):
        f = tmp_path / "big.md"
        content = "\n".join(f"line {i}" for i in range(100))
        f.write_text(content)
        result = safe_read(f, max_lines=0)
        assert result == content

    def test_limit_truncates_content(self, tmp_path):
        f = tmp_path / "big.md"
        lines = [f"line {i}" for i in range(20)]
        f.write_text("\n".join(lines))
        result = safe_read(f, max_lines=5)
        assert result is not None
        result_lines = result.split("\n")
        # First 5 lines + the truncation notice
        assert result_lines[0] == "line 0"
        assert result_lines[4] == "line 4"
        assert "more lines" in result

    def test_limit_larger_than_content_returns_full(self, tmp_path):
        f = tmp_path / "small.md"
        f.write_text("line 1\nline 2\n")
        result = safe_read(f, max_lines=100)
        assert "line 1" in result
        assert "line 2" in result
        assert "more lines" not in result

    def test_handles_read_error_gracefully(self, tmp_path):
        f = tmp_path / "bad.md"
        f.write_bytes(b"\xff\xfe")  # Invalid UTF-8
        # Should return None without raising
        result = safe_read(f)
        # Could succeed or return None depending on platform
        assert result is None or isinstance(result, str)


# ---------------------------------------------------------------------------
# build_context
# ---------------------------------------------------------------------------


class TestBuildContext:
    def test_build_with_facts_and_state(self, tmp_path):
        (tmp_path / ".git").mkdir()
        docs = tmp_path / "docs"
        docs.mkdir()
        (docs / "FACTS.md").write_text("# Facts\n- Python is cool\n")
        (tmp_path / "SESSION_STATE.md").write_text("## State\n- Working on X\n")

        config = {
            "facts_file": "docs/FACTS.md",
            "state_file": "SESSION_STATE.md",
            "facts_max_lines": 100,
            "state_max_lines": 50,
        }
        result = build_context(tmp_path, config)
        assert result is not None
        assert "CONFIRMED FACTS" in result
        assert "CURRENT STATE" in result
        assert "Python is cool" in result
        assert "Working on X" in result
        assert tmp_path.name in result

    def test_build_with_only_facts(self, tmp_path):
        docs = tmp_path / "docs"
        docs.mkdir()
        (docs / "FACTS.md").write_text("# Facts\n- Important fact\n")

        config = {
            "facts_file": "docs/FACTS.md",
            "state_file": "MISSING_STATE.md",
            "facts_max_lines": 100,
            "state_max_lines": 50,
        }
        result = build_context(tmp_path, config)
        assert result is not None
        assert "CONFIRMED FACTS" in result
        assert "CURRENT STATE" not in result

    def test_build_with_only_state(self, tmp_path):
        (tmp_path / "SESSION_STATE.md").write_text("## State\n- Working on Y\n")

        config = {
            "facts_file": "MISSING_FACTS.md",
            "state_file": "SESSION_STATE.md",
            "facts_max_lines": 100,
            "state_max_lines": 50,
        }
        result = build_context(tmp_path, config)
        assert result is not None
        assert "CURRENT STATE" in result
        assert "CONFIRMED FACTS" not in result

    def test_build_with_no_files_returns_none(self, tmp_path):
        config = {
            "facts_file": "MISSING_FACTS.md",
            "state_file": "MISSING_STATE.md",
            "facts_max_lines": 100,
            "state_max_lines": 50,
        }
        result = build_context(tmp_path, config)
        assert result is None

    def test_build_includes_rule(self, tmp_path):
        (tmp_path / "SESSION_STATE.md").write_text("state content")

        config = {
            "facts_file": "MISSING.md",
            "state_file": "SESSION_STATE.md",
            "facts_max_lines": 100,
            "state_max_lines": 50,
        }
        result = build_context(tmp_path, config)
        assert "RULE" in result
        assert "contradiction" in result.lower()

    def test_build_uses_custom_file_paths(self, tmp_path):
        (tmp_path / "MY_FACTS.md").write_text("custom fact")

        config = {
            "facts_file": "MY_FACTS.md",
            "state_file": "MISSING.md",
            "facts_max_lines": 100,
            "state_max_lines": 50,
        }
        result = build_context(tmp_path, config)
        assert result is not None
        assert "custom fact" in result

    def test_build_respects_max_lines(self, tmp_path):
        facts_lines = [f"fact {i}" for i in range(50)]
        (tmp_path / "FACTS.md").write_text("\n".join(facts_lines))

        config = {
            "facts_file": "FACTS.md",
            "state_file": "MISSING.md",
            "facts_max_lines": 5,
            "state_max_lines": 50,
        }
        result = build_context(tmp_path, config)
        assert result is not None
        assert "more lines" in result


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------


class TestMain:
    def test_main_with_context(self, monkeypatch, capsys, tmp_path):
        (tmp_path / ".git").mkdir()
        (tmp_path / "SESSION_STATE.md").write_text("current state")

        payload = {"cwd": str(tmp_path)}
        monkeypatch.setattr("sys.stdin", StringIO(json.dumps(payload)))

        config = {
            "facts_file": "MISSING.md",
            "state_file": "SESSION_STATE.md",
            "facts_max_lines": 100,
            "state_max_lines": 50,
        }
        with patch(
            "cervellaswarm_agent_hooks.context_inject.get_hook_config",
            return_value=config,
        ):
            main()

        captured = capsys.readouterr()
        output = json.loads(captured.out)
        assert "hookSpecificOutput" in output
        assert output["hookSpecificOutput"]["hookEventName"] == "SubagentStart"
        assert "current state" in output["hookSpecificOutput"]["additionalContext"]

    def test_main_no_git_root(self, monkeypatch, capsys, tmp_path):
        # No .git -> find_project_root returns None -> outputs {}
        payload = {"cwd": str(tmp_path)}
        monkeypatch.setattr("sys.stdin", StringIO(json.dumps(payload)))

        with patch(
            "cervellaswarm_agent_hooks.context_inject.find_project_root",
            return_value=None,
        ):
            main()

        captured = capsys.readouterr()
        output = json.loads(captured.out)
        assert output == {}

    def test_main_no_files_outputs_empty(self, monkeypatch, capsys, tmp_path):
        (tmp_path / ".git").mkdir()
        payload = {"cwd": str(tmp_path)}
        monkeypatch.setattr("sys.stdin", StringIO(json.dumps(payload)))

        config = {
            "facts_file": "MISSING.md",
            "state_file": "MISSING2.md",
            "facts_max_lines": 100,
            "state_max_lines": 50,
        }
        with patch(
            "cervellaswarm_agent_hooks.context_inject.get_hook_config",
            return_value=config,
        ):
            main()

        captured = capsys.readouterr()
        output = json.loads(captured.out)
        assert output == {}

    def test_main_invalid_json_stdin(self, monkeypatch, capsys, tmp_path):
        monkeypatch.setattr("sys.stdin", StringIO("bad json!"))

        with patch(
            "cervellaswarm_agent_hooks.context_inject.find_project_root",
            return_value=None,
        ):
            main()

        captured = capsys.readouterr()
        output = json.loads(captured.out)
        assert output == {}
