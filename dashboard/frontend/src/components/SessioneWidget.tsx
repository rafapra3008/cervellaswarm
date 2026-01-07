import { useEffect, useState } from 'react';
import type { SessioneAttiva, LogMessage } from '../types';

interface SessioneWidgetProps {
  sessione?: SessioneAttiva;
  loading?: boolean;
}

// Dati mock per sviluppo
const mockLogs: LogMessage[] = [
  { timestamp: '01:15:23', message: 'Task avviato: Dashboard Frontend Base', type: 'info' },
  { timestamp: '01:15:24', message: 'Leggendo studi di riferimento...', type: 'info' },
  { timestamp: '01:16:05', message: 'Studio UX completato', type: 'success' },
  { timestamp: '01:16:10', message: 'Studio TECH completato', type: 'success' },
  { timestamp: '01:16:30', message: 'Creando progetto Vite + React...', type: 'info' },
  { timestamp: '01:17:15', message: 'Configurando Tailwind CSS...', type: 'info' },
  { timestamp: '01:18:00', message: 'Creando componenti...', type: 'info' },
];

const mockSessione: SessioneAttiva = {
  taskId: 'TASK_DASHBOARD_FRONTEND',
  taskNome: 'Dashboard Frontend Base',
  workerAssegnato: 'cervella-frontend',
  inizioTimestamp: '2026-01-07T01:15:23',
  durataSecondi: 180,
  outputFile: 'dashboard/frontend/',
  logs: mockLogs,
  isActive: true,
};

function formatDuration(seconds: number): string {
  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return `${mins}m ${secs.toString().padStart(2, '0')}s`;
}

function getLogTypeColor(type: LogMessage['type']): string {
  switch (type) {
    case 'success':
      return 'text-green-400';
    case 'warning':
      return 'text-amber-400';
    case 'error':
      return 'text-red-400';
    default:
      return 'text-slate-400';
  }
}

function getLogTypeIcon(type: LogMessage['type']): string {
  switch (type) {
    case 'success':
      return '\u2713';
    case 'warning':
      return '\u26A0';
    case 'error':
      return '\u2717';
    default:
      return '\u25B6';
  }
}

export function SessioneWidget({ sessione = mockSessione, loading = false }: SessioneWidgetProps) {
  const [duration, setDuration] = useState(sessione.durataSecondi);

  // Timer per durata
  useEffect(() => {
    if (!sessione.isActive) return;

    const interval = setInterval(() => {
      setDuration((prev) => prev + 1);
    }, 1000);

    return () => clearInterval(interval);
  }, [sessione.isActive]);

  if (loading) {
    return (
      <div className="bg-slate-800 rounded-lg p-6 border border-slate-700 animate-pulse">
        <div className="h-6 bg-slate-700 rounded w-40 mb-4"></div>
        <div className="space-y-3">
          <div className="h-4 bg-slate-700 rounded w-3/4"></div>
          <div className="h-4 bg-slate-700 rounded w-1/2"></div>
          <div className="h-24 bg-slate-700 rounded"></div>
        </div>
      </div>
    );
  }

  if (!sessione.isActive) {
    return (
      <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
        <div className="flex items-center gap-2 mb-4">
          <span className="text-2xl">&#x1F4BB;</span>
          <h2 className="text-lg font-semibold text-white">SESSIONE ATTIVA</h2>
        </div>
        <div className="text-center py-8">
          <span className="text-4xl mb-3 block">&#x1F634;</span>
          <p className="text-slate-400">Nessun task in esecuzione</p>
          <p className="text-sm text-slate-500 mt-1">Lo sciame e' in attesa di istruzioni</p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-slate-800 rounded-lg p-6 border border-green-500/30">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <span className="text-2xl animate-pulse">&#x1F41D;</span>
          <h2 className="text-lg font-semibold text-white">SESSIONE ATTIVA</h2>
        </div>
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
          <span className="text-green-400 text-sm">In esecuzione</span>
        </div>
      </div>

      {/* Task info */}
      <div className="bg-slate-900/50 rounded-lg p-4 mb-4 border border-slate-700">
        <div className="grid grid-cols-2 gap-4">
          <div>
            <span className="text-xs text-slate-500 uppercase">Task</span>
            <p className="text-white font-medium">{sessione.taskNome}</p>
          </div>
          <div>
            <span className="text-xs text-slate-500 uppercase">Worker</span>
            <p className="text-amber-400 font-medium">{sessione.workerAssegnato}</p>
          </div>
          <div>
            <span className="text-xs text-slate-500 uppercase">Durata</span>
            <p className="text-white font-mono text-lg">{formatDuration(duration)}</p>
          </div>
          <div>
            <span className="text-xs text-slate-500 uppercase">Output</span>
            <p className="text-slate-400 text-sm truncate">{sessione.outputFile}</p>
          </div>
        </div>
      </div>

      {/* Logs */}
      <div>
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs text-slate-500 uppercase">Log</span>
          <button className="text-xs text-slate-400 hover:text-white">Vedi completo</button>
        </div>
        <div className="bg-slate-900 rounded-lg p-3 max-h-40 overflow-y-auto font-mono text-xs">
          {sessione.logs.slice(-7).map((log, i) => (
            <div key={i} className="flex gap-2 py-0.5">
              <span className="text-slate-600">{log.timestamp}</span>
              <span className={getLogTypeColor(log.type)}>{getLogTypeIcon(log.type)}</span>
              <span className={getLogTypeColor(log.type)}>{log.message}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Actions */}
      <div className="mt-4 flex gap-3">
        <button className="flex-1 px-4 py-2 bg-slate-700 hover:bg-slate-600 rounded-lg text-sm text-white transition-colors">
          Vedi Log Completo
        </button>
        <button className="px-4 py-2 bg-red-500/20 hover:bg-red-500/30 border border-red-500/30 rounded-lg text-sm text-red-400 transition-colors">
          Ferma
        </button>
      </div>
    </div>
  );
}
