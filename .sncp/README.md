# SNCP - Sistema Nervoso Centrale Persistente

> **Progetto:** CervellaSwarm
> **Versione SNCP:** 3.0 (Semplificato!)
> **Aggiornato:** 11 Gennaio 2026 - Sessione 163

---

## REGOLA D'ORO

```
+------------------------------------------------------------------+
|                                                                  |
|   "SNCP funziona solo se lo VIVIAMO!"                           |
|                                                                  |
|   Semplice da usare. Chiaro dove mettere cosa.                  |
|   Se e' troppo complicato, non viene usato.                     |
|                                                                  |
+------------------------------------------------------------------+
```

---

## STRUTTURA REALE

```
.sncp/
├── README.md              # Questo file
│
├── stato/                 # IL PRESENTE
│   └── oggi.md            # Stato OGGI - aggiornare ogni sessione!
│
├── coscienza/             # IL CUORE
│   └── pensieri_regina.md # Stream pensieri Regina
│
├── idee/                  # LE IDEE
│   ├── in_attesa/         # Idee da valutare
│   ├── integrate/         # Idee realizzate
│   ├── roadmap/           # Roadmap e planning
│   └── ricerche/          # Ricerche approfondite
│
├── memoria/               # IL PASSATO
│   ├── sessioni/          # Log sessioni
│   ├── decisioni/         # Decisioni prese con PERCHE
│   └── lezioni/           # Lezioni imparate
│
├── futuro/                # DOVE ANDIAMO
│   └── roadmap.md         # Linea principale
│
├── analisi/               # ANALISI
│   └── *.md               # Report analisi
│
├── regole/                # REGOLE
│   └── *.md               # Regole del progetto
│
└── archivio/              # FILE VECCHI
    └── 2026-01/           # Archiviati per mese
```

---

## COME USARE

### INIZIO SESSIONE
```
1. Leggi stato/oggi.md
2. Aggiorna data/sessione
```

### DURANTE SESSIONE
```
- Nuova idea?      → idee/in_attesa/YYYYMMDD_nome.md
- Decisione?       → memoria/decisioni/YYYYMMDD_cosa.md
- Pensiero?        → coscienza/pensieri_regina.md
- Ricerca?         → idee/ricerche/YYYYMMDD_ricerca_topic.md
```

### FINE SESSIONE
```
1. Aggiorna stato/oggi.md con cosa fatto
2. Commit SNCP insieme al codice
```

---

## NAMING FILE

```
IDEE:      YYYYMMDD_NOME_BREVE.md
DECISIONI: YYYYMMDD_COSA_DECISO.md
RICERCHE:  YYYYMMDD_RICERCA_TOPIC.md
```

---

## TOOLS SNCP

### sncp-init - Wizard nuovo progetto

```bash
# Uso base
sncp-init nome-progetto

# Con analisi automatica stack
sncp-init nome-progetto --analyze

# Help
sncp-init --help
```

**Cosa crea:**
```
.sncp/progetti/{nome}/
├── stato.md          <- UNICA fonte di verita
├── CONFIG.md         <- Configurazione progetto
├── decisioni/        <- Decisioni importanti
├── roadmaps/         <- Piani attivi
└── handoff/          <- Sessioni parallele
```

### verify-sync - Verifica coerenza docs/codice

```bash
# Tutti i progetti
verify-sync

# Singolo progetto
verify-sync miracollo

# Output dettagliato
verify-sync --verbose
```

**Cosa controlla:**
- stato.md aggiornato di recente
- Commit recenti documentati
- Migrations menzionate
- File grandi modificati

### Altri script (in scripts/sncp/)

| Script | Cosa fa |
|--------|---------|
| `pre-session-check.sh` | Check salute SNCP a inizio sessione |
| `health-check.sh` | Check completo stato SNCP |
| `compact-state.sh` | Compatta file troppo grandi |
| `post-session-update.sh` | Update automatico fine sessione |

---

## FILOSOFIA

> "Il sistema centrale DEVE funzionare!"
> "Semplificare = usare di piu!"
> "Lavoriamo in pace! Senza casino!"
> "La memoria e' il fondamento dell'intelligenza collettiva."

---

*Sessione 163 - Semplificazione SNCP*
*Sessione 207 - Aggiunto sncp-init wizard*
*"La MAGIA ora e' con coscienza!"*
