# Task: Implementazione spawn-workers v3.2.0 - Unbuffered Output

**Assegnato a:** cervella-devops
**Sessione:** 124 (8 Gennaio 2026)
**Sprint:** 2 - Fix Buffering Output
**Priorità:** ALTA
**Stato:** ready

---

## 🎯 OBIETTIVO

Implementare **output realtime** in spawn-workers basandosi sui risultati della ricerca.

**PROBLEMA:**
- Output worker arriva in blocchi
- Non vediamo progresso in tempo reale
- Buffering nasconde cosa sta succedendo

**SOLUZIONE:**
Modificare spawn-workers v3.1.0 → v3.2.0 usando **stdbuf -oL** (raccomandazione ricerca).

---

## ⭐ RICERCA COMPLETATA - RACCOMANDAZIONE

**File ricerca:** `docs/studio/RICERCA_UNBUFFERED_OUTPUT.md` (1,045 righe!)
**Rating:** ⭐⭐⭐⭐⭐
**Raccomandazione:** `stdbuf -oL`

**Comando esatto:**
```bash
stdbuf -oL claude --append-system-prompt "$PROMPT_FILE"
```

**Motivazione:**
- Line-buffered perfetto per output Claude (righe complete)
- Performance ottimale (flush solo al \n)
- Compatibilità verificata con Claude
- Standard industry (Docker, K8s, CI/CD)

**Fallback plan:**
1. `stdbuf` (preferito)
2. `gstdbuf` (macOS coreutils con g-prefix)
3. `unbuffer` (expect package)
4. Warning + continue (degraded mode)

**Setup richiesto:**
```bash
brew install coreutils  # Se non già installato
```

---

## 📋 TASK SPECIFICI

### 1. Leggere Ricerca
- Leggere `docs/studio/RICERCA_UNBUFFERED_OUTPUT.md`
- Capire raccomandazione finale
- Identificare comando esatto da usare

### 2. Modificare spawn-workers
**File:** `scripts/swarm/spawn-workers` (attualmente v3.1.0)

**Modifiche da fare:**
- [x] Aggiungere flag unbuffered al comando claude
- [x] Testare compatibilità macOS
- [x] Aggiornare version string a v3.2.0
- [x] Aggiornare commenti con spiegazione
- [x] Verificare backward compatibility

**Linea da modificare (~400):**
```bash
# PRIMA (v3.1.0)
tmux send-keys -t "$SESSION_NAME" \
    "claude --append-system-prompt '$PROMPT_FILE'" Enter

# DOPO (v3.2.0) - CON stdbuf
tmux send-keys -t "$SESSION_NAME" \
    "$STDBUF_CMD claude --append-system-prompt '$PROMPT_FILE'" Enter
```

**Check availability (aggiungere all'inizio script):**
```bash
# Check stdbuf availability (linea ~50)
STDBUF_CMD=""
if command -v stdbuf &>/dev/null; then
    STDBUF_CMD="stdbuf -oL"
elif command -v gstdbuf &>/dev/null; then
    STDBUF_CMD="gstdbuf -oL"
elif command -v unbuffer &>/dev/null; then
    STDBUF_CMD="unbuffer"
    echo "⚠️  Using unbuffer (stdout+stderr merged)"
else
    echo "⚠️  WARNING: No unbuffer tool found. Output may be delayed."
    echo "   Install with: brew install coreutils"
fi
```

### 3. Test Locale
Prima di chiudere task, testare:
```bash
# Test base
spawn-workers --backend

# Verificare in altra finestra
tmux attach -t swarm_backend_[ID]
# Output dovrebbe essere realtime!

# Test capture
tmux capture-pane -t swarm_backend_[ID] -p
# Dovrebbe mostrare output progressivo
```

### 4. Documentazione
- Aggiornare commenti in spawn-workers
- Aggiungere note nella sezione CHANGELOG interno
- Spiegare PERCHÉ abbiamo usato questa soluzione

---

## 📤 OUTPUT ATTESO

1. **spawn-workers v3.2.0** con output realtime
2. **Test locale** eseguito e passato
3. **Note implementazione** nel commit message

**File da modificare:**
- `scripts/swarm/spawn-workers` (1 file)

**Versione:** v3.1.0 → v3.2.0

---

## ✅ CRITERI DI SUCCESSO

- [x] spawn-workers modificato correttamente
- [x] Version string aggiornata a v3.2.0
- [x] Test locale passato (output realtime)
- [x] Compatibilità macOS verificata
- [x] Backward compatibility mantenuta
- [x] Documentazione aggiornata
- [x] Pronto per HARDTEST (task 2.3)

---

## 🔗 CONTESTO

**File da leggere:**
- `docs/studio/RICERCA_UNBUFFERED_OUTPUT.md` (RICERCA COMPLETATA!)
- `scripts/swarm/spawn-workers` (current v3.1.0)

**Riferimento versioni:**
- v3.0.0: Flag --headless aggiunto
- v3.1.0: Headless diventa DEFAULT
- v3.2.0: Output realtime (questa implementazione!)

---

## 💡 NOTE

- ASPETTARE che Task 2.1 (ricerca) sia completata
- Implementare ESATTAMENTE la raccomandazione della ricerca
- Se ci sono dubbi, chiedere alla Regina
- Test locale PRIMA di chiudere task
- Pensare alla semplicità - minimal change, maximum impact

---

**Creato:** 8 Gennaio 2026 - Sessione 124
**Regina:** Cervella Orchestratrice
**Worker:** cervella-devops

*"Implementa con precisione, testa con fiducia!"* 🚀🔧
