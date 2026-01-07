import { useEffect, useRef, useState, useCallback } from 'react';
import type { SSEEvent, SSEEventType } from '../types';

interface UseSSEOptions {
  reconnectInterval?: number; // in milliseconds
  maxRetries?: number;
  onOpen?: () => void;
  onError?: (error: Event) => void;
}

interface UseSSEResult {
  isConnected: boolean;
  lastEvent: SSEEvent | null;
  error: Event | null;
  reconnect: () => void;
}

const SSE_URL = '/api/events';

export function useSSE(
  onEvent: (event: SSEEvent) => void,
  options: UseSSEOptions = {}
): UseSSEResult {
  const {
    reconnectInterval = 3000,
    maxRetries = 10,
    onOpen,
    onError,
  } = options;

  const [isConnected, setIsConnected] = useState(false);
  const [lastEvent, setLastEvent] = useState<SSEEvent | null>(null);
  const [error, setError] = useState<Event | null>(null);

  const eventSourceRef = useRef<EventSource | null>(null);
  const retriesRef = useRef(0);
  const reconnectTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const connect = useCallback(() => {
    // Clean up existing connection
    if (eventSourceRef.current) {
      eventSourceRef.current.close();
    }

    try {
      const eventSource = new EventSource(SSE_URL);
      eventSourceRef.current = eventSource;

      eventSource.onopen = () => {
        setIsConnected(true);
        setError(null);
        retriesRef.current = 0;
        onOpen?.();
      };

      eventSource.onmessage = (event) => {
        try {
          const data: SSEEvent = JSON.parse(event.data);
          setLastEvent(data);
          onEvent(data);
        } catch (e) {
          console.error('Failed to parse SSE event:', e);
        }
      };

      eventSource.onerror = (err) => {
        setIsConnected(false);
        setError(err);
        onError?.(err);

        // Attempt reconnection
        if (retriesRef.current < maxRetries) {
          retriesRef.current += 1;
          reconnectTimeoutRef.current = setTimeout(() => {
            connect();
          }, reconnectInterval);
        }
      };
    } catch (err) {
      console.error('Failed to create EventSource:', err);
    }
  }, [onEvent, onOpen, onError, reconnectInterval, maxRetries]);

  const reconnect = useCallback(() => {
    retriesRef.current = 0;
    connect();
  }, [connect]);

  // Connect on mount
  useEffect(() => {
    connect();

    return () => {
      if (eventSourceRef.current) {
        eventSourceRef.current.close();
      }
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
    };
  }, [connect]);

  return { isConnected, lastEvent, error, reconnect };
}

// Hook per gestire gli update della dashboard via SSE
export function useDashboardSSE(
  onUpdate: (type: SSEEventType, data: Partial<SSEEvent['data']>) => void
) {
  const handleEvent = useCallback(
    (event: SSEEvent) => {
      onUpdate(event.type, event.data);
    },
    [onUpdate]
  );

  return useSSE(handleEvent, {
    onOpen: () => console.log('SSE connected'),
    onError: () => console.log('SSE disconnected, retrying...'),
  });
}
