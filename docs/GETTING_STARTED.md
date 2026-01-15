# Getting Started with CervellaSwarm

> **Time to first value: ~10 minutes**

This guide will get you from zero to working with your AI team.

---

## Prerequisites

Before starting, make sure you have:

- [ ] macOS or Linux (Windows WSL works too)
- [ ] [Claude Code CLI](https://claude.ai/code) installed
- [ ] Claude Pro subscription (for API access)
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
│   ├── agents/          # 16 agent definitions
│   ├── hooks/           # Automatic triggers
│   └── settings.json    # Configuration
├── .sncp/               # Memory system
│   ├── progetti/        # Per-project memory
│   └── stato/           # Current state
├── scripts/
│   └── sncp/            # Setup scripts
├── docs/                # Documentation
└── spawn-workers        # Main CLI tool
```

---

## Step 3: Initialize Memory for Your Project

CervellaSwarm can manage multiple projects. Initialize memory for each:

```bash
# Initialize for a new project
./scripts/sncp/sncp-init.sh my-project

# This creates:
# .sncp/progetti/my-project/
#   ├── stato.md           # Project state
#   ├── PROMPT_RIPRESA.md  # Session continuity
#   ├── idee/              # Ideas and research
#   ├── decisioni/         # Decisions log
#   └── roadmaps/          # Project plans
```

**Expected output:**
```
Inizializzazione SNCP per: my-project
Creazione struttura...
OK - Progetto inizializzato!
```

---

## Step 4: Launch Your First Agent

```bash
# See all available agents
spawn-workers --list
```

**Expected output:**
```
Available agents:
  --backend      Python, FastAPI, APIs
  --frontend     React, CSS, UI/UX
  --tester       Testing, QA
  --researcher   Technical research
  --reviewer     Code review
  ...
```

**Launch a specific agent:**
```bash
# Launch the backend specialist
spawn-workers --backend

# Or launch the researcher
spawn-workers --researcher
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
spawn-workers --orchestrator
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
| `spawn-workers --list` | Show all agents |
| `spawn-workers --backend` | Launch backend agent |
| `spawn-workers --frontend` | Launch frontend agent |
| `spawn-workers --tester` | Launch testing agent |
| `spawn-workers --researcher` | Launch research agent |
| `spawn-workers --orchestrator` | Launch Queen to coordinate |

---

## Troubleshooting

### "spawn-workers: command not found"

Make sure you're in the CervellaSwarm directory:
```bash
cd ~/Developer/CervellaSwarm
./spawn-workers --list  # Use ./ prefix
```

Or add to your PATH:
```bash
export PATH="$PATH:~/Developer/CervellaSwarm"
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

- **Issues:** [GitHub Issues](https://github.com/rafapra3008/CervellaSwarm/issues)
- **Documentation:** Check the `docs/` folder

---

*"Un po' ogni giorno fino al 100000%!"*
*(A little every day until 100000%!)*
