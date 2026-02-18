# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for cervellaswarm_agent_templates.cli module."""

import sys
from io import StringIO
from pathlib import Path
from unittest.mock import patch

import pytest

from cervellaswarm_agent_templates import __version__
from cervellaswarm_agent_templates.cli import build_parser, main


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _capture(capsys, argv):
    """Run main() with argv, return (returncode, stdout, stderr)."""
    rc = main(argv)
    captured = capsys.readouterr()
    return rc, captured.out, captured.err


# ---------------------------------------------------------------------------
# main() with no args shows help
# ---------------------------------------------------------------------------


class TestMainNoArgs:
    def test_no_args_returns_0(self, capsys):
        rc = main([])
        assert rc == 0

    def test_no_args_prints_something(self, capsys):
        main([])
        captured = capsys.readouterr()
        assert len(captured.out) > 0


# ---------------------------------------------------------------------------
# list command
# ---------------------------------------------------------------------------


class TestCommandList:
    def test_list_returns_0(self, capsys):
        rc, out, err = _capture(capsys, ["list"])
        assert rc == 0

    def test_list_shows_agent_types(self, capsys):
        rc, out, err = _capture(capsys, ["list"])
        assert "coordinator" in out
        assert "worker" in out
        assert "architect" in out
        assert "quality-gate" in out

    def test_list_shows_specialties(self, capsys):
        rc, out, err = _capture(capsys, ["list"])
        assert "backend" in out
        assert "frontend" in out

    def test_list_shows_team_presets(self, capsys):
        rc, out, err = _capture(capsys, ["list"])
        assert "minimal" in out
        assert "standard" in out
        assert "full" in out


# ---------------------------------------------------------------------------
# init command - single agent
# ---------------------------------------------------------------------------


class TestCommandInit:
    def test_init_coordinator_returns_0(self, tmp_dir, capsys):
        rc, out, err = _capture(capsys, ["init", "coordinator", "--output", str(tmp_dir)])
        assert rc == 0

    def test_init_coordinator_creates_file(self, tmp_dir, capsys):
        _capture(capsys, ["init", "coordinator", "--output", str(tmp_dir)])
        md_files = list(tmp_dir.glob("*.md"))
        assert any(f.name != "_shared_dna.md" for f in md_files)

    def test_init_worker_returns_0(self, tmp_dir, capsys):
        rc, out, err = _capture(capsys, ["init", "worker", "--output", str(tmp_dir)])
        assert rc == 0

    def test_init_worker_with_specialty_returns_0(self, tmp_dir, capsys):
        rc, out, err = _capture(capsys, [
            "init", "worker", "--specialty", "backend", "--output", str(tmp_dir)
        ])
        assert rc == 0

    def test_init_worker_with_specialty_creates_file(self, tmp_dir, capsys):
        _capture(capsys, ["init", "worker", "--specialty", "backend", "--output", str(tmp_dir)])
        assert (tmp_dir / "worker.md").exists()

    def test_init_with_name_uses_name(self, tmp_dir, capsys):
        _capture(capsys, ["init", "coordinator", "--name", "my-lead", "--output", str(tmp_dir)])
        assert (tmp_dir / "my-lead.md").exists()

    def test_init_prints_created_path(self, tmp_dir, capsys):
        rc, out, err = _capture(capsys, ["init", "coordinator", "--output", str(tmp_dir)])
        assert "Created" in out

    def test_init_also_creates_shared_dna(self, tmp_dir, capsys):
        _capture(capsys, ["init", "coordinator", "--output", str(tmp_dir)])
        assert (tmp_dir / "_shared_dna.md").exists()

    def test_init_architect_returns_0(self, tmp_dir, capsys):
        rc, out, err = _capture(capsys, ["init", "architect", "--output", str(tmp_dir)])
        assert rc == 0

    def test_init_quality_gate_returns_0(self, tmp_dir, capsys):
        rc, out, err = _capture(capsys, ["init", "quality-gate", "--output", str(tmp_dir)])
        assert rc == 0

    def test_init_with_team_name(self, tmp_dir, capsys):
        _capture(capsys, ["init", "coordinator", "--team", "my-squad", "--output", str(tmp_dir)])
        content = (tmp_dir / "coordinator.md").read_text()
        assert "my-squad" in content

    def test_init_invalid_type_returns_non_zero(self, tmp_dir, capsys):
        # argparse will refuse unknown choice - SystemExit raised
        with pytest.raises(SystemExit) as exc_info:
            main(["init", "superagent", "--output", str(tmp_dir)])
        assert exc_info.value.code != 0

    def test_init_does_not_overwrite_existing_shared_dna(self, tmp_dir, capsys):
        # Create shared_dna with known content first
        dna_path = tmp_dir / "_shared_dna.md"
        dna_path.write_text("original content", encoding="utf-8")
        _capture(capsys, ["init", "coordinator", "--output", str(tmp_dir)])
        # Should still contain original (not overwritten)
        assert dna_path.read_text() == "original content"


