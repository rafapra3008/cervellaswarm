# Pattern Comunicazione - CervellaSwarm

> **Data:** 17 Gennaio 2026 - Sessione 247
> **Fase:** Casa Pulita - Fase 7

Questo documento formalizza i pattern di comunicazione che lo sciame GIA utilizza.

---

## Pattern 1: Maker-Checker

```
Worker (Maker)           Guardiana (Checker)
     |                         |
     | produce output          |
     +------------------------>|
                               | verifica qualita
                               | valida compliance
     |<------------------------+
     | feedback/approvazione   |
```

**Dove lo usiamo:**
- Worker Backend/Frontend -> Guardiana Qualita
- Worker qualsiasi -> Guardiana Ops (per deploy)
- Researcher -> Guardiana Ricerca

**Valore:** Nessun output importante passa senza verifica.

---

## Pattern 2: Artifact System

```
Agente esegue task
       |
       v
Scrive output in file persistente
       |
       v
File disponibile per altri agenti
```

**Dove lo usiamo:**
- `.sncp/progetti/{progetto}/reports/` - Output ricerche
- `.swarm/tasks/TASK_XXX_OUTPUT.md` - Output task
- `docs/decisioni/` - Decisioni tecniche

**Valore:** Output sopravvive alla sessione, riusabile.

---

## Pattern 3: Stigmergy

```
Agente A                    Agente B
    |                           |
    | modifica ambiente         |
    | (scrive file)             |
    +----------> FILE <---------+
                  |             |
                  |    legge file
                  |             |
    nessun dialogo diretto!     |
```

**Dove lo usiamo:**
- `docs/decisioni/` - Decisioni condivise
- `.sncp/stato/` - Stato globale
- `.sncp/progetti/*/stato.md` - Stato per progetto

**Valore:** Comunicazione asincrona, scalabile, audit naturale.

---

## Pattern 4: Hierarchical + Peer Hybrid

```
         REGINA
        /  |   \
       /   |    \
Guardiana Guardiana Guardiana
   |        |        |
Worker   Worker   Worker
```

**Come funziona:**
- Regina coordina TUTTI
- Guardiane comunicano TRA LORO per validazione
- Worker comunicano SOLO via file (stigmergy)

**Valore:** Gerarchia chiara + flessibilita peer tra Guardiane.

---

## Pattern 5: Memory Types (STM/MTM/LTM)

| Tipo | Scope | File | Retention |
|------|-------|------|-----------|
| **STM** (Short-term) | Sessione | `oggi.md` | 1 giorno |
| **MTM** (Medium-term) | Progetto | `stato.md` | Fino archivio |
| **LTM** (Long-term) | Globale | `COSTITUZIONE.md` | Permanente |

**Valore:** Informazioni giuste al momento giusto.

---

## Pattern 6: Deterministic Controls

```
SBAGLIATO:
  DNA dice "ricordati di non superare 150 righe"
  Agente puo' ignorare

CORRETTO:
  Hook pre-commit BLOCCA se > 150 righe
  Impossibile violare
```

**Dove lo usiamo:**
- `.git/hooks/pre-commit` - Limiti righe, naming
- `scripts/sncp/compliance-check.sh` - Verifica giornaliera

**Valore:** Regole ENFORCED, non solo suggerite.

---

## Checklist Nuovo Agente

Quando crei un nuovo agente, verifica:

- [ ] DNA include `_SHARED_DNA.md`
- [ ] Output include `COSTITUZIONE-APPLIED: SI/NO`
- [ ] Report scritti in `.sncp/progetti/{progetto}/reports/`
- [ ] Decisioni importanti in `docs/decisioni/`
- [ ] Segue pattern Maker-Checker (Guardiana valida)

---

*"I pattern documentati sono pattern rispettati."*

*Cervella & Rafa*
