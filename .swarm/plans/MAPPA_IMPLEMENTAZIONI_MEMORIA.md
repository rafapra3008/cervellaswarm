# Mappa Implementazioni Memoria SNCP 3.0

**Data analisi:** 29 Gennaio 2026
**Analista:** Cervella Ingegnera
**Input:** Studio Moltbot Memory + SNCP 2.0 esistente

---

## Executive Summary

**STATUS SNCP 2.0:**
- ✅ File-based (Markdown) - OTTIMO!
- ✅ Project isolation (progetti/) - MEGLIO di Moltbot!
- ✅ Git-tracked, no secrets exposure - SICURO!
- ✅ Hooks automatici (pre-commit, session start/end) - AVANZATO!
- ⚠️ Mancano: Auto memory flush, temporal logs, security audit automatico

**COSA IMPLEMENTARE:**
3 Quick Wins + 4 Miglioramenti Medi + 2 Evoluzioni Future + 3 DA NON FARE

**PRIORITA:** Security audit (HIGH), Auto memory flush (HIGH), Daily logs (MEDIUM)

---

## 1. QUICK WINS (Implementabili Subito)

### QW1: Security Audit Script ⚡ HIGH

**GAP:** Moltbot ha problemi gravi con plaintext secrets in MEMORY.md. SNCP non ha audit automatico.

**IMPLEMENTAZIONE:**
```bash
scripts/sncp/audit-secrets.sh
  → Scansiona PROMPT_RIPRESA_*.md per pattern sospetti
  → Pattern: API_KEY, password, token, secret, credential
  → Ritorna: lista file con potenziali segreti + linea
  → Integrato in pre-commit hook
```

**FILE DA CREARE:**
- `scripts/sncp/audit-secrets.sh`

**FILE DA MODIFICARE:**
- `scripts/hooks/pre-commit` (aggiungere chiamata ad audit-secrets)

**EFFORT:** S (2-3 ore)

**PRIORITA:** HIGH - Security è non-negoziabile!

**DIPENDENZE:** Nessuna

**ESEMPIO OUTPUT:**
```
⚠️  Possibile secret trovato:
    File: .sncp/progetti/miracollo/PROMPT_RIPRESA_miracollo.md
    Linea 42: "API_KEY=sk-1234abcd..."
    AZIONE: Rimuovere e usare .env!
```

---

### QW2: PROMPT_RIPRESA Size Monitor ⚡ MEDIUM

**GAP:** Hook pre-commit verifica limiti (150 righe), ma non avvisa PRIMA che l'utente committi.

**IMPLEMENTAZIONE:**
```bash
scripts/sncp/check-ripresa-size.sh [progetto]
  → Legge PROMPT_RIPRESA_{progetto}.md
  → Se > 120 righe (80%): WARNING
  → Se > 150 righe: ERROR + suggerisce archiviazione
  → Chiamato da Cervella PRIMA di checkpoint
```

**FILE DA CREARE:**
- `scripts/sncp/check-ripresa-size.sh`

**FILE DA MODIFICARE:**
- Hook `session_start_swarm.py` (mostra warning se vicino al limite)

**EFFORT:** S (1-2 ore)

**PRIORITA:** MEDIUM - Previene problemi, non blocca lavoro

**DIPENDENZE:** Nessuna

**ESEMPIO OUTPUT:**
```
📊 PROMPT_RIPRESA Status:
    cervellaswarm: 88/150 righe (59%) ✅
    miracollo: 74/150 righe (49%) ✅
    saasexplorer: 126/150 righe (84%) ⚠️  VICINO AL LIMITE!
    
    AZIONE: Archivia sessioni vecchie di saasexplorer!
```

---

### QW3: Memory Stats Dashboard ⚡ LOW

**GAP:** Non abbiamo visibilità su trend crescita memoria (utile per capire quando archiviare).

**IMPLEMENTAZIONE:**
```bash
scripts/sncp/memory-stats.sh
  → Conta righe PROMPT_RIPRESA_*.md
  → Conta file in archivio/
  → Mostra trend (usa git log per vedere crescita)
  → Output: tabella + grafico ASCII opzionale
```

**FILE DA CREARE:**
- `scripts/sncp/memory-stats.sh`

**FILE DA MODIFICARE:**
- Nessuno (standalone script)

