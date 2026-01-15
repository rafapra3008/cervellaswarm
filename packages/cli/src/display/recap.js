/**
 * Recap Generator
 *
 * Generates session recap based on time since last session.
 * No judgment, just helpful context.
 *
 * Philosophy: "Welcome back! Here's where we were."
 */

import chalk from 'chalk';

export async function generateRecap(context, lastSession, daysSince) {
  let recap = '';

  if (daysSince === 0) {
    // Same day - minimal recap
    recap += chalk.gray('  You were here earlier today.\n');
    recap += chalk.white(`  Last task: ${lastSession.summary}\n`);

  } else if (daysSince <= 3) {
    // Recent - quick recap
    recap += chalk.gray(`  Last session: ${daysSince} day(s) ago\n`);
    recap += chalk.white(`  You worked on: ${lastSession.summary}\n`);
    recap += chalk.cyan(`  Next step: ${context.nextStep}\n`);

  } else if (daysSince <= 7) {
    // Week - fuller recap
    recap += chalk.cyan.bold('  Quick Recap:\n');
    recap += chalk.gray(`  Last session: ${daysSince} days ago\n`);
    recap += '\n';
    recap += chalk.white('  What you did:\n');
    recap += chalk.gray(`    ${lastSession.summary}\n`);
    recap += '\n';
    recap += chalk.white('  Suggested next step:\n');
    recap += chalk.cyan(`    ${context.nextStep}\n`);

  } else {
    // Long gap - full recap (no judgment!)
    recap += chalk.cyan.bold('  Welcome back!\n');
    recap += '\n';
    recap += chalk.white.bold(`  Project: ${context.name}\n`);
    recap += chalk.gray(`  Goal: ${context.goal}\n`);
    recap += '\n';
    recap += chalk.white('  Last session:\n');
    recap += chalk.gray(`    ${lastSession.date}\n`);
    recap += chalk.gray(`    ${lastSession.summary}\n`);
    recap += '\n';
    recap += chalk.white('  Suggested next step:\n');
    recap += chalk.cyan(`    ${context.nextStep}\n`);
  }

  return recap;
}
