/**
 * Tier Configuration for CervellaSwarm
 *
 * Defines limits and pricing for each subscription tier.
 * Single source of truth for tier-related constants.
 *
 * Copyright 2026 CervellaSwarm Contributors
 * Licensed under the Apache License, Version 2.0
 */
/**
 * Monthly call limits per tier
 */
export const TIER_LIMITS = {
    free: 50,
    pro: 500,
    team: 1000,
    enterprise: Infinity,
};
/**
 * Tier pricing (USD/month)
 */
export const TIER_PRICES = {
    free: 0,
    pro: 20,
    team: 35,
    enterprise: -1, // Custom pricing
};
/**
 * Tier display names
 */
export const TIER_NAMES = {
    free: "Free",
    pro: "Pro",
    team: "Team",
    enterprise: "Enterprise",
};
/**
 * Upgrade path (what's the next tier up)
 */
export const TIER_UPGRADE_PATH = {
    free: "pro",
    pro: "team",
    team: "enterprise",
    enterprise: null,
};
/**
 * Warning threshold (percentage)
 */
export const WARNING_THRESHOLD = 0.8; // 80%
/**
 * Maximum history records to keep
 */
export const MAX_HISTORY_RECORDS = 12;
/**
 * Current schema version
 */
export const SCHEMA_VERSION = "1.0.0";
/**
 * Get limit for a tier
 */
export function getLimitForTier(tier) {
    return TIER_LIMITS[tier] ?? TIER_LIMITS.free;
}
/**
 * Get next upgrade tier
 */
export function getUpgradeTier(currentTier) {
    return TIER_UPGRADE_PATH[currentTier];
}
/**
 * Check if tier has unlimited calls
 */
export function isUnlimited(tier) {
    return TIER_LIMITS[tier] === Infinity;
}
/**
 * Get upgrade URL (placeholder for now)
 */
export function getUpgradeUrl(fromTier) {
    const nextTier = getUpgradeTier(fromTier);
    if (!nextTier) {
        return "https://cervellaswarm.com/contact";
    }
    return `https://cervellaswarm.com/upgrade?from=${fromTier}&to=${nextTier}`;
}
//# sourceMappingURL=tiers.js.map