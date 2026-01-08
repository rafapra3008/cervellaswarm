# Task: Ricerca Tecnica Unbuffered Output

**Assegnato a:** cervella-researcher
**Sessione:** 124 (8 Gennaio 2026)
**Sprint:** 2 - Fix Buffering Output
**Priorità:** ALTA
**Stato:** ready

---

## 🎯 OBIETTIVO

Ricerca tecnica approfondita su come ottenere **output realtime** dai worker.

**PROBLEMA ATTUALE:**
- Output worker arriva in blocchi, non realtime
- Non vediamo cosa sta facendo MENTRE lavora
- Buffering nasconde il progresso

**SOLUZIONE DA STUDIARE:**
- `stdbuf -oL` per unbuffered output
- Come tmux gestisce output buffering
- Best practices Python logging realtime
- Altri tool/tecniche per output immediato

---

## 📋 TASK SPECIFICI

1. **Studiare stdbuf**
   - Come funziona stdbuf -oL
   - Differenza tra -oL, -o0, line buffering vs unbuffered
   - Compatibilità macOS vs Linux
   - Limitazioni conosciute

2. **Analizzare tmux output**
   - Come tmux bufferizza output
   - `tmux capture-pane` - opzioni e comportamento
   - Differenza tra tmux buffer e terminal buffer
   - Best practices per log realtime in tmux

3. **Python logging realtime**
   - sys.stdout.flush()
   - logging handlers (StreamHandler vs FileHandler)
   - PYTHONUNBUFFERED environment variable
   - Best practices per output immediato

4. **Altri approcci**
   - Esistono alternative a stdbuf?
   - Tool moderni per log streaming
   - Confronto con tail -f
   - Pro/contro di ogni approccio

5. **Ricerca Best Practices**
   - Come fanno i framework moderni (Docker, Kubernetes)
   - Pattern industry standard per worker output
   - Cosa fanno competitors (GitHub Actions, etc.)

---

## 📤 OUTPUT ATTESO

**File:** `docs/studio/RICERCA_UNBUFFERED_OUTPUT.md`

**Sezioni richieste:**
1. Overview del problema buffering
2. Spiegazione tecnica stdbuf (con esempi)
3. Analisi tmux output management
4. Python logging realtime (best practices)
5. Approcci alternativi (se esistono)
6. Confronto soluzioni (tabella pro/contro)
7. **RACCOMANDAZIONE FINALE** con motivazione tecnica
8. Esempio pratico comando per spawn-workers
9. Test da fare per validare (preparazione HARDTEST)

**Lunghezza:** 400-800 righe (ricerca approfondita!)

**Stile:**
- Tecnico ma chiaro
- Esempi pratici
- Pro/contro di ogni opzione
- Fonti quando possibile

---

## ✅ CRITERI DI SUCCESSO

- [x] File RICERCA_UNBUFFERED_OUTPUT.md creato
- [x] Tutte le sezioni richieste presenti
- [x] Raccomandazione finale chiara e motivata
- [x] Esempi pratici inclusi
- [x] Test per HARDTEST preparati
- [x] Regina può implementare basandosi su questa ricerca

---

## 🔗 CONTESTO

**Da leggere prima:**
- `scripts/swarm/spawn-workers` (current version 3.1.0)
- `scripts/swarm/watcher-regina.sh` (v1.5.0)
- `docs/roadmap/SUB_ROADMAP_CONSOLIDAMENTO_v123.md` (Sprint 2)

**Lezione correlata:**
Database memoria ha lezione #11: "Output Buffering Blocca Log"

**Riferimento:**
```bash
# Current command in spawn-workers (line ~180)
claude --append-system-prompt "$PROMPT_FILE"

# Dobbiamo aggiungere qualcosa tipo:
stdbuf -oL claude --append-system-prompt "$PROMPT_FILE"
```

---

## 💡 NOTE

- Questa è ricerca TECNICA, non implementazione
- Focalizza su COSA fare e PERCHÉ
- La cervella-devops implementerà dopo
- Pensa al NOSTRO caso d'uso specifico (macOS, tmux, claude)

---

**Creato:** 8 Gennaio 2026 - Sessione 124
**Regina:** Cervella Orchestratrice
**Worker:** cervella-researcher

*"Studia profondamente, raccomanda chiaramente!"* 🔬📚
