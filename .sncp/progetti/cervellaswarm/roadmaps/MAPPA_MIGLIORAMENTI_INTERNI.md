# MAPPA MIGLIORAMENTI INTERNI - CervellaSwarm

> **"Prima di costruire per altri, costruisci il MEGLIO per te."** - Rafa
> **Data creazione:** 10 Febbraio 2026 - Sessione 349
> **Ultima modifica:** 10 Febbraio 2026 - S351

---

## COME LEGGERE QUESTA MAPPA

```
STATO POSSIBILI:
[FATTO]       = Completato, testato, REALE
[IN CORSO]    = Attualmente in lavorazione
[STUDIATO]    = Ricerca fatta, approccio chiaro
[DA FARE]     = Chiaro cosa fare, serve solo tempo

OGNI STEP HA:
- Stato
- Tempo stimato
- Dipende da (step precedenti)
- Output (cosa produce)
- Criterio completamento
- Score target
```

---

## CONTESTO

```
+================================================================+
|   PUNTO DI PARTENZA (S349):                                     |
|                                                                  |
|   19 agenti, 22 hooks, 968 test, 95% coverage                   |
|   CLAUDE.md: ~450 righe (main)                                  |
|   Contesto caricato/sessione: ~10,500 righe                     |
|   Token stimati/sessione: ~25,000+ solo contesto                |
|   Tech debt: ZERO                                                |
|                                                                  |
|   OBIETTIVO: Dal 95000% al 100000%                               |
+================================================================+
```

---

# FASE A: QUICK WINS - Migliorare Quello Che C'e (8h)

> **"Fixare prima, innovare dopo"**

---

## STEP A.1: Async Hooks - SessionEnd Veloce

**Stato:** [FATTO] - S350, Score 9/10
**Tempo stimato:** 2h
**Dipende da:** Nulla
**Output:** SessionEnd istantaneo (da ~2min a <5sec)

**PROBLEMA:**
Oggi SessionEnd esegue 6 hooks in serie. Se uno e lento, TUTTI aspettano.
L'utente (Rafa) deve aspettare prima di chiudere il terminale.

**SOLUZIONE:**
Aggiungere `async: true` agli hook non-critici di SessionEnd.
Solo `session_end_save.py` e `update_prompt_ripresa.py` restano sincroni (dati critici).

**IMPLEMENTAZIONE:**
```json
{
  "type": "command",
  "command": "python3 session_end_flush.py",
  "timeout": 30,
  "async": true
}
```

**Hook da rendere async:**
- session_end_flush.py (flush memoria)
- sncp_verify_sync_hook.py (verifica sync)
- file_limits_guard.py (check limiti)
- sncp_auto_update.py (aggiornamento SNCP)

**Criterio completamento:** SessionEnd < 5 secondi. Score target: 9/10.

---

## STEP A.2: PreToolUse Bash Validation

**Stato:** [FATTO] - S350, Score 9.5/10
**Tempo stimato:** 4h
**Dipende da:** Nulla
**Output:** Comandi bash validati automaticamente

**PROBLEMA:**
Oggi qualsiasi comando bash viene eseguito senza check preventivo.
Un rm -rf sbagliato o un git push --force passa senza filtro.

**SOLUZIONE:**
Hook PreToolUse su matcher "Bash" che:
1. Blocca comandi distruttivi (rm -rf, git push --force, drop table)
2. Avvisa per comandi rischiosi (git reset, chmod 777)
3. Auto-inject safety flags dove possibile

**IMPLEMENTAZIONE:**
- Nuovo file: `~/.claude/hooks/bash_validator.py`
- Matcher: `Bash`
- Tipo: PreToolUse (puo BLOCCARE il tool)
- Lista comandi bloccati/avvertiti configurabile

**Criterio completamento:** 0 comandi distruttivi passano senza conferma. Score target: 9.5/10.

---

## STEP A.3: Persistent Memory per Guardiane