# ---------------------------------------------------------------------------
# init-team command
# ---------------------------------------------------------------------------


class TestCommandInitTeam:
    def test_init_team_minimal_returns_0(self, tmp_dir, capsys):
        rc, out, err = _capture(capsys, ["init-team", "minimal", "--output", str(tmp_dir)])
        assert rc == 0

    def test_init_team_minimal_creates_files(self, tmp_dir, capsys):
        _capture(capsys, ["init-team", "minimal", "--output", str(tmp_dir)])
        all_files = list(tmp_dir.iterdir())
        assert len(all_files) >= 5

    def test_init_team_standard_returns_0(self, tmp_dir, capsys):
        rc, out, err = _capture(capsys, ["init-team", "standard", "--output", str(tmp_dir)])
        assert rc == 0

    def test_init_team_full_returns_0(self, tmp_dir, capsys):
        rc, out, err = _capture(capsys, ["init-team", "full", "--output", str(tmp_dir)])
        assert rc == 0

    def test_init_team_prints_file_count(self, tmp_dir, capsys):
        rc, out, err = _capture(capsys, ["init-team", "minimal", "--output", str(tmp_dir)])
        assert "5" in out or "files" in out.lower() or "Created" in out

    def test_init_team_invalid_preset_exits_nonzero(self, tmp_dir, capsys):
        with pytest.raises(SystemExit) as exc_info:
            main(["init-team", "mega", "--output", str(tmp_dir)])
        assert exc_info.value.code != 0

    def test_init_team_with_name(self, tmp_dir, capsys):
        _capture(capsys, ["init-team", "minimal", "--name", "alpha-team", "--output", str(tmp_dir)])
        import yaml
        data = yaml.safe_load((tmp_dir / "team.yaml").read_text())
        assert data["name"] == "alpha-team"

    def test_init_team_creates_team_yaml(self, tmp_dir, capsys):
        _capture(capsys, ["init-team", "minimal", "--output", str(tmp_dir)])
        assert (tmp_dir / "team.yaml").exists()

    def test_init_team_creates_shared_dna(self, tmp_dir, capsys):
        _capture(capsys, ["init-team", "minimal", "--output", str(tmp_dir)])
        assert (tmp_dir / "_shared_dna.md").exists()


# ---------------------------------------------------------------------------
# validate command
# ---------------------------------------------------------------------------


VALID_CONTENT = """\
---
name: my-agent
description: Does important things.
model: sonnet
tools: Read, Edit, Bash
---

This is a sufficiently long body to pass the short-body check. It explains
what the agent does and provides instructions for how to behave correctly.
"""

INVALID_CONTENT = """\
---
description: Missing name and bad model.
model: gpt-4
tools: Read
---

This is a sufficiently long body to pass the short-body check at least.
"""


