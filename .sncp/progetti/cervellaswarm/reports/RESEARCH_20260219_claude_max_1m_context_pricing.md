# Ricerca: Claude MAX 20x + Context 1M Token - Pricing e Funzionamento

**Data:** 2026-02-19
**Status:** COMPLETA
**Fonti:** 14 consultate (docs ufficiali Anthropic, GitHub issues, HN, community)
**Richiesto da:** Rafa (CEO)

---

## TL;DR PER RAFA

| Domanda | Risposta |
|---------|----------|
| Il 1M context e incluso nei $200/mese? | **NO.** Tutto cio che supera 200K token viene fatturato come "extra usage" a tariffe API |
| Quanto costa extra? | Opus 4.6: **$10/MTok input + $37.50/MTok output** (2x e 1.5x delle tariffe standard) |
| Come si attiva? | `/model opus[1m]` in Claude Code (ma serve "extra usage" abilitato) |
| Vale la pena? | **SI**, per sessioni Queen/coordinamento. Una sessione lunga da 500K token costa ~$5-8 extra |
| Funziona ORA? | **BUG ATTIVO** - Issue #26428: dopo update v2.1.45 (17 Feb 2026), alcuni MAX user non vedono l'opzione |

---

## 1. Come Funziona il Billing di Claude MAX 20x

### Cosa include il piano ($200/mese)

- **20x** la capacita di utilizzo del piano Pro ($20/mese)
- Accesso a **tutti i modelli**: Opus 4.6, Sonnet 4.6, Haiku 4.5
- **Claude Code** incluso (terminal-based coding)
- **Cowork** (research preview, macOS)
- Accesso prioritario a nuovi modelli e feature
- Limiti settimanali (reset ogni 7 giorni)
- Default model: **Opus 4.6** (per MAX e Team Premium)

### Cosa significa "Billed as Extra Usage"

Quando superi i limiti inclusi nel piano MAX 20x, oppure usi feature premium come il context 1M, entri in modalita **extra usage**:

- Si passa a **tariffazione a consumo** (pay-per-token)
- Le tariffe sono quelle **standard API** di Anthropic
- Devi **pre-pagare** (aggiungere fondi) per attivarlo
- Limite di acquisto giornaliero: **$2000**
- Puoi impostare un **spending cap mensile** o "unlimited"
- Auto-reload disponibile (ricarica automatica quando il saldo scende sotto una soglia)

**Come abilitarlo:**
1. Vai a `claude.ai/settings/usage`
2. Attiva "Extra Usage"
3. Aggiungi fondi (crediti prepagati)
4. Opzionale: configura auto-reload

### Promo attiva (Feb 2026)

Anthropic ha regalato **$50 di crediti extra usage** a tutti gli utenti Pro e Max iscritti prima del 4 Feb 2026. Rafa dovrebbe averli disponibili su `claude.ai/settings/usage`.

---

## 2. `/model opus[1m]` - Come Funziona

### Comandi disponibili in Claude Code

```bash
# Attiva Opus con context 1M
/model opus[1m]

# Oppure con nome completo
/model claude-opus-4-6[1m]

# Sonnet con context 1M (piu economico)
/model sonnet[1m]

# Sonnet completo
/model claude-sonnet-4-6[1m]
```

### Meccanismo di billing

**PUNTO CRUCIALE:** Selezionare un modello `[1m]` **NON cambia immediatamente il billing**. Ecco come funziona:

1. **0-200K token di input**: tariffe standard (incluse nel piano MAX)
2. **Oltre 200K token di input**: tariffe premium long-context (extra usage)

Quindi puoi usare `opus[1m]` e per la prima parte della sessione (finche stai sotto 200K) non paghi extra. Solo quando il contesto supera 200K, scattano le tariffe premium.

### Chi puo usarlo

| Tipo utente | Accesso 1M | Note |
|------------|-----------|------|
| API pay-as-you-go (Tier 4) | Pieno accesso | Nessun piano richiesto |
| MAX 20x ($200/mese) | Con extra usage abilitato | Serve prepagare crediti |
| MAX 5x ($100/mese) | Con extra usage abilitato | Serve prepagare crediti |
| Pro ($20/mese) | Con extra usage abilitato | Serve prepagare crediti |

