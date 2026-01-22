/**
 * Agent Registry
 *
 * Central registry of all CervellaSwarm agents.
 *
 * Copyright 2026 Rafa & Cervella
 * Licensed under the Apache License, Version 2.0
 */

import type {
  WorkerType,
  GuardianType,
  AgentType,
  AgentConfig,
  ModelTier
} from './types.js';
import { AGENT_PROMPTS } from './prompts.js';

/**
 * Agent descriptions for CLI/UI
 */
export const AGENT_DESCRIPTIONS: Record<string, string> = {
  'backend': 'Python, FastAPI, API, Database',
  'frontend': 'React, CSS, Tailwind, UI/UX',
  'tester': 'Testing, Debug, QA',
  'docs': 'Documentation, README, Guides',
  'devops': 'Deploy, CI/CD, Docker',
  'data': 'SQL, Analytics, Database Design',
  'security': 'Security Audit, Vulnerabilities',
  'researcher': 'Research, Analysis, Best Practices',
  'marketing': 'Marketing, UX Strategy, Positioning',
  'ingegnera': 'Codebase Analysis, Technical Debt',
  'scienziata': 'Market Research, Competitor Analysis',
  'reviewer': 'Code Review, Best Practices',
  'guardiana-qualita': 'Quality Gate, Standards Verification',
  'guardiana-ops': 'Ops Security, Deployment Validation',
  'guardiana-ricerca': 'Research Quality, Fact Checking',
  'orchestrator': 'Team Coordination, Task Delegation',
  'architect': 'Architecture Planning, System Design'
};

/**
 * Model tier for each agent type
 */
export const AGENT_MODEL_TIERS: Record<string, ModelTier> = {
  // Workers use Sonnet
  'backend': 'sonnet',
  'frontend': 'sonnet',
  'tester': 'sonnet',
  'docs': 'sonnet',
  'devops': 'sonnet',
  'data': 'sonnet',
  'security': 'sonnet',
  'researcher': 'sonnet',
  'marketing': 'sonnet',
  'ingegnera': 'sonnet',
  'scienziata': 'sonnet',
  'reviewer': 'sonnet',
  // Guardians and special agents use Opus
  'guardiana-qualita': 'opus',
  'guardiana-ops': 'opus',
  'guardiana-ricerca': 'opus',
  'orchestrator': 'opus',
  'architect': 'opus'
};

/**
 * Suggested next steps per agent type
 */
export const AGENT_NEXT_STEPS: Record<string, string> = {
  'backend': 'Review the code and run: npm test',
  'frontend': 'Preview in browser: npm run dev',
  'tester': 'Run the test suite: npm test',
  'docs': 'Review documentation for clarity',
  'devops': 'Test deployment in staging first',
  'data': 'Verify query performance with EXPLAIN',
  'security': 'Apply the security fixes',
  'researcher': 'Apply findings to your project',
  'marketing': 'Validate with user feedback',
  'ingegnera': 'Prioritize technical debt items',
  'scienziata': 'Create action plan from insights',
  'reviewer': 'Address review comments',
  'guardiana-qualita': 'Fix issues before merge',
  'guardiana-ops': 'Implement security recommendations',
  'guardiana-ricerca': 'Update research with corrections',
  'orchestrator': 'Execute delegated tasks',
  'architect': 'Begin implementation per plan'
};

/**
 * Get agent configuration by type
 */
export function getAgentConfig(type: string): AgentConfig | null {
  const promptData = AGENT_PROMPTS[type];
  if (!promptData) return null;

  return {
    name: type,
    fullName: `cervella-${type}`,
    description: AGENT_DESCRIPTIONS[type] || '',
    model: AGENT_MODEL_TIERS[type] || 'sonnet',
    prompt: promptData.intro,
    focus: promptData.focus,
    style: promptData.style
  };
}

/**
 * Get all available workers (Sonnet-powered)
 */
export function getAvailableWorkers(): Array<{ name: string; description: string }> {
  const workers: WorkerType[] = [
    'backend', 'frontend', 'tester', 'docs',
    'devops', 'data', 'security', 'researcher',
    'marketing', 'ingegnera', 'scienziata', 'reviewer'
  ];

  return workers.map(w => ({
    name: `cervella-${w}`,
    description: AGENT_DESCRIPTIONS[w] || ''
  }));
}

/**
 * Get all available guardians (Opus-powered)
 */
export function getAvailableGuardians(): Array<{ name: string; description: string }> {
  const guardians: GuardianType[] = [
    'guardiana-qualita', 'guardiana-ops', 'guardiana-ricerca'
  ];

  return guardians.map(g => ({
    name: `cervella-${g}`,
    description: AGENT_DESCRIPTIONS[g] || ''
  }));
}

/**
 * Get all available agents
 */
export function getAllAgents(): Array<{ name: string; description: string; model: ModelTier }> {
  return Object.entries(AGENT_DESCRIPTIONS).map(([type, desc]) => ({
    name: `cervella-${type}`,
    description: desc,
    model: AGENT_MODEL_TIERS[type] || 'sonnet'
  }));
}

/**
 * Check if agent type is valid
 */
export function isValidAgent(type: string): boolean {
  // Handle both formats: 'backend' and 'cervella-backend'
  const normalizedType = type.replace(/^cervella-/, '');
  return normalizedType in AGENT_DESCRIPTIONS;
}

/**
 * Normalize agent type (remove cervella- prefix if present)
 */
export function normalizeAgentType(type: string): string {
  return type.replace(/^cervella-/, '');
}

/**
 * Get suggested next step for an agent
 */
export function getSuggestedNextStep(agentType: string): string {
  const normalizedType = normalizeAgentType(agentType);
  return AGENT_NEXT_STEPS[normalizedType] || 'Continue with your next task';
}
