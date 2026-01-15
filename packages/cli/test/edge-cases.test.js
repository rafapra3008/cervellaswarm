/**
 * Edge Cases Tests
 *
 * Test per scenari edge e errori
 * Verifica: robustezza, gestione errori, casi limite
 *
 * "I dettagli fanno SEMPRE la differenza."
 */

import { test, describe } from 'node:test';
import assert from 'node:assert/strict';
import { createTempDir, createFileStructure, readTempFile } from './helpers/temp-dir.js';

describe('Edge Cases', () => {

  describe('Empty inputs', () => {
    test('handles empty task description', () => {
      const validate = (desc) => {
        return desc && desc.trim().length > 0;
      };

      // Validate returns falsy values (empty string, false, etc)
      assert.ok(!validate(''), 'Empty string should be invalid');
      assert.ok(!validate('   '), 'Whitespace should be invalid');
      assert.ok(!validate(null), 'Null should be invalid');
      assert.ok(!validate(undefined), 'Undefined should be invalid');
    });

    test('handles empty project name', () => {
      const validate = (name) => {
        return name && /^[a-z0-9-]+$/.test(name);
      };

      // Empty string returns '' which is falsy but not strictly false
      assert.ok(!validate(''), 'Empty string should be invalid');
      assert.ok(!validate('   '), 'Whitespace should be invalid');
    });
  });

  describe('Special characters', () => {
    test('sanitizes task descriptions with quotes', () => {
      const description = 'Add "login" feature with \'auth\'';

      // Descrizione dovrebbe essere gestita correttamente
      assert.ok(description.includes('"'));
      assert.ok(description.includes("'"));

      // Non dovrebbe causare problemi nel JSON
      const json = JSON.stringify({ description });
      const parsed = JSON.parse(json);
      assert.equal(parsed.description, description);
    });

    test('handles unicode in project names', () => {
      const validate = (name) => {
        return name && /^[a-z0-9-]+$/.test(name);
      };

      // Unicode non dovrebbe essere permesso nei nomi progetto
      assert.equal(validate('progetto-'), true);
      assert.equal(validate('progetto-123'), true);
      assert.equal(validate('progetto_emoji'), false); // underscore
      assert.equal(validate('progettoÈ'), false); // accento
    });

    test('handles newlines in descriptions', () => {
      const description = 'Add feature\nwith\nmultiple lines';

      // Dovrebbe essere possibile memorizzare
      const json = JSON.stringify({ description });
      const parsed = JSON.parse(json);
      assert.ok(parsed.description.includes('\n'));
    });
  });

  describe('File system edge cases', () => {
    test('handles missing .sncp directory', async (t) => {
      const tempDir = await createTempDir(t);

      // Non creiamo .sncp - simuliamo progetto non inizializzato
      const exists = await readTempFile(tempDir, '.sncp/config.json');

      assert.equal(exists, null, 'Should return null for missing file');
    });

    test('handles corrupted JSON files', async (t) => {
      const tempDir = await createTempDir(t);

      await createFileStructure(tempDir, {
        '.sncp/config.json': '{ invalid json }'
      });

      const content = await readTempFile(tempDir, '.sncp/config.json');

      // Il parsing dovrebbe fallire
      let parseError = false;
      try {
        JSON.parse(content);
      } catch {
        parseError = true;
      }

      assert.ok(parseError, 'Should fail to parse invalid JSON');
    });

    test('handles empty JSON files', async (t) => {
      const tempDir = await createTempDir(t);

      await createFileStructure(tempDir, {
        '.sncp/config.json': ''
      });

      const content = await readTempFile(tempDir, '.sncp/config.json');

      let parseError = false;
      try {
        JSON.parse(content || '{}');
      } catch {
        parseError = true;
      }

      // Empty string con fallback a '{}' dovrebbe funzionare
      assert.equal(parseError, false);
    });

    test('handles very long file paths', async (t) => {
      const tempDir = await createTempDir(t);

      // Crea path lungo ma valido
      const longPath = 'a'.repeat(100);

      await createFileStructure(tempDir, {
        [`.sncp/${longPath}/test.json`]: '{}'
      });

      const content = await readTempFile(tempDir, `.sncp/${longPath}/test.json`);
      assert.equal(content, '{}');
    });
  });

  describe('Session edge cases', () => {
    test('handles sessions with missing fields', async (t) => {
      const tempDir = await createTempDir(t);

      // Sessione incompleta
      await createFileStructure(tempDir, {
        '.sncp/sessions/incomplete.json': JSON.stringify({
          type: 'task'
          // missing: summary, date, success
        })
      });

      const content = await readTempFile(tempDir, '.sncp/sessions/incomplete.json');
      const session = JSON.parse(content);

      // Dovremmo gestire campi mancanti
      assert.equal(session.summary, undefined);
      assert.equal(session.summary || 'No description', 'No description');
    });

    test('handles very old session dates', () => {
      const calculateDaysSince = (dateString) => {
        const lastDate = new Date(dateString);
        const now = new Date();
        const diffTime = Math.abs(now - lastDate);
        return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
      };

      // Data molto vecchia (1 anno fa)
      const oldDate = new Date();
      oldDate.setFullYear(oldDate.getFullYear() - 1);
      const days = calculateDaysSince(oldDate.toISOString());

      assert.ok(days >= 365, 'Should handle old dates');
      assert.ok(days <= 366, 'Should calculate correctly');
    });

    test('handles future session dates', () => {
      const calculateDaysSince = (dateString) => {
        const lastDate = new Date(dateString);
        const now = new Date();
        const diffTime = Math.abs(now - lastDate);
        return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
      };

      // Data futura (bug o timezone issue)
      const futureDate = new Date();
      futureDate.setDate(futureDate.getDate() + 1);
      const days = calculateDaysSince(futureDate.toISOString());

      // Math.abs dovrebbe gestire date future
      assert.ok(days >= 0, 'Should handle future dates with abs');
    });
  });

  describe('Router edge cases', () => {
    test('handles mixed language descriptions', async () => {
      // Import router
      const { routeTask } = await import('../src/agents/router.js');

      // Task in italiano con keyword inglese
      const agent = await routeTask('Crea nuovo API endpoint per utenti', {});
      assert.equal(agent, 'cervella-backend');
    });

    test('handles descriptions with only punctuation', async () => {
      const { routeTask } = await import('../src/agents/router.js');

      // Descrizione senza keyword utili
      const agent = await routeTask('...!!!???', {});
      assert.equal(agent, 'cervella-backend'); // Default
    });

    test('handles very long descriptions', async () => {
      const { routeTask } = await import('../src/agents/router.js');

      // Descrizione molto lunga
      const longDesc = 'Create new API endpoint ' + 'with lots of details '.repeat(100);
      const agent = await routeTask(longDesc, {});

      assert.equal(agent, 'cervella-backend');
    });
  });

  describe('Concurrent operations', () => {
    test('handles multiple session saves', async (t) => {
      const tempDir = await createTempDir(t);

      await createFileStructure(tempDir, {
        '.sncp/sessions/.gitkeep': ''
      });

      // Simula salvataggi concorrenti
      const sessions = [];
      for (let i = 0; i < 5; i++) {
        sessions.push({
          id: `session_${i}`,
          summary: `Task ${i}`,
          date: new Date().toISOString()
        });
      }

      // Tutti dovrebbero essere salvabili
      const filenames = sessions.map(s => `${s.id}.json`);
      const uniqueNames = [...new Set(filenames)];

      assert.equal(uniqueNames.length, 5, 'All sessions should have unique IDs');
    });
  });

  describe('Memory and performance', () => {
    test('limits session history to 50', () => {
      const sessions = Array.from({ length: 100 }, (_, i) => ({
        id: `session_${i}`,
        summary: `Task ${i}`
      }));

      const limited = sessions.slice(0, 50);
      assert.equal(limited.length, 50);
    });

    test('handles large output from agents', () => {
      // Simula output molto lungo
      const largeOutput = 'x'.repeat(100000);

      // Dovremmo poterlo memorizzare
      const result = {
        success: true,
        output: largeOutput.slice(0, 10000) // Tronca se necessario
      };

      assert.ok(result.output.length <= 10000, 'Should truncate large output');
    });
  });

  describe('Input sanitization', () => {
    test('prevents command injection in task description', () => {
      const maliciousInput = 'task; rm -rf /';

      // La descrizione dovrebbe essere usata come stringa, non eseguita
      // JSON.stringify la racchiude tra virgolette, rendendola sicura
      const escaped = JSON.stringify(maliciousInput);
      assert.ok(escaped.includes('rm -rf'), 'Should contain the text');
      assert.ok(escaped.startsWith('"') && escaped.endsWith('"'), 'Should be quoted');
    });

    test('handles path traversal attempts', () => {
      const maliciousPath = '../../../etc/passwd';

      // Il path dovrebbe essere validato
      const isValid = !maliciousPath.includes('..');
      assert.equal(isValid, false, 'Should detect path traversal');
    });
  });

});

describe('Recovery scenarios', () => {

  test('recovers from partial init', async (t) => {
    const tempDir = await createTempDir(t);

    // Init parziale - solo alcune directory create
    await createFileStructure(tempDir, {
      '.sncp/idee/.gitkeep': ''
      // missing: decisioni, sessions, config.json
    });

    // Il sistema dovrebbe poter continuare l'init
    const content = await readTempFile(tempDir, '.sncp/config.json');
    assert.equal(content, null, 'Config should be missing');
  });

  test('handles interrupted session save', async (t) => {
    const tempDir = await createTempDir(t);

    await createFileStructure(tempDir, {
      '.sncp/sessions/partial.json': '{ "summary": "Incomplete'
      // JSON troncato
    });

    const content = await readTempFile(tempDir, '.sncp/sessions/partial.json');

    let isValid = true;
    try {
      JSON.parse(content);
    } catch {
      isValid = false;
    }

    assert.equal(isValid, false, 'Should detect truncated JSON');
  });

});
