# CervellaSwarm MCP Server

> **The only AI coding team that checks its own work.**
>
> 17 AI agents with quality guardians for Claude Code.

## Quick Start

### 1. Install

```bash
npm install -g @cervellaswarm/mcp-server
```

### 2. Configure Claude Code

Add to your `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "cervellaswarm": {
      "command": "cervellaswarm-mcp"
    }
  }
}
```

Or add to your project's `.mcp.json`:

```json
{
  "mcpServers": {
    "cervellaswarm": {
      "command": "cervellaswarm-mcp"
    }
  }
}
```

### 3. Set API Key

Install the CLI and run init:

```bash
npm install -g cervellaswarm
cervellaswarm init
```

Or set environment variable directly:

```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

### 4. Restart Claude Code

Restart Claude Code to load the MCP server. You'll have access to these tools:

- **spawn_worker**: Execute tasks with specialized AI workers
- **list_workers**: See available workers and their specialties
- **check_status**: Verify configuration and API key
- **check_usage**: Check your usage quota

## Available Agents (17)

**Models:** Regina/Guardiane/Architect use Opus 4.5, Workers use Sonnet 4.5

### The Architect (1) - Strategic Planner [OPUS]

| Agent | Specialty |
|-------|-----------|
| architect | Plans complex tasks, creates PLAN.md before implementation |

### Guardiane (3) - Quality Gates [OPUS]

| Guardiana | Role |
|-----------|------|
| guardiana-qualita | Verifies code quality (9.5+ standard) |
| guardiana-ricerca | Verifies research accuracy |
| guardiana-ops | Verifies deploy safety & security |

### Regina (1) [OPUS]

| Agent | Role |
|-------|------|
| orchestrator | The Queen - Coordinates all agents |

### Workers (12) [SONNET]

| Worker | Specialty |
|--------|-----------|
| backend | Python, FastAPI, API, Database |
| frontend | React, CSS, Tailwind, UI/UX |
| tester | Testing, Debug, QA |
| docs | Documentation, README, Guides |
| devops | Deploy, CI/CD, Docker |
| data | SQL, Analytics, Database Design |
| security | Security Audit, Vulnerabilities |
| researcher | Research, Analysis, Best Practices |
| marketing | UX Strategy, Positioning, Copywriting |
| ingegnera | Architecture, Refactoring, Tech Debt |
| scienziata | Market Research, Competitor Analysis |
| reviewer | Code Review, Best Practices |

## Example Usage in Claude Code

```
Use spawn_worker to create a REST API endpoint for user authentication
```

Claude Code will call the `spawn_worker` tool with `worker: "backend"` automatically.

## Development (for contributors)

```bash
# Clone and install
git clone https://github.com/rafapra3008/CervellaSwarm
cd cervellaswarm/packages/mcp-server
npm install

# Watch mode
npm run dev

# Test with MCP Inspector
npm run inspect

# Build
npm run build
```

### Local Development Config

For local development, use path-based config in `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "cervellaswarm": {
      "command": "node",
      "args": ["/path/to/CervellaSwarm/packages/mcp-server/dist/index.js"]
    }
  }
}
```

## Architecture

```
MCP Server
    │
    ├── Tools
    │   ├── spawn_worker    → Anthropic API (your key)
    │   ├── list_workers    → Static list
    │   ├── check_status    → Config check
    │   └── check_usage     → Quota info
    │
    └── Shares config with CLI
        └── Uses same API key from cervellaswarm init
```

## Philosophy

> "Sometimes it feels like magic."

We're honest: AI tools aren't perfect. Context gets lost, mistakes happen. Our solution? **Built-in quality guardians** - three dedicated agents whose job is to review and verify the work of others.

Not promising perfection. Promising honesty and continuous improvement.

## Links

- CLI: [cervellaswarm on npm](https://www.npmjs.com/package/cervellaswarm)
- GitHub: [rafapra3008/CervellaSwarm](https://github.com/rafapra3008/CervellaSwarm)

---

*"17 agents with quality guardians. Your AI team in Claude Code."*
