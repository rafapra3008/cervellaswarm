/**
 * Diagnostics
 *
 * Health checks and API key validation.
 *
 * Copyright 2026 Rafa & Cervella
 * Licensed under the Apache License, Version 2.0
 */

import { getApiKey, getApiKeySource } from './api-key.js';
import { getDefaultModel, getConfigPath } from './settings.js';

/**
 * Run diagnostic checks
 * Returns object with status of each check
 */
export function runDiagnostics() {
  const results = {
    configFile: { status: 'ok', path: getConfigPath() },
    apiKey: { status: 'missing', source: 'none' },
    model: { status: 'ok', value: getDefaultModel() }
  };

  // Check API key
  const apiKey = getApiKey();
  if (apiKey) {
    results.apiKey.status = 'ok';
    results.apiKey.source = getApiKeySource();
    // Mask the key for display
    results.apiKey.preview = `${apiKey.substring(0, 10)}...${apiKey.substring(apiKey.length - 4)}`;
  }

  return results;
}

/**
 * Validate API key by making a test call
 * Returns { valid: boolean, error?: string }
 */
export async function validateApiKey(key = null) {
  const testKey = key || getApiKey();

  if (!testKey) {
    return { valid: false, error: 'No API key provided' };
  }

  if (!testKey.startsWith('sk-ant-')) {
    return { valid: false, error: 'Invalid key format' };
  }

  try {
    // Dynamic import to avoid loading Anthropic if not needed
    const { default: Anthropic } = await import('@anthropic-ai/sdk');
    const client = new Anthropic({ apiKey: testKey });

    // Minimal test call - just check if key works
    await client.messages.create({
      model: 'claude-sonnet-4-6',
      max_tokens: 10,
      messages: [{ role: 'user', content: 'hi' }]
    });

    return { valid: true };
  } catch (error) {
    // Map error codes to user-friendly messages
    if (error.status === 401) {
      return { valid: false, error: 'Invalid API key' };
    }
    if (error.status === 403) {
      return { valid: false, error: 'API key lacks permissions' };
    }
    if (error.status === 429) {
      // Rate limited but key is valid
      return { valid: true, warning: 'Rate limited, but key is valid' };
    }
    return { valid: false, error: error.message || 'Unknown error' };
  }
}
