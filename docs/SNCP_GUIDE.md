# SNCP Guide

> **Sistema Nervoso Centrale del Progetto - Persistent Memory for Your AI Team**

This guide explains SNCP, CervellaSwarm's persistent memory system that keeps your AI agents aligned across sessions.

---

## What is SNCP?

**SNCP** (Sistema Nervoso Centrale del Progetto) is a file-based memory system that stores:

- Project state across sessions
- Decisions and their reasoning
- Ideas captured during development
- Roadmaps and progress tracking
- Research findings
- Session handoffs

Think of it as the "brain" that persists between sessions. When you restart work, your agents read SNCP files to remember context instantly.

---

## Why Persistent Memory?

**The Problem:**
AI assistants are powerful but have a critical limitation: **they forget**. Every new session starts from scratch unless you manually explain context.

**The Traditional Workaround:**
Developers copy-paste from previous chats, maintain context in external tools (Notion, Linear), or rewrite the same context repeatedly. This is tedious and error-prone.

**The SNCP Solution:**
Your AI team writes its own memory to disk. Next session, they read it back. No manual context transfer needed.

**Benefits:**
- **Zero Context Loss** - Agents remember decisions, progress, blockers
- **Instant Session Start** - No "let me catch you up" needed
- **Audit Trail** - Every decision documented with reasoning
- **Multi-Project Support** - Each project has isolated memory

---

## Folder Structure

```
.sncp/
├── progetti/                   # Per-project memory
│   ├── my-project/
│   │   ├── PROMPT_RIPRESA.md   # Session resume file (auto-loaded)
│   │   ├── stato.md            # Current state
│   │   ├── idee/               # Ideas captured during work
│   │   ├── decisioni/          # Decisions with reasoning
│   │   └── roadmaps/           # Project plans
│   └── another-project/
│       └── ...
├── stato/
│   └── oggi.md                 # Global daily state
├── handoff/                    # Session handoffs
└── memoria/
    └── decisioni/              # Global decisions
```

### Key Files

| File | Purpose | When Used |
|------|---------|-----------|
| `PROMPT_RIPRESA.md` | Session resume context | Auto-loaded at session start |
| `stato.md` | Current project state | Read before working on project |
| `idee/*.md` | Captured ideas | Written during sessions |
| `decisioni/*.md` | Decision log | When important choice is made |
| `roadmaps/*.md` | Project plans | Planning and tracking |

---

## How It Works

### Session Flow

```
1. SESSION START
   Agent reads: .sncp/progetti/my-project/PROMPT_RIPRESA.md
   → Instantly knows: current state, last decisions, next steps

2. DURING WORK
   Agent writes to: idee/, decisioni/, stato.md
   → Captures insights, decisions, progress

3. SESSION END
   Agent updates: PROMPT_RIPRESA.md
   → Summarizes session for next time
```

### Example: Multi-Session Feature Development

**Session 1:**
```
Agent: "I'll research authentication best practices."
Writes: .sncp/progetti/myapp/idee/IDEA_auth_approach.md
Updates: PROMPT_RIPRESA.md with research findings
```

**Session 2 (next day):**
```
Agent reads PROMPT_RIPRESA.md
Agent: "I see we researched JWT vs sessions yesterday. Implementing JWT..."
Writes: .sncp/progetti/myapp/decisioni/DECISION_use_jwt.md
```

**Session 3:**
```
Agent reads PROMPT_RIPRESA.md
Agent: "JWT implemented. Running tests..."
Updates: stato.md with completion status
```

**Zero manual context transfer needed.**

---

## Usage

### Initialize for a New Project

```bash
# From CervellaSwarm directory
./scripts/sncp/sncp-init.sh my-project

# Creates:
# .sncp/progetti/my-project/
#   ├── PROMPT_RIPRESA.md
#   ├── stato.md
#   ├── idee/
#   ├── decisioni/
#   └── roadmaps/
```

