/**
 * Config Schema & Singleton
 *
 * Base configuration schema and singleton instance for CervellaSwarm.
 *
 * Copyright 2026 Rafa & Cervella
 * Licensed under the Apache License, Version 2.0
 */

import Conf from 'conf';
import type { ConfigSchema, ClaudeModel, SubscriptionTier } from './types.js';

/**
 * Schema for Conf validation
 */
export const globalSchema = {
  apiKey: {
    type: 'string',
    default: ''
  },
  defaultModel: {
    type: 'string',
    enum: ['claude-sonnet-4-20250514', 'claude-opus-4-5-20251101'] as ClaudeModel[],
    default: 'claude-sonnet-4-20250514' as ClaudeModel
  },
  timeout: {
    type: 'number',
    minimum: 10000,
    maximum: 600000,
    default: 120000
  },
  maxRetries: {
    type: 'number',
    minimum: 1,
    maximum: 10,
    default: 3
  },
  verbose: {
    type: 'boolean',
    default: false
  },
  telemetry: {
    type: 'boolean',
    default: false
  },
  tier: {
    type: 'string',
    enum: ['free', 'pro', 'team', 'enterprise'] as SubscriptionTier[],
    default: 'free' as SubscriptionTier
  },
  customerId: {
    type: 'string',
    default: ''
  },
  subscriptionId: {
    type: 'string',
    default: ''
  },
  email: {
    type: 'string',
    default: ''
  },
  lastSync: {
    type: 'number',
    default: 0
  }
} as const;

/**
 * Default configuration values
 */
export const DEFAULT_CONFIG: ConfigSchema = {
  apiKey: '',
  defaultModel: 'claude-sonnet-4-20250514',
  timeout: 120000,
  maxRetries: 3,
  verbose: false,
  telemetry: false,
  tier: 'free',
  customerId: '',
  subscriptionId: '',
  email: '',
  lastSync: 0
};

// Global config instance (singleton)
let globalConfig: Conf<ConfigSchema> | null = null;

/**
 * Get global config instance
 * Creates it on first call with schema validation
 */
export function getGlobalConfig(): Conf<ConfigSchema> {
  if (!globalConfig) {
    globalConfig = new Conf<ConfigSchema>({
      projectName: 'cervellaswarm',
      schema: globalSchema as any,
      defaults: DEFAULT_CONFIG
    });
  }
  return globalConfig;
}

/**
 * Reset singleton (for testing)
 */
export function resetGlobalConfig(): void {
  globalConfig = null;
}
