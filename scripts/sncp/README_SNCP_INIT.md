# SNCP-INIT v2.0.0

> **Script per inizializzare la memoria SNCP in un nuovo progetto**
>
> "La memoria e' il fondamento dell'intelligenza collettiva."

---

## Quick Start

```bash
# Inizializza SNCP per un nuovo progetto
./scripts/sncp/sncp-init.sh nome-progetto

# Con analisi automatica dello stack (se il progetto esiste in ~/Developer/)
./scripts/sncp/sncp-init.sh nome-progetto --analyze
```

### Quando Usare

| Scenario | Azione |
|----------|--------|
| Nuovo progetto | `sncp-init nome-progetto` |
| Progetto esistente senza SNCP | `sncp-init nome-progetto --analyze` |
| Progetto con SNCP gia configurato | Usa `health-check.sh` invece |

---

## Cosa Crea v2.0.0

### Struttura SNCP (in CervellaSwarm/.sncp/progetti/)

```
.sncp/progetti/{nome_progetto}/
├── PROMPT_RIPRESA_{nome_progetto}.md  <- Stato sessioni (LEGGI QUESTO!)
├── stato.md                           <- Stato tecnico progetto
├── CONFIG.md                          <- Configurazione e convenzioni
├── decisioni/                         <- Decisioni importanti
├── roadmaps/                          <- Piani e subroadmap
├── handoff/                           <- Sessioni parallele
├── archivio/                          <- Sessioni vecchie (> 150 righe)
└── ricerche/                          <- Studi e analisi
```

### NORD.md (nella root del progetto)

Se il progetto esiste in `~/Developer/{nome-progetto}/`, viene creato anche:

```
{progetto}/
└── NORD.md  <- LA BUSSOLA (sacro!)
```

---

## Naming Convention

Lo script normalizza automaticamente i nomi:

| Input | Output SNCP |
|-------|-------------|
| `mio-progetto` | `PROMPT_RIPRESA_mio_progetto.md` |
| `MioProgetto` | `PROMPT_RIPRESA_mioprogetto.md` |
| `test-app-v2` | `PROMPT_RIPRESA_test_app_v2.md` |

**Regola:** trattini → underscore, tutto minuscolo

---

## Checklist Nuovo Progetto

Dopo aver eseguito `sncp-init`:

### 1. Compila PROMPT_RIPRESA

```markdown
# Modifica questi placeholder:
- {{STATUS_BREVE}} -> "MVP in sviluppo" / "Produzione" / etc.
- {{TASK_1}}, {{TASK_2}} -> Task reali
- {{FASE_1}}, {{FASE_2}} -> Fasi del progetto
```

### 2. Compila NORD.md

```markdown
# Sezioni da compilare:
- LA GRANDE VISIONE -> Cosa fa il progetto in 3 righe
- DOVE SIAMO -> Progress bar reale
- DECISIONI CHIUSE -> Decisioni gia prese
- PUNTATORI -> Link a docs importanti
```

### 3. Aggiorna stato.md

```markdown
# Info tecniche:
- Stack reale (Python, React, etc.)
- Comandi utili (dev, test, build)
- Struttura cartelle
```

### 4. Inizia a lavorare!

```bash
# Ogni inizio sessione, leggi:
cat .sncp/progetti/{progetto}/PROMPT_RIPRESA_{progetto}.md

# Ogni fine sessione, aggiorna lo stesso file
```

---

## Opzioni

| Flag | Descrizione |
|------|-------------|
| `--analyze` | Rileva automaticamente stack e deploy dal codebase |
| `--help` | Mostra help |

### Esempio con --analyze

```bash
./scripts/sncp/sncp-init.sh miracollo --analyze

# Output:
# [OK] Stack rilevato: Python, FastAPI, PostgreSQL
# [OK] Deploy rilevato: Docker, GitHub Actions
```

---

## Troubleshooting

### "Template non trovato"

```bash
# Verifica che i template esistano:
ls scripts/sncp/templates/
# Dovrebbe mostrare:
# - PROMPT_RIPRESA_TEMPLATE.md
# - NORD_TEMPLATE.md
```

### "NORD.md non creato"

Lo script cerca il progetto in:
1. `~/Developer/{nome-progetto}/`
2. `./{nome-progetto}/`
3. Directory corrente se ha lo stesso nome

Se non trova il path, mostra un warning. Crea manualmente:

```bash
cp scripts/sncp/templates/NORD_TEMPLATE.md ~/Developer/mio-progetto/NORD.md
# Poi compila i placeholder
```

### "Progetto gia esistente"

Se la cartella SNCP esiste gia, lo script chiede conferma:

```
[!] Progetto gia' esistente!
Vuoi sovrascrivere? (y/n):
```

Rispondi `y` per sovrascrivere, `n` per annullare.

---

## Comandi Correlati

| Comando | Scopo |
|---------|-------|
| `pre-session-check.sh {progetto}` | Verifica salute SNCP a inizio sessione |
| `check-ripresa-size.sh {progetto}` | Controlla limite 150 righe |
| `health-check.sh` | Check completo di tutti i progetti |
| `compact-state.sh {progetto}` | Compatta stato.md se troppo grande |

---

## Versioni

| Versione | Data | Novita |
|----------|------|--------|
| 2.0.0 | 3 Feb 2026 | Templates, NORD.md, archivio/, ricerche/ |
| 1.0.0 | 14 Gen 2026 | Versione iniziale |

---

## File Correlati

- Template PROMPT_RIPRESA: `scripts/sncp/templates/PROMPT_RIPRESA_TEMPLATE.md`
- Template NORD.md: `scripts/sncp/templates/NORD_TEMPLATE.md`
- Script principale: `scripts/sncp/sncp-init.sh`

---

*"Ultrapassar os proprios limites!"*
*Cervella & Rafa - Sessione 332*
