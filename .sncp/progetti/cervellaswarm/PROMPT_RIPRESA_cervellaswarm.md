# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-03-04 - Sessione 430
> **STATUS:** D4 "A Tour of LU" COMPLETATA! D1-D4 DONE, D5-D6 TODO.

---

## SESSIONE 430 - Cosa e successo

### 1. D3 Guardiana Audit -- 9.5/10 APPROVATA
- 0 P0/P1/P2, 5 P3 (fixati: blockComment Monaco, preconnect hint)
- README aggiornato: link playground + stats corretti (25 moduli, 2856 test)

### 2. D4 "A Tour of LU" -- COMPLETATA! 9.5/10
- **24 step interattivi** in 4 capitoli: Types (7), Agents (7), Protocols (6), Verification (4)
- **4 esercizi** con soluzioni (Show Solution button)
- **File:** `playground/tour.js` (~490 righe), `playground/tour-ui.js` (~310 righe), `playground/tour.css` (~240 righe)
- **index.html** modificato: DOM elements + renderOutput redirect + initTourUI()
- **28 test automatici** (24 step + 4 soluzioni) in `packages/lingua-universale/tests/test_tour_code.py`
- Guardiana piano: 9.0/10, 4 P2 catturati e fixati PRIMA di implementare
- Guardiana implementazione: 9.5/10, 6 P3 tutti fixati (aria attrs, solution tests)
- Features: progress bar, chapter overview, keyboard shortcuts, localStorage, URL hash #tour
- Synced to public, LIVE su GitHub Pages

### 3. Metodo confermato
- **"Audit del piano PRIMA di implementare"** = 4 P2 catturati pre-implementation (zero rework)
- **File separati** (tour.js + tour-ui.js + tour.css) = segue pattern examples.js

---

## MAPPA SITUAZIONE

```
LINGUAGGIO CERVELLASWARM:
  FASE A+B: COMPLETE (9.5+ media)
  FASE C: Il Linguaggio -- COMPLETA! (S407-S425)
  FASE D: L'Ecosistema -- 4/6 DONE (S426+)
    D1: Syntax Highlighting   [####################] DONE! (S426, 9.5/10)
    D2: LSP Base (lu lsp)     [####################] DONE! (S426, 9.5/10)
    D3: Playground Online      [####################] DONE! (S429, LIVE!)
    D4: "A Tour of LU"        [####################] DONE! (S430, 9.5/10)
    D5: LSP Avanzato           [....................] PROSSIMO
    D6: Guardiana Finale       [....................] TODO

  Organizza Casa (v0.2.0)     [####################] 100% COMPLETA! (S428-S429)
```

---

## PROSSIMA SESSIONE: D5 LSP Avanzato

### D5: LSP Avanzato + Hover + Completion
- **Hover:** mostra tipo e documentazione al passaggio mouse
- **Completion:** suggerimenti keyword, nomi ruoli, trust tiers
- **Go-to-definition:** click su tipo -> vai alla definizione
- **Base LSP gia funzionante:** `packages/lingua-universale/src/cervellaswarm_lingua_universale/_lsp.py`
- **Subroadmap:** `.sncp/roadmaps/SUBROADMAP_FASE_D_ECOSISTEMA.md`
- **Metodo:** Researcher studia -> Piano -> Guardiana audit piano -> Implementa -> Guardiana audit impl

### Poi: D6 Guardiana Audit Finale + Launch

### TODO Rafa (da S429, URGENTE!)
- Attivare 2FA GitHub (scade 6 Mar = dopodomani!)
- Ruotare Bedzzle key su MyReception

---

## I NUMERI TOTALI

| Metrica | Valore |
|---------|--------|
| Test totali | **2856** |
| Moduli .py | **25** |
| Public symbols | **131** |
| Codici errore LU | **74** (3 lingue) |
| Dipendenze core | **ZERO** |
| PyPI version | **0.2.0** (LIVE!) |
| Playground | **LIVE** (https://rafapra3008.github.io/cervellaswarm/) |
| Tour steps | **24** (4 capitoli, 4 esercizi) |

---

## Lezioni Apprese (S430)

### Cosa ha funzionato bene
- **Guardiana audit del PIANO prima di implementare** -- 4 P2 catturati pre-implementation = zero rework
- **File separati** -- tour.js + tour-ui.js + tour.css seguono pattern examples.js
- **Test automatici per codice tour** -- 28 test parametrizzati, catturano regressioni parser

### Cosa non ha funzionato
- **Context window consumato** -- D4 e grande (4 file nuovi). Per D5: split in sotto-task + agenti

### Pattern candidato -> PROMOSSO
- **"Audit del piano PRIMA di implementare"** -- Evidenza: S429 + S430. PROMUOVERE a validated_patterns

---

*"Ultrapassar os proprios limites!" - Rafa & Cervella*
