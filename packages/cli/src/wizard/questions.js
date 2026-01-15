/**
 * Wizard Questions
 *
 * The 10 strategic questions that create the project constitution.
 * Based on WIZARD_INIZIALE_STUDIO.md research.
 *
 * Philosophy: "Define once, never re-explain."
 */

import { input, select, checkbox, confirm } from '@inquirer/prompts';
import chalk from 'chalk';

export async function runWizard() {
  const answers = {};

  // Progress indicator
  const showProgress = (current, total) => {
    const filled = Math.floor((current / total) * 20);
    const empty = 20 - filled;
    const bar = '█'.repeat(filled) + '░'.repeat(empty);
    console.log(chalk.gray(`  [${current}/${total}] ${bar}`));
    console.log('');
  };

  // QUESTION 1: Project Name
  showProgress(1, 10);
  answers.projectName = await input({
    message: 'Project name:',
    default: process.cwd().split('/').pop(),
    validate: (value) => {
      if (!/^[a-z0-9-]+$/.test(value)) {
        return 'Use lowercase letters, numbers, and hyphens only';
      }
      return true;
    }
  });

  // QUESTION 2: Description
  showProgress(2, 10);
  answers.description = await input({
    message: 'Brief description (1-2 sentences):',
    validate: (value) => value.length > 0 || 'Please enter a description'
  });

  // QUESTION 3: Project Type
  showProgress(3, 10);
  answers.projectType = await select({
    message: 'Project type:',
    choices: [
      { name: 'Web Application (frontend + backend)', value: 'webapp' },
      { name: 'API / Backend Service', value: 'api' },
      { name: 'CLI Tool', value: 'cli' },
      { name: 'Library / Package', value: 'library' },
      { name: 'Mobile App', value: 'mobile' },
      { name: 'Data Analysis', value: 'data' },
      { name: 'Other', value: 'other' }
    ]
  });

  // QUESTION 4: Main Goal
  showProgress(4, 10);
  console.log(chalk.gray('  What problem does this project solve?'));
  console.log(chalk.gray('  What\'s the end goal?'));
  console.log('');
  answers.mainGoal = await input({
    message: 'Main goal:',
    validate: (value) => value.length > 0 || 'Please describe your main goal'
  });

  // QUESTION 5: Success Criteria
  showProgress(5, 10);
  answers.successCriteria = await checkbox({
    message: 'How will you know the project succeeded?',
    choices: [
      { name: 'Users actively using it', value: 'users' },
      { name: 'Revenue / profit generated', value: 'revenue' },
      { name: 'Problem personally solved', value: 'personal' },
      { name: 'Portfolio / learning completed', value: 'portfolio' },
      { name: 'Open source adoption', value: 'opensource' }
    ]
  });

  // QUESTION 6: Timeline (but no pressure!)
  showProgress(6, 10);
  answers.timeline = await select({
    message: 'What pace feels right for this project?',
    choices: [
      { name: 'Quick prototype (exploring ideas)', value: 'prototype' },
      { name: 'MVP (building something real)', value: 'mvp' },
      { name: 'Full product (comprehensive)', value: 'full' },
      { name: 'Long-term (no rush, steady progress)', value: 'longterm' },
      { name: 'Exploratory (see where it goes)', value: 'exploratory' }
    ]
  });

  // QUESTION 7: Tech Stack
  showProgress(7, 10);
  const knowsStack = await confirm({
    message: 'Do you already know what technologies you\'ll use?',
    default: true
  });

  if (knowsStack) {
    answers.techStack = await input({
      message: 'Tech stack (comma-separated):',
      default: ''
    });
  } else {
    answers.techStackLevel = await select({
      message: 'What\'s your comfort level?',
      choices: [
        { name: 'Beginner (need recommendations)', value: 'beginner' },
        { name: 'Intermediate (open to suggestions)', value: 'intermediate' },
        { name: 'Expert (I\'ll decide as I go)', value: 'expert' }
      ]
    });
  }

  // QUESTION 8: Working Mode
  showProgress(8, 10);
  answers.workingMode = await select({
    message: 'How are you working on this?',
    choices: [
      { name: 'Solo (just you + the AI team)', value: 'solo' },
      { name: 'Small team (2-5 people)', value: 'small' },
      { name: 'Larger team (5+ people)', value: 'large' }
    ]
  });

  // QUESTION 9: Session Preference
  showProgress(9, 10);
  answers.sessionLength = await select({
    message: 'Typical session length for you?',
    choices: [
      { name: 'Short sessions (30-60 min)', value: 'short' },
      { name: 'Medium sessions (1-2 hours)', value: 'medium' },
      { name: 'Long sessions (2+ hours)', value: 'long' },
      { name: 'Variable (depends on the day)', value: 'variable' }
    ]
  });

  // QUESTION 10: Notification Style
  showProgress(10, 10);
  answers.notificationStyle = await select({
    message: 'How verbose should updates be?',
    choices: [
      { name: 'Minimal (errors only)', value: 'minimal' },
      { name: 'Standard (important updates)', value: 'standard' },
      { name: 'Verbose (every step visible)', value: 'verbose' }
    ]
  });

  return answers;
}
