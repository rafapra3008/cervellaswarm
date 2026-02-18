# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""
Team configuration loader.

Reads team.yaml files (compatible with cervellaswarm-agent-templates)
and extracts spawn-relevant configuration.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import yaml


@dataclass
class AgentConfig:
    """Configuration for a single agent to spawn."""

    name: str
    type: str = "worker"
    specialty: str = "generic"
    model: str = "sonnet"
    role: str = ""
    prompt_file: Optional[str] = None
    system_prompt: Optional[str] = None
    spawn_on_start: bool = True


@dataclass
class SpawnConfig:
    """Spawn-specific configuration from team.yaml."""

    backend: Optional[str] = None  # None = auto-detect
    max_workers: int = 5
    tasks_dir: str = ".swarm/tasks"
    logs_dir: str = ".swarm/logs"
    status_dir: str = ".swarm/status"


@dataclass
class TeamConfig:
    """Complete team configuration."""

    name: str = "unnamed"
    version: str = "1.0.0"
    agents: list[AgentConfig] = field(default_factory=list)
    spawn: SpawnConfig = field(default_factory=SpawnConfig)
    entry_point: Optional[str] = None
    process: str = "hierarchical"


def load_team(path: Path) -> TeamConfig:
    """Load team configuration from a YAML file.

    Args:
        path: Path to team.yaml file.

    Returns:
        Parsed TeamConfig.

    Raises:
        FileNotFoundError: If the file doesn't exist.
        ValueError: If the YAML is invalid or missing required fields.
    """
    if not path.exists():
        raise FileNotFoundError(f"Team config not found: {path}")

    content = path.read_text()
    return load_team_string(content)


def load_team_string(content: str) -> TeamConfig:
    """Load team configuration from a YAML string.

    Args:
        content: YAML content string.

    Returns:
        Parsed TeamConfig.

    Raises:
        ValueError: If the YAML is invalid or missing required fields.
    """
    try:
        data = yaml.safe_load(content)
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML: {e}") from e

    if not isinstance(data, dict):
        raise ValueError("Team config must be a YAML mapping")

    if "name" not in data:
        raise ValueError("Team config must have a 'name' field")

    agents = []
    for agent_data in data.get("agents", []):
        if not isinstance(agent_data, dict):
            raise ValueError(f"Agent entry must be a mapping, got: {type(agent_data).__name__}")
        if "name" not in agent_data:
            raise ValueError("Each agent must have a 'name' field")
        agents.append(
            AgentConfig(
                name=agent_data["name"],
                type=agent_data.get("type", "worker"),
                specialty=agent_data.get("specialty", "generic"),
                model=agent_data.get("model", "sonnet"),
                role=agent_data.get("role", ""),
                prompt_file=agent_data.get("prompt_file"),
                system_prompt=agent_data.get("system_prompt"),
                spawn_on_start=agent_data.get("spawn_on_start", True),
            )
        )

    spawn_data = data.get("spawn", {})
    spawn = SpawnConfig(
        backend=spawn_data.get("backend"),
        max_workers=spawn_data.get("max_workers", 5),
        tasks_dir=spawn_data.get("tasks_dir", ".swarm/tasks"),
        logs_dir=spawn_data.get("logs_dir", ".swarm/logs"),
        status_dir=spawn_data.get("status_dir", ".swarm/status"),
    )

    return TeamConfig(
        name=data["name"],
        version=data.get("version", "1.0.0"),
        agents=agents,
        spawn=spawn,
        entry_point=data.get("entry_point"),
        process=data.get("process", "hierarchical"),
    )


def get_spawnables(team: TeamConfig) -> list[AgentConfig]:
    """Get agents that should be spawned.

    Returns agents where spawn_on_start is True and type is 'worker'.

    Args:
        team: TeamConfig to filter.

    Returns:
        List of AgentConfig for agents to spawn.
    """
    return [
        agent
        for agent in team.agents
        if agent.spawn_on_start and agent.type in ("worker", "guardian")
    ]
