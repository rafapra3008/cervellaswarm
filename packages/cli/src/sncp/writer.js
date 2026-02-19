/**
 * SNCP Writer
 *
 * Writes reports and updates to .sncp folder.
 * Memoria esterna - "MINIMO in memoria, MASSIMO su disco"
 *
 * Copyright 2026 CervellaSwarm Contributors
 * Licensed under the Apache License, Version 2.0
 * http://www.apache.org/licenses/LICENSE-2.0
 */

import { writeFileSync, mkdirSync, existsSync, readFileSync } from 'fs';
import { join } from 'path';

/**
 * Find .sncp directory in current or parent directories
 */
function findSncpDir() {
  let dir = process.cwd();

  for (let i = 0; i < 5; i++) {
    const sncpPath = join(dir, '.sncp');
    if (existsSync(sncpPath)) {
      return sncpPath;
    }
    const parent = join(dir, '..');
    if (parent === dir) break;
    dir = parent;
  }

  // Create .sncp in current directory if not found
  const sncpPath = join(process.cwd(), '.sncp');
  return sncpPath;
}

/**
 * Generate timestamp for filenames
 */
function getTimestamp() {
  const now = new Date();
  return now.toISOString()
    .replace(/[:-]/g, '')
    .replace('T', '_')
    .slice(0, 15);
}

/**
 * Generate human-readable date
 */
function getHumanDate() {
  return new Date().toLocaleDateString('it-IT', {
    day: '2-digit',
    month: 'long',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
}

/**
 * Save task report to .sncp/reports/
 */
export async function saveTaskReport(description, agent, result) {
  try {
    const sncpDir = findSncpDir();
    const reportsDir = join(sncpDir, 'reports', 'tasks');

    // Ensure directories exist
    mkdirSync(reportsDir, { recursive: true });

    // Generate report filename
    const timestamp = getTimestamp();
    const agentShort = agent.replace('cervella-', '');
    const filename = `task_${timestamp}_${agentShort}.json`;
    const filepath = join(reportsDir, filename);

    // Create report object
    const report = {
      timestamp: new Date().toISOString(),
      description: description.trim(),
      agent,
      result: {
        success: result.success,
        duration: result.duration || null,
        filesModified: result.filesModified || [],
        error: result.error || null
      },
      output: result.output ? result.output.slice(0, 5000) : null, // Limit output size
      nextStep: result.nextStep || null
    };

    // Write JSON report
    writeFileSync(filepath, JSON.stringify(report, null, 2));

    // NOTE: stato.md eliminated in SNCP 4.0 (S357). Reports are self-contained.

    console.log(`  Report saved: ${filename}`);
    return filepath;

  } catch (error) {
    // Graceful degradation - don't fail task if report saving fails
    console.log(`  (Could not save report: ${error.message})`);
    return null;
  }
}

/**
 * Save session data for resume functionality
 */
export async function saveSession(sessionData) {
  try {
    const sncpDir = findSncpDir();
    const sessionsDir = join(sncpDir, 'sessions');

    mkdirSync(sessionsDir, { recursive: true });

    const timestamp = getTimestamp();
    const filename = `session_${timestamp}.json`;
    const filepath = join(sessionsDir, filename);

    writeFileSync(filepath, JSON.stringify(sessionData, null, 2));
    return filepath;

  } catch (error) {
    console.log(`  (Could not save session: ${error.message})`);
    return null;
  }
}

/**
 * Append to daily log
 */
export async function appendToDailyLog(message, type = 'info') {
  try {
    const sncpDir = findSncpDir();
    const logsDir = join(sncpDir, 'logs');

    mkdirSync(logsDir, { recursive: true });

    const today = new Date().toISOString().slice(0, 10);
    const logFile = join(logsDir, `daily_${today}.log`);

    const timestamp = new Date().toTimeString().slice(0, 8);
    const logLine = `[${timestamp}] [${type.toUpperCase()}] ${message}\n`;

    // Append to file
    const { appendFileSync } = await import('fs');
    appendFileSync(logFile, logLine);

  } catch (_error) {
    // Silent fail for logging
  }
}
