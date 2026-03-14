"""Configuration for Moltbook bot -- lingua-universale agent."""

import os


def _require_env(name: str) -> str:
    """Get a required env var with a clear error message."""
    val = os.environ.get(name)
    if not val:
        raise SystemExit(f"Required environment variable {name} is not set. Check your .env or Fly.io secrets.")
    return val


MOLTBOOK_API_KEY: str = _require_env("MOLTBOOK_API_KEY")
ANTHROPIC_API_KEY: str = _require_env("ANTHROPIC_API_KEY")

MOLTBOOK_BASE: str = "https://www.moltbook.com/api/v1"

# NOTE: Always use www prefix -- without it, 307 redirect strips Authorization header.
# Source: bug report on Moltbook itself (post d45e46d1).

CHECK_INTERVAL: int = int(os.environ.get("CHECK_INTERVAL_SECONDS", "900"))  # 15 min
MAX_REPLIES_PER_CYCLE: int = int(os.environ.get("MAX_REPLIES_PER_CYCLE", "5"))

AGENT_NAME: str = "lingua-universale"

# Rate limiting (Moltbook API documented limits)
# 50 comments/hour, 100 requests/minute
BETWEEN_REPLIES_SLEEP: float = 25.0  # seconds (buffer above 1/20s limit for established agents)
MAX_COMMENTS_PER_HOUR: int = 50

# Persistent storage path (Fly.io volume mount)
DATA_DIR: str = os.environ.get("DATA_DIR", "/data")
REPLIED_FILE: str = f"{DATA_DIR}/replied_ids.json"

# Retry config
MAX_RETRIES: int = 3
INITIAL_BACKOFF: float = 5.0  # seconds
