/**
 * Stripe Client Setup
 *
 * Singleton Stripe client with proper configuration.
 *
 * Copyright 2026 Rafa & Cervella
 */

import Stripe from "stripe";

if (!process.env.STRIPE_SECRET_KEY) {
  throw new Error("STRIPE_SECRET_KEY is required");
}

export const stripe = new Stripe(process.env.STRIPE_SECRET_KEY, {
  typescript: true,
});

/**
 * Map Price ID to tier name
 */
export function mapPriceIdToTier(priceId: string): "free" | "pro" | "team" {
  const priceMap: Record<string, "pro" | "team"> = {
    [process.env.STRIPE_PRICE_PRO || ""]: "pro",
    [process.env.STRIPE_PRICE_TEAM || ""]: "team",
  };

  return priceMap[priceId] || "free";
}

/**
 * Get Price ID for tier
 */
export function getTierPriceId(tier: "pro" | "team"): string {
  const tierMap: Record<string, string> = {
    pro: process.env.STRIPE_PRICE_PRO || "",
    team: process.env.STRIPE_PRICE_TEAM || "",
  };

  const priceId = tierMap[tier];
  if (!priceId) {
    throw new Error(`No Price ID configured for tier: ${tier}`);
  }

  return priceId;
}
