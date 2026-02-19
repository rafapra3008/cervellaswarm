/**
 * Update Checker
 *
 * Notifies users when a new version of CervellaSwarm is available.
 * Uses update-notifier for smart, non-intrusive notifications.
 *
 * Best practices implemented:
 * - Check runs in background (zero performance impact)
 * - Cache for 24 hours (no spam)
 * - Delayed notification (check run N, notify run N+1)
 * - Auto-disabled in CI environments
 * - Opt-out via NO_UPDATE_NOTIFIER=1
 *
 * Philosophy: "Keep your tools updated, but never interrupt the flow."
 *
 * Copyright 2026 CervellaSwarm Contributors
 * Licensed under the Apache License, Version 2.0
 * http://www.apache.org/licenses/LICENSE-2.0
 */

import updateNotifier from 'update-notifier';
import { readFileSync } from 'fs';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';

// Get package.json
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

let pkg;
try {
  const pkgPath = join(__dirname, '..', '..', 'package.json');
  pkg = JSON.parse(readFileSync(pkgPath, 'utf8'));
} catch {
  // Fallback if package.json not found
  pkg = { name: 'cervellaswarm', version: '0.0.0' };
}

/**
 * Check for updates and notify if available.
 * Call this at CLI startup - it's non-blocking.
 *
 * @param {Object} options
 * @param {boolean} options.defer - If true, defer notification to end of process (default: false)
 */
export function checkForUpdates(options = {}) {
  // Skip if explicitly disabled
  if (process.env.NO_UPDATE_NOTIFIER === '1') {
    return;
  }

  const notifier = updateNotifier({
    pkg,
    // Check every 24 hours (in milliseconds)
    updateCheckInterval: 1000 * 60 * 60 * 24
  });

  // Notify immediately or defer to process exit
  if (options.defer) {
    // Notify when process exits
    process.on('exit', () => {
      notifier.notify({
        isGlobal: true,
        message: `Update available: {currentVersion} → {latestVersion}
Run {updateCommand} to update

"Un progresso al giorno = stay updated!"`
      });
    });
  } else {
    // Notify now (still non-blocking, uses cached check from previous run)
    notifier.notify({
      isGlobal: true,
      message: `Update available: {currentVersion} → {latestVersion}
Run {updateCommand} to update

"Un progresso al giorno = stay updated!"`
    });
  }
}

/**
 * Get current version
 */
export function getCurrentVersion() {
  return pkg.version;
}

/**
 * Get package name
 */
export function getPackageName() {
  return pkg.name;
}
