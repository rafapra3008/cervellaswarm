/**
 * UX Messages for CervellaSwarm Billing
 *
 * User-friendly messages for quota warnings and limits.
 * Designed to be helpful, not aggressive.
 *
 * Copyright 2026 CervellaSwarm Contributors
 * Licensed under the Apache License, Version 2.0
 */
import { TIER_NAMES, TIER_LIMITS, TIER_PRICES, getUpgradeTier, getUpgradeUrl, } from "./tiers.js";
/**
 * Format date for display
 */
function formatResetDate(isoDate) {
    const date = new Date(isoDate);
    return date.toLocaleDateString("en-US", {
        month: "long",
        day: "numeric",
        year: "numeric",
    });
}
/**
 * Get warning message (shown at 80% usage)
 */
export function getWarningMessage(tier, used, limit) {
    const remaining = limit - used;
    const nextTier = getUpgradeTier(tier);
    let message = `You're running low on API calls.\n`;
    message += `Used: ${used}/${limit} (${remaining} remaining)\n\n`;
    if (nextTier) {
        const nextLimit = TIER_LIMITS[nextTier];
        const nextPrice = TIER_PRICES[nextTier];
        message += `Upgrade to ${TIER_NAMES[nextTier]} for ${nextLimit} calls/month ($${nextPrice}/mo).\n`;
        message += `${getUpgradeUrl(tier)}`;
    }
    return message;
}
/**
 * Get limit exceeded message (shown at 100%)
 */
export function getLimitExceededMessage(tier, limit, resetsAt) {
    const nextTier = getUpgradeTier(tier);
    const resetDate = formatResetDate(resetsAt);
    let message = `Monthly limit reached.\n\n`;
    message += `You've used all ${limit} calls for ${TIER_NAMES[tier]} plan.\n`;
    message += `Your quota resets on ${resetDate}.\n\n`;
    if (nextTier) {
        const nextLimit = TIER_LIMITS[nextTier];
        const nextPrice = TIER_PRICES[nextTier];
        message += `Upgrade to ${TIER_NAMES[nextTier]} for ${nextLimit} calls/month ($${nextPrice}/mo):\n`;
        message += `${getUpgradeUrl(tier)}\n\n`;
        message += `Or wait until ${resetDate} for your quota to reset.`;
    }
    else {
        message += `Contact us for custom Enterprise plans:\n`;
        message += `https://cervellaswarm.com/contact`;
    }
    return message;
}
/**
 * Get usage status message (for check_usage tool)
 */
export function getUsageStatusMessage(tier, used, limit, resetsAt) {
    const remaining = limit - used;
    const percentage = Math.round((used / limit) * 100);
    const resetDate = formatResetDate(resetsAt);
    let message = `# CervellaSwarm Usage\n\n`;
    message += `**Plan:** ${TIER_NAMES[tier]}\n`;
    message += `**Usage:** ${used}/${limit} calls (${percentage}%)\n`;
    message += `**Remaining:** ${remaining} calls\n`;
    message += `**Resets:** ${resetDate}\n`;
    // Progress bar
    const barLength = 20;
    const filled = Math.round((used / limit) * barLength);
    const empty = barLength - filled;
    const bar = "█".repeat(filled) + "░".repeat(empty);
    message += `\n\`[${bar}]\` ${percentage}%\n`;
    // Status indicator
    if (percentage >= 100) {
        message += `\n⛔ **Limit reached** - Upgrade or wait for reset.\n`;
    }
    else if (percentage >= 80) {
        message += `\n⚠️ **Running low** - Consider upgrading.\n`;
    }
    else {
        message += `\n✅ **Good standing**\n`;
    }
    // Upgrade suggestion if not enterprise
    const nextTier = getUpgradeTier(tier);
    if (nextTier && percentage >= 50) {
        const nextLimit = TIER_LIMITS[nextTier];
        const nextPrice = TIER_PRICES[nextTier];
        message += `\n---\n`;
        message += `**Upgrade to ${TIER_NAMES[nextTier]}:** ${nextLimit} calls/month for $${nextPrice}/mo\n`;
        message += `${getUpgradeUrl(tier)}`;
    }
    return message;
}
/**
 * Get first-time welcome message
 */
export function getWelcomeMessage(tier) {
    const limit = TIER_LIMITS[tier];
    return (`Welcome to CervellaSwarm!\n\n` +
        `You're on the ${TIER_NAMES[tier]} plan with ${limit} calls/month.\n` +
        `Use \`check_status\` anytime to see your usage.`);
}
//# sourceMappingURL=messages.js.map