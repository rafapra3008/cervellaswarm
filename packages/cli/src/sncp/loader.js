/**
 * SNCP Loader
 *
 * Loads project context from .sncp folder.
 */

import { readFile, access } from 'fs/promises';
import { join } from 'path';

export async function loadProjectContext() {
  // TODO: Implement full context loading
  const projectPath = process.cwd();
  const sncpPath = join(projectPath, '.sncp');

  try {
    await access(sncpPath);
    // Return stub context for now
    return {
      name: 'project',
      description: 'A project',
      goal: 'Build something great',
      nextStep: 'Continue with your next task'
    };
  } catch {
    return null;
  }
}
