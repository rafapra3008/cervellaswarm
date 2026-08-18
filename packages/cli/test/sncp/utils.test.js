/**
 * SNCP Utils Tests - Phase 2
 *
 * Tests for sncp/utils.js: findSncpDir() directory discovery.
 * Uses real temp dirs (mock FS via temp filesystem).
 *
 * "Edge cases: dove si nascondono i mostri."
 */

import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { createTempDir, createFileStructure } from '../helpers/temp-dir.js';

describe('SNCP Utils - findSncpDir', () => {

  it('finds .sncp in current directory', async (t) => {
    const tempDir = await createTempDir(t);
    await createFileStructure(tempDir, {
      '.sncp/.gitkeep': ''
    });

    const originalCwd = process.cwd;
    t.mock.method(process, 'cwd', () => tempDir);

    // Dynamic import to pick up mocked cwd
    const { findSncpDir } = await import(`../../src/sncp/utils.js?t=${Date.now()}_1`);
    const result = findSncpDir();

    assert.ok(result.endsWith('.sncp'), `Should end with .sncp, got: ${result}`);
    assert.ok(result.startsWith(tempDir), `Should be inside tempDir, got: ${result}`);

    process.cwd = originalCwd;
  });

  it('finds .sncp in parent directory (1 level up)', async (t) => {
    const tempDir = await createTempDir(t);
    await createFileStructure(tempDir, {
      '.sncp/.gitkeep': '',
      'subdir/.gitkeep': ''
    });

    const subDir = `${tempDir}/subdir`;
    const originalCwd = process.cwd;
    t.mock.method(process, 'cwd', () => subDir);

    const { findSncpDir } = await import(`../../src/sncp/utils.js?t=${Date.now()}_2`);
    const result = findSncpDir();

    assert.ok(result.startsWith(tempDir), 'Should find .sncp in parent');
    assert.ok(result.endsWith('.sncp'));
    // Should NOT be subdir/.sncp
    assert.ok(!result.includes('subdir'), 'Should be parent .sncp, not subdir');

    process.cwd = originalCwd;
  });

  it('finds .sncp 3 levels up', async (t) => {
    const tempDir = await createTempDir(t);
    await createFileStructure(tempDir, {
      '.sncp/.gitkeep': '',
      'a/b/c/.gitkeep': ''
    });

    const deepDir = `${tempDir}/a/b/c`;
    const originalCwd = process.cwd;
    t.mock.method(process, 'cwd', () => deepDir);

    const { findSncpDir } = await import(`../../src/sncp/utils.js?t=${Date.now()}_3`);
    const result = findSncpDir();

    assert.ok(result.startsWith(tempDir));
    assert.ok(result.endsWith('.sncp'));

    process.cwd = originalCwd;
  });

  it('returns cwd/.sncp fallback when no .sncp found (within 5 levels)', async (t) => {
    const tempDir = await createTempDir(t);
    // No .sncp anywhere
    await createFileStructure(tempDir, {
      'deep/nested/.gitkeep': ''
    });

    const deepDir = `${tempDir}/deep/nested`;
    const originalCwd = process.cwd;
    t.mock.method(process, 'cwd', () => deepDir);

    const { findSncpDir } = await import(`../../src/sncp/utils.js?t=${Date.now()}_4`);
    const result = findSncpDir();

    // Fallback: join(process.cwd(), '.sncp')
    assert.equal(result, `${deepDir}/.sncp`, 'Should fallback to cwd/.sncp');

    process.cwd = originalCwd;
  });

  it('stops at max 5 levels (does not go higher)', async (t) => {
    const tempDir = await createTempDir(t);
    // .sncp is 6 levels up -- too far
    await createFileStructure(tempDir, {
      '.sncp/.gitkeep': '',
      'a/b/c/d/e/f/.gitkeep': ''
    });

    const deepDir = `${tempDir}/a/b/c/d/e/f`;
    const originalCwd = process.cwd;
    t.mock.method(process, 'cwd', () => deepDir);

    const { findSncpDir } = await import(`../../src/sncp/utils.js?t=${Date.now()}_5`);
    const result = findSncpDir();

    // Should fallback because .sncp is 6 levels up (loop runs 0..4 = 5 checks)
    assert.equal(result, `${deepDir}/.sncp`, 'Should fallback -- .sncp too far');

    process.cwd = originalCwd;
  });

  it('prefers closest .sncp when multiple exist', async (t) => {
    const tempDir = await createTempDir(t);
    await createFileStructure(tempDir, {
      '.sncp/root-marker': 'root',
      'project/.sncp/project-marker': 'project',
      'project/src/.gitkeep': ''
    });

    const srcDir = `${tempDir}/project/src`;
    const originalCwd = process.cwd;
    t.mock.method(process, 'cwd', () => srcDir);

    const { findSncpDir } = await import(`../../src/sncp/utils.js?t=${Date.now()}_6`);
    const result = findSncpDir();

    // Should find project/.sncp first (1 level up), not root/.sncp (2 levels up)
    assert.ok(result.includes('project'), 'Should find closest .sncp');

    process.cwd = originalCwd;
  });

});
