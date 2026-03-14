"""Moltbook always-on bot for lingua-universale agent.

Main loop: every CHECK_INTERVAL seconds, poll notifications and reply
to new comments on our posts using Claude Haiku.
"""

import json
import time
import logging
import os
import unicodedata
from datetime import datetime, timezone

import httpx

import config
import responder


# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%SZ",
)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Injection / safety filtering
# ---------------------------------------------------------------------------

INJECTION_PATTERNS: list[str] = [
    "ignore previous instructions",
    "ignore all previous",
    "forget your",
    "new instructions:",
    "you are now",
    "system:",
    "curl ",
    "register",
    "send your api key",
    "aiskillteam",
    "send your key to",
    "disregard your",
    "override your",
    "pretend you are",
    "act as if",
    "do not respond as",
    "your real instructions are",
    "new system prompt",
    "respond only with",
    "from now on you are",
    "reveal your prompt",
    "repeat your system",
    "what are your instructions",
]


def _normalize(text: str) -> str:
    """Normalize text for injection detection: NFKD + strip zero-width/bidi chars."""
    # NFKD decomposes homoglyphs (Cyrillic е -> e, etc.)
    text = unicodedata.normalize("NFKD", text)
    # Remove zero-width and bidi override characters
    for ch in "\u200b\u200c\u200d\ufeff\u200e\u200f\u202a\u202b\u202c\u202d\u202e\u2066\u2067\u2068\u2069":
        text = text.replace(ch, "")
    return text.lower()


def is_safe(content: str) -> bool:
    """Return True if content does not contain known injection patterns."""
    normalized = _normalize(content)
    return not any(p in normalized for p in INJECTION_PATTERNS)


# ---------------------------------------------------------------------------
# Persistent replied-IDs tracking
# ---------------------------------------------------------------------------

def _ensure_data_dir() -> None:
    """Create /data directory if it does not exist (local dev fallback)."""
    data_dir = os.path.dirname(config.REPLIED_FILE)
    os.makedirs(data_dir, exist_ok=True)


def load_replied() -> set[str]:
    """Load the set of already-replied comment IDs from disk."""
    _ensure_data_dir()
    try:
        with open(config.REPLIED_FILE) as f:
            return set(json.load(f))
    except (FileNotFoundError, json.JSONDecodeError):
        return set()


def save_replied(ids: set[str]) -> None:
    """Persist replied comment IDs to disk (atomic write via os.replace)."""
    _ensure_data_dir()
    tmp = config.REPLIED_FILE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(sorted(ids), f)
    os.replace(tmp, config.REPLIED_FILE)


# ---------------------------------------------------------------------------
# HTTP client with retry / backoff
# ---------------------------------------------------------------------------

def _make_headers() -> dict[str, str]:
    return {
        "Authorization": f"Bearer {config.MOLTBOOK_API_KEY}",
        "Content-Type": "application/json",
    }


def _get(client: httpx.Client, path: str, params: dict | None = None) -> dict | None:
    """GET request with exponential backoff on network errors.

    Returns parsed JSON dict, or None on unrecoverable error.
    """
    url = f"{config.MOLTBOOK_BASE}{path}"
    backoff = config.INITIAL_BACKOFF

    for attempt in range(1, config.MAX_RETRIES + 1):
        try:
            resp = client.get(url, params=params, timeout=30)

            if resp.status_code == 429:
                reset = resp.headers.get("X-RateLimit-Reset", "unknown")
                logger.warning("Rate limited on GET %s (attempt %d). Reset: %s", path, attempt, reset)
                time.sleep(backoff)
                backoff *= 2
                continue

            if resp.status_code == 200:
                return resp.json()

            if 300 <= resp.status_code < 400:
                logger.warning(
                    "Redirect %d on GET %s -- check if MOLTBOOK_BASE URL has changed. Location: %s",
                    resp.status_code, path, resp.headers.get("Location", "unknown"),
                )
            else:
                logger.warning("GET %s returned %d: %s", path, resp.status_code, resp.text[:200])
            return None

        except httpx.RequestError as exc:
            logger.warning("Network error on GET %s (attempt %d): %s", path, attempt, exc)
            if attempt < config.MAX_RETRIES:
                time.sleep(backoff)
                backoff *= 2

    logger.error("GET %s failed after %d attempts", path, config.MAX_RETRIES)
    return None


