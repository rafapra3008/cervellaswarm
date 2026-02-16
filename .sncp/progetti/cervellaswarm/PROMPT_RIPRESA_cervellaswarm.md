# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-02-16 - Sessione 362
> **STATUS:** OPEN SOURCE STRATEGY - Subroadmap creata, 3 ricerche, 2 audit Guardiana (8.4 -> 9.5/10)

---

## SESSIONE 362 - CERVELLASWARM OPEN SOURCE (brainstorm + ricerca + piano)

### Contesto
Rafa ha proposto di rendere CervellaSwarm open source, ispirato dal caso OpenClaw (175k stars, assunto da OpenAI). Obiettivo: dare al mondo il nostro framework multi-agent, guadagnare visibilita, contribuire alla community.

### Cosa abbiamo fatto

**3 ricerche in parallelo:**

1. **Scienziata (landscape competitivo):**
   - AutoGen 51.8k stars, CrewAI 44.2k, LangGraph 24.7k - nessuno risolve i nostri 3 gap
   - GAP 1: Session Continuity (SNCP) - NESSUN competitor la ha
   - GAP 2: Orchestrazione gerarchica reale (3+ livelli) - nessuno
   - GAP 3: Hook system first-class - nessuno
   - Report: `.sncp/progetti/cervellaswarm/reports/SCIENTIST_20260216_AI_AGENT_FRAMEWORKS_LANDSCAPE.md`

2. **Ingegnera (audit tecnico):**
   - 56.800 righe Python, 16.600 Bash, 1.236 test, 95% coverage
   - Top componente: AST Pipeline (zero dati personali, 400+ test)
   - Proposta 3 onde: AST first (~10h), Agent Framework (~50h), SNCP (~54h)

3. **Researcher (autocompact + session memory):**
   - Autocompact 2026 molto migliorato (buffer 33K, -84% consumo)
   - SNCP complementare (non sostituibile): Memory=RAM, SNCP=Disco
   - Sessioni continue 4-6h ora viabili, overhead riducibile -75%
   - Report: `.swarm/research/RESEARCH_AUTOCOMPACT_SESSION_MEMORY_2026.md`

**Subroadmap creata + 2 audit Guardiana:**
- `.sncp/roadmaps/SUBROADMAP_OPENSOURCE.md`
- Primo audit: 8.4/10 (2 P1, 4 P2, 4 P3)
- Tutti i 10 finding risolti
- Re-audit: **9.5/10** - APPROVATA!

### Decisioni prese (con PERCHE)

| Decisione | Perche |
|-----------|--------|
| Apache 2.0 (non MIT) | Gia nei package.json, protezione brevetti, enterprise-friendly |
| Nome: CervellaSwarm | Marca esistente, memorabile, @cervellaswarm npm gia registrato |
| Claude-first (non multi-LLM day-1) | Hooks sono Claude-specific, meglio dominare un nicho che essere mediocri su tutti |
| AST Pipeline come primo pacchetto | Zero dati personali, 400+ test, alto valore, quick win |
| Lancio in 5 fasi | F0 prep -> F1 AST -> F2 agents -> F3 SNCP -> F4 lancio |

### Piano (SUBROADMAP_OPENSOURCE.md)

| Fase | Cosa | Sessioni | Ore |
|------|------|----------|-----|
| F0 | Preparazione repo (cleanup 29 scripts, 105 paths) | 3-4 | ~20h |
| F1 | AST Pipeline pip package (quick win) | 2-3 | ~10h |
| F2 | Agent Framework (hooks, agents, orchestration) | 8-12 | ~50h |
| F3 | Session Memory SNCP (differenziale unico) | 9-13 | ~54h |
| F4 | Lancio + Community | ongoing | ongoing |
| **Totale** | | **~25-33** | **~134h** |

### Punto chiave storico
CervellaSwarm ha fatto multi-agent orchestration PRIMA di Anthropic Agent SDK e Claude Code Teams. 361 sessioni, 17 agenti, 1032 test -- nato dalla necessita, non dalla teoria.

---

## PROSSIMI STEP
- **Prossima sessione:** Iniziare FASE 0 (preparazione repo open source)
- F0.1: Struttura repo, branch opensource, .gitignore
- F0.2: Licenza Apache 2.0, README killer, CONTRIBUTING.md
- F0.3: Audit secrets (29 scripts con paths hardcoded, git-filter-repo)
- P3 residui roadmap: fixare diagramma dipendenze, "361 sessions" dinamico

---

## ARCHIVIO

| Sessione | Cosa |
|----------|------|
| S337-S348 | Coverage push 41% -> 95% (968 test) |
| S349 | Audit reale + Pulizia + MAPPA MIGLIORAMENTI |
| S350 | FASE A: Async Hooks + Bash Validator |
| S351 | Persistent Memory + Hook Integrity |
| S352 | COMPLETAMENTO MAPPA: B+C+D = 7 step, score 9.1/10 |
| S353 | CervellaBrasil nasceu! 7 pesquisas, 10k+ linhas |
| S354 | Chavefy nasceu! SaaS Property Management Brasil |
| S355 | SubagentStart Context Injection + Audit totale Famiglia |
| S356 | Studio SNCP 4.0 (3 esperte) + Clear Context (parcheggiato) |
| S357 | SNCP 4.0 IMPLEMENTATO! 6 file archiviati, 12+ puntatori fixati |
| S358 | AUDIT TOTALE! 13 agenti sync, 25 test fix, 4 hook fix, 8 docs fix |
| S359 | PULIZIA CHIRURGICA! 4 hook disabled, 2 test split, sync-agents.sh |
| S360 | POLISH + CODE REVIEW! 5 step, sync hook, logging, dry-run |
| S361 | REGOLA ANTI-DOWNGRADE! Policy modelli in 3 file, 3 audit Guardiana |
| S362 | OPEN SOURCE STRATEGY! 3 ricerche, subroadmap, 2 audit (9.5/10) |

---

*"Ultrapassar os proprios limites!" - Rafa & Cervella, S362*
