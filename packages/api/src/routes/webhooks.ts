/**
 * Stripe Webhook Handler
 *
 * Receives and processes Stripe webhook events.
 * CRITICAL: Uses raw body for signature verification!
 *
 * Copyright 2026 Rafa & Cervella
 */

import { Router, Request, Response } from "express";
import Stripe from "stripe";
import { stripe, mapPriceIdToTier } from "../utils/stripe.js";
import {
  saveSubscription,
  updateSubscription,
  updateSubscriptionStatus,
  getSubscription,
} from "../db/index.js";

const router = Router();

/**
 * POST /webhooks/stripe
 *
 * Receives Stripe webhook events.
 * NOTE: This route must receive RAW body (not JSON parsed)!
 */
router.post(
  "/stripe",
  async (req: Request, res: Response) => {
    const sig = req.headers["stripe-signature"];
    const endpointSecret = process.env.STRIPE_WEBHOOK_SECRET;

    if (!sig || !endpointSecret) {
      console.error("Missing signature or webhook secret");
      res.status(400).json({ error: "Missing signature" });
      return;
    }

    let event: Stripe.Event;

    // 1. Verify webhook signature (CRITICAL!)
    try {
      // req.body must be raw Buffer, not parsed JSON
      event = stripe.webhooks.constructEvent(
        req.body,
        sig,
        endpointSecret
      );
    } catch (err) {
      const message = err instanceof Error ? err.message : "Unknown error";
      console.error("Webhook signature verification failed:", message);
      res.status(400).json({ error: `Webhook Error: ${message}` });
      return;
    }

    // 2. Log event for debugging
    console.log(`Received event: ${event.type} [${event.id}]`);

    // 3. Handle event
    try {
      switch (event.type) {
        case "checkout.session.completed":
          await handleCheckoutCompleted(event.data.object as Stripe.Checkout.Session);
          break;

        case "invoice.paid":
          await handleInvoicePaid(event.data.object as Stripe.Invoice);
          break;

        case "invoice.payment_failed":
          await handlePaymentFailed(event.data.object as Stripe.Invoice);
          break;

        case "customer.subscription.created":
          await handleSubscriptionCreated(event.data.object as Stripe.Subscription);
          break;

        case "customer.subscription.updated":
          await handleSubscriptionUpdated(event.data.object as Stripe.Subscription);
          break;

        case "customer.subscription.deleted":
          await handleSubscriptionDeleted(event.data.object as Stripe.Subscription);
          break;

        default:
          console.log(`Unhandled event type: ${event.type}`);
      }

      res.json({ received: true });
    } catch (error) {
      console.error(`Error handling ${event.type}:`, error);
      // Return 200 anyway to prevent Stripe retries for handler errors
      // (Stripe will retry on 4xx/5xx, which could cause duplicate processing)
      res.json({ received: true, error: "Handler error logged" });
    }
  }
);

// ============================================
// Event Handlers
// ============================================

/**
 * Handle checkout.session.completed
 *
 * User completed payment - save customer and tier.
 */
async function handleCheckoutCompleted(session: Stripe.Checkout.Session): Promise<void> {
  console.log("Processing checkout.session.completed");

  const customerId = session.customer as string;
  const subscriptionId = session.subscription as string;
  const tier = (session.metadata?.tier as "pro" | "team") || "pro";
  const email = session.customer_email || session.client_reference_id || "";

  if (!customerId || !email) {
    console.error("Missing customerId or email in checkout session");
    return;
  }

  // Get subscription details for period end
  let currentPeriodEnd: number | undefined;
  if (subscriptionId) {
    try {
      const subscription = await stripe.subscriptions.retrieve(subscriptionId);
      currentPeriodEnd = subscription.current_period_end;
    } catch (error) {
      console.error("Failed to fetch subscription details:", error);
    }
  }

  await saveSubscription({
    customerId,
    subscriptionId,
    tier,
    status: "active",
    email,
    currentPeriodEnd,
  });

  console.log(`Subscription saved: ${email} -> ${tier} (${customerId})`);
}

