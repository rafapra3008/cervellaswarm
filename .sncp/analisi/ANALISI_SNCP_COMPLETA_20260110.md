# Analisi SNCP Completa

> **Data:** 10 Gennaio 2026
> **Analista:** cervella-researcher
> **Sessione:** 148

---

## Statistiche

### Struttura Generale

| Cartella | File | Note |
|----------|------|------|
| `/analisi` | 4 | Bug fixes, audit |
| `/coscienza` | 4 | Pensieri, domande, pattern |
| `/futuro` | 2 | Roadmap, prossimi step |
| `/idee` | 35 | Ricerche, roadmap, studi |
| `/memoria` | 3 sottocartelle | Decisioni, lezioni, sessioni |
| `/perne` | 3 | Template + cartelle vuote! |
| `/regole` | 1 | PRINCIPI_LAVORO |
| `/reports` | 1 | Code review |
| `/stato` | 2 | Mappa viva, oggi |
| `/test` | 2 | Test scrittura |

### Sottocartelle Memoria

| Cartella | File |
|----------|------|
| `decisioni/` | 13 (incluso template) |
| `lezioni/` | 2 (incluso template) |
| `sessioni/` | 3 (incluso template) |

### Sottocartelle Idee

| Cartella | Stato |
|----------|-------|
| `in_attesa/` | 1 file (SNCP originale) |
| `in_studio/` | **VUOTA** |
| `integrate/` | **VUOTA** |
| `ricerche_prodotto/` | 16 file |

**TOTALE FILE MD:** 84 file

---

## Contenuti Chiave Trovati

### Decisioni Strategiche (Alta Importanza)

1. **ARCHITETTURA_SCELTA.md** - CLI + Web Dashboard (DECISO)
2. **PRICING_STRATEGIA.md** - $0/19/39 tier (DECISO)
3. **20260109_BYOK_vs_bundled_da_decidere.md** - BYOK per MVP (DECISO)
4. **20260110_PARCHEGGIO_PRODOTTO.md** - Focus miglioramento, non lancio (DECISO)

### Ricerche Complete

- Competitor analysis (Cursor, Windsurf, Copilot)
- Claude Code studio
- Pricing modulare
- Storia Cursor
- Target market

### Regole Operative

- `PRINCIPI_LAVORO.md` - 7 principi fondamentali

---

## Decisioni Non Implementate

| Decisione | File | Status |
|-----------|------|--------|
| Tier limits nel CLI | BYOK_vs_bundled | **NON FATTO** |
| Tracking usage per analytics | BYOK_vs_bundled | **NON FATTO** |
| License key system | BYOK_vs_bundled | **PARCHEGGIATO** (ok) |
| Aggiungere regole a hook inizio sessione | MIGLIORARE_SNCP | **NON FATTO** |
| SNCP su Contabilita | roadmap.md | **NON FATTO** |
| Dashboard SNCP | roadmap.md | **FUTURO** |
| Automazione worker -> SNCP | roadmap.md | **FUTURO** |

### Da Investigare (dalla lezione)

- Verificare quali tools ha cervella-researcher
- Aggiungere logging ai salvataggi worker

---

## Idee Da Riprendere

### Alta Priorita

1. **ROADMAP_MIGLIORAMENTO_FAMIGLIA.md** - Appena creato, da eseguire
2. **BEST_PRACTICES_FAMIGLIA.md** - Appena creato, da applicare
3. **SETUP_MULTI_ACCOUNT_CLAUDE.md** - Per scalare team

### Media Priorita

4. **DASHBOARD_MIGLIORAMENTO_PIANO.md** - Per quando riprende prodotto
5. **MARKETING_VENDITA_MASTER.md** - Per quando riprende prodotto
6. **SESSIONE_DEDICATA_VIDEO_CONTENUTI.md** - Per quando riprende prodotto

### Interessanti (Future)

7. **WORKFLOW_FINALE_100_PERCENTO.md** - Workflow ideale
8. **MAPPA_APP_VERA.md** - Architettura prodotto

---

## Gaps Trovati

### 1. Cartelle Vuote o Sottoutilizzate

| Cartella | Problema |
|----------|----------|
| `idee/in_studio/` | **VUOTA** - Nessuna idea in studio |
| `idee/integrate/` | **VUOTA** - Nessuna idea marcata integrata |
| `perne/attive/` | **VUOTA** - Nessuna perna attiva |
| `perne/archivio/` | **VUOTA** - Nessuna perna archiviata |

