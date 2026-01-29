# Best Practices Memory Systems 2026

**Data:** 29 Gennaio 2026
**Ricercatrice:** Cervella Researcher
**Baseline:** Report Moltbot (`reports/RICERCA_MEMORIA_PERSISTENTE_MOLTBOT.md`)

---

## Executive Summary

**TL;DR:**
- **Memory Flush:** Trigger automatico al 70-80% token budget, con silent turn per salvataggio
- **Daily vs Session:** Industria preferisce session-based con metadata, ma daily logs utili per context temporale
- **Security Audit:** Tool multipli (Gitleaks, TruffleHog) + 1600+ regex patterns disponibili open-source
- **MCP Memory:** Diversi server disponibili (mcp-memory-service, claude-memory-mcp), tutti local-first con semantic search

**Raccomandazione CervellaSwarm:** Implementare memory flush automatico (HIGH), aggiungere security audit script (HIGH), sperimentare daily logs (MEDIUM).

---

## 1. MEMORY FLUSH PATTERNS

### 1.1 Token Budget Triggers

**Standard Industria 2026:**

| Trigger Point | Action | Use Case |
|---------------|--------|----------|
| **70-80% token budget** | Auto-compact with summarization | Most agents (Goose, Moltbot) |
| **4,000 tokens before limit** | Silent agentic turn for memory write | Moltbot/Clawdbot approach |
| **Event-driven** | Memory pressure alert → LLM reviews working memory | MemGPT OS paradigm |

**Best Practice:** Non aspettare il limite - agire proattivamente per evitare context loss.

#### Pattern 1: Auto-Compact con Threshold (Goose)

```bash
# Environment variable per configurare threshold
export GOOSE_AUTO_COMPACT_THRESHOLD=0.80  # 80% del context window

# Goose auto-compacts quando tokens_used > (context_limit * threshold)
# Preserva parti chiave, comprime il resto
```

**Pro:** Automatico, configurabile, trasparente
**Contro:** Richiede LLM call per summarization (costo + latenza)

#### Pattern 2: Silent Agentic Turn (Moltbot)

```pseudocode
if tokens_used > (context_limit - 4000):
    trigger_silent_turn()
    # Agent scrive memoria critica in MEMORY.md
    # Risponde con NO_REPLY (non visibile a utente)
    compact_context()
```

**Pro:** Seamless per user, nessuna interruzione workflow
**Contro:** Richiede agent capability di identificare info critica

#### Pattern 3: OS Paradigm con Paging (MemGPT)

```
Primary Context (RAM):
├── Static system prompt
├── Dynamic working context
└── FIFO message buffer

External Context (Disk):
├── Recall Storage (searchable history)
└── Archival Storage (vector-based semantic search)

# LLM usa function calls per accedere external context
function conversation_search(query)
function archival_insert(content)
```

**Pro:** Scalabile, separazione esplicita working/long-term memory
**Contro:** Complessità implementativa, richiede function calling capability

### 1.2 Checkpointing Strategies

**Tre approcci principali:**

#### A. Continuous Checkpoint (OpenAI Memory)
- Background extraction ogni 24 ore
- Automatic summarization conversazioni recenti
- User-facing memory editable in UI

**Quando usare:** User-facing assistants, long-lived agents

#### B. Session-Based Checkpoint (Claude Projects)
- Memory summary aggiornato al termine sessione
- Project-scoped isolation
- Manual edit disponibile

**Quando usare:** Project-based workflows, multi-project agents

#### C. Self-Managed Write-Back (MemGPT)
- LLM decide autonomamente quando scrivere
- Memory correction capability (overwrite outdated facts)
- Event-driven triggers

**Quando usare:** Autonomous agents, complex multi-turn workflows

### 1.3 Implementazione Pratica per CervellaSwarm

**Proposta: Memory Flush Hook**

```bash
#!/bin/bash
# scripts/swarm/memory-flush.sh [worker_name]

WORKER=$1
TOKEN_USAGE=$(get_current_token_usage)
TOKEN_LIMIT=$(get_model_token_limit)
THRESHOLD=0.75  # 75%

if (( TOKEN_USAGE > TOKEN_LIMIT * THRESHOLD )); then
    echo "[MEMORY FLUSH] Token usage at ${TOKEN_USAGE}/${TOKEN_LIMIT}"

    # Silent turn: save critical decisions
    save_to_prompt_ripresa "$WORKER"
    update_stato_md "$WORKER"

    # Log flush event
    log_memory_flush "$WORKER" "$TOKEN_USAGE"

    # Optional: trigger context summarization
    # summarize_and_compact "$WORKER"
fi
```

**Integration points:**
1. Call in `spawn-workers` before session end
2. Periodic check every N turns (configurable)
3. Pre-checkpoint trigger (before git commit)

**Success criteria:**
- Zero memory loss during long sessions
- No user-visible interruptions
- Audit trail in logs

---

## 2. DAILY LOGS VS SESSION LOGS

### 2.1 Confronto Approcci

| Aspetto | Daily Logs | Session Logs |
|---------|------------|--------------|
| **Organizzazione** | Chronological (YYYY-MM-DD) | Per-session (unique ID) |
| **Pro** | Easy temporal browsing, natural date-based retrieval | Clear session boundaries, better for debugging |
| **Contro** | Single day spans multiple sessions | Harder to answer "what happened on date X?" |
| **Best for** | Context-aware assistants, proactive agents | Task-based workflows, isolated operations |

### 2.2 Industria 2026: Session-Based Dominance

**Consensus emergente:** Session-based logging con metadata enrichment.

**Pattern standard:**
```json
{
  "session_id": "uuid",
  "user_id": "user_identifier",
  "timestamp": "2026-01-29T14:30:00Z",
  "project": "miracollo",
  "worker": "cervella-backend",
  "task": "implement_sse_endpoint",
  "status": "completed",
  "decisions": [],
  "files_modified": []
}
```

