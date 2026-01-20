# Cervella CLI

> AI Team per Developer Professionali - 17 agenti specializzati al tuo servizio.

## Installazione

```bash
# Clona il repo
git clone https://github.com/tuouser/cervellaswarm.git
cd cervellaswarm/cervella

# Installa
pip install -e .

# Aggiungi al PATH (se necessario)
export PATH="$HOME/Library/Python/3.13/bin:$PATH"
```

## Configurazione

```bash
# Imposta la tua API key Anthropic
export ANTHROPIC_API_KEY="sk-ant-..."
```

## Quick Start

```bash
# Inizializza in un progetto
cd /path/to/your/project
cervella init

# Verifica status
cervella status

# Delega un task
cervella task "Implementa autenticazione JWT"

# Specifica un agente
cervella task "Analizza i competitor" --agent scienziata
```

## Comandi

| Comando | Descrizione |
|---------|-------------|
| `cervella init` | Inizializza SNCP nel progetto |
| `cervella status` | Mostra agenti e stato memoria |
| `cervella task "..."` | Delega un task agli agenti |
| `cervella checkpoint -m "..."` | Salva stato con messaggio |

## Agenti Disponibili (16)

### Worker (Sonnet)
| Agente | Specializzazione |
|--------|------------------|
| backend | Python, FastAPI, Database |
| frontend | React, CSS, UI/UX |
| tester | Testing, QA, Debugging |
| researcher | Ricerca tecnica |
| scienziata | Ricerca strategica, mercato |
| docs | Documentazione |
| reviewer | Code review |
| data | SQL, Analytics |
| devops | Deploy, Docker, CI/CD |
| security | Sicurezza, Audit |
| marketing | UX Strategy |
| ingegnera | Analisi codebase |

### Supervisori (Opus)
| Agente | Ruolo |
|--------|-------|
| regina | Orchestratrice principale |
| guardiana-ops | Supervisione operazioni |
| guardiana-qualita | Verifica qualità codice |
| guardiana-ricerca | Verifica qualità ricerche |

## SNCP - Memoria Esterna

Cervella usa SNCP (Sistema Nervoso Centrale Persistente) per ricordare:

```
.sncp/
├── idee/           # Ricerche, analisi
├── memoria/
│   ├── decisioni/  # Con il PERCHE
│   ├── sessioni/   # Checkpoint
│   └── lezioni/    # Lessons learned
└── coscienza/      # Stato corrente
```

## Variabili Ambiente

| Variabile | Descrizione | Default |
|-----------|-------------|---------|
| `ANTHROPIC_API_KEY` | API key Anthropic | (required) |
| `CERVELLA_DEFAULT_MODEL` | Modello default | claude-sonnet-4 |
| `CERVELLA_OPUS_MODEL` | Modello Opus | claude-opus-4 |

## Filosofia

> "Lavoriamo in PACE! Senza CASINO!"
> "Fatto BENE > Fatto VELOCE"
> "I dettagli fanno SEMPRE la differenza"

## BYOK - Bring Your Own Key

Cervella usa il tuo API key Anthropic. Tu paghi solo quello che usi, direttamente ad Anthropic.

---

**CervellaSwarm** - Fare il mondo meglio su di come riusciamo a fare.
