# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""CervellaSwarm Agent Templates - Template agent definitions for Claude Code."""

__version__ = "0.1.0"

from cervellaswarm_agent_templates.scaffold import (
    create_agent,
    create_team,
    list_templates,
)
from cervellaswarm_agent_templates.validator import validate_agent

__all__ = [
    "__version__",
    "create_agent",
    "create_team",
    "list_templates",
    "validate_agent",
]
