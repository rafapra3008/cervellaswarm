# Task: Fix SwarmWidget Layout

**Assegnato a:** cervella-frontend
**Stato:** ready
**Priorità:** ALTA

## Problema

Lo SwarmWidget ha problemi di layout:
1. La Regina appare in alto a sinistra invece che al centro
2. I nodi escono dal contenitore (overflow: visible)
3. Il viewBox SVG non scala correttamente
4. Il contenitore non ha altezza definita correttamente

## Screenshot del problema

La Regina (corona 👑) appare tagliata in alto a sinistra del widget invece che al centro dello sciame.

## Cosa DEVE succedere

1. Regina AL CENTRO del widget (visibile!)
2. 3 Guardiane in cerchio interno attorno alla Regina
3. 12 Worker in cerchio esterno
4. Header "🐝 Lo Sciame" VISIBILE in alto
5. Legenda VISIBILE in basso
6. Tutto contenuto DENTRO il glass-card

## File da modificare

- `dashboard/frontend/src/components/swarm/SwarmWidget.tsx`
- `dashboard/frontend/src/components/swarm/swarm.module.css`

## Specifiche tecniche

```
SVG_SIZE = 450
CENTER = 225
viewBox = "0 0 450 450"

Il problema è probabilmente:
1. swarmContainer ha height: 100% ma il parent non ha altezza
2. SVG overflow: visible causa rendering fuori dal box
3. aspect-ratio mancante per mantenere quadrato
```

## Fix suggerito

1. Aggiungere `aspect-ratio: 1` al contenitore
2. Dare altezza fissa o min-height adeguata
3. Verificare che overflow non causi problemi
4. Testare che tutti i nodi siano visibili

## Output atteso

File modificati + screenshot che mostri:
- Regina al centro con glow oro
- 3 Guardiane viola primo anello
- 12 Worker blu secondo anello
- Header e legenda visibili

## Test

Verificare su http://localhost:5173 che il widget sia corretto
