# Output: TASK_RICERCA_STORIA_FINESTRE

## Risultato
✅ RICERCA COMPLETATA

## Success Criteria Verificati
- [x] Trovati almeno 3 tentativi documentati → **TROVATI 6 TENTATIVI**
- [x] Capito PERCHÉ non hanno funzionato → **LIMITAZIONE ARCHITETTURALE**
- [x] Identificato pattern comune → **TUTTI RISOLVONO SOTTO-PROBLEMI, NON IL ROOT**
- [x] Proposto direzione diversa → **4 DIREZIONI PROPOSTE**

## Tentativi Trovati

| # | Sessione | Tentativo | Risultato |
|---|----------|-----------|-----------|
| 1 | 60 | Studio Multi-Finestra | ❌ Non risolve chi apre |
| 2 | 64-69 | spawn-workers.sh | ⚠️ Script funziona, ma serve trigger |
| 3 | 86-87 | AUTO-HANDOFF | ❌ Risolve altro problema |
| 4 | 93 | REGOLA 13 Riscritta | ⚠️ Solo documentazione |
| 5 | 95-96 | AUTO-SVEGLIA | ⚠️ Risolve sotto-problema notifiche |
| 6 | 101-104 | Fix Sveglia Regina | ⚠️ Fix di fix |

## Insight Chiave

**PROBLEMA ROOT:** Claude Code NON PUÒ aprire nuove finestre Terminal in modo completamente autonomo.

- È REATTIVO, non PROATTIVO
- Non ha background thread
- MCP non supporta push notifications

**TUTTI i tentativi hanno risolto SOTTO-PROBLEMI ma non il ROOT.**

## Direzioni Future Proposte

1. **Daemon Esterno** - Processo che monitora e spawna
2. **Hook Claude Code** - Post-tool triggers
3. **Automator/Shortcuts macOS** - Nativo macOS
4. **Feature Request Anthropic** - Supporto nativo

## File Creato

`docs/studio/STUDIO_STORIA_PROBLEMA_FINESTRE.md` - Report completo con:
- Timeline tutti i tentativi
- Pattern comune fallimenti
- Perché è difficile (architetturale)
- Workaround attuale
- Direzioni future
- Raccomandazioni

## Raccomandazione

**Per ora:** Accettare workaround "Rafa come Dispatcher" - funziona bene!

**Per futuro:** Considerare daemon esterno SE il workflow diventa tedioso.

---

**Ricerca completata!** 🔬

cervella-researcher - 7 Gennaio 2026
