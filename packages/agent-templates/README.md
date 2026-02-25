# cervellaswarm-agent-templates

**Template agent definitions for Claude Code multi-agent teams.** Scaffold a coordinator, architect, quality gate, and specialized workers in under 10 minutes.

```
pip install cervellaswarm-agent-templates
cervella-agent init-team standard --name my-project
```

Built by the [CervellaSwarm](https://github.com/rafapra3008/cervellaswarm) team. Battle-tested with 17 AI agents across hundreds of real development sessions.

---

## Why Templates?

Claude Code [custom agents](https://docs.anthropic.com/en/docs/claude-code/sub-agents) use Markdown files with YAML frontmatter. But designing effective agent definitions from scratch means figuring out roles, tool permissions, output formats, and team composition by trial and error.

This package gives you **battle-tested templates** for 4 core agent roles, a **shared DNA** system for team-wide behavior, and a **team.yaml** composition format no other framework offers:

```
cervella-agent init-team standard --name my-project -o .claude/agents/

Created 9 files in .claude/agents/:
  _shared_dna.md     <-- Shared behavior for ALL agents
  team.yaml          <-- Declarative team composition
  lead.md            <-- Coordinator (Opus)
  planner.md         <-- Architect (Opus)
  reviewer.md        <-- Quality Gate (Opus)
  backend.md         <-- Backend Worker (Sonnet)
  frontend.md        <-- Frontend Worker (Sonnet)
  tester.md          <-- Tester Worker (Sonnet)
  researcher.md      <-- Researcher Worker (Sonnet)
```

## Agent Roles

| Role | Model | Purpose | Can Write Code? |
|------|-------|---------|-----------------|
| **Coordinator** | Opus | Routes tasks, delegates to specialists, consolidates results | No (delegates) |
| **Architect** | Opus | Plans complex changes, produces structured plans for workers | No (read-only) |
| **Quality Gate** | Opus | Reviews output, enforces standards, approves or rejects | Yes (fixes) |
| **Worker** | Sonnet | Implements changes in a specific domain (backend, frontend, etc.) | Yes |

Workers come in 7 specialties: `backend`, `frontend`, `tester`, `researcher`, `devops`, `docs`, `generic`.

## Quick Start

### 1. Create a single agent

```bash
# Create a coordinator
cervella-agent init coordinator --name my-lead

# Create a backend worker
cervella-agent init worker --name my-backend --specialty backend

# Create an architect
cervella-agent init architect --name my-planner
```

### 2. Create a full team

```bash
# Minimal team (3 agents: coordinator + worker + quality gate)
cervella-agent init-team minimal --name my-project -o .claude/agents/

# Standard team (7 agents: + architect, 4 workers)
cervella-agent init-team standard --name my-project -o .claude/agents/

# Full team (17 agents: all specialist roles)
cervella-agent init-team full --name my-project -o .claude/agents/
```

### 3. Validate your agents

```bash
# Check agent files for errors
cervella-agent validate .claude/agents/*.md
```

### 4. Customize

Edit the generated `.md` files to match your project. The YAML frontmatter controls capabilities; the Markdown body is the system prompt.

## The team.yaml Format

**No other multi-agent framework has declarative team composition.** CervellaSwarm introduces `team.yaml`:

```yaml
name: my-project
version: 1.0.0
description: Standard 7-agent team with architect and multiple workers
agents:
  - name: lead
    type: coordinator
    role: lead
  - name: planner
    type: architect
    role: planner
  - name: reviewer
    type: quality-gate
    role: validator
  - name: backend
    type: worker
    specialty: backend
    role: worker
  - name: frontend
    type: worker
    specialty: frontend
    role: worker
entry_point: lead
process: hierarchical
```

This file serves as the single source of truth for your team structure.

## Frontmatter Reference

Every agent file uses YAML frontmatter to declare its identity and capabilities:

```yaml
---
# IDENTITY
name: my-agent              # Required. Unique agent identifier
version: 1.0.0              # Semver. Track agent definition changes
updated: 2026-02-18         # Last modified date
description: >              # Required. What this agent does
  One-line summary shown in agent listings.
role: Worker                # Human-readable role label

# CAPABILITIES
model: sonnet               # Required. opus | sonnet | haiku
tools: Read, Edit, Bash     # Required. Comma-separated tool allowlist
disallowedTools: Write      # Explicit tool denylist
permissionMode: default     # default | plan | bypassPermissions | acceptEdits
maxTurns: 30                # Max API round-trips before stopping

# KNOWLEDGE
shared_dna: _shared_dna.md  # Shared behavior file (loaded automatically)

# MEMORY
memory: user                # Persistent memory: user | project | local
---
```

See [docs/FRONTMATTER_REFERENCE.md](docs/FRONTMATTER_REFERENCE.md) for the complete field reference.

## Shared DNA

The `_shared_dna.md` file defines behavior shared by ALL agents in your team. Instead of duplicating rules across every agent file, reference them once:

```markdown
> **Shared DNA:** See `_shared_dna.md` for team-wide rules.
```

The template includes:
- Autonomous decision rules (when to proceed vs. ask vs. stop)
- Structured output format
- Context efficiency guidelines
- Tool usage patterns

Customize it for your team's conventions, coding standards, and communication style.

## Comparison with Other Frameworks

| Feature | CervellaSwarm | CrewAI | AutoGen | LangGraph |
|---------|---------------|--------|---------|-----------|
| **Config format** | Markdown + YAML | YAML + Python | Pure Python | Pure Python |
| **Agent versioning** | semver per agent | No | No | No |
| **Shared behavior** | `_shared_dna.md` | None | Python inheritance | None |
| **Team composition file** | `team.yaml` | None | None | None |
| **Beginner-friendly** | High (edit Markdown) | Medium | Low | Very Low |
| **Non-dev editable** | Yes (it's Markdown) | Partial | No | No |
| **Tool permissions** | Declarative allowlist | Python only | Python only | Python only |

> **Honest note:** CrewAI has excellent DX with its role/goal/backstory model. AutoGen is more powerful for complex orchestration patterns. LangGraph offers maximum flexibility for custom state machines. CervellaSwarm's strength is **readability, versioning, and team composition** -- your agent definitions live in version-controlled Markdown that anyone on the team can read and edit.

## CLI Reference

```
cervella-agent init <type>     Create a single agent
  --name, -n NAME              Agent name (default: type name)
  --team, -t TEAM              Team name (default: my-team)
  --specialty, -s SPEC         Worker specialty (default: generic)
  --output, -o DIR             Output directory (default: current)

cervella-agent init-team <preset>  Create a complete team
  --name, -n NAME              Team name (default: my-team)
  --output, -o DIR             Output directory (default: current)

cervella-agent list            List available templates and specialties
cervella-agent validate <files>  Validate agent definition files
cervella-agent --version       Show version
```

## Examples

The `examples/` directory contains complete team setups:

```
examples/
  minimal-team/    # 3 agents: coordinator + backend + quality gate
  standard-team/   # 7 agents: + architect, frontend, tester, researcher
  full-team/       # 17 agents: all specialist roles
```

Each example includes a `team.yaml` and all agent `.md` files, ready to copy into your project.

## Python API

```python
from cervellaswarm_agent_templates import create_agent, create_team, validate_agent

# Create a single agent
path = create_agent("coordinator", name="my-lead", team_name="my-project")

# Create a full team
files = create_team("standard", output_dir=".claude/agents/", team_name="my-project")

# Validate an agent file
result = validate_agent(".claude/agents/my-lead.md")
print(result.valid)   # True
print(result.issues)  # []
```

## Requirements

- Python 3.10+
- pyyaml >= 6.0

## License

Apache-2.0. See [LICENSE](LICENSE).
