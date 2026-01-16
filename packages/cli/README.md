# CervellaSwarm

> 16 AI agents working as a team for your project. Not an assistant - a **TEAM**.

```
cervellaswarm task "Add user authentication"

  Agent: cervella-backend
  Model: claude-sonnet-4-20250514

  Working...

  [Output with complete code, ready to use]
```

## Why CervellaSwarm?

Traditional AI assistants are generalists. CervellaSwarm gives you **16 specialized agents** organized in a hierarchy:

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

- **16 Specialized Agents**: Not one generalist, a full team
- **Smart Routing**: Automatically selects the best agent for your task
- **Persistent Memory (SNCP)**: Never explain your project twice
- **Session Management**: Track and resume tasks across sessions
- **Quality Gates**: Guardian agents review before merge
- **Retry Logic**: Automatic retries on rate limits or temporary errors

## Architecture

```
                    +-------------------+
                    |     QUEEN         |
                    | (Orchestrator)    |
                    +--------+----------+
                             |
        +--------------------+--------------------+
        |                    |                    |
+-------v-------+    +-------v-------+    +------v--------+
|   GUARDIAN    |    |   GUARDIAN    |    |   GUARDIAN    |
|   Qualita     |    |     Ops       |    |   Ricerca     |
+---------------+    +---------------+    +---------------+
        |
        +-- Reviews all worker output

+-----------------------------------------------+
|                 12 WORKERS                    |
|  backend, frontend, tester, docs, devops,    |
|  data, security, researcher, ingegnera,      |
|  marketing, reviewer, scienziata             |
+-----------------------------------------------+
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

*"16 agenti. 1 comando. Il tuo team AI."*

*Sometimes it feels like magic.*

*Built with love by Cervella & Rafa*