**Perché session-based vince:**
1. **Tracing:** Request ID/Session ID linkano logs, traces, metrics
2. **Debugging:** Fault isolation per-session più facile
3. **Compliance:** Audit trail per-session requirement enterprise
4. **User-facing:** User session = natural boundary

### 2.3 Daily Logs: Quando Hanno Senso

**Use cases validi:**
- Proactive agents (24/7 running, no clear session boundary)
- Temporal pattern analysis ("cosa succede di solito il Lunedì?")
- Daily standup automation
- Calendar-integrated workflows

**Esempio Moltbot:**
```
memory/
├── 2026-01-29.md   # Today + Yesterday loaded every session
├── 2026-01-28.md   # Running context, day-to-day notes
└── 2026-01-27.md   # Archived
```

**Vantaggi:** Facile rispondere "cosa abbiamo fatto ieri?", natural temporal browsing.

### 2.4 Hybrid Approach (Best of Both)

**Proposta per CervellaSwarm:**

```
.sncp/progetti/miracollo/
├── PROMPT_RIPRESA_miracollo.md     # Long-term curated
├── stato.md                         # Current status
├── handoff/                         # Session-based (SNCP 2.0)
│   ├── session_20260129_143000.md
│   └── session_20260129_093000.md
└── memoria/                         # NEW: Daily logs (optional)
    ├── 2026-01-29.md                # Aggregate of today's sessions
    └── 2026-01-28.md                # Yesterday
```

**Workflow:**
1. **Durante sessione:** Scrivi in handoff/session_*.md (session-based, attuale)
2. **Fine giornata:** Aggregate script crea memoria/YYYY-MM-DD.md (daily summary)
3. **Long-term:** Informazioni critiche → PROMPT_RIPRESA (curated)

**Benefit:** Best of both - session granularity + temporal browsing.

### 2.5 Logging Best Practices (2026 Consensus)

**MUST HAVE:**
- Structured logging (JSON)
- Session/Request ID per tutti gli eventi
- Timestamp preciso (ISO 8601)
- Metadata enrichment (worker, project, task)
- Appropriate log levels (info, warning, error)

**NICE TO HAVE:**
- Latency tracking
- Model version logging
- Tool call tracing
- Context size monitoring

**AVOID:**
- Plain text logs without structure
- Missing timestamps
- No session correlation
- Secrets in logs (CRITICAL!)

---

## 3. SECURITY AUDIT FOR MEMORY FILES

### 3.1 Il Problema

**Moltbot lesson learned:** Plaintext secrets in memory files = security nightmare.

**Vettori di attacco:**
- Filesystem access → read secrets
- Malware targeting (Redline, Lumma, Vidar confermati)
- Prompt injection → extract stored credentials
- Accidental git commit di secrets
- Public repo exposure

### 3.2 Detection Methods (2026 State-of-Art)

**Multi-layer approach:**

#### Layer 1: Regex-Based Pattern Matching

Database: **secrets-patterns-db** (1600+ patterns, open-source)

Esempi pattern comuni:

```regex
# AWS Access Key ID
AKIA[0-9A-Z]{16}

# GitHub Personal Access Token
ghp_[0-9a-zA-Z]{36}

# Generic API Key (high entropy)
[a-zA-Z0-9_-]{32,}

# JWT Token
eyJ[A-Za-z0-9-_=]+\.eyJ[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*

# OpenAI API Key
sk-[a-zA-Z0-9]{48}

# Password patterns
(password|passwd|pwd|secret|token|api_key)\s*[:=]\s*['"]?[^\s'"]+['"]?
```

#### Layer 2: Entropy Analysis

```python
import math
from collections import Counter

def calculate_entropy(string):
    """Shannon entropy to detect high-randomness strings"""
    if not string:
        return 0

    counter = Counter(string)
    length = len(string)
    entropy = -sum(
        (count / length) * math.log2(count / length)
        for count in counter.values()
    )
    return entropy

# Threshold: entropy > 4.5 = potential secret
if calculate_entropy(candidate_string) > 4.5:
    flag_as_potential_secret()
```

**Use case:** Catch generic secrets non coperti da regex specifici.

#### Layer 3: Contextual Validation

```python
def validate_context(line, match):
    """Reduce false positives via context analysis"""

    # Check surrounding keywords
    secret_keywords = ['api_key', 'secret', 'token', 'password', 'credential']
    if any(kw in line.lower() for kw in secret_keywords):
        return True

    # Check if in assignment
    if '=' in line and match.start() > line.index('='):
        return True

    # Check if in config-like structure
    if ':' in line and match.start() > line.index(':'):
        return True

    return False
```

### 3.3 Tool Comparison (2026)

| Tool | Patterns | Verification | Speed | Best For |
|------|----------|--------------|-------|----------|
| **Gitleaks** | ~60 built-in | No | Fast (Golang) | CI/CD integration |
| **TruffleHog** | 700+ detectors | Yes (700+ APIs) | Slower | Historical scan + verification |
| **GitGuardian** | Proprietary | Yes | Cloud-based | Enterprise, dashboards |
| **secrets-patterns-db** | 1600+ (YAML) | No | - | Custom tool integration |

**Academic findings (2026):**
- Gitleaks finds more secrets (higher recall)
- TruffleHog better classification (higher precision)
- **1533 + 438 non-overlapping secrets** → Need BOTH tools!

**Raccomandazione:** Use multiple tools - no single tool catches everything.

### 3.4 Implementazione CervellaSwarm

**Script proposto:** `scripts/sncp/audit-secrets.sh`

