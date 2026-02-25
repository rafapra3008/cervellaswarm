/**
 * Tests for billing/usage.ts
 *
 * Tests usage tracking, quota checking, and billing logic.
 */

import { describe, it, beforeEach, afterEach } from "node:test";
import assert from "node:assert/strict";
import * as fs from "fs";
import * as path from "path";
import * as os from "os";
import { getUsageTracker, resetUsageTracker, QuotaStatus } from "../dist/billing/usage.js";
import type { Tier } from "../dist/billing/types.js";

describe("Usage Tracker", () => {
  let testConfigDir: string;

  beforeEach(() => {
    // Create temp directory for tests
    testConfigDir = fs.mkdtempSync(path.join(os.tmpdir(), "cervellaswarm-test-"));
    resetUsageTracker();
  });

  afterEach(() => {
    // Cleanup
    if (fs.existsSync(testConfigDir)) {
      fs.rmSync(testConfigDir, { recursive: true, force: true });
    }
    resetUsageTracker();
  });

  describe("Initialization", () => {
    it("should create usage file on first use", async () => {
      const tracker = getUsageTracker(testConfigDir, () => "free");
      await tracker.checkQuota();

      const usageFile = path.join(testConfigDir, "usage.json");
      assert.ok(fs.existsSync(usageFile));
    });

    it("should initialize with zero calls", async () => {
      const tracker = getUsageTracker(testConfigDir, () => "free");
      const stats = await tracker.getStats();

      assert.equal(stats.calls, 0);
      assert.equal(stats.remaining, 50); // free tier limit
    });

    it("should use correct tier limit", async () => {
      const tracker = getUsageTracker(testConfigDir, () => "pro");
      const stats = await tracker.getStats();

      assert.equal(stats.limit, 500); // pro tier limit
    });
  });

  describe("checkQuota - Free Tier", () => {
    it("should allow calls when under limit", async () => {
      const tracker = getUsageTracker(testConfigDir, () => "free");
      const result = await tracker.checkQuota();

      assert.equal(result.allowed, true);
      assert.equal(result.status, QuotaStatus.OK);
      assert.equal(result.used, 0);
      assert.equal(result.limit, 50);
      assert.equal(result.remaining, 50);
    });

    it("should show warning at 80% usage", async () => {
      const tracker = getUsageTracker(testConfigDir, () => "free");

      // Track 40 calls (80% of 50)
      for (let i = 0; i < 40; i++) {
        await tracker.trackCall();
      }

      const result = await tracker.checkQuota();

      assert.equal(result.allowed, true);
      assert.equal(result.status, QuotaStatus.WARNING);
      assert.equal(result.used, 40);
      assert.equal(result.remaining, 10);
      assert.ok(result.warning);
    });

    it("should block calls when limit exceeded", async () => {
      const tracker = getUsageTracker(testConfigDir, () => "free");

      // Track 50 calls (100% of limit)
      for (let i = 0; i < 50; i++) {
        await tracker.trackCall();
      }

      const result = await tracker.checkQuota();

      assert.equal(result.allowed, false);
      assert.equal(result.status, QuotaStatus.EXCEEDED);
      assert.equal(result.used, 50);
      assert.equal(result.remaining, 0);
      assert.ok(result.error);
    });

    it("should not show warning twice in same period", async () => {
      const tracker = getUsageTracker(testConfigDir, () => "free");

      // Track 40 calls to trigger warning
      for (let i = 0; i < 40; i++) {
        await tracker.trackCall();
      }

      const result1 = await tracker.checkQuota();
      assert.equal(result1.status, QuotaStatus.WARNING);
      assert.ok(result1.warning);

      // Second check should not show warning
      const result2 = await tracker.checkQuota();
      assert.equal(result2.status, QuotaStatus.OK); // Warning already shown
      assert.equal(result2.warning, undefined);
    });
  });

  describe("checkQuota - Enterprise Tier", () => {
    it("should allow unlimited calls", async () => {
      const tracker = getUsageTracker(testConfigDir, () => "enterprise");

      // Track many calls
      for (let i = 0; i < 1000; i++) {
        await tracker.trackCall();
      }

      const result = await tracker.checkQuota();

      assert.equal(result.allowed, true);
      assert.equal(result.status, QuotaStatus.OK);
      assert.equal(result.used, 1000);
      assert.equal(result.limit, Infinity);
      assert.equal(result.remaining, Infinity);
    });
  });

  describe("trackCall", () => {
    it("should increment call count", async () => {
      const tracker = getUsageTracker(testConfigDir, () => "free");

      await tracker.trackCall();
      const stats1 = await tracker.getStats();
      assert.equal(stats1.calls, 1);

      await tracker.trackCall();
      const stats2 = await tracker.getStats();
      assert.equal(stats2.calls, 2);
    });

    it("should persist across instances", async () => {
      const tracker1 = getUsageTracker(testConfigDir, () => "free");
      await tracker1.trackCall();

      resetUsageTracker();

      const tracker2 = getUsageTracker(testConfigDir, () => "free");
      const stats = await tracker2.getStats();

      assert.equal(stats.calls, 1);
    });

    it("should update lastCallAt timestamp", async () => {
      const tracker = getUsageTracker(testConfigDir, () => "free");
      const before = new Date().toISOString();

      await tracker.trackCall();

      const usageFile = path.join(testConfigDir, "usage.json");
      const data = JSON.parse(fs.readFileSync(usageFile, "utf8"));

      assert.ok(data.currentPeriod.lastCallAt);
      assert.ok(data.currentPeriod.lastCallAt >= before);
    });
  });

  describe("getStats", () => {
    it("should return correct statistics", async () => {
      const tracker = getUsageTracker(testConfigDir, () => "pro");

      await tracker.trackCall();
      await tracker.trackCall();

      const stats = await tracker.getStats();

      assert.equal(stats.tier, "pro");
      assert.equal(stats.calls, 2);
      assert.equal(stats.limit, 500);
      assert.equal(stats.remaining, 498);
      assert.equal(stats.percentage, 0); // Less than 1%
      assert.ok(stats.period);
      assert.ok(stats.resetsAt);
    });

    it("should calculate percentage correctly", async () => {
      const tracker = getUsageTracker(testConfigDir, () => "free");

      // Track 25 calls (50% of 50)
      for (let i = 0; i < 25; i++) {
        await tracker.trackCall();
      }

      const stats = await tracker.getStats();
      assert.equal(stats.percentage, 50);
    });
  });

  describe("getUsageMessage", () => {
    it("should return formatted usage message", async () => {
      const tracker = getUsageTracker(testConfigDir, () => "free");
      const message = await tracker.getUsageMessage();

      assert.ok(message.includes("Usage"));
      assert.ok(typeof message === "string");
      assert.ok(message.length > 0);
    });
  });

  describe("Data Integrity", () => {
    it("should create backup file on save", async () => {
      const tracker = getUsageTracker(testConfigDir, () => "free");
      await tracker.trackCall();
      await tracker.trackCall();

      const backupFile = path.join(testConfigDir, "usage.json.backup");
      assert.ok(fs.existsSync(backupFile));
    });

    it("should include checksum in saved data", async () => {
      const tracker = getUsageTracker(testConfigDir, () => "free");
      await tracker.trackCall();

      const usageFile = path.join(testConfigDir, "usage.json");
      const data = JSON.parse(fs.readFileSync(usageFile, "utf8"));

      assert.ok(data._checksum);
      assert.equal(typeof data._checksum, "string");
      assert.ok(data._checksum.length > 0);
    });

    it("should include schema version", async () => {
      const tracker = getUsageTracker(testConfigDir, () => "free");
      await tracker.trackCall();

      const usageFile = path.join(testConfigDir, "usage.json");
      const data = JSON.parse(fs.readFileSync(usageFile, "utf8"));

      assert.ok(data.version);
      assert.equal(typeof data.version, "string");
    });
  });

  describe("Monthly Reset", () => {
    it("should detect current month correctly", async () => {
      const tracker = getUsageTracker(testConfigDir, () => "free");
      const stats = await tracker.getStats();

      const expectedMonth = new Date().toISOString().substring(0, 7);
      assert.equal(stats.period, expectedMonth);
    });

    it("should reset calls in new month", async () => {
      const tracker = getUsageTracker(testConfigDir, () => "free");
      await tracker.trackCall();

      // Manually modify usage file to simulate past month
      const usageFile = path.join(testConfigDir, "usage.json");
      const data = JSON.parse(fs.readFileSync(usageFile, "utf8"));
      data.currentPeriod.month = "2025-01"; // Past month
      data.currentPeriod.calls = 25;
      fs.writeFileSync(usageFile, JSON.stringify(data));

      resetUsageTracker();

      const newTracker = getUsageTracker(testConfigDir, () => "free");
      const stats = await newTracker.getStats();

      // Should have reset to 0
      assert.equal(stats.calls, 0);
    });
  });

  describe("Tier Changes", () => {
    it("should respect tier changes", async () => {
      let currentTier: Tier = "free";
      const tierGetter = () => currentTier;

      const tracker = getUsageTracker(testConfigDir, tierGetter);

      // Start with free tier
      const stats1 = await tracker.getStats();
      assert.equal(stats1.tier, "free");
      assert.equal(stats1.limit, 50);

      // Change to pro tier
      currentTier = "pro";
      resetUsageTracker();

      const tracker2 = getUsageTracker(testConfigDir, tierGetter);
      const stats2 = await tracker2.getStats();
      assert.equal(stats2.tier, "pro");
      assert.equal(stats2.limit, 500);
    });
  });
});
