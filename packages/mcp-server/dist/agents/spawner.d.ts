/**
 * Agent Spawner for MCP Server
 *
 * Launches specialized agents via Anthropic API.
 * Uses @cervellaswarm/core for prompts and worker definitions.
 *
 * Copyright 2026 Rafa & Cervella
 * Licensed under the Apache License, Version 2.0
 */
import { type AgentType } from "@cervellaswarm/core/workers";
type WorkerType = AgentType;
interface WorkerInfo {
    name: string;
    description: string;
}
interface SpawnResult {
    success: boolean;
    output?: string;
    error?: string;
    duration?: string;
    nextStep?: string;
    usage?: {
        inputTokens: number;
        outputTokens: number;
    };
    attempts?: number;
}
/**
 * Get all available workers
 * (Now uses @cervellaswarm/core - single source of truth!)
 */
export declare function getAvailableWorkers(): WorkerInfo[];
/**
 * Spawn a worker to execute a task
 */
export declare function spawnWorker(worker: WorkerType, task: string, context?: string): Promise<SpawnResult>;
export {};
//# sourceMappingURL=spawner.d.ts.map