# Analisi Comunicazione Interna - CervellaSwarm

> **Data:** 17 Gennaio 2026 - Sessione 247
> **Fase:** Casa Pulita - Fase 7

---

## STATO ATTUALE

### Come Comunicano Oggi le Cervelle

```
                    REGINA (me)
                        |
            +-----------+-----------+
            |           |           |
        Guardiane    Worker      Worker
            |           |           |
            +-----+-----+-----+-----+
                  |           |
                SNCP        SNCP
              (files)      (files)
```

### Meccanismi Attuali

| Cosa | Come Funziona | Dove |
|------|---------------|------|
| **DNA Condiviso** | Istruzioni comuni | `_SHARED_DNA.md` |
| **DNA Specifico** | Specializzazioni | `cervella-*.md` |
| **COSTITUZIONE** | Chi siamo | `~/.claude/COSTITUZIONE.md` |
| **SNCP** | Memoria esterna | `.sncp/` |
| **Hook SessionStart** | Carica contesto | `session_start_swarm.py` |

---

## GAP IDENTIFICATI

### GAP 1: Nessuna Verifica Lettura

```
PROBLEMA:
Il DNA dice "leggi COSTITUZIONE prima di iniziare"
Ma NON c'e modo di VERIFICARE che l'agente lo faccia.

IMPATTO:
- Agenti potrebbero ignorare la COSTITUZIONE
- Regole non applicate consistentemente
```

### GAP 2: Nessun Tracking Decisioni

```
PROBLEMA:
Durante una sessione si prendono decisioni importanti.
Queste NON vengono registrate in modo strutturato.
La prossima sessione/agente non sa cosa e stato deciso.

IMPATTO:
- Decisioni perse
- Lavoro duplicato
- Inconsistenze
```

### GAP 3: Comunicazione Unidirezionale

```
PROBLEMA:
Regina -> Agente (ok)
Agente -> SNCP (ok)
Agente <-> Agente (NON ESISTE!)

IMPATTO:
- Agenti non si coordinano tra loro
- Lavoro duplicato o conflittuale
```

### GAP 4: Nessun Compliance Check

```
PROBLEMA:
Non c'e modo di verificare che l'output di un agente
segua le regole stabilite (formato, principi, etc).

IMPATTO:
- Output inconsistente
- Qualita variabile
```

---

## PROPOSTE SOLUZIONE

### Soluzione 1: Decision Log

```
COSA: File centrale per registrare decisioni
DOVE: .sncp/stato/decisioni_sessione.md
COME: Ogni agente DEVE registrare decisioni importanti
```

### Soluzione 2: Pre-Check Automatico

```
COSA: Aggiungere al DNA una sezione OBBLIGATORIA
DOVE: _SHARED_DNA.md
COME: Output deve includere "COSTITUZIONE-APPLIED: SI/NO"
```

### Soluzione 3: Shared Context File

```
COSA: File che si aggiorna durante la sessione
DOVE: .sncp/stato/context_sessione_YYYYMMDD.md
COME: Ogni agente legge E aggiorna prima/dopo task
```

### Soluzione 4: Guardiana Compliance

```
COSA: Guardiana che verifica compliance regole
QUANDO: Dopo output significativi
COME: Check automatico formato + principi
```

---

## PRIORITA IMPLEMENTAZIONE

```
1. [QUICK WIN] Decision Log - File semplice, grande impatto
2. [QUICK WIN] Pre-check nel DNA - gia parzialmente presente
3. [MEDIO] Shared Context - richiede pattern nuovo
4. [FUTURO] Guardiana Compliance - da studiare
```

---

*"La comunicazione chiara e la base del lavoro di squadra."*
