# cervellaswarm-agent-hooks

**Ready-to-use hooks for Claude Code.** Block dangerous commands, inject context into subagents, track file limits, and auto-checkpoint your sessions.

```
pip install cervellaswarm-agent-hooks
cervella-hooks setup            # generates config + settings.json snippet
```

Built by the [CervellaSwarm](https://github.com/rafapra3008/cervellaswarm) team. Battle-tested across 370+ development sessions with 17 AI agents.

---

## Why Hooks?

Claude Code [hooks](https://docs.anthropic.com/en/docs/claude-code/hooks) let you run custom scripts at key lifecycle events (before tool calls, session end, subagent spawn, etc.). But writing them from scratch means dealing with JSON stdin/stdout protocols, edge cases, and configuration.

This package gives you **5 production-ready hooks** you can install in under 5 minutes:

```
Before tool call          After session ends         When subagent spawns
     |                          |                          |
     v                          v                          v
+----------------+    +------------------+    +--------------------+
| bash-validator |    | file-limits      |    | context-inject     |
| Blocks rm -rf /|    | Warns >300 lines |    | Injects facts +    |
| Fixes --force  |    +------------------+    | project state      |
+----------------+    | session-         |    +--------------------+
                      | checkpoint       |
                      | Saves git state  |
                      +------------------+

When session stops
     |
     v
+----------------+
| git-reminder   |
| "3 uncommitted"|
+----------------+
```

## Available Hooks

| Hook | Event | What it does | Dependencies |
|------|-------|-------------|-------------|
| `cervella-bash-validator` | PreToolUse | Blocks destructive commands (`rm -rf /`, `DROP TABLE`, fork bombs), asks for risky ones (`git reset --hard`), auto-fixes `--force` to `--force-with-lease` | stdlib only |
| `cervella-git-reminder` | Stop | Desktop notification about uncommitted files. Max once every 30 min. Works on macOS (osascript) and Linux (notify-send) | stdlib only |
| `cervella-file-limits` | SessionEnd | Warns when files exceed configured line count or file count limits. Prevents session state bloat | pyyaml |
| `cervella-context-inject` | SubagentStart | Injects project facts and session state into all subagents. They start with full project context | pyyaml |
| `cervella-session-checkpoint` | SessionEnd | Auto-saves git status, recent commits, and branch info to a state file at session end | pyyaml |

**All hooks work independently.** Install one, install all -- your choice.

## Quick Start (< 5 minutes)

### 1. Install

```bash
pip install cervellaswarm-agent-hooks
```

### 2. Setup

```bash
cervella-hooks setup
```

This creates `.cervella/hooks.yaml` in your project and prints the `settings.json` snippet you need.

### 3. Add to Claude Code

Copy the relevant hooks into `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{"type": "command", "command": "cervella-bash-validator", "timeout": 5}]
    }],
    "Stop": [{
      "matcher": "",
      "hooks": [{"type": "command", "command": "cervella-git-reminder", "timeout": 10}]
    }],
    "SessionEnd": [{
      "matcher": "",
      "hooks": [
        {"type": "command", "command": "cervella-file-limits", "timeout": 10},
        {"type": "command", "command": "cervella-session-checkpoint", "timeout": 15}
      ]
    }],
    "SubagentStart": [{
      "matcher": "",
      "hooks": [{"type": "command", "command": "cervella-context-inject", "timeout": 5}]
    }]
  }
}
```

### 4. Done

Start a Claude Code session. Your hooks are active.

## Configuration

Hooks read configuration from (in priority order):
1. `CERVELLA_HOOKS_CONFIG` environment variable
2. `.cervella/hooks.yaml` in your project root
3. `~/.claude/hooks.yaml` (user-level default)

If no config exists, hooks use sensible defaults. See [`examples/hooks.yaml`](examples/hooks.yaml) for all options.

Example `.cervella/hooks.yaml`:

```yaml
file_limits:
  checks:
    - pattern: "SESSION_STATE.md"
      max_lines: 300
      action: "Archive old content"

context_inject:
  facts_file: "docs/FACTS.md"
  state_file: "SESSION_STATE.md"

session_checkpoint:
  state_file: "SESSION_STATE.md"
  include_git_status: true

git_reminder:
  interval_minutes: 30
```

## Bash Validator in Detail

The most immediately useful hook. Protects you from accidental destruction:

| Category | Examples | Action |
|----------|----------|--------|
| **BLOCK** | `rm -rf /`, `DROP TABLE`, `mkfs.ext4`, fork bomb | Denied. Period. |
| **ASK** | `git reset --hard`, `chmod 777`, `kill -9`, `docker system prune` | User must confirm |
| **AUTO-FIX** | `git push --force` (non-main) | Silently replaced with `--force-with-lease` |
| **SAFE** | `rm -rf node_modules`, `rm -rf dist` | Allowed without warning |
| **ALLOW** | Everything else | Silent pass-through |

Add custom patterns via `hooks.yaml`:

```yaml
bash_validator:
  extra_blocked:
    - pattern: "kubectl delete namespace production"
      reason: "Never delete production namespace"
  extra_safe_rm:
    - ".angular/?"
```

## Create Your Own Hooks

Claude Code hooks are Python scripts that read JSON from stdin and optionally output JSON to stdout.

```python
#!/usr/bin/env python3
"""My custom hook - blocks commands containing 'production'."""
import json, sys

def main():
    hook_input = json.load(sys.stdin)
    command = hook_input.get("tool_input", {}).get("command", "")

    if "production" in command.lower():
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "ask",
                "permissionDecisionReason": "This command targets production. Are you sure?"
            }
        }))
    # No output = allow silently

if __name__ == "__main__":
    main()
```

### Hook Event Reference

| Event | Fires when | Input fields | Can block? |
|-------|-----------|-------------|-----------|
| `PreToolUse` | Before any tool call | `tool_input` (command, params) | Yes: deny / ask / allow |
| `PostToolUse` | After tool completes | `tool_input` + `tool_output` | No |
| `SessionStart` | Session begins | `cwd`, session info | No |
| `SessionEnd` | Session ends | `cwd`, session info | No |
| `SubagentStart` | Subagent spawns | `cwd`, agent info | Can inject `additionalContext` |
| `PreCompact` | Before context compaction | `cwd` | No |
| `Stop` | Session stopping | `cwd` | No |
| `UserPromptSubmit` | User sends prompt | `cwd`, message | Can modify prompt |

### Decision Protocol

For `PreToolUse` hooks, output one of:

```json
{"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny", "permissionDecisionReason": "Why"}}
{"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "ask", "permissionDecisionReason": "Why"}}
{"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "allow"}}
```

No output = allow (silent pass-through). This is the most common case.

For `SubagentStart` hooks, inject context:

```json
{"hookSpecificOutput": {"hookEventName": "SubagentStart", "additionalContext": "# Context\nYour markdown here"}}
```

## Requirements

- Python >= 3.10
- pyyaml >= 6.0 (only for configurable hooks; bash-validator and git-reminder use stdlib only)

## Tests

```bash
git clone https://github.com/rafapra3008/cervellaswarm.git
cd cervellaswarm/packages/agent-hooks
pip install -e ".[test]"
pytest
```

227 tests, 98% coverage, runs in 0.12s.

## License

[Apache-2.0](LICENSE)

## Part of CervellaSwarm

This package is part of [CervellaSwarm](https://github.com/rafapra3008/cervellaswarm), an open-source multi-agent framework for Claude Code with real session continuity.

Other packages:
- [`cervellaswarm-code-intelligence`](https://pypi.org/project/cervellaswarm-code-intelligence/) - AST-based code analysis (symbol extraction, dependency graphs, semantic search)
