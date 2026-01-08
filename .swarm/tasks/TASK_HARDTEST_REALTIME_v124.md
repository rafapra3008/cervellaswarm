# Task: HARDTEST Output Realtime v3.2.0

**Assegnato a:** cervella-tester
**Sessione:** 124 (8 Gennaio 2026)
**Sprint:** 2 - Fix Buffering Output
**Priorità:** ALTA
**Stato:** waiting (dipende da Task 2.2 implementazione)

---

## 🎯 OBIETTIVO

Testare che spawn-workers v3.2.0 produce **output realtime** senza buffering.

**COSA TESTIAMO:**
- Output worker arriva in tempo reale (< 2s delay)
- tmux capture-pane mostra log progressivi
- Nessuna perdita di informazioni
- Compatibilità con watcher-regina

---

## 📋 HARDTEST SCENARIO

### Test 1: Output Realtime Base
**Setup:**
```bash
# Spawna worker con task semplice
spawn-workers --docs

# Task: Scrivere FAQ con 5 sezioni
# Ogni sezione = ~30 secondi lavoro
```

**Verifica:**
```bash
# In loop ogni 2 secondi per 3 minuti
for i in {1..90}; do
  echo "=== Check $i ($(date +%H:%M:%S)) ==="
  tmux capture-pane -t swarm_docs_* -p | tail -5
  sleep 2
done > hardtest_output_realtime.log
```

**Criteri successo:**
- [ ] Output cambia OGNI 2 secondi (non solo alla fine)
- [ ] Vediamo progresso incrementale
- [ ] Nessun blocco di 30+ secondi senza output

---

### Test 2: Cattura Completa

**Setup:**
Stesso worker del Test 1

**Verifica:**
```bash
# Cattura TUTTO l'output dopo completamento
tmux capture-pane -t swarm_docs_* -p -S - > hardtest_full_capture.log

# Analizza
wc -l hardtest_full_capture.log
grep -c "Tool:" hardtest_full_capture.log
grep -c "assistant:" hardtest_full_capture.log
```

**Criteri successo:**
- [ ] File contiene TUTTO l'output
- [ ] Nessuna linea mancante
- [ ] Tool calls visibili
- [ ] Risposte assistant visibili

---

### Test 3: Comparazione v3.1.0 vs v3.2.0

**Setup:**
```bash
# Checkout v3.1.0 temporaneamente
git stash
git checkout [commit v3.1.0]

# Test worker
spawn-workers --backend
# Task identico (es: analisi file grande)

# Torna a v3.2.0
git checkout -
git stash pop

# Test worker
spawn-workers --backend
# Stesso task identico
```

**Comparazione:**
- Tempo primo output: v3.1.0 vs v3.2.0
- Frequenza output: ogni quanti secondi?
- Completezza: stesse righe?

**Criteri successo:**
- [ ] v3.2.0 ha output più frequente
- [ ] v3.2.0 primo output < 5s
- [ ] v3.2.0 mantiene completezza

---

### Test 4: Stress Test - Worker Multipli

**Setup:**
```bash
# Spawna 3 worker contemporaneamente
spawn-workers --backend --frontend --tester

# Task identici per tutti (es: analisi ROADMAP_SACRA.md)
```

**Verifica:**
```bash
# Monitora tutti e 3
for session in swarm_backend_* swarm_frontend_* swarm_tester_*; do
  echo "=== $session ==="
  tmux capture-pane -t "$session" -p | tail -3
done
```

**Criteri successo:**
- [ ] Tutti e 3 worker output realtime
- [ ] Nessuna interferenza tra sessioni
- [ ] tmux gestisce correttamente multipli

---

### Test 5: Watcher Integration

**Setup:**
```bash
# Spawna worker con auto-sveglia
spawn-workers --researcher --auto-sveglia

# Task veloce (5 minuti)
```

**Verifica:**
- Watcher rileva .done correttamente?
- Notifica arriva quando completato?
- Output finale è completo?

**Criteri successo:**
- [ ] Watcher notifica alla fine
- [ ] Notifica tempestiva (< 10s da .done)
- [ ] Output completo disponibile

---

## 📤 OUTPUT ATTESO

**File da creare:**
```
docs/tests/HARDTEST_UNBUFFERED_OUTPUT_v124.md
```

**Struttura:**
1. Setup ambiente
2. Test 1 risultati (con timestamps!)
3. Test 2 risultati (analisi completezza)
4. Test 3 risultati (comparazione)
5. Test 4 risultati (stress test)
6. Test 5 risultati (watcher)
7. **RATING FINALE**: X/10
8. **RACCOMANDAZIONE**: APPROVA / RICHIEDE FIX

**Allegati:**
- `hardtest_output_realtime.log`
- `hardtest_full_capture.log`
- Screenshots (se utili)

---

## ✅ CRITERI DI SUCCESSO OVERALL

- [x] Tutti i 5 test eseguiti
- [x] Almeno 4/5 test PASS
- [x] Rating finale ≥ 9/10
- [x] Output realtime verificato
- [x] Nessuna regressione identificata
- [x] Raccomandazione APPROVA

---

## 🔗 CONTESTO

**File da leggere:**
- `docs/studio/RICERCA_UNBUFFERED_OUTPUT.md` (ricerca)
- `scripts/swarm/spawn-workers` (v3.2.0 implementato)
- `docs/roadmap/SUB_ROADMAP_CONSOLIDAMENTO_v123.md` (Sprint 2)

**Versioni:**
- v3.1.0: Baseline (buffered)
- v3.2.0: Target (unbuffered)

---

## 💡 NOTE

- ASPETTARE che Task 2.2 (implementazione) sia completata
- Test REALI, non simulati
- Timestamps importanti per verificare realtime
- Se test falliscono: documentare PERCHÉ
- La Regina decide se approvare basandosi su questi test

---

**Creato:** 8 Gennaio 2026 - Sessione 124
**Regina:** Cervella Orchestratrice
**Worker:** cervella-tester

*"Testa tutto, dubita di nulla, valida con precisione!"* 🧪✅
