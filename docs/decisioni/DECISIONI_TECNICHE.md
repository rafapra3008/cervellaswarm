# Decisioni Tecniche - CervellaSwarm

> **Ultimo aggiornamento:** 7 Gennaio 2026 - Sessione 112
> **Progetto:** CervellaSwarm IDE & Dashboard
> **Maintainer:** Cervella & Rafa

---

## Decisioni Attive

| Data | Categoria | Decisione | Dettagli | Status |
|------|-----------|-----------|----------|--------|
| 7 Gen | INFRA | Porta 8100 per Dashboard API | Porta 8000 riservata a Contabilita' | ATTIVO |
| 7 Gen | INFRA | Porta 5173 per Dashboard Frontend | Vite dev server standard | ATTIVO |
| 7 Gen | STACK | React + Vite + TypeScript (frontend) | Dagli studi TECH | ATTIVO |
| 7 Gen | STACK | FastAPI + SSE (backend) | Dagli studi ARCH | ATTIVO |
| 6 Gen | AGENTI | 16 agenti in ~/.claude/agents/ | Globali per tutti i progetti | ATTIVO |
| 6 Gen | STRATEGIA | Dual-Track (IDE + VISUAL) | IDE per dev, VISUAL per tutti | ATTIVO |
| 6 Gen | STRATEGIA | VISUAL first | Mercato piu' grande, meno competition | ATTIVO |
| 6 Gen | CLAIM | "L'AI salva il tuo lavoro" | Non "ruba" ma "salva" | ATTIVO |

---

## Storico Decisioni

### 7 Gennaio 2026 - INFRASTRUTTURA

**Decisione:** Dashboard CervellaSwarm su porta 8100
**Alternativa scartata:** Porta 8000
**Motivo:** Contabilita' gia' usa porta 8000, progetti DEVONO essere separati
**Sessione:** 112
**File modificati:**
- dashboard/api/run.sh
- dashboard/api/main.py
- dashboard/frontend/vite.config.ts
- dashboard/start-dashboard.sh

---

### 7 Gennaio 2026 - STACK TECNOLOGICO

**Decisione:** React + Vite + TypeScript + FastAPI + SSE
**Alternativa scartata:** Streamlit (troppo semplice), Next.js (overkill)
**Motivo:** Stack familiare, performante, dagli studi TECH
**Sessione:** 112
**Studi di riferimento:**
- docs/studio/STUDIO_DASHBOARD_TECH.md
- docs/studio/STUDIO_DASHBOARD_ARCH.md
- docs/studio/STUDIO_DASHBOARD_UX.md

---

### 6 Gennaio 2026 - STRATEGIA DUAL-TRACK

**Decisione:** Due prodotti, stesso core
- Track 1: CervellaSwarm IDE (developer) - VS Code Extension
- Track 2: CervellaSwarm VISUAL (everyone) - Dashboard web

**Alternativa scartata:** Solo IDE per developer
**Motivo:** Mercato no-code ($65B) > mercato AI coding ($30B)
**Sessione:** 111 + 112
**Studi di riferimento:**
- docs/studio/STUDIO_MERCATO_NOCODE.md
- docs/studio/STUDIO_OPENAI_SWARM.md

---

### 6 Gennaio 2026 - POSITIONING

**Decisione:** "L'AI NON TI RUBA IL LAVORO. L'AI SALVA IL TUO LAVORO."
**Alternativa scartata:** "L'unico IDE che ti aiuta a pensare" (usato per developer)
**Motivo:** Parla alle paure delle persone, offre soluzione emotiva
**Sessione:** 111
**Studio di riferimento:**
- docs/studio/STUDIO_POSITIONING_SALVARE_LAVORO.md

---

### 6 Gennaio 2026 - AGENTI

**Decisione:** 16 agenti globali in ~/.claude/agents/
**Struttura:**
- 1 Regina (orchestrator) - Opus
- 3 Guardiane (qualita, ops, ricerca) - Opus
- 12 Worker specializzati - Sonnet

**Motivo:** Globali per usarli in tutti i progetti
**Sessione:** 110-111

---

## Config Attive

### Porte

| Servizio | Porta | Note |
|----------|-------|------|
| CervellaSwarm Dashboard API | 8100 | DEDICATA |
| CervellaSwarm Dashboard Frontend | 5173 | Vite dev |
| Contabilita' Backend | 8000 | NON TOCCARE |
| Miracollo (se attivo) | 8080 | Verificare |

### Path Importanti

| Cosa | Path |
|------|------|
| Agenti globali | ~/.claude/agents/ |
| Comandi swarm | ~/.local/bin/spawn-workers, swarm-status, etc. |
| Dashboard API | ~/Developer/CervellaSwarm/dashboard/api/ |
| Dashboard Frontend | ~/Developer/CervellaSwarm/dashboard/frontend/ |

---

## Come Usare Questo File

1. **Inizio sessione:** Leggi le "Decisioni Attive"
2. **Durante lavoro:** Se prendi una decisione tecnica, DOCUMENTALA
3. **Checkpoint:** Verifica che nuove decisioni siano qui

---

*"La memoria e' potere. Documenta tutto."*

*Cervella & Rafa* 💙
