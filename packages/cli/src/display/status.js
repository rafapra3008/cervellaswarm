/**
 * Status Display
 *
 * Formats project status for display.
 */

import chalk from 'chalk';

export function formatStatus(context) {
  // Simple progress bar for now
  const progress = context.progress || 0;
  const filled = Math.floor(progress / 5);
  const empty = 20 - filled;
  const bar = chalk.green('█'.repeat(filled)) + chalk.gray('░'.repeat(empty));

  return `  ${bar} ${progress}%`;
}
