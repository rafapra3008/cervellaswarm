# Plan: AI Code Review System -- Project 5 Showcase

## Metadata
- **Architect**: cervella-architect
- **Created**: 2026-03-14
- **Complexity**: High
- **Files Affected**: 7 (same structure as LU Debugger)
- **Risk Score**: 0.3 (low -- proven pattern from Debugger)
- **Estimated Sessions**: 1-2 (pattern is identical to Debugger, built in 1 session)

---

## Phase 1: Understanding

### User Request

Build the 5th and final showcase: an AI Code Review app where users paste code and 4 AI agents analyze it using a verified LU protocol. The protocol ENFORCES that Security review completes before Performance can start, demonstrating that LU makes unsafe ordering STRUCTURALLY IMPOSSIBLE.

### Codebase Analysis

**Pattern to follow:** `lu-debugger/` (7 files, 1474 LOC)

| File | LOC | Purpose |
|------|-----|---------|
| `server.py` | 165 | FastAPI + SSE + rate limiting (SlowAPI) |
| `runner.py` | 346 | Async Claude API agents + SessionChecker |
| `demo_data.py` | 184 | Protocol source + pre-scripted steps |
| `static/index.html` | 748 | Monaco + chat UI |
| `Dockerfile` | 5 | Python 3.12-slim |
| `fly.toml` | 18 | Fly.io Frankfurt config |
| `requirements.txt` | 5 | Dependencies |

**Key LU types available:**
- `TaskRequest(task_id, description)` -- used for "orchestrator asks reviewer"
- `TaskResult(task_id, status, summary)` -- used for "reviewer returns findings"
- `DirectMessage(content)` -- used for "developer sends code" and "orchestrator sends report"

**SessionChecker behavior (critical for violation demo):**
- Enforces step-by-step sequential ordering
- If step 3 expects `orchestrator -> security: TaskRequest`, sending `orchestrator -> performance: TaskRequest` at step 3 raises `ProtocolViolation`
- The ordering is inherent in the protocol definition sequence, NOT via `X before Y` properties (those operate on MessageKind, not roles)
- `X before Y` properties verify MessageKind ordering (e.g., `task_request before task_result`)

**Color palettes:**
- Debugger uses GitHub Dark theme (`--bg: #0d1117`)
- Incident + Zoo use Catppuccin Mocha (`--bg-base: #1e1e2e`)
- **Decision:** Use Catppuccin Mocha for visual consistency with the newer showcases (Incident + Zoo)

### Constraints

1. Protocol must use existing LU syntax and message types (TaskRequest, TaskResult, DirectMessage)
2. SessionChecker enforces sequential ordering -- the protocol step order IS the enforcement
3. Violation demo must trigger ProtocolViolation exception, caught and displayed
4. Haiku for cost ($0.000005/run target)
5. Must deploy to Fly.io Frankfurt (same region as Debugger)
6. Single HTML file for consistency with other showcases

---

## Phase 2: Design

### Approach

1. **Copy the Debugger pattern exactly** -- same file structure, same SSE mechanism, same async runner
2. **5 roles instead of 3** -- developer, orchestrator, security, performance, quality
3. **User code input** -- Monaco editor is EDITABLE (not read-only), user pastes code to review
4. **Protocol display** -- second read-only Monaco shows the CodeReview.lu protocol
5. **Categorized findings** -- each reviewer returns structured findings (severity + description)
6. **Violation scenario** -- quality tries to review before security finishes, BLOCKED

### Protocol Design (Final)

