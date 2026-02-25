/**
 * Error handling utilities
 *
 * @module @cervellaswarm/core/client
 */

/**
 * User-friendly error messages mapped by status code
 */
export const ERROR_MESSAGES: Record<number, string> = {
  400: 'Invalid request. Please check your input.',
  401: 'Authentication failed. Please check your API key.',
  403: 'Access denied. Your API key may not have permission for this operation.',
  404: 'Resource not found.',
  429: 'Rate limit exceeded. Please wait and try again.',
  500: 'Server error. Please try again later.',
  529: 'Service is temporarily overloaded. Please try again in a moment.',
};

/**
 * Detailed error information
 */
export interface ErrorInfo {
  /** HTTP status code (if applicable) */
  status?: number;
  /** User-friendly message */
  message: string;
  /** Whether the error is retryable */
  retryable: boolean;
  /** Original error */
  original?: unknown;
  /** Suggested action for the user */
  suggestion?: string;
}

/**
 * Parse an error and return user-friendly information
 */
export function parseError(error: unknown): ErrorInfo {
  // Handle null/undefined
  if (!error) {
    return {
      message: 'An unknown error occurred.',
      retryable: false,
    };
  }

  // Handle Error objects
  if (error instanceof Error) {
    const err = error as Error & { status?: number; type?: string };

    // Anthropic API errors
    if (err.status) {
      const status = err.status;
      const retryable = status === 429 || status === 529 || status >= 500;
      const message =
        ERROR_MESSAGES[status] || err.message || 'An error occurred.';

      return {
        status,
        message,
        retryable,
        original: error,
        suggestion: getSuggestion(status),
      };
    }

    // Generic Error
    return {
      message: err.message || 'An error occurred.',
      retryable: false,
      original: error,
    };
  }

  // Handle objects with status
  if (typeof error === 'object') {
    const obj = error as { status?: number; message?: string };

    if (obj.status) {
      const status = obj.status;
      const retryable = status === 429 || status === 529 || status >= 500;
      const message =
        ERROR_MESSAGES[status] ||
        obj.message ||
        'An error occurred.';

      return {
        status,
        message,
        retryable,
        original: error,
        suggestion: getSuggestion(status),
      };
    }

    if (obj.message) {
      return {
        message: obj.message,
        retryable: false,
        original: error,
      };
    }
  }

  // Fallback for strings
  if (typeof error === 'string') {
    return {
      message: error,
      retryable: false,
    };
  }

  // Unknown error type
  return {
    message: 'An unexpected error occurred.',
    retryable: false,
    original: error,
  };
}

/**
 * Get a suggestion based on error status
 */
function getSuggestion(status: number): string | undefined {
  switch (status) {
    case 401:
      return 'Run "cervellaswarm config" to update your API key.';
    case 403:
      return 'Check that your Claude subscription is active.';
    case 429:
      return 'Wait a few seconds and try again.';
    case 529:
      return 'The service is busy. Wait a moment and retry.';
    default:
      return undefined;
  }
}

/**
 * Format an error for display to the user
 */
export function formatError(error: unknown): string {
  const info = parseError(error);

  let result = info.message;

  if (info.suggestion) {
    result += `\n${info.suggestion}`;
  }

  if (info.retryable) {
    result += '\n(This error is temporary - you can retry)';
  }

  return result;
}

/**
 * CervellaSwarm custom error class
 */
export class CervellaSwarmError extends Error {
  public readonly status?: number;
  public readonly retryable: boolean;
  public readonly suggestion?: string;

  constructor(info: ErrorInfo) {
    super(info.message);
    this.name = 'CervellaSwarmError';
    this.status = info.status;
    this.retryable = info.retryable;
    this.suggestion = info.suggestion;
  }

  /**
   * Create from any error
   */
  static from(error: unknown): CervellaSwarmError {
    if (error instanceof CervellaSwarmError) {
      return error;
    }
    const info = parseError(error);
    return new CervellaSwarmError(info);
  }
}
