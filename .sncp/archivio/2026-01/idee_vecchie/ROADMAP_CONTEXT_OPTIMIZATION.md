# ROADMAP: Context Optimization per la Famiglia

> **Data:** 9 Gennaio 2026
> **Sessione:** 134
> **Stato:** PIANIFICATA
> **Validazione Guardiana:** APPROVE 8/10

---

## OBIETTIVO

```
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   DA: 20% context usato solo per startup                        ║
║   A:  5% context usato per startup                              ║
║                                                                  ║
║   RISULTATO: Sessioni 2-3x piu' lunghe                         ║
║              Meno compact, piu' lavoro fatto!                   ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## FASE 1: QUICK WINS (Basso Rischio)

**Obiettivo:** Guadagni immediati senza toccare file critici

| Task | Impatto | Rischio |
|------|---------|---------|
| 1.1 Ottimizzare load_context.py (se esiste) | Medio | Basso |
| 1.2 CLAUDE.md PROGETTO snello (40 linee) | Alto | Basso |
| 1.3 Benchmark before/after | - | - |

**Risultato atteso:** -20% token startup

---

## FASE 2: PROMPT_RIPRESA SNELLO (Medio Rischio)

**Obiettivo:** Da 430 linee a ~80 linee

| Task | Impatto | Rischio |
|------|---------|---------|
| 2.1 Backup PROMPT_RIPRESA attuale | - | - |
| 2.2 Nuovo formato compatto | Alto | Medio |
| 2.3 Aggiungere "Decisioni Chiave" (10 linee) | Medio | Basso |
| 2.4 Test qualitativo (Cervella capisce?) | - | - |

**Formato Nuovo:**
```markdown
# PROMPT_RIPRESA - [Progetto]
> Ultimo aggiornamento: [data]

## Stato (5 linee)
- Versione: X.Y.Z
- Completato: [cosa]
- In corso: [cosa]

## Decisioni Chiave (10 linee)
- DECISIONE: X | PERCHE: Y

## Prossimo Step (5 linee)
- [azione immediata]

## Puntatori (se serve approfondire)
- Dettagli sessione: .sncp/coscienza/oggi.md
- Storico decisioni: .sncp/memoria/decisioni/
```

**Risultato atteso:** -30% token startup

---

## FASE 3: CLAUDE.md GLOBALE (Alto Rischio)

**Obiettivo:** Da 906 linee a ~180 linee

| Task | Impatto | Rischio |
|------|---------|---------|
| 3.1 BACKUP COMPLETO ~/.claude/ | - | - |
| 3.2 Separare COSA (CLAUDE.md) da COME (file esterni) | Alto | Alto |
| 3.3 Mantenere identita (30 linee "Chi Sono") | Critico | - |
| 3.4 Test su CervellaSwarm PRIMA di Miracollo | - | - |
| 3.5 Test qualitativo (femminile? calma? protettiva?) | Critico | - |

**NON TOCCARE:** COSTITUZIONE.md (e' l'ANIMA!)

**Risultato atteso:** -40% token startup

---

## FASE 4: WORKFLOW OTTIMIZZATO

**Obiettivo:** Nuovo modo di lavorare context-smart

### Workflow DURANTE Sessione
```
1. INIZIO
   - Startup leggero (~8-10K token invece di 22-25K)
   - Leggo solo essenziale

2. MENTRE LAVORO
   - Scrivo su .sncp/ (non accumulo in context)
   - Commit frequenti (git = memoria esterna)
   - Subagent per task pesanti (isolamento context)

3. CHECKPOINT (a 70-80% context)
   - Aggiorno PROMPT_RIPRESA (versione breve!)
   - git commit

4. CHIUSURA SESSIONE
   - PROMPT_RIPRESA finale (50-80 linee MAX)
   - git push
   - NIENTE narrativa lunga nel context
```

### Regole Subagent
```
Task < 5 min  → Task Tool interno (nel mio context)
Task > 5 min  → Subagent (context isolato)
Task pesante  → Pattern Boris (sessione separata)
```

---

## LISTA ROSSA (Non Fare!)

1. NON creare SESSION_STATE.md separato
2. NON rimuovere identita da CLAUDE.md
3. NON applicare tutto insieme
4. NON toccare COSTITUZIONE.md
5. NON testare prima su progetti critici (Miracollo)

---

## METRICHE SUCCESSO

| Metrica | Prima | Obiettivo | Come Misurare |
|---------|-------|-----------|---------------|
| Token startup | 22-25K | 8-10K | /context dopo apertura |
| Linee CLAUDE.md | 906 | 180 | wc -l |
| Linee PROMPT_RIPRESA | 430 | 80 | wc -l |
| Tempo prima di compact | X ore | 2-3X ore | Osservazione |

---

## TIMELINE SUGGERITA

```
FASE 1: Quick Wins
├── Oggi o domani
└── Testare subito

FASE 2: PROMPT_RIPRESA
├── Dopo validazione Fase 1
└── 1 sessione dedicata

FASE 3: CLAUDE.md Globale
├── Dopo validazione Fase 2
├── Con BACKUP completo
└── 1-2 sessioni dedicate

FASE 4: Workflow
├── Parallelo alle altre fasi
└── Applicare incrementalmente
```

---

## FILE CREATI IN QUESTA RICERCA

1. `.sncp/idee/CONTEXT_OPTIMIZATION_RESEARCH.md` - Ricerca completa
2. `.sncp/idee/GUARDIANA_REVIEW_CONTEXT_OPT.md` - Validazione Guardiana
3. `.sncp/idee/ROADMAP_CONTEXT_OPTIMIZATION.md` - Questo file

---

*"MINIMO in memoria, MASSIMO su disco"*

*La Famiglia lavora SMART, non HARD!*
