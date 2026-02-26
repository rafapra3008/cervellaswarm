# SUBROADMAP - Context Optimization v2

> **Creata:** 26 Febbraio 2026 - Sessione 404
> **Predecessore:** SUBROADMAP_CONTEXT_OPTIMIZATION.md (S307) + SUBROADMAP_CONTEXT_DURANTE_LAVORO.md (S308)
> **Fonti:** Analisi Ingegnera S404 + Audit Guardiana S404 (9.0/10)
> **Score target:** 9.5/10 per ogni step (audit Guardiana)
> **Filosofia:** "Ogni token conta. Context intelligente > Context grande."

---

## IL PROBLEMA (Aggiornato S404)

```
+================================================================+
|   ATTUALE (S404):                                               |
|   - Sessione tipica: ~20,200 token di "overhead"               |
|   - Sessione intensiva: ~41,800 token (21% del context 200K)   |
|   - MEMORY.md: ~350 token caricati AUTO in OGNI messaggio       |
|                                                                  |
|   TARGET:                                                        |
|   - Sessione tipica: ~14,000 token (-30%)                       |
|   - Sessione intensiva: ~27,000 token (-35%)                    |
|   - MEMORY.md: ~200 token/messaggio (-43%)                      |
|                                                                  |
|   VINCOLO ASSOLUTO: ZERO perdita qualita!                       |
+================================================================+
```

### Evoluzione dal v1 (S307)

| Aspetto | v1 (S307) | v2 (S404) |
|---------|-----------|-----------|
| Analisi | Quick audit | Ingegnera deep + Guardiana audit |
| File analizzati | 5 | 11 |
| Proposte | 4 fasi generiche | 9 proposte specifiche, riga per riga |
| Ridondanze mappate | ~3 | ~8 (con righe precise) |
| Verdetto Guardiana | N/A | 9.0/10 APPROVED |

---

## PRINCIPI

1. **STUDIO prima, IMPLEMENTAZIONE dopo** - ogni step inizia con lettura e verifica
2. **Guardiana audit dopo ogni step** - standard 9.5/10
3. **COSTITUZIONE INTATTA** - MAI modificare il file originale (condizione Guardiana)
4. **Regole Critiche MEMORY.md sacre** - 5 lezioni da bug reali MAI eliminate
5. **Rischio NULLO prima** - ordine: sicuro -> con cura -> con test

---

## FASE 1: QUICK WINS - Rischio NULLO (1 sessione)

> Implementare i 4 cambiamenti a rischio zero.
> Nessun file "sacro" toccato. Solo rimozione duplicati e aggiunta indici.

### Step 1.1: Indice MANUALE_DIAMANTE (P7)

**Problema:** ~1,180 righe, se letto intero = ~7,900 token sprecati.
**Soluzione:** Aggiungere line ranges all'indice esistente.
**File:** `~/.claude/MANUALE_DIAMANTE.md`
**Effort:** 10 minuti
**Rischio:** NULLO

**Criterio completamento:**
- [ ] Indice con line ranges precisi
- [ ] Nota "Leggere solo la sezione rilevante con parametro offset/limit"
- [ ] Guardiana verifica

---

### Step 1.2: Dedup CervellaSwarm/CLAUDE.md (P2)

**Problema:** 78 righe, ripete SNCP structure + spawn-workers + progetti gia nel globale.
**Soluzione:** Ridurre a ~40 righe con solo info uniche del progetto.
**File:** `~/Developer/CervellaSwarm/CLAUDE.md`
**Effort:** 20 minuti
**Rischio:** BASSO

**Cosa MANTENERE (unica e critica):**
- DUAL REPO regola sacra (box ASCII incluso - errore ricorrente!)
- Hook attivi CervellaSwarm (tabella 3 righe)
- La Famiglia (composizione)
- File Chiave (NORD, MASTER, roadmaps)
- SNCP 4.0 nota

