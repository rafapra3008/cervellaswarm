/**
 * Customer Portal Route
 *
 * Creates Stripe Customer Portal session for self-service billing.
 * Users can update payment method, change plan, cancel, etc.
 *
 * Copyright 2026 Rafa & Cervella
 */

import { Router, Request, Response } from "express";
import { stripe } from "../utils/stripe.js";

const router = Router();

interface PortalRequest {
  customerId: string;
}

/**
 * POST /api/create-portal-session
 *
 * Creates a Stripe Customer Portal session.
 * Returns the portal URL for the CLI to open in browser.
 */
router.post("/create-portal-session", async (req: Request, res: Response) => {
  try {
    const { customerId } = req.body as PortalRequest;

    if (!customerId) {
      res.status(400).json({ error: "customerId is required" });
      return;
    }

    const frontendUrl = process.env.FRONTEND_URL || "https://cervellaswarm.com";

    // Create Portal Session
    const session = await stripe.billingPortal.sessions.create({
      customer: customerId,
      return_url: `${frontendUrl}/account`,
    });

    res.json({
      url: session.url,
    });
  } catch (error) {
    console.error("Portal session error:", error);

    if (error instanceof Error) {
      // Handle specific Stripe errors
      if (error.message.includes("No such customer")) {
        res.status(404).json({ error: "Customer not found" });
        return;
      }
      res.status(500).json({ error: error.message });
    } else {
      res.status(500).json({ error: "Failed to create portal session" });
    }
  }
});

export default router;
