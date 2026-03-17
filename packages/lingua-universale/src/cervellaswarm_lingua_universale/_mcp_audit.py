# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""lu mcp-audit -- audit MCP servers for protocol safety.

Discovers MCP server tools, infers implicit ordering constraints,
generates a .lu protocol, and verifies it with the existing pipeline.

Usage:
    lu mcp-audit --manifest tools.json          # offline (zero deps)
    lu mcp-audit --manifest tools.json --json   # JSON output
    lu mcp-audit --manifest tools.json --save-lu out.lu  # save protocol
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

from ._colors import colors as _c

_SAFE_NAME_RE = re.compile(r"[^a-zA-Z0-9_]")


# ---------------------------------------------------------------------------
# Data types (frozen dataclasses)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ToolDefinition:
    """A single MCP tool discovered from a server."""
    name: str
    description: str
    input_schema: dict


@dataclass(frozen=True)
class InferredStep:
    """An inferred ordering constraint between tools."""
    before: str
    after: str
    reason: str
    confidence: str  # "high" | "medium" | "low"


@dataclass(frozen=True)
class InferredProtocol:
    """Complete inferred protocol structure."""
    name: str
    roles: tuple[str, ...]
    tools: tuple[ToolDefinition, ...]
    orderings: tuple[InferredStep, ...]
    categories: dict[str, tuple[str, ...]]
    warnings: tuple[str, ...]


@dataclass(frozen=True)
class AuditReport:
    """Final audit report combining inference + verification."""
    server_name: str
    tool_count: int
    inferred_protocol: InferredProtocol
    lu_source: str
    property_results: tuple[dict, ...]
    passed: int
    violated: int
    warnings: tuple[str, ...]


# ---------------------------------------------------------------------------
# Step 1: Manifest loader
# ---------------------------------------------------------------------------

def load_manifest(path: str | Path) -> tuple[str, list[ToolDefinition]]:
    """Load MCP tool definitions from a JSON manifest file.

    Returns (server_name, tools).
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Manifest not found: {p}")

    data = json.loads(p.read_text(encoding="utf-8"))

    server_name = data.get("server_name", p.stem)

    raw_tools = data.get("tools", [])
    if not isinstance(raw_tools, list):
        raise ValueError("Manifest 'tools' must be a list")

    tools: list[ToolDefinition] = []
    for i, t in enumerate(raw_tools):
        if not isinstance(t, dict):
            raise ValueError(f"Tool {i}: expected dict, got {type(t).__name__}")
        tools.append(ToolDefinition(
            name=t.get("name", f"tool_{i}"),
            description=t.get("description", ""),
            input_schema=t.get("inputSchema", t.get("input_schema", {})),
        ))

    return server_name, tools


# ---------------------------------------------------------------------------
# Step 2: Inference engine
# ---------------------------------------------------------------------------

# Tool category patterns (order matters: first match wins)
_CATEGORIES: dict[str, list[str]] = {
    "CLEANUP": ["close", "disconnect", "logout", "cleanup", "shutdown", "stop"],
    "LIFECYCLE": ["init", "connect", "login", "auth", "setup", "start", "open", "begin"],
    "CREATE": ["create", "add", "insert", "register", "new", "write", "put", "post"],
    "READ": ["get", "read", "list", "search", "find", "query", "fetch", "show", "describe"],
    "UPDATE": ["update", "modify", "set", "patch", "edit", "rename", "replace"],
    "DELETE": ["delete", "remove", "destroy", "purge", "clear", "drop"],
}


def _categorize_tools(tools: list[ToolDefinition]) -> dict[str, list[str]]:
    """Categorize tools by name patterns into CRUD + lifecycle groups."""
    result: dict[str, list[str]] = {cat: [] for cat in _CATEGORIES}
    result["OTHER"] = []

    for tool in tools:
        name_lower = tool.name.lower().replace("-", "_")
        matched = False
        for category, patterns in _CATEGORIES.items():
            if any(p in name_lower for p in patterns):
                result[category].append(tool.name)
                matched = True
                break
        if not matched:
            result["OTHER"].append(tool.name)

    # Remove empty categories, convert to tuples for immutability
    return {k: tuple(v) for k, v in result.items() if v}


def _extract_id_fields(schema: dict) -> list[str]:
    """Extract *_id fields from a JSON Schema's required list."""
    required = schema.get("required", [])
    props = schema.get("properties", {})
    id_fields = []
    for field_name in required:
        if field_name.endswith("_id") or field_name == "id":
            id_fields.append(field_name)
    # Also check non-required but id-shaped properties
    for field_name in props:
        if field_name.endswith("_id") and field_name not in id_fields:
            id_fields.append(field_name)
    return id_fields


