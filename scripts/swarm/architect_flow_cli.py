#!/usr/bin/env python3
"""CLI entry point for Architect Flow.

Extracted from architect_flow.py (S342) to keep library under 500 lines.
"""

import sys
from pathlib import Path

# Aggiungi root al path per import
_root = Path(__file__).parent.parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from scripts.swarm.architect_flow import (
    route_task, validate_plan_file
)


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python architect_flow.py route '<task description>'")
        print("  python architect_flow.py validate <plan.md>")
        print("\nExamples:")
        print("  python architect_flow.py route 'refactor auth module'")
        print("  python architect_flow.py validate .swarm/plans/PLAN_001.md")
        sys.exit(1)

    command = sys.argv[1]

    if command == "route":
        if len(sys.argv) < 3:
            print("Error: task description required")
            sys.exit(1)

        task = " ".join(sys.argv[2:])
        decision = route_task(task)

        print(f"\nTask: {task}")
        print(f"{'='*60}")
        print(f"Use Architect:    {decision.use_architect}")
        print(f"Complexity:       {decision.classification.complexity.value}")
        print(f"Confidence:       {decision.classification.confidence:.2f}")
        print(f"Reason:           {decision.reason}")
        if decision.suggested_workers:
            workers = [w.value for w in decision.suggested_workers]
            print(f"Suggested Workers: {', '.join(workers)}")

    elif command == "validate":
        if len(sys.argv) < 3:
            print("Error: plan path required")
            sys.exit(1)

        plan_path = Path(sys.argv[2])
        result = validate_plan_file(plan_path)

        print(f"\nValidating: {plan_path}")
        print(f"{'='*60}")
        print(f"Valid:    {result.is_valid}")
        print(f"Score:    {result.score:.1f}/10")

        if result.errors:
            print(f"\nErrors:")
            for e in result.errors:
                print(f"  - {e}")

        if result.warnings:
            print(f"\nWarnings:")
            for w in result.warnings:
                print(f"  - {w}")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
