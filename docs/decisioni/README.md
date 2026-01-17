# Decisioni - CervellaSwarm

> **Pattern: Stigmergy** - Comunicazione indiretta via documenti condivisi

---

## Come Funziona

```
Worker prende decisione
       ↓
Scrive in docs/decisioni/
       ↓
Altri agenti LEGGONO prima di agire
       ↓
Guardiana valida
       ↓
Decisione PROPAGATA a tutto lo sciame
```

---

## Regole

1. **OGNI decisione tecnica importante** va documentata qui
2. **PRIMA di implementare**, controlla se esiste già una decisione
3. **Usa il TEMPLATE.md** per nuove decisioni
4. **Naming:** `YYYYMMDD_NOME_DECISIONE.md`

---

## File in Questa Cartella

| File | Contenuto |
|------|-----------|
| `DECISIONI_TECNICHE.md` | Decisioni tecniche attive (principale) |
| `TEMPLATE.md` | Template per nuove decisioni |
| `YYYYMMDD_*.md` | Decisioni singole dettagliate |

---

## Quando Documentare

- Scelta tra 2+ opzioni tecniche
- Cambio di architettura
- Nuova convenzione/pattern
- Decisione che impatta altri agenti

---

## Quando NON Serve

- Bug fix semplici
- Refactoring minore
- Aggiunta commenti/docs

---

*"La memoria condivisa e' la forza dello sciame."*
