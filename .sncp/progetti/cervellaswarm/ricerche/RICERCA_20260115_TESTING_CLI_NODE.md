# Ricerca: Testing CLI Node.js con node:test

**Data:** 15 Gennaio 2026
**Progetto:** CervellaSwarm CLI
**Ricercatrice:** Cervella Researcher
**Obiettivo:** Pattern PRATICI per testare CLI con node:test runner

---

## TL;DR - Decisioni Chiave

```
✅ @inquirer/testing per mock prompt (UFFICIALE!)
✅ node:test mock.fn() per child_process.spawn
✅ Struttura: test/ alla root del package
✅ ZERO dipendenze extra (tutto built-in!)

AGGIUNGI SOLO: @inquirer/testing (devDependencies)
```

---

## 1. MOCK INQUIRER - @inquirer/testing (UFFICIALE)

### Installazione

```json
// package.json
{
  "devDependencies": {
    "@inquirer/testing": "^2.x.x"
  }
}
```

### Esempio PRATICO - Test Wizard

```javascript
// test/wizard.test.js
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { render } from '@inquirer/testing';
import { input } from '@inquirer/prompts';

test('wizard - project name validation', async () => {
  const { answer, events, getScreen } = await render(input, {
    message: 'Project name:',
    validate: (value) => {
      if (!/^[a-z0-9-]+$/.test(value)) {
        return 'Use lowercase letters, numbers, and hyphens only';
      }
      return true;
    }
  });

  // Verifica rendering iniziale
  assert.ok(getScreen().includes('Project name:'));

  // Simula input utente
  events.type('MyProject123'); // Invalido!
  events.keypress('enter');

  // Verifica errore validazione
  assert.ok(getScreen().includes('lowercase'));

  // Input corretto
  events.type('my-project-123');
  events.keypress('enter');

  // Verifica risposta
  const result = await answer;
  assert.equal(result, 'my-project-123');
});

test('wizard - select question', async () => {
  const { answer, events, getScreen } = await render(
    async () => {
      const { select } = await import('@inquirer/prompts');
      return select({
        message: 'Project type:',
        choices: [
          { name: 'Web Application', value: 'webapp' },
          { name: 'CLI Tool', value: 'cli' }
        ]
      });
    }
  );

  // Verifica menu visibile
  assert.ok(getScreen().includes('Web Application'));

  // Naviga menu
  events.keypress('down'); // Vai a CLI Tool
  events.keypress('enter');

  // Verifica selezione
  const result = await answer;
  assert.equal(result, 'cli');
});
```

### API @inquirer/testing

```javascript
const { answer, events, getScreen } = await render(promptFunction, config);

// answer: Promise<any>
//   - Risolve con la risposta finale

// getScreen({ raw: false }): string
//   - Ottieni output CLI corrente
//   - raw: true = include ANSI codes

// events.type(text: string)
//   - Simula digitazione testo

// events.keypress(key: string | { name: string })
//   - Simula pressione tasto
//   - Esempi: 'enter', 'up', 'down', 'space'
```

---

## 2. MOCK CHILD_PROCESS - node:test (BUILT-IN)

### Esempio PRATICO - Mock spawn()

```javascript
// test/agents.test.js
import { test } from 'node:test';
import assert from 'node:assert/strict';
import EventEmitter from 'node:events';

test('spawn agent - success', async (t) => {
  // Mock ChildProcess che simula claude spawn
  class MockChildProcess extends EventEmitter {
    constructor() {
      super();
      this.stdout = new EventEmitter();
      this.stderr = new EventEmitter();
      this.exitCode = null;
    }

    // Simula output claude
    simulateOutput() {
      this.stdout.emit('data', Buffer.from('Task completed\n'));
      this.emit('close', 0); // Exit code 0 = successo
    }
  }

  // Mock spawn function
  const mockSpawn = t.mock.fn(() => {
    const process = new MockChildProcess();
    // Simula output dopo 10ms
    setTimeout(() => process.simulateOutput(), 10);
    return process;
  });

  // Mock del modulo child_process
  t.mock.module('node:child_process', {
    namedExports: {
      spawn: mockSpawn
    }
  });

  // IMPORTANTE: Import DOPO mock setup
  const { spawn } = await import('node:child_process');

  // Testa la funzione che usa spawn
  const agentProcess = spawn('claude', ['--model', 'sonnet']);

  let output = '';
  agentProcess.stdout.on('data', (data) => {
    output += data.toString();
  });

  await new Promise(resolve => {
    agentProcess.on('close', resolve);
  });

  // Verifica chiamata
  assert.equal(mockSpawn.mock.calls.length, 1);
  assert.deepEqual(mockSpawn.mock.calls[0].arguments, [
    'claude',
    ['--model', 'sonnet']
  ]);

  // Verifica output
  assert.ok(output.includes('Task completed'));
});

test('spawn agent - error handling', async (t) => {
  // Mock per simulare errore
  const mockSpawn = t.mock.fn(() => {
    const process = new EventEmitter();
    process.stdout = new EventEmitter();
    process.stderr = new EventEmitter();

    setTimeout(() => {
      process.stderr.emit('data', Buffer.from('Error: Model not found\n'));
      process.emit('close', 1); // Exit code 1 = errore
    }, 10);

    return process;
  });

  t.mock.module('node:child_process', {
    namedExports: { spawn: mockSpawn }
  });

  const { spawn } = await import('node:child_process');
  const agentProcess = spawn('claude', ['--model', 'invalid']);

  let errorOutput = '';
  agentProcess.stderr.on('data', (data) => {
    errorOutput += data.toString();
  });

  const exitCode = await new Promise(resolve => {
    agentProcess.on('close', resolve);
  });

  assert.equal(exitCode, 1);
  assert.ok(errorOutput.includes('Model not found'));
});
```

