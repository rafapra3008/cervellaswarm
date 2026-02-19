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

import * as fs from "fs";
import * as path from "path";
import * as crypto from "crypto";
import * as os from "os";
import { z } from "zod";
import {
  type UsageData,
  type BillingPeriod,
  type HistoryRecord,
  type Tier,
  type QuotaResult,
  QuotaStatus,
  type UsageStats,
} from "./types.js";
import {
  SCHEMA_VERSION,
  MAX_HISTORY_RECORDS,
  WARNING_THRESHOLD,
  getLimitForTier,
  isUnlimited,
} from "./tiers.js";
import {
  getWarningMessage,
  getLimitExceededMessage,
  getUsageStatusMessage,
} from "./messages.js";

// Re-export QuotaStatus for convenience
export { QuotaStatus };

// Checksum secret (machine-specific)
// Uses hostname + uid for better uniqueness than just USER env var
const CHECKSUM_SECRET =
  process.env.CERVELLASWARM_SECRET ||
  `cs-${process.env.USER || "user"}-${os.hostname()}-${process.getuid?.() ?? 0}`;

// Zod schema for validation
const BillingPeriodSchema = z.object({
  month: z.string().regex(/^\d{4}-\d{2}$/),
  calls: z.number().int().min(0),
  tier: z.enum(["free", "pro", "team", "enterprise"]),
  firstCallAt: z.string().nullable(),
  lastCallAt: z.string().nullable(),
});

const HistoryRecordSchema = z.object({
  month: z.string(),
  calls: z.number().int().min(0),
  tier: z.enum(["free", "pro", "team", "enterprise"]),
  limit: z.number().int().min(0),
  startDate: z.string(),
  endDate: z.string(),
});

const UsageDataSchema = z.object({
  version: z.string(),
  currentPeriod: BillingPeriodSchema,
  history: z.array(HistoryRecordSchema).max(MAX_HISTORY_RECORDS),
  warningShown: z.boolean(),
  lastSyncTime: z.number(),
  _checksum: z.string(),
});

/**
 * Usage Tracker class
 * Singleton pattern for consistent state
 */
class UsageTracker {
  private usagePath: string;
  private backupPath: string;
  private writeQueue: Promise<void> = Promise.resolve();
  private tierGetter: () => Tier;

  constructor(configDir: string, tierGetter: () => Tier) {
    this.usagePath = path.join(configDir, "usage.json");
    this.backupPath = path.join(configDir, "usage.json.backup");
    this.tierGetter = tierGetter;

    // Ensure config directory exists
    if (!fs.existsSync(configDir)) {
      fs.mkdirSync(configDir, { recursive: true, mode: 0o700 });
    }
  }

  /**
   * Check quota before making an API call
   */
  async checkQuota(): Promise<QuotaResult> {
    const data = await this.loadUsage();
    const tier = this.tierGetter();
    const limit = getLimitForTier(tier);

    // Calculate reset date (end of current month)
    const resetsAt = this.getEndOfMonth(data.currentPeriod.month);

    // Unlimited tier
    if (isUnlimited(tier)) {
      return {
        allowed: true,
        status: QuotaStatus.OK,
        used: data.currentPeriod.calls,
        limit,
        remaining: Infinity,
        resetsAt,
      };
    }

    const used = data.currentPeriod.calls;
    const remaining = Math.max(0, limit - used);
    const percentage = used / limit;

    // Exceeded
    if (used >= limit) {
      return {
        allowed: false,
        status: QuotaStatus.EXCEEDED,
        used,
        limit,
        remaining: 0,
        error: getLimitExceededMessage(tier, limit, resetsAt),
        resetsAt,
      };
    }

    // Warning (80%+)
    if (percentage >= WARNING_THRESHOLD && !data.warningShown) {
      // Mark warning as shown
      await this.enqueueWrite(async () => {
        const d = await this.loadUsageRaw();
        d.warningShown = true;
        await this.saveUsage(d);
      });

      return {
        allowed: true,
        status: QuotaStatus.WARNING,
        used,
        limit,
        remaining,
        warning: getWarningMessage(tier, used, limit),
        resetsAt,
      };
    }

    // OK
    return {
      allowed: true,
      status: QuotaStatus.OK,
      used,
      limit,
      remaining,
      resetsAt,
    };
  }

