# SPDX-License-Identifier: Apache-2.0
"""Async live runner: real Claude API agents on the OrderProcessing protocol.

Wraps sync anthropic calls in asyncio.to_thread() for SSE streaming.
Falls back to demo mode if LU library or anthropic SDK are not installed.
"""

from __future__ import annotations

import asyncio
import json
import os
import re
import uuid
from typing import AsyncGenerator

from demo_data import LINE, PROTOCOL_SOURCE

# Optional deps -- live mode requires both
try:
    from cervellaswarm_lingua_universale._ast import ProtocolNode
    from cervellaswarm_lingua_universale._eval import _protocol_node_to_runtime
    from cervellaswarm_lingua_universale._parser import parse
    from cervellaswarm_lingua_universale.checker import (
        ProtocolViolation,
        SessionChecker,
    )
    from cervellaswarm_lingua_universale.types import (
        DirectMessage,
        TaskRequest,
        TaskResult,
        TaskStatus,
    )

    HAS_LU = True
except ImportError:
    HAS_LU = False

try:
    import anthropic

    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False


def is_live_available() -> bool:
    """True when both LU library and anthropic SDK are installed with a key."""
    return HAS_LU and HAS_ANTHROPIC and bool(os.environ.get("ANTHROPIC_API_KEY"))


# ---------------------------------------------------------------------------
# Agent system prompts
# ---------------------------------------------------------------------------

_SYSTEM_PROMPTS: dict[str, str] = {
    "customer": (
        "You are playing the role of a Customer agent in a SIMULATED e-commerce demo. "
        "This is a protocol verification demo, not real commerce. "
        "Ask about product availability with specific details (product name, quantity, city). "
        "Reply in 1 sentence, max 120 characters."
    ),
    "warehouse": (
        "You are playing the role of a Warehouse agent in a SIMULATED e-commerce demo. "
        "Products are always IN STOCK in this demo. "
        "Report availability with specific unit counts and shipping estimate. "
        "Reply in 1 sentence, max 120 characters."
    ),
    "payment": (
        "You are playing the role of a Payment Processor in a SIMULATED e-commerce demo. "
        "This is fictional -- confirm the simulated payment with a made-up transaction ID "
        "(format: TXN-XXXX-XXXX) and amount. "
        "Reply in 1 sentence, max 120 characters."
    ),
}

MODEL = "claude-haiku-4-5-20251001"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _build_checker(session_id: str) -> SessionChecker:
    """Parse the protocol source and create a SessionChecker."""
    program = parse(PROTOCOL_SOURCE)
    protocol_node = next(
        d for d in program.declarations if isinstance(d, ProtocolNode)
    )
    protocol = _protocol_node_to_runtime(protocol_node)
    return SessionChecker(protocol, session_id=session_id)


def _call_agent(client: anthropic.Anthropic, role: str, context: str) -> str:
    """Synchronous Claude API call for one agent."""
    response = client.messages.create(
        model=MODEL,
        max_tokens=150,
        system=_SYSTEM_PROMPTS[role],
        messages=[{"role": "user", "content": context}],
    )
    if not response.content or not hasattr(response.content[0], "text"):
        return "(no response)"
    text = response.content[0].text.strip()
    if len(text) > 190:
        text = text[:187] + "..."
    return text


def _sse_event(data: dict) -> str:
    """Format a dict as an SSE data line."""
    return f"data: {json.dumps(data)}\n\n"


# ---------------------------------------------------------------------------
# Live happy path generator
# ---------------------------------------------------------------------------


