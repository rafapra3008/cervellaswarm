# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for cli module. All SpawnManager operations are mocked."""

import sys
from io import StringIO
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from cervellaswarm_spawn_workers import __version__
from cervellaswarm_spawn_workers.cli import (
    _cmd_kill,
    _cmd_list,
    _cmd_status,
    _cmd_team,
    _cmd_worker,
    _format_uptime,
    main,
)
from cervellaswarm_spawn_workers.prompt_builder import SPECIALTIES
from cervellaswarm_spawn_workers.spawner import SpawnResult, WorkerInfo, WorkerStatus


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_worker(name="alpha", backend="tmux", session_name="swarm_alpha_1", pid=None):
    """Create a stub WorkerInfo."""
    return WorkerInfo(name=name, backend=backend, session_name=session_name, pid=pid)


def _make_status(name="alpha", alive=True, backend="tmux", session_name="swarm_alpha_1", pid=None, uptime=30.0):
    """Create a stub WorkerStatus."""
    return WorkerStatus(
        name=name,
        alive=alive,
        backend=backend,
        pid=pid,
        session_name=session_name,
        uptime_seconds=uptime,
    )


def _run_main(argv, capsys=None):
    """Run main() and return captured output."""
    with patch("cervellaswarm_spawn_workers.cli.SpawnManager"):
        main(argv)


# ---------------------------------------------------------------------------
# main() dispatch
# ---------------------------------------------------------------------------


def test_main_list_calls_cmd_list(capsys):
    """main --list calls _cmd_list and prints specialties."""
    with patch("cervellaswarm_spawn_workers.cli._cmd_list") as mock_list:
        main(["--list"])
    mock_list.assert_called_once()


def test_main_status_calls_cmd_status(capsys):
    """main --status calls _cmd_status."""
    with patch("cervellaswarm_spawn_workers.cli._cmd_status") as mock_status:
        main(["--status"])
    mock_status.assert_called_once()


def test_main_kill_calls_cmd_kill():
    """main --kill calls _cmd_kill."""
    with patch("cervellaswarm_spawn_workers.cli._cmd_kill") as mock_kill:
        main(["--kill"])
    mock_kill.assert_called_once()


def test_main_team_calls_cmd_team():
    """main --team path calls _cmd_team."""
    with patch("cervellaswarm_spawn_workers.cli._cmd_team") as mock_team:
        main(["--team", "/tmp/team.yaml"])
    mock_team.assert_called_once()


def test_main_worker_calls_cmd_worker():
    """main --worker name calls _cmd_worker."""
    with patch("cervellaswarm_spawn_workers.cli._cmd_worker") as mock_worker:
        main(["--worker", "myworker"])
    mock_worker.assert_called_once()


def test_main_no_args_prints_help(capsys):
    """main with no arguments calls print_help and returns normally."""
    # main([]) calls parser.print_help() then returns - no SystemExit unlike --help
    with patch("cervellaswarm_spawn_workers.cli.SpawnManager"):
        main([])  # Should not raise

    captured = capsys.readouterr()
    # print_help writes to stdout
    assert "cervella-spawn" in captured.out or "usage" in captured.out.lower()


def test_main_version_shows_version(capsys):
    """main --version outputs the package version."""
    with pytest.raises(SystemExit):
        main(["--version"])
    captured = capsys.readouterr()
    assert __version__ in captured.out


# ---------------------------------------------------------------------------
# _cmd_list()
# ---------------------------------------------------------------------------


def test_cmd_list_prints_all_specialties(capsys):
    """_cmd_list prints all specialty names."""
    _cmd_list()
    captured = capsys.readouterr()
    for name in SPECIALTIES:
        assert name in captured.out


def test_cmd_list_prints_header(capsys):
    """_cmd_list prints a header line."""
    _cmd_list()
    captured = capsys.readouterr()
    assert "specialties" in captured.out.lower()


# ---------------------------------------------------------------------------
# _cmd_status()
# ---------------------------------------------------------------------------


def _make_args(**kwargs):
    """Build a minimal namespace for CLI args."""
    import argparse
    defaults = {
        "tasks_dir": ".swarm/tasks",
        "logs_dir": ".swarm/logs",
        "max_workers": 5,
        "backend": None,
        "claude_bin": None,
        "specialty": "generic",
        "prompt": None,
        "worker": None,
        "team": None,
    }
    defaults.update(kwargs)
    return argparse.Namespace(**defaults)


