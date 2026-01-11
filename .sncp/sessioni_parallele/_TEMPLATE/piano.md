# Piano Sessione Parallela: [NOME]

> **Data:** [DATA]
> **Progetto:** [PROGETTO]
> **Workers:** [LISTA]

---

## Obiettivo

[Cosa vogliamo ottenere con questa sessione parallela]

---

## Task Definiti

### TASK-001: [Nome]
- **Worker:** cervella-[nome]
- **Area:** [file/cartelle da modificare]
- **Dipende da:** nessuno
- **Descrizione:** [cosa deve fare]

### TASK-002: [Nome]
- **Worker:** cervella-[nome]
- **Area:** [file/cartelle da modificare]
- **Dipende da:** TASK-001 (o nessuno se indipendente)
- **Descrizione:** [cosa deve fare]

---

## Aree File (Nessuna Sovrapposizione!)

| Worker | Può Modificare | NON Toccare |
|--------|----------------|-------------|
| backend | backend/, api/ | frontend/ |
| frontend | frontend/, css/ | backend/ |

---

## Migrations

Chi crea migrations: [WORKER_NAME]
Range riservato: [036-039]

---

## Rischi Identificati

- [Rischio 1 e come mitigare]
- [Rischio 2 e come mitigare]

---

*Piano creato da Regina - [TIMESTAMP]*
