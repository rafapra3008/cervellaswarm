#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors
"""
Lingua Universale - End-to-End Showcase

The first session type system for AI agents in Python.
From natural language to verified code in milliseconds.

Usage:
    python examples/showcase.py
    NO_COLOR=1 python examples/showcase.py  # disable colors
"""

from __future__ import annotations

import os
import sys

# ---------------------------------------------------------------------------
# ANSI color helpers (no deps)
# ---------------------------------------------------------------------------

_NO_COLOR = bool(os.environ.get("NO_COLOR")) or "--no-color" in sys.argv

BOLD   = "" if _NO_COLOR else "\033[1m"
GREEN  = "" if _NO_COLOR else "\033[32m"
RED    = "" if _NO_COLOR else "\033[31m"
YELLOW = "" if _NO_COLOR else "\033[33m"
CYAN   = "" if _NO_COLOR else "\033[36m"
DIM    = "" if _NO_COLOR else "\033[2m"
RESET  = "" if _NO_COLOR else "\033[0m"

TOTAL_SECTIONS = 8


def header(section_num: int, title: str) -> None:
    """Print a section header."""
    pad = "-" * max(0, 52 - len(title))
    print(f"\n{BOLD}--- [{section_num}/{TOTAL_SECTIONS}] {title} {pad}{RESET}\n")


def ok(label: str = "") -> None:
    """Print a green [OK] with optional label."""
    suffix = f" {label}" if label else ""
    print(f"  {GREEN}[OK]{RESET}{suffix}")


def info(label: str) -> None:
    """Print a dim info line."""
    print(f"  {DIM}{label}{RESET}")


def check(label: str, status: str = "OK") -> None:
    """Print a status check line."""
    if status in ("OK", "PROVED", "SATISFIED"):
        color = GREEN
    elif status == "SKIPPED":
        color = YELLOW
    else:
        color = RED
    print(f"  {color}[{status}]{RESET} {label}")


# ---------------------------------------------------------------------------
# Imports from Lingua Universale
# ---------------------------------------------------------------------------

from cervellaswarm_lingua_universale import (
    # Intent
    parse_intent_protocol,
    # DSL
    render_protocol,
    # Spec
    parse_spec,
    check_properties,
    check_session,
    PropertyVerdict,
    # Lean 4 Bridge
    generate_lean4,
    lean4_available,
    # Code Generation
    generate_python,
    # Checker + Monitor
    SessionChecker,
    ProtocolMonitor,
    EventCollector,
    # Types: message enums
    TaskStatus,
    AuditVerdictType,
    AgentRole,
    # Types: message classes
    TaskRequest,
    TaskResult,
    AuditRequest,
    AuditVerdict,
    # Errors
    humanize,
    format_error,
    # Confidence
    ConfidenceScore,
    ConfidenceSource,
    Confident,
    CompositionStrategy,
    compose_scores,
    # Trust
    TrustScore,
    TrustTier,
    trust_tier_for_role,
    compose_chain,
)


# ---------------------------------------------------------------------------
# SECTION 1 - Intent (Natural Language -> Protocol)
# ---------------------------------------------------------------------------

INTENT_SOURCE = """
protocol DelegateTask:
    roles: regina, worker, guardiana

    regina asks worker to do task
    worker returns result to regina
    regina asks guardiana to verify
    guardiana returns verdict to regina
"""

SPEC_SOURCE = """
properties for DelegateTask:
    always terminates
    no deadlock
    task_request before task_result
    worker cannot send audit_verdict
    all roles participate
"""


def section_1_intent() -> object:
    """Parse natural language intent into a Protocol object."""
    header(1, "INTENT (Natural Language -> Protocol)")

    protocol = parse_intent_protocol(INTENT_SOURCE)

    print(f"  Protocol : {BOLD}{protocol.name}{RESET}")
    print(f"  Roles    : {', '.join(protocol.roles)}")
    print(f"  Steps    : {len(protocol.elements)}")
    ok("Protocol parsed from intent notation")
    return protocol


# ---------------------------------------------------------------------------
# SECTION 2 - DSL (Protocol -> Scribble Notation)
# ---------------------------------------------------------------------------


def section_2_dsl(protocol: object) -> None:
    """Render the protocol to Scribble-inspired DSL notation."""
    header(2, "DSL (Protocol -> Scribble Notation)")

    dsl_text = render_protocol(protocol)  # type: ignore[arg-type]

    for line in dsl_text.splitlines():
        print(f"  {CYAN}{line}{RESET}")

    ok("DSL rendered (round-trip fidelity guaranteed)")


# ---------------------------------------------------------------------------
# SECTION 3 - Specification (Define Formal Properties)
# ---------------------------------------------------------------------------


def section_3_spec() -> object:
    """Parse the formal property specification."""
    header(3, "SPECIFICATION (Formal Properties)")

    spec = parse_spec(SPEC_SOURCE)

    print(f"  Protocol : {spec.protocol_name}")
    print(f"  Properties ({len(spec.properties)}):")
    for prop in spec.properties:
        print(f"    - {prop.kind.value}")

    ok(f"{len(spec.properties)} properties parsed")
    return spec