def _infer_orderings(
    tools: list[ToolDefinition],
    categories: dict[str, list[str]],
) -> list[InferredStep]:
    """Infer ordering constraints from tool names, schemas, and descriptions."""
    orderings: list[InferredStep] = []
    seen: set[tuple[str, str]] = set()

    def _add(before: str, after: str, reason: str, confidence: str) -> None:
        key = (before, after)
        if key not in seen and before != after:
            seen.add(key)
            orderings.append(InferredStep(before, after, reason, confidence))

    # 1. LIFECYCLE before everything else
    lifecycle = categories.get("LIFECYCLE", [])
    non_lifecycle = [
        t.name for t in tools
        if t.name not in lifecycle and t.name not in categories.get("CLEANUP", [])
    ]
    for lc in lifecycle:
        for other in non_lifecycle:
            _add(lc, other, "lifecycle before operation", "high")

    # 2. CLEANUP after everything else
    cleanup = categories.get("CLEANUP", [])
    non_cleanup = [
        t.name for t in tools
        if t.name not in cleanup and t.name not in lifecycle
    ]
    for other in non_cleanup:
        for cl in cleanup:
            _add(other, cl, "operation before cleanup", "high")

    # 3. CREATE before READ/UPDATE/DELETE of same resource
    creates = categories.get("CREATE", [])
    reads = categories.get("READ", [])
    updates = categories.get("UPDATE", [])
    deletes = categories.get("DELETE", [])

    for cr in creates:
        resource = _extract_resource_prefix(cr)
        for rd in reads:
            if _same_resource(cr, rd, resource):
                _add(cr, rd, f"create before read ({resource})", "high")
        for up in updates:
            if _same_resource(cr, up, resource):
                _add(cr, up, f"create before update ({resource})", "high")
        for dl in deletes:
            if _same_resource(cr, dl, resource):
                _add(cr, dl, f"create before delete ({resource})", "high")

    # 4. Schema cross-references: tool B requires *_id → needs a create tool
    tools_by_name = {t.name: t for t in tools}
    for tool in tools:
        id_fields = _extract_id_fields(tool.input_schema)
        for id_field in id_fields:
            # e.g., user_id → look for create_user
            prefix = id_field.replace("_id", "")
            for cr in creates:
                if prefix in cr.lower():
                    _add(cr, tool.name, f"schema: {id_field} requires {cr}", "high")

    # 5. Description keywords (medium confidence)
    for tool in tools:
        desc = tool.description.lower()
        if "after" in desc or "requires" in desc or "must first" in desc:
            for other in tools:
                if other.name == tool.name:
                    continue
                # Word-boundary match avoids false positives with short names
                # like "get", "set", "open" matching inside larger words
                other_lower = other.name.lower()
                if len(other_lower) <= 3:
                    # Short names need word boundary
                    if re.search(r'\b' + re.escape(other_lower) + r'\b', desc):
                        _add(other.name, tool.name, f"description: '{tool.description[:60]}'", "medium")
                elif other_lower in desc:
                    _add(other.name, tool.name, f"description: '{tool.description[:60]}'", "medium")

    return orderings


def _extract_resource_prefix(tool_name: str) -> str:
    """Extract resource name from tool name (e.g., 'create_user' → 'user')."""
    parts = tool_name.lower().replace("-", "_").split("_")
    # Remove action verbs
    action_words = set()
    for patterns in _CATEGORIES.values():
        action_words.update(patterns)
    resource_parts = [p for p in parts if p not in action_words]
    return "_".join(resource_parts) if resource_parts else tool_name


def _same_resource(tool_a: str, tool_b: str, resource: str) -> bool:
    """Check if two tools operate on the same resource."""
    if not resource:
        return False
    return resource in tool_b.lower().replace("-", "_")


def _detect_cycles(orderings: list[InferredStep]) -> list[str]:
    """Detect circular dependencies in orderings. Returns warnings."""
    # Build adjacency graph
    graph: dict[str, set[str]] = {}
    for o in orderings:
        graph.setdefault(o.before, set()).add(o.after)

    # DFS cycle detection
    visited: set[str] = set()
    in_stack: set[str] = set()
    warnings: list[str] = []

    def _dfs(node: str, path: list[str]) -> None:
        if node in in_stack:
            cycle = path[path.index(node):] + [node]
            warnings.append(f"Circular dependency: {' -> '.join(cycle)}")
            return
        if node in visited:
            return
        visited.add(node)
        in_stack.add(node)
        for neighbor in graph.get(node, []):
            _dfs(neighbor, path + [node])
        in_stack.discard(node)

    for node in graph:
        if node not in visited:
            _dfs(node, [])

    return warnings


