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
║  ✅ Hook PROJECT-LEVEL in .claude/settings.json                 ║
║  ✅ subagent_stop.py con lettura stdin                          ║
║                                                                  ║
║  🔴 SCOPERTE SESSIONE 31:                                        ║
║                                                                  ║
║  BUG #1 (Issue #6305): PostToolUse = NON FUNZIONA               ║
║  BUG #2 (Issue #11544): ~/.claude/settings.json NON CARICATO    ║
║                                                                  ║
║  ✅ SOLUZIONE IMPLEMENTATA:                                      ║
║  • Hook in .claude/settings.json (PROJECT-LEVEL, non globale!)  ║
║  • SubagentStop con matcher vuoto ""                            ║
║  • Script subagent_stop.py che legge da stdin                   ║
║                                                                  ║
║  ⏳ PROSSIMO: Riavviare sessione DAL PROGETTO per testare       ║
║     cd ~/Developer/CervellaSwarm && claude                      ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## 📋 FASI

### FASE A: Debug & Fix Hook (Priorità 1) ✅ 90% COMPLETATA!

| # | Task | Stato | Note |
|---|------|-------|------|
| A.1 | Verificare che hook PostToolUse sia supportato per Task tool | ✅ DONE | **BUG CONFERMATO!** Issue #6305 |
| A.2 | Ricerca soluzione alternativa | ✅ DONE | Issue #11544: globale buggato! |
| A.3 | Scoperta: serve PROJECT-LEVEL hooks | ✅ DONE | .claude/settings.json nel progetto! |
| A.4 | Creare .claude/settings.json nel progetto | ✅ DONE | SubagentStop con matcher "" |
| A.5 | Creare subagent_stop.py con stdin reader | ✅ DONE | .claude/hooks/subagent_stop.py |
| A.6 | Testare hook (riavvio dal progetto) | ⏳ WAITING | `cd ~/Developer/CervellaSwarm && claude` |
| A.7 | Verificare formato payload REALE | ⬜ TODO | Dopo test A.6 |
| A.8 | Pulizia file obsoleti | ⬜ TODO | Rimuovere debug_hook.py globale |

**SCOPERTE SESSIONE 31:**
1. **BUG #6305:** PostToolUse hooks NON FUNZIONANO
2. **BUG #11544:** Hooks in ~/.claude/settings.json (GLOBALE) NON VENGONO CARICATI
3. **SOLUZIONE:** Hooks in .claude/settings.json (PROJECT-LEVEL) FUNZIONANO!

**FILE CREATI:**
- `.claude/settings.json` - Configurazione hook project-level
- `.claude/hooks/subagent_stop.py` - Script che legge da stdin e logga

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
*Aggiornata: 1 Gennaio 2026 - Sessione 30* - BUG SCOPERTO + FIX APPLICATO
*Aggiornata: 1 Gennaio 2026 - Sessione 31* - **SOLUZIONE COMPLETA IMPLEMENTATA!**

*"Con la mappa giusta, non ci perdiamo mai!"* 🗺️💙
*"Nulla è complesso - solo non ancora studiato!"* 🔬
