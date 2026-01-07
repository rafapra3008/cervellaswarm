import { useState, useEffect, useCallback } from 'react';

interface UseApiOptions {
  autoFetch?: boolean;
  refreshInterval?: number; // in milliseconds
}

interface UseApiResult<T> {
  data: T | null;
  loading: boolean;
  error: Error | null;
  refetch: () => Promise<void>;
}

const API_BASE = '/api';

export function useApi<T>(
  endpoint: string,
  options: UseApiOptions = {}
): UseApiResult<T> {
  const { autoFetch = true, refreshInterval } = options;

  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(autoFetch);
  const [error, setError] = useState<Error | null>(null);

  const fetchData = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      const response = await fetch(`${API_BASE}${endpoint}`);

      if (!response.ok) {
        throw new Error(`API Error: ${response.status} ${response.statusText}`);
      }

      const result = await response.json();
      setData(result);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Unknown error'));
    } finally {
      setLoading(false);
    }
  }, [endpoint]);

  // Auto-fetch on mount
  useEffect(() => {
    if (autoFetch) {
      fetchData();
    }
  }, [autoFetch, fetchData]);

  // Optional refresh interval
  useEffect(() => {
    if (!refreshInterval) return;

    const interval = setInterval(fetchData, refreshInterval);
    return () => clearInterval(interval);
  }, [refreshInterval, fetchData]);

  return { data, loading, error, refetch: fetchData };
}

// Specialized hooks for each data type
export function useNord() {
  return useApi<{
    obiettivo: string;
    descrizione: string;
    progressoGenerale: number;
    sessioneCorrente: number;
    frase?: string;
  }>('/nord');
}

export function useFamiglia() {
  return useApi<{
    regina: unknown;
    guardiane: unknown[];
    workers: unknown[];
    attiviCount: number;
    idleCount: number;
  }>('/famiglia', { refreshInterval: 5000 }); // Refresh every 5s
}

export function useRoadmap() {
  return useApi<{
    steps: unknown[];
    stepCorrente: number;
    progressoTotale: number;
  }>('/roadmap');
}

export function useSessione() {
  return useApi<{
    taskId?: string;
    taskNome?: string;
    workerAssegnato?: string;
    inizioTimestamp?: string;
    durataSecondi: number;
    outputFile?: string;
    logs: unknown[];
    isActive: boolean;
  }>('/sessione', { refreshInterval: 2000 }); // Refresh every 2s
}

export function useDashboard() {
  return useApi<{
    nord: unknown;
    famiglia: unknown;
    roadmap: unknown;
    sessione: unknown;
    lastUpdate: string;
  }>('/dashboard');
}
