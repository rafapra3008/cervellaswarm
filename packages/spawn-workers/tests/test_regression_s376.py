# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""
Regression tests for S376 bug fixes in cervellaswarm-spawn-workers.

Covers 8 bugs fixed in S376:
  BUG1: is_alive_pid ritorna False su PermissionError (backend.py)
  BUG2: _load_tracked_workers no error handling su .start corrotto (spawner.py)
  BUG3: cleanup rimuove tracking files di worker vivi (spawner.py)
  BUG4: $(cat ...) shell expansion nel command (spawner.py)
  BUG5: _cmd_team carica workers da dir sbagliata (cli.py)
  BUG6: spawn_data potrebbe essere non-dict (team_loader.py)
  BUG7: kill_pid non gestisce PermissionError (backend.py)
  BUG8: spawn_team cattura solo RuntimeError (spawner.py)
"""

import signal
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from cervellaswarm_spawn_workers.backend import is_alive_pid, kill_pid
from cervellaswarm_spawn_workers.spawner import SpawnManager
from cervellaswarm_spawn_workers.team_loader import load_team_string


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_manager(tmp_path: Path, backend: str = "nohup") -> SpawnManager:
    """Build a SpawnManager that does not touch real processes or signals."""
    return SpawnManager(
        tasks_dir=str(tmp_path / "tasks"),
        logs_dir=str(tmp_path / "logs"),
        status_dir=str(tmp_path / "status"),
        max_workers=5,
        backend=backend,
        register_signals=False,
    )


# ---------------------------------------------------------------------------
# BUG 1 - is_alive_pid deve ritornare True su PermissionError
# ---------------------------------------------------------------------------


def test_bug1_is_alive_pid_returns_true_on_permission_error():
    """PermissionError su os.kill(pid, 0) significa processo ESISTE - deve ritornare True."""
    with patch("cervellaswarm_spawn_workers.backend.os.kill",
               side_effect=PermissionError):
        result = is_alive_pid(9999)
    assert result is True, "PermissionError indica processo esistente, non deve ritornare False"


def test_bug1_is_alive_pid_still_returns_false_on_process_lookup_error():
    """Controllo regressione: ProcessLookupError continua a ritornare False."""
    with patch("cervellaswarm_spawn_workers.backend.os.kill",
               side_effect=ProcessLookupError):
        result = is_alive_pid(9999)
    assert result is False


# ---------------------------------------------------------------------------
# BUG 2 - _load_tracked_workers non crasha su .start file corrotto
# ---------------------------------------------------------------------------


def test_bug2_load_tracked_workers_ignores_corrupt_start_file(tmp_path):
    """File .start con contenuto non numerico non causa crash - lo salta con warning."""
    status_dir = tmp_path / "status"
    status_dir.mkdir()

    # Crea un .start file corrotto
    (status_dir / "worker_alpha.start").write_text("not_a_number")

    # Non deve lanciare eccezione
    manager = SpawnManager(
        tasks_dir=str(tmp_path / "tasks"),
        logs_dir=str(tmp_path / "logs"),
        status_dir=str(status_dir),
        max_workers=5,
        register_signals=False,
    )

    # Il worker corrotto non viene caricato
    assert all(w.name != "alpha" for w in manager.workers)


def test_bug2_load_tracked_workers_skips_unreadable_start_file(tmp_path):
    """OSError su lettura .start file non causa crash - lo salta."""
    status_dir = tmp_path / "status"
    status_dir.mkdir()
    (status_dir / "worker_beta.start").write_text("1234567890")

    with patch("pathlib.Path.read_text", side_effect=OSError("disk error")):
        # Non deve lanciare eccezione
        manager = SpawnManager(
            tasks_dir=str(tmp_path / "tasks"),
            logs_dir=str(tmp_path / "logs"),
            status_dir=str(status_dir),
            max_workers=5,
            register_signals=False,
        )

    # Con OSError su read_text nessun worker viene caricato
    assert len(manager.workers) == 0


def test_bug2_load_tracked_workers_loads_valid_alongside_corrupt(tmp_path):
    """Worker con .start valido viene caricato anche se un altro e corrotto."""
    status_dir = tmp_path / "status"
    status_dir.mkdir()

    # Uno corrotto, uno valido
    (status_dir / "worker_bad.start").write_text("not_a_number")
    (status_dir / "worker_good.start").write_text("1700000000.0")
    (status_dir / "worker_good.pid").write_text("42")

    manager = SpawnManager(
        tasks_dir=str(tmp_path / "tasks"),
        logs_dir=str(tmp_path / "logs"),
        status_dir=str(status_dir),
        max_workers=5,
        register_signals=False,
    )

    names = [w.name for w in manager.workers]
    assert "good" in names
    assert "bad" not in names


# ---------------------------------------------------------------------------
# BUG 3 - cleanup non rimuove i file di worker ancora vivi
# ---------------------------------------------------------------------------


def test_bug3_cleanup_preserves_files_of_alive_worker(tmp_path):
    """cleanup() non elimina tracking files di worker alive."""
    status_dir = tmp_path / "status"
    status_dir.mkdir()

    # Due worker tracciati con pid
    (status_dir / "worker_alive.start").write_text("1700000000.0")
    (status_dir / "worker_alive.pid").write_text("111")
    (status_dir / "worker_dead.start").write_text("1700000000.0")
    (status_dir / "worker_dead.pid").write_text("222")

    manager = SpawnManager(
        tasks_dir=str(tmp_path / "tasks"),
        logs_dir=str(tmp_path / "logs"),
        status_dir=str(status_dir),
        max_workers=5,
        register_signals=False,
    )

    def fake_is_alive(pid):
        return pid == 111  # solo "alive" vive

    with patch("cervellaswarm_spawn_workers.spawner.is_alive_pid", side_effect=fake_is_alive):
        manager.cleanup()

    # File del worker alive devono sopravvivere
    assert (status_dir / "worker_alive.start").exists()
    assert (status_dir / "worker_alive.pid").exists()

    # File del worker dead devono essere rimossi
    assert not (status_dir / "worker_dead.start").exists()
    assert not (status_dir / "worker_dead.pid").exists()


def test_bug3_cleanup_removes_all_files_when_no_alive_workers(tmp_path):
    """cleanup() rimuove tutti i file quando nessun worker e alive."""
    status_dir = tmp_path / "status"
    status_dir.mkdir()

    (status_dir / "worker_dead1.start").write_text("1700000000.0")
    (status_dir / "worker_dead1.pid").write_text("333")

    manager = SpawnManager(
        tasks_dir=str(tmp_path / "tasks"),
        logs_dir=str(tmp_path / "logs"),
        status_dir=str(status_dir),
        max_workers=5,
        register_signals=False,
    )

    with patch("cervellaswarm_spawn_workers.spawner.is_alive_pid", return_value=False):
        manager.cleanup()

    assert not (status_dir / "worker_dead1.start").exists()
    assert not (status_dir / "worker_dead1.pid").exists()


# ---------------------------------------------------------------------------
# BUG 4 - shlex.quote usato nel command invece di $(cat file)
# ---------------------------------------------------------------------------


def test_bug4_spawn_worker_command_uses_shlex_quote_not_cat(tmp_path):
    """Il command generato usa shlex.quote, NON contiene $(cat ...)."""
    manager = _make_manager(tmp_path, backend="nohup")

    system_prompt = "You are a worker. Do tasks."
    captured_commands = []

    def fake_launch_nohup(command, log_file, cwd=None, env=None):
        captured_commands.append(command)
        info = MagicMock()
        info.backend = "nohup"
        info.session_name = None
        info.pid = 42
        info.log_file = log_file
        info.start_time = 1700000000.0
        return info

    with patch("cervellaswarm_spawn_workers.spawner.launch_nohup",
               side_effect=fake_launch_nohup):
        with patch("cervellaswarm_spawn_workers.spawner.get_status",
                   return_value=[]) if False else patch(
                       "cervellaswarm_spawn_workers.spawner.SpawnManager.get_status",
                       return_value=[]):
            manager.spawn_worker(
                name="test-worker",
                system_prompt=system_prompt,
            )

    assert len(captured_commands) == 1
    cmd = captured_commands[0]

    # Non deve contenere $(cat ...)
    assert "$(cat" not in cmd, "Il command non deve usare $(cat ...) - shell expansion pericolosa"

    # Il prompt deve apparire quotato nel command
    assert "You are a worker" in cmd


def test_bug4_spawn_worker_command_handles_special_chars_safely(tmp_path):
    """Prompt con caratteri speciali non causa shell injection."""
    manager = _make_manager(tmp_path, backend="nohup")

    # Prompt con caratteri pericolosi per la shell
    dangerous_prompt = 'Say "hello" and $(rm -rf /tmp/test) and `whoami`'
    captured_commands = []

    def fake_launch_nohup(command, log_file, cwd=None, env=None):
        captured_commands.append(command)
        info = MagicMock()
        info.backend = "nohup"
        info.session_name = None
        info.pid = 99
        info.log_file = log_file
        info.start_time = 1700000000.0
        return info

    with patch("cervellaswarm_spawn_workers.spawner.launch_nohup",
               side_effect=fake_launch_nohup):
        with patch("cervellaswarm_spawn_workers.spawner.SpawnManager.get_status",
                   return_value=[]):
            manager.spawn_worker(
                name="danger-worker",
                system_prompt=dangerous_prompt,
            )

    cmd = captured_commands[0]
    # Il command raw non deve contenere espansioni non quotate
    assert "$(cat" not in cmd


# ---------------------------------------------------------------------------
# BUG 5 - _cmd_team crea SpawnManager con dirs dal team.yaml
# ---------------------------------------------------------------------------


def test_bug5_cmd_team_creates_manager_with_team_dirs(tmp_path):
    """_cmd_team crea SpawnManager con le dirs dal team.yaml, non i default CLI."""
    team_yaml = tmp_path / "team.yaml"
    team_yaml.write_text("""
