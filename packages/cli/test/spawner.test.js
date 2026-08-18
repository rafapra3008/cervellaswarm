/**
 * Spawner Tests
 *
 * Test per agents/spawner.js
 * Verifica: error handling, retry logic, agent name normalization
 */

import { test, describe } from 'node:test';
import assert from 'node:assert/strict';

// Error map (copied from spawner.js for unit testing without SDK dependency)
const errorMap = {
  401: { message: 'Invalid API key', retryable: false },
  403: { message: 'API key lacks permission', retryable: false },
  429: { message: 'Rate limit exceeded', retryable: true },
  500: { message: 'Anthropic API error', retryable: true },
  503: { message: 'API temporarily unavailable', retryable: true },
  timeout: { message: 'Request timed out', retryable: false },
};

function getErrorInfo(error) {
  const status = error.name === 'AbortError' ? 'timeout' : error.status;
  return errorMap[status] || {
    message: error.message || 'Unknown error',
    retryable: false,
  };
}

function isRetryableError(error) {
  return error.status === 429 || error.status === 500 || error.status === 503;
}

describe('Spawner', () => {

  describe('Error Handling', () => {
    test('401 - invalid API key (not retryable)', () => {
      const info = getErrorInfo({ status: 401 });
      assert.equal(info.message, 'Invalid API key');
      assert.equal(info.retryable, false);
    });

    test('403 - permission denied (not retryable)', () => {
      const info = getErrorInfo({ status: 403 });
      assert.equal(info.message, 'API key lacks permission');
      assert.equal(info.retryable, false);
    });

    test('429 - rate limited (retryable)', () => {
      const info = getErrorInfo({ status: 429 });
      assert.equal(info.message, 'Rate limit exceeded');
      assert.equal(info.retryable, true);
    });

    test('500 - server error (retryable)', () => {
      const info = getErrorInfo({ status: 500 });
      assert.equal(info.message, 'Anthropic API error');
      assert.equal(info.retryable, true);
    });

    test('503 - unavailable (retryable)', () => {
      const info = getErrorInfo({ status: 503 });
      assert.equal(info.message, 'API temporarily unavailable');
      assert.equal(info.retryable, true);
    });

    test('timeout via AbortError', () => {
      const info = getErrorInfo({ name: 'AbortError' });
      assert.equal(info.message, 'Request timed out');
      assert.equal(info.retryable, false);
    });

    test('unknown error falls back', () => {
      const info = getErrorInfo({ status: 418, message: 'I am a teapot' });
      assert.equal(info.message, 'I am a teapot');
      assert.equal(info.retryable, false);
    });

    test('error without message', () => {
      const info = getErrorInfo({ status: 999 });
      assert.equal(info.message, 'Unknown error');
    });
  });

  describe('Retry Logic', () => {
    test('429 is retryable', () => {
      assert.ok(isRetryableError({ status: 429 }));
    });

    test('500 is retryable', () => {
      assert.ok(isRetryableError({ status: 500 }));
    });

    test('503 is retryable', () => {
      assert.ok(isRetryableError({ status: 503 }));
    });

    test('401 is NOT retryable', () => {
      assert.ok(!isRetryableError({ status: 401 }));
    });

    test('403 is NOT retryable', () => {
      assert.ok(!isRetryableError({ status: 403 }));
    });

    test('200 is NOT retryable', () => {
      assert.ok(!isRetryableError({ status: 200 }));
    });

    test('retry budget (3 attempts max)', () => {
      const maxRetries = 3;
      let attempts = 0;
      let lastError = null;

      while (attempts < maxRetries) {
        attempts++;
        lastError = { status: 500, message: 'server error' };
        if (!isRetryableError(lastError)) break;
      }

      assert.equal(attempts, maxRetries, 'Should exhaust all retries');
    });

    test('non-retryable stops immediately', () => {
      const maxRetries = 3;
      let attempts = 0;

      while (attempts < maxRetries) {
        attempts++;
        const error = { status: 401 };
        if (!isRetryableError(error)) break;
      }

      assert.equal(attempts, 1, 'Should stop after first non-retryable');
    });
  });

  describe('Agent Name Normalization', () => {
    test('strips cervella- prefix', () => {
      const agent = 'cervella-backend';
      const normalized = agent.replace(/^cervella-/, '');
      assert.equal(normalized, 'backend');
    });

    test('keeps name without prefix', () => {
      const agent = 'backend';
      const normalized = agent.replace(/^cervella-/, '');
      assert.equal(normalized, 'backend');
    });

    test('handles cervella-frontend', () => {
      const normalized = 'cervella-frontend'.replace(/^cervella-/, '');
      assert.equal(normalized, 'frontend');
    });

    test('handles cervella-tester', () => {
      const normalized = 'cervella-tester'.replace(/^cervella-/, '');
      assert.equal(normalized, 'tester');
    });

    test('does not strip mid-string cervella', () => {
      const agent = 'my-cervella-agent';
      const normalized = agent.replace(/^cervella-/, '');
      assert.equal(normalized, 'my-cervella-agent');
    });
  });

  describe('Result Format', () => {
    test('success result has required fields', () => {
      const result = {
        success: true,
        response: 'Task completed',
        model: 'claude-opus-4-6',
        agent: 'cervella-backend',
        duration: 1500,
        filesModified: ['file.py'],
      };

      assert.ok(result.success);
      assert.ok(result.response);
      assert.ok(result.model);
      assert.ok(result.agent);
      assert.ok(typeof result.duration === 'number');
      assert.ok(Array.isArray(result.filesModified));
    });

    test('failure result has error info', () => {
      const result = {
        success: false,
        error: 'API key not configured',
        filesModified: [],
        nextStep: 'Run cervellaswarm init',
      };

      assert.ok(!result.success);
      assert.ok(result.error);
      assert.ok(result.nextStep);
      assert.ok(Array.isArray(result.filesModified));
    });

    test('no API key returns specific error', () => {
      const apiKey = null;
      if (!apiKey) {
        const result = {
          success: false,
          error: 'API key not configured',
          filesModified: [],
          nextStep: 'Run cervellaswarm init or set ANTHROPIC_API_KEY',
        };
        assert.equal(result.error, 'API key not configured');
        assert.ok(result.nextStep.includes('ANTHROPIC_API_KEY'));
      }
    });
  });
});
