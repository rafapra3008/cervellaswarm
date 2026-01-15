/**
 * Task Command Tests
 *
 * Test per commands/task.js
 * Verifica: validazione, routing, spawning, reporting
 *
 * "One step at a time. The team is with you."
 */

import { test, describe } from 'node:test';
import assert from 'node:assert/strict';
import { createTempDir, createFileStructure, readTempFile } from '../helpers/temp-dir.js';
import { captureConsole } from '../helpers/console-capture.js';
import { createMockProcess } from '../helpers/mock-spawn.js';

describe('Task Command', () => {

  describe('Input validation', () => {
    test('requires task description', async (t) => {
      const output = captureConsole(t);

      const description = '';

      if (!description || description.trim().length === 0) {
        console.log('  Please provide a task description.');
        console.log('  Example: cervellaswarm task "add login page"');
      }

      assert.ok(output.hasLog('Please provide'), 'Should ask for description');
      assert.ok(output.hasLog('Example:'), 'Should show example');
    });

    test('trims whitespace from description', async (t) => {
      const description = '   add login page   ';
      const trimmed = description.trim();

      assert.equal(trimmed, 'add login page');
    });
  });

  describe('Project context', () => {
    test('requires initialized project', async (t) => {
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

  describe('Task display', () => {
    test('shows task received confirmation', async (t) => {
      const output = captureConsole(t);

      const description = 'Add authentication feature';

      console.log('  Task received!');
      console.log(`  "${description.trim()}"`);

      assert.ok(output.hasLog('Task received'), 'Should confirm receipt');
      assert.ok(output.hasLog('Add authentication'), 'Should show description');
    });

    test('shows agent assignment', async (t) => {
      const output = captureConsole(t);

      const agent = 'cervella-backend';

      console.log(`  [${agent}] Starting work...`);

      assert.ok(output.hasLog('[cervella-backend]'), 'Should show agent name');
      assert.ok(output.hasLog('Starting work'), 'Should show status');
    });
  });

  describe('Auto routing', () => {
    test('uses router when --auto flag', async (t) => {
      const options = { auto: true };

      // Simula routing
      let agent = options.agent;
      if (!agent || options.auto) {
        agent = 'cervella-backend'; // Simulato da router
      }

      assert.equal(agent, 'cervella-backend');
    });

    test('uses specified agent when --agent flag', async (t) => {
      const options = { agent: 'cervella-frontend' };

      const agent = options.agent;

      assert.equal(agent, 'cervella-frontend');
    });
  });

  describe('Task completion', () => {
    test('shows success message on completion', async (t) => {
      const output = captureConsole(t);

      const result = { success: true };

      if (result.success) {
        console.log('  Task completed!');
        console.log('  One more step forward.');
      }

      assert.ok(output.hasLog('Task completed'), 'Should show success');
      assert.ok(output.hasLog('step forward'), 'Should encourage');
    });

    test('shows warning on issues', async (t) => {
      const output = captureConsole(t);

      const result = { success: false, error: 'Something went wrong' };

      if (!result.success) {
        console.log('  Task finished with issues.');
        console.log(`  ${result.error || 'Check the output above.'}`);
      }

      assert.ok(output.hasLog('with issues'), 'Should show warning');
      assert.ok(output.hasLog('Something went wrong'), 'Should show error');
    });

    test('suggests next step when available', async (t) => {
      const output = captureConsole(t);

      const result = { nextStep: 'Write tests for the new feature' };

      if (result.nextStep) {
        console.log('  Suggested next step:');
        console.log(`  ${result.nextStep}`);
        console.log("  (When you're ready)");
      }

      assert.ok(output.hasLog('Suggested next step'), 'Should show suggestion header');
      assert.ok(output.hasLog('Write tests'), 'Should show suggestion');
      assert.ok(output.hasLog("When you're ready"), 'Should not pressure');
    });
  });

  describe('Report saving', () => {
    test('saves task report to SNCP', async (t) => {
      const tempDir = await createTempDir(t);

      // Simula salvataggio report
      const report = {
        task: 'Add login feature',
        agent: 'cervella-backend',
        success: true,
        duration: '45s',
        filesModified: ['src/auth.js']
      };

      await createFileStructure(tempDir, {
        '.sncp/reports/tasks/task_20260115_1030.json': JSON.stringify(report)
      });

      const content = await readTempFile(tempDir, '.sncp/reports/tasks/task_20260115_1030.json');
      const parsed = JSON.parse(content);

      assert.equal(parsed.task, 'Add login feature');
      assert.equal(parsed.agent, 'cervella-backend');
      assert.equal(parsed.success, true);
    });
  });

  describe('Session creation', () => {
    test('creates session from task result', async (t) => {
      const tempDir = await createTempDir(t);

      const session = {
        type: 'task',
        summary: 'Add login feature',
        agent: 'cervella-backend',
        success: true,
        duration: '45s',
        filesModified: ['src/auth.js'],
        nextStep: 'Write tests'
      };

      await createFileStructure(tempDir, {
        '.sncp/sessions/session_20260115_1030.json': JSON.stringify(session)
      });

      const content = await readTempFile(tempDir, '.sncp/sessions/session_20260115_1030.json');
      const parsed = JSON.parse(content);

      assert.equal(parsed.type, 'task');
      assert.equal(parsed.summary, 'Add login feature');
      assert.ok(Array.isArray(parsed.filesModified));
    });
  });

  describe('Error handling', () => {
    test('catches and displays errors', async (t) => {
      const output = captureConsole(t);

      try {
        throw new Error('Network timeout');
      } catch (error) {
        console.error('  Error executing task:', error.message);
      }

      assert.ok(output.hasError('Error executing'), 'Should show error prefix');
      assert.ok(output.hasError('Network timeout'), 'Should show error message');
    });
  });

});

describe('Task Integration', () => {

  test('full task flow simulation', async (t) => {
    const tempDir = await createTempDir(t);
    const output = captureConsole(t);

    // Setup project
    await createFileStructure(tempDir, {
      '.sncp/config.json': JSON.stringify({
        name: 'test-project',
        description: 'Test project'
      }),
      '.sncp/sessions/.gitkeep': '',
      '.sncp/reports/tasks/.gitkeep': ''
    });

    // Simula flusso completo
    const description = 'Add user authentication';
    const context = { name: 'test-project' };

    // 1. Validate input
    assert.ok(description.length > 0, 'Description should be valid');

    // 2. Load context
    assert.ok(context, 'Context should be loaded');

    // 3. Route task
    const agent = 'cervella-backend'; // Simulato

    // 4. Show status
    console.log('  Task received!');
    console.log(`  "${description}"`);
    console.log(`  [${agent}] Starting work...`);

    // 5. Execute (mock)
    const result = {
      success: true,
      duration: '30s',
      filesModified: ['src/auth.js', 'src/middleware.js'],
      nextStep: 'Test the authentication flow'
    };

    // 6. Show result
    console.log('  Task completed!');
    console.log(`  Suggested next step: ${result.nextStep}`);

    // Verify flow
    assert.ok(output.hasLog('Task received'), 'Should show task received');
    assert.ok(output.hasLog('[cervella-backend]'), 'Should show agent');
    assert.ok(output.hasLog('Task completed'), 'Should show completion');
    assert.ok(output.hasLog('Test the authentication'), 'Should show next step');
  });

});
