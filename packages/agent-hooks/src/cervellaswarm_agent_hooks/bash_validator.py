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

__version__ = "1.0.0"


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
    except Exception:
        return [], [], []

# ============================================================
# PATTERNS - Commands to block / warn about
# ============================================================

# BLOCK (deny) - IRREVERSIBLE commands, never execute
BLOCKED_PATTERNS = [
    # Filesystem destruction
    (r"rm\s+(-[a-zA-Z]*f[a-zA-Z]*\s+)?/(\s|$)", "rm on root /"),
    (r"rm\s+(-[a-zA-Z]*f[a-zA-Z]*\s+)?~/", "rm on home ~/"),
    (r"rm\s+-[a-zA-Z]*rf[a-zA-Z]*\s+\.\s*$", "rm -rf . (current directory)"),
    (r"rm\s+-[a-zA-Z]*rf[a-zA-Z]*\s+\.\.", "rm -rf .. (parent directory)"),
    # Git force push to main/master
    (r"git\s+push\s+.*--force\s+.*\b(main|master)\b", "force push to main/master"),
    (r"git\s+push\s+.*-f\s+.*\b(main|master)\b", "force push to main/master"),
    (r"git\s+push\s+--force\s+\S+\s+(main|master)", "force push to main/master"),
    (r"git\s+push\s+-f\s+\S+\s+(main|master)", "force push to main/master"),
    # SQL destruction
    (r"DROP\s+TABLE", "DROP TABLE"),
    (r"DROP\s+DATABASE", "DROP DATABASE"),
    (r"TRUNCATE\s+TABLE", "TRUNCATE TABLE"),
    # System destruction
    (r"mkfs\.", "filesystem format"),
    (r"dd\s+if=.+of=/dev/", "raw write to device"),
    (r":\(\)\s*\{\s*:\s*\|\s*:\s*&\s*\}\s*;", "fork bomb"),
    (r">\s*/dev/sd[a-z]", "device overwrite"),
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
    r"/tmp/",
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
    """Check if rm -rf targets a safe directory."""
    match = re.search(r"rm\s+-[a-zA-Z]*rf[a-zA-Z]*\s+(.+)", command)
    if not match:
        return False

    target = match.group(1).strip()
    targets = safe_targets if safe_targets is not None else SAFE_RM_TARGETS
    return any(re.search(safe, target) for safe in targets)


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
