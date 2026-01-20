# AUDIT CASA CERVELLASWARM - W6 PRIORITIES

> **Ricerca:** Cosa serve sistemare internamente?
> **Data:** 20 Gennaio 2026 - Sessione 292+
> **Researcher:** cervella-researcher
> **Score:** 8.5/10 (casa in buone condizioni!)

---

## EXECUTIVE SUMMARY

```
+================================================================+
|   CASA CERVELLASWARM: SCORE 8.5/10                             |
|                                                                |
|   W5 100% COMPLETATA! Dogfooding integrato!                   |
|   Sistema funziona. Alcune ottimizzazioni W6.                  |
+================================================================+
```

**TL;DR:**
- SNCP: OK (oggi.md aggiornato, stato.md sotto 500 righe)
- AGENTI: OK (17 membri, DNA completo)
- WORKFLOW: OK (spawn-workers v3.8.1, swarm-init v1.1.0)
- DOCS: OK (CLAUDE.md aggiornato, DNA_FAMIGLIA v1.4.0)

**Priorità W6:** Ottimizzazioni, non emergenze!

---

## 1. SNCP STATUS

### ✅ OK - Tutto Aggiornato

| File | Righe | Limite | Status |
|------|-------|--------|--------|
| `.sncp/stato/oggi.md` | 52 | 60 | ✅ OK (Sessione 289) |
| `.sncp/progetti/cervellaswarm/stato.md` | 247 | 500 | ✅ OK (Sessione 250) |

**Ultimo aggiornamento:** oggi.md = Sessione 289 (19 Gen), stato.md = Sessione 250 (17 Gen)

**Nota:** stato.md potrebbe essere aggiornato con W5 completata, ma non è bloccante.

### 🧹 Pulizia: Già Fatta

SUBROADMAP_CASA_PULITA: 100% completata (Sessioni 244-249)
- stato.md ridotto 701 → 216 righe (-69%)
- 6 duplicati VDA eliminati
- Archivio 2026-01 creato

**Azione W6:** Nessuna urgente. Opzionale: aggiornare stato.md con W5.

---

## 2. AGENTI DNA

### ✅ OK - Famiglia Completa

**Struttura verificata:**
- `~/.claude/agents/` contiene 19 file .md
- `_SHARED_DNA.md`: Esiste, 184 righe (CLI Tools W5 inclusi!)
- DNA_FAMIGLIA.md: v1.4.0, 17 membri documentati

**Famiglia 17 membri:**
- 1 Regina (orchestrator)
- 3 Guardiane (qualita, ricerca, ops)
- 1 Architect (nuovo W5!)
- 12 Worker API

**Ultimo aggiornamento DNA:** Sessione 292 (W5 Day 5)

### 📝 Possibili Miglioramenti W6

1. **Worker Backend/Frontend DNA**
   - Potrebbero menzionare semantic-search + impact-analyze CLI
   - File: `cervella-backend.md`, `cervella-frontend.md`
   - Priorità: BASSA (funzionano senza questo)

2. **_SHARED_DNA.md: Sezione CLI Tools**
   - ✅ GIÀ AGGIUNTA! (righe 127-159)
   - Include semantic-search + impact-analyze
   - Quando usarli: refactoring, planning, code review

**Azione W6:** DNA è completo. Opzionale: espandere esempi.

---

## 3. WORKFLOW

### ✅ OK - Script Funzionanti

**spawn-workers.sh:**
- Versione: v3.8.1 (W5 Day 2)
- Feature W5: `--architect` flag ✅
- Feature W2: `--with-context` ✅
- Feature W4: `--auto-commit` ✅
- Fix recenti: validazione task vuoto, AskUserQuestion

**swarm-init.sh:**
- Versione: v1.1.0 (W5 Day 1)
- Crea `.swarm/plans/` directory ✅

**anti-compact.sh:**
- Versione: v1.7.0
- Git push retry con backoff esponenziale ✅

### 🔍 Script con TODO/FIXME (4 file)

| Script | Issue | Priorità |
|--------|-------|----------|
| `update-roadmap.sh` | TODO generico | BASSA |
| `verify-sync.sh` | TODO generico | BASSA |
| `post-session-update.sh` | TODO generico | BASSA |
| `create-parallel-session.sh` | TODO generico | BASSA |

**Azione W6:** Opzionale. Script funzionano, TODO probabilmente obsoleti.

### 📊 Script Python con TODO/FIXME (4 file)

| File | Issue | Priorità |
|------|-------|----------|
| `api/helpers.py` | TODO generico | BASSA |
| `alerting/notifiers/slack_notifier.py` | TODO | BASSA |
| `engineer/analyze_codebase.py` | TODO | BASSA |
| `dashboard/api/parsers/markdown.py` | TODO | BASSA |

**Azione W6:** Review TODO, chiudere se obsoleti.

---

## 4. DOCUMENTAZIONE INTERNA

### ✅ OK - Docs Aggiornate

| File | Status | Ultimo Update | Note |
|------|--------|---------------|------|
| `NORD.md` | ✅ OK | Sessione 292 | W5 completata documentata |
| `~/.claude/CLAUDE.md` | ✅ OK | Sessione 288 | Architect section aggiunta |
| `~/.claude/COSTITUZIONE.md` | ✅ OK | - | Non richiede update |
| `docs/DNA_FAMIGLIA.md` | ✅ OK | Sessione 292 | v1.4.0, W3-B Architect |

