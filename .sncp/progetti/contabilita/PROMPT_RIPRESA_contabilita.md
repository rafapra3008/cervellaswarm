# PROMPT RIPRESA - Contabilita Antigravity

> **Ultimo aggiornamento:** 25 Febbraio 2026 - Sessione 148
> **Branch attivo:** lab-v3 (sviluppo V3) + lab-v2 (intoccato) + main (produzione)
> **Versione canonica:** `CervellaSwarm/.sncp/progetti/contabilita/PROMPT_RIPRESA_contabilita.md`

---

## Stato Attuale - S148 FASE N.6 DEPLOY COMPLETATA

| Cosa | Stato |
|------|-------|
| **Produzione** | v2.11.0 LIVE su contabilitafamigliapra.it (INTATTA) |
| **V3 VM** | v3.contabilitafamigliapra.it LIVE (**main.py v1.14.0** - deployato S148) |
| **3 Hotel Agent** | TUTTI **v2.0.1** deployato S148. NL+SHE+HP scheduler ON |
| **Lab v2** | INTOCCATO, frozen S87 |
| **Test** | **1441 portale** + **348 agent** = **1789 PASS** (0 warning) |
| **Round QA** | **112** (R111 Deploy Audit 9.5 + R112 Guardiana Finale 9.5) |
| **Subroadmap Lucidatura** | **100% COMPLETATA** (20/20 step, S140-S148) |

---

## S148 - Cosa e' stato fatto (FASE N.6 Deploy)

### Step 18: Deploy PORTALE (11 file)
- Script `deploy_v3_files.sh v2.0.0` - 12/12 step FORTEZZA verdi
- **11 file**: main.py v1.14.0, auth.py, admin.py v1.2.0, transactions.py (router+db), seasons.py, ericsoft_transformer.py, style.css, annullamenti.js, data.js, selection.js
- MD5 match 11/11, backup `.backup.20260225_063602`
- Health: v1.13.0 -> v1.14.0 OK. Prod + Lab-v2 intatti
- Cache bust: 3 JS -> `?v=202602250636`

### Step 19: Deploy AGENT (4 file su 3 hotel)
- Rafa via VPN: stop scheduler -> copy 4 file -> dry-run -> start scheduler
- **NL**: v2.0.1, WM 4039, 0 mov, HC.io OK
- **SHE**: v2.0.1, WM 21659, 6 mov CAP pronti
- **HP**: v2.0.1, WM 24368, 3 mov CAP pronti

### Step 20: Guardiana Finale
- Pre-Deploy Check: 7/7 PASS
- Guardiana R111 (Deploy Audit): 9.5/10 APPROVED
- Guardiana R112 (Post-Deploy): 9.5/10 APPROVED
- Live check: V3+Prod+Lab-v2 tutti OK, NL/HP/SHE pagine HTTP 200

---

## Cosa MONITORARE (prossime 24h)

1. **SHE**: 6 mov pronti al prossimo run reale (scheduler ogni 1h)
2. **HP**: 3 mov pronti al prossimo run reale
3. **Reconcile**: NL 14:00, SHE 14:10, HP 14:20 - verificare HC.io verde
4. **Rafa verifica UI**: colori HP, DELETE 409 messaggio, annullamenti card

---

## P3 Pendenti (cosmetici, NON bloccanti)

- ericsoft_transformer.py `__version__` 1.4.0 vs docs 1.5.0 (allineare in prossima sessione)
- f-string in logger (pre-esistente, performance marginale)
- Debug vars non usate in data.js (pre-esistente)

---

## Lezioni Apprese (Sessione 148)

### Cosa ha funzionato bene
- **Script FORTEZZA V3** (`deploy_v3_files.sh` + `pre_deploy_check_v3.sh`): 12 step automatizzati con rollback, zero errori manuali
- **Guardiana pre + post deploy**: audit sia sul codice che sul processo = confidenza massima
- **Dry-run agent su ogni hotel**: verifica PRIMA di attivare scheduler, zero sorprese

### Pattern candidato
- "Pre-deploy check script + dry-run deploy + real deploy" - tre fasi distinte prevengono errori. Evidenza: S148 (0 errori su 11+4 file, 3 hotel). Azione: PROMUOVERE

---

*S148: FASE N.6 DEPLOY COMPLETATA. 11 file portale + 4 file agent 3 hotel. Guardiane R111+R112 9.5/10. Subroadmap "La Lucidatura" 100% (20/20 step). 1789 test. 112 round QA.*
