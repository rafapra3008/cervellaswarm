/**
 * Workers Module Tests
 */

import { describe, it } from 'node:test';
import assert from 'node:assert';
import {
  WORKERS_VERSION,
  WORKER_TYPES,
  GUARDIAN_TYPES,
  ALL_AGENT_TYPES,
  buildAgentPrompt,
  getAgentPromptData,
  getAvailableWorkers,
  getAvailableGuardians,
  getAllAgents,
  isValidAgent,
  isValidWorker,
  isValidGuardian,
  normalizeAgentType,
  getSuggestedNextStep,
  extractFilesFromOutput,
  extractCodeBlocks,
  formatDuration,
  parseAgentName,
  estimateTokens,
  truncateText,
  hasErrorIndicators,
  extractSummary
} from '../dist/workers/index.js';

describe('Workers Module', () => {
  describe('Constants', () => {
    it('should export version', () => {
      assert.strictEqual(WORKERS_VERSION, '1.0.0-alpha.2');
    });

    it('should export worker types', () => {
      assert.ok(Array.isArray(WORKER_TYPES));
      assert.ok(WORKER_TYPES.includes('backend'));
      assert.ok(WORKER_TYPES.includes('frontend'));
      assert.ok(WORKER_TYPES.includes('tester'));
      assert.ok(WORKER_TYPES.length >= 8);
    });

    it('should export guardian types', () => {
      assert.ok(Array.isArray(GUARDIAN_TYPES));
      assert.ok(GUARDIAN_TYPES.includes('guardiana-qualita'));
      assert.strictEqual(GUARDIAN_TYPES.length, 3);
    });

    it('should export all agent types', () => {
      assert.ok(Array.isArray(ALL_AGENT_TYPES));
      assert.ok(ALL_AGENT_TYPES.length > WORKER_TYPES.length);
    });
  });

  describe('Prompts', () => {
    it('should build agent prompt with context', () => {
      const prompt = buildAgentPrompt('backend', {
        name: 'TestProject',
        description: 'A test project',
        path: '/test/path'
      });

      assert.ok(prompt.includes('CERVELLA-BACKEND'));
      assert.ok(prompt.includes('TestProject'));
      assert.ok(prompt.includes('/test/path'));
    });

    it('should build agent prompt without context', () => {
      const prompt = buildAgentPrompt('frontend');
      assert.ok(prompt.includes('CERVELLA-FRONTEND'));
    });

    it('should fallback to backend for unknown agent', () => {
      const prompt = buildAgentPrompt('unknown-agent');
      assert.ok(prompt.includes('CERVELLA-BACKEND'));
    });

    it('should get raw prompt data', () => {
      const data = getAgentPromptData('tester');
      assert.ok(data);
      assert.ok(data.intro.includes('CERVELLA-TESTER'));
      assert.ok(data.focus);
      assert.ok(data.style);
      assert.ok(data.output);
    });
  });

  describe('Registry', () => {
    it('should get available workers', () => {
      const workers = getAvailableWorkers();
      assert.ok(Array.isArray(workers));
      assert.ok(workers.length >= 8);

      const backend = workers.find(w => w.name === 'cervella-backend');
      assert.ok(backend);
      assert.ok(backend.description);
    });

    it('should get available guardians', () => {
      const guardians = getAvailableGuardians();
      assert.strictEqual(guardians.length, 3);

      const qualita = guardians.find(g => g.name === 'cervella-guardiana-qualita');
      assert.ok(qualita);
    });

    it('should get all agents', () => {
      const agents = getAllAgents();
      assert.ok(agents.length > 0);

      // Check model tier
      const backend = agents.find(a => a.name === 'cervella-backend');
      assert.strictEqual(backend?.model, 'sonnet');

      const guardiana = agents.find(a => a.name === 'cervella-guardiana-qualita');
      assert.strictEqual(guardiana?.model, 'opus');
    });

    it('should validate agent types', () => {
      assert.strictEqual(isValidAgent('backend'), true);
      assert.strictEqual(isValidAgent('cervella-backend'), true);
      assert.strictEqual(isValidAgent('not-an-agent'), false);
    });

    it('should validate worker types', () => {
      assert.strictEqual(isValidWorker('backend'), true);
      assert.strictEqual(isValidWorker('cervella-frontend'), true);
      assert.strictEqual(isValidWorker('guardiana-qualita'), false);
    });

    it('should validate guardian types', () => {
      assert.strictEqual(isValidGuardian('guardiana-qualita'), true);
      assert.strictEqual(isValidGuardian('cervella-guardiana-ops'), true);
      assert.strictEqual(isValidGuardian('backend'), false);
    });

    it('should normalize agent type', () => {
      assert.strictEqual(normalizeAgentType('cervella-backend'), 'backend');
      assert.strictEqual(normalizeAgentType('frontend'), 'frontend');
    });

    it('should get suggested next step', () => {
      const step = getSuggestedNextStep('tester');
      assert.ok(step.includes('test'));
    });
  });

  describe('Utils', () => {
    it('should extract files from output', () => {
      const output = `
        Create file: src/utils/helper.ts
        Modified: lib/core.js

        \`\`\`typescript
        // src/components/Button.tsx
        export const Button = () => {};
        \`\`\`
      `;

      const files = extractFilesFromOutput(output);
      assert.ok(files.includes('src/utils/helper.ts'));
      assert.ok(files.includes('lib/core.js'));
    });

    it('should extract code blocks', () => {
      const output = `
        Here's the code:

        \`\`\`typescript
        // helpers.ts
        export function helper() {}
        \`\`\`

        \`\`\`css
        .button { color: red; }
        \`\`\`
      `;

      const blocks = extractCodeBlocks(output);
      assert.strictEqual(blocks.length, 2);
      assert.strictEqual(blocks[0].language, 'typescript');
      assert.strictEqual(blocks[1].language, 'css');
    });

    it('should format duration', () => {
      assert.strictEqual(formatDuration(500), '500ms');
      assert.strictEqual(formatDuration(5000), '5s');
      assert.strictEqual(formatDuration(90000), '1m 30s');
    });

    it('should parse agent name', () => {
      const result1 = parseAgentName('backend');
      assert.strictEqual(result1.type, 'backend');
      assert.strictEqual(result1.fullName, 'cervella-backend');

      const result2 = parseAgentName('cervella-frontend');
      assert.strictEqual(result2.type, 'frontend');
      assert.strictEqual(result2.fullName, 'cervella-frontend');

      const result3 = parseAgentName('CERVELLA-TESTER');
      assert.strictEqual(result3.type, 'tester');
    });
  });

  describe('estimateTokens', () => {
    it('should estimate tokens based on char length / 4', () => {
      // 12 chars -> ceil(12/4) = 3
      assert.strictEqual(estimateTokens('hello world!'), 3);
    });

    it('should return 0 for empty string', () => {
      assert.strictEqual(estimateTokens(''), 0);
    });

    it('should ceil fractional results', () => {
      // 5 chars -> ceil(5/4) = 2
      assert.strictEqual(estimateTokens('hello'), 2);
      // 1 char -> ceil(1/4) = 1
      assert.strictEqual(estimateTokens('a'), 1);
    });

    it('should handle long text', () => {
      const longText = 'x'.repeat(4000);
      assert.strictEqual(estimateTokens(longText), 1000);
    });
  });

  describe('truncateText', () => {
    it('should return text unchanged if within limit', () => {
      assert.strictEqual(truncateText('short', 100), 'short');
    });

    it('should truncate with ellipsis when over limit', () => {
      const result = truncateText('hello world, this is long', 10);
      assert.strictEqual(result.length, 10);
      assert.ok(result.endsWith('...'));
      assert.strictEqual(result, 'hello w...');
    });

    it('should handle exact length boundary', () => {
      assert.strictEqual(truncateText('abcde', 5), 'abcde');
    });

    it('should handle text one char over limit', () => {
      const result = truncateText('abcdef', 5);
      assert.strictEqual(result, 'ab...');
      assert.strictEqual(result.length, 5);
    });
  });

  describe('hasErrorIndicators', () => {
    it('should detect "error:" pattern', () => {
      assert.strictEqual(hasErrorIndicators('Error: something broke'), true);
    });

    it('should detect "exception:" pattern', () => {
      assert.strictEqual(hasErrorIndicators('Exception: null ref'), true);
    });

    it('should detect "failed:" pattern', () => {
      assert.strictEqual(hasErrorIndicators('Build failed: timeout'), true);
    });

    it('should detect "cannot find" pattern', () => {
      assert.strictEqual(hasErrorIndicators('cannot find module'), true);
    });

    it('should detect "permission denied" pattern', () => {
      assert.strictEqual(hasErrorIndicators('Permission denied'), true);
    });

    it('should detect "not found" pattern', () => {
      assert.strictEqual(hasErrorIndicators('File not found'), true);
    });

    it('should return false for clean output', () => {
      assert.strictEqual(hasErrorIndicators('All tests passed successfully'), false);
    });

    it('should return false for empty string', () => {
      assert.strictEqual(hasErrorIndicators(''), false);
    });

    it('should be case insensitive', () => {
      assert.strictEqual(hasErrorIndicators('ERROR: boom'), true);
      assert.strictEqual(hasErrorIndicators('PERMISSION DENIED'), true);
    });
  });

  describe('extractSummary', () => {
    it('should extract text after summary header', () => {
      const output = `
Some work done here.
Summary:
Task completed with 3 files changed.
All tests pass.
      `;
      const result = extractSummary(output);
      assert.ok(result.includes('Task completed'));
    });

    it('should fallback to last line when no summary header', () => {
      const output = `
First line
Second line
Last meaningful line
      `;
      const result = extractSummary(output);
      assert.strictEqual(result, 'Last meaningful line');
    });

    it('should respect maxLength parameter', () => {
      const output = 'A'.repeat(300);
      const result = extractSummary(output, 50);
      assert.ok(result.length <= 50);
    });

    it('should handle empty output', () => {
      const result = extractSummary('');
      assert.strictEqual(result, '');
    });

    it('should recognize different header keywords', () => {
      const variants = ['Result:', 'Done:', 'Completed:', 'Conclusion:'];
      for (const header of variants) {
        const output = `Work log\n${header}\nFinished the job.`;
        const result = extractSummary(output);
        assert.ok(result.includes('Finished'), `Failed for header: ${header}`);
      }
    });
  });
});
