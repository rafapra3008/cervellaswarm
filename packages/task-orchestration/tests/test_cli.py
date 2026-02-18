# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for cervellaswarm_task_orchestration.cli."""

import json
import pytest
from pathlib import Path
from unittest.mock import patch

from cervellaswarm_task_orchestration.cli import (
    main_classify,
    main_route,
    main_validate_plan,
    main_validate_output,
    main_task,
    main,
)
from cervellaswarm_task_orchestration import __version__

# Minimal valid plan for validate-plan tests
VALID_PLAN = """## Metadata
- Task ID: TASK_001
- Complexity: complex
- Files Affected: `src/main.py`, `tests/test_main.py`

## Phase 1: Understanding
Understand the problem. See `config.json`.

### Success Criteria
- All tests pass

## Phase 2: Design
Design the solution.

### Execution Order
1. Step one
2. Step two

## Phase 3: Review
Review the design.

## Phase 4: Final Plan
The final plan is ready.
""" + ("x" * 500)  # ensure >500 chars

LONG_VALID_OUTPUT = "Task completed successfully. All tests PASSED. DONE. " * 5


# ---------------------------------------------------------------------------
# main_classify
# ---------------------------------------------------------------------------


def test_main_classify_basic(capsys):
    main_classify(["fix typo in README"])
    out = capsys.readouterr().out
    assert "Complexity" in out
    assert "simple" in out.lower()


def test_main_classify_complex_task(capsys):
    main_classify(["refactor the entire architecture"])
    out = capsys.readouterr().out
    assert "Complexity" in out


def test_main_classify_json_output(capsys):
    main_classify(["--json", "refactor the entire architecture"])
    out = capsys.readouterr().out
    data = json.loads(out)
    assert "complexity" in data
    assert "should_architect" in data
    assert "confidence" in data
    assert "triggers" in data
    assert "reasoning" in data


def test_main_classify_json_should_architect_simple(capsys):
    main_classify(["--json", "fix typo"])
    out = capsys.readouterr().out
    data = json.loads(out)
    assert data["should_architect"] is False


def test_main_classify_version(capsys):
    with pytest.raises(SystemExit) as exc:
        main_classify(["--version"])
    assert exc.value.code == 0
    captured = capsys.readouterr()
    assert __version__ in captured.out or __version__ in captured.err


def test_main_classify_multi_word_description(capsys):
    main_classify(["update", "the", "comment", "in", "file"])
    out = capsys.readouterr().out
    assert "Complexity" in out


# ---------------------------------------------------------------------------
# main_route
# ---------------------------------------------------------------------------


def test_main_route_basic(capsys):
    main_route(["fix a small typo"])
    out = capsys.readouterr().out
    assert "Use Architect" in out


def test_main_route_json(capsys):
    main_route(["--json", "fix a small typo"])
    out = capsys.readouterr().out
    data = json.loads(out)
    assert "use_architect" in data
    assert "complexity" in data
    assert "confidence" in data
    assert "reason" in data
    assert "suggested_workers" in data


def test_main_route_force_architect(capsys):
    main_route(["--force-architect", "--json", "fix a typo"])
    out = capsys.readouterr().out
    data = json.loads(out)
    assert data["use_architect"] is True


def test_main_route_force_direct(capsys):
    main_route(["--force-direct", "--json", "refactor entire system"])
    out = capsys.readouterr().out
    data = json.loads(out)
    assert data["use_architect"] is False


def test_main_route_version(capsys):
    with pytest.raises(SystemExit) as exc:
        main_route(["--version"])
    assert exc.value.code == 0


def test_main_route_shows_workers_when_direct(capsys):
    main_route(["fix", "a", "bug", "in", "pytest"])
    out = capsys.readouterr().out
    assert "Suggested Workers" in out or "use_architect" in out.lower()


# ---------------------------------------------------------------------------
# main_validate_plan
# ---------------------------------------------------------------------------


def test_main_validate_plan_valid_file(tmp_path, capsys):
    plan_file = tmp_path / "plan.md"
    plan_file.write_text(VALID_PLAN)
    main_validate_plan([str(plan_file)])
    out = capsys.readouterr().out
    assert "Valid" in out
    assert "Score" in out


def test_main_validate_plan_missing_file(tmp_path, capsys):
    missing = str(tmp_path / "nonexistent.md")
    main_validate_plan([missing])
    out = capsys.readouterr().out
    assert "not found" in out.lower() or "False" in out


def test_main_validate_plan_json_valid(tmp_path, capsys):
    plan_file = tmp_path / "plan.md"
    plan_file.write_text(VALID_PLAN)
    main_validate_plan(["--json", str(plan_file)])
    out = capsys.readouterr().out
    data = json.loads(out)
    assert "valid" in data
    assert "score" in data
    assert "errors" in data
    assert "warnings" in data


