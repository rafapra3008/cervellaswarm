import type { Nord } from '../types';

interface NordWidgetProps {
  nord?: Nord;
  loading?: boolean;
}

// Dati mock per sviluppo
const mockNord: Nord = {
  obiettivo: "LIBERTA' GEOGRAFICA",
  descrizione: "Quando l'avremo raggiunta, Rafa scattera una foto da un posto speciale nel mondo.",
  progressoGenerale: 15,
  sessioneCorrente: 111,
  frase: "L'idea e' fare il mondo meglio su di come riusciamo a fare."
};

export function NordWidget({ nord = mockNord, loading = false }: NordWidgetProps) {
  if (loading) {
    return (
      <div className="bg-slate-800 rounded-lg p-6 border border-slate-700 animate-pulse">
        <div className="h-6 bg-slate-700 rounded w-24 mb-4"></div>
        <div className="h-10 bg-slate-700 rounded w-full mb-4"></div>
        <div className="h-4 bg-slate-700 rounded w-3/4"></div>
      </div>
    );
  }

  return (
    <div className="bg-slate-800 rounded-lg p-6 border border-slate-700 hover:border-amber-500/50 transition-colors">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <span className="text-2xl">&#x2B50;</span>
          <h2 className="text-lg font-semibold text-amber-500">IL NORD</h2>
        </div>
        <span className="text-sm text-slate-400">
          Sessione {nord.sessioneCorrente}
        </span>
      </div>

      {/* Obiettivo principale */}
      <div className="bg-slate-900/50 rounded-lg p-4 mb-4 border border-amber-500/20">
        <h3 className="text-2xl font-bold text-white text-center mb-2">
          {nord.obiettivo}
        </h3>
        <p className="text-sm text-slate-400 text-center">
          {nord.descrizione}
        </p>
      </div>

      {/* Progress bar */}
      <div className="mb-4">
        <div className="flex justify-between text-sm mb-1">
          <span className="text-slate-400">Progresso Generale</span>
          <span className="text-amber-500 font-semibold">{nord.progressoGenerale}%</span>
        </div>
        <div className="w-full bg-slate-700 rounded-full h-3 overflow-hidden">
          <div
            className="bg-gradient-to-r from-amber-600 to-amber-400 h-full rounded-full transition-all duration-500"
            style={{ width: `${nord.progressoGenerale}%` }}
          />
        </div>
      </div>

      {/* Frase motivazionale */}
      {nord.frase && (
        <blockquote className="text-sm text-slate-400 italic border-l-2 border-amber-500/30 pl-3">
          "{nord.frase}"
        </blockquote>
      )}
    </div>
  );
}
