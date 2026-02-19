/**
 * Config Schema & Singleton
 *
 * Base configuration schema and singleton instance for CervellaSwarm CLI.
 *
 * Copyright 2026 CervellaSwarm Contributors
 * Licensed under the Apache License, Version 2.0
 */

import Conf from 'conf';

// Schema for global config validation
export const globalSchema = {
  apiKey: {
    type: 'string',
    default: ''
  },
  defaultModel: {
    type: 'string',
    enum: ['claude-sonnet-4-6', 'claude-opus-4-6', 'claude-sonnet-4-20250514', 'claude-opus-4-5-20251101'],
    default: 'claude-sonnet-4-6'
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
  // Billing/Subscription fields
  tier: {
    type: 'string',
    enum: ['free', 'pro', 'team', 'enterprise'],
    default: 'free'
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
};

// Global config instance (singleton)
let globalConfig = null;

/**
 * Get global config instance
 * Creates it on first call with schema validation
 */
export function getGlobalConfig() {
  if (!globalConfig) {
    globalConfig = new Conf({
      projectName: 'cervellaswarm',
      schema: globalSchema,
      defaults: {
        apiKey: '',
        defaultModel: 'claude-sonnet-4-6',
        timeout: 120000,
        maxRetries: 3,
        verbose: false,
        telemetry: false,
        tier: 'free',
        customerId: '',
        subscriptionId: '',
        email: '',
        lastSync: 0
      }
    });
  }
  return globalConfig;
}

/**
 * Reset singleton (for testing)
 */
export function resetGlobalConfig() {
  globalConfig = null;
}
