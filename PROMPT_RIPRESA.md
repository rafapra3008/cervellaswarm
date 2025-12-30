# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 30 Dicembre 2025, ore 09:15

---

## 🎯 STATO ATTUALE

**FASE 2: Primi Subagent** - 66% IN CORSO 🟡

### Cosa abbiamo fatto OGGI (Sessione 2):

1. ✅ **Creato cervella-frontend.md** - Specialista UI/React/CSS
2. ✅ **Creato cervella-backend.md** - Specialista Python/API
3. ✅ **Creato cervella-tester.md** - Specialista QA/Testing
4. ✅ **Creato cervella-reviewer.md** - Specialista Code Review

**Location:** `~/.claude/agents/` (globali, disponibili ovunque!)

### Prossimi step immediati:

1. ⬜ **Test su progetto reale** (Miracollo o Contabilità)
   - Invocare un subagent
   - Verificare che funzioni
   - Vedere come si comporta
2. ⬜ **Documentare risultati** - Cosa funziona, cosa no

---

## 📂 SUBAGENT CREATI

| File | Specializzazione | Model |
|------|------------------|-------|
| `cervella-frontend.md` | React, CSS, UI/UX, Responsive | sonnet |
| `cervella-backend.md` | Python, FastAPI, Database, API | sonnet |
| `cervella-tester.md` | pytest, Jest, E2E, Bug hunting | sonnet |
| `cervella-reviewer.md` | Code review, Best practices | sonnet |

**Come invocare:**
```
"Usa cervella-frontend per creare il componente"
"Chiedi a cervella-tester di verificare"
"Fai fare review a cervella-reviewer"
```

---

## 🧠 FILO DEL DISCORSO

### Stavamo ragionando su:
Abbiamo creato i 4 subagent fondamentali dello sciame. Ogni Cervella ha la sua specializzazione e le sue zone di competenza. Sono installati globalmente in `~/.claude/agents/` quindi funzionano in TUTTI i progetti.

### La decisione presa:
- Subagent globali (non per progetto) = più semplice da gestire
- Ogni subagent sa cosa PUÒ e cosa NON PUÒ toccare
- cervella-reviewer è SOLO lettura (non modifica)

### Il momentum:
🔥🔥🔥 ALTO! 4 subagent creati in 10 minuti!

### Da NON fare:
- ❌ Modificare i subagent senza testarli prima
- ❌ Creare altri subagent prima di validare questi
- ❌ Saltare il test su progetto reale

---

## ⏭️ QUANDO RIPRENDI

1. Leggi questo file
2. Vai su un progetto reale (Miracollo)
3. Prova a invocare un subagent
4. Documenta cosa succede

---

## 📊 RIASSUNTO SESSIONI

| Sessione | Data | Cosa Fatto |
|----------|------|------------|
| 1 | 30 Dic mattina | FASE 0+1 complete, studi, architettura |
| 2 | 30 Dic 09:10 | 4 subagent creati (FASE 2 al 66%) |

---

*"Uno sciame di Cervelle. Pronte per il test!"* 🐝💙
