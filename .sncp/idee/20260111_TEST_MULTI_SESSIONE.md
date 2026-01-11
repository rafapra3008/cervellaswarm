# TEST MULTI-SESSIONE - Piano di Test

> **Data:** 11 Gennaio 2026
> **Obiettivo:** Validare sistema multi-sessione PRIMA di usarlo su progetti reali

---

## PERCHÉ TEST FUORI PROGETTO

```
+==================================================================+
|                                                                  |
|   "Fatto BENE > Fatto VELOCE"                                   |
|                                                                  |
|   Testiamo su progetto FAKE per:                                |
|   1. Zero rischio su Miracollo/CervellaSwarm                    |
|   2. Capire se script funzionano                                |
|   3. Identificare problemi prima che siano critici              |
|   4. Imparare il workflow senza pressione                       |
|                                                                  |
+==================================================================+
```

---

## SETUP TEST

### Creare Progetto Test

```bash
# Crea cartella test
mkdir -p ~/Developer/test-multi-sessione
cd ~/Developer/test-multi-sessione

# Inizializza git
git init
git checkout -b main

# Crea struttura fake
mkdir -p backend frontend tests
echo "# Test Multi-Sessione" > README.md
echo "print('backend')" > backend/app.py
echo "console.log('frontend');" > frontend/app.js
echo "def test(): pass" > tests/test_all.py

# Commit iniziale
git add -A
git commit -m "Initial commit - test project"
```

### Creare Sessione Parallela

```bash
# Usa lo script
~/Developer/CervellaSwarm/scripts/create-parallel-session.sh \
    ~/Developer/test-multi-sessione \
    test-parallel \
    backend frontend
```

---

## SCENARI DI TEST

### TEST 1: Task Indipendenti (Semplice)

**Obiettivo:** Verificare che 2 worker possono lavorare in parallelo senza dipendenze

```
WORKER 1 (backend):
- Modifica backend/app.py
- Aggiungi funzione hello()
- Commit
- create-signal.sh TASK-001 success "Added hello function"

WORKER 2 (frontend):
- Modifica frontend/app.js
- Aggiungi funzione greet()
- Commit
- create-signal.sh TASK-002 success "Added greet function"

REGINA:
- Verifica entrambi i segnali
- Merge
- Verifica nessun conflitto
```

**Risultato atteso:** Merge senza conflitti, entrambe le modifiche presenti

---

### TEST 2: Task con Dipendenze

**Obiettivo:** Verificare che wait-for-dependencies funziona

```
WORKER 1 (backend):
- Lavora per 2 minuti (simula lavoro)
- Commit
- create-signal.sh TASK-001 success "API ready"

WORKER 2 (frontend):
- Esegue: wait-for-dependencies.sh TASK-002
- DEVE ASPETTARE finché TASK-001 non è pronto
- Quando segnale arriva, inizia
- Commit
- create-signal.sh TASK-002 success "UI ready"

REGINA:
- Osserva che frontend ha aspettato
- Merge in ordine
```

**Risultato atteso:** Frontend attende, poi parte quando backend finisce

---

### TEST 3: Conflitto Intenzionale

**Obiettivo:** Verificare cosa succede se entrambi modificano stesso file

```
WORKER 1 (backend):
- Modifica README.md riga 1

WORKER 2 (frontend):
- Modifica README.md riga 1 (DIVERSO!)

REGINA:
- Tenta merge
- DEVE FALLIRE con conflitto
- Risolvi manualmente
```

**Risultato atteso:** Conflitto rilevato, risoluzione manuale necessaria

---

### TEST 4: SNCP Separato

**Obiettivo:** Verificare che ogni worker scrive nel suo file SNCP

```
SETUP:
mkdir -p .sncp/sessioni_parallele/test-parallel/

WORKER 1:
- Scrive in .sncp/sessioni_parallele/test-parallel/backend.md
- "Decisione: uso FastAPI"

WORKER 2:
- Scrive in .sncp/sessioni_parallele/test-parallel/frontend.md
- "Decisione: uso React"

REGINA:
- Verifica entrambi i file esistono
- Nessuna sovrascrittura
```

**Risultato atteso:** Due file separati con contenuti corretti

---

### TEST 5: Failure e Recovery

**Obiettivo:** Verificare gestione errori

```
WORKER 1:
- create-signal.sh TASK-001 failure "Build failed"

WORKER 2:
- wait-for-dependencies.sh TASK-002
- DEVE vedere che dipendenza ha fallito
- NON deve procedere

REGINA:
- Vede failure
- Decide: retry o abort
```

**Risultato atteso:** Sistema gestisce failure correttamente

---

## CHECKLIST TEST

```
TEST 1 - Task Indipendenti:
[ ] Script create-parallel-session.sh funziona
[ ] Worktrees creati correttamente
[ ] Worker possono lavorare in parallelo
[ ] create-signal.sh funziona
[ ] Merge senza conflitti
[ ] Cleanup funziona

TEST 2 - Dipendenze:
[ ] check-dependencies.sh funziona
[ ] wait-for-dependencies.sh aspetta
[ ] Segnale rileva dipendenza soddisfatta
[ ] Timeout funziona

TEST 3 - Conflitti:
[ ] Merge rileva conflitto
[ ] Risoluzione manuale possibile

TEST 4 - SNCP:
[ ] Struttura creata
[ ] File separati per worker
[ ] Nessuna sovrascrittura

TEST 5 - Failure:
[ ] Failure segnalato
[ ] Dipendenti vedono failure
[ ] Recovery possibile
```

---

## COMANDI TEST RAPIDI

```bash
# Verifica prerequisiti
which fswatch  # Deve esistere
which jq       # Deve esistere
git --version  # >= 2.20

# Crea progetto test
mkdir -p ~/Developer/test-multi-sessione && cd ~/Developer/test-multi-sessione
git init && echo "test" > README.md && git add -A && git commit -m "init"

# Crea sessione
~/Developer/CervellaSwarm/scripts/create-parallel-session.sh . test1 backend frontend

# Verifica struttura
ls -la .swarm/
ls -la .swarm/segnali/
ls -la .swarm/dipendenze/

# Test segnale
~/Developer/CervellaSwarm/scripts/create-signal.sh TASK-001 success "test"
cat .swarm/segnali/TASK-001-complete.signal.json

# Test dipendenze
~/Developer/CervellaSwarm/scripts/check-dependencies.sh TASK-001
~/Developer/CervellaSwarm/scripts/check-dependencies.sh TASK-002

# Cleanup test
cd .. && rm -rf test-multi-sessione
```

---

## DOPO IL TEST

```
SE TUTTI I TEST PASSANO:
1. Documenta eventuali fix necessari
2. Aggiorna protocollo se serve
3. Siamo pronti per usarlo su progetti reali!

SE QUALCHE TEST FALLISCE:
1. Documenta il problema
2. Fix lo script
3. Ri-testa
4. Non usare su progetti reali finché non passa tutto
```

---

*Test plan creato: 11 Gennaio 2026*
*"Prima testa, poi usa!"*
