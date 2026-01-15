/**
 * Tests for error handling module
 */

import { describe, it, before, after, mock } from 'node:test';
import assert from 'node:assert/strict';
import {
  ExitCode,
  ErrorType,
  CervellaError,
  displayError,
  httpStatusToErrorType,
  isRetryable
} from '../../src/utils/errors.js';

describe('Error Module', () => {
  describe('ExitCode', () => {
    it('has standard codes', () => {
      assert.equal(ExitCode.SUCCESS, 0);
      assert.equal(ExitCode.GENERAL_ERROR, 1);
      assert.equal(ExitCode.MISUSE, 2);
      assert.equal(ExitCode.CANCELLED, 130);
    });

    it('has custom codes for CervellaSwarm', () => {
      assert.equal(ExitCode.NOT_INITIALIZED, 3);
      assert.equal(ExitCode.API_ERROR, 4);
      assert.equal(ExitCode.CONFIG_ERROR, 5);
    });
  });

  describe('ErrorType', () => {
    it('has NOT_INITIALIZED error', () => {
      assert.ok(ErrorType.NOT_INITIALIZED);
      assert.equal(ErrorType.NOT_INITIALIZED.code, ExitCode.NOT_INITIALIZED);
      assert.ok(ErrorType.NOT_INITIALIZED.message);
      assert.ok(ErrorType.NOT_INITIALIZED.recovery);
    });

    it('has NO_API_KEY error with multi-step recovery', () => {
      assert.ok(ErrorType.NO_API_KEY);
      assert.ok(Array.isArray(ErrorType.NO_API_KEY.recovery));
      assert.equal(ErrorType.NO_API_KEY.recovery.length, 2);
    });

    it('has all required error types', () => {
      const requiredTypes = [
        'NOT_INITIALIZED',
        'MISSING_DESCRIPTION',
        'NO_API_KEY',
        'INVALID_API_KEY',
        'RATE_LIMITED',
        'TASK_TIMEOUT',
        'UNKNOWN'
      ];

      requiredTypes.forEach(type => {
        assert.ok(ErrorType[type], `Missing error type: ${type}`);
      });
    });
  });

  describe('CervellaError', () => {
    it('creates error with correct type', () => {
      const error = new CervellaError('NOT_INITIALIZED');
      assert.equal(error.name, 'CervellaError');
      assert.equal(error.type, 'NOT_INITIALIZED');
      assert.equal(error.code, ExitCode.NOT_INITIALIZED);
      assert.ok(error.message);
      assert.ok(error.recovery);
    });

    it('creates error with details', () => {
      const error = new CervellaError('WRITE_FAILED', 'Permission denied');
      assert.equal(error.details, 'Permission denied');
    });

    it('defaults to UNKNOWN for invalid type', () => {
      const error = new CervellaError('INVALID_TYPE_XYZ');
      assert.equal(error.code, ExitCode.GENERAL_ERROR);
    });

    it('is instanceof Error', () => {
      const error = new CervellaError('NOT_INITIALIZED');
      assert.ok(error instanceof Error);
    });
  });

  describe('httpStatusToErrorType', () => {
    it('maps 401 to INVALID_API_KEY', () => {
      assert.equal(httpStatusToErrorType(401), 'INVALID_API_KEY');
    });

    it('maps 403 to API_PERMISSION', () => {
      assert.equal(httpStatusToErrorType(403), 'API_PERMISSION');
    });

    it('maps 429 to RATE_LIMITED', () => {
      assert.equal(httpStatusToErrorType(429), 'RATE_LIMITED');
    });

    it('maps 500/503 to API_UNAVAILABLE', () => {
      assert.equal(httpStatusToErrorType(500), 'API_UNAVAILABLE');
      assert.equal(httpStatusToErrorType(503), 'API_UNAVAILABLE');
    });

    it('maps unknown status to UNKNOWN', () => {
      assert.equal(httpStatusToErrorType(999), 'UNKNOWN');
    });
  });

  describe('isRetryable', () => {
    it('RATE_LIMITED is retryable', () => {
      assert.ok(isRetryable('RATE_LIMITED'));
    });

    it('API_UNAVAILABLE is retryable', () => {
      assert.ok(isRetryable('API_UNAVAILABLE'));
    });

    it('INVALID_API_KEY is not retryable', () => {
      assert.ok(!isRetryable('INVALID_API_KEY'));
    });

    it('NOT_INITIALIZED is not retryable', () => {
      assert.ok(!isRetryable('NOT_INITIALIZED'));
    });
  });

  describe('displayError', () => {
    let originalLog;
    let output = [];

    before(() => {
      originalLog = console.log;
      console.log = (...args) => output.push(args.join(' '));
    });

    after(() => {
      console.log = originalLog;
    });

    it('displays CervellaError with recovery', () => {
      output = [];
      const error = new CervellaError('NOT_INITIALIZED');
      displayError(error);

      const fullOutput = output.join('\n');
      assert.ok(fullOutput.includes('Error'));
      assert.ok(fullOutput.includes('init'));
    });

    it('displays regular Error', () => {
      output = [];
      const error = new Error('Something went wrong');
      displayError(error);

      const fullOutput = output.join('\n');
      assert.ok(fullOutput.includes('Error'));
    });
  });
});
