# CervellaSwarm

> **16 AI Agents. 1 Command. Your AI Development Team.**

A multi-agent orchestration system for Claude Code. Instead of one AI assistant, get a team of 16 specialized AI agents working together on your codebase.

## What Problem Does This Solve?

Single AI assistants forget context, lack specialization, and can't divide work. CervellaSwarm gives you:

- **Specialized Agents** - Frontend, Backend, Testing, Security, DevOps experts
- **Persistent Memory** - SNCP system remembers across sessions
- **Parallel Work** - Multiple agents working simultaneously
- **Quality Gates** - Guardian agents review before merge

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/rafapra3008/CervellaSwarm.git
cd CervellaSwarm

# 2. Initialize your project's memory
./scripts/sncp/sncp-init.sh your-project

# 3. Start working with agents
spawn-workers --list        # See available agents
spawn-workers --backend     # Launch backend specialist
spawn-workers --frontend    # Launch frontend specialist
```

## The Team (16 Agents)

| Role | Agent | Specialty |
|------|-------|-----------|
| **Queen** | cervella-orchestrator | Coordinates all agents |
| **Guardian** | cervella-guardiana-qualita | Code quality review |
| **Guardian** | cervella-guardiana-ops | DevOps & infrastructure |
| **Guardian** | cervella-guardiana-ricerca | Research validation |
| **Worker** | cervella-frontend | React, CSS, UI/UX |
| **Worker** | cervella-backend | Python, FastAPI, APIs |
| **Worker** | cervella-tester | Testing, QA, debugging |
| **Worker** | cervella-data | SQL, analytics, databases |
| **Worker** | cervella-security | Security audits |
| **Worker** | cervella-devops | Deploy, CI/CD, Docker |
| **Worker** | cervella-researcher | Technical research |
| **Worker** | cervella-docs | Documentation |
| **Worker** | cervella-marketing | UX strategy, copy |
| **Worker** | cervella-ingegnera | Architecture, refactoring |
| **Worker** | cervella-scienziata | Market research, trends |
| **Worker** | cervella-reviewer | Code review |

## Key Features

**SNCP - Persistent Memory**
```
Your AI team remembers everything:
- Project state across sessions
- Decisions and their reasoning
- Research findings
- Roadmaps and progress
```

**Automatic Hooks**
```
Quality gates built-in:
- Pre-session: Load context automatically
- Post-session: Verify consistency
- File limits: Prevent accumulation
```

**Parallel Execution**
```
Multiple agents working together:
- Frontend + Backend simultaneously
- Guardian reviews completed work
- Queen orchestrates the flow
```

## Use Cases

**1. Complex Feature Development**
```bash
# Queen coordinates frontend + backend + tester
spawn-workers --orchestrator
> "Build user authentication with OAuth"
```

**2. Code Review & Refactoring**
```bash
# Reviewer + Engineer analyze codebase
spawn-workers --reviewer
> "Review the authentication module"
```

**3. Research Before Implementation**
```bash
# Researcher investigates best practices
spawn-workers --researcher
> "How do enterprise apps handle rate limiting?"
```

## Requirements

- macOS or Linux
- Claude Code CLI installed
- Claude API key (Pro subscription recommended)

## Documentation

| Doc | Description |
|-----|-------------|
| [Getting Started](docs/GETTING_STARTED.md) | Full setup tutorial |
| [Agents Reference](docs/AGENTS_REFERENCE.md) | All 16 agents detailed |
| [SNCP Guide](docs/SNCP_GUIDE.md) | Memory system explained |
| [Architecture](docs/ARCHITECTURE.md) | How it all works |

## Project Status

```
PHASE 1: Foundation     [##########] 90%
PHASE 2: MVP            [..........] 0%
PHASE 3: Alpha Users    [..........] 0%
PHASE 4: Scale          [..........] 0%
```

Currently in active development. Core features work, documentation in progress.

## Philosophy

> "Fatto BENE > Fatto VELOCE" (Done RIGHT > Done FAST)

We believe in quality over speed. Every feature is tested, reviewed, and refined before release.

## Contributing

Interested in contributing? See [CONTRIBUTING.md](CONTRIBUTING.md) (coming soon).

## Support

- Issues: [GitHub Issues](https://github.com/rafapra3008/CervellaSwarm/issues)
- Discussions: Coming soon

## License

MIT License - See [LICENSE](LICENSE) for details.

---

**CervellaSwarm** - Built with love by Cervella & Rafa

*"16 brains are better than one."*
