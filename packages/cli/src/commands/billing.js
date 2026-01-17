/**
 * cervellaswarm billing
 *
 * Manage billing and subscription.
 * Opens Stripe Customer Portal for self-service.
 *
 * Philosophy: "Full control over your subscription."
 *
 * Copyright 2026 Rafa & Cervella
 * Licensed under the Apache License, Version 2.0
 */

import chalk from 'chalk';
import {
  getBillingApiUrl,
  getCustomerId,
  getEmail,
  getSubscriptionInfo,
  updateSubscriptionData,
  needsSync
} from '../config/manager.js';

// Tier limits for display
const TIER_LIMITS = {
  free: 50,
  pro: 500,
  team: 1000,
  enterprise: 'Unlimited'
};

/**
 * Open URL in browser (cross-platform)
 */
async function openBrowser(url) {
  const { default: open } = await import('open');
  await open(url);
}

/**
 * Sync subscription status from API
 */
async function syncSubscription() {
  const customerId = getCustomerId();
  const email = getEmail();

  if (!customerId && !email) {
    return null;
  }

  const apiUrl = getBillingApiUrl();

  try {
    let response;
    if (customerId) {
      response = await fetch(`${apiUrl}/api/subscription/${customerId}`);
    } else if (email) {
      response = await fetch(`${apiUrl}/api/subscription/by-email/${encodeURIComponent(email)}`);
    }

    if (response && response.ok) {
      const data = await response.json();
      if (data.tier) {
        updateSubscriptionData(data);
        return data;
      }
    }
  } catch {
    // Network error, use cached data
  }

  return null;
}

/**
 * Display current subscription status
 */
function displayStatus(info) {
  const tier = info.tier || 'free';
  const limit = TIER_LIMITS[tier];

  console.log('');
  console.log(chalk.cyan.bold('  ' + '='.repeat(50)));
  console.log(chalk.cyan.bold('  SUBSCRIPTION STATUS'));
  console.log(chalk.cyan.bold('  ' + '='.repeat(50)));
  console.log('');

  // Tier badge
  const tierColors = {
    free: chalk.gray,
    pro: chalk.cyan,
    team: chalk.green,
    enterprise: chalk.magenta
  };
  const tierColor = tierColors[tier] || chalk.white;
  console.log(chalk.white('  Current Tier: ') + tierColor.bold(tier.toUpperCase()));
  console.log(chalk.white('  Monthly Limit: ') + chalk.cyan(`${limit} calls`));

  if (info.email) {
    console.log(chalk.white('  Email: ') + chalk.gray(info.email));
  }

  if (info.lastSync) {
    const lastSyncDate = new Date(info.lastSync);
    console.log(chalk.white('  Last Sync: ') + chalk.gray(lastSyncDate.toLocaleString()));
  }

  console.log('');
}

/**
 * Main billing command
 */
export async function billingCommand(options) {
  try {
    // Get current subscription info
    let info = getSubscriptionInfo();

    // Sync if needed or forced
    if (options.sync || needsSync()) {
      console.log(chalk.gray('  Syncing subscription status...'));
      const synced = await syncSubscription();
      if (synced) {
        info = getSubscriptionInfo();
      }
    }

    // Show status if requested
    if (options.status) {
      displayStatus(info);
      return;
    }

    // If no customer ID, show status and upgrade prompt
    const customerId = getCustomerId();
    if (!customerId) {
      displayStatus(info);

      console.log(chalk.yellow('  No active subscription found.'));
      console.log('');
      console.log(chalk.white.bold('  Upgrade options:'));
      console.log('');
      console.log(chalk.cyan('  cervellaswarm upgrade pro   ') + chalk.gray('$20/mo - 500 calls'));
      console.log(chalk.cyan('  cervellaswarm upgrade team  ') + chalk.gray('$35/mo - 1000 calls'));
      console.log('');
      return;
    }

    // Open Stripe Customer Portal
    console.log('');
    console.log(chalk.white('  Opening billing portal...'));

    const apiUrl = getBillingApiUrl();
    const response = await fetch(`${apiUrl}/api/create-portal-session`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ customerId })
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Failed to create portal session');
    }

    const { url } = await response.json();

    // Open browser
    await openBrowser(url);

    console.log(chalk.green('  Browser opened!'));
    console.log('');
    console.log(chalk.gray('  In the portal you can:'));
    console.log(chalk.gray('    - Update payment method'));
    console.log(chalk.gray('    - Change plan (upgrade/downgrade)'));
    console.log(chalk.gray('    - Cancel subscription'));
    console.log(chalk.gray('    - View invoices'));
    console.log('');

  } catch (error) {
    console.log('');
    console.log(chalk.red(`  Error: ${error.message}`));
    console.log('');

    if (error.message.includes('fetch') || error.message.includes('Failed')) {
      console.log(chalk.yellow('  Could not connect to billing server.'));
      console.log(chalk.gray('  Check your internet connection and try again.'));
      console.log('');
      console.log(chalk.gray('  Showing cached subscription info:'));
      displayStatus(getSubscriptionInfo());
    }

    process.exit(1);
  }
}
