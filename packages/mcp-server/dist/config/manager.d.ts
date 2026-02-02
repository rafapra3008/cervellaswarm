/**
 * Config Manager for MCP Server
 *
 * Shares configuration with CLI through `conf` package.
 * Same config file = CLI and MCP see same settings.
 *
 * Copyright 2026 Rafa & Cervella
 * Licensed under the Apache License, Version 2.0
 */
export declare function getApiKey(): string | null;
export declare function hasApiKey(): boolean;
export declare function getApiKeySource(): "environment" | "config" | "none";
export declare function getDefaultModel(): string;
export declare function getTimeout(): number;
export declare function getMaxRetries(): number;
export declare function isVerbose(): boolean;
export declare function getTier(): "free" | "pro" | "team" | "enterprise";
export declare function setTier(tier: "free" | "pro" | "team" | "enterprise"): void;
export declare function getConfigPath(): string;
export declare function getConfigDir(): string;
export interface ValidationResult {
    valid: boolean;
    error?: string;
    warning?: string;
}
export interface FormatValidationResult {
    valid: boolean;
    error?: string;
    suggestion?: string;
}
/**
 * Validate API key FORMAT only (no API call)
 * Fast check that can be done before every operation
 */
export declare function validateApiKeyFormat(key?: string | null): FormatValidationResult;
/**
 * Validate API key by making a minimal test call
 * Returns { valid: boolean, error?: string, warning?: string }
 */
export declare function validateApiKey(key?: string | null): Promise<ValidationResult>;
//# sourceMappingURL=manager.d.ts.map