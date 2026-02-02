# Quality Check - SNCP 4.0 FASE 2

> Script per valutare qualità PROMPT_RIPRESA files

## Overview

`quality-check.py` analizza i PROMPT_RIPRESA di ogni progetto e assegna uno **score 0-10** basato su 4 criteri chiave.

**Target:** 9.5/10 per tutti i progetti

## Criteri di Valutazione

### 1. Actionability (30%)
**"Contiene TODO chiari e prossimi step?"**

Cerca:
- `TODO:`, `PROSSIMI STEP`, `NEXT:`
- Checkbox `[ ]`, `⬜`
- Liste numerate di step

**Score:**
- 10/10: ≥10% righe con action items + sezione PROSSIMI STEP
- 8/10: 5-10% righe con action items
- 6/10: 2-5% righe con action items
- 4/10: Almeno qualche action item
- 2/10: Nessun action item chiaro

### 2. Specificity (30%)
**"Info specifiche vs vaghe?"**

**Good indicators:**
- Date specifiche: `2026-02-02`, `5 Gennaio`
- Versioni: `v1.2.3`
- Score numerici: `9.5/10`, `150/200 test`
- Porte: `:8001`
- Percentuali: `90%`

**Bad indicators:**
- "presto", "poi", "forse"
- "vari", "qualche", "alcuni"
- "recente", "molto", "probabile"

**Score:** Basato su ratio good/bad indicators

### 3. Freshness (20%)
**"Aggiornato di recente?"**

- < 7 giorni: 10/10
- 7-14 giorni: 8/10
- 14-30 giorni: 5/10
- 30-60 giorni: 3/10
- > 60 giorni: 2/10

### 4. Conciseness (20%)
**"Rispetta limiti di righe?"**

- < 100 righe: 10/10
- 100-150 righe: 8/10 + warning
- 150-200 righe: 4/10 + WARNING
- > 200 righe: 0/10 + ERROR

## Usage

### Controlla tutti i progetti
```bash
./scripts/sncp/quality-check.py
```

### Controlla progetto specifico
```bash
./scripts/sncp/quality-check.py cervellaswarm
./scripts/sncp/quality-check.py miracollo
./scripts/sncp/quality-check.py contabilita
```

### Output JSON
```bash
./scripts/sncp/quality-check.py --json
./scripts/sncp/quality-check.py cervellaswarm --json
```

## Output Example

```
======================================================================
SNCP 4.0 - PROMPT_RIPRESA Quality Check
======================================================================

🌟 CERVELLASWARM
   File: .sncp/progetti/cervellaswarm/PROMPT_RIPRESA_cervellaswarm.md
   Lines: 99 | Updated: 2026-02-02

   Scores:
      Actionability:  10.0/10  (30%)
      Specificity:    10.0/10  (30%)
      Freshness:      10.0/10  (20%)
      Conciseness:    10.0/10  (20%)

   TOTAL: 10.0/10 [EXCELLENT]

----------------------------------------------------------------------

✅ CONTABILITA
   File: .sncp/progetti/contabilita/PROMPT_RIPRESA_contabilita.md
   Lines: 57 | Updated: 2026-01-26

   Scores:
      Actionability:  2.0/10  (30%)
      Specificity:    10.0/10  (30%)
      Freshness:      8.0/10  (20%)
      Conciseness:    10.0/10  (20%)

   TOTAL: 7.2/10 [PASS]

   Suggestions:
      • Add more specific TODO items and NEXT steps

----------------------------------------------------------------------

======================================================================
AVERAGE SCORE: 8.9/10
======================================================================
```

## Status Levels

| Status | Score | Emoji |
|--------|-------|-------|
| EXCELLENT | ≥9.0 | 🌟 |
| PASS | 7.0-8.9 | ✅ |
| NEEDS_IMPROVEMENT | 5.0-6.9 | ⚠️ |
| FAIL | <5.0 | ❌ |

## JSON Output Format

```json
{
  "project": "cervellaswarm",
  "file": ".sncp/progetti/cervellaswarm/PROMPT_RIPRESA_cervellaswarm.md",
  "lines": 99,
  "updated": "2026-02-02",
  "scores": {
    "actionability": 10.0,
    "specificity": 10.0,
    "freshness": 10.0,
    "conciseness": 10.0
  },
  "total": 10.0,
  "status": "EXCELLENT",
  "warnings": [],
  "suggestions": []
}
```

## Uso Raccomandato

**1. Fine sessione:**
```bash
./scripts/sncp/quality-check.py [progetto]
```

**2. Pre-checkpoint:**
Verifica score ≥8.0 prima di commit

**3. Weekly review:**
Controlla tutti i progetti:
```bash
./scripts/sncp/quality-check.py
```

## Implementazione

**File:** `scripts/sncp/quality-check.py`
**Versione:** 1.0.0
**Data:** 2026-02-02
**Fase:** SNCP 4.0 FASE 2 - MF2
**Dipendenze:** Python 3.10+ standard library only

## Note Tecniche

- **No dipendenze esterne** - solo stdlib Python
- **Regex-based analysis** - veloce e affidabile
- **File mtime** per freshness check
- **Media pesata** per score finale
- **Suggestions automatiche** basate su score

## Prossimi Miglioramenti (v1.1.0)

- [ ] Trend tracking (score nel tempo)
- [ ] Integration con pre-commit hook
- [ ] Export HTML report
- [ ] Comparison tra progetti

---

*Script creato: Sessione 325 - SNCP 4.0 FASE 2*
*Cervella Backend + Cervella Regina*