### 2. File Obsoleti

| File | Problema |
|------|----------|
| `stato/oggi.md` | Fermo a **8 Gennaio** (2 giorni fa) |
| `futuro/roadmap.md` | Fermo a **Sessione 129** |
| `coscienza/pensieri_regina.md` | Fermo a **Sessione 129** |
| `coscienza/domande_aperte.md` | Fermo a **Sessione 129** |

### 3. Sessioni Non Loggate

- Solo 2 sessioni documentate (119, 140)
- Mancano sessioni 120-139, 141-147!

### 4. Lezioni Non Documentate

- Solo 1 lezione (agente non salva)
- Sicuramente ci sono state altre lezioni non catturate

### 5. Struttura Inconsistente

- Molte idee sono nella root di `idee/` invece che in `in_attesa/`, `in_studio/`, `integrate/`
- La convenzione naming non e sempre rispettata (IDEA_YYYYMMDD_*)

---

## Raccomandazioni

### Top 5 Azioni Immediate

#### 1. AGGIORNA FILE OBSOLETI

```
stato/oggi.md              -> aggiorna a oggi
coscienza/pensieri_regina.md -> nuove entry
coscienza/domande_aperte.md  -> review domande
futuro/roadmap.md          -> sincronizza con NORD.md
```

**Effort:** 30 min
**Impatto:** ALTO - SNCP diventa di nuovo attuale

#### 2. ORGANIZZA IDEE

Sposta le 32 idee root nelle cartelle giuste:
- Ricerche complete -> `integrate/` o archivia
- Idee parcheggiate -> `in_attesa/`
- Studi in corso -> `in_studio/`

**Effort:** 1 ora
**Impatto:** MEDIO - Struttura piu chiara

#### 3. DOCUMENTA LEZIONI MANCANTI

Dalla Sessione 141-147 sono emersi:
- Bug reviewer senza Bash
- Bug spawn-workers API vs Claude Max
- Hook protezione disattivati di proposito

Creare file in `memoria/lezioni/`

**Effort:** 45 min
**Impatto:** MEDIO - Non si perdono lezioni

#### 4. USA LE PERNE!

La feature "perne" (deviazioni temporanee) non e mai stata usata.
Quando c'e una deviazione dalla roadmap -> creare perna.

**Effort:** Ongoing
**Impatto:** BASSO - Ma utile per tracciare deviazioni

#### 5. AUTOMATIZZA AGGIORNAMENTI

Creare hook o reminder per:
- Fine sessione -> aggiorna `stato/oggi.md`
- Decisione presa -> crea file in `memoria/decisioni/`
- Lezione appresa -> crea file in `memoria/lezioni/`

**Effort:** 2 ore (script)
**Impatto:** ALTO - SNCP rimane aggiornato

---

## Top 3 Miglioramenti SNCP

### 1. SNCP VIVO, NON MORTO

**Problema:** I file non vengono aggiornati regolarmente.

**Soluzione:**
- Checkpoint automatico fine sessione
- Regina DEVE aggiornare `stato/oggi.md` prima di chiudere
- Hook che ricorda di aggiornare

### 2. STRUTTURA SEMPLIFICATA

**Problema:** Troppi livelli, non usati correttamente.

**Soluzione:**
- Rimuovere o ripensare `in_studio/`, `integrate/`
- Usare tags invece di cartelle per stato idee
- Un file `IDEE_MASTER.md` che lista tutte con status

### 3. INTEGRAZIONE CON WORKFLOW

**Problema:** SNCP e separato dal workflow quotidiano.

**Soluzione:**
- `spawn-workers` aggiorna SNCP quando finisce
- Regina legge `stato/oggi.md` a inizio sessione
- Dashboard che mostra SNCP in tempo reale

---

## Conclusione

SNCP e un'ottima idea con buona struttura base, ma:

1. **NON VIENE USATO ATTIVAMENTE** - I file sono obsoleti
2. **STRUTTURA SOTTOUTILIZZATA** - Cartelle vuote, convenzioni non seguite
3. **MANCA AUTOMAZIONE** - Dipende tutto dalla disciplina manuale

**Rating SNCP attuale:** 5/10

**Potenziale con miglioramenti:** 9/10

---

*"Qui nulla si perde... ma solo se lo aggiorniamo!"*

*Analisi completata: 10 Gennaio 2026*
