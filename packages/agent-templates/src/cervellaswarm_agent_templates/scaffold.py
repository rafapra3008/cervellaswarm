# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Scaffold agent definitions and team configurations."""

from __future__ import annotations

from datetime import date
from importlib import resources
from pathlib import Path
from typing import Any

import yaml

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

TEMPLATE_TYPES = {
    "coordinator": {
        "display_name": "Coordinator",
        "default_name": "coordinator",
    },
    "quality-gate": {
        "display_name": "Quality Gate",
        "default_name": "quality-gate",
    },
    "architect": {
        "display_name": "Architect",
        "default_name": "architect",
    },
    "worker": {
        "display_name": "Worker",
        "default_name": "worker",
    },
}

WORKER_SPECIALTIES = {
    "backend": {
        "description": "Specialist in Python, APIs, databases, and server-side logic.",
        "details": (
            "- **Python** - Clean code, type hints, best practices\n"
            "- **FastAPI/Flask** - REST APIs, endpoints, middleware\n"
            "- **Databases** - SQL, migrations, ORM\n"
            "- **Integrations** - External APIs, webhooks, auth"
        ),
        "allowed": '- `*.py`, `api/**`, `backend/**`, `server/**`\n- `*.sql`, migrations, `requirements.txt`',
        "disallowed": "- Frontend files (`*.jsx`, `*.css`)\n- Test files (leave to the tester agent)",
    },
    "frontend": {
        "description": "Specialist in UI/UX, React, CSS, and responsive design.",
        "details": (
            "- **React/Next.js** - Components, hooks, state management\n"
            "- **CSS/Tailwind** - Styling, responsive design, animations\n"
            "- **TypeScript** - Type-safe frontend code\n"
            "- **Accessibility** - ARIA, semantic HTML, keyboard navigation"
        ),
        "allowed": "- `*.tsx`, `*.jsx`, `*.css`, `*.html`\n- `components/**`, `pages/**`, `styles/**`",
        "disallowed": "- Backend files (`*.py`, `*.sql`)\n- Test files (leave to the tester agent)",
    },
    "tester": {
        "description": "Specialist in testing, debugging, and quality assurance.",
        "details": (
            "- **Unit tests** - pytest, Jest, coverage\n"
            "- **Integration tests** - API testing, E2E\n"
            "- **Debugging** - Root cause analysis, reproduction\n"
            "- **CI/CD** - Test pipelines, automated checks"
        ),
        "allowed": "- `tests/**`, `*.test.*`, `*.spec.*`\n- `conftest.py`, test fixtures",
        "disallowed": "- Production code (suggest changes to the appropriate worker)",
    },
    "researcher": {
        "description": "Specialist in research, analysis, and technical investigation.",
        "details": (
            "- **Technical research** - Best practices, architecture patterns\n"
            "- **Competitor analysis** - Feature comparison, benchmarks\n"
            "- **Documentation** - Findings, recommendations, reports\n"
            "- **Web search** - Current information, library evaluation"
        ),
        "allowed": "- `docs/**`, `reports/**`\n- Research output files",
        "disallowed": "- Source code (report findings for workers to implement)",
    },
    "devops": {
        "description": "Specialist in deployment, CI/CD, Docker, and infrastructure.",
        "details": (
            "- **Docker** - Dockerfiles, compose, multi-stage builds\n"
            "- **CI/CD** - GitHub Actions, pipelines, automation\n"
            "- **Infrastructure** - Nginx, SSL, monitoring\n"
            "- **Scripts** - Deployment, backup, maintenance"
        ),
        "allowed": "- `Dockerfile`, `docker-compose.yml`, `.github/workflows/**`\n- `scripts/**`, `nginx/**`, infrastructure config",
        "disallowed": "- Application source code\n- Test files",
    },
    "docs": {
        "description": "Specialist in documentation, guides, and technical writing.",
        "details": (
            "- **README files** - Clear, structured, with examples\n"
            "- **API docs** - Endpoint reference, schemas\n"
            "- **Guides** - Getting started, tutorials, migration\n"
            "- **Architecture docs** - System design, diagrams"
        ),
        "allowed": "- `*.md`, `docs/**`\n- README files, CHANGELOG, CONTRIBUTING",
        "disallowed": "- Source code\n- Test files",
    },
    "generic": {
        "description": "General-purpose worker for tasks not covered by specialized roles.",
        "details": (
            "- **Flexible** - Adapts to the task at hand\n"
            "- **Cross-functional** - Can work across domains\n"
            "- **Task-focused** - Follows instructions precisely"
        ),
        "allowed": "- Files relevant to the assigned task",
        "disallowed": "- Files outside the scope of the current task",
    },
}

