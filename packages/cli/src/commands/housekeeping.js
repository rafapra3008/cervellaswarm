/**
 * cervellaswarm housekeeping
 *
 * Keep your .sncp/ folder clean and healthy.
 * Checks file sizes, suggests cleanup, and optionally auto-fixes.
 *
 * Philosophy: "Casa pulita = mente pulita = lavoro pulito!"
 *
 * Copyright 2026 CervellaSwarm Contributors
 * Licensed under the Apache License, Version 2.0
 * http://www.apache.org/licenses/LICENSE-2.0
 */

import chalk from 'chalk';
import { readFile, readdir, mkdir, rename, stat } from 'fs/promises';
import { join } from 'path';
import { loadProjectContext } from '../sncp/loader.js';
import { CervellaError, displayError } from '../utils/errors.js';

// File limits (in lines)
// NOTE: stato.md eliminated in SNCP 4.0 (S357). Only PROMPT_RIPRESA checked.
const LIMITS = {
  PROMPT_RIPRESA: 150,
  REPORT_DAYS: 30
};

// Status icons
const ICONS = {
  ok: chalk.green('OK'),
  warning: chalk.yellow('WARNING'),
  error: chalk.red('ERROR')
};

/**
 * Count lines in a file
 */
async function countLines(filePath) {
  try {
    const content = await readFile(filePath, 'utf8');
    return content.split('\n').length;
  } catch {
    return 0;
  }
}

/**
 * Get file age in days
 */
async function getFileAgeDays(filePath) {
  try {
    const stats = await stat(filePath);
    const now = new Date();
    const modified = new Date(stats.mtime);
    return Math.floor((now - modified) / (1000 * 60 * 60 * 24));
  } catch {
    return 0;
  }
}

/**
 * Check health of SNCP files
 */
async function checkHealth(context) {
  const results = {
    promptRipresa: { lines: 0, limit: LIMITS.PROMPT_RIPRESA, status: 'ok' },
    reports: { total: 0, old: 0, status: 'ok' }
  };

  const sncpPath = context.sncpPath;

  // Check PROMPT_RIPRESA
  const promptPath = join(sncpPath, `PROMPT_RIPRESA_${context.name}.md`);
  results.promptRipresa.lines = await countLines(promptPath);
  if (results.promptRipresa.lines > LIMITS.PROMPT_RIPRESA) {
    results.promptRipresa.status = 'error';
  } else if (results.promptRipresa.lines > LIMITS.PROMPT_RIPRESA * 0.8) {
    results.promptRipresa.status = 'warning';
  }

  // Check reports folder
  const reportsPath = join(sncpPath, 'reports');
  try {
    const files = await readdir(reportsPath);
    results.reports.total = files.length;

    for (const file of files) {
      const filePath = join(reportsPath, file);
      const ageDays = await getFileAgeDays(filePath);
      if (ageDays > LIMITS.REPORT_DAYS) {
        results.reports.old++;
      }
    }

    if (results.reports.old > 0) {
      results.reports.status = 'warning';
    }
  } catch {
    // reports folder might not exist - that's ok
  }

  return results;
}

/**
 * Display health check results
 */
function displayHealth(results) {
  console.log('');
  console.log(chalk.cyan.bold('  Checking .sncp/ health...'));
  console.log('');

  // PROMPT_RIPRESA
  const prStatus = ICONS[results.promptRipresa.status];
  const prPercent = Math.round((results.promptRipresa.lines / results.promptRipresa.limit) * 100);
  console.log(`  PROMPT_RIPRESA: ${results.promptRipresa.lines} lines [${prStatus}] (${prPercent}% of limit)`);

  // reports
  const rpStatus = ICONS[results.reports.status];
  console.log(`  reports/:       ${results.reports.total} files (${results.reports.old} > ${LIMITS.REPORT_DAYS} days) [${rpStatus}]`);

  console.log('');
}

/**
 * Display suggestions based on health check
 */
function displaySuggestions(results) {
  const suggestions = [];

  if (results.promptRipresa.status !== 'ok') {
    suggestions.push(`Archive old sessions from PROMPT_RIPRESA (${results.promptRipresa.lines}/${results.promptRipresa.limit} lines)`);
  }

  if (results.reports.old > 0) {
    suggestions.push(`Archive ${results.reports.old} old reports with: cervellaswarm housekeeping --archive`);
  }

  if (suggestions.length > 0) {
    console.log(chalk.yellow.bold('  Suggestions:'));
    suggestions.forEach(s => console.log(chalk.yellow(`  - ${s}`)));
    console.log('');
  } else {
    console.log(chalk.green('  Everything looks good! Casa pulita!'));
    console.log('');
  }
}

/**
 * Archive old reports
 */
async function archiveReports(context, results) {
  console.log('');
  console.log(chalk.cyan.bold('  Archiving old reports...'));
  console.log('');

  if (results.reports.old === 0) {
    console.log(chalk.gray('  No old reports to archive.'));
    console.log('');
    return;
  }

  const reportsPath = join(context.sncpPath, 'reports');
  const archivePath = join(context.sncpPath, 'archivio', 'reports');

  try {
    await mkdir(archivePath, { recursive: true });

    const files = await readdir(reportsPath);
    let archived = 0;

    for (const file of files) {
      const filePath = join(reportsPath, file);
      const ageDays = await getFileAgeDays(filePath);

      if (ageDays > LIMITS.REPORT_DAYS) {
        await rename(filePath, join(archivePath, file));
        archived++;
      }
    }

    console.log(chalk.green(`  Archived ${archived} reports to .sncp/archivio/reports/`));
  } catch (error) {
    console.log(chalk.red(`  Failed to archive reports - ${error.message}`));
  }

  console.log('');
}

/**
 * Main housekeeping command
 */
export async function housekeepingCommand(options) {
  try {
    // Load project context
    const context = await loadProjectContext();

    if (!context) {
      const error = new CervellaError('NOT_INITIALIZED');
      displayError(error);
      process.exit(error.code);
    }

    // Display header
    console.log('');
    console.log(chalk.cyan.bold(`  CervellaSwarm Housekeeping`));
    console.log(chalk.gray(`  Project: ${context.name}`));

    // Check health
    const results = await checkHealth(context);

    // Display results
    displayHealth(results);

    // Handle options
    if (options.auto || options.archive) {
      // Auto/archive mode: archive old reports
      await archiveReports(context, results);
      console.log(chalk.green('  Housekeeping complete!'));
      console.log('');
    } else if (options.compact) {
      // NOTE: stato.md compaction eliminated in SNCP 4.0 (S357)
      console.log(chalk.gray('  Compact is no longer needed (stato.md eliminated in SNCP 4.0).'));
      console.log('');
    } else {
      // Just show suggestions
      displaySuggestions(results);
    }

    // Footer
    console.log(chalk.gray('  "Casa pulita = mente pulita = lavoro pulito!"'));
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
