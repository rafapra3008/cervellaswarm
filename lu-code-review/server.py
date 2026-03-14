# SPDX-License-Identifier: Apache-2.0
"""AI Code Review -- FastAPI server with SSE streaming.

Endpoints:
    GET  /                      -> serves the review UI
    GET  /api/protocol          -> returns the .lu protocol source
    GET  /api/status            -> health check + live mode availability
    GET  /api/run/demo          -> SSE stream: pre-scripted all-clear
    GET  /api/run/demo-critical -> SSE stream: pre-scripted critical-found
    GET  /api/run/demo-break    -> SSE stream: pre-scripted violation
    POST /api/run/live          -> SSE stream: real Claude API + user code
    POST /api/run/live-break    -> SSE stream: real API + forced violation
"""

from __future__ import annotations

import asyncio
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, PlainTextResponse
import pydantic
from pydantic import BaseModel
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from starlette.responses import Response, StreamingResponse

from demo_data import (
    DEMO_ALL_CLEAR,
    DEMO_BREAK,
    DEMO_CRITICAL,
    PROTOCOL_SOURCE,
    SAMPLE_CLEAN,
    SAMPLE_VULNERABLE,
)
from runner import _sse_event, is_live_available, live_break, live_review

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="AI Code Review", version="0.1.0")
app.state.limiter = limiter

STATIC_DIR = Path(__file__).parent / "static"


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded) -> Response:
    return PlainTextResponse("Rate limit exceeded. Try again in a minute.", status_code=429)


# ---------------------------------------------------------------------------
# Static files
# ---------------------------------------------------------------------------


@app.get("/")
async def index():
    return FileResponse(STATIC_DIR / "index.html")


# ---------------------------------------------------------------------------
# API endpoints
# ---------------------------------------------------------------------------


@app.get("/api/protocol")
async def get_protocol():
    """Return the .lu protocol source for the Monaco editor."""
    return PlainTextResponse(PROTOCOL_SOURCE)


@app.get("/api/samples")
async def get_samples():
    """Return sample code snippets for the code editor."""
    return {"clean": SAMPLE_CLEAN, "vulnerable": SAMPLE_VULNERABLE}


@app.get("/api/status")
async def status():
    """Health check and feature flags."""
    return {
        "status": "ok",
        "live_available": is_live_available(),
        "version": "0.1.0",
    }


# ---------------------------------------------------------------------------
# SSE helpers
# ---------------------------------------------------------------------------


async def _demo_generator(steps: list[dict]):
    """Yield pre-scripted steps as SSE events with delays."""
    for step in steps:
        delay = step.get("delay", 0.5)
        await asyncio.sleep(delay)
        event = {k: v for k, v in step.items() if k != "delay"}
        yield _sse_event(event)


SSE_HEADERS = {"Cache-Control": "no-cache", "X-Accel-Buffering": "no"}


# ---------------------------------------------------------------------------
# Demo endpoints (GET, pre-scripted)
# ---------------------------------------------------------------------------


@app.get("/api/run/demo")
@limiter.limit("10/minute")
async def run_demo(request: Request):
    """Pre-scripted all-clear: clean code passes all reviewers."""
    return StreamingResponse(
        _demo_generator(DEMO_ALL_CLEAR),
        media_type="text/event-stream",
        headers=SSE_HEADERS,
    )


@app.get("/api/run/demo-critical")
@limiter.limit("10/minute")
async def run_demo_critical(request: Request):
    """Pre-scripted critical: vulnerable code triggers critical_found branch."""
    return StreamingResponse(
        _demo_generator(DEMO_CRITICAL),
        media_type="text/event-stream",
        headers=SSE_HEADERS,
    )


@app.get("/api/run/demo-break")
@limiter.limit("10/minute")
async def run_demo_break(request: Request):
    """Pre-scripted violation: quality skips security."""
    return StreamingResponse(
        _demo_generator(DEMO_BREAK),
        media_type="text/event-stream",
        headers=SSE_HEADERS,
    )


# ---------------------------------------------------------------------------
# Live endpoints (POST, real Claude API)
# ---------------------------------------------------------------------------


class CodeRequest(BaseModel):
    code: str = pydantic.Field(max_length=5000)


async def _unavailable_stream():
    """SSE error stream when live mode is not available."""
    yield _sse_event({
        "type": "error",
        "message": "Live mode unavailable. Set ANTHROPIC_API_KEY.",
    })


@app.post("/api/run/live")
@limiter.limit("3/minute")
async def run_live(request: Request, body: CodeRequest):
    """Live review with real Claude API agents."""
    if not is_live_available():
        return StreamingResponse(
            _unavailable_stream(),
            media_type="text/event-stream",
            headers=SSE_HEADERS,
        )
    return StreamingResponse(
        live_review(body.code),
        media_type="text/event-stream",
        headers=SSE_HEADERS,
    )


@app.post("/api/run/live-break")
@limiter.limit("3/minute")
async def run_live_break(request: Request, body: CodeRequest):
    """Live violation: 2 real steps then forced protocol violation."""
    if not is_live_available():
        return StreamingResponse(
            _unavailable_stream(),
            media_type="text/event-stream",
            headers=SSE_HEADERS,
        )
    return StreamingResponse(
        live_break(body.code),
        media_type="text/event-stream",
        headers=SSE_HEADERS,
    )
