/**
 * SNCP Writer Tests - Phase 2
 *
 * Tests for sncp/writer.js: saveTaskReport, saveSession, appendToDailyLog.
 * Uses real temp dirs + mocked process.cwd + mocked findSncpDir.
 *
 * "Se non e testato, non funziona."
 */

import { describe, it, mock } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import fsPromises from 'node:fs/promises';
import path from 'node:path';
import { createTempDir, createFileStructure, readTempFile } from '../helpers/temp-dir.js';

describe('SNCP Writer - saveTaskReport', () => {

  it('creates report file with correct JSON structure', async (t) => {
    const tempDir = await createTempDir(t);
    const sncpDir = path.join(tempDir, '.sncp');
    await createFileStructure(tempDir, { '.sncp/.gitkeep': '' });

    t.mock.method(process, 'cwd', () => tempDir);

    // Import with cache-busting to get fresh module
    const writerMod = await import(`../../src/sncp/writer.js?t=${Date.now()}_w1`);

    const result = await writerMod.saveTaskReport(
      'Implement login feature',
      'cervella-backend',
      { success: true, duration: '30s', filesModified: ['src/auth.js'] }
    );

    assert.ok(result, 'Should return filepath');
    assert.ok(result.endsWith('.json'), 'Should be a JSON file');

    // Read and verify
    const content = fs.readFileSync(result, 'utf-8');
    const report = JSON.parse(content);

    assert.equal(report.description, 'Implement login feature');
    assert.equal(report.agent, 'cervella-backend');
    assert.equal(report.result.success, true);
    assert.equal(report.result.duration, '30s');
    assert.deepEqual(report.result.filesModified, ['src/auth.js']);
    assert.ok(report.timestamp, 'Should have ISO timestamp');

    process.cwd = process.cwd;
  });

  it('creates reports/tasks/ directory if missing', async (t) => {
    const tempDir = await createTempDir(t);
    // Only .sncp exists, no reports/tasks/
    await createFileStructure(tempDir, { '.sncp/.gitkeep': '' });

    t.mock.method(process, 'cwd', () => tempDir);

    const writerMod = await import(`../../src/sncp/writer.js?t=${Date.now()}_w2`);
    const result = await writerMod.saveTaskReport(
      'Test task',
      'cervella-tester',
      { success: true }
    );

    assert.ok(result, 'Should succeed');
    const reportsDir = path.join(tempDir, '.sncp', 'reports', 'tasks');
    assert.ok(fs.existsSync(reportsDir), 'Should create reports/tasks dir');
  });

  it('filename contains agent short name (without cervella- prefix)', async (t) => {
    const tempDir = await createTempDir(t);
    await createFileStructure(tempDir, { '.sncp/.gitkeep': '' });

    t.mock.method(process, 'cwd', () => tempDir);

    const writerMod = await import(`../../src/sncp/writer.js?t=${Date.now()}_w3`);
    const result = await writerMod.saveTaskReport(
      'A task',
      'cervella-frontend',
      { success: true }
    );

    const filename = path.basename(result);
    assert.ok(filename.startsWith('task_'), 'Should start with task_');
    assert.ok(filename.includes('frontend'), 'Should include agent short name');
    assert.ok(!filename.includes('cervella-'), 'Should strip cervella- prefix');
  });

  it('trims description whitespace', async (t) => {
    const tempDir = await createTempDir(t);
    await createFileStructure(tempDir, { '.sncp/.gitkeep': '' });

    t.mock.method(process, 'cwd', () => tempDir);

    const writerMod = await import(`../../src/sncp/writer.js?t=${Date.now()}_w4`);
    const result = await writerMod.saveTaskReport(
      '  padded description  ',
      'cervella-backend',
      { success: true }
    );

    const content = JSON.parse(fs.readFileSync(result, 'utf-8'));
    assert.equal(content.description, 'padded description', 'Should trim whitespace');
  });

  it('truncates output to 5000 chars max', async (t) => {
    const tempDir = await createTempDir(t);
    await createFileStructure(tempDir, { '.sncp/.gitkeep': '' });

    t.mock.method(process, 'cwd', () => tempDir);

    const writerMod = await import(`../../src/sncp/writer.js?t=${Date.now()}_w5`);
    const longOutput = 'x'.repeat(10000);
    const result = await writerMod.saveTaskReport(
      'Big output task',
      'cervella-backend',
      { success: true, output: longOutput }
    );

    const content = JSON.parse(fs.readFileSync(result, 'utf-8'));
    assert.equal(content.output.length, 5000, 'Output should be truncated to 5000');
  });

  it('handles null output gracefully', async (t) => {
    const tempDir = await createTempDir(t);
    await createFileStructure(tempDir, { '.sncp/.gitkeep': '' });

    t.mock.method(process, 'cwd', () => tempDir);

    const writerMod = await import(`../../src/sncp/writer.js?t=${Date.now()}_w6`);
    const result = await writerMod.saveTaskReport(
      'No output task',
      'cervella-backend',
      { success: false, error: 'Something broke' }
    );

    const content = JSON.parse(fs.readFileSync(result, 'utf-8'));
    assert.equal(content.output, null, 'Output should be null');
    assert.equal(content.result.error, 'Something broke');
  });

  it('returns null on write failure (graceful degradation)', async (t) => {
    const tempDir = await createTempDir(t);
    // Don't create .sncp -- findSncpDir will return a path but mkdirSync could fail
    // Actually, mkdirSync recursive creates it. Let's use a read-only approach.
    // We'll mock cwd to a non-writable location
    t.mock.method(process, 'cwd', () => '/nonexistent/path/that/does/not/exist');

    const writerMod = await import(`../../src/sncp/writer.js?t=${Date.now()}_w7`);
    const result = await writerMod.saveTaskReport(
      'Will fail',
      'cervella-backend',
      { success: true }
    );

    assert.equal(result, null, 'Should return null on failure');
  });

});

