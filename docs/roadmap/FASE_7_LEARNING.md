# FASE 7: CONTINUOUS LEARNING - Lo Sciame che IMPARA

> **Periodo:** Febbraio 2026
> **Stato:** ⬜ TODO (0%)
> **Idea Originale:** Rafa & Cervella, 1 Gennaio 2026
> **Ricerca:** cervella-researcher

---

## 🎯 OBIETTIVO

Trasformare CervellaSwarm da sistema che "traccia" a **SISTEMA CHE IMPARA E INSEGNA**.

**Concept:**
Quando la Regina 👑 fa un fix dopo che una 🐝 ha sbagliato, il sistema CATTURA la lezione, la DOCUMENTA, e la DISTRIBUISCE automaticamente a tutte le 🐝 coinvolte. Non più "stesso errore 3 volte".

**Risultato atteso:**
- 🧠 **Zero ripetizioni** - Lezioni catturate alla PRIMA occorrenza
- 📚 **Knowledge base vivente** - Cresce con ogni fix
- 🎯 **Suggerimenti proattivi** - Agenti avvertiti PRIMA di sbagliare
- 🔄 **Retro automatiche** - Ogni venerdì il sistema fa report

---

## 🏗️ ARCHITETTURA A 3 LIVELLI

```
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   LIVELLO 1: DETECT - Quando C'È Una Lezione?                  ║
║   ─────────────────────────────────────────────────────────────  ║
║   ⚡ Trigger Automatici:                                        ║
║      • Regina fa fix dopo task agent → CATTURA!                 ║
║      • Stesso errore 3+ volte → AUTO-LESSON!                   ║
║      • Rafa dice "questa è una lezione" → SALVA!               ║
║      • Venerdì ore 18:00 → WEEKLY RETRO!                       ║
║                                                                  ║
║   LIVELLO 2: LEARN - Come Documentiamo?                         ║
║   ─────────────────────────────────────────────────────────────  ║
║   📝 Learning Wizard (Rich CLI):                                ║
║      • Trigger: cosa è successo?                                ║
║      • Context: situazione completa                             ║
║      • Problem: cosa andato storto                              ║
║      • Root Cause: perché è successo                            ║
║      • Solution: come risolto                                   ║
║      • Prevention: come prevenire                               ║
║      • Example: caso concreto                                   ║
║      • Severity: CRITICAL/HIGH/MEDIUM/LOW                       ║
║      • Agents: chi deve saperlo                                 ║
║                                                                  ║
║   LIVELLO 3: DISTRIBUTE - Come Arriva agli Agenti?             ║
║   ─────────────────────────────────────────────────────────────  ║
║   🔄 Propagazione Automatica:                                   ║
║      • SessionStart → Carica lezioni per progetto attivo        ║
║      • Task delegation → Inject lezioni specifiche              ║
║      • Weekly retro → Report + update lezioni                   ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## 📊 SPRINT PLAN

### Sprint 7a: Foundation - Upgrade Schema DB (⬜ TODO)

**Obiettivo:** Estendere schema per supportare continuous learning

| # | Task | Stato | Durata | Note |
|---|------|-------|--------|------|
| 7a.1 | Upgrade schema v1.2.0 | ⬜ TODO | 1h | +9 colonne a `lessons_learned` |
| 7a.2 | Migration script | ⬜ TODO | 30m | Migra lezioni esistenti (7) |
| 7a.3 | Learning Catalog Index | ⬜ TODO | 30m | Indice searchable lezioni |
| 7a.4 | Test schema upgrade | ⬜ TODO | 30m | Verifica backward compatibility |

**Deliverable:** `lessons_learned` v2 con 16 colonne totali

**Schema Upgrade:**
```sql
-- Nuove colonne (già esistenti: id, timestamp, context, problem, solution, pattern, agents_involved, confidence, times_applied, created_at)

