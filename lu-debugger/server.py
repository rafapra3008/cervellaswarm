# SPDX-License-Identifier: Apache-2.0
"""LU Debugger -- FastAPI server with SSE streaming.

Endpoints:
    GET /              -> serves the debugger UI
    GET /api/protocol  -> returns the .lu protocol source
    GET /api/run/demo       -> SSE stream: pre-scripted happy path
    GET /api/run/demo-break -> SSE stream: pre-scripted violation
    GET /api/run/live       -> SSE stream: real Claude API agents
    GET /api/run/live-break -> SSE stream: real API + forced violation
    GET /api/status         -> health check + live mode availability
"""

from __future__ import annotations

import asyncio
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response, StreamingResponse

from demo_data import DEMO_BREAK, DEMO_HAPPY, PROTOCOL_SOURCE
from runner import _sse_event, is_live_available, live_break, live_happy_path

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        return response


limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="LU Debugger", version="0.1.0")
app.add_middleware(SecurityHeadersMiddleware)
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
        # Remove the delay key before sending to client
        event = {k: v for k, v in step.items() if k != "delay"}
        yield _sse_event(event)


# ---------------------------------------------------------------------------
# Run endpoints
# ---------------------------------------------------------------------------


@app.get("/api/run/demo")
@limiter.limit("10/minute")
async def run_demo(request: Request):
    """Pre-scripted happy path: OrderProcessing in_stock branch."""
    return StreamingResponse(
        _demo_generator(DEMO_HAPPY),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.get("/api/run/demo-break")
@limiter.limit("10/minute")
async def run_demo_break(request: Request):
    """Pre-scripted violation: customer skips to payment."""
    return StreamingResponse(
        _demo_generator(DEMO_BREAK),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.get("/api/run/live")
@limiter.limit("3/minute")
async def run_live(request: Request):
    """Live happy path with real Claude API agents."""
    if not is_live_available():
        async def _unavailable():
            yield _sse_event({
                "type": "error",
                "message": "Live mode unavailable. Set ANTHROPIC_API_KEY and install dependencies.",
            })
        return StreamingResponse(
            _unavailable(),
            media_type="text/event-stream",
            headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
        )
    return StreamingResponse(
        live_happy_path(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.get("/api/run/live-break")
@limiter.limit("3/minute")
async def run_live_break(request: Request):
    """Live violation: 1 real API step then forced protocol violation."""
    if not is_live_available():
        async def _unavailable():
            yield _sse_event({
                "type": "error",
                "message": "Live mode unavailable. Set ANTHROPIC_API_KEY and install dependencies.",
            })
        return StreamingResponse(
            _unavailable(),
            media_type="text/event-stream",
            headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
        )
    return StreamingResponse(
        live_break(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
