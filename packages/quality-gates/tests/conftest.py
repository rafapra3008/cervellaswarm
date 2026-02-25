# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Shared fixtures for cervellaswarm-quality-gates tests."""

import os
import stat
import pytest
from pathlib import Path


@pytest.fixture
def tmp_hooks_dir(tmp_path):
    """Create a temporary hooks directory with sample hook files."""
    hooks_dir = tmp_path / "hooks"
    hooks_dir.mkdir()
    return hooks_dir


@pytest.fixture
def valid_hook(tmp_hooks_dir):
    """Create a valid executable hook with shebang."""
    hook = tmp_hooks_dir / "session_start.py"
    hook.write_text("#!/usr/bin/env python3\nprint('hello')\n")
    hook.chmod(hook.stat().st_mode | stat.S_IXUSR)
    return hook


@pytest.fixture
def broken_hook(tmp_hooks_dir):
    """Create a hook with bad shebang."""
    hook = tmp_hooks_dir / "broken_hook.py"
    hook.write_text("not a shebang\nprint('broken')\n")
    hook.chmod(hook.stat().st_mode | stat.S_IXUSR)
    return hook


@pytest.fixture
def not_exec_hook(tmp_hooks_dir):
    """Create a hook without execute permission."""
    hook = tmp_hooks_dir / "no_exec.py"
    hook.write_text("#!/usr/bin/env python3\nprint('no exec')\n")
    hook.chmod(stat.S_IRUSR | stat.S_IWUSR)  # rw only
    return hook


@pytest.fixture
def disabled_hook(tmp_hooks_dir):
    """Create a disabled hook (underscore prefix)."""
    hook = tmp_hooks_dir / "_disabled.py"
    hook.write_text("#!/usr/bin/env python3\nprint('disabled')\n")
    hook.chmod(hook.stat().st_mode | stat.S_IXUSR)
    return hook


@pytest.fixture
def agent_source(tmp_path):
    """Create a source agent directory."""
    src = tmp_path / "agents_source"
    src.mkdir()
    (src / "agent_a.md").write_text("# Agent A\nRole: backend\n")
    (src / "agent_b.md").write_text("# Agent B\nRole: frontend\n")
    (src / "shared.md").write_text("# Shared DNA\nVersion: 1.0\n")
    return src


@pytest.fixture
def agent_target(tmp_path):
    """Create a target agent directory (partially different)."""
    tgt = tmp_path / "agents_target"
    tgt.mkdir()
    (tgt / "agent_a.md").write_text("# Agent A\nRole: backend\n")  # same
    (tgt / "agent_b.md").write_text("# Agent B\nRole: frontend v2\n")  # different
    (tgt / "agent_c.md").write_text("# Agent C\nRole: tester\n")  # only in target
    return tgt


@pytest.fixture
def sample_session_content():
    """Return sample session content for quality scoring."""
    return """# Session 42

> **Ultimo aggiornamento:** 2026-02-24 - Sessione 42

## What happened

- Fixed auth bug in `login_handler.py` v0.2.1
- Added 15 tests for edge cases
- Guardiana score: 9.5/10

## Next steps

1. Deploy to staging server
2. Run integration tests
3. TODO: Update migration docs

## Decisions

- Chose JWT over sessions (stateless, S42)
"""


@pytest.fixture
def clean_env(monkeypatch):
    """Remove quality-gates env vars for clean test."""
    monkeypatch.delenv("CERVELLASWARM_QUALITY_GATES_CONFIG", raising=False)
