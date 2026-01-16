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
import { doctorCommand } from '../src/commands/doctor.js';

// ASCII Art Banner
const banner = `
   ____                    _ _       ____
  / ___|___ _ ____   _____| | | __ _/ ___|_      ____ _ _ __ _ __ ___
 | |   / _ \\ '__\\ \\ / / _ \\ | |/ _\` \\___ \\ \\ /\\ / / _\` | '__| '_ \` _ \\
 | |__|  __/ |   \\ V /  __/ | | (_| |___) \\ V  V / (_| | |  | | | | | |
  \\____\\___|_|    \\_/ \\___|_|_|\\__,_|____/ \\_/\\_/ \\__,_|_|  |_| |_| |_|

  16 AI agents. 1 command. Your AI dev team.
`;

// Help footer with examples and getting started
const helpFooter = `
Getting Started:
  $ cervellaswarm init          Create project constitution
  $ cervellaswarm task "..."    Execute a task with AI team
  $ cervellaswarm status        Check project progress
  $ cervellaswarm resume        Continue from last session
  $ cervellaswarm doctor        Check setup and diagnose issues

Examples:
  $ cervellaswarm init -y                    Quick init with defaults
  $ cervellaswarm task "add login page"      Frontend task
  $ cervellaswarm task "create user API"     Backend task
  $ cervellaswarm task "write tests" -a tester

Available Agents:
  backend   Python, FastAPI, APIs, Database
  frontend  React, CSS, Tailwind, UI/UX
  tester    Testing, Debug, QA
  docs      Documentation, README
  devops    Deploy, CI/CD, Docker
  data      SQL, Analytics, Queries
  security  Security Audit, Vulnerabilities
  researcher  Research, Analysis

Documentation: https://cervellaswarm.dev
`;

// Setup program
program
  .name('cervellaswarm')
  .description('16 AI agents working as a team for your project')
  .version(packageJson.version, '-v, --version', 'Output the current version')
  .addHelpText('beforeAll', banner)
  .addHelpText('after', helpFooter);

// Register commands
program
  .command('init')
  .description('Initialize CervellaSwarm for your project')
  .option('-y, --yes', 'Skip wizard, use defaults')
  .option('-n, --name <name>', 'Project name')
  .option('-f, --force', 'Reinitialize even if already initialized')
  .addHelpText('after', `
Examples:
  $ cervellaswarm init              Interactive wizard (recommended)
  $ cervellaswarm init -y           Quick init with defaults
  $ cervellaswarm init -y -n myapp  Quick init with custom name
  $ cervellaswarm init --force      Reinitialize existing project

The wizard asks 10 questions to create your project constitution.
This ensures the AI team understands your project from day one.
Define once, never re-explain.
`)
  .action(initCommand);

program
  .command('status')
  .alias('s')
  .description('Show current project status')
  .option('-d, --detailed', 'Show detailed constitution and progress')
  .addHelpText('after', `
Examples:
  $ cervellaswarm status         Quick overview
  $ cervellaswarm s              Same (alias)
  $ cervellaswarm status -d      Detailed view with constitution

Shows:
  - Project name and description
  - Current progress
  - Last session info
  - Suggested next step
`)
  .action(statusCommand);

program
  .command('task <description>')
  .alias('t')
  .description('Execute a task with the AI team')
  .option('-a, --agent <agent>', 'Specify agent (see list below)')
  .option('--auto', 'Let Regina decide which agent (default)')
  .addHelpText('after', `
Examples:
  $ cervellaswarm task "add login page"           Auto-routes to frontend
  $ cervellaswarm task "create REST API"          Auto-routes to backend
  $ cervellaswarm task "fix bug in auth"          Auto-routes to tester
  $ cervellaswarm task "optimize queries"         Auto-routes to data
  $ cervellaswarm task "review code" -a security  Force security agent

Available Agents:
  backend     Python, FastAPI, APIs, Database, server-side logic
  frontend    React, CSS, Tailwind, UI/UX, components
  tester      Testing, Debug, QA, bug hunting
  docs        Documentation, README, guides, tutorials
  devops      Deploy, CI/CD, Docker, infrastructure
  data        SQL, Analytics, queries, database design
  security    Security audit, vulnerabilities, best practices
  researcher  Research, analysis, comparisons

The Regina (orchestrator) automatically routes tasks to the right agent
based on keywords. Use -a to override if needed.
`)
  .action(taskCommand);

program
  .command('resume')
  .alias('r')
  .description('Resume from last session')
  .option('-l, --list', 'List recent sessions')
  .option('-s, --session <id>', 'Resume specific session by ID')
  .addHelpText('after', `
Examples:
  $ cervellaswarm resume         Resume from last session
  $ cervellaswarm r              Same (alias)
  $ cervellaswarm resume -l      List all recent sessions
  $ cervellaswarm resume -s 3    Resume specific session

The recap adapts to time since last session:
  - Same day: Brief reminder
  - Few days: Context summary
  - Weeks/months: Full project recap

No judgment, no pressure - just helpful context.
`)
  .action(resumeCommand);

program
  .command('doctor')
  .description('Check CervellaSwarm setup and diagnose issues')
  .option('--validate', 'Test API key with actual call')
  .option('--config', 'Show current configuration')
  .option('--verbose', 'Show detailed information')
  .option('--strict', 'Exit with error code if issues found')
  .addHelpText('after', `
Examples:
  $ cervellaswarm doctor            Quick health check
  $ cervellaswarm doctor --validate Test API key works
  $ cervellaswarm doctor --config   Show all config values
  $ cervellaswarm doctor --strict   For CI/scripts (exits 1 on issues)

Checks:
  - Node.js version (requires 18+)
  - API key configured
  - Project initialized
  - Configuration valid
`)
  .action(doctorCommand);

// Parse arguments
program.parse();