```lu
# SPDX-License-Identifier: Apache-2.0
# Code Review Protocol -- AI Code Review Demo
#
# Four AI agents review code in enforced order:
# Security MUST complete before Performance starts.
# Performance MUST complete before Quality starts.
# Why? No point optimizing insecure code. No point
# polishing code with performance bugs.

type ReviewSeverity = Critical | Warning | Info

agent Developer:
    role: developer
    trust: standard
    accepts: DirectMessage
    produces: DirectMessage
    requires: code.ready
    ensures: code.submitted

agent ReviewOrchestrator:
    role: orchestrator
    trust: verified
    accepts: TaskResult, DirectMessage
    produces: TaskRequest, DirectMessage
    requires: code.received
    ensures: review.complete

agent SecurityReviewer:
    role: security
    trust: trusted
    accepts: TaskRequest
    produces: TaskResult
    requires: code.available
    ensures: security.checked

agent PerformanceReviewer:
    role: performance
    trust: trusted
    accepts: TaskRequest
    produces: TaskResult
    requires: security.passed
    ensures: performance.checked

agent QualityReviewer:
    role: quality
    trust: trusted
    accepts: TaskRequest
    produces: TaskResult
    requires: performance.passed
    ensures: quality.checked

protocol CodeReview:
    roles: developer, orchestrator, security, performance, quality

    developer sends code to orchestrator
    orchestrator asks security to review code
    security returns security findings to orchestrator
    orchestrator asks performance to review code
    performance returns performance findings to orchestrator
    orchestrator asks quality to review code
    quality returns quality findings to orchestrator

    when orchestrator decides:
        critical_found:
            orchestrator sends urgent report to developer
        all_clear:
            orchestrator sends clean report to developer

    properties:
        always terminates
        no deadlock
        all roles participate
        task_request before task_result
```

**Why this protocol works:**

The SessionChecker enforces that steps happen in EXACTLY this order:
1. developer -> orchestrator (DirectMessage: code)
2. orchestrator -> security (TaskRequest: review)
3. security -> orchestrator (TaskResult: findings)
4. orchestrator -> performance (TaskRequest: review)
5. performance -> orchestrator (TaskResult: findings)
6. orchestrator -> quality (TaskRequest: review)
7. quality -> orchestrator (TaskResult: findings)
8. CHOICE: orchestrator decides critical_found or all_clear
9. orchestrator -> developer (DirectMessage: report)

If anyone tries step 4 before step 3, ProtocolViolation is raised. The ordering is NOT a convention -- it is STRUCTURAL.

**Violation scenario:**

After step 2 (security receives code), quality tries to send findings to orchestrator. SessionChecker expects step 3 (security -> orchestrator: TaskResult), but gets (quality -> orchestrator: TaskResult). BLOCKED.

This is compelling because: "Quality reviewer decided it already knows the code quality without waiting for security. The protocol says NO -- security review MUST complete first. Not by company policy. By mathematical proof."

### Critical Files

| File | Modification | Risk |
|------|-------------|------|
| `code-review/server.py` | New file, copy Debugger pattern | Low |
| `code-review/runner.py` | New file, 5 agents instead of 3, code input | Low |
| `code-review/demo_data.py` | New file, CodeReview protocol + scenarios | Low |
| `code-review/static/index.html` | New file, dual Monaco + findings UI | Medium |
| `code-review/Dockerfile` | New file, identical to Debugger | Low |
| `code-review/fly.toml` | New file, app name change only | Low |
| `code-review/requirements.txt` | New file, identical to Debugger | Low |

### API Endpoints

| Endpoint | Method | Purpose | Rate Limit |
|----------|--------|---------|------------|
| `GET /` | GET | Serve the HTML UI | none |
| `GET /api/protocol` | GET | Return CodeReview.lu source | none |
| `GET /api/status` | GET | Health check + live mode flag | none |
| `GET /api/run/demo` | GET | Pre-scripted happy path (all clear) | 10/min |
| `GET /api/run/demo-critical` | GET | Pre-scripted happy path (critical found) | 10/min |
| `GET /api/run/demo-break` | GET | Pre-scripted violation (quality skips security) | 10/min |
| `POST /api/run/live` | POST | Real Claude API + user code | 3/min |
| `POST /api/run/live-break` | POST | Real API + forced violation | 3/min |

**Note:** Live endpoints are POST (not GET) because they accept user code in the request body:
```json
{"code": "def transfer(amount): ..."}
```

For demo mode, GET is fine (no user input needed -- code is pre-scripted).

### SSE Event Types

```typescript
// Same as Debugger, plus new types
type SSEEvent =
    | { type: "agent_message"; step: number; from: string; to: string;
        message_type: string; content: string; protocol_line: number; status: "ok" }
    | { type: "choice"; step: number; who: string; branch: string; protocol_line: number }
    | { type: "info"; step: number; content: string }
    | { type: "violation"; step: number; from: string; to: string;
        message_type: string; expected: string; got: string;
        protocol_line: number; error: string }
    | { type: "finding"; reviewer: string; severity: "critical"|"warning"|"info";
        title: string; detail: string; line?: number }
    | { type: "done"; completed: boolean; blocked?: boolean;
        messages: number; branch?: string;
        findings_count?: { critical: number; warning: number; info: number } }
```

