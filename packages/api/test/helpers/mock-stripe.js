/**
 * Mock Stripe API
 *
 * Mock Stripe SDK per testare senza chiamate reali.
 * Include signature verification simulata.
 *
 * "Se non è testato, non funziona."
 */

import crypto from 'crypto';

/**
 * Crea evento Stripe mock con signature valida
 *
 * @param {string} type - Event type (es. 'checkout.session.completed')
 * @param {object} data - Event data
 * @param {string} secret - Webhook secret (default: 'whsec_test')
 * @returns {object} - { event, signature, rawBody }
 */
export function createMockEvent(type, data, secret = 'whsec_test') {
  const event = {
    id: `evt_${Date.now()}`,
    type,
    data: {
      object: data
    },
    created: Math.floor(Date.now() / 1000)
  };

  const rawBody = JSON.stringify(event);
  const timestamp = Math.floor(Date.now() / 1000);

  // Generate valid signature (Stripe webhook signature v1)
  const signature = generateStripeSignature(rawBody, timestamp, secret);

  return {
    event,
    signature,
    rawBody: Buffer.from(rawBody)
  };
}

/**
 * Genera signature Stripe valida
 */
function generateStripeSignature(payload, timestamp, secret) {
  const signedPayload = `${timestamp}.${payload}`;
  const signature = crypto
    .createHmac('sha256', secret)
    .update(signedPayload)
    .digest('hex');

  return `t=${timestamp},v1=${signature}`;
}

/**
 * Mock Stripe SDK
 */
export class MockStripe {
  constructor() {
    this.customers = new MockCustomers();
    this.subscriptions = new MockSubscriptions();
    this.paymentLinks = new MockPaymentLinks();
    this.webhooks = new MockWebhooks();
    this.billingPortal = new MockBillingPortal();
  }
}

class MockBillingPortal {
  constructor() {
    this.sessions = new MockPortalSessions();
  }
}

class MockPortalSessions {
  async create(params) {
    if (!params.customer) {
      throw new Error('customer is required');
    }
    if (params.customer === 'cus_nonexistent') {
      const err = new Error('No such customer: \'cus_nonexistent\'');
      err.type = 'StripeInvalidRequestError';
      throw err;
    }
    return {
      id: `bps_${Date.now()}`,
      url: `https://billing.stripe.com/p/session/test_${Date.now()}`,
      customer: params.customer,
      return_url: params.return_url || null,
    };
  }
}

class MockCustomers {
  async retrieve(id) {
    if (id === 'cus_error') {
      throw new Error('Customer not found');
    }
    return {
      id,
      email: 'test@example.com',
      deleted: false
    };
  }
}

class MockSubscriptions {
  async retrieve(id) {
    if (id === 'sub_error') {
      throw new Error('Subscription not found');
    }
    return {
      id,
      current_period_end: Math.floor(Date.now() / 1000) + 30 * 24 * 60 * 60,
      status: 'active'
    };
  }
}

class MockPaymentLinks {
  async create(params) {
    if (!params.line_items) {
      throw new Error('line_items is required');
    }
    // Generate unique URL with random component
    const uniqueId = Math.random().toString(36).substring(7);
    return {
      id: `plink_${uniqueId}`,
      url: `https://buy.stripe.com/test_${uniqueId}`,
      active: true
    };
  }
}

class MockWebhooks {
  constructEvent(payload, signature, secret) {
    // Simula verifica firma
    if (signature === 'invalid_signature') {
      throw new Error('No signatures found matching the expected signature for payload');
    }

    if (!signature || !signature.startsWith('t=')) {
      throw new Error('Invalid signature format');
    }

    // Parse payload
    const event = JSON.parse(payload.toString());
    return event;
  }
}

/**
 * Mock DB functions
 */
export const mockDb = {
  subscriptions: new Map(),

  async saveSubscription(data) {
    this.subscriptions.set(data.customerId, {
      ...data,
      createdAt: Date.now(),
      updatedAt: Date.now()
    });
  },

  async updateSubscription(customerId, updates) {
    const existing = this.subscriptions.get(customerId);
    if (!existing) {
      throw new Error('Subscription not found');
    }
    this.subscriptions.set(customerId, {
      ...existing,
      ...updates,
      updatedAt: Date.now()
    });
  },

  async updateSubscriptionStatus(customerId, status) {
    const existing = this.subscriptions.get(customerId);
    if (!existing) {
      throw new Error('Subscription not found');
    }
    this.subscriptions.set(customerId, {
      ...existing,
      status,
      updatedAt: Date.now()
    });
  },

  async getSubscription(customerId) {
    return this.subscriptions.get(customerId) || null;
  },

  async getSubscriptionByEmail(email) {
    const matches = [];
    for (const sub of this.subscriptions.values()) {
      if (sub.email && sub.email.toLowerCase() === email.toLowerCase()) {
        matches.push(sub);
      }
    }
    matches.sort((a, b) => b.updatedAt - a.updatedAt);
    return matches[0] || null;
  },

  reset() {
    this.subscriptions.clear();
  }
};
