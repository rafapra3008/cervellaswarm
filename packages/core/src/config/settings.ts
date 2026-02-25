/**
 * Settings Management
 *
 * Model configuration, preferences, and bulk operations.
 *
 * Copyright 2026 Rafa & Cervella
 * Licensed under the Apache License, Version 2.0
 */

import { getGlobalConfig } from './schema.js';
import { getApiKeySource } from './api-key.js';
import {
  type ClaudeModel,
  type ConfigSummary,
  VALID_MODELS,
  CONFIG_CONSTRAINTS
} from './types.js';

// ============================================
// MODEL & AGENT SETTINGS
// ============================================

/**
 * Get default model
 */
export function getDefaultModel(): ClaudeModel {
  const config = getGlobalConfig();
  return config.get('defaultModel');
}

/**
 * Set default model
 * @throws Error if model is invalid
 */
export function setDefaultModel(model: ClaudeModel): boolean {
  if (!VALID_MODELS.includes(model)) {
    throw new Error(`Invalid model. Choose from: ${VALID_MODELS.join(', ')}`);
  }
  const config = getGlobalConfig();
  config.set('defaultModel', model);
  return true;
}

/**
 * Get timeout setting (ms)
 */
export function getTimeout(): number {
  const config = getGlobalConfig();
  return config.get('timeout');
}

/**
 * Set timeout (ms)
 * @throws Error if timeout is out of range
 */
export function setTimeout(ms: number): boolean {
  const { min, max } = CONFIG_CONSTRAINTS.timeout;
  if (ms < min || ms > max) {
    throw new Error(`Timeout must be between ${min}ms (${min/1000}s) and ${max}ms (${max/60000}min)`);
  }
  const config = getGlobalConfig();
  config.set('timeout', ms);
  return true;
}

/**
 * Get max retries
 */
export function getMaxRetries(): number {
  const config = getGlobalConfig();
  return config.get('maxRetries');
}

/**
 * Set max retries
 * @throws Error if retries is out of range
 */
export function setMaxRetries(retries: number): boolean {
  const { min, max } = CONFIG_CONSTRAINTS.maxRetries;
  if (retries < min || retries > max) {
    throw new Error(`Max retries must be between ${min} and ${max}`);
  }
  const config = getGlobalConfig();
  config.set('maxRetries', retries);
  return true;
}

// ============================================
// PREFERENCES
// ============================================

/**
 * Get verbose mode
 */
export function isVerbose(): boolean {
  const config = getGlobalConfig();
  return config.get('verbose');
}

/**
 * Set verbose mode
 */
export function setVerbose(enabled: boolean): boolean {
  const config = getGlobalConfig();
  config.set('verbose', !!enabled);
  return true;
}

/**
 * Get telemetry setting
 */
export function isTelemetryEnabled(): boolean {
  const config = getGlobalConfig();
  return config.get('telemetry');
}

/**
 * Set telemetry setting
 */
export function setTelemetry(enabled: boolean): boolean {
  const config = getGlobalConfig();
  config.set('telemetry', !!enabled);
  return true;
}

// ============================================
// BULK OPERATIONS
// ============================================

/**
 * Get all global config as object (safe to display)
 */
export function getAllConfig(): ConfigSummary {
  const config = getGlobalConfig();
  return {
    apiKey: config.get('apiKey') ? '***configured***' : 'not set',
    apiKeySource: getApiKeySource(),
    defaultModel: config.get('defaultModel'),
    timeout: config.get('timeout'),
    maxRetries: config.get('maxRetries'),
    verbose: config.get('verbose'),
    telemetry: config.get('telemetry')
  };
}

/**
 * Reset all config to defaults
 */
export function resetConfig(): boolean {
  const config = getGlobalConfig();
  config.clear();
  return true;
}

/**
 * Get config file path (for diagnostics)
 */
export function getConfigPath(): string {
  const config = getGlobalConfig();
  return config.path;
}