The `finding` event type is NEW -- it lets the UI render individual findings in a structured panel as they arrive. Each reviewer can emit 1-3 findings. These are ADDITIONAL to the `agent_message` events (the message shows the full response, findings extract the structured parts).

### Agent System Prompts

**Orchestrator** (coordinates, does NOT review):
```
You are the Orchestrator in an AI Code Review demo using Lingua Universale protocols.
Your job is to coordinate the review. You do NOT review code yourself.
When you receive findings from all reviewers, summarize them into a final report.
Keep messages under 120 characters. Be professional and concise.
```

**Security Reviewer** (OWASP, injection, auth):
```
You are a Security Reviewer AI agent in a code review demo.
Analyze the provided code for security vulnerabilities:
- SQL injection, XSS, command injection
- Authentication/authorization flaws
- Hardcoded secrets or credentials
- Input validation gaps
- OWASP Top 10 issues

Return 1-3 findings. Each finding: [SEVERITY] Title: Detail.
Severity: CRITICAL, WARNING, or INFO.
Keep total response under 200 characters.
```

**Performance Reviewer** (complexity, memory, queries):
```
You are a Performance Reviewer AI agent in a code review demo.
Analyze the provided code for performance issues:
- Algorithm complexity (O(n^2) loops, unnecessary iterations)
- Memory leaks or excessive allocation
- N+1 query patterns
- Missing caching opportunities
- Blocking operations in async contexts

Return 1-3 findings. Each finding: [SEVERITY] Title: Detail.
Severity: CRITICAL, WARNING, or INFO.
Keep total response under 200 characters.
```

**Quality Reviewer** (patterns, naming, testability):
```
You are a Quality Reviewer AI agent in a code review demo.
Analyze the provided code for quality issues:
- Naming conventions and readability
- Design pattern violations (god objects, tight coupling)
- Missing error handling
- Testability concerns (hard to mock dependencies)
- Code duplication

Return 1-3 findings. Each finding: [SEVERITY] Title: Detail.
Severity: CRITICAL, WARNING, or INFO.
Keep total response under 200 characters.
```

### UI Layout (Text-Based Wireframe)

```
+------------------------------------------------------------------+
| AI Code Review  Lingua Universale  | [Demo v] [Review] [Break] | Live ready |
+------------------------------------------------------------------+
|                    |                    |                         |
|  CODE INPUT        |  PROTOCOL          |  AGENT ACTIVITY        |
|  (Monaco,editable) |  (Monaco,readonly) |                        |
|                    |                    |  Step 1                |
|  def transfer():   |  protocol Code... |  developer -> orch     |
|    amount = ...    |    roles: ...      |  "Submitted 12 lines"  |
|    db.execute(     |    dev sends code  |                        |
|      "SELECT..."   |    orch asks sec   |  Step 2                |
|    )               |    sec returns ... |  orch -> security      |
|                    |    orch asks perf  |  "Reviewing security"  |
|                    |    perf returns ...|                        |
|                    |    ...             |  Step 3                |
|                    |                    |  security -> orch      |
|                    |                    |  "2 findings"          |
+------------------------------------------------------------------+
|  FINDINGS PANEL                                                   |
|  [Security: 2]  [Performance: 1]  [Quality: 1]  [All: 4]        |
|                                                                   |
|  CRITICAL  SQL Injection in transfer()                           |
|  Line 4: Raw string interpolation in SQL query. Use parameterized|
|  queries to prevent injection attacks.                            |
|                                                                   |
|  WARNING   Missing input validation                               |
|  No bounds checking on amount parameter. Negative values allowed. |
+------------------------------------------------------------------+
```

**Layout Details:**

- **Top bar:** Title, mode selector (Demo/Live), Review button (green), Break button (red), status indicator
- **Main area:** 3-column grid (code input | protocol | agent activity)
  - Code input: Monaco editor, EDITABLE, with sample vulnerable code pre-loaded
  - Protocol: Monaco editor, read-only, CodeReview.lu with line highlighting
  - Agent activity: Chat log (same style as Debugger) with role-colored messages
- **Bottom panel:** Findings summary with tabs per reviewer + "All" tab
  - Each finding has severity pill (Critical=red, Warning=yellow, Info=blue)
  - Findings animate in as they arrive via SSE