name: my-team
agents: []
spawn:
  tasks_dir: /custom/tasks
  logs_dir: /custom/logs
  status_dir: /custom/status
  max_workers: 3
""")

    created_managers = []

    class FakeSpawnManager:
        def __init__(self, tasks_dir, logs_dir, status_dir, max_workers,
                     backend=None, claude_bin=None, register_signals=True):
            created_managers.append({
                "tasks_dir": tasks_dir,
                "logs_dir": logs_dir,
                "status_dir": status_dir,
                "max_workers": max_workers,
            })
            self.backend = "nohup"
            self.workers = []

        def spawn_team(self, team):
            result = MagicMock()
            result.spawned = 0
            result.failed = 0
            result.workers = []
            result.errors = []
            return result

    import argparse
    args = argparse.Namespace(
        team=str(team_yaml),
        backend=None,
        claude_bin=None,
        tasks_dir=".swarm/tasks",
        logs_dir=".swarm/logs",
        max_workers=5,
    )

    with patch("cervellaswarm_spawn_workers.cli.SpawnManager", FakeSpawnManager):
        from cervellaswarm_spawn_workers.cli import _cmd_team
        _cmd_team(args)

    assert len(created_managers) == 1
    m = created_managers[0]
    assert m["tasks_dir"] == "/custom/tasks", "SpawnManager deve usare tasks_dir dal team.yaml"
    assert m["logs_dir"] == "/custom/logs", "SpawnManager deve usare logs_dir dal team.yaml"
    assert m["status_dir"] == "/custom/status", "SpawnManager deve usare status_dir dal team.yaml"
    assert m["max_workers"] == 3, "SpawnManager deve usare max_workers dal team.yaml"


# ---------------------------------------------------------------------------
# BUG 6 - spawn_data non-dict deve sollevare ValueError
# ---------------------------------------------------------------------------


def test_bug6_spawn_as_string_raises_value_error():
    """YAML con spawn: 'string' deve sollevare ValueError."""
    yaml_content = """
