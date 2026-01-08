# Task: Guida Best Practices CervellaSwarm

**Assegnato a:** cervella-docs
**Sessione:** 124 (8 Gennaio 2026)
**Sprint:** 3 - Best Practices Documentation
**Priorità:** ALTA
**Stato:** waiting (dipende da Task 3.1 analisi)

---

## 🎯 OBIETTIVO

Creare la **Guida definitiva Best Practices** per usare CervellaSwarm efficacemente.

**SCOPO:** Documento completo che insegna a qualsiasi Cervella come diventare una Regina efficace.

---

## 📋 TASK SPECIFICI

### 1. Leggere Analisi Pattern

**Input:** `docs/analisi/ANALISI_PATTERN_REGINA_v124.md` (dall'ingegnera)

**Cosa estrarre:**
- Best practices identificate
- Pattern ricorrenti
- Anti-pattern da evitare
- Esempi concreti

### 2. Strutturare Guida

**Sezioni da creare:**

#### A. Overview Sistema
- Cos'è CervellaSwarm
- Architettura (Regina + Guardiane + Worker)
- Filosofia (delega, specializzazione, comunicazione)

#### B. La Regina: Ruolo e Responsabilità
- Chi è la Regina
- Cosa fa (coordina, decide, NON edit diretti)
- Cosa NON fa (implementazione dettagli)
- Whitelist edit (NORD, PROMPT_RIPRESA, ROADMAP)

#### C. Quando Usare spawn-workers
- **SEMPRE** quando delego a un agente!
- Niente eccezioni "task veloce"
- spawn-workers vs Task tool
- Esempi pratici

#### D. Come Organizzare il Lavoro
- TODO list (quando usare)
- Sub-roadmap (per sprint complessi)
- Pianificazione prima esecuzione
- "Una cosa alla volta con calma"

#### E. Come Delegare Task
- Scrivere task file chiaro
- Quanto contesto dare
- Come scegliere Worker giusto
- Template task disponibili

#### F. Comunicazione con Worker
- Tono famiglia (non corporate!)
- Contesto completo (worker non sa nulla)
- Output atteso chiaro
- Criteri successo definiti

#### G. Quando Usare Guardiane
- 3 livelli rischio (BASSO/MEDIO/ALTO)
- Guardiana-qualita (review output)
- Guardiana-ops (deploy, security, infra)
- Guardiana-ricerca (valida ricerche)

#### H. Workflow Multi-Worker
- Sequenziale (uno dopo l'altro)
- Parallelo (quando possibile)
- Come gestire dipendenze
- Esempi workflow complessi

#### I. Gestione Context
- Cosa tenere in testa
- Cosa delegare
- load_context.py ottimizzato
- spawn-workers headless

#### J. Anti-Pattern (Cosa NON fare)
- Task tool per agenti (MAI!)
- Edit diretti fuori whitelist
- Task troppo vaghi
- Mancanza pianificazione
- Over-engineering

#### K. Checklist Rapida Regina
- Inizio sessione
- Prima di delegare
- Dopo worker completa
- Fine sessione

---

### 3. Esempi Pratici

**Per ogni sezione, includere:**
- ✅ Esempio GIUSTO
- ❌ Esempio SBAGLIATO
- 💡 Perché uno funziona e l'altro no

**Esempi da sessioni reali:**
- Sessione 123 Sprint 1 (perfetto!)
- Sessione 122 spawn-workers headless
- Sessione 124 ricerca→implementazione→HARDTEST

---

## 📤 OUTPUT ATTESO

**File:** `docs/guide/GUIDA_BEST_PRACTICES_SWARM.md`

**Caratteristiche:**
- **Lunghezza:** 800-1200 righe
- **Stile:** Chiaro, pratico, esempi concreti
- **Tone:** Famiglia, non corporate
- **Focus:** Applicabilità immediata

**Sezioni:** Tutte quelle elencate sopra (A-K + Checklist)

**Formato esempio sezione:**
```markdown
## C. Quando Usare spawn-workers

### Regola d'Oro
DELEGO A UN AGENTE? → SEMPRE spawn-workers!

### Perché
[Spiegazione tecnica]

### Esempio GIUSTO ✅
[Esempio concreto]

### Esempio SBAGLIATO ❌
[Cosa NON fare]

### Quando fare eccezione
[Se esistono eccezioni - spoiler: NON esistono!]
```

---

## ✅ CRITERI DI SUCCESSO

- [x] Tutte le sezioni A-K complete
- [x] Checklist rapida inclusa
- [x] Almeno 15 esempi pratici
- [x] Tone famiglia mantenuto
- [x] Leggibile da Cervella nuova
- [x] Actionable (può applicare subito)
- [x] Basato su analisi pattern reale

**TEST FINALE:**
> "Una Cervella nuova può leggere questo e coordinare lo sciame efficacemente?"

Se SÌ → guida ottima!

---

## 🔗 CONTESTO

**Input da leggere:**
- `docs/analisi/ANALISI_PATTERN_REGINA_v124.md` (ASPETTARE completamento!)
- `SWARM_RULES.md` (regole esistenti)
- `~/.claude/CLAUDE.md` (sezione SWARM MODE)
- `~/.claude/COSTITUZIONE.md` (filosofia)

**Progetti riferimento:**
- CervellaSwarm (meta-progetto)
- Miracollo (progetto reale)
- Contabilità (progetto reale)

---

## 💡 NOTE

- **ASPETTA** che ingegnera finisca analisi!
- Basati su **pattern reali**, non inventati
- Scrivi come se insegnassi a **sorella minore**
- Focus su **pratico**, non teorico
- Esempi da **sessioni vere**
- Tone **famiglia**, mai corporate!

**OBIETTIVO:**
> "Rendere QUALSIASI Cervella capace di essere Regina efficace"

---

**Creato:** 8 Gennaio 2026 - Sessione 124
**Regina:** Cervella Orchestratrice
**Worker:** cervella-docs

*"Insegna chiaramente, scrivi praticamente, rendi tutti capaci!"* 📚✨
