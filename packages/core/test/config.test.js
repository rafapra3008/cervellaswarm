/**
 * Config Module Tests
 */

import { describe, it, beforeEach, afterEach } from 'node:test';
import assert from 'node:assert';
import {
  getApiKey,
  hasApiKey,
  getApiKeySource,
  getDefaultModel,
  setDefaultModel,
  getTimeout,
  setTimeout,
  getMaxRetries,
  setMaxRetries,
  isVerbose,
  setVerbose,
  getAllConfig,
  resetConfig,
  resetGlobalConfig,
  VALID_MODELS,
  CONFIG_CONSTRAINTS
} from '../dist/config/index.js';

describe('Config Module', () => {
  beforeEach(() => {
    // Reset config before each test
    resetGlobalConfig();
    resetConfig();
  });

  afterEach(() => {
    resetGlobalConfig();
  });

  describe('Types & Constants', () => {
    it('should export valid models', () => {
      assert.ok(Array.isArray(VALID_MODELS));
      assert.ok(VALID_MODELS.includes('claude-sonnet-4-20250514'));
      assert.ok(VALID_MODELS.includes('claude-opus-4-5-20251101'));
    });

    it('should export config constraints', () => {
      assert.ok(CONFIG_CONSTRAINTS.timeout.min === 10000);
      assert.ok(CONFIG_CONSTRAINTS.timeout.max === 600000);
      assert.ok(CONFIG_CONSTRAINTS.maxRetries.min === 1);
      assert.ok(CONFIG_CONSTRAINTS.maxRetries.max === 10);
    });
  });

  describe('API Key', () => {
    it('should return null when no API key is set', () => {
      // Clear env var for this test
      const originalEnv = process.env.ANTHROPIC_API_KEY;
      delete process.env.ANTHROPIC_API_KEY;

      assert.strictEqual(getApiKey(), null);
      assert.strictEqual(hasApiKey(), false);
      assert.strictEqual(getApiKeySource(), 'none');

      // Restore
      if (originalEnv) process.env.ANTHROPIC_API_KEY = originalEnv;
    });

    it('should prioritize environment variable', () => {
      process.env.ANTHROPIC_API_KEY = 'sk-ant-test123';
      assert.strictEqual(getApiKey(), 'sk-ant-test123');
      assert.strictEqual(getApiKeySource(), 'environment');
      delete process.env.ANTHROPIC_API_KEY;
    });
  });

  describe('Default Model', () => {
    it('should have correct default', () => {
      assert.strictEqual(getDefaultModel(), 'claude-sonnet-4-20250514');
    });

    it('should allow setting valid model', () => {
      setDefaultModel('claude-opus-4-5-20251101');
      assert.strictEqual(getDefaultModel(), 'claude-opus-4-5-20251101');
    });

    it('should reject invalid model', () => {
      assert.throws(() => setDefaultModel('invalid-model'), /Invalid model/);
    });
  });

  describe('Timeout', () => {
    it('should have correct default', () => {
      assert.strictEqual(getTimeout(), 120000);
    });

    it('should allow setting valid timeout', () => {
      setTimeout(60000);
      assert.strictEqual(getTimeout(), 60000);
    });

    it('should reject out of range timeout', () => {
      assert.throws(() => setTimeout(5000), /Timeout must be between/);
      assert.throws(() => setTimeout(700000), /Timeout must be between/);
    });
  });

  describe('Max Retries', () => {
    it('should have correct default', () => {
      assert.strictEqual(getMaxRetries(), 3);
    });

    it('should allow setting valid retries', () => {
      setMaxRetries(5);
      assert.strictEqual(getMaxRetries(), 5);
    });

    it('should reject out of range retries', () => {
      assert.throws(() => setMaxRetries(0), /Max retries must be between/);
      assert.throws(() => setMaxRetries(15), /Max retries must be between/);
    });
  });

  describe('Verbose', () => {
    it('should default to false', () => {
      assert.strictEqual(isVerbose(), false);
    });

    it('should allow toggling', () => {
      setVerbose(true);
      assert.strictEqual(isVerbose(), true);
      setVerbose(false);
      assert.strictEqual(isVerbose(), false);
    });
  });

  describe('getAllConfig', () => {
    it('should return config summary', () => {
      const config = getAllConfig();
      assert.ok(config.hasOwnProperty('apiKey'));
      assert.ok(config.hasOwnProperty('apiKeySource'));
      assert.ok(config.hasOwnProperty('defaultModel'));
      assert.ok(config.hasOwnProperty('timeout'));
      assert.ok(config.hasOwnProperty('maxRetries'));
      assert.ok(config.hasOwnProperty('verbose'));
      assert.ok(config.hasOwnProperty('telemetry'));
    });

    it('should mask API key', () => {
      const config = getAllConfig();
      assert.ok(!config.apiKey.includes('sk-ant'));
    });
  });
});