def test_main_validate_plan_json_missing_file(tmp_path, capsys):
    missing = str(tmp_path / "nonexistent.md")
    main_validate_plan(["--json", missing])
    out = capsys.readouterr().out
    data = json.loads(out)
    assert data["valid"] is False
    assert len(data["errors"]) > 0


def test_main_validate_plan_version(capsys):
    with pytest.raises(SystemExit) as exc:
        main_validate_plan(["--version", "dummy.md"])
    assert exc.value.code == 0


# ---------------------------------------------------------------------------
# main_validate_output
# ---------------------------------------------------------------------------


def test_main_validate_output_file_valid(tmp_path, capsys):
    f = tmp_path / "TASK_001_output.md"
    f.write_text(LONG_VALID_OUTPUT)
    with pytest.raises(SystemExit) as exc:
        main_validate_output(["--file", str(f)])
    assert exc.value.code == 0
    out = capsys.readouterr().out
    assert "VALID" in out


def test_main_validate_output_file_invalid(tmp_path, capsys):
    f = tmp_path / "TASK_001_output.md"
    f.write_text("Error: fatal crash\nTraceback\nFAILED\n" + LONG_VALID_OUTPUT)
    with pytest.raises(SystemExit) as exc:
        main_validate_output(["--file", str(f)])
    assert exc.value.code == 1
    out = capsys.readouterr().out
    assert "INVALID" in out


def test_main_validate_output_file_json(tmp_path, capsys):
    f = tmp_path / "TASK_001_output.md"
    f.write_text(LONG_VALID_OUTPUT)
    with pytest.raises(SystemExit):
        main_validate_output(["--file", str(f), "--json"])
    out = capsys.readouterr().out
    data = json.loads(out)
    assert "valid" in data
    assert "score" in data
    assert "errors" in data
    assert "warnings" in data
    assert "retry_needed" in data
    assert "retry_context" in data


def test_main_validate_output_last_output_not_found(tmp_path, capsys):
    with patch("cervellaswarm_task_orchestration.cli.find_last_output", return_value=None):
        with pytest.raises(SystemExit) as exc:
            main_validate_output(["--last-output"])
    assert exc.value.code == 2


def test_main_validate_output_last_output_found(tmp_path, capsys):
    f = tmp_path / "TASK_001_output.md"
    f.write_text(LONG_VALID_OUTPUT)
    with patch("cervellaswarm_task_orchestration.cli.find_last_output", return_value=f):
        with pytest.raises(SystemExit) as exc:
            main_validate_output(["--last-output"])
    assert exc.value.code == 0


def test_main_validate_output_task_found(tmp_path, capsys):
    f = tmp_path / "TASK_001_output.md"
    f.write_text(LONG_VALID_OUTPUT)
    with patch("cervellaswarm_task_orchestration.cli.find_task_output", return_value=f):
        with pytest.raises(SystemExit) as exc:
            main_validate_output(["--task", "TASK_001"])
    assert exc.value.code == 0


def test_main_validate_output_task_not_found(tmp_path, capsys):
    with patch("cervellaswarm_task_orchestration.cli.find_task_output", return_value=None):
        with pytest.raises(SystemExit) as exc:
            main_validate_output(["--task", "TASK_999"])
    assert exc.value.code == 2


def test_main_validate_output_missing_file_exits(tmp_path, capsys):
    missing = str(tmp_path / "missing.md")
    with pytest.raises(SystemExit) as exc:
        main_validate_output(["--file", missing])
    assert exc.value.code == 1


# ---------------------------------------------------------------------------
# main_task - list
# ---------------------------------------------------------------------------


def test_main_task_list_no_tasks(capsys, monkeypatch):
    monkeypatch.setattr(
        "cervellaswarm_task_orchestration.cli.list_tasks", lambda: []
    )
    main_task(["list"])
    out = capsys.readouterr().out
    assert "No tasks" in out


def test_main_task_list_with_tasks(capsys, monkeypatch):
    monkeypatch.setattr(
        "cervellaswarm_task_orchestration.cli.list_tasks",
        lambda: [{"task_id": "TASK_001", "status": "created", "ack": "-/-/-",
                  "agent": "agent", "file": "/tmp/TASK_001.md"}],
    )
    main_task(["list"])
    out = capsys.readouterr().out
    assert "TASK_001" in out


# ---------------------------------------------------------------------------
# main_task - create
# ---------------------------------------------------------------------------


