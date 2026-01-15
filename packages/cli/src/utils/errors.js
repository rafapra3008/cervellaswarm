/**
 * CervellaSwarm Error Handling
 *
 * Centralized error management with clear messages and recovery suggestions.
 * Uses standard CLI exit codes for proper shell integration.
 *
 * Philosophy: "Errors should help, not frustrate."
 *
 * Copyright 2026 Rafa & Cervella
 * Licensed under the Apache License, Version 2.0
 * http://www.apache.org/licenses/LICENSE-2.0
 */

import chalk from 'chalk';

/**
 * Standard exit codes (POSIX/BSD convention)
 */
export const ExitCode = {
  SUCCESS: 0,          // All good
  GENERAL_ERROR: 1,    // Generic error
  MISUSE: 2,           // Wrong command usage
  NOT_INITIALIZED: 3,  // Project not initialized
  API_ERROR: 4,        // External API failed
  CONFIG_ERROR: 5,     // Configuration problem
  IO_ERROR: 6,         // File/network I/O error
  TIMEOUT: 7,          // Operation timed out
  CANCELLED: 130       // Ctrl+C (128 + SIGINT)
};

/**
 * Error types with messages and recovery suggestions
 */
export const ErrorType = {
  // Project errors
  NOT_INITIALIZED: {
    code: ExitCode.NOT_INITIALIZED,
    message: 'No CervellaSwarm project found',
    recovery: 'Run `cervellaswarm init` to initialize a project'
  },
  ALREADY_INITIALIZED: {
    code: ExitCode.SUCCESS,  // Not really an error
    message: 'Project already initialized',
    recovery: 'Use `cervellaswarm status` to see current state, or `--force` to reinitialize'
  },

  // Input errors
  MISSING_DESCRIPTION: {
    code: ExitCode.MISUSE,
    message: 'Task description is required',
    recovery: 'Example: cervellaswarm task "add login page"'
  },
  INVALID_AGENT: {
    code: ExitCode.MISUSE,
    message: 'Invalid agent specified',
    recovery: 'Use --list to see available agents'
  },

  // API errors
  NO_API_KEY: {
    code: ExitCode.CONFIG_ERROR,
    message: 'ANTHROPIC_API_KEY not found',
    recovery: [
      'Get your key at: https://console.anthropic.com/',
      'Set it: export ANTHROPIC_API_KEY=sk-ant-...'
    ]
  },
  INVALID_API_KEY: {
    code: ExitCode.CONFIG_ERROR,
    message: 'Invalid API key',
    recovery: 'Check your ANTHROPIC_API_KEY is correct'
  },
  API_PERMISSION: {
    code: ExitCode.API_ERROR,
    message: 'API key lacks permission',
    recovery: 'Check your API key permissions at console.anthropic.com'
  },
  RATE_LIMITED: {
    code: ExitCode.API_ERROR,
    message: 'Rate limit exceeded',
    recovery: 'Wait a moment and try again, or check your API usage'
  },
  API_UNAVAILABLE: {
    code: ExitCode.API_ERROR,
    message: 'Anthropic API temporarily unavailable',
    recovery: 'Wait a moment and try again'
  },

  // Timeout errors
  TASK_TIMEOUT: {
    code: ExitCode.TIMEOUT,
    message: 'Task timed out',
    recovery: 'Task may be too complex. Try breaking it into smaller steps.'
  },

  // I/O errors
  FILE_NOT_FOUND: {
    code: ExitCode.IO_ERROR,
    message: 'File not found',
    recovery: 'Check the file path and try again'
  },
  WRITE_FAILED: {
    code: ExitCode.IO_ERROR,
    message: 'Failed to write file',
    recovery: 'Check disk space and permissions'
  },
  READ_FAILED: {
    code: ExitCode.IO_ERROR,
    message: 'Failed to read file',
    recovery: 'Check the file exists and has read permissions'
  },

  // Session errors
  NO_SESSIONS: {
    code: ExitCode.SUCCESS,  // Not really an error
    message: 'No sessions yet',
    recovery: 'Run `cervellaswarm task "..."` to start your first session'
  },
  SESSION_NOT_FOUND: {
    code: ExitCode.GENERAL_ERROR,
    message: 'Session not found',
    recovery: 'Use `cervellaswarm resume --list` to see available sessions'
  },

  // Unknown
  UNKNOWN: {
    code: ExitCode.GENERAL_ERROR,
    message: 'An unexpected error occurred',
    recovery: 'Check the error details and try again'
  }
};

/**
 * Create a CervellaSwarm error with type info
 */
export class CervellaError extends Error {
  constructor(type, details = null) {
    const errorType = ErrorType[type] || ErrorType.UNKNOWN;
    super(errorType.message);
    this.name = 'CervellaError';
    this.type = type;
    this.code = errorType.code;
    this.recovery = errorType.recovery;
    this.details = details;
  }
}

/**
 * Display error to user with recovery suggestion
 */
export function displayError(error) {
  console.log('');

  if (error instanceof CervellaError) {
    console.log(chalk.red(`  Error: ${error.message}`));
    if (error.details) {
      console.log(chalk.gray(`  Details: ${error.details}`));
    }
    console.log('');
    displayRecovery(error.recovery);
  } else {
    // Handle regular errors
    console.log(chalk.red(`  Error: ${error.message || 'Unknown error'}`));
    console.log('');
    console.log(chalk.gray('  If this persists, check your setup and try again.'));
  }

  console.log('');
}

/**
 * Display recovery suggestion(s)
 */
function displayRecovery(recovery) {
  if (!recovery) return;

  if (Array.isArray(recovery)) {
    console.log(chalk.white('  To fix this:'));
    recovery.forEach((step, i) => {
      console.log(chalk.cyan(`  ${i + 1}. ${step}`));
    });
  } else {
    console.log(chalk.cyan(`  ${recovery}`));
  }
}

/**
 * Handle error and exit with appropriate code
 * Use this at the top level of commands
 */
export function handleError(error) {
  displayError(error);

  const exitCode = error instanceof CervellaError
    ? error.code
    : ExitCode.GENERAL_ERROR;

  process.exit(exitCode);
}

/**
 * Wrap an async command with error handling
 * Catches errors and exits with proper code
 */
export function withErrorHandling(fn) {
  return async (...args) => {
    try {
      await fn(...args);
    } catch (error) {
      if (error.name === 'ExitPromptError') {
        // User cancelled with Ctrl+C
        console.log('');
        console.log(chalk.yellow('  Cancelled.'));
        console.log('');
        process.exit(ExitCode.CANCELLED);
      }
      handleError(error);
    }
  };
}

/**
 * Map HTTP status code to ErrorType
 */
export function httpStatusToErrorType(status) {
  const map = {
    401: 'INVALID_API_KEY',
    403: 'API_PERMISSION',
    429: 'RATE_LIMITED',
    500: 'API_UNAVAILABLE',
    503: 'API_UNAVAILABLE'
  };
  return map[status] || 'UNKNOWN';
}

/**
 * Check if an error type is recoverable (retryable)
 */
export function isRetryable(type) {
  return ['RATE_LIMITED', 'API_UNAVAILABLE'].includes(type);
}
