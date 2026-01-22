/**
 * Configuration management (placeholder for future migration)
 *
 * @module @cervellaswarm/core/config
 *
 * TODO: Migrate from packages/cli/src/config/
 * - getApiKey()
 * - getDefaultModel()
 * - getTimeout()
 * - getMaxRetries()
 * - Schema validation
 */

export const CONFIG_VERSION = '1.0.0-alpha.1';

// Placeholder exports - will be populated in v1.0.0
export interface ConfigOptions {
  apiKey?: string;
  model?: string;
  timeout?: number;
  maxRetries?: number;
}

export function getConfigVersion(): string {
  return CONFIG_VERSION;
}