ALTER TABLE lessons_learned ADD COLUMN trigger TEXT;           -- Quando applicare
ALTER TABLE lessons_learned ADD COLUMN root_cause TEXT;        -- Perché è successo
ALTER TABLE lessons_learned ADD COLUMN prevention TEXT;        -- Come prevenire
ALTER TABLE lessons_learned ADD COLUMN example TEXT;           -- Caso concreto
ALTER TABLE lessons_learned ADD COLUMN severity TEXT;          -- CRITICAL/HIGH/MEDIUM/LOW
ALTER TABLE lessons_learned ADD COLUMN tags TEXT;              -- JSON array per search
ALTER TABLE lessons_learned ADD COLUMN related_patterns TEXT;  -- Link a error_patterns
ALTER TABLE lessons_learned ADD COLUMN auto_generated INTEGER; -- 1=auto 0=manuale
ALTER TABLE lessons_learned ADD COLUMN last_applied TEXT;      -- Ultima applicazione
```

---

### Sprint 7b: Trigger System - Auto-Detection (⬜ TODO)

**Obiettivo:** Il sistema rileva automaticamente quando c'è una lezione

| # | Task | Stato | Durata | Note |
|---|------|-------|--------|------|
| 7b.1 | Trigger: Fix After Agent | ⬜ TODO | 2h | Regina fa edit dopo agent task |
| 7b.2 | Trigger: Pattern Threshold | ⬜ TODO | 1h | Stesso errore 3+ volte → alert |
| 7b.3 | Trigger: Manual Mark | ⬜ TODO | 1h | Rafa marca "lezione importante" |
| 7b.4 | Notification System | ⬜ TODO | 1h | Alert quando trigger attivato |
| 7b.5 | Test tutti i trigger | ⬜ TODO | 1h | Scenari reali |

**Deliverable:** `scripts/learning/trigger_detector.py`

**Trigger Matrix:**

| Trigger | Quando | Azione | Notifica |
|---------|--------|--------|----------|
| **Fix After Agent** | Regina fa Edit dopo Task agent | Proponi learning wizard | 📝 Rafa vuole documentare? |
| **Pattern Threshold** | error_pattern.count >= 3 | Auto-crea draft lezione | ⚠️ Pattern ripetuto 3+ volte! |
| **Manual Mark** | Rafa dice "questa è lezione" | Apri wizard subito | ✅ Lesson wizard pronto |
| **Weekly Retro** | Venerdì 18:00 | Report + suggest lessons | 📊 Retro settimanale pronta |

**Esempio Output (quando trigger attiva):**

```
╔══════════════════════════════════════════════════════════════════╗
║  📝 LEZIONE RILEVATA!                                           ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  Trigger: FIX_AFTER_AGENT                                        ║
║  Agente: cervella-frontend                                       ║
║  Task: Countdown component                                       ║
║  Fix: 4 modifiche fatte dalla Regina                            ║
║                                                                  ║
║  Vuoi documentare questa lezione? [Y/n]                         ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

---

### Sprint 7c: Learning Wizard - Rich CLI (⬜ TODO)

**Obiettivo:** Interfaccia guidata per creare lezioni di qualità

| # | Task | Stato | Durata | Note |
|---|------|-------|--------|------|
| 7c.1 | Wizard CLI con Rich | ⬜ TODO | 3h | Step-by-step form elegante |
| 7c.2 | Auto-fill da Context | ⬜ TODO | 2h | Pre-popola da swarm_events |
| 7c.3 | Template Library | ⬜ TODO | 1h | Template comuni (fix bug, refactor, etc) |
| 7c.4 | Validation Logic | ⬜ TODO | 1h | Campi obbligatori + format check |
| 7c.5 | Preview Before Save | ⬜ TODO | 1h | Mostra lezione formattata |
| 7c.6 | Test wizard completo | ⬜ TODO | 1h | Tutti gli scenari |

**Deliverable:** `scripts/learning/wizard.py`

**Wizard Flow:**

