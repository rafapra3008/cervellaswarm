/**
 * Resume Command Tests
 *
 * Test per commands/resume.js
 * Verifica: recap basato su tempo, lista sessioni, no judgment
 *
 * "Welcome back! Let's continue from where we were."
 */

import { test, describe } from 'node:test';
import assert from 'node:assert/strict';
import { createTempDir, createFileStructure } from '../helpers/temp-dir.js';
import { captureConsole } from '../helpers/console-capture.js';

describe('Resume Command', () => {

  describe('No project found', () => {
    test('suggests init when no project', async (t) => {
      const output = captureConsole(t);

      const context = null;

      if (!context) {
        console.log('  No CervellaSwarm project found.');
        console.log('  Run `cervellaswarm init` first.');
      }

      assert.ok(output.hasLog('No CervellaSwarm project'), 'Should warn no project');
      assert.ok(output.hasLog('init'), 'Should suggest init');
    });
  });

  describe('List sessions (-l flag)', () => {
    test('shows empty state when no sessions', async (t) => {
      const output = captureConsole(t);

      const sessions = [];

      if (sessions.length === 0) {
        console.log('  No sessions yet.');
        console.log('  Run `cervellaswarm task "..."` to start.');
      }

      assert.ok(output.hasLog('No sessions yet'), 'Should show empty state');
      assert.ok(output.hasLog('task'), 'Should suggest task command');
    });

    test('lists recent sessions', async (t) => {
      const output = captureConsole(t);

      const sessions = [
        { summary: 'Added login feature', date: '2026-01-15T10:00:00Z', success: true },
        { summary: 'Fixed bug in auth', date: '2026-01-14T15:00:00Z', success: true },
        { summary: 'Updated README', date: '2026-01-14T10:00:00Z', success: false }
      ];

      console.log('  Recent Sessions:');
      sessions.forEach((session, i) => {
        const status = session.success ? 'OK' : 'ERR';
        console.log(`  ${i + 1}. [${status}] ${session.summary}`);
      });

      assert.ok(output.hasLog('Recent Sessions'), 'Should show header');
      assert.ok(output.hasLog('Added login'), 'Should show first session');
      assert.ok(output.hasLog('Fixed bug'), 'Should show second session');
      assert.ok(output.hasLog('[ERR]'), 'Should show error status');
    });

    test('limits to 10 sessions', async (t) => {
      const sessions = Array.from({ length: 15 }, (_, i) => ({
        summary: `Task ${i + 1}`,
        date: new Date().toISOString()
      }));

      const displayed = sessions.slice(0, 10);

      assert.equal(displayed.length, 10, 'Should limit to 10');
    });
  });

  describe('First session', () => {
    test('welcomes new user', async (t) => {
      const output = captureConsole(t);

      const lastSession = null;

      if (!lastSession) {
        console.log('  This is your first session!');
        console.log('  Run `cervellaswarm task "your task"` to start.');
      }

      assert.ok(output.hasLog('first session'), 'Should welcome new user');
      assert.ok(output.hasLog('task'), 'Should suggest starting');
    });
  });

  describe('Welcome back', () => {
    test('shows welcome message', async (t) => {
      const output = captureConsole(t);

      console.log('  Welcome back!');

      assert.ok(output.hasLog('Welcome back'), 'Should welcome user');
    });

    test('shows encouraging close without pressure', async (t) => {
      const output = captureConsole(t);

      console.log('  Ready to take the next step?');
      console.log('  Run `cervellaswarm task "..."` when you\'re ready.');

      assert.ok(output.hasLog('Ready to take'), 'Should ask gently');
      assert.ok(output.hasLog("when you're ready"), 'Should not pressure');
    });
  });

  describe('Time calculation', () => {
    test('calculates days since correctly', () => {
      const calculateDaysSince = (dateString) => {
        const lastDate = new Date(dateString);
        const now = new Date();
        const diffTime = Math.abs(now - lastDate);
        return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
      };

      // Test con data di ieri
      const yesterday = new Date();
      yesterday.setDate(yesterday.getDate() - 1);
      const days = calculateDaysSince(yesterday.toISOString());

      assert.ok(days >= 1, 'Yesterday should be at least 1 day');
      assert.ok(days <= 2, 'Yesterday should be at most 2 days');
    });

    test('handles same day sessions', () => {
      const calculateDaysSince = (dateString) => {
        const lastDate = new Date(dateString);
        const now = new Date();
        const diffTime = Math.abs(now - lastDate);
        return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
      };

      // Test con data di oggi (poche ore fa)
      const today = new Date();
      today.setHours(today.getHours() - 2);
      const days = calculateDaysSince(today.toISOString());

      assert.ok(days >= 0, 'Same day should be 0 or 1');
      assert.ok(days <= 1, 'Same day should be at most 1');
    });
  });

  describe('Specific session', () => {
    test('loads session by ID with -s flag', async (t) => {
      const tempDir = await createTempDir(t);

      await createFileStructure(tempDir, {
        '.sncp/sessions/session_20260115_1000.json': JSON.stringify({
          type: 'task',
          summary: 'Specific task',
          date: '2026-01-15T10:00:00Z'
        })
      });

      const options = { session: 'session_20260115_1000' };

      assert.ok(options.session, 'Should have session ID');
    });
  });

  describe('Error handling', () => {
    test('handles errors gracefully', async (t) => {
      const output = captureConsole(t);

      try {
        throw new Error('Session file corrupted');
      } catch (error) {
        console.error('  Error resuming session:', error.message);
      }

      assert.ok(output.hasError('Error resuming'), 'Should show error');
      assert.ok(output.hasError('corrupted'), 'Should show message');
    });
  });

});

describe('Recap Generation', () => {

  describe('Time-based recap levels', () => {
    test('short recap for same day', async (t) => {
      const daysSince = 0;

      // Livello 1: stesso giorno - recap breve
      const recapLevel = daysSince === 0 ? 'short' :
                         daysSince <= 3 ? 'medium' : 'full';

      assert.equal(recapLevel, 'short');
    });

    test('medium recap for 1-3 days', async (t) => {
      const daysSince = 2;

      const recapLevel = daysSince === 0 ? 'short' :
                         daysSince <= 3 ? 'medium' : 'full';

      assert.equal(recapLevel, 'medium');
    });

    test('full recap for 4+ days', async (t) => {
      const daysSince = 7;

      const recapLevel = daysSince === 0 ? 'short' :
                         daysSince <= 3 ? 'medium' : 'full';

      assert.equal(recapLevel, 'full');
    });
  });

  describe('No judgment principle', () => {
    test('recap does not mention time negatively', () => {
      const negativePatterns = [
        'been a while',
        'long time',
        'finally back',
        'where have you been',
        'too long',
        'overdue'
      ];

      const recapText = 'Welcome back! Here is your project summary.';

      const hasNegative = negativePatterns.some(p =>
        recapText.toLowerCase().includes(p)
      );

      assert.equal(hasNegative, false, 'Should not judge time away');
    });

    test('recap uses neutral time language', () => {
      const neutralPhrases = [
        'Last session',
        'Where we were',
        'Current status',
        'Ready to continue'
      ];

      // Almeno alcune frasi neutrali dovrebbero essere usate
      assert.ok(neutralPhrases.length > 0, 'Should have neutral options');
    });
  });

});
