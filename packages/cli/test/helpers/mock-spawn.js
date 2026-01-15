/**
 * Mock Spawn Helper
 *
 * Helper riutilizzabile per mockare child_process.spawn
 * nei test della CLI.
 *
 * "16 agenti. 1 comando. Il tuo team AI."
 */

import EventEmitter from 'node:events';

/**
 * Crea mock ChildProcess configurabile
 *
 * @param {Object} config - Configurazione mock
 * @param {string} config.stdout - Output su stdout
 * @param {string} config.stderr - Output su stderr
 * @param {number} config.exitCode - Exit code (0 = success)
 * @param {number} config.delay - Delay prima di emettere output (ms)
 * @returns {MockProcess} - Mock process
 */
export function createMockProcess({
  stdout = '',
  stderr = '',
  exitCode = 0,
  delay = 10
} = {}) {
  class MockProcess extends EventEmitter {
    constructor() {
      super();
      this.stdout = new EventEmitter();
      this.stderr = new EventEmitter();
      this.exitCode = null;
      this.pid = Math.floor(Math.random() * 10000);
    }

    simulate() {
      if (stdout) {
        this.stdout.emit('data', Buffer.from(stdout));
      }
      if (stderr) {
        this.stderr.emit('data', Buffer.from(stderr));
      }
      this.exitCode = exitCode;
      this.emit('close', exitCode);
    }
  }

  const proc = new MockProcess();
  setTimeout(() => proc.simulate(), delay);
  return proc;
}

/**
 * Setup mock spawn con configurazione
 *
 * @param {Object} t - Test context (from node:test)
 * @param {Object} config - Configurazione per createMockProcess
 * @returns {Function} - Mock spawn function con tracking
 */
export function setupSpawnMock(t, config = {}) {
  const mockSpawn = t.mock.fn(() => createMockProcess(config));

  t.mock.module('node:child_process', {
    namedExports: { spawn: mockSpawn }
  });

  return mockSpawn;
}

/**
 * Crea mock spawn che risponde diversamente in base ai parametri
 *
 * @param {Object} t - Test context
 * @param {Object} responses - Mappa comando -> risposta
 * @returns {Function} - Mock spawn function
 */
export function setupConditionalSpawnMock(t, responses = {}) {
  const mockSpawn = t.mock.fn((command, args) => {
    // Cerca match in responses
    const key = args?.join(' ') || command;

    for (const [pattern, config] of Object.entries(responses)) {
      if (key.includes(pattern)) {
        return createMockProcess(config);
      }
    }

    // Default: successo
    return createMockProcess({ stdout: 'OK\n', exitCode: 0 });
  });

  t.mock.module('node:child_process', {
    namedExports: { spawn: mockSpawn }
  });

  return mockSpawn;
}
