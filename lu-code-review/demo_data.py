# SPDX-License-Identifier: Apache-2.0
"""Pre-scripted demo data for the AI Code Review showcase.

Three scenarios:
1. All clear: clean code, no critical issues, orchestrator -> all_clear branch
2. Critical: vulnerable code with SQL injection, orchestrator -> critical_found branch
3. Break: quality tries to review before security finishes -> BLOCKED
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Protocol source -- displayed in the read-only Monaco editor
# ---------------------------------------------------------------------------

PROTOCOL_SOURCE = """\
# SPDX-License-Identifier: Apache-2.0
# Code Review Protocol -- AI Code Review Demo
#
# Four AI agents review code in enforced order:
# Security MUST complete before Performance starts.
# Performance MUST complete before Quality starts.
# Why? No point optimizing insecure code.

type ReviewSeverity = Critical | Warning | Info

type CodeSubmission =
    language: String
    source: String
    filename: String

type ReviewFinding =
    category: String
    severity: ReviewSeverity
    line: Number
    message: String
    suggestion: String

type ReviewReport =
    total_findings: Number
    critical_count: Number
    summary: String

agent Developer:
    role: developer
    trust: standard
    accepts: ReviewReport
    produces: CodeSubmission
    requires: code.valid
    ensures: code.submitted

agent SecurityReviewer:
    role: security
    trust: verified
    accepts: CodeSubmission
    produces: ReviewFinding
    requires: code.received
    ensures: security.reviewed

agent PerformanceReviewer:
    role: performance
    trust: trusted
    accepts: CodeSubmission
    produces: ReviewFinding
    requires: security.cleared
    ensures: performance.reviewed

agent QualityReviewer:
    role: quality
    trust: trusted
    accepts: CodeSubmission
    produces: ReviewFinding
    requires: performance.done
    ensures: quality.reviewed

agent Orchestrator:
    role: orchestrator
    trust: verified
    accepts: ReviewFinding, CodeSubmission
    produces: ReviewReport, CodeSubmission
    requires: reviews.collected
    ensures: report.generated

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
        security before performance
        performance before quality
"""

# Protocol line numbers (1-indexed, matching PROTOCOL_SOURCE)
LINE = {
    "dev_sends": 71,
    "orch_asks_sec": 72,
    "sec_returns": 73,
    "orch_asks_perf": 74,
    "perf_returns": 75,
    "orch_asks_qual": 76,
    "qual_returns": 77,
    "choice": 79,
    "critical_found": 80,
    "orch_sends_urgent": 81,
    "all_clear": 82,
    "orch_sends_clean": 83,
}

# ---------------------------------------------------------------------------
# Sample code snippets
# ---------------------------------------------------------------------------

SAMPLE_CLEAN = """\
def greet(name: str) -> str:
    \"\"\"Return a greeting message.\"\"\"
    if not name or not name.strip():
        return "Hello, stranger!"
    return f"Hello, {name.strip()}!"
"""

SAMPLE_VULNERABLE = """\
import sqlite3

def transfer_funds(amount, from_account, to_account):
    conn = sqlite3.connect("bank.db")
    conn.execute(f"UPDATE accounts SET balance = balance - {amount} WHERE id = '{from_account}'")
    conn.execute(f"UPDATE accounts SET balance = balance + {amount} WHERE id = '{to_account}'")
    conn.commit()
    return {"status": "ok", "amount": amount}

def get_user(user_id):
    conn = sqlite3.connect("bank.db")
    result = conn.execute(f"SELECT * FROM users WHERE id = {user_id}")
    return result.fetchone()
