import { useState } from 'react';
import type { Roadmap, Step, StepStatus } from '../types';

interface RoadmapWidgetProps {
  roadmap?: Roadmap;
  loading?: boolean;
}

// Dati mock per sviluppo
const mockRoadmap: Roadmap = {
  steps: [
    {
      id: 'step-0',
      numero: 0,
      titolo: 'Setup Base',
      descrizione: 'Configurazione iniziale del progetto',
      status: 'completed',
      progresso: 100,
      subSteps: [
        { id: '0.1', titolo: 'Creare repository', status: 'completed' },
        { id: '0.2', titolo: 'Setup agent families', status: 'completed' },
        { id: '0.3', titolo: 'Documentazione base', status: 'completed' },
      ],
    },
    {
      id: 'step-1',
      numero: 1,
      titolo: 'Dashboard MAPPA',
      descrizione: 'Interfaccia visuale per monitorare lo sciame',
      status: 'in_progress',
      progresso: 35,
      subSteps: [
        { id: '1.1', titolo: 'Studio UX', status: 'completed' },
        { id: '1.2', titolo: 'Studio Tech', status: 'completed' },
        { id: '1.3', titolo: 'Frontend React', status: 'in_progress' },
        { id: '1.4', titolo: 'Backend FastAPI', status: 'in_progress' },
        { id: '1.5', titolo: 'SSE Real-time', status: 'pending' },
      ],
    },
    {
      id: 'step-2',
      numero: 2,
      titolo: 'VS Code Extension',
      descrizione: 'Estensione per integrare lo sciame in VS Code',
      status: 'pending',
      progresso: 0,
      subSteps: [
        { id: '2.1', titolo: 'Setup extension', status: 'pending' },
        { id: '2.2', titolo: 'Sidebar panel', status: 'pending' },
        { id: '2.3', titolo: 'Commands', status: 'pending' },
      ],
    },
    {
      id: 'step-3',
      numero: 3,
      titolo: 'Marketplace',
      descrizione: 'Pubblicazione e distribuzione',
      status: 'pending',
      progresso: 0,
      subSteps: [
        { id: '3.1', titolo: 'Packaging', status: 'pending' },
        { id: '3.2', titolo: 'Documentation', status: 'pending' },
        { id: '3.3', titolo: 'Launch', status: 'pending' },
      ],
    },
  ],
  stepCorrente: 1,
  progressoTotale: 34,
};

function getStatusColor(status: StepStatus): string {
  switch (status) {
    case 'completed':
      return 'bg-green-500';
    case 'in_progress':
      return 'bg-amber-500';
    default:
      return 'bg-slate-600';
  }
}

function getStatusTextColor(status: StepStatus): string {
  switch (status) {
    case 'completed':
      return 'text-green-400';
    case 'in_progress':
      return 'text-amber-400';
    default:
      return 'text-slate-500';
  }
}

interface StepCardProps {
  step: Step;
  isCurrent: boolean;
  onExpand: () => void;
  isExpanded: boolean;
}

function StepCard({ step, isCurrent, onExpand, isExpanded }: StepCardProps) {
  return (
    <div
      className={`
        flex-shrink-0 w-48 rounded-lg border transition-all cursor-pointer
        ${isCurrent ? 'bg-slate-700 border-amber-500/50 ring-2 ring-amber-500/20' : 'bg-slate-800/50 border-slate-700 hover:border-slate-600'}
      `}
      onClick={onExpand}
    >
      {/* Header */}
      <div className="p-4">
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs text-slate-500 uppercase">Step {step.numero}</span>
          <span className={`w-2 h-2 rounded-full ${getStatusColor(step.status)}`} />
        </div>
        <h3 className="font-semibold text-white text-sm mb-1">{step.titolo}</h3>
        <p className="text-xs text-slate-400 line-clamp-2">{step.descrizione}</p>
      </div>

      {/* Progress */}
      <div className="px-4 pb-4">
        <div className="flex justify-between text-xs mb-1">
          <span className={getStatusTextColor(step.status)}>
            {step.status === 'completed' ? 'Completato' : step.status === 'in_progress' ? 'In corso' : 'Da fare'}
          </span>
          <span className="text-slate-400">{step.progresso}%</span>
        </div>
        <div className="w-full bg-slate-700 rounded-full h-1.5 overflow-hidden">
          <div
            className={`h-full rounded-full transition-all duration-500 ${getStatusColor(step.status)}`}
            style={{ width: `${step.progresso}%` }}
          />
        </div>
      </div>

      {/* Expand indicator */}
      <div className={`px-4 pb-3 text-center transition-transform ${isExpanded ? 'rotate-180' : ''}`}>
        <span className="text-slate-500 text-xs">&#x25BC;</span>
      </div>
    </div>
  );
}

