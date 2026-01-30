/**
 * Client Module Tests (errors.ts + retry.ts)
 */

import { describe, it } from 'node:test';
import assert from 'node:assert';
import {
  ERROR_MESSAGES,
  parseError,
  formatError,
  CervellaSwarmError
} from '../dist/client/errors.js';
import {
  RETRY_DELAYS,
  DEFAULT_TIMEOUT,
  DEFAULT_MAX_RETRIES,
  sleep,
  isRetryableError,
  withRetry,
  withTimeout,
  withRetryAndTimeout
} from '../dist/client/retry.js';

describe('Client Module - Errors', () => {
  describe('ERROR_MESSAGES', () => {
    it('should have user-friendly messages for common status codes', () => {
      assert.ok(ERROR_MESSAGES[400]);
      assert.ok(ERROR_MESSAGES[401]);
      assert.ok(ERROR_MESSAGES[403]);
      assert.ok(ERROR_MESSAGES[404]);
      assert.ok(ERROR_MESSAGES[429]);
      assert.ok(ERROR_MESSAGES[500]);
      assert.ok(ERROR_MESSAGES[529]);
    });

    it('should have meaningful content', () => {
      assert.ok(ERROR_MESSAGES[401].includes('API key'));
      assert.ok(ERROR_MESSAGES[429].includes('Rate limit'));
      assert.ok(ERROR_MESSAGES[529].includes('overload'));
    });
  });

  describe('parseError', () => {
    it('should handle null/undefined', () => {
      const result1 = parseError(null);
      assert.strictEqual(result1.retryable, false);
      assert.ok(result1.message);

      const result2 = parseError(undefined);
      assert.strictEqual(result2.retryable, false);
    });

    it('should handle Error with status 401', () => {
      const error = new Error('Unauthorized');
      error.status = 401;

      const result = parseError(error);
      assert.strictEqual(result.status, 401);
      assert.strictEqual(result.retryable, false);
      assert.ok(result.suggestion?.includes('config'));
    });

    it('should handle Error with status 429 (retryable)', () => {
      const error = new Error('Rate limited');
      error.status = 429;

      const result = parseError(error);
      assert.strictEqual(result.status, 429);
      assert.strictEqual(result.retryable, true);
      assert.ok(result.suggestion);
    });

    it('should handle Error with status 529 (retryable)', () => {
      const error = new Error('Overloaded');
      error.status = 529;

      const result = parseError(error);
      assert.strictEqual(result.status, 529);
      assert.strictEqual(result.retryable, true);
    });

    it('should handle Error with status 500+ (retryable)', () => {
      const error = new Error('Server error');
      error.status = 500;

      const result = parseError(error);
      assert.strictEqual(result.status, 500);
      assert.strictEqual(result.retryable, true);
    });

    it('should handle plain Error without status', () => {
      const error = new Error('Something went wrong');

      const result = parseError(error);
      assert.strictEqual(result.message, 'Something went wrong');
      assert.strictEqual(result.retryable, false);
      assert.ok(result.original === error);
    });

    it('should handle object with status', () => {
      const error = { status: 403, message: 'Forbidden' };

      const result = parseError(error);
      assert.strictEqual(result.status, 403);
      assert.strictEqual(result.retryable, false);
      assert.ok(result.suggestion);
    });

    it('should handle object with message only', () => {
      const error = { message: 'Custom error' };

      const result = parseError(error);
      assert.strictEqual(result.message, 'Custom error');
      assert.strictEqual(result.retryable, false);
    });

    it('should handle string error', () => {
      const result = parseError('Error string');
      assert.strictEqual(result.message, 'Error string');
      assert.strictEqual(result.retryable, false);
    });

    it('should handle unknown error type', () => {
      const result = parseError(42);
      assert.ok(result.message);
      assert.strictEqual(result.retryable, false);
      assert.strictEqual(result.original, 42);
    });
  });

  describe('formatError', () => {
    it('should format simple error', () => {
      const error = new Error('Test error');
      const formatted = formatError(error);
      assert.ok(formatted.includes('Test error'));
    });

    it('should include suggestion when present', () => {
      const error = new Error('Auth error');
      error.status = 401;
      const formatted = formatError(error);
      assert.ok(formatted.includes('config'));
    });

    it('should indicate when retryable', () => {
      const error = new Error('Rate limit');
      error.status = 429;
      const formatted = formatError(error);
      assert.ok(formatted.includes('retry'));
    });
  });

  describe('CervellaSwarmError', () => {
    it('should create from ErrorInfo', () => {
      const error = new CervellaSwarmError({
        status: 429,
        message: 'Rate limited',
        retryable: true,
        suggestion: 'Wait a moment'
      });

      assert.strictEqual(error.name, 'CervellaSwarmError');
      assert.strictEqual(error.status, 429);
      assert.strictEqual(error.retryable, true);
      assert.strictEqual(error.suggestion, 'Wait a moment');
    });

    it('should create from any error via from()', () => {
      const originalError = new Error('Original');
      originalError.status = 500;

      const swarmError = CervellaSwarmError.from(originalError);
      assert.ok(swarmError instanceof CervellaSwarmError);
      assert.strictEqual(swarmError.status, 500);
      assert.strictEqual(swarmError.retryable, true);
    });

    it('should return same instance if already CervellaSwarmError', () => {
      const error = new CervellaSwarmError({
        message: 'Test',
        retryable: false
      });

      const result = CervellaSwarmError.from(error);
      assert.strictEqual(result, error);
    });
  });
});

