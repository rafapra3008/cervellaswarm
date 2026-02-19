# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""
Project initialization, discovery, and management for session memory.

Handles creating new project structures from templates, discovering
existing projects, and archiving old session states.
"""

import shutil
from dataclasses import dataclass, field
from datetime import date as date_type
from importlib import resources
from pathlib import Path

from cervellaswarm_session_memory.config import DEFAULTS, load_config, get_memory_dir


@dataclass
class ProjectInfo:
    """Represents a discovered or initialized project."""

    name: str
    memory_dir: Path
    state_file: Path
    compass_file: Path | None = None
    archive_dir: Path = field(default_factory=lambda: Path("."))

    def __post_init__(self):
        if self.archive_dir == Path("."):
            self.archive_dir = self.memory_dir / self.name / "archive"


def normalize_name(name: str) -> str:
    """Normalize a project name to a consistent format.

    Converts to lowercase, replaces spaces and special chars with hyphens.

    Args:
        name: Raw project name.

    Returns:
        Normalized name (lowercase, hyphens).
    """
    result = name.strip().lower()
    result = result.replace(" ", "-").replace("_", "-")
    # Remove consecutive hyphens
    while "--" in result:
        result = result.replace("--", "-")
    return result.strip("-")


def init_project(
    name: str,
    project_root: Path | None = None,
    memory_dir: str | None = None,
    session_number: int = 1,
    description: str = "",
    create_compass: bool = True,
) -> ProjectInfo:
    """Initialize a new project with session memory structure.

    Creates the memory directory, session state file from template,
    and optionally a project compass file.

    Args:
        name: Project name.
        project_root: Root directory for the project. Defaults to CWD.
        memory_dir: Override for memory directory name.
        session_number: Starting session number.
        description: Project description for compass file.
        create_compass: Whether to create PROJECT_COMPASS.md.

    Returns:
        ProjectInfo with paths to created files.

    Raises:
        FileExistsError: If project already exists.
    """
    normalized = normalize_name(name)
    root = project_root if project_root else Path.cwd()
    config = load_config()

    mem_dir_name = memory_dir if memory_dir else config.get("memory_dir", DEFAULTS["memory_dir"])
    mem_dir = root / mem_dir_name

    project_dir = mem_dir / normalized
    if project_dir.exists():
        raise FileExistsError(f"Project already exists: {project_dir}")

    # Create directories
    project_dir.mkdir(parents=True, exist_ok=True)
    archive_dir = project_dir / "archive"
    archive_dir.mkdir(exist_ok=True)

    # Render session state template
    state_filename = config.get("state_file", DEFAULTS["state_file"])
    state_file_name = f"{state_filename.rsplit('.', 1)[0]}_{normalized}.md"
    state_file = project_dir / state_file_name

    today = date_type.today().isoformat()
    variables = {
        "project_name": name,
        "project_name_lower": normalized,
        "date": today,
        "session_number": str(session_number),
        "status": "Getting started",
        "session_title": "Project Setup",
        "task_placeholder": "Initialize project",
        "decision_placeholder": "Use session memory",
        "choice_placeholder": "cervellaswarm-session-memory",
        "reason_placeholder": "Git-native, human-readable",
        "description": description or f"A project tracked with session memory.",
    }

    state_content = _load_and_render("session_state.md", variables)
    state_file.write_text(state_content, encoding="utf-8")

    # Optionally create project compass
    compass_file = None
    if create_compass:
        compass_filename = config.get("compass_file", DEFAULTS["compass_file"])
        compass_file = root / compass_filename
        if not compass_file.exists():
            compass_content = _load_and_render("project_compass.md", variables)
            compass_file.write_text(compass_content, encoding="utf-8")

    return ProjectInfo(
        name=normalized,
        memory_dir=mem_dir,
        state_file=state_file,
        compass_file=compass_file,
        archive_dir=archive_dir,
    )


def discover_projects(
    base_dir: Path | None = None,
    config: dict | None = None,
) -> list[ProjectInfo]:
    """Discover all projects with session memory in a directory.

    Scans the memory directory for subdirectories containing state files.

    Args:
        base_dir: Base directory to scan. Defaults to CWD.
        config: Pre-loaded config. If None, loads automatically.

    Returns:
        List of discovered ProjectInfo objects.
    """
    if config is None:
        config = load_config()

    root = base_dir if base_dir else Path.cwd()
    mem_dir = get_memory_dir(root, config)

    if not mem_dir.exists():
        return []

    projects = []
    for entry in sorted(mem_dir.iterdir()):
        if not entry.is_dir() or entry.name.startswith("."):
            continue

        # Look for state files matching pattern
        state_files = list(entry.glob("SESSION_STATE_*.md"))
        if not state_files:
            # Also check for exact state_file name
            state_file_name = config.get("state_file", DEFAULTS["state_file"])
            candidate = entry / state_file_name
            if candidate.exists():
                state_files = [candidate]

        if state_files:
            state_file = state_files[0]
            compass_file_name = config.get("compass_file", DEFAULTS["compass_file"])
            compass_file = root / compass_file_name
            projects.append(
                ProjectInfo(
                    name=entry.name,
                    memory_dir=mem_dir,
                    state_file=state_file,
                    compass_file=compass_file if compass_file.exists() else None,
                    archive_dir=entry / "archive",
                )
            )

    return projects


def get_project(
    name: str,
    base_dir: Path | None = None,
    config: dict | None = None,
) -> ProjectInfo | None:
    """Get a specific project by name.

    Args:
        name: Project name to find.
        base_dir: Base directory. Defaults to CWD.
        config: Pre-loaded config.

    Returns:
        ProjectInfo if found, None otherwise.
    """
    normalized = normalize_name(name)
    projects = discover_projects(base_dir, config)
    for p in projects:
        if p.name == normalized:
            return p
    return None


def archive_state(
    project: ProjectInfo,
    reason: str = "",
) -> Path:
    """Archive the current session state file.

    Copies the current state file to the archive directory with a
    timestamp suffix.

    Args:
        project: Project to archive state for.
        reason: Optional reason for archiving.

    Returns:
        Path to the archived file.

    Raises:
        FileNotFoundError: If state file doesn't exist.
    """
    if not project.state_file.exists():
        raise FileNotFoundError(f"State file not found: {project.state_file}")

    project.archive_dir.mkdir(parents=True, exist_ok=True)

    today = date_type.today().isoformat()
    # Sanitize reason to prevent path traversal or illegal filename chars
    if reason:
        import re
        safe_reason = re.sub(r"[^a-zA-Z0-9_-]", "_", reason)
        suffix = f"_{safe_reason}"
    else:
        suffix = ""
    archive_name = f"{project.state_file.stem}_archived_{today}{suffix}.md"
    archive_path = project.archive_dir / archive_name

    # Avoid overwriting existing archives
    counter = 1
    while archive_path.exists():
        archive_name = f"{project.state_file.stem}_archived_{today}{suffix}_{counter}.md"
        archive_path = project.archive_dir / archive_name
        counter += 1

    shutil.copy2(project.state_file, archive_path)
    return archive_path


def _load_template(template_name: str) -> str:
    """Load a template file from the package templates directory.

    Args:
        template_name: Name of the template file.

    Returns:
        Template content as string.

    Raises:
        FileNotFoundError: If template doesn't exist.
    """
    template_dir = resources.files("cervellaswarm_session_memory") / "templates"
    template_path = template_dir / template_name
    return template_path.read_text(encoding="utf-8")


def _load_and_render(template_name: str, variables: dict[str, str]) -> str:
    """Load a template and render it with variables.

    Uses simple {{ variable }} placeholder substitution.

    Args:
        template_name: Name of the template file.
        variables: Dictionary of placeholder -> value mappings.

    Returns:
        Rendered template content.
    """
    content = _load_template(template_name)
    return _render_template(content, variables)


def _render_template(content: str, variables: dict[str, str]) -> str:
    """Render a template string with {{ variable }} placeholders.

    Args:
        content: Template content with {{ variable }} placeholders.
        variables: Dictionary of placeholder -> value mappings.

    Returns:
        Rendered content.
    """
    for key, value in variables.items():
        content = content.replace("{{ " + key + " }}", value)
    return content
