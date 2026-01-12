# Nota: Errore "File Modified Since Read"

> Data: 12 Gennaio 2026
> Tipo: Problema tecnico ricorrente

---

## Il Problema

Quando edito un file, a volte appare:
```
Error: File has been modified since read
```

## Perche Succede

1. Sessioni parallele modificano lo stesso file
2. Linter/formatter modifica il file
3. Hook automatici
4. Altro processo

## Soluzione

**SEMPRE rileggere il file prima di editare:**

```
1. Read(file)
2. Edit(file, old_string, new_string)
```

Se errore:
```
1. Read(file) di nuovo
2. Trova la stringa corretta (potrebbe essere cambiata)
3. Edit(file, new_old_string, new_string)
```

## Regola

> "Se file modified error -> rileggi e riprova"

---

*Non e un bug, e normale con sessioni parallele.*
