#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Live dogfood runner: real AI agents on a verified LU protocol.

Each agent is a Claude API call. The protocol (AgentOrchestration)
defines WHO sends WHAT to WHOM. The AI decides the CONTENT.
The SessionChecker validates every step at runtime.

    ANTHROPIC_API_KEY=sk-... python dogfood_runner_live.py

If no API key is set, falls back to mock responses (same protocol flow).
"""

from __future__ import annotations

import os
import re
from pathlib import Path

from cervellaswarm_lingua_universale._ast import ProtocolNode
from cervellaswarm_lingua_universale._eval import _protocol_node_to_runtime
from cervellaswarm_lingua_universale._parser import parse
from cervellaswarm_lingua_universale.checker import SessionChecker, ProtocolViolation
from cervellaswarm_lingua_universale.types import (
    TaskRequest,
    TaskResult,
    TaskStatus,
    DirectMessage,
    Broadcast,
)

LU_FILE = Path(__file__).parent / "dogfood_agent_orchestration.lu"

# ---------------------------------------------------------------------------
# Agent system prompts
# ---------------------------------------------------------------------------

_SYSTEM_PROMPTS: dict[str, str] = {
    "supervisor": (
        "You are a Supervisor agent in an AI orchestration system. "
        "You delegate analysis tasks and coordinate the team. "
        "Reply in 1 sentence, max 150 characters. Be specific."
    ),
    "worker": (
        "You are an Analysis Worker agent. You execute tasks assigned by the Supervisor. "
        "Perform the analysis and report results. "
        "Reply in 1 sentence, max 150 characters. Include specific findings."
    ),
    "validator": (
        "You are a Quality Validator agent. You verify analysis results for correctness. "
        "Evaluate critically. Start your reply with exactly PASS or FAIL. "
        "Reply in 1 sentence, max 150 characters."
    ),
}

# ---------------------------------------------------------------------------
# AI Agent wrapper
# ---------------------------------------------------------------------------


class Agent:
    """Wraps a Claude API call as a protocol participant."""

    def __init__(self, role: str, *, client: object | None = None, model: str = "claude-haiku-4-5-20251001") -> None:
        self.role = role
        self._client = client
        self._model = model

    @property
    def is_live(self) -> bool:
        """True when backed by a real API client."""
        return self._client is not None

    def think(self, context: str) -> str:
        """Ask the AI agent to produce a response given context."""
        if self._client is None:
            return self._mock_response(context)

        try:
            response = self._client.messages.create(
                model=self._model,
                max_tokens=150,
                system=_SYSTEM_PROMPTS[self.role],
                messages=[{"role": "user", "content": context}],
                timeout=30,
            )
        except Exception as exc:
            print(f"  [API error for {self.role}: {exc}]")
            return self._mock_response(context)

        if not response.content or not hasattr(response.content[0], "text"):
            return self._mock_response(context)
        text = response.content[0].text.strip()
        # Protocol types enforce max 200 chars on summaries
        if len(text) > 190:
            text = text[:187] + "..."
        return text

    def _mock_response(self, context: str) -> str:
        """Fallback when no API key is available."""
        mocks = {
            "supervisor": "Analyze Q1 revenue data for anomalies and trends.",
            "worker": "Analysis complete: Q1 revenue up 12%, no anomalies detected in 847 transactions.",
            "validator": "PASS",
        }
        return mocks.get(self.role, "OK")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _sep(title: str) -> None:
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}")


def _build_checker(session_id: str) -> SessionChecker:
    source = LU_FILE.read_text()
    program = parse(source)
    protocol_node = next(
        d for d in program.declarations if isinstance(d, ProtocolNode)
    )
    protocol = _protocol_node_to_runtime(protocol_node)
    return SessionChecker(protocol, session_id=session_id)


# ---------------------------------------------------------------------------
# Live orchestration
# ---------------------------------------------------------------------------


def run_live(agents: dict[str, Agent]) -> None:
    """Run the AgentOrchestration protocol with live AI agents."""
    checker = _build_checker("live-session")

    _sep("LIVE ORCHESTRATION")
    mode = "LIVE (Claude API)" if agents["supervisor"].is_live else "MOCK (no API key)"
    print(f"Mode: {mode}")
    print(f"Protocol: {checker.protocol_name}")
    print()

    # --- Step 1: Supervisor creates task for worker ---
    task_desc = agents["supervisor"].think(
        "You need to delegate an analysis task to your worker. "
        "What specific analysis should they perform? (1-2 sentences)"
    )
    print(f"[supervisor thinks] {task_desc}")

    checker.send(
        "supervisor", "worker",
        TaskRequest(task_id="live-001", description=task_desc),
    )
    print("[1] supervisor -> worker: TASK_REQUEST")
    print(f"    {task_desc}")
    print()

    # --- Step 2: Worker executes and returns result ---
    result_text = agents["worker"].think(
        f"The supervisor has asked you to: {task_desc}\n"
        "Execute the analysis and report your findings. (1-2 sentences)"
    )
    print(f"[worker thinks] {result_text}")

    checker.send(
        "worker", "supervisor",
        TaskResult(task_id="live-001", status=TaskStatus.OK, summary=result_text),
    )
    print("[2] worker -> supervisor: TASK_RESULT")
    print(f"    {result_text}")
    print()

    # --- Step 3: Supervisor forwards to validator ---
    verify_desc = agents["supervisor"].think(
        f"Your worker returned: '{result_text}'\n"
        "Ask the validator to verify this result. (1 sentence)"
    )
    print(f"[supervisor thinks] {verify_desc}")

    checker.send(
        "supervisor", "validator",
        TaskRequest(task_id="verify-001", description=verify_desc),
    )
    print("[3] supervisor -> validator: TASK_REQUEST")
    print(f"    {verify_desc}")
    print()

    # --- Step 4: Validator decides PASS or FAIL ---
    verdict_text = agents["validator"].think(
        f"The worker's analysis result was: '{result_text}'\n"
        f"The supervisor asked you to: '{verify_desc}'\n"
        f"Evaluate the quality. Reply with exactly PASS or FAIL, then a brief reason."
    )
    print(f"[validator thinks] {verdict_text}")

    has_fail = bool(re.search(r"\bFAIL\b", verdict_text, re.IGNORECASE))
    has_pass = bool(re.search(r"\bPASS\b", verdict_text, re.IGNORECASE))
    passed = has_pass and not has_fail
    branch = "pass" if passed else "fail"
    checker.choose_branch(branch)
    print(f"[4] validator decides: {branch}")
    print()

    if passed:
        # --- Pass branch: validator sends approval ---
        checker.send(
            "validator", "supervisor",
            TaskResult(
                task_id="verify-001",
                status=TaskStatus.OK,
                summary=verdict_text,
            ),
        )
        print("[5] validator -> supervisor: APPROVAL")
        print(f"    {verdict_text}")
    else:
        # --- Fail branch: validator feedback + supervisor revises ---
        feedback = agents["validator"].think(
            f"You rejected the work: '{verdict_text}'\n"
            "Give specific feedback on what needs to be fixed. (1 sentence)"
        )
        checker.send(
            "validator", "supervisor",
            DirectMessage(sender_role="validator", content=feedback),
        )
        print("[5] validator -> supervisor: FEEDBACK")
        print(f"    {feedback}")

        revision = agents["supervisor"].think(
            f"Validator rejected with feedback: '{feedback}'\n"
            "Tell the worker what to revise. (1 sentence)"
        )
        checker.send(
            "supervisor", "worker",
            Broadcast(sender_role="supervisor", content=revision),
        )
        print("[6] supervisor -> worker: REVISE")
        print(f"    {revision}")

    # --- Summary ---
    summary = checker.summary()
    print()
    print(f"Protocol completed: {summary['completed']}")
    print(f"Messages exchanged: {summary['messages']}")
    if summary.get("choice_depth", 0) > 0:
        print(f"Branch taken: {summary.get('branch_path', branch)}")


# ---------------------------------------------------------------------------
# Violation demo (same as mock runner)
# ---------------------------------------------------------------------------


def run_violation_demo() -> None:
    """Show that the protocol blocks out-of-order messages."""
    _sep("VIOLATION DEMO")
    checker = _build_checker("violation-demo")

    print("Attempting: worker sends FIRST (protocol says supervisor goes first)")
    print()

    try:
        checker.send(
            "worker", "supervisor",
            TaskResult(task_id="bad", status=TaskStatus.OK, summary="Out of order"),
        )
        print("FAIL - violation not detected")
    except ProtocolViolation as exc:
        print("BLOCKED! ProtocolViolation raised")
        print(f"  Protocol: {exc.protocol}")
        print(f"  Session:  {exc.session_id}")
        print(f"  Step:     {exc.step}")
        print(f"  Expected: {exc.expected}")
        print(f"  Got:      {exc.got}")
        print()
        print("The protocol structure makes violations IMPOSSIBLE.")
        print("Not because we trust the code -- because the session type forbids it.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    print("Lingua Universale -- Live Dogfood Runner")
    print(f"Protocol: {LU_FILE.name}")
    print()

    # Try to create API client
    client = None
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if api_key:
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=api_key)
            print("Claude API: CONNECTED")
        except ImportError:
            print("Claude API: anthropic SDK not installed (pip install anthropic)")
    else:
        print("Claude API: no key (set ANTHROPIC_API_KEY for live mode)")
        print("Running in MOCK mode -- same protocol flow, deterministic responses")

    agents = {
        role: Agent(role, client=client)
        for role in ("supervisor", "worker", "validator")
    }

    run_live(agents)
    run_violation_demo()

    _sep("DONE")
    if client:
        print("Real AI agents communicated through a formally verified protocol.")
    else:
        print("Mock run complete. Set ANTHROPIC_API_KEY for live AI agents.")
    print("The protocol guaranteed safety at every step.")


if __name__ == "__main__":
    main()
