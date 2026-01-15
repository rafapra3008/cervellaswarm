/**
 * cervellaswarm task
 *
 * Execute a task with the AI team.
 * Routes to appropriate agent(s) based on task description.
 *
 * Philosophy: "One step at a time. The team is with you."
 *
 * Copyright 2026 Rafa & Cervella
 * Licensed under the Apache License, Version 2.0
 * http://www.apache.org/licenses/LICENSE-2.0
 */

import chalk from 'chalk';
import ora from 'ora';
import { loadProjectContext } from '../sncp/loader.js';
import { routeTask } from '../agents/router.js';
import { spawnAgent } from '../agents/spawner.js';
import { saveTaskReport } from '../sncp/writer.js';
import { createTaskSession } from '../session/manager.js';
import { CervellaError, displayError } from '../utils/errors.js';

export async function taskCommand(description, options) {
  try {
    // Validate description
    if (!description || description.trim().length === 0) {
      const error = new CervellaError('MISSING_DESCRIPTION');
      displayError(error);
      process.exit(error.code);
    }

    // Load project context
    const context = await loadProjectContext();

    if (!context) {
      const error = new CervellaError('NOT_INITIALIZED');
      displayError(error);
      process.exit(error.code);
    }

    console.log('');
    console.log(chalk.cyan.bold('  Task received!'));
    console.log(chalk.gray(`  "${description.trim()}"`));
    console.log('');

    // Determine which agent to use
    let agent = options.agent;
    if (!agent || options.auto) {
      const spinner = ora('Regina is analyzing your task...').start();
      agent = await routeTask(description, context);
      spinner.succeed(`Task assigned to: ${agent}`);
    }

    console.log('');
    console.log(chalk.white(`  [${agent}] Starting work...`));
    console.log('');

    // Execute task
    const result = await spawnAgent(agent, description, context);

    // Save report and session
    await saveTaskReport(description, agent, result);
    await createTaskSession(description, agent, result);

    console.log('');
    if (result.success) {
      console.log(chalk.green.bold('  Task completed!'));
      console.log(chalk.gray('  One more step forward.'));
    } else {
      console.log(chalk.yellow.bold('  Task finished with issues.'));
      console.log(chalk.gray(`  ${result.error || 'Check the output above.'}`));
    }
    console.log('');

    // Suggest next step (no time pressure)
    if (result.nextStep) {
      console.log(chalk.white('  Suggested next step:'));
      console.log(chalk.cyan(`  ${result.nextStep}`));
      console.log(chalk.gray('  (When you\'re ready)'));
      console.log('');
    }

  } catch (error) {
    if (error instanceof CervellaError) {
      displayError(error);
      process.exit(error.code);
    }
    const cervellaError = new CervellaError('UNKNOWN', error.message);
    displayError(cervellaError);
    process.exit(cervellaError.code);
  }
}
