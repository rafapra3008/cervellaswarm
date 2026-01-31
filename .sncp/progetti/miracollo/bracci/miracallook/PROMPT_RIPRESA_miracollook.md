<!-- DISCRIMINATORE: MIRACOLLOOK EMAIL CLIENT -->
<!-- PORTA: 8002 | TIPO: Email client AI per hotel -->
<!-- PATH: ~/Developer/miracollogeminifocus/miracallook/ -->
<!-- NON CONFONDERE CON: PMS Core (8001), Room Hardware (8003) -->

# PROMPT RIPRESA - Miracollook

> **Ultimo aggiornamento:** 31 Gennaio 2026 - Sessione 324
> **STATUS:** READ-ONLY ATTIVO - Focus su perfezionare Miracollo

---

## SESSIONE 324 - DECISIONE STRATEGICA

### La Grande Decisione

```
+================================================================+
|   APPROCCIO: READ-ONLY (Ericsoft → Miracollo)                 |
|                                                                |
|   "Miracollo è ancora prototipo. Dobbiamo migliorarlo         |
|    al 30000% prima di fare sync bidirezionale."               |
|                                                 - Rafa         |
|                                                                |
|   GUARDIANE: APPROVE 100%                                      |
|   - Qualità: 10/10                                             |
|   - Security: 9.5/10                                           |
+================================================================+
```

### Cosa Abbiamo Fatto

| # | Task | Risultato |
|---|------|-----------|
| 1 | Ricerca completa (3 agenti) | Pattern sync studiati |
| 2 | Verifica permessi in hotel | Script eseguito |
| 3 | Scoperto accesso ADMIN | Possiamo fare tutto |
| 4 | Piano bidirezionale pronto | Ma PARCHEGGIATO |
| 5 | **Decisione Rafa** | **READ-ONLY per ora** |
| 6 | **Guardiane validazione** | **APPROVE 100%** |

### Perché READ-ONLY

- Miracollo è ancora prototipo (planning, prenotazioni, ospiti da sistemare)
- Scrivere su Ericsoft con bug = DISASTRO (prenotazioni perse, dati corrotti)
- READ-ONLY = zero rischio per Ericsoft
- Tempo per perfezionare Miracollo con dati REALI

---

## STATO INTEGRAZIONE ERICSOFT

```
FASE 1: READ-ONLY              [####################] 100% ← GIÀ FATTO!
FASE 2: Perfezionare Miracollo [....................] CURRENT
FASE 3: Sync Bidirezionale     [....................] FUTURO (quando pronto)
FASE 4: Transizione            [....................] FUTURO LONTANO
```

**Connector v2.1.0:** FUNZIONANTE (READ-ONLY)
**Cache Layer:** ATTIVO (aiocache, S323)
**Change Tracking:** NON NECESSARIO per ora

---

## COSA NON FARE (per ora)

| Cosa | Perché |
|------|--------|
| Abilitare Change Tracking | Non serve per READ-ONLY |
| Creare utente WRITE | Non scriviamo su Ericsoft |
| Implementare Outbox | Solo per bidirezionale |

**Tutto parcheggiato fino a quando Miracollo ≥ 9.0/10**

---

## PROSSIMI STEP (S325+)

1. **Focus su Miracollo** - Planning, prenotazioni, ospiti
2. **Usare dati reali** - Connector già funziona
3. **NON toccare** - Sync bidirezionale
4. **Rivalutare** - Quando Miracollo score ≥ 9.0

---

## FILE CHIAVE

| File | Path |
|------|------|
| Connector v2.1.0 | `miracallook/backend/ericsoft/connector.py` |
| Script permessi | `miracallook/backend/scripts/check_ericsoft_permissions.py` |
| **SUBROADMAP** | `.sncp/.../miracallook/SUBROADMAP_ERICSOFT_SYNC.md` |
| Credenziali | `.env` (reader), `.env.admin` (admin - per futuro) |

---

## TEST: 38/38 PASS

- test_guest_profile.py: 18/18
- test_cache_layer.py: 20/20

---

*"Fatto BENE > Fatto VELOCE"*
*"Dobbiamo migliorare Miracollo al 30000% prima" - Rafa*

*Cervella & Rafa - Sessione 324*
