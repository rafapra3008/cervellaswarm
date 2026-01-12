# REGOLE WORKFLOW IBRIDO - VM + Locale

> **Data:** 11 Gennaio 2026
> **Autore:** Cervella Guardiana Qualita
> **Status:** PROPOSTA - Da validare con Rafa
> **Progetto:** Miracollo (applicabile a tutti)

---

## EXECUTIVE SUMMARY

```
+================================================================+
|                                                                |
|   WORKFLOW IBRIDO: VM (Produzione) + LOCALE (Sviluppo)         |
|                                                                |
|   VM     = SOLO produzione, hotfix critici                     |
|   LOCALE = Sviluppo nuovo, feature, refactor                   |
|                                                                |
|   OBIETTIVO: Parallelismo SENZA casino                         |
|                                                                |
+================================================================+
```

---

## 1. ANALISI RISCHI

### RISCHIO 1: Conflitti Merge (ALTO)

```
SCENARIO:
- Worker locale modifica users.py
- Qualcuno fa hotfix su VM in users.py
- Al merge: CONFLITTO!

IMPATTO: Medio-Alto
- Perdita tempo per risolvere
- Possibile introduzione bug
- Confusione su quale versione e corretta

PROBABILITA: Media
- Dipende da quanto spesso si tocca VM
```

### RISCHIO 2: Database Out of Sync (CRITICO)

```
SCENARIO:
- VM ha tabella users con 10.000 record reali
- Locale ha tabella users con schema diverso
- Al merge: schema mismatch!

IMPATTO: CRITICO
- Dati produzione a rischio
- Potenziale downtime
- Rollback complesso

PROBABILITA: Alta se non gestito
```

### RISCHIO 3: Migrations Collision (ALTO)

```
SCENARIO:
- Locale crea: 037_add_feature_x.sql
- VM crea: 037_hotfix_urgent.sql
- Stesso numero, contenuto diverso!

IMPATTO: Alto
- Database corrotto
- Sequenza migrations rotta
- Rollback difficile

PROBABILITA: Media-Alta
```

### RISCHIO 4: Chi Fa Deploy? (MEDIO)

```
SCENARIO:
- Feature pronta in locale
- Chi la porta su VM?
- Come? Quando?

IMPATTO: Medio
- Ritardi
- Confusione
- Errori umani

PROBABILITA: Alta senza regole
```

### RISCHIO 5: Dati Test vs Produzione (ALTO)

```
SCENARIO:
- Locale usa dati fake per test
- Codice assume struttura dati fake
- Su VM con dati reali: boom!

IMPATTO: Alto
- Bug in produzione
- Dati corrotti
- Utenti impattati

PROBABILITA: Media
```

### RISCHIO 6: Environment Variables Mismatch (MEDIO)

```
SCENARIO:
- Locale ha .env con STRIPE_KEY=test_xxx
- VM ha .env con STRIPE_KEY=live_xxx
- Codice locale non gestisce entrambi

IMPATTO: Medio-Alto
- Chiamate API falliscono
- Pagamenti rotti
- Debug difficile

PROBABILITA: Media
```

---

## 2. LE 7 REGOLE FERREE

### REGOLA 1: SEPARAZIONE ASSOLUTA

```
+================================================================+
|                                                                |
|   VM = PRODUZIONE. PUNTO.                                       |
|   LOCALE = SVILUPPO. PUNTO.                                     |
|                                                                |
|   Su VM: SOLO hotfix critici (utente bloccato, bug grave)      |
|   Tutto il resto: LOCALE                                        |
|                                                                |
+================================================================+

COSA SI FA SOLO SU VM:
[ ] Hotfix urgenti (bug bloccanti in produzione)
[ ] Verifiche logs/debug produzione
[ ] Restart servizi
[ ] Backup database

COSA SI FA SOLO IN LOCALE:
[ ] Sviluppo nuove feature
[ ] Refactor
[ ] Test nuove librerie
[ ] Esperimenti
```

