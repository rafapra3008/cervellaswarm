/**
 * Config Module - Main Entry Point
 *
 * Re-exports all config functions.
 *
 * @example
 * ```ts
 * import { getApiKey, getDefaultModel } from '@cervellaswarm/core/config';
 * ```
 *
 * Copyright 2026 Rafa & Cervella
 * Licensed under the Apache License, Version 2.0
 */

// Types
export type {
  ClaudeModel,
  SubscriptionTier,
  ApiKeySource,
  ConfigSchema,
  ConfigOptions,
  ConfigSummary
} from './types.js';

export {
  VALID_MODELS,
  VALID_TIERS,
  CONFIG_CONSTRAINTS
} from './types.js';

// Schema & Singleton
export {
  getGlobalConfig,
  resetGlobalConfig,
  globalSchema,
  DEFAULT_CONFIG
} from './schema.js';

// API Key Management
export {
  getApiKey,
  setApiKey,
  hasApiKey,
  clearApiKey,
  getApiKeySource
} from './api-key.js';

// Settings (Model, Preferences, Bulk)
export {
  getDefaultModel,
  setDefaultModel,
  getTimeout,
  setTimeout,
  getMaxRetries,
  setMaxRetries,
  isVerbose,
  setVerbose,
  isTelemetryEnabled,
  setTelemetry,
  getAllConfig,
  resetConfig,
  getConfigPath
} from './settings.js';
