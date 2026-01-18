#!/usr/bin/env node
/**
 * CervellaSwarm MCP Server
 *
 * 16 AI agents exposed as MCP tools for Claude Code integration.
 * "Not an assistant - a TEAM."
 *
 * Copyright 2026 Rafa & Cervella
 * Licensed under the Apache License, Version 2.0
 * http://www.apache.org/licenses/LICENSE-2.0
 */

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { spawnWorker, getAvailableWorkers } from "./agents/spawner.js";
import {
  getApiKey,
  hasApiKey,
  getApiKeySource,
  validateApiKey,
  getConfigPath,
  getConfigDir,
  getTier,
} from "./config/manager.js";
import { getUsageTracker, QuotaStatus } from "./billing/usage.js";

// Server metadata
const SERVER_NAME = "cervellaswarm";
const SERVER_VERSION = "0.2.1";

// Create MCP server instance
const server = new McpServer({
  name: SERVER_NAME,
  version: SERVER_VERSION,
});

// ============================================
// TOOLS
// ============================================

/**
 * Tool: spawn_worker
 * Spawn a specialized AI agent to execute a task
 */
server.tool(
  "spawn_worker",
  "Spawn a CervellaSwarm worker agent to execute a task. " +
    "Available workers: backend, frontend, tester, docs, devops, data, security, researcher. " +
    "The worker will analyze the task and provide code, documentation, or analysis.",
  {
    worker: z
      .enum([
        "backend",
        "frontend",
        "tester",
        "docs",
        "devops",
        "data",
        "security",
        "researcher",
      ])
      .describe("The type of worker to spawn"),
    task: z.string().min(1).describe("The task description for the worker"),
    context: z
      .string()
      .optional()
      .describe("Additional context about the project or task"),
  },
  {
    title: "Spawn CervellaSwarm Worker",
    readOnlyHint: false,
    destructiveHint: false,
    idempotentHint: false,
    openWorldHint: true,
  },
  async ({ worker, task, context }) => {
    // Check API key
    if (!hasApiKey()) {
      return {
        content: [
          {
            type: "text",
            text:
              "Error: No API key configured.\n\n" +
              "To use CervellaSwarm, set your Anthropic API key:\n" +
              "1. Run: cervellaswarm init\n" +
              "2. Or set: export ANTHROPIC_API_KEY=sk-ant-...\n\n" +
              "Get your key at: https://console.anthropic.com/",
          },
        ],
        isError: true,
      };
    }

    // Check quota before executing
    const usageTracker = getUsageTracker(getConfigDir(), getTier);
    const quotaResult = await usageTracker.checkQuota();

    if (!quotaResult.allowed) {
      return {
        content: [
          {
            type: "text",
            text: quotaResult.error || "Monthly limit reached.",
          },
        ],
        isError: true,
      };
    }

    // Show warning if approaching limit (but still allow)
    let warningMessage = "";
    if (quotaResult.status === QuotaStatus.WARNING && quotaResult.warning) {
      warningMessage = `\n\n---\n\n⚠️ ${quotaResult.warning}`;
    }

    try {
      const result = await spawnWorker(worker, task, context);

      if (!result.success) {
        // Failed calls don't count toward quota
        return {
          content: [
            {
              type: "text",
              text: `Error: ${result.error}\n\nNext step: ${result.nextStep}`,
            },
          ],
          isError: true,
        };
      }

      // Track successful call
      await usageTracker.trackCall();

      // Get updated usage for display
      const stats = await usageTracker.getStats();
      const usageInfo = `Usage: ${stats.calls}/${stats.limit} calls this month`;

      return {
        content: [
          {
            type: "text",
            text:
              `Worker: cervella-${worker}\n` +
              `Duration: ${result.duration}\n` +
              `Tokens: ${result.usage?.inputTokens || 0} in / ${result.usage?.outputTokens || 0} out\n` +
              `${usageInfo}\n\n` +
              `---\n\n${result.output}\n\n---\n\n` +
              `Next step: ${result.nextStep}${warningMessage}`,
          },
        ],
      };
    } catch (error) {
      return {
        content: [
          {
            type: "text",
            text: `Unexpected error: ${error instanceof Error ? error.message : "Unknown"}`,
          },
        ],
        isError: true,
      };
    }
  }
);

/**
 * Tool: list_workers
 * List all available CervellaSwarm workers
 */
