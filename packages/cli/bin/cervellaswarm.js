#!/usr/bin/env node

/**
 * CervellaSwarm CLI
 *
 * 16 AI agents working as a team for your project.
 * "Not an assistant - a TEAM."
 *
 * Copyright 2026 Rafa & Cervella
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import { program } from 'commander';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { readFileSync } from 'fs';

// Get package version
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const packageJson = JSON.parse(
  readFileSync(join(__dirname, '..', 'package.json'), 'utf8')
);

// Import commands
import { initCommand } from '../src/commands/init.js';
import { statusCommand } from '../src/commands/status.js';
import { taskCommand } from '../src/commands/task.js';
import { resumeCommand } from '../src/commands/resume.js';

// ASCII Art Banner
const banner = `
   ____                    _ _       ____
  / ___|___ _ ____   _____| | | __ _/ ___|_      ____ _ _ __ _ __ ___
 | |   / _ \\ '__\\ \\ / / _ \\ | |/ _\` \\___ \\ \\ /\\ / / _\` | '__| '_ \` _ \\
 | |__|  __/ |   \\ V /  __/ | | (_| |___) \\ V  V / (_| | |  | | | | | |
  \\____\\___|_|    \\_/ \\___|_|_|\\__,_|____/ \\_/\\_/ \\__,_|_|  |_| |_| |_|

  16 AI agents. 1 command. Your AI dev team.
`;

// Setup program
program
  .name('cervellaswarm')
  .description('16 AI agents working as a team for your project')
  .version(packageJson.version, '-v, --version', 'Output the current version')
  .addHelpText('beforeAll', banner);

// Register commands
program
  .command('init')
  .description('Initialize CervellaSwarm for your project')
  .option('-y, --yes', 'Skip wizard, use defaults')
  .option('-n, --name <name>', 'Project name')
  .action(initCommand);

program
  .command('status')
  .alias('s')
  .description('Show current project status')
  .option('-d, --detailed', 'Show detailed status')
  .action(statusCommand);

program
  .command('task <description>')
  .alias('t')
  .description('Execute a task with the AI team')
  .option('-a, --agent <agent>', 'Specify agent (backend, frontend, tester...)')
  .option('--auto', 'Let Regina decide which agent to use')
  .action(taskCommand);

program
  .command('resume')
  .alias('r')
  .description('Resume from last session')
  .option('-l, --list', 'List recent sessions')
  .option('-s, --session <id>', 'Resume specific session')
  .action(resumeCommand);

// Parse arguments
program.parse();