**Cosa RIMUOVERE (duplicata):**
- Albero SNCP (gia in CLAUDE.md globale)
- spawn-workers comandi (gia in CLAUDE.md globale)
- Progetti collegati (gia in CLAUDE.md globale)

**Criterio completamento:**
- [ ] File <= 45 righe
- [ ] Dual Repo box INTATTO
- [ ] Guardiana verifica zero info perse

---

### Step 1.3: Snellire MEMORY.md (P5)

**Problema:** 115 righe caricate AUTO in OGNI messaggio. Contiene duplicati.
**Soluzione:** Ridurre a ~50 righe con solo info UNICHE.
**File:** `~/.claude-insiders/projects/-Users-rafapra-Developer-CervellaSwarm/memory/MEMORY.md`
**Effort:** 30 minuti
**Rischio:** BASSO

**Cosa MANTENERE (unica, NON esiste altrove):**
- LA MISSIONE (righe 3-15) - principio fondante
- Regole Critiche (righe 29-50) - 5 lezioni da BUG REALI:
  - Package Shadowing Fix (S340)
  - Content Scanner Rule (S363-S367)
  - Agent Model Anti-Downgrade (S361)
  - Tester Agent File Size
  - Dual Repo
- Detail Files indice (righe 82-90) - navigazione memoria
- 1 riga: "Per stato corrente: leggi PROMPT_RIPRESA_cervellaswarm.md"

**Cosa RIMUOVERE (duplicata):**
- Stato Attuale S403 (identico a PROMPT_RIPRESA)
- 9 Packages Summary (identica a PROMPT_RIPRESA)
- Test Suite (gia in PROMPT_RIPRESA)
- Progetti Collegati (gia in CLAUDE.md globale)
- Open Source Strategy (gia in PROMPT_RIPRESA)

**Criterio completamento:**
- [ ] File <= 55 righe
- [ ] 5 Regole Critiche INTATTE (verificare parola per parola)
- [ ] Detail Files indice presente
- [ ] Guardiana verifica

---

### Step 1.4: Unificare settings.json (P9)

**Problema:** Due copie identiche in ~/.claude/ e ~/.claude-insiders/.
**Soluzione:** Symlink.
**File:** `~/.claude-insiders/settings.json` -> `~/.claude/settings.json`
**Effort:** 5 minuti
**Rischio:** NULLO (verificare diff prima)

**Nota rischio symlink (finding F5 Guardiana):** Se Claude/Claude Insiders usano file watching (inotify/fswatch) su settings.json, un symlink potrebbe causare problemi di lock file. Verificare DOPO il symlink che entrambe le app funzionano normalmente. Se problemi: revertire a copia e creare script di sync invece.

**Criterio completamento:**
- [ ] diff conferma file identici
- [ ] Symlink creato
- [ ] Claude Code funziona normalmente (test: aprire e chiudere)
- [ ] Claude Insiders funziona normalmente (test: aprire e chiudere)
- [ ] Se problemi: revertire e usare sync script invece
- [ ] Documentare in CLAUDE.md del progetto

---

### Audit FASE 1

```
DOPO Step 1.1-1.4:
  -> Guardiana Qualita audit
  -> Target: 9.5/10
  -> Verifica: nessuna info persa, comportamento agenti invariato
  -> Risparmio atteso: ~6,150 token/sessione + ~350 token/messaggio
```

---

## FASE 2: CON CURA - Rischio BASSO-MEDIO (1-2 sessioni)

> Proposte che richiedono attenzione. File condivisi tra agenti.
> Studio PRIMA, implementazione DOPO.

### Step 2.1: STUDIO - Leggere _SHARED_DNA + tutti gli agenti coinvolti

