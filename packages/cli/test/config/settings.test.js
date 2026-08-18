/**
 * Tests for Settings Management
 *
 * Covers: model, timeout, retries, verbose, telemetry, getAllConfig, resetConfig, getConfigPath
 * Validates boundaries and type coercion.
 */

import { describe, it, beforeEach, afterEach } from 'node:test';
import assert from 'node:assert/strict';
import {
  resetGlobalConfig,
  getGlobalConfig,
  getDefaultModel,
  setDefaultModel,
  getTimeout,
  setTimeout as setTimeoutConfig,
  getMaxRetries,
  setMaxRetries,
  isVerbose,
  setVerbose,
  isTelemetryEnabled,
  setTelemetry,
  getAllConfig,
  resetConfig,
  getConfigPath,
  setApiKey
} from '../../src/config/index.js';

describe('Settings Management', () => {
  let savedEnvKey;

  beforeEach(() => {
    savedEnvKey = process.env.ANTHROPIC_API_KEY;
    delete process.env.ANTHROPIC_API_KEY;
    resetGlobalConfig();
    getGlobalConfig().clear();
  });

  afterEach(() => {
    if (savedEnvKey !== undefined) {
      process.env.ANTHROPIC_API_KEY = savedEnvKey;
    } else {
      delete process.env.ANTHROPIC_API_KEY;
    }
    resetGlobalConfig();
  });

  describe('setDefaultModel / getDefaultModel', () => {
    it('returns default model initially', () => {
      assert.equal(getDefaultModel(), 'claude-sonnet-4-6');
    });

    it('accepts claude-opus-4-6', () => {
      const result = setDefaultModel('claude-opus-4-6');
      assert.equal(result, true);
      assert.equal(getDefaultModel(), 'claude-opus-4-6');
    });

    it('accepts claude-sonnet-4-20250514', () => {
      setDefaultModel('claude-sonnet-4-20250514');
      assert.equal(getDefaultModel(), 'claude-sonnet-4-20250514');
    });

    it('accepts claude-opus-4-5-20251101', () => {
      setDefaultModel('claude-opus-4-5-20251101');
      assert.equal(getDefaultModel(), 'claude-opus-4-5-20251101');
    });

    it('throws on invalid model name', () => {
      assert.throws(() => setDefaultModel('gpt-4'), {
        message: /Invalid model/
      });
    });

    it('throws on empty string', () => {
      assert.throws(() => setDefaultModel(''), {
        message: /Invalid model/
      });
    });
  });

  describe('setTimeout / getTimeout', () => {
    it('returns default timeout initially', () => {
      assert.equal(getTimeout(), 120000);
    });

    it('accepts minimum boundary (10000)', () => {
      const result = setTimeoutConfig(10000);
      assert.equal(result, true);
      assert.equal(getTimeout(), 10000);
    });

    it('accepts maximum boundary (600000)', () => {
      setTimeoutConfig(600000);
      assert.equal(getTimeout(), 600000);
    });

    it('accepts value in middle of range', () => {
      setTimeoutConfig(300000);
      assert.equal(getTimeout(), 300000);
    });

    it('throws below minimum (9999)', () => {
      assert.throws(() => setTimeoutConfig(9999), {
        message: /between 10000ms/
      });
    });

    it('throws above maximum (600001)', () => {
      assert.throws(() => setTimeoutConfig(600001), {
        message: /between 10000ms/
      });
    });

    it('throws on zero', () => {
      assert.throws(() => setTimeoutConfig(0), {
        message: /between 10000ms/
      });
    });

    it('throws on negative value', () => {
      assert.throws(() => setTimeoutConfig(-1), {
        message: /between 10000ms/
      });
    });
  });

  describe('setMaxRetries / getMaxRetries', () => {
    it('returns default retries initially', () => {
      assert.equal(getMaxRetries(), 3);
    });

    it('accepts minimum boundary (1)', () => {
      const result = setMaxRetries(1);
      assert.equal(result, true);
      assert.equal(getMaxRetries(), 1);
    });

    it('accepts maximum boundary (10)', () => {
      setMaxRetries(10);
      assert.equal(getMaxRetries(), 10);
    });

    it('throws below minimum (0)', () => {
      assert.throws(() => setMaxRetries(0), {
        message: /between 1 and 10/
      });
    });

    it('throws above maximum (11)', () => {
      assert.throws(() => setMaxRetries(11), {
        message: /between 1 and 10/
      });
    });

    it('throws on negative value', () => {
      assert.throws(() => setMaxRetries(-1), {
        message: /between 1 and 10/
      });
    });
  });

  describe('setVerbose / isVerbose', () => {
    it('defaults to false', () => {
      assert.equal(isVerbose(), false);
    });

    it('sets to true', () => {
      const result = setVerbose(true);
      assert.equal(result, true);
      assert.equal(isVerbose(), true);
    });

    it('sets to false explicitly', () => {
      setVerbose(true);
      setVerbose(false);
      assert.equal(isVerbose(), false);
    });

    it('coerces truthy value to boolean', () => {
      setVerbose(1);
      assert.equal(isVerbose(), true);
    });

    it('coerces falsy value to boolean', () => {
      setVerbose(true);
      setVerbose(0);
      assert.equal(isVerbose(), false);
    });
  });

  describe('setTelemetry / isTelemetryEnabled', () => {
    it('defaults to false', () => {
      assert.equal(isTelemetryEnabled(), false);
    });

    it('sets to true', () => {
      const result = setTelemetry(true);
      assert.equal(result, true);
      assert.equal(isTelemetryEnabled(), true);
    });

    it('coerces truthy to boolean', () => {
      setTelemetry('yes');
      assert.equal(isTelemetryEnabled(), true);
    });
  });

  describe('getAllConfig', () => {
    it('returns object with all keys', () => {
      const config = getAllConfig();
      assert.ok('apiKey' in config);
      assert.ok('apiKeySource' in config);
      assert.ok('defaultModel' in config);
      assert.ok('timeout' in config);
      assert.ok('maxRetries' in config);
      assert.ok('verbose' in config);
      assert.ok('telemetry' in config);
    });

    it('masks apiKey when set', () => {
      setApiKey('sk-ant-secret-key');
      const config = getAllConfig();
      assert.equal(config.apiKey, '***configured***');
    });

    it('shows not set when apiKey empty', () => {
      const config = getAllConfig();
      assert.equal(config.apiKey, 'not set');
    });

    it('reflects current settings', () => {
      setDefaultModel('claude-opus-4-6');
      setTimeoutConfig(30000);
      setMaxRetries(5);
      setVerbose(true);

      const config = getAllConfig();
      assert.equal(config.defaultModel, 'claude-opus-4-6');
      assert.equal(config.timeout, 30000);
      assert.equal(config.maxRetries, 5);
      assert.equal(config.verbose, true);
    });
  });

  describe('resetConfig', () => {
    it('resets all settings to defaults', () => {
      setDefaultModel('claude-opus-4-6');
      setTimeoutConfig(60000);
      setMaxRetries(7);
      setVerbose(true);
      setTelemetry(true);

      const result = resetConfig();
      assert.equal(result, true);

      assert.equal(getDefaultModel(), 'claude-sonnet-4-6');
      assert.equal(getTimeout(), 120000);
      assert.equal(getMaxRetries(), 3);
      assert.equal(isVerbose(), false);
      assert.equal(isTelemetryEnabled(), false);
    });
  });

  describe('getConfigPath', () => {
    it('returns a string path', () => {
      const path = getConfigPath();
      assert.equal(typeof path, 'string');
      assert.ok(path.length > 0);
    });

    it('path contains cervellaswarm', () => {
      const path = getConfigPath();
      assert.ok(path.includes('cervellaswarm'), `Expected path to contain cervellaswarm: ${path}`);
    });
  });
});