class TestCommandValidate:
    def test_valid_file_returns_0(self, tmp_dir, capsys):
        p = tmp_dir / "valid.md"
        p.write_text(VALID_CONTENT, encoding="utf-8")
        rc, out, err = _capture(capsys, ["validate", str(p)])
        assert rc == 0

    def test_invalid_file_returns_1(self, tmp_dir, capsys):
        p = tmp_dir / "invalid.md"
        p.write_text(INVALID_CONTENT, encoding="utf-8")
        rc, out, err = _capture(capsys, ["validate", str(p)])
        assert rc == 1

    def test_valid_file_prints_valid(self, tmp_dir, capsys):
        p = tmp_dir / "valid.md"
        p.write_text(VALID_CONTENT, encoding="utf-8")
        rc, out, err = _capture(capsys, ["validate", str(p)])
        assert "VALID" in out

    def test_invalid_file_prints_invalid(self, tmp_dir, capsys):
        p = tmp_dir / "invalid.md"
        p.write_text(INVALID_CONTENT, encoding="utf-8")
        rc, out, err = _capture(capsys, ["validate", str(p)])
        assert "INVALID" in out

    def test_nonexistent_file_returns_1(self, tmp_dir, capsys):
        rc, out, err = _capture(capsys, ["validate", str(tmp_dir / "ghost.md")])
        assert rc == 1

    def test_validate_multiple_files_all_valid(self, tmp_dir, capsys):
        p1 = tmp_dir / "a.md"
        p2 = tmp_dir / "b.md"
        p1.write_text(VALID_CONTENT, encoding="utf-8")
        p2.write_text(VALID_CONTENT, encoding="utf-8")
        rc, out, err = _capture(capsys, ["validate", str(p1), str(p2)])
        assert rc == 0

    def test_validate_one_invalid_returns_1(self, tmp_dir, capsys):
        p1 = tmp_dir / "good.md"
        p2 = tmp_dir / "bad.md"
        p1.write_text(VALID_CONTENT, encoding="utf-8")
        p2.write_text(INVALID_CONTENT, encoding="utf-8")
        rc, out, err = _capture(capsys, ["validate", str(p1), str(p2)])
        assert rc == 1

    def test_validate_shows_agent_name(self, tmp_dir, capsys):
        p = tmp_dir / "valid.md"
        p.write_text(VALID_CONTENT, encoding="utf-8")
        rc, out, err = _capture(capsys, ["validate", str(p)])
        assert "my-agent" in out

    def test_validate_shows_model(self, tmp_dir, capsys):
        p = tmp_dir / "valid.md"
        p.write_text(VALID_CONTENT, encoding="utf-8")
        rc, out, err = _capture(capsys, ["validate", str(p)])
        assert "sonnet" in out

    def test_validate_shows_error_prefix(self, tmp_dir, capsys):
        p = tmp_dir / "invalid.md"
        p.write_text(INVALID_CONTENT, encoding="utf-8")
        rc, out, err = _capture(capsys, ["validate", str(p)])
        assert "ERROR" in out or "WARN" in out


# ---------------------------------------------------------------------------
# --version flag
# ---------------------------------------------------------------------------


class TestVersionFlag:
    def test_version_flag_raises_system_exit(self, capsys):
        with pytest.raises(SystemExit) as exc_info:
            main(["--version"])
        assert exc_info.value.code == 0

    def test_version_output_contains_version(self, capsys):
        with pytest.raises(SystemExit):
            main(["--version"])
        captured = capsys.readouterr()
        assert __version__ in captured.out or __version__ in captured.err

    def test_version_matches_package_version(self):
        assert __version__ == "0.1.0"


# ---------------------------------------------------------------------------
# build_parser tests
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Error paths in _cmd_init and _cmd_init_team (ValueError from scaffold)
# ---------------------------------------------------------------------------


