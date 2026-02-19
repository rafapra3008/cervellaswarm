# PROMPT RIPRESA - Contabilita Antigravity

> **Ultimo aggiornamento:** 19 Febbraio 2026 - Sessione 97
> **Branch attivo:** lab-v3 (sviluppo V3) + lab-v2 (intoccato) + main (produzione)
> **Versione canonica:** `CervellaSwarm/.sncp/progetti/contabilita/PROMPT_RIPRESA_contabilita.md`

---

## Stato Attuale - S97 COMPLETATA (Deploy V3 su VM - V3 LIVE!)

| Cosa | Stato |
|------|-------|
| **Produzione** | v2.11.0 LIVE su contabilitafamigliapra.it (INTATTA) |
| **Lab v2 VM** | v1.13.0 LIVE su lab.contabilitafamigliapra.it (sync auto 4:30 AM) |
| **V3 VM** | **LIVE su https://v3.contabilitafamigliapra.it** (SSL, 12 headers, Health OK) |
| **FASE E.2-E.4** | **COMPLETATA S97** - Deploy V3, 3 servizi attivi sulla VM |
| **Test** | 1506/1506 PASS (0 warnings) - 1270 portale + 236 agent |
| **Prossimo** | **FASE E.5 - Script agent Windows (.bat + README)** |

---

## VM - 3 servizi attivi

| Servizio | URL | Porta |
|----------|-----|-------|
| Produzione | contabilitafamigliapra.it | :8000 |
| Lab v2 | lab.contabilitafamigliapra.it | :8001 |
| **V3 Ericsoft** | **v3.contabilitafamigliapra.it** | **:8003** |

---

## Subroadmap FASE E

| Step | Cosa | Status |
|------|------|--------|
| E.1 | Studio + File deploy | COMPLETATO S95 |
| E.2-E.4 | DNS + Deploy + SSL | **COMPLETATO S97** |
| **E.5** | Script .bat Windows + README agent | **PROSSIMO** |
| E.6-E.10 | Agent su NL + E2E | PENDING |

---

## Dove leggere

| Cosa | File (lab-v3 worktree) |
|------|------|
| Script deploy | `scripts/deploy_v3_setup.sh` + `scripts/deploy_v3_nginx.sh` |
| Nginx V3 | `deployment/nginx/contabilita-v3.conf` |
| Agent (8 moduli) | `agent/` directory |
| API keys V3 | `.v3_api_keys` (chmod 600, in .gitignore) |

---

*Per dettagli completi: leggi NORD.md su lab-v3*
