# PROMPT RIPRESA - Contabilita Antigravity

> **Ultimo aggiornamento:** 19 Febbraio 2026 - Sessione 88
> **Branch attivo:** lab-v3 (sviluppo V3) + lab-v2 (intoccato) + main (produzione)
> **Versione canonica:** `CervellaSwarm/.sncp/progetti/contabilita/PROMPT_RIPRESA_contabilita.md`

---

## Stato Attuale - S88 COMPLETATA (CR + Bug Hunt + Studio Logica V3)

| Cosa | Stato |
|------|-------|
| **Produzione** | v2.11.0 LIVE su contabilitafamigliapra.it (INTATTA, zero modifiche) |
| **Lab v2 VM** | v1.13.0 LIVE su lab.contabilitafamigliapra.it (HTTPS, DB v10) |
| **Lab v2 locale** | INTOCCATO, branch lab-v2, porta 8001 |
| **Lab V3 locale** | branch lab-v3, porta 8003, Docker healthy |
| **FASE C** | COMPLETATA S84-S87 (7/7 step) |
| **S88** | **COMPLETATA** - 33 fix, 19 test nuovi, 4 audit Guardiana (9.7+9.5+9.5+9.3/10) |
| **Test** | 1265/1265 PASS (0 warnings) |
| **Prossimo** | **FASE D - Agent Python + Delta sync + Test reali NL** |

---

## S88 - Riepilogo

- **CR V3**: 3 Cervelle parallele, 30 fix (logger, dead code, info leak, DRY, validate_source, UUID merge)
- **Bug Hunt V3**: 2 Cervelle, 6 bug (match_status update, batch_id guard, double space, format_amount, warnings)
- **Studio Logica V3**: 2 Cervelle, 3 fix (match_status='unmatched' per errori, doc fix, fallback SCONOSCIUTO)
- **Finding FASE D**: nome formato diverso pdf vs ericsoft, movimenti orfani retry, PAYMENT_MAP HP/SHE

---

## Subroadmap V3

| Fase | Cosa | Status |
|------|------|--------|
| **A-C** | Setup + Studio + Transformer + Source | **COMPLETATA S80-S87** |
| **QA+QA2** | 4 Round QA + CR + BH + SL | **COMPLETATA S82-S88** |
| **D** | Agent Python + Delta sync + Test reali NL | PENDING |
| **E** | Deploy VM + Agent su NL + E2E | PENDING |
| **F** | Confronto Ericsoft vs PDF + Decisione | PENDING |

---

## Dove leggere

| Cosa | File (lab-v3 worktree) |
|------|------|
| EricsoftMixin (ingest + match_status) | `backend/database/ericsoft.py` |
| EricsoftTransformer v1.0.1 | `backend/processors/ericsoft_transformer.py` |
| Router Ericsoft v1.2.0 | `backend/routers/ericsoft.py` |
| VALID_SOURCES | `backend/database/transactions.py` |

---

*Per dettagli completi: leggi NORD.md nella root del progetto (lab-v3)*