**Stato:** [FATTO] - S351, Score 9/10
**Tempo stimato:** 2h
**Dipende da:** Nulla
**Output:** Guardiane che ricordano pattern tra sessioni

**PROBLEMA:**
Ogni volta che una Guardiana fa audit, parte da zero. Non ricorda
gli errori trovati prima, i pattern ricorrenti, le lezioni apprese.

**SOLUZIONE:**
Aggiungere `memory: user` ai profili delle 3 Guardiane (Opus):
- cervella-guardiana-qualita.md
- cervella-guardiana-ops.md
- cervella-guardiana-ricerca.md

**IMPLEMENTAZIONE:**
Aggiungere nel frontmatter YAML degli agent file:
```yaml
---
memory: user
---
```

La Guardiana accumula conoscenza tra sessioni su:
- Pattern di errori ricorrenti
- Standard di qualita del progetto
- Preferenze di Rafa

**Criterio completamento:** Guardiana cita lezione da sessione precedente. Score target: 9/10.

---

# FASE B: CONTEXT OPTIMIZATION - Risparmiare Token (10h)

> **"Ogni token conta. Context intelligente > Context grande."**
>
> Include lo studio "Carl" / Dynamic Context Injection

---

## STEP B.1: Audit e Riduzione CLAUDE.md

**Stato:** [STUDIATO]
**Tempo stimato:** 4h
**Dipende da:** A.1 (async hooks - per non rallentare)
**Output:** CLAUDE.md ottimizzato < 300 righe

**PROBLEMA:**
~/.claude/CLAUDE.md ha 372 righe. Molte sezioni sono ridondanti
o servono solo in contesti specifici. TUTTO viene caricato SEMPRE.

**SOLUZIONE:**
1. Identificare sezioni che servono SEMPRE vs SOLO in certi contesti
2. Spostare contesto specifico in Skills (caricato on-demand)
3. CLAUDE.md diventa "regole core" (<300 righe)
4. Tutto il resto in Skills con Dynamic Context

**ESEMPIO:**
- SEMPRE: Regole git, SNCP path, swarm mode base
- ON-DEMAND: Disambiguazione Miracollo (solo se progetto Miracollo)
- ON-DEMAND: Checklist Deploy (solo se deploy)
- ON-DEMAND: SNCP 3.0 script reference (solo se maintenance)

**Criterio completamento:** CLAUDE.md < 300 righe, zero informazione persa. Score target: 9/10.

---

## STEP B.2: Skills con Dynamic Context Injection

**Stato:** [STUDIATO]
**Tempo stimato:** 4h
**Dipende da:** B.1
**Output:** 3-5 Skills con dati LIVE

**PROBLEMA:**
Il contesto caricato a inizio sessione e STATICO. Non sa lo stato
attuale di git, test, branch. Serve guardare manualmente.

**SOLUZIONE:**
Creare Skills che iniettano dati LIVE con sintassi `!command`:

**Skill 1: /swarm-status**
```markdown
## Stato Progetto LIVE
- Branch: !`git branch --show-current`
- Ultimo commit: !`git log --oneline -1`
- File modificati: !`git status --short`
- Test: !`python3 -m pytest tests/ -q --tb=no 2>&1 | tail -1`
```

**Skill 2: /swarm-context (per progetto)**
```markdown
## Contesto Sessione
!`cat .sncp/progetti/cervellaswarm/PROMPT_RIPRESA_cervellaswarm.md`
## NORD Attuale
!`head -50 NORD.md`
```

**Skill 3: /swarm-health**
```markdown
## Health Check
- SNCP size: !`./scripts/sncp/check-ripresa-size.sh 2>&1`
- Secrets: !`./scripts/sncp/audit-secrets.sh 2>&1 | tail -3`
- Coverage: !`python3 -m pytest --co -q 2>&1 | tail -1`
```

**Criterio completamento:** 3+ Skills funzionanti con dati live. Score target: 9.5/10.

---

## STEP B.3: SessionStart Smart Loading

