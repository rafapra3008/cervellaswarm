# SESSIONE 218 - TUTTE LE DECISIONI

**Data:** 15 Gennaio 2026
**Durata:** ~60 minuti
**Partecipanti:** Rafa + Regina

---

## SOMMARIO ESECUTIVO

```
+================================================================+
|   SESSIONE 218: DECISIONI FONDAMENTALI PRESE                   |
+================================================================+

1. CLI (non App Desktop)
2. Wizard COMPLETO prima di tutto
3. 8 settimane implementazione wizard
4. Package npm come contenitore
5. SNCP come memoria

TUTTO documentato. NULLA dimenticato.
```

---

## DECISIONE 1: CLI vs App Desktop

**File:** `20260115_ARCHITETTURA_CLI_VS_APP.md`

**Scelta:** CLI

**Perché:**
- Risorse: siamo in 2, non 100+ come Cursor
- Tempo: 2-3 mesi vs 10-18 mesi
- Compatibilità: funziona con QUALSIASI IDE
- Differenziale: è il TEAM AI, non l'interfaccia

**Implicazioni:**
- `npm install -g cervellaswarm`
- Comandi: init, task, status, resume
- Nessun fork VS Code
- Extension VS Code possibile come v2.0 (futuro)

---

## DECISIONE 2: Wizard PRIMA di tutto

**File:** `20260115_WIZARD_PRIMA_DI_TUTTO.md`

**Scelta:** Wizard completo (8 settimane) PRIMA di task execution

**Perché:**
- Wizard È il differenziale
- "Definisci progetto UNA VOLTA, mai più rispiegare"
- Prima impressione conta
- Ricerca già fatta (WIZARD STUDY 1526 righe)

**Implicazioni:**
- Settimane 1-2: Foundation + domande wizard
- Settimane 3-4: Session management
- Settimane 5-6: Re-engagement + commands
- Settimane 7-8: Polish + test
- Task execution DOPO wizard perfetto

---

## DECISIONE 3: Timeline

**File:** `SUB_ROADMAP_MVP_FEBBRAIO.md`

**Scelta:** Target 10 Febbraio 2026 (con split 60/40)

**Dettaglio:**
- 60% tempo su Miracollo
- 40% tempo su CervellaSwarm
- Ogni giorno un po'
- Weekend = riposo

**Implicazioni:**
- 4 settimane calendario = ~8 settimane effettive (40%)
- Target realistico: Fine Marzo 2026 per wizard completo
- OK se serve più tempo - qualità > velocità

---

## DECISIONE 4: Struttura Package

**Creato:** `packages/cli/`

**Struttura:**
```
packages/cli/
├── bin/cervellaswarm.js    # Entry point
├── package.json            # npm config
└── src/
    ├── commands/           # init, task, status, resume
    ├── wizard/             # 10 domande
    ├── session/            # Session management
    ├── agents/             # Integrazione agenti
    ├── display/            # Output, progress
    ├── sncp/               # Lettura/scrittura SNCP
    ├── utils/              # Utilities
    └── templates/          # Handlebars templates
```

---

## DECISIONE 5: Stack Tecnologico CLI

**Scelta:**
- Node.js (ESM modules)
- Commander.js (CLI framework)
- @inquirer/prompts (wizard interattivo)
- Chalk (colori)
- Ora (spinner)
- Handlebars (templates)
- Conf (configurazione)

**Perché:**
- Standard industria per CLI tools
- Usato da eslint, webpack, yarn, etc.
- Documentazione eccellente
- Facile da mantenere

---

## DOCUMENTI CREATI OGGI

| Documento | Path | Contenuto |
|-----------|------|-----------|
| Roadmap MVP | `roadmaps/SUB_ROADMAP_MVP_FEBBRAIO.md` | Piano 4 settimane |
| Decisione CLI | `decisioni/20260115_ARCHITETTURA_CLI_VS_APP.md` | CLI vs App |
| Decisione Wizard | `decisioni/20260115_WIZARD_PRIMA_DI_TUTTO.md` | Wizard prima |
| Questo file | `decisioni/20260115_SESSIONE_218_TUTTE_DECISIONI.md` | Sommario |

---

## CODICE CREATO OGGI

| File | Path | Stato |
|------|------|-------|
| package.json | `packages/cli/package.json` | Creato |
| Entry point | `packages/cli/bin/cervellaswarm.js` | Creato (skeleton) |
| Cartelle src/ | `packages/cli/src/*` | Create (vuote) |

---

## PROSSIMI PASSI (Sessione 219+)

```
1. [ ] Installare dipendenze npm
2. [ ] Creare src/commands/init.js (stub)
3. [ ] Creare src/commands/status.js (stub)
4. [ ] Creare src/wizard/questions.js
5. [ ] Implementare le 10 domande wizard
6. [ ] Generare COSTITUZIONE.md da wizard
7. [ ] Test su cartella vuota
8. [ ] Test su CervellaSwarm stesso
```

---

## CITAZIONI CHIAVE SESSIONE

> **Rafa:** "Il wizard NON è una feature. È IL PRODOTTO."

> **Rafa:** "Non importa il TEMPO per fare.. noi abbiamo TEMPO..
>           ogni giorno un po', fino che siamo al 100000%"

> **Rafa:** "Ultrapassar os próprios limites!"

> **Regina:** "Il differenziale non è l'interfaccia. È il TEAM AI con memoria."

---

## STATO FINE SESSIONE

```
FASE 1: FONDAMENTA     [####################] 100%
FASE 2: MVP PRODOTTO   [#...................] 5%
  - Package skeleton creato
  - Decisioni documentate
  - Roadmap definita

PROSSIMO: Implementare wizard questions
```

---

*Sessione 218 completata. Tutto documentato. Nulla dimenticato.*

*"Lavoriamo in pace! Senza casino! Dipende da noi!"*
