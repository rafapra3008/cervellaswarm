/**
 * Progress Display
 *
 * Utilities for showing progress during task execution.
 * Clean, minimal, informative.
 *
 * Copyright 2026 Rafa & Cervella
 * Licensed under the Apache License, Version 2.0
 * http://www.apache.org/licenses/LICENSE-2.0
 */

import chalk from 'chalk';
import ora from 'ora';

/**
 * Create a spinner with CervellaSwarm style
 */
export function createSpinner(text) {
  return ora({
    text,
    spinner: 'dots',
    color: 'cyan'
  });
}

/**
 * Show task header
 */
export function showTaskHeader(description) {
  console.log('');
  console.log(chalk.cyan.bold('  Task received!'));
  console.log(chalk.gray(`  "${description.trim()}"`));
  console.log('');
}

/**
 * Show agent assignment
 */
export function showAgentAssigned(agent) {
  console.log(chalk.white(`  [${agent}] Starting work...`));
  console.log('');
}

/**
 * Show task completion
 */
export function showTaskComplete(result) {
  console.log('');
  if (result.success) {
    console.log(chalk.green.bold('  Task completed!'));
    if (result.duration) {
      console.log(chalk.gray(`  Duration: ${result.duration}`));
    }
    if (result.filesModified && result.filesModified.length > 0) {
      console.log(chalk.gray(`  Files modified: ${result.filesModified.length}`));
    }
  } else {
    console.log(chalk.yellow.bold('  Task finished with issues.'));
    if (result.error) {
      console.log(chalk.gray(`  ${result.error}`));
    }
  }
  console.log('');
}

/**
 * Show suggested next step
 */
export function showNextStep(nextStep) {
  if (nextStep) {
    console.log(chalk.white('  Suggested next step:'));
    console.log(chalk.cyan(`  ${nextStep}`));
    console.log(chalk.gray("  (When you're ready)"));
    console.log('');
  }
}

/**
 * Show error message
 */
export function showError(message) {
  console.log('');
  console.log(chalk.red(`  Error: ${message}`));
  console.log('');
}

/**
 * Show info message
 */
export function showInfo(message) {
  console.log(chalk.gray(`  ${message}`));
}

/**
 * Show section divider
 */
export function showDivider() {
  console.log(chalk.gray('  ─'.repeat(30)));
}

/**
 * Format file list for display
 */
export function formatFileList(files) {
  if (!files || files.length === 0) {
    return chalk.gray('  (no files modified)');
  }

  return files.map(f => chalk.white(`  • ${f}`)).join('\n');
}

/**
 * Show progress percentage
 */
export function showProgress(current, total, label = '') {
  const percent = Math.round((current / total) * 100);
  const filled = Math.floor(percent / 5);
  const empty = 20 - filled;
  const bar = chalk.green('█'.repeat(filled)) + chalk.gray('░'.repeat(empty));

  console.log(`  ${bar} ${percent}% ${label}`);
}
