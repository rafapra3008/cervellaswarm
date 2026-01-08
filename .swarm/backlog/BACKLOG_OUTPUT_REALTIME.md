# BACKLOG: Output Realtime Worker

**Data creata:** 8 Gennaio 2026 - Sessione 124
**Priorità:** BASSA (futuro)
**Stato:** RICERCA NECESSARIA

---

## CONTESTO

Durante Sprint 2 (Fix Buffering Output) abbiamo scoperto:
- `stdbuf -oL` implementato perfettamente ✅
- MA `claude -p` NON produce output progressivo ❌
- Output arriva solo al completamento

**HARDTEST Rating:** 4/10 - implementazione corretta ma obiettivo non raggiunto

---

## RICERCHE DA FARE (FUTURO)

1. **Claude CLI Output Modes**
2. **Alternative CLI** 
3. **Heartbeat Pattern**

---

## PERCHÉ BACKLOG

**Sistema funziona perfettamente:**
- ✅ Watcher rileva .done (3s delay)
- ✅ Worker completano task
- ✅ Sciame operativo 100%

**Nice to have, non must have.**

---

*"Focus su cose più importanti!" - Rafa, 8 Gennaio 2026*
