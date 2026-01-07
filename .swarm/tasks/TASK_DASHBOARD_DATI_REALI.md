# Task: Collegare Dashboard a Dati Reali

**Assegnato a:** cervella-frontend
**Stato:** ready
**Priorita:** ALTA
**Data:** 2026-01-07

---

## Obiettivo

Collegare i widget della Dashboard ai dati reali dell'API invece dei mock data.

---

## Situazione Attuale

I componenti in `dashboard/frontend/src/components/` usano mock data hardcoded:
- `NordWidget.tsx` - mockNord a riga 5-11
- `FamigliaWidget.tsx` - mock data
- `RoadmapWidget.tsx` - mock data
- `SessioneWidget.tsx` - mock data

L'API backend e' GIA' funzionante su `http://localhost:8100`:
- GET /api/mappa -> Mappa completa (nord, roadmap, steps)
- GET /api/nord -> Solo NORD
- GET /api/tasks -> Lista task
- GET /api/workers -> Stato worker

---

## Azione Richiesta

1. Crea un hook `useDashboardData.ts` in `dashboard/frontend/src/hooks/` che:
   - Fa fetch a http://localhost:8100/api/mappa
   - Gestisce loading state
   - Gestisce errori
   - Ritorna i dati strutturati

2. Modifica `App.tsx` per:
   - Usare il nuovo hook
   - Passare i dati reali ai widget
   - Mostrare loading state

3. Verifica che i widget accettino i dati come props (gia' fatto)

---

## API Response Structure

```json
{
  "version": "1.0.0",
  "updated_at": "2026-01-07...",
  "project": {
    "name": "CervellaSwarm",
    "claim": "Uno sciame di Cervelle...",
    "objective": "LIBERTA GEOGRAFICA"
  },
  "nord": {
    "source_file": "NORD.md",
    "current_session": {"number": 118, "date": "...", "title": "..."},
    "stato_reale": [...],
    "pezzi": [...]
  },
  "roadmap": {
    "source_file": "ROADMAP_SACRA.md",
    "current_phase": {"number": 12, "name": "...", "status": "IN CORSO"},
    "completed_phases": [...]
  }
}
```

---

## Output Atteso

- Hook `useDashboardData.ts` creato
- `App.tsx` modificato per usare dati reali
- Dashboard mostra dati dal vivo invece di mock

---

## Test

1. Apri http://localhost:5173
2. Verifica che i dati cambino quando modifichi NORD.md
3. Verifica che "Sessione 118" appaia (non 117)