# Team presets
TEAM_PRESETS = {
    "minimal": {
        "description": "Minimal 3-agent team: coordinator + backend worker + quality gate",
        "agents": [
            {"type": "coordinator", "name": "lead"},
            {"type": "worker", "name": "dev", "specialty": "backend"},
            {"type": "quality-gate", "name": "reviewer"},
        ],
    },
    "standard": {
        "description": "Standard 7-agent team with architect and multiple workers",
        "agents": [
            {"type": "coordinator", "name": "lead"},
            {"type": "architect", "name": "planner"},
            {"type": "quality-gate", "name": "reviewer"},
            {"type": "worker", "name": "backend", "specialty": "backend"},
            {"type": "worker", "name": "frontend", "specialty": "frontend"},
            {"type": "worker", "name": "tester", "specialty": "tester"},
            {"type": "worker", "name": "researcher", "specialty": "researcher"},
        ],
    },
    "full": {
        "description": "Full 17-agent team with all specialist roles",
        "agents": [
            {"type": "coordinator", "name": "lead"},
            {"type": "architect", "name": "planner"},
            {"type": "quality-gate", "name": "qa-code"},
            {"type": "quality-gate", "name": "qa-ops"},
            {"type": "quality-gate", "name": "qa-research"},
            {"type": "worker", "name": "backend", "specialty": "backend"},
            {"type": "worker", "name": "frontend", "specialty": "frontend"},
            {"type": "worker", "name": "tester", "specialty": "tester"},
            {"type": "worker", "name": "researcher", "specialty": "researcher"},
            {"type": "worker", "name": "devops", "specialty": "devops"},
            {"type": "worker", "name": "docs", "specialty": "docs"},
            {"type": "worker", "name": "data", "specialty": "generic"},
            {"type": "worker", "name": "security", "specialty": "generic"},
            {"type": "worker", "name": "marketing", "specialty": "generic"},
            {"type": "worker", "name": "reviewer", "specialty": "generic"},
            {"type": "worker", "name": "scientist", "specialty": "generic"},
            {"type": "worker", "name": "engineer", "specialty": "generic"},
        ],
    },
}


# ---------------------------------------------------------------------------
# Template loading
# ---------------------------------------------------------------------------


def _load_template(template_name: str) -> str:
    """Load a template file from the bundled templates directory."""
    ref = resources.files("cervellaswarm_agent_templates") / "templates" / template_name
    return ref.read_text(encoding="utf-8")


def _render_template(content: str, variables: dict[str, str]) -> str:
    """Replace {{ variable }} placeholders in template content."""
    result = content
    for key, value in variables.items():
        result = result.replace("{{ " + key + " }}", value)
    return result


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def list_templates() -> dict[str, dict[str, Any]]:
    """List all available template types and worker specialties.

    Returns a dict with 'types' and 'specialties' keys.
    """
    return {
        "types": {k: v["display_name"] for k, v in TEMPLATE_TYPES.items()},
        "specialties": {k: v["description"] for k, v in WORKER_SPECIALTIES.items()},
        "team_presets": {k: v["description"] for k, v in TEAM_PRESETS.items()},
    }


def create_agent(
    agent_type: str,
    name: str | None = None,
    output_dir: str | Path = ".",
    team_name: str = "my-team",
    specialty: str = "generic",
) -> Path:
    """Create an agent definition file from a template.

    Args:
        agent_type: One of 'coordinator', 'quality-gate', 'architect', 'worker'
        name: Agent name (defaults to template default)
        output_dir: Directory to write the file to
        team_name: Team name for the agent
        specialty: Worker specialty (only used for 'worker' type)

    Returns:
        Path to the created file.

    Raises:
        ValueError: If agent_type or specialty is invalid.
    """
    if agent_type not in TEMPLATE_TYPES:
        valid = ", ".join(sorted(TEMPLATE_TYPES))
        raise ValueError(f"Unknown agent type '{agent_type}'. Valid types: {valid}")

    if agent_type == "worker" and specialty not in WORKER_SPECIALTIES:
        valid = ", ".join(sorted(WORKER_SPECIALTIES))
        raise ValueError(f"Unknown specialty '{specialty}'. Valid: {valid}")

    type_info = TEMPLATE_TYPES[agent_type]
    name = name or type_info["default_name"]
    today = date.today().isoformat()

    # Build template variables
    variables = {
        "name": name,
        "display_name": name.replace("-", " ").title(),
        "date": today,
        "team_name": team_name,
    }

    # Worker-specific variables
    if agent_type == "worker":
        spec = WORKER_SPECIALTIES[specialty]
        variables["specialty"] = specialty.title()
        variables["specialty_description"] = spec["description"]
        variables["specialty_details"] = spec["details"]
        variables["allowed_files"] = spec["allowed"]
        variables["disallowed_files"] = spec["disallowed"]

    # Load and render template
    template_file = f"{agent_type}.md"
    template_content = _load_template(template_file)
    rendered = _render_template(template_content, variables)

    # Write output
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    file_path = output_path / f"{name}.md"
    file_path.write_text(rendered, encoding="utf-8")

    return file_path