  /**
   * Track a successful API call
   */
  async trackCall(): Promise<void> {
    await this.enqueueWrite(async () => {
      const data = await this.loadUsageRaw();
      const now = new Date().toISOString();

      data.currentPeriod.calls++;
      data.currentPeriod.lastCallAt = now;

      if (!data.currentPeriod.firstCallAt) {
        data.currentPeriod.firstCallAt = now;
      }

      data.lastSyncTime = Date.now();

      await this.saveUsage(data);
    });
  }

  /**
   * Get usage statistics
   */
  async getStats(): Promise<UsageStats> {
    const data = await this.loadUsage();
    const tier = this.tierGetter();
    const limit = getLimitForTier(tier);
    const used = data.currentPeriod.calls;
    const remaining = Math.max(0, limit - used);
    const percentage = isUnlimited(tier) ? 0 : Math.round((used / limit) * 100);
    const resetsAt = this.getEndOfMonth(data.currentPeriod.month);

    let status: QuotaStatus;
    if (percentage >= 100) {
      status = QuotaStatus.EXCEEDED;
    } else if (percentage >= WARNING_THRESHOLD * 100) {
      status = QuotaStatus.WARNING;
    } else {
      status = QuotaStatus.OK;
    }

    return {
      tier,
      calls: used,
      limit,
      remaining,
      percentage,
      period: data.currentPeriod.month,
      resetsAt,
      status,
    };
  }

  /**
   * Get formatted usage message (for check_usage tool)
   */
  async getUsageMessage(): Promise<string> {
    const stats = await this.getStats();
    return getUsageStatusMessage(
      stats.tier,
      stats.calls,
      stats.limit,
      stats.resetsAt
    );
  }

  // ============================================
  // PRIVATE METHODS
  // ============================================

  /**
   * Serialize write operations to prevent race conditions
   */
  private async enqueueWrite(operation: () => Promise<void>): Promise<void> {
    this.writeQueue = this.writeQueue.then(operation).catch((error) => {
      console.error("UsageTracker write error:", error);
      throw error;
    });
    return this.writeQueue;
  }

  /**
   * Load usage data with auto-reset if new period
   */
  private async loadUsage(): Promise<UsageData> {
    let data = await this.loadUsageRaw();

    // Check if period needs reset
    const currentMonth = this.getCurrentMonth();
    if (data.currentPeriod.month !== currentMonth) {
      data = await this.resetPeriod(data, currentMonth);
    }

    return data;
  }

  /**
   * Load raw usage data from file
   */
  private async loadUsageRaw(): Promise<UsageData> {
    // File doesn't exist - initialize
    if (!fs.existsSync(this.usagePath)) {
      const initial = this.createInitialUsage();
      await this.saveUsage(initial);
      return initial;
    }

    try {
      const content = fs.readFileSync(this.usagePath, "utf8");
      const parsed = JSON.parse(content);
      const validated = UsageDataSchema.parse(parsed);

      // Verify checksum integrity
      if (!this.verifyChecksum(validated)) {
        console.warn(
          "UsageTracker: Checksum mismatch - file may have been tampered"
        );
        // Continue anyway for MVP, but log warning
      }

      return validated;
    } catch (error) {
      // Try backup
      if (fs.existsSync(this.backupPath)) {
        console.warn("UsageTracker: Primary file corrupted, trying backup");
        try {
          const backup = fs.readFileSync(this.backupPath, "utf8");
          const parsed = JSON.parse(backup);
          return UsageDataSchema.parse(parsed);
        } catch {
          // Backup also corrupted
        }
      }

      // All corrupted - reinitialize
      console.error("UsageTracker: All files corrupted, reinitializing");
      const initial = this.createInitialUsage();
      await this.saveUsage(initial);
      return initial;
    }
  }

