/**
 * Agent Spawner for MCP Server
 *
 * Launches specialized agents via Anthropic API.
 * Uses @cervellaswarm/core for prompts and worker definitions.
 *
 * Copyright 2026 Rafa & Cervella
 * Licensed under the Apache License, Version 2.0
 */
import Anthropic from "@anthropic-ai/sdk";
import { getApiKey, getDefaultModel, getTimeout, getMaxRetries, } from "../config/manager.js";
import { buildAgentPrompt, getAllAgents, getSuggestedNextStep, } from "@cervellaswarm/core/workers";
// Retry delays (ms)
const RETRY_DELAYS = [1000, 3000, 5000];
// Prompts and next steps now come from @cervellaswarm/core
/**
 * Get all available workers
 * (Now uses @cervellaswarm/core - single source of truth!)
 */
export function getAvailableWorkers() {
    return getAllAgents().map(agent => ({
        name: agent.name.replace(/^cervella-/, ''),
        description: agent.description
    }));
}
/**
 * Sleep utility
 */
function sleep(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
}
/**
 * Build system prompt for worker
 * (Now uses @cervellaswarm/core - single source of truth!)
 */
function buildSystemPrompt(worker, context) {
    const projectContext = context ? {
        description: context
    } : undefined;
    return buildAgentPrompt(worker, projectContext);
}
/**
 * Spawn a worker to execute a task
 */
export async function spawnWorker(worker, task, context) {
    const apiKey = getApiKey();
    if (!apiKey) {
        return {
            success: false,
            error: "API key not configured",
            nextStep: "Run cervellaswarm init or set ANTHROPIC_API_KEY",
        };
    }
    const systemPrompt = buildSystemPrompt(worker, context);
    const model = getDefaultModel();
    const maxTokens = 4096;
    const timeout = getTimeout();
    const maxRetries = getMaxRetries();
    const startTime = Date.now();
    let lastError = null;
    let attempt = 0;
    while (attempt < maxRetries) {
        attempt++;
        try {
            const client = new Anthropic({ apiKey });
            // Create abort controller for timeout
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), timeout);
            try {
                const message = await client.messages.create({
                    model,
                    max_tokens: maxTokens,
                    system: systemPrompt,
                    messages: [{ role: "user", content: task }],
                }, { signal: controller.signal });
                clearTimeout(timeoutId);
                const duration = Math.round((Date.now() - startTime) / 1000);
                const output = message.content
                    .filter((block) => block.type === "text")
                    .map((block) => block.text)
                    .join("\n");
                return {
                    success: true,
                    output: output.trim(),
                    duration: `${duration}s`,
                    nextStep: getSuggestedNextStep(worker),
                    usage: {
                        inputTokens: message.usage.input_tokens,
                        outputTokens: message.usage.output_tokens,
                    },
                    attempts: attempt,
                };
            }
            finally {
                clearTimeout(timeoutId);
            }
        }
        catch (error) {
            lastError = error instanceof Error ? error : new Error(String(error));
            // Check if retryable
            const status = error.status;
            const isRetryable = status === 429 || status === 500 || status === 503;
            if (!isRetryable || attempt >= maxRetries) {
                const duration = Math.round((Date.now() - startTime) / 1000);
                // Map error to user-friendly message
                let errorMessage = lastError.message;
                let nextStep = "Check the error and try again";
                if (status === 401) {
                    errorMessage = "Invalid API key";
                    nextStep =
                        "Your API key is invalid. Get a new one at https://console.anthropic.com/";
                }
                else if (status === 403) {
                    errorMessage = "API key lacks permissions";
                    nextStep =
                        "Your API key doesn't have the required permissions. Check at https://console.anthropic.com/";
                }
                else if (status === 429) {
                    errorMessage = "Rate limit exceeded";
                    nextStep =
                        "You've hit the rate limit. Wait a few seconds and try again, or upgrade your plan.";
                }
                else if (status === 500) {
                    errorMessage = "Anthropic API server error";
                    nextStep =
                        "Anthropic is having issues. Check https://status.anthropic.com/ and try again later.";
                }
                else if (status === 503) {
                    errorMessage = "Anthropic API temporarily unavailable";
                    nextStep =
                        "The API is temporarily overloaded. Wait a moment and try again.";
                }
                else if (lastError.name === "AbortError") {
                    errorMessage = "Request timed out";
                    nextStep = `The request took too long. Try a simpler task or increase timeout.`;
                }
                return {
                    success: false,
                    error: errorMessage,
                    duration: `${duration}s`,
                    nextStep,
                    attempts: attempt,
                };
            }
            // Wait before retry
            const delay = RETRY_DELAYS[attempt - 1] || RETRY_DELAYS[RETRY_DELAYS.length - 1];
            await sleep(delay);
        }
    }
    // Should not reach here
    return {
        success: false,
        error: lastError?.message || "Unknown error after retries",
        nextStep: "Check the error and try again",
        attempts: attempt,
    };
}
//# sourceMappingURL=spawner.js.map