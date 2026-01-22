/**
 * Workers Module - Main Entry Point
 *
 * Re-exports all worker/agent functions.
 *
 * @example
 * ```ts
 * import { getAvailableWorkers, buildAgentPrompt } from '@cervellaswarm/core/workers';
 * ```
 *
 * Copyright 2026 Rafa & Cervella
 * Licensed under the Apache License, Version 2.0
 */

export const WORKERS_VERSION = '1.0.0-alpha.2';

// Import for local use
import {
  WORKER_TYPES as _WORKER_TYPES,
  GUARDIAN_TYPES as _GUARDIAN_TYPES
} from './types.js';

// Types
export type {
  WorkerType,
  GuardianType,
  SpecialAgentType,
  AgentType,
  ModelTier,
  AgentConfig,
  ProjectContext,
  SpawnOptions,
  SpawnResult
} from './types.js';

export {
  WORKER_TYPES,
  GUARDIAN_TYPES,
  ALL_AGENT_TYPES
} from './types.js';

// Prompts
export {
  buildBaseContext,
  buildAgentPrompt,
  getAgentPromptData,
  AGENT_PROMPTS
} from './prompts.js';

// Registry
export {
  getAgentConfig,
  getAvailableWorkers,
  getAvailableGuardians,
  getAllAgents,
  isValidAgent,
  normalizeAgentType,
  getSuggestedNextStep,
  AGENT_DESCRIPTIONS,
  AGENT_MODEL_TIERS,
  AGENT_NEXT_STEPS
} from './registry.js';

// Utils
export {
  extractFilesFromOutput,
  extractCodeBlocks,
  estimateTokens,
  formatDuration,
  truncateText,
  parseAgentName,
  hasErrorIndicators,
  extractSummary
} from './utils.js';

/**
 * Check if a worker type is valid
 */
export function isValidWorker(type: string): boolean {
  const normalizedType = type.replace(/^cervella-/, '');
  return (_WORKER_TYPES as readonly string[]).includes(normalizedType);
}

/**
 * Check if a guardian type is valid
 */
export function isValidGuardian(type: string): boolean {
  const normalizedType = type.replace(/^cervella-/, '');
  return (_GUARDIAN_TYPES as readonly string[]).includes(normalizedType);
}

/**
 * Get workers version
 */
export function getWorkersVersion(): string {
  return WORKERS_VERSION;
}
