/**
 * Config Manager for MCP Server
 *
 * Shares configuration with CLI through `conf` package.
 * Same config file = CLI and MCP see same settings.
 *
 * Copyright 2026 CervellaSwarm Contributors
 * Licensed under the Apache License, Version 2.0
 */
import Conf from "conf";
// Schema for validation
const schema = {
    apiKey: { type: "string", default: "" },
    defaultModel: {
        type: "string",
        enum: ["claude-sonnet-4-6", "claude-opus-4-6", "claude-sonnet-4-20250514", "claude-opus-4-5-20251101"],
        default: "claude-sonnet-4-6",
    },
    timeout: {
        type: "number",
        minimum: 10000,
        maximum: 600000,
        default: 120000,
    },
    maxRetries: {
        type: "number",
        minimum: 1,
        maximum: 10,
        default: 3,
    },
    verbose: { type: "boolean", default: false },
    telemetry: { type: "boolean", default: false },
    tier: {
        type: "string",
        enum: ["free", "pro", "team", "enterprise"],
        default: "free",
    },
};
// Singleton config instance
// Uses same projectName as CLI = same config file!
let config = null;
function getConfig() {
    if (!config) {
        config = new Conf({
            projectName: "cervellaswarm", // Same as CLI!
            schema,
            defaults: {
                apiKey: "",
                defaultModel: "claude-sonnet-4-6",
                timeout: 120000,
                maxRetries: 3,
                verbose: false,
                telemetry: false,
                tier: "free",
            },
        });
    }
    return config;
}
// ============================================
// API KEY
// ============================================
export function getApiKey() {
    // Environment variable takes priority
    const envKey = process.env.ANTHROPIC_API_KEY;
    if (envKey) {
        return envKey;
    }
    // Fall back to saved config
    const savedKey = getConfig().get("apiKey");
    return savedKey || null;
}
export function hasApiKey() {
    return getApiKey() !== null;
}
export function getApiKeySource() {
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
export function getDefaultModel() {
    return getConfig().get("defaultModel");
}
export function getTimeout() {
    return getConfig().get("timeout");
}
export function getMaxRetries() {
    return getConfig().get("maxRetries");
}
export function isVerbose() {
    return getConfig().get("verbose");
}
export function getTier() {
    return getConfig().get("tier");
}
export function setTier(tier) {
    getConfig().set("tier", tier);
}
// ============================================
// CONFIG PATH (for diagnostics)
// ============================================
export function getConfigPath() {
    return getConfig().path;
}
export function getConfigDir() {
    const configPath = getConfig().path;
    return configPath.substring(0, configPath.lastIndexOf("/"));
}
/**
 * Validate API key FORMAT only (no API call)
 * Fast check that can be done before every operation
 */
export function validateApiKeyFormat(key = null) {
    const testKey = key || getApiKey();
    if (!testKey) {
        return {
            valid: false,
            error: "MISSING_API_KEY",
            suggestion: "Run: cervellaswarm init or set ANTHROPIC_API_KEY"
        };
    }
    if (!testKey.startsWith("sk-ant-")) {
        return {
            valid: false,
            error: "INVALID_API_KEY_FORMAT",
            suggestion: "API key must start with 'sk-ant-'. Get yours at https://console.anthropic.com/"
        };
    }
    // Basic length check (Anthropic keys are ~100+ chars)
    if (testKey.length < 40) {
        return {
            valid: false,
            error: "INVALID_API_KEY_FORMAT",
            suggestion: "API key seems too short. Get a valid key at https://console.anthropic.com/"
        };
    }
    return { valid: true };
}
/**
 * Validate API key by making a minimal test call
 * Returns { valid: boolean, error?: string, warning?: string }
 */
export async function validateApiKey(key = null) {
    const testKey = key || getApiKey();
    if (!testKey) {
        return { valid: false, error: "No API key provided" };
    }
    if (!testKey.startsWith("sk-ant-")) {
        return { valid: false, error: "Invalid key format (must start with sk-ant-)" };
    }
    try {
        // Dynamic import to avoid loading if not needed
        const Anthropic = (await import("@anthropic-ai/sdk")).default;
        const client = new Anthropic({ apiKey: testKey });
        // Minimal test call - just check if key works
        await client.messages.create({
            model: "claude-sonnet-4-6",
            max_tokens: 10,
            messages: [{ role: "user", content: "hi" }],
        });
        return { valid: true };
    }
    catch (error) {
        // Map error codes to user-friendly messages
        const status = error.status;
        const message = error.message;
        if (status === 401) {
            return { valid: false, error: "Invalid API key" };
        }
        if (status === 403) {
            return { valid: false, error: "API key lacks permissions" };
        }
        if (status === 429) {
            // Rate limited but key is valid!
            return { valid: true, warning: "Rate limited, but key is valid" };
        }
        if (status === 500 || status === 503) {
            return { valid: false, error: "Anthropic API temporarily unavailable" };
        }
        return { valid: false, error: message || "Unknown error" };
    }
}
//# sourceMappingURL=manager.js.map