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

> **Note:** Package currently being prepared for public release. Coming soon!

### 2. Set your API key

```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

Get your key at [console.anthropic.com](https://console.anthropic.com/)

### 3. Initialize your project

```bash
cd your-project
cervellaswarm init
```

### 4. Run your first task

```bash
cervellaswarm task "Create a REST API endpoint for user registration"
```

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
- Anthropic API key (Claude Pro recommended)

## Configuration

```bash
# Required
export ANTHROPIC_API_KEY=sk-ant-...
```

## License

MIT

---

*"16 agenti. 1 comando. Il tuo team AI."*

*Built with love by Cervella & Rafa*
