/**
 * Billing & Subscription
 *
 * Tier management, subscription data, and sync logic.
 *
 * Copyright 2026 CervellaSwarm Contributors
 * Licensed under the Apache License, Version 2.0
 */

import { getGlobalConfig } from './schema.js';

// API URL for billing backend
const BILLING_API_URL = process.env.CERVELLASWARM_API_URL || 'https://cervellaswarm-api.fly.dev';

/**
 * Get billing API URL
 */
export function getBillingApiUrl() {
  return BILLING_API_URL;
}

/**
 * Get current tier
 */
export function getTier() {
  const config = getGlobalConfig();
  return config.get('tier');
}

/**
 * Set tier
 */
export function setTier(tier) {
  const validTiers = ['free', 'pro', 'team', 'enterprise'];
  if (!validTiers.includes(tier)) {
    throw new Error(`Invalid tier. Choose from: ${validTiers.join(', ')}`);
  }
  const config = getGlobalConfig();
  config.set('tier', tier);
  return true;
}

/**
 * Get customer ID
 */
export function getCustomerId() {
  const config = getGlobalConfig();
  return config.get('customerId') || null;
}

/**
 * Set customer ID
 */
export function setCustomerId(customerId) {
  const config = getGlobalConfig();
  config.set('customerId', customerId);
  return true;
}

/**
 * Get subscription ID
 */
export function getSubscriptionId() {
  const config = getGlobalConfig();
  return config.get('subscriptionId') || null;
}

/**
 * Set subscription ID
 */
export function setSubscriptionId(subscriptionId) {
  const config = getGlobalConfig();
  config.set('subscriptionId', subscriptionId);
  return true;
}

/**
 * Get email
 */
export function getEmail() {
  const config = getGlobalConfig();
  return config.get('email') || null;
}

/**
 * Set email
 */
export function setEmail(email) {
  const config = getGlobalConfig();
  config.set('email', email);
  return true;
}

/**
 * Get last sync timestamp
 */
export function getLastSync() {
  const config = getGlobalConfig();
  return config.get('lastSync') || 0;
}

/**
 * Set last sync timestamp
 */
export function setLastSync(timestamp = Date.now()) {
  const config = getGlobalConfig();
  config.set('lastSync', timestamp);
  return true;
}

/**
 * Update subscription data from API response
 */
export function updateSubscriptionData(data) {
  const config = getGlobalConfig();
  if (data.tier) config.set('tier', data.tier);
  if (data.customerId) config.set('customerId', data.customerId);
  if (data.subscriptionId) config.set('subscriptionId', data.subscriptionId);
  if (data.email) config.set('email', data.email);
  config.set('lastSync', Date.now());
  return true;
}

/**
 * Get subscription info for display
 */
export function getSubscriptionInfo() {
  const config = getGlobalConfig();
  return {
    tier: config.get('tier'),
    customerId: config.get('customerId') || null,
    subscriptionId: config.get('subscriptionId') || null,
    email: config.get('email') || null,
    lastSync: config.get('lastSync') || 0
  };
}

/**
 * Check if subscription needs sync (older than 24h)
 */
export function needsSync() {
  const lastSync = getLastSync();
  const twentyFourHours = 24 * 60 * 60 * 1000;
  return Date.now() - lastSync > twentyFourHours;
}
