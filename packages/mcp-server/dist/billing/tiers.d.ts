/**
 * Tier Configuration for CervellaSwarm
 *
 * Defines limits and pricing for each subscription tier.
 * Single source of truth for tier-related constants.
 *
 * Copyright 2026 CervellaSwarm Contributors
 * Licensed under the Apache License, Version 2.0
 */
import type { Tier } from "./types.js";
/**
 * Monthly call limits per tier
 */
export declare const TIER_LIMITS: Record<Tier, number>;
/**
 * Tier pricing (USD/month)
 */
export declare const TIER_PRICES: Record<Tier, number>;
/**
 * Tier display names
 */
export declare const TIER_NAMES: Record<Tier, string>;
/**
 * Upgrade path (what's the next tier up)
 */
export declare const TIER_UPGRADE_PATH: Record<Tier, Tier | null>;
/**
 * Warning threshold (percentage)
 */
export declare const WARNING_THRESHOLD = 0.8;
/**
 * Maximum history records to keep
 */
export declare const MAX_HISTORY_RECORDS = 12;
/**
 * Current schema version
 */
export declare const SCHEMA_VERSION = "1.0.0";
/**
 * Get limit for a tier
 */
export declare function getLimitForTier(tier: Tier): number;
/**
 * Get next upgrade tier
 */
export declare function getUpgradeTier(currentTier: Tier): Tier | null;
/**
 * Check if tier has unlimited calls
 */
export declare function isUnlimited(tier: Tier): boolean;
/**
 * Get upgrade URL (placeholder for now)
 */
export declare function getUpgradeUrl(fromTier: Tier): string;
//# sourceMappingURL=tiers.d.ts.map