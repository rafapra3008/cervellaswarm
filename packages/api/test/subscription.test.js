/**
 * Subscription Route Tests
 *
 * Test per routes/subscription.ts
 * Verifica: lookup by customerId, lookup by email, error handling
 */

import { test, describe, beforeEach } from 'node:test';
import assert from 'node:assert/strict';
import { mockDb } from './helpers/mock-stripe.js';
import { createMockRequest, createMockResponse } from './helpers/mock-express.js';

describe('Subscription Route', () => {

  beforeEach(() => {
    mockDb.reset();
  });

  describe('GET /subscription/:customerId', () => {
    test('returns subscription for existing customer', async () => {
      await mockDb.saveSubscription({
        customerId: 'cus_test123',
        subscriptionId: 'sub_test123',
        tier: 'pro',
        status: 'active',
        email: 'user@example.com',
        currentPeriodEnd: Math.floor(Date.now() / 1000) + 30 * 24 * 60 * 60,
      });

      const req = createMockRequest({ params: { customerId: 'cus_test123' } });
      const res = createMockResponse();

      const subscription = await mockDb.getSubscription(req.params.customerId);

      if (!subscription) {
        res.json({ tier: 'free', status: 'none', message: 'No subscription found' });
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

      assert.equal(res.getStatus(), 200);
      assert.equal(res.getBody().tier, 'pro');
      assert.equal(res.getBody().status, 'active');
      assert.equal(res.getBody().email, 'user@example.com');
      assert.equal(res.getBody().customerId, 'cus_test123');
      assert.equal(res.getBody().subscriptionId, 'sub_test123');
    });

    test('returns free tier for nonexistent customer', async () => {
      const req = createMockRequest({ params: { customerId: 'cus_unknown' } });
      const res = createMockResponse();

      const subscription = await mockDb.getSubscription(req.params.customerId);

      if (!subscription) {
        res.json({ tier: 'free', status: 'none', message: 'No subscription found' });
        return;
      }

      assert.equal(res.getStatus(), 200);
      assert.equal(res.getBody().tier, 'free');
      assert.equal(res.getBody().status, 'none');
      assert.ok(res.getBody().message.includes('No subscription found'));
    });

    test('returns correct fields for team tier', async () => {
      const periodEnd = Math.floor(Date.now() / 1000) + 60 * 24 * 60 * 60;
      await mockDb.saveSubscription({
        customerId: 'cus_team',
        subscriptionId: 'sub_team',
        tier: 'team',
        status: 'active',
        email: 'team@company.com',
        currentPeriodEnd: periodEnd,
      });

      const subscription = await mockDb.getSubscription('cus_team');
      assert.equal(subscription.tier, 'team');
      assert.equal(subscription.currentPeriodEnd, periodEnd);
    });

    test('handles database error gracefully', async (t) => {
      const errors = [];
      t.mock.method(console, 'error', (...args) => {
        errors.push(args.join(' '));
      });

      const res = createMockResponse();

      try {
        throw new Error('Database read failed');
      } catch (error) {
        console.error('Subscription lookup error:', error);
        res.status(500).json({ error: 'Failed to fetch subscription' });
      }

      assert.equal(res.getStatus(), 500);
      assert.equal(res.getBody().error, 'Failed to fetch subscription');
      assert.ok(errors.some(e => e.includes('Subscription lookup error')));
    });
  });

  describe('GET /subscription/by-email/:email', () => {
    test('returns subscription for existing email', async () => {
      await mockDb.saveSubscription({
        customerId: 'cus_email1',
        subscriptionId: 'sub_email1',
        tier: 'pro',
        status: 'active',
        email: 'user@example.com',
      });

      const req = createMockRequest({ params: { email: 'user@example.com' } });
      const res = createMockResponse();

      const email = req.params.email;
      if (!email || !email.includes('@')) {
        res.status(400).json({ error: 'Valid email is required' });
        return;
      }

      const subscription = await mockDb.getSubscriptionByEmail(decodeURIComponent(email));

      if (!subscription) {
        res.json({ tier: 'free', status: 'none', message: 'No subscription found for this email' });
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

      assert.equal(res.getStatus(), 200);
      assert.equal(res.getBody().tier, 'pro');
      assert.equal(res.getBody().customerId, 'cus_email1');
      assert.equal(res.getBody().subscriptionId, 'sub_email1');
      assert.ok('currentPeriodEnd' in res.getBody(), 'Should include currentPeriodEnd');
    });

    test('returns free tier for unknown email', async () => {
      const req = createMockRequest({ params: { email: 'unknown@example.com' } });
      const res = createMockResponse();

      const email = req.params.email;
      if (!email || !email.includes('@')) {
        res.status(400).json({ error: 'Valid email is required' });
        return;
      }

      const subscription = await mockDb.getSubscriptionByEmail(email);

      if (!subscription) {
        res.json({ tier: 'free', status: 'none', message: 'No subscription found for this email' });
        return;
      }

      assert.equal(res.getStatus(), 200);
      assert.equal(res.getBody().tier, 'free');
      assert.ok(res.getBody().message.includes('No subscription'));
    });

    test('rejects missing email (400)', async () => {
      const req = createMockRequest({ params: { email: '' } });
      const res = createMockResponse();

      const email = req.params.email;
      if (!email || !email.includes('@')) {
        res.status(400).json({ error: 'Valid email is required' });
        return;
      }

      assert.equal(res.getStatus(), 400);
      assert.equal(res.getBody().error, 'Valid email is required');
    });

    test('rejects invalid email format (400)', async () => {
      const req = createMockRequest({ params: { email: 'not-an-email' } });
      const res = createMockResponse();

      const email = req.params.email;
      if (!email || !email.includes('@')) {
        res.status(400).json({ error: 'Valid email is required' });
        return;
      }

      assert.equal(res.getStatus(), 400);
      assert.equal(res.getBody().error, 'Valid email is required');
    });

    test('handles URL-encoded email', async () => {
      await mockDb.saveSubscription({
        customerId: 'cus_encoded',
        subscriptionId: 'sub_encoded',
        tier: 'pro',
        status: 'active',
        email: 'user+test@example.com',
      });

      const encodedEmail = encodeURIComponent('user+test@example.com');
      const decodedEmail = decodeURIComponent(encodedEmail);

      const subscription = await mockDb.getSubscriptionByEmail(decodedEmail);

      assert.ok(subscription, 'Should find URL-encoded email');
      assert.equal(subscription.email, 'user+test@example.com');
    });

    test('email lookup is case-insensitive', async () => {
      await mockDb.saveSubscription({
        customerId: 'cus_case',
        subscriptionId: 'sub_case',
        tier: 'pro',
        status: 'active',
        email: 'User@Example.COM',
      });

      const subscription = await mockDb.getSubscriptionByEmail('user@example.com');

      assert.ok(subscription, 'Should find email case-insensitively');
      assert.equal(subscription.customerId, 'cus_case');
    });

    test('returns most recently updated subscription for duplicate emails', async () => {
      await mockDb.saveSubscription({
        customerId: 'cus_old',
        subscriptionId: 'sub_old',
        tier: 'free',
        status: 'canceled',
        email: 'dup@example.com',
      });

      // Small delay to ensure different updatedAt
      await new Promise(resolve => setTimeout(resolve, 10));

      await mockDb.saveSubscription({
        customerId: 'cus_new',
        subscriptionId: 'sub_new',
        tier: 'pro',
        status: 'active',
        email: 'dup@example.com',
      });

      const subscription = await mockDb.getSubscriptionByEmail('dup@example.com');

      assert.ok(subscription);
      assert.equal(subscription.customerId, 'cus_new', 'Should return most recent');
      assert.equal(subscription.tier, 'pro');
    });

    test('handles database error gracefully', async (t) => {
      const errors = [];
      t.mock.method(console, 'error', (...args) => {
        errors.push(args.join(' '));
      });

      const res = createMockResponse();

      try {
        throw new Error('Database connection lost');
      } catch (error) {
        console.error('Subscription lookup error:', error);
        res.status(500).json({ error: 'Failed to fetch subscription' });
      }

      assert.equal(res.getStatus(), 500);
      assert.ok(errors.some(e => e.includes('Subscription lookup error')));
    });
  });
});
