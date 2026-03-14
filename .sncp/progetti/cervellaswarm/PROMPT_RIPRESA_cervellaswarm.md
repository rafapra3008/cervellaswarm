# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-03-14 - Sessione 461
> **STATUS:** 3/5 progetti showcase DONE. Moltbook + OpenClaw strategy scoperta.

---

## DOVE SIAMO -- IL QUADRO COMPLETO

### La storia recente (S455-S461)

**S455-S456:** Svolta strategica. 5 progetti showcase PRIMA di lanciare.
**S458-S459:** LU Debugger LIVE + Tour of LU LIVE. 2/5 pronti.
**S460:** Auto-compact + SNCP health (9.5/10). Sistema pulito.

**S461 (oggi):** Sessione grande! Due breakthrough:

1. **Incident Replay DONE** -- `playground/incident.html`, ~1700 LOC
   - Narrativa "$34K bug" con choice/branching LU reale
   - Ricerca: Counterfactual Replay (AgenTracer 2025), Evil Martians devtool pattern
   - Architect plan dettagliato, Guardiana 9.1→9.5+ (7 finding fixati)
   - IntersectionObserver, counter animato, violation shake, responsive, a11y

2. **Scoperta Moltbook + OpenClaw** -- nuovo canale di lancio!
   - Moltbook: Reddit per AI agents, 1.6M agenti, Meta acquisito 10/03
   - OpenClaw: ogni skill e un MCP server, 13.729 su ClawHub
   - LU = "missing verification layer" per A2A/MCP
   - Report: 3 ricerche complete in `.sncp/progetti/cervellaswarm/reports/`
   - Serve da Rafa: email + tweet verifica per registrare agente

---

## COSA E LIVE

### 1. LU Debugger -- https://lu-debugger.fly.dev/
3 agenti AI su protocollo verificato. Demo + Live (Claude API).

### 2. Tour of LU -- https://rafapra3008.github.io/cervellaswarm/?tour
24 step interattivi, 4 capitoli, 4 esercizi.

### 3. Incident Replay -- https://rafapra3008.github.io/cervellaswarm/incident.html
"$34,000 — The cost of one missing protocol." 5 atti, counter animato, violation replay.

---

## MAPPA SITUAZIONE

```
LINGUA UNIVERSALE:
  31 moduli | 3684 test | PyPI v0.3.3 | VS Code v0.2.0

5 PROGETTI SHOWCASE:
  1. LU Debugger      DONE! LIVE (S458)
  2. Tour of LU       DONE! LIVE (S459)
  3. Incident Replay   DONE! (S461) -- deploy con push
  4. Protocol Zoo     <- PROSSIMO (2-3 sessioni)
  5. AI Code Review   (3-4 sessioni)

CANALE BONUS:
  Moltbook Agent + OpenClaw Skill (1-2 sessioni)
  Report: RESEARCH_20260314_MOLTBOOK_GUIDA_OPERATIVA.md
  Report: RESEARCH_20260314_OPENCLAW_SKILL_LU.md

LANCIO:
  Show HN v2: READY (docs/SHOW_HN_V2_DRAFT.md) -- aggiungere Incident Replay
  Blog: READY | Public repo: SYNCED | Discord: DA CREARE
```

---

## PROSSIMI STEP (ordine suggerito)

### 1. Moltbook Agent (finestra limitata, Meta)
Registrare agente LU. Serve: email Rafa + tweet verifica.
Guida operativa: `RESEARCH_20260314_MOLTBOOK_GUIDA_OPERATIVA.md`

### 2. Protocol Zoo (Progetto 4)
15 protocolli reali eseguibili. Stdlib ne ha 20, base pronta.

### 3. OpenClaw Skill MCP
4 tool: load_protocol, verify_message, check_properties, list_steps.
Primo skill con verifica formale tra 13.729 su ClawHub.

### 4. Show HN v2
Con 3 progetti + Moltbook presence. Pitch: "missing verification layer for A2A/MCP".

### Da Rafa (CEO)
- [ ] Email + tweet per Moltbook agent
- [ ] Creare Discord "Lingua Universale"
- [ ] Decidere: Moltbook prima o Protocol Zoo prima?

---

## DOVE TROVARE LE COSE

| Cosa | Path |
|------|------|
| **MAPPA 5 PROGETTI** | `.sncp/roadmaps/MAPPA_5_PROGETTI_LU.md` |
| **Incident Replay** | `playground/incident.html` |
| **Moltbook Guida** | `.sncp/progetti/cervellaswarm/reports/RESEARCH_20260314_MOLTBOOK_GUIDA_OPERATIVA.md` |
| **OpenClaw Skill** | `.sncp/progetti/cervellaswarm/reports/RESEARCH_20260314_OPENCLAW_SKILL_LU.md` |
| **AI Agent Networks** | `.sncp/progetti/cervellaswarm/reports/RESEARCH_20260314_AI_AGENT_SOCIAL_NETWORKS.md` |
| **Incident Research** | `.sncp/progetti/cervellaswarm/reports/RESEARCH_20260314_INCIDENT_REPLAY_PAGE.md` |
| **Show HN v2** | `docs/SHOW_HN_V2_DRAFT.md` |

---

## DECISIONI PRESE (S461)

1. **Choice/branching per narrativa** -- usare meccanismo LU REALE, non "no duplicate" fittizio
2. **Catppuccin Mocha** -- palette unica per tutti i showcase (non GitHub Dark del Debugger)
3. **Moltbook = canale parallelo** -- non sostituisce Show HN, lo complementa
4. **OpenClaw skill = MCP server** -- riutilizzabile da noi stesse in Claude Code/Cursor

---

## Lezioni Apprese (S461)

### Cosa ha funzionato bene
- **"Script PRIMA, codice DOPO" + Architect plan**: piano dettagliato prima dell'implementazione = Frontend ha prodotto pagina completa al primo tentativo
- **Guardiana catch critico**: `receives`/`investigates` non sono verbi LU validi. Un dev che prova nel Playground avrebbe trovato parse error. Fix prima del deploy.
- **Ricerca parallela**: 3 Researcher in background mentre la Regina coordina. Zero consumo di context.
- **Idea di Rafa (Moltbook)**: CEO vede opportunita che la tecnica non vede. Partnership vera.

### Cosa non ha funzionato
- **Gemini hallucination parziale**: i nomi erano giusti ma alcuni dettagli erano inventati. Sempre verificare con ricerca propria.

### Pattern confermato
- **"Audit piano → implementa → audit risultato"**: terza sessione consecutiva che funziona (S459, S460, S461)
- **Worker in background per ricerca**: 5 agent in background in una sessione, tutti completati con successo

---
*"Ultrapassar os proprios limites!"*
*S461: 3/5 showcase + Moltbook discovery. Il mondo si apre.*
