# Getting Started with CervellaSwarm

> **Time to first value: ~10 minutes**

This guide will get you from zero to working with your AI team.

---

## Prerequisites

Before starting, make sure you have:

- [ ] macOS or Linux (Windows WSL works too)
- [ ] Python 3.10+ installed
- [ ] [Claude Code CLI](https://claude.ai/code) installed
- [ ] Anthropic API key (for MCP server) or Claude Pro subscription
- [ ] Git installed
- [ ] Terminal/shell access

**Check your setup:**
```bash
# Should return version number
claude --version

# Should show your home directory
echo $HOME
```

---

## Step 1: Clone the Repository

```bash
cd ~/Developer  # or your preferred directory
git clone https://github.com/rafapra3008/CervellaSwarm.git
cd CervellaSwarm
```

**Expected output:**
```
Cloning into 'CervellaSwarm'...
...
done.
```

---

## Step 2: Understand the Structure

```
CervellaSwarm/
├── .claude/
│   ├── agents/          # 17 agent definitions
│   ├── hooks/           # Automatic triggers
│   └── settings.json    # Configuration
├── .sncp/               # Memory system (SNCP 4.0)
│   └── progetti/        # Per-project memory
├── packages/            # 9 Python packages (pip installable)
├── docs/                # Documentation
└── NORD.md              # Project compass
```

---

## Step 3: Initialize Memory for Your Project

CervellaSwarm can manage multiple projects. Initialize memory for each:

```bash
# Install session memory package
pip install cervellaswarm-session-memory

# Initialize for a new project
cervella-session init my-project

# This creates:
# .cervella/
#   ├── session-memory.yaml    # Configuration
#   └── projects/
#       └── my-project/
#           ├── PROMPT_RIPRESA_my-project.md   # Session state
#           └── NORD.md                         # Project compass
```

---

## Step 4: Launch Your First Agent

```bash
# Install spawn workers package
pip install cervellaswarm-spawn-workers

# See all available agents
cervella-spawn --list
```

**Launch a specific agent:**
```bash
# Launch the backend specialist
cervella-spawn --worker backend

# Or launch a whole team from config
cervella-spawn --team team.yaml
```

---

## Step 5: Your First Task

Once an agent is running, give it a task:

```
You: "Analyze the codebase structure and identify potential improvements"

Agent: [Analyzes your code, reads files, provides recommendations]
```

**Tips for effective tasks:**
- Be specific about what you want
- Provide context if needed
- Let the agent ask clarifying questions

---

## Step 6: Using Multiple Agents

For complex work, use the Queen (orchestrator):

```bash
cervella-spawn --team team.yaml
```

The Queen will:
1. Break down your task
2. Assign work to specialized agents
3. Coordinate their output
4. Have Guardians review quality

**Example:**
```
You: "Build a REST API for user management with tests"

Queen:
- Assigns Backend agent for API code
- Assigns Tester agent for tests
- Assigns Reviewer for code review
- Coordinates the work
```

---

## Common Commands

| Command | Description |
|---------|-------------|
| `cervella-spawn --list` | Show all available agents |
| `cervella-spawn --worker backend` | Launch backend agent |
| `cervella-spawn --worker frontend` | Launch frontend agent |
| `cervella-spawn --worker tester` | Launch testing agent |
| `cervella-spawn --team team.yaml` | Launch full team from config |
| `cervella-check all --project-dir .` | Run quality gates |
| `cervella-session check` | Check session health |
| `cervella-events stats` | View agent analytics |

---

## Troubleshooting

### "cervella-spawn: command not found"

Install the spawn-workers package:
```bash
pip install cervellaswarm-spawn-workers

# Verify installation
cervella-spawn --list
```

### "Claude not authenticated"

Run Claude Code and complete authentication:
```bash
claude
# Follow prompts to authenticate
```

### "Agent not responding"

Check your Claude API quota. Pro subscription is recommended for heavy usage.

---

## Next Steps

- [ ] Read [Agents Reference](AGENTS_REFERENCE.md) - Learn what each agent does
- [ ] Read [SNCP Guide](SNCP_GUIDE.md) - Understand the memory system
- [ ] Try a real task on your project
- [ ] Join the community (coming soon)

---

## Need Help?

- **Issues:** [GitHub Issues](https://github.com/rafapra3008/cervellaswarm/issues)
- **Documentation:** Check the `docs/` folder

---

*"Un po' ogni giorno fino al 100000%!"*
*(A little every day until 100000%!)*
