/**
 * Agent Spawner for MCP Server
 *
 * Launches specialized agents via Anthropic API.
 * Port from CLI spawner.js to TypeScript.
 *
 * Copyright 2026 Rafa & Cervella
 * Licensed under the Apache License, Version 2.0
 */

import Anthropic from "@anthropic-ai/sdk";
import {
  getApiKey,
  getDefaultModel,
  getTimeout,
  getMaxRetries,
} from "../config/manager.js";

// Retry delays (ms)
const RETRY_DELAYS = [1000, 3000, 5000];

// Worker type definition
type WorkerType =
  | "backend"
  | "frontend"
  | "tester"
  | "docs"
  | "devops"
  | "data"
  | "security"
  | "researcher";

interface WorkerInfo {
  name: string;
  description: string;
}

interface SpawnResult {
  success: boolean;
  output?: string;
  error?: string;
  duration?: string;
  nextStep?: string;
  usage?: {
    inputTokens: number;
    outputTokens: number;
  };
  attempts?: number;
}

// Worker system prompts
const WORKER_PROMPTS: Record<WorkerType, string> = {
  backend: `Sei CERVELLA-BACKEND, specialista Python, FastAPI, Database, API REST, logica business.
Focus: Backend, API, database, server-side logic.
Stile: Codice pulito, ben documentato, testabile.
Output: Mostra il codice completo da creare/modificare.`,

  frontend: `Sei CERVELLA-FRONTEND, specialista React, CSS, Tailwind, UI/UX, componenti.
Focus: UI, componenti, styling, user experience.
Stile: Componenti riutilizzabili, accessibili, responsive.
Output: Mostra il codice JSX/CSS completo.`,

  tester: `Sei CERVELLA-TESTER, specialista Testing, Debug, QA, validazione.
Focus: Test unitari, integration test, bug hunting.
Stile: Test completi, edge cases, coverage alta.
Output: Mostra i test completi pronti per essere eseguiti.`,

  docs: `Sei CERVELLA-DOCS, specialista Documentazione, README, guide, tutorial.
Focus: Documentazione chiara, esempi pratici, getting started.
Stile: Conciso ma completo, utente-first.
Output: Mostra la documentazione markdown completa.`,

  devops: `Sei CERVELLA-DEVOPS, specialista Deploy, CI/CD, Docker, infrastruttura.
Focus: Deployment, automation, monitoring, infrastructure.
Stile: Sicuro, scalabile, automatizzato.
Output: Mostra configurazioni complete (Dockerfile, CI config, etc).`,

  data: `Sei CERVELLA-DATA, specialista SQL, analytics, query, database design.
Focus: Query ottimizzate, schema design, data integrity.
Stile: Performance-first, normalization quando serve.
Output: Mostra query SQL e schema completi.`,

  security: `Sei CERVELLA-SECURITY, specialista sicurezza, audit, vulnerabilita.
Focus: Security audit, vulnerabilities, best practices.
Stile: Defense in depth, zero trust, secure by default.
Output: Lista vulnerabilita trovate e fix raccomandati.`,

  researcher: `Sei CERVELLA-RESEARCHER, specialista ricerca tecnica, studi, analisi.
Focus: Ricerca approfondita, comparazioni, best practices.
Stile: Fonti affidabili, analisi critica, raccomandazioni chiare.
Output: Report strutturato con findings e raccomandazioni.`,
};

// Next step suggestions per worker type
const NEXT_STEPS: Record<WorkerType, string> = {
  backend: "Review the code and run: npm test",
  frontend: "Preview in browser: npm run dev",
  tester: "Run the test suite: npm test",
  docs: "Review documentation for clarity",
  devops: "Test deployment in staging first",
  data: "Verify query performance with EXPLAIN",
  security: "Apply the security fixes",
  researcher: "Apply findings to your project",
};

/**
 * Get all available workers
 */
