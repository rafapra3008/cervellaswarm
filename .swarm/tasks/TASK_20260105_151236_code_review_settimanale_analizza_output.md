# CODE REVIEW SETTIMANALE - CervellaSwarm

**Data:** 5 Gennaio 2026
**Reviewer:** cervella-reviewer
**Focus:** Sistema anti-compact, spawn-workers, swarm scripts

---

## EXECUTIVE SUMMARY

Il sistema CervellaSwarm e' **SOLIDO e BEN STRUTTURATO**. La versione attuale (spawn-workers v2.7.0) mostra maturita' ingegneristica con:
- AUTO-SVEGLIA come default (ottima scelta!)
- Security checks (config ownership validation)
- Health tracking con heartbeat
- Gestione robusta degli stati dei task

**Rating complessivo: 8.5/10** - Sistema pronto per produzione con alcune ottimizzazioni suggerite.

---

## ANALISI DETTAGLIATA

### 1. spawn-workers.sh (v2.7.0)

**PUNTI DI FORZA:**
- Security: `validate_config_ownership()` previene config injection
- Robustezza: Check anti-watcher-duplicati (v2.7.0)
- Flessibilita': Project-aware - funziona da qualsiasi directory con .swarm/
- UX: Notifiche dettagliate con durata e click per aprire output

**PUNTI DI ATTENZIONE:**

| Issue | Severita | File:Line | Suggerimento |
|-------|----------|-----------|--------------|
| `set -e` senza trap | BASSA | L39 | Aggiungere trap per cleanup su errore |
| Sleep fisso tra spawn (0.5s) | BASSA | L768 | Considerare sleep variabile se molti worker |
| Nessun limite max worker | MEDIA | - | Aggiungere `--max-workers N` per evitare sovraccarico |

**CODICE ESEMPIO - Miglioramento trap:**
```bash
cleanup() {
    # Cleanup su errore (rimuovi PID files orfani)
    rm -f "${SWARM_DIR}/status/worker_*.pid" 2>/dev/null
}
trap cleanup ERR EXIT
```

---

### 2. anti-compact.sh (v1.6.0)

**PUNTI DI FORZA:**
- Template PROMPT_RIPRESA.md completo per nuova Cervella
- Integrazione VS Code Tasks per auto-spawn
- Git workflow solido (add -> commit -> push)

**PUNTI DI ATTENZIONE:**

| Issue | Severita | File:Line | Suggerimento |
|-------|----------|-----------|--------------|
| Nessun check `git push` fallito | MEDIA | L198-202 | Il warning c'e' ma non blocca - considerare retry |
| Heredoc nel PROMPT_RIPRESA | BASSA | L125-172 | Potenziale problema con caratteri speciali in CUSTOM_MESSAGE |
| `set -e` con git commands | MEDIA | L33 | Git status/diff possono avere exit code non-zero legittimi |

**SUGGERIMENTO CRITICO:**
```bash
# Riga 190 - Migliorare gestione git diff
if ! git diff --cached --quiet 2>/dev/null; then
    # Ci sono modifiche staged
    git commit -m "$COMMIT_MSG" || { log_error "Commit fallito!"; exit 1; }
fi
```

---

### 3. watcher-regina.sh (v1.0.0)

**PUNTI DI FORZA:**
- Usa fswatch (efficiente su macOS)
- Notifiche sia terminal-notifier che osascript (fallback)
- AppleScript per svegliare Regina (keystroke injection)

**PUNTI DI ATTENZIONE:**

| Issue | Severita | File:Line | Suggerimento |
|-------|----------|-----------|--------------|
| Keystroke injection potenziale | MEDIA | L77 | Sanitizzare `$task_name` prima di iniettarlo |
| Nessun timeout su fswatch | BASSA | L90 | Considerare `-o` per batch mode |
| Hardcoded "Code" come default | BASSA | L19 | Potrebbe non funzionare se Regina e' in Terminal |

**FIX SUGGERITO per keystroke injection:**
```bash
# Sanitizza task_name per prevenire injection
safe_task_name=$(echo "$task_name" | tr -cd '[:alnum:]_-')
```

---

### 4. task_manager.py (v1.1.0)

**PUNTI DI FORZA:**
- Validazione task_id robusta (path traversal prevention)
- Stato ACK multi-livello (R/U/D)
- Clean separation of concerns

**PUNTI DI ATTENZIONE:**