def test_cmd_status_shows_column_headers(capsys):
    """_cmd_status prints NAME/STATUS/BACKEND/UPTIME/SESSION columns."""
    mock_manager = MagicMock()
    mock_manager.get_status.return_value = [_make_status()]

    with patch("cervellaswarm_spawn_workers.cli.SpawnManager", return_value=mock_manager):
        _cmd_status(_make_args())

    captured = capsys.readouterr()
    assert "NAME" in captured.out
    assert "STATUS" in captured.out
    assert "BACKEND" in captured.out
    assert "UPTIME" in captured.out


def test_cmd_status_shows_alive_for_alive_workers(capsys):
    """_cmd_status shows ALIVE for alive workers."""
    mock_manager = MagicMock()
    mock_manager.get_status.return_value = [_make_status(alive=True)]

    with patch("cervellaswarm_spawn_workers.cli.SpawnManager", return_value=mock_manager):
        _cmd_status(_make_args())

    captured = capsys.readouterr()
    assert "ALIVE" in captured.out


def test_cmd_status_shows_dead_for_dead_workers(capsys):
    """_cmd_status shows DEAD for dead workers."""
    mock_manager = MagicMock()
    mock_manager.get_status.return_value = [_make_status(alive=False, uptime=0.0)]

    with patch("cervellaswarm_spawn_workers.cli.SpawnManager", return_value=mock_manager):
        _cmd_status(_make_args())

    captured = capsys.readouterr()
    assert "DEAD" in captured.out


def test_cmd_status_no_workers_message(capsys):
    """_cmd_status prints 'No workers tracked.' when list is empty."""
    mock_manager = MagicMock()
    mock_manager.get_status.return_value = []

    with patch("cervellaswarm_spawn_workers.cli.SpawnManager", return_value=mock_manager):
        _cmd_status(_make_args())

    captured = capsys.readouterr()
    assert "No workers tracked." in captured.out


# ---------------------------------------------------------------------------
# _cmd_kill()
# ---------------------------------------------------------------------------


def test_cmd_kill_calls_kill_all(capsys):
    """_cmd_kill calls manager.kill_all()."""
    mock_manager = MagicMock()
    mock_manager.kill_all.return_value = 3

    with patch("cervellaswarm_spawn_workers.cli.SpawnManager", return_value=mock_manager):
        _cmd_kill(_make_args())

    mock_manager.kill_all.assert_called_once()


def test_cmd_kill_calls_cleanup(capsys):
    """_cmd_kill calls manager.cleanup() after killing."""
    mock_manager = MagicMock()
    mock_manager.kill_all.return_value = 2

    with patch("cervellaswarm_spawn_workers.cli.SpawnManager", return_value=mock_manager):
        _cmd_kill(_make_args())

    mock_manager.cleanup.assert_called_once()


def test_cmd_kill_prints_killed_count(capsys):
    """_cmd_kill prints the number of killed workers."""
    mock_manager = MagicMock()
    mock_manager.kill_all.return_value = 4

    with patch("cervellaswarm_spawn_workers.cli.SpawnManager", return_value=mock_manager):
        _cmd_kill(_make_args())

    captured = capsys.readouterr()
    assert "4" in captured.out


# ---------------------------------------------------------------------------
# _cmd_team()
# ---------------------------------------------------------------------------


def test_cmd_team_loads_team_config(tmp_path, capsys):
    """_cmd_team loads team config from the given path."""
    team_file = tmp_path / "team.yaml"
    team_file.write_text("name: test-team\nagents: []\n")

    mock_manager = MagicMock()
    mock_manager.backend = "tmux"
    mock_result = SpawnResult(spawned=0, failed=0, workers=[], errors=[])
    mock_manager.spawn_team.return_value = mock_result

    from cervellaswarm_spawn_workers.team_loader import TeamConfig, SpawnConfig
    mock_team = TeamConfig(name="test-team", spawn=SpawnConfig())

    with patch("cervellaswarm_spawn_workers.cli.SpawnManager", return_value=mock_manager), \
         patch("cervellaswarm_spawn_workers.cli.load_team", return_value=mock_team) as mock_load:
        _cmd_team(_make_args(team=str(team_file)))

    mock_load.assert_called_once_with(Path(str(team_file)))


def test_cmd_team_spawns_workers(tmp_path, capsys):
    """_cmd_team calls manager.spawn_team with the loaded team config."""
    team_file = tmp_path / "team.yaml"
    team_file.write_text("name: test\nagents: []\n")

    mock_manager = MagicMock()
    mock_manager.backend = "tmux"
    mock_result = SpawnResult(spawned=2, failed=0, workers=[_make_worker("w1"), _make_worker("w2")], errors=[])
    mock_manager.spawn_team.return_value = mock_result

    from cervellaswarm_spawn_workers.team_loader import TeamConfig, SpawnConfig
    mock_team = TeamConfig(name="test", spawn=SpawnConfig())

    with patch("cervellaswarm_spawn_workers.cli.SpawnManager", return_value=mock_manager), \
         patch("cervellaswarm_spawn_workers.cli.load_team", return_value=mock_team):
        _cmd_team(_make_args(team=str(team_file)))

    mock_manager.spawn_team.assert_called_once_with(mock_team)


