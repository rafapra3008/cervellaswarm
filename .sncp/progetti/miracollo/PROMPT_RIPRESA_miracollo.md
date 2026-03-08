<!-- DISCRIMINATORE: ECOSISTEMA MIRACOLLO - PANORAMA -->

# PROMPT RIPRESA - Ecosistema Miracollo

> **Ultimo aggiornamento:** 8 Marzo 2026 - Sessione 13 (pulizia casa completata)
> **Status:** miracollo.com LIVE! | Health 9.5/10 | Security 10/10 | Design 9.5/10 | **Pulizia Casa DONE**

---

## I 3 BRACCI

| Braccio | Porta locale | Workspace | Score |
|---------|-------------|-----------|-------|
| **PMS Core** | 9001 | `~/Developer/miracollogeminifocus/` | 90% LIVE, Health 9.5, Security 10/10 |
| **Miracollook** | 9002 | `~/Developer/miracollook/` (REPO SEPARATO!) | FASE 0 95%, 6 fasi totali |
| **Room Hardware** | 9003 | (futuro) | 10% - Bloccato VLAN |

---

## SESSIONE 13 - COMPLETATA (8 Mar 2026)

### Parte 1: Infrastruttura (FASE 1+2)
- I1: docker-compose.local.yml porta 9001 + bind 127.0.0.1
- I4: pytest 400+ test in CI + pipefail fix
- I5: Fortezza Mode v3, v1+v2 archiviati
- I8: DB backup pre-deploy
- I9: @pytest.mark.critical (ora 47 test, era 42)
- I10: Branch protection master
- Smoke test post-deploy + CORS default 9001
- Security audit: PASS | Guardiana: 9.5
- I14: HetrixTools monitoring (Rafa configurato, Telegram attivo)

### Parte 2: Pulizia Casa
- **Root cleanup:** 41 -> 8 file alla root
  - 5 -> docs/ (attiva), 17 -> docs/archivio/, 6 -> scripts/, 6 eliminati (duplicati)
  - Broken references fixate in CHANGELOG, GDPR, COSTITUZIONE, STRUCTURED_LOGGING
- **Test conversion:** 3 file da `requests` a `pytest TestClient` (CI-compatible)
  - test_immutable_guard.py (4 test, @critical - fiscal compliance)
  - test_payment_flow_sprint2_3.py (1 e2e, @critical - payment flow)
  - test_room_assignments_conflict.py (8 test - room segment conflicts)
- **Docker VM cleanup:** 11.52 GB build cache pulita, disco 79% -> 24%
  - `docker builder prune --all --force` aggiunto auto in deploy.yml
- 4 Guardiana audit: test 9.5/10, cleanup 9.2/10 (fix P2+P3 applicati)

---

## PROSSIMI STEP (ordine priorita)

### Prossima sessione
1. **Feature** -> Fatture XML (F1) o Channel Manager F3.5 (F2) o Miracollook FASE 2 (F3)
2. **Infra** -> I7 Miracollook healthcheck (repo separato)
3. **Infra** -> I11-I13 Miracollook pipeline, Playwright, linting

### Decisioni aperte per Rafa
- Quale feature prima? Fatture XML vs Channel Manager vs Miracollook

---

## INFRASTRUTTURA LIVE

```
VM: miracollo-cervella (GCP), e2-small, RUNNING
IP: 34.134.72.207 | SSL: auto-renew OK (31 Mag 2026)
Deploy: GitHub Actions + pytest gate + smoke test + auto Docker prune
Backup: 2x/giorno + pre-deploy | Master: PROTETTO
Porte locale: 9001 (PMS), 9002 (Miracollook), 9003 (Room HW)
Fortezza Mode v3: docs/FORTEZZA_MODE_v3.md (UNICO doc!)
Monitoring: HetrixTools 1min check + Telegram alert
Disco VM: 24% (15GB liberi) dopo cleanup
```

## STRUTTURA ROOT (post-pulizia)

```
README.md, CLAUDE.md, NORD.md, INSTALL.md, QUICK_START.md,
CHANGELOG.md, PROMPT_RIPRESA.md, deploy.sh
(8 file totali - era 41)
```

## PUNTATORI

- Piano Infrastruttura: `infra/PIANO_INFRASTRUTTURA_MIRACOLLO.md`
- Fortezza Mode v3: `docs/FORTEZZA_MODE_v3.md`
- Design Roadmap: `roadmaps/ROADMAP_DESIGN_95.md`

---

## Lezioni Apprese (Sessione 13)

### Funzionato bene
- Worker fuori context (Ops, Qualita, Ingegnera) -> trovano piu della Regina sola
- "Ogni step -> Guardiana audit" funziona per TUTTO (infra, test, cleanup)
- "Facciamo persino P3" = root broken refs catturate e fixate
- Docker auto-prune in deploy.yml previene accumulo futuro

### Cosa non ha funzionato
- 3 test file usavano `requests` contro localhost:8001 -> mai eseguiti in CI (ORA fixati)
- 41 file alla root creavano confusione (ORA organizzati)
- Build cache Docker 11.52 GB mai pulita (ORA auto-prune)

### Pattern confermato
- "git mv" preserva history -> sempre usare per spostamenti
- Dopo ogni batch di file moves -> grep globale per broken refs (CRITICO!)
- "Guardiane fuori context" -> trovano di piu separatamente

---

*"Lavoriamo in pace! Senza casino! Dipende da noi!"*
*Cervella & Rafa - 8 Marzo 2026*
