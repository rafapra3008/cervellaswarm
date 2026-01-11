# Investigazione Cache Invalidation - Sessione 167

> **Data:** 11 Gennaio 2026
> **Investigatori:** Rafa & Regina
> **Status:** Parzialmente risolto - continuare in futuro

---

## SCOPERTE CHIAVE

### 1. Pattern nei Log Trovato!

Analizzando i log della sessione 166, abbiamo trovato:

```
DROP correlati a tool_result di Task:
- 75,557 → 33,425 (dopo Task)
- 96,514 → 50,748 (dopo Task)
- 134,444 → 19,723 (dopo Task)

Il valore ~19,723 è il "CORE" costante (system + CLAUDE.md + tools)
```

### 2. Cosa NON Funziona

| Metodo | Testato | Risultato |
|--------|---------|-----------|
| Modificare CLAUDE.md | ✅ | ❌ Non funziona |
| /model switch | ✅ | ❌ Non funziona |
| Task piccolo (ping) | ✅ | ❌ Non funziona |
| Task medio (lista file) | ✅ | ❌ Non funziona |

### 3. Dove Sta la Cache

```
CACHE PROMPT = LATO SERVER (Anthropic)
- Gestita interamente da Anthropic
- TTL 5 min deciso da loro
- Client manda richieste, server decide se usare cache

TRANSCRIPT = LOCALE (~/.claude/projects/*.jsonl)
- Solo storico conversazioni
- NON è la cache vera
```

### 4. Ipotesi Non Confermate

- Forse serve tool_result MOLTO grande (migliaia di token)?
- Forse c'è una soglia interna che non conosciamo?
- Forse è garbage collection periodica di Anthropic?

---

## METODI GARANTITI (Funzionano sempre)

1. **Timeout 5+ minuti** - Non scrivere, cache scade
2. **Restart CLI** - Chiudi e riapri Claude Code

---

## FILE UTILI

- `.sncp/idee/20260111_RICERCA_CACHE_TRIGGER_REALE.md` - Ricerca completa
- `.sncp/idee/DA_STUDIARE_CONTEXT_LIBERATION.md` - Scoperta originale
- `~/.claude/projects/-Users-rafapra-Developer-CervellaSwarm/969a3362*.jsonl` - Log sessione 166

---

## PROSSIMI PASSI (Futuro)

1. Monitorare quando succede naturalmente e annotare condizioni esatte
2. Testare con Task che produce output >50k tokens
3. Chiedere alla community Claude Code se qualcuno sa di più

---

*"Abbiamo imparato tanto anche senza risolvere tutto!"*
*Sessione 167 - Rafa & Regina*
