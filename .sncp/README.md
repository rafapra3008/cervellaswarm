# SNCP - Sistema Nervoso Centrale Persistente

> **Progetto:** CervellaSwarm
> **Versione SNCP:** 5.0 (Semplificato + Senza Ridondanza!)
> **Aggiornato:** 20 Gennaio 2026 - Sessione 296

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
|   ORA AUTOMATICO: Hook pre/post sessione + Launchd!             |
|                                                                  |
+------------------------------------------------------------------+
```

---

## STRUTTURA REALE (v4.0)

```
.sncp/
├── README.md              # Questo file
│
├── progetti/              # CUORE - Un folder per progetto!
│   ├── cervellaswarm/     # CervellaSwarm
│   ├── miracollo/         # Miracollo
│   └── contabilita/       # Contabilita
│
├── stato/                 # (DEPRECATO - vedi sotto)
│
├── memoria/               # DECISIONI GLOBALI
│   └── decisioni/         # Decisioni architetturali cross-progetto
│
├── idee/                  # IDEE CORRENTI
│   └── *.md               # Idee in valutazione
│
├── handoff/               # PASSAGGI SESSIONE
│   └── *.md               # Handoff tra sessioni
│
├── reports/               # REPORT GLOBALI
│   └── daily/             # Health check giornalieri
│
├── sessioni_parallele/    # TEMPLATE
│   └── _TEMPLATE/         # Template per sessioni parallele
│
├── validazioni/           # VALIDAZIONI
│   └── *.md               # Report validazione
│
└── archivio/              # ARCHIVIO (automatico!)
    ├── 2026-01/           # Per mese
    └── 2026-W03/          # Per settimana
```

---

## RUOLI FILE (v5.0 - Chiarimento!)

```
+------------------------------------------------------------------+
|   stato.md (MAX 500 righe)                                       |
|   └── Verita COMPLETA progetto (architettura, decisioni, stack)  |
|   └── Aggiornare: ogni sessione significativa                    |
|   └── Leggere: quando serve contesto PROFONDO                    |
|                                                                  |
|   PROMPT_RIPRESA_{progetto}.md (MAX 150 righe)                   |
|   └── Context ripresa VELOCE (ultima sessione, next, blockers)   |
|   └── Aggiornare: OGNI sessione                                  |
|   └── Leggere: SEMPRE a inizio sessione                          |
|                                                                  |
|   PROMPT_RIPRESA_MASTER.md (MAX 50 righe)                        |
|   └── INDICE puro (tabella link progetti)                        |
|   └── Aggiornare: quando cambia progetto                         |
|   └── Leggere: quando switch progetto                            |
|                                                                  |
|   oggi.md                                                        |
|   └── DEPRECATO (Sessione 296) - NON USARE                       |
|   └── Motivo: ridondante con PROMPT_RIPRESA                      |
|   └── Rimozione: 27 Gennaio 2026                                 |
+------------------------------------------------------------------+
```

---

## STRUTTURA PROGETTO (dentro progetti/)

Ogni progetto ha la stessa struttura:

```
.sncp/progetti/{nome}/
├── stato.md          # UNICA fonte di verita per il progetto
├── CONFIG.md         # Configurazione (stack, path, convenzioni)
├── decisioni/        # Decisioni specifiche del progetto
├── idee/             # Idee specifiche
├── reports/          # Report e audit
├── roadmaps/         # Piani attivi
├── workflow/         # Protocolli specifici
└── moduli/           # Sotto-moduli (es: room_manager)
```

---

## COME USARE

### INIZIO SESSIONE (Automatico!)
```
Hook pre-session fa:
1. Check stato SNCP
2. Mostra ultimo aggiornamento
3. Warning se docs vecchi

Tu fai:
1. Leggi progetti/{nome}/stato.md del progetto
2. Leggi PROMPT_RIPRESA.md per contesto
```

### DURANTE SESSIONE
```
- Lavoro su progetto?  → progetti/{nome}/...
- Decisione globale?   → memoria/decisioni/YYYYMMDD_cosa.md
- Idea corrente?       → idee/YYYYMMDD_nome.md
- Ricerca?             → progetti/{nome}/ricerche/YYYYMMDD_topic.md
- Report?              → progetti/{nome}/reports/YYYYMMDD_report.md
```

### FINE SESSIONE (Automatico!)
```
Hook post-session fa:
1. Verifica coerenza docs/codice
2. Warning se stato.md non aggiornato
3. Reminder per commit

Tu fai:
1. Aggiorna progetti/{nome}/stato.md
2. Aggiorna PROMPT_RIPRESA.md (se lavoro significativo)
3. Commit
```

---

## HANDOFF SESSIONE (SNCP 2.0)

Template 6-sezioni in `.swarm/templates/TEMPLATE_SESSION_HANDOFF.md`

**Naming:** `HANDOFF_YYYYMMDD_{progetto}_S{N}.md`
**Dove:** `.swarm/handoff/`

**Sezioni:**
1. ACCOMPLISHED - Cosa completato
2. CURRENT STATE - Stato attuale
3. LESSONS LEARNED - Cosa imparato
4. NEXT STEPS - Prossimi passi
5. KEY FILES - File importanti
6. BLOCKERS - Problemi aperti

---

## NAMING FILE

```
GENERALE:    YYYYMMDD_NOME_BREVE.md
DECISIONI:   YYYYMMDD_COSA_DECISO.md
RICERCHE:    YYYYMMDD_RICERCA_TOPIC.md
REPORT:      YYYYMMDD_TIPO_cosa.md
```

---

## AUTOMAZIONI ATTIVE

| Quando | Cosa | Hook/Script |
|--------|------|-------------|
| Inizio sessione | Check stato SNCP + Warning | session_start_swarm.py |
| Fine sessione | Verifica limiti file | file_limits_guard.py |
| Login Mac | Daily maintenance | Launchd daily |
| Ogni Lunedi | Weekly archive | Launchd weekly |

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
> "Avere attrezzature ma non usarle = non averle" (ORA SI USANO DA SOLE!)

---

## CHANGELOG

| Sessione | Cosa |
|----------|------|
| 163 | Semplificazione iniziale |
| 207 | sncp-init wizard + verify-sync |
| 209 | Hook automatici + Launchd manutenzione |
| 211 | Pulizia struttura v4.0 (rimosse 4 cartelle obsolete) |
| **296** | **SNCP 5.0: Deprecato oggi.md, chiariti ruoli file** |
| 299 | SNCP 2.0 Day 5-6: Hook v2.1.0 + Documentazione finale |

---

*"SNCP: Semplice, Chiaro, Senza Ridondanza!"*
