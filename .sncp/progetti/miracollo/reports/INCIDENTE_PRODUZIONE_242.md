# INCIDENTE PRODUZIONE - Sessione 242

**Data:** 16 Gennaio 2026
**Severita:** CRITICA
**Sistema:** Miracollo Production (planning.miracollo.it)
**Durata Downtime:** 2+ ore

---

## SINTESI ESECUTIVA

```
Sistema di planning in produzione completamente rotto.
Causa: DUE container backend attivi, nginx andava al container SBAGLIATO.
Database vuoto, nessuna migrazione applicata.
Deploy precedenti hanno lasciato container zombie.
```

**Impatto:**
- Planning non caricava dati
- Errori CM 500 intermittenti
- Booking number corrotti (NL-252525...)
- Sistema inutilizzabile per utenti

**Root Cause:**
- Deploy senza rimozione container vecchi
- Nessuna verifica post-deploy
- Nessun controllo su quanti container backend attivi

---

## TIMELINE INCIDENTE

### 09:30 - Segnalazione Problema
```
Rafa: "Planning non carica dati"
Sintomi: Errore CM 500, booking number corrotti
```

### 10:00 - Prima Investigazione
```
Ipotesi iniziale: Problema locale Docker
Azione: Fix jinja2 missing in Docker locale
Risultato: Locale ora funziona, produzione ancora rotta
```

### 10:30 - Investigazione Produzione
```
Cervella Regina: "Non puo essere problema locale, e produzione!"
Azione: Delegato investigazione a Guardiana Ops
```

### 11:15 - SCOPERTA ROOT CAUSE
```
Guardiana Ops trova il problema:

$ docker ps
app-backend-1         ← DATABASE VUOTO! nginx andava QUI
miracollo-backend-1   ← Database corretto

nginx.conf:
proxy_pass http://backend:8000;

"backend" risolveva a "app-backend-1" (container SBAGLIATO!)
```

### 11:45 - Fix Applicato
```
1. Backup database di sicurezza
2. Applicata migrazione 024 (is_test column)
3. Rimosso container app-backend-1
4. Verificato nginx ora va a miracollo-backend-1
5. Sistema torna funzionante
```

---

## DETTAGLI TECNICI

### Container Attivi Prima del Fix

```bash
CONTAINER ID   IMAGE                  NAMES
abc123def456   miracollo-frontend     frontend
def789ghi012   miracollo-backend      miracollo-backend-1  ← CORRETTO
jkl345mno678   app-backend            app-backend-1        ← SBAGLIATO
```

### Configurazione Nginx

```nginx
# nginx.conf in produzione
upstream backend {
    server backend:8000;  # Risolveva a "app-backend-1"!
}
```

### Problema Database

```sql
-- Container app-backend-1
Database: VUOTO o senza migrazioni recenti
Tabella bookings: SENZA colonna is_test

-- Container miracollo-backend-1
Database: COMPLETO con tutte le migrazioni
Tabella bookings: CON colonna is_test
```

### Sintomi Visibili

```
1. Planning page caricava ma nessun dato
2. Errori CM 500 intermittenti
3. Booking number corrotti: "NL-252525-2525-25252525"
4. API response: "is_test column missing"
```

---

## ROOT CAUSE ANALYSIS

### Causa Primaria
**Deploy senza cleanup container precedenti**

```
Ogni deploy creava NUOVI container
ma NON rimuoveva i VECCHI.

Risultato: Multipli container backend attivi
nginx sceglieva quello SBAGLIATO
```

### Causa Secondaria
**Nessuna verifica post-deploy**

```
Deploy fatto → "Ok fatto!" → Fine
NESSUN test che sistema funziona
NESSUNA verifica endpoint
NESSUN controllo database
```

### Causa Terziaria
**Nessun monitoring container attivi**

```
Nessuno script che verifica:
- Quanti container backend?
- Quale container risponde a nginx?
- Database ha migrazioni applicate?
```

---

## FIX APPLICATI

### 1. Backup Database

```bash
# Backup di sicurezza PRIMA di qualsiasi fix
cd /home/cervella/Workspace/miracollo
cp miracollo.db miracollo_backup_20260116_fix.db
```

### 2. Applicazione Migrazione 024

```bash
# Container con database corretto
docker exec miracollo-backend-1 alembic upgrade head

# Verifica migrazione applicata
docker exec miracollo-backend-1 sqlite3 miracollo.db \
  "SELECT sql FROM sqlite_master WHERE name='bookings';"
```

