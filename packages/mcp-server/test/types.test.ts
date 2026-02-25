/**
 * Tests for billing/types.ts
 *
 * Tests type definitions and enums.
 */

import { describe, it } from "node:test";
import assert from "node:assert/strict";
import { QuotaStatus } from "../dist/billing/types.js";

describe("Billing Types", () => {
  describe("QuotaStatus Enum", () => {
    it("should have OK status", () => {
      assert.equal(QuotaStatus.OK, "ok");
    });

    it("should have WARNING status", () => {
      assert.equal(QuotaStatus.WARNING, "warning");
    });

    it("should have EXCEEDED status", () => {
      assert.equal(QuotaStatus.EXCEEDED, "exceeded");
    });

    it("should have exactly 3 status values", () => {
      const statuses = Object.values(QuotaStatus);
      assert.equal(statuses.length, 3);
    });

    it("should use lowercase string values", () => {
      Object.values(QuotaStatus).forEach((status) => {
        assert.equal(typeof status, "string");
        assert.equal(status, status.toLowerCase());
      });
    });
  });
});