**EFFORT:** S (2-3 ore)

**PRIORITA:** LOW - Nice to have, non critico

**DIPENDENZE:** Nessuna

**ESEMPIO OUTPUT:**
```
📈 Memory Growth Trend (last 7 days)

Progetto       | Righe Oggi | Δ 7gg | Archivi | Health
---------------|------------|-------|---------|--------
cervellaswarm  | 88         | +12   | 15      | ✅
miracollo      | 74         | +8    | 22      | ✅
saasexplorer   | 126        | +34   | 3       | ⚠️  Crescita rapida!
```

---

## 2. MIGLIORAMENTI MEDI (1-2 Giorni)

### MM1: Auto Memory Flush ⚡ HIGH

**GAP:** Moltbot fa auto-flush PRIMA di context compaction (silent turn). SNCP si basa su checkpoint manuali.

**COSA FA MOLTBOT:**
```javascript
if (tokens > context_limit - 4000) {
  // Silent agentic turn
  model.respond("Write durable memories to MEMORY.md");
  // NO_REPLY (invisibile all'utente)
}
```

**IMPLEMENTAZIONE SNCP:**
```bash
scripts/swarm/memory-flush.sh [worker_name]
  
  1. Detecta context usage (via API? o timer?)
  2. Quando vicino al limite (es: dopo 20 min sessione):
     - Scrive summary sessione in PROMPT_RIPRESA
     - Aggiorna stato.md con decisioni chiave
  3. Silent (no output user)
  4. Log in .swarm/logs/memory_flush.log
```

**ALTERNATIVA PRAGMATICA (più facile):**
```bash
spawn-workers.sh
  → Dopo 30 minuti di lavoro worker:
     - Automaticamente chiama memory-flush.sh
     - Worker scrive summary in .swarm/handoff/
     - Regina legge handoff al termine
```

**FILE DA CREARE:**
- `scripts/swarm/memory-flush.sh`

**FILE DA MODIFICARE:**
- `scripts/swarm/spawn-workers.sh` (aggiungere timer/trigger)
- Hook `session_end_swarm.py` (flush automatico pre-close)

**EFFORT:** M (4-6 ore) - Richiede integrazione con workflow worker

**PRIORITA:** HIGH - Previene perdita memoria in sessioni lunghe!

**DIPENDENZE:** Nessuna tecnica, ma va testato con workers reali

**NOTA:** Implementazione PRAGMATICA preferibile a quella "smart" (no API usage detection).

---

### MM2: Daily Logs (Temporal Organization) ⚡ MEDIUM

**GAP:** SNCP usa handoff/ (session-based). Moltbot usa `memoria/YYYY-MM-DD.md` (temporal).

**BENEFICIO:** Più facile rispondere "cosa abbiamo fatto il 15 Gennaio?" vs "cosa c'era nella sessione 302?"

**IMPLEMENTAZIONE:**
```
.sncp/progetti/{progetto}/
├── PROMPT_RIPRESA_{progetto}.md   # Long-term curated
├── stato.md                        # Current status
└── memoria/
    ├── 2026-01-29.md               # Today's log (auto-generato)
    ├── 2026-01-28.md               # Yesterday
    └── 2026-01/                    # Archivio mensile
        ├── 2026-01-15.md
        └── ...
```

**Daily log contiene:**
- Sessioni del giorno (link a handoff se esistono)
- Decisioni prese
- Sprint completati
- Link a file modificati (git log)

**SCRIPT:**
```bash
scripts/sncp/daily-log.sh [progetto] "note"
  → Appende nota a .sncp/progetti/{progetto}/memoria/YYYY-MM-DD.md
  → Crea file se non esiste (con template)
  → Chiamato da checkpoint
```

**FILE DA CREARE:**
- `scripts/sncp/daily-log.sh`
- Template: `templates/DAILY_LOG_TEMPLATE.md`

**FILE DA MODIFICARE:**
- Hook `session_end_swarm.py` (chiamare daily-log.sh)

**EFFORT:** M (5-7 ore) - Include template, script, integrazione

**PRIORITA:** MEDIUM - Nice to have, migliora organizzazione

**DIPENDENZE:** Nessuna

**NOTA:** Esperimento da fare SU CERVELLASWARM prima di estendere a tutti progetti!

