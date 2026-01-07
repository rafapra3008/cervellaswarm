import { useState, useEffect, useCallback } from 'react';
import type { Nord, Famiglia, Roadmap, SessioneAttiva, Worker, Step } from '../types';

// API response from /api/mappa
interface MappaApiResponse {
  version: string;
  updated_at: string;
  project: {
    name: string;
    claim: string;
    objective: string;
  };
  nord: {
    source_file: string;
    current_session: {
      number: number;
      date: string;
      title: string;
    };
    stato_reale: Array<{ cosa: string; status: string }>;
    pezzi: string[];
  };
  roadmap: {
    source_file: string;
    current_phase: {
      number: number;
      name: string;
      status: string;
    };
    completed_phases: Array<{ number: number; name: string }>;
  };
}

// Transform API response to dashboard types
function transformNord(apiNord: MappaApiResponse['nord'], project: MappaApiResponse['project']): Nord {
  const completedItems = apiNord.stato_reale.filter(s => s.status === 'FUNZIONANTE').length;
  const totalItems = apiNord.stato_reale.length || 1;
  const progresso = Math.round((completedItems / totalItems) * 100);

  return {
    obiettivo: project.objective,
    descrizione: project.claim,
    progressoGenerale: progresso,
    sessioneCorrente: apiNord.current_session.number,
    frase: apiNord.pezzi[0] || undefined,
  };
}

function transformFamiglia(): Famiglia {
  // Static famiglia data - workers status will be updated via SSE/polling
  const allWorkers: Worker[] = [
    { id: 'regina', nome: 'cervella-orchestrator', emoji: '👑', descrizione: 'La Regina', model: 'opus', status: 'idle' },
    { id: 'g1', nome: 'cervella-guardiana-qualita', emoji: '🛡️', descrizione: 'Qualita', model: 'opus', status: 'idle' },
    { id: 'g2', nome: 'cervella-guardiana-ops', emoji: '🛡️', descrizione: 'Ops', model: 'opus', status: 'idle' },
    { id: 'g3', nome: 'cervella-guardiana-ricerca', emoji: '🛡️', descrizione: 'Ricerca', model: 'opus', status: 'idle' },
    { id: 'fe', nome: 'cervella-frontend', emoji: '🎨', descrizione: 'UI/UX', model: 'sonnet', status: 'idle' },
    { id: 'be', nome: 'cervella-backend', emoji: '⚙️', descrizione: 'API', model: 'sonnet', status: 'idle' },
    { id: 'ts', nome: 'cervella-tester', emoji: '🧪', descrizione: 'QA', model: 'sonnet', status: 'idle' },
    { id: 'rv', nome: 'cervella-reviewer', emoji: '📋', descrizione: 'Review', model: 'sonnet', status: 'idle' },
    { id: 'rs', nome: 'cervella-researcher', emoji: '🔬', descrizione: 'Ricerca', model: 'sonnet', status: 'idle' },
    { id: 'sc', nome: 'cervella-scienziata', emoji: '🔬', descrizione: 'Strategia', model: 'sonnet', status: 'idle' },
    { id: 'ig', nome: 'cervella-ingegnera', emoji: '👷', descrizione: 'Analisi', model: 'sonnet', status: 'idle' },
    { id: 'mk', nome: 'cervella-marketing', emoji: '📈', descrizione: 'Marketing', model: 'sonnet', status: 'idle' },
    { id: 'dv', nome: 'cervella-devops', emoji: '🚀', descrizione: 'DevOps', model: 'sonnet', status: 'idle' },
    { id: 'dc', nome: 'cervella-docs', emoji: '📝', descrizione: 'Docs', model: 'sonnet', status: 'idle' },
    { id: 'dt', nome: 'cervella-data', emoji: '📊', descrizione: 'Data', model: 'sonnet', status: 'idle' },
    { id: 'sy', nome: 'cervella-security', emoji: '🔒', descrizione: 'Security', model: 'sonnet', status: 'idle' },
  ];

  return {
    regina: allWorkers[0],
    guardiane: allWorkers.slice(1, 4),
    workers: allWorkers.slice(4),
    attiviCount: 0,
    idleCount: 16,
  };
}

function transformRoadmap(apiRoadmap: MappaApiResponse['roadmap']): Roadmap {
  const steps: Step[] = [];

  // Add completed phases
  apiRoadmap.completed_phases.forEach((phase) => {
    steps.push({
      id: `step-${phase.number}`,
      numero: phase.number,
      titolo: phase.name.length > 20 ? phase.name.substring(0, 20) + '...' : phase.name,
      descrizione: phase.name,
      status: 'completed',
      progresso: 100,
      subSteps: [],
    });
  });

  // Add current phase
  steps.push({
    id: `step-${apiRoadmap.current_phase.number}`,
    numero: apiRoadmap.current_phase.number,
    titolo: apiRoadmap.current_phase.name.length > 20
      ? apiRoadmap.current_phase.name.substring(0, 20) + '...'
      : apiRoadmap.current_phase.name,
    descrizione: apiRoadmap.current_phase.name,
    status: 'in_progress',
    progresso: 50,
    subSteps: [],
  });

  const progressoTotale = Math.round((apiRoadmap.completed_phases.length / (apiRoadmap.completed_phases.length + 1)) * 100);

  return {
    steps: steps.slice(-4), // Show last 4 steps to fit UI
    stepCorrente: apiRoadmap.current_phase.number,
    progressoTotale,
  };
}

function transformSessione(): SessioneAttiva {
  // Will be updated via polling or SSE
  return {
    durataSecondi: 0,
    logs: [],
    isActive: false,
  };
}

export interface DashboardState {
  nord: Nord | null;
  famiglia: Famiglia | null;
  roadmap: Roadmap | null;
  sessione: SessioneAttiva | null;
  loading: boolean;
  error: Error | null;
  lastUpdate: string | null;
}

export function useDashboardData(refreshInterval = 30000) {
  const [state, setState] = useState<DashboardState>({
    nord: null,
    famiglia: null,
    roadmap: null,
    sessione: null,
    loading: true,
    error: null,
    lastUpdate: null,
  });

  const fetchData = useCallback(async () => {
    try {
      setState(prev => ({ ...prev, loading: prev.nord === null, error: null }));

      const response = await fetch('http://localhost:8100/api/mappa');

      if (!response.ok) {
        throw new Error(`API Error: ${response.status} ${response.statusText}`);
      }

      const data: MappaApiResponse = await response.json();

      setState({
        nord: transformNord(data.nord, data.project),
        famiglia: transformFamiglia(),
        roadmap: transformRoadmap(data.roadmap),
        sessione: transformSessione(),
        loading: false,
        error: null,
        lastUpdate: data.updated_at,
      });
    } catch (err) {
      setState(prev => ({
        ...prev,
        loading: false,
        error: err instanceof Error ? err : new Error('Unknown error'),
      }));
    }
  }, []);

  // Initial fetch
  useEffect(() => {
    fetchData();
  }, [fetchData]);

  // Refresh interval
  useEffect(() => {
    if (!refreshInterval) return;

    const interval = setInterval(fetchData, refreshInterval);
    return () => clearInterval(interval);
  }, [refreshInterval, fetchData]);

  return {
    ...state,
    refetch: fetchData,
  };
}