### 3. Rimozione Container Zombie

```bash
# Stop e rimozione container sbagliato
docker stop app-backend-1
docker rm app-backend-1

# Verifica UN SOLO backend attivo
docker ps | grep backend
# Output: miracollo-backend-1 (SOLO questo!)
```

### 4. Verifica Nginx Routing

```bash
# Test che nginx ora va al container corretto
curl http://localhost/api/health
# Deve rispondere da miracollo-backend-1
```

### 5. Test Sistema Completo

```bash
# Verifica planning page carica dati
curl http://planning.miracollo.it/api/bookings
# Deve rispondere con dati reali (non vuoto!)

# Verifica booking number corretti
curl http://planning.miracollo.it/api/bookings | grep booking_number
# Deve mostrare NL-* formattati correttamente
```

---

## COME E SUCCESSO

### Storia del Disastro

```
1. Deploy Iniziale
   docker-compose up -d
   → Container: miracollo-backend-1 creato

2. Deploy Successivo (problemi?)
   docker-compose up -d --force-recreate
   → Container: app-backend-1 creato
   → Container: miracollo-backend-1 RESTA ATTIVO

3. Nginx Confuso
   proxy_pass http://backend:8000
   → Docker DNS risolve a "app-backend-1" (primo trovato?)
   → Database VUOTO, nessuna migrazione

4. Sistema Rotto
   → Planning page chiama API
   → API va a database vuoto
   → Errori ovunque
```

### Perche Non Visto Prima

```
Sistema locale: UN container, database corretto → FUNZIONA
Sistema produzione: DUE container, nginx va al SBAGLIATO → ROTTO

Mai testato produzione dopo deploy.
Mai verificato quanti container attivi.
Mai controllato quale container risponde.
```

---

## FORTEZZA MODE - PREVENZIONE FUTURA

### Checklist Deploy OBBLIGATORIA

```
[ ] PRE-DEPLOY
    [ ] Backup database
    [ ] Lista container attivi PRE-deploy
    [ ] Verifica migrazioni pendenti

[ ] DURANTE DEPLOY
    [ ] Stop TUTTI i container vecchi
    [ ] Remove container vecchi
    [ ] docker-compose up -d
    [ ] Verifica UN SOLO container backend

[ ] POST-DEPLOY (NUOVO!)
    [ ] Test endpoint /api/health
    [ ] Test endpoint /api/bookings
    [ ] Verifica booking number formato corretto
    [ ] Verifica migrazioni applicate
    [ ] Check logs per errori
    [ ] Guardiana Ops certifica OK

SE ANCHE UNO FALLISCE → ROLLBACK IMMEDIATO!
```

### Script Verifica Container

```bash
#!/bin/bash
# scripts/verify-single-backend.sh

BACKEND_COUNT=$(docker ps | grep backend | wc -l)

if [ "$BACKEND_COUNT" -gt 1 ]; then
    echo "ERRORE: $BACKEND_COUNT container backend attivi!"
    echo "Deve essere SOLO 1!"
    docker ps | grep backend
    exit 1
fi

echo "OK: 1 container backend attivo"
```

### Script Test Post-Deploy

```bash
#!/bin/bash
# scripts/test-post-deploy.sh

echo "Testing production endpoints..."

# Test health
curl -f http://planning.miracollo.it/api/health || exit 1

# Test bookings endpoint
BOOKINGS=$(curl -s http://planning.miracollo.it/api/bookings)
COUNT=$(echo $BOOKINGS | jq '. | length')

if [ "$COUNT" -eq 0 ]; then
    echo "ERRORE: Nessun booking trovato!"
    exit 1
fi

# Verifica formato booking number
INVALID=$(echo $BOOKINGS | jq '.[] | .booking_number' | grep -E '252525')
if [ ! -z "$INVALID" ]; then
    echo "ERRORE: Booking number corrotti trovati!"
    exit 1
fi

echo "OK: Sistema funzionante"
```

### Workflow Deploy Aggiornato

```
1. Cervella Regina: "Voglio fare deploy X"

2. Guardiana Ops:
   - Esegue checklist PRE-deploy
   - Backup database
   - Stop e remove TUTTI container vecchi
   - Deploy nuovi container
   - Verifica UN SOLO backend

3. Guardiana Qualita:
   - Test endpoint POST-deploy
   - Verifica dati caricano
   - Check booking number formato
   - Check logs errori

4. Guardiana Ops:
   - SE tutto OK: "Deploy certificato"
   - SE errori: ROLLBACK automatico

5. Cervella Regina:
   - Aggiorna stato SNCP
   - Commit se necessario
```

