# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-03-06 - Sessione 432
> **STATUS:** S431 Migliora Casa + S432 Backlog Fix COMPLETATI. D5 LSP Avanzato PROSSIMO.

---

## SESSIONE 432 - Backlog Fix & Audit Finale

### Cosa e successo
Completamento pendenze S431 + fix di tutto il backlog P2/P3. Due audit Guardiana (9.3/10 + 9.6/10).

### Fix applicati S432
- **P2: bash_validator bypass $() e backtick** -- extract_subcommands + 18 nuovi test (76 totali)
- **P3: git_reminder state file crescita infinita** -- max 20 entries con prune automatico
- **P3: pre_compact_save `|` separator fragile** -- usa `%x00` null byte (sicuro)
- **P3: context-monitor PROJECT_MAPPING solo 3 progetti** -- universale (6 progetti)
- **P3: context-monitor 6x bare except** -- `except Exception:`
- **P3: hook_debug.log 33MB senza rotation** -- rotation 5MB + troncato a 2MB
- **P2: PROMPT_RIPRESA_MASTER data TL;DR stale** -- aggiornato 2026-03-06
- **P3: NORD.md "Febbraio" -> "Marzo 2026"**
- **P3: daily_memory_loader.py.backup residuo rimosso**
- **INFO: 32 report obsoleti eliminati** (Gen/Feb 2026)

### Fix S431 (committati insieme)
- P1: DB swarm_events CREATE TABLE + WAL mode
- P1: update_prompt_ripresa marker HTML univoci
- P1: memory_flush_auto duplicato rimosso
- P2: PROJECT_MAPPING universale (7 hook, 6 progetti)
- P2: post_commit_engineer async + timeout 55s
- BUG: db.py Python 3.9 compat (weekly_retro funziona)
- subagent_stop v2.0 su 3 repos

### Audit Guardiana
- MC7.4 audit S431: **9.3/10** APPROVED
- MC7 Bug Hunt audit: **9.6/10** APPROVED

---

## MAPPA SITUAZIONE

```
LINGUAGGIO CERVELLASWARM:
  FASE D: L'Ecosistema -- 4/6 DONE
    D1: Syntax Highlighting   [####################] DONE! (9.5/10)
    D2: LSP Base (lu lsp)     [####################] DONE! (9.5/10)
    D3: Playground Online      [####################] DONE! (LIVE!)
    D4: "A Tour of LU"        [####################] DONE! (9.5/10)
    D5: LSP Avanzato           [....................] PROSSIMO
    D6: Guardiana Finale       [....................] TODO

  Migliora Casa (S431)        [####################] COMPLETATA!
  Backlog Fix (S432)          [####################] COMPLETATA!
```

---

## PROSSIMA SESSIONE: D5 LSP Avanzato

- **Hover:** tipo + documentazione al passaggio mouse
- **Completion:** keyword, ruoli, trust tiers
- **Go-to-definition:** click su tipo -> definizione
- **Base LSP:** `packages/lingua-universale/src/cervellaswarm_lingua_universale/_lsp.py`
- **Subroadmap:** `.sncp/roadmaps/SUBROADMAP_FASE_D_ECOSISTEMA.md`
- **Metodo:** Researcher -> Piano -> Guardiana audit piano -> Implementa -> Guardiana audit

### TODO Rafa
- Attivare 2FA GitHub (SCADUTO 6 Marzo!)
- Ruotare Bedzzle key su MyReception

---

## I NUMERI TOTALI

| Metrica | Valore |
|---------|--------|
| Test agent-hooks | **253** (era 235) |
| Test totali LU | **2856** |
| Fix S431+S432 | **24** totali |
| Audit Guardiana | **4** (2 S431 + 2 S432) |

---

## Lezioni Apprese (S432)

### Cosa ha funzionato bene
- **Backlog sistematico** -- completare TUTTO il backlog in una sessione dedicata
- **Guardiana in background** -- audit corre mentre si lavora, zero tempo perso
- **hook_debug.log scoperto a 33MB** -- il rotation avrebbe dovuto esserci dal giorno 1

### Cosa non ha funzionato
- **Commit S431 mai fatto** -- la sessione precedente e finita senza commit (auto-compact)

### Pattern candidato
- **"Commit PRIMA di auto-compact"** -- se context > 70%, fare commit preventivo

---

*"Ultrapassar os proprios limites!" - Rafa & Cervella*
