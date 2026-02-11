/**
 * SNCP MCP Tools - Project Memory Access via MCP
 *
 * 4 tools for accessing CervellaSwarm SNCP memory:
 * - sncp_read_ripresa: Read session context
 * - sncp_read_stato: Read project state
 * - sncp_list_projects: List all projects
 * - sncp_search: Search across SNCP files
 *
 * Version: 1.0.0
 * Date: 2026-02-10 - Sessione 352 (Step D.2)
 */
import type { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
/**
 * Register all SNCP tools on the MCP server instance.
 */
export declare function registerSncpTools(server: McpServer): void;
//# sourceMappingURL=tools.d.ts.map