async def live_happy_path() -> AsyncGenerator[str, None]:
    """Run OrderProcessing with real Claude API calls, yielding SSE events."""
    if not is_live_available():
        yield _sse_event({"type": "error", "message": "Live mode unavailable"})
        return

    client = anthropic.Anthropic(timeout=30.0)
    checker = _build_checker(f"live-{uuid.uuid4().hex[:8]}")

    # Step 1: customer -> warehouse
    content = await asyncio.to_thread(
        _call_agent,
        client,
        "customer",
        "You need to check availability for an order. Ask the warehouse about "
        "a specific product with quantity and shipping destination. (1 sentence)",
    )
    checker.send(
        "customer",
        "warehouse",
        TaskRequest(task_id="order-001", description=content),
    )
    yield _sse_event(
        {
            "type": "agent_message",
            "step": 1,
            "from": "customer",
            "to": "warehouse",
            "message_type": "TaskRequest",
            "content": content,
            "protocol_line": LINE["customer_asks_warehouse"],
            "status": "ok",
        }
    )
    await asyncio.sleep(0.3)

    # Step 2: warehouse -> customer
    content = await asyncio.to_thread(
        _call_agent,
        client,
        "warehouse",
        f"Customer asked: '{content}'. Check inventory and report availability "
        "with unit count. (1 sentence)",
    )
    checker.send(
        "warehouse",
        "customer",
        TaskResult(task_id="order-001", status=TaskStatus.OK, summary=content),
    )
    yield _sse_event(
        {
            "type": "agent_message",
            "step": 2,
            "from": "warehouse",
            "to": "customer",
            "message_type": "TaskResult",
            "content": content,
            "protocol_line": LINE["warehouse_returns"],
            "status": "ok",
        }
    )
    await asyncio.sleep(0.3)

    # Step 3: customer decides (always in_stock for demo reliability)
    checker.choose_branch("in_stock")
    yield _sse_event(
        {
            "type": "choice",
            "step": 3,
            "who": "customer",
            "branch": "in_stock",
            "protocol_line": LINE["in_stock"],
        }
    )
    await asyncio.sleep(0.3)

    # Step 4: customer -> payment
    content = await asyncio.to_thread(
        _call_agent,
        client,
        "customer",
        "Stock is confirmed. Send the order total to the payment processor. "
        "Example: 'Please process order total: $149.98 for 2x Widget Pro'. (1 sentence)",
    )
    checker.send(
        "customer",
        "payment",
        TaskRequest(task_id="pay-001", description=content),
    )
    yield _sse_event(
        {
            "type": "agent_message",
            "step": 4,
            "from": "customer",
            "to": "payment",
            "message_type": "TaskRequest",
            "content": content,
            "protocol_line": LINE["customer_asks_payment"],
            "status": "ok",
        }
    )
    await asyncio.sleep(0.3)

    # Step 5: payment -> customer
    content = await asyncio.to_thread(
        _call_agent,
        client,
        "payment",
        f"The customer says: '{content}'. Confirm the order is processed and provide "
        "a fictional transaction ID. (1 sentence)",
    )
    checker.send(
        "payment",
        "customer",
        TaskResult(task_id="pay-001", status=TaskStatus.OK, summary=content),
    )
    yield _sse_event(
        {
            "type": "agent_message",
            "step": 5,
            "from": "payment",
            "to": "customer",
            "message_type": "TaskResult",
            "content": content,
            "protocol_line": LINE["payment_returns"],
            "status": "ok",
        }
    )
    await asyncio.sleep(0.2)

    yield _sse_event(
        {
            "type": "done",
            "completed": True,
            "messages": 5,
            "branch": "in_stock",
        }
    )


# ---------------------------------------------------------------------------
# Live break generator
# ---------------------------------------------------------------------------


async def live_break() -> AsyncGenerator[str, None]:
    """Run 1 real step, then force a protocol violation."""
    if not is_live_available():
        yield _sse_event({"type": "error", "message": "Live mode unavailable"})
        return

    client = anthropic.Anthropic(timeout=30.0)
    checker = _build_checker(f"live-break-{uuid.uuid4().hex[:8]}")

    # Step 1: customer -> warehouse (real)
    content = await asyncio.to_thread(
        _call_agent,
        client,
        "customer",
        "You need to check availability for an urgent order of 10 Red Widgets. "
        "Ask the warehouse. (1 sentence)",
    )
    checker.send(
        "customer",
        "warehouse",
        TaskRequest(task_id="order-bad", description=content),
    )
    yield _sse_event(
        {
            "type": "agent_message",
            "step": 1,
            "from": "customer",
            "to": "warehouse",
            "message_type": "TaskRequest",
            "content": content,
            "protocol_line": LINE["customer_asks_warehouse"],
            "status": "ok",
        }
    )
    await asyncio.sleep(0.5)

    # Info: what's about to happen
    yield _sse_event(
        {
            "type": "info",
            "step": 2,
            "content": "Customer tries to skip ahead and pay before Warehouse confirms...",
        }
    )
    await asyncio.sleep(1.0)

    # Step 2: VIOLATION -- customer tries to talk to payment directly
    try:
        checker.send(
            "customer",
            "payment",
            TaskRequest(task_id="order-bad", description="Process payment now!"),
        )
        # Should never reach here
        yield _sse_event({"type": "error", "message": "Violation not caught!"})
    except ProtocolViolation as exc:
        yield _sse_event(
            {
                "type": "violation",
                "step": 2,
                "from": "customer",
                "to": "payment",
                "message_type": "TaskRequest",
                "expected": f"{exc.expected}",
                "got": f"{exc.got}",
                "protocol_line": LINE["warehouse_returns"],
                "error": "ProtocolViolation: Payment cannot process before Warehouse "
                "confirms availability. The session type makes this IMPOSSIBLE -- "
                "not by convention, by mathematical proof.",
            }
        )

    await asyncio.sleep(0.3)
    yield _sse_event(
        {
            "type": "done",
            "completed": False,
            "blocked": True,
            "messages": 1,
        }
    )
