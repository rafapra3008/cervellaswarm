#!/usr/bin/env python3
"""verify-hooks.py - Verifica integrita di tutti gli hook Claude Code

Legge settings.json (main + insiders) e verifica:
1. File esiste
2. File e eseguibile (per .sh) o leggibile (per .py)
3. Rileva file .DISABLED
4. Confronta main vs insiders per divergenze
5. Verifica MCP server e statusLine

Output: Report con status OK / BROKEN / DISABLED / NOT_EXEC per ogni hook
Exit code: 0 = tutto OK, 1 = problemi trovati
"""

import json
import os
import sys
from typing import Optional

# Paths
MAIN_SETTINGS = os.path.expanduser("~/.claude/settings.json")
INSIDERS_SETTINGS = os.path.expanduser("~/.claude-insiders/settings.json")


def extract_hook_files(settings_data: dict) -> list[dict]:
    """Extract all file paths referenced in hook commands."""
    files = []
    hooks = settings_data.get("hooks", {})

    for event_type, matchers in hooks.items():
        for matcher_group in matchers:
            matcher = matcher_group.get("matcher", "")
            for hook in matcher_group.get("hooks", []):
                command = hook.get("command", "")
                file_path = _extract_file_path(command)
                if file_path:
                    files.append({
                        "path": file_path,
                        "event": event_type,
                        "matcher": matcher,
                        "is_async": hook.get("async", False),
                    })

    # statusLine
    status_line = settings_data.get("statusLine", {})
    if status_line.get("type") == "command":
        file_path = _extract_file_path(status_line.get("command", ""))
        if file_path:
            files.append({
                "path": file_path,
                "event": "statusLine",
                "matcher": "",
                "is_async": False,
            })

    # MCP servers
    mcp = settings_data.get("mcpServers", {})
    for name, config in mcp.items():
        args = config.get("args", [])
        for arg in args:
            if isinstance(arg, str) and os.path.isabs(arg) and "." in os.path.basename(arg):
                files.append({
                    "path": arg,
                    "event": f"mcpServer:{name}",
                    "matcher": "",
                    "is_async": False,
                })
                break

    return files


def _extract_file_path(command: str) -> Optional[str]:
    """Extract file path from a hook command string."""
    if not command:
        return None

    parts = command.split()
    for part in parts:
        # Clean quotes
        part = part.strip("'\"")
        if os.path.isabs(part) and ("." in os.path.basename(part)):
            # Skip osascript arguments
            if "display notification" in command and part == parts[0]:
                continue
            return part
    return None


def check_file(path: str) -> str:
    """Check status of a hook file."""
    disabled_path = path + ".DISABLED"
    has_disabled = os.path.exists(disabled_path)
    has_active = os.path.exists(path)

    if has_disabled and not has_active:
        return "DISABLED"

    if not has_active:
        return "BROKEN"

    if path.endswith(".sh") and not os.access(path, os.X_OK):
        return "NOT_EXEC"

    return "OK"


def main() -> int:
    verbose = "--verbose" in sys.argv or "-v" in sys.argv

    results = {}
    all_paths_by_source = {}

    for label, settings_path in [("main", MAIN_SETTINGS), ("insiders", INSIDERS_SETTINGS)]:
        if not os.path.exists(settings_path):
            print(f"  [SKIP] {label}: settings.json non trovato")
            continue

        try:
            with open(settings_path) as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"  [ERROR] {label}: settings.json malformato: {e}")
            continue

        files = extract_hook_files(data)
        seen = set()
        source_results = []

        for file_info in files:
            path = file_info["path"]
            if path in seen:
                continue
            seen.add(path)

            status = check_file(path)
            source_results.append({**file_info, "status": status})

        results[label] = source_results
        all_paths_by_source[label] = seen

    # Print report
    print("=" * 70)
    print("  HOOK INTEGRITY CHECK - CervellaSwarm")
    print("=" * 70)

    total_ok = 0
    total_broken = 0
    total_disabled = 0
    total_not_exec = 0

    for label in ["main", "insiders"]:
        if label not in results:
            continue

        short_settings = MAIN_SETTINGS if label == "main" else INSIDERS_SETTINGS
        short_settings = short_settings.replace(os.path.expanduser("~"), "~")
        print(f"\n--- {label.upper()} ({short_settings}) ---\n")

        # Sort: BROKEN first, then DISABLED, NOT_EXEC, OK
        priority = {"BROKEN": 0, "DISABLED": 1, "NOT_EXEC": 2, "OK": 3}
        sorted_results = sorted(results[label], key=lambda x: (priority.get(x["status"], 9), x["event"]))

        for r in sorted_results:
            status = r["status"]
            short_path = r["path"].replace(os.path.expanduser("~"), "~")
            event = r["event"]
            matcher = f"[{r['matcher']}]" if r["matcher"] else ""
            async_tag = " (async)" if r["is_async"] else ""

            if status == "OK":
                icon = "OK"
                total_ok += 1
            elif status == "BROKEN":
                icon = "BROKEN"
                total_broken += 1
            elif status == "DISABLED":
                icon = "DISABLED"
                total_disabled += 1
            elif status == "NOT_EXEC":
                icon = "NOT_EXEC"
                total_not_exec += 1

            if verbose:
                print(f"  [{icon:8s}] {event}{matcher}{async_tag}")
                print(f"            {short_path}")
            else:
                print(f"  [{icon:8s}] {event:25s} {short_path}")

    # Divergence check
    main_paths = all_paths_by_source.get("main", set())
    insiders_paths = all_paths_by_source.get("insiders", set())

    only_main = main_paths - insiders_paths
    only_insiders = insiders_paths - main_paths

    if only_main or only_insiders:
        print(f"\n--- DIVERGENZE main vs insiders ---\n")
        for p in sorted(only_main):
            short = p.replace(os.path.expanduser("~"), "~")
            print(f"  [ONLY_MAIN]     {short}")
        for p in sorted(only_insiders):
            short = p.replace(os.path.expanduser("~"), "~")
            print(f"  [ONLY_INSIDERS] {short}")

    # Summary
    total = total_ok + total_broken + total_disabled + total_not_exec
    print(f"\n{'=' * 70}")
    print(f"  SUMMARY: {total} hook files checked")
    print(f"  OK: {total_ok}  |  BROKEN: {total_broken}  |  DISABLED: {total_disabled}  |  NOT_EXEC: {total_not_exec}")

    if total_broken > 0 or total_not_exec > 0:
        print(f"\n  ATTENZIONE: {total_broken + total_not_exec} hook richiedono intervento!")
        return 1
    elif total_disabled > 0:
        print(f"\n  Nota: {total_disabled} hook disabilitati (verificare se intenzionale)")
        return 0
    else:
        print(f"\n  Tutti gli hook sono integri!")
        return 0


if __name__ == "__main__":
    sys.exit(main())
