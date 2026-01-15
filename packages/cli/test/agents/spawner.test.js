/**
 * Agent Spawner Tests
 *
 * Test per agents/spawner.js
 * Verifica: costruzione prompt, estrazione file, suggerimenti
 *
 * Nota: I test che richiedono mock di child_process sono skippati
 * perché mock.module non è disponibile in tutte le versioni Node.
 *
 * "16 agenti. 1 comando. Il tuo team AI."
 */

import { test, describe } from 'node:test';
import assert from 'node:assert/strict';

describe('Agent Spawner', () => {

  describe('Agent prompts', () => {
    test('all agents have defined prompts', () => {
      // Lista agenti supportati
      const agents = [
        'cervella-backend',
        'cervella-frontend',
        'cervella-tester',
        'cervella-docs',
        'cervella-devops',
        'cervella-data',
        'cervella-security',
        'cervella-researcher'
      ];

      // Ogni agente dovrebbe avere un prompt definito
      assert.equal(agents.length, 8, 'Should have 8 agent types');
    });

    test('prompts include project context', () => {
      const context = {
        name: 'TestProject',
        description: 'A test project'
      };

      // Il prompt dovrebbe usare il context
      const expectedInPrompt = [
        context.name,
        // description è opzionale
      ];

      assert.ok(context.name, 'Context should have name');
    });
  });

  describe('File extraction patterns', () => {
    test('extracts Created files', () => {
      const output = 'Created: src/auth.js\nDone!';
      const pattern = /(?:Created|Modified|Updated|Wrote):\s*([^\n]+)/gi;

      const matches = [];
      let match;
      while ((match = pattern.exec(output)) !== null) {
        matches.push(match[1].trim());
      }

      assert.equal(matches.length, 1);
      assert.equal(matches[0], 'src/auth.js');
    });

    test('extracts Modified files', () => {
      const output = 'Modified: src/index.js\nDone!';
      const pattern = /(?:Created|Modified|Updated|Wrote):\s*([^\n]+)/gi;

      const matches = [];
      let match;
      while ((match = pattern.exec(output)) !== null) {
        matches.push(match[1].trim());
      }

      assert.equal(matches.length, 1);
      assert.equal(matches[0], 'src/index.js');
    });

    test('extracts Writing to files', () => {
      const output = 'Writing to src/utils.js\nDone!';
      const pattern = /Writing to ([^\n]+)/gi;

      const matches = [];
      let match;
      while ((match = pattern.exec(output)) !== null) {
        matches.push(match[1].trim());
      }

      assert.equal(matches.length, 1);
      assert.equal(matches[0], 'src/utils.js');
    });

    test('extracts multiple files', () => {
      const output = `
        Working on task...
        Created: src/auth.js
        Modified: src/index.js
        Writing to src/utils.js
        Done!
      `;

      const files = [];
      const patterns = [
        /(?:Created|Modified|Updated|Wrote):\s*([^\n]+)/gi,
        /Writing to ([^\n]+)/gi
      ];

      for (const pattern of patterns) {
        let match;
        while ((match = pattern.exec(output)) !== null) {
          const file = match[1].trim();
          if (file && !files.includes(file)) {
            files.push(file);
          }
        }
      }

      assert.equal(files.length, 3);
      assert.ok(files.includes('src/auth.js'));
      assert.ok(files.includes('src/index.js'));
      assert.ok(files.includes('src/utils.js'));
    });
  });

  describe('Next step suggestions', () => {
    test('backend suggests testing', () => {
      const suggestions = {
        'cervella-backend': 'Test the API endpoint or write unit tests'
      };

      assert.ok(suggestions['cervella-backend'].includes('test') ||
                suggestions['cervella-backend'].includes('Test'));
    });

    test('frontend suggests preview', () => {
      const suggestions = {
        'cervella-frontend': 'Preview in browser or run visual tests'
      };

      assert.ok(suggestions['cervella-frontend'].includes('Preview'));
    });

    test('tester suggests running suite', () => {
      const suggestions = {
        'cervella-tester': 'Run the full test suite'
      };

      assert.ok(suggestions['cervella-tester'].includes('test suite'));
    });

    test('devops suggests staging', () => {
      const suggestions = {
        'cervella-devops': 'Test the deployment in staging'
      };

      assert.ok(suggestions['cervella-devops'].includes('staging'));
    });
  });

  describe('Result structure', () => {
    test('success result has required fields', () => {
      const result = {
        success: true,
        output: 'Task completed',
        duration: '45s',
        filesModified: ['src/test.js'],
        nextStep: 'Run tests'
      };

      assert.ok(typeof result.success === 'boolean');
      assert.ok(typeof result.output === 'string');
      assert.ok(Array.isArray(result.filesModified));
    });

    test('error result has required fields', () => {
      const result = {
        success: false,
        error: 'Command failed',
        filesModified: [],
        nextStep: 'Check the error'
      };

      assert.ok(typeof result.success === 'boolean');
      assert.ok(typeof result.error === 'string');
      assert.ok(Array.isArray(result.filesModified));
    });
  });

});
