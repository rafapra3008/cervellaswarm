/**
 * Tests for API Key Management
 *
 * Covers: setApiKey, getApiKey, hasApiKey, clearApiKey, getApiKeySource
 * Priority logic: env > config
 */

import { describe, it, beforeEach, afterEach } from 'node:test';
import assert from 'node:assert/strict';
import {
  resetGlobalConfig,
  getGlobalConfig,
  getApiKey,
  setApiKey,
  hasApiKey,
  clearApiKey,
  getApiKeySource
} from '../../src/config/index.js';

describe('API Key Management', () => {
  let savedEnvKey;

  beforeEach(() => {
    // Save and clear env to isolate tests
    savedEnvKey = process.env.ANTHROPIC_API_KEY;
    delete process.env.ANTHROPIC_API_KEY;
    // Reset config singleton and clear persisted values
    resetGlobalConfig();
    getGlobalConfig().clear();
  });

  afterEach(() => {
    // Restore env
    if (savedEnvKey !== undefined) {
      process.env.ANTHROPIC_API_KEY = savedEnvKey;
    } else {
      delete process.env.ANTHROPIC_API_KEY;
    }
    // Clean up config
    resetGlobalConfig();
  });

  describe('setApiKey', () => {
    it('accepts valid sk-ant- key', () => {
      const result = setApiKey('sk-ant-abc123');
      assert.equal(result, true);
    });

    it('persists key to config', () => {
      setApiKey('sk-ant-test-key-123');
      const config = getGlobalConfig();
      assert.equal(config.get('apiKey'), 'sk-ant-test-key-123');
    });

    it('throws on empty string', () => {
      assert.throws(() => setApiKey(''), {
        message: /non-empty string/
      });
    });

    it('throws on null', () => {
      assert.throws(() => setApiKey(null), {
        message: /non-empty string/
      });
    });

    it('throws on undefined', () => {
      assert.throws(() => setApiKey(undefined), {
        message: /non-empty string/
      });
    });

    it('throws on non-string (number)', () => {
      assert.throws(() => setApiKey(12345), {
        message: /non-empty string/
      });
    });

    it('throws on invalid prefix', () => {
      assert.throws(() => setApiKey('invalid-key-format'), {
        message: /sk-ant-/
      });
    });

    it('throws on key starting with sk- but not sk-ant-', () => {
      assert.throws(() => setApiKey('sk-other-prefix'), {
        message: /sk-ant-/
      });
    });
  });

  describe('getApiKey', () => {
    it('returns null when no key set anywhere', () => {
      assert.equal(getApiKey(), null);
    });

    it('returns config key when set', () => {
      setApiKey('sk-ant-from-config');
      assert.equal(getApiKey(), 'sk-ant-from-config');
    });

    it('returns env key when set', () => {
      process.env.ANTHROPIC_API_KEY = 'sk-ant-from-env';
      assert.equal(getApiKey(), 'sk-ant-from-env');
    });

    it('env key takes priority over config key', () => {
      setApiKey('sk-ant-from-config');
      process.env.ANTHROPIC_API_KEY = 'sk-ant-from-env';
      assert.equal(getApiKey(), 'sk-ant-from-env');
    });
  });

  describe('hasApiKey', () => {
    it('returns false when no key set', () => {
      assert.equal(hasApiKey(), false);
    });

    it('returns true when config key set', () => {
      setApiKey('sk-ant-test');
      assert.equal(hasApiKey(), true);
    });

    it('returns true when env key set', () => {
      process.env.ANTHROPIC_API_KEY = 'sk-ant-env-test';
      assert.equal(hasApiKey(), true);
    });
  });

  describe('clearApiKey', () => {
    it('clears saved config key', () => {
      setApiKey('sk-ant-to-clear');
      assert.equal(hasApiKey(), true);

      clearApiKey();
      // Without env, should now be null
      assert.equal(getApiKey(), null);
    });

    it('returns true', () => {
      assert.equal(clearApiKey(), true);
    });

    it('does not affect env key', () => {
      process.env.ANTHROPIC_API_KEY = 'sk-ant-env-stays';
      setApiKey('sk-ant-config-goes');

      clearApiKey();
      // Env key should still work
      assert.equal(getApiKey(), 'sk-ant-env-stays');
    });
  });

  describe('getApiKeySource', () => {
    it('returns none when no key set', () => {
      assert.equal(getApiKeySource(), 'none');
    });

    it('returns config when only config key set', () => {
      setApiKey('sk-ant-config-only');
      assert.equal(getApiKeySource(), 'config');
    });

    it('returns environment when env key set', () => {
      process.env.ANTHROPIC_API_KEY = 'sk-ant-env-only';
      assert.equal(getApiKeySource(), 'environment');
    });

    it('returns environment when both set (env wins)', () => {
      setApiKey('sk-ant-config');
      process.env.ANTHROPIC_API_KEY = 'sk-ant-env';
      assert.equal(getApiKeySource(), 'environment');
    });
  });
});
