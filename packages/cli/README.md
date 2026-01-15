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

Traditional AI assistants are generalists. CervellaSwarm gives you **8 specialized agents**, each expert in their domain:

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

## Quick Start

### 1. Install

```bash
npm install -g cervellaswarm
```

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

Initialize CervellaSwarm in your project. Creates a `.sncp/` directory for session management.

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

Resume the last task session.

## Features

- **Smart Routing**: Automatically selects the best agent for your task
- **Session Management**: Track and resume tasks across sessions
- **Retry Logic**: Automatic retries on rate limits or temporary errors
- **Project Context**: Agents understand your project structure

## Requirements

- Node.js 18+
- Anthropic API key

## Configuration

Set these environment variables:

```bash
# Required
ANTHROPIC_API_KEY=sk-ant-...
```

## License

MIT - [Rafa & Cervella](https://github.com/cervellaswarm)

---

*"16 agenti. 1 comando. Il tuo team AI."*