**Non toccare nulla.** Solo leggere e mappare:
- `~/.claude/agents/_SHARED_DNA.md` (tutte le 222 righe)
- `~/.claude/agents/cervella-architect.md` (verificare CLI TOOLS duplicati)
- 2-3 agenti worker (verificare cosa usano del DNA)
**Output:** Mappa precisa di chi usa cosa.
**Effort:** 30 minuti

**Criterio completamento:**
- [ ] Tabella "sezione -> usata da quali agenti" completata
- [ ] Conteggio righe reale con `wc -l` per ogni file (verifica numeri Ingegnera)
- [ ] Conferma che CLI TOOLS in _SHARED_DNA e identica a cervella-architect.md

---

### Step 2.2: Tagliare _SHARED_DNA (P3)

**Problema:** 222 righe caricate in OGNI agente. Contiene sezioni usate solo dall'Architect + DNA duplicato dalla COSTITUZIONE.
**Soluzione:** Ridurre a ~150 righe.
**File:** `~/.claude/agents/_SHARED_DNA.md`
**Effort:** 45 minuti
**Rischio:** BASSO-MEDIO

**Azioni:**
1. RIMUOVERE CLI TOOLS AVANZATI (righe 165-196, 32 righe) - GIA presente in cervella-architect.md (duplicato verbatim, confermato Guardiana)
2. RIDURRE DNA DI FAMIGLIA (righe 67-97) da ~30 righe a ~5 righe - mantenere 4 citazioni core come reminder
3. NON toccare REGOLA MODELLI (non e un duplicato nel contesto agenti)
4. Compattare POST-FLIGHT CHECK a 3 righe

**Criterio completamento:**
- [ ] File <= 155 righe
- [ ] CLI TOOLS solo in cervella-architect.md
- [ ] DNA reminder 5 righe presente
- [ ] REGOLA MODELLI intatta
- [ ] Guardiana verifica

---

### Step 2.3: Quick validated_patterns (P6)

**Problema:** 277 righe lette prima di ogni nuovo modulo.
**Soluzione:** Creare versione compatta INDICE (~70 righe). File completo resta.
**File nuovo:** `~/.claude/patterns/validated_patterns_quick.md`
**File esistente:** `~/.claude/patterns/validated_patterns.md` (non toccare!)
**Effort:** 45 minuti
**Rischio:** MEDIO

**Formato quick:**
```
## Architecture (P01-P06)
P01 - Frozen Dataclass: @dataclass(frozen=True) per strutture "valore". Anti: mutabili dict/list.
P02 - ...
```

**Aggiornare CLAUDE.md:** "Leggi `validated_patterns_quick.md` prima di nuovo modulo. Se serve dettaglio: `validated_patterns.md`"

**Criterio completamento:**
- [ ] Quick version con tutti 20 pattern
- [ ] Categorie per navigazione rapida
- [ ] CLAUDE.md aggiornato
- [ ] File originale NON toccato
- [ ] Guardiana verifica completezza

---

### Step 2.4: Spezzare CHECKLIST_AZIONE (P4)

**Problema:** 356 righe, 12 sezioni, letta tutta ma ne serve 1-2 per volta.
**Soluzione:** CHECKLIST_AZIONE diventa indice (30 righe) + 2 micro-checklist nuove.
**Effort:** 1 ora
**Rischio:** MEDIO

**Piano:**
1. Creare `CHECKLIST_SESSIONE.md` (sezioni 1+4+11 = inizio/durante/fine, ~40 righe)
2. Creare `CHECKLIST_EDIT.md` (sezioni 2+5+6 = codice/proposte/edit, ~50 righe)
3. CHECKLIST_DEPLOY.md GIA ESISTE - migrare dettagli deploy (righe 115-160) li
4. CHECKLIST_AZIONE.md diventa indice (30 righe) + sezioni corte restanti (3, 9, 10, 12)
5. Aggiornare tabella in CLAUDE.md globale

