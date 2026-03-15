# SPDX-License-Identifier: Apache-2.0
"""Smoke tests for lu-mcp-server."""

from __future__ import annotations

import json


def test_import():
    """Module imports without error."""
    import lu_mcp_server  # noqa: F401


def test_version():
    """Package exposes __version__."""
    from lu_mcp_server import __version__
    assert isinstance(__version__, str)
    assert "." in __version__


def test_main_exists():
    """Entry point function exists."""
    from lu_mcp_server import main
    assert callable(main)


def test_mcp_server_instance():
    """FastMCP server is created with correct name."""
    from lu_mcp_server import mcp
    assert mcp.name == "lingua-universale"


def test_require_lu():
    """Helper returns the LU module."""
    from lu_mcp_server import _require_lu
    lu = _require_lu()
    assert hasattr(lu, "check_source")
    assert hasattr(lu, "SessionChecker")


def test_steps_to_list_empty():
    """Empty step list returns empty list."""
    from lu_mcp_server import _steps_to_list
    assert _steps_to_list([]) == []


def test_tool_lu_load_protocol():
    """lu_load_protocol parses a simple protocol."""
    import asyncio
    from lu_mcp_server import lu_load_protocol

    protocol = (
        "protocol Ping:\n"
        "    roles: a, b\n"
        "    a asks b to ping\n"
        "    b returns pong to a\n"
        "    properties:\n"
        "        always terminates\n"
    )
    result = json.loads(asyncio.run(lu_load_protocol(protocol)))
    assert result["ok"] is True
    assert result["protocols"][0]["name"] == "Ping"
    assert len(result["protocols"][0]["roles"]) == 2


def test_tool_lu_check_properties():
    """lu_check_properties verifies safety properties."""
    import asyncio
    from lu_mcp_server import lu_check_properties

    protocol = (
        "protocol Safe:\n"
        "    roles: x, y\n"
        "    x asks y to do thing\n"
        "    y returns result to x\n"
        "    properties:\n"
        "        always terminates\n"
        "        no deadlock\n"
    )
    result = json.loads(asyncio.run(lu_check_properties(protocol)))
    assert result["ok"] is True
    assert result["summary"]["total_violated"] == 0


def test_tool_lu_list_templates():
    """lu_list_templates returns standard library templates."""
    import asyncio
    from lu_mcp_server import lu_list_templates

    result = json.loads(asyncio.run(lu_list_templates()))
    assert result["ok"] is True
    assert result["total"] == 20


def test_tool_lu_list_templates_filtered():
    """lu_list_templates filters by category."""
    import asyncio
    from lu_mcp_server import lu_list_templates

    result = json.loads(asyncio.run(lu_list_templates(category="security")))
    assert result["ok"] is True
    assert result["total"] == 3
    assert all(t["category"] == "security" for t in result["templates"])


def test_tool_lu_verify_message_valid():
    """lu_verify_message accepts a valid first message."""
    import asyncio
    from lu_mcp_server import lu_verify_message

    protocol = (
        "protocol Ping:\n"
        "    roles: a, b\n"
        "    a asks b to ping\n"
        "    b returns pong to a\n"
        "    properties:\n"
        "        always terminates\n"
    )
    result = json.loads(asyncio.run(lu_verify_message(
        protocol_text=protocol,
        messages=[],
        next_message={"sender": "a", "receiver": "b", "action": "asks"},
    )))
    assert result["valid"] is True
    assert "next_expected" in result


def test_tool_lu_verify_message_invalid_action():
    """lu_verify_message returns error for unknown action."""
    import asyncio
    from lu_mcp_server import lu_verify_message

    protocol = (
        "protocol PingPong:\n"
        "    roles: a, b\n"
        "    a asks b to ping\n"
        "    b returns pong to a\n"
        "    properties:\n"
        "        always terminates\n"
    )
    result = json.loads(asyncio.run(lu_verify_message(
        protocol_text=protocol,
        messages=[],
        next_message={"sender": "a", "receiver": "b", "action": "invalid"},
    )))
    assert result["valid"] is False
    assert "error" in result


def test_tool_lu_verify_message_no_protocol():
    """lu_verify_message returns error when no protocol found."""
    import asyncio
    from lu_mcp_server import lu_verify_message

    result = json.loads(asyncio.run(lu_verify_message(
        protocol_text="not a protocol",
        messages=[],
        next_message={"sender": "a", "receiver": "b", "action": "asks"},
    )))
    assert result["valid"] is False


def test_tool_lu_load_protocol_invalid():
    """lu_load_protocol returns error for invalid input."""
    import asyncio
    from lu_mcp_server import lu_load_protocol

    result = json.loads(asyncio.run(lu_load_protocol("not a protocol")))
    assert result["ok"] is False


def test_tool_lu_verify_message_none_in_history():
    """lu_verify_message handles None in messages list."""
    import asyncio
    from lu_mcp_server import lu_verify_message

    protocol = "protocol P:\n    roles: a, b\n    a asks b to ping\n"
    result = json.loads(asyncio.run(lu_verify_message(
        protocol_text=protocol,
        messages=[None],
        next_message={"sender": "a", "receiver": "b", "action": "asks"},
    )))
    assert result["valid"] is False
    assert "expected dict" in result["error"]


