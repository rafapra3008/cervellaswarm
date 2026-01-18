# Architecture

> **Multi-agent orchestration system for AI-powered development with built-in quality gates**

This document explains how CervellaSwarm works under the hood: the agent hierarchy, task routing, quality assurance layer, and integrations.

---

## High-Level Overview

CervellaSwarm is a **three-tier architecture** with 16 specialized AI agents:

```
                      ┌─────────────────┐
                      │  REGINA (Queen) │
                      │  Orchestrator   │
                      └────────┬────────┘
                               │
            ┌──────────────────┼──────────────────┐
            │                                     │
    ┌───────▼────────┐                  ┌────────▼────────┐
    │  GUARDIANE (3) │                  │   WORKERS (12)  │
    │  Quality Gates │                  │  Specialists    │
    └────────────────┘                  └─────────────────┘
         │                                       │
    [Opus Model]                          [Sonnet Model]
    - Quality Check                       - Code Execution
    - Research Validation                 - Testing
    - Ops Security                        - Documentation
```

**Key Design Principles:**

1. **Specialization** - Each agent masters one domain
2. **Quality First** - Guardians review before merge
3. **Persistent Memory** - SNCP system retains context
4. **Parallel Execution** - Multiple agents work simultaneously

---

## Components

### 1. Regina (Orchestrator)

**Role:** The coordinator. Routes tasks, manages workflows, ensures quality.

**Capabilities:**
- Breaks complex tasks into subtasks
- Assigns work to appropriate specialists
- Coordinates parallel execution
- Triggers Guardian reviews

**Model:** Claude Opus (highest reasoning capability)

**Example Flow:**
```
User: "Build user authentication"
  │
  ├─► Regina analyzes requirements
  ├─► Delegates to Backend (API logic)
  ├─► Delegates to Frontend (login UI)
  ├─► Delegates to Tester (tests)
  └─► Guardiana-Qualita validates
```

---

### 2. Guardiane (Quality Gates)

**Role:** The reviewers. Three specialized auditors that verify work quality.

| Guardian | Focus | Validates |
|----------|-------|-----------|
| **guardiana-qualita** | Code quality | Frontend, Backend, Tester output |
| **guardiana-ricerca** | Research accuracy | Researcher, Docs output |
| **guardiana-ops** | Security & deployment | DevOps, Security, Data output |

**Model:** Claude Opus (critical thinking needed)

**When Activated:**
- After Worker completes task
- Before merging to main branch
- On manual quality audit requests

**Quality Standard:** 9.5/10 minimum for production code

**Example Validation:**
```
Backend Worker → Implements API endpoint
     ↓
Guardiana-Qualita reviews:
  - Is authentication secure?
  - Are errors handled properly?
  - Is code tested?
  - Does it follow best practices?
     ↓
[PASS: 9.5] or [FAIL: 7.2 - Issues found]
```

---

### 3. Workers (Specialists)

**Role:** The executors. 12 domain experts that implement tasks.

**Worker Categories:**

**Core Development:**
- `backend` - Python, FastAPI, APIs, business logic
- `frontend` - React, CSS, UI/UX, responsive design
- `tester` - Unit/integration tests, debugging

**Infrastructure & Data:**
- `devops` - Docker, CI/CD, deployment
- `data` - SQL, analytics, database design
- `security` - Security audits, vulnerability scanning

**Knowledge Work:**
- `researcher` - Technical research, best practices
- `docs` - Documentation, READMEs, guides
- `reviewer` - Code review, PR feedback

**Strategic:**
- `marketing` - UX strategy, positioning, copywriting
- `ingegnera` - Architecture, refactoring, tech debt
- `scienziata` - Market research, competitor analysis

**Model:** Claude Sonnet (cost-effective for execution)

---

## Task Flow

### Standard Task Execution

```
┌──────────────┐
│ User Request │
└──────┬───────┘
       │
       ▼
┌─────────────────────────────────────────┐
│ 1. ROUTING (Regina)                     │
│    - Analyze task complexity            │
│    - Identify required specialists      │
│    - Check dependencies                 │
└──────┬──────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────┐
│ 2. EXECUTION (Workers)                  │
│    - Workers receive specific subtasks  │
│    - Execute in parallel if independent │
│    - Write results to .swarm/tasks/     │
└──────┬──────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────┐
│ 3. VALIDATION (Guardians)               │
│    - Guardian reviews worker output     │
│    - Checks quality standards (9.5+)    │
│    - Provides feedback or approval      │
└──────┬──────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────┐
│ 4. INTEGRATION (Regina)                 │
│    - Merges approved changes            │
│    - Updates SNCP memory                │
│    - Reports to user                    │
└─────────────────────────────────────────┘
```

