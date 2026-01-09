# BUG: cervella-researcher non ha Write/Bash

**Data:** 9 Gennaio 2026
**Sessione:** 137

## Problema

`cervella-researcher` ha solo questi tool:
- Read, Glob, Grep, WebSearch, WebFetch

**Manca:** Write, Bash, Edit

## Impatto

- Non può salvare output direttamente
- Regina deve salvare manualmente
- Workaround funziona ma non elegante

## Fix Proposto

Aggiungere Write a cervella-researcher in `~/.claude/agents/cervella-researcher.md`

## Priorità

BASSA - workaround funziona (Regina salva)

---

*Da fixare quando facciamo manutenzione DNA*
