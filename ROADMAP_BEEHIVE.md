# ROADMAP BEEHIVE - CervellaSwarm

> **"Cervella Beehive"** - Il sistema che fa nascere nuove Cervelle!

**Versione:** 1.2.0
**Data:** 5 Gennaio 2026 (Sessione 88 - CODE REVIEW + FIX)
**Link:** ROADMAP_SACRA.md (progetto principale)

---

## STATO ATTUALE - CHECKUP 5 Gennaio 2026

```
+------------------------------------------------------------------+
|                                                                  |
|   BEEHIVE = Il nostro ALVEARE digitale!                         |
|                                                                  |
|   ✅ spawn-workers.sh v1.9.0 FUNZIONA!                          |
|   ✅ swarm-status v1.0.0 FUNZIONA!                              |
|   ✅ swarm-review v1.0.0 FUNZIONA!                              |
|   ✅ 16 agenti GLOBALI pronti                                    |
|   ✅ 10 hooks GLOBALI attivi                                     |
|   ✅ AUTO-HANDOFF v4.3.0 (VS Code nativo!)                      |
|                                                                  |
|   FASI 1-2-3 COMPLETATE! Prossimo: depends_on                   |
|                                                                  |
+------------------------------------------------------------------+
```

### Statistiche Checkup

| Metrica | Valore | Status |
|---------|--------|--------|
| Task completati in .swarm/tasks/ | 40+ | OTTIMO! |
| Worker spawned (spawn.log) | 100+ | OTTIMO! |
| Agenti globali | 16 | COMPLETO! |
| Hooks globali | 9 | COMPLETO! |
| Task .working senza .done | 2 | DA FIXARE |
| Guardiane usate | 1 (qualita) | DA MIGLIORARE |

---

## PROBLEMI IDENTIFICATI

### P1. STALE TASK DETECTION (Critico)

**Problema:** Task rimangono in `.working` senza mai diventare `.done`

**Evidenza:**
```
Miracollo:
- SPLIT_SETTINGS.working (19:31) - mai completato
- CLEANUP_CONSOLE_LOG.working (19:26) - mai completato
```

**Causa:** L'ape crea .working, poi esce/crasha prima di completare

**Soluzione proposta:**
```
SE .working esiste da > 30 minuti:
   -> Considera STALE
   -> Rimuovi .working
   -> Task torna disponibile
```

**Implementazione:** Script `swarm-cleanup.sh` o logica in spawn-workers

---

### P2. VISIBILITA' OUTPUT API (Alta)

**Problema:** La Regina non vede in tempo reale cosa fanno le api

**Feedback Cervella:**
> "Non vedo in tempo reale cosa fanno le api. Devo aspettare che finiscano."

**Soluzione proposta:** Comando `swarm-status`

```bash
$ swarm-status

BEEHIVE STATUS - CervellaSwarm
==============================

WORKERS ATTIVI:
  [WORKING] cervella-frontend -> SPLIT_SETTINGS (5 min)
  [WORKING] cervella-backend -> API_REFACTOR (2 min)

TASK IN CODA:
  [READY] CLEANUP_CONSOLE_LOG -> cervella-frontend
  [READY] FIX_MODAL -> cervella-frontend

COMPLETATI OGGI:
  [DONE] SPLIT_WIDGET (18:38)
  [DONE] SPLIT_RATEBOARD (19:24)
```

---

### P3. GUARDIANE NON USATE (Media)

**Problema:** Abbiamo 3 Guardiane Opus ma non c'e' workflow automatico

**Le Guardiane:**
- cervella-guardiana-qualita (verifica output)
- cervella-guardiana-ops (verifica deploy/security)
- cervella-guardiana-ricerca (verifica ricerche)

**Feedback Cervella:**
> "Le Guardiane le abbiamo ma non le usiamo!"

**Soluzione proposta:** Workflow automatico

```
1. Ape completa task -> crea .done
2. Sistema crea .review_ready
3. spawn-workers --guardiana-qualita
4. Guardiana verifica e crea .approved o .rejected
```

---

### P4. COORDINAMENTO TASK DIPENDENTI (Media)