**Criterio completamento:**
- [ ] CHECKLIST_AZIONE.md <= 80 righe (indice + sezioni corte)
- [ ] 2 micro-checklist create
- [ ] CHECKLIST_DEPLOY.md arricchita
- [ ] CLAUDE.md aggiornato con puntatori giusti
- [ ] MAX 3 nuovi file (non di piu!)
- [ ] Guardiana verifica zero checklist perse

---

### Audit FASE 2

```
DOPO Step 2.1-2.4:
  -> Guardiana Qualita audit COMPLETO
  -> Target: 9.5/10
  -> Test: spawnare 3 agenti diversi, verificare comportamento invariato
  -> Risparmio atteso: ~5,800 token/sessione aggiuntivi
```

---

## FASE 3: CON TEST - Rischio ALTO (1 sessione dedicata)

> File identitari. Richiedono test comportamentale.
> MAI fare nella stessa sessione della FASE 2.

### Step 3.1: STUDIO - Analisi COSTITUZIONE per OPERATIVA

**Non toccare nulla.** Analizzare:
- Quali sezioni della COSTITUZIONE sono principi OPERATIVI (influenzano decisioni)
- Quali sono storiche/motivazionali (importanti ma non operative)
- Come _SHARED_DNA referenzia la COSTITUZIONE
- Il trigger `mi sento persa` come funziona oggi

**Output:** Proposta di COSTITUZIONE_OPERATIVA.md (~80 righe) per revisione.
**Effort:** 45 minuti

**Criterio completamento:**
- [ ] Conteggio righe reale COSTITUZIONE con `wc -l`
- [ ] Lista sezioni operative vs storiche/motivazionali documentata
- [ ] Draft COSTITUZIONE_OPERATIVA (~80 righe) pronto per revisione Guardiana
- [ ] Verifica come `mi sento persa` trigger funziona (hook o manuale?)

---

### Step 3.2: Creare COSTITUZIONE_OPERATIVA (P1)

**Problema:** 510 righe lette integralmente ogni sessione + da ogni agente.
**Soluzione:** Versione operativa (~80 righe). Originale INTATTA su disco.
**File nuovo:** `~/.claude/COSTITUZIONE_OPERATIVA.md`
**File originale:** `~/.claude/COSTITUZIONE.md` (NON TOCCARE!)
**Effort:** 1 ora
**Rischio:** ALTO se fatto male

**Contenuto COSTITUZIONE_OPERATIVA (~80 righe):**
1. I 5 principi operativi con citazione Rafa per ognuno
2. Regola "Partner, non assistente" (4 domande prima di agire)
3. Formula Magica (5 pilastri, 1 riga ciascuno)
4. Regola "IL TEMPO NON CI INTERESSA" (condensata)
5. Regola consulenza esperti (tabella 6 righe)
6. Footer: "Dettagli completi, storia, momenti: Read ~/.claude/COSTITUZIONE.md"

**Condizioni Guardiana (INVIOLABILI):**
- COSTITUZIONE.md originale MAI toccata
- `mi sento persa` carica ancora la COMPLETA
- Citazioni dirette di Rafa presenti (almeno 1 per sezione)
- Test: 3 agenti leggono OPERATIVA -> comportamento invariato

**Aggiornare:**
- `session_start_swarm.py`: carica OPERATIVA al posto di COMPLETA
- `_SHARED_DNA.md`: punta a OPERATIVA

---

### Step 3.3: SubagentStart ottimizzazione (P8)

**Problema:** Inietta 50 righe PROMPT_RIPRESA in ogni agente spawnato.
**Soluzione:** Ridurre a 40 righe (header + sessione corrente, no tabella packages).
**File:** `~/.claude/hooks/subagent_context_inject.py`
**Effort:** 20 minuti
**Rischio:** MEDIO

**Condizioni Guardiana:**
- RIPRESA_MAX_LINES da 50 a 40 (non 30)
- FATOS_MAX_LINES resta a 100
- Aggiungere riga finale: "Full context: Read PROMPT_RIPRESA_{project}.md"
- Le info critiche della sessione corrente DEVONO essere nelle prime 40 righe

