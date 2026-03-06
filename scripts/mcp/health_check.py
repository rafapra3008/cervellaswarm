#!/usr/bin/env python3
"""
MCP Server Health Check - CervellaSwarm

Verifica lo stato del MCP server:
1. Build exists and not stale
2. Config correct in settings.json (main + insiders)
3. API key present
4. Node.js available and >= 18.0.0
5. Dependencies installed

Versione: 1.0.0
Data: 2026-02-10 - Sessione 352 (Step C.2)

Usage:
    python3 scripts/mcp/health_check.py [--verbose] [--auto-rebuild]
"""

__version__ = "1.0.0"
__version_date__ = "2026-02-10"

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional


# Paths
MCP_SERVER_DIR = Path(__file__).parent.parent.parent / "packages" / "mcp-server"
DIST_INDEX = MCP_SERVER_DIR / "dist" / "index.js"
SRC_INDEX = MCP_SERVER_DIR / "src" / "index.ts"
PACKAGE_JSON = MCP_SERVER_DIR / "package.json"
NODE_MODULES = MCP_SERVER_DIR / "node_modules"

SETTINGS_MAIN = Path.home() / ".claude" / "settings.json"
SETTINGS_INSIDERS = Path.home() / ".claude-insiders" / "settings.json"

CONFIG_DIR = Path.home() / ".config" / "cervellaswarm"
CONFIG_FILE = CONFIG_DIR / "config.json"


class HealthStatus:
    """Health check result."""
    OK = "OK"
    WARN = "WARN"
    FAIL = "FAIL"


def check_build_exists() -> tuple[str, str]:
    """Check if compiled build exists."""
    if not DIST_INDEX.exists():
        return HealthStatus.FAIL, f"Build mancante: {DIST_INDEX}"
    return HealthStatus.OK, f"Build presente: {DIST_INDEX.name}"


def check_build_stale() -> tuple[str, str]:
    """Check if build is older than source."""
    if not DIST_INDEX.exists() or not SRC_INDEX.exists():
        return HealthStatus.WARN, "Impossibile verificare staleness (file mancanti)"

    dist_mtime = os.path.getmtime(DIST_INDEX)
    src_mtime = os.path.getmtime(SRC_INDEX)

    if src_mtime > dist_mtime:
        return HealthStatus.WARN, "Build STALE: sorgente piu recente del compilato"
    return HealthStatus.OK, "Build aggiornato"


def check_node_version() -> tuple[str, str]:
    """Check Node.js version >= 18.0.0."""
    try:
        result = subprocess.run(
            ["node", "--version"],
            capture_output=True, text=True, timeout=5
        )
        version = result.stdout.strip().lstrip("v")
        major = int(version.split(".")[0])
        if major < 18:
            return HealthStatus.FAIL, f"Node.js {version} (richiesto >= 18.0.0)"
        return HealthStatus.OK, f"Node.js v{version}"
    except FileNotFoundError:
        return HealthStatus.FAIL, "Node.js non trovato"
    except Exception as e:
        return HealthStatus.FAIL, f"Errore check Node.js: {e}"


def check_dependencies() -> tuple[str, str]:
    """Check if node_modules exists."""
    if not NODE_MODULES.exists():
        return HealthStatus.FAIL, "node_modules mancante (eseguire npm install)"
    return HealthStatus.OK, "Dipendenze installate"


def check_settings_config(settings_path: Path) -> tuple[str, str]:
    """Check MCP config in settings.json."""
    if not settings_path.exists():
        return HealthStatus.WARN, f"Settings non trovato: {settings_path.name}"

    try:
        with open(settings_path) as f:
            settings = json.load(f)

        mcp_servers = settings.get("mcpServers", {})
        if "cervellaswarm" not in mcp_servers:
            return HealthStatus.FAIL, f"MCP 'cervellaswarm' non configurato in {settings_path.name}"

        config = mcp_servers["cervellaswarm"]
        command = config.get("command", "")
        args = config.get("args", [])

        if command == "node" and args:
            target = args[0]
            if not Path(target).exists():
                return HealthStatus.FAIL, f"Target build non esiste: {target}"
            return HealthStatus.OK, f"Config OK in {settings_path.name}"
        elif command == "cervellaswarm-mcp":
            return HealthStatus.OK, f"Config OK (published package) in {settings_path.name}"
        else:
            return HealthStatus.WARN, f"Config inattesa in {settings_path.name}: command={command}"

    except json.JSONDecodeError:
        return HealthStatus.FAIL, f"JSON invalido: {settings_path.name}"
    except Exception as e:
        return HealthStatus.FAIL, f"Errore lettura {settings_path.name}: {e}"