---

### MM3: PROMPT_RIPRESA Auto-Archiver ⚡ MEDIUM

**GAP:** Archiviazione è manuale. Potremmo automatizzare quando PROMPT_RIPRESA > 150 righe.

**IMPLEMENTAZIONE:**
```bash
scripts/sncp/auto-archive.sh [progetto]
  
  1. Legge PROMPT_RIPRESA_{progetto}.md
  2. Se > 150 righe:
     - Estrae sezioni "vecchie" (es: sprint completati > 30gg fa)
     - Sposta in archivio/YYYY-MM/
     - Mantiene in PROMPT_RIPRESA solo "recente"
  3. Commit automatico: "Auto-archive: {progetto} PROMPT_RIPRESA"
```

**LOGICA "VECCHIO":**
- Sprint DONE da > 30 giorni
- Decisioni superate da nuove
- File modificati > 60 giorni fa

**FILE DA CREARE:**
- `scripts/sncp/auto-archive.sh`

**FILE DA MODIFICARE:**
- Hook `pre-commit` (suggerisce auto-archive se > 140 righe)

**EFFORT:** M (6-8 ore) - Logica "vecchio" complessa, richiede parsing Markdown

**PRIORITA:** MEDIUM - Riduce lavoro manuale

**DIPENDENZE:** Nessuna

**RISCHIO:** Potrebbe rimuovere cose importanti! → Serve review manuale prima di commit.

---

### MM4: Cross-Project Memory Search ⚡ LOW

**GAP:** Non possiamo cercare "quando abbiamo discusso di X?" cross-progetto.

**IMPLEMENTAZIONE:**
```bash
scripts/sncp/search-memory.sh "query"
  
  → Cerca in TUTTI i PROMPT_RIPRESA_*.md + archivio/
  → Output: lista risultati con context
  → Opzionale: usa grep con context (-C 3)
```

**FILE DA CREARE:**
- `scripts/sncp/search-memory.sh`

**EFFORT:** M (3-4 ore) - Script semplice, ma output va formattato bene

**PRIORITA:** LOW - Nice to have

**DIPENDENZE:** Nessuna

**ESEMPIO OUTPUT:**
```
🔍 Searching for "Ericsoft"...

Found 3 results:

1️⃣  miracollo/PROMPT_RIPRESA_miracollo.md (L42):
    "Decisione: Ericsoft Integration via PMS Core Connector"
    Context: Sprint S318 - Architettura connettori esterni

2️⃣  miracollo/archivio/2026-01/sessione_270.md (L18):
    "Ericsoft DB ha 15 tabelle, mappiamo a Room Types"
    
3️⃣  miracollo/ricerche/RICERCA_DB_ERICSOFT.md (L1):
    "Studio schema Ericsoft per integrazione..."
```

---

## 3. EVOLUZIONI FUTURE (Settimane)

### EF1: Optional RAG Layer (quando SNCP > 100 progetti)

**QUANDO:** Solo se cresciamo OLTRE 100 progetti attivi o utenti richiedono "trova quando abbiamo discusso X".

**ARCHITETTURA:**
```
PROMPT_RIPRESA_*.md (plaintext - source of truth)
       ↓
   Embedding script (nightly cron)
       ↓
PostgreSQL + pgvector (semantic search)
       ↓
scripts/sncp/semantic-search.sh "query"
```

**NON SOSTITUISCE file Markdown!** File = source of truth, vector = acceleratore.

**EFFORT:** L (2-3 settimane) - Infrastruttura DB, embedding pipeline, testing

**PRIORITA:** FUTURE - Solo se necessario

**DIPENDENZE:** PostgreSQL, pgvector, OpenAI/local embeddings

---

### EF2: Multi-Agent Shared Memory

**GAP:** Oggi ogni worker ha memoria isolata (handoff/). Potrebbero servire decisioni condivise.

**USE CASE:**
- Backend decide "usiamo JWT per auth"
- Frontend deve saperlo per implementare login
- Oggi: passa via handoff/ o PROMPT_RIPRESA

**PROPOSTA:**
```
.swarm/shared_memory/
├── decisions/
│   └── auth_strategy.md  # "Decisione team: JWT"
├── patterns/
│   └── error_handling.md # "Pattern condiviso: sempre try/catch"
└── conventions/
    └── naming.md         # "Variabili: camelCase"
```