def create_shared_dna(
    output_dir: str | Path = ".",
    team_name: str = "my-team",
) -> Path:
    """Create a shared DNA file from the template.

    Args:
        output_dir: Directory to write the file to
        team_name: Team name to include in the DNA

    Returns:
        Path to the created file.
    """
    template_content = _load_template("_shared_dna.md")
    rendered = _render_template(template_content, {"team_name": team_name})

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    file_path = output_path / "_shared_dna.md"
    file_path.write_text(rendered, encoding="utf-8")

    return file_path


def create_team_config(
    preset: str,
    output_dir: str | Path = ".",
    team_name: str = "my-team",
) -> Path:
    """Create a team.yaml composition file from a preset.

    Args:
        preset: One of 'minimal', 'standard', 'full'
        output_dir: Directory to write the file to
        team_name: Team name

    Returns:
        Path to the created team.yaml file.

    Raises:
        ValueError: If preset is invalid.
    """
    if preset not in TEAM_PRESETS:
        valid = ", ".join(sorted(TEAM_PRESETS))
        raise ValueError(f"Unknown preset '{preset}'. Valid: {valid}")

    team_data = TEAM_PRESETS[preset]

    config = {
        "name": team_name,
        "version": "1.0.0",
        "description": team_data["description"],
        "agents": [],
    }

    for agent_def in team_data["agents"]:
        agent_entry: dict[str, str] = {
            "name": agent_def["name"],
            "type": agent_def["type"],
        }
        if "specialty" in agent_def:
            agent_entry["specialty"] = agent_def["specialty"]
        # Assign role based on type
        if agent_def["type"] == "coordinator":
            agent_entry["role"] = "lead"
        elif agent_def["type"] == "quality-gate":
            agent_entry["role"] = "validator"
        elif agent_def["type"] == "architect":
            agent_entry["role"] = "planner"
        else:
            agent_entry["role"] = "worker"
        config["agents"].append(agent_entry)

    # Determine entry point
    config["entry_point"] = "lead"
    config["process"] = "hierarchical"

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    file_path = output_path / "team.yaml"
    file_path.write_text(
        yaml.dump(config, default_flow_style=False, sort_keys=False),
        encoding="utf-8",
    )

    return file_path


def create_team(
    preset: str,
    output_dir: str | Path = ".",
    team_name: str = "my-team",
) -> list[Path]:
    """Create a complete team from a preset (team.yaml + all agent files + shared DNA).

    Args:
        preset: One of 'minimal', 'standard', 'full'
        output_dir: Directory to write files to
        team_name: Team name

    Returns:
        List of all created file paths.

    Raises:
        ValueError: If preset is invalid.
    """
    if preset not in TEAM_PRESETS:
        valid = ", ".join(sorted(TEAM_PRESETS))
        raise ValueError(f"Unknown preset '{preset}'. Valid: {valid}")

    created_files: list[Path] = []

    # Create shared DNA
    dna_path = create_shared_dna(output_dir, team_name)
    created_files.append(dna_path)

    # Create team.yaml
    config_path = create_team_config(preset, output_dir, team_name)
    created_files.append(config_path)

    # Create each agent
    for agent_def in TEAM_PRESETS[preset]["agents"]:
        agent_path = create_agent(
            agent_type=agent_def["type"],
            name=agent_def["name"],
            output_dir=output_dir,
            team_name=team_name,
            specialty=agent_def.get("specialty", "generic"),
        )
        created_files.append(agent_path)

    return created_files
