# /init-sncp

Inizializza la struttura SNCP (Sistema Nervoso Centrale Progetti) nel progetto corrente.

## Cosa Fa

Crea la struttura cartelle per la memoria esterna del progetto:

```
.sncp/
├── idee/              # Idee, ricerche, brainstorming
├── memoria/
│   ├── decisioni/     # Decisioni prese con PERCHE
│   ├── sessioni/      # Log sessioni di lavoro
│   └── lezioni/       # Lezioni apprese
└── coscienza/         # Pensieri correnti, stato
```

## Istruzioni per Claude

Quando l'utente esegue `/init-sncp`:

1. Crea le cartelle se non esistono
2. Crea file template in ogni cartella
3. Crea un file `README.md` che spiega SNCP
4. Conferma all'utente cosa e stato creato

## Template da Creare

### .sncp/idee/_TEMPLATE_IDEA.md
```markdown
# IDEA: [Titolo]

> Data: [oggi]
> Status: DRAFT | IN_PROGRESS | DONE | ARCHIVED

## Descrizione
[Cosa e questa idea]

## Perche
[Perche e importante]

## Come
[Come implementarla]

## Note
[Altre considerazioni]
```

### .sncp/memoria/decisioni/_TEMPLATE_DECISIONE.md
```markdown
# DECISIONE: [Titolo]

> Data: [oggi]
> Decisore: [chi ha deciso]
> Status: DECISO | IN_DISCUSSIONE

## La Decisione
[Cosa abbiamo deciso]

## Perche Questa Scelta
[Motivazione - IMPORTANTE!]

## Alternative Considerate
[Cosa altro abbiamo valutato]

## Conseguenze
[Cosa cambia con questa decisione]
```

### .sncp/README.md
```markdown
# SNCP - Sistema Nervoso Centrale Progetti

> "MINIMO in memoria, MASSIMO su disco"

## Cosa e SNCP

SNCP e il sistema di memoria esterna di CervellaSwarm.
Invece di tenere tutto nel context (che si riempie),
scriviamo su disco e leggiamo quando serve.

## Struttura

- `idee/` - Idee, ricerche, brainstorming
- `memoria/decisioni/` - Decisioni prese (con PERCHE!)
- `memoria/sessioni/` - Log delle sessioni
- `memoria/lezioni/` - Lezioni apprese
- `coscienza/` - Stato corrente, pensieri

## Come Usarlo

1. Hai un'idea? → Scrivi in `idee/`
2. Prendi una decisione? → Documenta in `memoria/decisioni/`
3. Impari qualcosa? → Salva in `memoria/lezioni/`

## Regola d'Oro

Scrivi come se la prossima sessione non sapesse NULLA.
Il context si azzera, ma `.sncp/` resta!
```

## Esecuzione

```bash
mkdir -p .sncp/idee
mkdir -p .sncp/memoria/decisioni
mkdir -p .sncp/memoria/sessioni
mkdir -p .sncp/memoria/lezioni
mkdir -p .sncp/coscienza
```

Poi crea i file template come descritto sopra.