```bash
#!/bin/bash
# scripts/sncp/audit-secrets.sh
# Scan SNCP files for accidental secret exposure

set -euo pipefail

SNCP_DIR=".sncp/progetti"
REPORT_FILE=".swarm/security/secrets_audit_$(date +%Y%m%d_%H%M%S).txt"

echo "[SECURITY AUDIT] Scanning SNCP files for secrets..."

# Pattern list (high-precision, low false-positive)
PATTERNS=(
    "AKIA[0-9A-Z]{16}"                                    # AWS
    "ghp_[0-9a-zA-Z]{36}"                                 # GitHub PAT
    "sk-[a-zA-Z0-9]{48}"                                  # OpenAI
    "AIza[0-9A-Za-z_-]{35}"                              # Google API
    "['\"]password['\"]:\s*['\"][^'\"]+['\"]"           # Password in JSON
    "bearer [a-zA-Z0-9_-]{30,}"                          # Bearer token
    "api[_-]?key['\"]?\s*[:=]\s*['\"]?[a-zA-Z0-9_-]{20,}" # Generic API key
)

FOUND=0

for pattern in "${PATTERNS[@]}"; do
    matches=$(grep -r -E -i "$pattern" "$SNCP_DIR" 2>/dev/null || true)
    if [[ -n "$matches" ]]; then
        echo "⚠️  FOUND: $pattern"
        echo "$matches"
        echo ""
        FOUND=$((FOUND + 1))
    fi
done

if [[ $FOUND -eq 0 ]]; then
    echo "✅ No secrets detected"
    exit 0
else
    echo "❌ CRITICAL: $FOUND potential secrets found!"
    echo "Review: $REPORT_FILE"
    exit 1
fi
```

**Integration points:**
1. Pre-commit hook (blocca commit se trova secrets)
2. Weekly cron job (audit periodico)
3. CI/CD pipeline (scan repo completo)

**Success criteria:**
- Zero secrets committed to git
- Audit trail in `.swarm/security/`
- Automated alerts on detection

### 3.5 Security Best Practices (2026)

**DO:**
- ✅ Use environment variables (`.env`, excluded from git)
- ✅ Use secret managers (Vault, AWS Secrets Manager, 1Password)
- ✅ Educate Workers: NEVER write credentials to memory
- ✅ Regular audits (automated)
- ✅ Private repos (baseline, not sufficient)

**DON'T:**
- ❌ Store API keys in PROMPT_RIPRESA or stato.md
- ❌ Commit `.env` to git (even private repos)
- ❌ Rely on `.gitignore` alone (history still exposed)
- ❌ Trust single tool for detection
- ❌ Leave memory files world-readable

**Emergency response:**
```bash
# If secret leaked to git:
1. Rotate/revoke secret IMMEDIATELY
2. git filter-repo --invert-paths --path <file>  # Remove from history
3. Force push (breaks history, coordinate team)
4. Audit who had access
5. Improve detection pipeline
```

---

## 4. MCP MEMORY SERVERS

### 4.1 Overview Ecosystem (2026)

**MCP (Model Context Protocol):** Standard Anthropic per tool integration con Claude.

**Memory servers disponibili:**

| Server | Storage | Semantic Search | Verification | Best For |
|--------|---------|-----------------|--------------|----------|
| **mcp-memory-service** | SQLite-vec OR Cloudflare | ✅ MiniLM-L6-v2 | Quality scoring (DeBERTa) | Multi-tool, 13+ AI apps |
| **claude-memory-mcp** | SQLite | ✅ Sentence transformers | No | Claude Desktop focus |
| **mcp-knowledge-graph** | Neo4j/local graph | ✅ + Graph traversal | No | Relationship-heavy workflows |
| **mcp-memory-keeper** | SQLite | Basic | No | Simple persistent context |
| **OpenMemory MCP** | Mem0 backend | ✅ Advanced | Yes | Enterprise, Mem0 ecosystem |

### 4.2 Deep Dive: mcp-memory-service

**Perché è interessante:**

#### A. Modular Backend Architecture
```
Backend options:
├── SQLite-vec (local, ~5ms latency, single-user)
├── Cloudflare D1 + Vectorize (cloud sync, multi-device)
└── Hybrid (local cache + background cloud sync)
```

**Benefit:** Start local, scale to cloud se necessario.

#### B. Knowledge Graph + Vector Search

```
Memory storage = Vector embeddings + Graph relationships

Relationships:
- causes (decision → consequence)
- fixes (solution → problem)
- supports (evidence → claim)
- contradicts (conflict detection)

Query: Find similar memories → Traverse graph → Get connected context
```

**Benefit:** Non solo semantic similarity, ma context traversal.

#### C. Quality-First Design

```python
# DeBERTa classifier filters noise
quality_score = assess_memory_quality(text)

if quality_score < THRESHOLD:
    skip_storage()  # Don't pollute memory

# Weight recent/frequently-accessed
relevance_score = combine(
    semantic_similarity,
    recency_weight,
    access_frequency
)
```

**Benefit:** Memory curata automaticamente, meno rumore.

#### D. 12 Unified MCP Tools

```
Core:
- store_memory(content, metadata)
- recall_memory(query, filters)

Advanced:
- search_memories(semantic_query, time_range, tags)
- manage_relationships(source_id, target_id, relation_type)
- get_quality_score(memory_id)
- forget_memory(memory_id)
```

**Tool metadata:**
- Read-only hints (guide LLM usage)
- Destructive markers (prevent accidental deletion)

#### E. SHODH Ecosystem Compatibility

**SHODH:** Unified Memory API Specification v1.0.0

**Benefit:** Interoperability across memory services, no vendor lock-in.

### 4.3 Comparison: mcp-memory-service vs Moltbot

| Aspect | Moltbot | mcp-memory-service |
|--------|---------|-------------------|
| **Storage** | Plaintext Markdown | SQLite-vec + embeddings |
| **Search** | Linear (load files) | Semantic vector search |
| **Structure** | Flat (daily + MEMORY.md) | Graph (entities + relations) |
| **Quality control** | Manual (user curates) | Automatic (DeBERTa scoring) |
| **Multi-tool** | Moltbot-specific | 13+ AI apps |
| **Privacy** | Local files | Local OR cloud (choice) |
| **Transparency** | ✅ Human-readable | 🟡 Embeddings not interpretable |

