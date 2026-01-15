/**
 * Status Display
 *
 * Formats project status for display.
 *
 * Copyright 2026 Rafa & Cervella
 * Licensed under the Apache License, Version 2.0
 * http://www.apache.org/licenses/LICENSE-2.0
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