| Issue | Severita | File:Line | Suggerimento |
|-------|----------|-----------|--------------|
| Nessun locking su file marker | MEDIA | L171-220 | Race condition se due agenti prendono stesso task |
| Max 50 char task_id arbitrario | BASSA | L47 | Documentare il perche' del limite |
| Print statements invece di logging | BASSA | L182-183 | Usare logging module per produzione |

**FIX SUGGERITO per race condition:**
```python
import fcntl

def mark_working(task_id: str) -> bool:
    # ... validazione ...
    working_file = Path(TASKS_DIR) / f"{task_id}.working"
    try:
        fd = working_file.open('x')  # Exclusive create - fails if exists
        fd.close()
        return True
    except FileExistsError:
        print(f"Task {task_id} gia' in lavorazione da altro worker!")
        return False
```

---

### 5. Handoff System

**PUNTI DI FORZA:**
- Template TEMPLATE_RICHIESTA.md chiaro e completo
- Monitor con watch mode per Regina
- Sistema di archiviazione

**PUNTI DI ATTENZIONE:**

| Issue | Severita | Suggerimento |
|-------|----------|--------------|
| Nessuna priorita' sui handoff | BASSA | Aggiungere campo Priorita: ALTA/MEDIA/BASSA |
| Nessun TTL sui messaggi | BASSA | Auto-archiviare dopo 24h se non gestiti |
| Manca notifica push alla Regina | MEDIA | Integrare con watcher-regina per notifiche |

---

## MIGLIORAMENTI SUGGERITI (Prioritizzati)

### ALTA PRIORITA' (fare presto)

1. **Race condition su task_manager.py**
   - Problema: Due worker potrebbero prendere lo stesso task
   - Soluzione: Usare file locking con `open('x')` exclusive

2. **Sanitizzazione keystroke watcher-regina.sh**
   - Problema: Task name potrebbe contenere caratteri pericolosi
   - Soluzione: Sanitizzare prima di iniettare in AppleScript

### MEDIA PRIORITA' (prossime sessioni)

3. **Max workers limit in spawn-workers**
   - Valore suggerito: `--max-workers 5` come default
   - Previene sovraccarico sistema

4. **Retry su git push fallito in anti-compact**
   - 3 retry con backoff esponenziale
   - Critico per salvare lavoro!

5. **Integrazione handoff con watcher**
   - Quando worker crea handoff, Regina riceve notifica

### BASSA PRIORITA' (nice to have)

6. **Dashboard unificata**
   - Combinare monitor-status.sh + monitor-handoff.sh
   - Visualizzazione unica stato swarm

7. **Metriche e analytics**
   - Tempo medio completamento task per worker
   - Success rate per tipo di task

---

## AUTO-SVEGLIA: ANALISI APPROFONDITA

L'implementazione AUTO-SVEGLIA (v2.6.0 -> v2.7.0 default) e' **ECCELLENTE**:

```
FLUSSO:
spawn-workers --backend
       |
       v
Worker lavora (finestra separata)
       |
       v
Worker crea .done
       |
       v
fswatch rileva evento
       |
       v
AppleScript digita nella finestra Regina
       |
       v
REGINA SVEGLIATA!
```

**Punti di forza:**
- Default=true e' la scelta giusta (meno friction)
- Check anti-duplicati previene watcher multipli
- PID file per cleanup

**Possibili miglioramenti:**
- Aggiungere `--silent` per disabilitare notifiche audio
- Considerare webhook come alternativa a keystroke (piu' robusto)

---

## SECURITY CHECKLIST

| Check | Stato | Note |
|-------|-------|------|
| Config ownership validation | OK | validate_config_ownership() |
| Path traversal prevention | OK | validate_task_id() |
| Command injection | PARZIALE | Sanitizzare task_name in watcher |
| No secrets in code | OK | Usa env vars |
| File permissions | OK | Check world-writable |

---

## CONCLUSIONI

Il sistema CervellaSwarm e' **maturo e pronto per uso intensivo**. Le criticita' identificate sono minori e non bloccanti. I miglioramenti suggeriti sono evolutivi, non correttivi.

**Prossimi step consigliati:**
1. Fix race condition task_manager.py (1 ora)
2. Sanitizzazione watcher-regina.sh (30 min)
3. Documentare limiti e best practices (1 ora)

---

*Report generato da cervella-reviewer*
*5 Gennaio 2026 - Code Review Settimanale*