**Trade-off:** Moltbot più trasparente, mcp-memory-service più scalabile.

### 4.4 Integration con CervellaSwarm

**Opzioni:**

#### Option 1: Keep Current (File-Based SNCP)
**Pro:** Massima trasparenza, git-native, zero dependencies
**Contro:** No semantic search, linear scaling

**Quando:** < 100 progetti attivi, plaintext sufficient

#### Option 2: Add MCP Memory Layer (Optional)
**Pro:** Semantic search, scalability, relational memory
**Contro:** Complessità, embeddings overhead

**Quando:** > 100 progetti, users request "find when we discussed X"

#### Option 3: Hybrid (Raccomandazione)
```
Primary: SNCP file-based (source of truth)
       ↓
Optional: MCP memory layer (accelerator)
       ↓
Workflow: Write to SNCP, optionally index in MCP
```

**Architecture:**

```
.sncp/progetti/miracollo/
├── PROMPT_RIPRESA_miracollo.md   # Source of truth (plaintext)
└── stato.md

~/.mcp/memory/
└── miracollo_index/              # Optional vector index
    ├── embeddings.db
    └── graph.db

# Sync script
scripts/sncp/sync-to-mcp.sh miracollo
  → Read PROMPT_RIPRESA
  → Extract facts/decisions
  → Store in MCP memory layer
  → Enable semantic search
```

**When to trigger sync:**
- Post-checkpoint (after PROMPT_RIPRESA update)
- On-demand ("Cervella, what did we decide about SSE?")
- Weekly batch (background indexing)

**Success criteria:**
- SNCP remains source of truth (no lock-in)
- MCP layer OPTIONAL (system works without it)
- Semantic search available when needed

### 4.5 Installation Example (mcp-memory-service)

```bash
# 1. Install
pip install mcp-memory-service

# 2. Quick setup (60 seconds)
python -m mcp_memory_service.scripts.installation.install --quick

# 3. Configure Claude Desktop (~/.config/claude/config.json)
{
  "mcpServers": {
    "memory": {
      "command": "memory",
      "args": ["server"]
    }
  }
}

# 4. Restart Claude Desktop → MCP tools available
```

**Test:**
```
User: "Remember that we decided to use SSE for real-time updates"
Claude: [stores in MCP memory]

User: "What did we decide about real-time?"
Claude: [semantic search retrieves SSE decision]
```

---

## 5. RACCOMANDAZIONI PER CERVELLASWARM

### 5.1 Immediate Actions (HIGH Priority)

#### 1. Memory Flush Automation
**File:** `scripts/swarm/memory-flush.sh`

**Trigger points:**
- 75% token budget (proactive)
- Before spawn-workers session end
- Pre-checkpoint (before git commit)

**Implementation:**
```bash
# Integration in spawn-workers
if [ "$TOKEN_USAGE_PERCENT" -gt 75 ]; then
    scripts/swarm/memory-flush.sh "$WORKER_NAME"
fi
```

**Success metric:** Zero reported memory loss in worker sessions.

#### 2. Security Audit Script
**File:** `scripts/sncp/audit-secrets.sh`

**Integration:**
- Pre-commit hook (block commit if secrets found)
- Weekly cron job
- CI/CD pipeline

**Pattern database:** Use secrets-patterns-db (1600+ regex)

**Success metric:** Zero secrets in git history (audit verified).

### 5.2 Medium Priority

#### 3. Daily Logs Experiment
**File structure:**
```
.sncp/progetti/cervellaswarm/
└── memoria/
    ├── 2026-01-29.md   # Aggregate of today's sessions
    └── 2026-01-28.md   # Yesterday
```

**Test on:** CervellaSwarm itself (dogfooding)

**Duration:** 1 settimana

**Evaluation criteria:**
- Does it improve temporal clarity?
- Is it worth the extra file?
- Feedback from Rafa/Workers

**Decision:** Continue, iterate, or drop based on data.

#### 4. Tool Comparison (Gitleaks vs TruffleHog)
**Action:** Run both on CervellaSwarm repo

**Compare:**
- Detection overlap
- False positive rate
- Performance (scan time)

**Decide:** Single tool or dual-tool pipeline.

### 5.3 Future (LOW Priority)

#### 5. MCP Memory Layer (Optional RAG)
**Trigger:** IF > 100 progetti OR user requests semantic search

**Architecture:** Hybrid (SNCP = source of truth, MCP = accelerator)

**POC:** Test mcp-memory-service with Miracollo

**Success criteria:**
- SNCP still works without MCP
- Semantic search adds value
- Sync script reliable

#### 6. Memory Quality Scoring
**Borrow from:** mcp-memory-service (DeBERTa classifier)

**Goal:** Auto-detect low-quality entries in PROMPT_RIPRESA

**Implementation:**
```python
# scripts/sncp/quality-check.py
score = assess_prompt_ripresa_quality(file_path)

if score < THRESHOLD:
    warn("Low quality entries detected, consider cleanup")
```

### 5.4 Implementation Roadmap

```
┌─────────────────────────────────────────────┐
│ FASE 1 (Week 1): Security + Memory Flush    │
│ - audit-secrets.sh (pre-commit hook)        │
│ - memory-flush.sh (worker integration)      │
│ - Test on CervellaSwarm                     │
└─────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────┐
│ FASE 2 (Week 2-3): Daily Logs Experiment    │
│ - Add memoria/ to cervellaswarm             │
│ - 1 week trial                              │
│ - Evaluate: continue or drop                │
└─────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────┐
│ FASE 3 (Month 2): Tool Optimization         │
│ - Compare Gitleaks vs TruffleHog            │
│ - Quality scoring POC                       │
│ - Iterate based on learnings                │
└─────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────┐
│ FASE 4 (Future): Optional MCP Layer         │
│ - IF scale triggers (>100 progetti)         │
│ - MCP memory service POC                    │
│ - Hybrid architecture validation            │
└─────────────────────────────────────────────┘
```

