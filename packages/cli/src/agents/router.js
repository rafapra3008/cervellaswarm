/**
 * Task Router
 *
 * Determines which agent should handle a task.
 * Regina's brain for task assignment.
 *
 * Copyright 2026 Rafa & Cervella
 * Licensed under the Apache License, Version 2.0
 * http://www.apache.org/licenses/LICENSE-2.0
 */

export async function routeTask(description, _context) {
  // Simple keyword-based routing for now
  const desc = description.toLowerCase();

  if (desc.includes('api') || desc.includes('backend') || desc.includes('endpoint')) {
    return 'cervella-backend';
  }
  if (desc.includes('ui') || desc.includes('frontend') || desc.includes('component')) {
    return 'cervella-frontend';
  }
  if (desc.includes('test') || desc.includes('bug') || desc.includes('debug')) {
    return 'cervella-tester';
  }
  if (desc.includes('database') || desc.includes('sql') || desc.includes('query')) {
    return 'cervella-data';
  }
  if (desc.includes('deploy') || desc.includes('docker') || desc.includes('ci')) {
    return 'cervella-devops';
  }
  if (desc.includes('security') || desc.includes('auth') || desc.includes('vulnerab')) {
    return 'cervella-security';
  }
  if (desc.includes('doc') || desc.includes('readme') || desc.includes('guide')) {
    return 'cervella-docs';
  }

  // Default to backend for general tasks
  return 'cervella-backend';
}
