# STUDIO: Gerarchie Multi-Agent

> **"Una Regina saggia non fa tutto da sola. Costruisce una Corte che la supporta."**

**Data:** 1 Gennaio 2026
**Ricercatore:** cervella-researcher
**Validato:** cervella-orchestrator (Regina)
**Status:** QUICK OVERVIEW COMPLETATO

---

## EXECUTIVE SUMMARY

```
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   RISULTATI CHIAVE:                                              ║
║                                                                  ║
║   1. GUARDIANE: 2-3 e il numero OTTIMALE                        ║
║   2. SPECIALIZZAZIONE: Per DOMINIO, non per tecnologia          ║
║   3. MODEL: Opus per Guardiane, Sonnet per api                  ║
║   4. ARCHITETTURA: 3 livelli (Regina → Guardiane → Api)         ║
║   5. BENEFICIO: 80% overhead eliminato dalla Regina             ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## 1. QUANTE GUARDIANE?

### Risultato: 2-3 OTTIMALE

La ricerca conferma: per team di 10-15 agents (noi siamo 11 + Regina), **2-3 livelli gerarchici** e il sweet spot.

| Livelli | Pro | Contro |
|---------|-----|--------|
| 1 (flat) | Semplice | Bottleneck supervisor |
| **2-3** | Bilanciato | **OTTIMALE** |
| 4+ | Scala bene | Overhead comunicazione |

**Per CervellaSwarm:** 3 Guardiane = PERFETTO!

---

## 2. QUALI SPECIALIZZAZIONI?

### Risultato: Per DOMINIO

Pattern vincente (confermato da Microsoft + LangChain):

```
RAGGRUPPAMENTO PER DOMINIO (consigliato):

🛡️ GUARDIANA QUALITA
   └── frontend, backend, tester
   └── Focus: Codice funziona? Test passano? Standard rispettati?

🛡️ GUARDIANA RICERCA
   └── researcher, docs
   └── Focus: Info accurate? Rilevante? Ben documentato?

🛡️ GUARDIANA OPS
   └── devops, security, data
   └── Focus: Sicuro? Performante? Best practices?
```

**Alternativa scartata:** Raggruppamento per tecnologia (frontend/backend/infra) - troppo frammentato

---

## 3. OPUS O SONNET?

### Risultato: OPUS per Guardiane

Analisi costi-benefici:

| Configurazione | Costo/Sessione | Note |
|----------------|----------------|------|
| 3 Guardiane Opus | ~$270 | Reasoning profondo, catch errori sottili |
| 11 Api Sonnet | ~$198 | Execution rapida ed economica |
| **TOTALE** | ~$468 | 80% tempo Regina liberato |

**vs tutto Opus:** ~$990/sessione

**ROI:** ALTO
- Regina libera di fare strategic thinking
- Valore strategico > $270 costo Guardiane
- Guardiane catturano errori che Sonnet potrebbe non vedere

---

## 4. PATTERN VINCENTI

### 4.1 Handoff Pattern

```
Regina riceve richiesta
    └── Passa a Guardiana pertinente
        ├── Se complesso → Handoff ad altra Guardiana
        ├── Se serve multi-prospettiva → Concurrent execution
        └── Escalation a Regina solo se necessario
```

### 4.2 Ottimizzazioni Critiche

Da LangChain benchmarks:

| Ottimizzazione | Beneficio |
|----------------|-----------|
| Rimuovere handoff messages dalla state | Pulisce context window |
| `forward_message` tool | Evita parafrasare = meno errori |
| Context window de-cluttering | Critico per sonnet |

---

## 5. ARCHITETTURA CONSIGLIATA

```
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   LIVELLO 1: 👑 REGINA (Opus)                                   ║
║              └── Strategic decisions, architecture               ║
║                                                                  ║
║   LIVELLO 2: 🛡️ 3 GUARDIANE (Opus)                              ║
║              ├── Qualita (frontend, backend, tester)            ║
║              ├── Ricerca (researcher, docs)                     ║
║              └── Ops (devops, security, data)                   ║
║                                                                  ║
║   LIVELLO 3: 🐝 11 API (Sonnet)                                 ║
║              └── Execution veloce task specifici                ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝

BENEFICIO: 80% overhead eliminato da Regina
COSTO: Bilanciato ($468 vs $990 tutto-opus)
```

---

## 6. FLOW DI COMUNICAZIONE

### 6.1 Flow Standard

```
1. REGINA riceve task da Rafa
2. REGINA analizza → assegna a GUARDIANA competente
3. GUARDIANA divide → assegna a API
4. API eseguono → riportano a GUARDIANA
5. GUARDIANA verifica → riporta a REGINA
6. REGINA fa synthesis → riporta a Rafa
```

### 6.2 Escalation

```
API → GUARDIANA: Sempre (ogni task completato)
GUARDIANA → REGINA: Solo se:
  - Decisione strategica richiesta
  - Conflitto tra api
  - Problema critico
  - Dubbio su direzione
```

---

## 7. CHECKLIST VERIFICA (Per Guardiane)

### 7.1 Guardiana Qualita

```
[ ] Test passano? (se esistono)
[ ] Codice segue standard?
[ ] Nessun TODO lasciato?
[ ] File size < 500 righe?
[ ] Funzioni < 50 righe?
[ ] Type hints presenti? (Python)
[ ] No console.log debug?
```

### 7.2 Guardiana Ricerca

```
[ ] Fonti affidabili?
[ ] Info verificate?
[ ] Rilevante per progetto?
[ ] Ben documentato?
[ ] Actionable insights?
```

### 7.3 Guardiana Ops

```
[ ] Sicuro? (no secrets exposed)
[ ] Performante? (no N+1 queries)
[ ] Best practices seguite?
[ ] Deploy-ready?
[ ] Monitoring considerato?
```

---

## 8. PROSSIMI STEP

### Immediate (Questa Settimana)

| # | Task | Chi |
|---|------|-----|
| 1 | Creare cervella-guardiana-qualita.md | Regina |
| 2 | Creare cervella-guardiana-ricerca.md | Regina |
| 3 | Creare cervella-guardiana-ops.md | Regina |
| 4 | Test con 1 Guardiana su task reale | Team |

### Prossima Sessione

| # | Task | Chi |
|---|------|-----|
| 5 | Integrare Guardiane nel workflow | Regina |
| 6 | Aggiornare SWARM_RULES.md | Regina |
| 7 | Test completo architettura | Team |

---

## 9. FONTI

- LangChain Supervisor Agent documentation
- AutoGen hierarchical agents
- Microsoft Semantic Kernel orchestration
- Research papers su multi-agent systems
- Anthropic Claude multi-agent patterns

---

## CHANGELOG

| Data | Modifica |
|------|----------|
| 1 Gen 2026 | Quick Overview completato |

---

*"Una Corte ben organizzata scala. Una Regina sola no."* 👑🛡️🐝