### 5.5 Success Metrics

**Memory Flush:**
- Zero memory loss incidents (target: 0 per month)
- Worker sessions complete without context truncation

**Security Audit:**
- Zero secrets in git (verified by audit)
- Pre-commit hook blocks 100% of secret commits

**Daily Logs (if adopted):**
- Faster temporal questions ("cosa abbiamo fatto Lunedì?")
- Rafa/Workers report value in usage

**Overall:**
- CervellaSwarm memory system = best-in-class
- Transparent + secure + scalable

---

## 6. CODE EXAMPLES

### 6.1 Memory Flush Script

```bash
#!/bin/bash
# scripts/swarm/memory-flush.sh
# Automatic memory flush before context limit

set -euo pipefail

WORKER_NAME="${1:-unknown}"
PROJECT="${2:-cervellaswarm}"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE=".swarm/logs/memory_flush_${TIMESTAMP}.log"

echo "[MEMORY FLUSH] Starting for worker: $WORKER_NAME" | tee -a "$LOG_FILE"

# 1. Identify critical information from current session
CRITICAL_ITEMS=$(
    # Parse recent conversation for decisions, TODOs, errors
    # This would be LLM-powered in production
    echo "- Decision: Use SSE for real-time"
    echo "- TODO: Implement security audit"
    echo "- Error: Fixed z-index issue"
)

# 2. Append to PROMPT_RIPRESA
PROMPT_RIPRESA=".sncp/progetti/${PROJECT}/PROMPT_RIPRESA_${PROJECT}.md"

if [[ -f "$PROMPT_RIPRESA" ]]; then
    echo "" >> "$PROMPT_RIPRESA"
    echo "## Session $TIMESTAMP (Auto-flushed)" >> "$PROMPT_RIPRESA"
    echo "$CRITICAL_ITEMS" >> "$PROMPT_RIPRESA"
    echo "✅ Appended to PROMPT_RIPRESA" | tee -a "$LOG_FILE"
else
    echo "⚠️  PROMPT_RIPRESA not found: $PROMPT_RIPRESA" | tee -a "$LOG_FILE"
fi

# 3. Update stato.md with current state
STATO_FILE=".sncp/progetti/${PROJECT}/stato.md"

if [[ -f "$STATO_FILE" ]]; then
    # Update "Last Updated" timestamp
    sed -i '' "s/Ultimo aggiornamento:.*/Ultimo aggiornamento: $(date)/" "$STATO_FILE"
    echo "✅ Updated stato.md" | tee -a "$LOG_FILE"
fi

# 4. Log flush event
echo "[MEMORY FLUSH] Completed at $(date)" | tee -a "$LOG_FILE"
echo "  Worker: $WORKER_NAME" | tee -a "$LOG_FILE"
echo "  Project: $PROJECT" | tee -a "$LOG_FILE"
```

### 6.2 Security Audit Script

```bash
#!/bin/bash
# scripts/sncp/audit-secrets.sh
# Scan SNCP files for accidental secrets

set -euo pipefail

SNCP_DIR=".sncp/progetti"
PATTERNS_FILE="scripts/sncp/secret_patterns.txt"
REPORT_DIR=".swarm/security"
REPORT_FILE="$REPORT_DIR/secrets_audit_$(date +%Y%m%d_%H%M%S).txt"

mkdir -p "$REPORT_DIR"

echo "============================================" | tee "$REPORT_FILE"
echo "SECURITY AUDIT: SNCP Secrets Detection" | tee -a "$REPORT_FILE"
echo "Started: $(date)" | tee -a "$REPORT_FILE"
echo "============================================" | tee -a "$REPORT_FILE"
echo "" | tee -a "$REPORT_FILE"

# Pattern list (high-precision)
declare -a PATTERNS=(
    "AKIA[0-9A-Z]{16}"                                      # AWS Access Key
    "(?i)(aws_secret_access_key|aws_session_token)\s*=\s*[a-zA-Z0-9/+=]{40}"  # AWS Secret
    "ghp_[0-9a-zA-Z]{36}"                                   # GitHub PAT
    "gho_[0-9a-zA-Z]{36}"                                   # GitHub OAuth
    "sk-[a-zA-Z0-9]{48}"                                    # OpenAI API Key
    "AIza[0-9A-Za-z_-]{35}"                                # Google API Key
    "ya29\.[0-9A-Za-z_-]+"                                 # Google OAuth
    "['\"]password['\"]:\s*['\"][^'\"]{8,}['\"]"          # Password in JSON
    "bearer\s+[a-zA-Z0-9_-]{30,}"                          # Bearer token
    "api[_-]?key['\"]?\s*[:=]\s*['\"]?[a-zA-Z0-9_-]{20,}"  # Generic API key
    "-----BEGIN\s+(RSA\s+)?PRIVATE\s+KEY-----"              # Private key
)

FOUND=0
TOTAL_MATCHES=0

# Scan each pattern
for pattern in "${PATTERNS[@]}"; do
    echo "Scanning pattern: $pattern" >> "$REPORT_FILE"

    # Use ripgrep (faster) if available, else grep
    if command -v rg &> /dev/null; then
        matches=$(rg --no-heading --line-number -e "$pattern" "$SNCP_DIR" 2>/dev/null || true)
    else
        matches=$(grep -r -n -E "$pattern" "$SNCP_DIR" 2>/dev/null || true)
    fi

    if [[ -n "$matches" ]]; then
        echo "⚠️  POTENTIAL SECRET DETECTED!" | tee -a "$REPORT_FILE"
        echo "Pattern: $pattern" | tee -a "$REPORT_FILE"
        echo "$matches" | tee -a "$REPORT_FILE"
        echo "" | tee -a "$REPORT_FILE"
        FOUND=$((FOUND + 1))
        TOTAL_MATCHES=$((TOTAL_MATCHES + $(echo "$matches" | wc -l)))
    fi
done

# Summary
echo "============================================" | tee -a "$REPORT_FILE"
echo "AUDIT SUMMARY" | tee -a "$REPORT_FILE"
echo "============================================" | tee -a "$REPORT_FILE"
echo "Patterns checked: ${#PATTERNS[@]}" | tee -a "$REPORT_FILE"
echo "Patterns with matches: $FOUND" | tee -a "$REPORT_FILE"
echo "Total matches: $TOTAL_MATCHES" | tee -a "$REPORT_FILE"
echo "Report saved: $REPORT_FILE" | tee -a "$REPORT_FILE"
echo "" | tee -a "$REPORT_FILE"

if [[ $FOUND -eq 0 ]]; then
    echo "✅ PASS: No secrets detected" | tee -a "$REPORT_FILE"
    exit 0
else
    echo "❌ FAIL: Potential secrets found!" | tee -a "$REPORT_FILE"
    echo "ACTION REQUIRED: Review matches and rotate exposed credentials" | tee -a "$REPORT_FILE"
    exit 1
fi
```

