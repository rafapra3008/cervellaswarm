#!/usr/bin/env python3
"""
LaunchAgent Health Check - CervellaSwarm

Verifica lo stato dei LaunchAgent di tutti i progetti:
1. Exit code (launchctl list)
2. Script referenziato esiste
3. Path nei plist validi
4. Log file size (warning se > 10MB)

Versione: 1.0.0
Data: 2026-02-10 - Sessione 352 (Step C.3)

Usage:
    python3 scripts/mcp/launchagent_health.py [--verbose] [--hook]
"""

__version__ = "1.0.0"
__version_date__ = "2026-02-10"

import json
import os
import plistlib
import subprocess
import sys
from pathlib import Path
from typing import Optional


# Our LaunchAgent prefixes
AGENT_PREFIXES = ["com.miracollook.", "com.cervellaswarm."]
LAUNCH_AGENTS_DIR = Path.home() / "Library" / "LaunchAgents"
LOG_SIZE_WARN_MB = 10


class Status:
    OK = "OK"
    WARN = "WARN"
    FAIL = "FAIL"


def get_our_plists() -> list[Path]:
    """Find all our LaunchAgent plist files."""
    plists = []
    if not LAUNCH_AGENTS_DIR.exists():
        return plists
    for prefix in AGENT_PREFIXES:
        plists.extend(LAUNCH_AGENTS_DIR.glob(f"{prefix}*.plist"))
    return sorted(plists)


def parse_plist(plist_path: Path) -> Optional[dict]:
    """Parse a plist file. Uses plutil as fallback for XML with comments."""
    try:
        with open(plist_path, "rb") as f:
            return plistlib.load(f)
    except Exception:
        # Fallback: use plutil to convert to json
        try:
            result = subprocess.run(
                ["plutil", "-convert", "json", "-o", "-", str(plist_path)],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                return json.loads(result.stdout)
        except Exception:
            pass
        return None


def get_launchctl_status() -> dict[str, tuple[int, Optional[int]]]:
    """Get exit codes from launchctl list. Returns {label: (pid, exit_code)}."""
    statuses = {}
    try:
        result = subprocess.run(
            ["launchctl", "list"],
            capture_output=True, text=True, timeout=5
        )
        for line in result.stdout.strip().split("\n")[1:]:  # Skip header
            parts = line.split("\t")
            if len(parts) >= 3:
                pid_str, exit_code_str, label = parts[0], parts[1], parts[2]
                for prefix in AGENT_PREFIXES:
                    if label.startswith(prefix):
                        pid = int(pid_str) if pid_str != "-" else None
                        exit_code = int(exit_code_str) if exit_code_str != "-" else None
                        statuses[label] = (pid, exit_code)
    except Exception:
        pass
    return statuses


def extract_program(plist_data: dict) -> Optional[str]:
    """Extract the executable path from plist."""
    if "Program" in plist_data:
        return plist_data["Program"]
    if "ProgramArguments" in plist_data:
        args = plist_data["ProgramArguments"]
        if args:
            # For scripts run via bash/python, check the script path
            for arg in args:
                if arg.endswith((".sh", ".py")) and "/" in arg:
                    return arg
            return args[0]
    return None


def check_log_size(path_str: str) -> Optional[tuple[str, str]]:
    """Check if a log file is too large."""
    if not path_str:
        return None
    p = Path(path_str)
    if not p.exists():
        return None
    size_mb = p.stat().st_size / (1024 * 1024)
    if size_mb > LOG_SIZE_WARN_MB:
        return Status.WARN, f"Log {p.name}: {size_mb:.0f}MB (> {LOG_SIZE_WARN_MB}MB)"
    return None


def check_agent(plist_path: Path, launchctl_statuses: dict) -> list[tuple[str, str, str]]:
    """Check a single LaunchAgent. Returns list of (check_name, status, detail)."""
    results = []
    label = plist_path.stem

    # Parse plist
    plist_data = parse_plist(plist_path)
    if plist_data is None:
        results.append((label, Status.FAIL, "Plist non leggibile"))
        return results

    # Check exit code
    if label in launchctl_statuses:
        pid, exit_code = launchctl_statuses[label]
        if exit_code is not None and exit_code != 0:
            running = f"PID {pid}" if pid else "non running"
            results.append((label, Status.FAIL, f"Exit code: {exit_code} ({running})"))
        elif pid:
            results.append((label, Status.OK, f"Running (PID {pid})"))
        else:
            results.append((label, Status.OK, f"Ultimo exit: 0"))
    else:
        results.append((label, Status.WARN, "Non in launchctl list"))

    # Check script exists
    program = extract_program(plist_data)
    if program:
        program_path = Path(os.path.expanduser(program))
        if not program_path.exists():
            results.append((f"  script", Status.FAIL, f"Non esiste: {program}"))
        else:
            results.append((f"  script", Status.OK, f"Esiste: {program_path.name}"))
    else:
        results.append((f"  script", Status.WARN, "Nessun programma trovato nel plist"))

    # Check log sizes
    for key in ["StandardOutPath", "StandardErrorPath"]:
        log_path = plist_data.get(key)
        if log_path:
            log_issue = check_log_size(log_path)
            if log_issue:
                results.append((f"  log", log_issue[0], log_issue[1]))

    return results


def main():
    """Run LaunchAgent health checks."""
    verbose = "--verbose" in sys.argv
    hook_mode = "--hook" in sys.argv

    plists = get_our_plists()
    launchctl_statuses = get_launchctl_status()

    all_results = []
    has_fail = False
    has_warn = False

    for plist_path in plists:
        agent_results = check_agent(plist_path, launchctl_statuses)
        all_results.extend(agent_results)
        for _, status, _ in agent_results:
            if status == Status.FAIL:
                has_fail = True
            elif status == Status.WARN:
                has_warn = True

    # Hook mode
    if hook_mode:
        if has_fail:
            issues = [f"- [{s}] {n}: {d}" for n, s, d in all_results if s != Status.OK]
            context = "## LaunchAgent Health FAIL\n" + "\n".join(issues)
            print(json.dumps({
                "hookSpecificOutput": {
                    "hookEventName": "SessionStart",
                    "additionalContext": context
                }
            }))
        else:
            print(json.dumps({}))
        sys.exit(0)

    # CLI mode
    print(f"LaunchAgent Health Check v{__version__}")
    print(f"Directory: {LAUNCH_AGENTS_DIR}")
    print(f"Agenti trovati: {len(plists)}")
    print("=" * 55)

    for name, status, detail in all_results:
        icon = {"OK": "[OK]", "WARN": "[!!]", "FAIL": "[XX]"}[status]
        print(f"  {icon} {name}: {detail}")

    print("=" * 55)

    if has_fail:
        print("STATUS: FAIL - Azione richiesta!")
        sys.exit(1)
    elif has_warn:
        print("STATUS: WARN - Controllare i warning")
        sys.exit(0)
    else:
        print("STATUS: OK - Tutti gli agenti funzionanti")
        sys.exit(0)


if __name__ == "__main__":
    main()
