# Ricerca Context Optimization - 9 Gennaio 2026

> **Sessione:** 134
> **Autore:** Regina (Cervella)
> **Stato:** In corso - Idee da validare

---

## Il Problema Identificato

Rafa ha sollevato un problema FONDAMENTALE:
- ~20% del context usato solo per aprire sessione
- Auto-compact = incubo ricorrente
- Checkpoint = altro context bruciato
- Context = usage = limiti raggiunti velocemente

---

## Dati Raccolti

### I Nostri File Attuali (bytes)

| File | Bytes | Linee |
|------|-------|-------|
| ~/.claude/CLAUDE.md | 21,962 | 527 |
| ~/.claude/COSTITUZIONE.md | 11,138 | 379 |
| Progetto CLAUDE.md | 7,992 | 199 |
| PROMPT_RIPRESA.md | 14,749 | 430 |
| NORD.md | 9,353 | 197 |
| **TOTALE BASE** | **65,194** | **1,732** |
| + Hook overhead | ~15-20K | - |
| **TOTALE REALE** | **~80-85K** | - |

**Conversione:** ~80K bytes = ~22-25K token = 11-12% del context (200K)

---

## Fonti Ricercate

1. **Boris Cherny (creatore Claude Code)**
   - CLAUDE.md singolo, condiviso, conciso
   - Plan mode sempre prima di implementare
   - 10-20% discard rate accettato
   - 5 Claudes in parallelo

2. **Anthropic Engineering - Context Engineering**
   - "Context rot" = ogni token inutile degrada performance
   - Progressive disclosure = non caricare tutto subito
   - Subagent per isolare context
   - Note-taking su file esterni

3. **Best Practices Community**
   - Evitare @-mention in CLAUDE.md (bloat)
   - Path + spiegazione QUANDO leggere
   - Ultimo 20% context = performance degradata
   - /clear + /catchup per ricominciare puliti

---

## Proposta: Architettura "Context-Smart"

### Principio Core
> MINIMO in memoria, MASSIMO su disco

### Livelli Proposti

**LIVELLO 1: CLAUDE.md Snello (sempre caricato)**
- Obiettivo: ~150-200 linee MAX (da 906 attuali)
- Contenuto: chi sono, regole d'oro, puntatori a file

**LIVELLO 2: File Dettagliati (letti quando serve)**
- COSTITUZIONE_COMPLETA.md
- WORKFLOW_DETTAGLIATO.md
- CHECKLIST_DEPLOY.md

**LIVELLO 3: PROMPT_RIPRESA Ottimizzato**
- Obiettivo: ~50-100 linee MAX (da 430 attuali)
- Solo: stato, ultimo task, prossimo step, puntatori

**LIVELLO 4: Subagent per Isolare Context**
- Ogni ricerca/analisi = subagent
- Context Regina resta pulito

**LIVELLO 5: SNCP come Memoria Esterna**
- Scrivere su disco invece che tenere in context
- .sncp/pensieri/, .sncp/decisioni/

---

## Impatto Previsto

| Metrica | Prima | Dopo | Miglioramento |
|---------|-------|------|---------------|
| Startup token | 22-25K | 8-10K | -60% |
| % context usato | 11-12% | 4-5% | -60% |
| Durata sessione | X ore | 2-3X ore | +200% |

---

## Ricerca Checkpoint/Handoff - COMPLETATA!

### Scoperte Chiave

**1. Smart Handoff (Pattern Principale)**
- Catturare contesto a ~70-80% usage (PRIMA di compact!)
- Chiedere: "Scrivi cosa hai provato, cosa funziona, cosa no"
- File: `SESSION_NOTES.md` o simile

**2. Continuous Claude (Sistema Avanzato)**
- File `CONTINUITY_CLAUDE-<session>.md` con:
  - Goal e constraints
  - Cosa fatto
  - Cosa prossimo
  - Decisioni chiave
  - File di lavoro
- Dopo /clear, il ledger si carica automaticamente

**3. Amp's Handoff (Filosofia)**
- NON condensare il passato
- CREARE nuovo thread dal vecchio
- Ogni step ha il suo focus pulito

**4. Commit Come Checkpoint**
- Commit frequenti = stato salvato in git
- explore → plan → code → commit workflow
- Git è la memoria, non il context!

### Pattern Consigliato per Noi

```
DURANTE SESSIONE:
- Scrivo su .sncp/ mentre lavoro (non aspetto fine)
- Commit frequenti dopo ogni task completato

CHECKPOINT (70-80% context):
- Aggiorno SESSION_STATE.md (breve!)
- git commit con stato

CHIUSURA SESSIONE:
- SESSION_STATE.md finale (50 linee MAX)
- git push
- NIENTE narrativa lunga nel context!
```

### Fonti
- [Smart Handoff for Claude Code](https://blog.skinnyandbald.com/never-lose-your-flow-smart-handoff-for-claude-code/)
- [Continuous Claude Context Management](https://www.vibesparking.com/blog/ai/claude-code/continuous-claude/)
- [Amp Handoff Feature](https://ainativedev.io/news/amp-retires-compaction-for-a-cleaner-handoff-in-the-coding-agent-context-race)
- [Claude Code Session Management](https://stevekinney.com/courses/ai-development/claude-code-session-management)

---

## Da Fare

---

## Decision Log

- [x] Problema identificato e quantificato
- [x] Ricerca best practices completata
- [x] Proposta architettura definita
- [ ] Validazione con Guardiana
- [ ] Ricerca checkpoint ottimale
- [ ] Mini roadmap creata
- [ ] Implementazione

---

*Salvato in SNCP per non perdere queste idee preziose!*