### 6.3 Daily Log Aggregator

```bash
#!/bin/bash
# scripts/sncp/aggregate-daily.sh
# Aggregate session logs into daily summary

set -euo pipefail

PROJECT="${1:-cervellaswarm}"
DATE="${2:-$(date +%Y-%m-%d)}"

HANDOFF_DIR=".sncp/progetti/${PROJECT}/handoff"
MEMORIA_DIR=".sncp/progetti/${PROJECT}/memoria"
DAILY_FILE="$MEMORIA_DIR/${DATE}.md"

mkdir -p "$MEMORIA_DIR"

echo "# Daily Summary: $DATE" > "$DAILY_FILE"
echo "" >> "$DAILY_FILE"
echo "**Project:** $PROJECT" >> "$DAILY_FILE"
echo "**Generated:** $(date)" >> "$DAILY_FILE"
echo "" >> "$DAILY_FILE"

# Find all session files for this date
sessions=$(find "$HANDOFF_DIR" -name "session_${DATE//-/}_*.md" 2>/dev/null | sort)

if [[ -z "$sessions" ]]; then
    echo "No sessions found for $DATE" >> "$DAILY_FILE"
    exit 0
fi

echo "## Sessions" >> "$DAILY_FILE"
echo "" >> "$DAILY_FILE"

# Aggregate each session
while IFS= read -r session_file; do
    session_name=$(basename "$session_file" .md)
    echo "### $session_name" >> "$DAILY_FILE"
    echo "" >> "$DAILY_FILE"

    # Extract key sections (customize as needed)
    if grep -q "## Decisioni" "$session_file"; then
        echo "**Decisioni:**" >> "$DAILY_FILE"
        sed -n '/## Decisioni/,/## /p' "$session_file" | head -n -1 >> "$DAILY_FILE"
        echo "" >> "$DAILY_FILE"
    fi

    if grep -q "## Completato" "$session_file"; then
        echo "**Completato:**" >> "$DAILY_FILE"
        sed -n '/## Completato/,/## /p' "$session_file" | head -n -1 >> "$DAILY_FILE"
        echo "" >> "$DAILY_FILE"
    fi

    echo "---" >> "$DAILY_FILE"
    echo "" >> "$DAILY_FILE"
done <<< "$sessions"

echo "✅ Daily summary created: $DAILY_FILE"
```

### 6.4 Pre-Commit Hook Integration

```bash
#!/bin/bash
# .git/hooks/pre-commit
# Block commits with secrets

set -e

echo "Running security audit..."

if ! scripts/sncp/audit-secrets.sh; then
    echo ""
    echo "❌ COMMIT BLOCKED: Secrets detected in staged files!"
    echo "Review the audit report and remove secrets before committing."
    echo ""
    echo "To bypass (NOT RECOMMENDED): git commit --no-verify"
    exit 1
fi

echo "✅ Security audit passed"
```

### 6.5 MCP Memory Sync (Optional)

```python
#!/usr/bin/env python3
# scripts/sncp/sync-to-mcp.py
# Sync PROMPT_RIPRESA to MCP memory layer (optional)

import json
import sys
from pathlib import Path
from datetime import datetime

def parse_prompt_ripresa(file_path):
    """Extract structured facts from PROMPT_RIPRESA"""
    with open(file_path, 'r') as f:
        content = f.read()

    # Simple parser - extract decisions, facts, TODOs
    facts = []
    current_section = None

    for line in content.split('\n'):
        if line.startswith('## '):
            current_section = line[3:].strip()
        elif line.startswith('- ') and current_section:
            facts.append({
                'section': current_section,
                'content': line[2:].strip(),
                'timestamp': datetime.now().isoformat()
            })

    return facts

def store_in_mcp(facts, project_name):
    """Store facts in MCP memory layer"""
    # This would call MCP memory service API
    # For demo, just print

    print(f"Storing {len(facts)} facts for project: {project_name}")

    for fact in facts:
        print(f"  - [{fact['section']}] {fact['content'][:50]}...")

        # Actual MCP call would be:
        # mcp_client.store_memory(
        #     content=fact['content'],
        #     metadata={'section': fact['section'], 'project': project_name}
        # )

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: sync-to-mcp.py <project>")
        sys.exit(1)

    project = sys.argv[1]
    file_path = Path(f".sncp/progetti/{project}/PROMPT_RIPRESA_{project}.md")

    if not file_path.exists():
        print(f"Error: {file_path} not found")
        sys.exit(1)

    facts = parse_prompt_ripresa(file_path)
    store_in_mcp(facts, project)

    print(f"✅ Synced {len(facts)} facts to MCP memory layer")
```

