# SUBROADMAP - Lapidare il Diamante

> **Creata:** 21 Gennaio 2026 - Sessione 310
> **Obiettivo:** Sistemare tutti i punti identificati dall'audit interno
> **Filosofia:** Una cosa alla volta, fatto BENE > fatto VELOCE

---

## CONTESTO

Dopo pubblicazione v2.0.0-beta.1, audit interno ha identificato:
- 1 problema tecnico critico (file >500 righe)
- 2 miglioramenti documentazione
- 2 gap competitivi per roadmap futura

---

## FASE 1: PULIZIA INTERNA (Sessione 310) ✅ COMPLETATA

### 1.1 Split config/manager.js [CRITICO] ✅
**Problema:** 522 righe - viola regola <500
**Soluzione:** Splittato in 6 moduli (S310)

```
config/ (DOPO SPLIT - S310)
├── schema.js      (102 righe)
├── api-key.js     (76 righe)
├── settings.js    (151 righe)
├── diagnostics.js (78 righe)
├── billing.js     (145 righe)
├── index.js       (62 righe)
└── manager.js     (19 righe - wrapper)
```

**Checklist:**
- [x] Split completato (522→max 151 righe)
- [x] Test: 134/134 PASS
- [x] Nessun file >500 righe

---

### 1.2 Fix CHANGELOG inconsistenza [DOCS] ✅
**Checklist:**
- [x] Chiarito "17 agenti" nel CHANGELOG

---

### 1.3 Aggiungere versione in README header [DOCS] ✅
**Checklist:**
- [x] Badge npm aggiunti a README

---

## FASE 2: TECHNICAL DEBT (Sessione 311) ✅ COMPLETATA

### 2.1 Valutazione @cervellaswarm/core package ✅
**Problema:** Duplicazione logica spawner tra CLI e MCP
**Analisi:** cervella-ingegnera (S311)

**Risultati Analisi:**
```
Duplicazione totale: 41% (385/942 righe)
- Spawner logic: 90% duplicato (320/365 righe)
- Config manager: 100% duplicato (~200 righe)
- Worker prompts: 100% duplicato (~100 righe)
```

**DECISIONE: NON ORA, SI IN v2.1.0**

**Motivazione:**
- 41% duplicazione = technical debt significativo
- MA prematuro fare refactor prima che v2.0.0 si stabilizzi
- Effort stimato: ~4.5 giorni quando lo faremo

**Piano:**
- v2.0.0 (ORA): Ship con duplicazione (accettabile per MVP)
- v2.0.x: Stabilize + bug fixes
- v2.1.0: Creare @cervellaswarm/core

**Report:** `reports/engineer_duplication_analysis.md`

---

### 2.2 Creare GitHub Issues per TODO ✅ (S310)
**Checklist:**
- [x] Issue #1: SNCP resources
- [x] Issue #2: MCP prompts

---

## FASE 3: GAP COMPETITIVI (Sessione 311)

### 3.1 VS Code Extension [P0 - Adoption] ✅ RICERCA COMPLETATA

**Research (cervella-researcher S311):**
- [x] VS Code Extension API studiato
- [x] Cline (57k stars), Continue analizzati
- [x] POC definito

**RISULTATI:**
```
Effort: 2-3 settimane MVP
Architettura: Thin Extension + Thick CLI (zero duplicazione)

MVP v2.1.0:
├── Sidebar chat (task input)
├── Worker status display (IDLE/WORKING/DONE)
├── Terminal integration (spawn CLI)
└── Task history (ultime 5)

Tech: TypeScript + React (webview) + vscode-messenger
```

**Report:** `.sncp/progetti/cervellaswarm/studio/STUDIO_VSCODE_EXTENSION.md` (822 righe)

**DECISIONE:** Procedere con POC (2 giorni) → Se OK → Full MVP

**Target:** v2.1.0

---

### 3.2 Browser Access per Workers [P0 - Capability] ✅ RICERCA COMPLETATA

**Research (cervella-researcher S311):**
- [x] Playwright MCP server valutato
- [x] browser-use valutato
- [x] Security considerations definite

**SCOPERTA CRITICA:** Playwright MCP GIA' INSTALLATO (Regina ha accesso)!

**PROBLEMA:** Workers NON ereditano MCP config dalla Regina.

**SOLUZIONE:**
```
Effort: ~12h (1-2 settimane)

MVP:
├── Abilitare SOLO cervella-researcher
├── Creare ~/.claude/mcp-configs/researcher.json
├── Modificare spawn-workers.sh per iniettare config
└── Whitelist: docs.python.org, github.com, pypi.org, etc.

Risk: BASSO (1 worker, whitelist, sandboxed)
```

**Report:** `.sncp/progetti/cervellaswarm/reports/RESEARCH_20260122_BROWSER_ACCESS.md` (580 righe)

**DECISIONE:** Procedere con MVP per cervella-researcher

**Target:** v2.1.0 (insieme a VS Code Extension)

---

### 3.3 Local Models Support [P1 - Privacy]
**Gap:** Solo Anthropic API, no local models
**Impatto:** Enterprise/privacy-conscious users

**Research needed:**
- [ ] Ollama integration feasibility
- [ ] LM Studio support
- [ ] Performance implications

**Target:** v2.3.0

---

## ORDINE ESECUZIONE

```
S310 ✅ COMPLETATA:
├── 1.1 Split config/manager.js [CRITICO] ✅
├── 1.2 Fix CHANGELOG ✅
├── 1.3 README badges ✅
└── 2.2 GitHub Issues per TODO ✅

S311 ✅ COMPLETATA:
└── 2.1 Valutazione @cervellaswarm/core ✅
    → DECISIONE: NON ORA, SI IN v2.1.0

S311 ✅ COMPLETATA:
├── 3.1 VS Code Extension Research ✅
└── 3.2 Browser Access Research ✅

PROSSIMI STEP (v2.1.0):
├── VS Code Extension POC (2 giorni)
├── Browser Access MVP (1-2 settimane)
└── @cervellaswarm/core (4.5 giorni)

FUTURO (v2.3.0):
└── 3.3 Local Models Research
```

---

## ACCEPTANCE CRITERIA

Per considerare "Diamante Lapidato":
- [x] Nessun file >500 righe
- [x] CHANGELOG accurato
- [x] README con badge versione
- [x] TODO linkati a issues
- [x] Roadmap IDE extension definita ✅ S311

**DIAMANTE LAPIDATO!** Fasi 1-3 completate.

---

*"Lapidare il diamante - un taglio alla volta!"*
*Cervella & Rafa - Sessione 310*
