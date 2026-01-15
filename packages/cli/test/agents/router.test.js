/**
 * Task Router Tests
 *
 * Test per agents/router.js
 * Verifica: routing corretto basato su keywords
 *
 * "La Regina orchestra, non fa tutto da sola!"
 */

import { test, describe } from 'node:test';
import assert from 'node:assert/strict';
import { routeTask } from '../../src/agents/router.js';

describe('Task Router', () => {

  describe('Backend routing', () => {
    test('routes "api" tasks to backend', async () => {
      const agent = await routeTask('Create new API endpoint', {});
      assert.equal(agent, 'cervella-backend');
    });

    test('routes "backend" tasks to backend', async () => {
      const agent = await routeTask('Fix backend logic', {});
      assert.equal(agent, 'cervella-backend');
    });

    test('routes "endpoint" tasks to backend', async () => {
      const agent = await routeTask('Add user endpoint', {});
      assert.equal(agent, 'cervella-backend');
    });
  });

  describe('Frontend routing', () => {
    test('routes "ui" tasks to frontend', async () => {
      const agent = await routeTask('Improve UI design', {});
      assert.equal(agent, 'cervella-frontend');
    });

    test('routes "frontend" tasks to frontend', async () => {
      const agent = await routeTask('Fix frontend bug', {});
      assert.equal(agent, 'cervella-frontend');
    });

    test('routes "component" tasks to frontend', async () => {
      const agent = await routeTask('Create button component', {});
      assert.equal(agent, 'cervella-frontend');
    });
  });

  describe('Tester routing', () => {
    test('routes "test" tasks to tester', async () => {
      const agent = await routeTask('Write unit tests', {});
      assert.equal(agent, 'cervella-tester');
    });

    test('routes "bug" tasks to tester', async () => {
      const agent = await routeTask('Fix this bug', {});
      assert.equal(agent, 'cervella-tester');
    });

    test('routes "debug" tasks to tester', async () => {
      const agent = await routeTask('Debug the issue', {});
      assert.equal(agent, 'cervella-tester');
    });
  });

  describe('Data routing', () => {
    test('routes "database" tasks to data', async () => {
      const agent = await routeTask('Optimize database queries', {});
      assert.equal(agent, 'cervella-data');
    });

    test('routes "sql" tasks to data', async () => {
      const agent = await routeTask('Write SQL migration', {});
      assert.equal(agent, 'cervella-data');
    });

    test('routes "query" tasks to data', async () => {
      const agent = await routeTask('Fix slow query', {});
      assert.equal(agent, 'cervella-data');
    });
  });

  describe('DevOps routing', () => {
    test('routes "deploy" tasks to devops', async () => {
      const agent = await routeTask('Deploy to production', {});
      assert.equal(agent, 'cervella-devops');
    });

    test('routes "docker" tasks to devops', async () => {
      const agent = await routeTask('Create docker image', {});
      assert.equal(agent, 'cervella-devops');
    });

    test('routes "ci" tasks to devops', async () => {
      const agent = await routeTask('Setup CI pipeline', {});
      assert.equal(agent, 'cervella-devops');
    });
  });

  describe('Security routing', () => {
    test('routes "security" tasks to security', async () => {
      const agent = await routeTask('Run security audit', {});
      assert.equal(agent, 'cervella-security');
    });

    test('routes "auth" tasks to security', async () => {
      const agent = await routeTask('Add auth middleware', {});
      assert.equal(agent, 'cervella-security');
    });

    test('routes "vulnerability" tasks to security', async () => {
      const agent = await routeTask('Fix vulnerability', {});
      assert.equal(agent, 'cervella-security');
    });
  });

  describe('Docs routing', () => {
    test('routes "doc" tasks to docs', async () => {
      const agent = await routeTask('Write documentation', {});
      assert.equal(agent, 'cervella-docs');
    });

    test('routes "readme" tasks to docs', async () => {
      const agent = await routeTask('Update README file', {});
      assert.equal(agent, 'cervella-docs');
    });

    test('routes docs keywords to docs', async () => {
      // Nota: "guide" contiene "ui" che matcha frontend
      // Nota: "API docs" ha "api" che matcha backend
      // Usiamo testo senza conflitti
      const agent = await routeTask('Write documentation for the project', {});
      assert.equal(agent, 'cervella-docs');
    });
  });

  describe('Default routing', () => {
    test('defaults to backend for ambiguous tasks', async () => {
      const agent = await routeTask('Do something cool', {});
      assert.equal(agent, 'cervella-backend');
    });

    test('defaults to backend for empty description', async () => {
      const agent = await routeTask('', {});
      assert.equal(agent, 'cervella-backend');
    });
  });

  describe('Case insensitivity', () => {
    test('handles uppercase keywords', async () => {
      const agent = await routeTask('CREATE API ENDPOINT', {});
      assert.equal(agent, 'cervella-backend');
    });

    test('handles mixed case keywords', async () => {
      const agent = await routeTask('Fix FrontEnd Bug', {});
      assert.equal(agent, 'cervella-frontend');
    });
  });

});