---

### Audit FASE 3

```
DOPO Step 3.2-3.3:
  -> Guardiana Qualita audit COMPLETO
  -> Target: 9.5/10
  -> TEST COMPORTAMENTALE OBBLIGATORIO:
    1. Spawnare Guardiana Qualita -> verifica che applica gli stessi standard
    2. Spawnare Backend worker -> verifica che conosce regole sviluppo
    3. Spawnare Researcher -> verifica che rispetta autonomia decisionale
  -> Se qualsiasi agente mostra degradazione: ROLLBACK immediato
  -> Risparmio atteso: ~3,600 token/sessione aggiuntivi
```

---

## RIEPILOGO

```
+================================================================+
|   SUBROADMAP CONTEXT OPTIMIZATION v2                            |
+================================================================+

FASE 1: Quick Wins (Rischio NULLO)   [....................] 0%
  1.1 Indice MANUALE_DIAMANTE         10min   TODO
  1.2 Dedup CervellaSwarm/CLAUDE.md   20min   TODO
  1.3 Snellire MEMORY.md              30min   TODO
  1.4 Unificare settings.json         5min    TODO

FASE 2: Con Cura (Rischio MEDIO)     [....................] 0%
  2.1 STUDIO _SHARED_DNA              30min   TODO
  2.2 Tagliare _SHARED_DNA            45min   TODO
  2.3 Quick validated_patterns        45min   TODO
  2.4 Spezzare CHECKLIST_AZIONE       1h      TODO

FASE 3: Con Test (Rischio ALTO)      [....................] 0%
  3.1 STUDIO COSTITUZIONE             45min   TODO
  3.2 COSTITUZIONE_OPERATIVA          1h      TODO
  3.3 SubagentStart ottimizzazione    20min   TODO

EFFORT TOTALE: ~6-7 ore (2-3 sessioni)
ORDINE: FASE 1 -> FASE 2 -> FASE 3 (mai saltare)
AUDIT: Guardiana dopo OGNI fase
```

---

## METRICHE TARGET

| Metrica | Attuale | Target | Risparmio |
|---------|---------|--------|-----------|
| Overhead sessione tipica | ~20,200 tok | ~15,000 tok | -25% |
| Overhead sessione intensiva | ~41,800 tok | ~31,000 tok | -25% |
| MEMORY.md per messaggio | ~350 tok | ~200 tok | -43% |
| _SHARED_DNA per agente | ~1,560 tok | ~1,000 tok | -36% |
| CHECKLIST_AZIONE per lettura | ~2,430 tok | ~600 tok | -75% |

---

## SUCCESS CRITERIA

- [ ] Risparmio >= 20% overhead sessione tipica (numeri esatti verranno verificati negli step STUDIO)
- [ ] ZERO degradazione qualita (Guardiana 9.5/10 su ogni fase)
- [ ] Test comportamentale 3 agenti superato
- [ ] COSTITUZIONE.md originale INTATTA
- [ ] 5 Regole Critiche MEMORY.md INTATTE
- [ ] Nessun agente perde accesso a info necessarie

---

## DIPENDENZE

```
FASE 1 (indipendente, inizio subito)
   |
   v
FASE 2 (dopo audit FASE 1 OK)
   |
   v
FASE 3 (dopo audit FASE 2 OK, sessione dedicata)
```

---

*"Ogni token conta. Context intelligente > Context grande."*
*"Fatto BENE > Fatto VELOCE"*

*Cervella Regina - CervellaSwarm S404*
*Fonti: Ingegnera (analisi), Guardiana Qualita (audit 9.0/10 proposte + 9.3/10 subroadmap)*
*Nota: conteggi righe da verificare negli step STUDIO con wc -l reale (finding F1 Guardiana)*
