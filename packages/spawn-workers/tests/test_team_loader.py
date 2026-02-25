# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for team_loader.py - team configuration parsing."""

import pytest

from cervellaswarm_spawn_workers.team_loader import (
    AgentConfig,
    SpawnConfig,
    TeamConfig,
    get_spawnables,
    load_team,
    load_team_string,
)


# ---------------------------------------------------------------------------
# load_team (file-based)
# ---------------------------------------------------------------------------


def test_load_team_loads_valid_file(tmp_path, sample_team_yaml):
    """Loads a valid team.yaml from disk."""
    yaml_file = tmp_path / "team.yaml"
    yaml_file.write_text(sample_team_yaml)

    config = load_team(yaml_file)
    assert config.name == "test-team"


def test_load_team_raises_file_not_found(tmp_path):
    """Raises FileNotFoundError for a missing file."""
    missing = tmp_path / "nonexistent.yaml"
    with pytest.raises(FileNotFoundError, match="Team config not found"):
        load_team(missing)


def test_load_team_raises_value_error_for_invalid_yaml(tmp_path):
    """Raises ValueError when the file contains invalid YAML."""
    bad_file = tmp_path / "bad.yaml"
    bad_file.write_text("key: [unclosed bracket")
    with pytest.raises(ValueError, match="Invalid YAML"):
        load_team(bad_file)


# ---------------------------------------------------------------------------
# load_team_string - minimal / full config
# ---------------------------------------------------------------------------


def test_load_team_string_parses_minimal_config():
    """Parses the minimal valid config - just a name."""
    config = load_team_string("name: my-team")
    assert config.name == "my-team"


def test_load_team_string_parses_full_config(sample_team_yaml):
    """Parses a full config with agents and spawn section."""
    config = load_team_string(sample_team_yaml)
    assert config.name == "test-team"
    assert len(config.agents) == 3
    assert config.spawn.max_workers == 3
    assert config.spawn.backend == "tmux"


# ---------------------------------------------------------------------------
# load_team_string - defaults
# ---------------------------------------------------------------------------


def test_load_team_string_default_version():
    """Sets version='1.0.0' when not specified."""
    config = load_team_string("name: alpha")
    assert config.version == "1.0.0"


def test_load_team_string_default_process():
    """Sets process='hierarchical' when not specified."""
    config = load_team_string("name: alpha")
    assert config.process == "hierarchical"


def test_load_team_string_explicit_version():
    """Parses specified version."""
    config = load_team_string("name: alpha\nversion: 2.5.0")
    assert config.version == "2.5.0"


def test_load_team_string_explicit_process():
    """Parses specified process."""
    config = load_team_string("name: alpha\nprocess: flat")
    assert config.process == "flat"


# ---------------------------------------------------------------------------
# load_team_string - agent field parsing
# ---------------------------------------------------------------------------


def test_load_team_string_agent_name():
    """Parses agent name field."""
    yaml = "name: t\nagents:\n  - name: worker-1\n"
    config = load_team_string(yaml)
    assert config.agents[0].name == "worker-1"


def test_load_team_string_agent_type():
    """Parses agent type field."""
    yaml = "name: t\nagents:\n  - name: w\n    type: guardian\n"
    config = load_team_string(yaml)
    assert config.agents[0].type == "guardian"


def test_load_team_string_agent_specialty():
    """Parses agent specialty field."""
    yaml = "name: t\nagents:\n  - name: w\n    specialty: frontend\n"
    config = load_team_string(yaml)
    assert config.agents[0].specialty == "frontend"


def test_load_team_string_agent_model():
    """Parses agent model field."""
    yaml = "name: t\nagents:\n  - name: w\n    model: opus\n"
    config = load_team_string(yaml)
    assert config.agents[0].model == "opus"


def test_load_team_string_agent_role():
    """Parses agent role field."""
    yaml = "name: t\nagents:\n  - name: w\n    role: Senior backend engineer\n"
    config = load_team_string(yaml)
    assert config.agents[0].role == "Senior backend engineer"


def test_load_team_string_agent_prompt_file():
    """Parses agent prompt_file field."""
    yaml = "name: t\nagents:\n  - name: w\n    prompt_file: prompts/worker.md\n"
    config = load_team_string(yaml)
    assert config.agents[0].prompt_file == "prompts/worker.md"


