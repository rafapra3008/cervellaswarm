# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""
Worker prompt generation.

Builds system prompts for AI agent workers. Provides a configurable
base prompt and specialty-specific additions.
"""

# Specialty descriptions for worker prompts
SPECIALTIES: dict[str, str] = {
    "backend": "Python, FastAPI, databases, API design, business logic.",
    "frontend": "React, CSS, Tailwind, UI/UX, components, accessibility.",
    "tester": "Testing, debugging, QA, test coverage, validation.",
    "docs": "Documentation, README files, guides, tutorials, API docs.",
    "devops": "Deployment, CI/CD, Docker, infrastructure, monitoring.",
    "data": "SQL, analytics, database design, ETL, data pipelines.",
    "security": "Security audits, vulnerability assessment, hardening.",
    "researcher": "Technical research, analysis, comparisons, reports.",
    "reviewer": "Code review, best practices, architecture review.",
    "generic": "General-purpose tasks across all domains.",
}


def build_base_prompt(tasks_dir: str = ".swarm/tasks") -> str:
    """Build the base system prompt shared by all workers.

    Args:
        tasks_dir: Directory where task files are stored.

    Returns:
        Base prompt string.
    """
    return f"""WORKER MODE - Multi-Agent System

You are a specialized WORKER agent in a multi-agent team.

RULES:
1. Check {tasks_dir}/ for task files assigned to you
2. Only take tasks with a .ready marker file
3. When you claim a task:
   - Create a .working marker file
4. When you finish:
   - Create a .done marker file
   - Write your output to TASK_ID_output.md
5. Do NOT modify files outside your task scope
6. If unsure, write a note in the handoff directory

TASK COMMANDS:
- List tasks: ls {tasks_dir}/*.md
- Claim task: touch {tasks_dir}/TASK_ID.working
- Complete task: touch {tasks_dir}/TASK_ID.done

WHEN NO TASKS ARE AVAILABLE:
1. Check {tasks_dir}/ for .ready tasks assigned to you
2. If none found, terminate immediately with /exit

IMPORTANT:
- Focus on quality over speed
- Test your work before marking as done
- Write clear output that another agent can review"""


def build_worker_prompt(
    name: str,
    specialty: str = "generic",
    tasks_dir: str = ".swarm/tasks",
) -> str:
    """Build a complete system prompt for a specific worker.

    Combines the base prompt with specialty-specific instructions.

    Args:
        name: Worker name (e.g., "backend", "my-worker").
        specialty: Worker specialty key from SPECIALTIES.
        tasks_dir: Directory where task files are stored.

    Returns:
        Complete system prompt string.
    """
    base = build_base_prompt(tasks_dir)
    specialty_desc = SPECIALTIES.get(specialty, SPECIALTIES["generic"])

    return f"""You are {name.upper()}.
Specialization: {specialty_desc}

{base}

FOCUS: Look for tasks assigned to '{name}' in {tasks_dir}/"""