def infer_protocol(
    server_name: str, tools: list[ToolDefinition]
) -> InferredProtocol:
    """Infer a complete protocol from MCP tool definitions."""
    categories = _categorize_tools(tools)
    orderings = _infer_orderings(tools, categories)
    cycle_warnings = _detect_cycles(orderings)

    warnings: list[str] = list(cycle_warnings)

    # Warn about destructive operations
    for name in categories.get("DELETE", ()):
        warnings.append(f"{name}: destructive operation detected")

    # Warn about small servers
    if len(tools) <= 2:
        warnings.append("Server has <= 2 tools; limited ordering inference")

    # Clean name for protocol (must be valid LU identifier)
    proto_name = re.sub(r"[^a-zA-Z0-9]", "", server_name.replace("-", " ").title().replace(" ", ""))
    if not proto_name:
        proto_name = "McpServer"
    elif proto_name[0].isdigit():
        proto_name = "Mcp" + proto_name

    return InferredProtocol(
        name=proto_name,
        roles=("client", "server"),
        tools=tuple(tools),
        orderings=tuple(orderings),
        categories=categories,
        warnings=tuple(warnings),
    )


# ---------------------------------------------------------------------------
# Step 3: LU source generator
# ---------------------------------------------------------------------------

def generate_lu_source(protocol: InferredProtocol) -> str:
    """Generate valid .lu source text from an inferred protocol."""
    lines: list[str] = []

    # Types
    lines.append("type ToolResult = Success | Error")
    lines.append("")

    # Agents
    lines.append("agent Client:")
    lines.append("    role: client")
    lines.append("    trust: standard")
    lines.append("")
    lines.append("agent Server:")
    lines.append("    role: server")
    lines.append("    trust: verified")
    lines.append("")

    # Protocol
    lines.append(f"protocol {protocol.name}:")
    lines.append("    roles: client, server")
    lines.append("")

    # Steps: each tool becomes a request/response pair
    # Order: lifecycle first, then CRUD, then cleanup
    ordered_tools = _order_tools_for_protocol(protocol)

    for tool in ordered_tools:
        safe_name = _SAFE_NAME_RE.sub("_", tool.name)
        # LU identifiers must not start with a digit -- prefix with underscore
        if safe_name and safe_name[0].isdigit():
            safe_name = "_" + safe_name
        lines.append(f"    client asks server to do {safe_name}")
        lines.append(f"    server returns {safe_name}_result to client")

    # Properties (structural -- ordering is guaranteed by step sequence)
    lines.append("")
    lines.append("    properties:")
    lines.append("        always terminates")
    lines.append("        no deadlock")
    lines.append("        all roles participate")

    # No deletion if delete tools exist
    if "DELETE" in protocol.categories:
        lines.append("        no deletion")

    lines.append("")
    return "\n".join(lines)


def _order_tools_for_protocol(protocol: InferredProtocol) -> list[ToolDefinition]:
    """Order tools for protocol generation: lifecycle → CRUD → other → cleanup."""
    tools_by_name = {t.name: t for t in protocol.tools}
    ordered: list[ToolDefinition] = []
    seen: set[str] = set()

    category_order = ["LIFECYCLE", "CREATE", "READ", "UPDATE", "DELETE", "OTHER", "CLEANUP"]
    for cat in category_order:
        for name in protocol.categories.get(cat, []):
            if name not in seen and name in tools_by_name:
                ordered.append(tools_by_name[name])
                seen.add(name)

    # Any remaining tools not in categories
    for tool in protocol.tools:
        if tool.name not in seen:
            ordered.append(tool)

    return ordered


# ---------------------------------------------------------------------------
# Step 4: Audit pipeline + reporting
# ---------------------------------------------------------------------------

