/**
 * Config Manager for MCP Server
 *
 * Shares configuration with CLI through `conf` package.
 * Same config file = CLI and MCP see same settings.
 *
 * Copyright 2026 Rafa & Cervella
 * Licensed under the Apache License, Version 2.0
 */

import Conf from "conf";

interface ConfigSchema {
  apiKey: string;
  defaultModel: string;
  timeout: number;
  maxRetries: number;
  verbose: boolean;
  telemetry: boolean;
}

// Schema for validation
const schema = {
  apiKey: { type: "string" as const, default: "" },
  defaultModel: {
    type: "string" as const,
    enum: ["claude-sonnet-4-20250514", "claude-opus-4-5-20251101"],
    default: "claude-sonnet-4-20250514",
  },
  timeout: {
    type: "number" as const,
    minimum: 10000,
    maximum: 600000,
    default: 120000,
  },
  maxRetries: {
    type: "number" as const,
    minimum: 1,
    maximum: 10,
    default: 3,
  },
  verbose: { type: "boolean" as const, default: false },
  telemetry: { type: "boolean" as const, default: false },
};

// Singleton config instance
// Uses same projectName as CLI = same config file!
let config: Conf<ConfigSchema> | null = null;

function getConfig(): Conf<ConfigSchema> {
  if (!config) {
    config = new Conf<ConfigSchema>({
      projectName: "cervellaswarm", // Same as CLI!
      schema,
      defaults: {
        apiKey: "",
        defaultModel: "claude-sonnet-4-20250514",
        timeout: 120000,
        maxRetries: 3,
        verbose: false,
        telemetry: false,
      },
    });
  }
  return config;
}

// ============================================
// API KEY
// ============================================

export function getApiKey(): string | null {
  // Environment variable takes priority
  const envKey = process.env.ANTHROPIC_API_KEY;
  if (envKey) {
    return envKey;
  }

  // Fall back to saved config
  const savedKey = getConfig().get("apiKey");
  return savedKey || null;
}

export function hasApiKey(): boolean {
  return getApiKey() !== null;
}

export function getApiKeySource(): "environment" | "config" | "none" {
  if (process.env.ANTHROPIC_API_KEY) {
    return "environment";
  }
  if (getConfig().get("apiKey")) {
    return "config";
  }
  return "none";
}

// ============================================
// MODEL & SETTINGS
// ============================================

export function getDefaultModel(): string {
  return getConfig().get("defaultModel");
}

export function getTimeout(): number {
  return getConfig().get("timeout");
}

export function getMaxRetries(): number {
  return getConfig().get("maxRetries");
}

export function isVerbose(): boolean {
  return getConfig().get("verbose");
}

// ============================================
// CONFIG PATH (for diagnostics)
// ============================================

export function getConfigPath(): string {
  return getConfig().path;
}
