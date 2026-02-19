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
const LIMITS = {
  PROMPT_RIPRESA: 150,
  STATO: 500,
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
    stato: { lines: 0, limit: LIMITS.STATO, status: 'ok' },
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

  // Check stato.md
  const statoPath = join(sncpPath, 'stato.md');
  results.stato.lines = await countLines(statoPath);
  if (results.stato.lines > LIMITS.STATO) {
    results.stato.status = 'error';
  } else if (results.stato.lines > LIMITS.STATO * 0.8) {
    results.stato.status = 'warning';
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

  // stato.md
  const stStatus = ICONS[results.stato.status];
  const stPercent = Math.round((results.stato.lines / results.stato.limit) * 100);
  console.log(`  stato.md:       ${results.stato.lines} lines [${stStatus}] (${stPercent}% of limit)`);

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

  if (results.stato.status !== 'ok') {
    suggestions.push(`Compact stato.md with: cervellaswarm housekeeping --compact`);
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
 * Compact oversized files
 */
async function compactFiles(context, results) {
  console.log('');
  console.log(chalk.cyan.bold('  Compacting files...'));
  console.log('');

  let compacted = 0;

  // Compact stato.md if needed
  if (results.stato.status !== 'ok') {
    const statoPath = join(context.sncpPath, 'stato.md');
    const archivePath = join(context.sncpPath, 'archivio');

    try {
      await mkdir(archivePath, { recursive: true });

      const timestamp = new Date().toISOString().split('T')[0].replace(/-/g, '');
      const backupName = `stato_backup_${timestamp}.md`;

      await rename(statoPath, join(archivePath, backupName));

      // Create fresh stato.md
      const freshStato = `# ${context.name} - Stato Attuale

<!-- LIMITI: Questo file deve restare < 500 righe -->
<!-- Se cresce troppo, usa: cervellaswarm housekeeping -->

> **Ultimo aggiornamento:** ${new Date().toISOString().split('T')[0]}
> **Fase:** Continuazione

---

## COSA STA SUCCEDENDO

*Stato compattato. Vedi archivio per storico.*

---

## PROSSIMI PASSI

1. [ ] Continua dal punto precedente

---

*Previous stato archived to: ${backupName}*
`;

      const { writeFile } = await import('fs/promises');
      await writeFile(statoPath, freshStato, 'utf8');

      console.log(chalk.green(`  stato.md: Archived and reset (backup: ${backupName})`));
      compacted++;
    } catch (error) {
      console.log(chalk.red(`  stato.md: Failed to compact - ${error.message}`));
    }
  }

  if (compacted === 0) {
    console.log(chalk.gray('  No files needed compacting.'));
  }

  console.log('');
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
    if (options.auto) {
      // Auto mode: compact and archive if needed
      await compactFiles(context, results);
      await archiveReports(context, results);
      console.log(chalk.green('  Auto housekeeping complete!'));
      console.log('');
    } else if (options.compact) {
      await compactFiles(context, results);
    } else if (options.archive) {
      await archiveReports(context, results);
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