**Responsive:** On mobile, stack vertically: Code > Agent Activity > Findings. Protocol hidden behind a toggle.

### Demo Scenarios

**Scenario 1: Happy Path -- All Clear**

Pre-loaded code: simple, clean Python function
```python
def greet(name: str) -> str:
    """Return a greeting message."""
    if not name or not name.strip():
        return "Hello, stranger!"
    return f"Hello, {name.strip()}!"
```

Steps:
1. developer -> orchestrator: "Submitted 5 lines of Python for review"
2. orchestrator -> security: "Review this code for security vulnerabilities"
3. security -> orchestrator: "[INFO] No issues found. Input is sanitized, no SQL/XSS vectors."
4. orchestrator -> performance: "Review this code for performance issues"
5. performance -> orchestrator: "[INFO] O(1) complexity. No concerns."
6. orchestrator -> quality: "Review this code for quality issues"
7. quality -> orchestrator: "[INFO] Clean code. Good docstring, type hints, edge case handling."
8. CHOICE: all_clear
9. orchestrator -> developer: "All clear. 3 reviewers, 0 issues. Code is production-ready."

Findings: 3 INFO (one per reviewer, all clean).

**Scenario 2: Happy Path -- Critical Found**

Pre-loaded code: vulnerable Python with SQL injection
```python
def transfer(amount, from_acct, to_acct):
    db.execute(f"UPDATE accounts SET balance = balance - {amount} WHERE id = {from_acct}")
    db.execute(f"UPDATE accounts SET balance = balance + {amount} WHERE id = {to_acct}")
    return {"status": "ok"}
```

Steps:
1. developer -> orchestrator: "Submitted 4 lines of Python for review"
2. orchestrator -> security: "Review this code for security vulnerabilities"
3. security -> orchestrator: "[CRITICAL] SQL Injection: raw f-string in SQL. [WARNING] No auth check."
4. orchestrator -> performance: "Review this code for performance issues"
5. performance -> orchestrator: "[WARNING] No transaction wrapping -- partial transfer possible on failure."
6. orchestrator -> quality: "Review this code for quality issues"
7. quality -> orchestrator: "[WARNING] No type hints. [INFO] Missing docstring."
8. CHOICE: critical_found
9. orchestrator -> developer: "URGENT: 1 critical, 3 warnings, 1 info. Security review found SQL injection."

Findings: 1 CRITICAL (SQL injection), 3 WARNING (no auth, no transaction, no types), 1 INFO (docstring).

**Scenario 3: Violation -- Quality Skips Ahead**

Same vulnerable code as Scenario 2.

Steps:
1. developer -> orchestrator: "Submitted 4 lines of Python for review"
2. orchestrator -> security: "Review this code for security vulnerabilities"
3. INFO: "Quality reviewer tries to skip ahead and submit findings before Security completes..."
4. VIOLATION: quality -> orchestrator: TaskResult
   - Expected: security -> orchestrator: TaskResult (security findings)
   - Got: quality -> orchestrator: TaskResult (quality findings)
   - Error: "ProtocolViolation: Quality cannot review before Security completes. The session type makes this IMPOSSIBLE -- not by convention, by mathematical proof. Why? No point polishing code with SQL injection."

This scenario is compelling because the WHY is obvious: why would you fix naming conventions when the code has a SQL injection vulnerability?

### Dependencies

```
# requirements.txt (identical to Debugger)
fastapi>=0.115.0
uvicorn[standard]>=0.30.0
slowapi>=0.1.9
anthropic>=0.40.0
cervellaswarm-lingua-universale>=0.3.3
```

### Deployment

```toml
# fly.toml
app = 'lu-code-review'
primary_region = 'fra'

[build]

[http_service]
  internal_port = 8000
  force_https = true
  auto_stop_machines = 'stop'
  auto_start_machines = true
  min_machines_running = 0
  processes = ['app']

[[vm]]
  cpu_kind = 'shared'
  cpus = 1
  memory_mb = 1024
```

Deploy commands (same as Debugger):
```bash
cd code-review
fly apps create lu-code-review
fly secrets set ANTHROPIC_API_KEY=sk-...
fly deploy
```

### LOC Estimates

