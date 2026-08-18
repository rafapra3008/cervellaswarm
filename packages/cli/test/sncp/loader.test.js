/**
 * SNCP Loader Tests - Phase 2
 *
 * Tests for sncp/loader.js: loadProjectContext() with mock FS.
 * Uses real temp dirs with fixture .sncp structures.
 *
 * "Se non e testato, non funziona."
 */

import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import path from 'node:path';
import { createTempDir, createFileStructure } from '../helpers/temp-dir.js';

describe('SNCP Loader - loadProjectContext', () => {

  it('returns null when .sncp/progetti does not exist', async (t) => {
    const tempDir = await createTempDir(t);
    // No .sncp at all

    const originalCwd = process.cwd;
    t.mock.method(process, 'cwd', () => tempDir);

    const { loadProjectContext } = await import(`../../src/sncp/loader.js?t=${Date.now()}_l1`);
    const result = await loadProjectContext();

    assert.equal(result, null, 'Should return null without .sncp/progetti');

    process.cwd = originalCwd;
  });

  it('returns null when .sncp exists but progetti/ is empty', async (t) => {
    const tempDir = await createTempDir(t);
    await createFileStructure(tempDir, {
      '.sncp/progetti/.gitkeep': ''
    });
    // .gitkeep is a file, not a dir -- readdir will return ['.gitkeep']
    // Actually the code checks projects.length === 0, but .gitkeep counts.
    // Let's use an actually empty directory.

    const originalCwd = process.cwd;
    t.mock.method(process, 'cwd', () => tempDir);

    // We need progetti/ to exist but be truly empty
    const fs = await import('node:fs/promises');
    const gitkeepPath = path.join(tempDir, '.sncp', 'progetti', '.gitkeep');
    await fs.unlink(gitkeepPath);

    const { loadProjectContext } = await import(`../../src/sncp/loader.js?t=${Date.now()}_l2`);
    const result = await loadProjectContext();

    assert.equal(result, null, 'Should return null when progetti/ is empty');

    process.cwd = originalCwd;
  });

  it('loads context with project.json', async (t) => {
    const tempDir = await createTempDir(t);
    const projectJson = JSON.stringify({
      projectName: 'myproject',
      description: 'A test project',
      mainGoal: 'Test everything',
      projectType: 'cli',
      techStack: 'node',
      timeline: '2 weeks'
    });
    await createFileStructure(tempDir, {
      '.sncp/progetti/myproject/project.json': projectJson
    });

    const originalCwd = process.cwd;
    t.mock.method(process, 'cwd', () => tempDir);

    const { loadProjectContext } = await import(`../../src/sncp/loader.js?t=${Date.now()}_l3`);
    const result = await loadProjectContext();

    assert.ok(result, 'Should return context');
    assert.equal(result.name, 'myproject');
    assert.equal(result.description, 'A test project');
    assert.equal(result.goal, 'Test everything');
    assert.equal(result.projectType, 'cli');
    assert.equal(result.techStack, 'node');
    assert.equal(result.timeline, '2 weeks');

    process.cwd = originalCwd;
  });

  it('falls back gracefully when project.json is missing', async (t) => {
    const tempDir = await createTempDir(t);
    await createFileStructure(tempDir, {
      '.sncp/progetti/testproj/.gitkeep': ''
    });

    const originalCwd = process.cwd;
    t.mock.method(process, 'cwd', () => tempDir);

    const { loadProjectContext } = await import(`../../src/sncp/loader.js?t=${Date.now()}_l4`);
    const result = await loadProjectContext();

    assert.ok(result, 'Should return context even without project.json');
    assert.equal(result.name, 'testproj', 'Should infer name from folder');
    assert.equal(result.description, 'A CervellaSwarm project', 'Should use default description');
    assert.equal(result.projectType, 'unknown');

    process.cwd = originalCwd;
  });

  it('prefers CWD name match for project selection', async (t) => {
    // Simulate: cwd is named "cervellaswarm", progetti has both "alpha" and "cervellaswarm"
    const tempDir = await createTempDir(t, 'cervellaswarm-');
    // We need CWD basename to match a project folder
    // createTempDir appends random chars so we nest a known-name dir
    const projectDir = path.join(tempDir, 'cervellaswarm');
    const fsMod = await import('node:fs/promises');
    await fsMod.mkdir(projectDir);

    await createFileStructure(projectDir, {
      '.sncp/progetti/alpha/project.json': JSON.stringify({ projectName: 'alpha' }),
      '.sncp/progetti/cervellaswarm/project.json': JSON.stringify({ projectName: 'cervellaswarm', description: 'The swarm' })
    });

    const originalCwd = process.cwd;
    t.mock.method(process, 'cwd', () => projectDir);

    const { loadProjectContext } = await import(`../../src/sncp/loader.js?t=${Date.now()}_l5`);
    const result = await loadProjectContext();

    assert.ok(result, 'Should return context');
    assert.equal(result.name, 'cervellaswarm', 'Should prefer CWD name match');

    process.cwd = originalCwd;
  });

  it('extracts nextStep from PROMPT_RIPRESA', async (t) => {
    const tempDir = await createTempDir(t);
    const promptRipresa = `# PROMPT RIPRESA - myproject

## PROSSIMI STEPS

- Deploy v2.0 to production
- Update documentation
`;
    await createFileStructure(tempDir, {
      '.sncp/progetti/myproject/project.json': JSON.stringify({ projectName: 'myproject' }),
      '.sncp/progetti/myproject/PROMPT_RIPRESA_myproject.md': promptRipresa
    });

    const originalCwd = process.cwd;
    t.mock.method(process, 'cwd', () => tempDir);

    const { loadProjectContext } = await import(`../../src/sncp/loader.js?t=${Date.now()}_l6`);
    const result = await loadProjectContext();

    assert.ok(result, 'Should return context');
    assert.ok(result.nextStep.includes('Deploy v2.0'), `Should extract next step, got: ${result.nextStep}`);

    process.cwd = originalCwd;
  });

  it('extracts lastSession date from PROMPT_RIPRESA', async (t) => {
    const tempDir = await createTempDir(t);
    const promptRipresa = `# PROMPT RIPRESA

**Ultimo aggiornamento:** 2026-04-01

Some content here.
`;
    await createFileStructure(tempDir, {
      '.sncp/progetti/testproj/project.json': JSON.stringify({ projectName: 'testproj' }),
      '.sncp/progetti/testproj/PROMPT_RIPRESA_testproj.md': promptRipresa
    });

    const originalCwd = process.cwd;
    t.mock.method(process, 'cwd', () => tempDir);

    const { loadProjectContext } = await import(`../../src/sncp/loader.js?t=${Date.now()}_l7`);
    const result = await loadProjectContext();

    assert.ok(result.lastSession, 'Should have lastSession');
    assert.equal(result.lastSession.date, '2026-04-01');

    process.cwd = originalCwd;
  });

  it('lastSession is null when PROMPT_RIPRESA has no date', async (t) => {
    const tempDir = await createTempDir(t);
    const promptRipresa = `# PROMPT RIPRESA

No date in here.
`;
    await createFileStructure(tempDir, {
      '.sncp/progetti/testproj/PROMPT_RIPRESA_testproj.md': promptRipresa
    });

    const originalCwd = process.cwd;
    t.mock.method(process, 'cwd', () => tempDir);

    const { loadProjectContext } = await import(`../../src/sncp/loader.js?t=${Date.now()}_l8`);
    const result = await loadProjectContext();

    assert.equal(result.lastSession, null, 'Should be null without date pattern');

    process.cwd = originalCwd;
  });

  it('uses default nextStep when PROMPT_RIPRESA has no steps section', async (t) => {
    const tempDir = await createTempDir(t);
    const promptRipresa = `# PROMPT RIPRESA

Just some notes, no steps section.
`;
    await createFileStructure(tempDir, {
      '.sncp/progetti/testproj/PROMPT_RIPRESA_testproj.md': promptRipresa
    });

    const originalCwd = process.cwd;
    t.mock.method(process, 'cwd', () => tempDir);

    const { loadProjectContext } = await import(`../../src/sncp/loader.js?t=${Date.now()}_l9`);
    const result = await loadProjectContext();

    assert.ok(result.nextStep.includes('cervellaswarm task'), 'Should use default nextStep');

    process.cwd = originalCwd;
  });

  it('returns sncpPath in result', async (t) => {
    const tempDir = await createTempDir(t);
    await createFileStructure(tempDir, {
      '.sncp/progetti/testproj/.gitkeep': ''
    });

    const originalCwd = process.cwd;
    t.mock.method(process, 'cwd', () => tempDir);

    const { loadProjectContext } = await import(`../../src/sncp/loader.js?t=${Date.now()}_l10`);
    const result = await loadProjectContext();

    assert.ok(result.sncpPath, 'Should include sncpPath');
    assert.ok(result.sncpPath.includes('testproj'), 'sncpPath should point to project dir');

    process.cwd = originalCwd;
  });

  it('progress defaults to 0', async (t) => {
    const tempDir = await createTempDir(t);
    await createFileStructure(tempDir, {
      '.sncp/progetti/testproj/.gitkeep': ''
    });

    const originalCwd = process.cwd;
    t.mock.method(process, 'cwd', () => tempDir);

    const { loadProjectContext } = await import(`../../src/sncp/loader.js?t=${Date.now()}_l11`);
    const result = await loadProjectContext();

    assert.equal(result.progress, 0, 'Progress should default to 0');

    process.cwd = originalCwd;
  });

});