def test_load_team_string_agent_system_prompt():
    """Parses agent system_prompt field."""
    yaml = "name: t\nagents:\n  - name: w\n    system_prompt: You are helpful.\n"
    config = load_team_string(yaml)
    assert config.agents[0].system_prompt == "You are helpful."


def test_load_team_string_agent_spawn_on_start_false():
    """Parses agent spawn_on_start=false."""
    yaml = "name: t\nagents:\n  - name: w\n    spawn_on_start: false\n"
    config = load_team_string(yaml)
    assert config.agents[0].spawn_on_start is False


# ---------------------------------------------------------------------------
# load_team_string - agent defaults
# ---------------------------------------------------------------------------


def test_load_team_string_agent_default_type():
    """Agent defaults to type='worker' when not specified."""
    yaml = "name: t\nagents:\n  - name: w\n"
    config = load_team_string(yaml)
    assert config.agents[0].type == "worker"


def test_load_team_string_agent_default_specialty():
    """Agent defaults to specialty='generic' when not specified."""
    yaml = "name: t\nagents:\n  - name: w\n"
    config = load_team_string(yaml)
    assert config.agents[0].specialty == "generic"


def test_load_team_string_agent_default_model():
    """Agent defaults to model='sonnet' when not specified."""
    yaml = "name: t\nagents:\n  - name: w\n"
    config = load_team_string(yaml)
    assert config.agents[0].model == "sonnet"


def test_load_team_string_agent_default_spawn_on_start():
    """Agent defaults to spawn_on_start=True when not specified."""
    yaml = "name: t\nagents:\n  - name: w\n"
    config = load_team_string(yaml)
    assert config.agents[0].spawn_on_start is True


# ---------------------------------------------------------------------------
# load_team_string - spawn field parsing
# ---------------------------------------------------------------------------


def test_load_team_string_spawn_backend():
    """Parses spawn.backend field."""
    yaml = "name: t\nspawn:\n  backend: nohup\n"
    config = load_team_string(yaml)
    assert config.spawn.backend == "nohup"


def test_load_team_string_spawn_max_workers():
    """Parses spawn.max_workers field."""
    yaml = "name: t\nspawn:\n  max_workers: 10\n"
    config = load_team_string(yaml)
    assert config.spawn.max_workers == 10


def test_load_team_string_spawn_tasks_dir():
    """Parses spawn.tasks_dir field."""
    yaml = "name: t\nspawn:\n  tasks_dir: /custom/tasks\n"
    config = load_team_string(yaml)
    assert config.spawn.tasks_dir == "/custom/tasks"


def test_load_team_string_spawn_logs_dir():
    """Parses spawn.logs_dir field."""
    yaml = "name: t\nspawn:\n  logs_dir: /custom/logs\n"
    config = load_team_string(yaml)
    assert config.spawn.logs_dir == "/custom/logs"


def test_load_team_string_spawn_status_dir():
    """Parses spawn.status_dir field."""
    yaml = "name: t\nspawn:\n  status_dir: /custom/status\n"
    config = load_team_string(yaml)
    assert config.spawn.status_dir == "/custom/status"


def test_load_team_string_spawn_defaults_when_absent():
    """Spawn section uses defaults when key 'spawn' absent."""
    config = load_team_string("name: t")
    assert config.spawn.backend is None
    assert config.spawn.max_workers == 5
    assert config.spawn.tasks_dir == ".swarm/tasks"
    assert config.spawn.logs_dir == ".swarm/logs"
    assert config.spawn.status_dir == ".swarm/status"


# ---------------------------------------------------------------------------
# load_team_string - validation errors
# ---------------------------------------------------------------------------


def test_load_team_string_raises_when_not_dict():
    """Raises ValueError when YAML root is not a mapping."""
    with pytest.raises(ValueError, match="must be a YAML mapping"):
        load_team_string("- item1\n- item2\n")


def test_load_team_string_raises_when_name_missing():
    """Raises ValueError when 'name' field is absent."""
    with pytest.raises(ValueError, match="must have a 'name' field"):
        load_team_string("version: 1.0.0\n")


