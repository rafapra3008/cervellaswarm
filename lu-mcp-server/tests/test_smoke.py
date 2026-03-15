# SPDX-License-Identifier: Apache-2.0
"""Smoke tests for lu-mcp-server."""

from __future__ import annotations

import json


def test_import():
    """Module imports without error."""
    import lu_mcp_server  # noqa: F401


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