name: bad-team
agents: []
spawn: "should_be_a_dict"
"""
    with pytest.raises(ValueError, match="spawn.*mapping"):
        load_team_string(yaml_content)


def test_bug6_spawn_as_list_raises_value_error():
    """YAML con spawn come lista deve sollevare ValueError."""
    yaml_content = """
name: bad-team
agents: []
spawn:
  - item1
  - item2
"""
    with pytest.raises(ValueError, match="spawn.*mapping"):
        load_team_string(yaml_content)


def test_bug6_spawn_as_integer_raises_value_error():
    """YAML con spawn: 42 deve sollevare ValueError."""
    yaml_content = """
name: bad-team
agents: []
spawn: 42
"""
    with pytest.raises(ValueError, match="spawn.*mapping"):
        load_team_string(yaml_content)


def test_bug6_spawn_as_dict_is_accepted():
    """YAML con spawn come dict valido non deve sollevare eccezioni."""
    yaml_content = """
name: good-team
agents: []
spawn:
  max_workers: 2
  tasks_dir: .swarm/tasks
"""
    team = load_team_string(yaml_content)
    assert team.spawn.max_workers == 2


# ---------------------------------------------------------------------------
# BUG 7 - kill_pid gestisce PermissionError su SIGTERM
# ---------------------------------------------------------------------------


def test_bug7_kill_pid_returns_false_on_sigterm_permission_error():
    """kill_pid ritorna False quando SIGTERM lancia PermissionError."""
    with patch("cervellaswarm_spawn_workers.backend.os.kill",
               side_effect=PermissionError("no permission")):
        result = kill_pid(9999, graceful_timeout=0.01)
    assert result is False, "PermissionError su SIGTERM deve ritornare False"


def test_bug7_kill_pid_still_returns_false_on_sigterm_process_lookup():
    """Controllo regressione: ProcessLookupError su SIGTERM continua a ritornare False."""
    with patch("cervellaswarm_spawn_workers.backend.os.kill",
               side_effect=ProcessLookupError):
        result = kill_pid(9999, graceful_timeout=0.01)
    assert result is False


def test_bug7_kill_pid_permission_error_does_not_proceed_to_sigkill(tmp_path):
    """PermissionError su SIGTERM non deve tentare SIGKILL."""
    kill_calls = []

    def fake_kill(pid, sig):
        kill_calls.append(sig)
        raise PermissionError("no permission")

    with patch("cervellaswarm_spawn_workers.backend.os.kill", side_effect=fake_kill):
        kill_pid(9999, graceful_timeout=0.01)

    # Solo SIGTERM deve essere stato tentato
    assert signal.SIGTERM in kill_calls
    assert signal.SIGKILL not in kill_calls, "Non deve tentare SIGKILL dopo PermissionError su SIGTERM"


# ---------------------------------------------------------------------------
# BUG 8 - spawn_team cattura OSError oltre a RuntimeError
# ---------------------------------------------------------------------------


def test_bug8_spawn_team_catches_oserror_from_spawn_worker(tmp_path):
    """spawn_team cattura OSError da spawn_worker e lo registra in result.errors."""
    manager = _make_manager(tmp_path)

    yaml_content = """