def _post(client: httpx.Client, path: str, body: dict) -> dict | None:
    """POST request with exponential backoff on network errors.

    Returns parsed JSON dict, or None on unrecoverable error.
    """
    url = f"{config.MOLTBOOK_BASE}{path}"
    backoff = config.INITIAL_BACKOFF

    for attempt in range(1, config.MAX_RETRIES + 1):
        try:
            resp = client.post(url, json=body, timeout=30)

            if resp.status_code == 429:
                reset = resp.headers.get("X-RateLimit-Reset", "unknown")
                logger.warning("Rate limited on POST %s (attempt %d). Reset: %s", path, attempt, reset)
                time.sleep(backoff)
                backoff *= 2
                continue

            if resp.status_code in (200, 201):
                return resp.json()

            logger.warning("POST %s returned %d: %s", path, resp.status_code, resp.text[:200])
            return None

        except httpx.RequestError as exc:
            logger.warning("Network error on POST %s (attempt %d): %s", path, attempt, exc)
            if attempt < config.MAX_RETRIES:
                time.sleep(backoff)
                backoff *= 2

    logger.error("POST %s failed after %d attempts", path, config.MAX_RETRIES)
    return None


# ---------------------------------------------------------------------------
# Moltbook API helpers
# ---------------------------------------------------------------------------

def fetch_home(client: httpx.Client) -> dict | None:
    """Fetch home/feed with notification info."""
    return _get(client, "/home")


def extract_posts_from_home(home_data: dict) -> list[dict]:
    """Extract post stubs from the /home response's activity_on_your_posts."""
    activity = home_data.get("activity_on_your_posts", [])
    posts = []
    for item in activity:
        post_id = item.get("post_id")
        post_title = item.get("post_title", "")
        if post_id:
            posts.append({"id": post_id, "title": post_title, "content": ""})
    return posts


def fetch_comments(client: httpx.Client, post_id: str) -> list[dict]:
    """Fetch comments for a specific post."""
    data = _get(client, f"/posts/{post_id}/comments", params={"sort": "new"})
    if not data:
        return []
    # API may return list or {comments: [...]}
    if isinstance(data, list):
        return data
    return data.get("comments", [])


def post_comment(client: httpx.Client, post_id: str, content: str, parent_id: str | None = None) -> bool:
    """Post a reply comment. Returns True on success."""
    body: dict = {"content": content}
    if parent_id:
        body["parent_id"] = parent_id

    result = _post(client, f"/posts/{post_id}/comments", body)
    return result is not None


def mark_notifications_read(client: httpx.Client, post_ids: list[str]) -> None:
    """Mark notifications as read for specific posts."""
    for post_id in post_ids:
        _post(client, f"/notifications/read-by-post/{post_id}", {})


# ---------------------------------------------------------------------------
# Core heartbeat logic
# ---------------------------------------------------------------------------

def process_post(
    client: httpx.Client,
    post: dict,
    replied_ids: set[str],
    replies_this_cycle: list[int],
) -> None:
    """Process one post: fetch comments, reply to new ones.

    Mutates replied_ids and increments replies_this_cycle[0] counter.
    """
    post_id = post.get("id") or post.get("post_id")
    post_title = post.get("title", "")
    post_content = post.get("content", "")

    if not post_id:
        logger.warning("Post has no id, skipping: %s", post)
        return

    comments = fetch_comments(client, post_id)
    logger.info("Post %s ('%s'): %d comments found", post_id, post_title[:50], len(comments))

    # Auto-seed replied_ids: any comment that already has a LU reply after it
    # is considered "handled" (covers manual replies before bot deployment)
    seen_non_lu: list[str] = []
    for c in comments:
        cid = c.get("id") or c.get("comment_id")
        author_obj = c.get("author", {})
        cname = author_obj.get("name", "") if isinstance(author_obj, dict) else ""
        if cname == config.AGENT_NAME:
            # Our reply found -- mark all preceding non-LU comments as replied
            for prev_id in seen_non_lu:
                if prev_id not in replied_ids:
                    replied_ids.add(prev_id)
                    logger.debug("Auto-seeded replied_id %s (manual reply exists)", prev_id)
            seen_non_lu.clear()
        elif cid:
            seen_non_lu.append(cid)

    for comment in comments:
        if replies_this_cycle[0] >= config.MAX_REPLIES_PER_CYCLE:
            logger.info("Max replies per cycle (%d) reached, stopping.", config.MAX_REPLIES_PER_CYCLE)
            return

        comment_id = comment.get("id") or comment.get("comment_id")
        author = comment.get("author", {})
        author_name = author.get("name", "") if isinstance(author, dict) else str(author)
        comment_content = comment.get("content", "")

        if not comment_id or not comment_content:
            continue

        # Skip our own comments
        if author_name == config.AGENT_NAME:
            logger.debug("Skipping own comment %s", comment_id)
            continue

        # Skip already replied
        if comment_id in replied_ids:
            logger.debug("Already replied to comment %s", comment_id)
            continue

        # Skip low-effort comments (< 30 chars, not worth a Haiku call)
        if len(comment_content.strip()) < 30:
            logger.debug("Skipping short comment %s (%d chars)", comment_id, len(comment_content))
            replied_ids.add(comment_id)
            continue

        # Safety check
        if not is_safe(comment_content):
            logger.warning(
                "Injection attempt detected in comment %s by %s -- skipping.",
                comment_id,
                author_name,
            )
            replied_ids.add(comment_id)  # mark so we don't re-check
            continue

        logger.info("Generating reply to comment %s by %s...", comment_id, author_name)

        try:
            reply_text = responder.generate_response(
                comment_content=comment_content,
                post_title=post_title,
                post_content=post_content,
                author_name=author_name,
            )
        except Exception as exc:
            logger.error("Haiku error for comment %s: %s", comment_id, exc)
            continue

        if not reply_text:
            logger.info("Haiku returned empty reply for comment %s, skipping.", comment_id)
            replied_ids.add(comment_id)
            continue

        success = post_comment(client, post_id, reply_text, parent_id=comment_id)

        if success:
            replied_ids.add(comment_id)
            replies_this_cycle[0] += 1
            logger.info(
                "Replied to comment %s (post %s). Cycle count: %d/%d",
                comment_id,
                post_id,
                replies_this_cycle[0],
                config.MAX_REPLIES_PER_CYCLE,
            )
            # Respect rate limit between replies
            if replies_this_cycle[0] < config.MAX_REPLIES_PER_CYCLE:
                logger.debug("Sleeping %.0fs for rate limit...", config.BETWEEN_REPLIES_SLEEP)
                time.sleep(config.BETWEEN_REPLIES_SLEEP)
        else:
            logger.warning("Failed to post reply to comment %s", comment_id)