def test_load_team_string_raises_when_agent_is_not_dict():
    """Raises ValueError when an agent entry is not a mapping."""
    yaml = "name: t\nagents:\n  - just-a-string\n"
    with pytest.raises(ValueError, match="must be a mapping"):
        load_team_string(yaml)


def test_load_team_string_raises_when_agent_has_no_name():
    """Raises ValueError when an agent entry lacks 'name'."""
    yaml = "name: t\nagents:\n  - type: worker\n"
    with pytest.raises(ValueError, match="must have a 'name' field"):
        load_team_string(yaml)


def test_load_team_string_raises_on_invalid_yaml():
    """Raises ValueError on invalid YAML syntax."""
    with pytest.raises(ValueError, match="Invalid YAML"):
        load_team_string("key: [unclosed bracket")


# ---------------------------------------------------------------------------
# load_team_string - special fields
# ---------------------------------------------------------------------------


def test_load_team_string_parses_entry_point():
    """Parses entry_point field from config."""
    yaml = "name: t\nentry_point: scripts/run_team.py\n"
    config = load_team_string(yaml)
    assert config.entry_point == "scripts/run_team.py"


def test_load_team_string_entry_point_defaults_none():
    """entry_point defaults to None when absent."""
    config = load_team_string("name: t")
    assert config.entry_point is None


def test_load_team_string_handles_empty_agents_list():
    """Handles 'agents: []' without error."""
    yaml = "name: t\nagents: []\n"
    config = load_team_string(yaml)
    assert config.agents == []


def test_load_team_string_handles_absent_agents_key():
    """Handles missing 'agents' key - defaults to empty list."""
    config = load_team_string("name: t")
    assert config.agents == []


# ---------------------------------------------------------------------------
# get_spawnables
# ---------------------------------------------------------------------------


def _make_team(*agents: AgentConfig) -> TeamConfig:
    """Helper: build a TeamConfig with given agents."""
    return TeamConfig(name="test", agents=list(agents))


def test_get_spawnables_returns_workers_with_spawn_on_start():
    """Returns worker agents that have spawn_on_start=True."""
    team = _make_team(
        AgentConfig(name="w1", type="worker", spawn_on_start=True),
        AgentConfig(name="w2", type="worker", spawn_on_start=True),
    )
    result = get_spawnables(team)
    assert len(result) == 2
    assert result[0].name == "w1"
    assert result[1].name == "w2"


def test_get_spawnables_returns_guardians_with_spawn_on_start():
    """Returns guardian agents that have spawn_on_start=True."""
    team = _make_team(
        AgentConfig(name="g1", type="guardian", spawn_on_start=True),
    )
    result = get_spawnables(team)
    assert len(result) == 1
    assert result[0].name == "g1"


def test_get_spawnables_excludes_spawn_on_start_false():
    """Excludes agents with spawn_on_start=False."""
    team = _make_team(
        AgentConfig(name="w1", type="worker", spawn_on_start=True),
        AgentConfig(name="w2", type="worker", spawn_on_start=False),
    )
    result = get_spawnables(team)
    assert len(result) == 1
    assert result[0].name == "w1"


def test_get_spawnables_excludes_non_worker_non_guardian():
    """Excludes agents whose type is not 'worker' or 'guardian'."""
    team = _make_team(
        AgentConfig(name="leader1", type="leader", spawn_on_start=True),
        AgentConfig(name="w1", type="worker", spawn_on_start=True),
    )
    result = get_spawnables(team)
    assert len(result) == 1
    assert result[0].name == "w1"


def test_get_spawnables_returns_empty_when_no_agents():
    """Returns empty list when team has no agents."""
    team = _make_team()
    result = get_spawnables(team)
    assert result == []


def test_get_spawnables_mixed_types_and_flags():
    """Complex case: workers, guardians, leaders, mixed flags."""
    team = _make_team(
        AgentConfig(name="w1", type="worker", spawn_on_start=True),
        AgentConfig(name="w2", type="worker", spawn_on_start=False),
        AgentConfig(name="g1", type="guardian", spawn_on_start=True),
        AgentConfig(name="leader", type="leader", spawn_on_start=True),
    )
    result = get_spawnables(team)
    names = [a.name for a in result]
    assert "w1" in names
    assert "g1" in names
    assert "w2" not in names
    assert "leader" not in names
    assert len(result) == 2
