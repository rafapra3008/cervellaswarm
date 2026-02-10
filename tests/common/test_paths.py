#!/usr/bin/env python3
"""
Test suite for scripts/common/paths.py

Coverage target: 100% (excluding __main__ block)
Lines to cover: 41, 66, 83, 100, 150-152, 162-164, 179-184, 194-203, 212-226
"""

import os
from pathlib import Path
import pytest

from scripts.common.paths import (
    _get_project_root,
    _get_home_agents_path,
    get_agents_path,
    get_data_dir,
    get_db_path,
    get_logs_dir,
    get_scripts_dir,
    ensure_data_dir,
    ensure_logs_dir,
    get_agent_file,
    list_agents,
    print_paths,
)


# =============================================================================
# Test _get_project_root
# =============================================================================

def test_get_project_root_finds_marker(tmp_path, monkeypatch):
    """Test _get_project_root quando trova CLAUDE.md"""
    fake_project = tmp_path / "fake_project"
    fake_scripts = fake_project / "scripts" / "common"
    fake_scripts.mkdir(parents=True)
    fake_file = fake_scripts / "paths.py"
    fake_file.touch()
    (fake_project / "CLAUDE.md").touch()

    monkeypatch.setattr("scripts.common.paths.__file__", str(fake_file))

    result = _get_project_root()
    assert result == fake_project


def test_get_project_root_fallback_no_marker(tmp_path, monkeypatch):
    """Test _get_project_root fallback quando non trova marker (line 41)"""
    fake_scripts = tmp_path / "scripts" / "common"
    fake_scripts.mkdir(parents=True)
    fake_file = fake_scripts / "paths.py"
    fake_file.touch()

    monkeypatch.setattr("scripts.common.paths.__file__", str(fake_file))

    result = _get_project_root()
    assert result == fake_file.parent.parent.parent


def test_get_home_agents_path():
    """Test _get_home_agents_path ritorna ~/.claude/agents/"""
    result = _get_home_agents_path()
    expected = Path.home() / ".claude" / "agents"
    assert result == expected


# =============================================================================
# Test get_agents_path
# =============================================================================

def test_get_agents_path_default(monkeypatch):
    """Test get_agents_path default (no env var) returns ~/.claude/agents/"""
    monkeypatch.delenv("CERVELLASWARM_AGENTS_PATH", raising=False)
    result = get_agents_path()
    assert result == Path.home() / ".claude" / "agents"


def test_get_agents_path_with_env_var(monkeypatch):
    """Test get_agents_path con env var override (line 66)"""
    custom_path = "/custom/agents"
    monkeypatch.setenv("CERVELLASWARM_AGENTS_PATH", custom_path)

    result = get_agents_path()
    assert result == Path(custom_path)


# =============================================================================
# Test get_data_dir
# =============================================================================

def test_get_data_dir_default(monkeypatch):
    """Test get_data_dir default (no env var) returns {project_root}/data"""
    monkeypatch.delenv("CERVELLASWARM_DATA_DIR", raising=False)
    result = get_data_dir()
    assert result.name == "data"


def test_get_data_dir_with_env_var(monkeypatch):
    """Test get_data_dir con env var override (line 83)"""
    custom_path = "/custom/data"
    monkeypatch.setenv("CERVELLASWARM_DATA_DIR", custom_path)

    result = get_data_dir()
    assert result == Path(custom_path)


# =============================================================================
# Test get_db_path
# =============================================================================

def test_get_db_path_default(monkeypatch):
    """Test get_db_path default (no env var) returns {data_dir}/swarm_memory.db"""
    monkeypatch.delenv("CERVELLASWARM_DB_PATH", raising=False)
    result = get_db_path()
    assert result.name == "swarm_memory.db"


def test_get_db_path_with_env_var(monkeypatch):
    """Test get_db_path con env var override (line 100)"""
    custom_path = "/custom/swarm.db"
    monkeypatch.setenv("CERVELLASWARM_DB_PATH", custom_path)

    result = get_db_path()
    assert result == Path(custom_path)


# =============================================================================
# Test get_logs_dir / get_scripts_dir
# =============================================================================