describe('SNCP Writer - saveSession', () => {

  it('creates session file with correct data', async (t) => {
    const tempDir = await createTempDir(t);
    await createFileStructure(tempDir, { '.sncp/.gitkeep': '' });

    t.mock.method(process, 'cwd', () => tempDir);

    const writerMod = await import(`../../src/sncp/writer.js?t=${Date.now()}_ws1`);
    const sessionData = {
      type: 'task',
      summary: 'Build feature X',
      agent: 'cervella-backend',
      success: true
    };

    const result = await writerMod.saveSession(sessionData);

    assert.ok(result, 'Should return filepath');
    assert.ok(result.includes('sessions'), 'Path should include sessions dir');

    const content = JSON.parse(fs.readFileSync(result, 'utf-8'));
    assert.equal(content.type, 'task');
    assert.equal(content.summary, 'Build feature X');
  });

  it('creates sessions/ directory if missing', async (t) => {
    const tempDir = await createTempDir(t);
    await createFileStructure(tempDir, { '.sncp/.gitkeep': '' });

    t.mock.method(process, 'cwd', () => tempDir);

    const writerMod = await import(`../../src/sncp/writer.js?t=${Date.now()}_ws2`);
    await writerMod.saveSession({ type: 'test' });

    const sessionsDir = path.join(tempDir, '.sncp', 'sessions');
    assert.ok(fs.existsSync(sessionsDir), 'Should create sessions dir');
  });

  it('filename starts with session_ and ends with .json', async (t) => {
    const tempDir = await createTempDir(t);
    await createFileStructure(tempDir, { '.sncp/.gitkeep': '' });

    t.mock.method(process, 'cwd', () => tempDir);

    const writerMod = await import(`../../src/sncp/writer.js?t=${Date.now()}_ws3`);
    const result = await writerMod.saveSession({ type: 'task' });

    const filename = path.basename(result);
    assert.ok(filename.startsWith('session_'), `Should start with session_: ${filename}`);
    assert.ok(filename.endsWith('.json'), `Should end with .json: ${filename}`);
  });

  it('returns null on write failure', async (t) => {
    t.mock.method(process, 'cwd', () => '/nonexistent/path');

    const writerMod = await import(`../../src/sncp/writer.js?t=${Date.now()}_ws4`);
    const result = await writerMod.saveSession({ type: 'test' });

    assert.equal(result, null, 'Should return null on failure');
  });

});

describe('SNCP Writer - appendToDailyLog', () => {

  it('creates log file with correct format', async (t) => {
    const tempDir = await createTempDir(t);
    await createFileStructure(tempDir, { '.sncp/.gitkeep': '' });

    t.mock.method(process, 'cwd', () => tempDir);

    const writerMod = await import(`../../src/sncp/writer.js?t=${Date.now()}_wl1`);
    await writerMod.appendToDailyLog('Test message', 'info');

    // Find the log file
    const logsDir = path.join(tempDir, '.sncp', 'logs');
    assert.ok(fs.existsSync(logsDir), 'Should create logs dir');

    const logFiles = fs.readdirSync(logsDir).filter(f => f.startsWith('daily_'));
    assert.equal(logFiles.length, 1, 'Should create one daily log');

    const content = fs.readFileSync(path.join(logsDir, logFiles[0]), 'utf-8');
    assert.ok(content.includes('[INFO]'), 'Should contain INFO type');
    assert.ok(content.includes('Test message'), 'Should contain message');
  });

  it('appends multiple messages to same daily log', async (t) => {
    const tempDir = await createTempDir(t);
    await createFileStructure(tempDir, { '.sncp/.gitkeep': '' });

    t.mock.method(process, 'cwd', () => tempDir);

    const writerMod = await import(`../../src/sncp/writer.js?t=${Date.now()}_wl2`);
    await writerMod.appendToDailyLog('First message', 'info');
    await writerMod.appendToDailyLog('Second message', 'warn');

    const logsDir = path.join(tempDir, '.sncp', 'logs');
    const logFiles = fs.readdirSync(logsDir).filter(f => f.startsWith('daily_'));
    const content = fs.readFileSync(path.join(logsDir, logFiles[0]), 'utf-8');

    const lines = content.trim().split('\n');
    assert.equal(lines.length, 2, 'Should have 2 log lines');
    assert.ok(lines[0].includes('First message'));
    assert.ok(lines[1].includes('[WARN]'), 'Second line should be WARN');
    assert.ok(lines[1].includes('Second message'));
  });

  it('defaults type to info when not specified', async (t) => {
    const tempDir = await createTempDir(t);
    await createFileStructure(tempDir, { '.sncp/.gitkeep': '' });

    t.mock.method(process, 'cwd', () => tempDir);

    const writerMod = await import(`../../src/sncp/writer.js?t=${Date.now()}_wl3`);
    await writerMod.appendToDailyLog('Default type message');

    const logsDir = path.join(tempDir, '.sncp', 'logs');
    const logFiles = fs.readdirSync(logsDir).filter(f => f.startsWith('daily_'));
    const content = fs.readFileSync(path.join(logsDir, logFiles[0]), 'utf-8');

    assert.ok(content.includes('[INFO]'), 'Should default to INFO');
  });

  it('silently fails on write error (no throw)', async (t) => {
    t.mock.method(process, 'cwd', () => '/nonexistent/path');

    const writerMod = await import(`../../src/sncp/writer.js?t=${Date.now()}_wl4`);

    // Should not throw
    await assert.doesNotReject(
      () => writerMod.appendToDailyLog('Will fail silently', 'error'),
      'Should not throw on failure'
    );
  });

});