def test_cmd_team_shows_spawned_count(tmp_path, capsys):
    """_cmd_team prints the spawned worker count."""
    team_file = tmp_path / "team.yaml"
    team_file.write_text("name: test\nagents: []\n")

    mock_manager = MagicMock()
    mock_manager.backend = "tmux"
    mock_result = SpawnResult(spawned=3, failed=0, workers=[_make_worker() for _ in range(3)], errors=[])
    mock_manager.spawn_team.return_value = mock_result

    from cervellaswarm_spawn_workers.team_loader import TeamConfig, SpawnConfig
    mock_team = TeamConfig(name="test", spawn=SpawnConfig())

    with patch("cervellaswarm_spawn_workers.cli.SpawnManager", return_value=mock_manager), \
         patch("cervellaswarm_spawn_workers.cli.load_team", return_value=mock_team):
        _cmd_team(_make_args(team=str(team_file)))

    captured = capsys.readouterr()
    assert "3" in captured.out


def test_cmd_team_shows_errors_on_failure(tmp_path, capsys):
    """_cmd_team prints failure count and errors."""
    team_file = tmp_path / "team.yaml"
    team_file.write_text("name: test\nagents: []\n")

    mock_manager = MagicMock()
    mock_manager.backend = "tmux"
    mock_result = SpawnResult(spawned=1, failed=1, workers=[_make_worker()], errors=["w2: max workers"])
    mock_manager.spawn_team.return_value = mock_result

    from cervellaswarm_spawn_workers.team_loader import TeamConfig, SpawnConfig
    mock_team = TeamConfig(name="test", spawn=SpawnConfig())

    with patch("cervellaswarm_spawn_workers.cli.SpawnManager", return_value=mock_manager), \
         patch("cervellaswarm_spawn_workers.cli.load_team", return_value=mock_team):
        _cmd_team(_make_args(team=str(team_file)))

    captured = capsys.readouterr()
    assert "1" in captured.out
    assert "w2" in captured.out or "max workers" in captured.out


def test_cmd_team_exits_1_on_file_not_found(tmp_path, capsys):
    """_cmd_team exits with code 1 when team config file is missing."""
    with patch("cervellaswarm_spawn_workers.cli.load_team", side_effect=FileNotFoundError("not found")):
        with pytest.raises(SystemExit) as exc_info:
            _cmd_team(_make_args(team="/nonexistent/team.yaml"))
    assert exc_info.value.code == 1


def test_cmd_team_exits_1_on_invalid_yaml(tmp_path, capsys):
    """_cmd_team exits with code 1 on invalid YAML (ValueError)."""
    with patch("cervellaswarm_spawn_workers.cli.load_team", side_effect=ValueError("bad yaml")):
        with pytest.raises(SystemExit) as exc_info:
            _cmd_team(_make_args(team="/some/team.yaml"))
    assert exc_info.value.code == 1


def test_cmd_team_applies_all_spawn_config_fields(capsys):
    """_cmd_team creates manager with team.yaml dirs from the start (not post-override)."""
    from cervellaswarm_spawn_workers.team_loader import TeamConfig, SpawnConfig

    mock_team = TeamConfig(
        name="test",
        spawn=SpawnConfig(
            backend="nohup",
            max_workers=3,
            tasks_dir="/custom/tasks",
            logs_dir="/custom/logs",
            status_dir="/custom/status",
        ),
    )

    mock_manager = MagicMock()
    mock_manager.backend = "nohup"
    mock_manager.spawn_team.return_value = SpawnResult(spawned=0)

    with patch("cervellaswarm_spawn_workers.cli.SpawnManager", return_value=mock_manager) as MockMgr, \
         patch("cervellaswarm_spawn_workers.cli.load_team", return_value=mock_team):
        _cmd_team(_make_args(team="/fake/team.yaml"))

    # Verify SpawnManager was created with team's dirs (not default then overridden)
    call_kwargs = MockMgr.call_args[1]
    assert call_kwargs["tasks_dir"] == "/custom/tasks"
    assert call_kwargs["logs_dir"] == "/custom/logs"
    assert call_kwargs["status_dir"] == "/custom/status"
    assert call_kwargs["max_workers"] == 3
    assert call_kwargs["backend"] == "nohup"


# ---------------------------------------------------------------------------
# _cmd_worker()
# ---------------------------------------------------------------------------


