#!/usr/bin/env python3
"""
memory_flush_auto.py - Auto-detect project and run memory-flush

Called by SessionEnd hook. Detects current project from CWD and
runs memory-flush.sh with correct arguments.

Version: 1.0.0
Date: 30 Gennaio 2026
"""

import os
import subprocess
import sys

# Project detection mapping
PROJECT_PATHS = {
    'CervellaSwarm': 'cervellaswarm',
    'miracollogeminifocus': 'miracollo',
    'ContabilitaAntigravity': 'contabilita',
}

def detect_project():
    """Detect project from current working directory."""
    cwd = os.getcwd()

    for path_fragment, project_name in PROJECT_PATHS.items():
        full_path = os.path.expanduser(f'~/Developer/{path_fragment}')
        if cwd.startswith(full_path):
            return project_name

    return None

def main():
    project = detect_project()

    if not project:
        # Silent exit if not in a known project
        sys.exit(0)

    # Run memory-flush.sh silently
    script_path = os.path.expanduser(
        '~/Developer/CervellaSwarm/scripts/swarm/memory-flush.sh'
    )

    if os.path.exists(script_path):
        try:
            subprocess.run(
                [script_path, project, 'auto', 'true'],
                capture_output=True,
                timeout=5
            )
        except Exception:
            pass  # Silent failure

if __name__ == '__main__':
    main()
