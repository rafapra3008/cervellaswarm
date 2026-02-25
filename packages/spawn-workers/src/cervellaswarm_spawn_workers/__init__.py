# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""CervellaSwarm Spawn Workers - Config-driven worker spawning for multi-agent systems."""

from importlib.metadata import version as _version

__version__ = _version("cervellaswarm-spawn-workers")

from cervellaswarm_spawn_workers.backend import (
    ProcessInfo,
    detect_backend,
    is_alive_tmux,
    is_alive_pid,
    kill_pid,
    kill_tmux,
    launch_nohup,
    launch_tmux,
    list_tmux_sessions,
)
from cervellaswarm_spawn_workers.team_loader import (
    AgentConfig,
    SpawnConfig,
    TeamConfig,
    get_spawnables,
    load_team,
    load_team_string,
)
from cervellaswarm_spawn_workers.spawner import (
    SpawnManager,
    SpawnResult,
    WorkerInfo,
    WorkerStatus,
)
from cervellaswarm_spawn_workers.prompt_builder import (
    SPECIALTIES,
    build_base_prompt,
    build_worker_prompt,
)

__all__ = [
    # backend
    "ProcessInfo",
    "detect_backend",
    "is_alive_tmux",
    "is_alive_pid",
    "kill_pid",
    "kill_tmux",
    "launch_nohup",
    "launch_tmux",
    "list_tmux_sessions",
    # team_loader
    "AgentConfig",
    "SpawnConfig",
    "TeamConfig",
    "get_spawnables",
    "load_team",
    "load_team_string",
    # spawner
    "SpawnManager",
    "SpawnResult",
    "WorkerInfo",
    "WorkerStatus",
    # prompt_builder
    "SPECIALTIES",
    "build_base_prompt",
    "build_worker_prompt",
]
