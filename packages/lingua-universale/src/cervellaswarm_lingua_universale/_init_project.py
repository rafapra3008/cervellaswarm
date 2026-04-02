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
# Standard Library template support
# ============================================================

_STDLIB_DIR = Path(__file__).resolve().parent / "stdlib"


def list_templates() -> list[str]:
    """Return available stdlib template names (e.g. 'rag_pipeline')."""
    templates: list[str] = []
    if not _STDLIB_DIR.is_dir():
        return templates
    for category_dir in sorted(_STDLIB_DIR.iterdir()):
        if category_dir.is_dir() and not category_dir.name.startswith("."):
            for lu_file in sorted(category_dir.glob("*.lu")):
                templates.append(lu_file.stem)
    return templates


def _find_template(template_name: str) -> Path | None:
    """Find a stdlib template .lu file by name."""
    if not _STDLIB_DIR.is_dir():
        return None
    for category_dir in _STDLIB_DIR.iterdir():
        if category_dir.is_dir():
            candidate = category_dir / f"{template_name}.lu"
            if candidate.exists():
                return candidate
    return None


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
    template: str | None = None,
) -> list[Path]:
    """Create a new LU project directory with scaffolding files.

    Args:
        name: Project name (used for filenames and protocol names).
        target_dir: Parent directory. Defaults to current working directory.
        minimal: If True, only create the .lu file (no README/test).
        force: If True, overwrite existing files.
        template: If provided, copy a stdlib template instead of generating
            a default skeleton. Use :func:`list_templates` to see options.

    Returns:
        List of created file paths.

    Raises:
        FileExistsError: If the project directory is non-empty and force=False.
        ValueError: If name is empty, contains invalid characters,
            or template not found.
    """
    stripped = name.replace("-", "").replace("_", "")
    if not name or not stripped.isalnum() or not stripped[0].isalpha():
        raise ValueError(
            f"Invalid project name: {name!r}. "
            "Must start with a letter and contain only "
            "alphanumeric characters, hyphens, or underscores."
        )

    # Resolve stdlib template if requested
    template_content: str | None = None
    if template is not None:
        template_path = _find_template(template)
        if template_path is None:
            available = ", ".join(list_templates()) or "(none found)"
            raise ValueError(
                f"Template {template!r} not found. "
                f"Available: {available}"
            )
        template_content = template_path.read_text(encoding="utf-8")

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
    lu_file.write_text(
        template_content if template_content else _template_protocol(name),
        encoding="utf-8",
    )
    created.append(lu_file)

    if not minimal:
        # Test file (always generated, not from template)
        test_file = base / f"{name}_test.lu"
        test_file.write_text(_template_test(name), encoding="utf-8")
        created.append(test_file)

        # README
        readme = base / "README.md"
        readme.write_text(_template_readme(name), encoding="utf-8")
        created.append(readme)

    return created
