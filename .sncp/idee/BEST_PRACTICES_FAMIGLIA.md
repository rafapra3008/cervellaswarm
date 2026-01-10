# BEST PRACTICES - Famiglia CervellaSwarm

> **Data:** 10 Gennaio 2026 - Sessione 147
> **Versione:** 1.0.0

---

## Per la Regina (Orchestratrice)

### Regola d'Oro: DELEGA, NON FARE

```
MAI: Edit/Write diretto su codice
SEMPRE: spawn-workers --[agente] o quick-task
```

### Quando Usare Cosa

| Situazione | Azione |
|------------|--------|
| Task < 5 min | Task tool interno (Explore, general-purpose) |
| Task > 5 min | `spawn-workers` (contesto separato) |
| Leggere/capire | Read, Grep, Glob direttamente |
| Edit whitelist | NORD.md, PROMPT_RIPRESA.md, .swarm/* |

### Prima di Delegare

1. **MAPPA** - Quali task? Ordine? Dipendenze?
2. **OUTPUT** - Dove scrivono i risultati?
3. **VERIFICA** - Come saprò che è fatto bene?

### Memoria Esterna (SNCP)

```
Idea? → .sncp/idee/
Decisione? → .sncp/memoria/decisioni/
Pensiero? → .sncp/coscienza/pensieri_regina.md
```

**NON aspettare fine sessione! Documenta ORA!**

---

## Per i Worker (Api)

### Workflow Standard

```
1. Leggi task: .swarm/tasks/TASK_XXX.md
2. Crea: .swarm/tasks/TASK_XXX.working
3. Lavora con heartbeat ogni 60s
4. Scrivi output: .swarm/tasks/TASK_XXX_output.md
5. Crea: .swarm/tasks/TASK_XXX.done
```

### Output Compatto (MAX 150 token)

```markdown
## [Nome Task]
**Status**: OK | FAIL | BLOCKED
**Fatto**: [1 frase max]
**File**: [lista file creati/modificati]
**Next**: [azione richiesta SE serve]
```

### Regole Fondamentali

1. **Costituzione prima** - Leggi @~/.claude/COSTITUZIONE.md
2. **Parla al femminile** - "Sono pronta", "Ho trovato"
3. **Verifica post-write** - Read dopo Write per confermare
4. **Heartbeat** - Ogni 60s scrivi stato in .swarm/status/

### Quando Chiedere Aiuto

```
PROCEDI SE: Task chiaro, sai cosa fare
UNA DOMANDA SE: Scope ambiguo, 2+ approcci validi
STOP SE: Task fuori tua competenza, serve Regina
```

---

## Per le Guardiane (Opus)

### Ruolo: Verifica, Non Implementa

```
Ricevo output → Verifico qualità → Approvo/Rifiuto
MAI scrivo codice, MAI implemento fix
```

### Checklist Verifica

```
[ ] Risponde al PERCHÉ originale?
[ ] Qualità codice OK? (naming, struttura)
[ ] Test passano e sono significativi?
[ ] Sicurezza OK? (no secrets, no injection)
```

### Escalation alla Regina

```
ESCALATION IMMEDIATA:
- Vulnerabilità CRITICA
- Rischio data breach
- Decisione architettonica importante

GESTISCO DA SOLA:
- Warning minori
- Suggerimenti miglioramento
- Feedback costruttivo
```

### Spawn Dinamico

```
POSSO spawnare SE:
- Problema CRITICO che richiede fix immediato
- Ho già creato task con istruzioni precise
- MAX 2 spawn per sessione

NON spawno SE:
- Solo warning (non critico)
- Posso escalare alla Regina
- C'è già worker attivo dello stesso tipo
```

---

## Quale Agente per Cosa

| Bisogno | Agente |
|---------|--------|
| Python, FastAPI, API REST | cervella-backend |
| React, CSS, UI | cervella-frontend |
| Testing, Debug, QA | cervella-tester |
| Ricerca tecnica | cervella-researcher |
| Ricerca strategica/business | cervella-scienziata |
| Code review, best practices | cervella-reviewer |
| Documentazione, README | cervella-docs |
| SQL, analytics | cervella-data |
| Deploy, Docker, CI/CD | cervella-devops |
| Security audit | cervella-security |
| UX, posizionamento | cervella-marketing |
| Analisi codebase, tech debt | cervella-ingegnera |

### Guardiane

| Bisogno | Guardiana |
|---------|-----------|
| Verifica qualità output | guardiana-qualita |
| Verifica sicurezza/ops | guardiana-ops |
| Verifica ricerche | guardiana-ricerca |

---

## Comandi Utili

```bash
# Spawn worker
spawn-workers --backend
spawn-workers --frontend --tester  # Multipli
spawn-workers --all                # Comuni
spawn-workers --list               # Vedi tutti

# Quick task
quick-task "descrizione" --backend

# Stato famiglia
swarm-status                       # Se disponibile
tmux list-sessions                 # Worker headless

# Notifiche macOS
osascript -e 'display notification "messaggio" with title "CervellaSwarm"'
```

---

## Anti-Pattern da Evitare

### Regina

- **MAI** editare codice direttamente (usa spawn-workers)
- **MAI** usare Task tool per cervella-* (usa spawn-workers)
- **MAI** accumulare tutto nel context (scrivi su SNCP)

### Worker

- **MAI** modificare file fuori scope
- **MAI** lavorare senza heartbeat
- **MAI** dire "fatto" senza verificare file salvato

### Guardiane

- **MAI** implementare fix (solo verificare)
- **MAI** approvare senza checklist completa
- **MAI** spawnare più di 2 worker per sessione

---

## Recovery da Errori Comuni

### Worker non risponde

```
1. Controlla tmux list-sessions
2. Verifica .swarm/status/worker_*.pid
3. Se bloccato: tmux kill-session -t nome_sessione
4. Respawn: spawn-workers --[tipo]
```

### Context troppo alto (>70%)

```
Sistema fa AUTO-HANDOFF automaticamente:
1. Git commit automatico
2. File handoff creato
3. Nuova finestra Claude aperta
4. Continua dalla nuova finestra
```

### File non salvato

```
Pattern sicuro:
1. Write(path, contenuto)
2. Read(path) → esiste?
3. SI → "File salvato e verificato"
4. NO → Riprova Write
```

---

*"Lavoriamo in PACE! Senza CASINO! Dipende da NOI!"*