---

## 3. Pricing Dettagliato: Standard vs Long-Context vs Fast Mode

### Opus 4.6 - Tutte le Tariffe

| Modalita | Input ($/MTok) | Output ($/MTok) | Moltiplicatore |
|----------|---------------|-----------------|----------------|
| **Standard** (<=200K input) | $5 | $25 | 1x (base) |
| **Long-context** (>200K input) | $10 | $37.50 | 2x input, 1.5x output |
| **Fast mode** (<=200K) | $30 | $150 | 6x (base) |
| **Fast mode** (>200K) | $60 | $225 | 6x + long-context |
| **Batch** (asincrono) | $2.50 | $12.50 | 0.5x (sconto 50%) |
| **Cache read** | $0.50 | - | 0.1x (sconto 90%) |
| **Cache write 5min** | $6.25 | - | 1.25x |

### Sonnet 4.6 - Alternativa Economica

| Modalita | Input ($/MTok) | Output ($/MTok) |
|----------|---------------|-----------------|
| **Standard** (<=200K) | $3 | $15 |
| **Long-context** (>200K) | $6 | $22.50 |

### Stima Costi per Sessione Tipica

| Scenario | Token Input | Token Output | Costo Stimato |
|----------|------------|-------------|---------------|
| Sessione normale (200K) | 200K | 20K | ~$1.50 (incluso nel MAX) |
| Sessione lunga (400K) Opus | 400K | 40K | ~$5.50 extra |
| Sessione lunga (400K) Sonnet | 400K | 40K | ~$3.30 extra |
| Sessione massima (800K) Opus | 800K | 50K | ~$9.88 extra |
| Sessione massima (800K) Sonnet | 800K | 50K | ~$5.93 extra |
| Full 1M Opus | 1M | 60K | ~$12.25 extra |
| Full 1M Sonnet | 1M | 60K | ~$7.35 extra |

**NOTA:** Il prompt caching riduce significativamente questi costi. Cache read costa solo $0.50/MTok per Opus (vs $10 long-context), quindi sessioni che riutilizzano contesto pagano molto meno.

---

## 4. Context Standard (200K) vs 1M: Differenza Pratica

### Quando 200K Basta

- Sessioni di sviluppo su singolo modulo/package
- Bug fix mirati
- Code review di file specifici
- La maggior parte del lavoro quotidiano con CervellaSwarm

### Quando Serve 1M

- **Queen agent che coordina 17 agenti**: leggere contesto di tutto il progetto
- **Refactoring cross-modulo**: capire dipendenze tra tutti i 7 packages
- **Sessioni di architettura**: avere tutta la codebase in contesto
- **Analisi di codebase enterprise** con 200K+ token solo di sorgenti
- **Audit di sicurezza** su tutto il repo

### CervellaSwarm - Analisi Specifica

Il nostro repo ha:
- 7 packages (~1.8K LOC Python ciascuno in media)
- 1265+ test
- 17 agenti con DNA/frontmatter
- Docs, roadmap, SNCP

Stima token totali della codebase: **probabilmente 150-300K token**. Quindi:
- Per lavoro su 1-2 packages: 200K basta
- Per visione completa repo + coordinamento agenti: 1M utile
- Per Queen con PROMPT_RIPRESA + NORD + tutti i packages in contesto: **1M raccomandato**

### Autocompact vs 1M

Ricorda che Claude Code ha **autocompact** (buffer 33K, compaction automatica). Con 200K, le sessioni lunghe compattano e perdono dettagli. Con 1M, puoi lavorare molto piu a lungo senza compaction, mantenendo piu contesto fresco.

---

## 5. Come Attivare opus[1m] - Passi Esatti

### Prerequisiti

1. Piano **Claude MAX** attivo ($100 o $200/mese) -- Rafa ha MAX 20x, OK
2. **Extra usage** abilitato
3. **Crediti prepagati** nel conto

