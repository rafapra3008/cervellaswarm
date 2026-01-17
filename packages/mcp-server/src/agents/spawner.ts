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
  | "researcher"
  // New workers
  | "marketing"
  | "ingegnera"
  | "scienziata"
  | "reviewer"
  // Guardiane (quality gates)
  | "guardiana-qualita"
  | "guardiana-ricerca"
  | "guardiana-ops"
  // Regina
  | "orchestrator";

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

  // NEW WORKERS
  marketing: `Sei CERVELLA-MARKETING, specialista UX strategy, posizionamento, copywriting.
Focus: Dove mettere bottoni, user flow, landing page, messaggi, analisi utente.
Stile: User-centered, data-driven, persuasivo ma onesto.
Output: Specifiche UX/UI dettagliate con razionale per ogni scelta.`,

  ingegnera: `Sei CERVELLA-INGEGNERA, specialista analisi codebase, technical debt, refactoring.
Focus: Trovare file grandi, codice duplicato, TODO dimenticati, problemi di architettura.
Stile: Analitica, sistemica, propone miglioramenti concreti.
Output: Report analisi con lista prioritizzata di interventi.
IMPORTANTE: Analizzi e proponi, NON modifichi direttamente.`,

  scienziata: `Sei CERVELLA-SCIENZIATA, specialista ricerca STRATEGICA, trend di mercato, competitor analysis.
Focus: Capire il mercato, monitorare competitor, trovare opportunità business.
Stile: Visione macro, dati reali, insights azionabili.
Output: Report strategico con opportunità e rischi.
NOTA: Diversa da researcher (tecnica), tu guardi il BUSINESS.`,

  reviewer: `Sei CERVELLA-REVIEWER, specialista code review, best practices, architettura.
Focus: Review di codice, controllo qualità, suggerimenti di miglioramento, verifica pattern.
Stile: Costruttiva, specifica, con esempi di codice migliorato.
Output: Lista di osservazioni con severity (critico/importante/suggerimento).`,

  // GUARDIANE - Quality Gates (usano Opus)
  "guardiana-qualita": `Sei CERVELLA-GUARDIANA-QUALITA, la guardiana che verifica output e standard codice.
Ruolo: Verifichi il lavoro di frontend, backend, tester PRIMA che venga considerato fatto.
Focus: Qualità codice, test coverage, best practices, standard 9.5 minimo!
Stile: Rigorosa ma costruttiva, feedback specifico e azionabile.
Output: Verdetto (APPROVATO/DA RIVEDERE) con lista dettagliata di cosa sistemare.
STANDARD: Se non è almeno 9.5/10, non passa!`,

  "guardiana-ricerca": `Sei CERVELLA-GUARDIANA-RICERCA, la guardiana che verifica qualità delle ricerche.
Ruolo: Verifichi il lavoro di researcher, docs, scienziata per accuratezza e completezza.
Focus: Fonti verificabili, bias detection, completezza analisi.
Stile: Scettica costruttiva, verifica cross-reference.
Output: Verdetto (VERIFICATO/DA APPROFONDIRE) con note su cosa manca o è impreciso.`,

  "guardiana-ops": `Sei CERVELLA-GUARDIANA-OPS, la guardiana che supervisiona deploy, security, data.
Ruolo: Verifichi il lavoro di devops, security, data PRIMA di andare in produzione.
Focus: Sicurezza, performance, backup, rollback plan, compliance.
Stile: Zero tolerance per rischi non mitigati.
Output: Verdetto (PRONTO PER DEPLOY/BLOCCO) con checklist di sicurezza.`,

  // REGINA - Orchestrator
  orchestrator: `Sei CERVELLA-ORCHESTRATOR, la REGINA dello sciame CervellaSwarm.
Ruolo: Coordini tutti i 16 agenti, deleghi task, verifichi qualità finale.
Focus: Orchestrazione intelligente, non fai lavoro diretto - DELEGHI sempre!
Stile: Strategica, visione d'insieme, quality-first.
Output: Piano di esecuzione con assegnazione task ai worker appropriati.
REGOLA D'ORO: Tu coordini, le Guardiane verificano, i Worker eseguono.`,
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
  // New workers
  marketing: "Validate UX decisions with user testing",
  ingegnera: "Prioritize technical debt items",
  scienziata: "Share strategic insights with the team",
  reviewer: "Address critical issues first, then important ones",
  // Guardiane
  "guardiana-qualita": "If APPROVATO: proceed. If DA RIVEDERE: fix and resubmit",
  "guardiana-ricerca": "If VERIFICATO: publish. If DA APPROFONDIRE: research more",
  "guardiana-ops": "If PRONTO: deploy. If BLOCCO: address security concerns first",
  // Regina
  orchestrator: "Execute the plan with the assigned workers",
};

/**
 * Get all available workers
 */
export function getAvailableWorkers(): WorkerInfo[] {
  return [
    // API Workers (12)
    { name: "backend", description: "Python, FastAPI, API, Database" },
    { name: "frontend", description: "React, CSS, Tailwind, UI/UX" },
    { name: "tester", description: "Testing, Debug, QA" },
    { name: "docs", description: "Documentation, README, Guides" },
    { name: "devops", description: "Deploy, CI/CD, Docker" },
    { name: "data", description: "SQL, Analytics, Database Design" },
    { name: "security", description: "Security Audit, Vulnerabilities" },
    { name: "researcher", description: "Research, Analysis, Best Practices" },
    { name: "marketing", description: "UX Strategy, Positioning, Copywriting" },
    { name: "ingegnera", description: "Architecture, Refactoring, Tech Debt" },
    { name: "scienziata", description: "Market Research, Competitor Analysis" },
    { name: "reviewer", description: "Code Review, Best Practices" },
    // Guardiane (3) - Quality Gates
    { name: "guardiana-qualita", description: "Verifies code quality (9.5+ standard)" },
    { name: "guardiana-ricerca", description: "Verifies research accuracy" },
    { name: "guardiana-ops", description: "Verifies deploy safety & security" },
    // Regina (1)
    { name: "orchestrator", description: "The Queen - Coordinates all agents" },
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
          nextStep =
            "Your API key is invalid. Get a new one at https://console.anthropic.com/";
        } else if (status === 403) {
          errorMessage = "API key lacks permissions";
          nextStep =
            "Your API key doesn't have the required permissions. Check at https://console.anthropic.com/";
        } else if (status === 429) {
          errorMessage = "Rate limit exceeded";
          nextStep =
            "You've hit the rate limit. Wait a few seconds and try again, or upgrade your plan.";
        } else if (status === 500) {
          errorMessage = "Anthropic API server error";
          nextStep =
            "Anthropic is having issues. Check https://status.anthropic.com/ and try again later.";
        } else if (status === 503) {
          errorMessage = "Anthropic API temporarily unavailable";
          nextStep =
            "The API is temporarily overloaded. Wait a moment and try again.";
        } else if (lastError.name === "AbortError") {
          errorMessage = "Request timed out";
          nextStep = `The request took too long. Try a simpler task or increase timeout.`;
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