def test_cmd_worker_spawns_worker(capsys):
    """_cmd_worker calls manager.spawn_worker with correct name."""
    mock_manager = MagicMock()
    mock_worker = _make_worker("myworker")
    mock_manager.spawn_worker.return_value = mock_worker

    with patch("cervellaswarm_spawn_workers.cli.SpawnManager", return_value=mock_manager):
        _cmd_worker(_make_args(worker="myworker"))

    mock_manager.spawn_worker.assert_called_once()
    call_kwargs = mock_manager.spawn_worker.call_args
    assert call_kwargs[1]["name"] == "myworker" or call_kwargs[0][0] == "myworker"


def test_cmd_worker_uses_custom_prompt(capsys):
    """_cmd_worker passes custom prompt when --prompt is given."""
    mock_manager = MagicMock()
    mock_worker = _make_worker("myworker")
    mock_manager.spawn_worker.return_value = mock_worker

    with patch("cervellaswarm_spawn_workers.cli.SpawnManager", return_value=mock_manager), \
         patch("cervellaswarm_spawn_workers.cli.build_worker_prompt") as mock_build:
        _cmd_worker(_make_args(worker="myworker", prompt="my custom prompt"))

    # build_worker_prompt should NOT be called when custom prompt is provided
    mock_build.assert_not_called()
    call_kwargs = mock_manager.spawn_worker.call_args[1]
    assert call_kwargs["system_prompt"] == "my custom prompt"


def test_cmd_worker_auto_generates_prompt_when_not_provided(capsys):
    """_cmd_worker calls build_worker_prompt when no --prompt given."""
    mock_manager = MagicMock()
    mock_worker = _make_worker("myworker")
    mock_manager.spawn_worker.return_value = mock_worker

    with patch("cervellaswarm_spawn_workers.cli.SpawnManager", return_value=mock_manager), \
         patch("cervellaswarm_spawn_workers.cli.build_worker_prompt", return_value="auto-gen") as mock_build:
        _cmd_worker(_make_args(worker="myworker", prompt=None, specialty="backend"))

    mock_build.assert_called_once_with("myworker", "backend", ".swarm/tasks")


def test_cmd_worker_exits_1_on_runtime_error(capsys):
    """_cmd_worker exits with code 1 on RuntimeError."""
    mock_manager = MagicMock()
    mock_manager.spawn_worker.side_effect = RuntimeError("max workers reached")

    with patch("cervellaswarm_spawn_workers.cli.SpawnManager", return_value=mock_manager):
        with pytest.raises(SystemExit) as exc_info:
            _cmd_worker(_make_args(worker="myworker"))

    assert exc_info.value.code == 1


def test_cmd_worker_shows_session_name(capsys):
    """_cmd_worker prints session name when worker has session_name."""
    mock_manager = MagicMock()
    mock_worker = _make_worker("myworker", session_name="swarm_myworker_99")
    mock_manager.spawn_worker.return_value = mock_worker

    with patch("cervellaswarm_spawn_workers.cli.SpawnManager", return_value=mock_manager):
        _cmd_worker(_make_args(worker="myworker"))

    captured = capsys.readouterr()
    assert "swarm_myworker_99" in captured.out


def test_cmd_worker_shows_pid(capsys):
    """_cmd_worker prints PID when worker has pid."""
    mock_manager = MagicMock()
    mock_worker = _make_worker("myworker", session_name=None, pid=4242)
    mock_manager.spawn_worker.return_value = mock_worker

    with patch("cervellaswarm_spawn_workers.cli.SpawnManager", return_value=mock_manager):
        _cmd_worker(_make_args(worker="myworker"))

    captured = capsys.readouterr()
    assert "4242" in captured.out


# ---------------------------------------------------------------------------
# _format_uptime()
# ---------------------------------------------------------------------------


def test_format_uptime_seconds_only():
    """_format_uptime returns Xs for values less than 60."""
    assert _format_uptime(0) == "0s"
    assert _format_uptime(45) == "45s"
    assert _format_uptime(59) == "59s"


def test_format_uptime_minutes_and_seconds():
    """_format_uptime returns Xm Ys for values between 60 and 3599 seconds."""
    assert _format_uptime(60) == "1m 0s"
    assert _format_uptime(90) == "1m 30s"
    assert _format_uptime(3599) == "59m 59s"


def test_format_uptime_hours_and_minutes():
    """_format_uptime returns Xh Ym for values of 3600 seconds or more."""
    assert _format_uptime(3600) == "1h 0m"
    assert _format_uptime(3660) == "1h 1m"
    assert _format_uptime(7200) == "2h 0m"
    assert _format_uptime(7322) == "2h 2m"
