/**
 * Config Manager - DEPRECATED
 *
 * This file is kept for backward compatibility.
 * All functionality has been split into separate modules:
 * - schema.js: Config schema and singleton
 * - api-key.js: API key management
 * - settings.js: Model, preferences, bulk operations
 * - diagnostics.js: Health checks and validation
 * - billing.js: Subscription and tier management
 *
 * Import from './config/index.js' instead.
 *
 * Copyright 2026 CervellaSwarm Contributors
 * Licensed under the Apache License, Version 2.0
 */

// Re-export everything from index for backward compatibility
export * from './index.js';
