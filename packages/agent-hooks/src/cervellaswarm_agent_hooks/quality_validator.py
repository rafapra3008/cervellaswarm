# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""
SNCP 5.1 Quality Validator -- SessionEnd Hook for Claude Code.

Validates PROMPT_RIPRESA quality across 6 metrics (warning only, mai blocco):
1. Density (>=0.30, max 0.55)
2. Recency scope-restricted (DOVE SIAMO + PROSSIMI only)
3. Coverage (3 HARD + 2 WARN obbligatorie)
4. Actionability (>=3 step con owner+effort)
5. Anti-rot (>=80% path navigabili come markdown link)
6. Self-sufficiency (prime 50r rispondono 3 boolean Q)

3-state validator A/B/C per SNCP version detection:
- A: Legacy 5.0 (solo CORE PROMPT_RIPRESA)
- B: Partial split (CORE + 1 di DECISIONI/APPENDIX)
- C: Complete 5.1 (CORE + DECISIONI + APPENDIX)

Disable via env var: SNCP_QUALITY_VALIDATOR_DISABLE=1

Usage in Claude Code settings.json:
    "SessionEnd": [{
        "matcher": "",
        "hooks": [{"type": "command", "command": "cervella-quality-validator"}]
    }]

Public API (importable for testing / scripting):
    main()                          -> hook entry point (stdin JSON {cwd}, exit code)
    validate_project(project_dir)   -> dict[metric -> result] per single project
    detect_state(project_dir)       -> "A" / "B" / "C" / "NONE" / "INVALID"
    format_report(results)          -> markdown table string for daily report
    write_report(content, path)     -> atomic write report to disk
    find_project_root()             -> repo root Path (git-based)
    get_core_file(project_dir)      -> CORE PROMPT_RIPRESA Path
    is_core_file(path)              -> bool (excludes .DECISIONI.md / .APPENDIX.md)

Public Metric Calculators (testable in isolation):
    calculate_density(content)           -> {density, status}
    calculate_recency(content)           -> {fresh, stale, status, scope}
    calculate_coverage(content)          -> {hard, warn, status}
    calculate_actionability(content)     -> {score, status}
    calculate_anti_rot(content)          -> {ratio, status}
    calculate_self_sufficiency(content)  -> {score, status}

Evergreen Protection (S519 D3 P4.6 3-livello flags):
    detect_evergreen_file(content)            -> bool (file-level flag)
    parse_evergreen_scopes(content)           -> list[tuple] (scope-level)
    is_h2_evergreen_protected(line_num, ...)  -> bool (line-num scope check)
    get_hook_config()                         -> dict (constants from config.py)

NOTE: No `score_prompt_ripresa()` function exists -- use `validate_project()`
for per-project results, or `main()` for full SessionEnd hook flow.

