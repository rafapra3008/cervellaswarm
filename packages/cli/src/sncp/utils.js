/**
 * SNCP Shared Utilities
 *
 * Single source of truth for SNCP directory discovery.
 * DRY fix: was duplicated in writer.js and session/manager.js (S508).
 */

import { join } from 'node:path';
import { existsSync } from 'node:fs';

/**
 * Find .sncp directory by walking up from cwd (max 5 levels).
 * Returns the .sncp path (creates in cwd if not found).
 */
export function findSncpDir() {
  let dir = process.cwd();

  for (let i = 0; i < 5; i++) {
    const sncpPath = join(dir, '.sncp');
    if (existsSync(sncpPath)) {
      return sncpPath;
    }
    const parent = join(dir, '..');
    if (parent === dir) break;
    dir = parent;
  }

  return join(process.cwd(), '.sncp');
}
