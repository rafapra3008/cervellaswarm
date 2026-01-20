# CervellaSwarm

> **The only AI coding team that checks its own work.**
>
> 17 specialized AI agents. Regina coordinates, Architect plans, Workers execute, Guardians verify.

```
cervellaswarm task "Add user authentication"

  Agent: cervella-backend
  Model: claude-sonnet-4-20250514

  Working...

  [Output with complete code, ready to use]
```

## Why CervellaSwarm?

Traditional AI assistants are generalists. CervellaSwarm gives you **17 specialized agents** organized in a hierarchy:

### The Queen (Orchestrator)

| Agent | Role |
|-------|------|
| `cervella-orchestrator` | Coordinates all agents, delegates tasks |

### The Guardians (Quality Gates)

| Agent | Specialty |
|-------|-----------|
| `cervella-guardiana-qualita` | Code quality, standards, reviews |
| `cervella-guardiana-ops` | DevOps, infrastructure, deploy |
| `cervella-guardiana-ricerca` | Research validation, fact-checking |

### The Architect (Strategic Planner)

| Agent | Specialty |
|-------|-----------|
| `cervella-architect` | Plans complex tasks, creates PLAN.md before implementation |

### The Workers (Specialists)

| Agent | Specialty |
|-------|-----------|
| `cervella-backend` | Python, FastAPI, API, Database |
| `cervella-frontend` | React, CSS, Tailwind, UI/UX |
| `cervella-tester` | Testing, Debug, QA |
| `cervella-docs` | Documentation, README, Guides |
| `cervella-devops` | Deploy, CI/CD, Docker |
| `cervella-data` | SQL, Analytics, Database Design |
| `cervella-security` | Security Audit, Vulnerabilities |
| `cervella-researcher` | Research, Analysis, Best Practices |
| `cervella-ingegnera` | Architecture, Refactoring, Tech Debt |
| `cervella-marketing` | UX Strategy, Copywriting, Positioning |
| `cervella-reviewer` | Code Review, Best Practices |
| `cervella-scienziata` | Market Research, Competitor Analysis |

## Quick Start

### 1. Install

```bash
npm install -g cervellaswarm
```

> **Requires:** Node.js 18+

### 2. Initialize your project

```bash
cd your-project
cervellaswarm init
```

