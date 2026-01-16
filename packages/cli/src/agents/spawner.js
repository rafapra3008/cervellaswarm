/**
 * Agent Spawner
 *
 * Launches specialized agents to execute tasks.
 * Uses Anthropic API for REAL agent execution.
 *
 * "16 agenti. 1 comando. Il tuo team AI."
 *
 * Copyright 2026 Rafa & Cervella
 * Licensed under the Apache License, Version 2.0
 * http://www.apache.org/licenses/LICENSE-2.0
 */

import Anthropic from '@anthropic-ai/sdk';
import * as config from '../config/manager.js';

// Retry delays (ms between retries)
const RETRY_DELAYS = [1000, 3000, 5000];

/**
 * Get agent-specific system prompt
 */
function getAgentPrompt(agent, context) {
  const projectName = context?.name || 'this project';
  const projectDescription = context?.description || '';
  const projectPath = context?.path || process.cwd();

  const baseContext = `
Lavori su: ${projectName}${projectDescription ? ` - ${projectDescription}` : ''}
Path: ${projectPath}

REGOLE:
- Scrivi codice REALE che funziona
- Se crei/modifichi file, indica chiaramente quali
- Sii conciso ma completo
- Segui le best practices del linguaggio
`;

  const prompts = {
    'cervella-backend': `Sei CERVELLA-BACKEND, specialista Python, FastAPI, Database, API REST, logica business.
${baseContext}
Focus: Backend, API, database, server-side logic.
Stile: Codice pulito, ben documentato, testabile.
Output: Mostra il codice completo da creare/modificare.`,

    'cervella-frontend': `Sei CERVELLA-FRONTEND, specialista React, CSS, Tailwind, UI/UX, componenti.
${baseContext}
Focus: UI, componenti, styling, user experience.
Stile: Componenti riutilizzabili, accessibili, responsive.
Output: Mostra il codice JSX/CSS completo.`,

    'cervella-tester': `Sei CERVELLA-TESTER, specialista Testing, Debug, QA, validazione.
${baseContext}
Focus: Test unitari, integration test, bug hunting.
Stile: Test completi, edge cases, coverage alta.
Output: Mostra i test completi pronti per essere eseguiti.`,

    'cervella-docs': `Sei CERVELLA-DOCS, specialista Documentazione, README, guide, tutorial.
${baseContext}
Focus: Documentazione chiara, esempi pratici, getting started.
Stile: Conciso ma completo, utente-first.
Output: Mostra la documentazione markdown completa.`,

    'cervella-devops': `Sei CERVELLA-DEVOPS, specialista Deploy, CI/CD, Docker, infrastruttura.
${baseContext}
Focus: Deployment, automation, monitoring, infrastructure.
Stile: Sicuro, scalabile, automatizzato.
Output: Mostra configurazioni complete (Dockerfile, CI config, etc).`,

    'cervella-data': `Sei CERVELLA-DATA, specialista SQL, analytics, query, database design.
${baseContext}
Focus: Query ottimizzate, schema design, data integrity.
Stile: Performance-first, normalization quando serve.
Output: Mostra query SQL e schema completi.`,

    'cervella-security': `Sei CERVELLA-SECURITY, specialista sicurezza, audit, vulnerabilita.
${baseContext}
Focus: Security audit, vulnerabilities, best practices.
Stile: Defense in depth, zero trust, secure by default.
Output: Lista vulnerabilita trovate e fix raccomandati.`,

    'cervella-researcher': `Sei CERVELLA-RESEARCHER, specialista ricerca tecnica, studi, analisi.
${baseContext}
Focus: Ricerca approfondita, comparazioni, best practices.
Stile: Fonti affidabili, analisi critica, raccomandazioni chiare.
Output: Report strutturato con findings e raccomandazioni.`,
  };

  return prompts[agent] || prompts['cervella-backend'];
}

/**
 * Sleep for specified milliseconds
 */
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Check if error is retryable
 */
function _isRetryableError(error) {
  // Rate limit or server errors are retryable
  return error.status === 429 || error.status === 500 || error.status === 503;
}

/**
 * Get human-readable error info
 */
function getErrorInfo(error) {
  const errorMap = {
    401: {
      message: 'Invalid API key',
      nextStep: 'Check your ANTHROPIC_API_KEY is correct',
      retryable: false
    },
    403: {
      message: 'API key lacks permission',
      nextStep: 'Check your API key permissions at console.anthropic.com',
      retryable: false
    },
    429: {
      message: 'Rate limit exceeded',
      nextStep: 'Waiting and retrying automatically...',
      retryable: true
    },
    500: {
      message: 'Anthropic API error',
      nextStep: 'Retrying automatically...',
      retryable: true
    },
    503: {
      message: 'API temporarily unavailable',
      nextStep: 'Retrying automatically...',
      retryable: true
    },
    timeout: {
      message: 'Request timed out',
      nextStep: 'Task may be too complex. Try breaking it down.',
      retryable: false
    }
  };

  const status = error.name === 'AbortError' ? 'timeout' : error.status;
  return errorMap[status] || {
    message: error.message || 'Unknown error',
    nextStep: 'Check the error and try again',
    retryable: false
  };
}

/**
 * Spawn an agent to execute a task via Anthropic API
 */
