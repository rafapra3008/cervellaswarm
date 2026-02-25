/**
 * Settings Management
 *
 * Model configuration, preferences, and bulk operations.
 *
 * Copyright 2026 CervellaSwarm Contributors
 * Licensed under the Apache License, Version 2.0
 */

import { getGlobalConfig } from './schema.js';
import { getApiKeySource } from './api-key.js';

// ============================================
// MODEL & AGENT SETTINGS
// ============================================

/**
 * Get default model
 */
export function getDefaultModel() {
  const config = getGlobalConfig();
  return config.get('defaultModel');
}

/**
 * Set default model
 */
export function setDefaultModel(model) {
  const validModels = ['claude-sonnet-4-6', 'claude-opus-4-6', 'claude-sonnet-4-20250514', 'claude-opus-4-5-20251101'];
  if (!validModels.includes(model)) {
    throw new Error(`Invalid model. Choose from: ${validModels.join(', ')}`);
  }
  const config = getGlobalConfig();
  config.set('defaultModel', model);
  return true;
}

/**
 * Get timeout setting (ms)
 */
export function getTimeout() {
  const config = getGlobalConfig();
  return config.get('timeout');
}

/**
 * Set timeout (ms)
 */
export function setTimeout(ms) {
  if (ms < 10000 || ms > 600000) {
    throw new Error('Timeout must be between 10000ms (10s) and 600000ms (10min)');
  }
  const config = getGlobalConfig();
  config.set('timeout', ms);
  return true;
}

/**
 * Get max retries
 */
export function getMaxRetries() {
  const config = getGlobalConfig();
  return config.get('maxRetries');
}

/**
 * Set max retries
 */
export function setMaxRetries(retries) {
  if (retries < 1 || retries > 10) {
    throw new Error('Max retries must be between 1 and 10');
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
export function isVerbose() {
  const config = getGlobalConfig();
  return config.get('verbose');
}

/**
 * Set verbose mode
 */
export function setVerbose(enabled) {
  const config = getGlobalConfig();
  config.set('verbose', !!enabled);
  return true;
}

/**
 * Get telemetry setting
 */
export function isTelemetryEnabled() {
  const config = getGlobalConfig();
  return config.get('telemetry');
}

/**
 * Set telemetry setting
 */
export function setTelemetry(enabled) {
  const config = getGlobalConfig();
  config.set('telemetry', !!enabled);
  return true;
}

// ============================================
// BULK OPERATIONS
// ============================================

/**
 * Get all global config as object
 */
export function getAllConfig() {
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
export function resetConfig() {
  const config = getGlobalConfig();
  config.clear();
  return true;
}

/**
 * Get config file path (for diagnostics)
 */
export function getConfigPath() {
  const config = getGlobalConfig();
  return config.path;
}
