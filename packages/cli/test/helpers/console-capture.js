/**
 * Console Capture Helper
 *
 * Helper per catturare output console nei test.
 *
 * "I dettagli fanno SEMPRE la differenza."
 */

/**
 * Cattura output console durante un test
 *
 * @param {Object} t - Test context (from node:test)
 * @returns {Object} - { logs, errors, warnings }
 *
 * @example
 * const output = captureConsole(t);
 * myFunction();
 * assert.ok(output.logs.includes('Success'));
 */
export function captureConsole(t) {
  const logs = [];
  const errors = [];
  const warnings = [];

  // Mock console methods
  t.mock.method(console, 'log', (...args) => {
    logs.push(args.map(arg => String(arg)).join(' '));
  });

  t.mock.method(console, 'error', (...args) => {
    errors.push(args.map(arg => String(arg)).join(' '));
  });

  t.mock.method(console, 'warn', (...args) => {
    warnings.push(args.map(arg => String(arg)).join(' '));
  });

  return {
    logs,
    errors,
    warnings,
    // Helper per cercare in tutto l'output
    hasOutput: (text) => {
      return logs.some(l => l.includes(text)) ||
             errors.some(e => e.includes(text)) ||
             warnings.some(w => w.includes(text));
    },
    // Helper per cercare solo nei log
    hasLog: (text) => logs.some(l => l.includes(text)),
    // Helper per cercare solo negli errori
    hasError: (text) => errors.some(e => e.includes(text)),
    // Stampa tutto l'output (per debug)
    dump: () => {
      console.log('=== LOGS ===');
      logs.forEach(l => console.log(l));
      console.log('=== ERRORS ===');
      errors.forEach(e => console.log(e));
      console.log('=== WARNINGS ===');
      warnings.forEach(w => console.log(w));
    }
  };
}

/**
 * Cattura stdout/stderr di process
 *
 * @param {Object} t - Test context
 * @returns {Object} - { stdout, stderr }
 */
export function captureProcessOutput(t) {
  const stdout = [];
  const stderr = [];

  const originalStdoutWrite = process.stdout.write.bind(process.stdout);
  const originalStderrWrite = process.stderr.write.bind(process.stderr);

  t.mock.method(process.stdout, 'write', (chunk) => {
    stdout.push(chunk.toString());
    return true;
  });

  t.mock.method(process.stderr, 'write', (chunk) => {
    stderr.push(chunk.toString());
    return true;
  });

  // Restore alla fine del test
  t.after(() => {
    process.stdout.write = originalStdoutWrite;
    process.stderr.write = originalStderrWrite;
  });

  return {
    stdout,
    stderr,
    getStdout: () => stdout.join(''),
    getStderr: () => stderr.join('')
  };
}
