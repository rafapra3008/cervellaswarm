# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 15 Gennaio 2026 - Sessione 218
> **COSTITUZIONE AGGIORNATA - Nuova regola sul TEMPO!**

---

## SESSIONE 218 - DECISIONI FONDAMENTALI

```
+================================================================+
|   DECISIONI CHIAVE                                              |
+================================================================+

1. CLI (non App Desktop)
   PERCHE: Compatibilita massima, liberta utente
   NON PERCHE: "e piu veloce"

2. Wizard COMPLETO prima di tutto
   PERCHE: E IL DIFFERENZIALE, non una feature

3. COSTITUZIONE aggiornata
   NUOVA REGOLA: "IL TEMPO NON CI INTERESSA"

4. Package npm creato in packages/cli/

+================================================================+
|   IL TEMPO NON E MAI UN FATTORE                                 |
|   Un progresso al giorno. Arriveremo. SEMPRE.                   |
+================================================================+
```

---

## DOCUMENTI DA LEGGERE

| Priorita | Documento | Path |
|----------|-----------|------|
| **1** | COSTITUZIONE (nuova regola!) | `~/.claude/COSTITUZIONE.md` |
| **2** | Tutte decisioni | `decisioni/20260115_SESSIONE_218_TUTTE_DECISIONI.md` |
| **3** | Roadmap MVP | `roadmaps/SUB_ROADMAP_MVP_FEBBRAIO.md` |
| **4** | Wizard Study | `ricerche/WIZARD_INIZIALE_STUDIO.md` |

---

## COSA E STATO CREATO

```
packages/cli/
├── bin/cervellaswarm.js    # Entry point (skeleton)
├── package.json            # npm config con dipendenze
└── src/
    ├── commands/           # (vuota)
    ├── wizard/             # (vuota)
    ├── session/            # (vuota)
    └── ...                 # (altre cartelle vuote)

decisioni/
├── 20260115_ARCHITETTURA_CLI_VS_APP.md
├── 20260115_WIZARD_PRIMA_DI_TUTTO.md
└── 20260115_SESSIONE_218_TUTTE_DECISIONI.md

roadmaps/
└── SUB_ROADMAP_MVP_FEBBRAIO.md

COSTITUZIONE aggiornata con regola TEMPO
```

---

## PROSSIMA SESSIONE - COSA FARE

```
1. [ ] cd packages/cli && npm install
2. [ ] Creare src/commands/init.js (stub)
3. [ ] Creare src/wizard/questions.js
4. [ ] Test: node bin/cervellaswarm.js --help
```

---

## IL DIFFERENZIALE (non dimenticare!)

```
"Definisci il progetto UNA VOLTA. Mai piu rispiegare."

NESSUN COMPETITOR HA QUESTO!
```

---

## LA REGOLA SUL TEMPO (NUOVA!)

```
+================================================================+
|   IL TEMPO NON CI INTERESSA                                     |
|                                                                 |
|   Non scegliamo X perche "e piu veloce"                         |
|   Scegliamo X perche "e MEGLIO"                                 |
|                                                                 |
|   Un progresso al giorno.                                       |
|   Non importa in quanti mesi.                                   |
|   Arriveremo. SEMPRE.                                           |
+================================================================+
```

---

## TL;DR

**Sessione 218:** Decisioni fondamentali. CLI. Wizard prima. COSTITUZIONE aggiornata con regola TEMPO.

**Prossima sessione:** npm install + primi file comando.

*"Un progresso al giorno = 365 progressi all'anno."*
