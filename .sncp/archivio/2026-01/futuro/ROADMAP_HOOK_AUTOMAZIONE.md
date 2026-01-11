# ROADMAP Hook Automazione SNCP

> **Data:** 11 Gennaio 2026
> **Status:** In Sviluppo
> **Priorita:** Media-Alta

---

## STATO ATTUALE

### Hook Esistenti

| Hook | File | Funzione | Status |
|------|------|----------|--------|
| sncp_auto_update.py | scripts/memory/ | Auto-checkpoint fine sessione | ATTIVO |
| debug_hook.py | scripts/memory/ | Debug payload hook | ATTIVO |

### Cosa Fa sncp_auto_update.py

1. **SessionStart:** Verifica file obsoleti (>48h)
2. **SessionEnd:** Appende checkpoint a `stato/oggi.md`

---

## HOOK PIANIFICATI

### PRIORITA 1: Questa Settimana

#### Hook 1: SNCP Health Check
```python
# Trigger: SessionStart
# Azione: Calcola health score SNCP
# Output: Warning se score < 7/10

Metriche:
- File aggiornati ultimi 7 giorni
- Lezioni documentate vs bug fix
- Sessioni loggate vs commit
- Idee organizzate vs sparse
```

#### Hook 2: Weekly SNCP Report
```python
# Trigger: Lunedi mattina (cron-like)
# Azione: Genera report settimanale
# Output: File in reports/sncp_health_YYYYMMDD.md

Report include:
- Score SNCP 0-10
- File piu attivi
- GAP identificati
- Suggerimenti miglioramento
```

### PRIORITA 2: Prossime 2 Settimane

#### Hook 3: Audit Trail Auto
```python
# Trigger: PostToolUse (Edit, Write)
# Azione: Log modifiche significative
# Output: Log in data/logs/audit_trail.jsonl

Traccia:
- File modificati
- Timestamp
- Worker/Regina
- Tipo modifica
```

#### Hook 4: SNCP Troppo Vuoto
```python
# Trigger: SessionEnd
# Azione: Warning se SNCP non usato durante sessione
# Output: Prompt "Hai dimenticato di documentare?"

Check:
- Nessun file scritto in .sncp/
- Sessione > 30 min
- Modifiche significative al codice
```

#### Hook 5: Domande con Scadenza
```python
# Trigger: SessionStart
# Azione: Check domande aperte scadute
# Output: Warning se scadenze superate

File: coscienza/domande_aperte.md
Format: - [ ] Domanda @deadline:2026-01-15
```

### PRIORITA 3: Prossimo Mese

#### Hook 6: Pattern Emerso Auto
```python
# Trigger: PostToolUse (se 3+ volte stesso pattern)
# Azione: Suggerisce di documentare pattern
# Output: Prompt + draft in coscienza/pattern_emersi.md
```

#### Hook 7: Lezione da Bug
```python
# Trigger: Dopo fix bug (commit con "fix" o "bug")
# Azione: Prompt per documentare lezione
# Output: Template pre-compilato in memoria/lezioni/
```

#### Hook 8: Correlazione Codice-SNCP
```python
# Trigger: PostToolUse (Edit file importanti)
# Azione: Verifica se SNCP aggiornato
# Output: Reminder se modifica significativa non documentata
```

---

## IMPLEMENTAZIONE SUGGERITA

### Struttura File Hook

```
scripts/
├── hooks/
│   ├── __init__.py
│   ├── sncp_health.py      # Hook 1
│   ├── weekly_report.py    # Hook 2
│   ├── audit_trail.py      # Hook 3
│   ├── empty_warning.py    # Hook 4
│   ├── deadline_check.py   # Hook 5
│   ├── pattern_detect.py   # Hook 6
│   ├── bug_to_lesson.py    # Hook 7
│   └── code_sncp_link.py   # Hook 8
└── memory/
    ├── sncp_auto_update.py # Esistente
    └── debug_hook.py       # Esistente
```

### Registrazione in settings.json

```json
{
  "hooks": {
    "SessionStart": [
      "python scripts/memory/sncp_auto_update.py",
      "python scripts/hooks/sncp_health.py",
      "python scripts/hooks/deadline_check.py"
    ],
    "SessionEnd": [
      "python scripts/memory/sncp_auto_update.py",
      "python scripts/hooks/empty_warning.py"
    ],
    "PostToolUse": [
      "python scripts/hooks/audit_trail.py",
      "python scripts/hooks/pattern_detect.py"
    ]
  }
}
```

---

## I 15 SUGGERIMENTI (da Ricerca)

| # | Suggerimento | Hook Collegato | Status |
|---|--------------|----------------|--------|
| 1 | ADR Pattern per decisioni | Template | FATTO |
| 2 | Session log strutturato | Template | FATTO |
| 3 | Lezioni con categoria + impatto | Template | FATTO |
| 4 | Idee linkate a decisioni | Template | FATTO |
| 5 | Audit trail automatico | Hook 3 | TODO |
| 6 | Weekly SNCP health report | Hook 2 | TODO |
| 7 | Template per "blocco tecnico" | Template | TODO |
| 8 | Correlazione codice-SNCP | Hook 8 | TODO |
| 9 | Domande aperte con scadenza | Hook 5 | TODO |
| 10 | Pattern -> linea guida | Hook 6 | TODO |
| 11 | Roadmap live vs archivio | Organizzazione | FATTO |
| 12 | Categoria frontmatter | Template | FATTO |
| 13 | Lezioni riusabili | Template | FATTO |
| 14 | idee/scartate/ per non perdere | Cartella | FATTO |
| 15 | Hook "SNCP troppo vuoto" | Hook 4 | TODO |

---

## METRICHE SUCCESSO

| Metrica | Prima | Target 30gg |
|---------|-------|-------------|
| Score SNCP | 5/10 | 9/10 |
| Hook attivi | 2 | 5 |
| Automazione | 20% | 60% |
| Warning ignorati | N/A | < 10% |

---

## PROSSIMI STEP

1. [ ] Implementare Hook 1 (SNCP Health Check)
2. [ ] Implementare Hook 4 (SNCP Troppo Vuoto)
3. [ ] Testare su 3 sessioni
4. [ ] Aggiungere altri hook gradualmente

---

*"L'automazione ci libera dalla disciplina"*
*"SNCP cresce con noi!"*
