/**
 * Tests for billing/tiers.ts
 *
 * Tests tier configuration, limits, and utility functions.
 */

import { describe, it } from "node:test";
import assert from "node:assert/strict";
import {
  TIER_LIMITS,
  TIER_PRICES,
  TIER_NAMES,
  TIER_UPGRADE_PATH,
  WARNING_THRESHOLD,
  getLimitForTier,
  getUpgradeTier,
  isUnlimited,
  getUpgradeUrl,
} from "../dist/billing/tiers.js";

describe("Tier Configuration", () => {
  describe("TIER_LIMITS", () => {
    it("should define correct limits for each tier", () => {
      assert.equal(TIER_LIMITS.free, 50);
      assert.equal(TIER_LIMITS.pro, 500);
      assert.equal(TIER_LIMITS.team, 1000);
      assert.equal(TIER_LIMITS.enterprise, Infinity);
    });
  });

  describe("TIER_PRICES", () => {
    it("should define correct prices for each tier", () => {
      assert.equal(TIER_PRICES.free, 0);
      assert.equal(TIER_PRICES.pro, 20);
      assert.equal(TIER_PRICES.team, 35);
      assert.equal(TIER_PRICES.enterprise, -1);
    });
  });

  describe("TIER_NAMES", () => {
    it("should define display names for each tier", () => {
      assert.equal(TIER_NAMES.free, "Free");
      assert.equal(TIER_NAMES.pro, "Pro");
      assert.equal(TIER_NAMES.team, "Team");
      assert.equal(TIER_NAMES.enterprise, "Enterprise");
    });
  });

  describe("TIER_UPGRADE_PATH", () => {
    it("should define correct upgrade path", () => {
      assert.equal(TIER_UPGRADE_PATH.free, "pro");
      assert.equal(TIER_UPGRADE_PATH.pro, "team");
      assert.equal(TIER_UPGRADE_PATH.team, "enterprise");
      assert.equal(TIER_UPGRADE_PATH.enterprise, null);
    });
  });

  describe("WARNING_THRESHOLD", () => {
    it("should be set to 80%", () => {
      assert.equal(WARNING_THRESHOLD, 0.8);
    });
  });
});

describe("Tier Utility Functions", () => {
  describe("getLimitForTier", () => {
    it("should return correct limit for free tier", () => {
      assert.equal(getLimitForTier("free"), 50);
    });

    it("should return correct limit for pro tier", () => {
      assert.equal(getLimitForTier("pro"), 500);
    });

    it("should return correct limit for team tier", () => {
      assert.equal(getLimitForTier("team"), 1000);
    });

    it("should return Infinity for enterprise tier", () => {
      assert.equal(getLimitForTier("enterprise"), Infinity);
    });

    it("should return free tier limit for invalid tier", () => {
      // @ts-expect-error Testing invalid tier
      assert.equal(getLimitForTier("invalid"), 50);
    });
  });

  describe("getUpgradeTier", () => {
    it("should return pro for free tier", () => {
      assert.equal(getUpgradeTier("free"), "pro");
    });

    it("should return team for pro tier", () => {
      assert.equal(getUpgradeTier("pro"), "team");
    });

    it("should return enterprise for team tier", () => {
      assert.equal(getUpgradeTier("team"), "enterprise");
    });

    it("should return null for enterprise tier (no upgrade)", () => {
      assert.equal(getUpgradeTier("enterprise"), null);
    });
  });

  describe("isUnlimited", () => {
    it("should return false for free tier", () => {
      assert.equal(isUnlimited("free"), false);
    });

    it("should return false for pro tier", () => {
      assert.equal(isUnlimited("pro"), false);
    });

    it("should return false for team tier", () => {
      assert.equal(isUnlimited("team"), false);
    });

    it("should return true for enterprise tier", () => {
      assert.equal(isUnlimited("enterprise"), true);
    });
  });

  describe("getUpgradeUrl", () => {
    it("should return upgrade URL for free tier", () => {
      const url = getUpgradeUrl("free");
      assert.ok(url.includes("cervellaswarm.com/upgrade"));
      assert.ok(url.includes("from=free"));
      assert.ok(url.includes("to=pro"));
    });

    it("should return upgrade URL for pro tier", () => {
      const url = getUpgradeUrl("pro");
      assert.ok(url.includes("cervellaswarm.com/upgrade"));
      assert.ok(url.includes("from=pro"));
      assert.ok(url.includes("to=team"));
    });

    it("should return contact URL for enterprise tier (no upgrade)", () => {
      const url = getUpgradeUrl("enterprise");
      assert.ok(url.includes("cervellaswarm.com/contact"));
    });
  });
});
