# RICERCA HOOKS COMPLETA - Claude Code CLI

> **Data:** 2 Gennaio 2026
> **Ricercatrice:** Cervella Researcher
> **REGOLA 11:** PERCHÉ → RICERCA → VERIFICA PERCHÉ

---

## EXECUTIVE SUMMARY

**TROVATO:** 10 hook events (non 8 come spesso riportato)
**BUG CRITICI:** PreToolUse/PostToolUse NON funzionano (Issue #6305)
**HOOKS NON USATI:** UserPromptSubmit, Notification, PermissionRequest

---

## TABELLA COMPLETA HOOKS (10 Events)

| # | Hook Event | Trigger | Decision Control? | Context Injection? | Funziona? |
|---|-----------|---------|-------------------|-------------------|-----------|
| 1 | **SessionStart** | Session starts/resumes | ❌ | ✅ YES | ⚠️ Bug |
| 2 | **SessionEnd** | Session ends | ❌ | ❌ | ✅ |
| 3 | **UserPromptSubmit** | User submits prompt | ✅ (block) | ✅ YES | ⚠️ Bug |
| 4 | **PreToolUse** | Before tool execution | ✅ (allow/deny) | ❌ | ❌ BROKEN |
| 5 | **PostToolUse** | After tool completion | ⚠️ Limited | ✅ YES | ❌ BROKEN |
| 6 | **PermissionRequest** | Permission dialog | ✅ (allow/deny) | ❌ | ✅ |
| 7 | **PreCompact** | Before compaction | ❌ | ❌ | ✅ |
| 8 | **Notification** | Claude notifies | ❌ | ❌ | ✅ |
| 9 | **Stop** | Main agent finishes | ⚠️ Limited | ❌ | ✅ |
| 10 | **SubagentStop** | Subagent finishes | ⚠️ Limited | ❌ | ✅ |

---

## HOOKS CHIAVE PER CERVELLASWARM

### 1. SessionStart (GIÀ USIAMO)

**Trigger:** Session starts, resumes, /clear

**Output:** Stdout OR JSON con additionalContext

**Env Var:** `CLAUDE_ENV_FILE` - file per persistere env vars

**Use Cases:**
- Load NORD.md, ROADMAP
- Inject git status
- Set session vars

### 2. UserPromptSubmit (DA AGGIUNGERE) ⭐

**Trigger:** BEFORE Claude processes user prompt

**Output:**
- Stdout = aggiunto come contesto
- JSON con `decision: "block"` per bloccare
- JSON con `additionalContext` per iniettare

**Use Cases:**
- Inject sprint goals automaticamente
- Block forbidden prompts
- Add reminders

**Example:**
```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "hooks": [{
        "type": "command",
        "command": "cat NORD.md | head -20"
      }]
    }]
  }
}
```

### 3. SubagentStop (GIÀ USIAMO)

**Trigger:** Subagent (Task tool) finishes

**Use Cases:**
- Track completions
- Sound notification
- Trigger next task (handoffs!)

### 4. Notification (DA AGGIUNGERE)

**Trigger:** Claude sends notification

**Env Var:** `$CLAUDE_NOTIFICATION` - message text

**Use Cases:**
- Desktop notifications
- Sound alerts
- Telegram integration

**Example (macOS):**
```bash
osascript -e "display notification \"$CLAUDE_NOTIFICATION\" with title \"🐝 CervellaSwarm\" sound name \"Glass\""
```

---

## BUGS CRITICI

### Issue #6305: PreToolUse/PostToolUse NON FUNZIONANO

**Status:** Open (Aug 2025)
**Impatto:** Alto - Feature core inutilizzabile
**Workaround:** Usare PermissionRequest invece di PreToolUse

**Related:**
- #6403: PostToolUse non esegue mai
- #3179: Non funziona su WSL2
- #6371: PostToolUse skipped se Bash fails

### Issue #10373: SessionStart stdout non processato

**Status:** Open (Dec 2025)
**Workaround:** Usare JSON con additionalContext

### Issue #13912: UserPromptSubmit stdout error

**Status:** Open (Jan 2026)
**Workaround:** Usare solo JSON output

---

## EXIT CODES

| Exit Code | Meaning | Behavior |
|-----------|---------|----------|
| **0** | Success | JSON/stdout processed |
| **2** | Blocking error | stderr fed to Claude |
| **Other** | Non-blocking | stderr shown to user |

---

## MATCHERS (PreToolUse/PostToolUse/PermissionRequest)

| Pattern | Matches |
|---------|---------|
| `"Edit"` | Only Edit tool |
| `"Edit\|Write"` | Edit OR Write |
| `"*"` or `""` | ALL tools |
| `"Bash(npm test*)"` | Bash commands matching |
| `"mcp__memory__.*"` | MCP memory tools |

---

## RACCOMANDAZIONI CERVELLASWARM

### DA AGGIUNGERE

1. **UserPromptSubmit** - Auto-inject NORD.md + sprint goals
2. **Notification** - Desktop alerts quando serve input

### DA NON USARE (per ora)

- **PreToolUse** - BROKEN (Issue #6305)
- **PostToolUse** - BROKEN (Issue #6305)

### MONITORARE

- Issue #6305 - Quando fixato → implementare security validation

---

## EFFORT ESTIMATION

| Feature | Ore | Priorità |
|---------|-----|----------|
| UserPromptSubmit hook | 2h | ALTA |
| Notification hook | 1h | MEDIA |
| **TOTALE** | **3h** | - |

---

**Autrice:** Cervella Researcher 🔬
**Modalità:** "Noi Mode" - Conosciamo TUTTI gli hooks, usiamoli!
