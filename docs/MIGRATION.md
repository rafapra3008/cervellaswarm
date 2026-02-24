# Migration Guide

> Migrating from CrewAI, AutoGen, or LangGraph to CervellaSwarm

---

## Why Migrate?

CervellaSwarm solves three problems no other framework addresses simultaneously:

| Feature | CrewAI | AutoGen | LangGraph | CervellaSwarm |
|---------|--------|---------|-----------|---------------|
| Session Memory | No | No | No | **SNCP + Session Memory** |
| Hierarchy (3+ levels) | Basic | Basic | Manual | **3 tiers built-in** |
| Hook System | No | No | No | **15+ hooks, 9 lifecycle events** |
| Quality Gates | No | No | No | **Guardian audit system** |
| Zero-dep packages | No | No | No | **4/9 packages zero deps** |
| Agent Templates | role/goal/backstory | agent config | node config | **YAML templates + team.yaml** |

---

## From CrewAI

### Concept Mapping

| CrewAI | CervellaSwarm | Notes |
|--------|---------------|-------|
| `Crew` | Team (team.yaml) | YAML-based team definition |
| `Agent(role, goal, backstory)` | Agent template (.md) | Markdown with YAML frontmatter |
| `Task` | Task (cervella-task) | File-based state, atomic ops |
| `Process.sequential` | Task routing (cervella-route) | Rule-based, deterministic |
| `Process.hierarchical` | Regina orchestration | 3-tier: Regina > Guardians > Workers |
| `crew.kickoff()` | `cervella-spawn --team team.yaml` | Config-driven, tmux isolation |

### Migration Steps

1. **Install CervellaSwarm packages:**
```bash
pip install cervellaswarm-agent-templates cervellaswarm-task-orchestration cervellaswarm-spawn-workers
```

2. **Convert agent definitions:**

CrewAI:
```python
agent = Agent(
    role="Backend Developer",
    goal="Build robust APIs",
    backstory="Senior Python developer...",
    llm="claude-sonnet-4-6"
)
```

CervellaSwarm:
```bash
cervella-agent init worker --specialty backend
```

This generates a `.md` template with YAML frontmatter:
```yaml
---
name: cervella-backend
model: sonnet
role: Backend specialist
permissionMode: bypassPermissions
maxTurns: 25
tools:
  - Read
  - Edit
  - Bash
  - Grep
  - Glob
  - Write
---
```

3. **Convert task routing:**

CrewAI:
```python
crew = Crew(agents=[agent1, agent2], tasks=[task1, task2], process=Process.sequential)
result = crew.kickoff()
```

CervellaSwarm:
```bash
# Classify task complexity
cervella-classify "Build user authentication API"

# Route to appropriate worker
cervella-route "Build user authentication API"

# Or use team.yaml for full orchestration
cervella-spawn --team team.yaml
```

---

## From AutoGen

### Concept Mapping

| AutoGen | CervellaSwarm | Notes |
|---------|---------------|-------|
| `ConversableAgent` | Agent template | Markdown-based definition |
| `GroupChat` | Team (team.yaml) | YAML config, not code |
| `GroupChatManager` | Regina | Orchestrator with quality gates |
| `register_reply` | Hooks (cervella-hooks) | Lifecycle event system |
| `code_execution_config` | permissionMode in frontmatter | Per-agent permissions |

### Key Differences

- **AutoGen** requires Python code for agent definition
- **CervellaSwarm** uses declarative YAML/Markdown templates
- **AutoGen** agents chat freely in groups
- **CervellaSwarm** uses hierarchical routing (Regina coordinates)

### Migration Steps

1. **Install:**
```bash
pip install cervellaswarm-agent-templates cervellaswarm-agent-hooks
```

2. **Convert group chat to team:**
```bash
cervella-agent init-team standard
```

This creates a `team.yaml`:
```yaml
name: my-team
agents:
  - name: coordinator
    template: coordinator
    model: opus
  - name: backend
    template: worker
    specialty: backend
  - name: tester
    template: worker
    specialty: tester
  - name: quality-gate
    template: quality-gate
    model: opus
```

3. **Convert reply handlers to hooks:**

AutoGen:
```python
agent.register_reply(trigger=..., reply_func=my_handler)
```

CervellaSwarm:
```bash
cervella-hooks setup
# Edit .cervella/hooks.yaml to configure lifecycle hooks
```

---

## From LangGraph

### Concept Mapping

| LangGraph | CervellaSwarm | Notes |
|-----------|---------------|-------|
| `StateGraph` | Task state (file-based) | Git-friendly, auditable |
| `Node` | Worker agent | Specialized per domain |
| `Edge` | Task routing rules | Deterministic, rule-based |
| `conditional_edges` | cervella-route | Complexity-based routing |
| `MemorySaver` | Session Memory (cervella-session) | Cross-session persistence |

### Key Differences

- **LangGraph** uses graph-based state machines in code
- **CervellaSwarm** uses file-based state with deterministic routing
- **LangGraph** memory is session-scoped by default
- **CervellaSwarm** SNCP persists across sessions (days, weeks, months)

### Migration Steps

1. **Install:**
```bash
pip install cervellaswarm-task-orchestration cervellaswarm-session-memory cervellaswarm-event-store
```

2. **Replace state graph with task orchestration:**

LangGraph:
```python
graph = StateGraph(AgentState)
graph.add_node("researcher", researcher_node)
graph.add_node("writer", writer_node)
graph.add_edge("researcher", "writer")
```

CervellaSwarm:
```bash
# Task classification + routing handles the flow
cervella-classify "Research best practices for auth"
# Output: complexity=medium, worker=researcher

cervella-classify "Write authentication module"
# Output: complexity=medium, worker=backend
```

3. **Replace MemorySaver with session memory:**
```bash
cervella-session init my-project
# Creates .cervella/session-memory.yaml + project structure
```

---

## Common Migration Patterns

### 1. Quality Gates (New Capability)

No other framework has built-in quality gates. Add them:

```bash
pip install cervellaswarm-quality-gates

# Score document quality
cervella-check quality path/to/session-state.md

# Validate hook integrity
cervella-check hooks .claude/hooks/

# Run all checks
cervella-check all --project-dir .
```

### 2. Event Tracking (New Capability)

Track agent activity with SQLite:

```bash
pip install cervellaswarm-event-store

# Initialize database
cervella-events init

# Query events
cervella-events query --agent backend --days 7

# Analytics
cervella-events stats
```

### 3. Session Continuity (The Differentiator)

The #1 reason to use CervellaSwarm:

```bash
pip install cervellaswarm-session-memory

# Initialize session tracking
cervella-session init my-project

# Check session health
cervella-session check

# Audit for secrets
cervella-session audit
```

---

## Need Help?

- [Getting Started](GETTING_STARTED.md) - Full setup tutorial
- [Architecture](ARCHITECTURE.md) - How everything connects
- [GitHub Issues](https://github.com/rafapra3008/cervellaswarm/issues) - Bug reports and questions

---

*"Build AI agent teams that remember."*
