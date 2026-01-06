# Task: Creare Template Task Comuni

**Assegnato a:** cervella-backend
**Priorita:** ALTA
**Stato:** ready

---

## Obiettivo

Creare 4 template task pre-fatti per risparmiare tempo ogni giorno.

## Template da Creare

Crea in `~/.claude/scripts/templates/`:

### 1. TASK_TEMPLATE_RICERCA.md
```markdown
# Task: [TITOLO RICERCA]

**Assegnato a:** cervella-researcher
**Priorita:** [ALTA/MEDIA/BASSA]
**Stato:** ready

## Obiettivo
[Cosa deve essere ricercato]

## Domande Specifiche
1. [Domanda 1]
2. [Domanda 2]
3. [Domanda 3]

## Output Atteso
- Report in .swarm/tasks/[NOME]_output.md
- Fonti citate
- Raccomandazioni

## Deadline
[Se applicabile]
```

### 2. TASK_TEMPLATE_FIX_BUG.md
```markdown
# Task: Fix Bug - [DESCRIZIONE]

**Assegnato a:** cervella-backend / cervella-frontend
**Priorita:** [ALTA/MEDIA/BASSA]
**Stato:** ready

## Bug
[Descrizione del bug]

## Come Riprodurre
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Comportamento Atteso
[Cosa dovrebbe succedere]

## File Coinvolti
- [file1.py]
- [file2.py]

## Output Atteso
- Bug fixato
- Test che verifica il fix
```

### 3. TASK_TEMPLATE_FEATURE.md
```markdown
# Task: Feature - [NOME FEATURE]

**Assegnato a:** cervella-backend / cervella-frontend
**Priorita:** [ALTA/MEDIA/BASSA]
**Stato:** ready

## Feature
[Descrizione della feature]

## Requisiti
1. [Requisito 1]
2. [Requisito 2]

## Design (se applicabile)
[Mockup o descrizione UI]

## File da Modificare/Creare
- [file1]
- [file2]

## Output Atteso
- Feature funzionante
- Documentazione aggiornata (se serve)
```

### 4. TASK_TEMPLATE_REVIEW.md
```markdown
# Task: Code Review - [COSA REVIEWARE]

**Assegnato a:** cervella-reviewer / cervella-guardiana-qualita
**Priorita:** [ALTA/MEDIA/BASSA]
**Stato:** ready

## Scope Review
[Cosa deve essere reviewato]

## File da Revieware
- [file1]
- [file2]

## Focus Particolare
- [ ] Sicurezza
- [ ] Performance
- [ ] Leggibilita
- [ ] Test coverage

## Output Atteso
- Report con rating /10
- Lista problemi trovati
- Suggerimenti miglioramento
```

## Dopo Aver Creato i Template

1. Crea anche uno script `task-new` che:
   - Accetta tipo template (ricerca, bug, feature, review)
   - Copia il template in .swarm/tasks/
   - Apre l'editor per compilarlo

Esempio uso:
```bash
task-new ricerca "Studio API WhatsApp"
# Crea .swarm/tasks/TASK_STUDIO_API_WHATSAPP.md dal template
```

## Output

- 4 file template in ~/.claude/scripts/templates/
- Script task-new in ~/.claude/scripts/
- Documentazione uso in output

---

*"Risparmio 2 min/task = ORE risparmiate!"*
