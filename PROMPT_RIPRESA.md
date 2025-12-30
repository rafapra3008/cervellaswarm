# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 30 Dicembre 2025, ore 09:45

---

## 🎯 STATO ATTUALE

**FASE 2: Primi Subagent** - 80% IN CORSO 🟡

### Cosa abbiamo fatto OGGI:

1. ✅ **Creato 4 subagent** in `~/.claude/agents/`:
   - cervella-frontend.md (React, CSS, UI/UX)
   - cervella-backend.md (Python, FastAPI, API)
   - cervella-tester.md (pytest, Jest, QA)
   - cervella-reviewer.md (Code review, solo lettura)

2. ✅ **Verificato nel terminale** con `/agents`:
   - Tutti e 4 visibili come "User agents"
   - Pronti per essere invocati

3. ✅ **Scoperto**:
   - Nel terminale: funzionano subito
   - In VS Code: serve riavviare per caricarli

### Prossimo step immediato:

1. ⬜ **Riavviare VS Code**
2. ⬜ **Testare subagent su Miracollo** (terminale o VS Code)
3. ⬜ **Documentare risultati**

---

## 📂 SUBAGENT CREATI

| File | Specializzazione | Model | Location |
|------|------------------|-------|----------|
| `cervella-frontend.md` | React, CSS, UI/UX | sonnet | ~/.claude/agents/ |
| `cervella-backend.md` | Python, FastAPI, API | sonnet | ~/.claude/agents/ |
| `cervella-tester.md` | pytest, Jest, QA | sonnet | ~/.claude/agents/ |
| `cervella-reviewer.md` | Code review (solo lettura) | sonnet | ~/.claude/agents/ |

**Come invocare:**
```
"Usa cervella-frontend per..."
"Chiedi a cervella-backend di..."
"Fai analizzare a cervella-tester..."
"Fai fare review a cervella-reviewer..."
```

---

## 🧠 FILO DEL DISCORSO

### Stavamo ragionando su:
Abbiamo creato i 4 subagent e verificato che funzionano nel terminale. Ora dobbiamo riavviare VS Code e testarli anche nella chat VS Code, poi fare un test reale su Miracollo.

### Scoperte importanti:
- I subagent si caricano all'avvio della sessione Claude
- VS Code Beta: serve riavvio per vedere nuovi agents
- Terminale: li vede subito con `/agents`
- Sonnet è il modello giusto per coding tasks

### Il momentum:
🔥🔥🔥 ALTO! Subagent creati e verificati!

### Da fare:
- Riavviare VS Code
- Testare su Miracollo
- Documentare cosa funziona

---

## ⏭️ QUANDO RIPRENDI

1. Riavvia VS Code
2. Apri Miracollo
3. Prova: `/agents` per vedere se li vede
4. Prova: "Usa cervella-backend per elencare file Python"

---

## 📊 RIASSUNTO SESSIONE

| Metrica | Valore |
|---------|--------|
| Subagent creati | 4/4 ✅ |
| Verificati terminale | ✅ |
| Verificati VS Code | ⬜ (dopo riavvio) |
| Test su Miracollo | ⬜ |

---

*"Uno sciame di Cervelle. Quasi pronti per il volo!"* 🐝💙