---

## 3. MOCK MULTIPLI - Pattern Avanzato

### Mock sia inquirer CHE spawn

```javascript
// test/task-command.test.js
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { render } from '@inquirer/testing';
import EventEmitter from 'node:events';

test('task command - full workflow', async (t) => {
  // Mock spawn
  const mockSpawn = t.mock.fn(() => {
    const proc = new EventEmitter();
    proc.stdout = new EventEmitter();
    proc.stderr = new EventEmitter();
    setTimeout(() => {
      proc.stdout.emit('data', Buffer.from('Agent working...\n'));
      proc.emit('close', 0);
    }, 10);
    return proc;
  });

  t.mock.module('node:child_process', {
    namedExports: { spawn: mockSpawn }
  });

  // Import DOPO mock
  const { spawn } = await import('node:child_process');

  // Test prompt + spawn insieme
  const taskPrompt = async () => {
    const { input } = await import('@inquirer/prompts');
    return input({
      message: 'Describe your task:',
      validate: (v) => v.length > 0 || 'Required'
    });
  };

  const { answer, events } = await render(taskPrompt);

  // Simula input
  events.type('Fix bug in auth');
  events.keypress('enter');

  const taskDescription = await answer;
  assert.equal(taskDescription, 'Fix bug in auth');

  // Spawn agent con task description
  const agentProc = spawn('claude', ['--task', taskDescription]);

  let output = '';
  agentProc.stdout.on('data', (d) => output += d);

  await new Promise(resolve => agentProc.on('close', resolve));

  // Verifica spawn chiamato correttamente
  assert.equal(mockSpawn.mock.calls.length, 1);
  assert.ok(mockSpawn.mock.calls[0].arguments[1].includes('Fix bug in auth'));
  assert.ok(output.includes('Agent working'));
});
```

---

## 4. TEST CONSOLE OUTPUT

### Catturare console.log/error

```javascript
// test/display.test.js
import { test } from 'node:test';
import assert from 'node:assert/strict';

test('display status - console output', async (t) => {
  const logs = [];
  const errors = [];

  // Mock console
  const originalLog = console.log;
  const originalError = console.error;

  t.mock.method(console, 'log', (...args) => {
    logs.push(args.join(' '));
  });

  t.mock.method(console, 'error', (...args) => {
    errors.push(args.join(' '));
  });

  // Testa funzione che stampa
  const displayStatus = () => {
    console.log('Status: Active');
    console.log('Agents: 16');
  };

  displayStatus();

  // Verifica output
  assert.equal(logs.length, 2);
  assert.ok(logs[0].includes('Active'));
  assert.ok(logs[1].includes('16'));

  // Cleanup automatico alla fine del test
  // (node:test restora automaticamente i mock)
});
```

---

## 5. DIRECTORY TEMPORANEE - Pattern fs

### Setup/Teardown con fs

