# CervellaSwarm VS Code Extension

> Multi-Agent AI Orchestration System for VS Code

## Features

### Sidebar Control Panel
- **Task Input**: Submit tasks directly from VS Code
- **Worker Status**: Monitor active workers in real-time
- **Quick Spawn**: Launch specific workers with one click

### Terminal Integration
- Seamless integration with CervellaSwarm CLI
- Tasks run in dedicated terminal
- Full output visibility

## Requirements

- VS Code 1.107.0+
- CervellaSwarm CLI installed (`npm install -g cervellaswarm`)
- Claude API access (Pro subscription recommended)

## Getting Started

1. Open the CervellaSwarm sidebar (bee icon in activity bar)
2. Enter a task description
3. Click "Run Task" or press Enter
4. Watch the task execute in the terminal

## Quick Spawn Workers

Use the quick spawn buttons to launch specific workers:
- **Backend**: Python, FastAPI specialist
- **Frontend**: React, CSS specialist
- **Tester**: Testing, QA specialist
- **Researcher**: Technical research specialist

## Architecture

```
VS Code Extension (Thin Layer)
    |
    +-- Sidebar Webview (UI)
    |   +-- Task input, status, worker buttons
    |
    +-- Terminal Integration
        +-- Spawns CLI commands
            |
            v
    CervellaSwarm CLI (Thick Layer)
        +-- Worker management, SNCP, execution
```

## Version History

- **v0.1.0** (2026-01-22): Initial POC with sidebar and terminal integration
- **v0.0.1**: Scaffold with basic commands

## Development

```bash
# Install dependencies
npm install

# Compile
npm run compile

# Watch mode
npm run watch

# Package VSIX
npm run package
```

## License

Apache 2.0 - See LICENSE

---

*CervellaSwarm - 17 brains are better than one*