**SCRIPT:**
```bash
scripts/swarm/shared-decision.sh "topic" "decision"
  → Scrive in .swarm/shared_memory/decisions/
  → Notifica workers attivi (via .swarm/status/)
```

**EFFORT:** L (1-2 settimane) - Richiede workflow coordination

**PRIORITA:** FUTURE - Solo se coordiniamo 5+ workers simultanei

**DIPENDENZE:** Protocolli comunicazione swarm maturi

---

## 4. DA NON FARE (Lessons from Moltbot Mistakes)

### ❌ DNF1: Plaintext Secrets in Memory Files

**PROBLEMA MOLTBOT:** Scrive API keys, passwords in `MEMORY.md` → malware target.

**REGOLA SNCP:** MAI scrivere segreti in PROMPT_RIPRESA o stato.md!

**COME PREVENIRE:**
1. Security audit script (QW1) scansiona automaticamente
2. Pre-commit hook BLOCCA se trova pattern sospetti
3. Educazione workers: "Segreti vanno in .env, MAI in memoria!"

**GIA' IMPLEMENTATO:** Parzialmente (pre-commit verifica file), ma serve audit specifico.

---

### ❌ DNF2: Manual Memory Prompts (User-Driven)

**PROBLEMA MOLTBOT:** Utente deve ricordare all'agent "salva questo in memoria!"

**APPROCCIO SNCP (MIGLIORE):** Automation-first!
- Checkpoint automatici ogni fine sessione
- Hooks salvano stato senza input utente
- Memory flush automatico (MM1) quando necessario

**DECISIONE:** Continuare con automation, NON copiare approccio manuale Moltbot.

---

### ❌ DNF3: Single Workspace (No Project Isolation)

**PROBLEMA MOLTBOT:** `~/clawd/` unico workspace → mix progetti diversi.

**APPROCCIO SNCP (MIGLIORE):** `.sncp/progetti/` con isolation!
- Miracollo, Contabilita, CervellaSwarm separati
- Bracci (pms-core, miracollook, room-hardware) isolati
- Cross-contamination impossibile

**DECISIONE:** Mantenere struttura gerarchica SNCP, NON semplificare a flat workspace.

---

## 5. ROADMAP IMPLEMENTAZIONE

### Fase 1: Security (Week 1)
```
[x] QW1: Security audit script      (2-3h, HIGH)
[x] Pre-commit integration           (1h)
[ ] Test su tutti progetti           (1h)
```

### Fase 2: Memory Monitoring (Week 1-2)
```
[ ] QW2: PROMPT_RIPRESA size monitor (1-2h, MEDIUM)
[ ] QW3: Memory stats dashboard      (2-3h, LOW)
[ ] MM1: Auto memory flush           (4-6h, HIGH)
```

### Fase 3: Temporal Organization (Week 2-3)
```
[ ] MM2: Daily logs experiment       (5-7h, MEDIUM)
    - Testare SU cervellaswarm 1 settimana
    - Se funziona → estendere a miracollo
[ ] MM4: Cross-project search        (3-4h, LOW)
```

### Fase 4: Automation (Week 3-4)
```
[ ] MM3: Auto-archiver               (6-8h, MEDIUM)
    - Con review manuale obbligatoria!
```

### Fase 5: Future (Solo se necessario)
```
[ ] EF1: RAG layer                   (2-3w, quando > 100 progetti)
[ ] EF2: Multi-agent shared memory   (1-2w, quando > 5 workers simultanei)
```

---

## 6. FILE INVENTORY

### File da CREARE:

| File | Fase | Effort |
|------|------|--------|
| `scripts/sncp/audit-secrets.sh` | 1 | S |
| `scripts/sncp/check-ripresa-size.sh` | 2 | S |
| `scripts/sncp/memory-stats.sh` | 2 | S |
| `scripts/swarm/memory-flush.sh` | 2 | M |
| `scripts/sncp/daily-log.sh` | 3 | M |
| `templates/DAILY_LOG_TEMPLATE.md` | 3 | S |
| `scripts/sncp/auto-archive.sh` | 4 | M |
| `scripts/sncp/search-memory.sh` | 3 | M |

### File da MODIFICARE:

