/**
 * cervellaswarm upgrade
 *
 * Upgrade subscription to Pro or Team tier.
 * Opens Stripe Checkout in browser.
 *
 * Philosophy: "Invest in your tools, multiply your results."
 *
 * Copyright 2026 Rafa & Cervella
 * Licensed under the Apache License, Version 2.0
 */

import chalk from 'chalk';
import { createInterface } from 'readline';
import {
  getBillingApiUrl,
  getEmail,
  setEmail,
  getTier,
  updateSubscriptionData
} from '../config/manager.js';

// Tier info for display
const TIER_INFO = {
  pro: {
    name: 'Pro',
    price: '$29/month',
    calls: 'Unlimited tasks',
    features: ['All 17 agents', 'Priority support', 'Unlimited tasks']
  },
  team: {
    name: 'Team',
    price: '$49/user/month',
    calls: 'Unlimited tasks',
    features: ['All Pro features', 'Team collaboration', 'Shared memory']
  }
};

/**
 * Prompt for email if not set
 */
async function promptEmail() {
  const rl = createInterface({
    input: process.stdin,
    output: process.stdout
  });

  return new Promise((resolve) => {
    rl.question(chalk.cyan('  Enter your email: '), (answer) => {
      rl.close();
      resolve(answer.trim());
    });
  });
}

/**
 * Open URL in browser (cross-platform)
 */
async function openBrowser(url) {
  const { default: open } = await import('open');
  await open(url);
}

/**
 * Poll for payment completion
 */
async function pollPaymentStatus(email, maxAttempts = 60) {
  const apiUrl = getBillingApiUrl();

  console.log('');
  console.log(chalk.gray('  Waiting for payment confirmation...'));
  console.log(chalk.gray('  (This will update automatically when complete)'));
  console.log('');

  for (let i = 0; i < maxAttempts; i++) {
    await new Promise(resolve => setTimeout(resolve, 3000)); // 3s

    try {
      const response = await fetch(
        `${apiUrl}/api/subscription/by-email/${encodeURIComponent(email)}`
      );
      const data = await response.json();

      if (data.tier && data.tier !== 'free') {
        // Payment confirmed!
        updateSubscriptionData(data);

        console.log('');
        console.log(chalk.green.bold('  ' + '='.repeat(50)));
        console.log(chalk.green.bold('  UPGRADE SUCCESSFUL!'));
        console.log(chalk.green.bold('  ' + '='.repeat(50)));
        console.log('');
        console.log(chalk.white(`  Tier: ${chalk.cyan.bold(data.tier.toUpperCase())}`));
        console.log(chalk.white(`  Email: ${chalk.gray(data.email)}`));
        console.log('');
        console.log(chalk.green('  Thank you for supporting CervellaSwarm!'));
        console.log('');

        return true;
      }
    } catch {
      // Network error, continue polling
    }

    // Show progress dot
    process.stdout.write(chalk.gray('.'));
  }

  console.log('');
  console.log('');
  console.log(chalk.yellow('  Payment timeout. If you completed the payment,'));
  console.log(chalk.yellow('  run `cervellaswarm billing` to check your status.'));
  console.log('');

  return false;
}

/**
 * Main upgrade command
 */
export async function upgradeCommand(tier, options) {
  try {
    // Validate tier
    if (!tier || !['pro', 'team'].includes(tier.toLowerCase())) {
      console.log('');
      console.log(chalk.red('  Invalid tier. Choose "pro" or "team".'));
      console.log('');
      console.log(chalk.white.bold('  Available tiers:'));
      console.log('');
      console.log(chalk.cyan('  pro   ') + chalk.gray('$29/mo - 17 agents, unlimited tasks'));
      console.log(chalk.cyan('  team  ') + chalk.gray('$49/user/mo - 17 agents, shared memory'));
      console.log('');
      console.log(chalk.gray('  Usage: cervellaswarm upgrade <pro|team>'));
      console.log('');
      process.exit(1);
    }

    const tierKey = tier.toLowerCase();
    const tierData = TIER_INFO[tierKey];
    const currentTier = getTier();

    // Check if already on this tier or higher
    if (currentTier === tierKey) {
      console.log('');
      console.log(chalk.yellow(`  You're already on the ${tierData.name} tier.`));
      console.log(chalk.gray('  Run `cervellaswarm billing` to manage your subscription.'));
      console.log('');
      return;
    }

    if (currentTier === 'team' && tierKey === 'pro') {
      console.log('');
      console.log(chalk.yellow('  You\'re on Team tier. To downgrade, use `cervellaswarm billing`.'));
      console.log('');
      return;
    }

    // Display upgrade info
    console.log('');
    console.log(chalk.cyan.bold('  ' + '='.repeat(50)));
    console.log(chalk.cyan.bold(`  UPGRADE TO ${tierData.name.toUpperCase()}`));
    console.log(chalk.cyan.bold('  ' + '='.repeat(50)));
    console.log('');
    console.log(chalk.white(`  Price: ${chalk.green.bold(tierData.price)}`));
    console.log(chalk.white(`  Quota: ${chalk.cyan(tierData.calls)}`));
    console.log('');
    console.log(chalk.white.bold('  Features:'));
    tierData.features.forEach(f => {
      console.log(chalk.green(`    + ${f}`));
    });
    console.log('');

    // Get email
    let email = getEmail();
    if (!email) {
      email = await promptEmail();
      if (!email || !email.includes('@')) {
        console.log(chalk.red('  Invalid email. Please try again.'));
        process.exit(1);
      }
      setEmail(email);
    } else {
      console.log(chalk.gray(`  Using email: ${email}`));
      console.log(chalk.gray('  (Change with --email flag)'));
    }

    // Override email if provided
    if (options.email) {
      email = options.email;
      setEmail(email);
    }

    console.log('');
    console.log(chalk.white('  Opening Stripe Checkout...'));

    // Call API to create checkout session
    const apiUrl = getBillingApiUrl();
    const response = await fetch(`${apiUrl}/api/create-checkout-session`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ tier: tierKey, email })
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Failed to create checkout session');
    }

    const { url } = await response.json();

    // Open browser
    await openBrowser(url);

    console.log(chalk.green('  Browser opened!'));
    console.log('');
    console.log(chalk.gray('  Complete the payment in your browser.'));

    // Poll for completion
    await pollPaymentStatus(email);

  } catch (error) {
    console.log('');
    console.log(chalk.red(`  Error: ${error.message}`));
    console.log('');

    if (error.message.includes('fetch')) {
      console.log(chalk.yellow('  Could not connect to billing server.'));
      console.log(chalk.gray('  Check your internet connection and try again.'));
    }

    process.exit(1);
  }
}
