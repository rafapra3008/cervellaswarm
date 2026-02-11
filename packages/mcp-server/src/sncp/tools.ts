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
  KNOWN_PROJECTS,
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
        .enum(KNOWN_PROJECTS)
        .describe("Project name: cervellaswarm, miracollo, or contabilita"),
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
          project,
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
   * Read stato.md for a project (detailed state)
   */
  server.tool(
    "sncp_read_stato",
    "Read the stato.md (detailed project state) for a CervellaSwarm project. " +
      "Contains: current progress, open issues, technical details.",
    {
      project: z
        .enum(KNOWN_PROJECTS)
        .describe("Project name: cervellaswarm, miracollo, or contabilita"),
    },
    {
      title: "Read Project State",
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: false,
    },
    async ({ project }) => {
      try {
        const { content, path } = await readProjectFile(project, "stato");
        return {
          content: [
            {
              type: "text",
              text:
                `# Stato - ${project}\n` +
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
              text: `Error reading stato.md for ${project}: ${error instanceof Error ? error.message : "File not found"}`,
            },
          ],
          isError: true,
        };
      }
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
            p.hasStato ? "STATO" : "",
            p.hasMemory ? "MEMORY" : "",
          ]
            .filter(Boolean)
            .join(", ");

          output += `## ${p.name}\n`;
          output += `Available: ${indicators}\n`;
          output += `Files: ${p.files.join(", ")}\n\n`;
        }

        output += `\nUse \`sncp_read_ripresa\` or \`sncp_read_stato\` to read specific files.`;

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
      "Searches PROMPT_RIPRESA, stato.md, roadmaps, and other .md files.",
    {
      query: z.string().min(1).describe("Search query (case-insensitive)"),
      project: z
        .enum(KNOWN_PROJECTS)
        .optional()
        .describe("Limit search to a specific project"),
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
        const results = await searchSncp(query, project);

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
