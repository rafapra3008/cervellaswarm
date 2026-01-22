/**
 * Configuration Types
 *
 * TypeScript types for CervellaSwarm configuration.
 *
 * Copyright 2026 Rafa & Cervella
 * Licensed under the Apache License, Version 2.0
 */

/**
 * Supported Claude models
 */
export type ClaudeModel = 'claude-sonnet-4-20250514' | 'claude-opus-4-5-20251101';

/**
 * Subscription tiers
 */
export type SubscriptionTier = 'free' | 'pro' | 'team' | 'enterprise';

/**
 * API key source
 */
export type ApiKeySource = 'environment' | 'config' | 'none';

/**
 * Full configuration schema
 */
export interface ConfigSchema {
  apiKey: string;
  defaultModel: ClaudeModel;
  timeout: number;
  maxRetries: number;
  verbose: boolean;
  telemetry: boolean;
  tier: SubscriptionTier;
  customerId: string;
  subscriptionId: string;
  email: string;
  lastSync: number;
}

/**
 * Configuration options for initialization
 */
export interface ConfigOptions {
  apiKey?: string;
  model?: ClaudeModel;
  timeout?: number;
  maxRetries?: number;
}

/**
 * Config summary (safe to display)
 */
export interface ConfigSummary {
  apiKey: string; // masked
  apiKeySource: ApiKeySource;
  defaultModel: ClaudeModel;
  timeout: number;
  maxRetries: number;
  verbose: boolean;
  telemetry: boolean;
}

/**
 * Valid models list
 */
export const VALID_MODELS: ClaudeModel[] = [
  'claude-sonnet-4-20250514',
  'claude-opus-4-5-20251101'
];

/**
 * Valid tiers list
 */
export const VALID_TIERS: SubscriptionTier[] = [
  'free',
  'pro',
  'team',
  'enterprise'
];

/**
 * Configuration constraints
 */
export const CONFIG_CONSTRAINTS = {
  timeout: {
    min: 10000,   // 10 seconds
    max: 600000   // 10 minutes
  },
  maxRetries: {
    min: 1,
    max: 10
  }
} as const;
