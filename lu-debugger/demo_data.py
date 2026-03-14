# SPDX-License-Identifier: Apache-2.0
"""Pre-scripted demo data for the LU Debugger.

Two scenarios:
1. Happy path: OrderProcessing runs successfully (in_stock branch)
2. Break: Payment tries to process before Warehouse confirms -> BLOCKED
"""

from __future__ import annotations

# The protocol source -- displayed in the Monaco editor.
# Line numbers in DEMO_HAPPY and DEMO_BREAK reference this exact text.
PROTOCOL_SOURCE = """\
# SPDX-License-Identifier: Apache-2.0
# Order Processing Protocol -- LU Debugger Demo
#
# Three agents coordinate an order: Customer places it,
# Warehouse checks stock, Payment processes only AFTER
# Warehouse confirms availability. If out of stock,
# Payment never runs -- the protocol makes it impossible.

type OrderStatus = Pending | Confirmed | OutOfStock

agent Customer:
    role: customer
    trust: standard
    accepts: TaskResult
    produces: TaskRequest
    requires: order.valid
    ensures: order.placed

agent Warehouse:
    role: warehouse
    trust: trusted
    accepts: TaskRequest
    produces: TaskResult
    requires: order.received
    ensures: stock.checked

agent PaymentProcessor:
    role: payment
    trust: verified
    accepts: TaskRequest
    produces: TaskResult
    requires: stock.confirmed
    ensures: payment.processed

protocol OrderProcessing:
    roles: customer, warehouse, payment

    customer asks warehouse to check availability
    warehouse returns stock status to customer

    when customer decides:
        in_stock:
            customer asks payment to process order
            payment returns confirmation to customer

        out_of_stock:
            customer sends cancellation to warehouse

    properties:
        always terminates
        no deadlock
        no deletion
        all roles participate
"""

# Protocol line numbers (1-indexed, matching PROTOCOL_SOURCE)
LINE = {
    "customer_asks_warehouse": 38,
    "warehouse_returns": 39,
    "choice": 41,
    "in_stock": 42,
    "customer_asks_payment": 43,
    "payment_returns": 44,
    "out_of_stock": 46,
    "customer_cancels": 47,
}


DEMO_HAPPY: list[dict] = [
    {
        "type": "agent_message",
        "step": 1,
        "from": "customer",
        "to": "warehouse",
        "message_type": "TaskRequest",
        "content": "Check availability for Order #1247: Blue Widget x3, shipping to Milano.",
        "protocol_line": LINE["customer_asks_warehouse"],
        "status": "ok",
        "delay": 0.8,
    },
    {
        "type": "agent_message",
        "step": 2,
        "from": "warehouse",
        "to": "customer",
        "message_type": "TaskResult",
        "content": "In stock. 127 units available in EU warehouse. Ready to ship within 24h.",
        "protocol_line": LINE["warehouse_returns"],
        "status": "ok",
        "delay": 1.0,
    },
    {
        "type": "choice",
        "step": 3,
        "who": "customer",
        "branch": "in_stock",
        "protocol_line": LINE["in_stock"],
        "delay": 0.6,
    },
    {
        "type": "agent_message",
        "step": 4,
        "from": "customer",
        "to": "payment",
        "message_type": "TaskRequest",
        "content": "Process payment: \u20ac89.97 (3x Blue Widget @ \u20ac29.99). Card ending 4242.",
        "protocol_line": LINE["customer_asks_payment"],
        "status": "ok",
        "delay": 0.8,
    },
    {
        "type": "agent_message",
        "step": 5,
        "from": "payment",
        "to": "customer",
        "message_type": "TaskResult",
        "content": "Payment confirmed. Transaction ID: TXN-7829-AXKD. Receipt sent to customer.",
        "protocol_line": LINE["payment_returns"],
        "status": "ok",
        "delay": 0.8,
    },
    {
        "type": "done",
        "completed": True,
        "messages": 5,
        "branch": "in_stock",
        "delay": 0.3,
    },
]


DEMO_BREAK: list[dict] = [
    {
        "type": "agent_message",
        "step": 1,
        "from": "customer",
        "to": "warehouse",
        "message_type": "TaskRequest",
        "content": "Check availability for Order #5678: Red Widget x10, urgent delivery.",
        "protocol_line": LINE["customer_asks_warehouse"],
        "status": "ok",
        "delay": 0.8,
    },
    {
        "type": "info",
        "step": 2,
        "content": "Customer tries to skip ahead and pay before Warehouse confirms...",
        "delay": 1.2,
    },
    {
        "type": "violation",
        "step": 2,
        "from": "customer",
        "to": "payment",
        "message_type": "TaskRequest",
        "expected": "warehouse \u2192 customer: TaskResult (stock status)",
        "got": "customer \u2192 payment: TaskRequest (process payment)",
        "protocol_line": LINE["warehouse_returns"],
        "error": "ProtocolViolation: Payment cannot process before Warehouse confirms "
        "availability. The session type makes this IMPOSSIBLE -- not by convention, "
        "by mathematical proof.",
        "delay": 0.5,
    },
    {
        "type": "done",
        "completed": False,
        "blocked": True,
        "messages": 1,
        "delay": 0.3,
    },
]
