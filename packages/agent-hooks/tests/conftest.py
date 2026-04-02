# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Shared fixtures for cervellaswarm-agent-hooks tests."""

import json
from io import StringIO

import pytest


# ---------------------------------------------------------------------------
# Temp directory fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def tmp_project(tmp_path):
    """Create a minimal temp project with a .git directory."""
    (tmp_path / ".git").mkdir()
    return tmp_path


@pytest.fixture
def tmp_project_with_config(tmp_path):
    """Temp project with .cervella/hooks.yaml config."""
    (tmp_path / ".git").mkdir()
    cervella_dir = tmp_path / ".cervella"
    cervella_dir.mkdir()
    config_file = cervella_dir / "hooks.yaml"
    config_file.write_text(
        """
file_limits:
  checks:
    - pattern: "*.md"
      name: "Markdown files"
      max_lines: 10
      action: "Trim it"

context_inject:
  facts_file: "docs/FACTS.md"
  state_file: "SESSION_STATE.md"
  facts_max_lines: 50
  state_max_lines: 20

session_checkpoint:
  state_file: "SESSION_STATE.md"
  include_git_status: true
  include_recent_commits: false
  max_lines: 100

git_reminder:
  interval_minutes: 15
""",
        encoding="utf-8",
    )
    return tmp_path


# ---------------------------------------------------------------------------
# stdin helpers
# ---------------------------------------------------------------------------


@pytest.fixture
def make_stdin(monkeypatch):
    """Return helper that patches sys.stdin with JSON payload."""

    def _make(data: dict):
        monkeypatch.setattr("sys.stdin", StringIO(json.dumps(data)))

    return _make


@pytest.fixture
def make_stdin_bad(monkeypatch):
    """Patch sys.stdin with invalid JSON."""

    def _make():
        monkeypatch.setattr("sys.stdin", StringIO("not-json{{{"))

    return _make


# ---------------------------------------------------------------------------
# Sample config
# ---------------------------------------------------------------------------


SAMPLE_CONFIG_YAML = """
file_limits:
  checks:
    - pattern: "*.md"
      name: "Markdown"
      max_lines: 5

context_inject:
  facts_file: "docs/FACTS.md"
  state_file: "SESSION_STATE.md"
  facts_max_lines: 20
  state_max_lines: 10

session_checkpoint:
  state_file: "SESSION_STATE.md"
  include_git_status: true
  include_recent_commits: true
  max_lines: 50

git_reminder:
  interval_minutes: 60
"""
