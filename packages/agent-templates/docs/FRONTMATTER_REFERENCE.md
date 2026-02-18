# Frontmatter Reference

Complete reference for all YAML frontmatter fields in CervellaSwarm agent definitions.

---

## Required Fields

### `name`
- **Type:** string
- **Required:** Yes
- **Example:** `name: my-backend`
- **Description:** Unique identifier for the agent. Used in task assignment, messaging, and file naming. Lowercase with hyphens.

### `description`
- **Type:** string or multiline
- **Required:** Yes
- **Example:**
  ```yaml
  description: >
    Specialist in Python, APIs, and databases.
    Use for backend implementation tasks.
  ```
- **Description:** What this agent does. Shown in agent listings and used by the coordinator to decide task routing.

### `model`
- **Type:** enum
- **Required:** Yes
- **Values:** `opus` | `sonnet` | `haiku`
- **Example:** `model: sonnet`
- **Description:** The AI model to use. Use `opus` for agents that make decisions (coordinator, architect, quality gate). Use `sonnet` for implementation workers. Use `haiku` only for batch automation tasks.

### `tools`
- **Type:** comma-separated string
- **Required:** Yes
- **Example:** `tools: Read, Edit, Bash, Glob, Grep, Write`
- **Description:** Allowlist of tools this agent can use. Available tools:

| Tool | Purpose |
|------|---------|
| `Read` | Read file contents |
| `Edit` | Modify existing files |
| `Write` | Create new files |
| `Bash` | Run shell commands |
| `Glob` | Find files by pattern |
| `Grep` | Search text in files |
| `WebSearch` | Search the web |
| `WebFetch` | Fetch URL content |
| `Task` | Delegate to other agents |
| `AskUserQuestion` | Ask the user a question |
| `NotebookEdit` | Edit Jupyter notebooks |
| `EnterPlanMode` | Enter planning mode |
| `ExitPlanMode` | Exit planning mode |

---

## Identity Fields

### `version`
- **Type:** semver string
- **Required:** No (recommended)
- **Example:** `version: 1.0.0`
- **Description:** Semantic version of the agent definition. Increment when you change the agent's behavior or capabilities. Unique to CervellaSwarm -- no other framework versions agent definitions.

### `updated`
- **Type:** date (ISO 8601)
- **Required:** No (recommended)
- **Example:** `updated: 2026-02-18`
- **Description:** Last modification date. Useful for auditing and tracking when agent definitions were last reviewed.

### `role`
- **Type:** string
- **Required:** No
- **Example:** `role: Coordinator`
- **Description:** Human-readable role label. Standard roles: `Coordinator`, `Quality Gate`, `Architect`, `Worker`, `Researcher`, `Reviewer`. Custom roles are allowed.
- **Inspired by:** CrewAI's agent identity model.

### `compatible_with`
- **Type:** semver range
- **Required:** No
- **Example:** `compatible_with: cervellaswarm >= 2.0.0`
- **Description:** Framework version compatibility. Documents which version of CervellaSwarm this agent definition was designed for.

---

## Capability Fields

### `disallowedTools`
- **Type:** comma-separated string
- **Required:** No
- **Example:** `disallowedTools: Write, Edit`
- **Description:** Explicit denylist of tools. Use this for read-only agents like the Architect that should never modify files. Takes precedence over `tools`.

### `permissionMode`
- **Type:** enum
- **Required:** No (default: `default`)
- **Values:** `default` | `plan` | `bypassPermissions` | `acceptEdits`
- **Example:** `permissionMode: plan`
- **Description:** Controls how the agent requests permission for actions:
  - `default` -- normal permission prompts
  - `plan` -- requires plan approval before implementation
  - `bypassPermissions` -- skips permission prompts (use with caution)
  - `acceptEdits` -- auto-approves file edits but prompts for other actions

### `maxTurns`
- **Type:** positive integer
- **Required:** No
- **Example:** `maxTurns: 30`
- **Description:** Maximum API round-trips before the agent stops. Use to prevent runaway agents. Recommended: 25-30 for workers, 50 for coordinators.

---

## Knowledge Fields

### `shared_dna`
- **Type:** filename
- **Required:** No (recommended)
- **Example:** `shared_dna: _shared_dna.md`
- **Description:** Path to the shared behavior file. This file is loaded and its content is available to the agent. Use it for team-wide rules, output formats, and conventions. Unique to CervellaSwarm.

### `skills`
- **Type:** list of strings
- **Required:** No
- **Example:**
  ```yaml
  skills:
    - code-review
    - testing-patterns
  ```
- **Description:** Named skill files to preload. Skills provide domain-specific knowledge and instructions.

---

## Memory Fields

### `memory`
- **Type:** enum
- **Required:** No
- **Values:** `user` | `project` | `local`
- **Example:** `memory: user`
- **Description:** Persistent memory scope:
  - `user` -- memory persists across all projects (good for quality gates)
  - `project` -- memory is specific to the current repository
  - `local` -- memory is not synced (gitignored)

---

## Lifecycle Fields

### `hooks`
- **Type:** object
- **Required:** No
- **Example:**
  ```yaml
  hooks:
    PreToolUse:
      - matcher: "Bash"
        hooks:
          - type: command
            command: "./scripts/validate.sh"
  ```
- **Description:** Agent-scoped hooks that run at specific lifecycle events. See [cervellaswarm-agent-hooks](https://github.com/rafapra3008/cervellaswarm/tree/main/packages/agent-hooks) for ready-to-use hooks.

### `mcpServers`
- **Type:** object
- **Required:** No
- **Description:** MCP (Model Context Protocol) server configuration for this agent. Allows agents to access external tools and data sources.

---

## Agent Body (Markdown)

Everything after the closing `---` of the frontmatter is the agent's **system prompt**. This is where you define:

1. **Who the agent is** -- its identity and role description
2. **How it works** -- step-by-step process
3. **What it can and cannot do** -- explicit capability constraints
4. **Output format** -- structured response template

### Recommended Structure

```markdown
# Agent Name

> **Shared DNA:** See `_shared_dna.md` for team-wide rules.

You are a **[Role]** specialist.

## Role
[What this agent is responsible for]

## Process
[Step-by-step workflow]

## Scope
[What it CAN and CANNOT modify]

## Output Format
[Structured output template]

*Agent Name - Role, Team Name*
```

### Tips

- **Be explicit about constraints.** "I do NOT write code" is clearer than "I focus on planning."
- **Include examples.** Show the exact output format you expect.
- **Keep it focused.** Each agent should have a single clear responsibility.
- **Use the shared DNA** for rules that apply to all agents.

---

## Validation

Use the CLI to validate your agent files:

```bash
cervella-agent validate .claude/agents/*.md
```

The validator checks:
- YAML frontmatter is parseable
- Required fields are present
- Model is valid (`opus`, `sonnet`, `haiku`)
- Tools are recognized
- Optional fields have valid values
- Body is not suspiciously short

---

*CervellaSwarm Agent Templates v0.1.0*
