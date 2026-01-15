/**
 * cervellaswarm task
 *
 * Execute a task with the AI team.
 * Routes to appropriate agent(s) based on task description.
 *
 * Philosophy: "One step at a time. The team is with you."
 */

import chalk from 'chalk';
import ora from 'ora';
import { loadProjectContext } from '../sncp/loader.js';
import { routeTask } from '../agents/router.js';
import { spawnAgent } from '../agents/spawner.js';
import { saveTaskReport } from '../sncp/writer.js';

export async function taskCommand(description, options) {
  try {
    // Validate description
    if (!description || description.trim().length === 0) {
      console.log('');
      console.log(chalk.yellow('  Please provide a task description.'));
      console.log(chalk.white('  Example: cervellaswarm task "add login page"'));
      console.log('');
      return;
    }

    // Load project context
    const context = await loadProjectContext();

    if (!context) {
      console.log('');
      console.log(chalk.yellow('  No CervellaSwarm project found.'));
      console.log(chalk.white('  Run `cervellaswarm init` first.'));
      console.log('');
      return;
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

    // Save report
    await saveTaskReport(description, agent, result);

    console.log('');
    console.log(chalk.green.bold('  Task completed!'));
    console.log(chalk.gray(`  One more step forward.`));
    console.log('');

    // Suggest next step (no time pressure)
    if (result.nextStep) {
      console.log(chalk.white('  Suggested next step:'));
      console.log(chalk.cyan(`  ${result.nextStep}`));
      console.log(chalk.gray('  (When you\'re ready)'));
      console.log('');
    }

  } catch (error) {
    console.error(chalk.red('  Error executing task:'), error.message);
  }
}