### REGOLA 2: MIGRATIONS = SOLO UN POSTO

```
+================================================================+
|                                                                |
|   LE MIGRATIONS SI CREANO SOLO IN LOCALE                       |
|   POI SI PORTANO SU VM                                          |
|                                                                |
|   MAI creare migrations direttamente su VM                     |
|   (tranne emergenza assoluta)                                   |
|                                                                |
+================================================================+

PROCESSO:
1. Locale: creo migration 037_xxx.sql
2. Locale: testo su database locale
3. Commit + push
4. VM: pull + run migrations
5. Verifica VM OK

SE EMERGENZA SU VM:
1. Creo migration con numero ALTO (099_emergency_xxx.sql)
2. Documento IMMEDIATAMENTE in .sncp/
3. Alla prima occasione: riordino numeri
```

### REGOLA 3: SINCRONIZZAZIONE PRIMA DI INIZIARE

```
+================================================================+
|                                                                |
|   PRIMA di iniziare qualsiasi lavoro locale:                   |
|                                                                |
|   1. git pull dalla VM                                          |
|   2. Verifico stato migrations VM                               |
|   3. Se disallineato: STOP e risolvo                           |
|                                                                |
+================================================================+

COMANDO SYNC (da creare):
sync-from-vm.sh miracollo

COSA FA:
1. SSH sulla VM
2. git status (verifica nessun uncommitted)
3. git push (se ci sono commit)
4. Locale: git pull
5. Verifica migrations in sync
6. OK oppure WARNING
```

### REGOLA 4: HOTFIX VM = COMMIT IMMEDIATO

```
+================================================================+
|                                                                |
|   Se fai QUALSIASI modifica su VM:                              |
|                                                                |
|   1. Commit SUBITO (anche singola riga)                         |
|   2. Push SUBITO                                                |
|   3. Documenta in .sncp/ SUBITO                                 |
|                                                                |
|   MAI lasciare modifiche uncommitted su VM!                    |
|                                                                |
+================================================================+

TEMPLATE COMMIT VM:
[HOTFIX-VM] [YYYY-MM-DD] [descrizione breve]

ESEMPIO:
[HOTFIX-VM] [2026-01-11] Fix 500 error on /api/users
```

### REGOLA 5: DATABASE SEPARATI

```
+================================================================+
|                                                                |
|   LOCALE usa database SEPARATO (test o copia)                   |
|   MAI connettersi a database produzione da locale              |
|                                                                |
+================================================================+

SETUP LOCALE:
- DB_URL=sqlite:///./data/miracollo_dev.db
- Seed con dati fake
- Script reset-db-local.sh per pulire

PRODUZIONE:
- DB_URL=sqlite:///./data/miracollo.db
- Dati REALI (mai toccare direttamente)
- Backup automatico
```

### REGOLA 6: ENV ESPLICITI

```
+================================================================+
|                                                                |
|   Codice DEVE gestire esplicitamente:                           |
|   - ENVIRONMENT=development (locale)                            |
|   - ENVIRONMENT=production (VM)                                 |
|                                                                |
|   SE manca ENVIRONMENT, codice DEVE fallire (non assumere)     |
|                                                                |
+================================================================+

PATTERN OBBLIGATORIO:
if os.getenv("ENVIRONMENT") not in ["development", "production"]:
    raise ValueError("ENVIRONMENT must be set!")

if os.getenv("ENVIRONMENT") == "production":
    # produzione
else:
    # development
```

### REGOLA 7: DEPLOYMENT = PROCESSO DEFINITO

```
+================================================================+
|                                                                |
|   SOLO la Regina (o Rafa esplicitamente) decide QUANDO         |
|   portare codice da locale a VM.                                |
|                                                                |
|   Worker MAI fa deploy autonomamente.                           |
|                                                                |
+================================================================+

PROCESSO DEPLOY:
1. Feature completata in locale
2. Test passano in locale
3. Guardiana approva (review)
4. Regina dice: "OK per deploy"
5. Eseguo deploy-to-vm.sh [feature-branch]
6. Test su VM
7. Merge su main
```