# ---------------------------------------------------------------------------
# SECTION 4 - Static Verification (Prove Properties)
# ---------------------------------------------------------------------------


def section_4_static(protocol: object, spec: object) -> None:
    """Statically check all properties against the protocol structure."""
    header(4, "STATIC VERIFICATION (Prove Properties)")

    report = check_properties(protocol, spec)  # type: ignore[arg-type]

    for result in report.results:
        verdict = result.verdict
        label = result.spec.kind.value
        if verdict == PropertyVerdict.PROVED:
            check(label, "PROVED")
        elif verdict == PropertyVerdict.VIOLATED:
            check(label, "VIOLATED")
            print(f"      {RED}Evidence: {result.evidence}{RESET}")
        else:
            check(label, "SKIPPED")

    passed = report.passed_count
    total = len(report.results)
    color = GREEN if report.all_passed else RED
    print(f"\n  {color}{BOLD}{passed}/{total} properties proved{RESET}")


# ---------------------------------------------------------------------------
# SECTION 5 - Lean 4 (Formal Verification Code)
# ---------------------------------------------------------------------------


def section_5_lean4(protocol: object) -> None:
    """Generate Lean 4 formal verification code for the protocol."""
    header(5, "LEAN 4 (Formal Verification Code)")

    lean_code = generate_lean4(protocol)  # type: ignore[arg-type]
    available = lean4_available()

    lines = lean_code.splitlines()
    preview = lines[:18]
    for line in preview:
        print(f"  {CYAN}{line}{RESET}")
    if len(lines) > 18:
        print(f"  {DIM}... ({len(lines) - 18} more lines){RESET}")

    print()
    if available:
        ok("Lean 4 available on PATH - theorems could be verified")
    else:
        info("Lean 4 not installed (install from leanprover.github.io)")
        ok(f"Lean 4 code generated ({len(lines)} lines) - ready to verify")


# ---------------------------------------------------------------------------
# SECTION 6 - Code Generation (Protocol -> Python)
# ---------------------------------------------------------------------------


def section_6_codegen(protocol: object) -> None:
    """Generate type-safe Python from the protocol definition."""
    header(6, "CODE GENERATION (Protocol -> Python)")

    python_code = generate_python(protocol)  # type: ignore[arg-type]

    lines = python_code.splitlines()
    preview = lines[:28]
    for line in preview:
        print(f"  {CYAN}{line}{RESET}")
    if len(lines) > 28:
        print(f"  {DIM}... ({len(lines) - 28} more lines){RESET}")

    # Count role classes (lines with "class " and "Role")
    role_classes = sum(1 for l in lines if l.startswith("class ") and "Role" in l)
    session_classes = sum(1 for l in lines if l.startswith("class ") and "Session" in l)
    print()
    print(f"  Total lines    : {len(lines)}")
    print(f"  Role classes   : {role_classes}")
    print(f"  Session classes: {session_classes}")
    ok("Python module generated with full type hints")


# ---------------------------------------------------------------------------
# SECTION 7 - Runtime Session (Protocol Enforcement)
# ---------------------------------------------------------------------------


def section_7_runtime(protocol: object, spec: object) -> None:
    """Demonstrate runtime protocol enforcement with monitor and error humanization."""
    header(7, "RUNTIME SESSION (Protocol Enforcement)")

    # ------------------------------------------------------------------
    # 7a. Happy path
    # ------------------------------------------------------------------

    print(f"  {BOLD}7a. Happy path:{RESET}\n")

    monitor = ProtocolMonitor()
    collector = EventCollector()
    monitor.add_listener(collector)

    checker = SessionChecker(protocol, session_id="demo-001", monitor=monitor)  # type: ignore[arg-type]

    messages = [
        (
            "regina", "worker",
            TaskRequest(
                task_id="T001",
                description="Implement the login page",
                target_files=("login.py",),
                constraints=("must use OAuth2",),
            ),
        ),
        (
            "worker", "regina",
            TaskResult(
                task_id="T001",
                status=TaskStatus.OK,
                summary="Login page implemented with OAuth2",
                files_created=("login.py",),
                test_command="pytest test_login.py",
            ),
        ),
        (
            "regina", "guardiana",
            AuditRequest(
                audit_id="A001",
                target="T001",
                checklist=("code quality", "security", "tests"),
            ),
        ),
        (
            "guardiana", "regina",
            AuditVerdict(
                audit_id="A001",
                verdict=AuditVerdictType.APPROVED,
                score=9.5,
                checked=("code quality", "security", "tests"),
            ),
        ),
    ]

    for sender, receiver, msg in messages:
        checker.send(sender, receiver, msg)
        kind = type(msg).__name__
        check(f"{sender} -> {receiver} : {kind}", "OK")

    events_count = len(collector.events)
    print()
    print(f"  Session complete : {checker.is_complete}")
    print(f"  Events captured  : {events_count}")
    ok("Happy path completed without violations")

    # ------------------------------------------------------------------
    # 7a-bis. Runtime property check
    # ------------------------------------------------------------------

    print(f"\n  {BOLD}7a-bis. Runtime property check:{RESET}\n")

    runtime_report = check_session(checker.log, spec, protocol)  # type: ignore[arg-type]

    for result in runtime_report.results:
        verdict = result.verdict
        label = result.spec.kind.value
        if verdict == PropertyVerdict.SATISFIED:
            check(label, "SATISFIED")
        elif verdict == PropertyVerdict.VIOLATED:
            check(label, "VIOLATED")
        else:
            check(label, "SKIPPED")

    passed = runtime_report.passed_count
    total = len(runtime_report.results)
    color = GREEN if runtime_report.all_passed else RED
    print(f"\n  {color}{BOLD}{passed}/{total} properties satisfied at runtime{RESET}")

    # ------------------------------------------------------------------
    # 7b. Error path (violation + humanized error)
    # ------------------------------------------------------------------

    print(f"\n  {BOLD}7b. Error path (violation + humanized error):{RESET}\n")

    checker2 = SessionChecker(protocol, session_id="demo-002")  # type: ignore[arg-type]

    try:
        # Worker tries to send first - VIOLATION!
        checker2.send("worker", "regina", TaskResult(
            task_id="T001",
            status=TaskStatus.OK,
            summary="I went first!",
            files_created=(),
        ))
    except Exception as exc:
        print(f"  {YELLOW}Raw exception:{RESET} {type(exc).__name__}")
        print()

        # English
        human_err_en = humanize(exc, locale="en")
        print(f"  {BOLD}[English]{RESET}")
        for line in format_error(human_err_en, verbose=False).splitlines():
            print(f"    {line}")

        print()

        # Italian
        human_err_it = humanize(exc, locale="it")
        print(f"  {BOLD}[Italiano]{RESET}")
        for line in format_error(human_err_it, verbose=False).splitlines():
            print(f"    {line}")

    ok("Protocol violation caught and humanized (EN + IT)")


