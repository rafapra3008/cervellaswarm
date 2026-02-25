# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Shared fixtures for spawn-workers tests."""

import pytest


@pytest.fixture
def tmp_tasks_dir(tmp_path):
    """Temp directory for task files."""
    d = tmp_path / "tasks"
    d.mkdir()
    return d


@pytest.fixture
def tmp_logs_dir(tmp_path):
    """Temp directory for log files."""
    d = tmp_path / "logs"
    d.mkdir()
    return d


@pytest.fixture
def tmp_status_dir(tmp_path):
    """Temp directory for status files."""
    d = tmp_path / "status"
    d.mkdir()
    return d


@pytest.fixture
def sample_team_yaml():
    """Valid team.yaml string for testing."""
    return """
name: test-team
version: 1.0.0
process: hierarchical
agents:
  - name: worker-alpha
    type: worker
    specialty: backend
    model: sonnet
    spawn_on_start: true
  - name: guardian-beta
    type: guardian
    specialty: generic
    model: opus
    spawn_on_start: true
  - name: leader-gamma
    type: leader
    spawn_on_start: true
spawn:
  backend: tmux
  max_workers: 3
  tasks_dir: .swarm/tasks
  logs_dir: .swarm/logs
  status_dir: .swarm/status
"""
