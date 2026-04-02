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
import { z } from "zod";
import {
  readProjectFile,
  listProjects,
  searchSncp,
  type SncpProject,
} from "./reader.js";

/**
 * Register all SNCP tools on the MCP server instance.
 */
export function registerSncpTools(server: McpServer): void {
  /**
   * Tool: sncp_read_ripresa
   * Read PROMPT_RIPRESA for a project (session context)
   */
  server.tool(
    "sncp_read_ripresa",
    "Read the PROMPT_RIPRESA (session context) for a CervellaSwarm project. " +
      "Contains: last session summary, decisions made, next steps.",
    {
      project: z
        .string()
        .min(1)
        .describe("SNCP project name (e.g. cervellaswarm)"),
    },
    {
      title: "Read Project Session Context",
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: false,
    },
    async ({ project }) => {
      try {
        const { content, path } = await readProjectFile(
          project as SncpProject,
          "PROMPT_RIPRESA"
        );
        return {
          content: [
            {
              type: "text",
              text:
                `# PROMPT_RIPRESA - ${project}\n` +
                `Source: ${path}\n\n---\n\n` +
                content,
            },
          ],
        };
      } catch (error) {
        return {
          content: [
            {
              type: "text",
              text: `Error reading PROMPT_RIPRESA for ${project}: ${error instanceof Error ? error.message : "File not found"}`,
            },
          ],
          isError: true,
        };
      }
    }
  );

  /**
   * Tool: sncp_read_stato
   * DEPRECATED: stato.md was eliminated in SNCP 4.0 (S357).
   * Kept for backward compatibility - returns deprecation notice.
   */
  server.tool(
    "sncp_read_stato",
    "Read the stato.md (detailed project state) for a CervellaSwarm project. " +
      "Contains: current progress, open issues, technical details.",
    {
      project: z
        .string()
        .min(1)
        .describe("SNCP project name (e.g. cervellaswarm)"),
    },
    {
      title: "Read Project State",
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: false,
    },
    async ({ project }) => {
      return {
        content: [
          {
            type: "text",
            text:
              `# stato.md - DEPRECATED\n\n` +
              `stato.md was eliminated in SNCP 4.0 (S357).\n` +
              `Use \`sncp_read_ripresa\` instead to read the PROMPT_RIPRESA for ${project}.\n` +
              `PROMPT_RIPRESA contains: session state, decisions, next steps.`,
          },
        ],
      };
    }
  );

  /**
   * Tool: sncp_list_projects
   * List all SNCP projects and their available files
   */
  server.tool(
    "sncp_list_projects",
    "List all CervellaSwarm SNCP projects with their available files and status.",
    {},
    {
      title: "List SNCP Projects",
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: false,
    },
    async () => {
      try {
        const projects = await listProjects();

        if (projects.length === 0) {
          return {
            content: [
              {
                type: "text",
                text: "No SNCP projects found. Check .sncp/progetti/ directory.",
              },
            ],
            isError: true,
          };
        }

        let output = "# SNCP Projects\n\n";
        for (const p of projects) {
          const indicators = [
            p.hasPromptRipresa ? "RIPRESA" : "",
            p.hasMemory ? "MEMORY" : "",
          ]
            .filter(Boolean)
            .join(", ");

          output += `## ${p.name}\n`;
          output += `Available: ${indicators}\n`;
          output += `Files: ${p.files.join(", ")}\n\n`;
        }

        output += `\nUse \`sncp_read_ripresa\` to read session context for a project.`;

        return {
          content: [{ type: "text", text: output }],
        };
      } catch (error) {
        return {
          content: [
            {
              type: "text",
              text: `Error listing projects: ${error instanceof Error ? error.message : "Unknown"}`,
            },
          ],
          isError: true,
        };
      }
    }
  );

  /**
   * Tool: sncp_search
   * Search across SNCP files for a query
   */
  server.tool(
    "sncp_search",
    "Search across all CervellaSwarm SNCP project files for a query string. " +
      "Searches PROMPT_RIPRESA, roadmaps, and other .md files.",
    {
      query: z.string().min(1).describe("Search query (case-insensitive)"),
      project: z
        .string()
        .min(1)
        .optional()
        .describe("Limit search to a specific project (e.g. cervellaswarm)"),
    },
    {
      title: "Search SNCP Files",
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: false,
    },
    async ({ query, project }) => {
      try {
        const results = await searchSncp(query, project as SncpProject | undefined);

        if (results.length === 0) {
          return {
            content: [
              {
                type: "text",
                text: `No matches found for "${query}"${project ? ` in ${project}` : ""}.`,
              },
            ],
          };
        }

        let output = `# Search Results: "${query}"\n\n`;
        let totalMatches = 0;

        for (const r of results) {
          output += `## ${r.project}/${r.file}\n`;
          for (const m of r.matches.slice(0, 10)) {
            output += `  L${m.line}: ${m.text}\n`;
            totalMatches++;
          }
          if (r.matches.length > 10) {
            output += `  ... and ${r.matches.length - 10} more matches\n`;
            totalMatches += r.matches.length - 10;
          }
          output += "\n";
        }

        output += `---\nTotal: ${totalMatches} matches in ${results.length} files.`;

        return {
          content: [{ type: "text", text: output }],
        };
      } catch (error) {
        return {
          content: [
            {
              type: "text",
              text: `Error searching: ${error instanceof Error ? error.message : "Unknown"}`,
            },
          ],
          isError: true,
        };
      }
    }
  );
}