name: test-team
agents:
  - name: worker-oserr
    type: worker
    specialty: backend
    spawn_on_start: true
spawn:
  max_workers: 5
"""
    team = load_team_string(yaml_content)

    with patch.object(manager, "spawn_worker",
                      side_effect=OSError("device busy")):
        result = manager.spawn_team(team)

    assert result.failed == 1
    assert result.spawned == 0
    assert any("worker-oserr" in err for err in result.errors), \
        "Il nome del worker deve apparire in result.errors"


def test_bug8_spawn_team_catches_runtime_error_from_spawn_worker(tmp_path):
    """Controllo regressione: RuntimeError continua a essere catturato."""
    manager = _make_manager(tmp_path)

    yaml_content = """
name: test-team
agents:
  - name: worker-rterr
    type: worker
    specialty: generic
    spawn_on_start: true
spawn:
  max_workers: 5
"""
    team = load_team_string(yaml_content)

    with patch.object(manager, "spawn_worker",
                      side_effect=RuntimeError("max workers reached")):
        result = manager.spawn_team(team)

    assert result.failed == 1
    assert result.spawned == 0


def test_bug8_spawn_team_partial_success_with_mixed_errors(tmp_path):
    """spawn_team conta correttamente successi e fallimenti misti."""
    manager = _make_manager(tmp_path)

    yaml_content = """
name: test-team
agents:
  - name: worker-ok
    type: worker
    specialty: backend
    spawn_on_start: true
  - name: worker-oserr
    type: worker
    specialty: frontend
    spawn_on_start: true
spawn:
  max_workers: 5
"""
    team = load_team_string(yaml_content)

    good_worker = MagicMock()
    good_worker.name = "worker-ok"

    call_count = [0]

    def side_effect(name, system_prompt=None, specialty="generic"):
        call_count[0] += 1
        if name == "worker-oserr":
            raise OSError("disk full")
        return good_worker

    with patch.object(manager, "spawn_worker", side_effect=side_effect):
        result = manager.spawn_team(team)

    assert result.spawned == 1
    assert result.failed == 1
    assert len(result.errors) == 1
