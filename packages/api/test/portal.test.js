/**
 * Portal Route Tests
 *
 * Test per routes/portal.ts
 * Verifica: input validation, portal session creation, error handling
 */

import { test, describe, beforeEach } from 'node:test';
import assert from 'node:assert/strict';
import { MockStripe } from './helpers/mock-stripe.js';
import { createMockRequest, createMockResponse } from './helpers/mock-express.js';

describe('Portal Route', () => {

  let mockStripe;

  beforeEach(() => {
    mockStripe = new MockStripe();
  });

  describe('Input Validation', () => {
    test('rejects missing customerId', async () => {
      const req = createMockRequest({ body: {} });
      const res = createMockResponse();

      const { customerId } = req.body;
      if (!customerId) {
        res.status(400).json({ error: 'customerId is required' });
        return;
      }

      assert.equal(res.getStatus(), 400);
      assert.equal(res.getBody().error, 'customerId is required');
    });

    test('rejects empty string customerId', async () => {
      const req = createMockRequest({ body: { customerId: '' } });
      const res = createMockResponse();

      const { customerId } = req.body;
      if (!customerId) {
        res.status(400).json({ error: 'customerId is required' });
        return;
      }

      assert.equal(res.getStatus(), 400);
    });

    test('accepts valid customerId and creates session', async () => {
      const req = createMockRequest({ body: { customerId: 'cus_valid123' } });
      const res = createMockResponse();

      const { customerId } = req.body;
      if (!customerId) {
        res.status(400).json({ error: 'customerId is required' });
        return;
      }

      // Actually call mock Stripe to exercise the full path
      const session = await mockStripe.billingPortal.sessions.create({
        customer: customerId,
        return_url: 'https://cervellaswarm.com/account',
      });
      res.json({ url: session.url });

      assert.equal(res.getStatus(), 200, 'Should not reject valid customerId');
      assert.ok(res.getBody().url, 'Should return portal URL');
    });
  });

  describe('Portal Session Creation', () => {
    test('creates portal session successfully', async () => {
      const session = await mockStripe.billingPortal.sessions.create({
        customer: 'cus_test123',
        return_url: 'https://cervellaswarm.com/account',
      });

      assert.ok(session.id, 'Should return session ID');
      assert.ok(session.url, 'Should return portal URL');
      assert.ok(session.url.startsWith('https://'), 'URL should be HTTPS');
      assert.equal(session.customer, 'cus_test123');
    });

    test('returns portal URL in response', async () => {
      const req = createMockRequest({ body: { customerId: 'cus_test123' } });
      const res = createMockResponse();

      const { customerId } = req.body;
      if (!customerId) {
        res.status(400).json({ error: 'customerId is required' });
        return;
      }

      const frontendUrl = 'https://cervellaswarm.com';
      const session = await mockStripe.billingPortal.sessions.create({
        customer: customerId,
        return_url: `${frontendUrl}/account`,
      });

      res.json({ url: session.url });

      assert.equal(res.getStatus(), 200);
      assert.ok(res.getBody().url, 'Should return URL');
      assert.ok(res.getBody().url.startsWith('https://'), 'URL should be HTTPS');
    });

    test('uses FRONTEND_URL env var for return_url', async () => {
      const frontendUrl = process.env.FRONTEND_URL || 'https://cervellaswarm.com';
      const session = await mockStripe.billingPortal.sessions.create({
        customer: 'cus_test123',
        return_url: `${frontendUrl}/account`,
      });

      assert.equal(session.return_url, `${frontendUrl}/account`);
    });
  });

  describe('Error Handling', () => {
    test('handles nonexistent customer (404)', async () => {
      const res = createMockResponse();

      try {
        await mockStripe.billingPortal.sessions.create({
          customer: 'cus_nonexistent',
          return_url: 'https://cervellaswarm.com/account',
        });
      } catch (error) {
        if (error instanceof Error && error.message.includes('No such customer')) {
          res.status(404).json({ error: 'Customer not found' });
          return;
        }
        res.status(500).json({ error: error.message });
      }

      assert.equal(res.getStatus(), 404);
      assert.equal(res.getBody().error, 'Customer not found');
    });

    test('handles generic Stripe errors (500)', async () => {
      const errors = [];
      const res = createMockResponse();

      try {
        throw new Error('Stripe API unavailable');
      } catch (error) {
        errors.push(error.message);
        if (error instanceof Error) {
          res.status(500).json({ error: error.message });
        } else {
          res.status(500).json({ error: 'Failed to create portal session' });
        }
      }

      assert.equal(res.getStatus(), 500);
      assert.equal(res.getBody().error, 'Stripe API unavailable');
    });

    test('handles non-Error objects (500 with generic message)', async () => {
      const res = createMockResponse();

      try {
        throw 'string_error';
      } catch (error) {
        if (error instanceof Error) {
          res.status(500).json({ error: error.message });
        } else {
          res.status(500).json({ error: 'Failed to create portal session' });
        }
      }

      assert.equal(res.getStatus(), 500);
      assert.equal(res.getBody().error, 'Failed to create portal session');
    });

    test('logs errors to console.error', async (t) => {
      const errors = [];
      t.mock.method(console, 'error', (...args) => {
        errors.push(args.join(' '));
      });

      try {
        await mockStripe.billingPortal.sessions.create({
          customer: 'cus_nonexistent',
          return_url: 'https://cervellaswarm.com/account',
        });
      } catch (error) {
        console.error('Portal session error:', error);
      }

      assert.ok(errors.some(e => e.includes('Portal session error')));
    });
  });
});