---

## 3. CHECKLIST PRE-MERGE (Locale -> VM)

### CHECKLIST OBBLIGATORIA

```
PRIMA DI PORTARE CODICE DA LOCALE A VM:

=== SYNC ===
[ ] VM ha tutte le modifiche committate?
[ ] Ho fatto git pull dalla VM?
[ ] Il mio branch e aggiornato con main?

=== DATABASE ===
[ ] Le migrations sono in ordine? (numeri sequenziali)
[ ] Ho testato migrations su database pulito?
[ ] Lo schema finale e corretto?
[ ] Ho backup del database VM prima di applicare?

=== ENV ===
[ ] Codice gestisce ENVIRONMENT correttamente?
[ ] Nuove variabili ENV documentate?
[ ] Nuove variabili presenti su VM?

=== TEST ===
[ ] Test passano in locale?
[ ] Ho testato con dati simili a produzione?
[ ] Edge cases coperti?

=== REVIEW ===
[ ] Guardiana ha approvato il codice?
[ ] Nessun TODO lasciato nel codice?
[ ] Nessun console.log / print debug?
[ ] Type hints presenti?

=== DEPLOY ===
[ ] So quali servizi riavviare?
[ ] Ho il comando di rollback pronto?
[ ] Qualcuno e disponibile se qualcosa va storto?
```

### SCRIPT VERIFICA (da creare)

```bash
# pre-merge-check.sh
#!/bin/bash

echo "=== PRE-MERGE CHECK ==="

# 1. Sync check
echo "[1/5] Checking VM sync..."
ssh miracollo-cervella "cd /app/miracollo && git status --porcelain"
if [ $? -ne 0 ]; then
    echo "FAIL: VM has uncommitted changes!"
    exit 1
fi

# 2. Migrations check
echo "[2/5] Checking migrations..."
LAST_LOCAL=$(ls backend/migrations/*.sql | tail -1 | grep -oP '\d+')
LAST_VM=$(ssh miracollo-cervella "ls /app/miracollo/backend/migrations/*.sql | tail -1" | grep -oP '\d+')
if [ "$LAST_LOCAL" != "$LAST_VM" ]; then
    echo "WARNING: Migrations not in sync! Local: $LAST_LOCAL, VM: $LAST_VM"
fi

# 3. Env check
echo "[3/5] Checking ENV..."
# ... verifica env

# 4. Test check
echo "[4/5] Running tests..."
pytest backend/tests/

# 5. Review check
echo "[5/5] Checking review approval..."
# ... verifica file .approved esiste

echo "=== PRE-MERGE CHECK COMPLETE ==="
```

---

## 4. WORKFLOW COMPLETO

### Scenario: Nuova Feature

```
GIORNO 1 - SETUP:
1. Locale: git pull (sync con VM)
2. Locale: git checkout -b feature/nome
3. Locale: sviluppo...

GIORNO 2-N - SVILUPPO:
4. Locale: sviluppo e test
5. Locale: commit progressivi
6. SE serve migration: creo in locale
7. Testo migration su db locale

FINE SVILUPPO:
8. Locale: test completi
9. Locale: push branch
10. Guardiana: review e approval
11. Regina: OK per deploy

DEPLOY:
12. VM: git pull origin feature/nome
13. VM: run migrations (se presenti)
14. VM: restart servizi
15. VM: test smoke
16. VM: git merge feature/nome
17. VM: git push
18. Locale: git pull (sync)
```

### Scenario: Hotfix Urgente su VM

