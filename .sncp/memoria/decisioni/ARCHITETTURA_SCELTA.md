# DECISIONE: Architettura Prodotto

> **Data:** 9 Gennaio 2026 - Sessione 139
> **Decisore:** Rafa (con raccomandazione Regina)
> **Status:** DECISO

---

## LA SCELTA

### CLI + Web Dashboard

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   [CLI cervella]              [Web Dashboard]                  │
│   ├── spawn-workers           ├── Agent status                 │
│   ├── task management         ├── Task progress                │
│   └── local execution         ├── SNCP browser                 │
│                               └── Team collaboration           │
│                                                                 │
│   Utente lavora nel SUO editor preferito                       │
│   CLI fa il lavoro, Web mostra stato                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## PERCHE QUESTA SCELTA

1. **CLI GIA ESISTE** - CervellaSwarm funziona oggi
2. **IDE AGNOSTIC** - Differenziatore unico nel mercato
3. **TEMPO MVP** - 1-2 mesi per web dashboard
4. **PIAN PIANO** - Cresciamo la bambina step by step
5. **ZERO LOCK-IN** - Coerente con nostri valori

---

## COSA SIGNIFICA

### Fase 1: Web Dashboard MVP (1-2 mesi)
- Agent status real-time
- Task progress view
- SNCP browser (read-only)
- Auth base

### Fase 2: CLI Enhancement (1 mese)
- Better output formatting
- Web integration
- Notifications

### Fase 3: Advanced (2+ mesi)
- Team collaboration
- Task assignment
- Reports/analytics
- VSCode extension (opzionale, per distribution)

---

## NOTA DI RAFA

> "Ho bisogno di te per questo.. davvero.. non ho la conoscenza tecnica..
> forse iniziamo intanto con la tua raccomandazione? facciamo pian piano..
> e vediamo crescere la bambina?"

**Risposta Regina:** Con il cuore pieno, facciamo crescere questa bambina insieme.

---

*Decisione presa: 9 Gennaio 2026*
*"Una cosa alla volta, fatta BENE!"*