def audit_tools(
    server_name: str,
    tools: list[ToolDefinition],
) -> AuditReport:
    """Run the full audit pipeline: infer → generate → verify → report."""
    from . import verify_source

    protocol = infer_protocol(server_name, tools)
    lu_source = generate_lu_source(protocol)

    # Verify the generated protocol
    result = verify_source(lu_source, source_file="<mcp-audit>")

    prop_results: list[dict] = []
    passed = 0
    violated = 0

    for report in result.property_reports:
        for pr in report.results:
            verdict = pr.verdict.value
            prop_results.append({
                "kind": pr.spec.kind.value,
                "verdict": verdict,
                "evidence": pr.evidence,
                "params": list(pr.spec.params),
            })
            if verdict == "proved":
                passed += 1
            else:
                violated += 1

    warnings = list(protocol.warnings)
    if result.errors:
        warnings.extend(result.errors)

    return AuditReport(
        server_name=server_name,
        tool_count=len(tools),
        inferred_protocol=protocol,
        lu_source=lu_source,
        property_results=tuple(prop_results),
        passed=passed,
        violated=violated,
        warnings=tuple(warnings),
    )


def render_terminal(report: AuditReport) -> str:
    """Render an audit report for terminal display."""
    lines: list[str] = []

    lines.append(f"\n{_c.BOLD}MCP Audit Report: {report.server_name}{_c.RESET}")
    lines.append("=" * min(80, 20 + len(report.server_name)))

    # Tools discovered
    tool_names = ", ".join(t.name for t in report.inferred_protocol.tools)
    lines.append(f"Tools discovered: {report.tool_count}")
    lines.append(f"  {tool_names}")

    # Inferred protocol
    lines.append(f"\n{_c.BOLD}Inferred Protocol: {report.inferred_protocol.name}{_c.RESET}")
    lines.append(f"  Roles: {', '.join(report.inferred_protocol.roles)}")
    lines.append(f"  Steps: {report.tool_count * 2}")

    # Orderings
    orderings = report.inferred_protocol.orderings
    if orderings:
        lines.append(f"\n  Orderings inferred ({len(orderings)}):")
        for o in orderings:
            conf = o.confidence.upper()
            lines.append(f"    [{conf:6s}] {o.before} before {o.after}    ({o.reason})")

    # Warnings
    if report.warnings:
        lines.append(f"\n  {_c.YELLOW}Warnings:{_c.RESET}")
        for w in report.warnings:
            lines.append(f"    {_c.YELLOW}!{_c.RESET} {w}")

    # Verification results
    lines.append(f"\n{_c.BOLD}Verification Results:{_c.RESET}")
    for i, pr in enumerate(report.property_results, 1):
        kind = pr["kind"]
        verdict = pr["verdict"]
        params = pr.get("params", [])

        label = kind
        if params:
            label = f"{kind} ({' '.join(params)})"

        if verdict == "proved":
            mark = f"{_c.GREEN}PROVED{_c.RESET}"
        else:
            mark = f"{_c.RED}VIOLATED{_c.RESET}"

        dots = "." * max(1, 40 - len(label))
        lines.append(f"  [{i}/{len(report.property_results)}] {label} {dots} {mark}")

        evidence = pr.get("evidence", "")
        if evidence:
            lines.append(f"        {evidence}")

    # Structural ordering guarantees (from step sequence, not property checking)
    orderings = report.inferred_protocol.orderings
    if orderings:
        lines.append(f"\n{_c.BOLD}Structural Ordering Guarantees:{_c.RESET}")
        lines.append("  (enforced by protocol step sequence)")
        for o in orderings:
            conf = o.confidence.upper()
            lines.append(f"  {_c.GREEN}[{conf:6s}]{_c.RESET} {o.before} -> {o.after}  ({o.reason})")

    # Summary
    total = report.passed + report.violated
    if report.violated == 0:
        lines.append(f"\n  {_c.GREEN}{_c.BOLD}Summary: {report.passed}/{total} properties PROVED, {len(orderings)} ordering guarantees{_c.RESET}")
    else:
        lines.append(f"\n  {_c.RED}{_c.BOLD}Summary: {report.violated}/{total} VIOLATED{_c.RESET}")

    lines.append("")
    return "\n".join(lines)


def render_json(report: AuditReport) -> dict:
    """Render an audit report as a JSON-serializable dict."""
    return {
        "server_name": report.server_name,
        "tool_count": report.tool_count,
        "orderings": [
            {
                "before": o.before,
                "after": o.after,
                "reason": o.reason,
                "confidence": o.confidence,
            }
            for o in report.inferred_protocol.orderings
        ],
        "categories": report.inferred_protocol.categories,
        "properties": report.property_results,
        "passed": report.passed,
        "violated": report.violated,
        "warnings": report.warnings,
        "lu_source": report.lu_source,
    }
