/**
 * Wizard Integration Tests
 *
 * Test di integrazione per il wizard con @inquirer/testing.
 * Questi test sono più lenti e vanno eseguiti separatamente.
 *
 * Esecuzione: npm run test:wizard
 *
 * "Define once, never re-explain."
 */

import { test, describe } from 'node:test';
import assert from 'node:assert/strict';
import { render } from '@inquirer/testing';

describe('Wizard Questions - Integration', () => {

  describe('Project name validation', () => {
    test('accepts valid project names', async () => {
      const { answer, events } = await render(
        async () => {
          const { input } = await import('@inquirer/prompts');
          return input({
            message: 'Project name:',
            validate: (value) => {
              if (!/^[a-z0-9-]+$/.test(value)) {
                return 'Use lowercase letters, numbers, and hyphens only';
              }
              return true;
            }
          });
        }
      );

      events.type('my-project');
      events.keypress('enter');

      const result = await answer;
      assert.equal(result, 'my-project');
    });

    test('accepts hyphens in project names', async () => {
      const { answer, events } = await render(
        async () => {
          const { input } = await import('@inquirer/prompts');
          return input({
            message: 'Project name:',
            validate: (value) => {
              if (!/^[a-z0-9-]+$/.test(value)) {
                return 'Use lowercase letters, numbers, and hyphens only';
              }
              return true;
            }
          });
        }
      );

      events.type('my-cool-project-123');
      events.keypress('enter');

      const result = await answer;
      assert.equal(result, 'my-cool-project-123');
    });
  });

  describe('Project type selection', () => {
    test('allows selecting webapp', async () => {
      const { answer, events } = await render(
        async () => {
          const { select } = await import('@inquirer/prompts');
          return select({
            message: 'Project type:',
            choices: [
              { name: 'Web Application (frontend + backend)', value: 'webapp' },
              { name: 'API / Backend Service', value: 'api' },
              { name: 'CLI Tool', value: 'cli' }
            ]
          });
        }
      );

      events.keypress('enter');

      const result = await answer;
      assert.equal(result, 'webapp');
    });

    test('allows navigating and selecting cli', async () => {
      const { answer, events } = await render(
        async () => {
          const { select } = await import('@inquirer/prompts');
          return select({
            message: 'Project type:',
            choices: [
              { name: 'Web Application', value: 'webapp' },
              { name: 'API Service', value: 'api' },
              { name: 'CLI Tool', value: 'cli' }
            ]
          });
        }
      );

      events.keypress('down');
      events.keypress('down');
      events.keypress('enter');

      const result = await answer;
      assert.equal(result, 'cli');
    });
  });

  describe('Success criteria checkbox', () => {
    test('allows multiple selections', async () => {
      const { answer, events } = await render(
        async () => {
          const { checkbox } = await import('@inquirer/prompts');
          return checkbox({
            message: 'How will you know the project succeeded?',
            choices: [
              { name: 'Users actively using it', value: 'users' },
              { name: 'Revenue generated', value: 'revenue' },
              { name: 'Problem solved', value: 'personal' }
            ]
          });
        }
      );

      events.keypress('space');
      events.keypress('down');
      events.keypress('down');
      events.keypress('space');
      events.keypress('enter');

      const result = await answer;
      assert.deepEqual(result, ['users', 'personal']);
    });
  });

  describe('Confirm prompts', () => {
    test('accepts default true', async () => {
      const { answer, events } = await render(
        async () => {
          const { confirm } = await import('@inquirer/prompts');
          return confirm({
            message: 'Do you already know what technologies you\'ll use?',
            default: true
          });
        }
      );

      events.keypress('enter');

      const result = await answer;
      assert.equal(result, true);
    });

    test('accepts explicit no', async () => {
      const { answer, events } = await render(
        async () => {
          const { confirm } = await import('@inquirer/prompts');
          return confirm({
            message: 'Continue?',
            default: true
          });
        }
      );

      events.type('n');
      events.keypress('enter');

      const result = await answer;
      assert.equal(result, false);
    });
  });

});
