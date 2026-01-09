# BUG: cervella-researcher cerca tool non disponibili

**Data**: 9 Gennaio 2026
**Segnalato da**: Rafa durante ricerca Cursor

---

## Il Problema

```
Error: No such tool available: Bash
Read(.sncp)
Error: EISDIR: illegal operation on a directory, read
```

## Causa

`cervella-researcher` ha questi tool disponibili:
- Read, Glob, Grep, WebSearch, WebFetch

**NON ha**: Bash, Write, Edit

Ma nel suo comportamento:
1. Cerca di usare Bash (non disponibile)
2. Cerca di fare Read su directory invece che file

## Fix Necessario

### Opzione 1: Aggiungere Write a researcher
Se deve salvare output, serve Write. Ma questo va contro la filosofia "researcher = solo ricerca, non modifica".

### Opzione 2: Cambiare istruzioni DNA
Nel DNA di researcher, specificare chiaramente:
- "NON hai Bash - usa solo WebSearch, WebFetch, Read, Glob, Grep"
- "Read funziona SOLO su file, NON su directory"
- "Per salvare output, restituisci il contenuto e la Regina salverà"

### Opzione 3: Output diverso
Researcher restituisce il contenuto, Regina lo salva. Questo è più pulito.

---

## Decisione

**DA FARE**: Aggiornare DNA cervella-researcher con istruzioni più chiare sui tool disponibili e comportamento atteso.

**Priorità**: MEDIA (non blocca, ma crea confusione)

---

*Nota: La ricerca su Cursor è comunque completata con successo nonostante gli errori.*
