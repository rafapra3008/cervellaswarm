# cervellaswarm-spawn-workers

Config-driven worker spawning for multi-agent systems.

> Part of [CervellaSwarm](https://github.com/rafapra3008/cervellaswarm) - Build AI agent teams that remember.

## Features

- **Auto-detect backend**: tmux (preferred) or nohup (universal fallback)
- **Config-driven**: Spawn teams from `team.yaml` files
- **Signal handling**: Graceful shutdown on SIGINT/SIGTERM
- **Health checks**: Monitor worker status, uptime, and liveness
- **File-based state**: `.ready` / `.working` / `.done` task markers
- **Cross-platform**: Works on macOS and Linux

## Quick Start

```bash
pip install cervellaswarm-spawn-workers
```

```bash
# Spawn a single worker
cervella-spawn --worker backend --specialty backend

# Spawn a team from config
cervella-spawn --team team.yaml

# Check worker status
cervella-spawn --status

# Kill all workers
cervella-spawn --kill

# List available specialties
cervella-spawn --list
```

## How It Works

```
team.yaml ──→ TeamLoader ──→ SpawnManager ──→ Backend (tmux/nohup)
                                   │
                              PromptBuilder
                                   │
                          claude -p --append-system-prompt
```

1. **TeamLoader** reads your `team.yaml` and extracts agent configurations
2. **PromptBuilder** generates English system prompts with specialty focus
3. **SpawnManager** launches workers via the detected backend
4. Workers check `tasks_dir/` for `.ready` files, claim with `.working`, finish with `.done`

## team.yaml Format

```yaml
name: my-project
version: "1.0.0"
process: hierarchical

agents:
  - name: backend
    type: worker
    specialty: backend
    model: sonnet

  - name: tester
    type: worker
    specialty: tester
    model: sonnet

spawn:
  max_workers: 5
  tasks_dir: .swarm/tasks
  logs_dir: .swarm/logs
  backend: tmux  # or "nohup", omit for auto-detect
```

## CLI Reference

```
cervella-spawn [OPTIONS]

Options:
  --team PATH          Spawn workers from team.yaml config
  --worker NAME        Spawn a single worker by name
  --status             Show worker status (alive/dead/uptime)
  --kill               Kill all workers gracefully
  --list               List available worker specialties
  --specialty TYPE     Worker specialty (default: generic)
  --prompt TEXT        Custom system prompt for the worker
  --tasks-dir DIR      Tasks directory (default: .swarm/tasks)
  --logs-dir DIR       Logs directory (default: .swarm/logs)
  --max-workers N      Max concurrent workers (default: 5)
  --backend TYPE       Force backend: tmux or nohup
  --claude-bin PATH    Path to claude CLI binary
  --version            Show version
```

## Available Specialties

| Specialty | Focus Area |
|-----------|------------|
| `backend` | Python, FastAPI, databases, API design |
| `frontend` | React, CSS, Tailwind, UI/UX, accessibility |
| `tester` | Testing, debugging, QA, validation |
| `docs` | Documentation, README, guides, tutorials |
| `devops` | Deployment, CI/CD, Docker, infrastructure |
| `data` | SQL, analytics, database design, ETL |
| `security` | Security audits, vulnerability assessment |
| `researcher` | Technical research, analysis, reports |
| `reviewer` | Code review, best practices, architecture |
| `generic` | General-purpose tasks across all domains |

## Python API

```python
from cervellaswarm_spawn_workers import SpawnManager, load_team

# Spawn from team config
team = load_team(Path("team.yaml"))
manager = SpawnManager(max_workers=5)
result = manager.spawn_team(team)
print(f"Spawned: {result.spawned}, Failed: {result.failed}")

# Spawn a single worker
worker = manager.spawn_worker(
    name="backend",
    specialty="backend",
)

# Check status
for status in manager.get_status():
    print(f"{status.name}: {'ALIVE' if status.alive else 'DEAD'}")

# Cleanup
manager.kill_all()
```

## How It Compares

| Feature | CervellaSwarm | CrewAI | AutoGen | LangGraph |
|---------|:---:|:---:|:---:|:---:|
| Config-driven spawn | team.yaml | agents.yaml | No | No |
| Subprocess isolation | tmux/nohup | threads | threads | in-process |
| Backend auto-detect | Yes | N/A | N/A | N/A |
| Signal handling | SIGINT/SIGTERM | No | No | No |
| File-based state | .ready/.working/.done | No | No | No |
| Worker health check | CLI `--status` | No | max_turns | No |
| Cross-platform | macOS + Linux | Yes | Yes | Yes |
| Dependencies | 1 (pyyaml) | 20+ | 15+ | 10+ |

> **Honest note:** CrewAI and AutoGen excel at in-process agent orchestration with rich LLM routing.
> CervellaSwarm targets a different niche: subprocess-isolated workers with file-based coordination,
> ideal for long-running tasks where process isolation and crash recovery matter.

## Architecture

The package has 4 core modules:

- **`backend`** - Execution backends (tmux/nohup) with auto-detection
- **`team_loader`** - YAML config parser compatible with agent-templates
- **`spawner`** - SpawnManager lifecycle (spawn, monitor, kill, cleanup)
- **`prompt_builder`** - English system prompt generation with specialties

## Development

```bash
git clone https://github.com/rafapra3008/cervellaswarm.git
cd cervellaswarm/packages/spawn-workers
pip install -e ".[test]"
pytest
```

## License

Apache-2.0 - See [LICENSE](LICENSE) for details.