### Let Agents Use SNCP Automatically

Agents automatically read `PROMPT_RIPRESA.md` at session start (via hooks). You don't need to do anything.

During work, agents write to SNCP when:
- They have an idea worth capturing
- They make a significant decision
- They complete a milestone
- Session ends

### Manual SNCP Operations

```bash
# Check current state
cat .sncp/progetti/my-project/stato.md

# See recent ideas
ls -lt .sncp/progetti/my-project/idee/

# Review decisions
ls -lt .sncp/progetti/my-project/decisioni/

# Read session resume context
cat .sncp/progetti/my-project/PROMPT_RIPRESA.md
```

---

## Best Practices

### 1. Keep PROMPT_RIPRESA.md Concise
**Problem:** Files > 150 lines slow down session start.
**Solution:** Archive old sessions regularly.

```bash
# Archive sessions older than 2 weeks
mv .sncp/progetti/my-project/PROMPT_RIPRESA.md \
   .sncp/progetti/my-project/archivio/PROMPT_RIPRESA_2026_01.md

# Start fresh PROMPT_RIPRESA.md with current state only
```

### 2. Let Agents Write, You Read
SNCP is designed for agents to write and humans to review. Don't manually edit SNCP files unless correcting errors.

### 3. One Project Per Directory
Each codebase gets its own `.sncp/progetti/name/` folder. Don't mix projects.

```
Good:
.sncp/progetti/backend-api/
.sncp/progetti/frontend-app/

Bad:
.sncp/progetti/my-monorepo/  (mixing multiple projects)
```

### 4. Capture Ideas Immediately
If an agent suggests something interesting mid-session, ask them to save it:
```
You: "Save that routing idea to SNCP for later"
Agent: Writes to .sncp/progetti/myapp/idee/IDEA_routing_optimization.md
```

### 5. Review Decisions Weekly
Once a week, review `.sncp/progetti/*/decisioni/` to ensure you agree with agent decisions.

---

## Common Questions

**Q: Is SNCP just fancy markdown files?**
Yes. Intentionally simple. No databases, no complex tools. Files are portable, greppable, and version-controllable.

**Q: Does SNCP work with git?**
Yes. Commit SNCP files to track project memory over time. `.gitignore` already excludes temporary files.

**Q: Can I use SNCP without CervellaSwarm?**
Technically yes, but you lose automatic hooks and agent integration. It's designed for the swarm.

**Q: What if PROMPT_RIPRESA.md gets too long?**
Archive it. Move old content to `archivio/` and keep only recent context (< 150 lines recommended).

**Q: Can multiple projects share SNCP?**
Each project gets isolated memory in `.sncp/progetti/project-name/`. Projects don't interfere.

---

## Troubleshooting

### "Agent doesn't remember previous session"
Check if `PROMPT_RIPRESA.md` was updated at end of last session:
```bash
ls -l .sncp/progetti/my-project/PROMPT_RIPRESA.md
# Should show recent timestamp
```

### "SNCP folder doesn't exist"
Initialize it:
```bash
./scripts/sncp/sncp-init.sh my-project
```

### "Too many old files cluttering SNCP"
Archive old content:
```bash
# Move files older than 30 days
find .sncp/progetti/my-project/idee/ -mtime +30 -exec mv {} .sncp/archivio/ \;
```

---

## Philosophy

SNCP embodies CervellaSwarm's core principle:

> **"Context persistence is not optional—it's the foundation of effective AI collaboration."**

Traditional AI assistants are brilliant but forgetful. SNCP makes them remember. That's the difference between a chatbot and a team.

---

## Next Steps

- Read [Architecture](ARCHITECTURE.md) to understand how SNCP integrates with agents
- See [Agents Reference](AGENTS_REFERENCE.md) for which agents use SNCP most
- Check `.sncp/progetti/cervellaswarm/` to see SNCP in action on CervellaSwarm itself

---

*SNCP - Because your AI team deserves a memory.*