server.tool(
  "list_workers",
  "List all available CervellaSwarm worker agents and their specialties.",
  {},
  {
    title: "List Available Workers",
    readOnlyHint: true,
    destructiveHint: false,
    idempotentHint: true,
    openWorldHint: false,
  },
  async () => {
    const workers = getAvailableWorkers();

    const list = workers
      .map((w) => `- **${w.name}**: ${w.description}`)
      .join("\n");

    return {
      content: [
        {
          type: "text",
          text:
            "# CervellaSwarm Workers\n\n" +
            "16 specialized AI agents ready to help:\n\n" +
            list +
            "\n\n" +
            "Use `spawn_worker` to assign a task to any worker.",
        },
      ],
    };
  }
);

/**
 * Tool: check_status
 * Check CervellaSwarm configuration status with optional validation
 */
server.tool(
  "check_status",
  "Check if CervellaSwarm is properly configured (API key, etc).",
  {
    validate: z
      .boolean()
      .optional()
      .default(false)
      .describe("If true, validates the API key with a test call to Anthropic"),
  },
  {
    title: "Check Configuration Status",
    readOnlyHint: true,
    destructiveHint: false,
    idempotentHint: true,
    openWorldHint: true,
  },
  async ({ validate }) => {
    const hasKey = hasApiKey();
    const apiKey = getApiKey();
    const keySource = getApiKeySource();
    const configPath = getConfigPath();

    let status = "# CervellaSwarm Status\n\n";

    // Basic info
    status += `## Configuration\n\n`;
    status += `- Config file: \`${configPath}\`\n`;
    status += `- Server version: ${SERVER_VERSION}\n\n`;

    // API Key section
    status += `## API Key\n\n`;

    if (hasKey && apiKey) {
      const maskedKey = `${apiKey.substring(0, 10)}...${apiKey.substring(apiKey.length - 4)}`;
      status += `- Status: Configured\n`;
      status += `- Source: ${keySource}\n`;
      status += `- Key: \`${maskedKey}\`\n`;

      // Validate if requested
      if (validate) {
        status += `\n### Validation\n\n`;
        const result = await validateApiKey();

        if (result.valid) {
          if (result.warning) {
            status += `- Result: Valid (with warning)\n`;
            status += `- Warning: ${result.warning}\n`;
          } else {
            status += `- Result: Valid\n`;
            status += `- API connection: Working\n`;
          }
        } else {
          status += `- Result: Invalid\n`;
          status += `- Error: ${result.error}\n`;
          status += `\nTo fix: Check your API key at https://console.anthropic.com/\n`;
        }
      }

      status += `\n## Ready\n\n`;
      status += `You can now use \`spawn_worker\` to execute tasks.\n`;
      if (!validate) {
        status += `\nTip: Use \`check_status(validate=true)\` to test the API connection.`;
      }
    } else {
      status += `- Status: Not configured\n`;
      status += `- Source: none\n\n`;
      status += `## Setup Required\n\n`;
      status += `To configure your API key:\n\n`;
      status += `1. **Recommended:** Run \`cervellaswarm init\`\n`;
      status += `2. **Alternative:** Set environment variable:\n`;
      status += `   \`\`\`\n`;
      status += `   export ANTHROPIC_API_KEY=sk-ant-...\n`;
      status += `   \`\`\`\n\n`;
      status += `Get your key at: https://console.anthropic.com/`;
    }

    return {
      content: [{ type: "text", text: status }],
    };
  }
);

/**
 * Tool: check_usage
 * Check current usage and quota status
 */
server.tool(
  "check_usage",
  "Check your current CervellaSwarm usage, remaining calls, and quota status.",
  {},
  {
    title: "Check Usage and Quota",
    readOnlyHint: true,
    destructiveHint: false,
    idempotentHint: true,
    openWorldHint: false,
  },
  async () => {
    const usageTracker = getUsageTracker(getConfigDir(), getTier);
    const message = await usageTracker.getUsageMessage();

    return {
      content: [{ type: "text", text: message }],
    };
  }
);

// ============================================
// RESOURCES
// ============================================

// TODO: Add SNCP resources in future versions
// - Project state (.sncp/progetti/*/stato.md)
// - Session history
// - Worker reports

// ============================================
// PROMPTS
// ============================================

// TODO: Add prompts in future versions
// - coordinate_workers: Plan multi-agent tasks
// - analyze_codebase: Full project analysis

// ============================================
// START SERVER
// ============================================

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error(`CervellaSwarm MCP Server v${SERVER_VERSION} started`);
}

main().catch((error) => {
  console.error("Failed to start server:", error);
  process.exit(1);
});
