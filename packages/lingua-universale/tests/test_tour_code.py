"""Verify all Tour of LU code snippets pass check_source().

Prevents silent regressions when the parser changes.
Each tour step's LU code is validated against check_source().
Step 'verify-2-errors' is intentionally invalid (teaches error messages).
"""

import re
from pathlib import Path

import pytest

from cervellaswarm_lingua_universale import check_source

TOUR_JS = Path(__file__).resolve().parents[3] / "playground" / "tour.js"


def _extract_tour_codes():
    """Extract (step_id, code) pairs from tour.js."""
    content = TOUR_JS.read_text()

    # Extract code blocks by splitting on `code: \``
    parts = content.split("code: `")
    codes = []
    for part in parts[1:]:
        end = part.index("`,")
        code = part[:end].replace("\\n", "\n").replace("\\`", "`")
        codes.append(code)

    # Extract step IDs (skip chapter-level IDs)
    # Step IDs are inside steps arrays, chapter IDs are at chapter level
    # We match id: "..." that appears after a steps: [ context
    id_pattern = re.compile(r'id:\s*"([^"]+)"')
    all_ids = id_pattern.findall(content)

    # Chapter IDs are: types, agents, protocols, verification
    chapter_ids = {"types", "agents", "protocols", "verification"}
    step_ids = [i for i in all_ids if i not in chapter_ids]

    return list(zip(step_ids, codes))


def _extract_solution_codes():
    """Extract (step_id, solution_code) pairs from tour.js."""
    content = TOUR_JS.read_text()
    solutions = []

    # Find solution blocks: `solution: \`...\``
    parts = content.split("solution: `")
    for part in parts[1:]:
        end = part.index("`,")
        code = part[:end].replace("\\n", "\n").replace("\\`", "`")
        # Find the step ID by looking backwards for the nearest id: "..."
        # Get position in original content
        pos = content.index("solution: `" + part[:20])
        preceding = content[:pos]
        ids_before = re.findall(r'id:\s*"([^"]+)"', preceding)
        step_id = ids_before[-1] if ids_before else "unknown"
        solutions.append((step_id + "-solution", code))

    return solutions


TOUR_STEPS = _extract_tour_codes()
TOUR_SOLUTIONS = _extract_solution_codes()

# Step with intentional error (teaches error messages)
INTENTIONAL_ERROR_STEPS = {"verify-2-errors"}


@pytest.mark.parametrize(
    "step_id,code",
    TOUR_STEPS,
    ids=[s[0] for s in TOUR_STEPS],
)
def test_tour_step_valid(step_id, code):
    """Each tour step code must pass check_source(), except intentional errors."""
    result = check_source(code)

    if step_id in INTENTIONAL_ERROR_STEPS:
        assert not result.ok, (
            f"Tour step '{step_id}' is marked as intentional error "
            f"but check_source() passed. Update INTENTIONAL_ERROR_STEPS "
            f"or fix the step code."
        )
    else:
        assert result.ok, (
            f"Tour step '{step_id}' failed check_source():\n"
            f"{chr(10).join(result.errors)}"
        )


@pytest.mark.parametrize(
    "solution_id,code",
    TOUR_SOLUTIONS,
    ids=[s[0] for s in TOUR_SOLUTIONS],
)
def test_tour_solution_valid(solution_id, code):
    """Each exercise solution must pass check_source()."""
    result = check_source(code)
    assert result.ok, (
        f"Tour solution '{solution_id}' failed check_source():\n"
        f"{chr(10).join(result.errors)}"
    )
