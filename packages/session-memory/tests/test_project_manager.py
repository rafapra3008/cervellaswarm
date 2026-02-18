# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for cervellaswarm_session_memory.project_manager module."""

import pytest
from datetime import date
from pathlib import Path

from cervellaswarm_session_memory.project_manager import (
    normalize_name,
    init_project,
    discover_projects,
    get_project,
    archive_state,
    ProjectInfo,
    _load_template,
    _render_template,
)


# ---------------------------------------------------------------------------
# normalize_name
# ---------------------------------------------------------------------------

def test_normalize_name_lowercase():
    """Converts name to lowercase."""
    assert normalize_name("MyProject") == "myproject"


def test_normalize_name_spaces():
    """Converts spaces to hyphens."""
    assert normalize_name("My Project") == "my-project"


def test_normalize_name_underscores():
    """Converts underscores to hyphens."""
    assert normalize_name("my_project") == "my-project"


def test_normalize_name_consecutive_hyphens():
    """Collapses consecutive hyphens to a single hyphen."""
    assert normalize_name("my--project") == "my-project"


def test_normalize_name_strips():
    """Strips leading and trailing whitespace."""
    assert normalize_name(" project ") == "project"


# ---------------------------------------------------------------------------
# init_project - directory creation
# ---------------------------------------------------------------------------

def test_init_project_creates_dirs(tmp_path):
    """init_project creates the project directory and archive subdirectory."""
    info = init_project("alpha", project_root=tmp_path)
    assert info.memory_dir.exists()
    assert (info.memory_dir / "alpha").is_dir()
    assert info.archive_dir.is_dir()


def test_init_project_creates_state_file(tmp_path):
    """init_project creates a session state file."""
    info = init_project("alpha", project_root=tmp_path)
    assert info.state_file.exists()


def test_init_project_creates_compass(tmp_path):
    """init_project creates PROJECT_COMPASS.md by default."""
    info = init_project("alpha", project_root=tmp_path)
    assert info.compass_file is not None
    assert info.compass_file.exists()


def test_init_project_no_compass(tmp_path):
    """init_project skips compass file when create_compass=False."""
    info = init_project("alpha", project_root=tmp_path, create_compass=False)
    assert info.compass_file is None


def test_init_project_custom_memory_dir(tmp_path):
    """init_project uses custom memory_dir name when provided."""
    info = init_project("alpha", project_root=tmp_path, memory_dir=".my-mem")
    assert info.memory_dir.name == ".my-mem"
    assert info.memory_dir.exists()


def test_init_project_custom_session_number(tmp_path):
    """init_project uses the given session_number in state content."""
    info = init_project("alpha", project_root=tmp_path, session_number=42)
    content = info.state_file.read_text(encoding="utf-8")
    assert "42" in content


def test_init_project_exists_error(tmp_path):
    """init_project raises FileExistsError when project already exists."""
    init_project("alpha", project_root=tmp_path)
    with pytest.raises(FileExistsError):
        init_project("alpha", project_root=tmp_path)


def test_init_project_returns_project_info(tmp_path):
    """init_project returns a ProjectInfo dataclass."""
    info = init_project("alpha", project_root=tmp_path)
    assert isinstance(info, ProjectInfo)
    assert info.name == "alpha"


def test_init_project_state_content(tmp_path):
    """init_project renders template placeholders correctly."""
    info = init_project("My Project", project_root=tmp_path, session_number=5)
    content = info.state_file.read_text(encoding="utf-8")
    assert "My Project" in content
    assert "{{ project_name }}" not in content
    assert date.today().isoformat() in content


def test_init_project_compass_not_overwritten(tmp_path):
    """If compass file already exists, init_project does not overwrite it."""
    compass_path = tmp_path / "PROJECT_COMPASS.md"
    compass_path.write_text("# Existing Compass\n", encoding="utf-8")
    init_project("alpha", project_root=tmp_path, create_compass=True)
    assert compass_path.read_text(encoding="utf-8") == "# Existing Compass\n"


# ---------------------------------------------------------------------------
# discover_projects
# ---------------------------------------------------------------------------

def test_discover_projects_empty(tmp_path):
    """discover_projects returns empty list when memory dir is missing."""
    result = discover_projects(base_dir=tmp_path)
    assert result == []


def test_discover_projects_finds_project(tmp_path):
    """discover_projects finds 1 project after init."""
    init_project("alpha", project_root=tmp_path, create_compass=False)
    projects = discover_projects(base_dir=tmp_path)
    assert len(projects) == 1
    assert projects[0].name == "alpha"


