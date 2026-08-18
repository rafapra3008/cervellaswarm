/**
 * Tests for display/status.js -- formatStatus
 */

import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { formatStatus } from '../../src/display/status.js';

// Strip ANSI escape codes for text comparison
function stripAnsi(str) {
  return str.replace(/\x1b\[[0-9;]*m/g, '');
}

describe('formatStatus', () => {
  it('formats 0% progress', () => {
    const result = formatStatus({ progress: 0 });
    const text = stripAnsi(result);
    assert.ok(text.includes('0%'));
    assert.ok(text.includes('░'), 'Should have empty blocks');
  });

  it('formats 100% progress', () => {
    const result = formatStatus({ progress: 100 });
    const text = stripAnsi(result);
    assert.ok(text.includes('100%'));
    assert.ok(text.includes('█'), 'Should have filled blocks');
  });

  it('formats 50% progress', () => {
    const result = formatStatus({ progress: 50 });
    const text = stripAnsi(result);
    assert.ok(text.includes('50%'));
  });

  it('handles missing progress (defaults to 0)', () => {
    const result = formatStatus({});
    const text = stripAnsi(result);
    assert.ok(text.includes('0%'));
  });

  it('returns a string', () => {
    assert.equal(typeof formatStatus({ progress: 42 }), 'string');
  });
});
