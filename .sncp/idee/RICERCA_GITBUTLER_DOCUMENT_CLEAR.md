# RICERCA: GitButler + Document & Clear Pattern

**Data:** 10 Gennaio 2026
**Researcher:** Cervella Researcher
**Obiettivo:** Valutare integrazione GitButler e pattern Document & Clear per spawn-workers

---

## 1. GITBUTLER CON CLAUDE CODE

### Come Funziona
GitButler usa **hooks lifecycle** di Claude Code per intercettare azioni e creare virtual branches automatiche.

**Setup Config** (`~/.claude/settings.json` o `.claude/settings.json`):
```json
{
  "hooks": {
    "PreToolUse": [
      {"matcher": "Edit|MultiEdit|Write", "hooks": [{"type": "command", "command": "but claude pre-tool"}]}
    ],
    "PostToolUse": [
      {"matcher": "Edit|MultiEdit|Write", "hooks": [{"type": "command", "command": "but claude post-tool"}]}
    ],
    "Stop": [
      {"matcher": "", "hooks": [{"type": "command", "command": "but claude stop"}]}
    ]
  }
}
```

**Cosa Fa:**
- Pre-tool: GitButler crea/switch virtual branch prima di modifiche
- Post-tool: Commit automatico con prompt come messaggio (poi AI lo riscrive)
- Stop: Finalizza branch e commit quando agent termina

**Pro:**
- 1 commit = 1 chat round, 1 branch = 1 session Claude
- Multiple sessioni parallele senza conflitti
- No worktree manuali
- Commit messages automatici con AI

**Contro:**
- Richiede GitButler installato e configurato
- Non funziona con spawn-workers (diverso meccanismo spawn)
- Hook solo per Claude Code UI, non per agent Python/spawn

---

## 2. DOCUMENT & CLEAR PATTERN

### Patterns Trovati (Anthropic + Google ADK)

**A. Tool Result Clearing**
- Rimuovi output tool una volta processati
- "Safest lightest touch compaction"
- Ora disponibile nativamente in Claude API

**B. Structured Note-Taking (Agentic Memory)**
- Agent scrive `.sncp/`, `NOTES.md`, file esterni
- Recupera solo quando rilevante
- Esempio: Claude Code to-do lists, Pokemon agent con mappa gioco

**C. Context Isolation (Multi-Agent)**
- "Share memory by communicating, don't communicate by sharing memory"
- Sub-agent con contesto fresco, passa solo input/output specifici
- Mantieni storia completa solo quando necessario

**D. Session State Management**
- `session.state` come whiteboard condiviso
- Ogni agent scrive chiavi uniche (evita race conditions)
- Event-based tracking per debug e recovery

**E. Pre-Rot Threshold**
- Se model ha 1M context, degrado ~256k tokens
- Compaction PRIMA del "rot zone"

---

## 3. IMPLEMENTAZIONE NEL NOSTRO WORKFLOW

### Vale la Pena? **SI (parziale)**

**GitButler Hooks:** ❌ NO
- Non compatibile con spawn-workers (process separati, non Claude Code UI)
- Richiederebbe riscrittura spawn system

**Document & Clear:** ✅ SI
- Già implementato parzialmente con SNCP
- Migliorabile con patterns trovati

---

## 4. STEPS CONCRETI (IMPLEMENTAZIONE)

### A. Migliorare SNCP Esistente

**Pattern "Structured Note-Taking"** (già abbiamo base):

1. **Durante task:**
   ```bash
   # Worker scrive pensieri/stato
   echo "Decision: Using SSE over WebSocket because..." >> .sncp/memoria/decisioni/$(date +%Y%m%d)_worker_backend.md
   ```

2. **Fine task:**
   ```bash
   # Worker aggiorna stato
   cat > .swarm/tasks/TASK_001_OUTPUT.md << EOF
   # Output Task
   ## Fatto: [...]
   ## File: .sncp/idee/STUDIO_SSE.md
   ## Next: [...]
   EOF
   ```

### B. Tool Result Clearing (Pattern Compaction)

**Script helper:** `.swarm/scripts/compact-context.sh`
```bash
#!/bin/bash
# Rimuove tool output vecchi da history
# Chiamato da Regina quando context > 100k tokens

# Esempio: conserva solo ultimi 50 tool calls
# Implementa con API Claude message compaction
```

### C. Context Isolation (già funzionante!)

Nostro spawn-workers GIA FA questo:
- Clone separato = contesto isolato ✅
- Comunicazione via file (.swarm/tasks/) ✅
- "Share by communicating" ✅

### D. Session State Whiteboard

**Nuovo file:** `.swarm/session_state.json`
```json
{
  "regina": {"status": "ORCHESTRATING", "tasks_active": 3},
  "worker_backend": {"status": "WORKING", "task": "TASK_001"},
  "worker_frontend": {"status": "IDLE"}
}
```

Scripts:
- `scripts/swarm/update-session-state.sh [worker] [key] [value]`
- Regina legge state prima di spawn decision

---

## 5. RACCOMANDAZIONE FINALE

### IMPLEMENTA (Priorità Alta):

1. **Structured Note-Taking** (upgrade SNCP)
   - Workers scrivono decisioni in `.sncp/memoria/decisioni/YYYYMMDD_worker.md`
   - Regina legge solo summary in `.swarm/tasks/OUTPUT.md`
   - Effort: 2h, Beneficio: -30% context sprecato

2. **Session State Whiteboard**
   - File `.swarm/session_state.json` condiviso
   - Update-session-state.sh helper
   - Effort: 1h, Beneficio: migliore orchestration

3. **Pre-Compaction Warning**
   - Regina monitora context usage
   - Avviso a 150k tokens (prima rot zone)
   - Effort: 30min, Beneficio: evita degrado

### NON IMPLEMENTARE:

1. **GitButler Hooks** - incompatibile con spawn architecture

---

## FONTI CONSULTATE

- [Claude Code Hooks | GitButler Docs](https://docs.gitbutler.com/features/ai-integration/claude-code-hooks)
- [Automate AI Workflows with Claude Code Hooks](https://blog.gitbutler.com/automate-your-ai-workflows-with-claude-code-hooks)
- [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Context Management: Missing Piece in Agentic AI](https://datahub.com/blog/context-management-is-the-missing-piece-in-the-agentic-ai-puzzle/)
- [Developer's Guide to Multi-Agent Patterns (Google ADK)](https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/)
- [How We Built Multi-Agent Research System (Anthropic)](https://www.anthropic.com/engineering/multi-agent-research-system)

---

**TL;DR:**
GitButler hooks = non applicabile.
Document & Clear patterns = già parzialmente implementato, upgrade SNCP + session state = quick wins.
