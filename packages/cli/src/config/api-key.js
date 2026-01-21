/**
 * API Key Management
 *
 * Functions for managing Anthropic API keys.
 * Priority: Environment variable > Saved config
 *
 * Copyright 2026 Rafa & Cervella
 * Licensed under the Apache License, Version 2.0
 */

import { getGlobalConfig } from './schema.js';

/**
 * Get API key from config or environment
 * Priority: 1. Environment variable, 2. Saved config
 */
export function getApiKey() {
  // Environment variable takes priority (for CI/CD, containers, etc)
  const envKey = process.env.ANTHROPIC_API_KEY;
  if (envKey) {
    return envKey;
  }

  // Fall back to saved config
  const config = getGlobalConfig();
  const savedKey = config.get('apiKey');
  return savedKey || null;
}

/**
 * Save API key to config
 */
export function setApiKey(key) {
  if (!key || typeof key !== 'string') {
    throw new Error('API key must be a non-empty string');
  }

  // Basic validation - Anthropic keys start with 'sk-ant-'
  if (!key.startsWith('sk-ant-')) {
    throw new Error('Invalid API key format. Anthropic keys start with sk-ant-');
  }

  const config = getGlobalConfig();
  config.set('apiKey', key);
  return true;
}

/**
 * Check if API key is configured (either env or saved)
 */
export function hasApiKey() {
  return getApiKey() !== null;
}

/**
 * Clear saved API key from config
 */
export function clearApiKey() {
  const config = getGlobalConfig();
  config.set('apiKey', '');
  return true;
}

/**
 * Get API key source (for diagnostics)
 */
export function getApiKeySource() {
  if (process.env.ANTHROPIC_API_KEY) {
    return 'environment';
  }
  const config = getGlobalConfig();
  if (config.get('apiKey')) {
    return 'config';
  }
  return 'none';
}