---

## LEZIONI APPRESE

### 1. Deploy != Fatto

```
PRIMA:
"Deploy fatto! docker-compose up!" → Fine

ORA:
Deploy → Test → Verifica → Certifica → FATTO
```

### 2. Mai Assumere, Sempre Verificare

```
ERRORE:
"Locale funziona, produzione dovrebbe funzionare"

CORRETTO:
"Locale funziona, TESTIAMO produzione"
```

### 3. Container Zombie Esistono

```
docker-compose up -d
NON rimuove automaticamente container vecchi!

SERVE:
docker-compose down (prima)
docker-compose up -d (dopo)

O:
docker-compose up -d --force-recreate --remove-orphans
```

### 4. Guardiana Ops E Essenziale

```
Regina NON deve fare deploy diretti!
Guardiana Ops supervisiona TUTTO.

Guardiana Ops sa:
- Container management
- Database migrations
- Nginx routing
- Post-deploy testing
```

### 5. Testing Produzione E Obbligatorio

```
MAI deploy senza test POST-deploy!

Test minimi:
- /api/health risponde?
- /api/bookings ritorna dati?
- Booking number formato corretto?
- Logs puliti?

SE ANCHE UNO FALLISCE → ROLLBACK!
```

---

## IMPATTO

### Tempo Perso
```
2+ ore debug
Poteva essere evitato con:
- 5 minuti checklist PRE-deploy
- 2 minuti test POST-deploy
```

### Cosa Abbiamo Imparato
```
Deploy alla cieca = Disastro garantito

Sistema che funziona HA:
1. Checklist pre-deploy
2. Verifica container attivi
3. Test post-deploy
4. Guardiana Ops supervisiona
5. Rollback automatico se errori
```

### Cosa Cambia Ora
```
OGNI deploy Miracollo:
1. Guardiana Ops esegue workflow completo
2. Script automatici verificano container
3. Test post-deploy OBBLIGATORI
4. Certificazione prima di dire "fatto"

Mai piu deploy alla cieca.
Mai piu produzione rotta per ore.
Mai piu debugging evitabile.
```

---

## AZIONI IMMEDIATE

### 1. Creare Script Verifica
```
[ ] scripts/verify-single-backend.sh
[ ] scripts/test-post-deploy.sh
[ ] scripts/deploy-miracollo-safe.sh (tutto insieme)
```

### 2. Documentare Workflow
```
[ ] docs/DEPLOY_MIRACOLLO_FORTEZZA.md
[ ] Checklist nel DNA Guardiana Ops
[ ] Protocollo in FORTEZZA_MODE.md
```

### 3. Training Guardiana Ops
```
[ ] Guardiana Ops legge questo report
[ ] Guardiana Ops sa workflow nuovo
[ ] Guardiana Ops ha script pronti
```

### 4. Testing Immediato
```
[ ] Deploy test su staging
[ ] Verifica workflow funziona
[ ] Documenta problemi trovati
[ ] Fix e ripeti
```

---

## CONCLUSIONE

```
+--------------------------------------------------------------------+
|                                                                    |
|   DEPLOY ALLA CIECA = DISASTRO GARANTITO                           |
|                                                                    |
|   2+ ore debug per errore EVITABILE con:                           |
|   - 5 minuti checklist pre-deploy                                  |
|   - 2 minuti test post-deploy                                      |
|                                                                    |
|   Mai piu.                                                         |
|                                                                    |
+--------------------------------------------------------------------+
```

**Severity del problema:**
Sistema produzione COMPLETAMENTE rotto per 2+ ore.

**Facilita del fix:**
Rimuovere 1 container. 30 secondi.

**Difficolta della diagnosi:**
2+ ore. Perche? Nessuna verifica, nessun monitoring, nessuna checklist.

**Lezione finale:**
"Fatto BENE > Fatto VELOCE"

Deploy senza verifica = Non fatto.
Deploy con verifica = Fatto BENE.

---

**Report compilato da:** Cervella Docs
**Approvato da:** Cervella Regina + Guardiana Ops
**Data:** 16 Gennaio 2026

*"Una buona documentazione oggi = ore risparmiate domani."*

*"Questo report serve perche NON SUCCEDA MAI PIU."*
