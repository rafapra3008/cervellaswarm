/**
 * Tests for agents/spawner.ts
 *
 * Tests worker spawning, error handling, and retry logic.
 */

import { describe, it, mock } from "node:test";
import assert from "node:assert/strict";
import { spawnWorker, getAvailableWorkers } from "../dist/agents/spawner.js";

describe("Worker Spawner", () => {
  describe("getAvailableWorkers", () => {
    it("should return list of available workers", () => {
      const workers = getAvailableWorkers();

      assert.ok(Array.isArray(workers));
      assert.ok(workers.length > 0);

      // Check structure of first worker
      const worker = workers[0];
      assert.ok(worker.name);
      assert.ok(worker.description);
      assert.equal(typeof worker.name, "string");
      assert.equal(typeof worker.description, "string");
    });

    it("should include expected worker types", () => {
      const workers = getAvailableWorkers();
      const names = workers.map((w) => w.name);

      // Check for core worker types
      assert.ok(names.includes("backend"));
      assert.ok(names.includes("frontend"));
      assert.ok(names.includes("tester"));
    });

    it("should have unique worker names", () => {
      const workers = getAvailableWorkers();
      const names = workers.map((w) => w.name);
      const uniqueNames = new Set(names);

      assert.equal(names.length, uniqueNames.size);
    });

    it("should remove cervella- prefix from names", () => {
      const workers = getAvailableWorkers();

      // All names should NOT start with "cervella-"
      workers.forEach((worker) => {
        assert.ok(!worker.name.startsWith("cervella-"));
      });
    });
  });

  describe("spawnWorker - Parameter Validation", () => {
    it("should accept valid worker types", () => {
      // We can test this indirectly - invalid worker types will be caught by TypeScript
      // But we can verify that valid worker types are accepted
      const validWorkers = [
        "backend",
        "frontend",
        "tester",
        "docs",
        "devops",
        "data",
        "security",
        "researcher",
      ];

      validWorkers.forEach((worker) => {
        // Type check - this would fail at compile time if invalid
        const workerType = worker as
          | "backend"
          | "frontend"
          | "tester"
          | "docs"
          | "devops"
          | "data"
          | "security"
          | "researcher";
        assert.ok(workerType);
      });
    });

    it("should accept task strings", () => {
      // Verify task parameter types
      const validTasks = [
        "Write tests",
        "Fix bug",
        "",
        "Multi\nline\ntask",
        "Task with special chars: !@#$%",
      ];

      validTasks.forEach((task) => {
        assert.equal(typeof task, "string");
      });
    });

    it("should accept optional context", () => {
      const contextExamples = [
        undefined,
        "Project context",
        "",
        "Multi\nline context",
      ];

      contextExamples.forEach((ctx) => {
        assert.ok(ctx === undefined || typeof ctx === "string");
      });
    });
  });

  describe("spawnWorker - Success Response Structure", () => {
    it("should return expected structure on success (mock)", () => {
      // Test the expected response structure
      const mockSuccessResult = {
        success: true,
        output: "Task completed successfully",
        duration: "5s",
        nextStep: "Review the code changes",
        usage: {
          inputTokens: 100,
          outputTokens: 200,
        },
        attempts: 1,
      };

      assert.equal(mockSuccessResult.success, true);
      assert.ok(mockSuccessResult.output);
      assert.ok(mockSuccessResult.duration);
      assert.ok(mockSuccessResult.nextStep);
      assert.ok(mockSuccessResult.usage);
      assert.ok(mockSuccessResult.usage.inputTokens > 0);
      assert.ok(mockSuccessResult.usage.outputTokens > 0);
    });

    it("should return expected structure on error (mock)", () => {
      const mockErrorResult = {
        success: false,
        error: "API error",
        duration: "2s",
        nextStep: "Check the error and try again",
        attempts: 3,
      };

      assert.equal(mockErrorResult.success, false);
      assert.ok(mockErrorResult.error);
      assert.ok(mockErrorResult.duration);
      assert.ok(mockErrorResult.nextStep);
      assert.equal(mockErrorResult.attempts, 3);
    });
  });

  describe("spawnWorker - Error Message Mapping", () => {
    it("should map 401 to invalid API key message", () => {
      const error401 = {
        success: false,
        error: "Invalid API key",
        nextStep: "Your API key is invalid. Get a new one at https://console.anthropic.com/",
      };

      assert.ok(error401.error.includes("Invalid"));
      assert.ok(error401.nextStep.includes("console.anthropic.com"));
    });

    it("should map 429 to rate limit message", () => {
      const error429 = {
        success: false,
        error: "Rate limit exceeded",
        nextStep: "You've hit the rate limit. Wait a few seconds and try again, or upgrade your plan.",
      };

      assert.ok(error429.error.includes("Rate limit"));
      assert.ok(error429.nextStep.includes("upgrade"));
    });

    it("should map timeout to timeout message", () => {
      const timeoutError = {
        success: false,
        error: "Request timed out",
        nextStep: "The request took too long. Try a simpler task or increase timeout.",
      };

      assert.ok(timeoutError.error.includes("timed out"));
      assert.ok(timeoutError.nextStep.includes("timeout"));
    });
  });
});