```javascript
// test/sncp-init.test.js
import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';

test('sncp init - creates structure', async (t) => {
  // Crea temp dir
  const tempDir = await fs.mkdtemp(
    path.join(os.tmpdir(), 'cervellaswarm-test-')
  );

  // Cleanup automatico alla fine
  t.after(async () => {
    await fs.rm(tempDir, { recursive: true, force: true });
  });

  // Test la funzione che crea SNCP
  const sncpInit = async (projectDir) => {
    const sncpDir = path.join(projectDir, '.sncp');
    await fs.mkdir(sncpDir, { recursive: true });
    await fs.mkdir(path.join(sncpDir, 'idee'));
    await fs.mkdir(path.join(sncpDir, 'decisioni'));
    await fs.writeFile(
      path.join(sncpDir, 'stato.md'),
      '# Stato Progetto\n'
    );
  };

  await sncpInit(tempDir);

  // Verifica struttura creata
  const sncpPath = path.join(tempDir, '.sncp');
  const stat = await fs.stat(sncpPath);
  assert.ok(stat.isDirectory());

  const ideePath = path.join(sncpPath, 'idee');
  const ideeStat = await fs.stat(ideePath);
  assert.ok(ideeStat.isDirectory());

  const statoPath = path.join(sncpPath, 'stato.md');
  const statoContent = await fs.readFile(statoPath, 'utf-8');
  assert.ok(statoContent.includes('Stato Progetto'));
});
```

---

## 6. STRUTTURA CONSIGLIATA

```
packages/cli/
├── src/
│   ├── commands/
│   ├── wizard/
│   ├── agents/
│   └── sncp/
├── test/
│   ├── commands/
│   │   ├── init.test.js
│   │   ├── task.test.js
│   │   └── resume.test.js
│   ├── wizard/
│   │   └── questions.test.js
│   ├── agents/
│   │   ├── spawner.test.js
│   │   └── router.test.js
│   ├── sncp/
│   │   ├── init.test.js
│   │   └── writer.test.js
│   └── helpers/
│       ├── mock-spawn.js      # Helper per mock spawn
│       └── temp-dir.js        # Helper per temp directories
└── package.json
```

### Naming Convention

```
✅ nome.test.js         - File test
✅ nome.spec.js         - Alternativa (meno comune)
❌ test-nome.js         - Non standard
❌ nome_test.js         - Underscore evitato
```

### Script package.json

```json
{
  "scripts": {
    "test": "node --test",
    "test:watch": "node --test --watch",
    "test:coverage": "node --test --experimental-test-coverage",
    "test:commands": "node --test test/commands/",
    "test:wizard": "node --test test/wizard/"
  }
}
```

---

## 7. HELPER RIUTILIZZABILI

### mock-spawn.js

```javascript
// test/helpers/mock-spawn.js
import EventEmitter from 'node:events';

/**
 * Crea mock ChildProcess configurabile
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
 */
export function setupSpawnMock(t, config = {}) {
  const mockSpawn = t.mock.fn(() => createMockProcess(config));

  t.mock.module('node:child_process', {
    namedExports: { spawn: mockSpawn }
  });

  return mockSpawn;
}
```

### temp-dir.js

```javascript
// test/helpers/temp-dir.js
import fs from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';

/**
 * Crea directory temporanea con cleanup automatico
 */
export async function createTempDir(t, prefix = 'test-') {
  const tempDir = await fs.mkdtemp(
    path.join(os.tmpdir(), prefix)
  );

  t.after(async () => {
    await fs.rm(tempDir, { recursive: true, force: true });
  });

  return tempDir;
}

/**
 * Crea struttura file per test
 */
export async function createFileStructure(baseDir, structure) {
  for (const [filePath, content] of Object.entries(structure)) {
    const fullPath = path.join(baseDir, filePath);
    const dir = path.dirname(fullPath);

    await fs.mkdir(dir, { recursive: true });

    if (typeof content === 'string') {
      await fs.writeFile(fullPath, content);
    }
  }
}
```

### Uso Helper

```javascript
// test/commands/init.test.js
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createTempDir, createFileStructure } from '../helpers/temp-dir.js';
import { setupSpawnMock } from '../helpers/mock-spawn.js';

test('init command - full flow', async (t) => {
  const tempDir = await createTempDir(t);

  await createFileStructure(tempDir, {
    'package.json': '{"name":"test"}',
    'src/index.js': 'console.log("hi");'
  });

  setupSpawnMock(t, {
    stdout: 'Initialization complete\n',
    exitCode: 0
  });

  // Testa init command...
  assert.ok(true);
});
```

---

## 8. DIPENDENZE FINALI

### package.json

```json
{
  "type": "module",
  "scripts": {
    "test": "node --test",
    "test:watch": "node --test --watch"
  },
  "dependencies": {
    "commander": "^12.1.0",
    "@inquirer/prompts": "^7.2.0",
    "chalk": "^5.3.0"
  },
  "devDependencies": {
    "@inquirer/testing": "^2.2.0"
  }
}
```

**ZERO altre dipendenze test!** Tutto built-in con node:test.

---

## 9. PATTERN ASSERTION

### assert/strict - Metodi Utili

