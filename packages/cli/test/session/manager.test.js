/**
 * Session Manager Tests
 *
 * Test per session/manager.js
 * Verifica: save, load, create, format sessions
 *
 * "Un progresso al giorno = 365 progressi all'anno."
 */

import { test, describe } from 'node:test';
import assert from 'node:assert/strict';
import { createTempDir, createFileStructure, readTempFile } from '../helpers/temp-dir.js';
import fs from 'node:fs/promises';
import path from 'node:path';

// Nota: Importiamo le funzioni da testare.
// Per testare con directory diverse, mocchiamo process.cwd()

describe('Session Manager', () => {

  test('saveSession - creates session file with correct structure', async (t) => {
    const tempDir = await createTempDir(t);

    // Crea struttura .sncp/sessions
    await createFileStructure(tempDir, {
      '.sncp/sessions/.gitkeep': ''
    });

    // Mock process.cwd per usare tempDir
    const originalCwd = process.cwd;
    t.mock.method(process, 'cwd', () => tempDir);

    // Import DOPO mock
    const { saveSession } = await import('../../src/session/manager.js');

    // Salva sessione
    const session = await saveSession({
      type: 'task',
      summary: 'Test task',
      agent: 'cervella-backend',
      success: true
    });

    // Verifica sessione salvata
    assert.ok(session, 'Session should be returned');
    assert.ok(session.id, 'Session should have ID');
    assert.ok(session.id.startsWith('session_'), 'ID should start with session_');
    assert.equal(session.type, 'task');
    assert.equal(session.summary, 'Test task');
    assert.equal(session.agent, 'cervella-backend');
    assert.equal(session.success, true);
    assert.ok(session.date, 'Session should have date');

    // Verifica file creato
    const sessionsDir = path.join(tempDir, '.sncp', 'sessions');
    const files = await fs.readdir(sessionsDir);
    const sessionFiles = files.filter(f => f.endsWith('.json'));
    assert.equal(sessionFiles.length, 1, 'Should create one session file');

    // Verifica contenuto file
    const fileContent = await readTempFile(tempDir, `.sncp/sessions/${sessionFiles[0]}`);
    const parsed = JSON.parse(fileContent);
    assert.equal(parsed.summary, 'Test task');

    // Restore
    process.cwd = originalCwd;
  });

  test('loadSessions - returns empty array when no sessions', async (t) => {
    const tempDir = await createTempDir(t);

    // Crea struttura vuota
    await createFileStructure(tempDir, {
      '.sncp/sessions/.gitkeep': ''
    });

    const originalCwd = process.cwd;
    t.mock.method(process, 'cwd', () => tempDir);

    // Reimport per usare nuovo mock
    const managerPath = '../../src/session/manager.js';
    // Clear cache per forzare reimport con nuovo cwd
    delete (await import(managerPath)).default;

    const { loadSessions } = await import(managerPath);
    const sessions = await loadSessions();

    assert.ok(Array.isArray(sessions), 'Should return array');
    assert.equal(sessions.length, 0, 'Should be empty');

    process.cwd = originalCwd;
  });

  test('loadSessions - returns sessions sorted by date (newest first)', async (t) => {
    const tempDir = await createTempDir(t);

    // Crea sessioni con date diverse
    await createFileStructure(tempDir, {
      '.sncp/sessions/session_20260114_1000.json': JSON.stringify({
        type: 'task',
        summary: 'First task',
        date: '2026-01-14T10:00:00Z'
      }),
      '.sncp/sessions/session_20260115_1200.json': JSON.stringify({
        type: 'task',
        summary: 'Second task',
        date: '2026-01-15T12:00:00Z'
      }),
      '.sncp/sessions/session_20260115_0800.json': JSON.stringify({
        type: 'task',
        summary: 'Third task',
        date: '2026-01-15T08:00:00Z'
      })
    });

    const originalCwd = process.cwd;
    t.mock.method(process, 'cwd', () => tempDir);

    const { loadSessions } = await import('../../src/session/manager.js');
    const sessions = await loadSessions();

    assert.equal(sessions.length, 3, 'Should load all sessions');
    // Verifico che sia ordinato per filename (che contiene timestamp)
    assert.equal(sessions[0].summary, 'Second task', 'Newest should be first');

    process.cwd = originalCwd;
  });

  test('getLastSession - returns most recent session', async (t) => {
    const tempDir = await createTempDir(t);

    await createFileStructure(tempDir, {
      '.sncp/sessions/session_20260114_1000.json': JSON.stringify({
        type: 'task',
        summary: 'Old task',
        date: '2026-01-14T10:00:00Z'
      }),
      '.sncp/sessions/session_20260115_1500.json': JSON.stringify({
        type: 'task',
        summary: 'Latest task',
        date: '2026-01-15T15:00:00Z'
      })
    });

    const originalCwd = process.cwd;
    t.mock.method(process, 'cwd', () => tempDir);

    const { getLastSession } = await import('../../src/session/manager.js');
    const last = await getLastSession();

    assert.ok(last, 'Should return a session');
    assert.equal(last.summary, 'Latest task', 'Should be the most recent');

    process.cwd = originalCwd;
  });

  test('getLastSession - returns null when no sessions', async (t) => {
    const tempDir = await createTempDir(t);

    await createFileStructure(tempDir, {
      '.sncp/sessions/.gitkeep': ''
    });

    const originalCwd = process.cwd;
    t.mock.method(process, 'cwd', () => tempDir);

    const { getLastSession } = await import('../../src/session/manager.js');
    const last = await getLastSession();

    assert.equal(last, null, 'Should return null');

    process.cwd = originalCwd;
  });

  test('loadSession - loads by exact ID', async (t) => {
    const tempDir = await createTempDir(t);

    await createFileStructure(tempDir, {
      '.sncp/sessions/session_20260115_1000.json': JSON.stringify({
        type: 'task',
        summary: 'Target task',
        date: '2026-01-15T10:00:00Z'
      })
    });

    const originalCwd = process.cwd;
    t.mock.method(process, 'cwd', () => tempDir);

    const { loadSession } = await import('../../src/session/manager.js');
    const session = await loadSession('session_20260115_1000');

    assert.ok(session, 'Should find session');
    assert.equal(session.summary, 'Target task');

    process.cwd = originalCwd;
  });

  test('loadSession - finds by partial ID', async (t) => {
    const tempDir = await createTempDir(t);

    await createFileStructure(tempDir, {
      '.sncp/sessions/session_20260115_1234.json': JSON.stringify({
        type: 'task',
        summary: 'Partial match',
        date: '2026-01-15T12:34:00Z'
      })
    });

    const originalCwd = process.cwd;
    t.mock.method(process, 'cwd', () => tempDir);

    const { loadSession } = await import('../../src/session/manager.js');
    const session = await loadSession('1234');

    assert.ok(session, 'Should find by partial ID');
    assert.equal(session.summary, 'Partial match');

    process.cwd = originalCwd;
  });

  test('loadSession - returns null for non-existent ID', async (t) => {
    const tempDir = await createTempDir(t);

    await createFileStructure(tempDir, {
      '.sncp/sessions/.gitkeep': ''
    });

    const originalCwd = process.cwd;
    t.mock.method(process, 'cwd', () => tempDir);

    const { loadSession } = await import('../../src/session/manager.js');
    const session = await loadSession('nonexistent');

    assert.equal(session, null, 'Should return null');

    process.cwd = originalCwd;
  });

  test('createTaskSession - creates session from task result', async (t) => {
    const tempDir = await createTempDir(t);

    await createFileStructure(tempDir, {
      '.sncp/sessions/.gitkeep': ''
    });

    const originalCwd = process.cwd;
    t.mock.method(process, 'cwd', () => tempDir);

    const { createTaskSession } = await import('../../src/session/manager.js');

    const session = await createTaskSession(
      'Add authentication feature',
      'cervella-backend',
      {
        success: true,
        duration: '45s',
        filesModified: ['src/auth.js', 'src/middleware.js'],
        nextStep: 'Write tests'
      }
    );

    assert.ok(session, 'Should create session');
    assert.equal(session.type, 'task');
    assert.equal(session.summary, 'Add authentication feature');
    assert.equal(session.agent, 'cervella-backend');
    assert.equal(session.success, true);
    assert.equal(session.duration, '45s');
    assert.deepEqual(session.filesModified, ['src/auth.js', 'src/middleware.js']);
    assert.equal(session.nextStep, 'Write tests');

    process.cwd = originalCwd;
  });

  test('formatSessionSummary - formats session for display', async (t) => {
    const { formatSessionSummary } = await import('../../src/session/manager.js');

    const session = {
      date: '2026-01-15T14:30:00Z',
      success: true,
      summary: 'Add login page'
    };

    const formatted = formatSessionSummary(session);

    assert.ok(formatted.includes('[OK]'), 'Should include status');
    assert.ok(formatted.includes('Add login page'), 'Should include summary');
    // Data in formato italiano
    assert.ok(formatted.includes('gen') || formatted.includes('15'), 'Should include date');
  });

  test('formatSessionSummary - shows ERR for failed sessions', async (t) => {
    const { formatSessionSummary } = await import('../../src/session/manager.js');

    const session = {
      date: '2026-01-15T14:30:00Z',
      success: false,
      summary: 'Failed task'
    };

    const formatted = formatSessionSummary(session);

    assert.ok(formatted.includes('[ERR]'), 'Should show ERR for failure');
  });

});
