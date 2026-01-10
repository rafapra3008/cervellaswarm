# Review: cervella-backend.md

**Reviewer:** cervella-guardiana-qualita
**Data:** 2026-01-10

---

## Score: 9/10

## Verdetto: APPROVE

---

## Top 3 Punti Positivi

1. **Struttura chiara e ben organizzata** - Il file segue un pattern logico: DNA di famiglia, regole operative, specializzazioni, zone di competenza, pattern di codice, protocolli di comunicazione. Facile da navigare e consultare.

2. **Regole decisionali esplicite** - La sezione "REGOLA DECISIONE AUTONOMA" con i tre livelli (procedere/chiedere/fermarsi) è eccellente. Riduce ambiguità e rende l'agente più efficiente.

3. **Esempi pratici e concreti** - Gli esempi di codice Python, workflow task, e output atteso sono molto utili. L'agente sa esattamente cosa produrre.

---

## Top 3 Aree di Miglioramento

1. **Zone di competenza troppo ampie** - "*.py (tutti i file Python)" è molto ampio. Potrebbe creare conflitti con tester o security. Suggerimento: specificare meglio le cartelle di competenza esclusiva.

2. **Manca sezione errori comuni** - Sarebbe utile una sezione "ERRORI DA EVITARE" con anti-pattern specifici backend (es: query N+1, secrets hardcoded, no rate limiting).

3. **Riferimento a file esterno non linkato** - Riga 228 menziona "DNA cervella-guardiana-qualita (sezione 483 righe)" ma non c'è un path chiaro. Potrebbe confondere.

---

## Note Tecniche

- Versione file: 1.0.0 (aggiornata 2026-01-02)
- Lunghezza: 301 righe - dimensione appropriata
- Compatibilità: cervellaswarm >= 1.0.0
- Tools dichiarati: Read, Edit, Bash, Glob, Grep, Write, WebSearch, WebFetch - completi per il ruolo
- Model: sonnet - appropriato per task operativi

---

*Reviewed by cervella-guardiana-qualita (Opus)*
