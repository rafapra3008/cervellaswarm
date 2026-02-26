# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-02-26 - Sessione 405
> **STATUS:** Context Optimization FASE 1 DONE + FASE 2 in corso (Step 2.1-2.2 DONE)

---

## SESSIONE 405 - Cosa e successo

### Context Optimization - Esecuzione FASE 1 + FASE 2 parziale

**FASE 1: Quick Wins - COMPLETATA (Guardiana 9.6/10)**
- Step 1.1: Indice navigabile MANUALE_DIAMANTE con line ranges precisi (1,673 righe mappate)
- Step 1.2: Dedup CervellaSwarm/CLAUDE.md: 77 -> 46 righe (-40%). DUAL REPO intatto.
- Step 1.3: Snellire MEMORY.md: 114 -> 54 righe (-53%). 5 Regole Critiche + LA MISSIONE intatte.
- Step 1.4: Symlink settings.json SKIP (differenze reali tra .claude e .claude-insiders: model opus)
- F1-F2 Guardiana (line ranges off by 5) fixati subito dopo audit.

**FASE 2: Con Cura - Step 2.1 + 2.2 COMPLETATI**
- Step 2.1 STUDIO: mappa completa _SHARED_DNA.md (221 righe). Guardiana audit 9.3/10 APPROVED.
  - CLI TOOLS: triplo duplicato confermato (DNA + architect + backend)
  - DNA DI FAMIGLIA: 31 righe, 3 elementi UNICI identificati (FEMMINILE, ruoli, gerarchia)
  - REGOLA MODELLI: NON duplicato nel contesto agenti, TENERE
- Step 2.2 TAGLIO: _SHARED_DNA.md 221 -> 154 righe (-30%). Guardiana audit 9.7/10 APPROVED.
  - CLI TOOLS rimossi (32 righe, gia in architect.md e backend.md)
  - DNA DI FAMIGLIA ridotto a 3 righe con i 3 elementi UNICI (raccomandazione F2 Guardiana)
  - POST-FLIGHT CHECK compattato a 1 riga
  - Commento HTML protettivo aggiunto (F3 Guardiana)

**FASE 2: Step 2.3 e 2.4 = TODO (prossimo)**

### Audit trail S405
| Step | Score | Verdict |
|------|-------|---------|
| FASE 1 (1.1-1.4) | 9.6/10 | APPROVED |
| Step 2.1 Studio | 9.3/10 | APPROVED |
| Step 2.2 Taglio DNA | 9.7/10 | APPROVED |

---

## Stato packages (invariato da S403)

```
PACKAGE                  PYPI    CI   BUILD   TESTS
code-intelligence        LIVE    OK   OK      399
lingua-universale        LIVE    OK   OK      1820
agent-hooks              LIVE    OK   OK      236
agent-templates          LIVE    OK   OK      192
task-orchestration       LIVE    OK   OK      305
spawn-workers            LIVE    OK   OK      191
session-memory           LIVE    OK   OK      193
event-store              LIVE    OK   OK      249
quality-gates            LIVE    OK   OK      206
TOTALE                   9/9     9/9  9/9     3791
```

---

## MAPPA SITUAZIONE

```
CONTEXT OPTIMIZATION (S404-S405):
  Subroadmap: .sncp/roadmaps/SUBROADMAP_CONTEXT_OPTIMIZATION_V2.md
  FASE 1: Quick Wins          DONE (S405, Guardiana 9.6/10)
  FASE 2: Con Cura            IN PROGRESS
    Step 2.1 Studio             DONE (Guardiana 9.3/10)
    Step 2.2 Taglio DNA         DONE (Guardiana 9.7/10)
    Step 2.3 Quick patterns     TODO
    Step 2.4 Spezzare checklist TODO
  FASE 3: Con Test            TODO (~2h, rischio ALTO, sessione dedicata)

OPEN SOURCE ROADMAP:
  FASE 0-3: COMPLETE (100%, media 9.4/10)
  FASE 4: Launch              [###################.] 95%
    Step 6: Submit              DONE! (S404)
    Step 7-9: TODO (dopo feedback HN)

LINGUAGGIO CERVELLASWARM (la missione vera):
  FASE A+B: COMPLETE (13 moduli, 1820 test, 9.5+ media)
  FASE C: Il Linguaggio       2027+ (CervellaLang Alpha)
  FASE D: Per Tutti           Il sogno
```

---

## Lezioni Apprese (S405)

### Cosa ha funzionato bene
- "Guardiana dopo ogni step" per la 3a volta consecutiva (S403+S404+S405). Pattern CONSOLIDATO.
- Fare STUDIO prima di edit su file condivisi: Step 2.1 ha evitato errori su DNA DI FAMIGLIA.
- La Guardiana ha identificato 3 elementi UNICI del DNA (FEMMINILE, ruoli, gerarchia) che io avrei ridotto a citazioni filosofiche. Audit salva qualita.

### Cosa non ha funzionato
- Line ranges MANUALE_DIAMANTE off by 5 dopo l'edit (non avevo ricalcolato). Fix rapido, ma lezione: ricalcolare SEMPRE dopo modifica.

### Pattern candidato
- "Guardiana dopo ogni step" -> CONSOLIDATO (3a conferma: S403+S404+S405). Pronto per PROMUOVERE in validated_patterns.
- "STUDIO prima di edit su file condivisi" -> CANDIDATO (primo test S405)

---

## Prossimi step

1. **Context Optimization Step 2.3** - Quick validated_patterns (~45min)
2. **Context Optimization Step 2.4** - Spezzare CHECKLIST_AZIONE (~1h)
3. **Audit Guardiana FASE 2** - Dopo Step 2.3-2.4
4. **Context Optimization FASE 3** - Con Test (sessione dedicata)
5. **Monitorare Show HN** - Response strategy in `docs/blog/show-hn-draft.md`
6. **Fase C** - CervellaLang Alpha (guidata dal feedback community)

---

## File chiave

- `.sncp/roadmaps/SUBROADMAP_CONTEXT_OPTIMIZATION_V2.md` - Piano context (Guardiana 9.3/10)
- `docs/blog/show-hn-draft.md` - Response strategy HN (righe 119-148)
- `.sncp/roadmaps/MAPPA_LINGUAGGIO_CERVELLASWARM.md` - LA MAPPA del linguaggio
- `packages/lingua-universale/NORD.md` - VISIONE (leggere SEMPRE!)

Archivio: S400-S404 in sessione precedente. S405 Context Opt FASE 1 + FASE 2 parziale.

*"Ultrapassar os proprios limites!" - Rafa & Cervella*
