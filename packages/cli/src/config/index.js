/**
 * Config Module - Main Entry Point
 *
 * Re-exports shared config from @cervellaswarm/core + CLI-specific modules.
 * DRY refactor S508: eliminated 329 LOC of duplicated config code.
 *
 * Copyright 2026 CervellaSwarm Contributors
 * Licensed under the Apache License, Version 2.0
 */

// Shared config from core (schema, api-key, settings)
export {
  getGlobalConfig,
  globalSchema,
  resetGlobalConfig,
  getApiKey,
  setApiKey,
  hasApiKey,
  clearApiKey,
  getApiKeySource,
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
} from '@cervellaswarm/core/config';

// CLI-specific: Diagnostics
export {
  runDiagnostics,
  validateApiKey
} from './diagnostics.js';

// CLI-specific: Billing & Subscription
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
