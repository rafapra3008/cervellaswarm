#!/usr/bin/env python3
"""
Debug script per vedere cosa riceve il PostToolUse hook.
Salva TUTTO il payload in un file di log.
"""

import json
import sys
from datetime import datetime
from pathlib import Path

def main():
    log_file = Path(__file__).parent.parent.parent / "data" / "logs" / "hook_debug.log"
    log_file.parent.mkdir(parents=True, exist_ok=True)

    try:
        # Leggi TUTTO da stdin
        raw_input = sys.stdin.read()

        # Timestamp
        ts = datetime.now().isoformat()

        # Prova a parsare come JSON
        try:
            payload = json.loads(raw_input)
            formatted = json.dumps(payload, indent=2)
        except Exception:
            formatted = raw_input

        # Scrivi nel log
        with open(log_file, "a") as f:
            f.write(f"\n{'='*60}\n")
            f.write(f"TIMESTAMP: {ts}\n")
            f.write(f"{'='*60}\n")
            f.write(formatted)
            f.write(f"\n{'='*60}\n\n")

        # Output per hook
        print(json.dumps({"status": "debug_logged", "file": str(log_file)}))
        sys.exit(0)

    except Exception as e:
        print(json.dumps({"status": "error", "error": str(e)}))
        sys.exit(0)

if __name__ == "__main__":
    main()
