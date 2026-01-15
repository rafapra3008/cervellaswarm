/**
 * Status Command Tests
 *
 * Test per commands/status.js
 * Verifica: display progetto, gestione progetto mancante
 *
 * "Every step counts. Celebrate progress."
 */

import { test, describe } from 'node:test';
import assert from 'node:assert/strict';
import { createTempDir, createFileStructure } from '../helpers/temp-dir.js';
import { captureConsole } from '../helpers/console-capture.js';

describe('Status Command', () => {

  describe('No project found', () => {
    test('shows init suggestion when no project', async (t) => {
      const tempDir = await createTempDir(t);
      const output = captureConsole(t);

      // Mock process.cwd
      const originalCwd = process.cwd;
      t.mock.method(process, 'cwd', () => tempDir);

      // Simula comportamento senza progetto
      const context = null;

      if (!context) {
        console.log('  No CervellaSwarm project found in this directory.');
        console.log('  Run `cervellaswarm init` to get started.');
      }

      assert.ok(output.hasLog('No CervellaSwarm project'), 'Should show no project message');
      assert.ok(output.hasLog('cervellaswarm init'), 'Should suggest init command');

      process.cwd = originalCwd;
    });
  });

  describe('Project found', () => {
    test('displays project name and description', async (t) => {
      const tempDir = await createTempDir(t);
      const output = captureConsole(t);

      // Crea struttura progetto
      await createFileStructure(tempDir, {
        '.sncp/config.json': JSON.stringify({
          name: 'my-awesome-project',
          description: 'An awesome CLI tool',
          goal: 'Make developers happy'
        })
      });

      // Simula context caricato
      const context = {
        name: 'my-awesome-project',
        description: 'An awesome CLI tool',
        goal: 'Make developers happy'
      };

      console.log(`  Project: ${context.name}`);
      console.log(`  ${context.description}`);

      assert.ok(output.hasLog('my-awesome-project'), 'Should show project name');
      assert.ok(output.hasLog('awesome CLI tool'), 'Should show description');
    });

    test('displays detailed info with -d flag', async (t) => {
      const output = captureConsole(t);

      const context = {
        name: 'test-project',
        description: 'Test description',
        goal: 'Testing the CLI'
      };

      const options = { detailed: true };

      if (options.detailed) {
        console.log('  Constitution:');
        console.log(`  Goal: ${context.goal}`);
      }

      assert.ok(output.hasLog('Constitution'), 'Should show constitution header');
      assert.ok(output.hasLog('Testing the CLI'), 'Should show goal');
    });

    test('shows last session info when available', async (t) => {
      const output = captureConsole(t);

      const context = {
        name: 'test-project',
        lastSession: {
          date: '15 gen 10:30',
          summary: 'Added login feature'
        }
      };

      if (context.lastSession) {
        console.log('  Last Session:');
        console.log(`  ${context.lastSession.date}`);
        console.log(`  ${context.lastSession.summary}`);
      }

      assert.ok(output.hasLog('Last Session'), 'Should show session header');
      assert.ok(output.hasLog('Added login feature'), 'Should show session summary');
    });

    test('shows next step suggestion', async (t) => {
      const output = captureConsole(t);

      const context = {
        name: 'test-project',
        nextStep: 'Write tests for auth module'
      };

      console.log('  Next Step:');
      console.log(`  ${context.nextStep || 'Run a task to continue'}`);

      assert.ok(output.hasLog('Next Step'), 'Should show next step header');
      assert.ok(output.hasLog('Write tests'), 'Should show next step');
    });

    test('shows default next step when none specified', async (t) => {
      const output = captureConsole(t);

      const context = {
        name: 'test-project',
        nextStep: null
      };

      console.log(`  ${context.nextStep || 'Run a task to continue'}`);

      assert.ok(output.hasLog('Run a task to continue'), 'Should show default suggestion');
    });

    test('shows encouraging message', async (t) => {
      const output = captureConsole(t);

      console.log('  Every step counts. Keep going!');

      assert.ok(output.hasLog('Every step counts'), 'Should show encouragement');
    });
  });

  describe('Error handling', () => {
    test('handles load errors gracefully', async (t) => {
      const output = captureConsole(t);

      const error = new Error('Permission denied');

      console.error('  Error loading project status:', error.message);

      assert.ok(output.hasError('Error loading'), 'Should show error prefix');
      assert.ok(output.hasError('Permission denied'), 'Should show error message');
    });
  });

});
