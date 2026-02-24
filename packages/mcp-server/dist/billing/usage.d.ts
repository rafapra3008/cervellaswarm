/**
 * Usage Tracker for CervellaSwarm
 *
 * Tracks API call usage per billing period.
 * Features:
 * - Atomic file writes with backup
 * - Checksum integrity verification
 * - Serialized writes (race condition safe)
 * - Lazy monthly reset
 *
 * Copyright 2026 CervellaSwarm Contributors
 * Licensed under the Apache License, Version 2.0
 */
import { type Tier, type QuotaResult, QuotaStatus, type UsageStats } from "./types.js";
export { QuotaStatus };
/**
 * Usage Tracker class
 * Singleton pattern for consistent state
 */
declare class UsageTracker {
    private usagePath;
    private backupPath;
    private writeQueue;
    private tierGetter;
    constructor(configDir: string, tierGetter: () => Tier);
    /**
     * Check quota before making an API call
     */
    checkQuota(): Promise<QuotaResult>;
    /**
     * Track a successful API call
     */
    trackCall(): Promise<void>;
    /**
     * Get usage statistics
     */
    getStats(): Promise<UsageStats>;
    /**
     * Get formatted usage message (for check_usage tool)
     */
    getUsageMessage(): Promise<string>;
    /**
     * Serialize write operations to prevent race conditions
     */
    private enqueueWrite;
    /**
     * Load usage data with auto-reset if new period
     */
    private loadUsage;
    /**
     * Load raw usage data from file
     */
    private loadUsageRaw;
    /**
     * Save usage data atomically with backup
     */
    private saveUsage;
    /**
     * Reset to new billing period
     */
    private resetPeriod;
    /**
     * Create initial usage data
     */
    private createInitialUsage;
    /**
     * Compute checksum for integrity verification
     */
    private computeChecksum;
    /**
     * Verify checksum integrity
     */
    private verifyChecksum;
    /**
     * Get current month in YYYY-MM format
     */
    private getCurrentMonth;
    /**
     * Get start of month ISO string
     */
    private getStartOfMonth;
    /**
     * Get end of month ISO string
     */
    private getEndOfMonth;
}
/**
 * Get or create the usage tracker instance
 */
export declare function getUsageTracker(configDir: string, tierGetter: () => Tier): UsageTracker;
/**
 * Reset tracker instance (for testing)
 */
export declare function resetUsageTracker(): void;
//# sourceMappingURL=usage.d.ts.map