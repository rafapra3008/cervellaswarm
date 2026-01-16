/**
 * cervellaswarm doctor
 *
 * Diagnose CervellaSwarm setup and configuration.
 * Helps users identify and fix issues.
 *
 * Philosophy: "Fix problems before they become blockers."
 *
 * Copyright 2026 Rafa & Cervella
 * Licensed under the Apache License, Version 2.0
 * http://www.apache.org/licenses/LICENSE-2.0
 */

import chalk from 'chalk';
import ora from 'ora';
import { existsSync } from 'fs';
import { join } from 'path';
import * as config from '../config/manager.js';

// Check symbols
const CHECK_OK = chalk.green('✓');
const CHECK_WARN = chalk.yellow('⚠');
const CHECK_FAIL = chalk.red('✗');

/**
 * Run all diagnostic checks
 */
async function runChecks(options) {
  const results = [];

  // Check 1: Node.js version
  const nodeVersion = process.version;
  const nodeMajor = parseInt(nodeVersion.slice(1).split('.')[0], 10);
  results.push({
    name: 'Node.js',
    status: nodeMajor >= 18 ? 'ok' : 'fail',
    message: `${nodeVersion}${nodeMajor >= 18 ? '' : ' (requires >= 18.0.0)'}`,
    fix: nodeMajor < 18 ? 'Install Node.js 18 or higher: https://nodejs.org/' : null
  });

  // Check 2: API Key
  const hasKey = config.hasApiKey();
  const keySource = config.getApiKeySource();

  if (hasKey) {
    results.push({
      name: 'API Key',
      status: 'ok',
      message: `Configured (from ${keySource})`,
      fix: null
    });

    // Check 2b: API Key validation (if --validate flag)
    if (options.validate) {
      const spinner = ora('Validating API key...').start();
      const validation = await config.validateApiKey();
      spinner.stop();

      if (validation.valid) {
        results.push({
          name: 'API Key Valid',
          status: validation.warning ? 'warn' : 'ok',
          message: validation.warning || 'Key works correctly',
          fix: null
        });
      } else {
        results.push({
          name: 'API Key Valid',
          status: 'fail',
          message: validation.error,
          fix: 'Get a new key at https://console.anthropic.com/'
        });
      }
    }
  } else {
    results.push({
      name: 'API Key',
      status: 'fail',
      message: 'Not configured',
      fix: 'Run: cervellaswarm init'
    });
  }

  // Check 3: Config file
  const configPath = config.getConfigPath();
  results.push({
    name: 'Config File',
    status: 'ok',
    message: configPath,
    fix: null
  });

  // Check 4: Project initialized
  const sncpPath = join(process.cwd(), '.sncp');
  const projectsPath = join(sncpPath, 'progetti');
  const hasProject = existsSync(projectsPath);

  results.push({
    name: 'Project Init',
    status: hasProject ? 'ok' : 'warn',
    message: hasProject ? 'Initialized in current directory' : 'Not initialized here',
    fix: hasProject ? null : 'Run: cervellaswarm init'
  });

  // Check 5: Default Model
  const defaultModel = config.getDefaultModel();
  results.push({
    name: 'Default Model',
    status: 'ok',
    message: defaultModel,
    fix: null
  });

  // Check 6: Timeout
  const timeout = config.getTimeout();
  results.push({
    name: 'Timeout',
    status: 'ok',
    message: `${timeout / 1000}s`,
    fix: null
  });

  return results;
}

/**
 * Display check results
 */
function displayResults(results) {
  console.log('');
  console.log(chalk.cyan.bold('  CervellaSwarm Doctor'));
  console.log(chalk.gray('  ─────────────────────────────────────────'));
  console.log('');

  let hasIssues = false;
  const fixes = [];

  for (const check of results) {
    const icon = check.status === 'ok' ? CHECK_OK
               : check.status === 'warn' ? CHECK_WARN
               : CHECK_FAIL;

    console.log(`  ${icon} ${check.name.padEnd(16)} ${chalk.gray(check.message)}`);

    if (check.status !== 'ok') {
      hasIssues = true;
      if (check.fix) {
        fixes.push({ name: check.name, fix: check.fix });
      }
    }
  }

  console.log('');

  // Show fixes if needed
  if (fixes.length > 0) {
    console.log(chalk.yellow.bold('  To fix issues:'));
    console.log(chalk.gray('  ─────────────────────────────────────────'));
    console.log('');
    for (const item of fixes) {
      console.log(`  ${chalk.white(item.name)}: ${chalk.cyan(item.fix)}`);
    }
    console.log('');
  }

  // Summary
  if (hasIssues) {
    console.log(chalk.yellow('  Some issues found. Fix them to use CervellaSwarm fully.'));
  } else {
    console.log(chalk.green('  All checks passed! CervellaSwarm is ready.'));
  }
  console.log('');

  return hasIssues;
}

/**
 * Display config values
 */
function displayConfig() {
  console.log('');
  console.log(chalk.cyan.bold('  Current Configuration'));
  console.log(chalk.gray('  ─────────────────────────────────────────'));
  console.log('');

  const allConfig = config.getAllConfig();

  for (const [key, value] of Object.entries(allConfig)) {
    const displayValue = typeof value === 'object' ? JSON.stringify(value) : value;
    console.log(`  ${chalk.white(key.padEnd(16))} ${chalk.gray(displayValue)}`);
  }

  console.log('');
}

/**
 * Doctor command entry point
 */
export async function doctorCommand(options) {
  // If --config flag, just show config
  if (options.config) {
    displayConfig();
    return;
  }

  // Run diagnostics
  const results = await runChecks(options);
  const hasIssues = displayResults(results);

  // Show config path for advanced users
  if (options.verbose) {
    displayConfig();
  }

  // Exit with error code if issues found (for CI/scripting)
  if (hasIssues && options.strict) {
    process.exit(1);
  }
}
