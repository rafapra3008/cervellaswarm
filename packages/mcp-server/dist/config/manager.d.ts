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
export declare function getConfigPath(): string;
//# sourceMappingURL=manager.d.ts.map