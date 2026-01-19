/**
 * Subscription Status Route
 *
 * Returns current subscription status for CLI sync.
 * CLI polls this to verify tier after payment.
 *
 * Copyright 2026 Rafa & Cervella
 */

import { Router, Request, Response } from "express";
import { getSubscription, getSubscriptionByEmail } from "../db/index.js";

const router = Router();

/**
 * GET /api/subscription/:customerId
 *
 * Get subscription status by customer ID.
 * Used by CLI for periodic sync.
 */
router.get("/subscription/:customerId", async (req: Request, res: Response) => {
  try {
    const customerId = req.params.customerId as string;

    const subscription = await getSubscription(customerId);

    if (!subscription) {
      res.json({
        tier: "free",
        status: "none",
        message: "No subscription found",
      });
      return;
    }

    res.json({
      tier: subscription.tier,
      status: subscription.status,
      customerId: subscription.customerId,
      subscriptionId: subscription.subscriptionId,
      currentPeriodEnd: subscription.currentPeriodEnd,
      email: subscription.email,
    });
  } catch (error) {
    console.error("Subscription lookup error:", error);
    res.status(500).json({ error: "Failed to fetch subscription" });
  }
});

/**
 * GET /api/subscription/by-email/:email
 *
 * Get subscription status by email.
 * Used by CLI after checkout to find new customer ID.
 */
router.get("/subscription/by-email/:email", async (req: Request, res: Response) => {
  try {
    const email = req.params.email as string;

    if (!email || !email.includes("@")) {
      res.status(400).json({ error: "Valid email is required" });
      return;
    }

    const subscription = await getSubscriptionByEmail(decodeURIComponent(email));

    if (!subscription) {
      res.json({
        tier: "free",
        status: "none",
        message: "No subscription found for this email",
      });
      return;
    }

    res.json({
      tier: subscription.tier,
      status: subscription.status,
      customerId: subscription.customerId,
      subscriptionId: subscription.subscriptionId,
      currentPeriodEnd: subscription.currentPeriodEnd,
      email: subscription.email,
    });
  } catch (error) {
    console.error("Subscription lookup error:", error);
    res.status(500).json({ error: "Failed to fetch subscription" });
  }
});

export default router;