| File | Estimated LOC | Notes |
|------|--------------|-------|
| `server.py` | ~190 | Same as Debugger + POST endpoints for live mode |
| `runner.py` | ~450 | 5 agents instead of 3, finding extraction, code input |
| `demo_data.py` | ~280 | 3 scenarios (all_clear + critical + break), longer protocol |
| `static/index.html` | ~1100 | 3-column layout, findings panel, 5 role colors, Monaco x2 |
| `Dockerfile` | 5 | Identical |
| `fly.toml` | 18 | App name change |
| `requirements.txt` | 5 | Identical |
| **Total** | **~2050** | |

---

## Phase 3: Review

### Assumptions Validated

- [x] SessionChecker enforces step ordering sequentially (confirmed by reading checker.py)
- [x] ProtocolViolation is raised when sender/receiver/kind mismatch (confirmed in _validate_next_step)
- [x] `before` property uses MessageKind values, not role names (confirmed in spec.py)
- [x] TaskRequest and TaskResult are the correct types for orchestrator-reviewer exchange
- [x] DirectMessage is the correct type for developer-orchestrator exchange
- [x] Catppuccin Mocha palette is used in Incident + Zoo (confirmed CSS variables)
- [x] Fly.io Frankfurt with auto_stop_machines works (proven by Debugger)

### Risks

| Risk | Mitigation |
|------|------------|
| Live mode costs | Haiku at ~$0.000005/run, same as Debugger. 5 agents = ~$0.000025/run. Still negligible. |
| User code injection in prompts | Max 2000 chars, strip HTML/script tags, same pattern as any LLM app. Code is sent as user message, not system. |
| Claude returns inconsistent finding format | Robust regex parsing in runner.py. If parsing fails, show raw response. Demo mode is always reliable. |
| 3-column layout too cramped | Protocol column hides on mobile. Toggle button. Falls back to 2-column at 1024px. |
| Session takes too long (5 API calls) | Parallel is NOT possible (protocol enforces sequence). But each call is ~1s with Haiku. Total ~5s. Acceptable for SSE streaming. |

### Design Decisions

1. **POST for live mode (not GET):** User code needs to be sent to the server. GET endpoints don't have a body. Query param for code is too long and leaks in logs. POST is correct.

2. **Findings as separate SSE events:** The `finding` event type lets the UI build the findings panel incrementally. Each reviewer's `agent_message` contains the full text; findings are extracted and sent as structured events immediately after.

3. **3 demo scenarios (not 2):** The Debugger had 2 (happy + break). We add a third: "critical_found" path. This shows the choice/branching in action -- orchestrator decides between `critical_found` and `all_clear` based on findings.

4. **Editable Monaco for code input:** Unlike the Debugger where the protocol editor is read-only, here the code editor is editable. The user PASTES their code. A default vulnerable snippet is pre-loaded for first-time visitors.

5. **No "Live Break" initially:** The violation demo is most compelling with pre-scripted content where we control the narrative. Live break requires running 1 real API call then forcing a violation -- same pattern as Debugger. Include it but it is lower priority than the demo break.

---

## Phase 4: Final Plan

### File Structure

```
code-review/
  server.py          # FastAPI + SSE + rate limiting
  runner.py           # Async Claude API agents + SessionChecker
  demo_data.py        # Protocol source + 3 pre-scripted scenarios
  static/
    index.html        # Dual Monaco + agent panel + findings UI
  Dockerfile          # Python 3.12-slim + uvicorn
  fly.toml            # Fly.io Frankfurt config
  requirements.txt    # FastAPI, anthropic, LU
```

### Execution Order

| Step | Task | Files | Worker | Why This Order |
|------|------|-------|--------|----------------|
| 1 | Write protocol + demo data | `demo_data.py` | backend | Foundation. Everything depends on the protocol source and pre-scripted scenarios. |
| 2 | Write runner (agents + checker) | `runner.py` | backend | Depends on demo_data for protocol source. Core logic. |
| 3 | Write server (endpoints + SSE) | `server.py` | backend | Depends on runner for generator functions. Thin layer. |
| 4 | Write UI (HTML + CSS + JS) | `static/index.html` | frontend | Depends on knowing SSE event shapes from steps 1-3. |
| 5 | Write deploy files | `Dockerfile`, `fly.toml`, `requirements.txt` | backend | Copy from Debugger, change app name. |
| 6 | Local test | all | tester | `uvicorn server:app --reload`, test all 3 demo scenarios + violation. |
| 7 | Deploy to Fly.io | infra | devops | `fly deploy`, set ANTHROPIC_API_KEY secret. |
| 8 | Guardiana audit | all | guardiana | Audit against success criteria. Fix P1/P2. |

