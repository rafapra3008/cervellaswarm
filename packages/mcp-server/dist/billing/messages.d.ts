/**
 * UX Messages for CervellaSwarm Billing
 *
 * User-friendly messages for quota warnings and limits.
 * Designed to be helpful, not aggressive.
 *
 * Copyright 2026 CervellaSwarm Contributors
 * Licensed under the Apache License, Version 2.0
 */
import type { Tier } from "./types.js";
/**
 * Get warning message (shown at 80% usage)
 */
export declare function getWarningMessage(tier: Tier, used: number, limit: number): string;
/**
 * Get limit exceeded message (shown at 100%)
 */
export declare function getLimitExceededMessage(tier: Tier, limit: number, resetsAt: string): string;
/**
 * Get usage status message (for check_usage tool)
 */
export declare function getUsageStatusMessage(tier: Tier, used: number, limit: number, resetsAt: string): string;
/**
 * Get first-time welcome message
 */
export declare function getWelcomeMessage(tier: Tier): string;
//# sourceMappingURL=messages.d.ts.map