  /**
   * Save usage data atomically with backup
   */
  private async saveUsage(data: UsageData): Promise<void> {
    // Update checksum
    data._checksum = this.computeChecksum(data);

    // Validate before saving
    UsageDataSchema.parse(data);

    // Backup existing file
    if (fs.existsSync(this.usagePath)) {
      fs.copyFileSync(this.usagePath, this.backupPath);
    }

    // Atomic write (write to temp, then rename)
    const tempPath = `${this.usagePath}.tmp`;
    fs.writeFileSync(tempPath, JSON.stringify(data, null, 2), {
      mode: 0o600,
    });
    fs.renameSync(tempPath, this.usagePath);
  }

  /**
   * Reset to new billing period
   */
  private async resetPeriod(
    data: UsageData,
    newMonth: string
  ): Promise<UsageData> {
    const tier = this.tierGetter();
    const limit = getLimitForTier(tier);

    // Archive current period if had calls
    if (data.currentPeriod.calls > 0) {
      const historyRecord: HistoryRecord = {
        month: data.currentPeriod.month,
        calls: data.currentPeriod.calls,
        tier: data.currentPeriod.tier,
        limit: getLimitForTier(data.currentPeriod.tier),
        startDate: this.getStartOfMonth(data.currentPeriod.month),
        endDate: this.getEndOfMonth(data.currentPeriod.month),
      };

      data.history.unshift(historyRecord);

      // Keep only last 12 months
      if (data.history.length > MAX_HISTORY_RECORDS) {
        data.history = data.history.slice(0, MAX_HISTORY_RECORDS);
      }
    }

    // Reset current period
    data.currentPeriod = {
      month: newMonth,
      calls: 0,
      tier,
      firstCallAt: null,
      lastCallAt: null,
    };
    data.warningShown = false;
    data.lastSyncTime = Date.now();

    // Save
    await this.saveUsage(data);

    return data;
  }

  /**
   * Create initial usage data
   */
  private createInitialUsage(): UsageData {
    const tier = this.tierGetter();
    const month = this.getCurrentMonth();

    const data: UsageData = {
      version: SCHEMA_VERSION,
      currentPeriod: {
        month,
        calls: 0,
        tier,
        firstCallAt: null,
        lastCallAt: null,
      },
      history: [],
      warningShown: false,
      lastSyncTime: Date.now(),
      _checksum: "",
    };

    data._checksum = this.computeChecksum(data);
    return data;
  }

  /**
   * Compute checksum for integrity verification
   */
  private computeChecksum(data: UsageData): string {
    const payload = `${data.version}|${data.currentPeriod.month}|${data.currentPeriod.calls}|${data.currentPeriod.tier}|${CHECKSUM_SECRET}`;
    return crypto.createHash("sha256").update(payload).digest("hex");
  }

  /**
   * Verify checksum integrity
   */
  private verifyChecksum(data: UsageData): boolean {
    const expected = this.computeChecksum(data);
    return data._checksum === expected;
  }

  /**
   * Get current month in YYYY-MM format
   */
  private getCurrentMonth(): string {
    return new Date().toISOString().substring(0, 7);
  }

  /**
   * Get start of month ISO string
   */
  private getStartOfMonth(month: string): string {
    return `${month}-01T00:00:00.000Z`;
  }

  /**
   * Get end of month ISO string
   */
  private getEndOfMonth(month: string): string {
    const [year, monthNum] = month.split("-").map(Number);
    const lastDay = new Date(year, monthNum, 0).getDate();
    return `${month}-${String(lastDay).padStart(2, "0")}T23:59:59.999Z`;
  }
}

// ============================================
// SINGLETON INSTANCE
// ============================================

let trackerInstance: UsageTracker | null = null;

/**
 * Get or create the usage tracker instance
 */
export function getUsageTracker(
  configDir: string,
  tierGetter: () => Tier
): UsageTracker {
  if (!trackerInstance) {
    trackerInstance = new UsageTracker(configDir, tierGetter);
  }
  return trackerInstance;
}

/**
 * Reset tracker instance (for testing)
 */
export function resetUsageTracker(): void {
  trackerInstance = null;
}
