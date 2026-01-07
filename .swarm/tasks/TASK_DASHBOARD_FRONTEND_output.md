# Output: TASK_DASHBOARD_FRONTEND

**Worker:** cervella-frontend
**Stato:** COMPLETATO
**Data:** 2026-01-07 01:25

---

## CREATO

### Struttura Progetto

```
dashboard/frontend/
├── src/
│   ├── App.tsx              # App principale con layout a grid
│   ├── main.tsx             # Entry point
│   ├── index.css            # Tailwind imports + custom styles
│   ├── components/
│   │   ├── Layout.tsx       # Layout con header + footer
│   │   ├── NordWidget.tsx   # Widget IL NORD (obiettivo)
│   │   ├── FamigliaWidget.tsx # Widget LA FAMIGLIA (16 agenti)
│   │   ├── RoadmapWidget.tsx  # Widget LA ROADMAP (timeline)
│   │   └── SessioneWidget.tsx # Widget SESSIONE (task attivo)
│   ├── hooks/
│   │   ├── useApi.ts        # Hook per fetch API
│   │   └── useSSE.ts        # Hook per SSE events
│   └── types/
│       └── index.ts         # TypeScript types completi
├── index.html
├── package.json
├── vite.config.ts           # Con proxy per /api -> localhost:8000
├── tailwind.config.js       # Con palette colori da studio UX
├── postcss.config.js        # Con @tailwindcss/postcss
└── tsconfig.json
```

### Componenti Implementati

1. **Layout.tsx**
   - Header con logo e titolo "CERVELLASWARM DASHBOARD"
   - Footer fisso con frase e versione
   - Dark theme (bg-slate-900)

2. **NordWidget.tsx**
   - Mostra obiettivo "LIBERTA' GEOGRAFICA"
   - Progress bar con gradiente amber
   - Frase motivazionale
   - Sessione corrente

3. **FamigliaWidget.tsx**
   - Grid con tutti i 16 agenti
   - Regina, 3 Guardiane (Opus), 12 Worker (Sonnet)
   - Stati: idle (grigio), working (verde animato)
   - Contatore "X attivi | Y idle"

4. **RoadmapWidget.tsx**
   - Timeline orizzontale scorrevole
   - Step con progress bar
   - Espandibile per vedere substeps
   - NORD finale con stella

5. **SessioneWidget.tsx**
   - Info task attivo (nome, worker, durata)
   - Timer live che si aggiorna
   - Log scrollabile con icone colorate
   - Pulsanti "Vedi Log" e "Ferma"

### Hooks

- **useApi.ts**: Hook generico per fetch + hooks specifici per ogni endpoint
- **useSSE.ts**: Hook per Server-Sent Events con auto-reconnect

### Configurazione

- Vite proxy: `/api` -> `localhost:8000`
- Tailwind: palette custom (deep-blue, gold, success, etc.)
- TypeScript: types per tutti i modelli dati

---

## COMANDI

```bash
cd dashboard/frontend

# Sviluppo
npm run dev    # http://localhost:5173

# Build
npm run build  # Output in dist/
```

---

## NOTE

- Tutti i widget hanno dati mock per sviluppo
- Pronti per connettersi al backend (hooks gia' implementati)
- Build production funziona correttamente
- CSS dark theme con scrollbar custom

---

## PROSSIMI STEP

1. Backend crea API su localhost:8000
2. Sostituire dati mock con fetch reali
3. Attivare SSE per aggiornamenti live
4. Test integrazione frontend-backend

---

*"Prima la MAPPA, poi il VIAGGIO"*
