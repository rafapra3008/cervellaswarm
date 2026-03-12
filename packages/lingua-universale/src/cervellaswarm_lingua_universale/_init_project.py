# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Project scaffolding for Lingua Universale (T3.3).

Creates a minimal LU project with 3 files:

  - ``<name>.lu``       -- protocol skeleton with properties
  - ``<name>_test.lu``  -- example verification test
  - ``README.md``       -- one-paragraph project description

Design: one-shot, non-interactive, deno-init style.
ZERO external dependencies (pathlib + textwrap only).
"""

from __future__ import annotations

from pathlib import Path
from textwrap import dedent


# ============================================================
# Templates
# ============================================================


def _template_protocol(name: str) -> str:
    """Generate the main .lu protocol file."""
    # Convert project name to PascalCase for protocol/agent names
    pascal = "".join(word.capitalize() for word in name.replace("-", "_").split("_"))

    return dedent(f"""\
        type Status = Pending | Running | Done

        agent {pascal}Agent:
            role: worker
            trust: standard
            accepts: Request
            produces: Result

        protocol {pascal}:
            roles: requester, worker
            requester asks worker to do task
            worker returns result to requester
            properties:
                always terminates
                no deadlock
    """)


def _template_test(name: str) -> str:
    """Generate the test .lu file."""
    pascal = "".join(word.capitalize() for word in name.replace("-", "_").split("_"))

    return dedent(f"""\
        type TestStatus = Pass | Fail

        agent Verifier:
            role: auditor
            trust: verified
            accepts: VerifyRequest
            produces: VerifyResult

        protocol Verify{pascal}:
            roles: tester, verifier
            tester asks verifier to verify
            verifier returns verdict to tester
            properties:
                always terminates
                no deadlock
                all roles participate
    """)


def _template_readme(name: str) -> str:
    """Generate the README.md."""
    return dedent(f"""\
        # {name}

        A Lingua Universale project.

        ## Quick start

        ```bash
        lu check {name}.lu    # parse and compile
        lu verify {name}.lu   # formal verification
        lu run {name}.lu      # execute
        ```
    """)


# ============================================================
# Scaffolding logic
# ============================================================


def init_project(
    name: str,
    *,
    target_dir: Path | None = None,
    minimal: bool = False,
    force: bool = False,
) -> list[Path]:
    """Create a new LU project directory with scaffolding files.

    Args:
        name: Project name (used for filenames and protocol names).
        target_dir: Parent directory. Defaults to current working directory.
        minimal: If True, only create the .lu file (no README/test).
        force: If True, overwrite existing files.

    Returns:
        List of created file paths.

    Raises:
        FileExistsError: If the project directory is non-empty and force=False.
        ValueError: If name is empty or contains invalid characters.
    """
    stripped = name.replace("-", "").replace("_", "")
    if not name or not stripped.isalnum() or not stripped[0].isalpha():
        raise ValueError(
            f"Invalid project name: {name!r}. "
            "Must start with a letter and contain only "
            "alphanumeric characters, hyphens, or underscores."
        )

    base = (target_dir or Path.cwd()) / name
    created: list[Path] = []

    # Check for existing non-empty directory
    if base.exists() and any(base.iterdir()) and not force:
        raise FileExistsError(
            f"Directory {base} already exists and is not empty. "
            "Use --force to overwrite."
        )

    base.mkdir(parents=True, exist_ok=True)

    # Main protocol file
    lu_file = base / f"{name}.lu"
    lu_file.write_text(_template_protocol(name), encoding="utf-8")
    created.append(lu_file)

    if not minimal:
        # Test file
        test_file = base / f"{name}_test.lu"
        test_file.write_text(_template_test(name), encoding="utf-8")
        created.append(test_file)

        # README
        readme = base / "README.md"
        readme.write_text(_template_readme(name), encoding="utf-8")
        created.append(readme)

    return created
