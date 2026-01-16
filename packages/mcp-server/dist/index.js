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
import { getApiKey, hasApiKey } from "./config/manager.js";
// Server metadata
const SERVER_NAME = "cervellaswarm";
const SERVER_VERSION = "0.1.0";
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
server.tool("spawn_worker", "Spawn a CervellaSwarm worker agent to execute a task. " +
    "Available workers: backend, frontend, tester, docs, devops, data, security, researcher. " +
    "The worker will analyze the task and provide code, documentation, or analysis.", {
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
}, async ({ worker, task, context }) => {
    // Check API key
    if (!hasApiKey()) {
        return {
            content: [
                {
                    type: "text",
                    text: "Error: No API key configured.\n\n" +
                        "To use CervellaSwarm, set your Anthropic API key:\n" +
                        "1. Run: cervellaswarm init\n" +
                        "2. Or set: export ANTHROPIC_API_KEY=sk-ant-...\n\n" +
                        "Get your key at: https://console.anthropic.com/",
                },
            ],
            isError: true,
        };
    }
    try {
        const result = await spawnWorker(worker, task, context);
        if (!result.success) {
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
        return {
            content: [
                {
                    type: "text",
                    text: `Worker: cervella-${worker}\n` +
                        `Duration: ${result.duration}\n` +
                        `Tokens: ${result.usage?.inputTokens || 0} in / ${result.usage?.outputTokens || 0} out\n\n` +
                        `---\n\n${result.output}\n\n---\n\n` +
                        `Next step: ${result.nextStep}`,
                },
            ],
        };
    }
    catch (error) {
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
});
/**
 * Tool: list_workers
 * List all available CervellaSwarm workers
 */
server.tool("list_workers", "List all available CervellaSwarm worker agents and their specialties.", {}, async () => {
    const workers = getAvailableWorkers();
    const list = workers
        .map((w) => `- **${w.name}**: ${w.description}`)
        .join("\n");
    return {
        content: [
            {
                type: "text",
                text: "# CervellaSwarm Workers\n\n" +
                    "16 specialized AI agents ready to help:\n\n" +
                    list +
                    "\n\n" +
                    "Use `spawn_worker` to assign a task to any worker.",
            },
        ],
    };
});
/**
 * Tool: check_status
 * Check CervellaSwarm configuration status
 */
server.tool("check_status", "Check if CervellaSwarm is properly configured (API key, etc).", {}, async () => {
    const hasKey = hasApiKey();
    const apiKey = getApiKey();
    let status = "# CervellaSwarm Status\n\n";
    if (hasKey && apiKey) {
        const maskedKey = `${apiKey.substring(0, 10)}...${apiKey.substring(apiKey.length - 4)}`;
        status += `- API Key: Configured (${maskedKey})\n`;
        status += `- Status: Ready\n\n`;
        status += `You can now use \`spawn_worker\` to execute tasks.`;
    }
    else {
        status += `- API Key: Not configured\n`;
        status += `- Status: Not ready\n\n`;
        status += `To configure:\n`;
        status += `1. Run: cervellaswarm init\n`;
        status += `2. Or set: export ANTHROPIC_API_KEY=sk-ant-...\n`;
    }
    return {
        content: [{ type: "text", text: status }],
    };
});
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
//# sourceMappingURL=index.js.map