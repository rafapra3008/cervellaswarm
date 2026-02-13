# PROMPT RIPRESA - Contabilita

> **Ultimo aggiornamento:** 13 Febbraio 2026 - Sessione 12
> **Per SOLO questo progetto!**

---

## STATO ATTUALE

| Cosa | Stato |
|------|-------|
| **Produzione** | v2.10.0 LIVE (parser v1.9.0) - fix FEST DA DEPLOYARE |
| **IP** | 35.193.39.185 STATICO |
| **Lab 2.0** | Branch lab-v2, 28+ commit avanti, fix FEST cherry-picked |
| **Main** | Fix FEST (e43a480) + 34 guard test (c759c5d), da deployare |
| **Locale** | ISOLATO! :8000=main (baked), :8001=lab-v2 (mount) |
| **Telegram** | Solo produzione (locale/lab disabilitato) |

---

## Isolamento Ambienti - RISOLTO (Sessione 12)

Subroadmap "Struttura PER SEMPRE" **COMPLETATA** (6/6 step, score ~9.4/10).

```
ContabilitaAntigravity/       -> lab-v2 (sviluppo, hot-reload :8001)
ContabilitaAntigravity-main/  -> main (locale=produzione, baked :8000)
```

- `docker compose up -d --build` avvia :8000 con codice main
- `./scripts/lab.sh start` avvia :8001 con codice lab-v2
- `./scripts/verify-isolation.sh` verifica isolamento (10 check)

---

## PROSSIMI STEP

### Priorita 1 - Deploy fix FEST (FORTEZZA MODE)
- Dalla directory main, deploy su VM
- Post-deploy: verifica FEST17365 + FEST16364

### Priorita 2 - Riprendere v2.0
- FASE E (Chiusura Stagioni) + FASE F (Confronto SPRING)

---

## DECISIONI CHIAVE

| Decisione | Perche |
|-----------|--------|
| Git worktree per main/lab-v2 | Un solo repo, due directory, isolamento totale |
| Docker :8000 senza code mount | Codice baked = sempre uguale a main |
| Cherry-pick FEST prima di tutto | Evita perdita fix al merge futuro |
| Fix FEST su main E lab-v2 | Entrambi i branch hanno il fix |
| Dockerfile main allineato a lab-v2 | USER non-root, requirements-prod, no libpq-dev |

---

*"Contabilita e il nostro diamante."*