def test_discover_projects_finds_multiple(tmp_path):
    """discover_projects finds all 3 initialized projects."""
    for name in ["alpha", "beta", "gamma"]:
        init_project(name, project_root=tmp_path, create_compass=False)
    projects = discover_projects(base_dir=tmp_path)
    assert len(projects) == 3
    names = {p.name for p in projects}
    assert names == {"alpha", "beta", "gamma"}


def test_discover_projects_ignores_hidden(tmp_path):
    """discover_projects ignores directories starting with a dot."""
    init_project("alpha", project_root=tmp_path, create_compass=False)
    # Create a hidden dir with a state file - should be ignored
    mem_dir = tmp_path / ".session-memory"
    hidden = mem_dir / ".hidden"
    hidden.mkdir()
    (hidden / "SESSION_STATE_hidden.md").write_text("# State\n", encoding="utf-8")
    projects = discover_projects(base_dir=tmp_path)
    names = {p.name for p in projects}
    assert ".hidden" not in names


def test_discover_projects_ignores_no_state(tmp_path):
    """discover_projects ignores directories without a state file."""
    mem_dir = tmp_path / ".session-memory"
    mem_dir.mkdir()
    no_state = mem_dir / "no-state"
    no_state.mkdir()
    projects = discover_projects(base_dir=tmp_path)
    assert len(projects) == 0


# ---------------------------------------------------------------------------
# get_project
# ---------------------------------------------------------------------------

def test_get_project_found(tmp_path):
    """get_project returns ProjectInfo when project exists."""
    init_project("alpha", project_root=tmp_path, create_compass=False)
    result = get_project("alpha", base_dir=tmp_path)
    assert result is not None
    assert result.name == "alpha"


def test_get_project_not_found(tmp_path):
    """get_project returns None when project does not exist."""
    result = get_project("nonexistent", base_dir=tmp_path)
    assert result is None


def test_get_project_normalized(tmp_path):
    """get_project normalizes the search name before matching."""
    init_project("my-project", project_root=tmp_path, create_compass=False)
    result = get_project("My Project", base_dir=tmp_path)
    assert result is not None
    assert result.name == "my-project"


# ---------------------------------------------------------------------------
# archive_state
# ---------------------------------------------------------------------------

def test_archive_state_creates_file(tmp_path):
    """archive_state copies state file into the archive directory."""
    info = init_project("alpha", project_root=tmp_path, create_compass=False)
    archived = archive_state(info)
    assert archived.exists()
    assert archived.parent == info.archive_dir


def test_archive_state_with_reason(tmp_path):
    """archive_state includes the reason in the archived file name."""
    info = init_project("alpha", project_root=tmp_path, create_compass=False)
    archived = archive_state(info, reason="end-of-sprint")
    assert "end-of-sprint" in archived.name


def test_archive_state_no_overwrite(tmp_path):
    """archive_state uses a counter suffix when archive name already exists."""
    info = init_project("alpha", project_root=tmp_path, create_compass=False)
    first = archive_state(info)
    second = archive_state(info)
    assert first != second
    assert first.exists()
    assert second.exists()


def test_archive_state_missing_file(tmp_path):
    """archive_state raises FileNotFoundError when state file is missing."""
    info = init_project("alpha", project_root=tmp_path, create_compass=False)
    info.state_file.unlink()
    with pytest.raises(FileNotFoundError):
        archive_state(info)


# ---------------------------------------------------------------------------
# _load_template
# ---------------------------------------------------------------------------

def test_load_template_session_state():
    """_load_template loads session_state.md without error."""
    content = _load_template("session_state.md")
    assert content
    assert "{{ project_name }}" in content


def test_load_template_project_compass():
    """_load_template loads project_compass.md without error."""
    content = _load_template("project_compass.md")
    assert content
    assert "{{ project_name }}" in content


# ---------------------------------------------------------------------------
# _render_template
# ---------------------------------------------------------------------------

def test_render_template_substitution():
    """_render_template substitutes {{ variable }} placeholders."""
    template = "Hello {{ name }}, session {{ number }}!"
    result = _render_template(template, {"name": "World", "number": "42"})
    assert result == "Hello World, session 42!"
    assert "{{" not in result


def test_render_template_no_match():
    """_render_template leaves unknown placeholders unchanged."""
    template = "Hello {{ unknown }}!"
    result = _render_template(template, {"name": "World"})
    assert "{{ unknown }}" in result