---

## 7. CONFRONTO: SNCP vs Alternative

### 7.1 SNCP (Current) vs Moltbot

| Feature | SNCP | Moltbot |
|---------|------|---------|
| **Format** | Markdown | Markdown |
| **Organization** | Hierarchical (progetti/bracci) | Flat (workspace) |
| **Memory Flush** | Manual checkpoint | Automatic (80% token) |
| **Security** | ✅ No secrets policy | ⚠️ Plaintext secrets |
| **Multi-project** | ✅ Isolated | ❌ Single workspace |
| **Daily logs** | ❌ (handoff session-based) | ✅ (memory/YYYY-MM-DD.md) |
| **Automation** | ✅ Hooks, verify-sync | 🟡 Requires user prompts |
| **Git integration** | ✅ Native | 🟡 Recommended, not enforced |
| **Semantic search** | ❌ (linear) | ❌ (optional with API keys) |

**SNCP wins:** Security, multi-project, automation
**Moltbot wins:** Daily logs, auto-flush (learn from this!)

### 7.2 SNCP vs Claude Projects

| Feature | SNCP | Claude Projects |
|---------|------|----------------|
| **Storage** | Local files | Cloud (proprietary) |
| **Version control** | ✅ Git-native | ❌ No git |
| **Transparency** | ✅ Full (plaintext) | 🟡 Partial (summary visible) |
| **Isolation** | Project + Branch (bracci/) | Project-only |
| **Automation** | ✅ Scripts, hooks | 🟡 Limited API |
| **Cross-device** | Via git push/pull | ✅ Automatic sync |
| **Search** | Linear (grep) | ✅ Semantic + keyword |

**SNCP wins:** Transparency, version control, automation
**Claude Projects wins:** Cross-device sync, semantic search

### 7.3 SNCP + MCP Hybrid vs Mem0

| Feature | SNCP + MCP | Mem0 |
|---------|------------|------|
| **Storage** | Markdown + SQLite-vec | Proprietary + vector DB |
| **Source of truth** | ✅ Plaintext files | ❌ Embeddings |
| **Graph memory** | 🟡 Optional (MCP layer) | ✅ Native |
| **Performance** | Fast (local) | Optimized (26% accuracy gain) |
| **Lock-in risk** | ✅ Low (files = source) | 🟡 Medium (Mem0 ecosystem) |
| **Transparency** | ✅ Full | 🟡 Partial |
| **Scalability** | 🟡 Good (with MCP) | ✅ Excellent (enterprise-proven) |

**SNCP + MCP wins:** Transparency, no lock-in, flexibility
**Mem0 wins:** Performance, scalability, production-proven

### 7.4 Decision Matrix: When to Use What

```
┌─────────────────────────────────────────────────────────┐
│ SCENARIO                  │ RECOMMENDATION              │
├─────────────────────────────────────────────────────────┤
│ < 10 projects             │ SNCP file-based (current)   │
│ 10-100 projects           │ SNCP + optional MCP layer   │
│ > 100 projects            │ SNCP + MCP hybrid required  │
│ Enterprise (1000+ users)  │ Consider Mem0 or dedicated  │
│ Proactive agent           │ Add daily logs to SNCP      │
│ Strict compliance         │ SNCP (audit trail native)   │
│ Cross-device sync needed  │ Consider Claude Projects OR │
│                           │ SNCP + git + MCP cloud      │
└─────────────────────────────────────────────────────────┘
```

**CervellaSwarm current state:** ~5 progetti attivi → SNCP perfect fit!

**Growth path:** Add MCP layer when > 50 progetti or semantic search requested.

---

## 8. LESSONS LEARNED SUMMARY

### 8.1 Memory Flush
- ✅ **Adopt:** 70-80% token budget trigger (proactive)
- ✅ **Adopt:** Silent turn for seamless UX
- 🟡 **Consider:** Self-managed write-back (LLM decides what to keep)

### 8.2 Daily Logs
- ✅ **Experiment:** Add memoria/ to CervellaSwarm (1 week trial)
- 🟡 **Evaluate:** Useful for temporal questions?
- ❌ **Don't:** Replace session-based handoff/ (keep both)

### 8.3 Security
- ✅ **Adopt:** Multi-tool scanning (Gitleaks + TruffleHog)
- ✅ **Adopt:** Pre-commit hook (block secrets)
- ✅ **Adopt:** 1600+ regex patterns from secrets-patterns-db
- ❌ **Never:** Store secrets in memory files

### 8.4 MCP Memory
- 🟡 **Consider:** Optional layer for semantic search
- ✅ **Architecture:** Hybrid (SNCP = source, MCP = accelerator)
- ❌ **Don't:** Replace SNCP with MCP (no lock-in)

### 8.5 Industry Trends (2026)
- Shift from RAG to **Contextual Memory** (agentic)
- **Knowledge graphs** for relational reasoning
- **Quality scoring** to filter noise
- **Session-based logging** dominance (with metadata)
- **Multi-tool security** scanning (no single tool sufficient)

---

## 9. NEXT STEPS

### Immediate (This Week)
1. ✅ Completare questo report
2. ⏳ Implementare `scripts/swarm/memory-flush.sh`
3. ⏳ Implementare `scripts/sncp/audit-secrets.sh`
4. ⏳ Testare su CervellaSwarm

### Short-term (Next 2 Weeks)
1. ⏳ Add pre-commit hook per security audit
2. ⏳ Experiment con daily logs (memoria/)
3. ⏳ Compare Gitleaks vs TruffleHog performance

### Medium-term (Next Month)
1. ⏳ Evaluate daily logs experiment → continue or drop
2. ⏳ Quality scoring POC (borrow from mcp-memory-service)
3. ⏳ Documentation update (best practices learned)

