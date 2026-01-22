/**
 * Worker Types
 *
 * TypeScript types for CervellaSwarm workers and agents.
 *
 * Copyright 2026 Rafa & Cervella
 * Licensed under the Apache License, Version 2.0
 */

/**
 * Worker types available in CervellaSwarm (Sonnet-powered)
 */
export type WorkerType =
  | 'backend'
  | 'frontend'
  | 'tester'
  | 'docs'
  | 'devops'
  | 'data'
  | 'security'
  | 'researcher'
  | 'marketing'
  | 'ingegnera'
  | 'scienziata'
  | 'reviewer';

/**
 * Guardian types (Opus-powered supervisors)
 */
export type GuardianType =
  | 'guardiana-qualita'
  | 'guardiana-ops'
  | 'guardiana-ricerca';

/**
 * Special agent types
 */
export type SpecialAgentType = 'orchestrator' | 'architect';

/**
 * All agent types
 */
export type AgentType = WorkerType | GuardianType | SpecialAgentType;

/**
 * Model tier for agents
 */
export type ModelTier = 'sonnet' | 'opus';

/**
 * Worker/Agent configuration
 */
export interface AgentConfig {
  /** Internal name (e.g., 'backend') */
  name: string;
  /** Full name with prefix (e.g., 'cervella-backend') */
  fullName: string;
  /** Human-readable description */
  description: string;
  /** Model tier to use */
  model: ModelTier;
  /** System prompt template */
  prompt: string;
  /** Focus areas */
  focus: string;
  /** Output style */
  style: string;
}

/**
 * Project context for agent prompts
 */
export interface ProjectContext {
  /** Project name */
  name?: string;
  /** Project description */
  description?: string;
  /** Project path */
  path?: string;
}

/**
 * Agent spawn options
 */
export interface SpawnOptions {
  /** Override default model */
  model?: string;
  /** Max tokens for response */
  maxTokens?: number;
  /** Timeout in milliseconds */
  timeout?: number;
  /** Max retry attempts */
  maxRetries?: number;
}

/**
 * Spawn result
 */
export interface SpawnResult {
  /** Whether the task succeeded */
  success: boolean;
  /** Agent output (on success) */
  output?: string;
  /** Error message (on failure) */
  error?: string;
  /** Duration string (e.g., "5s") */
  duration?: string;
  /** Files mentioned in output */
  filesModified: string[];
  /** Suggested next step */
  nextStep: string;
  /** Token usage (on success) */
  usage?: {
    inputTokens: number;
    outputTokens: number;
  };
  /** Number of attempts made */
  attempts?: number;
}

/**
 * Worker list as array
 */
export const WORKER_TYPES: WorkerType[] = [
  'backend',
  'frontend',
  'tester',
  'docs',
  'devops',
  'data',
  'security',
  'researcher',
  'marketing',
  'ingegnera',
  'scienziata',
  'reviewer',
];

/**
 * Guardian list as array
 */
export const GUARDIAN_TYPES: GuardianType[] = [
  'guardiana-qualita',
  'guardiana-ops',
  'guardiana-ricerca',
];

/**
 * All agent types as array
 */
export const ALL_AGENT_TYPES: AgentType[] = [
  ...WORKER_TYPES,
  ...GUARDIAN_TYPES,
  'orchestrator',
  'architect',
];