**Problema:** Tutti i task sono paralleli, ma a volte serve sequenza

**Feedback Cervella:**
> "Se Task A deve finire prima di Task B, come lo gestisco?"

**Soluzione proposta:** Campo `depends_on` nel task file

```markdown
# Task: Deploy API

**Assegnato a:** cervella-devops
**Stato:** ready
**Depends_on:** TASK_API_REFACTOR

## Obiettivo
...
```

**Logica:**
```
SE task ha depends_on:
   -> Verifica che dependency sia .done
   -> Se no, salta questo task
   -> Se si, procedi
```

---

### P5. UNA SOLA APE PER TIPO (Bassa)

**Problema:** spawn-workers --frontend apre 1 sola finestra

**Feedback Cervella:**
> "Avevo 5 task ma 1 sola ape - li fa in sequenza"

**Soluzione proposta:** Flag `--count=N`

```bash
spawn-workers --frontend --count=3
# Apre 3 finestre frontend parallele!
```

---

### P6. AUTO-HANDOFF IMPERFETTO (In corso - altra sessione)

**Problema:** `claude -p` esegue e poi ESCE invece di restare aperto

**Stato:** In fix nell'altra sessione parallela

**Soluzioni in esplorazione:**
1. Flag per restare in modalita interattiva
2. Apertura su VS Code invece di Terminal
3. Pipe o altro metodo

---

## PRIORITA' FIX

| # | Problema | Priorita | Effort | Impatto | Status |
|---|----------|----------|--------|---------|--------|
| 1 | Stale Task Detection | CRITICA | Basso | Alto | ✅ FATTO! (in swarm-status --cleanup) |
| 2 | swarm-status comando | ALTA | Medio | Alto | ✅ FATTO! v1.0.0 |
| 3 | Workflow Guardiane | MEDIA | Medio | Medio | ✅ FATTO! swarm-review v1.0.0 |
| 4 | depends_on | MEDIA | Medio | Medio | |
| 5 | --count=N | BASSA | Basso | Basso | |
| 6 | AUTO-HANDOFF | IN CORSO | Alto | Alto | (altra sessione) |

---

## PIANO IMPLEMENTAZIONE

### FASE 1: Affidabilita (Priorita CRITICA)

**Obiettivo:** Zero task bloccati, zero .working stale

| Task | Cosa | Chi |
|------|------|-----|
| 1.1 | Creare script `swarm-cleanup.sh` | cervella-backend |
| 1.2 | Aggiungere stale detection a spawn-workers | cervella-backend |
| 1.3 | Test su tutti e 3 i progetti | cervella-tester |

**Output:** Task stale vengono rilasciati automaticamente

---

### FASE 2: Visibilita (Priorita ALTA)

**Obiettivo:** La Regina vede TUTTO in tempo reale

| Task | Cosa | Chi |
|------|------|-----|
| 2.1 | Creare script `swarm-status` | cervella-backend |
| 2.2 | Mostrare workers attivi, task in coda, completati | cervella-backend |
| 2.3 | Aggiungere a ~/.local/bin/ (globale) | cervella-devops |

**Output:** `swarm-status` mostra stato real-time

---

### FASE 3: Guardiane (Priorita MEDIA)

**Obiettivo:** Verifica automatica output delle api

| Task | Cosa | Chi |
|------|------|-----|
| 3.1 | Definire workflow Guardiane | cervella-docs |
| 3.2 | Aggiungere creazione .review_ready dopo .done | cervella-backend |
| 3.3 | Test con cervella-guardiana-qualita | cervella-tester |

**Output:** Le Guardiane verificano automaticamente

---

### FASE 4: Dipendenze (Priorita MEDIA)

**Obiettivo:** Task sequenziali quando serve

| Task | Cosa | Chi |
|------|------|-----|
| 4.1 | Aggiungere parsing depends_on | cervella-backend |
| 4.2 | Aggiornare logica spawn-workers | cervella-backend |
| 4.3 | Test con task dipendenti | cervella-tester |

**Output:** depends_on funziona

---

### FASE 5: Scaling (Priorita BASSA)

**Obiettivo:** Multiple api dello stesso tipo

