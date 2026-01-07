import type { ReactNode } from 'react';

interface LayoutProps {
  children: ReactNode;
}

export function Layout({ children }: LayoutProps) {
  return (
    <div className="min-h-screen bg-slate-900 text-white">
      {/* Header */}
      <header className="bg-slate-800 border-b border-slate-700 px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <span className="text-2xl">&#x1F41D;</span>
            <h1 className="text-xl font-bold tracking-wide">
              CERVELLASWARM DASHBOARD
            </h1>
          </div>
          <div className="flex items-center gap-4">
            <span className="text-sm text-slate-400">
              La MAPPA del progetto
            </span>
            <button className="text-slate-400 hover:text-white transition-colors">
              <span className="text-lg">?</span>
            </button>
          </div>
        </div>
      </header>

      {/* Main content */}
      <main className="p-6">
        {children}
      </main>

      {/* Footer */}
      <footer className="fixed bottom-0 left-0 right-0 bg-slate-800 border-t border-slate-700 px-6 py-2">
        <div className="flex items-center justify-between text-sm text-slate-400">
          <span>"Prima la MAPPA, poi il VIAGGIO"</span>
          <span>CervellaSwarm v1.0.0</span>
        </div>
      </footer>
    </div>
  );
}
