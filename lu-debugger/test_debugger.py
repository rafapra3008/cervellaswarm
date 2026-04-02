# SPDX-License-Identifier: Apache-2.0
"""Tests for lu-debugger server and runner."""

import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Ensure lu-debugger modules are importable
sys.path.insert(0, str(Path(__file__).parent))

from demo_data import DEMO_BREAK, DEMO_HAPPY, PROTOCOL_SOURCE
from runner import _build_checker, _sse_event, is_live_available


# ---------------------------------------------------------------------------
# Runner tests
# ---------------------------------------------------------------------------


class TestSSEEvent:
    """Test SSE event formatting."""

    def test_formats_dict_as_sse(self):
        result = _sse_event({"type": "step", "role": "customer"})
        assert result.startswith("data: ")
        assert result.endswith("\n\n")

    def test_valid_json_payload(self):
        result = _sse_event({"type": "done", "ok": True})
        payload = result.removeprefix("data: ").rstrip("\n")
        parsed = json.loads(payload)
        assert parsed["type"] == "done"
        assert parsed["ok"] is True

    def test_empty_dict(self):
        result = _sse_event({})
        assert result == "data: {}\n\n"


class TestBuildChecker:
    """Test _build_checker creates a valid SessionChecker."""

    def test_creates_checker(self):
        checker = _build_checker("test-session")
        assert checker is not None
        assert checker.session_id == "test-session"

    def test_protocol_name_is_order_processing(self):
        checker = _build_checker("test")
        assert "Order" in checker.protocol_name


class TestIsLiveAvailable:
    """Test live mode availability detection."""

    @patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key"}, clear=False)
    def test_available_with_key_and_deps(self):
        # LU is installed in dev, anthropic might not be
        result = is_live_available()
        assert isinstance(result, bool)

    @patch.dict("os.environ", {}, clear=True)
    def test_unavailable_without_key(self):
        assert is_live_available() is False


# ---------------------------------------------------------------------------
# Demo data tests
# ---------------------------------------------------------------------------


class TestDemoData:
    """Test pre-scripted demo scenarios."""

    def test_happy_path_not_empty(self):
        assert len(DEMO_HAPPY) > 0

    def test_break_not_empty(self):
        assert len(DEMO_BREAK) > 0

    def test_happy_path_has_done_event(self):
        types = [step.get("type") for step in DEMO_HAPPY]
        assert "done" in types

    def test_break_has_violation(self):
        types = [step.get("type") for step in DEMO_BREAK]
        assert "violation" in types or "error" in types

    def test_protocol_source_is_valid_lu(self):
        from cervellaswarm_lingua_universale._parser import parse

        program = parse(PROTOCOL_SOURCE)
        assert program is not None
        assert len(program.declarations) > 0

    def test_all_steps_have_type(self):
        for step in DEMO_HAPPY:
            assert "type" in step, f"Missing type in step: {step}"
        for step in DEMO_BREAK:
            assert "type" in step, f"Missing type in step: {step}"


# ---------------------------------------------------------------------------
# Server tests (FastAPI TestClient)
# ---------------------------------------------------------------------------


class TestServer:
    """Test FastAPI endpoints."""

    @pytest.fixture
    def client(self):
        from starlette.testclient import TestClient
        from server import app
        return TestClient(app)

    def test_index_returns_html(self, client):
        resp = client.get("/")
        assert resp.status_code == 200
        assert "text/html" in resp.headers.get("content-type", "")

    def test_protocol_returns_lu_source(self, client):
        resp = client.get("/api/protocol")
        assert resp.status_code == 200
        assert "protocol" in resp.text.lower()

    def test_status_endpoint(self, client):
        resp = client.get("/api/status")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"
        assert "live_available" in data
        assert "version" in data

    def test_demo_happy_sse_stream(self, client):
        resp = client.get("/api/run/demo")
        assert resp.status_code == 200
        assert "text/event-stream" in resp.headers.get("content-type", "")
        assert resp.text.startswith("data: ")

    def test_demo_break_sse_stream(self, client):
        resp = client.get("/api/run/demo-break")
        assert resp.status_code == 200
        assert "text/event-stream" in resp.headers.get("content-type", "")

    def test_security_headers(self, client):
        resp = client.get("/api/status")
        assert resp.headers.get("X-Content-Type-Options") == "nosniff"
        assert resp.headers.get("X-Frame-Options") == "DENY"
        assert "strict-origin" in resp.headers.get("Referrer-Policy", "")
