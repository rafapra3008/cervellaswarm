# Task: Aggiornamento watcher-regina v1.6.0 - Live Output

**Assegnato a:** cervella-devops
**Sessione:** 124 (8 Gennaio 2026)
**Sprint:** 2 - Fix Buffering Output
**Priorità:** ALTA
**Stato:** waiting (dipende da Task 2.3 HARDTEST)

---

## 🎯 OBIETTIVO

Aggiornare watcher-regina per mostrare **progresso live** dei worker alla Regina.

**PROBLEMA ATTUALE:**
- watcher-regina notifica solo quando task è COMPLETATO (.done)
- Non sappiamo cosa sta facendo il worker MENTRE lavora
- La Regina aspetta al buio

**SOLUZIONE:**
Con output realtime da spawn-workers v3.2.0, possiamo mostrare progresso live!

---

## 📋 TASK SPECIFICI

### 1. Analizzare HARDTEST Risultati
- Leggere `docs/tests/HARDTEST_UNBUFFERED_OUTPUT_v124.md`
- Capire come funziona output realtime
- Identificare pattern di progresso

### 2. Modificare watcher-regina.sh
**File:** `scripts/swarm/watcher-regina.sh` (attualmente v1.5.0)

**Nuove funzionalità:**

#### A. Monitor Live Output (opzionale)
```bash
# Ogni 30s, mostra ultime 3 righe di ogni worker attivo
function show_worker_progress() {
  for session in $(tmux list-sessions | grep "^swarm_" | cut -d: -f1); do
    echo "📊 $session:"
    tmux capture-pane -t "$session" -p | tail -3
    echo ""
  done
}
```

#### B. Notifica Progresso Significativo
```bash
# Se worker scrive "✅" o "COMPLETATO" o milestone
# Notifica opzionale alla Regina (non invasiva)
```

#### C. Dashboard Live (se richiesto)
```bash
# Output continuo (opzionale con flag --live)
# Mostra stato tutti worker in tempo reale
```

### 3. Design Decisioni

**IMPORTANTE:** Non vogliamo SPAM!

Opzioni:
1. **Silenzioso** (default) - notifica solo .done come ora
2. **Progress** (flag --progress) - mostra stato ogni 60s
3. **Live** (flag --live) - dashboard continua

Scegliere approccio basandosi su:
- Filosofia "la magia nascosta"
- Non disturbare Regina se non serve
- Ma dare visibilità se richiesta

### 4. Implementazione
- Aggiornare version string a v1.6.0
- Aggiungere nuove funzioni
- Testare con worker reali
- Aggiornare help/usage

### 5. Test Locale
```bash
# Test modalità default (silenzioso)
spawn-workers --researcher --auto-sveglia
# Deve comportarsi come v1.5.0

# Test modalità progress
spawn-workers --researcher --auto-sveglia --progress
# Deve mostrare aggiornamenti ogni 60s

# Test modalità live (se implementata)
spawn-workers --researcher --auto-sveglia --live
# Dashboard continua
```

---

## 📤 OUTPUT ATTESO

1. **watcher-regina.sh v1.6.0** con nuove funzionalità
2. **Test locale** passato (3 modalità)
3. **Documentazione** aggiornata

**File da modificare:**
- `scripts/swarm/watcher-regina.sh` (1 file)

**Versione:** v1.5.0 → v1.6.0

**Nuove features:**
- Modalità progress (opzionale)
- Modalità live (opzionale se ha senso)
- Backward compatible (default = v1.5.0 behavior)

---

## ✅ CRITERI DI SUCCESSO

- [x] watcher-regina.sh modificato
- [x] Version string v1.6.0
- [x] Almeno 1 nuova modalità implementata
- [x] Default behavior inalterato (backward compatible)
- [x] Test locale passato
- [x] Non invade/disturba se non richiesto
- [x] Help aggiornato con nuove opzioni
- [x] Pronto per uso quotidiano

---

## 🔗 CONTESTO

**File da leggere:**
- `docs/tests/HARDTEST_UNBUFFERED_OUTPUT_v124.md` (test v3.2.0)
- `scripts/swarm/watcher-regina.sh` (current v1.5.0)
- `scripts/swarm/spawn-workers` (v3.2.0 con unbuffered)

**Filosofia:**
- "La magia nascosta" - non disturbare se non serve
- "Visibilità quando richiesta" - opzioni per chi vuole vedere
- "Fiducia nel sistema" - default silenzioso = fiducia

**Versioni:**
- v1.0.0: Watcher base (Sessione 95)
- v1.5.0: Feedback + stuck detection
- v1.6.0: Live output (questa implementazione!)

---

## 💡 NOTE

- ASPETTARE che Task 2.3 (HARDTEST) sia completato
- Basarsi su risultati HARDTEST per decidere implementazione
- Pensare all'esperienza Regina:
  - Quando vuole vedere progresso? (casi d'uso)
  - Quando preferisce aspettare silenziosamente?
- Mantenere semplicità - non over-engineer
- Se in dubbio, chiedere alla Regina

**DOMANDA CHIAVE:** Che esperienza vogliamo per la Regina?
- Sempre informata? (live)
- Informata periodicamente? (progress)
- Informata solo al completamento? (default)

Scegliere basandosi su HARDTEST e filosofia "magia nascosta".

---

**Creato:** 8 Gennaio 2026 - Sessione 124
**Regina:** Cervella Orchestratrice
**Worker:** cervella-devops

*"Informare senza disturbare, mostrare senza invadere!"* 🔔✨