def test_main_task_create_success(tmp_path, capsys, monkeypatch):
    monkeypatch.setattr(
        "cervellaswarm_task_orchestration.cli.create_task",
        lambda task_id, agent, desc, risk: str(tmp_path / f"{task_id}.md"),
    )
    main_task(["create", "TASK_001", "agent", "Do the thing", "--risk", "1"])
    out = capsys.readouterr().out
    assert "TASK_001" in out
    assert "created" in out.lower()


def test_main_task_create_invalid_id(capsys):
    with pytest.raises(SystemExit) as exc:
        main_task(["create", "../../evil", "agent", "desc"])
    assert exc.value.code == 1
    err = capsys.readouterr().err
    assert "Error" in err or "Invalid" in err


def test_main_task_create_duplicate(tmp_path, capsys, monkeypatch):
    monkeypatch.setattr(
        "cervellaswarm_task_orchestration.cli.create_task",
        lambda *a, **kw: (_ for _ in ()).throw(FileExistsError("already exists")),
    )
    with pytest.raises(SystemExit) as exc:
        main_task(["create", "TASK_001", "agent", "desc"])
    assert exc.value.code == 1


# ---------------------------------------------------------------------------
# main_task - status transitions
# ---------------------------------------------------------------------------


def test_main_task_ready(capsys, monkeypatch):
    monkeypatch.setattr(
        "cervellaswarm_task_orchestration.cli.mark_ready", lambda tid: True
    )
    main_task(["ready", "TASK_001"])
    out = capsys.readouterr().out
    assert "READY" in out


def test_main_task_working(capsys, monkeypatch):
    monkeypatch.setattr(
        "cervellaswarm_task_orchestration.cli.mark_working", lambda tid: True
    )
    main_task(["working", "TASK_001"])
    out = capsys.readouterr().out
    assert "WORKING" in out


def test_main_task_done(capsys, monkeypatch):
    monkeypatch.setattr(
        "cervellaswarm_task_orchestration.cli.mark_done", lambda tid: True
    )
    main_task(["done", "TASK_001"])
    out = capsys.readouterr().out
    assert "DONE" in out


def test_main_task_status(capsys, monkeypatch):
    monkeypatch.setattr(
        "cervellaswarm_task_orchestration.cli.get_task_status", lambda tid: "ready"
    )
    monkeypatch.setattr(
        "cervellaswarm_task_orchestration.cli.get_ack_status", lambda tid: "Y/-/-"
    )
    main_task(["status", "TASK_001"])
    out = capsys.readouterr().out
    assert "TASK_001" in out
    assert "READY" in out


def test_main_task_cleanup(capsys, monkeypatch):
    monkeypatch.setattr(
        "cervellaswarm_task_orchestration.cli.cleanup_task", lambda tid: True
    )
    main_task(["cleanup", "TASK_001"])
    out = capsys.readouterr().out
    assert "TASK_001" in out
    assert "removed" in out


def test_main_task_no_command_shows_help(capsys):
    with pytest.raises(SystemExit) as exc:
        main_task([])
    assert exc.value.code == 0


# ---------------------------------------------------------------------------
# main() - unified dispatcher
# ---------------------------------------------------------------------------


def test_main_no_args_shows_help(capsys):
    with pytest.raises(SystemExit) as exc:
        main([])
    assert exc.value.code == 0


def test_main_dispatches_classify(capsys):
    main(["classify", "fix typo"])
    out = capsys.readouterr().out
    assert "Complexity" in out


def test_main_dispatches_route(capsys):
    main(["route", "fix a typo"])
    out = capsys.readouterr().out
    assert "Use Architect" in out


def test_main_dispatches_validate_plan(tmp_path, capsys):
    plan_file = tmp_path / "plan.md"
    plan_file.write_text(VALID_PLAN)
    main(["validate-plan", str(plan_file)])
    out = capsys.readouterr().out
    assert "Valid" in out or "Score" in out


def test_main_dispatches_validate_output(tmp_path, capsys):
    f = tmp_path / "TASK_001_output.md"
    f.write_text(LONG_VALID_OUTPUT)
    with pytest.raises(SystemExit) as exc:
        main(["validate-output", "--file", str(f)])
    assert exc.value.code == 0


def test_main_dispatches_task(capsys, monkeypatch):
    monkeypatch.setattr(
        "cervellaswarm_task_orchestration.cli.list_tasks", lambda: []
    )
    main(["task", "list"])
    out = capsys.readouterr().out
    assert "No tasks" in out


def test_main_version(capsys):
    with pytest.raises(SystemExit) as exc:
        main(["--version"])
    assert exc.value.code == 0
    captured = capsys.readouterr()
    assert __version__ in captured.out or __version__ in captured.err
