/**
 * cervellaswarm init
 *
 * Initialize CervellaSwarm for a project.
 * Creates project constitution through interactive wizard.
 *
 * Philosophy: "Define your project ONCE. Never re-explain."
 *
 * Copyright 2026 Rafa & Cervella
 * Licensed under the Apache License, Version 2.0
 * http://www.apache.org/licenses/LICENSE-2.0
 */

import chalk from 'chalk';
import ora from 'ora';
import { existsSync, readdirSync } from 'fs';
import { join } from 'path';
import { runWizard } from '../wizard/questions.js';
import { generateConstitution } from '../templates/constitution.js';
import { initSNCP } from '../sncp/init.js';
import { CervellaError, displayError, ExitCode } from '../utils/errors.js';

/**
 * Check if project is already initialized
 */
function isAlreadyInitialized() {
  const projectsPath = join(process.cwd(), '.sncp', 'progetti');
  if (!existsSync(projectsPath)) return false;
  try {
    const projects = readdirSync(projectsPath);
    return projects.length > 0;
  } catch {
    return false;
  }
}

export async function initCommand(options) {
  console.log('');
  console.log(chalk.cyan.bold('  Welcome to CervellaSwarm!'));
  console.log(chalk.gray('  16 AI agents. 1 command. Your AI dev team.'));
  console.log('');

  // Check if already initialized
  if (isAlreadyInitialized() && !options.force) {
    console.log(chalk.yellow('  Project already initialized!'));
    console.log(chalk.gray('  Use `cervellaswarm status` to see current state.'));
    console.log(chalk.gray('  Use `cervellaswarm init --force` to reinitialize.'));
    console.log('');
    return;
  }

  // Skip wizard if -y flag - use defaults
  if (options.yes) {
    const projectName = options.name || process.cwd().split('/').pop().toLowerCase().replace(/[^a-z0-9-]/g, '-');

    const defaultAnswers = {
      projectName,
      description: 'A CervellaSwarm project',
      projectType: 'webapp',
      mainGoal: 'Build something great',
      successCriteria: ['personal'],
      timeline: 'exploratory',
      techStack: '',
      workingMode: 'solo',
      sessionLength: 'variable',
      notificationStyle: 'standard'
    };

    console.log(chalk.yellow(`  Quick init for: ${projectName}`));

    const spinner = ora('Creating project structure...').start();

    try {
      await initSNCP(defaultAnswers);
      await generateConstitution(defaultAnswers);
      spinner.succeed('Project initialized!');

      console.log('');
      console.log(chalk.green.bold('  Ready to go!'));
      console.log(chalk.white('  Next: cervellaswarm task "your first task"'));
      console.log('');
    } catch (error) {
      spinner.fail('Initialization failed');
      const cervellaError = new CervellaError('WRITE_FAILED', error.message);
      displayError(cervellaError);
      process.exit(cervellaError.code);
    }
    return;
  }

  console.log(chalk.white('  Let\'s create your project constitution.'));
  console.log(chalk.white('  This takes ~5 minutes and prevents you from'));
  console.log(chalk.white('  ever having to re-explain your project.'));
  console.log('');
  console.log(chalk.gray('  (Press Ctrl+C anytime to cancel)'));
  console.log('');

  try {
    // Run the wizard
    const answers = await runWizard();

    // Generate files
    const spinner = ora('Creating your project constitution...').start();

    await initSNCP(answers);
    await generateConstitution(answers);

    spinner.succeed('Project initialized successfully!');

    console.log('');
    console.log(chalk.green.bold('  Your project constitution is ready!'));
    console.log(chalk.white('  You\'ll never need to re-explain your goals.'));
    console.log('');
    console.log(chalk.cyan('  Next: Start your first work session'));
    console.log(chalk.white('  $ cervellaswarm task "your first task"'));
    console.log('');

  } catch (error) {
    if (error.name === 'ExitPromptError') {
      console.log('');
      console.log(chalk.yellow('  Initialization cancelled.'));
      console.log(chalk.gray('  Run `cervellaswarm init` when you\'re ready.'));
      process.exit(ExitCode.CANCELLED);
    }
    const cervellaError = new CervellaError('WRITE_FAILED', error.message);
    displayError(cervellaError);
    process.exit(cervellaError.code);
  }
}
