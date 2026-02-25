/**
 * Retry utilities for API calls
 *
 * @module @cervellaswarm/core/client
 */

/** Default retry delays in milliseconds */
export const RETRY_DELAYS = [1000, 3000, 5000] as const;

/** Default timeout in milliseconds (10 minutes) */
export const DEFAULT_TIMEOUT = 600000;

/** Default max retries */
export const DEFAULT_MAX_RETRIES = 3;

/**
 * Sleep for a specified number of milliseconds
 */
export function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

/**
 * Add random jitter to a delay to prevent thundering herd
 * when multiple agents retry simultaneously (e.g., after 529 error)
 *
 * @param delay - Base delay in milliseconds
 * @param jitterPercent - Jitter range as decimal (default: 0.25 = ±25%)
 * @returns Delay with random jitter applied
 */
export function addJitter(delay: number, jitterPercent: number = 0.25): number {
  // Random value between -1 and +1
  const random = Math.random() * 2 - 1;
  const jitter = delay * jitterPercent * random;
  return Math.max(0, Math.round(delay + jitter));
}

/**
 * Options for retryable operations
 */
export interface RetryOptions {
  /** Maximum number of retry attempts (default: 3) */
  maxRetries?: number;
  /** Delays between retries in ms (default: [1000, 3000, 5000]) */
  delays?: readonly number[];
  /** Whether to check if error is retryable (default: true) */
  checkRetryable?: boolean;
  /** Custom function to determine if error is retryable */
  isRetryable?: (error: unknown) => boolean;
  /** Callback called on each retry */
  onRetry?: (attempt: number, error: unknown) => void;
}

/**
 * Check if an error is retryable (overloaded, rate limited, etc.)
 */
export function isRetryableError(error: unknown): boolean {
  if (!error || typeof error !== 'object') {
    return false;
  }

  const err = error as { status?: number; message?: string; type?: string };

  // Overloaded (529)
  if (err.status === 529) {
    return true;
  }

  // Rate limited (429)
  if (err.status === 429) {
    return true;
  }

  // Server errors (500-599)
  if (err.status && err.status >= 500 && err.status < 600) {
    return true;
  }

  // Anthropic overloaded error type
  if (err.type === 'overloaded_error') {
    return true;
  }

  // Message-based detection
  if (typeof err.message === 'string') {
    const msg = err.message.toLowerCase();
    if (
      msg.includes('overloaded') ||
      msg.includes('rate limit') ||
      msg.includes('too many requests') ||
      msg.includes('temporarily unavailable')
    ) {
      return true;
    }
  }

  return false;
}

/**
 * Execute a function with automatic retry on retryable errors
 *
 * @example
 * ```ts
 * const result = await withRetry(
 *   () => anthropicClient.messages.create(...),
 *   { maxRetries: 3, onRetry: (attempt) => console.log(`Retry ${attempt}`) }
 * );
 * ```
 */
export async function withRetry<T>(
  fn: () => Promise<T>,
  options: RetryOptions = {}
): Promise<T> {
  const {
    maxRetries = DEFAULT_MAX_RETRIES,
    delays = RETRY_DELAYS,
    checkRetryable = true,
    isRetryable = isRetryableError,
    onRetry,
  } = options;

  let lastError: unknown;

  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error;

      // Check if we should retry
      const shouldRetry =
        attempt < maxRetries && (!checkRetryable || isRetryable(error));

      if (!shouldRetry) {
        throw error;
      }

      // Call onRetry callback if provided
      if (onRetry) {
        onRetry(attempt + 1, error);
      }

      // Wait before retrying (with jitter to prevent thundering herd)
      const baseDelay = delays[Math.min(attempt, delays.length - 1)];
      const delay = addJitter(baseDelay);
      await sleep(delay);
    }
  }

  // This should never be reached, but TypeScript needs it
  throw lastError;
}

/**
 * Execute a function with a timeout
 *
 * @example
 * ```ts
 * const result = await withTimeout(
 *   () => longRunningOperation(),
 *   30000, // 30 seconds
 *   'Operation timed out'
 * );
 * ```
 */
export async function withTimeout<T>(
  fn: () => Promise<T>,
  timeoutMs: number = DEFAULT_TIMEOUT,
  message: string = 'Operation timed out'
): Promise<T> {
  return new Promise((resolve, reject) => {
    const timeoutId = setTimeout(() => {
      reject(new Error(message));
    }, timeoutMs);

    fn()
      .then((result) => {
        clearTimeout(timeoutId);
        resolve(result);
      })
      .catch((error) => {
        clearTimeout(timeoutId);
        reject(error);
      });
  });
}

/**
 * Combine retry and timeout for resilient operations
 *
 * @example
 * ```ts
 * const result = await withRetryAndTimeout(
 *   () => anthropicClient.messages.create(...),
 *   { maxRetries: 3 },
 *   600000 // 10 minutes
 * );
 * ```
 */
export async function withRetryAndTimeout<T>(
  fn: () => Promise<T>,
  retryOptions: RetryOptions = {},
  timeoutMs: number = DEFAULT_TIMEOUT
): Promise<T> {
  return withTimeout(() => withRetry(fn, retryOptions), timeoutMs);
}
