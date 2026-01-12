# CRITICO: Workflow Locale ↔ VM/Produzione

> **Data:** 11 Gennaio 2026 - Sessione 166
> **Segnalato da:** Rafa
> **Priorita:** CRITICA - Ha gia' perso ore di lavoro!
> **Status:** DA RISOLVERE con sessione dedicata

---

## IL PROBLEMA

```
+================================================================+
|                                                                |
|   SCENARIO DISASTRO (gia' successo su Contabilita!):           |
|                                                                |
|   1. Modifichi direttamente su VM (produzione)                 |
|   2. Non aggiorni locale                                       |
|   3. Fai deploy da locale -> VM                                |
|   4. MODIFICHE SU VM SOVRASCRITTE!                             |
|   5. ORE DI LAVORO PERSE!                                      |
|                                                                |
+================================================================+
```

---

## REGOLA D'ORO (da implementare)

```
MAI MODIFICARE DIRETTAMENTE SU VM/PRODUZIONE!

TUTTO deve passare:
  LOCALE -> GIT -> DEPLOY AUTOMATICO -> PRODUZIONE

Se serve fix urgente:
  1. Fallo su LOCALE
  2. Commit + Push
  3. Deploy automatico
  4. MAI toccare VM direttamente!
```

---

## SOLUZIONI DA STUDIARE

### 1. Protezione VM (tecnica)
- [ ] Rendere file read-only in produzione?
- [ ] Utente deploy separato da utente dev?
- [ ] Alert se file modificati manualmente?

### 2. Sincronizzazione Forzata
- [ ] Script pre-deploy che verifica sync locale/remoto
- [ ] Blocca deploy se ci sono diff non committate su VM
- [ ] Pull automatico da VM prima di lavorare?

### 3. Hook Claude Code
- [ ] Hook che avvisa se stai modificando file di produzione
- [ ] Check automatico sync prima di ogni sessione

### 4. Processo Documentato
- [ ] Checklist obbligatoria prima di deploy
- [ ] Regole chiare in CLAUDE.md di ogni progetto
- [ ] Training per tutte le Cervelle

### 5. Backup Automatico
- [ ] Snapshot VM prima di ogni deploy
- [ ] Git history su VM (non solo locale)
- [ ] Recovery plan se succede di nuovo

---

## PROGETTI COINVOLTI

| Progetto | VM | Rischio |
|----------|-----|---------|
| Contabilita | cervella-contabilita | ALTO (gia' successo!) |
| Miracollo | miracollo-cervella | MEDIO |
| CervellaSwarm | N/A (solo locale) | BASSO |

---

## DOMANDE PER RAFA

1. Come e' successo esattamente su Contabilita?
   - Cosa hai modificato sulla VM?
   - Come hai fatto deploy dopo?

2. Quali file sono piu' a rischio?
   - Config? Backend? Frontend?

3. Preferisci soluzione tecnica (blocco) o processo (checklist)?

---

## SESSIONE DEDICATA

**Quando:** Prima possibile (prima di altri deploy!)
**Durata:** 1-2 ore
**Obiettivo:**
- Analizzare il problema
- Scegliere soluzione
- Implementare protezioni
- Documentare processo

**Output atteso:**
- Regole chiare in CLAUDE.md
- Script/hook di protezione
- Checklist pre-deploy

---

## NOTA IMPORTANTE

Questo problema e' PIU' IMPORTANTE di feature nuove!
Un deploy sbagliato puo' cancellare GIORNI di lavoro.

```
"Meglio 1 ora per prevenire che 10 ore per rifare!"
```

---

*"Mai piu' perdere lavoro per errori di workflow!"*
*Sessione 166 - Regina & Rafa*
