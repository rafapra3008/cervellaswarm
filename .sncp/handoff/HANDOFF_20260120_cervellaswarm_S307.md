# HANDOFF - Sessione 307

**Data:** 20 Gennaio 2026
**Progetto:** CervellaSwarm
**Focus:** FIX CONTEXT USAGE

---

## ACCOMPLISHED

1. **Investigazione Context Usage**
   - Rafa ha notato context DOPPIO del normale
   - Lanciata analisi con Ingegnera + Researcher

2. **Causa Radice Trovata**
   - COSTITUZIONE caricata DUE VOLTE:
     - Via `@` in ~/.claude/CLAUDE.md (riga 11)
     - Via session_start_swarm.py hook
   - Risparmio potenziale: ~2,500 tokens

3. **Fix Applicato**
   - Rimossa `@` da CLAUDE.md
   - Hook resta unica fonte di COSTITUZIONE
   - Guardiana ha APPROVED il fix (9/10)

4. **Documentazione Creata**
   - Script misurazione token
   - Subroadmap context optimization
   - Report causa radice
   - Ricerca ottimizzazione context

---

## CURRENT STATE

```
FIX APPLICATO - DA VERIFICARE PROSSIMA SESSIONE

Baseline misurata: ~9,600 tokens
Target: ~8,000 tokens
Risparmio atteso: ~2,500 tokens (-26%)
```

**Plugin submission:** IN ATTESA - servono info da Rafa (GitHub repo, email, URL org)

---

## LESSONS LEARNED

1. **"@ in CLAUDE.md = auto-expansion"**
   - Il simbolo @ causa inclusione automatica del file
   - Se un hook già carica lo stesso file = DUPLICAZIONE

2. **"Investigare PRIMA di fixare"**
   - Rafa ha insistito su capire la CAUSA VERA
   - Senza questo, avremmo creato workaround inutili

3. **"File grandi in claudeMd = context permanente sprecato"**
   - Regola: MAI includere file > 500 righe in claudeMd
   - Usare riferimenti invece di inclusione

---

## NEXT STEPS

**Sessione 308 - Priorità:**
1. [ ] Verificare risparmio token (nuova sessione)
2. [ ] Submit plugin → clau.de/plugin-directory
3. [ ] Submit MCP → registry.modelcontextprotocol.io
4. [ ] Join MCP Discord
5. [ ] Stripe Live Mode

**Info mancanti per plugin:**
- GitHub Repo pubblico
- Email contatto
- URL organizzazione

---

## KEY FILES

| File | Descrizione |
|------|-------------|
| `~/.claude/CLAUDE.md` | Rimossa @ da riga 11 |
| `~/.claude/docs/COSTITUZIONE_TRIGGER.md` | Version minimal (20 righe) |
| `scripts/utils/measure_context_tokens.py` | Script misurazione |
| `.sncp/roadmaps/SUBROADMAP_CONTEXT_OPTIMIZATION.md` | Piano |
| `reports/CAUSA_RADICE_CONTEXT_DOPPIO.md` | Analisi |

---

## BLOCKERS

**Nessun blocker tecnico.**

**In attesa da Rafa:**
- Info per plugin submission (GitHub repo, email, URL)

---

*Cervella & Rafa - Sessione 307*
*"Analizza prima di giudicare!"*
