/**
 * cervellaswarm resume
 *
 * Resume from last session.
 * Shows recap based on time since last session.
 * No judgment, no pressure - just helpful context.
 *
 * Philosophy: "Welcome back! Let's continue from where we were."
 *
 * Copyright 2026 Rafa & Cervella
 * Licensed under the Apache License, Version 2.0
 * http://www.apache.org/licenses/LICENSE-2.0
 */

import chalk from 'chalk';
import { loadProjectContext } from '../sncp/loader.js';
import { loadSessions, getLastSession, loadSession, formatSessionSummary } from '../session/manager.js';
import { generateRecap } from '../display/recap.js';
import { CervellaError, displayError } from '../utils/errors.js';

export async function resumeCommand(options) {
  try {
    // Load project context
    const context = await loadProjectContext();

    if (!context) {
      const error = new CervellaError('NOT_INITIALIZED');
      displayError(error);
      process.exit(error.code);
    }

    // List sessions if requested
    if (options.list) {
      const sessions = await loadSessions();
      console.log('');
      if (sessions.length === 0) {
        console.log(chalk.gray('  No sessions yet.'));
        console.log(chalk.white('  Run `cervellaswarm task "..."` to start.'));
      } else {
        console.log(chalk.cyan.bold('  Recent Sessions:'));
        console.log('');
        sessions.slice(0, 10).forEach((session, i) => {
          console.log(chalk.gray(`  ${i + 1}. ${formatSessionSummary(session)}`));
        });
      }
      console.log('');
      return;
    }

    // Get last session
    const lastSession = options.session
      ? await loadSession(options.session)
      : await getLastSession();

    if (!lastSession) {
      console.log('');
      console.log(chalk.cyan('  This is your first session!'));
      console.log(chalk.white('  Run `cervellaswarm task "your task"` to start.'));
      console.log('');
      return;
    }

    // Calculate time since last session
    const daysSince = calculateDaysSince(lastSession.date);

    // Generate appropriate recap (based on time)
    console.log('');
    console.log(chalk.cyan.bold('  Welcome back!'));
    console.log('');

    // Show recap (level based on time, but NO judgment)
    const recap = await generateRecap(context, lastSession, daysSince);
    console.log(recap);

    // Encouraging close (no time pressure!)
    console.log('');
    console.log(chalk.green('  Ready to take the next step?'));
    console.log(chalk.gray('  Run `cervellaswarm task "..."` when you\'re ready.'));
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

function calculateDaysSince(dateString) {
  const lastDate = new Date(dateString);
  const now = new Date();
  const diffTime = Math.abs(now - lastDate);
  return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
}
