# SUBROADMAP - Integrazione Ericsoft-Miracollo

> **Creato:** 30 Gennaio 2026 - Sessione 324
> **Aggiornato:** 31 Gennaio 2026 - Sessione 324 (decisione READ-ONLY)
> **Obiettivo:** Usare Miracollo con dati REALI da Ericsoft
> **Status:** READ-ONLY ATTIVO - Perfezionare Miracollo prima di bidirezionale

---

## DECISIONE STRATEGICA (S324)

```
+================================================================+
|                                                                |
|   APPROCCIO: READ-ONLY (Ericsoft → Miracollo)                 |
|                                                                |
|   "Miracollo è ancora prototipo. Sarebbe pericoloso           |
|    scrivere su Ericsoft. Dobbiamo migliorare Miracollo        |
|    al 30000% prima di fare sync bidirezionale."               |
|                                                 - Rafa, S324   |
|                                                                |
|   GUARDIANE: APPROVE 100% (Qualità 10/10, Security 9.5/10)    |
|                                                                |
+================================================================+
```

### Perché Questa Decisione

| Aspetto | Bidirezionale ORA | READ-ONLY ORA |
|---------|-------------------|---------------|
| Rischio Ericsoft | ALTO (bug → dati corrotti) | ZERO |
| Complessità | ALTA (Change Tracking, Outbox) | BASSA (già fatto!) |
| Miracollo pronto? | NO (prototipo) | Non serve |
| Tempo per perfezionare | NO | SI |

### Rischi Evitati

- **Data Corruption** - Bug in Miracollo NON può corrompere Ericsoft
- **Prenotazioni Perse** - Impossibile cancellare per errore
- **Conflitti Sync** - Ericsoft = unica fonte di verità

---

## INFO TECNICA

```
Server: SQL Server 2022 Express
IP: 192.168.200.5
Instance: NLTERMINAL01\SQLERICSOFT22
Database: PRA
```

### Credenziali

| Utente | Permessi | File | Git |
|--------|----------|------|-----|
| miracollook_reader | SELECT only | `.env` | NO |
| sa (ADMIN) | TUTTO | `.env.admin` | NO |

**NOTA:** Per READ-ONLY, `miracollook_reader` è SUFFICIENTE!

---

## STATO ATTUALE

```
+================================================================+
|   READ-ONLY: GIÀ FUNZIONANTE!                                  |
|                                                                |
|   Connector v2.1.0 + Cache Layer = PRONTO                     |
|   Miracollo può leggere dati Ericsoft ORA                     |
+================================================================+
```

| Componente | Status |
|------------|--------|
| Connector Ericsoft | v2.1.0 FUNZIONANTE |
| Cache Layer | ATTIVO (aiocache) |
| Utente DB | miracollook_reader (SELECT) |
| Change Tracking | NON NECESSARIO per ora |

---

## FASI AGGIORNATE

### FASE 1: READ-ONLY [COMPLETATA]

| Step | Descrizione | Status |
|------|-------------|--------|
| 1.1 | Connector base | FATTO (v2.1.0) |
| 1.2 | Cache layer | FATTO (S323) |
| 1.3 | Verifica permessi | FATTO (S324) |

**Output:** Miracollo può leggere dati Ericsoft in tempo reale

---

### FASE 2: Perfezionare Miracollo [CURRENT]

**Obiettivo:** Portare Miracollo al 30000% prima di pensare a bidirezionale

| Area | Da Sistemare |
|------|--------------|
| Planning | Quantità camere giuste |
| Prenotazioni | Schermata completa |
| Ospiti | Gestione quantità |
| UI/UX | Vari miglioramenti |
| Codice | Split file grandi |

**Criterio per passare a FASE 3:**
- Miracollo score ≥ 9.0/10
- Tutte le feature core funzionanti
- Test copertura adeguata

---

### FASE 3: Sync Bidirezionale [FUTURO]

**QUANDO:** Solo quando Miracollo è maturo (score ≥ 9.0)

| Step | Descrizione |
|------|-------------|
| 3.1 | Abilitare Change Tracking |
| 3.2 | Creare utente con permessi WRITE |
| 3.3 | Implementare Outbox pattern |
| 3.4 | Parallel running 30+ giorni |
| 3.5 | Validazione completa |

**NON fare prima che Miracollo sia pronto!**

---

### FASE 4: Transizione [FUTURO LONTANO]

**QUANDO:** Dopo 6+ mesi di bidirezionale stabile

| Step | Descrizione |
|------|-------------|
| 4.1 | Feature parity check |
| 4.2 | Training staff |
| 4.3 | Cutover graduale |

---

## COSA NON SERVE ORA

| Cosa | Perché Non Serve |
|------|------------------|
| Change Tracking | READ-ONLY non lo richiede |
| Utente con WRITE | Non scriviamo su Ericsoft |
| Outbox pattern | Solo per bidirezionale |
| CDC | Express non lo supporta + non serve |

**Tutto questo sarà valutato QUANDO Miracollo sarà pronto.**

---

## FILE CHIAVE

| File | Descrizione |
|------|-------------|
| `connector.py` | Connector v2.1.0 (READ-ONLY) |
| `check_ericsoft_permissions.py` | Script verifica (eseguito S324) |
| `setup_change_tracking.sql` | PARCHEGGIATO (per futuro) |
| `.env` | Credenziali reader |
| `.env.admin` | Credenziali admin (per futuro) |

---

## DECISION LOG

| Data | Decisione | Motivo | Chi |
|------|-----------|--------|-----|
| 30/01 | Focus uso INTERNO | "Non è per vendere, è per noi" | Rafa |
| 30/01 | Verifica permessi | Guardiana: rischio ALTER | Guardiana |
| 30/01 | Abbiamo accesso ADMIN | Documentato | Rafa |
| **31/01** | **READ-ONLY per ora** | **Miracollo è prototipo, troppo rischioso scrivere su Ericsoft** | **Rafa + Guardiane** |
| 31/01 | Bidirezionale SOLO quando pronto | Score ≥ 9.0 richiesto | Guardiane |

---

## PROSSIMI STEP (S325+)

1. **Focus su Miracollo** - Perfezionare UI/planning/prenotazioni
2. **Usare dati reali** - Connector già funziona per READ
3. **NON toccare** - Change Tracking, utenti WRITE, bidirezionale
4. **Rivalutare** - Quando Miracollo sarà ≥ 9.0/10

---

*"Fatto BENE > Fatto VELOCE"*
*"Dobbiamo migliorare Miracollo al 30000% prima" - Rafa*

*Cervella & Rafa - Sessione 324*
