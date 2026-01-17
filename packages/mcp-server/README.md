# CervellaSwarm MCP Server

> 16 AI agents as MCP tools for Claude Code integration.

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

## Available Agents (16)

### Workers (12)

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

### Guardiane (3) - Quality Gates

| Guardiana | Role |
|-----------|------|
| guardiana-qualita | Verifies code quality (9.5+ standard) |
| guardiana-ricerca | Verifies research accuracy |
| guardiana-ops | Verifies deploy safety & security |

### Regina (1)

| Agent | Role |
|-------|------|
| orchestrator | The Queen - Coordinates all agents |

## Example Usage in Claude Code

```
Use spawn_worker to create a REST API endpoint for user authentication
```

Claude Code will call the `spawn_worker` tool with `worker: "backend"` automatically.

## Development (for contributors)

```bash
# Clone and install
git clone https://github.com/rafapra/cervellaswarm
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

## Links

- CLI: [cervellaswarm on npm](https://www.npmjs.com/package/cervellaswarm)
- GitHub: [rafapra/cervellaswarm](https://github.com/rafapra/cervellaswarm)

---

*"16 agents. MCP integration. Your AI team in Claude Code."*
