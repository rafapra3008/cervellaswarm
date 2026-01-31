# SUBROADMAP - SNCP 4.0 "Memoria Intelligente"

> **Creata:** 31 Gennaio 2026 - Sessione 322
> **Obiettivo:** Portare memoria SNCP da 8.8/10 a 9.5/10
> **Ispirazione:** OpenClaw hybrid search + daily logs pattern
> **Filosofia:** "Fatto BENE > Fatto VELOCE"

---

## VISIONE

```
+================================================================+
|   SNCP 4.0: Il meglio di SNCP + OpenClaw                        |
|                                                                  |
|   MANTENIAMO:                                                    |
|   - Trasparenza (Markdown files = source of truth)              |
|   - Sicurezza (no secrets policy)                                |
|   - Multi-progetto (progetti/bracci)                             |
|   - Git-native (version control)                                 |
|                                                                  |
|   AGGIUNGIAMO:                                                   |
|   - Daily logs auto-caricati (pattern OpenClaw)                  |
|   - Memory flush automatico (pre-compaction)                     |
|   - BM25 search (keyword ranking intelligente)                   |
|   - Embeddings opzionali (semantic search - futuro)              |
+================================================================+
```

---

## CONTESTO - Studio OpenClaw (Sessione 322)

### Cosa Fa OpenClaw (verificato da Guardiana Ricerca)

| Feature | Come Funziona |
|---------|---------------|
| Daily logs | `memory/YYYY-MM-DD.md` - carica oggi + ieri |
| Long-term | `MEMORY.md` - facts durevoli |
| Ricerca | BM25 + embeddings (sqlite-vec) |
| Flush | Turno silenzioso pre-compaction |

### SNCP vs OpenClaw - Confronto

| Aspetto | SNCP 3.0 | OpenClaw | Vantaggio |
|---------|----------|----------|-----------|
| Multi-progetto | ✅ Nativo | ❌ Single | **SNCP** |
| Sicurezza | ✅ No secrets | ❌ Vulnerabilità | **SNCP** |
| Git-native | ✅ 100% | Recommended | **SNCP** |
| Daily logs auto | ❌ Manuale | ✅ Auto | OpenClaw |
| Memory flush | ❌ Manuale | ✅ Auto | OpenClaw |
| Ricerca semantica | ❌ Grep | ✅ BM25+emb | OpenClaw |

**Conclusione:** SNCP superiore su organizzazione/sicurezza. Manca automazione.

---

## FASE 1: QUICK WINS (~2 giorni)

### QW1: Auto-load Daily Logs (2-4h)
**File:** `scripts/sncp/load-daily-memory.sh`
**Hook:** Modificare session_start per caricare oggi + ieri

```bash
# Output atteso
./scripts/sncp/load-daily-memory.sh miracollo
# → JSON con contenuto oggi + ieri (se esistono)
```

### QW2: Memory Flush Token Trigger (3-4h)
**File:** `scripts/swarm/memory-flush.sh`
**Integrazione:** spawn-workers.sh

```bash
# Trigger automatico a 75% token budget
spawn-workers --backend --with-flush
```

### QW3: SessionEnd Hook Flush (1-2h)
**File:** `hooks/session_end_flush.py`
**Azione:** Chiama memory-flush a fine sessione

### QW4: BM25 Search (4-6h)
**File:** `scripts/sncp/smart-search.py`
**Libreria:** `rank-bm25` (pure Python, no API keys)

```bash
python3 scripts/sncp/smart-search.py "SSE real-time" .sncp/progetti/miracollo/
# → File ordinati per rilevanza BM25
```

### Acceptance Criteria Fase 1

- [ ] Daily logs caricati automaticamente (oggi + ieri)
- [ ] Memory flush trigger funziona
- [ ] SessionEnd hook attivo
- [ ] BM25 search restituisce risultati ordinati

---

## FASE 2: MEMORIA STRUTTURATA (1 settimana)

### MF1: MEMORY.md Curated
**Nuovo file:** `.sncp/progetti/{progetto}/MEMORY.md`

| File | Contenuto | Lifecycle |
|------|-----------|-----------|
| PROMPT_RIPRESA | Sessioni recenti | Rolling (archivio) |
| MEMORY.md | Facts permanenti | Durabile (mai archivio) |

### MF2: Quality Scoring
**File:** `scripts/sncp/quality-check.py`

Valuta qualità PROMPT_RIPRESA:
- Actionability (next steps chiari?)
- Specificity (info concrete?)
- Freshness (aggiornato?)

---

## FASE 3: EMBEDDINGS OPZIONALI (v2.1.0)

### Quando Implementare
- Solo se progetti > 5
- Solo se ricerca > 5 secondi
- Solo se grep non basta

### Architettura Proposta
```
.sncp/progetti/{progetto}/
├── PROMPT_RIPRESA.md       # Source of truth
├── MEMORY.md               # Long-term facts
└── .embeddings/            # Cache locale (opzionale)
    ├── index.db            # SQLite con sqlite-vec
    └── metadata.json       # Config
```

### Provider Options
| Provider | Pro | Contro |
|----------|-----|--------|
| sentence-transformers | Locale, gratis | ~1GB RAM |
| OpenAI | Qualità alta | API key, costo |
| Gemini | Gratis | Rate limits |

**Raccomandazione:** Iniziare con sentence-transformers (MiniLM-L6-v2)

---

## TIMELINE

```
FASE 1 (Quick Wins) → Prossima sessione
├── QW1: Daily logs auto
├── QW2: Memory flush trigger
├── QW3: SessionEnd hook
└── QW4: BM25 search

FASE 2 (Struttura) → Settimana dopo
├── MEMORY.md template
└── Quality scoring

FASE 3 (Embeddings) → v2.1.0 (se serve)
└── Local embeddings opzionali
```

---

## DECISIONI ARCHITETTURALI

| Decisione | Motivazione |
|-----------|-------------|
| BM25 prima di embeddings | Pure Python, zero dependencies |
| MEMORY.md separato | Separation of concerns |
| Embeddings opzionali | Non tutti i progetti ne hanno bisogno |
| NO sostituzione SNCP | Trasparenza + no lock-in |

---

## SUCCESS METRICS

| Metric | Attuale | Target |
|--------|---------|--------|
| Daily logs usage | 0% (manuale) | 100% (auto) |
| Memory loss incidents | ~2/mese | 0/mese |
| Search time (100 files) | 2-5s | <500ms |
| Overall score | 8.8/10 | 9.5/10 |

---

## NON-GOALS

- NON sostituiamo SNCP con sistema proprietario
- NON richiediamo API keys per funzionalità base
- NON complichiamo workflow esistente
- NON rompiamo compatibilità SNCP 3.0

---

*"La memoria è preziosa. Trattiamola con cura."*
*Sessione 322 - Cervella & Rafa*
