import type { Famiglia, Worker, WorkerStatus } from '../types';

interface FamigliaWidgetProps { famiglia?: Famiglia; loading?: boolean; }

const mockWorkers: Worker[] = [
  { id: 'regina', nome: 'cervella-orchestrator', emoji: '👑', descrizione: 'La Regina', model: 'opus', status: 'idle' },
  { id: 'g1', nome: 'cervella-guardiana-qualita', emoji: '🛡️', descrizione: 'Qualita', model: 'opus', status: 'idle' },
  { id: 'g2', nome: 'cervella-guardiana-ops', emoji: '🛡️', descrizione: 'Ops', model: 'opus', status: 'idle' },
  { id: 'g3', nome: 'cervella-guardiana-ricerca', emoji: '🛡️', descrizione: 'Ricerca', model: 'opus', status: 'idle' },
  { id: 'fe', nome: 'cervella-frontend', emoji: '🎨', descrizione: 'UI/UX', model: 'sonnet', status: 'working', taskCorrente: 'Design V2' },
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

const mockFamiglia: Famiglia = {
  regina: mockWorkers[0],
  guardiane: mockWorkers.slice(1, 4),
  workers: mockWorkers.slice(4),
  attiviCount: 1,
  idleCount: 15,
};

function getStatusClasses(status: WorkerStatus): string {
  switch (status) {
    case 'working': return 'status-working';
    case 'done': return 'status-success';
    default: return 'status-idle';
  }
}

function WorkerCard({ worker, compact = false }: { worker: Worker; compact?: boolean }) {
  const isW = worker.status === 'working';
  return (
    <div className={`glass-card p-3 cursor-pointer hover-lift ${isW ? 'border-accent/40' : ''}`}
         title={worker.nome}>
      <div className="flex items-center gap-3">
        <div className={`w-9 h-9 rounded-lg flex items-center justify-center text-lg ${isW ? 'bg-accent/20' : 'bg-bg-tertiary'}`}>
          {worker.emoji}
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2">
            <span className={`text-xs font-medium truncate ${isW ? 'text-accent' : 'text-text-primary'}`}>
              {compact ? worker.id.toUpperCase() : worker.nome.replace('cervella-', '')}
            </span>
            <span className={`status-dot ${getStatusClasses(worker.status)}`} />
          </div>
        </div>
      </div>
    </div>
  );
}

export function FamigliaWidget({ famiglia = mockFamiglia, loading = false }: FamigliaWidgetProps) {
  if (loading) {
    return <div className="glass-card p-8 animate-pulse"><div className="h-48 bg-bg-tertiary rounded-lg"></div></div>;
  }

  return (
    <div className="glass-card p-8">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-accent to-accent-light flex items-center justify-center">🐝</div>
          <span className="text-sm font-semibold tracking-wider uppercase text-text-secondary">La Famiglia</span>
        </div>
        <div className="flex items-center gap-4">
          <span className="text-xs text-accent">{famiglia.attiviCount} attivi</span>
          <span className="text-xs text-text-muted">{famiglia.idleCount} idle</span>
        </div>
      </div>
      <div className="mb-5">
        <div className="text-xs text-text-muted uppercase mb-2">Regina</div>
        <WorkerCard worker={famiglia.regina} />
      </div>
      <div className="mb-5">
        <div className="text-xs text-text-muted uppercase mb-2">Guardiane</div>
        <div className="grid grid-cols-3 gap-2">
          {famiglia.guardiane.map((g) => <WorkerCard key={g.id} worker={g} compact />)}
        </div>
      </div>
      <div>
        <div className="text-xs text-text-muted uppercase mb-2">Worker</div>
        <div className="grid grid-cols-4 gap-2">
          {famiglia.workers.map((w) => <WorkerCard key={w.id} worker={w} compact />)}
        </div>
      </div>
    </div>
  );
}
