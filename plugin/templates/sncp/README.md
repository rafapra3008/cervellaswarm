# SNCP - Sistema Nervoso Centrale Progetti

> "MINIMO in memoria, MASSIMO su disco"

---

## Cosa e SNCP

SNCP e il sistema di memoria esterna di CervellaSwarm.

**Il problema:** Il context di Claude si riempie e poi si azzera.
**La soluzione:** Scriviamo su disco. Il disco non si azzera!

---

## Struttura

```
.sncp/
├── idee/              # Idee, ricerche, brainstorming
├── memoria/
│   ├── decisioni/     # Decisioni prese (con PERCHE!)
│   ├── sessioni/      # Log sessioni di lavoro
│   └── lezioni/       # Lezioni apprese
└── coscienza/         # Stato corrente, pensieri
```

---

## Come Usarlo

| Situazione | Dove Scrivere |
|------------|---------------|
| Ho un'idea | `idee/IDEA_[nome].md` |
| Prendo una decisione | `memoria/decisioni/DECISIONE_[nome].md` |
| Imparo qualcosa | `memoria/lezioni/LEZIONE_[nome].md` |
| Fine sessione | `memoria/sessioni/SESSIONE_[numero].md` |
| Stato corrente | `coscienza/stato_corrente.md` |

---

## Regola d'Oro

> Scrivi come se la prossima sessione non sapesse NULLA.

Il context si azzera, ma `.sncp/` resta!

---

## Template

Ogni cartella ha un template `_TEMPLATE_*.md`.
Usalo come base per nuovi file.

---

*CervellaSwarm - "Lavoriamo in PACE! Senza CASINO!"*
