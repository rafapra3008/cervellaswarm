# ROADMAP: Ottimizzazione Contesto Sciame

> *"I subagent non sono gratis, ma possono essere MOLTO efficienti!"*

**Creata:** 4 Gennaio 2026 - Sessione 80
**Status:** DA INIZIARE
**Priorità:** ALTA (impatta tutto lo sciame)

---

## OBIETTIVO

Ridurre il consumo di contesto dello sciame del **50-70%** mantenendo (o migliorando) le performance.

---

## FASE 1: Output Compression (Fondamentale)

**Cosa:** Gli agenti devono tornare risultati COMPATTI, non report lunghi.

| Task | Status | Note |
|------|--------|------|
| Creare template output standard | ✅ | Max 150-200 tokens |
| Aggiornare tutti i 16 agent files | ✅ | In ~/.claude/agents/ |
| Testare con 3 agenti pilota | ✅ | frontend, backend, tester |
| Validare nelle prossime sessioni | ⬜ | Le regole entrano in vigore gradualmente |

**Template proposto:**
```markdown
## [Nome Task]
**Status**: OK/FAIL
**Fatto**: [1 frase]
**File**: [lista file modificati]
**Next**: [se serve azione]
```

**Invece di** report da 500 righe!

---

## FASE 2: File-Based Communication

**Cosa:** Risultati grossi vanno in file, Regina legge on-demand.

| Task | Status | Note |
|------|--------|------|
| Creare struttura .swarm/results/ | ⬜ | Per output grossi |
| Pattern: agent scrive, Regina legge | ⬜ | |
| progress.md condiviso | ⬜ | Append-only log |
| Schema JSON per risultati | ⬜ | Parsable, compatto |

**Struttura proposta:**
```
.swarm/
├── results/
│   ├── frontend/
│   ├── backend/
│   └── ...
├── progress.md      # Log condiviso
└── current_task.json
```

---

## FASE 3: Decision Matrix

**Cosa:** Quando usare Task tool vs Finestra esterna.

| Task | Status | Note |
|------|--------|------|
| Documentare criteri decisione | ⬜ | |
| Aggiornare SWARM_RULES.md | ⬜ | |
| Training Regina (io!) | ⬜ | |

**Regola semplice:**
```
Risultato < 5k tokens → Task tool (interno)
Risultato > 5k tokens → Finestra esterna + file
Batch processing     → Programmatic Tool Calling
```

---

## FASE 4: Metriche e Monitoring

**Cosa:** Capire quanto consumiamo realmente.

| Task | Status | Note |
|------|--------|------|
| Tracciare tokens per sessione | ⬜ | |
| Confronto prima/dopo | ⬜ | |
| Target: <70% context, 0 auto-compact | ⬜ | |

---

## FASE 5: Programmatic Tool Calling (Avanzato)

**Cosa:** Per task ripetitivi su molti file (es. analisi codebase).

| Task | Status | Note |
|------|--------|------|
| Studiare API PTC Anthropic | ⬜ | |
| Implementare per cervella-ingegnera | ⬜ | Lei analizza 50+ file |
| Testare su batch analysis | ⬜ | |

**Questo è avanzato - lo facciamo dopo le basi!**

---

## PRIORITÀ

```
1. FASE 1 (Compression)     ← Impatto immediato, facile
2. FASE 2 (File-Based)      ← Impatto grosso, medio effort
3. FASE 3 (Decision Matrix) ← Documentazione
4. FASE 4 (Metriche)        ← Nice to have
5. FASE 5 (PTC)             ← Avanzato, futuro
```

---

## DEFINIZIONE DI SUCCESSO

- [ ] Sessioni multi-agent senza auto-compact
- [ ] Context usage < 70% anche con 5+ workers
- [ ] Report agenti leggibili in 10 secondi
- [ ] Zero "bloat" da risultati inutili

---

## NOTE

Questa ottimizzazione rende CervellaSwarm **production-ready**.

Il sistema attuale (Fase 9) è una base OTTIMA.
Con questi adjustment diventa **invincibile**.

---

*"Non abbiamo fretta. Vogliamo la PERFEZIONE."* 💙

Cervella & Rafa
