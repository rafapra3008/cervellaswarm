/**
 * Checkout Session Route
 *
 * Creates Stripe Checkout Session for subscription.
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

/**
 * POST /api/create-checkout-session
 *
 * Creates a Stripe Checkout Session for the specified tier.
 * Returns the checkout URL for the CLI to open in browser.
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
    // Use our API URL for success/cancel pages (they exist!)
    const apiUrl = process.env.API_URL || "https://cervellaswarm-api.fly.dev";

    // Create Checkout Session
    const session = await stripe.checkout.sessions.create({
      mode: "subscription",
      payment_method_types: ["card"],
      line_items: [
        {
          price: priceId,
          quantity: 1,
        },
      ],
      customer_email: email,
      client_reference_id: email, // Used to identify user in webhook
      metadata: {
        tier, // Useful in webhook
        source: "cli",
      },
      success_url: `${apiUrl}/success?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${apiUrl}/cancel`,
      // Automatic tax if configured
      // automatic_tax: { enabled: true },
    });

    res.json({
      url: session.url,
      sessionId: session.id,
    });
  } catch (error) {
    console.error("Checkout session error:", error);

    if (error instanceof Error) {
      res.status(500).json({ error: error.message });
    } else {
      res.status(500).json({ error: "Failed to create checkout session" });
    }
  }
});

export default router;