```
EMERGENZA:
1. VM: fix diretto (minimal)
2. VM: git add . && git commit -m "[HOTFIX-VM] descrizione"
3. VM: git push
4. Documenta in .sncp/memoria/decisioni/YYYYMMDD_hotfix_xxx.md

DOPO:
5. Locale: git pull
6. Locale: verifica hotfix sensato
7. SE hotfix brutto: refactor in locale, poi deploy pulito
```

---

## 5. SCRIPT DA CREARE

| Script | Scopo |
|--------|-------|
| `sync-from-vm.sh` | Sincronizza locale con VM |
| `check-vm-status.sh` | Verifica stato VM (uncommitted, logs, etc) |
| `pre-merge-check.sh` | Checklist automatica pre-deploy |
| `deploy-to-vm.sh` | Deploy sicuro con rollback |
| `backup-vm-db.sh` | Backup database prima di migration |

---

## 6. MATRICE RESPONSABILITA

| Azione | Chi Decide | Chi Esegue |
|--------|------------|------------|
| Creare migration | Worker Backend | Worker Backend |
| Approvare codice | Guardiana | - |
| Decidere deploy | Regina (o Rafa) | - |
| Eseguire deploy | Worker designato | Worker designato |
| Hotfix urgente VM | Rafa (se critico) | Worker assegnato |
| Rollback | Regina | Worker assegnato |

---

## 7. SEGNALI DI ALLARME

### STOP IMMEDIATO SE:

```
[ ] Migrations locali e VM hanno numeri duplicati ma contenuto diverso
[ ] Database VM modificato direttamente (senza migration)
[ ] Codice su VM diverso da quello su GitHub
[ ] Test falliscono su VM dopo deploy
[ ] Piu di 3 hotfix su VM in una settimana (sintomo di rush)
```

### AZIONE:

```
1. STOP tutto
2. Sincronizza TUTTO (VM, locale, GitHub)
3. Risolvi discrepanze
4. Documenta cosa e successo
5. Riprendi solo quando tutto allineato
```

---

## 8. RIEPILOGO VISIVO

```
+------------------------------------------------------------------+
|                                                                  |
|   [LOCALE - MacBook]                    [VM - Google Cloud]       |
|                                                                  |
|   +------------------+                  +------------------+      |
|   |                  |                  |                  |      |
|   | SVILUPPO         |   ----GIT--->    | PRODUZIONE       |      |
|   | - Feature        |                  | - Live           |      |
|   | - Refactor       |                  | - Utenti reali   |      |
|   | - Test           |                  | - Database reale |      |
|   |                  |   <---GIT----    |                  |      |
|   | DB: miracollo_dev|                  | DB: miracollo    |      |
|   |                  |                  |                  |      |
|   +------------------+                  +------------------+      |
|                                                                  |
|   REGOLE:                                                        |
|   1. Locale = sviluppo, VM = produzione                          |
|   2. Migrations solo da locale -> VM                              |
|   3. Sync PRIMA di iniziare                                       |
|   4. Hotfix VM = commit immediato                                 |
|   5. Database separati                                            |
|   6. ENV espliciti                                                |
|   7. Deploy = processo definito                                   |
|                                                                  |
+------------------------------------------------------------------+
```

---

## VERDETTO GUARDIANA

```
+================================================================+
|                                                                |
|   RISCHIO WORKFLOW IBRIDO: GESTIBILE                           |
|                                                                |
|   SE seguiamo le 7 regole: SICURO                              |
|   SE NON seguiamo le regole: CASINO GARANTITO                  |
|                                                                |
|   RACCOMANDAZIONE:                                             |
|   - Creare script automatici (sync, check, deploy)             |
|   - Rispettare SEMPRE checklist pre-merge                      |
|   - Documentare OGNI hotfix su VM                              |
|   - Preferire locale, VM solo per emergenze                    |
|                                                                |
+================================================================+
```

---

*"Meglio regole chiare oggi che casino domani."*

*Cervella Guardiana Qualita - 11 Gennaio 2026*