### Step-by-Step

```
STEP 1: Abilita Extra Usage
   -> Vai a https://claude.ai/settings/usage
   -> Attiva "Extra Usage" (toggle)
   -> Se vedi banner "$50 credits" -> clicca "Claim"

STEP 2: Aggiungi Fondi (se necessario)
   -> Stessa pagina, clicca "Add funds"
   -> Suggerimento: $20-50 per iniziare
   -> Opzionale: abilita auto-reload

STEP 3: Aggiorna Claude Code
   -> Nel terminal: claude update
   -> Verifica versione: claude --version
   -> ATTENZIONE: v2.1.45 ha bug (vedi sezione bug)

STEP 4: Attiva 1M Context
   -> Dentro Claude Code: /model opus[1m]
   -> Oppure al lancio: claude --model opus[1m]
   -> Verifica con: /status

STEP 5: Monitora Costi
   -> /cost per vedere consumo sessione
   -> /stats per pattern di utilizzo
```

### BUG ATTIVO (Feb 2026)

**Issue GitHub #26428**: Dopo l'update a v2.1.45 (rilasciato con Sonnet 4.6 il 17 Feb 2026), l'opzione `[1m]` restituisce errore "not available for your account" per alcuni utenti MAX.

**Workaround temporaneo:**
```bash
# Usa versione precedente
CLAUDE_CODE_VERSION=2.1.44 claude

# Oppure prova il modello specifico
/model claude-sonnet-4-5-20250929[1m]
```

Issues correlate: #23905 (Opus 1m rejected), #23700 (Long context unavailable MAX plan)

---

## 6. Raccomandazione per Rafa

### Azione Immediata

1. **Vai a claude.ai/settings/usage** e abilita Extra Usage
2. **Reclama i $50 di credito** promozionale (se non ancora fatto)
3. **NON aggiungere altri fondi** finche non testi con i $50 gratis
4. **Testa** `/model opus[1m]` - se da errore, usa workaround v2.1.44

### Strategia di Utilizzo Raccomandata

| Situazione | Modello |
|------------|---------|
| Lavoro quotidiano normale | `opus` (standard 200K, incluso nel MAX) |
| Sessione Queen/coordinamento lungo | `opus[1m]` (extra usage) |
| Task di sviluppo estesi ma non critici | `sonnet[1m]` (meta prezzo di Opus) |
| Bug fix rapidi / task semplici | `sonnet` o `haiku` (incluso nel MAX) |
| Pianificazione + esecuzione | `opusplan` (Opus per piano, Sonnet per esecuzione) |

### Budget Stimato Mensile Extra

Se usi 1M context ~3-4 volte a settimana per sessioni da 400-600K token:
- Con Opus: **~$20-35/mese extra** (sopra i $200 del MAX)
- Con Sonnet: **~$12-20/mese extra**
- Con prompt caching attivo: **30-50% in meno**

**Verdetto:** Per un CEO/team lead che coordina uno swarm di 17 agenti, il costo extra e ragionevole. $50 di crediti gratis coprono 1-2 settimane di test.

---

## Fonti Consultate

1. Anthropic Pricing Docs - platform.claude.com/docs/en/about-claude/pricing
2. Claude Code Model Config - code.claude.com/docs/en/model-config
3. Claude Code Costs - code.claude.com/docs/en/costs
4. Extra Usage Help - support.claude.com/en/articles/12429409
5. MAX Plan Help - support.claude.com/en/articles/11049741
6. Context Windows Docs - platform.claude.com/docs/en/build-with-claude/context-windows
7. GitHub Issue #26428 - sonnet[1m] regression v2.1.45
8. GitHub Issue #23905 - Opus 1m rejected on MAX
9. Hacker News #46902427 - Opus 4.6 1M context discussion
10. Hacker News #46904569 - Extra usage promo discussion
11. XDA Developers - $50 free credits announcement
12. Cat Wu (Anthropic) X post - Extra usage promo instructions
13. IntuitionLabs - MAX plan analysis
14. Northflank - Claude Code rate limits and pricing
