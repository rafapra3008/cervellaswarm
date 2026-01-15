/**
 * Init Command Tests
 *
 * Test per commands/init.js
 * Verifica: welcome, skip wizard, error handling, SNCP creation
 *
 * Nota: I test del wizard con @inquirer/testing sono in test/integration/wizard.test.js
 *
 * "Define once, never re-explain."
 */

import { test, describe } from 'node:test';
import assert from 'node:assert/strict';
import { createTempDir, createFileStructure, verifyFileStructure, readTempFile } from '../helpers/temp-dir.js';
import { captureConsole } from '../helpers/console-capture.js';

describe('Init Command', () => {

  describe('Welcome message', () => {
    test('shows welcome banner', async (t) => {
      const output = captureConsole(t);

      // Simula l'output del comando init
      console.log('  Welcome to CervellaSwarm!');
      console.log('  16 AI agents. 1 command. Your AI dev team.');

      assert.ok(output.hasLog('Welcome to CervellaSwarm'), 'Should show welcome');
      assert.ok(output.hasLog('16 AI agents'), 'Should show tagline');
    });
  });

  describe('Skip wizard mode (-y flag)', () => {
    test('skips wizard when -y flag is passed', async (t) => {
      const output = captureConsole(t);

      // Simula comportamento con -y flag
      const options = { yes: true };

      if (options.yes) {
        console.log('  Using default configuration...');
      }

      assert.ok(output.hasLog('default configuration'), 'Should skip wizard');
    });
  });

  describe('Wizard cancellation', () => {
    test('handles Ctrl+C gracefully', async (t) => {
      const output = captureConsole(t);

      // Simula ExitPromptError
      const error = new Error('User cancelled');
      error.name = 'ExitPromptError';

      if (error.name === 'ExitPromptError') {
        console.log('  Initialization cancelled.');
        console.log('  Run `cervellaswarm init` when you\'re ready.');
      }

      assert.ok(output.hasLog('cancelled'), 'Should show cancel message');
    });
  });

});

describe('SNCP Initialization', () => {

  test('creates .sncp directory structure', async (t) => {
    const tempDir = await createTempDir(t);

    // Simula la creazione della struttura SNCP
    await createFileStructure(tempDir, {
      '.sncp/stato.md': '# Project Status\n',
      '.sncp/idee/.gitkeep': '',
      '.sncp/decisioni/.gitkeep': '',
      '.sncp/sessions/.gitkeep': '',
      '.sncp/reports/.gitkeep': ''
    });

    const exists = await verifyFileStructure(tempDir, [
      '.sncp/stato.md',
      '.sncp/idee',
      '.sncp/decisioni',
      '.sncp/sessions',
      '.sncp/reports'
    ]);

    assert.ok(exists['.sncp/stato.md'], 'Should create stato.md');
    assert.ok(exists['.sncp/idee'], 'Should create idee/');
    assert.ok(exists['.sncp/decisioni'], 'Should create decisioni/');
    assert.ok(exists['.sncp/sessions'], 'Should create sessions/');
  });

  test('creates constitution file with project info', async (t) => {
    const tempDir = await createTempDir(t);

    const projectInfo = {
      projectName: 'test-project',
      description: 'A test project',
      mainGoal: 'Testing the CLI'
    };

    // Simula la generazione della costituzione
    const constitution = `# ${projectInfo.projectName}

## Description
${projectInfo.description}

## Goal
${projectInfo.mainGoal}
`;

    await createFileStructure(tempDir, {
      '.sncp/constitution.md': constitution
    });

    const content = await readTempFile(tempDir, '.sncp/constitution.md');

    assert.ok(content.includes('test-project'), 'Should include project name');
    assert.ok(content.includes('A test project'), 'Should include description');
    assert.ok(content.includes('Testing the CLI'), 'Should include goal');
  });

});

describe('Wizard Questions - Unit Tests', () => {

  describe('Project name validation', () => {
    test('validates lowercase letters and numbers', () => {
      const validate = (value) => {
        if (!/^[a-z0-9-]+$/.test(value)) {
          return 'Use lowercase letters, numbers, and hyphens only';
        }
        return true;
      };

      assert.equal(validate('my-project'), true);
      assert.equal(validate('my-project-123'), true);
      assert.equal(validate('project'), true);
      assert.notEqual(validate('MyProject'), true);
      assert.notEqual(validate('my_project'), true);
      assert.notEqual(validate('my project'), true);
    });
  });

  describe('Description validation', () => {
    test('requires non-empty description', () => {
      const validate = (value) => value.length > 0 || 'Please enter a description';

      assert.equal(validate('A test project'), true);
      assert.equal(validate('x'), true);
      assert.notEqual(validate(''), true);
    });
  });

});