def heartbeat(client: httpx.Client, replied_ids: set[str]) -> None:
    """One heartbeat cycle: check notifications and reply to new comments."""
    now = datetime.now(timezone.utc).isoformat()
    logger.info("=== Heartbeat at %s ===", now)

    # Fetch home to check for activity notifications
    home = fetch_home(client)
    if home is None:
        logger.warning("Could not fetch home feed, will retry next cycle.")
        return

    # Extract posts with activity from home response
    my_posts = extract_posts_from_home(home)
    logger.info("Found %d posts with activity.", len(my_posts))

    if not my_posts:
        logger.info("No posts found. Nothing to do this cycle.")
        return

    # replies_this_cycle is a list so it can be mutated inside process_post
    replies_this_cycle = [0]

    for post in my_posts:
        if replies_this_cycle[0] >= config.MAX_REPLIES_PER_CYCLE:
            break
        try:
            process_post(client, post, replied_ids, replies_this_cycle)
        except Exception as exc:
            post_id = post.get("id", "unknown")
            logger.error("Unexpected error processing post %s: %s", post_id, exc)

    # Mark notifications as read for posts we processed
    processed_post_ids = [
        p.get("id") or p.get("post_id") for p in my_posts if (p.get("id") or p.get("post_id"))
    ]
    try:
        mark_notifications_read(client, processed_post_ids)
    except Exception as exc:
        logger.warning("Could not mark notifications read: %s", exc)

    # Prune replied IDs to prevent unbounded growth (keep last 10000)
    if len(replied_ids) > 10000:
        sorted_ids = sorted(replied_ids)
        replied_ids.clear()
        replied_ids.update(sorted_ids[-10000:])
        logger.info("Pruned replied_ids from %d to 10000", len(sorted_ids))

    # Persist replied IDs
    save_replied(replied_ids)
    logger.info(
        "Cycle complete. %d replies sent. Total tracked comment IDs: %d",
        replies_this_cycle[0],
        len(replied_ids),
    )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    """Run the bot main loop indefinitely."""
    logger.info("lingua-universale Moltbook bot starting up.")
    logger.info(
        "Config: interval=%ds, max_replies_per_cycle=%d",
        config.CHECK_INTERVAL,
        config.MAX_REPLIES_PER_CYCLE,
    )

    replied_ids = load_replied()
    logger.info("Loaded %d previously replied comment IDs.", len(replied_ids))

    # Single persistent HTTP client for connection reuse
    with httpx.Client(headers=_make_headers(), follow_redirects=False) as client:
        while True:
            try:
                heartbeat(client, replied_ids)
            except Exception as exc:
                logger.error("Unhandled error in heartbeat: %s", exc, exc_info=True)

            logger.info("Sleeping %ds until next heartbeat...", config.CHECK_INTERVAL)
            time.sleep(config.CHECK_INTERVAL)


if __name__ == "__main__":
    main()