def check_api_key() -> tuple[str, str]:
    """Check if API key is available.

    Necessaria per spawn-worker (spawner.ts usa Anthropic client direttamente).
    Non necessaria per gli altri tools (check_status, list_workers, ecc.).
    """
    # Check environment variable first
    env_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if env_key and env_key.startswith("sk-ant-"):
        return HealthStatus.OK, "API key presente (env ANTHROPIC_API_KEY)"

    # Check config file
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE) as f:
                config = json.load(f)
            key = config.get("apiKey", "")
            if key and key.startswith("sk-ant-"):
                return HealthStatus.OK, "API key presente (config file)"
        except Exception:
            pass

    return HealthStatus.WARN, "API key non trovata (necessaria per spawn-worker)"


def check_server_version() -> tuple[str, str]:
    """Check server version from package.json."""
    if not PACKAGE_JSON.exists():
        return HealthStatus.WARN, "package.json mancante"

    try:
        with open(PACKAGE_JSON) as f:
            pkg = json.load(f)
        version = pkg.get("version", "unknown")
        return HealthStatus.OK, f"Versione: {version}"
    except Exception as e:
        return HealthStatus.WARN, f"Errore lettura versione: {e}"


def auto_rebuild() -> tuple[str, str]:
    """Attempt to rebuild the MCP server."""
    try:
        result = subprocess.run(
            ["npm", "run", "build"],
            capture_output=True, text=True, timeout=30,
            cwd=str(MCP_SERVER_DIR)
        )
        if result.returncode == 0:
            return HealthStatus.OK, "Auto-rebuild completato con successo"
        return HealthStatus.FAIL, f"Auto-rebuild fallito: {result.stderr[:100]}"
    except Exception as e:
        return HealthStatus.FAIL, f"Auto-rebuild errore: {e}"


def is_cervellaswarm_context() -> bool:
    """Check if current working directory is within the CervellaSwarm project."""
    try:
        cwd = os.getcwd()
        return "CervellaSwarm" in cwd
    except Exception:
        # Graceful fallback: if CWD cannot be determined, assume we are in context
        return True


def main():
    """Run all health checks."""
    verbose = "--verbose" in sys.argv
    do_rebuild = "--auto-rebuild" in sys.argv
    hook_mode = "--hook" in sys.argv

    # In hook mode: skip silently if not in CervellaSwarm context
    if hook_mode and not is_cervellaswarm_context():
        print(json.dumps({}))
        sys.exit(0)

    checks = [
        ("Build", check_build_exists),
        ("Build Stale", check_build_stale),
        ("Node.js", check_node_version),
        ("Dependencies", check_dependencies),
        ("Settings (main)", lambda: check_settings_config(SETTINGS_MAIN)),
        ("Settings (insiders)", lambda: check_settings_config(SETTINGS_INSIDERS)),
        ("API Key", check_api_key),
        ("Version", check_server_version),
    ]

    results = []
    has_fail = False
    has_warn = False

    for name, check_fn in checks:
        status, detail = check_fn()
        results.append((name, status, detail))
        if status == HealthStatus.FAIL:
            has_fail = True
        elif status == HealthStatus.WARN:
            has_warn = True

    # Auto-rebuild if stale and requested
    if do_rebuild:
        for name, status, detail in results:
            if name == "Build Stale" and status == HealthStatus.WARN:
                rebuild_status, rebuild_detail = auto_rebuild()
                results.append(("Auto-Rebuild", rebuild_status, rebuild_detail))
                break

    # Hook mode: output JSON for Claude Code hook
    if hook_mode:
        if has_fail or has_warn:
            issues = [f"- [{s}] {n}: {d}" for n, s, d in results if s != HealthStatus.OK]
            severity = "FAIL" if has_fail else "WARN"
            context = f"## MCP Health {severity}\n" + "\n".join(issues)
            print(json.dumps({
                "hookSpecificOutput": {
                    "hookEventName": "SessionStart",
                    "additionalContext": context
                }
            }))
        else:
            # Silence if all OK
            print(json.dumps({}))
        sys.exit(0)

    # CLI mode: human-readable output
    print(f"MCP Server Health Check v{__version__}")
    print(f"Server: {MCP_SERVER_DIR}")
    print("=" * 50)

    for name, status, detail in results:
        icon = {"OK": "[OK]", "WARN": "[!!]", "FAIL": "[XX]"}[status]
        print(f"  {icon} {name}: {detail}")

    print("=" * 50)

    if has_fail:
        print("STATUS: FAIL - Azione richiesta!")
        sys.exit(1)
    elif has_warn:
        print("STATUS: WARN - Controllare i warning")
        sys.exit(0)
    else:
        print("STATUS: OK - Tutto funzionante")
        sys.exit(0)


if __name__ == "__main__":
    main()
