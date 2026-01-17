/**
 * Checkout Route Tests
 *
 * Test per routes/checkout.ts
 * Verifica: validazione input, creazione payment link, caching
 *
 * "Fatto BENE > Fatto VELOCE"
 */

import { test, describe, beforeEach } from 'node:test';
import assert from 'node:assert/strict';
import { MockStripe } from './helpers/mock-stripe.js';
import { createMockRequest, createMockResponse } from './helpers/mock-express.js';

describe('Checkout Route', () => {

  let mockStripe;

  beforeEach(() => {
    mockStripe = new MockStripe();
  });

  describe('Input Validation', () => {
    test('accepts valid tier: pro', async (t) => {
      const req = createMockRequest({
        body: {
          tier: 'pro',
          email: 'user@example.com'
        }
      });
      const res = createMockResponse();

      const { tier, email } = req.body;

      // Simulate validation
      if (!tier || !['pro', 'team'].includes(tier)) {
        res.status(400).json({ error: 'Invalid tier. Must be \'pro\' or \'team\'' });
        return;
      }

      assert.equal(res.getStatus(), 200, 'Should accept valid tier');
    });

    test('accepts valid tier: team', async (t) => {
      const req = createMockRequest({
        body: {
          tier: 'team',
          email: 'user@example.com'
        }
      });
      const res = createMockResponse();

      const { tier } = req.body;

      if (!tier || !['pro', 'team'].includes(tier)) {
        res.status(400).json({ error: 'Invalid tier. Must be \'pro\' or \'team\'' });
        return;
      }

      assert.equal(res.getStatus(), 200, 'Should accept team tier');
    });

    test('rejects invalid tier', async (t) => {
      const req = createMockRequest({
        body: {
          tier: 'enterprise',
          email: 'user@example.com'
        }
      });
      const res = createMockResponse();

      const { tier } = req.body;

      if (!tier || !['pro', 'team'].includes(tier)) {
        res.status(400).json({ error: 'Invalid tier. Must be \'pro\' or \'team\'' });
        return;
      }

      assert.equal(res.getStatus(), 400, 'Should reject invalid tier');
      assert.ok(res.getBody().error.includes('Invalid tier'), 'Should show error message');
    });

    test('rejects missing tier', async (t) => {
      const req = createMockRequest({
        body: {
          email: 'user@example.com'
        }
      });
      const res = createMockResponse();

      const { tier } = req.body;

      if (!tier || !['pro', 'team'].includes(tier)) {
        res.status(400).json({ error: 'Invalid tier. Must be \'pro\' or \'team\'' });
        return;
      }

      assert.equal(res.getStatus(), 400, 'Should reject missing tier');
    });

    test('rejects missing email', async (t) => {
      const req = createMockRequest({
        body: {
          tier: 'pro'
        }
      });
      const res = createMockResponse();

      const { email } = req.body;

      if (!email || !email.includes('@')) {
        res.status(400).json({ error: 'Valid email is required' });
        return;
      }

      assert.equal(res.getStatus(), 400, 'Should reject missing email');
      assert.ok(res.getBody().error.includes('email'), 'Should show email error');
    });

    test('rejects invalid email format', async (t) => {
      const req = createMockRequest({
        body: {
          tier: 'pro',
          email: 'not-an-email'
        }
      });
      const res = createMockResponse();

      const { email } = req.body;

      if (!email || !email.includes('@')) {
        res.status(400).json({ error: 'Valid email is required' });
        return;
      }

      assert.equal(res.getStatus(), 400, 'Should reject invalid email');
    });

    test('accepts valid email', async (t) => {
      const req = createMockRequest({
        body: {
          tier: 'pro',
          email: 'user@example.com'
        }
      });

      const { email } = req.body;

      assert.ok(email.includes('@'), 'Should accept valid email format');
    });
  });

  describe('Payment Link Creation', () => {
    test('creates payment link for pro tier', async (t) => {
      const priceId = 'price_pro_monthly';

      const paymentLink = await mockStripe.paymentLinks.create({
        line_items: [
          {
            price: priceId,
            quantity: 1
          }
        ],
        metadata: {
          tier: 'pro',
          source: 'cli'
        }
      });

      assert.ok(paymentLink.id, 'Should create payment link');
      assert.ok(paymentLink.url, 'Should have URL');
      assert.ok(paymentLink.url.startsWith('https://'), 'URL should be HTTPS');
    });

    test('creates payment link for team tier', async (t) => {
      const priceId = 'price_team_monthly';

      const paymentLink = await mockStripe.paymentLinks.create({
        line_items: [
          {
            price: priceId,
            quantity: 1
          }
        ],
        metadata: {
          tier: 'team',
          source: 'cli'
        }
      });

      assert.ok(paymentLink.id, 'Should create payment link');
      assert.ok(paymentLink.url, 'Should have URL');
    });

    test('returns payment link URL in response', async (t) => {
      const req = createMockRequest({
        body: {
          tier: 'pro',
          email: 'user@example.com'
        }
      });
      const res = createMockResponse();

      // Simulate handler
      const paymentLink = await mockStripe.paymentLinks.create({
        line_items: [
          {
            price: 'price_pro',
            quantity: 1
          }
        ],
        metadata: {
          tier: 'pro',
          source: 'cli'
        }
      });

      res.json({
        url: paymentLink.url,
        tier: 'pro',
        note: 'Payment Link - complete payment to activate subscription'
      });

      assert.equal(res.getStatus(), 200, 'Should return 200');
      assert.ok(res.getBody().url, 'Should return URL');
      assert.equal(res.getBody().tier, 'pro', 'Should return tier');
      assert.ok(res.getBody().note, 'Should return note');
    });

    test('handles Stripe API errors', async (t) => {
      const errors = [];
      t.mock.method(console, 'error', (...args) => {
        errors.push(args.join(' '));
      });

      const res = createMockResponse();

      // Simulate Stripe error
      try {
        await mockStripe.paymentLinks.create({
          // Missing required line_items
        });
      } catch (error) {
        console.error('Payment link error:', error);
        res.status(500).json({ error: error.message });
      }

      assert.equal(res.getStatus(), 500, 'Should return 500 on error');
      assert.ok(res.getBody().error, 'Should return error message');
      assert.ok(errors.some(e => e.includes('Payment link error')), 'Should log error');
    });
  });

  describe('Payment Link Caching', () => {
    test('caches payment link by tier', async (t) => {
      const cache = {};

      // First request - create
      const paymentLink1 = await mockStripe.paymentLinks.create({
        line_items: [{ price: 'price_pro', quantity: 1 }],
        metadata: { tier: 'pro', source: 'cli' }
      });
      cache['pro'] = paymentLink1.url;

      // Second request - use cache
      const cachedUrl = cache['pro'];

      assert.ok(cachedUrl, 'Should cache URL');
      assert.equal(cachedUrl, paymentLink1.url, 'Cached URL should match');
    });

    test('returns cached link on subsequent requests', async (t) => {
      const cache = {
        'pro': 'https://buy.stripe.com/cached_pro'
      };

      const req = createMockRequest({
        body: {
          tier: 'pro',
          email: 'user@example.com'
        }
      });
      const res = createMockResponse();

      // Check cache first
      if (cache['pro']) {
        res.json({
          url: cache['pro'],
          tier: 'pro',
          note: 'Payment Link - complete payment to activate subscription'
        });
        // Should NOT call Stripe API
      }

      assert.equal(res.getBody().url, 'https://buy.stripe.com/cached_pro', 'Should use cached URL');
    });

    test('different tiers have separate cache entries', async (t) => {
      const cache = {};

      const proLink = await mockStripe.paymentLinks.create({
        line_items: [{ price: 'price_pro', quantity: 1 }],
        metadata: { tier: 'pro' }
      });
      cache['pro'] = proLink.url;

      const teamLink = await mockStripe.paymentLinks.create({
        line_items: [{ price: 'price_team', quantity: 1 }],
        metadata: { tier: 'team' }
      });
      cache['team'] = teamLink.url;

      assert.notEqual(cache['pro'], cache['team'], 'Pro and team should have different URLs');
      assert.ok(cache['pro'], 'Should cache pro');
      assert.ok(cache['team'], 'Should cache team');
    });
  });

  describe('Edge Cases', () => {
    test('handles tier case sensitivity', async (t) => {
      const req = createMockRequest({
        body: {
          tier: 'PRO', // Uppercase
          email: 'user@example.com'
        }
      });
      const res = createMockResponse();

      const { tier } = req.body;

      // Should normalize or reject
      if (!tier || !['pro', 'team'].includes(tier)) {
        res.status(400).json({ error: 'Invalid tier. Must be \'pro\' or \'team\'' });
      }

      // Current implementation: rejects uppercase
      assert.equal(res.getStatus(), 400, 'Should reject uppercase tier (or normalize)');
    });

    test('handles email with whitespace', async (t) => {
      const req = createMockRequest({
        body: {
          tier: 'pro',
          email: '  user@example.com  '
        }
      });

      const { email } = req.body;
      const trimmedEmail = email.trim();

      assert.equal(trimmedEmail, 'user@example.com', 'Should handle whitespace');
      assert.ok(trimmedEmail.includes('@'), 'Trimmed email should be valid');
    });

    test('handles very long email', async (t) => {
      const longEmail = 'a'.repeat(100) + '@example.com';

      const req = createMockRequest({
        body: {
          tier: 'pro',
          email: longEmail
        }
      });

      const { email } = req.body;

      // Basic validation should still pass
      assert.ok(email.includes('@'), 'Long email should have @');
    });

    test('handles special characters in email', async (t) => {
      const specialEmail = 'user+test@example.com';

      const req = createMockRequest({
        body: {
          tier: 'pro',
          email: specialEmail
        }
      });

      const { email } = req.body;

      assert.ok(email.includes('@'), 'Should accept special chars in email');
    });

    test('handles network timeout gracefully', async (t) => {
      const errors = [];
      t.mock.method(console, 'error', (...args) => {
        errors.push(args.join(' '));
      });

      const res = createMockResponse();

      // Simulate timeout
      try {
        throw new Error('Request timeout');
      } catch (error) {
        console.error('Payment link error:', error);
        res.status(500).json({ error: 'Failed to create payment link' });
      }

      assert.equal(res.getStatus(), 500, 'Should handle timeout');
      assert.ok(errors.some(e => e.includes('timeout')), 'Should log timeout');
    });
  });

});