S519 Day 2 P4.4 FASE 1 (skeleton): structure + state detection + report stub.
S519 Day 3 P4.4 FASE 2 (logic): full metric calculation + atomic write.
S519 Day 4 P3 F4 fix: Public API documented in module docstring (Qualita audit).
"""

import json
import os
import re
import sys
import tempfile
from datetime import date, datetime, timezone
from pathlib import Path

from ._utils import find_project_root
from .config import get_hook_config

__version__ = "1.1.0"  # S519 D3 FASE 2: 6 real metrics implemented

# ---------------------------------------------------------------------------
# Metric thresholds (constants, NO magic numbers -- Ops M2 mandatory)
# ---------------------------------------------------------------------------

DENSITY_FLOOR = 0.30
DENSITY_CAP = 0.55
RECENCY_STALE_DAYS = 90
RECENCY_FRESH_DAYS = 14
RECENCY_MAX_STALE_PCT = 0.30
RECENCY_MIN_FRESH_H2 = 2
# P1.2.A: when no ISO-dated H2 found, fallback to status header date in head.
RECENCY_STATUS_FALLBACK = True
# HARD sections (FAIL only if ALL 3 missing -- Qualita A1 amendment)
COVERAGE_HARD_SECTIONS = ("status", "dove siamo", "puntator")
COVERAGE_WARN_SECTIONS = ("prossim", "lezion")
ACTIONABILITY_MIN_STEPS = 3
ANTI_ROT_MIN_PCT = 0.80
# P1.2.C: state A is lenient (legacy files have fewer markdown links).
ANTI_ROT_MIN_PCT_STATE_A = 0.20
SELF_SUFF_LINES = 50
# P4.6: an H2 is "evergreen-protected" if a scope marker appears in the N
# lines immediately above its header (typical position for section-level flag).
EVERGREEN_SCOPE_LOOKBACK_LINES = 5

# ---------------------------------------------------------------------------
# Regex patterns (compiled module-level to avoid ReDoS / re-compile per file)
# ---------------------------------------------------------------------------

# Anti-rot: path-like tokens (extension-anchored).
# Esteso a toml + .yml (Ops M3 extended path detection).
ANTI_ROT_PATH_RE = re.compile(
    r"[A-Za-z0-9_./\-]+\.(?:md|py|sh|json|yaml|yml|toml|ts|js)\b"
)

# Markdown link inline `[text](path)` per Anti-rot numerator.
MARKDOWN_LINK_PATH_RE = re.compile(
    r"\[[^\]]+\]\(\s*[^)\s]*\.(?:md|py|sh|json|yaml|yml|toml|ts|js)[^)\s]*\s*\)"
)

# Inline backtick code (single line) for stripping
INLINE_BACKTICK_RE = re.compile(r"`[^`\n]+`")

# Code fence toggle
CODE_FENCE_RE = re.compile(r"^```")

# H2 with date YYYY-MM-DD anywhere on header line
H2_DATE_RE = re.compile(r"^##\s+.*?(\d{4}-\d{2}-\d{2})", re.MULTILINE)

# Generic YYYY-MM-DD finder
DATE_RE = re.compile(r"\b(\d{4}-\d{2}-\d{2})\b")

# H2 generic
H2_RE = re.compile(r"^##\s+(.+)$", re.MULTILINE)
H3_RE = re.compile(r"^###\s+(.+)$", re.MULTILINE)

# Action bullets: `- [ ]` checklist OR numeric `1. ` step
ACTION_BULLET_RE = re.compile(r"^\s*(?:-\s+\[\s?\]|[0-9]+\.\s+)", re.MULTILINE)

# Actionability detection: original @owner / owner: / effort: convention (P1.2.B primary)
ACTIONABILITY_PRIMARY_RE = re.compile(
    r"(@\w+|owner\s*[:=]|effort\s*[:=])", re.IGNORECASE
)
# Legacy fallback (P1.2.B): parens-effort "(2h)" / "(15min)" / markdown link [step](file.md)
ACTIONABILITY_LEGACY_RE = re.compile(
    r"\([0-9]+(?:[\.\-][0-9]+)?\s*(?:h|hr|min|ore?)\)|"  # (2h) (15 min) (1.5h)
    r"\[[^\]]+\]\([^)\s]+\.(?:md|py|sh|json|yaml|yml|toml|ts|js)\)",  # [text](file.md)
    re.IGNORECASE,
)

# Scope sections for recency (Ops M1 anchored word-boundary)
RECENCY_SCOPE_HEADER_RE = re.compile(
    r"^##\s+(?:DOVE\s+SIAMO|PROSSIM\w*)\b.*$", re.IGNORECASE | re.MULTILINE
)

# Coverage detection patterns (P3.4 anchored ^ to avoid mid-line false positives)
STATUS_HEADER_RE = re.compile(
    r"^[\s>*\-]*(?:\*\*)?(?:STATUS|Ultimo\s+aggior)", re.IGNORECASE | re.MULTILINE
)
# P1.2.A: status header carrying an ISO date (back-compat for state A files
# without ISO-dated H2 headers). Captures the YYYY-MM-DD in group 1.
STATUS_DATE_RE = re.compile(
    r"^(?:>\s*\*\*)?(?:STATUS|Ultimo\s+aggior\w*)[:\s\-*]*.*?(\d{4}-\d{2}-\d{2})",
    re.IGNORECASE | re.MULTILINE,
)
DOVE_SIAMO_RE = re.compile(r"^##\s+DOVE\s+SIAMO\b", re.IGNORECASE | re.MULTILINE)
PUNTATORI_RE = re.compile(r"^##\s+PUNTATOR\w*\b", re.IGNORECASE | re.MULTILINE)
PROSSIMI_RE = re.compile(r"^##\s+PROSSIM\w*\b", re.IGNORECASE | re.MULTILINE)
LEZIONI_RE = re.compile(r"^##\s+LEZION\w*\b", re.IGNORECASE | re.MULTILINE)

# QUICK START header
QUICK_START_RE = re.compile(r"^##\s+QUICK\s+START\b", re.IGNORECASE | re.MULTILINE)

# Frontmatter YAML (--- ... ---)
FRONTMATTER_RE = re.compile(r"\A---\n.*?\n---\n", re.DOTALL)

# TOP-3 DIVIETI / DIVIETI heading (NOT as markdown link)
DIVIETI_RE = re.compile(r"\bDIVIETI\b", re.IGNORECASE)
LINKED_DIVIETI_RE = re.compile(r"\[[^\]]*DIVIETI[^\]]*\]", re.IGNORECASE)

# Flag evergreen 3-livello scope (P4.6 implemented).
# File-level flag: must be on the very first line of the file (anchored ^ + MULTILINE).
# Scope flag: section/entry-level, optionally with "-until: YYYY-MM-DD" expiration.
# NOTE: the two regexes are mutually exclusive by design -- "evergreen: file"
# (with colon) does NOT match EVERGREEN_SCOPE_RE, which requires either bare
# "evergreen" or "evergreen-until:" (with hyphen).
EVERGREEN_FILE_RE = re.compile(r"^<!--\s*evergreen:\s*file\s*-->", re.MULTILINE)
EVERGREEN_SCOPE_RE = re.compile(
    r"<!--\s*evergreen(?:-until:\s*(\d{4}-\d{2}-\d{2}))?\s*-->"
)


# ---------------------------------------------------------------------------
# Helpers (normalization, code-fence stripping, scope extraction)
# ---------------------------------------------------------------------------


def _normalize(content: str) -> str:
    """Normalize content: CRLF -> LF + strip BOM (EC8).

    Example:
        >>> _normalize("\\r\\nfoo")
        '\\nfoo'
    """
    # P3.1: explicit single-char strip (lstrip("﻿") would strip ALL leading BOMs
    # and any chars in the set -- startswith is the precise semantic we want).
    if content.startswith("﻿"):
        content = content[1:]
    return content.replace("\r\n", "\n")


def _strip_code_fences(content: str) -> str:
    """Remove fenced code blocks (EC9) -- preserve line count via blank lines.

    Uses a simple toggle state machine. Lines inside fences become "" so
    line numbers are preserved (needed for density's line count denominator).
    """
    lines = content.split("\n")
    inside = False
    out = []
    for line in lines:
        if CODE_FENCE_RE.match(line.lstrip()):
            inside = not inside
            out.append("")  # drop the fence marker line itself too
            continue
        out.append("" if inside else line)
    return "\n".join(out)


def _strip_inline_code(content: str) -> str:
    """Remove inline `...` backtick spans (EC4 + EC11)."""
    return INLINE_BACKTICK_RE.sub("", content)


def _strip_frontmatter(content: str) -> str:
    """Strip leading YAML frontmatter --- ... --- (EC10)."""
    m = FRONTMATTER_RE.match(content)
    if m:
        return content[m.end():]
    return content


def _extract_section(content: str, header_re: re.Pattern) -> str:
    """Return text of the first section matching header_re, until next H2 or EOF.

    If no section found, returns "" (empty -> downstream PASS-vacuous).
    """
    m = header_re.search(content)
    if not m:
        return ""
    start = m.end()
    # Find next H2 after this header
    next_h2 = re.search(r"^##\s+", content[start:], re.MULTILINE)
    if next_h2:
        return content[start:start + next_h2.start()]
    return content[start:]


def _extract_scope_recency(content: str) -> str:
    """Extract concatenated text of all DOVE SIAMO + PROSSIMI sections (Ops M1).

    INCLUDES the H2 header line itself (needed for H2-date detection in recency).
    Returns empty string if neither section is present.
    """
    chunks = []
    for m in RECENCY_SCOPE_HEADER_RE.finditer(content):
        start = m.start()  # include header line
        body_start = m.end()
        next_h2 = re.search(r"^##\s+", content[body_start:], re.MULTILINE)
        end = body_start + next_h2.start() if next_h2 else len(content)
        chunks.append(content[start:end])
    return "\n".join(chunks)


def _extract_scope_recency_bounds(content: str) -> list[tuple[int, int]]:
    """Return absolute char (start, end) bounds of every recency-scope section.

    F1 (P4.6 R2): line-number-based scope membership requires knowing exact
    char-offset bounds of each DOVE SIAMO / PROSSIMI section so we can map any
    H2 offset to a Boolean "is in scope?" without falling back to textual
    substring match (which has false positives when multiple H2 share text).

    Bounds are inclusive-start, exclusive-end (Python slice convention) and
    refer to offsets in the ORIGINAL ``content`` passed in -- callers are
    expected to pass the same (already normalized) buffer they use for line
    number computation, so offsets stay coherent.
    """
    bounds: list[tuple[int, int]] = []
    for m in RECENCY_SCOPE_HEADER_RE.finditer(content):
        start = m.start()  # include header line
        body_start = m.end()
        next_h2 = re.search(r"^##\s+", content[body_start:], re.MULTILINE)
        end = body_start + next_h2.start() if next_h2 else len(content)
        bounds.append((start, end))
    return bounds


# ---------------------------------------------------------------------------
# State detection (3-state A/B/C, SPEC sez 8)
# ---------------------------------------------------------------------------


def is_core_file(file_path: Path) -> bool:
    """Return True if file is CORE (not .DECISIONI.md / .APPENDIX.md)."""
    name = file_path.name
    return (
        name.startswith("PROMPT_RIPRESA_")
        and not name.endswith(".DECISIONI.md")
        and not name.endswith(".APPENDIX.md")
        and name.endswith(".md")
    )


def detect_state(project_dir: Path) -> str:
    """Detect SNCP state per progetto.

    Returns:
        "A"       -> Legacy SNCP 5.0 (solo CORE)
        "B"       -> Partial split (CORE + 1 di DECISIONI/APPENDIX)
        "C"       -> Complete 5.1 (CORE + DECISIONI + APPENDIX)
        "NONE"    -> Nessun PROMPT_RIPRESA trovato
        "INVALID" -> CORE mancante ma DECISIONI/APPENDIX presenti
    """
    if not project_dir.is_dir():
        return "NONE"

    files = list(project_dir.glob("PROMPT_RIPRESA_*.md"))
    if not files:
        return "NONE"

    has_core = any(is_core_file(f) for f in files)
    has_decisioni = any(f.name.endswith(".DECISIONI.md") for f in files)
    has_appendix = any(f.name.endswith(".APPENDIX.md") for f in files)

    if not has_core:
        return "INVALID"
    if has_decisioni and has_appendix:
        return "C"
    if has_decisioni or has_appendix:
        return "B"
    return "A"


def get_core_file(project_dir: Path) -> Path | None:
    """Return the CORE PROMPT_RIPRESA file or None if absent."""
    for f in sorted(project_dir.glob("PROMPT_RIPRESA_*.md")):
        if is_core_file(f):
            return f
    return None


# ---------------------------------------------------------------------------
# Evergreen flag parsing (P4.6, SPEC sez 5.1)
# ---------------------------------------------------------------------------


def detect_evergreen_file(content: str) -> bool:
    """Return True if first line is the file-level evergreen marker.

    SPEC sez 5.1: ``<!-- evergreen: file -->`` MUST appear on the very first
    line to mark the entire file as evergreen (skip archive checks).

    Examples:
        >>> detect_evergreen_file("<!-- evergreen: file -->\\n# Title\\n")
        True
        >>> detect_evergreen_file("# Title\\n<!-- evergreen: file -->\\n")
        False
        >>> detect_evergreen_file("")
        False
    """
    if not content:
        return False
    # Normalize line endings so CRLF files still detect on line 1 (EC8 parity).
    norm = _normalize(content)
    first_line = norm.split("\n", 1)[0]
    return bool(EVERGREEN_FILE_RE.match(first_line))


def parse_evergreen_scopes(
    content: str, today: date | None = None
) -> list[dict]:
    """Parse all section/entry-level evergreen scope markers.

    Returns a list of dicts (one per marker found), each with:
        - line_number: int (1-based, position of the marker)
        - until_date:  date | None  (None = no expiration)
        - is_active:   bool  (True if no until-date OR until-date > today)

    The file-level marker (if present on line 1) is intentionally skipped --
    that case is handled by ``detect_evergreen_file`` separately.

    Malformed ``evergreen-until:`` markers (e.g. with a non-ISO date) do NOT
    match ``EVERGREEN_SCOPE_RE`` and are therefore silently skipped -- they
    contribute no protection. This is the safer default: a typo shouldn't
    accidentally lock content as evergreen. Authors get bare ``<!-- evergreen -->``
    if they want unconditional protection without a date.

    The ``try/except ValueError`` branch is kept as belt-and-suspenders for the
    (defensive) case where the regex itself is later relaxed.

    Example:
        >>> from datetime import date, timedelta
        >>> past = (date.today() - timedelta(days=1)).isoformat()
        >>> c = f"## H2\\n<!-- evergreen-until: {past} -->\\n"
        >>> r = parse_evergreen_scopes(c)
        >>> r[0]["is_active"]
        False
    """
    if not content:
        return []
    if today is None:
        today = date.today()

    norm = _normalize(content)
    results: list[dict] = []
    for i, line in enumerate(norm.split("\n"), start=1):
        # Skip file-level flag on line 1 (handled by detect_evergreen_file).
        if i == 1 and EVERGREEN_FILE_RE.match(line):
            continue
        m = EVERGREEN_SCOPE_RE.search(line)
        if not m:
            continue
        until_str = m.group(1)
        until_date: date | None = None
        is_active = True
        if until_str:
            try:
                until_date = date.fromisoformat(until_str)
                # Active while until_date is in the FUTURE. On the exact day
                # of expiration (until_date == today) we consider it expired
                # so archive logic can claim the entry.
                is_active = until_date > today
            except ValueError:
                # Malformed -> defensive: treat as no expiration (active).
                until_date = None
                is_active = True
        results.append(
            {
                "line_number": i,
                "until_date": until_date,
                "is_active": is_active,
            }
        )
    return results


def is_h2_evergreen_protected(
    h2_line_number: int,
    scopes: list[dict],
    lookback: int = EVERGREEN_SCOPE_LOOKBACK_LINES,
) -> bool:
    """Return True if an ACTIVE evergreen scope marker appears in the
    ``lookback`` lines immediately preceding the H2 at ``h2_line_number``.

    Per SPEC sez 5.1, section-level markers are placed on the line(s)
    directly above an H2/H3 header. We use a small lookback window
    (default 5) to tolerate blank lines / comments between marker and
    header without bleeding protection across unrelated sections.

    Args:
        h2_line_number: 1-based line number of the H2 header in the file.
        scopes: list returned by ``parse_evergreen_scopes``.
        lookback: how many lines above the H2 to scan (default 5).

    Returns:
        True if any scope in ``scopes`` has ``is_active=True`` AND its
        ``line_number`` falls in the half-open interval
        ``[h2_line_number - lookback, h2_line_number)``.
    """
    if not scopes or h2_line_number <= 0:
        return False
    lower = h2_line_number - lookback
    for scope in scopes:
        ln = scope.get("line_number", 0)
        if lower <= ln < h2_line_number and scope.get("is_active", False):
            return True
    return False


# ---------------------------------------------------------------------------
# Metric 1: Density
# ---------------------------------------------------------------------------


def calculate_density(content: str, config: dict) -> dict:
    """Metric 1: Density = (H2 + H3 + action bullets) / total lines.

    PASS if DENSITY_FLOOR <= density <= DENSITY_CAP (default 0.30-0.55).

    Excludes code fences (EC9), normalizes CRLF+BOM (EC8), handles empty (EC1).

    Example PASS:
        File 200 righe, 30 H2, 15 H3, 15 action bullets -> 60/200 = 0.30 PASS.
    Example FAIL:
        File 100 righe, 70 H2 -> 0.70 (above cap) FAIL.
        File 200 righe, 10 H2 -> 0.05 (below floor) FAIL.
        Empty file -> 0.0 FAIL (vacuous).
    """
    if not content:
        return {
            "name": "density",
            "value": 0.0,
            "pass": False,
            "details": {"reason": "empty content"},
        }

    floor = config.get("density_min", DENSITY_FLOOR)
    cap = config.get("density_max", DENSITY_CAP)

    norm = _normalize(content)
    stripped = _strip_code_fences(norm)

    total_lines = max(len(stripped.splitlines()), 1)
    h2_count = len(H2_RE.findall(stripped))
    h3_count = len(H3_RE.findall(stripped))
    action_count = len(ACTION_BULLET_RE.findall(stripped))

    structured = h2_count + h3_count + action_count
    density = structured / total_lines
    passes = floor <= density <= cap

    return {
        "name": "density",
        "value": round(density, 3),
        "pass": passes,
        "details": {
            "h2": h2_count,
            "h3": h3_count,
            "action_bullets": action_count,
            "total_lines": total_lines,
            "floor": floor,
            "cap": cap,
        },
    }


# ---------------------------------------------------------------------------
# Metric 2: Recency (scope-restricted)
# ---------------------------------------------------------------------------


def _recency_protected_h2_lines(
    norm: str, evergreen_scopes: list[dict], lookback: int
) -> set[int]:
    """F1 (P4.6 R2): line numbers of H2 headers protected by an active marker.

    Each ACTIVE evergreen marker protects the CLOSEST (first) H2 strictly below
    it within its lookback window. Lookback is a CEILING, not a floor: a marker
    far above any H2 protects none. Without "first-H2" semantics a single
    ``<!-- evergreen -->`` would leak protection across every duplicate H2 in
    range (bug reproduced PRE-fix by
    ``test_recency_duplicate_h2_headers_only_one_protected``).
    """
    protected_h2_lines: set[int] = set()
    if not evergreen_scopes:
        return protected_h2_lines

    # Collect (line_no, offset) for every H2 in document, sorted by line.
    # H2_RE matches via MULTILINE so match.start() is the offset of the ^ char.
    h2_positions: list[tuple[int, int]] = []
    for m in H2_RE.finditer(norm):
        line_no = norm.count("\n", 0, m.start()) + 1
        h2_positions.append((line_no, m.start()))
    h2_positions.sort()

    for marker_scope in evergreen_scopes:
        if not marker_scope.get("is_active", False):
            continue
        marker_line = marker_scope.get("line_number", 0)
        if marker_line <= 0:
            continue
        # FIRST H2 strictly below marker AND within lookback ceiling.
        for h2_line, _h2_off in h2_positions:
            if h2_line <= marker_line:
                continue
            if h2_line - marker_line > lookback:
                break  # sorted list -- further H2 are even farther
            protected_h2_lines.add(h2_line)
            break  # FIRST H2 below -> stop
    return protected_h2_lines


def _recency_evergreen_skipped_count(
    norm: str,
    stale_cutoff: int,
    protected_h2_lines: set[int],
    scope_bounds: list[tuple[int, int]],
) -> int:
    """Count stale H2 dates that are evergreen-protected (to be excluded).

    F1 (P4.6 R2): membership via CHAR-OFFSET bounds (``scope_bounds``), not
    textual substring match -- a duplicate H2 with identical text but outside
    the protected section's bounds is correctly NOT counted.
    """
    if not (protected_h2_lines and scope_bounds):
        return 0
    skipped = 0
    for m in H2_DATE_RE.finditer(norm):
        line_no = norm.count("\n", 0, m.start()) + 1
        if line_no not in protected_h2_lines:
            continue
        # Offset-bounds membership check (NOT textual substring -- see F1 note).
        h2_offset = m.start()
        if not any(start <= h2_offset < end for start, end in scope_bounds):
            continue
        try:
            d = date.fromisoformat(m.group(1))
        except ValueError:
            continue
        if d.toordinal() < stale_cutoff:
            skipped += 1
    return skipped


def _recency_count_stale(
    norm: str,
    scope: str,
    stale_cutoff: int,
    protected_h2_lines: set[int],
    scope_bounds: list[tuple[int, int]],
) -> tuple[int, int, int]:
    """Count scope dates and stale ones, excluding evergreen-protected H2.

    Returns ``(total_dates, stale_count, evergreen_skipped_h2)``.

    F1 (P4.6 R2): protected-H2 membership uses CHAR-OFFSET bounds
    (``scope_bounds``) instead of textual substring match, so a duplicate H2
    with identical text but outside the protected section is NOT skipped.
    """
    # Parse all dates in scope (strict, skip malformed -- EC3).
    parsed_dates: list[date] = []
    for ds in DATE_RE.findall(scope):
        try:
            parsed_dates.append(date.fromisoformat(ds))
        except ValueError:
            continue  # EC3: skip malformed, do not crash

    total = len(parsed_dates)
    stale_count = sum(1 for d in parsed_dates if d.toordinal() < stale_cutoff)

    # P4.6: subtract stale H2 dates that fall under an active evergreen scope.
    evergreen_skipped_h2 = _recency_evergreen_skipped_count(
        norm, stale_cutoff, protected_h2_lines, scope_bounds
    )
    stale_count = max(stale_count - evergreen_skipped_h2, 0)
    return total, stale_count, evergreen_skipped_h2


def _recency_count_fresh(scope: str, fresh_cutoff: int) -> int:
    """Count H2 headers (in scope) whose ISO date is within the fresh window."""
    fresh_h2 = 0
    for m in H2_DATE_RE.finditer(scope):
        try:
            d = date.fromisoformat(m.group(1))
        except ValueError:
            continue
        if d.toordinal() >= fresh_cutoff:
            fresh_h2 += 1
    return fresh_h2


def _recency_status_fallback(norm: str, fresh_cutoff: int, config: dict) -> bool:
    """P1.2.A back-compat: legacy state-A files (no ISO-dated H2) with a fresh
    'Ultimo aggiornamento'/STATUS header in the head -> treat as 1 fresh H2.
    Returns True iff the fallback applies.
    """
    if not config.get("recency_status_fallback", RECENCY_STATUS_FALLBACK):
        return False
    head_lines = "\n".join(norm.split("\n")[:5])
    sm = STATUS_DATE_RE.search(head_lines)
    if not sm:
        return False
    try:
        status_date = date.fromisoformat(sm.group(1))
    except ValueError:
        return False  # malformed date, no fallback
    return status_date.toordinal() >= fresh_cutoff


def calculate_recency(content: str, config: dict) -> dict:
    """Metric 2: Recency on DOVE SIAMO + PROSSIMI sections (Ops M1).

    PASS if stale_pct <= 30% AND fresh_h2_count >= 2.
    - stale = date > 90 giorni
    - fresh = H2 with date within 14 giorni

    Vacuous PASS if scope is empty (no DOVE SIAMO / PROSSIMI sections found).

    P4.6 evergreen integration:
        1. File-level marker on line 1 -> vacuous PASS (skip archive checks).
        2. Section-level markers above stale H2 -> those H2 are NOT counted
           as stale (still counted in total to preserve denominator semantics,
           but excluded from stale_count).

    Example PASS:
        DOVE SIAMO con 2 H2 fresh (2 gg fa) + 0 stale -> stale_pct=0 PASS.
    Example FAIL:
        DOVE SIAMO con 5 date totali, 3 oltre 90gg -> stale_pct=0.60 FAIL.

    Notes
    -----
    - F1 (P4.6 R2): scope membership uses LINE NUMBER bounds (via
      ``_extract_scope_recency_bounds``) instead of textual substring match.
      This prevents false positives when two H2 headers share identical text
      but only the first is preceded by an evergreen marker -- the prior
      ``header_line in scope_text`` check would have falsely protected both.
    - F2 (P4.6 R2): the evergreen scope lookback distance is configurable via
      ``evergreen_scope_lookback_lines`` (default 5). Larger values protect
      H2 headers further below their marker; smaller values are stricter.
    - F3 (P4.6 R2) multiple-date H2: evergreen protection acts on the FIRST
      ISO date per H2 line only. If an H2 header includes more than one
      ISO date (e.g., ``## DOVE SIAMO 2024-01-01 vs 2024-02-02``), each date
      is parsed independently by ``DATE_RE.findall()`` and contributes to
      ``total_dates``, but the evergreen skip decision is anchored to the
      H2 header position via ``H2_DATE_RE`` (which captures the FIRST date
      only). Edge case empirically covered by
      ``test_recency_duplicate_h2_headers_only_one_protected``.
    """
    if not content:
        return {
            "name": "recency",
            "stale_pct": 0.0,
            "fresh_h2_count": 0,
            "pass": False,
            "scope_lines": 0,
            "details": {"reason": "empty content"},
        }

    # P4.6 short-circuit: file-level evergreen flag -> intero file = evergreen.
    # Skip archive check entirely (vacuous PASS for recency metric).
    if detect_evergreen_file(content):
        return {
            "name": "recency",
            "stale_pct": 0.0,
            "fresh_h2_count": 0,
            "pass": True,
            "scope_lines": 0,
            "details": {
                "reason": "evergreen file-level flag",
                "evergreen_file_level": True,
            },
        }

    max_stale_pct = config.get("recency_max_old_pct", RECENCY_MAX_STALE_PCT)
    min_fresh_h2 = config.get("recency_min_recent_h2", RECENCY_MIN_FRESH_H2)
    # F2 (P4.6 R2): expose lookback to hook config -- defaults to constant.
    lookback = config.get(
        "evergreen_scope_lookback_lines", EVERGREEN_SCOPE_LOOKBACK_LINES
    )

    norm = _normalize(content)
    scope = _extract_scope_recency(norm)

    if not scope.strip():
        # Vacuous: no scope found -> PASS (don't penalize new files).
        return {
            "name": "recency",
            "stale_pct": 0.0,
            "fresh_h2_count": 0,
            "pass": True,
            "scope_lines": 0,
            "details": {"reason": "scope empty (no DOVE SIAMO / PROSSIMI)"},
        }

    today = date.today()
    fresh_cutoff = today.toordinal() - RECENCY_FRESH_DAYS
    stale_cutoff = today.toordinal() - RECENCY_STALE_DAYS

    # P4.6: parse evergreen scopes once on the WHOLE document so we can map
    # stale H2 positions to protection markers. Using the full file (not just
    # the scope subset) preserves correct line numbering.
    evergreen_scopes = parse_evergreen_scopes(norm, today=today)

    # F1 (P4.6 R2): compute char-offset bounds of every recency scope section
    # so H2 membership uses LINE-NUMBER / OFFSET checks rather than textual
    # substring match. Substring match falsely protects duplicate H2 headers
    # that share identical text (e.g., two `## DOVE SIAMO` lines where only
    # the first carries an evergreen marker).
    scope_bounds = _extract_scope_recency_bounds(norm)

    # F1 (P4.6 R2): map stale H2 positions to their active evergreen marker.
    protected_h2_lines = _recency_protected_h2_lines(
        norm, evergreen_scopes, lookback
    )

    # Count scope dates + stale, excluding evergreen-protected H2 (offset bounds).
    total, stale_count, evergreen_skipped_h2 = _recency_count_stale(
        norm, scope, stale_cutoff, protected_h2_lines, scope_bounds
    )
    stale_pct = stale_count / max(total, 1) if total > 0 else 0.0

    # Fresh H2: headers in scope dated within the fresh window.
    fresh_h2 = _recency_count_fresh(scope, fresh_cutoff)

    # P1.2.A back-compat fallback: a fresh STATUS header counts as 1 fresh H2.
    status_fallback_used = False
    if fresh_h2 == 0 and _recency_status_fallback(norm, fresh_cutoff, config):
        fresh_h2 = 1
        status_fallback_used = True

    passes = (stale_pct <= max_stale_pct) and (fresh_h2 >= min_fresh_h2)

    return {
        "name": "recency",
        "stale_pct": round(stale_pct, 3),
        "fresh_h2_count": fresh_h2,
        "pass": passes,
        "scope_lines": len(scope.splitlines()),
        "details": {
            "total_dates": total,
            "stale_count": stale_count,
            "stale_cutoff_days": RECENCY_STALE_DAYS,
            "fresh_cutoff_days": RECENCY_FRESH_DAYS,
            "status_fallback_used": status_fallback_used,
            "evergreen_scopes_found": len(evergreen_scopes),
            "evergreen_skipped_h2": evergreen_skipped_h2,
        },
    }


# ---------------------------------------------------------------------------
# Metric 3: Coverage (3 HARD + 2 WARN)
# ---------------------------------------------------------------------------


def calculate_coverage(content: str, config: dict) -> dict:
    """Metric 3: Coverage of 3 HARD + 2 WARN sections.

    HARD: status (in first 5 lines) + DOVE SIAMO H2 + PUNTATORI H2
    WARN: PROSSIMI H2 + LEZIONI H2

    PASS if at least 1/3 HARD found (Qualita A1: FAIL only if 3/3 missing).

    Example PASS:
        Header con "Ultimo aggiornamento" + DOVE SIAMO H2 + PUNTATORI H2 -> 3/3 PASS.
    Example FAIL:
        File senza status header, senza DOVE SIAMO, senza PUNTATORI -> 0/3 FAIL.
    """
    if not content:
        return {
            "name": "coverage",
            "hard_found": 0,
            "warn_found": 0,
            "pass": False,
            "missing": list(COVERAGE_HARD_SECTIONS + COVERAGE_WARN_SECTIONS),
            "details": {"reason": "empty content"},
        }

    norm = _normalize(content)
    stripped = _strip_code_fences(norm)
    first_5 = "\n".join(stripped.splitlines()[:5])

    found = {}
    missing = []

    # HARD #1: status (first 5 lines)
    has_status = bool(STATUS_HEADER_RE.search(first_5))
    found["status"] = has_status
    if not has_status:
        missing.append("status")

    # HARD #2: DOVE SIAMO H2
    has_dove = bool(DOVE_SIAMO_RE.search(stripped))
    found["dove siamo"] = has_dove
    if not has_dove:
        missing.append("dove siamo")

    # HARD #3: PUNTATORI H2
    has_punt = bool(PUNTATORI_RE.search(stripped))
    found["puntator"] = has_punt
    if not has_punt:
        missing.append("puntator")

    # WARN #1: PROSSIMI H2
    has_prox = bool(PROSSIMI_RE.search(stripped))
    found["prossim"] = has_prox
    if not has_prox:
        missing.append("prossim")

    # WARN #2: LEZIONI H2
    has_lez = bool(LEZIONI_RE.search(stripped))
    found["lezion"] = has_lez
    if not has_lez:
        missing.append("lezion")

    hard_found = sum([has_status, has_dove, has_punt])
    warn_found = sum([has_prox, has_lez])
    # A1 Qualita amendment: PASS if at least 1/3 HARD found.
    passes = hard_found >= 1

    return {
        "name": "coverage",
        "hard_found": hard_found,
        "warn_found": warn_found,
        "pass": passes,
        "missing": missing,
        "details": {
            "found": found,
            "coverage_score": round(hard_found / 3, 2),
        },
    }


# ---------------------------------------------------------------------------
# Metric 4: Actionability
# ---------------------------------------------------------------------------


def calculate_actionability(content: str, config: dict) -> dict:
    """Metric 4: PROSSIMI section has >= 3 step with owner+effort (or @owner).

    Fallback: if PROSSIMI absent, use QUICK START.
    Counts lines that include AT LEAST one match of @\\w+ | owner: | effort:.

    Example PASS:
        PROSSIMI con 3 step "- @rafa effort: 2h" -> count=3 PASS.
    Example FAIL:
        PROSSIMI vuoto o con step generici senza owner/effort -> count=0 FAIL.
    """
    if not content:
        return {
            "name": "actionability",
            "actionable_count": 0,
            "pass": False,
            "scope": "none",
            "details": {"reason": "empty content"},
        }

    min_steps = config.get("actionability_min", ACTIONABILITY_MIN_STEPS)
    norm = _normalize(content)

    scope = _extract_section(norm, PROSSIMI_RE)
    scope_name = "PROSSIMI"
    if not scope.strip():
        scope = _extract_section(norm, QUICK_START_RE)
        scope_name = "QUICK_START (fallback)"

    if not scope.strip():
        return {
            "name": "actionability",
            "actionable_count": 0,
            "pass": False,
            "scope": "missing",
            "details": {"reason": "PROSSIMI and QUICK START both absent"},
        }

    count = 0
    for line in scope.splitlines():
        # P1.2.B: primary convention OR legacy "(2h)" / "[step](file.md)" fallback.
        if ACTIONABILITY_PRIMARY_RE.search(line) or ACTIONABILITY_LEGACY_RE.search(
            line
        ):
            count += 1

    passes = count >= min_steps

    return {
        "name": "actionability",
        "actionable_count": count,
        "pass": passes,
        "scope": scope_name,
        "details": {
            "min_steps": min_steps,
            "scope_lines": len(scope.splitlines()),
        },
    }


# ---------------------------------------------------------------------------
# Metric 5: Anti-rot (path linkability)
# ---------------------------------------------------------------------------


def calculate_anti_rot(content: str, config: dict, state: str = "C") -> dict:
    """Metric 5: >= 80% of paths mentioned are wrapped in markdown links.

    2-step algorithm (Ops M3):
      1. Denominator = path-like tokens OUTSIDE inline backticks + code fences.
      2. Numerator = `[text](path.ext)` markdown links.
    Vacuous PASS if no paths at all (denominator=0).

    P1.2.C: state A (legacy 5.0) uses a lenient 0.20 threshold; state B/C uses
    the strict 0.80 default. Override via config keys ``anti_rot_min_pct`` and
    ``anti_rot_min_pct_state_a``.

    Example PASS:
        10 path totali, 8 dentro [text](path.md) -> 0.80 PASS boundary.
    Example FAIL:
        10 path totali, 5 link -> 0.50 FAIL.
    Edge:
        Tabella ASCII `|file.md|` ha backtick -> denominator=0 (FP avoided).
    """
    if not content:
        return {
            "name": "anti_rot",
            "linked_pct": 1.0,
            "links": 0,
            "paths": 0,
            "pass": True,
            "details": {"reason": "empty content (vacuous PASS)"},
        }

    # P1.2.C: adaptive threshold per state (A lenient, B/C strict).
    if state == "A":
        min_pct = config.get("anti_rot_min_pct_state_a", ANTI_ROT_MIN_PCT_STATE_A)
    else:
        min_pct = config.get("anti_rot_min_pct", ANTI_ROT_MIN_PCT)
    norm = _normalize(content)
    stripped = _strip_code_fences(norm)

    # Numerator FIRST (before stripping inline code -- markdown links use no backtick)
    numerator = len(MARKDOWN_LINK_PATH_RE.findall(stripped))

    # Denominator AFTER stripping inline code (EC4 + EC11)
    no_backtick = _strip_inline_code(stripped)
    denominator = len(ANTI_ROT_PATH_RE.findall(no_backtick))

    if denominator == 0:
        # No paths to link -> vacuous PASS.
        return {
            "name": "anti_rot",
            "linked_pct": 1.0,
            "links": numerator,
            "paths": 0,
            "pass": True,
            "details": {"reason": "no paths (vacuous PASS)", "state": state},
        }

    # Clamp pct to [0, 1] (numerator can exceed denominator if link includes
    # paths that backticks would have masked; we treat as full coverage).
    pct = min(numerator / denominator, 1.0)
    passes = pct >= min_pct

    return {
        "name": "anti_rot",
        "linked_pct": round(pct, 3),
        "links": numerator,
        "paths": denominator,
        "pass": passes,
        "details": {
            "min_pct": min_pct,
            "state": state,
        },
    }


# ---------------------------------------------------------------------------
# Metric 6: Self-sufficiency (3 boolean Q in first 50 body lines)
# ---------------------------------------------------------------------------


def calculate_self_sufficiency(content: str, config: dict) -> dict:
    """Metric 6: first 50 body lines (post-frontmatter) answer 3 boolean Qs.

    Q1: "Cosa stiamo facendo?"   -> DOVE SIAMO H2 OR status header in first 5
    Q2: "Cosa devo fare appena arrivo?" -> QUICK START OR PROSSIMI + 1 step
    Q3: "Cosa NON devo toccare?" -> TOP-3 DIVIETI inline text (not link)

    Score 3/3 = PASS, <3/3 = WARN (mai BLOCK).

    Example PASS:
        File con frontmatter + body con DOVE SIAMO@line 8 + QUICK START@line 30
        + "## TOP-3 DIVIETI" @line 45 -> 3/3 PASS.
    """
    if not content:
        return {
            "name": "self_sufficiency",
            "q1": False,
            "q2": False,
            "q3": False,
            "score": "0/3",
            "pass": False,
            "details": {"reason": "empty content"},
        }

    n_lines = config.get("self_sufficiency_lines", SELF_SUFF_LINES)
    norm = _normalize(content)
    body = _strip_frontmatter(norm)  # EC10
    head = "\n".join(body.splitlines()[:n_lines])
    first_5 = "\n".join(head.splitlines()[:5])

    # Q1
    q1 = bool(DOVE_SIAMO_RE.search(head)) or bool(STATUS_HEADER_RE.search(first_5))

    # Q2: QUICK START or PROSSIMI present + at least 1 step bullet after header
    q2_section = ""
    if QUICK_START_RE.search(head):
        q2_section = _extract_section(head, QUICK_START_RE)
    elif PROSSIMI_RE.search(head):
        q2_section = _extract_section(head, PROSSIMI_RE)
    q2 = bool(q2_section.strip()) and bool(ACTION_BULLET_RE.search(q2_section))

    # Q3: DIVIETI inline (NOT as markdown link). Strip out [DIVIETI](...) tokens.
    no_link = LINKED_DIVIETI_RE.sub("", head)
    q3 = bool(DIVIETI_RE.search(no_link))

    score = sum([q1, q2, q3])
    passes = score == 3

    return {
        "name": "self_sufficiency",
        "q1": q1,
        "q2": q2,
        "q3": q3,
        "score": f"{score}/3",
        "pass": passes,
        "details": {
            "head_lines_examined": n_lines,
            "frontmatter_stripped": body != norm,
        },
    }


# ---------------------------------------------------------------------------
# Per-project validation
# ---------------------------------------------------------------------------


def validate_project(project_dir: Path, config: dict) -> dict:
    """Run all 6 metrics on a project's CORE PROMPT_RIPRESA."""
    state = detect_state(project_dir)
    project_name = project_dir.name

    if state in ("NONE", "INVALID"):
        return {
            "project": project_name,
            "state": state,
            "metrics": {},
            "warnings": [f"State {state}: skip metrics"],
        }

    core_path = get_core_file(project_dir)
    if core_path is None:
        return {
            "project": project_name,
            "state": state,
            "metrics": {},
            "warnings": ["No CORE file (unexpected)"],
        }

    try:
        content = core_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as e:
        return {
            "project": project_name,
            "state": state,
            "metrics": {},
            "warnings": [f"Read error: {e}"],
        }

    # F5 fix S519 D2: splitlines() instead of split("\n") to avoid off-by-one
    # from trailing newline (wc -l ground truth = N lines, split("\n") = N+1).
    line_count = len(content.splitlines())
    threshold = config.get("split_threshold_lines", 150)
    split_eligible = line_count >= threshold

    metrics = {
        "density": calculate_density(content, config),
        "recency": calculate_recency(content, config),
        "coverage": calculate_coverage(content, config),
        "actionability": calculate_actionability(content, config),
        # P1.2.C: pass state so anti_rot can use lenient threshold for state A.
        "anti_rot": calculate_anti_rot(content, config, state=state),
        "self_sufficiency": calculate_self_sufficiency(content, config),
    }

    return {
        "project": project_name,
        "state": state,
        "core": str(core_path),
        "lines": line_count,
        "split_eligible": split_eligible,
        "metrics": metrics,
    }


# ---------------------------------------------------------------------------
# Report writing
# ---------------------------------------------------------------------------


def _fmt_metric_cell(metric: dict) -> str:
    """Format one metric as a compact cell for the table.

    P3.6: surfaces ``details.reason`` (or ``status_fallback_used``) inline so
    operators can spot vacuous PASS / fallback usage without diving into JSON.
    """
    if not metric:
        return "-"
    p = metric.get("pass")
    icon = "PASS" if p else ("WARN" if p is False else "?")
    name = metric.get("name", "?")

    # P3.6: extract a short reason annotation when present.
    details = metric.get("details") or {}
    reason = details.get("reason", "")
    fallback = details.get("status_fallback_used", False)
    if fallback:
        reason_str = " (status-fb)"
    elif reason:
        reason_str = f" ({reason})"
    else:
        reason_str = ""

    # Show value/score where present
    if "value" in metric and metric["value"] is not None:
        return f"{name}={metric['value']} {icon}{reason_str}"
    if "score" in metric:
        return f"{name}={metric['score']} {icon}{reason_str}"
    if "linked_pct" in metric:
        return f"{name}={metric['linked_pct']} {icon}{reason_str}"
    if "stale_pct" in metric:
        return (
            f"{name}=stale{metric['stale_pct']}/"
            f"fresh{metric.get('fresh_h2_count', 0)} {icon}{reason_str}"
        )
    if "hard_found" in metric:
        return (
            f"{name}={metric['hard_found']}/3+"
            f"{metric.get('warn_found', 0)}/2 {icon}{reason_str}"
        )
    if "actionable_count" in metric:
        return f"{name}={metric['actionable_count']} {icon}{reason_str}"
    return f"{name} {icon}{reason_str}"


def _aggregate_verdict(metrics: dict) -> str:
    """P2.3: aggregate PASS/WARN across all metrics.

    Returns:
        "PASS" only if every metric reports pass=True. Any False -> "WARN".
        "SKIP" when no metric reports a pass status (state NONE/INVALID).
    """
    if not metrics:
        return "SKIP"
    statuses = [
        m.get("pass") for m in metrics.values() if m.get("pass") is not None
    ]
    if not statuses:
        return "SKIP"
    return "PASS" if all(statuses) else "WARN"


def format_report(results: list[dict]) -> str:
    """Format daily quality report as markdown table."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    lines = [
        f"# SNCP Quality Report -- {today}",
        "",
        f"**Validator version**: {__version__}",
        f"**Projects checked**: {len(results)}",
        "",
        "## Per-Project Status",
        "",
        "| Project | State | Lines | Split | Density | Recency | Coverage | Actionability | Anti-rot | Self-suff | Verdict |",
        "|---------|-------|-------|-------|---------|---------|----------|---------------|----------|-----------|---------|",
    ]
    for r in results:
        proj = r.get("project", "?")
        state = r.get("state", "?")
        n_lines = r.get("lines", "-")
        split = "YES" if r.get("split_eligible") else "no"
        m = r.get("metrics") or {}
        cells = [
            _fmt_metric_cell(m.get("density", {})),
            _fmt_metric_cell(m.get("recency", {})),
            _fmt_metric_cell(m.get("coverage", {})),
            _fmt_metric_cell(m.get("actionability", {})),
            _fmt_metric_cell(m.get("anti_rot", {})),
            _fmt_metric_cell(m.get("self_sufficiency", {})),
        ]
        verdict = _aggregate_verdict(m)
        lines.append(
            f"| {proj} | {state} | {n_lines} | {split} | "
            + " | ".join(cells)
            + f" | {verdict} |"
        )

    # Aggregate WARN summary
    total = len(results)
    n_a = sum(1 for r in results if r.get("state") == "A")
    n_b = sum(1 for r in results if r.get("state") == "B")
    n_c = sum(1 for r in results if r.get("state") == "C")
    lines.extend(
        [
            "",
            "## Aggregate",
            "",
            f"- Total projects: {total}",
            f"- State A (legacy 5.0): {n_a}",
            f"- State B (partial split): {n_b}",
            f"- State C (complete 5.1): {n_c}",
            "",
            "## Notes",
            "",
            "Generated by quality_validator FASE 2 (real metrics). Warning-only -- mai blocco.",
            "Disable with env var: SNCP_QUALITY_VALIDATOR_DISABLE=1",
            "",
        ]
    )
    return "\n".join(lines)


def write_report(results: list[dict], output_dir: Path) -> Path | None:
    """Write daily quality report (atomic write pattern, never in-place)."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    output_dir.mkdir(parents=True, exist_ok=True)
    report_path = output_dir / f"sncp_quality_{today}.md"

    content = format_report(results)

    # Atomic write: tmp + os.rename (POSIX safe same-filesystem)
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=output_dir,
            suffix=".tmp",
            delete=False,
        ) as tmp:
            tmp.write(content)
            tmp_path = Path(tmp.name)
        tmp_path.replace(report_path)
        return report_path
    except OSError as e:
        print(
            f"quality_validator: failed to write report: {e}",
            file=sys.stderr,
        )
        return None


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------


def main() -> int:
    """Entry point. Mai blocca, sempre warning + report file."""
    # Disable via env var (Ops D5 scenario 1)
    if os.environ.get("SNCP_QUALITY_VALIDATOR_DISABLE") == "1":
        print(json.dumps({"result": "disabled via SNCP_QUALITY_VALIDATOR_DISABLE"}))
        return 0

    # Parse stdin (Claude Code passes JSON: {"cwd": "...", ...})
    try:
        input_data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        input_data = {}

    cwd = input_data.get("cwd", os.getcwd())
    project_root = find_project_root(cwd) or Path(cwd)
    progetti_dir = project_root / ".sncp" / "progetti"

    if not progetti_dir.is_dir():
        print(
            json.dumps(
                {
                    "result": "ok",
                    "info": "no .sncp/progetti dir, skip validation",
                }
            )
        )
        return 0

    config = get_hook_config("quality_validator")

    results = []
    for d in sorted(progetti_dir.iterdir()):
        if not d.is_dir():
            continue
        results.append(validate_project(d, config))

    # Report dir from config or default
    report_dir = project_root / config.get("report_dir", ".sncp/reports/daily")
    report_path = write_report(results, report_dir)

    # Output summary (warning only, mai blocco)
    n_projects = len(results)
    n_invalid = sum(1 for r in results if r.get("state") in ("INVALID",))
    if n_invalid > 0:
        print(
            f"quality_validator: WARN {n_invalid}/{n_projects} project in INVALID state",
            file=sys.stderr,
        )

    print(
        json.dumps(
            {
                "result": "ok",
                "phase": "fase-2",
                "version": __version__,
                "report": str(report_path) if report_path else None,
                "projects_checked": n_projects,
                "states": {
                    "A": sum(1 for r in results if r.get("state") == "A"),
                    "B": sum(1 for r in results if r.get("state") == "B"),
                    "C": sum(1 for r in results if r.get("state") == "C"),
                    "NONE": sum(1 for r in results if r.get("state") == "NONE"),
                    "INVALID": sum(
                        1 for r in results if r.get("state") == "INVALID"
                    ),
                },
            }
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
