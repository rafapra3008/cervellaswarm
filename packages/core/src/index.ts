/**
 * @cervellaswarm/core
 *
 * Core utilities shared between CLI and MCP Server
 *
 * @example
 * ```ts
 * import { withRetry, parseError } from '@cervellaswarm/core/client';
 * import { getAvailableWorkers } from '@cervellaswarm/core/workers';
 * ```
 */

// Re-export all modules
export * from './client/index.js';
export * from './config/index.js';
export * from './workers/index.js';

// Package info
export const VERSION = '1.0.0-alpha.1';
export const PACKAGE_NAME = '@cervellaswarm/core';
