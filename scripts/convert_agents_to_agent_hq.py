#!/usr/bin/env python3
"""
Convert CervellaSwarm agents to Agent HQ .agent.md format.

This script reads agents from ~/.claude/agents/ and converts them
to the VS Code Agent HQ format in .github/agents/
"""

import os
import re
import yaml
from pathlib import Path

# Source and destination directories
SOURCE_DIR = Path.home() / ".claude" / "agents"
DEST_DIR = Path(__file__).resolve().parent.parent / ".github" / "agents"

# Tool mapping from our format to Agent HQ format
TOOL_MAPPING = {
    "Read": "read",
    "Edit": "edit",
    "Write": "write",
    "Bash": "terminal",
    "Glob": "search",
    "Grep": "search",
    "WebSearch": "fetch",
    "WebFetch": "fetch",
    "Task": "runSubagent",
}

# Model mapping
MODEL_MAPPING = {
    "sonnet": "claude-sonnet-4-6",
    "opus": "claude-opus-4-6",
    "haiku": "claude-haiku-4-5",
}

# Guardians that can receive handoffs
GUARDIANS = {
    "cervella-guardiana-qualita": "Quality review and standards compliance",
    "cervella-guardiana-ops": "Operations, security, and deployment review",
    "cervella-guardiana-ricerca": "Research quality verification",
}

def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Extract YAML frontmatter and body from markdown."""
    if not content.startswith("---"):
        return {}, content

    # Find the closing ---
    end_idx = content.find("---", 3)
    if end_idx == -1:
        return {}, content

    frontmatter_str = content[3:end_idx].strip()
    body = content[end_idx + 3:].strip()

    try:
        frontmatter = yaml.safe_load(frontmatter_str)
        return frontmatter or {}, body
    except yaml.YAMLError:
        return {}, content

def convert_tools(tools_str: str) -> list[str]:
    """Convert our tool format to Agent HQ format."""
    if not tools_str:
        return ["read", "edit", "search"]

    tools = [t.strip() for t in tools_str.split(",")]
    converted = set()
    for tool in tools:
        if tool in TOOL_MAPPING:
            converted.add(TOOL_MAPPING[tool])
        else:
            # Keep unknown tools as-is
            converted.add(tool.lower())

    return list(converted)

def get_handoff_for_agent(agent_name: str) -> list[dict] | None:
    """Determine appropriate handoff based on agent type."""
    # Guardians don't have handoffs (they ARE the escalation point)
    if "guardiana" in agent_name or "orchestrator" in agent_name:
        return None

    # Frontend, backend, tester -> guardiana-qualita
    if any(x in agent_name for x in ["frontend", "backend", "tester", "data"]):
        return [{
            "label": "Escalate to Quality Guardian",
            "agent": "cervella-guardiana-qualita",
            "prompt": "Review work for quality and standards compliance.",
            "send": False,
        }]

    # Researcher, scienziata, docs -> guardiana-ricerca
    if any(x in agent_name for x in ["researcher", "scienziata", "docs"]):
        return [{
            "label": "Escalate to Research Guardian",
            "agent": "cervella-guardiana-ricerca",
            "prompt": "Verify research quality and source reliability.",
            "send": False,
        }]

    # DevOps, security -> guardiana-ops
    if any(x in agent_name for x in ["devops", "security"]):
        return [{
            "label": "Escalate to Ops Guardian",
            "agent": "cervella-guardiana-ops",
            "prompt": "Review operations/security implementation.",
            "send": False,
        }]

    return None

def convert_agent(source_file: Path) -> None:
    """Convert a single agent file to Agent HQ format."""
    content = source_file.read_text(encoding="utf-8")
    frontmatter, body = parse_frontmatter(content)

    agent_name = frontmatter.get("name", source_file.stem)
    description = frontmatter.get("description", f"CervellaSwarm {agent_name} agent")
    tools_str = frontmatter.get("tools", "Read, Glob, Grep")
    model = frontmatter.get("model", "sonnet")

    # Convert to Agent HQ format
    new_frontmatter = {
        "name": agent_name,
        "description": description,
        "tools": convert_tools(tools_str),
        "model": MODEL_MAPPING.get(model, "claude-sonnet-4-6"),
        "target": "vscode",
        "infer": True,
    }

    # Add handoffs if applicable
    handoffs = get_handoff_for_agent(agent_name)
    if handoffs:
        new_frontmatter["handoffs"] = handoffs

    # Build new content
    new_content = "---\n"
    new_content += yaml.dump(new_frontmatter, default_flow_style=False, allow_unicode=True, sort_keys=False)
    new_content += "---\n\n"
    new_content += body

    # Write to destination
    dest_file = DEST_DIR / f"{agent_name}.agent.md"
    dest_file.write_text(new_content, encoding="utf-8")
    print(f"✅ Converted: {agent_name}")

def main():
    """Convert all agents."""
    print("🔄 Converting CervellaSwarm agents to Agent HQ format...\n")

    # Ensure destination exists
    DEST_DIR.mkdir(parents=True, exist_ok=True)

    # Find all agent files
    agent_files = list(SOURCE_DIR.glob("*.md"))

    if not agent_files:
        print("❌ No agent files found in", SOURCE_DIR)
        return

    print(f"📂 Found {len(agent_files)} agents in {SOURCE_DIR}\n")

    # Convert each agent
    for agent_file in sorted(agent_files):
        try:
            convert_agent(agent_file)
        except Exception as e:
            print(f"❌ Error converting {agent_file.name}: {e}")

    print(f"\n✨ Done! Converted agents saved to {DEST_DIR}")

if __name__ == "__main__":
    main()
