/**
 * Config Module - Main Entry Point
 *
 * Re-exports all config functions for backward compatibility.
 * Import from here: import { getApiKey } from './config/index.js'
 *
 * Copyright 2026 Rafa & Cervella
 * Licensed under the Apache License, Version 2.0
 */

// Schema & Singleton
export { getGlobalConfig, globalSchema, resetGlobalConfig } from './schema.js';

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

// Diagnostics
export {
  runDiagnostics,
  validateApiKey
} from './diagnostics.js';

// Billing & Subscription
export {
  getBillingApiUrl,
  getTier,
  setTier,
  getCustomerId,
  setCustomerId,
  getSubscriptionId,
  setSubscriptionId,
  getEmail,
  setEmail,
  getLastSync,
  setLastSync,
  updateSubscriptionData,
  getSubscriptionInfo,
  needsSync
} from './billing.js';
