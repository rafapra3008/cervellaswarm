/**
 * JSON Database for Subscription Storage
 *
 * Uses lowdb for simple JSON-based persistence.
 * Zero native compilation required.
 *
 * Copyright 2026 Rafa & Cervella
 */

import { Low } from "lowdb";
import { JSONFile } from "lowdb/node";
import path from "path";
import { fileURLToPath } from "url";
import fs from "fs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const DB_PATH = process.env.DATABASE_PATH || path.join(__dirname, "../../data/subscriptions.json");

// Ensure data directory exists
const dataDir = path.dirname(DB_PATH);
if (!fs.existsSync(dataDir)) {
  fs.mkdirSync(dataDir, { recursive: true });
}

// Types
export interface SubscriptionRecord {
  customerId: string;
  subscriptionId: string | null;
  tier: "free" | "pro" | "team";
  status: string;
  email: string;
  currentPeriodEnd: number | null;
  createdAt: number;
  updatedAt: number;
}

interface DatabaseSchema {
  subscriptions: SubscriptionRecord[];
}

// Initialize database
const adapter = new JSONFile<DatabaseSchema>(DB_PATH);
const defaultData: DatabaseSchema = { subscriptions: [] };
const db = new Low<DatabaseSchema>(adapter, defaultData);

// Load data on startup
await db.read();

/**
 * Save or update subscription
 */
export async function saveSubscription(data: {
  customerId: string;
  subscriptionId?: string;
  tier: "free" | "pro" | "team";
  status: string;
  email: string;
  currentPeriodEnd?: number;
}): Promise<void> {
  await db.read();

  const now = Math.floor(Date.now() / 1000);
  const existingIndex = db.data.subscriptions.findIndex(
    (s) => s.customerId === data.customerId
  );

  const record: SubscriptionRecord = {
    customerId: data.customerId,
    subscriptionId: data.subscriptionId || null,
    tier: data.tier,
    status: data.status,
    email: data.email,
    currentPeriodEnd: data.currentPeriodEnd || null,
    createdAt: existingIndex >= 0 ? db.data.subscriptions[existingIndex].createdAt : now,
    updatedAt: now,
  };

  if (existingIndex >= 0) {
    db.data.subscriptions[existingIndex] = record;
  } else {
    db.data.subscriptions.push(record);
  }

  await db.write();
}

/**
 * Get subscription by customer ID
 */
export async function getSubscription(customerId: string): Promise<SubscriptionRecord | null> {
  await db.read();
  return db.data.subscriptions.find((s) => s.customerId === customerId) || null;
}

/**
 * Get subscription by email
 */
export async function getSubscriptionByEmail(email: string): Promise<SubscriptionRecord | null> {
  await db.read();

  // Find most recently updated subscription for this email
  const matches = db.data.subscriptions
    .filter((s) => s.email.toLowerCase() === email.toLowerCase())
    .sort((a, b) => b.updatedAt - a.updatedAt);

  return matches[0] || null;
}

/**
 * Update subscription status
 */
export async function updateSubscriptionStatus(
  customerId: string,
  status: string
): Promise<void> {
  await db.read();

  const subscription = db.data.subscriptions.find((s) => s.customerId === customerId);
  if (subscription) {
    subscription.status = status;
    subscription.updatedAt = Math.floor(Date.now() / 1000);
    await db.write();
  }
}

/**
 * Update subscription tier and/or status
 */
export async function updateSubscription(
  customerId: string,
  data: { tier?: "free" | "pro" | "team"; status?: string }
): Promise<void> {
  await db.read();

  const subscription = db.data.subscriptions.find((s) => s.customerId === customerId);
  if (subscription) {
    if (data.tier) subscription.tier = data.tier;
    if (data.status) subscription.status = data.status;
    subscription.updatedAt = Math.floor(Date.now() / 1000);
    await db.write();
  }
}

export default db;
