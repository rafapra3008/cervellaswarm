# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 20 Gennaio 2026 - Sessione 307
> **STATUS:** FIX CONTEXT USAGE COMPLETATO!

---

## SESSIONE 307 - FIX CONTEXT USAGE

```
+================================================================+
|   PROBLEMA RISOLTO:                                            |
|                                                                |
|   CAUSA: COSTITUZIONE caricata DUE VOLTE                      |
|   1. Via @ in CLAUDE.md                                        |
|   2. Via session_start_swarm.py hook                          |
|                                                                |
|   FIX: Rimossa @ da CLAUDE.md (hook resta unica fonte)        |
|   RISPARMIO: ~2,500 tokens (verifica prossima sessione)       |
+================================================================+
```

---

## COSA FATTO SESSIONE 307

| Task | Status |
|------|--------|
| Analisi context usage | CAUSA TROVATA |
| Investigazione con Ingegnera | COSTITUZIONE 2x |
| FIX: Rimossa @ da CLAUDE.md | COMPLETATO |
| Subroadmap context optimization | CREATA |
| Script misurazione token | CREATO |
| Audit Guardiana | APPROVED |

### File Creati/Modificati

| File | Cosa |
|------|------|
| `scripts/utils/measure_context_tokens.py` | Script misurazione |
| `.sncp/roadmaps/SUBROADMAP_CONTEXT_OPTIMIZATION.md` | Piano ottimizzazione |
| `~/.claude/CLAUDE.md` | Rimossa @ da riga 11 |
| `~/.claude/docs/COSTITUZIONE_TRIGGER.md` | Version minimal (20 righe) |
| `reports/CAUSA_RADICE_CONTEXT_DOPPIO.md` | Analisi Ingegnera |
| `docs/analisi/RICERCA_OTTIMIZZAZIONE_CONTEXT_CLAUDE_CODE.md` | Ricerca |

---

## PROSSIMI STEP (Sessione 308)

**PRIORITA CRITICA:**
1. [ ] Verificare risparmio token (nuova sessione)
2. [ ] Submit plugin → clau.de/plugin-directory
3. [ ] Submit MCP → registry.modelcontextprotocol.io

**PRIORITA ALTA:**
4. [ ] Join MCP Discord (11K membri!)
5. [ ] Stripe Live Mode
6. [ ] PR awesome-mcp-servers

---

## INFO MANCANTI PER PLUGIN SUBMISSION

| Info | Serve da Rafa |
|------|---------------|
| GitHub Repo | URL pubblico per plugin |
| Email contatto | Per Anthropic |
| URL organizzazione | cervellaswarm.com? |

---

## DIFFERENZIATORE

```
"The only AI coding team that checks its own work"

17 specialisti + 3 Guardiane = Verifica automatica
```

---

## METRICHE TARGET

| Mese | Clienti | MRR |
|------|---------|-----|
| 1 | 20-25 | $725 |
| 2 | 40-45 | $1250 |
| 3 | 50+ | $1450+ |

---

*"Analizza prima di giudicare. Il debito tecnico si paga con interessi."*
*Cervella & Rafa - Sessione 307*