def test_get_logs_dir_returns_subpath(monkeypatch):
    """Test get_logs_dir returns {data_dir}/logs"""
    monkeypatch.setenv("CERVELLASWARM_DATA_DIR", "/custom/data")
    result = get_logs_dir()
    assert result == Path("/custom/data/logs")


def test_get_scripts_dir_returns_subpath():
    """Test get_scripts_dir returns {project_root}/scripts"""
    result = get_scripts_dir()
    assert result.name == "scripts"


# =============================================================================
# Test ensure_data_dir
# =============================================================================

def test_ensure_data_dir_creates_directory(tmp_path, monkeypatch):
    """Test ensure_data_dir crea directory se non esiste (lines 150-152)"""
    fake_data_dir = tmp_path / "data"
    monkeypatch.setenv("CERVELLASWARM_DATA_DIR", str(fake_data_dir))

    result = ensure_data_dir()

    assert result == fake_data_dir
    assert fake_data_dir.is_dir()


# =============================================================================
# Test ensure_logs_dir
# =============================================================================

def test_ensure_logs_dir_creates_directory(tmp_path, monkeypatch):
    """Test ensure_logs_dir crea directory se non esiste (lines 162-164)"""
    fake_data_dir = tmp_path / "data"
    monkeypatch.setenv("CERVELLASWARM_DATA_DIR", str(fake_data_dir))

    result = ensure_logs_dir()

    expected = fake_data_dir / "logs"
    assert result == expected
    assert expected.is_dir()


# =============================================================================
# Test get_agent_file
# =============================================================================

def test_get_agent_file_short_name(tmp_path, monkeypatch):
    """Test get_agent_file normalizza nome corto (lines 179-184)"""
    monkeypatch.setenv("CERVELLASWARM_AGENTS_PATH", str(tmp_path))

    result = get_agent_file("frontend")
    assert result == tmp_path / "cervella-frontend.md"


def test_get_agent_file_full_name(tmp_path, monkeypatch):
    """Test get_agent_file con nome completo"""
    monkeypatch.setenv("CERVELLASWARM_AGENTS_PATH", str(tmp_path))

    result = get_agent_file("cervella-frontend")
    assert result == tmp_path / "cervella-frontend.md"


def test_get_agent_file_with_extension(tmp_path, monkeypatch):
    """Test get_agent_file con estensione gia presente"""
    monkeypatch.setenv("CERVELLASWARM_AGENTS_PATH", str(tmp_path))

    result = get_agent_file("cervella-frontend.md")
    assert result == tmp_path / "cervella-frontend.md"


# =============================================================================
# Test list_agents
# =============================================================================

def test_list_agents_nonexistent_directory(tmp_path, monkeypatch):
    """Test list_agents con directory non esistente (line 195)"""
    fake_agents_dir = tmp_path / "agents"
    monkeypatch.setenv("CERVELLASWARM_AGENTS_PATH", str(fake_agents_dir))

    result = list_agents()
    assert result == []


def test_list_agents_populated_directory(tmp_path, monkeypatch):
    """Test list_agents con agent files"""
    fake_agents_dir = tmp_path / "agents"
    fake_agents_dir.mkdir()

    (fake_agents_dir / "cervella-frontend.md").touch()
    (fake_agents_dir / "cervella-backend.md").touch()
    (fake_agents_dir / "cervella-tester.md").touch()
    (fake_agents_dir / "other-file.md").touch()

    monkeypatch.setenv("CERVELLASWARM_AGENTS_PATH", str(fake_agents_dir))

    result = list_agents()
    assert result == ["backend", "frontend", "tester"]


# =============================================================================
# Test print_paths
# =============================================================================

def test_print_paths_runs_without_error(capsys, monkeypatch):
    """Test print_paths stampa output senza errori (lines 212-226)"""
    monkeypatch.delenv("CERVELLASWARM_AGENTS_PATH", raising=False)
    monkeypatch.delenv("CERVELLASWARM_DB_PATH", raising=False)
    monkeypatch.delenv("CERVELLASWARM_DATA_DIR", raising=False)

    print_paths()

    captured = capsys.readouterr()
    assert "CervellaSwarm - Path Configuration" in captured.out
    assert "PROJECT_ROOT:" in captured.out
    assert "Environment overrides:" in captured.out