/**
 * Handle invoice.paid
 *
 * Billing cycle completed successfully - confirm active status.
 */
async function handleInvoicePaid(invoice: Stripe.Invoice): Promise<void> {
  console.log("Processing invoice.paid");

  const customerId = invoice.customer as string;

  if (!customerId) {
    console.error("Missing customerId in invoice");
    return;
  }

  // Update status to active (in case it was past_due)
  await updateSubscriptionStatus(customerId, "active");

  console.log(`Invoice paid for customer: ${customerId}`);
}

/**
 * Handle invoice.payment_failed
 *
 * Payment failed - mark as past_due (downgrade after grace period).
 */
async function handlePaymentFailed(invoice: Stripe.Invoice): Promise<void> {
  console.log("Processing invoice.payment_failed");

  const customerId = invoice.customer as string;

  if (!customerId) {
    console.error("Missing customerId in invoice");
    return;
  }

  // Mark as past_due (Stripe will retry automatically)
  await updateSubscriptionStatus(customerId, "past_due");

  console.log(`Payment failed for customer: ${customerId}`);

  // TODO: Send notification email to user
}

/**
 * Handle customer.subscription.created
 *
 * New subscription created - save customer, tier, and email.
 * This is triggered by Payment Links (instead of checkout.session.completed).
 */
async function handleSubscriptionCreated(subscription: Stripe.Subscription): Promise<void> {
  console.log("Processing customer.subscription.created");

  const customerId = subscription.customer as string;
  const subscriptionId = subscription.id;

  if (!customerId) {
    console.error("Missing customerId in subscription");
    return;
  }

  // Get customer email from Stripe
  let email = "";
  try {
    const customer = await stripe.customers.retrieve(customerId);
    if (customer && !customer.deleted && "email" in customer) {
      email = customer.email || "";
    }
  } catch (error) {
    console.error("Failed to fetch customer:", error);
  }

  // Get tier from price
  const priceId = subscription.items.data[0]?.price?.id;
  const tier = priceId ? mapPriceIdToTier(priceId) : "pro";

  await saveSubscription({
    customerId,
    subscriptionId,
    tier,
    status: subscription.status,
    email,
    currentPeriodEnd: subscription.current_period_end,
  });

  console.log(`Subscription created: ${email} -> ${tier} (${customerId})`);
}

/**
 * Handle customer.subscription.updated
 *
 * Subscription changed - could be upgrade, downgrade, or status change.
 */
async function handleSubscriptionUpdated(subscription: Stripe.Subscription): Promise<void> {
  console.log("Processing customer.subscription.updated");

  const customerId = subscription.customer as string;

  if (!customerId) {
    console.error("Missing customerId in subscription");
    return;
  }

  // Check if this is newer than what we have
  const existing = await getSubscription(customerId);
  if (existing && existing.updatedAt > subscription.created) {
    console.log("Ignoring outdated event");
    return;
  }

  // Get new tier from price
  const priceId = subscription.items.data[0]?.price?.id;
  const tier = priceId ? mapPriceIdToTier(priceId) : "free";

  await updateSubscription(customerId, {
    tier,
    status: subscription.status,
  });

  console.log(`Subscription updated: ${customerId} -> ${tier} (${subscription.status})`);
}

/**
 * Handle customer.subscription.deleted
 *
 * Subscription cancelled - downgrade to free.
 */
async function handleSubscriptionDeleted(subscription: Stripe.Subscription): Promise<void> {
  console.log("Processing customer.subscription.deleted");

  const customerId = subscription.customer as string;

  if (!customerId) {
    console.error("Missing customerId in subscription");
    return;
  }

  await updateSubscription(customerId, {
    tier: "free",
    status: "canceled",
  });

  console.log(`Subscription cancelled: ${customerId} -> free`);
}

export default router;
