/**
 * Checkout Route
 *
 * Creates Stripe Payment Link for subscription.
 * Uses Payment Links API (more reliable than Checkout Sessions).
 * CLI calls this, user completes payment in browser.
 *
 * Copyright 2026 Rafa & Cervella
 */

import { Router, Request, Response } from "express";
import { stripe, getTierPriceId } from "../utils/stripe.js";

const router = Router();

interface CheckoutRequest {
  tier: "pro" | "team";
  email: string;
}

// Cache for payment links (they're reusable)
const paymentLinkCache: Record<string, string> = {};

/**
 * POST /api/create-checkout-session
 *
 * Creates or retrieves a Stripe Payment Link for the specified tier.
 * Returns the payment URL for the CLI to open in browser.
 */
router.post("/create-checkout-session", async (req: Request, res: Response) => {
  try {
    const { tier, email } = req.body as CheckoutRequest;

    // Validate input
    if (!tier || !["pro", "team"].includes(tier)) {
      res.status(400).json({ error: "Invalid tier. Must be 'pro' or 'team'" });
      return;
    }

    if (!email || !email.includes("@")) {
      res.status(400).json({ error: "Valid email is required" });
      return;
    }

    const priceId = getTierPriceId(tier);

    // Check cache first
    if (paymentLinkCache[tier]) {
      res.json({
        url: paymentLinkCache[tier],
        tier,
        note: "Payment Link - complete payment to activate subscription",
      });
      return;
    }

    // Create Payment Link (more reliable than Checkout Sessions)
    const paymentLink = await stripe.paymentLinks.create({
      line_items: [
        {
          price: priceId,
          quantity: 1,
        },
      ],
      metadata: {
        tier,
        source: "cli",
      },
      // Allow customer to adjust quantity? No for subscriptions
      // after_completion handled by webhook
    });

    // Cache for future use
    paymentLinkCache[tier] = paymentLink.url;

    res.json({
      url: paymentLink.url,
      tier,
      note: "Payment Link - complete payment to activate subscription",
    });
  } catch (error) {
    console.error("Payment link error:", error);

    if (error instanceof Error) {
      res.status(500).json({ error: error.message });
    } else {
      res.status(500).json({ error: "Failed to create payment link" });
    }
  }
});

export default router;