### Long-term (Future)
1. ⏳ IF scale triggers: POC MCP memory layer
2. ⏳ Hybrid architecture validation
3. ⏳ Consider OpenMemory MCP for enterprise features

---

## 10. FONTI

### Memory Flush & Token Management
- [OpenAI Cookbook: Session Memory Management](https://cookbook.openai.com/examples/agents_sdk/session_memory)
- [Serokell: Design Patterns for Long-Term Memory in LLM Architectures](https://serokell.io/blog/design-patterns-for-long-term-memory-in-llm-powered-architectures)
- [Medium: Ultimate Guide to LLM Memory](https://medium.com/@sonitanishk2003/the-ultimate-guide-to-llm-memory-from-context-windows-to-advanced-agent-memory-systems-3ec106d2a345)
- [Alok Mishra: 2026 Memory Stack for Enterprise Agents](https://alok-mishra.com/2026/01/07/a-2026-memory-stack-for-enterprise-agents/)
- [Goose Blog: Understanding Context Windows](https://block.github.io/goose/blog/2025/08/18/understanding-context-windows/)
- [Medium: How I Stopped LLM Token Overruns](https://medium.com/@bhagyarana80/how-i-stopped-llm-token-overruns-by-building-a-custom-memory-pruner-9250e81dc93e)
- [MarkTechPost: Agentic Memory Research](https://www.marktechpost.com/2026/01/12/how-this-agentic-memory-research-unifies-long-term-and-short-term-memory-for-llm-agents/)
- [Tekta.ai: SimpleMem 30x Efficiency](https://www.tekta.ai/ai-research-papers/simplemem-llm-agent-memory-2026)

### Logging Best Practices
- [AI Multiple: AI Agent Observability Tools 2026](https://research.aimultiple.com/agentic-monitoring/)
- [UptimeRobot: AI Agent Monitoring Best Practices](https://uptimerobot.com/knowledge-hub/monitoring/ai-agent-monitoring-best-practices-tools-and-metrics/)
- [O-mega: Top 5 Observability Platforms 2026](https://o-mega.ai/articles/top-5-ai-agent-observability-platforms-the-ultimate-2026-guide)
- [Medium: Mastering AI Agent Observability](https://medium.com/online-inference/mastering-ai-agent-observability-a-comprehensive-guide-b142ed3604b1)
- [Fiddler AI: Monitoring Agentic Applications](https://www.fiddler.ai/blog/monitoring-controlling-agentic-applications)
- [Temporal: Orchestrating Ambient Agents](https://temporal.io/blog/orchestrating-ambient-agents-with-temporal)
- [Shipbook: Logs for AI Agents](https://blog.shipbook.io/logs-for-ai-agents)

### Security & Secrets Detection
- [Jit: Top 8 Git Secrets Scanners 2026](https://www.jit.io/resources/appsec-tools/git-secrets-scanners-key-features-and-top-tools-)
- [Jit: TruffleHog vs Gitleaks Comparison](https://www.jit.io/resources/appsec-tools/trufflehog-vs-gitleaks-a-detailed-comparison-of-secret-scanning-tools)
- [GitGuardian: Secrets Detection Solutions](https://www.gitguardian.com/solutions/secrets-detection)
- [GitHub: secrets-patterns-db (1600+ patterns)](https://github.com/mazen160/secrets-patterns-db)
- [Nightfall AI: Essential Guide to Secrets Scanning](https://www.nightfall.ai/blog/essential-guide-secrets-scanning)
- [GitHub Docs: About Secret Scanning](https://docs.github.com/code-security/secret-scanning/about-secret-scanning)
- [GitGuardian: Building Reliable Secrets Detection](https://blog.gitguardian.com/secrets-in-source-code-episode-3-3-building-reliable-secrets-detection/)
- [GitGuardian: Secret Scanning Tools 2026](https://blog.gitguardian.com/secret-scanning-tools/)
- [Aikido: Best Secret Scanning Tools 2025](https://www.aikido.dev/blog/top-secret-scanning-tools)

### MCP Memory Servers
- [GitHub: mcp-memory-service](https://github.com/doobidoo/mcp-memory-service)
- [PulseMCP: Claude Memory MCP Server](https://www.pulsemcp.com/servers/whenmoon-memory)
- [GitHub: mcp-knowledge-graph](https://github.com/shaneholloman/mcp-knowledge-graph)
- [GitHub: claude-memory-mcp (WhenMoon)](https://github.com/WhenMoon-afk/claude-memory-mcp)
- [MCP.so: Memory Service](https://mcp.so/server/mcp-memory-service)
- [LobeHub: Claude Memory Setup Guide](https://lobehub.com/mcp/randall-gross-claude-memory-mcp)
- [Mem0: OpenMemory MCP Introduction](https://mem0.ai/blog/introducing-openmemory-mcp)
- [GitHub: mcp-memory-keeper](https://github.com/mkreyman/mcp-memory-keeper)

### Baseline (Moltbot)
- [Report interno: RICERCA_MEMORIA_PERSISTENTE_MOLTBOT.md](../reports/RICERCA_MEMORIA_PERSISTENTE_MOLTBOT.md)

---

## Conclusioni

**SNCP è ben posizionato** - trasparente, sicuro, automatizzato.

**Da adottare subito:**
1. Memory flush automatico (prevent loss)
2. Security audit script (prevent leaks)

**Da sperimentare:**
- Daily logs (temporal organization)

**Da considerare (future):**
- MCP memory layer (semantic search, IF scala)

**Philosophy confermata:** File-based, trasparenza, automation-first = vincente per CervellaSwarm.

---

*Cervella Researcher - Ricerca completata: 29 Gennaio 2026*
*"Studiare prima di agire - i player grossi hanno già risolto questi problemi!"*