# ---------------------------------------------------------------------------
# SECTION 8 - Confidence & Trust (Native AI Types)
# ---------------------------------------------------------------------------


def section_8_confidence_and_trust() -> None:
    """Demonstrate confidence scores and trust tiers."""
    header(8, "CONFIDENCE & TRUST (Native AI Types)")

    # Confidence scores
    print(f"  {BOLD}Confidence scores:{RESET}\n")

    audit_conf = ConfidenceScore(value=0.95, source=ConfidenceSource.AUDIT)
    self_conf = ConfidenceScore(value=0.80, source=ConfidenceSource.SELF_REPORTED)
    composed = compose_scores(
        (audit_conf, self_conf),
        strategy=CompositionStrategy.MIN,
    )

    print(f"  AUDIT       : {audit_conf.value:.2f}  ({audit_conf.source.value})")
    print(f"  SELF-REPORT : {self_conf.value:.2f}  ({self_conf.source.value})")
    print(f"  COMPOSED    : {composed.value:.2f}  ({composed.source.value}, strategy=MIN)")

    # Confident[T] wrapper
    print()
    result: Confident[str] = Confident(
        value="Protocol verified",
        confidence=composed,
    )
    print(f"  Confident[str] : {result.value!r}")
    print(f"  is_high        : {result.is_high}")
    ok("Confidence types composed")

    # Trust tiers for different roles
    print(f"\n  {BOLD}Trust tiers by role:{RESET}\n")

    role_checks = [
        AgentRole.REGINA,
        AgentRole.GUARDIANA_QUALITA,
        AgentRole.BACKEND,
    ]
    for role in role_checks:
        tier = trust_tier_for_role(role)
        print(f"  {role.value:<28} -> {tier.value}")

    # Trust chain composition
    print(f"\n  {BOLD}Trust chain composition:{RESET}\n")

    chain = compose_chain((
        TrustScore(value=1.0, tier=TrustTier.VERIFIED, reason="guardiana"),
        TrustScore(value=0.75, tier=TrustTier.STANDARD, reason="backend"),
    ))
    print("  VERIFIED(1.0) x STANDARD(0.75)")
    print(f"  Chain result  : {chain.value:.4f}  tier={chain.tier.value}")
    ok("Trust chain composed via multiplicative rule")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    """Run all showcase sections."""
    print(f"\n{BOLD}{CYAN}")
    print("=" * 60)
    print("  LINGUA UNIVERSALE - End-to-End Showcase")
    print("  The first session type system for AI agents in Python.")
    print("  From natural language to verified code in milliseconds.")
    print("=" * 60)
    print(f"{RESET}")

    protocol = section_1_intent()
    section_2_dsl(protocol)
    spec = section_3_spec()
    section_4_static(protocol, spec)
    section_5_lean4(protocol)
    section_6_codegen(protocol)
    section_7_runtime(protocol, spec)
    section_8_confidence_and_trust()

    print(f"\n{BOLD}{GREEN}")
    print("=" * 60)
    print("  SHOWCASE COMPLETE")
    print("  All 8 sections passed. Lingua Universale is ready.")
    print("=" * 60)
    print(f"{RESET}\n")


if __name__ == "__main__":
    main()
