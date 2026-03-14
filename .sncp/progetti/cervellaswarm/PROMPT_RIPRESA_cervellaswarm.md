# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-03-14 - Sessione 460
> **STATUS:** 2/5 progetti showcase LIVE. SNCP health 6.5→9.5/10. PostCompact hook attivo.

---

## DOVE SIAMO -- IL QUADRO COMPLETO

### La storia recente (S455-S460)

**S455-S456 (svolta strategica):** Rafa ha fermato tutto. 7 report indipendenti. Verita: 455 sessioni, 3684 test, ZERO utenti. Decisione: 5 progetti showcase PRIMA di lanciare.

**S458-S459:** LU Debugger LIVE (Fly.io) + Tour of LU LIVE (playground). 2/5 showcase pronti.

**S460 (oggi):** Sessione dedicata a auto-compact e SNCP health.
- Ricerca approfondita auto-compact (come funziona, `/compact` manual vs auto, hooks)
- PostCompact hook creato (salva compact_summary in markdown)
- COMPACT INSTRUCTIONS in CLAUDE.md ampliato (6 PRESERVE + 6 SAFE TO DROP)
- SNCP health: limite 150→250 allineato in 25+ file, stato.md rimosso ovunque
- README SNCP riscritto, NORD.md snellito (282→152), health-check.sh fixato
- 2 script zombie disabilitati, pre-commit allineato (staged-only logic)
- Guardiana QA 9.5/10, Guardiana Ops 8.6/10, TUTTI i finding fixati (17 fix totali)
- 33 file committati, +1203/-656 righe

---

## COSA E LIVE

### 1. LU Debugger -- https://lu-debugger.fly.dev/
3 agenti AI su protocollo verificato. Demo + Live (Claude API). "Break" = violazione BLOCCATA.
- Stack: FastAPI + SSE + Monaco + Fly.io (Frankfurt)

### 2. Tour of LU -- https://rafapra3008.github.io/cervellaswarm/?tour
24 step interattivi, 4 capitoli, 4 esercizi. Completion tracking + celebration.

---

## MAPPA SITUAZIONE

```
LINGUA UNIVERSALE:
  31 moduli | 3684 test | PyPI v0.3.3 | VS Code v0.2.0
  Playground: rafapra3008.github.io/cervellaswarm/
  Tour: playground/?tour | Debugger: lu-debugger.fly.dev/

5 PROGETTI SHOWCASE:
  1. LU Debugger      DONE! LIVE (S458)
  2. Tour of LU       DONE! LIVE (S459)
  3. Incident Replay  <- PROSSIMO (1 sessione, pagina statica)
  4. Protocol Zoo     (2-3 sessioni)
  5. AI Code Review   (3-4 sessioni)

LANCIO:
  Show HN v2: READY (docs/SHOW_HN_V2_DRAFT.md)
  Blog: READY, Guardiana 9.8/10
  Public repo: SYNCED
  Discord: DA CREARE (Rafa)
```

---

## PROSSIMI STEP (ordine suggerito)

### Opzione A: Incident Replay (Progetto 3)
"Un bug AI e costato $34K. Ecco come LU lo avrebbe fermato."
Pagina statica, 1 sessione. Dettagli: `.sncp/roadmaps/MAPPA_5_PROGETTI_LU.md`

### Opzione B: Show HN v2 (lancio con 2 progetti)
Abbiamo gia Debugger + Tour + Playground + Blog + Colab.
Draft: `docs/SHOW_HN_V2_DRAFT.md` | Playbook: `docs/HN_RESPONSE_PLAYBOOK.md`

### Da Rafa (CEO)
- [ ] Decidere: Incident Replay prima o Show HN ora?
- [ ] Creare Discord "Lingua Universale"
- [ ] Lista 15-20 persone per DM pre-lancio

---

## DOVE TROVARE LE COSE

| Cosa | Path |
|------|------|
| **LU Debugger** | `lu-debugger/` (codice) / lu-debugger.fly.dev (live) |
| **Tour of LU** | `playground/tour.js` / playground/?tour (live) |
| **MAPPA 5 PROGETTI** | `.sncp/roadmaps/MAPPA_5_PROGETTI_LU.md` |
| **Show HN v2** | `docs/SHOW_HN_V2_DRAFT.md` |
| **Auto-Compact Research** | `.sncp/progetti/cervellaswarm/reports/RESEARCH_20260314_AUTO_COMPACT_CLAUDE_CODE.md` |
| **SNCP Health Analysis** | `.sncp/progetti/cervellaswarm/reports/ENGINEER_20260314_SNCP_HEALTH_ANALYSIS.md` |
| **Public repo** | github.com/rafapra3008/cervellaswarm |

---

## DECISIONI PRESE (S460)

1. **PostCompact hook** -- salva compact_summary in markdown leggibile
2. **COMPACT INSTRUCTIONS** -- `/compact` manual con istruzioni > auto-compact generico
3. **Limite 250 righe** -- confermato come standard, allineato ovunque
4. **stato.md definitivamente morto** -- tutti i riferimenti rimossi, script zombie disabilitati
5. **NORD.md snellito** -- storia archiviata, focus su stato corrente

---

## Lezioni Apprese (S460)

### Cosa ha funzionato bene
- **Audit PRIMA di implementare**: La Guardiana ha trovato gap nel piano (33 file vs 25 stimati, 3 script non coperti). Pattern "audit piano -> implementa -> audit risultato" funziona.
- **Worker in background per grep/replace**: 25+ file aggiornati senza consumare context della Regina.
- **P3 fixati tutti**: "Ci piace fissare tutto!" -- diamante lucidato a zero residui.

### Cosa non ha funzionato
- **Stima file da aggiornare**: 25 stimati, 33 reali. Sempre fare grep COMPLETO prima di stimare.

### Pattern confermato
- **"Grep PRIMA, stima DOPO"**: quando cambi un parametro globale, conta TUTTE le occorrenze prima.
- **Guardiana QA + Ops su ogni blocco**: due prospettive diverse trovano problemi diversi.

---
*"Lavoriamo in pace! Senza casino! Dipende da noi!"*
*S460: SNCP diamante. Il sistema e piu pulito di sempre.*