export async function spawnAgent(agent, description, context, options = {}) {
  const apiKey = config.getApiKey();

  if (!apiKey) {
    console.log('');
    console.log('  API key not configured.');
    console.log('');
    console.log('  To use CervellaSwarm agents, you need an Anthropic API key:');
    console.log('');
    console.log('  Option 1: Run setup wizard');
    console.log('    $ cervellaswarm init');
    console.log('');
    console.log('  Option 2: Set environment variable');
    console.log('    $ export ANTHROPIC_API_KEY=sk-ant-...');
    console.log('');
    console.log('  Get your key at: https://console.anthropic.com/');
    console.log('');
    return {
      success: false,
      error: 'API key not configured',
      filesModified: [],
      nextStep: 'Run cervellaswarm init or set ANTHROPIC_API_KEY'
    };
  }

  const systemPrompt = getAgentPrompt(agent, context);
  const model = options.model || config.getDefaultModel();
  const maxTokens = options.maxTokens || 4096;
  const timeout = options.timeout || config.getTimeout();
  const maxRetries = options.maxRetries || config.getMaxRetries();

  const startTime = Date.now();
  let lastError = null;
  let attempt = 0;

  console.log('');
  console.log(`  Agent: ${agent}`);
  console.log(`  Model: ${model}`);
  console.log(`  Task: ${description}`);
  console.log('');

  while (attempt < maxRetries) {
    attempt++;

    try {
      const client = new Anthropic({ apiKey });

      if (attempt === 1) {
        console.log('  Working...');
      } else {
        console.log(`  Retry ${attempt}/${MAX_RETRIES}...`);
      }
      console.log('');

      // Create abort controller for timeout
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), timeout);

      try {
        const message = await client.messages.create({
          model,
          max_tokens: maxTokens,
          system: systemPrompt,
          messages: [
            {
              role: 'user',
              content: description
            }
          ]
        }, {
          signal: controller.signal
        });

        clearTimeout(timeoutId);

        const duration = Math.round((Date.now() - startTime) / 1000);
        const output = message.content
          .filter(block => block.type === 'text')
          .map(block => block.text)
          .join('\n');

        // Stream output to console
        console.log('  ─────────────────────────────────────────');
        console.log('');
        console.log(output);
        console.log('');
        console.log('  ─────────────────────────────────────────');

        return {
          success: true,
          output: output.trim(),
          duration: `${duration}s`,
          filesModified: extractFilesFromOutput(output),
          nextStep: suggestNextStep(agent, description),
          usage: {
            inputTokens: message.usage.input_tokens,
            outputTokens: message.usage.output_tokens
          },
          attempts: attempt
        };

      } finally {
        clearTimeout(timeoutId);
      }

    } catch (error) {
      lastError = error;
      const errorInfo = getErrorInfo(error);

      // If not retryable or last attempt, return error
      if (!errorInfo.retryable || attempt >= maxRetries) {
        const duration = Math.round((Date.now() - startTime) / 1000);

        console.log('');
        console.log(`  Error: ${errorInfo.message}`);
        if (attempt > 1) {
          console.log(`  (Failed after ${attempt} attempts)`);
        }
        console.log('');

        return {
          success: false,
          error: errorInfo.message,
          duration: `${duration}s`,
          filesModified: [],
          nextStep: errorInfo.nextStep,
          attempts: attempt
        };
      }

      // Wait before retry
      const delay = RETRY_DELAYS[attempt - 1] || RETRY_DELAYS[RETRY_DELAYS.length - 1];
      console.log(`  ${errorInfo.message}. Waiting ${delay / 1000}s before retry...`);
      await sleep(delay);
    }
  }

  // Should not reach here, but just in case
  const duration = Math.round((Date.now() - startTime) / 1000);
  return {
    success: false,
    error: lastError?.message || 'Unknown error after retries',
    duration: `${duration}s`,
    filesModified: [],
    nextStep: 'Check the error and try again',
    attempts: attempt
  };
}

/**
 * Extract files mentioned in agent output
 */
function extractFilesFromOutput(output) {
  const files = [];
  const patterns = [
    // Direct file mentions
    /(?:Create|Created|Modify|Modified|Update|Updated|Write|Wrote|Edit|Edited)(?:\s+file)?[:\s]+`?([^\s`\n]+\.[a-z]+)`?/gi,
    // Code block file headers
    /```[a-z]*\s*(?:\/\/|#|\/\*)\s*(?:File|Path)?[:\s]*([^\n]+\.[a-z]+)/gi,
    // Markdown file references
    /\*\*([^\*]+\.[a-z]+)\*\*/g,
    // Common file path patterns
    /(?:src|lib|test|components|pages|api)\/[^\s\n]+\.[a-z]+/gi
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
 * Suggest next step based on agent and task
 */
function suggestNextStep(agent, _description) {
  const suggestions = {
    'cervella-backend': 'Review the code and run: npm test',
    'cervella-frontend': 'Preview in browser: npm run dev',
    'cervella-tester': 'Run the test suite: npm test',
    'cervella-docs': 'Review documentation for clarity',
    'cervella-devops': 'Test deployment in staging first',
    'cervella-data': 'Verify query performance with EXPLAIN',
    'cervella-security': 'Apply the security fixes',
    'cervella-researcher': 'Apply findings to your project'
  };

  return suggestions[agent] || 'Continue with your next task';
}

/**
 * Get available agents list
 */
export function getAvailableAgents() {
  return [
    { name: 'cervella-backend', description: 'Python, FastAPI, API, Database' },
    { name: 'cervella-frontend', description: 'React, CSS, Tailwind, UI/UX' },
    { name: 'cervella-tester', description: 'Testing, Debug, QA' },
    { name: 'cervella-docs', description: 'Documentation, README, Guides' },
    { name: 'cervella-devops', description: 'Deploy, CI/CD, Docker' },
    { name: 'cervella-data', description: 'SQL, Analytics, Database Design' },
    { name: 'cervella-security', description: 'Security Audit, Vulnerabilities' },
    { name: 'cervella-researcher', description: 'Research, Analysis, Best Practices' }
  ];
}

/**
 * Check if spawner is ready (API key available)
 */
export function isReady() {
  return config.hasApiKey();
}