```javascript
import assert from 'node:assert/strict';

// Uguaglianza
assert.equal(actual, expected);
assert.deepEqual(obj1, obj2); // Deep comparison

// Boolean
assert.ok(value);
assert.ok(!value); // Falsy

// Errori
assert.throws(() => { throw new Error('test'); });
await assert.rejects(async () => { throw new Error('test'); });

// Stringhe
assert.match(text, /pattern/);
assert.ok(text.includes('substring'));

// Array
assert.equal(arr.length, 3);
assert.ok(arr.includes(item));

// Mock verification
assert.equal(mockFn.mock.calls.length, 2);
assert.deepEqual(mockFn.mock.calls[0].arguments, ['arg1', 'arg2']);
```

---

## 10. ESEMPIO COMPLETO - Test Realistico

### test/commands/task.test.js

```javascript
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { render } from '@inquirer/testing';
import { createTempDir } from '../helpers/temp-dir.js';
import { setupSpawnMock } from '../helpers/mock-spawn.js';

test('task command - end to end', async (t) => {
  // Setup
  const tempDir = await createTempDir(t);
  const mockSpawn = setupSpawnMock(t, {
    stdout: 'Agent completed task\n',
    exitCode: 0
  });

  // Mock task prompt
  const taskPrompt = async () => {
    const { input, select } = await import('@inquirer/prompts');

    const description = await input({
      message: 'Task description:',
      validate: (v) => v.length > 0 || 'Required'
    });

    const agent = await select({
      message: 'Which agent?',
      choices: [
        { name: 'Backend', value: 'backend' },
        { name: 'Frontend', value: 'frontend' }
      ]
    });

    return { description, agent };
  };

  // Test prompt interaction
  const { answer, events } = await render(taskPrompt);

  events.type('Add authentication');
  events.keypress('enter');
  events.keypress('down'); // Select Frontend
  events.keypress('enter');

  const taskConfig = await answer;
  assert.equal(taskConfig.description, 'Add authentication');
  assert.equal(taskConfig.agent, 'frontend');

  // Import spawn DOPO mock setup
  const { spawn } = await import('node:child_process');

  // Spawn agent
  const proc = spawn('cervellaswarm', [
    'task',
    '--agent', taskConfig.agent,
    '--description', taskConfig.description
  ]);

  let output = '';
  proc.stdout.on('data', (d) => output += d);

  await new Promise(resolve => proc.on('close', resolve));

  // Assertions
  assert.equal(mockSpawn.mock.calls.length, 1);
  const spawnArgs = mockSpawn.mock.calls[0].arguments;
  assert.ok(spawnArgs[1].includes('frontend'));
  assert.ok(spawnArgs[1].includes('Add authentication'));
  assert.ok(output.includes('completed task'));
});
```

---

## CONCLUSIONI

### ✅ Pro Node:test + @inquirer/testing

```
✅ ZERO dipendenze extra (oltre @inquirer/testing)
✅ Built-in Node.js (niente Jest/Vitest config)
✅ Veloce (no compilation, no transpilation)
✅ Mock potenti con mock.fn() e mock.module()
✅ ESM nativo (type: "module")
✅ Pattern moderno 2026
```

### 📦 Cosa Installare

```bash
npm install --save-dev @inquirer/testing
```

**STOP. Nient'altro serve!**

### 🎯 Raccomandazione

```
PROCEDI CON:
- node:test (built-in)
- @inquirer/testing (ufficiale Inquirer)
- Helper riutilizzabili (mock-spawn, temp-dir)

EVITA:
- Jest (overhead, config complessa)
- Mocha (vecchio stile)
- Sinon (non serve con node:test)

SCORE: 9/10 - Pattern perfetto per CLI moderno!
```

---

## Fonti

- [Node.js Test Runner Official Docs](https://nodejs.org/api/test.html)
- [Node.js Mocking Guide](https://nodejs.org/en/learn/test-runner/mocking)
- [@inquirer/testing Package](https://www.npmjs.com/package/@inquirer/testing)
- [Inquirer.js GitHub Testing](https://github.com/SBoudrias/Inquirer.js/tree/main/packages/testing)
- [Spies and Mocking with Node Test Runner](https://sevic.dev/notes/spies-mocking-node-test-runner/)
- [Better Stack: Node.js Test Runner Guide](https://betterstack.com/community/guides/testing/nodejs-test-runner/)
- [Medium: Testing CLI User Input](https://medium.com/@zorrodg/integration-tests-on-node-js-cli-part-2-testing-interaction-user-input-6f345d4b713a)

---

**COSTITUZIONE-APPLIED:** SI
**Principio usato:** "Studiare chi ha già risolto" - Analizzato docs ufficiali Node.js + Inquirer prima di proporre soluzione.

**Next:** Implementare struttura test/ con pattern documentati.
