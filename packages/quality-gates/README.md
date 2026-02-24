# cervellaswarm-quality-gates

> Quality gates for AI agent swarms: content scoring, hook validation, and agent sync.

Part of the [CervellaSwarm](https://github.com/rafapra3008/cervellaswarm) ecosystem.

## Features

- **Content Quality Scoring** - Score session documents across 4 dimensions: actionability (30%), specificity (30%), freshness (20%), conciseness (20%)
- **Hook Validation** - Verify hook file integrity: executable, correct shebang, proper permissions (OK/BROKEN/DISABLED/NOT_EXEC)
- **Agent Sync** - Compare and synchronize agent definition directories across projects
- **CLI** - `cervella-check` with subcommands: `quality`, `hooks`, `sync`, `all`
- **Zero dependencies** - Pure Python stdlib, no external packages required

## Installation

```bash
pip install cervellaswarm-quality-gates
```

## Quick Start

```python
from cervellaswarm_quality_gates import score_content, validate_hooks, compare_agents

# Score a session document
result = score_content("## Session 42\n### What happened\n- Fixed auth bug in login flow\n### Next steps\n1. Deploy to staging")
print(f"Quality: {result.total:.1f}/10")

# Validate hooks in a directory
reports = validate_hooks("/path/to/hooks/")
for r in reports:
    print(f"{r.name}: {r.status.value}")

# Compare agent directories
diff = compare_agents("/project-a/agents/", "/project-b/agents/")
print(f"Only in A: {diff.only_in_source}")
```

## CLI Usage

```bash
# Score content quality of a file
cervella-check quality path/to/session-state.md

# Validate all hooks in a directory
cervella-check hooks path/to/hooks/

# Compare agent directories
cervella-check sync /agents/source/ /agents/target/

# Run all checks with JSON output
cervella-check all --project-dir . --json
```

## Configuration

Config file search order:
1. `CERVELLASWARM_QUALITY_GATES_CONFIG` env var
2. `.cervella/quality-gates.yaml` in project root
3. `~/.claude/quality-gates.yaml` (user-level)

```yaml
# .cervella/quality-gates.yaml
quality:
  weights:
    actionability: 0.30
    specificity: 0.30
    freshness: 0.20
    conciseness: 0.20
  min_score: 7.0

hooks:
  directory: .claude/hooks/
  required_hooks:
    - session_start
    - file_limits

sync:
  ignore_patterns:
    - "*.pyc"
    - "__pycache__"
```

## Scoring Dimensions

| Dimension | Weight | What it measures |
|-----------|--------|-----------------|
| Actionability | 30% | Contains concrete next steps, decisions, action items |
| Specificity | 30% | Uses specific names, numbers, file paths (not vague) |
| Freshness | 20% | Has dates, session numbers, timestamps |
| Conciseness | 20% | Information density (not bloated with filler) |

## Hook Statuses

| Status | Meaning |
|--------|---------|
| `OK` | Hook exists, is executable, has valid shebang |
| `BROKEN` | Hook exists but has errors (bad shebang, syntax) |
| `DISABLED` | Hook file exists but is not enabled |
| `NOT_EXEC` | Hook exists but lacks execute permission |
| `MISSING` | Hook file not found |

## Comparison with Alternatives

| Feature | quality-gates | flake8/ruff | custom scripts |
|---------|:---:|:---:|:---:|
| Content quality scoring | Yes | No | Manual |
| Hook validation | Yes | No | Manual |
| Agent directory sync | Yes | No | Manual |
| AI-agent aware | Yes | No | Varies |
| Zero dependencies | Yes | No | Varies |
| YAML config | Yes | Yes | Manual |

## License

Apache-2.0 - see [LICENSE](LICENSE) for details.