The wizard will:
- **Ask for your API key** (get one at [console.anthropic.com](https://console.anthropic.com/))
- Set up your project constitution (10 quick questions)
- Create the `.sncp/` memory directory

Your API key is saved securely - you only need to enter it once.

### 3. Run your first task

```bash
cervellaswarm task "Create a REST API endpoint for user registration"
```

### 4. Check your setup

```bash
cervellaswarm doctor
```

Shows if everything is configured correctly.

## Talk to Your AI Team

CervellaSwarm understands natural language. Here are the essential phrases:

| Say This | To Do This |
|----------|------------|
| `cervellaswarm task "..."` | Execute a task with your AI team |
| `checkpoint` | Save your progress (during a session) |
| `prossimo passo` | Move to the next step |
| `spawn-workers --backend` | Activate a specific agent |
| `chiudiamo` | End session cleanly |

**Pro tip:** CervellaSwarm is not an assistant - it's a **team**. Delegate decisions:

```
"volete decidere" → Let the team choose the best approach
"consigli"        → Get suggestions before implementing
```

*"Not an assistant - a TEAM."*

## What Makes Us Different

CervellaSwarm is not just another AI coding tool. Here's what makes us unique:

### 1. Self-Checking System

3 Guardian agents powered by Opus verify EVERY output before delivery. Target quality score: 9.5/10.

**No other AI coding tool does this.** Most tools give you raw LLM output. We give you reviewed, production-ready code.

### 2. Semantic Code Search

Tree-sitter AST parsing, not grep. Find symbol definitions, function callers, and references in 2 seconds.

```bash
semantic-search.sh find-symbol "MyClass"
semantic-search.sh find-callers "my_function"
```

### 3. Architect-First Workflow

Complex task? Architect creates a detailed plan BEFORE writing code. Opus plans, Sonnet implements.

```bash
spawn-workers --architect "Refactor AuthService"
```

### 4. Git Attribution

Every agent signs their commits with `Co-Authored-By`. Full transparency on who did what.

### 5. SNCP Memory System

Persistent memory across sessions. Never explain your project twice. The swarm remembers context, decisions, and architecture.

### 6. Smart Task Routing

Automatic routing to the best worker based on task analysis. Frontend work goes to cervella-frontend, database queries to cervella-data.

**The result?** Code that works the first time. Documentation that stays updated. Architecture that makes sense.

## Commands

### `cervellaswarm init`

Initialize CervellaSwarm in your project. Creates a `.sncp/` directory for persistent memory.

### `cervellaswarm task <description>`

Execute a task with an AI agent.

```bash
# Auto-route to best agent
cervellaswarm task "Add login page"

# Specify agent manually
cervellaswarm task "Write unit tests" --agent cervella-tester
```

### `cervellaswarm status`

Show current project status and recent sessions.

### `cervellaswarm resume`

Resume the last task session with context recap.

### `cervellaswarm doctor`

Diagnose your setup and fix issues.

```bash
cervellaswarm doctor            # Quick health check
cervellaswarm doctor --validate # Test API key with actual call
cervellaswarm doctor --config   # Show all configuration values
```

## Key Features

- **17 Specialized Agents**: 1 Queen + 3 Guardians + 1 Architect + 12 Workers
- **Quality-First**: 3 Opus Guardians verify every output (9.5/10 target)
- **Architect Planning**: Complex tasks get a PLAN.md before implementation
- **Smart Routing**: Automatically selects the best agent for your task
- **Persistent Memory (SNCP)**: Never explain your project twice
- **Session Management**: Track and resume tasks across sessions
- **Semantic Search**: Tree-sitter AST parsing for intelligent code navigation
- **Git Attribution**: Every agent signs their commits
- **Retry Logic**: Automatic retries on rate limits or temporary errors

## Architecture

```
                    +-------------------+
                    |     QUEEN         |
                    | (Orchestrator)    |
                    | Opus              |
                    +--------+----------+
                             |
        +--------------------+--------------------+
        |                    |                    |
+-------v-------+    +-------v-------+    +------v--------+
|   GUARDIAN    |    |   GUARDIAN    |    |   GUARDIAN    |
|   Qualita     |    |     Ops       |    |   Ricerca     |
|   Opus        |    |   Opus        |    |   Opus        |
+---------------+    +---------------+    +---------------+
        |
        +-- Reviews all worker output

                    +-------------------+
                    |    ARCHITECT      |
                    | (Planner)         |
                    | Opus              |
                    +--------+----------+
                             |
                             +-- Creates PLAN.md for complex tasks

+-----------------------------------------------+
|                 12 WORKERS                    |
|  backend, frontend, tester, docs, devops,    |
|  data, security, researcher, ingegnera,      |
|  marketing, reviewer, scienziata             |
|  All Sonnet                                  |
+-----------------------------------------------+

TOTAL: 5 Opus + 12 Sonnet = 17 agents
```

## Requirements

- Node.js 18+
- Anthropic API key ([get one here](https://console.anthropic.com/))

## Configuration

### API Key Setup

CervellaSwarm supports two ways to configure your API key:

**Option 1: Through the wizard (recommended)**
```bash
cervellaswarm init
# The wizard will ask for your key and save it securely
```

**Option 2: Environment variable**
```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

The environment variable takes priority if both are set.

### Config Location

Your configuration is stored at:
- **macOS**: `~/Library/Preferences/cervellaswarm-nodejs/config.json`
- **Linux**: `~/.config/cervellaswarm-nodejs/config.json`
- **Windows**: `%APPDATA%\cervellaswarm-nodejs\Config\config.json`

### View/Reset Configuration

```bash
cervellaswarm doctor --config    # View current config
```

## Our Promise

We'll always tell the truth.

CervellaSwarm has limitations. Context limits. Session management. Manual checkpoints.

But also: **moments of pure magic**. When the swarm works together like an orchestra.

We're not perfect. We're honest. We're improving every day.

*"Sometimes it feels like magic."*

---

## License

Apache-2.0

---

*"17 agenti. 1 comando. Il tuo team AI."*

*Sometimes it feels like magic.*

*Built with love by Cervella & Rafa*
