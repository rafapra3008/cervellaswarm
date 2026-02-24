/**
 * Billing Types for CervellaSwarm
 *
 * Type definitions for usage tracking and tier management.
 * Schema designed for local JSON storage with future-proofing.
 *
 * Copyright 2026 CervellaSwarm Contributors
 * Licensed under the Apache License, Version 2.0
 */
/**
 * Available subscription tiers
 */
export type Tier = "free" | "pro" | "team" | "enterprise";
/**
 * Quota check status levels
 */
export declare enum QuotaStatus {
    OK = "ok",// Under 80%
    WARNING = "warning",// 80-99%
    EXCEEDED = "exceeded"
}
/**
 * Current billing period data
 */
export interface BillingPeriod {
    /** Period identifier (YYYY-MM format) */
    month: string;
    /** Number of successful API calls this period */
    calls: number;
    /** Tier snapshot for this period */
    tier: Tier;
    /** ISO8601 timestamp of first call */
    firstCallAt: string | null;
    /** ISO8601 timestamp of last call */
    lastCallAt: string | null;
}
/**
 * Historical period record (for analytics)
 */
export interface HistoryRecord {
    /** Period identifier (YYYY-MM format) */
    month: string;
    /** Total calls made */
    calls: number;
    /** Tier during this period */
    tier: Tier;
    /** Limit that was active */
    limit: number;
    /** ISO8601 start date */
    startDate: string;
    /** ISO8601 end date */
    endDate: string;
}
/**
 * Complete usage data schema (stored in usage.json)
 */
export interface UsageData {
    /** Schema version for migrations */
    version: string;
    /** Current billing period */
    currentPeriod: BillingPeriod;
    /** Historical records (last 12 months max) */
    history: HistoryRecord[];
    /** Whether warning was shown this period */
    warningShown: boolean;
    /** Last sync timestamp (for clock skew detection) */
    lastSyncTime: number;
    /** Integrity checksum */
    _checksum: string;
}
/**
 * Result of quota check
 */
export interface QuotaResult {
    /** Whether the call is allowed */
    allowed: boolean;
    /** Current quota status */
    status: QuotaStatus;
    /** Calls made this period */
    used: number;
    /** Limit for current tier */
    limit: number;
    /** Remaining calls */
    remaining: number;
    /** Warning message (if status is WARNING) */
    warning?: string;
    /** Error message (if status is EXCEEDED) */
    error?: string;
    /** When the period resets (ISO8601) */
    resetsAt: string;
}
/**
 * Usage statistics for check_usage tool
 */
export interface UsageStats {
    /** Current tier */
    tier: Tier;
    /** Calls this period */
    calls: number;
    /** Period limit */
    limit: number;
    /** Remaining calls */
    remaining: number;
    /** Usage percentage (0-100) */
    percentage: number;
    /** Current period month */
    period: string;
    /** When period resets */
    resetsAt: string;
    /** Quota status */
    status: QuotaStatus;
}
//# sourceMappingURL=types.d.ts.map