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
// Schema for validation
const schema = {
    apiKey: { type: "string", default: "" },
    defaultModel: {
        type: "string",
        enum: ["claude-sonnet-4-20250514", "claude-opus-4-5-20251101"],
        default: "claude-sonnet-4-20250514",
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
// ============================================
// CONFIG PATH (for diagnostics)
// ============================================
export function getConfigPath() {
    return getConfig().path;
}
//# sourceMappingURL=manager.js.map