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
import { runWizard } from '../wizard/questions.js';
import { generateConstitution } from '../templates/constitution.js';
import { initSNCP } from '../sncp/init.js';

export async function initCommand(options) {
  console.log('');
  console.log(chalk.cyan.bold('  Welcome to CervellaSwarm!'));
  console.log(chalk.gray('  16 AI agents. 1 command. Your AI dev team.'));
  console.log('');

  // Skip wizard if -y flag
  if (options.yes) {
    console.log(chalk.yellow('  Using default configuration...'));
    // TODO: Implement quick init with defaults
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
      return;
    }
    throw error;
  }
}
