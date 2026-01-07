import type { Roadmap, StepStatus } from '../types';

interface RoadmapWidgetProps { roadmap?: Roadmap; loading?: boolean; }

const mockRoadmap: Roadmap = {
  steps: [
    { id: 'step-0', numero: 0, titolo: 'Setup Base', descrizione: 'Config iniziale', status: 'completed', progresso: 100, subSteps: [] },
    { id: 'step-1', numero: 1, titolo: 'Dashboard MAPPA', descrizione: 'UI visuale', status: 'in_progress', progresso: 60, subSteps: [] },
    { id: 'step-2', numero: 2, titolo: 'VS Code Extension', descrizione: 'IDE integration', status: 'pending', progresso: 0, subSteps: [] },
    { id: 'step-3', numero: 3, titolo: 'Marketplace', descrizione: 'Pubblicazione', status: 'pending', progresso: 0, subSteps: [] },
  ],
  stepCorrente: 1,
  progressoTotale: 40,
};

function getStatusStyles(status: StepStatus) {
  switch (status) {
    case 'completed': return { text: 'text-success', dot: 'status-success' };
    case 'in_progress': return { text: 'text-accent', dot: 'status-working' };
    default: return { text: 'text-text-muted', dot: 'status-idle' };
  }
}

export function RoadmapWidget({ roadmap = mockRoadmap, loading = false }: RoadmapWidgetProps) {
  if (loading) {
    return <div className="glass-card p-8 animate-pulse"><div className="h-32 bg-bg-tertiary rounded-lg"></div></div>;
  }

  return (
    <div className="glass-card p-8">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-accent to-accent-light flex items-center justify-center">🗺️</div>
          <span className="text-sm font-semibold tracking-wider uppercase text-text-secondary">La Roadmap</span>
        </div>
        <div className="flex items-center gap-3">
          <span className="text-sm text-text-muted">Totale:</span>
          <div className="w-24 progress-bar h-1.5">
            <div className="progress-bar-fill" style={{ width: `${roadmap.progressoTotale}%` }} />
          </div>
          <span className="text-sm font-semibold text-accent">{roadmap.progressoTotale}%</span>
        </div>
      </div>

      <div className="flex gap-5 overflow-x-auto pb-4">
        {roadmap.steps.map((step) => {
          const styles = getStatusStyles(step.status);
          const isCurrent = step.numero === roadmap.stepCorrente;
          return (
            <div key={step.id} className={`flex-shrink-0 w-52 glass-card p-5 ${isCurrent ? 'ring-2 ring-accent/30' : ''}`}>
              <div className="flex items-center justify-between mb-3">
                <span className="text-xs text-text-muted uppercase">Step {step.numero}</span>
                <span className={`status-dot ${styles.dot}`} />
              </div>
              <h3 className="font-semibold text-text-primary text-sm mb-1">{step.titolo}</h3>
              <p className="text-xs text-text-muted mb-3">{step.descrizione}</p>
              <div className="flex justify-between text-xs mb-2">
                <span className={styles.text}>{step.status === 'completed' ? 'Completato' : step.status === 'in_progress' ? 'In corso' : 'Da fare'}</span>
                <span className="text-text-secondary">{step.progresso}%</span>
              </div>
              <div className="progress-bar h-1">
                <div className={`h-full rounded-full ${step.status === 'completed' ? 'bg-success' : 'progress-bar-fill'}`} style={{ width: `${step.progresso}%` }} />
              </div>
            </div>
          );
        })}
        <div className="flex-shrink-0 w-36 glass-card p-5 flex flex-col items-center justify-center border-accent/20 animate-glow-pulse">
          <span className="text-4xl mb-3">⭐</span>
          <span className="text-accent font-bold text-sm">NORD</span>
          <span className="text-xs text-text-muted">La foto!</span>
        </div>
      </div>
    </div>
  );
}
