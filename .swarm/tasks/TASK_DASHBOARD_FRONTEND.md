# TASK: Dashboard Frontend Base

**Assegnato a:** cervella-frontend
**Rischio:** 2-MEDIO
**Timeout:** 30 minuti
**Stato:** ready

---

## OBIETTIVO

Creare il frontend React per la Dashboard MAPPA di CervellaSwarm.

---

## CONTESTO

Stiamo costruendo una Dashboard visuale per vedere:
- IL NORD (obiettivo del progetto)
- LA FAMIGLIA (16 agenti e loro stato)
- LA ROADMAP (step del progetto)
- SESSIONE ATTIVA (task in corso)

Tu crei il FRONTEND. cervella-backend crea il BACKEND (API su localhost:8000).

---

## COSA CREARE

### Struttura

```
/Users/rafapra/Developer/CervellaSwarm/dashboard/
+-- frontend/
    +-- src/
    |   +-- App.tsx              # App principale
    |   +-- main.tsx             # Entry point
    |   +-- index.css            # Tailwind imports
    |   +-- components/
    |   |   +-- Layout.tsx       # Layout con header
    |   |   +-- NordWidget.tsx   # Widget IL NORD
    |   |   +-- FamigliaWidget.tsx # Widget LA FAMIGLIA
    |   |   +-- RoadmapWidget.tsx  # Widget LA ROADMAP
    |   |   +-- SessioneWidget.tsx # Widget SESSIONE
    |   +-- hooks/
    |   |   +-- useApi.ts        # Hook per fetch API
    |   |   +-- useSSE.ts        # Hook per SSE events
    |   +-- types/
    |       +-- index.ts         # TypeScript types
    +-- index.html
    +-- package.json
    +-- vite.config.ts
    +-- tailwind.config.js
    +-- postcss.config.js
    +-- tsconfig.json
```

### Setup Comandi

```bash
npm create vite@latest frontend -- --template react-ts
cd frontend
npm install
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

### Componenti

1. **Layout.tsx**
   - Header con "CERVELLASWARM DASHBOARD"
   - Grid layout per i widget
   - Dark theme (bg-slate-900)

2. **NordWidget.tsx**
   - Mostra obiettivo (es. "LIBERTA' GEOGRAFICA")
   - Progress bar generale
   - Sessione corrente

3. **FamigliaWidget.tsx**
   - Grid 4x4 con i 16 agenti
   - Icona + nome + stato
   - Colori: verde=working, grigio=idle
   - Contatore "X attivi | Y idle"

4. **RoadmapWidget.tsx**
   - Timeline orizzontale
   - Box per ogni STEP
   - Progress % per step
   - Espandibile per vedere substeps

5. **SessioneWidget.tsx**
   - Task attivo (se c'è)
   - Worker assegnato
   - Timer (tempo trascorso)
   - Ultimi log messages

### Hooks

```typescript
// useApi.ts
export function useApi<T>(endpoint: string) {
  // Fetch da http://localhost:8000/api/...
  // Ritorna { data, loading, error, refetch }
}

// useSSE.ts
export function useSSE(onEvent: (event: any) => void) {
  // Connette a http://localhost:8000/api/events
  // Chiama onEvent quando arriva un evento
}
```

### Palette Colori (da studio UX)

```
bg-slate-900     # Background principale
text-white       # Testo
amber-500        # Accenti, NORD
green-500        # Success, working
gray-500         # Idle
red-500          # Error
```

---

## STUDI DI RIFERIMENTO

Leggi questi file per design:
- docs/studio/STUDIO_DASHBOARD_UX.md (wireframe, palette, UX!)
- docs/studio/STUDIO_DASHBOARD_TECH.md (stack tecnico)

---

## OUTPUT

1. Tutti i file creati nella struttura sopra
2. `npm run dev` funziona su http://localhost:5173
3. Layout base visibile
4. Componenti placeholder per ogni widget
5. Hooks pronti per connettersi al backend

---

## NOTE

- Per ora i widget possono avere dati mock/placeholder
- L'importante è che la struttura sia pronta
- Il backend sarà su localhost:8000
- Vite proxy: configura per /api → localhost:8000
- Workspace: /Users/rafapra/Developer/CervellaSwarm/

---

*"Prima la MAPPA, poi il VIAGGIO"* - Tu costruisci l'interfaccia!
