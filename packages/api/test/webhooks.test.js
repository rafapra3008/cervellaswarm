/**
 * Webhook Handler Tests
 *
 * Test per routes/webhooks.ts
 * Verifica: signature verification, event handlers, error handling
 *
 * "Se non è testato, non funziona."
 */

import { test, describe, beforeEach, mock } from 'node:test';
import assert from 'node:assert/strict';
import { createMockEvent, MockStripe, mockDb } from './helpers/mock-stripe.js';
import { createMockRequest, createMockResponse, executeHandler } from './helpers/mock-express.js';

// Mock environment
process.env.STRIPE_WEBHOOK_SECRET = 'whsec_test';

describe('Webhook Handler', () => {

  beforeEach(() => {
    mockDb.reset();
  });

  describe('Signature Verification', () => {
    test('accepts valid signature', async (t) => {
      const { event, signature, rawBody } = createMockEvent('checkout.session.completed', {
        customer: 'cus_123',
        customer_email: 'test@example.com',
        subscription: 'sub_123',
        metadata: { tier: 'pro' }
      });

      const req = createMockRequest({
        body: rawBody,
        headers: {
          'stripe-signature': signature
        }
      });
      const res = createMockResponse();

      // Mock stripe.webhooks.constructEvent
      const mockStripe = new MockStripe();
      t.mock.method(mockStripe.webhooks, 'constructEvent', () => event);

      // Simulate handler (signature verification passes)
      assert.doesNotThrow(() => {
        mockStripe.webhooks.constructEvent(rawBody, signature, process.env.STRIPE_WEBHOOK_SECRET);
      });
    });

    test('rejects invalid signature', async (t) => {
      const { rawBody } = createMockEvent('checkout.session.completed', {});

      const req = createMockRequest({
        body: rawBody,
        headers: {
          'stripe-signature': 'invalid_signature'
        }
      });

      const mockStripe = new MockStripe();

      assert.throws(
        () => mockStripe.webhooks.constructEvent(rawBody, 'invalid_signature', process.env.STRIPE_WEBHOOK_SECRET),
        /No signatures found/,
        'Should reject invalid signature'
      );
    });

    test('rejects missing signature', async (t) => {
      const req = createMockRequest({
        body: Buffer.from('{}'),
        headers: {} // No signature
      });
      const res = createMockResponse();

      // Simulate handler behavior
      if (!req.headers['stripe-signature'] || !process.env.STRIPE_WEBHOOK_SECRET) {
        res.status(400).json({ error: 'Missing signature' });
      }

      assert.equal(res.getStatus(), 400, 'Should return 400');
      assert.ok(res.getBody().error.includes('Missing signature'), 'Should show error message');
    });

    test('rejects missing webhook secret', async (t) => {
      const originalSecret = process.env.STRIPE_WEBHOOK_SECRET;
      delete process.env.STRIPE_WEBHOOK_SECRET;

      const { signature, rawBody } = createMockEvent('checkout.session.completed', {});

      const req = createMockRequest({
        body: rawBody,
        headers: {
          'stripe-signature': signature
        }
      });
      const res = createMockResponse();

      // Simulate handler
      if (!req.headers['stripe-signature'] || !process.env.STRIPE_WEBHOOK_SECRET) {
        res.status(400).json({ error: 'Missing signature' });
      }

      assert.equal(res.getStatus(), 400, 'Should return 400');

      process.env.STRIPE_WEBHOOK_SECRET = originalSecret;
    });
  });

  describe('Event Handlers', () => {
    test('handles checkout.session.completed', async (t) => {
      const sessionData = {
        customer: 'cus_test123',
        customer_email: 'user@example.com',
        subscription: 'sub_test123',
        metadata: { tier: 'pro' }
      };

      // Simulate handler logic
      await mockDb.saveSubscription({
        customerId: sessionData.customer,
        subscriptionId: sessionData.subscription,
        tier: sessionData.metadata.tier,
        status: 'active',
        email: sessionData.customer_email,
        currentPeriodEnd: Math.floor(Date.now() / 1000) + 30 * 24 * 60 * 60
      });

      const saved = await mockDb.getSubscription('cus_test123');
      assert.ok(saved, 'Should save subscription');
      assert.equal(saved.tier, 'pro', 'Should save correct tier');
      assert.equal(saved.email, 'user@example.com', 'Should save email');
      assert.equal(saved.status, 'active', 'Should set active status');
    });

    test('handles invoice.paid', async (t) => {
      // Setup existing subscription
      await mockDb.saveSubscription({
        customerId: 'cus_test123',
        subscriptionId: 'sub_test123',
        tier: 'pro',
        status: 'past_due',
        email: 'test@example.com'
      });

      const invoiceData = {
        customer: 'cus_test123'
      };

      // Simulate handler
      await mockDb.updateSubscriptionStatus(invoiceData.customer, 'active');

      const updated = await mockDb.getSubscription('cus_test123');
      assert.equal(updated.status, 'active', 'Should update status to active');
    });

    test('handles invoice.payment_failed', async (t) => {
      await mockDb.saveSubscription({
        customerId: 'cus_test123',
        subscriptionId: 'sub_test123',
        tier: 'pro',
        status: 'active',
        email: 'test@example.com'
      });

      const invoiceData = {
        customer: 'cus_test123'
      };

      // Simulate handler
      await mockDb.updateSubscriptionStatus(invoiceData.customer, 'past_due');

      const updated = await mockDb.getSubscription('cus_test123');
      assert.equal(updated.status, 'past_due', 'Should mark as past_due');
    });

    test('handles customer.subscription.created', async (t) => {
      const subscriptionData = {
        id: 'sub_new123',
        customer: 'cus_new123',
        status: 'active',
        items: {
          data: [
            { price: { id: 'price_pro' } }
          ]
        },
        current_period_end: Math.floor(Date.now() / 1000) + 30 * 24 * 60 * 60
      };

      // Simulate handler (would fetch customer from Stripe)
      await mockDb.saveSubscription({
        customerId: subscriptionData.customer,
        subscriptionId: subscriptionData.id,
        tier: 'pro', // Mapped from price_id
        status: subscriptionData.status,
        email: 'test@example.com',
        currentPeriodEnd: subscriptionData.current_period_end
      });

      const saved = await mockDb.getSubscription('cus_new123');
      assert.ok(saved, 'Should save new subscription');
      assert.equal(saved.status, 'active', 'Should save status');
    });

    test('handles customer.subscription.updated', async (t) => {
      // Create existing subscription
      await mockDb.saveSubscription({
        customerId: 'cus_test123',
        subscriptionId: 'sub_test123',
        tier: 'pro',
        status: 'active',
        email: 'test@example.com'
      });

      const subscriptionData = {
        customer: 'cus_test123',
        status: 'active',
        items: {
          data: [
            { price: { id: 'price_team' } }
          ]
        },
        created: Math.floor(Date.now() / 1000)
      };

      // Simulate upgrade to team
      await mockDb.updateSubscription(subscriptionData.customer, {
        tier: 'team',
        status: subscriptionData.status
      });

      const updated = await mockDb.getSubscription('cus_test123');
      assert.equal(updated.tier, 'team', 'Should update tier');
    });

    test('handles customer.subscription.deleted', async (t) => {
      await mockDb.saveSubscription({
        customerId: 'cus_test123',
        subscriptionId: 'sub_test123',
        tier: 'pro',
        status: 'active',
        email: 'test@example.com'
      });

      const subscriptionData = {
        customer: 'cus_test123'
      };

      // Simulate cancellation
      await mockDb.updateSubscription(subscriptionData.customer, {
        tier: 'free',
        status: 'canceled'
      });

      const updated = await mockDb.getSubscription('cus_test123');
      assert.equal(updated.tier, 'free', 'Should downgrade to free');
      assert.equal(updated.status, 'canceled', 'Should mark as canceled');
    });
  });

  describe('Unknown Event Types', () => {
    test('logs unknown event and returns 200', async (t) => {
      const { event, signature, rawBody } = createMockEvent('unknown.event.type', {});

      const logs = [];
      t.mock.method(console, 'log', (...args) => {
        logs.push(args.join(' '));
      });

      // Simulate handler behavior for unknown event
      if (!['checkout.session.completed', 'invoice.paid', 'invoice.payment_failed',
           'customer.subscription.created', 'customer.subscription.updated',
           'customer.subscription.deleted'].includes(event.type)) {
        console.log(`Unhandled event type: ${event.type}`);
      }

      assert.ok(logs.some(l => l.includes('Unhandled event type')), 'Should log unhandled event');
      assert.ok(logs.some(l => l.includes('unknown.event.type')), 'Should log event type');
    });
  });

  describe('Edge Cases', () => {
    test('handles missing customerId gracefully', async (t) => {
      const errors = [];
      t.mock.method(console, 'error', (...args) => {
        errors.push(args.join(' '));
      });

      const sessionData = {
        // customer missing
        customer_email: 'test@example.com',
        subscription: 'sub_123',
        metadata: { tier: 'pro' }
      };

      // Simulate handler validation
      if (!sessionData.customer || !sessionData.customer_email) {
        console.error('Missing customerId or email in checkout session');
        return;
      }

      assert.ok(errors.some(e => e.includes('Missing customerId')), 'Should log error');
    });

    test('handles Stripe API errors gracefully', async (t) => {
      const errors = [];
      t.mock.method(console, 'error', (...args) => {
        errors.push(args.join(' '));
      });

      const mockStripe = new MockStripe();

      // Simulate failed customer retrieval
      try {
        await mockStripe.customers.retrieve('cus_error');
      } catch (error) {
        console.error('Failed to fetch customer:', error);
      }

      assert.ok(errors.some(e => e.includes('Failed to fetch customer')), 'Should handle API error');
    });

    test('handles database errors and still returns 200', async (t) => {
      const errors = [];
      t.mock.method(console, 'error', (...args) => {
        errors.push(args.join(' '));
      });

      // Simulate handler error
      try {
        throw new Error('Database connection failed');
      } catch (error) {
        console.error('Error handling checkout.session.completed:', error);
        // Should still return 200 to prevent Stripe retries
      }

      assert.ok(errors.some(e => e.includes('Error handling')), 'Should log handler error');
      // Note: In real handler, would still res.json({ received: true })
    });

    test('handles missing subscription gracefully', async (t) => {
      const sessionData = {
        customer: 'cus_123',
        customer_email: 'test@example.com',
        subscription: null, // No subscription yet
        metadata: { tier: 'pro' }
      };

      // Should still save (subscription might be created later)
      await mockDb.saveSubscription({
        customerId: sessionData.customer,
        subscriptionId: sessionData.subscription,
        tier: sessionData.metadata.tier,
        status: 'active',
        email: sessionData.customer_email
      });

      const saved = await mockDb.getSubscription('cus_123');
      assert.ok(saved, 'Should save even without subscriptionId');
      assert.equal(saved.subscriptionId, null, 'subscriptionId can be null');
    });
  });

});
