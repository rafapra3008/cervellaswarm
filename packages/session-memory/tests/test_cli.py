# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for cervellaswarm_session_memory.cli.

NOTE: audit_directory (called by main_audit) skips files whose full path
contains "test". pytest's tmp_path always embeds the test name (e.g.
test_audit_with_secret0). We use tempfile.mkdtemp() for audit tests that
need real secret detection.
"""

import json
import shutil
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from cervellaswarm_session_memory.cli import (
    main,
    main_audit,
    main_check,
    main_init,
    main_list,
    main_sync,
)


@pytest.fixture
def clean_dir():
    """Temporary directory whose path does NOT contain 'test' or 'mock'.

    audit_directory skips paths with those substrings. Using a neutral
    prefix keeps detection tests reliable.
    """
    d = Path(tempfile.mkdtemp(prefix="cerv_cli_"))
    yield d
    shutil.rmtree(d, ignore_errors=True)


# ---------------------------------------------------------------------------
# main() entry point
# ---------------------------------------------------------------------------


def test_main_no_args(capsys):
    """main() with no arguments prints help and exits with code 0."""
    with pytest.raises(SystemExit) as exc:
        main([])
    assert exc.value.code == 0
    out = capsys.readouterr().out
    assert "cervella-session" in out


def test_main_version(capsys):
    """main --version prints the package version."""
    with pytest.raises(SystemExit):
        main(["--version"])
    captured = capsys.readouterr()
    combined = captured.out + captured.err
    assert "cervella-session" in combined


# ---------------------------------------------------------------------------
# main_init
# ---------------------------------------------------------------------------


def test_init_creates_project(tmp_path, monkeypatch):
    """cervella-session init creates the project structure on disk."""
    monkeypatch.chdir(tmp_path)
    main_init(["my-project"])
    mem_dir = tmp_path / ".session-memory" / "my-project"
    assert mem_dir.exists()
    state_files = list(mem_dir.glob("SESSION_STATE_*.md"))
    assert len(state_files) == 1


def test_init_json_output(tmp_path, monkeypatch, capsys):
    """cervella-session init --json outputs valid JSON with project info."""
    monkeypatch.chdir(tmp_path)
    main_init(["my-project", "--json"])
    out = capsys.readouterr().out
    data = json.loads(out)
    assert data["project"] == "my-project"
    assert "state_file" in data
    assert "memory_dir" in data


def test_init_project_root(tmp_path, monkeypatch):
    """--project-root flag places the project in the specified directory."""
    monkeypatch.chdir(tmp_path)
    subdir = tmp_path / "custom-root"
    subdir.mkdir()
    main_init(["my-project", "--project-root", str(subdir)])
    mem_dir = subdir / ".session-memory" / "my-project"
    assert mem_dir.exists()


def test_init_no_compass(tmp_path, monkeypatch):
    """--no-compass skips creating PROJECT_COMPASS.md."""
    monkeypatch.chdir(tmp_path)
    main_init(["my-project", "--no-compass"])
    compass = tmp_path / "PROJECT_COMPASS.md"
    assert not compass.exists()


def test_init_duplicate_error(tmp_path, monkeypatch, capsys):
    """Initializing the same project twice exits with code 1."""
    monkeypatch.chdir(tmp_path)
    main_init(["my-project"])
    with pytest.raises(SystemExit) as exc:
        main_init(["my-project"])
    assert exc.value.code == 1
    err = capsys.readouterr().err
    assert "Error" in err


def test_init_duplicate_json_error(tmp_path, monkeypatch, capsys):
    """Duplicate project with --json outputs JSON error and exits with code 1."""
    monkeypatch.chdir(tmp_path)
    main_init(["my-project"])
    capsys.readouterr()  # clear output from first init
    with pytest.raises(SystemExit) as exc:
        main_init(["my-project", "--json"])
    assert exc.value.code == 1
    out = capsys.readouterr().out
    data = json.loads(out)
    assert "error" in data


# ---------------------------------------------------------------------------
# main_check
# ---------------------------------------------------------------------------


def test_check_no_projects(tmp_path, monkeypatch, capsys):
    """check with no projects prints a helpful message."""
    monkeypatch.chdir(tmp_path)
    main_check([])
    out = capsys.readouterr().out
    assert "No projects found" in out


def test_check_single_project(tmp_path, monkeypatch, capsys):
    """check after init shows quality results for the project."""
    monkeypatch.chdir(tmp_path)
    main_init(["my-project"])
    capsys.readouterr()  # clear init output

    main_check(["my-project"])
    out = capsys.readouterr().out
    assert "MY-PROJECT" in out or "my-project" in out.lower()


def test_check_all_projects(tmp_path, monkeypatch, capsys):
    """check with no project argument checks all discovered projects."""
    monkeypatch.chdir(tmp_path)
    main_init(["alpha"])
    main_init(["beta"])
    capsys.readouterr()

    main_check([])
    out = capsys.readouterr().out
    assert "ALPHA" in out or "alpha" in out.lower()
    assert "BETA" in out or "beta" in out.lower()


def test_check_json_output(tmp_path, monkeypatch, capsys):
    """check --json outputs a JSON list with quality info."""
    monkeypatch.chdir(tmp_path)
    main_init(["my-project"])
    capsys.readouterr()

    main_check(["my-project", "--json"])
    out = capsys.readouterr().out
    data = json.loads(out)
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["project"] == "my-project"


def test_check_project_not_found(tmp_path, monkeypatch, capsys):
    """check for a non-existent project exits with code 1."""
    monkeypatch.chdir(tmp_path)
    with pytest.raises(SystemExit) as exc:
        main_check(["ghost-project"])
    assert exc.value.code == 1
    err = capsys.readouterr().err
    assert "not found" in err.lower()


# ---------------------------------------------------------------------------
# main_audit
# ---------------------------------------------------------------------------


def test_audit_clean_dir(clean_dir, capsys):
    """audit on a directory with no secrets exits with code 0."""
    (clean_dir / "state.md").write_text("# Clean state\n\nNo secrets here.\n", encoding="utf-8")
    with pytest.raises(SystemExit) as exc:
        main_audit([str(clean_dir)])
    assert exc.value.code == 0


def test_audit_with_secret(clean_dir, capsys):
    """audit detecting a secret exits with code 1."""
    (clean_dir / "state.md").write_text(
        "api_key=sk-abcdefghijklmnopqrstu\n", encoding="utf-8"
    )
    with pytest.raises(SystemExit) as exc:
        main_audit([str(clean_dir)])
    assert exc.value.code == 1


def test_audit_json_output(clean_dir, capsys):
    """audit --json outputs valid JSON with findings info."""
    (clean_dir / "state.md").write_text(
        "api_key=sk-abcdefghijklmnopqrstu\n", encoding="utf-8"
    )
    with pytest.raises(SystemExit):
        main_audit([str(clean_dir), "--json"])
    out = capsys.readouterr().out
    data = json.loads(out)
    assert "scanned_files" in data
    assert "critical" in data
    assert "clean" in data
    assert isinstance(data["findings"], list)


def test_audit_default_path(clean_dir, monkeypatch, capsys):
    """audit with no path argument defaults to current directory."""
    monkeypatch.chdir(clean_dir)
    (clean_dir / "notes.md").write_text("# Just notes\n", encoding="utf-8")
    with pytest.raises(SystemExit) as exc:
        main_audit([])
    # Directory is clean so exit 0
    assert exc.value.code == 0


# ---------------------------------------------------------------------------
# main_sync
# ---------------------------------------------------------------------------


def test_sync_no_projects(tmp_path, monkeypatch, capsys):
    """sync with no projects prints a helpful message."""
    monkeypatch.chdir(tmp_path)
    main_sync([])
    out = capsys.readouterr().out
    assert "No projects found" in out


def test_sync_single_project(tmp_path, monkeypatch, capsys):
    """sync after init shows sync status for the project."""
    monkeypatch.chdir(tmp_path)
    main_init(["my-project"])
    capsys.readouterr()

    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = ""

    with patch("cervellaswarm_session_memory.sync_checker.subprocess.run", return_value=mock_result):
        main_sync(["my-project"])

    out = capsys.readouterr().out
    assert "MY-PROJECT" in out or "my-project" in out.lower()


def test_sync_json_output(tmp_path, monkeypatch, capsys):
    """sync --json outputs valid JSON list with sync info."""
    monkeypatch.chdir(tmp_path)
    main_init(["my-project"])
    capsys.readouterr()

    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = ""

    with patch("cervellaswarm_session_memory.sync_checker.subprocess.run", return_value=mock_result):
        main_sync(["my-project", "--json"])

    out = capsys.readouterr().out
    data = json.loads(out)
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["project"] == "my-project"
    assert "overall" in data[0]
    assert "checks" in data[0]


# ---------------------------------------------------------------------------
# main_list
# ---------------------------------------------------------------------------


def test_list_no_projects(tmp_path, monkeypatch, capsys):
    """list with no projects prints a helpful message."""
    monkeypatch.chdir(tmp_path)
    main_list([])
    out = capsys.readouterr().out
    assert "No projects found" in out


def test_list_with_projects(tmp_path, monkeypatch, capsys):
    """list after init shows the project names."""
    monkeypatch.chdir(tmp_path)
    main_init(["my-project"])
    capsys.readouterr()

    main_list([])
    out = capsys.readouterr().out
    assert "my-project" in out


def test_list_json_output(tmp_path, monkeypatch, capsys):
    """list --json outputs a JSON list of project info."""
    monkeypatch.chdir(tmp_path)
    main_init(["my-project"])
    capsys.readouterr()

    main_list(["--json"])
    out = capsys.readouterr().out
    data = json.loads(out)
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "my-project"
    assert "state_file" in data[0]
    assert "memory_dir" in data[0]


# ---------------------------------------------------------------------------
# main() dispatch
# ---------------------------------------------------------------------------


def test_main_dispatches_init(tmp_path, monkeypatch):
    """main(['init', 'x']) delegates to main_init and creates the project."""
    monkeypatch.chdir(tmp_path)
    main(["init", "test-dispatch"])
    mem_dir = tmp_path / ".session-memory" / "test-dispatch"
    assert mem_dir.exists()


def test_main_dispatches_check(tmp_path, monkeypatch, capsys):
    """main(['check']) delegates to main_check."""
    monkeypatch.chdir(tmp_path)
    main(["check"])
    out = capsys.readouterr().out
    # No projects -> helpful message
    assert "No projects found" in out


def test_main_dispatches_list(tmp_path, monkeypatch, capsys):
    """main(['list']) delegates to main_list."""
    monkeypatch.chdir(tmp_path)
    main(["list"])
    out = capsys.readouterr().out
    assert "No projects found" in out
