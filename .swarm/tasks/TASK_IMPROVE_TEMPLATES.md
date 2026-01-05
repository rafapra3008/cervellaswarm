# Task: Migliorare Template Task

**Assegnato a:** cervella-docs
**Stato:** ready
**Priorità:** BASSA

## Obiettivo

Migliorare i template in `.swarm/tasks/` per essere più completi e utili.

## File da Modificare

`/Users/rafapra/Developer/CervellaSwarm/.swarm/tasks/TEMPLATE_TASK.md`

## Nuovo Template Proposto

```markdown
# Task: [NOME_TASK]

**Assegnato a:** [cervella-backend|frontend|tester|docs|devops|...]
**Stato:** ready
**Priorità:** [ALTA|MEDIA|BASSA]
**Dipende da:** [opzionale - nome altro task]
**Stima:** [opzionale - es. "30 min", "2h"]

---

## Obiettivo

[Descrizione chiara di cosa deve essere fatto]

## Contesto

[Perché questo task è necessario, background]

## Specifiche

### Input
[Cosa riceve il worker - file da leggere, dati, etc.]

### Output Richiesto
[Cosa deve produrre - file da creare/modificare, formato]

### Vincoli
[Limitazioni, cose da NON fare, compatibilità]

## Criteri di Successo

- [ ] [Criterio 1 verificabile]
- [ ] [Criterio 2 verificabile]
- [ ] [Criterio 3 verificabile]

## Note

[Informazioni aggiuntive, link utili, riferimenti]

---
*Template v2.0 - CervellaSwarm*
```

## Anche Creare

1. `TEMPLATE_TASK_QUICK.md` - Versione breve per task semplici
2. `TEMPLATE_TASK_RESEARCH.md` - Per task di ricerca

## Output Richiesto

1. File: `.swarm/tasks/TEMPLATE_TASK.md` (aggiornato)
2. File: `.swarm/tasks/TEMPLATE_TASK_QUICK.md` (nuovo)
3. File: `.swarm/tasks/TEMPLATE_TASK_RESEARCH.md` (nuovo)

## Verifica

- [ ] Template principale più completo
- [ ] Template quick per task veloci
- [ ] Template research per ricerche
