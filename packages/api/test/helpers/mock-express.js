/**
 * Mock Express Request/Response
 *
 * Helper per creare mock req/res nei test Express.
 *
 * "I dettagli fanno SEMPRE la differenza."
 */

/**
 * Crea mock Express Request
 *
 * @param {object} options - Request options
 * @returns {object} - Mock request
 */
export function createMockRequest(options = {}) {
  return {
    body: options.body || {},
    headers: options.headers || {},
    params: options.params || {},
    query: options.query || {},
    method: options.method || 'GET',
    url: options.url || '/',
    ...options
  };
}

/**
 * Crea mock Express Response
 *
 * @returns {object} - Mock response
 */
export function createMockResponse() {
  const response = {
    statusCode: 200,
    headers: {},
    body: null,

    status(code) {
      response.statusCode = code;
      return response;
    },

    json(data) {
      response.body = data;
      return response;
    },

    send(data) {
      response.body = data;
      return response;
    },

    set(key, value) {
      response.headers[key] = value;
      return response;
    },

    // Helper per assertions
    getStatus() {
      return response.statusCode;
    },

    getBody() {
      return response.body;
    },

    getHeader(key) {
      return response.headers[key];
    }
  };

  return response;
}

/**
 * Simula Express middleware chain
 *
 * @param {Function} handler - Route handler
 * @param {object} req - Mock request
 * @param {object} res - Mock response
 * @returns {Promise<object>} - Response
 */
export async function executeHandler(handler, req, res) {
  await handler(req, res);
  return res;
}