def test_tool_lu_load_protocol_size_limit():
    """lu_load_protocol rejects oversized input."""
    import asyncio
    from lu_mcp_server import lu_load_protocol, MAX_PROTOCOL_SIZE

    huge = "x" * (MAX_PROTOCOL_SIZE + 1)
    result = json.loads(asyncio.run(lu_load_protocol(huge)))
    assert result["ok"] is False
    assert "exceeds maximum size" in result["error"]


def test_tool_lu_verify_message_history_limit():
    """lu_verify_message rejects oversized history."""
    import asyncio
    from lu_mcp_server import lu_verify_message, MAX_HISTORY_LENGTH

    protocol = "protocol P:\n    roles: a, b\n    a asks b to ping\n"
    messages = [{"sender": "a", "receiver": "b", "action": "asks"}] * (MAX_HISTORY_LENGTH + 1)
    result = json.loads(asyncio.run(lu_verify_message(
        protocol_text=protocol,
        messages=messages,
        next_message={"sender": "a", "receiver": "b", "action": "asks"},
    )))
    assert result["valid"] is False
    assert "too long" in result["error"]


def test_tool_lu_check_properties_invalid():
    """lu_check_properties returns error for invalid protocol."""
    import asyncio
    from lu_mcp_server import lu_check_properties

    result = json.loads(asyncio.run(lu_check_properties("not a protocol")))
    assert result["ok"] is False


def test_tool_lu_check_properties_size_limit():
    """lu_check_properties rejects oversized input."""
    import asyncio
    from lu_mcp_server import lu_check_properties, MAX_PROTOCOL_SIZE

    huge = "x" * (MAX_PROTOCOL_SIZE + 1)
    result = json.loads(asyncio.run(lu_check_properties(huge)))
    assert result["ok"] is False
    assert "exceeds maximum size" in result["error"]


def test_tool_lu_verify_message_wrong_sender():
    """lu_verify_message detects wrong sender (ProtocolViolation)."""
    import asyncio
    from lu_mcp_server import lu_verify_message

    protocol = (
        "protocol Ping:\n"
        "    roles: a, b\n"
        "    a asks b to ping\n"
        "    b returns pong to a\n"
        "    properties:\n"
        "        always terminates\n"
    )
    # b should not send first -- a should
    result = json.loads(asyncio.run(lu_verify_message(
        protocol_text=protocol,
        messages=[],
        next_message={"sender": "b", "receiver": "a", "action": "returns"},
    )))
    assert result["valid"] is False
    assert "violation" in result


def test_tool_lu_verify_message_session_complete():
    """lu_verify_message detects extra message after protocol completion."""
    import asyncio
    from lu_mcp_server import lu_verify_message

    protocol = (
        "protocol Ping:\n"
        "    roles: a, b\n"
        "    a asks b to ping\n"
        "    b returns pong to a\n"
        "    properties:\n"
        "        always terminates\n"
    )
    # Replay full session, then try to send one more
    result = json.loads(asyncio.run(lu_verify_message(
        protocol_text=protocol,
        messages=[
            {"sender": "a", "receiver": "b", "action": "asks"},
            {"sender": "b", "receiver": "a", "action": "returns"},
        ],
        next_message={"sender": "a", "receiver": "b", "action": "asks"},
    )))
    assert result["valid"] is False


def test_tool_lu_load_protocol_choice():
    """lu_load_protocol handles protocol with choice node."""
    import asyncio
    from lu_mcp_server import lu_load_protocol

    protocol = (
        "protocol Order:\n"
        "    roles: client, server\n"
        "    client asks server to order\n"
        "    when server decides:\n"
        "        accept:\n"
        "            server returns receipt to client\n"
        "        reject:\n"
        "            server tells client to retry\n"
        "    properties:\n"
        "        always terminates\n"
    )
    result = json.loads(asyncio.run(lu_load_protocol(protocol)))
    assert result["ok"] is True
    assert result["protocols"][0]["has_choices"] is True


def test_tool_lu_verify_message_action_not_string():
    """lu_verify_message handles non-string action gracefully."""
    import asyncio
    from lu_mcp_server import lu_verify_message

    protocol = "protocol P:\n    roles: a, b\n    a asks b to ping\n"
    result = json.loads(asyncio.run(lu_verify_message(
        protocol_text=protocol,
        messages=[],
        next_message={"sender": "a", "receiver": "b", "action": 42},
    )))
    assert result["valid"] is False
    assert "string" in result["error"]


def test_tool_lu_verify_message_none_containers():
    """lu_verify_message handles None messages/next_message."""
    import asyncio
    from lu_mcp_server import lu_verify_message

    protocol = "protocol P:\n    roles: a, b\n    a asks b to ping\n"

    result1 = json.loads(asyncio.run(lu_verify_message(
        protocol_text=protocol,
        messages=None,
        next_message={"sender": "a", "receiver": "b", "action": "asks"},
    )))
    assert result1["valid"] is False
    assert "list" in result1["error"]

    result2 = json.loads(asyncio.run(lu_verify_message(
        protocol_text=protocol,
        messages=[],
        next_message=None,
    )))
    assert result2["valid"] is False
    assert "dict" in result2["error"]


def test_tool_lu_list_templates_case_insensitive():
    """lu_list_templates category filter is case-insensitive."""
    import asyncio
    from lu_mcp_server import lu_list_templates

    lower = json.loads(asyncio.run(lu_list_templates(category="security")))
    upper = json.loads(asyncio.run(lu_list_templates(category="Security")))
    mixed = json.loads(asyncio.run(lu_list_templates(category="SECURITY")))

    assert lower["ok"] is True
    assert lower["total"] == upper["total"] == mixed["total"]