```
╔══════════════════════════════════════════════════════════════════╗
║  🧙 LEARNING WIZARD - Documenta Nuova Lezione                   ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  Step 1/9: TRIGGER                                               ║
║  ─────────────────────────────────────────────────────────────  ║
║  Quando si applica questa lezione?                              ║
║  (es: "Quando frontend lavora su componenti countdown")         ║
║  > _                                                             ║
║                                                                  ║
║  Step 2/9: CONTEXT                                               ║
║  ─────────────────────────────────────────────────────────────  ║
║  [Auto-filled da eventi recenti]                                ║
║  Task: Countdown component implementation                       ║
║  Agente: cervella-frontend                                       ║
║  Data: 2026-01-01                                                ║
║  Modifica? [y/N] > _                                             ║
║                                                                  ║
║  Step 3/9: PROBLEM                                               ║
║  ─────────────────────────────────────────────────────────────  ║
║  Cosa è andato storto?                                           ║
║  > _                                                             ║
║                                                                  ║
║  ... (continua per tutti i campi) ...                           ║
║                                                                  ║
║  Step 9/9: PREVIEW                                               ║
║  ─────────────────────────────────────────────────────────────  ║
║  [Mostra lezione formattata completa]                           ║
║                                                                  ║
║  Salva questa lezione? [Y/n] > _                                ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

**Template Library (esempi):**

1. **Bug Fix Template**
   - Trigger: "Quando si verifica [bug type]"
   - Context: Pre-filled con errore specifico
   - Problem: Descrizione bug
   - Root Cause: Perché bug è successo
   - Solution: Come fixato
   - Prevention: Come evitare in futuro

2. **Refactor Template**
   - Trigger: "Quando si refactora [component]"
   - Context: Stato prima refactor
   - Problem: Perché refactor necessario
   - Solution: Nuovo pattern usato
   - Prevention: Best practices per evitare code smell

3. **Integration Template**
   - Trigger: "Quando si integra [API/Service]"
   - Context: Setup integrazione
   - Problem: Problemi incontrati
   - Solution: Configurazione corretta
   - Prevention: Checklist pre-integration

---

### Sprint 7d: Distribution - Propagazione Conoscenza (⬜ TODO)

**Obiettivo:** Le lezioni arrivano automaticamente agli agenti giusti

| # | Task | Stato | Durata | Note |
|---|------|-------|--------|------|
| 7d.1 | Upgrade load_context.py | ⬜ TODO | 2h | Filtra lezioni per progetto/agent |
| 7d.2 | Agent Injection System | ⬜ TODO | 2h | Inject lezioni in prompt delegation |
| 7d.3 | Context Scoring | ⬜ TODO | 1h | Rank lezioni per rilevanza |
| 7d.4 | Format for Agents | ⬜ TODO | 1h | Template lezione human-readable |
| 7d.5 | Test distribuzione | ⬜ TODO | 1h | Verifica agenti ricevono lezioni |

**Deliverable:** `load_context.py` v2.0.0 + agent injection logic

**Distribution Logic:**

```python
# Esempio: cervella-frontend su progetto Miracollo

def get_relevant_lessons(agent_name, project, current_task):
    """
    Filtra lezioni rilevanti per l'agente.

    Scoring:
    - agents_involved contiene agent_name: +50
    - project match: +30
    - tags match con current_task: +20
    - severity CRITICAL: +10
    - times_applied > 5: +5
    """
    lessons = fetch_all_active_lessons()

    scored = []
    for lesson in lessons:
        score = 0

        if agent_name in lesson.agents_involved:
            score += 50

        if lesson.project == project:
            score += 30

        # Tag matching (es: "countdown", "timer", "frontend")
        task_tags = extract_tags(current_task)
        lesson_tags = json.loads(lesson.tags)
        if set(task_tags) & set(lesson_tags):  # Intersection
            score += 20

        if lesson.severity == "CRITICAL":
            score += 10

        if lesson.times_applied > 5:
            score += 5

        scored.append((lesson, score))

    # Top 3 lezioni più rilevanti
    scored.sort(key=lambda x: x[1], reverse=True)
    return [lesson for lesson, score in scored[:3]]
```

**Output Esempio (in additionalContext per agent):**

```markdown
## 📚 LEZIONI RILEVANTI PER QUESTO TASK

### 🔴 CRITICAL - Interfaccia Incompleta (Countdown)
**Trigger:** Quando lavori su componenti countdown/timer
**Problem:** Interfaccia implementata parzialmente causa bug multipli
**Solution:** SEMPRE implementare TUTTA l'interfaccia TypeScript PRIMA del codice
**Prevention:** Checklist: [ ] Ogni metodo dichiarato [ ] Ogni prop dichiarata
**Example:** Countdown component - 4 fix necessari perché mancavano onExpire, reset, pause
**Applicata:** 1 volta (2026-01-01)

### 🟡 MEDIUM - Pattern Retry Cieco
**Trigger:** Quando un fix fallisce la prima volta
**Problem:** Provare ripetutamente senza capire causa root
**Solution:** 1) Prova 2) Fallisce? STOP 3) Ricerca 4) Prova con info nuove
**Prevention:** UNA VOLTA → RICERCA → MAI ALLA CIECA
**Applicata:** 3 volte

