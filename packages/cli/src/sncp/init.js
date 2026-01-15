/**
 * SNCP Initializer
 *
 * Creates the .sncp folder structure for a project.
 */

import { mkdir, writeFile } from 'fs/promises';
import { join } from 'path';

export async function initSNCP(answers) {
  const projectPath = process.cwd();
  const sncpPath = join(projectPath, '.sncp', 'progetti', answers.projectName);

  // Create folder structure
  const folders = [
    '',
    'idee',
    'decisioni',
    'reports',
    'roadmaps',
    'workflow',
    'sessions'
  ];

  for (const folder of folders) {
    await mkdir(join(sncpPath, folder), { recursive: true });
  }

  console.log('  SNCP structure created...');
}
