/**
 * Worker Utilities
 *
 * Helper functions for agent operations.
 *
 * Copyright 2026 Rafa & Cervella
 * Licensed under the Apache License, Version 2.0
 */

/**
 * Extract file paths mentioned in agent output
 *
 * Looks for common patterns:
 * - "Create file: path/to/file.ts"
 * - Code block headers with file paths
 * - Markdown bold file references
 * - Common directory patterns (src/, lib/, etc.)
 */
export function extractFilesFromOutput(output: string): string[] {
  const files: string[] = [];
  const patterns = [
    // Direct file mentions
    /(?:Create|Created|Modify|Modified|Update|Updated|Write|Wrote|Edit|Edited)(?:\s+file)?[:\s]+`?([^\s`\n]+\.[a-z]+)`?/gi,
    // Code block file headers
    /```[a-z]*\s*(?:\/\/|#|\/\*)\s*(?:File|Path)?[:\s]*([^\n]+\.[a-z]+)/gi,
    // Markdown file references
    /\*\*([^\*]+\.[a-z]+)\*\*/g,
    // Common file path patterns
    /(?:src|lib|test|tests|components|pages|api|utils|services|hooks|styles)\/[^\s\n]+\.[a-z]+/gi
  ];

  for (const pattern of patterns) {
    let match;
    while ((match = pattern.exec(output)) !== null) {
      const file = match[1] || match[0];
      const cleanFile = file.trim().replace(/[`*]/g, '');
      if (cleanFile && !files.includes(cleanFile) && cleanFile.includes('.')) {
        files.push(cleanFile);
      }
    }
  }

  return [...new Set(files)]; // Remove duplicates
}

/**
 * Extract code blocks from agent output
 *
 * Returns array of { language, code, filename? }
 */
export function extractCodeBlocks(output: string): Array<{
  language: string;
  code: string;
  filename?: string;
}> {
  const blocks: Array<{ language: string; code: string; filename?: string }> = [];
  const codeBlockRegex = /```(\w*)\s*(?:\/\/\s*([^\n]+))?\n([\s\S]*?)```/g;

  let match;
  while ((match = codeBlockRegex.exec(output)) !== null) {
    blocks.push({
      language: match[1] || 'text',
      filename: match[2]?.trim(),
      code: match[3].trim()
    });
  }

  return blocks;
}

/**
 * Estimate token count from text (rough estimate)
 *
 * Uses ~4 chars per token as approximation
 */
export function estimateTokens(text: string): number {
  return Math.ceil(text.length / 4);
}

/**
 * Format duration from milliseconds to human-readable string
 */
export function formatDuration(ms: number): string {
  if (ms < 1000) {
    return `${ms}ms`;
  }
  const seconds = Math.round(ms / 1000);
  if (seconds < 60) {
    return `${seconds}s`;
  }
  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = seconds % 60;
  return `${minutes}m ${remainingSeconds}s`;
}

/**
 * Truncate text to max length with ellipsis
 */
export function truncateText(text: string, maxLength: number): string {
  if (text.length <= maxLength) {
    return text;
  }
  return text.slice(0, maxLength - 3) + '...';
}

/**
 * Parse agent name from various formats
 *
 * Handles: 'backend', 'cervella-backend', 'CERVELLA-BACKEND'
 */
export function parseAgentName(input: string): {
  type: string;
  fullName: string;
} {
  const normalized = input.toLowerCase().trim();
  const type = normalized.replace(/^cervella-/, '');
  const fullName = `cervella-${type}`;

  return { type, fullName };
}

/**
 * Check if output contains error indicators
 */
export function hasErrorIndicators(output: string): boolean {
  const errorPatterns = [
    /error:/i,
    /exception:/i,
    /failed:/i,
    /cannot\s+(?:find|read|write|access)/i,
    /permission\s+denied/i,
    /not\s+found/i
  ];

  return errorPatterns.some(pattern => pattern.test(output));
}

/**
 * Extract summary line from agent output
 *
 * Looks for common summary patterns at the end of output
 */
export function extractSummary(output: string, maxLength = 200): string {
  const lines = output.trim().split('\n').filter(l => l.trim());

  // Look for summary section
  const summaryIndex = lines.findIndex(l =>
    /^(?:summary|conclusion|result|done|completed):/i.test(l)
  );

  if (summaryIndex >= 0 && summaryIndex < lines.length - 1) {
    const summaryLines = lines.slice(summaryIndex + 1, summaryIndex + 4);
    return truncateText(summaryLines.join(' ').trim(), maxLength);
  }

  // Fall back to last non-empty line
  const lastLine = lines[lines.length - 1] || '';
  return truncateText(lastLine, maxLength);
}