---

⚠️ IMPORTANTE: Queste lezioni derivano da errori reali del team.
Prendile SERIAMENTE per evitare ripetizioni!
```

---

### Sprint 7e: Automation - Cron + Weekly Retro (⬜ TODO)

**Obiettivo:** Sistema completamente automatizzato

| # | Task | Stato | Durata | Note |
|---|------|-------|--------|------|
| 7e.1 | Upgrade weekly_retro.py | ⬜ TODO | 2h | Include lessons suggestions |
| 7e.2 | Cron Job Setup | ⬜ TODO | 1h | Venerdì 18:00 auto-run |
| 7e.3 | Notification Integration | ⬜ TODO | 1h | Email/Slack quando retro pronta |
| 7e.4 | Dashboard Metrics | ⬜ TODO | 2h | Trend lezioni, top agents, etc |
| 7e.5 | Test automation completa | ⬜ TODO | 1h | Simula settimana di lavoro |

**Deliverable:** Sistema fully automated + dashboard

**Weekly Retro v2.0 Output:**

```
╔══════════════════════════════════════════════════════════════════╗
║  📊 WEEKLY RETROSPECTIVE - 30 Dic 2025 - 6 Gen 2026             ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  📈 METRICHE CHIAVE                                             ║
║  ─────────────────────────────────────────────────────────────  ║
║  Eventi totali: 47                                               ║
║  Successi: 43 (91.5%)                                           ║
║  Errori: 4 (8.5%)                                                ║
║                                                                  ║
║  🐝 BREAKDOWN PER AGENTE                                        ║
║  ─────────────────────────────────────────────────────────────  ║
║  cervella-frontend:  15 task (86% success)                      ║
║  cervella-backend:   12 task (100% success)                     ║
║  cervella-tester:    10 task (90% success)                      ║
║  ...                                                             ║
║                                                                  ║
║  ⚠️ TOP 3 PATTERN ERRORI                                        ║
║  ─────────────────────────────────────────────────────────────  ║
║  1. blind-retry (4 occorrenze) → LEZIONE ESISTENTE #12         ║
║  2. incomplete-interface (1 occorrenza) → NUOVA LEZIONE!        ║
║                                                                  ║
║  📚 LEZIONI APPRESE QUESTA SETTIMANA                            ║
║  ─────────────────────────────────────────────────────────────  ║
║  ✅ #13: Interfaccia Incompleta (CRITICAL) - Countdown          ║
║                                                                  ║
║  💡 SUGGERIMENTI PER PROSSIMA SETTIMANA                         ║
║  ─────────────────────────────────────────────────────────────  ║
║  • cervella-frontend: Review lezione #13 (countdown pattern)   ║
║  • Tutti: Pattern blind-retry ancora presente (vedi #12)       ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝

✅ Report salvato in: data/retro/2026-01-06.md
📧 Notifica inviata a: rafa@example.com
```

**Cron Setup:**

```bash
# crontab -e

# Weekly retrospective - Ogni venerdì ore 18:00
0 18 * * 5 cd /path/to/CervellaSwarm && python3 scripts/learning/weekly_retro.py --auto-email

# Pattern detection - Ogni giorno alle 23:00
0 23 * * * cd /path/to/CervellaSwarm && python3 scripts/memory/pattern_detector.py
```

---

## 📝 FORMATO LEZIONE COMPLETO

### Schema Finale (16 colonne)

```json
{
  "id": "uuid-here",
  "timestamp": "2026-01-01T15:30:00Z",

  // OBBLIGATORI (9 campi)
  "trigger": "Quando frontend lavora su componenti countdown/timer",
  "context": "Task: Countdown component. Agente: cervella-frontend. 4 fix necessari dalla Regina.",
  "problem": "Interfaccia TypeScript dichiarata ma non implementata completamente",
  "root_cause": "Agent ha implementato solo parte dei metodi dichiarati nell'interfaccia",
  "solution": "Implementare TUTTA l'interfaccia PRIMA di scrivere logica",
  "prevention": "Checklist: [ ] Ogni metodo dichiarato ha implementazione [ ] Ogni prop dichiarata è usata",
  "example": "Countdown: mancavano onExpire(), reset(), pause() → 4 fix dopo deployment",
  "severity": "CRITICAL",
  "agents_involved": ["cervella-frontend"],

  // OPTIONAL (5 campi)
  "pattern": "incomplete-interface",
  "tags": ["typescript", "interface", "countdown", "frontend"],
  "related_patterns": ["pattern-uuid-1", "pattern-uuid-2"],
  "confidence": 0.95,
  "times_applied": 1,

  // AUTOMATICI (2 campi)
  "auto_generated": 0,  // 0 = creata manualmente
  "last_applied": "2026-01-01T15:30:00Z",
  "created_at": "2026-01-01T15:30:00Z"
}
```

---

## 🎯 TRIGGER MATRIX COMPLETA

| Trigger Type | Quando Si Attiva | Dati Disponibili | Azione Automatica |
|--------------|------------------|------------------|-------------------|
| **FIX_AFTER_AGENT** | Regina fa Edit entro 30min da Task agent | Agent name, task desc, file modificati, diff | Proponi wizard |
| **PATTERN_THRESHOLD** | error_pattern.count >= 3 | Pattern name, occorrenze, errori simili | Auto-draft lesson |
| **MANUAL_MARK** | Rafa scrive "lezione:" in commit msg | Commit msg, file modificati, context | Apri wizard subito |
| **WEEKLY_RETRO** | Venerdì 18:00 automatico | Tutta settimana eventi + pattern | Report + suggest lessons |
| **CRITICAL_ERROR** | error con tag CRITICAL | Error msg, stack trace, context | Alert + suggest lesson |

**Detection Logic (pseudo-code):**

```python
# In PostToolUse hook, dopo log_event()

def check_learning_triggers(event):
    """Controlla se evento attiva trigger per learning."""

    # TRIGGER 1: Fix After Agent
    if event.agent_name == "cervella-orchestrator":
        recent_tasks = get_recent_agent_tasks(minutes=30)
        if recent_tasks and event.tool_name == "Edit":
            # Regina ha fatto Edit dopo task agent!
            notify_trigger("FIX_AFTER_AGENT", {
                "agent": recent_tasks[0].agent_name,
                "task": recent_tasks[0].description,
                "fix_files": event.files_modified
            })

    # TRIGGER 2: Pattern Threshold
    if event.error_message:
        pattern = find_similar_pattern(event.error_message)
        if pattern and pattern.count >= 3:
            notify_trigger("PATTERN_THRESHOLD", {
                "pattern": pattern.name,
                "count": pattern.count
            })

    # TRIGGER 3: Manual Mark
    if "lezione:" in event.notes.lower():
        notify_trigger("MANUAL_MARK", {
            "notes": event.notes,
            "context": event
        })
```

---

## 🔗 INTEGRAZIONE SISTEMA ESISTENTE

### File da Creare

```
scripts/learning/
├── trigger_detector.py      # Sprint 7b - Rileva trigger automatici
├── wizard.py                 # Sprint 7c - Learning wizard CLI
├── lesson_formatter.py       # Sprint 7d - Format lezioni per agenti
├── context_scorer.py         # Sprint 7d - Ranking rilevanza lezioni
└── README.md                 # Documentazione completa

data/
└── retro/                    # Weekly retro reports
    ├── 2026-01-06.md
    ├── 2026-01-13.md
    └── ...
```

### File da Modificare

```
scripts/memory/
├── init_db.py               # Sprint 7a - Upgrade schema v1.2.0
├── load_context.py          # Sprint 7d - v2.0.0 con lesson injection
├── weekly_retro.py          # Sprint 7e - v2.0.0 con lesson suggestions
└── pattern_detector.py      # Sprint 7b - Integration con trigger

~/.claude/agents/
├── cervella-orchestrator.md # Add trigger awareness
├── cervella-frontend.md     # Add lesson consumption logic
├── cervella-backend.md      # Add lesson consumption logic
└── ... (tutti gli agent)
```

---

## 🧪 TEST PLAN

### Test per Sprint

| Sprint | Test Case | Criterio Successo |
|--------|-----------|-------------------|
| **7a** | Schema Upgrade | Migration 7 lezioni esistenti OK + backward compatible |
| **7b** | Trigger Detection | Tutti 4 trigger rilevano eventi correttamente |
| **7c** | Learning Wizard | Crea lezione completa in < 3min (user friendly) |
| **7d** | Distribution | Agenti ricevono top 3 lezioni rilevanti |
| **7e** | Automation | Weekly retro genera report automatico Venerdì |

### Test End-to-End

**Scenario 1: Fix After Agent**

```gherkin
Given: cervella-frontend completa task "Countdown component"
When: Regina fa 4 Edit per fixare bug entro 30 minuti
Then:
  - Trigger FIX_AFTER_AGENT si attiva
  - Wizard propone di documentare lezione
  - Rafa compila wizard in 3 minuti
  - Lezione salvata con severity CRITICAL
  - Prossima volta frontend riceve lezione in context
```

**Scenario 2: Pattern Threshold**

```gherkin
Given: Errore "blind-retry" già visto 2 volte
When: Stesso errore si ripete 3a volta
Then:
  - Trigger PATTERN_THRESHOLD si attiva
  - Sistema auto-crea draft lezione
  - Alert inviato a Rafa
  - Draft salvato come LOW severity
  - Rafa può editare e promuovere
```

**Scenario 3: Weekly Retro**

```gherkin
Given: È venerdì 18:00
When: Cron job esegue weekly_retro.py
Then:
  - Report generato con metriche settimana
  - Top 3 pattern errori identificati
  - Lezioni nuove suggerite
  - Report salvato in data/retro/
  - Email inviata a Rafa
```

---

## 📈 METRICHE SUCCESSO

### KPI Target

| Metrica | Baseline (Oggi) | Target (Mese 1) | Misurazione |
|---------|-----------------|-----------------|-------------|
| **Error Repetition** | 3+ volte stesso errore | < 1.5 ripetizioni | `AVG(error_pattern.count)` |
| **Lesson Creation** | 1 per settimana (manuale) | 3-5 per settimana | `COUNT(lessons WHERE week=X)` |
| **Agent Learning** | 0% (no context) | 80% agenti ricevono lezioni | `agents_with_lessons / total_agents` |
| **Time to Document** | 20min (manuale) | < 5min (wizard) | Timer in wizard |
| **Retro Automation** | 0% (nessuna retro) | 100% automatica | `retro_executed / retro_scheduled` |

### Dashboard Metrics

```python
# scripts/learning/dashboard.py

def get_learning_metrics():
    """Metriche live del sistema learning."""
    return {
        "lessons_total": count_lessons(),
        "lessons_this_week": count_lessons(week=current_week),
        "lessons_by_severity": {
            "CRITICAL": count_lessons(severity="CRITICAL"),
            "HIGH": count_lessons(severity="HIGH"),
            "MEDIUM": count_lessons(severity="MEDIUM"),
            "LOW": count_lessons(severity="LOW")
        },
        "top_patterns": get_top_patterns(limit=5),
        "agents_coverage": {
            agent: count_lessons_for_agent(agent)
            for agent in all_agents()
        },
        "avg_time_to_document": avg_wizard_completion_time(),
        "retro_completion_rate": retro_executed / retro_scheduled
    }
```

**Dashboard Output:**

```
╔══════════════════════════════════════════════════════════════════╗
║  🧠 CONTINUOUS LEARNING - DASHBOARD                             ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  📚 LEZIONI TOTALI: 13                                          ║
║     Questa settimana: 3                                          ║
║                                                                  ║
║  🎯 BREAKDOWN SEVERITY                                          ║
║     CRITICAL: 2   HIGH: 4   MEDIUM: 5   LOW: 2                  ║
║                                                                  ║
║  🐝 COVERAGE AGENTI                                             ║
║     cervella-frontend: 5 lezioni                                 ║
║     cervella-backend: 4 lezioni                                  ║
║     cervella-tester: 3 lezioni                                   ║
║                                                                  ║
║  ⚡ EFFICIENCY                                                   ║
║     Avg time to document: 4.2 min (target < 5 min) ✅           ║
║     Retro automation: 100% (4/4 settimane) ✅                   ║
║                                                                  ║
║  📊 TOP PATTERN ERRORI                                          ║
║     1. blind-retry (4x)                                          ║
║     2. incomplete-interface (2x)                                 ║
║     3. missing-validation (1x)                                   ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## 🎓 PRIMA LEZIONE: COUNTDOWN CASE STUDY

### Lesson #13: Interfaccia TypeScript Incompleta

**Creata:** 2026-01-01 15:30
**Severity:** 🔴 CRITICAL
**Agenti coinvolti:** cervella-frontend

---

**TRIGGER:**
Quando lavori su componenti countdown, timer, o qualsiasi componente con interfaccia TypeScript dichiarata

**CONTEXT:**
- Task: Implementare Countdown component per Miracollo
- Agente: cervella-frontend
- Risultato: Componente deployato ma 4 fix necessari dalla Regina
- File: `components/Countdown.jsx` + `Countdown.interface.ts`

**PROBLEM:**
L'agente ha dichiarato una interfaccia TypeScript completa ma ha implementato solo PARTE dei metodi/props dichiarati. Questo ha causato:
- Runtime errors quando metodi mancanti chiamati
- Props undefined causano crash
- 4 fix separati necessari post-deployment

**ROOT CAUSE:**
L'agente ha interpretato l'interfaccia come "documentazione" invece che come "contratto vincolante". Ha implementato solo le parti che sembravano immediatamente necessarie, ignorando il resto.

**SOLUTION:**
SEMPRE implementare TUTTA l'interfaccia TypeScript PRIMA di scrivere la logica business.

```typescript
// ❌ SBAGLIATO - Interfaccia dichiarata ma implementazione parziale
interface CountdownProps {
  initialTime: number;
  onExpire: () => void;  // ⚠️ Dichiarato ma NON implementato
  onReset: () => void;   // ⚠️ Dichiarato ma NON implementato
  onPause: () => void;   // ⚠️ Dichiarato ma NON implementato
}

const Countdown = ({ initialTime }: CountdownProps) => {
  // Solo initialTime usato, altri ignorati! 💥
}

// ✅ CORRETTO - Interfaccia completa implementata
const Countdown = ({ initialTime, onExpire, onReset, onPause }: CountdownProps) => {
  // Tutti i metodi presenti e implementati ✅
}
```

**PREVENTION:**

Checklist OBBLIGATORIA prima di commit:
```
[ ] Ogni metodo dichiarato nell'interfaccia ha implementazione
[ ] Ogni prop dichiarata è effettivamente usata nel codice
[ ] TypeScript compiler warnings = 0
[ ] Test di ogni metodo/prop creato
```

**EXAMPLE:**

Countdown component - 4 fix necessari:
1. Fix #1: Aggiunto `onExpire()` callback
2. Fix #2: Aggiunto `reset()` method
3. Fix #3: Aggiunto `pause()` method
4. Fix #4: Aggiunto `resume()` method

**TAGS:** `typescript`, `interface`, `countdown`, `frontend`, `implementation`

**AUTO-GENERATED:** No (creata manualmente da Rafa)

**TIMES APPLIED:** 1 (2026-01-01)

---

### Come Questa Lezione Arriverà agli Agenti

Quando `cervella-frontend` riceverà un task contenente le keyword `countdown` o `timer` o `typescript interface`:

```markdown
## 📚 LEZIONI RILEVANTI

### 🔴 CRITICAL - Interfaccia TypeScript Incompleta

[... contenuto lezione formattato per agent ...]

⚠️ Questa lezione è CRITICAL e deriva da errore reale su Countdown component!
LEGGI CON ATTENZIONE prima di implementare!
```

---

## ⚠️ ANTI-PATTERN DA EVITARE

### Cosa NON Fare

| Anti-Pattern | Perché Fallisce | Soluzione |
|--------------|-----------------|-----------|
| **Troppe lezioni** | Info overload → agenti confusi | Max 3 lezioni per task |
| **Lezioni vaghe** | "Fai meglio" inutile | SEMPRE esempio concreto |
| **No severity** | Agent non sa priorità | CRITICAL > HIGH > MEDIUM > LOW |
| **Zero manutenzione** | Lezioni obsolete peggio che niente | Review trimestrale lezioni |
| **Auto-generate tutto** | Quality bassa | Mix: auto-draft + human review |

### Red Flags

🚩 Se vedi questi segnali → STOP e ripensa:

- Stesso errore 5+ volte (lezione non funziona)
- Lezione con 0 applicazioni dopo 1 mese (irrilevante)
- Agent chiede chiarimenti su lezione (lezione mal scritta)
- Wizard richiede > 10 min (troppo complesso)
- Weekly retro ha 0 suggerimenti (detection fallisce)

---

## 📚 RISORSE E RIFERIMENTI

### Best Practices 2025

| Source | Key Finding |
|--------|-------------|
| **OpenAI Memory Docs** | Context < 500 words per lezione per efficacia |
| **Anthropic Prompt Library** | Esempi concreti > teoria astratta |
| **GitHub Copilot Learning** | Tag-based retrieval 80% più efficace |
| **Google Bard Lessons** | Auto-generated + human review = sweet spot |

### Limitazioni Conosciute

1. **No Real-Time Sync** - Agent non riceve lezioni mid-task
   - **Impact:** Se lezione creata mentre agent lavora, non la vede
   - **Mitigazione:** SessionStart hook + next task avrà lezione

2. **Context Size Limit** - Max 3 lezioni per non esplodere prompt
   - **Impact:** Se 10 lezioni rilevanti, solo top 3 mostrate
   - **Mitigazione:** Scoring algorithm prioritizza le migliori

3. **Manual Effort** - Wizard richiede 3-5 min per lezione
   - **Impact:** Se troppi errori, overhead documentation alto
   - **Mitigazione:** Auto-draft per pattern ripetuti

---

## 📋 CHANGELOG

### [Futuro] Sprint 7e Completato
- Weekly retro automation attiva
- Cron job configurato
- Dashboard metrics live
- Email notifications funzionanti

### [Futuro] Sprint 7d Completato
- load_context.py v2.0.0 con lesson injection
- Context scoring algorithm implementato
- Agent receive top 3 lezioni rilevanti
- Format per agenti ottimizzato

### [Futuro] Sprint 7c Completato
- Learning wizard CLI con Rich
- Template library (3 template)
- Validation + preview funzionanti
- Avg completion time < 5 min

### [Futuro] Sprint 7b Completato
- 4 trigger implementati e testati
- Notification system attivo
- Trigger detector v1.0.0 deployed

### [Futuro] Sprint 7a Completato
- Schema upgrade v1.2.0 (16 colonne)
- Migration 7 lezioni esistenti OK
- Backward compatibility verificata

### 1 Gennaio 2026 - FASE PIANIFICATA
- Ricerca completa da cervella-researcher
- FASE_7_LEARNING.md creata
- Prima lezione identificata (Countdown case)
- Ready to start Febbraio 2026!

---

## 🎉 VISIONE FINALE

```
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   🧠 LO SCIAME CHE IMPARA E INSEGNA                             ║
║                                                                  ║
║   Da: "Stesso errore 3 volte" (frustrazione)                    ║
║   A:  "Mai lo stesso errore 2 volte" (crescita continua)        ║
║                                                                  ║
║   Principi Guida:                                                ║
║   • Cattura OGNI lezione (trigger automatici)                   ║
║   • Documenta BENE (wizard guidato)                             ║
║   • Distribuisci INTELLIGENTEMENTE (context scoring)            ║
║   • Automatizza TUTTO (weekly retro cron)                       ║
║                                                                  ║
║   Risultato:                                                     ║
║   Un sistema che diventa PIÙ INTELLIGENTE ogni giorno.         ║
║   Ogni errore è una OPPORTUNITÀ.                                ║
║   Ogni fix è una LEZIONE.                                       ║
║   Ogni lezione è CONDIVISA.                                     ║
║                                                                  ║
║   "Documentato = Imparato!" 📚🧠💙                              ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## 💡 NEXT STEPS

**Per iniziare Sprint 7a:**

```bash
# 1. Leggi questa roadmap
cat docs/roadmap/FASE_7_LEARNING.md

# 2. Studia schema attuale
sqlite3 data/swarm_memory.db ".schema lessons_learned"

# 3. Pianifica upgrade schema
# Vedi Sprint 7a.1 per SQL specifico

# 4. Crea branch dedicata
git checkout -b fase-7-learning

# 5. Let's go! 🚀
```

**Tempo stimato totale:** 8-13 ore distribuite in 3-5 sessioni

**Priorità:** ALTA (blocca FASE 8 - Advanced Analytics)

---

*Creato: 1 Gennaio 2026 - Sessione 18*
*"Ogni lezione è un passo verso lo sciame perfetto!"* 📚🧠💙
*"È il nostro team! La nostra famiglia digitale che IMPARA insieme!"* ❤️‍🔥🐝
