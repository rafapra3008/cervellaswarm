import { Layout } from './components/Layout'
import { NordWidget } from './components/NordWidget'
import { FamigliaWidget } from './components/FamigliaWidget'
import { RoadmapWidget } from './components/RoadmapWidget'
import { SessioneWidget } from './components/SessioneWidget'
import { useDashboardData } from './hooks/useDashboardData'

function App() {
  const { nord, famiglia, roadmap, sessione, loading, error } = useDashboardData(30000);

  if (error) {
    return (
      <Layout>
        <div className="glass-card p-8 text-center">
          <span className="text-4xl mb-4 block">⚠️</span>
          <p className="text-error mb-2">Errore connessione API</p>
          <p className="text-text-muted text-sm">{error.message}</p>
          <p className="text-text-muted text-xs mt-4">Verifica che il backend sia attivo su localhost:8100</p>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        <NordWidget nord={nord ?? undefined} loading={loading} />
        <FamigliaWidget famiglia={famiglia ?? undefined} loading={loading} />
      </div>
      <div className="mb-8">
        <RoadmapWidget roadmap={roadmap ?? undefined} loading={loading} />
      </div>
      <div className="mb-24">
        <SessioneWidget sessione={sessione ?? undefined} loading={loading} />
      </div>
    </Layout>
  )
}

export default App
