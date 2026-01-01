# SUB-ROADMAP: Sistema Logging & Monitoraggio

> **Creata:** 1 Gennaio 2026
> **Stato:** IN CORSO
> **Priorità:** ALTA - Blocca FASE 9 (Apprendimento)

---

## 🎯 OBIETTIVO

Avere un sistema di logging che:
1. **Funziona AUTOMATICAMENTE** - Zero intervento manuale
2. **Logga TUTTO** - Ogni agent, ogni task, ogni progetto
3. **Analizza in TEMPO REALE** - Dashboard, metriche, pattern
4. **Prepara per APPRENDIMENTO** - Dati per machine learning futuro

---

## 📍 STATO ATTUALE

```
╔══════════════════════════════════════════════════════════════════╗
║  COSA ABBIAMO:                                                   ║
║  ✅ Database SQLite (swarm_memory.db)                           ║
║  ✅ 10 script Python (analytics, query, suggestions, ecc.)      ║
║  ✅ Hook configurato in settings.json (SubagentStop!)           ║
║  ✅ log_event.py v1.2.0 (formato payload fixato)                ║
║                                                                  ║
║  🔴 SCOPERTA SESSIONE 30:                                        ║
║  PostToolUse = BUG CONFERMATO! (GitHub Issue #6305)             ║
║  SOLUZIONE: Usare SubagentStop invece!                          ║
║                                                                  ║
║  ✅ FIX APPLICATO: settings.json aggiornato                     ║
║  ⏳ ATTESA: Serve riavvio sessione per applicare                ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## 📋 FASI

### FASE A: Debug & Fix Hook (Priorità 1) ✅ QUASI COMPLETATA!

| # | Task | Stato | Note |
|---|------|-------|------|
| A.1 | Verificare che hook PostToolUse sia supportato per Task tool | ✅ DONE | **BUG CONFERMATO!** Issue #6305 |
| A.2 | Ricerca soluzione alternativa | ✅ DONE | **SubagentStop funziona!** |
| A.3 | Applicare fix in settings.json | ✅ DONE | PostToolUse → SubagentStop |
| A.4 | Testare hook in sessione NUOVA (dopo riavvio) | ⏳ WAITING | Serve riavvio Claude Code |
| A.5 | Verificare formato payload REALE | ⬜ TODO | Dopo test A.4 |
| A.6 | Rimuovere debug_hook.py quando funziona | ⬜ TODO | Pulizia finale |

**SCOPERTA IMPORTANTE:** PostToolUse hooks NON FUNZIONANO in Claude Code (bug confermato).
Soluzione: usare `SubagentStop` che è l'hook DEDICATO per subagent e FUNZIONA!

### FASE B: Test End-to-End (Priorità 2)

| # | Task | Stato | Note |
|---|------|-------|------|
| B.1 | Sessione test su CervellaSwarm | ⬜ TODO | Invocare 3-4 agent |
| B.2 | Verificare eventi loggati | ⬜ TODO | analytics.py events |
| B.3 | Sessione test su Miracollo | ⬜ TODO | Usare Swarm reale |
| B.4 | Verificare progetto corretto | ⬜ TODO | Deve dire "miracollo" |
| B.5 | Sessione test su Contabilità | ⬜ TODO | Completezza |

### FASE C: Migliorare Prompt Swarm (Priorità 3)

| # | Task | Stato | Note |
|---|------|-------|------|
| C.1 | Analizzare cosa manca nel prompt attuale | ⬜ TODO | PROMPT_SWARM_MODE.md |
| C.2 | Aggiungere contesto progetto | ⬜ TODO | Ogni progetto ha sue regole |
| C.3 | Collegare con sistema memoria | ⬜ TODO | load_context al SessionStart |
| C.4 | Definire quando usare Guardiane | ⬜ TODO | Regole chiare |
| C.5 | Testare nuovo prompt | ⬜ TODO | Sessione reale |

### FASE D: Dashboard & Monitoraggio (Priorità 4)

| # | Task | Stato | Note |
|---|------|-------|------|
| D.1 | Creare script `monitor.py` live | ⬜ TODO | Watch del database |
| D.2 | Notifiche Telegram per eventi critici | ⬜ TODO | Errori, fallimenti |
| D.3 | Report automatico fine sessione | ⬜ TODO | Cosa è stato fatto |
| D.4 | Grafici performance (opzionale) | ⬜ TODO | Rich o ASCII |

---

## 🔗 DIPENDENZE

```
FASE A ──→ FASE B ──→ FASE C
                  ╲
                   ──→ FASE D

A deve funzionare PRIMA di B
B e C possono essere parallele
D richiede B completata
```

---

## ⏱️ STIMA

| Fase | Complessità | Note |
|------|-------------|------|
| A | Media | Debug tecnico, potrebbe richiedere ricerca |
| B | Bassa | Solo test, già tutto pronto |
| C | Media | Design + test |
| D | Bassa | Nice-to-have, può aspettare |

---

## 🎯 CRITERIO DI SUCCESSO

```
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   SUCCESSO = Quando posso vedere:                               ║
║                                                                  ║
║   $ python3 scripts/memory/analytics.py events                  ║
║                                                                  ║
║   E vedo TUTTI gli agent che ho usato nella sessione,           ║
║   con progetto corretto, timestamp, e descrizione task.         ║
║                                                                  ║
║   SENZA dover fare NULLA manualmente!                           ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## 📝 NOTE

- **Approccio:** Calma, studio, un passo alla volta
- **Filosofia:** "Nulla è complesso - solo non ancora studiato!"
- **Obiettivo finale:** Sistema che funziona DA SOLO

---

*Creata: 1 Gennaio 2026 - Sessione 29*
*Aggiornata: 1 Gennaio 2026 - Sessione 30* - **BUG SCOPERTO + FIX APPLICATO!**

*"Con la mappa giusta, non ci perdiamo mai!"* 🗺️💙
*"Nulla è complesso - solo non ancora studiato!"* 🔬
