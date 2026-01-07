import { Layout } from './components/Layout'
import { NordWidget } from './components/NordWidget'
import { FamigliaWidget } from './components/FamigliaWidget'
import { RoadmapWidget } from './components/RoadmapWidget'
import { SessioneWidget } from './components/SessioneWidget'

function App() {
  return (
    <Layout>
      {/* Grid layout per i widget */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        {/* IL NORD - Widget obiettivo */}
        <NordWidget />

        {/* LA FAMIGLIA - Widget 16 agenti */}
        <FamigliaWidget />
      </div>

      {/* LA ROADMAP - Timeline orizzontale */}
      <div className="mb-6">
        <RoadmapWidget />
      </div>

      {/* SESSIONE ATTIVA - Task in corso */}
      <div className="mb-20">
        <SessioneWidget />
      </div>
    </Layout>
  )
}

export default App