### Success Criteria

- [ ] Demo happy path (all_clear) runs end-to-end, all 9 steps visible in UI
- [ ] Demo happy path (critical_found) runs end-to-end, choice branch visible
- [ ] Demo violation shows ProtocolViolation with expected/got, shake animation, red highlight on protocol line
- [ ] Protocol displayed in Monaco with LU syntax highlighting (same tokenizer as Debugger)
- [ ] Code editor is editable, default vulnerable code pre-loaded
- [ ] Findings panel shows categorized findings with severity pills
- [ ] 5 role colors visually distinct in Catppuccin Mocha palette
- [ ] Live mode works with real Claude Haiku API calls when ANTHROPIC_API_KEY set
- [ ] Rate limiting active (10/min demo, 3/min live)
- [ ] Deploys to Fly.io Frankfurt, auto_stop_machines enabled
- [ ] Responsive: works on mobile (3-col -> stacked)
- [ ] Accessible: ARIA labels, prefers-reduced-motion, semantic HTML

### Role Color Assignment (Catppuccin Mocha)

| Role | Color | Hex | Rationale |
|------|-------|-----|-----------|
| developer | Blue | `#89b4fa` | User/initiator (blue = primary action) |
| orchestrator | Violet | `#cba6f7` | Coordinator (distinct, prominent) |
| security | Red | `#f38ba8` | Security = red (universal convention) |
| performance | Yellow | `#f9e2af` | Performance = speed = warm |
| quality | Teal | `#94e2d5` | Quality = clean = cool |

### What Makes This UNIQUE vs Existing Code Review Tools

1. **VERIFIED ordering** -- Not "security should run first" (convention). "Security MUST run first" (mathematical proof). Try to skip it? BLOCKED. Not by a rule engine. By session type theory.

2. **Visible enforcement** -- Users SEE the protocol, SEE each step, SEE the violation. No black box. The protocol source is displayed and lines highlight as agents communicate.

3. **Real AI agents, real protocol** -- This is not a mockup. Claude Haiku actually analyzes the code. The SessionChecker actually blocks violations. Both are REAL.

4. **Choice/branching** -- The orchestrator DECIDES based on findings (critical_found vs all_clear). This is a real protocol feature, not hardcoded logic.

5. **Educational** -- Users learn WHY ordering matters in code review. Security before performance is not arbitrary -- it is a best practice encoded as a guarantee.

6. **Cost** -- ~$0.000025/run with Haiku. Users can run it all day. This makes it a real tool, not a demo that breaks the bank.

### Estimated Effort

- **Session 1:** Steps 1-5 (backend + deploy files). ~2 hours. Proven pattern.
- **Session 2:** Steps 4-8 (UI + local test + deploy + audit). ~2 hours. UI is the most work.
- **Optimistic:** 1 session if the Debugger developer does both backend and frontend (proven in S458).

---

## Appendix: Sample Vulnerable Code for Default Editor

```python
import sqlite3

def transfer_funds(amount, from_account, to_account):
    conn = sqlite3.connect("bank.db")
    # BUG: SQL injection via string interpolation
    conn.execute(f"UPDATE accounts SET balance = balance - {amount} WHERE id = '{from_account}'")
    conn.execute(f"UPDATE accounts SET balance = balance + {amount} WHERE id = '{to_account}'")
    conn.commit()
    # BUG: No transaction -- partial transfer on crash
    # BUG: No auth check -- anyone can transfer
    # BUG: No input validation -- negative amounts?
    return {"status": "ok", "amount": amount}

def get_user(user_id):
    conn = sqlite3.connect("bank.db")
    # BUG: SQL injection
    result = conn.execute(f"SELECT * FROM users WHERE id = {user_id}")
    return result.fetchone()
```

This code has deliberate vulnerabilities that each reviewer will find:
- **Security:** SQL injection (2 locations), no auth check
- **Performance:** No connection pooling, no transaction wrapping
- **Quality:** No type hints, no docstrings, no error handling, hardcoded DB path

---

**Status**: PLAN_READY -- Awaiting approval to proceed with implementation.

COSTITUZIONE-APPLIED: SI | Principio: "Ricerca PRIMA di implementare"
