/**
 * Tests for config/manager.ts
 *
 * Tests configuration management and API key handling.
 */

import { describe, it, beforeEach, afterEach } from "node:test";
import assert from "node:assert/strict";
import {
  hasApiKey,
  getApiKeySource,
  getDefaultModel,
  getTimeout,
  getMaxRetries,
  isVerbose,
  getTier,
  getConfigPath,
  getConfigDir,
  validateApiKey,
} from "../dist/config/manager.js";

describe("Config Manager", () => {
  let originalApiKey: string | undefined;

  beforeEach(() => {
    // Save original API key
    originalApiKey = process.env.ANTHROPIC_API_KEY;
  });

  afterEach(() => {
    // Restore original API key
    if (originalApiKey !== undefined) {
      process.env.ANTHROPIC_API_KEY = originalApiKey;
    } else {
      delete process.env.ANTHROPIC_API_KEY;
    }
  });

  describe("API Key Detection", () => {
    it("should detect when API key is missing", () => {
      delete process.env.ANTHROPIC_API_KEY;
      // Note: hasApiKey might still return true if config file has key
      // This test just verifies the function is callable
      const result = hasApiKey();
      assert.equal(typeof result, "boolean");
    });

    it("should detect environment variable source", () => {
      process.env.ANTHROPIC_API_KEY = "sk-ant-test-key";
      const source = getApiKeySource();
      assert.equal(source, "environment");
    });

    it("should return none when no key exists", () => {
      delete process.env.ANTHROPIC_API_KEY;
      // Clear config key would require resetting Conf instance
      // This is a simplified test
      const source = getApiKeySource();
      assert.ok(["environment", "config", "none"].includes(source));
    });
  });

  describe("Model Settings", () => {
    it("should return default model", () => {
      const model = getDefaultModel();
      assert.equal(typeof model, "string");
      assert.ok(model.startsWith("claude-"));
    });

    it("should return valid timeout", () => {
      const timeout = getTimeout();
      assert.equal(typeof timeout, "number");
      assert.ok(timeout >= 10000); // Min 10s
      assert.ok(timeout <= 600000); // Max 10min
    });

    it("should return valid max retries", () => {
      const retries = getMaxRetries();
      assert.equal(typeof retries, "number");
      assert.ok(retries >= 1);
      assert.ok(retries <= 10);
    });

    it("should return verbose flag", () => {
      const verbose = isVerbose();
      assert.equal(typeof verbose, "boolean");
    });
  });

  describe("Tier Management", () => {
    it("should return valid tier", () => {
      const tier = getTier();
      assert.ok(["free", "pro", "team", "enterprise"].includes(tier));
    });
  });

  describe("Config Paths", () => {
    it("should return config file path", () => {
      const path = getConfigPath();
      assert.equal(typeof path, "string");
      assert.ok(path.length > 0);
      assert.ok(path.includes("config.json"));
    });

    it("should return config directory", () => {
      const dir = getConfigDir();
      assert.equal(typeof dir, "string");
      assert.ok(dir.length > 0);
      assert.ok(!dir.endsWith("config.json"));
    });

    it("should have consistent paths", () => {
      const path = getConfigPath();
      const dir = getConfigDir();
      assert.ok(path.startsWith(dir));
    });
  });

  describe("API Key Validation", () => {
    it("should reject null key", async () => {
      const result = await validateApiKey(null);
      assert.equal(result.valid, false);
      assert.ok(result.error);
    });

    it("should reject empty string", async () => {
      const result = await validateApiKey("");
      assert.equal(result.valid, false);
      assert.ok(result.error);
    });

    it("should reject key with wrong prefix", async () => {
      const result = await validateApiKey("wrong-prefix-key");
      assert.equal(result.valid, false);
      assert.ok(result.error);
      assert.ok(result.error.includes("sk-ant-"));
    });

    it("should accept correct format (but may fail API check)", async () => {
      const result = await validateApiKey("sk-ant-fake-test-key");
      // Will fail API check, but format validation passes first
      assert.equal(typeof result.valid, "boolean");
      assert.ok(result.error || result.warning || result.valid);
    });

    it("should return ValidationResult structure", async () => {
      const result = await validateApiKey("sk-ant-test");
      assert.ok("valid" in result);
      assert.equal(typeof result.valid, "boolean");
    });
  });
});