"""

# ---------------------------------------------------------------------------
# Scenario 1: All Clear (clean code)
# ---------------------------------------------------------------------------

DEMO_ALL_CLEAR: list[dict] = [
    {
        "type": "agent_message",
        "step": 1,
        "from": "developer",
        "to": "orchestrator",
        "message_type": "DirectMessage",
        "content": "Submitted 5 lines of Python for review: greet() function.",
        "protocol_line": LINE["dev_sends"],
        "status": "ok",
        "delay": 0.6,
    },
    {
        "type": "agent_message",
        "step": 2,
        "from": "orchestrator",
        "to": "security",
        "message_type": "TaskRequest",
        "content": "Review this code for security vulnerabilities.",
        "protocol_line": LINE["orch_asks_sec"],
        "status": "ok",
        "delay": 0.8,
    },
    {
        "type": "agent_message",
        "step": 3,
        "from": "security",
        "to": "orchestrator",
        "message_type": "TaskResult",
        "content": "[INFO] No security issues found. Input is validated, no SQL/XSS vectors.",
        "protocol_line": LINE["sec_returns"],
        "status": "ok",
        "delay": 1.2,
    },
    {
        "type": "finding",
        "reviewer": "security",
        "severity": "info",
        "title": "No security issues",
        "detail": "Input validated with strip(). No SQL, XSS, or injection vectors.",
        "delay": 0.1,
    },
    {
        "type": "agent_message",
        "step": 4,
        "from": "orchestrator",
        "to": "performance",
        "message_type": "TaskRequest",
        "content": "Review this code for performance issues.",
        "protocol_line": LINE["orch_asks_perf"],
        "status": "ok",
        "delay": 0.8,
    },
    {
        "type": "agent_message",
        "step": 5,
        "from": "performance",
        "to": "orchestrator",
        "message_type": "TaskResult",
        "content": "[INFO] O(1) complexity. No performance concerns.",
        "protocol_line": LINE["perf_returns"],
        "status": "ok",
        "delay": 1.0,
    },
    {
        "type": "finding",
        "reviewer": "performance",
        "severity": "info",
        "title": "No performance issues",
        "detail": "O(1) string operations. No loops, no allocations.",
        "delay": 0.1,
    },
    {
        "type": "agent_message",
        "step": 6,
        "from": "orchestrator",
        "to": "quality",
        "message_type": "TaskRequest",
        "content": "Review this code for quality issues.",
        "protocol_line": LINE["orch_asks_qual"],
        "status": "ok",
        "delay": 0.8,
    },
    {
        "type": "agent_message",
        "step": 7,
        "from": "quality",
        "to": "orchestrator",
        "message_type": "TaskResult",
        "content": "[INFO] Clean code. Type hints, docstring, edge case handling all present.",
        "protocol_line": LINE["qual_returns"],
        "status": "ok",
        "delay": 1.0,
    },
    {
        "type": "finding",
        "reviewer": "quality",
        "severity": "info",
        "title": "Well-structured code",
        "detail": "Type hints, docstring, and edge case handling present. No issues.",
        "delay": 0.1,
    },
    {
        "type": "choice",
        "step": 8,
        "who": "orchestrator",
        "branch": "all_clear",
        "protocol_line": LINE["all_clear"],
        "delay": 0.6,
    },
    {
        "type": "agent_message",
        "step": 9,
        "from": "orchestrator",
        "to": "developer",
        "message_type": "DirectMessage",
        "content": "All clear. 3 reviewers, 0 issues. Code is production-ready.",
        "protocol_line": LINE["orch_sends_clean"],
        "status": "ok",
        "delay": 0.6,
    },
    {
        "type": "done",
        "completed": True,
        "messages": 9,
        "branch": "all_clear",
        "findings_count": {"critical": 0, "warning": 0, "info": 3},
        "delay": 0.3,
    },
]


# ---------------------------------------------------------------------------
# Scenario 2: Critical Found (vulnerable code)
# ---------------------------------------------------------------------------

DEMO_CRITICAL: list[dict] = [
    {
        "type": "agent_message",
        "step": 1,
        "from": "developer",
        "to": "orchestrator",
        "message_type": "DirectMessage",
        "content": "Submitted 13 lines of Python for review: transfer_funds() + get_user().",
        "protocol_line": LINE["dev_sends"],
        "status": "ok",
        "delay": 0.6,
    },
    {
        "type": "agent_message",
        "step": 2,
        "from": "orchestrator",
        "to": "security",
        "message_type": "TaskRequest",
        "content": "Review this code for security vulnerabilities.",
        "protocol_line": LINE["orch_asks_sec"],
        "status": "ok",
        "delay": 0.8,
    },
    {
        "type": "agent_message",
        "step": 3,
        "from": "security",
        "to": "orchestrator",
        "message_type": "TaskResult",
        "content": "[CRITICAL] SQL Injection: f-string in SQL at lines 5, 6, 12. [WARNING] No authentication check.",
        "protocol_line": LINE["sec_returns"],
        "status": "ok",
        "delay": 1.4,
    },
    {
        "type": "finding",
        "reviewer": "security",
        "severity": "critical",
        "title": "SQL Injection",
        "detail": "Raw f-string interpolation in SQL queries at lines 5, 6, and 12. Use parameterized queries.",
        "line": 5,
        "delay": 0.1,
    },
    {
        "type": "finding",
        "reviewer": "security",
        "severity": "warning",
        "title": "No authentication check",
        "detail": "transfer_funds() has no authorization. Any caller can transfer any amount.",
        "line": 3,
        "delay": 0.2,
    },
    {
        "type": "agent_message",
        "step": 4,
        "from": "orchestrator",
        "to": "performance",
        "message_type": "TaskRequest",
        "content": "Review this code for performance issues.",
        "protocol_line": LINE["orch_asks_perf"],
        "status": "ok",
        "delay": 0.8,
    },
    {
        "type": "agent_message",
        "step": 5,
        "from": "performance",
        "to": "orchestrator",
        "message_type": "TaskResult",
        "content": "[WARNING] No transaction wrapping. Partial transfer possible on crash. [INFO] New connection per call.",
        "protocol_line": LINE["perf_returns"],
        "status": "ok",
        "delay": 1.2,
    },
    {
        "type": "finding",
        "reviewer": "performance",
        "severity": "warning",
        "title": "No transaction wrapping",
        "detail": "Two separate execute() calls without transaction. Crash between them = partial transfer.",
        "line": 5,
        "delay": 0.1,
    },
    {
        "type": "finding",
        "reviewer": "performance",
        "severity": "info",
        "title": "No connection pooling",
        "detail": "sqlite3.connect() called per function. Use a connection pool for production.",
        "line": 4,
        "delay": 0.2,
    },
    {
        "type": "agent_message",
        "step": 6,
        "from": "orchestrator",
        "to": "quality",
        "message_type": "TaskRequest",
        "content": "Review this code for quality issues.",
        "protocol_line": LINE["orch_asks_qual"],
        "status": "ok",
        "delay": 0.8,
    },
    {
        "type": "agent_message",
        "step": 7,
        "from": "quality",
        "to": "orchestrator",
        "message_type": "TaskResult",
        "content": "[WARNING] No type hints. [INFO] Missing docstrings. [INFO] Hardcoded DB path.",
        "protocol_line": LINE["qual_returns"],
        "status": "ok",
        "delay": 1.0,
    },
    {
        "type": "finding",
        "reviewer": "quality",
        "severity": "warning",
        "title": "Missing type hints",
        "detail": "transfer_funds() and get_user() have no type annotations. Add type hints for clarity.",
        "line": 3,
        "delay": 0.1,
    },
    {
        "type": "finding",
        "reviewer": "quality",
        "severity": "info",
        "title": "Missing docstrings",
        "detail": "No docstrings on either function. Add purpose, parameters, and return type.",
        "line": 3,
        "delay": 0.1,
    },
    {
        "type": "finding",
        "reviewer": "quality",
        "severity": "info",
        "title": "Hardcoded database path",
        "detail": "\"bank.db\" hardcoded. Use configuration or environment variable.",
        "line": 4,
        "delay": 0.1,
    },
    {
        "type": "choice",
        "step": 8,
        "who": "orchestrator",
        "branch": "critical_found",
        "protocol_line": LINE["critical_found"],
        "delay": 0.6,
    },
    {
        "type": "agent_message",
        "step": 9,
        "from": "orchestrator",
        "to": "developer",
        "message_type": "DirectMessage",
        "content": "URGENT: 1 critical, 3 warnings, 3 info. SQL injection found -- fix before merge.",
        "protocol_line": LINE["orch_sends_urgent"],
        "status": "ok",
        "delay": 0.6,
    },
    {
        "type": "done",
        "completed": True,
        "messages": 9,
        "branch": "critical_found",
        "findings_count": {"critical": 1, "warning": 3, "info": 3},
        "delay": 0.3,
    },
]


# ---------------------------------------------------------------------------
# Scenario 3: Break -- Quality tries to skip Security
# ---------------------------------------------------------------------------

DEMO_BREAK: list[dict] = [
    {
        "type": "agent_message",
        "step": 1,
        "from": "developer",
        "to": "orchestrator",
        "message_type": "DirectMessage",
        "content": "Submitted 13 lines of Python for review: transfer_funds() + get_user().",
        "protocol_line": LINE["dev_sends"],
        "status": "ok",
        "delay": 0.6,
    },
    {
        "type": "agent_message",
        "step": 2,
        "from": "orchestrator",
        "to": "security",
        "message_type": "TaskRequest",
        "content": "Review this code for security vulnerabilities.",
        "protocol_line": LINE["orch_asks_sec"],
        "status": "ok",
        "delay": 0.8,
    },
    {
        "type": "info",
        "step": 3,
        "content": "Quality reviewer tries to submit findings before Security completes...",
        "delay": 1.2,
    },
    {
        "type": "violation",
        "step": 3,
        "from": "quality",
        "to": "orchestrator",
        "message_type": "TaskResult",
        "expected": "security \u2192 orchestrator: TaskResult (security findings)",
        "got": "quality \u2192 orchestrator: TaskResult (quality findings)",
        "protocol_line": LINE["sec_returns"],
        "error": "ProtocolViolation: Quality cannot review before Security completes. "
        "The session type makes this IMPOSSIBLE \u2014 not by convention, by mathematical "
        "proof. Why? No point polishing code with SQL injection.",
        "delay": 0.5,
    },
    {
        "type": "done",
        "completed": False,
        "blocked": True,
        "messages": 2,
        "delay": 0.3,
    },
]
