/**
 * Session Manager
 *
 * Manages session history and resumption.
 * Stores sessions in .sncp/sessions/ as JSON files.
 *
 * Philosophy: "Welcome back! Here's where we were."
 *
 * Copyright 2026 Rafa & Cervella
 * Licensed under the Apache License, Version 2.0
 * http://www.apache.org/licenses/LICENSE-2.0
 */

import { readdirSync, readFileSync, writeFileSync, mkdirSync, existsSync } from 'fs';
import { join, basename } from 'path';

/**
 * Find .sncp directory
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

  return join(process.cwd(), '.sncp');
}

/**
 * Get sessions directory path
 */
function getSessionsDir() {
  const sncpDir = findSncpDir();
  const sessionsDir = join(sncpDir, 'sessions');

  // Ensure directory exists
  if (!existsSync(sessionsDir)) {
    mkdirSync(sessionsDir, { recursive: true });
  }

  return sessionsDir;
}

/**
 * Load all sessions, sorted by date (newest first)
 */
export async function loadSessions() {
  try {
    const sessionsDir = getSessionsDir();
    const files = readdirSync(sessionsDir)
      .filter(f => f.endsWith('.json'))
      .sort()
      .reverse(); // Newest first

    const sessions = [];

    for (const file of files.slice(0, 50)) { // Limit to last 50
      try {
        const filepath = join(sessionsDir, file);
        const content = readFileSync(filepath, 'utf8');
        const session = JSON.parse(content);
        session.id = basename(file, '.json');
        sessions.push(session);
      } catch {
        // Skip invalid files
      }
    }

    return sessions;

  } catch (_error) {
    return [];
  }
}

/**
 * Get the most recent session
 */
export async function getLastSession() {
  const sessions = await loadSessions();
  return sessions.length > 0 ? sessions[0] : null;
}

/**
 * Load a specific session by ID
 */
export async function loadSession(id) {
  try {
    const sessionsDir = getSessionsDir();

    // Try exact match first
    let filepath = join(sessionsDir, `${id}.json`);

    if (!existsSync(filepath)) {
      // Try to find by partial ID
      const files = readdirSync(sessionsDir).filter(f => f.includes(id));
      if (files.length > 0) {
        filepath = join(sessionsDir, files[0]);
      } else {
        return null;
      }
    }

    const content = readFileSync(filepath, 'utf8');
    const session = JSON.parse(content);
    session.id = basename(filepath, '.json');
    return session;

  } catch {
    return null;
  }
}

/**
 * Save a new session
 */
export async function saveSession(sessionData) {
  try {
    const sessionsDir = getSessionsDir();

    // Generate session ID from timestamp
    const timestamp = new Date().toISOString()
      .replace(/[:-]/g, '')
      .replace('T', '_')
      .slice(0, 15);
    const id = `session_${timestamp}`;

    const session = {
      ...sessionData,
      date: new Date().toISOString(),
      id
    };

    const filepath = join(sessionsDir, `${id}.json`);
    writeFileSync(filepath, JSON.stringify(session, null, 2));

    return session;

  } catch (error) {
    console.log(`  (Could not save session: ${error.message})`);
    return null;
  }
}

/**
 * Create a session from task execution
 */
export async function createTaskSession(description, agent, result) {
  const session = {
    type: 'task',
    summary: description.slice(0, 100),
    agent,
    success: result.success,
    duration: result.duration || null,
    filesModified: result.filesModified || [],
    nextStep: result.nextStep || null
  };

  return await saveSession(session);
}

/**
 * Get session summary for display
 */
export function formatSessionSummary(session) {
  const date = new Date(session.date);
  const dateStr = date.toLocaleDateString('it-IT', {
    day: '2-digit',
    month: 'short',
    hour: '2-digit',
    minute: '2-digit'
  });

  const status = session.success ? 'OK' : 'ERR';
  const summary = session.summary || 'No description';

  return `${dateStr} [${status}] ${summary}`;
}