**Stato:** [DA FARE]
**Tempo stimato:** 2h
**Dipende da:** B.1, B.2
**Output:** Hook SessionStart che carica solo il necessario

**PROBLEMA:**
Oggi SessionStart carica TUTTO (COSTITUZIONE + NORD + PROMPT_RIPRESA +
load_context.py). Anche quando non serve tutto.

**SOLUZIONE:**
SessionStart rileva il progetto dal cwd e carica SOLO:
1. Regole core (sempre)
2. PROMPT_RIPRESA del progetto attivo (dinamico)
3. Nota: COSTITUZIONE gia iniettata da hook subagent

Non carica:
- Info di altri progetti
- Sezioni CLAUDE.md non rilevanti

**Criterio completamento:** Token contesto ridotti del 30%+. Score target: 9/10.

---

# FASE C: SICUREZZA E ROBUSTEZZA (6h)

> **"La sicurezza non e un optional"**

---

## STEP C.1: Hook Integrity Check

**Stato:** [FATTO] - S351, Score 9.5/10
**Tempo stimato:** 2h
**Dipende da:** A.1
**Output:** Script che verifica tutti gli hook

**PROBLEMA:**
Abbiamo scoperto (S349) che session_start_scientist.py era referenziato
ma il file era .DISABLED. Quanti altri hook rotti ci sono?

**SOLUZIONE:**
Creare script `verify-hooks.sh` che:
1. Legge settings.json (main + insiders)
2. Per ogni hook, verifica che il file esista
3. Per ogni hook, verifica che sia eseguibile
4. Report: OK / BROKEN / DISABLED
5. Integrare nel sncp_daily_maintenance

**Criterio completamento:** 0 hook rotti non rilevati. Score target: 9/10.

---

## STEP C.2: MCP Server Health Monitor

**Stato:** [DA FARE]
**Tempo stimato:** 2h
**Dipende da:** Nulla
**Output:** Monitor che rileva MCP server down

**PROBLEMA:**
Il MCP server puo crashare silenziosamente. Lo scopriamo solo
quando un tool call fallisce (troppo tardi).

**SOLUZIONE:**
Aggiungere check MCP nel SessionStart hook:
1. Verifica che il processo MCP risponda
2. Verifica versione (match sorgente vs compilato)
3. Se stale: auto-rebuild
4. Warning visivo se down

**Criterio completamento:** MCP failure rilevato a inizio sessione. Score target: 9/10.

---

## STEP C.3: LaunchAgent Health Check

**Stato:** [DA FARE]
**Tempo stimato:** 2h
**Dipende da:** C.1
**Output:** Verifica automatica dei job background

**PROBLEMA:**
I LaunchAgent possono fallire silenziosamente (come Miracollook backend).
Non abbiamo un modo di saperlo senza controllare manualmente.

**SOLUZIONE:**
Aggiungere al sncp_daily_maintenance.sh:
1. Check exit code di ogni LaunchAgent nostro
2. Check che lo script referenziato esista
3. Check che i path nei plist siano validi
4. Report con status per ogni agent

**Criterio completamento:** Daily check rileva agent rotti. Score target: 9/10.

---

# FASE D: EVOLUZIONE AGENTI (6h)

> **"La Famiglia che impara e cresce"**

---

## STEP D.1: Agent Teams - Parallelismo Reale

**Stato:** [DA STUDIARE]
**Tempo stimato:** 4h
**Dipende da:** A.3 (persistent memory)
**Output:** Agenti che lavorano in parallelo vero

**PROBLEMA:**
Oggi gli agenti lavorano in serie (Task tool, uno alla volta) o
in parallelo limitato (multiple Task calls). Non c'e coordinamento.

**SOLUZIONE:**
Esplorare Agent Teams (Opus 4.6):
- TeammateTool per delegazione tra agenti
- Parallelismo reale vs sequenziale
- Valutare se migliora il nostro spawn-workers

