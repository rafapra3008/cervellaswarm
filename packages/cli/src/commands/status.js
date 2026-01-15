/**
 * cervellaswarm status
 *
 * Show current project status.
 * Displays progress, last session, next steps.
 *
 * Philosophy: "Every step counts. Celebrate progress."
 *
 * Copyright 2026 Rafa & Cervella
 * Licensed under the Apache License, Version 2.0
 * http://www.apache.org/licenses/LICENSE-2.0
 */

import chalk from 'chalk';
import { loadProjectContext } from '../sncp/loader.js';
import { formatStatus } from '../display/status.js';
import { CervellaError, displayError } from '../utils/errors.js';

export async function statusCommand(options) {
  try {
    // Load project context from SNCP
    const context = await loadProjectContext();

    if (!context) {
      const error = new CervellaError('NOT_INITIALIZED');
      displayError(error);
      process.exit(error.code);
    }

    // Display status
    console.log('');
    console.log(chalk.cyan.bold(`  Project: ${context.name}`));
    console.log(chalk.gray(`  ${context.description}`));
    console.log('');

    if (options.detailed) {
      // Detailed status
      console.log(chalk.white.bold('  Constitution:'));
      console.log(chalk.gray(`  Goal: ${context.goal}`));
      console.log('');
    }

    // Progress
    console.log(chalk.white.bold('  Progress:'));
    console.log(formatStatus(context));
    console.log('');

    // Last session
    if (context.lastSession) {
      console.log(chalk.white.bold('  Last Session:'));
      console.log(chalk.gray(`  ${context.lastSession.date}`));
      console.log(chalk.gray(`  ${context.lastSession.summary}`));
      console.log('');
    }

    // Next step
    console.log(chalk.white.bold('  Next Step:'));
    console.log(chalk.cyan(`  ${context.nextStep || 'Run a task to continue'}`));
    console.log('');

    // Encouraging message (no time pressure!)
    console.log(chalk.green('  Every step counts. Keep going!'));
    console.log('');

  } catch (error) {
    if (error instanceof CervellaError) {
      displayError(error);
      process.exit(error.code);
    }
    const cervellaError = new CervellaError('READ_FAILED', error.message);
    displayError(cervellaError);
    process.exit(cervellaError.code);
  }
}