### Task Complexity Routing

| Complexity | Handler | Guardian Review |
|-----------|---------|-----------------|
| **Simple** (< 5 min) | Single Worker | Optional |
| **Medium** (5-30 min) | 2-3 Workers | Required |
| **Complex** (> 30 min) | Orchestrator + Team | Required + User Approval |

---

## Quality Assurance Layer

### Three-Level Risk System

**Level 1: LOW RISK**
- Documentation updates
- CSS tweaks
- Non-critical copy changes
- **Action:** Worker proceeds, Guardian optional

**Level 2: MEDIUM RISK**
- New features
- Database migrations
- API changes
- **Action:** Worker implements → Guardian validates

**Level 3: HIGH RISK**
- Authentication/security
- Deployment configuration
- Data deletion operations
- **Action:** Worker implements → Guardian validates → User approves

### Guardian Review Process

```python
# Pseudo-code for Guardian validation

def validate_worker_output(worker_task):
    checks = {
        'correctness': score_correctness(),
        'security': score_security(),
        'testability': score_tests(),
        'maintainability': score_code_quality(),
        'documentation': score_docs()
    }

    total_score = average(checks.values())

    if total_score >= 9.5:
        return APPROVE(details=checks)
    else:
        return REJECT(issues=identify_issues(checks))
```

---

## MCP Integration

**MCP (Model Context Protocol)** enables CervellaSwarm to integrate with Claude Code as a tool provider.

### Architecture

```
┌──────────────────┐
│  Claude Code     │
│  (User Session)  │
└────────┬─────────┘
         │
         │ MCP Protocol
         ▼
┌──────────────────────────┐
│  MCP Server              │
│  @cervellaswarm/mcp      │
│                          │
│  Tools:                  │
│  - spawn_worker()        │
│  - list_workers()        │
│  - check_status()        │
└────────┬─────────────────┘
         │
         │ Anthropic API
         ▼
┌──────────────────────────┐
│  Specialized Agents      │
│  (Claude Opus/Sonnet)    │
└──────────────────────────┘
```

### Available MCP Tools

**spawn_worker(worker: string, task: string)**
- Spawns a specialized agent
- Executes task with that agent's expertise
- Returns result to Claude Code

**list_workers()**
- Lists all 16 available agents
- Shows specialties and capabilities

**check_status()**
- Validates configuration
- Checks API key setup

**check_usage()**
- Reports API usage quota
- Estimates remaining credits

### Configuration

**Global Setup** (`~/.claude/settings.json`):
```json
{
  "mcpServers": {
    "cervellaswarm": {
      "command": "cervellaswarm-mcp"
    }
  }
}
```

**Project Setup** (`.mcp.json`):
```json
{
  "mcpServers": {
    "cervellaswarm": {
      "command": "cervellaswarm-mcp"
    }
  }
}
```

---

## SNCP Integration

**SNCP (Sistema Nervoso Centrale Persistente)** is the persistent memory system.

### Purpose

AI agents are stateless - they forget everything between sessions. SNCP solves this by maintaining:

- **Project state** - Current status, next steps
- **Decisions** - What was decided and why
- **Research** - Findings from investigations
- **Roadmaps** - Long-term plans
- **Prompts** - Session continuity instructions

### Structure

```
.sncp/
├── progetti/
│   ├── project-a/
│   │   ├── PROMPT_RIPRESA.md      # Resume instructions
│   │   ├── stato.md               # Current state
│   │   ├── decisioni/             # Decision log
│   │   ├── idee/                  # Ideas and research
│   │   └── roadmaps/              # Plans
│   └── project-b/
│       └── [same structure]
├── stato/
│   └── oggi.md                    # Daily state
└── handoff/
    └── HANDOFF_*.md               # Session handoffs
```

### Context Mesh Pattern

Each project has its own **PROMPT_RIPRESA** (resume prompt):

```
Session Start:
  1. Hook loads PROMPT_RIPRESA_project.md
  2. Agent reads: "Where we are, what's next"
  3. Agent continues work seamlessly

Session End:
  1. Agent updates PROMPT_RIPRESA_project.md
  2. Documents: decisions, state, blockers
  3. Next session picks up exactly where left off
```