export function RoadmapWidget({ roadmap = mockRoadmap, loading = false }: RoadmapWidgetProps) {
  const [expandedStep, setExpandedStep] = useState<string | null>(null);

  if (loading) {
    return (
      <div className="bg-slate-800 rounded-lg p-6 border border-slate-700 animate-pulse">
        <div className="h-6 bg-slate-700 rounded w-32 mb-4"></div>
        <div className="flex gap-4 overflow-x-auto pb-4">
          {[...Array(4)].map((_, i) => (
            <div key={i} className="w-48 h-32 bg-slate-700 rounded flex-shrink-0"></div>
          ))}
        </div>
      </div>
    );
  }

  const expandedStepData = roadmap.steps.find((s) => s.id === expandedStep);

  return (
    <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <span className="text-2xl">&#x1F5FA;</span>
          <h2 className="text-lg font-semibold text-white">LA ROADMAP</h2>
        </div>
        <div className="flex items-center gap-2 text-sm">
          <span className="text-slate-400">Progresso totale:</span>
          <span className="text-amber-500 font-semibold">{roadmap.progressoTotale}%</span>
        </div>
      </div>

      {/* Timeline */}
      <div className="relative">
        {/* Connection line */}
        <div className="absolute top-1/2 left-0 right-0 h-0.5 bg-slate-700 -translate-y-1/2 z-0" />
        <div
          className="absolute top-1/2 left-0 h-0.5 bg-amber-500 -translate-y-1/2 z-0 transition-all duration-500"
          style={{ width: `${roadmap.progressoTotale}%` }}
        />

        {/* Steps */}
        <div className="flex gap-4 overflow-x-auto pb-4 relative z-10">
          {roadmap.steps.map((step) => (
            <StepCard
              key={step.id}
              step={step}
              isCurrent={step.numero === roadmap.stepCorrente}
              isExpanded={expandedStep === step.id}
              onExpand={() => setExpandedStep(expandedStep === step.id ? null : step.id)}
            />
          ))}

          {/* NORD finale */}
          <div className="flex-shrink-0 w-32 rounded-lg bg-gradient-to-br from-amber-500/20 to-amber-600/10 border border-amber-500/30 p-4 flex flex-col items-center justify-center">
            <span className="text-3xl mb-2">&#x2B50;</span>
            <span className="text-amber-400 font-bold text-sm">NORD</span>
            <span className="text-xs text-slate-400 mt-1">La foto!</span>
          </div>
        </div>
      </div>

      {/* Expanded step details */}
      {expandedStepData && (
        <div className="mt-4 p-4 bg-slate-900/50 rounded-lg border border-slate-700">
          <div className="flex items-center justify-between mb-3">
            <h4 className="font-semibold text-white">
              Step {expandedStepData.numero}: {expandedStepData.titolo}
            </h4>
            <button
              onClick={() => setExpandedStep(null)}
              className="text-slate-400 hover:text-white text-sm"
            >
              Chiudi
            </button>
          </div>
          <div className="space-y-2">
            {expandedStepData.subSteps.map((sub) => (
              <div
                key={sub.id}
                className="flex items-center gap-3 text-sm"
              >
                <span className={`w-5 h-5 rounded flex items-center justify-center text-xs ${
                  sub.status === 'completed'
                    ? 'bg-green-500/20 text-green-400'
                    : sub.status === 'in_progress'
                    ? 'bg-amber-500/20 text-amber-400'
                    : 'bg-slate-700 text-slate-500'
                }`}>
                  {sub.status === 'completed' ? '\u2713' : sub.status === 'in_progress' ? '\u25B6' : '\u25CB'}
                </span>
                <span className={`${sub.status === 'completed' ? 'text-slate-400 line-through' : 'text-white'}`}>
                  {sub.id} {sub.titolo}
                </span>
                {sub.status === 'in_progress' && (
                  <span className="text-xs text-amber-400 animate-pulse">IN CORSO</span>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
