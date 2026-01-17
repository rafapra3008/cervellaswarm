# ROADMAP - Casa Pulita per Clienti

> **Creato:** 17 Gennaio 2026 - Sessione 248
> **Fase 8 di Casa Pulita**

---

## OBIETTIVO

Portare i miglioramenti di Casa Pulita (interni) nel prodotto per i clienti.

---

## ANALISI COMPLETATA

### Cosa il CLI GIA FA (cervellaswarm init)

| Feature | Status |
|---------|--------|
| Struttura .sncp/ | OK |
| stato.md iniziale | OK |
| PROMPT_RIPRESA | OK |
| COSTITUZIONE.md | OK |
| project.json | OK |

### Cosa MANCA (da Casa Pulita)

| Feature | Valore Cliente | Priorità |
|---------|----------------|----------|
| Limiti file espliciti | Prevenzione bloat | P1 |
| Comando housekeeping | Manutenzione facile | P2 |
| Script auto-compact | Automazione | P3 |
| Best practices docs | Educazione | P1 |

---

## PIANO IMPLEMENTAZIONE

### P1: Aggiornare Templates (Quick Win)

**File da modificare:**
- `packages/cli/src/sncp/init.js`
- `packages/cli/src/templates/constitution.js`

**Cosa aggiungere:**

1. **PROMPT_RIPRESA template** - aggiungere commento limiti:
```markdown
<!-- LIMITI: Questo file deve restare < 150 righe -->
<!-- Se cresce troppo, archivia sessioni vecchie in .sncp/archivio/ -->
```

2. **stato.md template** - aggiungere commento limiti:
```markdown
<!-- LIMITI: Questo file deve restare < 500 righe -->
<!-- Se cresce troppo, usa: cervellaswarm housekeeping -->
```

3. **COSTITUZIONE.md** - aggiungere sezione "MANUTENZIONE":
```markdown
## MANUTENZIONE

> *"Casa pulita = mente pulita = lavoro pulito!"*

- PROMPT_RIPRESA: max 150 righe (archivia il vecchio)
- stato.md: max 500 righe (compatta periodicamente)
- reports/: archivia file > 30 giorni

Comando: `cervellaswarm housekeeping`
```

**Chi:** cervella-backend
**Effort:** Basso

---

### P2: Nuovo Comando `housekeeping`

**Cosa fa:**
```bash
cervellaswarm housekeeping

# Output:
# Checking .sncp/ health...
#
# PROMPT_RIPRESA: 45 righe [OK]
# stato.md: 320 righe [WARNING - considera compattazione]
# reports/: 12 file (3 > 30 giorni)
#
# Suggerimenti:
# - Compatta stato.md con --compact
# - Archivia report vecchi con --archive
```

**Opzioni:**
- `--compact` - compatta file grandi
- `--archive` - archivia file vecchi
- `--auto` - esegue tutto senza conferma

**File da creare:**
- `packages/cli/src/commands/housekeeping.js`

**Chi:** cervella-backend
**Effort:** Medio

---

### P3: Script Auto-Compact (Opzionale)

**Per utenti avanzati:**
- Script da aggiungere in `.sncp/scripts/`
- Integrazione con cron/launchd opzionale
- Documentazione in docs/

**Chi:** cervella-devops
**Effort:** Medio

---

### P1: Best Practices Docs

**File da creare/aggiornare:**
- `docs/guides/KEEPING_SNCP_CLEAN.md`

**Contenuto:**
```markdown
# Keeping Your .sncp/ Clean

## Why It Matters
- Smaller context = faster AI responses
- Clean history = easier debugging
- Less token usage = lower costs

## The Rules
1. PROMPT_RIPRESA: max 150 lines
2. stato.md: max 500 lines
3. Archive reports older than 30 days

## How To
- Run `cervellaswarm housekeeping` weekly
- Archive old sessions when starting fresh sprint
- Keep only CURRENT session in PROMPT_RIPRESA
```

**Chi:** cervella-docs
**Effort:** Basso

---

## PRIORITÀ ESECUZIONE

```
FASE 8.1: Templates + Docs (P1)
  -> Aggiornare init.js + constitution.js
  -> Creare KEEPING_SNCP_CLEAN.md
  -> VALORE IMMEDIATO per nuovi utenti

FASE 8.2: Comando housekeeping (P2)
  -> Nuovo comando CLI
  -> Health check + suggerimenti
  -> VALORE per utenti esistenti

FASE 8.3: Auto-compact script (P3)
  -> Per power users
  -> Opzionale, documentato
```

---

## METRICHE SUCCESS

| Metrica | Target |
|---------|--------|
| Nuovi utenti sanno limiti | 100% (nei template) |
| Comando housekeeping | Funzionante |
| Docs best practices | Pubblicate |

---

*"Quello che funziona per noi, funziona per i clienti!"*
