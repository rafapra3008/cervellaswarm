/**
 * Tests for Recap Generator
 *
 * Covers: generateRecap with 4 branches based on daysSince
 * Branch 0: same day, <=3: recent, <=7: week, >7: long gap
 */

import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { generateRecap } from '../../src/display/recap.js';

// Strip ANSI codes for content assertions
function stripAnsi(str) {
  // eslint-disable-next-line no-control-regex
  return str.replace(/\x1b\[[0-9;]*m/g, '');
}

describe('Recap Generator', () => {
  const context = {
    name: 'test-project',
    goal: 'Build something great',
    nextStep: 'Write more tests'
  };

  const lastSession = {
    date: '3 Apr 14:30',
    summary: 'Added authentication module'
  };

  describe('daysSince === 0 (same day)', () => {
    it('returns minimal recap', async () => {
      const recap = await generateRecap(context, lastSession, 0);
      const text = stripAnsi(recap);

      assert.ok(text.includes('earlier today'), 'Should mention earlier today');
      assert.ok(text.includes('Added authentication module'), 'Should show last task');
    });

    it('does not show next step', async () => {
      const recap = await generateRecap(context, lastSession, 0);
      const text = stripAnsi(recap);

      assert.ok(!text.includes('Next step'), 'Same-day recap should not show next step');
    });
  });

  describe('daysSince <= 3 (recent)', () => {
    it('shows days ago and next step', async () => {
      const recap = await generateRecap(context, lastSession, 2);
      const text = stripAnsi(recap);

      assert.ok(text.includes('2 day(s) ago'), 'Should show days count');
      assert.ok(text.includes('Added authentication module'), 'Should show what was worked on');
      assert.ok(text.includes('Write more tests'), 'Should show next step');
    });

    it('works for 1 day', async () => {
      const recap = await generateRecap(context, lastSession, 1);
      const text = stripAnsi(recap);

      assert.ok(text.includes('1 day(s) ago'));
    });

    it('works for 3 days (boundary)', async () => {
      const recap = await generateRecap(context, lastSession, 3);
      const text = stripAnsi(recap);

      assert.ok(text.includes('3 day(s) ago'));
    });
  });

  describe('daysSince <= 7 (week)', () => {
    it('shows fuller recap with Quick Recap header', async () => {
      const recap = await generateRecap(context, lastSession, 5);
      const text = stripAnsi(recap);

      assert.ok(text.includes('Quick Recap'), 'Should show Quick Recap header');
      assert.ok(text.includes('5 days ago'), 'Should show days count');
      assert.ok(text.includes('What you did'), 'Should have What you did section');
      assert.ok(text.includes('Suggested next step'), 'Should show next step section');
    });

    it('works for 4 days', async () => {
      const recap = await generateRecap(context, lastSession, 4);
      const text = stripAnsi(recap);

      assert.ok(text.includes('Quick Recap'));
      assert.ok(text.includes('4 days ago'));
    });

    it('works for 7 days (boundary)', async () => {
      const recap = await generateRecap(context, lastSession, 7);
      const text = stripAnsi(recap);

      assert.ok(text.includes('Quick Recap'));
    });
  });

  describe('daysSince > 7 (long gap)', () => {
    it('shows full welcome back recap', async () => {
      const recap = await generateRecap(context, lastSession, 14);
      const text = stripAnsi(recap);

      assert.ok(text.includes('Welcome back'), 'Should welcome user back');
      assert.ok(text.includes('test-project'), 'Should show project name');
      assert.ok(text.includes('Build something great'), 'Should show goal');
      assert.ok(text.includes('3 Apr 14:30'), 'Should show last session date');
      assert.ok(text.includes('Added authentication module'), 'Should show last session summary');
      assert.ok(text.includes('Suggested next step'), 'Should show next step section');
    });

    it('works for 30 days', async () => {
      const recap = await generateRecap(context, lastSession, 30);
      const text = stripAnsi(recap);

      assert.ok(text.includes('Welcome back'));
    });

    it('works for 8 days (just over boundary)', async () => {
      const recap = await generateRecap(context, lastSession, 8);
      const text = stripAnsi(recap);

      assert.ok(text.includes('Welcome back'));
      assert.ok(!text.includes('Quick Recap'), 'Should NOT show Quick Recap header');
    });
  });
});
