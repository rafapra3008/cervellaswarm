# SUBROADMAP - Pre-Launch Fix

> **Sessione 262** - 18 Gennaio 2026
> **Obiettivo:** Score 9.5/10 per Show HN
> **Score attuale:** 6/10

---

## ANALISI GUARDIANE

| Guardiana | Verdetto | Note |
|-----------|----------|------|
| Qualita | 6/10 | 4 problemi CRITICI |
| Researcher | Comandi sbagliati = FATALE | HN testa subito |

---

## FIX ORDINATI PER PRIORITA

### CRITICI (Bloccano lancio)

| # | File | Problema | Fix |
|---|------|----------|-----|
| 1 | `packages/cli/package.json` | homepage: cervellaswarm.dev | cervellaswarm.com |
| 1 | `packages/cli/package.json` | repo: cervellaswarm/cli | rafapra3008/CervellaSwarm |
| 2 | `packages/mcp-server/package.json` | repo: rafapra/ | rafapra3008/ |
| 3 | `packages/cli/bin/cervellaswarm.js` | help link .dev | .com |
| 4 | `docs/SHOW_HN_POST_READY.md` | comandi sbagliati | comandi corretti |

### IMPORTANTI (Prima del lancio)

| # | File | Problema | Fix |
|---|------|----------|-----|
| 5 | `README.md` | PHASE 2: 80% | PHASE 2: 100% |

### POST-FIX

| # | Azione |
|---|--------|
| 6 | npm publish --patch CLI |
| 7 | npm publish --patch MCP |
| 8 | Test su macchina pulita |

---

## COMANDI CORRETTI (riferimento)

```bash
# CORRETTO (quello che mettiamo)
npx cervellaswarm init
npx cervellaswarm task "add login page"

# SBAGLIATO (da rimuovere)
npx @cervellaswarm/cli init
npx @cervellaswarm/cli spawn --frontend
```

---

## CHECKLIST COMPLETAMENTO

- [x] FIX 1: CLI package.json
- [x] FIX 2: MCP package.json
- [x] FIX 3: CLI help link
- [x] FIX 4: Show HN comandi
- [x] FIX 5: README status
- [x] npm publish CLI (0.1.2)
- [x] npm publish MCP (0.2.3)
- [x] Test finale
- [x] FIX 6: MIT -> Apache-2.0 nel post
- [x] FIX 7: Checklist aggiornata

---

**SCORE FINALE: 9.5/10**

*Completato Sessione 262 - 18 Gennaio 2026*
*"Fatto BENE > Fatto VELOCE"*