**File Size Limits** (enforced by hooks):
- `PROMPT_RIPRESA_*.md`: 150 lines max
- `oggi.md`: 60 lines max
- `stato.md`: 500 lines max

When limits exceeded → Archive old sessions to `archivio/`

### Automatic Hooks

**session_start_swarm.py**
- Loads COSTITUZIONE (agent identity)
- Loads NORD.md (project direction)
- Loads PROMPT_RIPRESA (current state)
- Checks if code review day (Mon/Fri)

**file_limits_guard.py**
- Monitors SNCP file sizes
- Warns when approaching limits
- Prevents context overload

**subagent_start_costituzione.py**
- Injects COSTITUZIONE into spawned agents
- Ensures consistent behavior across swarm

---

## Communication Protocols

### Worker → Worker

Workers do **not** communicate directly. All coordination goes through Regina.

```
❌ BAD:  Backend → Frontend (direct)
✅ GOOD: Backend → Regina → Frontend
```

### Worker → Guardian

Workers write output to `.swarm/tasks/`, Guardian reads and validates:

```
1. Worker completes: .swarm/tasks/TASK_001_OUTPUT.md
2. Worker marks done: touch .swarm/tasks/TASK_001.done
3. Regina triggers: Guardian review
4. Guardian reads output, validates, scores
5. Guardian writes: .swarm/tasks/TASK_001_REVIEW.md
```

### Status Updates

Workers update status using helper scripts:

```bash
# Worker starts
scripts/swarm/update-status.sh WORKING "Implementing API"

# Worker finishes
scripts/swarm/update-status.sh DONE "API implemented"

# Worker blocked
scripts/swarm/ask-regina.sh BLOCKER "Need database schema"
```

---

## Deployment Architecture

### Local Development

```
Developer
    │
    ├─► spawn-workers CLI
    │       ↓
    │   Spawns local Claude Code sessions
    │   (one per agent)
    │
    └─► MCP Server (optional)
            ↓
        Integrates with Claude Code
        (tools within single session)
```

### Production Setup

```
User Project
    │
    ├─► cervellaswarm init
    │       ↓
    │   Initializes SNCP structure
    │   Configures MCP server
    │
    ├─► Claude Code + MCP
    │       ↓
    │   Uses spawn_worker tool
    │   Calls Anthropic API
    │
    └─► Specialized Agents
            ↓
        Execute on Anthropic infrastructure
        Return results via MCP
```

---

## Scalability Considerations

### Current Limits

- **Agents:** 16 (1 Regina + 3 Guardians + 12 Workers)
- **Parallel Workers:** Up to 5 simultaneously
- **Context Size:** ~150 lines per PROMPT_RIPRESA
- **API Model:** Anthropic Claude (Opus/Sonnet)

### Cost Management

**Model Selection:**
- Regina & Guardians: Opus (expensive, critical reasoning)
- Workers: Sonnet (cost-effective, good execution)

**Task Batching:**
- Small edits: Single worker, no guardian
- Medium features: Worker + guardian
- Complex projects: Full orchestration

**Context Optimization:**
- SNCP limits prevent context bloat
- Hooks enforce file size constraints
- Archive old sessions automatically

---

## Security Model

### API Key Management

- Keys stored in `~/.config/cervellaswarm/config.json`
- Never committed to git
- Shared between CLI and MCP server

### Agent Permissions

- Workers can read/write project files
- Workers cannot modify `.claude/` configuration
- Workers cannot spawn other workers (only Regina can)

### Code Review Gates

- Level 3 (HIGH RISK) requires human approval
- Guardians flag security issues
- `cervella-security` audits before deploy

---

## Future Architecture

**Planned Enhancements:**

1. **Remote Execution** - Deploy agents to cloud infrastructure
2. **Custom Agents** - User-defined specialists
3. **Agent Learning** - Improve from past mistakes
4. **Multi-Project Coordination** - Share learnings across projects
5. **Advanced Telemetry** - Track agent performance metrics

---

## References

- [Agents Reference](AGENTS_REFERENCE.md) - Detailed agent capabilities
- [SNCP Guide](SNCP_GUIDE.md) - Memory system deep dive
- [Getting Started](GETTING_STARTED.md) - Setup tutorial

---

*Architecture designed for quality, maintainability, and honest limitations.*
