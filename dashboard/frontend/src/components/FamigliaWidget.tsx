import type { Famiglia, Worker, WorkerStatus } from '../types';

interface FamigliaWidgetProps {
  famiglia?: Famiglia;
  loading?: boolean;
}

// Dati mock per sviluppo - I 16 membri della famiglia
const mockWorkers: Worker[] = [
  // Regina
  { id: 'regina', nome: 'cervella-orchestrator', emoji: '\u{1F451}', descrizione: 'La Regina - Coordina tutto', model: 'opus', status: 'idle' },
  // Guardiane (3)
  { id: 'g1', nome: 'cervella-guardiana-qualita', emoji: '\u{1F6E1}', descrizione: 'Verifica output agenti', model: 'opus', status: 'idle' },
  { id: 'g2', nome: 'cervella-guardiana-ops', emoji: '\u{1F6E1}', descrizione: 'Supervisiona devops/security', model: 'opus', status: 'idle' },
  { id: 'g3', nome: 'cervella-guardiana-ricerca', emoji: '\u{1F6E1}', descrizione: 'Verifica qualita ricerche', model: 'opus', status: 'idle' },
  // Worker (12)
  { id: 'fe', nome: 'cervella-frontend', emoji: '\u{1F3A8}', descrizione: 'React, CSS, UI/UX', model: 'sonnet', status: 'working', taskCorrente: 'Dashboard Frontend Base' },
  { id: 'be', nome: 'cervella-backend', emoji: '\u{2699}', descrizione: 'Python, FastAPI, API', model: 'sonnet', status: 'working', taskCorrente: 'Dashboard Backend Base' },
  { id: 'ts', nome: 'cervella-tester', emoji: '\u{1F9EA}', descrizione: 'Testing, Debug, QA', model: 'sonnet', status: 'idle' },
  { id: 'rv', nome: 'cervella-reviewer', emoji: '\u{1F4CB}', descrizione: 'Code review', model: 'sonnet', status: 'idle' },
  { id: 'rs', nome: 'cervella-researcher', emoji: '\u{1F52C}', descrizione: 'Ricerca TECNICA', model: 'sonnet', status: 'idle' },
  { id: 'sc', nome: 'cervella-scienziata', emoji: '\u{1F52C}', descrizione: 'Ricerca STRATEGICA', model: 'sonnet', status: 'idle' },
  { id: 'ig', nome: 'cervella-ingegnera', emoji: '\u{1F477}', descrizione: 'Analisi codebase', model: 'sonnet', status: 'idle' },
  { id: 'mk', nome: 'cervella-marketing', emoji: '\u{1F4C8}', descrizione: 'Marketing, UX strategy', model: 'sonnet', status: 'idle' },
  { id: 'dv', nome: 'cervella-devops', emoji: '\u{1F680}', descrizione: 'Deploy, CI/CD, Docker', model: 'sonnet', status: 'idle' },
  { id: 'dc', nome: 'cervella-docs', emoji: '\u{1F4DD}', descrizione: 'Documentazione', model: 'sonnet', status: 'idle' },
  { id: 'dt', nome: 'cervella-data', emoji: '\u{1F4CA}', descrizione: 'SQL, analytics', model: 'sonnet', status: 'idle' },
  { id: 'sy', nome: 'cervella-security', emoji: '\u{1F512}', descrizione: 'Audit sicurezza', model: 'sonnet', status: 'idle' },
];

const mockFamiglia: Famiglia = {
  regina: mockWorkers[0],
  guardiane: mockWorkers.slice(1, 4),
  workers: mockWorkers.slice(4),
  attiviCount: 2,
  idleCount: 14,
};

function getStatusColor(status: WorkerStatus): string {
  switch (status) {
    case 'working':
      return 'bg-green-500';
    case 'done':
      return 'bg-blue-500';
    case 'error':
      return 'bg-red-500';
    default:
      return 'bg-slate-600';
  }
}

function getStatusBorder(status: WorkerStatus): string {
  switch (status) {
    case 'working':
      return 'border-green-500/50 ring-2 ring-green-500/20';
    case 'done':
      return 'border-blue-500/50';
    case 'error':
      return 'border-red-500/50';
    default:
      return 'border-slate-700';
  }
}

interface WorkerCardProps {
  worker: Worker;
  compact?: boolean;
}

function WorkerCard({ worker, compact = false }: WorkerCardProps) {
  const isWorking = worker.status === 'working';

  return (
    <div
      className={`
        bg-slate-800/50 rounded-lg p-3 border transition-all cursor-pointer
        hover:bg-slate-700/50 hover:border-slate-600
        ${getStatusBorder(worker.status)}
        ${isWorking ? 'animate-pulse' : ''}
      `}
      title={`${worker.nome}\n${worker.descrizione}\nModel: ${worker.model}${worker.taskCorrente ? `\nTask: ${worker.taskCorrente}` : ''}`}
    >
      <div className="flex items-center gap-2">
        <span className="text-xl">{worker.emoji}</span>
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2">
            <span className={`text-xs font-medium truncate ${compact ? 'max-w-16' : ''}`}>
              {compact ? worker.id.toUpperCase() : worker.nome.replace('cervella-', '')}
            </span>
            <span className={`w-2 h-2 rounded-full ${getStatusColor(worker.status)}`} />
          </div>
          {!compact && worker.taskCorrente && (
            <p className="text-xs text-slate-400 truncate mt-1">
              {worker.taskCorrente}
            </p>
          )}
        </div>
      </div>
    </div>
  );
}

export function FamigliaWidget({ famiglia = mockFamiglia, loading = false }: FamigliaWidgetProps) {
  if (loading) {
    return (
      <div className="bg-slate-800 rounded-lg p-6 border border-slate-700 animate-pulse">
        <div className="h-6 bg-slate-700 rounded w-32 mb-4"></div>
        <div className="grid grid-cols-4 gap-3">
          {[...Array(16)].map((_, i) => (
            <div key={i} className="h-16 bg-slate-700 rounded"></div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <span className="text-2xl">&#x1F41D;</span>
          <h2 className="text-lg font-semibold text-white">LA FAMIGLIA</h2>
        </div>
        <div className="flex items-center gap-3 text-sm">
          <span className="flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-green-500"></span>
            <span className="text-green-400">{famiglia.attiviCount} attivi</span>
          </span>
          <span className="text-slate-500">|</span>
          <span className="flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-slate-600"></span>
            <span className="text-slate-400">{famiglia.idleCount} idle</span>
          </span>
        </div>
      </div>

      {/* Regina */}
      <div className="mb-4">
        <div className="text-xs text-slate-500 uppercase tracking-wide mb-2">Regina</div>
        <WorkerCard worker={famiglia.regina} />
      </div>

      {/* Guardiane */}
      <div className="mb-4">
        <div className="text-xs text-slate-500 uppercase tracking-wide mb-2">
          Guardiane (Opus)
        </div>
        <div className="grid grid-cols-3 gap-2">
          {famiglia.guardiane.map((g) => (
            <WorkerCard key={g.id} worker={g} compact />
          ))}
        </div>
      </div>

      {/* Worker */}
      <div>
        <div className="text-xs text-slate-500 uppercase tracking-wide mb-2">
          Worker (Sonnet)
        </div>
        <div className="grid grid-cols-4 gap-2">
          {famiglia.workers.map((w) => (
            <WorkerCard key={w.id} worker={w} compact />
          ))}
        </div>
      </div>
    </div>
  );
}