| File | Modifica | Fase |
|------|----------|------|
| `scripts/hooks/pre-commit` | Aggiungere audit-secrets check | 1 |
| `scripts/hooks/session_start_swarm.py` | Mostrare size warning | 2 |
| `scripts/hooks/session_end_swarm.py` | Auto memory flush + daily log | 2-3 |
| `scripts/swarm/spawn-workers.sh` | Timer per memory flush | 2 |

---

## 7. SUCCESS CRITERIA

### Fase 1 (Security):
- ✅ Pre-commit BLOCCA se trova "API_KEY=" in PROMPT_RIPRESA
- ✅ Scan completo progetti OK (zero segreti trovati)

### Fase 2 (Monitoring):
- ✅ Warning quando PROMPT_RIPRESA > 120 righe
- ✅ Memory flush automatico testato con 1 worker (30+ min sessione)

### Fase 3 (Temporal):
- ✅ Daily logs creati automaticamente per 1 settimana
- ✅ Facile rispondere "cosa abbiamo fatto il 22 Gennaio?"

### Fase 4 (Automation):
- ✅ Auto-archiver suggerisce cosa spostare (con review manuale)
- ✅ PROMPT_RIPRESA rimane < 150 righe senza intervento manuale

---

## 8. METRICHE DI SUCCESSO

| Metrica | Baseline (oggi) | Target (post-implementazione) |
|---------|-----------------|-------------------------------|
| Segreti in PROMPT_RIPRESA | 0 (manuale) | 0 (verificato automaticamente) |
| PROMPT_RIPRESA > 150 righe | Blocco pre-commit | Warning prima + auto-archiver |
| Memoria persa in sessioni lunghe | Rischio | Auto-flush previene |
| Tempo per trovare "cosa fatto il X?" | 5-10 min (grep manuale) | < 1 min (daily logs) |
| Archiviazione manuale | Ogni 2-3 settimane | Automatica (review 5 min) |

---

## 9. RISCHI E MITIGAZIONI

| Rischio | Probabilità | Impatto | Mitigazione |
|---------|-------------|---------|-------------|
| Auto-archiver rimuove decisioni importanti | MEDIUM | HIGH | Review manuale obbligatoria + dry-run mode |
| Memory flush interrompe workflow worker | LOW | MEDIUM | Timer conservativo (30 min), log dettagliato |
| Daily logs crescono indefinitamente | HIGH | LOW | Archivio mensile automatico |
| Security audit falsi positivi | MEDIUM | LOW | Pattern list configurabile |
| RAG layer troppo complesso | LOW | HIGH | Implementare SOLO se > 100 progetti |

---

## 10. CONCLUSIONI

### SNCP 2.0 è GIA' ECCELLENTE!

**Punti di forza vs Moltbot:**
- ✅ Project isolation (progetti/)
- ✅ No security issues (no plaintext secrets)
- ✅ Automation-first (hooks)
- ✅ Git-native (version control memoria)

**Cosa possiamo migliorare (da Moltbot):**
1. Auto memory flush (preventivo)
2. Daily logs (temporal organization)
3. Security audit automatico (paranoia sana!)

**Cosa NON copiare:**
1. Manual memory prompts (automation > manual)
2. Plaintext secrets (security nightmare)
3. Flat workspace (isolation matters)

### Prossimi Step Raccomandati:

**Immediate (questa settimana):**
1. QW1: Security audit script
2. MM1: Auto memory flush (prototype)

**Short-term (prossime 2 settimane):**
3. MM2: Daily logs experiment (CervellaSwarm only)
4. QW2: Size monitor

**Long-term (solo se necessario):**
5. EF1: RAG layer (quando > 100 progetti)

### Filosofia SNCP 3.0:

```
"File Markdown = Source of Truth"
"Automation > Manual Intervention"
"Security First, Always"
"Simple Until Proven Necessary"
```

**Moltbot ci ha insegnato:** La semplicità (plaintext files) è potente, MA serve disciplina (security, automation).

**SNCP ha già la disciplina.** Ora aggiungiamo le best practices temporali (daily logs, auto-flush).

---

**Fine Analisi**

*Cervella Ingegnera*
*29 Gennaio 2026*

*"Il progetto si MIGLIORA da solo quando lo analizziamo!"*