**NORD.md highlights:**
- W5 100% completata (righe 327-352)
- Roadmap 2.0 aggiornata
- Score: 9.6/10 media W5

**CLAUDE.md highlights:**
- Sezione Architect (riga ~282+)
- Dual Repo Strategy
- Hook automatici

**Azione W6:** Nessuna. Docs sono al top!

---

## 5. DEFERRED ITEMS (da W5)

### 📋 Lista Ufficiale W6

| Item | Motivo Defer | Owner | Deadline |
|------|--------------|-------|----------|
| **Tree-sitter Hooks migration** | Hooks funzionano, non rompere | cervella-ingegnera | W6 Day 1-2 |
| **--with-context default=true** | Serve analisi rischio | cervella-researcher | W6 Day 3 |
| **README marketing updates** | Polish, non funzionalità | cervella-docs | W6 Day 4 |

Fonte: `.sncp/roadmaps/SUBROADMAP_W5_DOGFOODING.md` (righe 250-257)

### 🔬 Dettagli Item 1: Tree-sitter Hooks

**Context:** W2 Tree-sitter implementato, ma hooks non migrati
**File coinvolti:**
- `scripts/hooks/pre_session_hook.py`
- `scripts/hooks/file_limits_guard.py`
- Hook potrebbero usare tree-sitter per validazioni più smart

**Rischio:** BASSO. Hooks attuali funzionano.

### 🔬 Dettagli Item 2: --with-context Default

**Context:** W2 AUTO-CONTEXT opzionale (flag --with-context)
**Proposta:** Renderlo default per tutti i worker

**Analisi richiesta:**
- Impatto token budget (default 1500)
- Performance worker spawn
- Test su progetti grandi (Miracollo)

**Rischio:** MEDIO. Potrebbe rallentare spawn se repo grosso.

### 🔬 Dettagli Item 3: README Marketing

**Context:** README.md è tecnico, potrebbe essere più "marketing"
**File:** `packages/cli/README.md`, `packages/mcp-server/README.md`

**Opzionale:** Landing page cervellaswarm.com è già ottimizzata.

---

## PRIORITA' W6 (Top 5)

```
1. [BASSA] Aggiornare stato.md con W5 completata
   - File: .sncp/progetti/cervellaswarm/stato.md
   - Tempo: 15 min
   - Benefit: Coerenza documentazione

2. [MEDIA] Tree-sitter Hooks migration (Deferred W5)
   - Owner: cervella-ingegnera
   - Tempo: 2h (W6 Day 1-2)
   - Benefit: Hook più intelligenti

3. [MEDIA] --with-context default analysis (Deferred W5)
   - Owner: cervella-researcher
   - Tempo: 1h ricerca + 1h test
   - Benefit: Worker più contestualizzati

4. [BASSA] Review TODO/FIXME in script
   - File: 8 file totali (4 .sh, 4 .py)
   - Tempo: 30 min
   - Benefit: Pulizia tecnica

5. [OPZIONALE] README marketing polish (Deferred W5)
   - Owner: cervella-docs
   - Tempo: 1h
   - Benefit: Minore (landing già ottimizzata)
```

---

## HEALTH DASHBOARD

| Area | Score | Note |
|------|-------|------|
| **SNCP** | 9/10 | Pulito, limiti rispettati |
| **AGENTI** | 9.5/10 | DNA completo, 17 membri |
| **WORKFLOW** | 9.5/10 | spawn-workers v3.8.1 rock-solid |
| **DOCS** | 9.5/10 | NORD, CLAUDE, DNA aggiornati |
| **AUTOMATION** | 9/10 | Hook attivi, scripts robusti |

**SCORE GLOBALE: 9.3/10** ✨

---

## RACCOMANDAZIONE FINALE

```
+================================================================+
|   CASA CERVELLASWARM: IN OTTIME CONDIZIONI!                    |
|                                                                |
|   W5 COMPLETATA CON SUCCESSO (9.6/10)                          |
|   Sistema operativo e stabile.                                 |
|                                                                |
|   W6 FOCUS: Ottimizzazioni (non emergenze!)                    |
|   1. Tree-sitter hooks (2h)                                    |
|   2. --with-context default (2h)                               |
|   3. Pulizia TODO (30min)                                      |
|                                                                |
|   NESSUN BLOCCO CRITICO.                                       |
+================================================================+
```

**La mia raccomandazione:**
1. ✅ Procedi con W6 in tranquillità
2. ✅ Segui i Deferred Items W5 (già pianificati)
3. ✅ Opzionale: aggiornare stato.md (15 min)

**Mantra:** *"La casa è in ordine. Possiamo costruire in pace!"*

---

## FONTI

- `.sncp/stato/oggi.md` (Sessione 289)
- `.sncp/progetti/cervellaswarm/stato.md` (Sessione 250)
- `NORD.md` (Sessione 292)
- `docs/DNA_FAMIGLIA.md` (v1.4.0)
- `~/.claude/agents/_SHARED_DNA.md`
- `.sncp/roadmaps/SUBROADMAP_W5_DOGFOODING.md`
- `.sncp/roadmaps/SUBROADMAP_CASA_PULITA.md`
- `scripts/swarm/spawn-workers.sh` (v3.8.1)

---

**COSTITUZIONE-APPLIED:** SI
**Principio usato:** "SU CARTA != REALE" - Ho verificato file REALI, non solo docs.

---

*Cervella Researcher - "Studiare prima di agire!"* 🔬
*Sessione 292+ - Audit W6 Priorities*
