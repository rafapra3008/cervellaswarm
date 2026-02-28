# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors
"""Test TextMate grammar coverage against all .lu example files.

This script validates that the TextMate grammar has rules that match
every significant construct in the Lingua Universale language by
testing regex patterns from the grammar against actual .lu files.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

GRAMMAR_PATH = Path(__file__).parent.parent / "syntaxes" / "lingua-universale.tmLanguage.json"
EXAMPLES_DIR = Path(__file__).parent.parent.parent.parent / "packages" / "lingua-universale" / "examples"

# Constructs that MUST be highlighted in each file
EXPECTED_CONSTRUCTS: dict[str, list[str]] = {
    "hello.lu": [
        "type-declaration",      # type TaskStatus = Pending | Running | Done
        "agent-declaration",     # agent Worker:
        "agent-clauses",         # role:, trust:, accepts:, etc.
        "protocol-declaration",  # protocol DelegateTask:
        "roles-declaration",     # roles: regina, worker, guardiana
        "protocol-step",         # regina asks worker to do task
        "properties-block",      # properties:
        "property-keywords",     # always terminates, no deadlock
        "trust-tiers",           # standard
    ],
    "confidence.lu": [
        "comment",               # # SPDX-License-Identifier...
        "type-declaration",      # type AnalysisStatus = ...
        "record-type-declaration",  # type AnalysisResult =
        "agent-declaration",     # agent Analyst:
        "agent-clauses",         # role:, trust:, etc.
        "protocol-declaration",  # protocol ConfidenceReview:
        "when-block",            # when reviewer decides:
        "choice-branch",         # approve:, needs_revision:
        "protocol-step",         # analyst returns report to regina
        "property-keywords",     # confidence >= high, trust >= standard
        "trust-tiers",           # verified
        "builtin-types",         # String, Number, List, Confident
        "confidence-levels",     # Certain, High (in properties)
    ],
    "multiagent.lu": [
        "use-statement",         # use python datetime
        "type-declaration",      # type Priority = Critical | High | ...
        "record-type-declaration",  # type DeploymentPlan =
        "agent-declaration",     # agent Architect:
        "agent-clauses",         # role:, trust:, etc.
        "protocol-declaration",  # protocol DeployPipeline:
        "when-block",            # when regina decides:
        "choice-branch",         # approve:, reject:
        "protocol-step",         # regina asks architect to plan deployment
        "property-keywords",     # all roles participate, X before Y, X cannot send Y
        "logical-operators",     # and
        "builtin-types",         # String, Boolean, Number, List
        "number",                # (in expressions)
    ],
    "ricette.lu": [
        "comment",               # # SPDX...
        "type-declaration",      # type Category = Antipasto | ...
        "record-type-declaration",  # type Recipe =
        "agent-declaration",     # agent RecipeManager:
        "protocol-declaration",  # protocol AddRecipe:
        "protocol-step",         # nonna asks manager to do save recipe
        "property-keywords",     # manager before checker
        "builtin-types",         # String, Number, List
    ],
    "errors.lu": [
        "comment",               # # SPDX..., # Intentionally Broken
        "type-declaration",      # type Mood = Happy | Sad
        "agent-declaration",     # agent BrokenBot:
        "agent-clauses",         # role:, trust:, accepts:
    ],
}


def load_grammar() -> dict:
    with open(GRAMMAR_PATH) as f:
        return json.load(f)


def extract_patterns(grammar: dict, rule_name: str) -> list[str]:
    """Extract regex patterns from a grammar rule."""
    repo = grammar.get("repository", {})
    rule = repo.get(rule_name, {})

    patterns_list: list[str] = []

    # Direct match
    if "match" in rule:
        patterns_list.append(rule["match"])

    # Nested patterns
    for pat in rule.get("patterns", []):
        if "match" in pat:
            patterns_list.append(pat["match"])
        if "begin" in pat:
            patterns_list.append(pat["begin"])

    # begin/end (e.g., strings)
    if "begin" in rule:
        patterns_list.append(rule["begin"])

    return patterns_list


def test_rule_matches_file(grammar: dict, rule_name: str, content: str) -> bool:
    """Test if at least one pattern from a rule matches something in the file."""
    patterns = extract_patterns(grammar, rule_name)

    for pattern in patterns:
        try:
            if re.search(pattern, content, re.MULTILINE):
                return True
        except re.error:
            # Some TextMate patterns may not be valid Python regex
            pass

    return False


def main() -> int:
    grammar = load_grammar()
    failures: list[str] = []
    total_checks = 0
    passed_checks = 0

    print("=" * 60)
    print("TextMate Grammar Coverage Test")
    print("=" * 60)

    for filename, expected_rules in EXPECTED_CONSTRUCTS.items():
        filepath = EXAMPLES_DIR / filename
        if not filepath.exists():
            failures.append(f"MISSING FILE: {filepath}")
            continue

        content = filepath.read_text()
        print(f"\n--- {filename} ---")

        for rule_name in expected_rules:
            total_checks += 1
            matched = test_rule_matches_file(grammar, rule_name, content)

            if matched:
                passed_checks += 1
                print(f"  [PASS] {rule_name}")
            else:
                failures.append(f"{filename}: rule '{rule_name}' did not match")
                print(f"  [FAIL] {rule_name}")

    print("\n" + "=" * 60)
    print(f"Results: {passed_checks}/{total_checks} checks passed")

    if failures:
        print(f"\n{len(failures)} FAILURES:")
        for f in failures:
            print(f"  - {f}")
        return 1

    print("\nAll grammar rules match their expected constructs!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
