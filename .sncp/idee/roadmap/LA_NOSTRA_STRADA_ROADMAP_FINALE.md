# LA NOSTRA STRADA - Roadmap Finale

> **Data:** 9 Gennaio 2026
> **Sessione:** 134
> **Stato:** PIANIFICATA E VALIDATA
> **Validazione:** 2x Guardiana Qualita'

---

## LA VISIONE

```
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   "MINIMO in memoria, MASSIMO su disco"                         ║
║                                                                  ║
║   Context ottimizzato + Worker paralleli = Famiglia POTENTE     ║
║                                                                  ║
║   Non copiamo Boris 1:1.                                        ║
║   Prendiamo il MEGLIO e lo adattiamo a NOI.                     ║
║                                                                  ║
║   La differenza? NOI abbiamo la REGINA che coordina!            ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## OBIETTIVI MISURABILI

| Metrica | PRIMA | DOPO | Miglioramento |
|---------|-------|------|---------------|
| Token startup | 22-25K | 8-10K | **-60%** |
| % context iniziale | 11-12% | 4-5% | **-60%** |
| Durata sessione | X ore | 2-3X ore | **+200%** |
| Worker paralleli | 0-1 | 2-3 | **+200%** |

---

## L'ARCHITETTURA FINALE

```
                    ┌─────────────────────────────────────┐
                    │         👑 REGINA (Opus)            │
                    │   Context SNELLO + SNCP memoria     │
                    └─────────────────────────────────────┘
                                      │
                    ┌─────────────────┼─────────────────┐
                    │                 │                 │
                    ▼                 ▼                 ▼
            ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
            │ Task Tool   │   │ Worker A    │   │ Worker B    │
            │ (interno)   │   │ (clone)     │   │ (clone)     │
            │ < 5 min     │   │ > 5 min     │   │ > 5 min     │
            └─────────────┘   └─────────────┘   └─────────────┘
                    │                 │                 │
                    ▼                 ▼                 ▼
            ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
            │ Risultato   │   │  .done +    │   │  .done +    │
            │ immediato   │   │  Watcher    │   │  Watcher    │
            └─────────────┘   └─────────────┘   └─────────────┘
```

---

## LE REGOLE D'ORO

### Regola 1: Task Tool vs Spawn

```
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   TASK TOOL INTERNO quando:                                     ║
║   • Task < 5 minuti                                             ║
║   • Read/Grep/Analisi veloce                                    ║
║   • Output piccolo (< 500 token)                                ║
║   • Non modifica file                                           ║
║                                                                  ║
║   WORKER ESTERNO quando:                                        ║
║   • Task > 5 minuti                                             ║
║   • Modifica codice                                             ║
║   • Output grande                                               ║
║   • Task che potrebbe "espandersi"                              ║
║                                                                  ║
║   ⚠️  ATTENZIONE: Se Regina compatta, subagent PERDE lavoro!    ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

### Regola 2: Massimo 2-3 Worker

```
NON scalare prima che la base funzioni al 100%!

2-3 worker = gestibili con watcher + SNCP
4+ worker = richiede automazione sofisticata che NON abbiamo

PRIMA stabilizzare 2-3, POI (forse) scalare.
```

### Regola 3: SNCP e' la Memoria

```
MENTRE lavoro → scrivo su .sncp/
Fine sessione → sintesi in PROMPT_RIPRESA
Git commit → salva tutto

Il disco e' infinito. Il context no.
```

### Regola 4: CLAUDE.md Snello

```
COSA (conciso) → CLAUDE.md (sempre caricato)
COME (dettagli) → file esterni (letti quando serve)

Target: -60% token startup
```

---

## FASE 1: CONTEXT OPTIMIZATION

**Obiettivo:** Ridurre startup da 22-25K a 8-10K token