class TestCmdInitErrorPath:
    """Test the ValueError except branch in _cmd_init and _cmd_init_team.

    argparse already blocks invalid choices, so we reach these branches by
    patching the underlying scaffold functions to raise ValueError.
    """

    def test_cmd_init_value_error_returns_1(self, tmp_dir, capsys):
        from unittest.mock import patch
        from cervellaswarm_agent_templates.cli import _cmd_init
        import argparse

        args = argparse.Namespace(
            type="worker",
            name=None,
            output=str(tmp_dir),
            team="my-team",
            specialty="generic",
        )
        with patch(
            "cervellaswarm_agent_templates.cli.create_agent",
            side_effect=ValueError("bad specialty"),
        ):
            rc = _cmd_init(args)
        assert rc == 1

    def test_cmd_init_value_error_prints_to_stderr(self, tmp_dir, capsys):
        from unittest.mock import patch
        from cervellaswarm_agent_templates.cli import _cmd_init
        import argparse

        args = argparse.Namespace(
            type="worker",
            name=None,
            output=str(tmp_dir),
            team="my-team",
            specialty="generic",
        )
        with patch(
            "cervellaswarm_agent_templates.cli.create_agent",
            side_effect=ValueError("bad specialty"),
        ):
            _cmd_init(args)
        captured = capsys.readouterr()
        assert "Error" in captured.err or "bad specialty" in captured.err

    def test_cmd_init_team_value_error_returns_1(self, tmp_dir, capsys):
        from unittest.mock import patch
        from cervellaswarm_agent_templates.cli import _cmd_init_team
        import argparse

        args = argparse.Namespace(
            preset="minimal",
            name="my-team",
            output=str(tmp_dir),
        )
        with patch(
            "cervellaswarm_agent_templates.cli.create_team",
            side_effect=ValueError("bad preset"),
        ):
            rc = _cmd_init_team(args)
        assert rc == 1

    def test_cmd_init_team_value_error_prints_to_stderr(self, tmp_dir, capsys):
        from unittest.mock import patch
        from cervellaswarm_agent_templates.cli import _cmd_init_team
        import argparse

        args = argparse.Namespace(
            preset="minimal",
            name="my-team",
            output=str(tmp_dir),
        )
        with patch(
            "cervellaswarm_agent_templates.cli.create_team",
            side_effect=ValueError("bad preset"),
        ):
            _cmd_init_team(args)
        captured = capsys.readouterr()
        assert "Error" in captured.err or "bad preset" in captured.err


class TestBuildParser:
    def test_returns_argument_parser(self):
        import argparse
        parser = build_parser()
        assert isinstance(parser, argparse.ArgumentParser)

    def test_parser_prog_name(self):
        parser = build_parser()
        assert parser.prog == "cervella-agent"

    def test_init_subcommand_exists(self):
        parser = build_parser()
        # Should parse "init coordinator" without error
        args = parser.parse_args(["init", "coordinator"])
        assert args.command == "init"
        assert args.type == "coordinator"

    def test_list_subcommand_exists(self):
        parser = build_parser()
        args = parser.parse_args(["list"])
        assert args.command == "list"

    def test_init_team_subcommand_exists(self):
        parser = build_parser()
        args = parser.parse_args(["init-team", "minimal"])
        assert args.command == "init-team"
        assert args.preset == "minimal"

    def test_validate_subcommand_exists(self):
        parser = build_parser()
        args = parser.parse_args(["validate", "agent.md"])
        assert args.command == "validate"
        assert args.files == ["agent.md"]

    def test_init_defaults(self):
        parser = build_parser()
        args = parser.parse_args(["init", "worker"])
        assert args.name is None
        assert args.team == "my-team"
        assert args.specialty == "generic"
        assert args.output == "."

    def test_init_team_defaults(self):
        parser = build_parser()
        args = parser.parse_args(["init-team", "standard"])
        assert args.name == "my-team"
        assert args.output == "."

    def test_validate_multiple_files(self):
        parser = build_parser()
        args = parser.parse_args(["validate", "a.md", "b.md", "c.md"])
        assert len(args.files) == 3
