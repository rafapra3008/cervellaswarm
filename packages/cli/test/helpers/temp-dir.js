/**
 * Temp Directory Helper
 *
 * Helper per creare directory temporanee nei test,
 * con cleanup automatico.
 *
 * "Fatto BENE > Fatto VELOCE"
 */

import fs from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';

/**
 * Crea directory temporanea con cleanup automatico
 *
 * @param {Object} t - Test context (from node:test)
 * @param {string} prefix - Prefisso per nome directory
 * @returns {Promise<string>} - Path directory creata
 */
export async function createTempDir(t, prefix = 'cervellaswarm-test-') {
  const tempDir = await fs.mkdtemp(
    path.join(os.tmpdir(), prefix)
  );

  // Cleanup automatico alla fine del test
  t.after(async () => {
    await fs.rm(tempDir, { recursive: true, force: true });
  });

  return tempDir;
}

/**
 * Crea struttura file per test
 *
 * @param {string} baseDir - Directory base
 * @param {Object} structure - Mappa path -> contenuto
 *
 * @example
 * await createFileStructure(tempDir, {
 *   'package.json': '{"name":"test"}',
 *   'src/index.js': 'console.log("hi");',
 *   '.sncp/stato.md': '# Stato'
 * });
 */
export async function createFileStructure(baseDir, structure) {
  for (const [filePath, content] of Object.entries(structure)) {
    const fullPath = path.join(baseDir, filePath);
    const dir = path.dirname(fullPath);

    await fs.mkdir(dir, { recursive: true });

    if (typeof content === 'string') {
      await fs.writeFile(fullPath, content);
    }
  }
}

/**
 * Verifica che una struttura file esista
 *
 * @param {string} baseDir - Directory base
 * @param {string[]} paths - Lista di path da verificare
 * @returns {Promise<Object>} - Mappa path -> exists
 */
export async function verifyFileStructure(baseDir, paths) {
  const results = {};

  for (const filePath of paths) {
    const fullPath = path.join(baseDir, filePath);
    try {
      await fs.access(fullPath);
      results[filePath] = true;
    } catch {
      results[filePath] = false;
    }
  }

  return results;
}

/**
 * Legge contenuto file in temp dir
 *
 * @param {string} baseDir - Directory base
 * @param {string} filePath - Path relativo
 * @returns {Promise<string|null>} - Contenuto o null se non esiste
 */
export async function readTempFile(baseDir, filePath) {
  try {
    const fullPath = path.join(baseDir, filePath);
    return await fs.readFile(fullPath, 'utf-8');
  } catch {
    return null;
  }
}