**DA STUDIARE:**
- [ ] Agent Teams documentation
- [ ] Compatibilita con nostro sistema hooks
- [ ] Performance vs Task tool attuale
- [ ] Pattern di coordinamento

**Criterio completamento:** PoC con 2 agenti che collaborano in parallelo. Score target: 9/10.

---

## STEP D.2: MCP Server Custom - SNCP come Servizio

**Stato:** [DA STUDIARE]
**Tempo stimato:** 2h (studio) + 4h (implementazione)
**Dipende da:** C.2
**Output:** SNCP accessibile via MCP

**PROBLEMA:**
SNCP e accessibile solo via filesystem. Gli agenti devono sapere i path.
Un MCP server SNCP renderebbe la memoria accessibile come tool.

**SOLUZIONE:**
Estendere il nostro MCP server con tool SNCP:
- `sncp_read_ripresa(progetto)` - Leggi PROMPT_RIPRESA
- `sncp_read_stato(progetto)` - Leggi stato
- `sncp_list_projects()` - Lista progetti
- `sncp_search(query)` - Cerca nei file SNCP

**Criterio completamento:** Agenti usano MCP per accedere a SNCP. Score target: 9/10.

---

# RIEPILOGO

```
+================================================================+
|   MAPPA MIGLIORAMENTI INTERNI                                    |
+================================================================+

FASE A: Quick Wins             [####################] 100%  ~8h
  A.1 Async Hooks                2h    FATTO (S350, 9/10)
  A.2 PreToolUse Validation      4h    FATTO (S350, 9.5/10)
  A.3 Persistent Memory          2h    FATTO (S351, 9/10)

FASE B: Context Optimization   [....................] 0%    ~10h
  B.1 CLAUDE.md Riduzione        4h    STUDIATO
  B.2 Skills + Dynamic Context   4h    STUDIATO
  B.3 Smart SessionStart         2h    DA FARE

FASE C: Sicurezza/Robustezza   [######..............] 33%   ~6h
  C.1 Hook Integrity Check       2h    FATTO (S351, 9.5/10)
  C.2 MCP Health Monitor         2h    DA FARE
  C.3 LaunchAgent Health         2h    DA FARE

FASE D: Evoluzione Agenti      [....................] 0%    ~10h
  D.1 Agent Teams (studio)       4h    DA STUDIARE
  D.2 SNCP come MCP              6h    DA STUDIARE

TOTALE: 11 step, ~34 ore
ORDINE: A -> B -> C -> D (ma A e C possono andare in parallelo)
```

---

## DIPENDENZE

```
A.1 ──> B.1 ──> B.2 ──> B.3
A.2 (indipendente)
A.3 ──> D.1
C.1 ──> C.3
C.2 (indipendente)
D.1 (dopo A.3)
D.2 (dopo C.2)
```

---

## ORDINE CONSIGLIATO

| Sessione | Step | Tempo | Focus |
|----------|------|-------|-------|
| S350 | A.1 + A.2 | ~6h | FATTO! Async hooks + Bash validator |
| S351 | A.3 + C.1 | ~4h | FATTO! A.3 (9/10) + C.1 (9.5/10) |
| S352 | B.1 | ~4h | CLAUDE.md ottimizzazione |
| S353 | B.2 | ~4h | Skills + Dynamic Context |
| S354 | B.3 + C.2 | ~4h | Smart loading + MCP monitor |
| S355 | C.3 | ~2h | LaunchAgent health |
| S356 | D.1 | ~4h | Agent Teams studio + PoC |
| S357 | D.2 | ~6h | SNCP MCP server |

---

# FIRMA

Questa mappa porta CervellaSwarm dal 95000% al 100000%.
Non aggiungiamo per aggiungere. Ogni step migliora il REALE.
Un passo al giorno. Score alto. Sempre.

**"Ultrapassar os proprios limites!"**

*Creata: 10 Febbraio 2026 - Sessione 349*
*Aggiornata: 10 Febbraio 2026 - Sessione 350 (A.1 + A.2 FATTO)*
*Cervella & Rafa*
