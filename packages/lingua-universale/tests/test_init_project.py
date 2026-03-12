# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for _init_project.py -- `lu init` scaffolding (T3.3)."""

from __future__ import annotations

import pytest
from pathlib import Path

from cervellaswarm_lingua_universale._init_project import (
    init_project,
    _template_protocol,
    _template_test,
    _template_readme,
)
from cervellaswarm_lingua_universale._eval import check_source, verify_source


# ============================================================
# Template generation
# ============================================================


class TestTemplates:
    """Verify template content is valid LU source."""

    def test_protocol_template_parses(self) -> None:
        src = _template_protocol("my-project")
        r = check_source(src)
        assert r.ok, f"Template failed: {r.errors}"
        assert r.compiled is not None
        assert "MyProject" in r.compiled.protocols
        assert "MyProjectAgent" in r.compiled.agents
        assert "Status" in r.compiled.types

    def test_protocol_template_verifies(self) -> None:
        src = _template_protocol("hello-world")
        r = verify_source(src)
        assert r.ok, f"Template verify failed: {r.errors}"
        assert r.property_reports
        report = r.property_reports[0]
        for result in report.results:
            assert result.verdict.name == "PROVED"

    def test_test_template_parses(self) -> None:
        src = _template_test("my-project")
        r = check_source(src)
        assert r.ok, f"Test template failed: {r.errors}"
        assert r.compiled is not None
        assert "VerifyMyProject" in r.compiled.protocols
        assert "Verifier" in r.compiled.agents

    def test_test_template_verifies(self) -> None:
        src = _template_test("my-project")
        r = verify_source(src)
        assert r.ok, f"Test template verify failed: {r.errors}"

    def test_readme_contains_name(self) -> None:
        readme = _template_readme("cool-proto")
        assert "# cool-proto" in readme
        assert "lu check cool-proto.lu" in readme
        assert "lu verify cool-proto.lu" in readme

    def test_pascal_case_conversion(self) -> None:
        """Hyphens and underscores convert to PascalCase."""
        src = _template_protocol("my-cool_project")
        assert "MyCoolProject" in src

    def test_simple_name(self) -> None:
        """Single word name works without hyphens."""
        src = _template_protocol("hello")
        r = check_source(src)
        assert r.ok
        assert "Hello" in r.compiled.protocols


# ============================================================
# init_project function
# ============================================================


class TestInitProject:
    """Core scaffolding logic."""

    def test_default_creates_three_files(self, tmp_path: Path) -> None:
        created = init_project("demo", target_dir=tmp_path)
        assert len(created) == 3
        names = {p.name for p in created}
        assert "demo.lu" in names
        assert "demo_test.lu" in names
        assert "README.md" in names

    def test_minimal_creates_one_file(self, tmp_path: Path) -> None:
        created = init_project("demo", target_dir=tmp_path, minimal=True)
        assert len(created) == 1
        assert created[0].name == "demo.lu"

    def test_creates_directory(self, tmp_path: Path) -> None:
        init_project("new-proto", target_dir=tmp_path)
        assert (tmp_path / "new-proto").is_dir()
        assert (tmp_path / "new-proto" / "new-proto.lu").exists()

    def test_files_are_utf8(self, tmp_path: Path) -> None:
        init_project("test", target_dir=tmp_path)
        content = (tmp_path / "test" / "test.lu").read_text(encoding="utf-8")
        assert "protocol Test:" in content

    def test_generated_lu_files_valid(self, tmp_path: Path) -> None:
        """All generated .lu files must parse and compile."""
        init_project("my-app", target_dir=tmp_path)
        for lu_file in (tmp_path / "my-app").glob("*.lu"):
            src = lu_file.read_text(encoding="utf-8")
            r = check_source(src, source_file=str(lu_file))
            assert r.ok, f"{lu_file.name} failed: {r.errors}"

    def test_error_on_empty_name(self, tmp_path: Path) -> None:
        with pytest.raises(ValueError, match="Invalid project name"):
            init_project("", target_dir=tmp_path)

    def test_error_on_invalid_chars(self, tmp_path: Path) -> None:
        with pytest.raises(ValueError, match="Invalid project name"):
            init_project("my project!", target_dir=tmp_path)

    def test_error_on_numeric_leading_name(self, tmp_path: Path) -> None:
        """Names starting with digits produce invalid LU identifiers."""
        with pytest.raises(ValueError, match="Must start with a letter"):
            init_project("123proto", target_dir=tmp_path)

    def test_error_on_pure_numeric_name(self, tmp_path: Path) -> None:
        with pytest.raises(ValueError, match="Must start with a letter"):
            init_project("999", target_dir=tmp_path)

    def test_error_on_existing_nonempty_dir(self, tmp_path: Path) -> None:
        proj_dir = tmp_path / "existing"
        proj_dir.mkdir()
        (proj_dir / "file.txt").write_text("occupied")
        with pytest.raises(FileExistsError, match="not empty"):
            init_project("existing", target_dir=tmp_path)

    def test_force_overwrites(self, tmp_path: Path) -> None:
        """--force allows overwriting; unrelated files are preserved."""
        proj_dir = tmp_path / "existing"
        proj_dir.mkdir()
        (proj_dir / "old.txt").write_text("old content")
        created = init_project("existing", target_dir=tmp_path, force=True)
        assert len(created) == 3
        assert (proj_dir / "existing.lu").exists()
        # Force is additive, not destructive
        assert (proj_dir / "old.txt").exists()

    def test_idempotent_on_empty_dir(self, tmp_path: Path) -> None:
        """Init into existing empty directory works without --force."""
        proj_dir = tmp_path / "empty"
        proj_dir.mkdir()
        created = init_project("empty", target_dir=tmp_path)
        assert len(created) == 3


# ============================================================
# CLI integration
# ============================================================


class TestInitCli:
    """Test `lu init` via CLI main()."""

    def test_cli_init_success(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture) -> None:
        monkeypatch.chdir(tmp_path)
        monkeypatch.setenv("NO_COLOR", "1")
        from cervellaswarm_lingua_universale._cli import main
        result = main(["init", "cli-test"])
        assert result == 0
        assert (tmp_path / "cli-test" / "cli-test.lu").exists()
        captured = capsys.readouterr()
        assert "Created" in captured.out
        assert "cli-test" in captured.out
        assert "lu check" in captured.out

    def test_cli_init_minimal(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture) -> None:
        monkeypatch.chdir(tmp_path)
        monkeypatch.setenv("NO_COLOR", "1")
        from cervellaswarm_lingua_universale._cli import main
        result = main(["init", "mini", "--minimal"])
        assert result == 0
        assert (tmp_path / "mini" / "mini.lu").exists()
        assert not (tmp_path / "mini" / "README.md").exists()
        captured = capsys.readouterr()
        assert "Created" in captured.out

    def test_cli_init_force(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.chdir(tmp_path)
        monkeypatch.setenv("NO_COLOR", "1")
        proj = tmp_path / "forced"
        proj.mkdir()
        (proj / "old.txt").write_text("old")
        from cervellaswarm_lingua_universale._cli import main
        result = main(["init", "forced", "--force"])
        assert result == 0

    def test_cli_init_error(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture) -> None:
        monkeypatch.chdir(tmp_path)
        monkeypatch.setenv("NO_COLOR", "1")
        proj = tmp_path / "taken"
        proj.mkdir()
        (proj / "file.txt").write_text("occupied")
        from cervellaswarm_lingua_universale._cli import main
        result = main(["init", "taken"])
        assert result == 1
        captured = capsys.readouterr()
        assert "not empty" in captured.err
