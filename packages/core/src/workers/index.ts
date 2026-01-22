/**
 * Worker registry and prompts (placeholder for future migration)
 *
 * @module @cervellaswarm/core/workers
 *
 * TODO: Migrate from:
 * - packages/cli/src/agents/spawner.js (WORKER_PROMPTS)
 * - packages/mcp-server/src/agents/spawner.ts (WORKER_CONFIGS)
 */

export const WORKERS_VERSION = '1.0.0-alpha.1';

/**
 * Worker types available in CervellaSwarm
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
 * All agent types
 */
export type AgentType = WorkerType | GuardianType | 'orchestrator' | 'architect';

/**
 * Worker configuration
 */
export interface WorkerConfig {
  name: string;
  prompt: string;
  model: 'sonnet' | 'opus';
  description: string;
}

/**
 * Get list of all available worker types
 */
export function getAvailableWorkers(): WorkerType[] {
  return [
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
}

/**
 * Get list of all guardian types
 */
export function getAvailableGuardians(): GuardianType[] {
  return ['guardiana-qualita', 'guardiana-ops', 'guardiana-ricerca'];
}

/**
 * Check if a worker type is valid
 */
export function isValidWorker(type: string): type is WorkerType {
  return getAvailableWorkers().includes(type as WorkerType);
}

/**
 * Check if a guardian type is valid
 */
export function isValidGuardian(type: string): type is GuardianType {
  return getAvailableGuardians().includes(type as GuardianType);
}

// Placeholder: Worker prompts will be migrated in v1.0.0
export function getWorkersVersion(): string {
  return WORKERS_VERSION;
}