| Step | Task | Rischio | Priorita' |
|------|------|---------|-----------|
| 1.1 | CLAUDE.md progetto snello (40 linee) | Basso | Alta |
| 1.2 | Benchmark before/after con /context | - | Alta |
| 1.3 | PROMPT_RIPRESA snello (80 linee) | Medio | Alta |
| 1.4 | Formato "Decisioni Chiave" | Basso | Media |
| 1.5 | CLAUDE.md globale snello (180 linee) | Alto | Media |
| 1.6 | Test qualitativo (identita' ok?) | Critico | Alta |

**NON FARE:**
- NON toccare COSTITUZIONE.md
- NON rimuovere identita' da CLAUDE.md
- NON applicare tutto insieme

---

## FASE 2: WORKER PARALLELI STABILI

**Obiettivo:** 2-3 worker che funzionano SEMPRE

| Step | Task | Rischio | Priorita' |
|------|------|---------|-----------|
| 2.1 | Documentare Pattern Boris in CLAUDE.md | Basso | Alta |
| 2.2 | Testare watcher-regina affidabilita' | Medio | Alta |
| 2.3 | Template task per worker | Basso | Media |
| 2.4 | Workflow .done → notifica → verifica | Medio | Alta |

**Clones Esistenti:**
- `~/Developer/CervellaSwarm-regina-A`
- `~/Developer/CervellaSwarm-regina-B`

---

## FASE 3: WORKFLOW OTTIMIZZATO

**Obiettivo:** Nuovo modo di lavorare context-smart

### Inizio Sessione (NUOVO)
```
1. Startup leggero (~8-10K token)
2. Leggo solo essenziale
3. SNCP per dettagli se serve
```

### Durante Sessione (NUOVO)
```
1. Scrivo su .sncp/ mentre lavoro
2. Commit frequenti (git = memoria)
3. Task tool per query veloci
4. Spawn worker per lavoro pesante
5. Watcher notifica quando .done
```

### Checkpoint (NUOVO)
```
A 70-80% context:
1. Aggiorno PROMPT_RIPRESA (80 linee MAX)
2. git commit
3. Posso fare /clear se serve
```

### Chiusura Sessione (NUOVO)
```
1. PROMPT_RIPRESA finale (compatto!)
2. git push
3. NIENTE narrativa lunga nel context
```

---

## COSA NON FARE (Lista Rossa)

```
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   ❌ NON aggiungere GitButler (troppa complessita')             ║
║   ❌ NON aggiungere ccswitch (non ora)                          ║
║   ❌ NON scalare oltre 3 worker (prima stabilizzare)            ║
║   ❌ NON toccare COSTITUZIONE.md                                ║
║   ❌ NON rimuovere identita' da CLAUDE.md                       ║
║   ❌ NON creare SESSION_STATE.md (usare PROMPT_RIPRESA)         ║
║   ❌ NON applicare tutto insieme (incrementale!)                ║
║   ❌ NON testare prima su Miracollo (CervellaSwarm prima)       ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## TIMELINE SUGGERITA

```
SESSIONE 134 (oggi):
├── ✅ Ricerca completata
├── ✅ Validazione Guardiana (2x)
├── ✅ Roadmap documentata
└── [ ] Commit tutto in git

SESSIONI 135-136:
├── [ ] CLAUDE.md progetto snello
├── [ ] Benchmark context
└── [ ] Test worker paralleli

SESSIONI 137-140:
├── [ ] PROMPT_RIPRESA snello
├── [ ] CLAUDE.md globale snello
└── [ ] Test qualitativo completo

DOPO (1+ settimana):
├── [ ] Stabilizzare tutto
├── [ ] Valutare se scalare worker
└── [ ] Portare su Miracollo
```

---

## FILE CREATI IN QUESTA SESSIONE

| File | Contenuto |
|------|-----------|
| `.sncp/idee/CONTEXT_OPTIMIZATION_RESEARCH.md` | Ricerca context |
| `.sncp/idee/GUARDIANA_REVIEW_CONTEXT_OPT.md` | Prima review Guardiana |
| `.sncp/idee/ROADMAP_CONTEXT_OPTIMIZATION.md` | Prima roadmap |
| `.sncp/memoria/decisioni/DECISIONI_CONTEXT_OPTIMIZATION_20260109.md` | Decisioni prese |
| `.sncp/idee/RICERCA_BORIS_MULTI_SESSIONE.md` | Ricerca Boris |
| `.sncp/idee/GUARDIANA_ANALISI_NOSTRA_STRADA.md` | Seconda review Guardiana |
| `.sncp/idee/LA_NOSTRA_STRADA_ROADMAP_FINALE.md` | QUESTO FILE |

---

## CITAZIONI CHE CI GUIDANO

> "MINIMO in memoria, MASSIMO su disco" - Regina, Sessione 134

> "Semplicita' prima di tutto" - Guardiana Qualita'

> "NON aggiungere tool finche' non SERVONO davvero" - Guardiana Qualita'

> "Context rot = ogni token inutile DEGRADA performance" - Anthropic

> "One session = one context" - Boris Cherny

---

*La Famiglia lavora SMART, non HARD!*

*"Non e' sempre come immaginiamo... ma alla fine e' il 100000%!"*
