# STUDIO WORKFLOW OTTIMALE RAFA-REGINA

> **Data:** 9 Gennaio 2026
> **Autore:** cervella-researcher
> **Sessione:** 137

---

## EXECUTIVE SUMMARY

**Soluzione proposta:**
Sistema a **3 livelli di autonomia** con **quality gates integrati** e **comunicazione strategica**.

**Risultato atteso:**
- Qualità 100% su ogni deliverable
- Zero perdita direzione
- Rafa hands-off su implementazione, hands-on su strategia
- Regina autonoma con confini chiari

---

## 1. WORKFLOW SESSIONE

```
[00:00-00:15] INIZIO
├─ Regina: Legge PROMPT_RIPRESA + NORD
├─ Rafa: Dà obiettivo sessione
├─ Regina: PLAN MODE (breakdown + worker + quality gates)
└─ Insieme: Validazione piano

[00:15-01:15] ESECUZIONE AUTONOMA
├─ Regina spawna worker secondo piano
├─ Worker lavorano (2-3 paralleli max)
├─ Regina monitora, report solo milestone
└─ Rafa hands-off

[01:15-01:30] CHIUSURA
├─ Regina: Review + test
├─ Guardiana se critico
├─ Deploy + triple check
└─ Checkpoint (NORD, PROMPT_RIPRESA, git)
```

---

## 2. CHI DECIDE COSA

| Chi | Cosa |
|-----|------|
| **RAFA** | Strategia, priorità, scope, business, quando release |
| **REGINA** | Breakdown, implementazione, tool, worker, come |
| **INSIEME** | Piano validato, architettura, deploy, timeline |

### Autonomia Regina

**PROCEDE SOLA:**
- Implementazione tecnica
- Quale worker usare
- Tool e librerie standard
- Refactoring interno
- Testing strategy

**PROPONE + VALIDA CON RAFA:**
- Architettura nuova
- Breaking changes
- UX ambigua
- Deploy produzione

---

## 3. QUALITY 100% - 3 Livelli

### Livello 1: By Design
- Plan mode sempre
- Specialist giusto per task
- Definition of Done chiara

### Livello 2: Quality Gates
- Test locale 100%
- Review output worker
- FORTEZZA MODE pre-deploy

### Livello 3: Guardiane
- Critical path → Guardiana Qualità
- Deploy prod → Guardiana Ops
- Security → Guardiana Security

---

## 4. COMUNICAZIONE

| Quando | Dettaglio |
|--------|-----------|
| INIZIO | Alto (piano breakdown) |
| DURANTE | Basso (solo milestone/blocco) |
| FINE | Medio (risultato + evidence + next) |

**NO:** Progress continuo, dettagli implementativi
**SÌ:** Risultati, blocchi, decisioni strategiche

---

## 5. SEGUIRE LA MAPPA

| File | Cosa |
|------|------|
| NORD.md | Dove siamo ORA |
| ROADMAP | Dove ANDIAMO |
| PROMPT_RIPRESA | FILO del discorso |
| .sncp/memoria/ | PERCHÉ decisioni |

**Reality check ogni 30 min:** Ancora su roadmap?
**Idee fuori scope:** → .sncp/idee/parking_lot.md

---

## 6. METRICHE SUCCESSO

| Metrica | Target |
|---------|--------|
| Worker utilization | > 60% |
| Rework rate | < 10% |
| Deploy success | > 95% |
| Roadmap adherence | > 85% |

---

## 7. ROLLOUT GRADUALE (4 settimane)

| Settimana | Focus |
|-----------|-------|
| 1 | Plan Mode + Result Report + Checklist deploy |
| 2 | Worker utilization 60% + Pattern multi-worker |
| 3 | Guardiane su critical + SNCP usage |
| 4 | Fine-tune + Retrospettiva |

---

## CHECKLIST RAPIDE

### Inizio Sessione
- [ ] Letto PROMPT_RIPRESA + NORD
- [ ] Obiettivo Rafa chiaro
- [ ] Plan mode fatto
- [ ] Piano validato insieme

### Pre-Deploy (FORTEZZA)
- [ ] Test locale 100%
- [ ] Screenshot/evidence
- [ ] Backup fatto
- [ ] Rollback plan ready
- [ ] Rafa conferma

### Fine Sessione
- [ ] NORD aggiornato
- [ ] PROMPT_RIPRESA aggiornato
- [ ] .sncp/decisioni/ popolato
- [ ] git commit + push

---

## PRINCIPI GUIDA

> "QUALITÀ 100% non è un obiettivo. È il PROCESSO."

> "Rafa hands-on su strategia. Hands-off su implementazione."

> "Regina autonoma con confini chiari. Partner, non assistente."

> "Fatto BENE > Fatto VELOCE. Sempre."

---

*Studio completo: vedi output originale researcher (400+ righe)*