export function getAvailableWorkers(): WorkerInfo[] {
  return [
    { name: "cervella-backend", description: "Python, FastAPI, API, Database" },
    { name: "cervella-frontend", description: "React, CSS, Tailwind, UI/UX" },
    { name: "cervella-tester", description: "Testing, Debug, QA" },
    { name: "cervella-docs", description: "Documentation, README, Guides" },
    { name: "cervella-devops", description: "Deploy, CI/CD, Docker" },
    { name: "cervella-data", description: "SQL, Analytics, Database Design" },
    {
      name: "cervella-security",
      description: "Security Audit, Vulnerabilities",
    },
    {
      name: "cervella-researcher",
      description: "Research, Analysis, Best Practices",
    },
  ];
}

/**
 * Sleep utility
 */
function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

/**
 * Build system prompt for worker
 */
function buildSystemPrompt(worker: WorkerType, context?: string): string {
  let prompt = WORKER_PROMPTS[worker];

  if (context) {
    prompt += `\n\nContesto progetto:\n${context}`;
  }

  prompt += `\n\nREGOLE:
- Scrivi codice REALE che funziona
- Se crei/modifichi file, indica chiaramente quali
- Sii conciso ma completo
- Segui le best practices del linguaggio`;

  return prompt;
}

/**
 * Spawn a worker to execute a task
 */
export async function spawnWorker(
  worker: WorkerType,
  task: string,
  context?: string
): Promise<SpawnResult> {
  const apiKey = getApiKey();

  if (!apiKey) {
    return {
      success: false,
      error: "API key not configured",
      nextStep: "Run cervellaswarm init or set ANTHROPIC_API_KEY",
    };
  }

  const systemPrompt = buildSystemPrompt(worker, context);
  const model = getDefaultModel();
  const maxTokens = 4096;
  const timeout = getTimeout();
  const maxRetries = getMaxRetries();

  const startTime = Date.now();
  let lastError: Error | null = null;
  let attempt = 0;

  while (attempt < maxRetries) {
    attempt++;

    try {
      const client = new Anthropic({ apiKey });

      // Create abort controller for timeout
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), timeout);

      try {
        const message = await client.messages.create(
          {
            model,
            max_tokens: maxTokens,
            system: systemPrompt,
            messages: [{ role: "user", content: task }],
          },
          { signal: controller.signal }
        );

        clearTimeout(timeoutId);

        const duration = Math.round((Date.now() - startTime) / 1000);
        const output = message.content
          .filter((block): block is Anthropic.TextBlock => block.type === "text")
          .map((block) => block.text)
          .join("\n");

        return {
          success: true,
          output: output.trim(),
          duration: `${duration}s`,
          nextStep: NEXT_STEPS[worker],
          usage: {
            inputTokens: message.usage.input_tokens,
            outputTokens: message.usage.output_tokens,
          },
          attempts: attempt,
        };
      } finally {
        clearTimeout(timeoutId);
      }
    } catch (error) {
      lastError = error instanceof Error ? error : new Error(String(error));

      // Check if retryable
      const status = (error as { status?: number }).status;
      const isRetryable = status === 429 || status === 500 || status === 503;

      if (!isRetryable || attempt >= maxRetries) {
        const duration = Math.round((Date.now() - startTime) / 1000);

        // Map error to user-friendly message
        let errorMessage = lastError.message;
        let nextStep = "Check the error and try again";

        if (status === 401) {
          errorMessage = "Invalid API key";
          nextStep = "Check your ANTHROPIC_API_KEY is correct";
        } else if (status === 403) {
          errorMessage = "API key lacks permission";
          nextStep = "Check your API key permissions at console.anthropic.com";
        } else if (status === 429) {
          errorMessage = "Rate limit exceeded";
          nextStep = "Wait a moment and try again";
        }

        return {
          success: false,
          error: errorMessage,
          duration: `${duration}s`,
          nextStep,
          attempts: attempt,
        };
      }

      // Wait before retry
      const delay =
        RETRY_DELAYS[attempt - 1] || RETRY_DELAYS[RETRY_DELAYS.length - 1];
      await sleep(delay);
    }
  }

  // Should not reach here
  return {
    success: false,
    error: lastError?.message || "Unknown error after retries",
    nextStep: "Check the error and try again",
    attempts: attempt,
  };
}
