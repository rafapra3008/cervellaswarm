# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""
Bash Validator - PreToolUse Hook for Claude Code.

Validates bash commands BEFORE execution:
- BLOCK: irreversible destructive commands (rm /, DROP TABLE, fork bomb)
- ASK: risky commands that need user confirmation (git reset --hard, chmod 777)
- AUTO-FIX: replaces with safer alternatives (--force -> --force-with-lease)
- ALLOW: everything else (silent pass-through)

Usage in Claude Code settings.json:
    "PreToolUse": [{
        "matcher": "Bash",
        "hooks": [{"type": "command", "command": "cervella-bash-validator"}]
    }]

Zero dependencies for core logic (stdlib only).
Optionally reads extra patterns from hooks.yaml config when pyyaml is available.
"""

import json
import re
import sys

__version__ = "1.3.0"


def _load_extra_patterns() -> tuple[list, list, list]:
    """Load extra patterns from config (optional, fails gracefully)."""
    try:
        from .config import get_hook_config

        cfg = get_hook_config("bash_validator")
        extra_blocked = []
        for p in cfg.get("extra_blocked", []):
            if isinstance(p, dict) and "pattern" in p and "reason" in p:
                try:
                    re.compile(p["pattern"])
                    extra_blocked.append((p["pattern"], p["reason"]))
                except re.error:
                    pass  # Skip invalid regex silently (hook must not crash)
        extra_risky = []
        for p in cfg.get("extra_risky", []):
            if isinstance(p, dict) and "pattern" in p and "reason" in p:
                try:
                    re.compile(p["pattern"])
                    extra_risky.append((p["pattern"], p["reason"]))
                except re.error:
                    pass  # Skip invalid regex silently
        extra_safe = []
        for s in cfg.get("extra_safe_rm", []):
            if isinstance(s, str):
                try:
                    re.compile(s)
                    extra_safe.append(s)
                except re.error:
                    pass  # Skip invalid regex silently
        return extra_blocked, extra_risky, extra_safe
    except (OSError, ValueError) as e:
        print(f"bash_validator: failed to load extra patterns: {e}", file=sys.stderr)
        return [], [], []

# ============================================================
# PATTERNS - Commands to block / warn about
# ============================================================

# BLOCK (deny) - IRREVERSIBLE commands, never execute
BLOCKED_PATTERNS = [
    # Filesystem destruction (original package style — not re-harmonized)
    (r"rm\s+(-[a-zA-Z]*f[a-zA-Z]*\s+)?/(\s|$)", "rm on root /"),
    (r"rm\s+(-[a-zA-Z]*f[a-zA-Z]*\s+)?~/", "rm on home ~/"),
    (r"rm\s+-[a-zA-Z]*rf[a-zA-Z]*\s+\.\s*$", "rm -rf . (current directory)"),
    (r"rm\s+-[a-zA-Z]*rf[a-zA-Z]*\s+\.\.", "rm -rf .. (parent directory)"),
    # Filesystem destruction (rich style, ported from HOME v1.5.0 — S526)
    # Prefix (?:^|[\s;&|`("']) anchors the rm at a command boundary so it also
    # fires inside subshells/chains; flag-skip (-[-\w]+\s+)* tolerates -rf, etc.
    # NOTE: 2 rm styles coexist by design (the 4 above are NOT re-harmonized —
    # that would be an out-of-scope refactor).
    (r"""(?:^|[\s;&|`("'])rm\s+(-[-\w]+\s+)*/\*""", "rm /* (glob root) -- S526"),
    (r"""(?:^|[\s;&|`("'])rm\s+(-[-\w]+\s+)*\$\{?HOME\b""", "rm on $HOME -- S526"),
    # Git force push to main/master
    (r"git\s+push\s+.*--force\s+.*\b(main|master)\b", "force push to main/master"),
    (r"git\s+push\s+.*-f\s+.*\b(main|master)\b", "force push to main/master"),
    (r"git\s+push\s+--force\s+\S+\s+(main|master)", "force push to main/master"),
    (r"git\s+push\s+-f\s+\S+\s+(main|master)", "force push to main/master"),
    # Git force push to main/master via +refspec (ported from HOME v1.5.0 — S526)
    (r"git\s+push\s+\S+\s+\+(?:refs/heads/)?(?:\S*:)?(?:main|master)(?:\s|$|[;&|])", "force push +refspec to main/master -- S526"),
    # SQL destruction
    (r"DROP\s+TABLE", "DROP TABLE"),
    (r"DROP\s+DATABASE", "DROP DATABASE"),
    (r"TRUNCATE\s+TABLE", "TRUNCATE TABLE"),
    # SQL DELETE FROM without WHERE (ported from HOME v1.5.0 — S519)
    # anchor ^[^#]*\b (skip comments) + terminator multi (;|&&|\|\||\||$)
    (r"^[^#]*\bDELETE\s+FROM\s+\w+\s*(?:;|&&|\|\||\||$)", "DELETE FROM without WHERE clause"),
    # System destruction
    (r"mkfs\.", "filesystem format"),
    (r"dd\s+if=.+of=/dev/", "raw write to device"),
    (r":\(\)\s*\{\s*:\s*\|\s*:\s*&\s*\}\s*;", "fork bomb"),
    (r">\s*/dev/sd[a-z]", "device overwrite"),
    # Config overwrite via redirect (ported from HOME v1.5.0 — S519)
    # S517 disaster scenario: settings.json overwrite = config + secret leak risk.
    (r"^[^#]*>\s*~/\.claude/settings\.json", "overwrite ~/.claude/settings.json (config + potential leak)"),
    (r"^[^#]*>\s*~/\.claude-insiders/settings\.json", "overwrite ~/.claude-insiders/settings.json"),
    # Curl/wget pipe to shell (ported from HOME v1.5.0 — S519)
    # Industry-wide anti-pattern: arbitrary code injection.
    (r"(?:curl|wget)\s+.*\|\s*(?:bash|sh|zsh)\b", "curl/wget pipe to shell -- arbitrary code injection"),
    # Remote main/master delete (ported from HOME v1.5.0 — S519)
    (r"git\s+push\s+(?:origin|public)\s+--delete\s+(?:main|master)\b", "git push --delete main/master"),
    # Mirror push overwrites ALL remote branches incl. protected (ported from HOME v1.5.0 — S519)
    # Dual-repo workflows must use a sync script, never --mirror.
    (r"git\s+push\s+--mirror\b", "git push --mirror overwrites ALL remote branches (incl. main). Use a sync script, never --mirror."),
]

# ASK (confirm) - RISKY commands, ask for user confirmation
RISKY_PATTERNS = [
    (r"git\s+reset\s+--hard", "git reset --hard discards uncommitted changes"),
    (r"git\s+clean\s+-[a-zA-Z]*f", "git clean -f removes untracked files"),
    (r"git\s+checkout\s+\.\s*$", "git checkout . undoes all changes"),
    (r"git\s+restore\s+\.\s*$", "git restore . undoes all changes"),
    (r"git\s+branch\s+-D\s+", "git branch -D force-deletes branch"),
    (r"git\s+stash\s+drop", "git stash drop removes stash entry"),
    (r"chmod\s+777", "chmod 777 makes everything world-readable/writable"),
    (r"kill\s+-9\s+", "kill -9 forcefully terminates the process"),
    (r"docker\s+system\s+prune", "docker system prune removes Docker data"),
    (r"rm\s+-[a-zA-Z]*rf", "recursive forced removal"),
    # ---- Ported from HOME v1.5.0 (S519 P2.3 sandbox-off extension) ----
    # Regex copied VERBATIM (behaviour parity with the live hook); messages
    # localised to EN for the public package. Known FPs are kept verbatim and
    # NOT "improved" here (a fix belongs in HOME first): the `>` patterns also
    # match `>>` (append) and `~/.zshrc.bak` (the `\b` sits at the `c`->`.`
    # boundary). These are RISKY (ASK), so a FP costs one confirm, not a block.
    # Lesson: bash_validator_regex_antipattern (S519).
    (r"^[^#]*>\s*~/\.zshrc\b", "overwrite ~/.zshrc -- shell config (check backup first) -- S519"),
    (r"^[^#]*>\s*~/\.bashrc\b", "overwrite ~/.bashrc -- shell config (check backup first) -- S519"),
    (r"(?:curl|wget)\s+.*-[oO]\s+\S+\.sh\s+.*&&\s*(?:bash|sh|zsh)\s+\S+\.sh\b", "curl/wget download + shell exec -- review script before running -- S519"),
    (r"sudo\s+rm\s+/etc/\w+", "sudo rm on critical /etc/ system file -- S519"),
]

# SAFE rm -rf targets (no warning needed)
SAFE_RM_TARGETS = [
    r"node_modules/?",
    r"dist/?",
    r"build/?",
    r"\.cache/?",
    r"__pycache__/?",
    r"\.next/?",
    r"\.turbo/?",
    r"coverage/?",
    r"\.pytest_cache/?",
    r"\.mypy_cache/?",
    r"tmp/?",
    r"/tmp/",  # nosec B108
    r"\.tsbuildinfo",
    r"\.parcel-cache/?",
    r"venv/?",
    r"\.venv/?",
    r"eggs/?",
    r"\.eggs/?",
    r"\*\.pyc",
]


# ============================================================
# VALIDATION LOGIC
# ============================================================


def _get_all_patterns() -> tuple[list, list, list]:
    """Get all patterns (builtin + extra from config)."""
    extra_blocked, extra_risky, extra_safe = _load_extra_patterns()
    all_blocked = BLOCKED_PATTERNS + extra_blocked
    all_risky = RISKY_PATTERNS + extra_risky
    all_safe = SAFE_RM_TARGETS + extra_safe
    return all_blocked, all_risky, all_safe


def is_safe_rm_target(command: str, safe_targets: list | None = None) -> bool:
    """Check if rm -rf targets ONLY safe directories.

    Every path token must match a safe pattern (not just one anywhere in
    the line), and only the rm's own arguments are considered (parsing
    stops at the first command terminator / redirect).
    """
    match = re.search(r"rm\s+-[a-zA-Z]*rf[a-zA-Z]*\s+(.+)", command)
    if not match:
        return False

    targets = safe_targets if safe_targets is not None else SAFE_RM_TARGETS

    # Only this rm's arguments: stop at the first terminator/redirect
    target = re.split(r"[;|&<>]", match.group(1))[0]

    # Path tokens only — drop flags like -v, --, etc.
    tokens = [t for t in target.split() if not t.startswith("-")]
    if not tokens:
        return False

    # EVERY token must be safe, otherwise the rm is NOT a safe target
    return all(
        any(re.search(safe, tok) for safe in targets)
        for tok in tokens
    )


def check_blocked(command: str, patterns: list | None = None) -> str | None:
    """Check if command matches a BLOCKED pattern."""
    for pattern, reason in (patterns if patterns is not None else BLOCKED_PATTERNS):
        if re.search(pattern, command, re.IGNORECASE):
            return reason
    return None


def check_risky(command: str, patterns: list | None = None, safe_targets: list | None = None) -> str | None:
    """Check if command matches a RISKY pattern."""
    for pattern, reason in (patterns if patterns is not None else RISKY_PATTERNS):
        if re.search(pattern, command, re.IGNORECASE):
            if "rm" in pattern and is_safe_rm_target(command, safe_targets):
                return None
            return reason
    return None


def check_autofix(command: str) -> tuple[str | None, str | None]:
    """Check if command can be auto-fixed to a safer alternative."""
    # git push --force -> --force-with-lease
    if re.search(r"git\s+push.*--force", command, re.IGNORECASE):
        if re.search(r"\b(main|master)\b", command):
            return None, None
        if "--force-with-lease" in command:
            return None, None
        new_command = command.replace("--force", "--force-with-lease", 1)
        return new_command, "auto-fix: --force -> --force-with-lease (safer)"

    # git push -f -> --force-with-lease
    if re.search(r"git\s+push.*\s-f\s", command, re.IGNORECASE):
        if re.search(r"\b(main|master)\b", command):
            return None, None
        new_command = re.sub(r"\s-f\s", " --force-with-lease ", command, count=1)
        return new_command, "auto-fix: -f -> --force-with-lease (safer)"

    return None, None


def extract_subcommands(command: str) -> list[str]:
    """Extract sub-commands from $(), backticks, ;, &&, ||.

    Returns a list of sub-command strings that should also be validated.
    Does NOT include the original command (caller handles that).
    """
    subs = []

    # Extract $(...) contents (handles nested by using a simple bracket counter)
    i = 0
    while i < len(command):
        if command[i:i+2] == "$(" :
            depth = 1
            start = i + 2
            j = start
            while j < len(command) and depth > 0:
                if command[j:j+2] == "$(":
                    depth += 1
                    j += 2
                    continue
                if command[j] == ")":
                    depth -= 1
                    if depth == 0:
                        subs.append(command[start:j])
                        break
                j += 1
            i = j + 1
        else:
            i += 1

    # Extract `...` contents (backtick substitution, no nesting)
    for m in re.finditer(r"`([^`]+)`", command):
        subs.append(m.group(1))

    # Split on ; && || and validate each segment
    # (the original command is already checked, but segments hide things like:
    #  "echo ok; rm -rf /" or "true && DROP TABLE users")
    for part in re.split(r"\s*(?:;|&&|\|\|)\s*", command):
        stripped = part.strip()
        if stripped and stripped != command.strip():
            subs.append(stripped)

    return subs


def validate(command: str) -> dict | None:
    """Validate a bash command. Returns hook output dict or None (allow)."""
    if not command or not command.strip():
        return None

    all_blocked, all_risky, all_safe = _get_all_patterns()

    # Collect all commands to check: the original + any sub-commands
    commands_to_check = [command] + extract_subcommands(command)

    # 1. Check BLOCKED (across all commands/sub-commands)
    for cmd in commands_to_check:
        blocked_reason = check_blocked(cmd, all_blocked)
        if blocked_reason:
            return {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": (
                        f"BLOCKED: {blocked_reason}. "
                        f"Command: {command[:80]}"
                    ),
                }
            }

    # 2. Check AUTO-FIX (only on the original command)
    fixed_command, fix_reason = check_autofix(command)
    if fixed_command:
        return {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "allow",
                "permissionDecisionReason": fix_reason,
                "updatedInput": {"command": fixed_command},
            }
        }

    # 3. Check RISKY (across all commands/sub-commands)
    for cmd in commands_to_check:
        risky_reason = check_risky(cmd, all_risky, all_safe)
        if risky_reason:
            return {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "ask",
                    "permissionDecisionReason": (
                        f"WARNING: {risky_reason}. "
                        f"Confirm to proceed."
                    ),
                }
            }

    # 4. ALLOW (silent)
    return None


# ============================================================
# MAIN
# ============================================================


def main():
    """Entry point - reads hook input from stdin, outputs decision."""
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)

    command = hook_input.get("tool_input", {}).get("command", "")
    decision = validate(command)

    if decision:
        print(json.dumps(decision))

    sys.exit(0)


if __name__ == "__main__":
    main()
