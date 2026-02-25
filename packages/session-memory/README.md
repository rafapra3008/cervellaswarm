# cervellaswarm-session-memory

**Git-native, human-readable session memory for AI agents.**

Every decision is a commit. Every state is Markdown. Every audit trail is a `git log` away.

```
Session 1          Session 2          Session 3
   |                  |                  |
   v                  v                  v
+-----------+    +-----------+    +-----------+
| State.md  |--->| State.md  |--->| State.md  |
| (v1)      |    | (v2)      |    | (v3)      |
+-----------+    +-----------+    +-----------+
   |                  |                  |
   v                  v                  v
  git commit        git commit        git commit
```

No vector databases. No cloud services. No embedding models.

## Why This Exists

AI agent frameworks lose context between sessions. Your agent forgets decisions, repeats mistakes, and can't explain what happened yesterday.

Current solutions store memory in opaque binary formats (LanceDB, ChromaDB, Qdrant) that you can't read, can't version-control, and can't audit.

**cervellaswarm-session-memory** takes a different approach: plain Markdown files tracked in git.

## Installation

```bash
pip install cervellaswarm-session-memory
```

Requires Python 3.10+. Single dependency: `pyyaml`.

## Quick Start

### Initialize a project

```bash
cervella-session init my-project
```

This creates:

```
.session-memory/
  my-project/
    SESSION_STATE_my-project.md    # Your session state
    archive/                        # Old states go here
PROJECT_COMPASS.md                  # Project direction
```

### Check quality

```bash
cervella-session check my-project
```

Scores your session state on 4 criteria (0-10 scale):
- **Actionability** (30%): Are there clear TODOs and next steps?
- **Specificity** (30%): Dates and numbers, or vague "soon" and "maybe"?
- **Freshness** (20%): Updated this week, or gathering dust?
- **Conciseness** (20%): Within line limits, or a novel?

### Audit for secrets

```bash
cervella-session audit .session-memory/
```

Detects accidentally committed API keys, tokens, passwords, and private keys. Supports custom patterns via config.

### Verify sync status

```bash
cervella-session sync my-project
```

Checks freshness, file size limits, git tracking, and uncommitted changes.

### List projects

```bash
cervella-session list
```

## Python API

```python
from cervellaswarm_session_memory import (
    init_project,
    check_quality,
    audit_directory,
    verify_project,
    discover_projects,
)

# Initialize
project = init_project("my-project", project_root=Path("/path/to/repo"))

# Quality check
result = check_quality(project.state_file, project.name)
print(f"Score: {result.total}/10 [{result.status}]")

# Secret audit
audit = audit_directory(Path(".session-memory"))
assert audit.clean, f"Found {audit.critical_count} critical secrets!"

# Sync verification
sync = verify_project("my-project")
print(f"Overall: {sync.overall.value}")

# Discovery
projects = discover_projects()
for p in projects:
    print(f"  {p.name}: {p.state_file}")
```

## Configuration

Create `.cervella/session-memory.yaml` in your project root:

```yaml
# Where session memory files live
memory_dir: ".session-memory"

# File size limits
max_lines: 300
warning_lines: 200

# Quality scoring weights (must sum to 1.0)
quality:
  weights:
    actionability: 0.30
    specificity: 0.30
    freshness: 0.20
    conciseness: 0.20
  target_score: 8.0

# Secret scanning
secrets:
  extra_patterns:
    - pattern: "CUSTOM_KEY_[a-zA-Z0-9]+"
      name: "Custom API Key"

# Multi-project registry
projects:
  my-app:
    path: ~/projects/my-app
  my-api:
    path: ~/projects/my-api
```

Config priority: `CERVELLASWARM_SESSION_MEMORY_CONFIG` env var > project `.cervella/session-memory.yaml` > user `~/.claude/session-memory.yaml` > defaults.

## How It Compares

| Feature | CervellaSwarm | CrewAI Memory | AutoGen Memory | Letta |
|---------|--------------|---------------|----------------|-------|
| Storage format | **Markdown files** | LanceDB (binary) | ChromaDB (binary) | PostgreSQL |
| Version control | **git native** | manual | none | developing |
| Human readable | **100%** | no | no | partial |
| Cloud required | **never** | optional | optional | optional |
| Setup time | **< 5 min** | 10-30 min | varies | varies |
| Audit trail | **`git log`** | none | none | developing |
| EU AI Act ready | **yes** | no | no | developing |
| Dependencies | **1 (pyyaml)** | LanceDB + embeddings | ChromaDB + embeddings | PostgreSQL + more |
| Multi-project | **native** | no | no | no |

> **Honest note:** CrewAI and AutoGen offer semantic search over memory using vector embeddings, which we deliberately don't include. If you need similarity-based retrieval, pair this package with `cervellaswarm-code-intelligence` or use a vector store alongside it. Our bet is that explicit, human-curated session state is more reliable than automated extraction for critical decisions.

## Template System

Session state files are created from templates with `{{ placeholder }}` substitution. The built-in templates provide a battle-tested structure for tracking:

- **Session progress**: What was done, what's next
- **Decisions**: What was decided, why, and when
- **Project status**: Progress bars and phase tracking
- **Archive**: Historical session summaries

## JSON Output

All CLI commands support `--json` for integration with CI/CD and automation:

```bash
cervella-session check --json | jq '.[] | select(.total < 8)'
```

## License

Apache-2.0. See [LICENSE](LICENSE) for details.

## Part of CervellaSwarm

This package is part of the [CervellaSwarm](https://github.com/rafapra3008/cervellaswarm) multi-agent framework. Other packages:

- [`cervellaswarm-code-intelligence`](https://pypi.org/project/cervellaswarm-code-intelligence/) - AST-based code analysis
- [`cervellaswarm-agent-hooks`](../agent-hooks/) - Lifecycle hooks for Claude Code agents
- [`cervellaswarm-agent-templates`](../agent-templates/) - Agent definition templates
- [`cervellaswarm-task-orchestration`](../task-orchestration/) - Deterministic task routing
- [`cervellaswarm-spawn-workers`](../spawn-workers/) - Worker process management