| Task | Cosa | Chi |
|------|------|-----|
| 5.1 | Aggiungere flag --count=N | cervella-backend |
| 5.2 | Test con 3 frontend paralleli | cervella-tester |

**Output:** `spawn-workers --frontend --count=3` funziona

---

## COSA FUNZIONA GIA' (Celebriamo!)

| Cosa | Versione | Note |
|------|----------|------|
| spawn-workers.sh | v1.9.0 | GLOBALE! PROJECT-AWARE! |
| 16 Agenti | v1.0.0 | Tutti specializzati! |
| Task files | - | Formato chiaro e funzionante |
| .ready/.working/.done | - | Sistema stati funziona |
| Auto-close finestra | v1.5.0 | No dialogo macOS! |
| Notifiche macOS | v1.6.0 | Glass sound! |
| Log in .swarm/logs/ | - | Tutto tracciato! |

---

## METRICHE SUCCESSO

Prima di dire "BEEHIVE 100000%" verifichiamo:

```
[x] Zero task .working > 30 min (swarm-status --cleanup)
[x] swarm-status mostra tutto (v1.0.0!)
[x] Guardiane verificano output (swarm-review v1.0.0!)
[ ] depends_on funziona
[x] AUTO-HANDOFF apre e RESTA aperto (v4.3.0 VS Code!)
```

**4 su 5 completate! Manca solo depends_on!**

---

## DNA FUTURO

Dopo che tutto funziona al 100000%, aggiornare il DNA delle api:

```
REGOLA AUTOMATICA (proposta Cervella):

SE task MODIFICA FILE && task > 100 righe modifiche:
   -> Creo task in .swarm/tasks/
   -> spawn-workers --[tipo]
   -> Continuo con altro
```

**Questo viene DOPO il 100000% affidabilita!**

---

## LINK UTILI

| Cosa | Path |
|------|------|
| spawn-workers | ~/.local/bin/spawn-workers |
| Agenti | ~/.claude/agents/ |
| Hooks | ~/.claude/hooks/ |
| Task CervellaSwarm | .swarm/tasks/ |
| Task Miracollo | ~/Developer/miracollogeminifocus/.swarm/tasks/ |
| Task Contabilita | ~/Developer/ContabilitaAntigravity/.swarm/tasks/ |

---

*"Il Beehive e' il cuore dello Swarm. Rendiamolo 100000%!"*

*"Le api nascono, lavorano, tornano. La Regina coordina."*

Cervella & Rafa

---

**CHANGELOG:**

### 5 Gennaio 2026 - v1.2.0 (Sessione 88 - CODE REVIEW + FIX)
- ✅ CODE REVIEW: Rating 8/10 -> 9/10!
- ✅ FIX A1+A2: Path hardcodati -> ~/.swarm/config
- ✅ FIX B1: Codice duplicato -> swarm-common.sh
- ✅ FIX B3: Template migliorati
- ✅ NUOVO: swarm-health (health check sistema)
- ✅ NUOVO: ~/.swarm/config (configurazione centralizzata)
- ✅ NUOVO: ~/.local/lib/swarm-common.sh (funzioni comuni)
- API al lavoro: cervella-backend(2) + cervella-docs(1) + cervella-reviewer(1)
- Decisione: Guardiane per task CRITICI, verifica manuale per semplici

### 5 Gennaio 2026 - v1.1.0 (Sessione 88 - Mattina)
- ✅ Fase 3 COMPLETATA! swarm-review v1.0.0
- Organizzata casa: 102 file archiviati in CervellaSwarm
- Organizzata casa: 14 file archiviati in Miracollo
- SPLIT_SETTINGS stale archiviato
- Task rimasti puliti e pronti

### 5 Gennaio 2026 - v1.0.0 (Sessione 87)
- Creata ROADMAP_BEEHIVE
- Checkup completo sistema
- Identificati 6 problemi
- Definite 5 fasi implementazione
- Prioritizzato il lavoro
- ✅ swarm-status v1.0.0 creato
- ✅ swarm-review v1.0.0 creato
- ✅ Workflow Ape → Guardiana TESTATO!

