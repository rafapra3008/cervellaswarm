# CervellaSwarm MCP Server

> 16 AI agents as MCP tools for Claude Code integration.

## Quick Start

### 1. Install

```bash
cd packages/mcp-server
npm install
npm run build
```

### 2. Configure Claude Code

Add to your `~/.claude/settings.json`:

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

Or add to your project's `.mcp.json`:

```json
{
  "mcpServers": {
    "cervellaswarm": {
      "command": "node",
      "args": ["./packages/mcp-server/dist/index.js"]
    }
  }
}
```

### 3. Set API Key

Either run `cervellaswarm init` or set environment variable:

```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

### 4. Use in Claude Code

Once configured, you'll have access to these tools in Claude Code:

- **spawn_worker**: Execute tasks with specialized AI workers
- **list_workers**: See available workers
- **check_status**: Verify configuration

## Available Workers

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

## Example Usage in Claude Code

```
Use spawn_worker to create a REST API endpoint for user authentication
```

Claude Code will call the `spawn_worker` tool with `worker: "backend"` automatically.

## Development

```bash
# Watch mode
npm run dev

# Test with MCP Inspector
npm run inspect

# Build
npm run build
```

## Architecture

```
MCP Server (this package)
    │
    ├── Tools
    │   ├── spawn_worker    → Anthropic API
    │   ├── list_workers    → Static list
    │   └── check_status    → Config check
    │
    └── Shares config with CLI
        └── ~/.config/cervellaswarm/config.json
```

---

*"16 agents. MCP integration. Your AI team in Claude Code."*