describe('Client Module - Retry', () => {
  describe('Constants', () => {
    it('should export retry delays', () => {
      assert.ok(Array.isArray(RETRY_DELAYS));
      assert.strictEqual(RETRY_DELAYS.length, 3);
      assert.strictEqual(RETRY_DELAYS[0], 1000);
      assert.strictEqual(RETRY_DELAYS[1], 3000);
      assert.strictEqual(RETRY_DELAYS[2], 5000);
    });

    it('should export default timeout', () => {
      assert.strictEqual(DEFAULT_TIMEOUT, 600000); // 10 minutes
    });

    it('should export default max retries', () => {
      assert.strictEqual(DEFAULT_MAX_RETRIES, 3);
    });
  });

  describe('sleep', () => {
    it('should sleep for specified milliseconds', async () => {
      const start = Date.now();
      await sleep(100);
      const duration = Date.now() - start;
      assert.ok(duration >= 90); // Allow 10ms tolerance
      assert.ok(duration < 200);
    });
  });

  describe('isRetryableError', () => {
    it('should return false for null/undefined', () => {
      assert.strictEqual(isRetryableError(null), false);
      assert.strictEqual(isRetryableError(undefined), false);
    });

    it('should return false for non-object', () => {
      assert.strictEqual(isRetryableError('string'), false);
      assert.strictEqual(isRetryableError(42), false);
    });

    it('should return true for status 529', () => {
      assert.strictEqual(isRetryableError({ status: 529 }), true);
    });

    it('should return true for status 429', () => {
      assert.strictEqual(isRetryableError({ status: 429 }), true);
    });

    it('should return true for status 500-599', () => {
      assert.strictEqual(isRetryableError({ status: 500 }), true);
      assert.strictEqual(isRetryableError({ status: 503 }), true);
      assert.strictEqual(isRetryableError({ status: 599 }), true);
    });

    it('should return false for status 400-499 (except 429)', () => {
      assert.strictEqual(isRetryableError({ status: 400 }), false);
      assert.strictEqual(isRetryableError({ status: 401 }), false);
      assert.strictEqual(isRetryableError({ status: 404 }), false);
    });

    it('should return true for overloaded_error type', () => {
      assert.strictEqual(isRetryableError({ type: 'overloaded_error' }), true);
    });

    it('should detect overloaded in message', () => {
      assert.strictEqual(
        isRetryableError({ message: 'Service is overloaded' }),
        true
      );
    });

    it('should detect rate limit in message', () => {
      assert.strictEqual(
        isRetryableError({ message: 'Rate limit exceeded' }),
        true
      );
      assert.strictEqual(
        isRetryableError({ message: 'Too many requests' }),
        true
      );
    });

    it('should detect temporarily unavailable in message', () => {
      assert.strictEqual(
        isRetryableError({ message: 'Temporarily unavailable' }),
        true
      );
    });
  });

  describe('withRetry', () => {
    it('should succeed on first try', async () => {
      let attempts = 0;
      const fn = async () => {
        attempts++;
        return 'success';
      };

      const result = await withRetry(fn);
      assert.strictEqual(result, 'success');
      assert.strictEqual(attempts, 1);
    });

    it('should retry on retryable error', async () => {
      let attempts = 0;
      const fn = async () => {
        attempts++;
        if (attempts < 3) {
          const error = new Error('Overloaded');
          error.status = 529;
          throw error;
        }
        return 'success';
      };

      const result = await withRetry(fn, { delays: [10, 20, 30] });
      assert.strictEqual(result, 'success');
      assert.strictEqual(attempts, 3);
    });

    it('should not retry on non-retryable error', async () => {
      let attempts = 0;
      const fn = async () => {
        attempts++;
        const error = new Error('Bad request');
        error.status = 400;
        throw error;
      };

      await assert.rejects(
        async () => await withRetry(fn, { delays: [10, 20, 30] }),
        /Bad request/
      );
      assert.strictEqual(attempts, 1);
    });

    it('should respect maxRetries', async () => {
      let attempts = 0;
      const fn = async () => {
        attempts++;
        const error = new Error('Always fails');
        error.status = 500;
        throw error;
      };

      await assert.rejects(
        async () => await withRetry(fn, { maxRetries: 2, delays: [10, 20] }),
        /Always fails/
      );
      assert.strictEqual(attempts, 3); // initial + 2 retries
    });

    it('should call onRetry callback', async () => {
      let retryCount = 0;
      const retryAttempts = [];

      const fn = async () => {
        retryCount++;
        if (retryCount < 3) {
          const error = new Error('Retry me');
          error.status = 500;
          throw error;
        }
        return 'done';
      };

      await withRetry(fn, {
        delays: [10, 20],
        onRetry: (attempt, error) => {
          retryAttempts.push(attempt);
        }
      });

      assert.deepStrictEqual(retryAttempts, [1, 2]);
    });

    it('should skip retryable check if checkRetryable is false', async () => {
      let attempts = 0;
      const fn = async () => {
        attempts++;
        if (attempts < 3) {
          throw new Error('Not retryable error');
        }
        return 'success';
      };

      const result = await withRetry(fn, {
        checkRetryable: false,
        delays: [10, 20]
      });
      assert.strictEqual(result, 'success');
      assert.strictEqual(attempts, 3);
    });

    it('should use custom isRetryable function', async () => {
      let attempts = 0;
      const fn = async () => {
        attempts++;
        if (attempts < 3) {
          throw new Error('CUSTOM_ERROR');
        }
        return 'success';
      };

      const result = await withRetry(fn, {
        isRetryable: (error) => {
          return error instanceof Error && error.message === 'CUSTOM_ERROR';
        },
        delays: [10, 20]
      });

      assert.strictEqual(result, 'success');
      assert.strictEqual(attempts, 3);
    });
  });

  describe('withTimeout', () => {
    it('should succeed before timeout', async () => {
      const fn = async () => {
        await sleep(50);
        return 'done';
      };

      const result = await withTimeout(fn, 200);
      assert.strictEqual(result, 'done');
    });

    it('should fail after timeout', async () => {
      const fn = async () => {
        await sleep(200);
        return 'done';
      };

      await assert.rejects(
        async () => await withTimeout(fn, 50, 'Too slow'),
        /Too slow/
      );
    });

    it('should use default timeout message', async () => {
      const fn = async () => {
        await sleep(200);
        return 'done';
      };

      await assert.rejects(
        async () => await withTimeout(fn, 50),
        /timed out/
      );
    });

    it('should propagate function errors', async () => {
      const fn = async () => {
        throw new Error('Function error');
      };

      await assert.rejects(
        async () => await withTimeout(fn, 200),
        /Function error/
      );
    });
  });

  describe('withRetryAndTimeout', () => {
    it('should combine retry and timeout', async () => {
      let attempts = 0;
      const fn = async () => {
        attempts++;
        if (attempts < 3) {
          const error = new Error('Retry me');
          error.status = 500;
          throw error;
        }
        return 'success';
      };

      const result = await withRetryAndTimeout(
        fn,
        { delays: [10, 20] },
        500
      );

      assert.strictEqual(result, 'success');
      assert.strictEqual(attempts, 3);
    });

    it('should timeout even with retries', async () => {
      const fn = async () => {
        await sleep(100);
        const error = new Error('Slow');
        error.status = 500;
        throw error;
      };

      await assert.rejects(
        async () => await withRetryAndTimeout(
          fn,
          { maxRetries: 10, delays: [50, 50, 50] },
          200
        ),
        /timed out/
      );
    });
  });
});
