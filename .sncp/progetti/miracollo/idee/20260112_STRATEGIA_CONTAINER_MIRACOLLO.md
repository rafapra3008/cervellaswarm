# STRATEGIA CONTAINER MIRACOLLO - REPORT GUARDIANA OPS

> **Data:** 12 Gennaio 2026
> **Autore:** Cervella Guardiana Ops
> **Richiesto da:** Rafa
> **Severity:** ALTO - Decisione archittetturale
> **Verdict:** RACCOMANDAZIONI CHIARE

---

## EXECUTIVE SUMMARY

```
+==================================================================+
|                                                                  |
|   DIAGNOSI: Container duplicati per deploy MANUALI               |
|                                                                  |
|   RACCOMANDAZIONE:                                               |
|   1. KEEP backend-12 (nella rete, usato da nginx)                |
|   2. RIMUOVI backend-35 (orfano, porta esposta inutile)          |
|   3. IMPLEMENTA docker-compose (mai piu duplicati)               |
|                                                                  |
|   WORKFLOW FUTURO: docker-compose up -d                          |
|                                                                  |
+==================================================================+
```

---

## 1. DIAGNOSI - Cosa e Successo

### Situazione Attuale (Confermata)

| Container | Network | Port | Usato da Nginx | Codice |
|-----------|---------|------|----------------|--------|
| miracollo-backend-12 | miracollo-net | interno | SI (proxy_pass) | AGGIORNATO |
| miracollo-backend-35 | bridge (default) | 8001 esposta | NO | VECCHIO |

### Perche Esistono 2 Container?

**CAUSA: Deploy manuali senza script.**

```
TIMELINE RICOSTRUITA:

Sessione X (giorni fa):
  docker run -d --name miracollo-backend-35 -p 8001:8001 ...
  # Container con porta esposta, codice vecchio

Sessione Y (piu recente):
  # Qualcuno ha creato miracollo-net per isolare i servizi
  docker network create miracollo-net

  # Nuovo container nella rete interna
  docker run -d --name miracollo-backend-12 --network miracollo-net ...

  # MA: nessuno ha fermato/rimosso backend-35!

Risultato:
  - backend-12: dentro miracollo-net, usato da nginx (CORRETTO)
  - backend-35: fuori dalla rete, porta esposta, codice vecchio (ORFANO)
```

### Evidenze

1. **Audit Ingegnera (12 Gen 04:00):**
   - backend-12: NO port mapping (corretto - nginx fa proxy)
   - backend-35: 0.0.0.0:8001->8001 (perche? non serve)

2. **HTTPS funziona (200 OK, 6 applications):**
   - Nginx proxia a backend-12 via rete interna
   - backend-35 non e mai raggiunto da utenti

3. **Porta 8001 da Internal Server Error:**
   - backend-35 ha codice vecchio/rotto
   - Conferma che e un container orfano

### Questo ERA Intenzionale?

**NO.** Non e un blue-green deploy perche:
- I 2 container NON hanno la stessa configurazione
- backend-35 NON e in miracollo-net
- NON c'e load balancer
- NON c'e switch automatico

E semplicemente **un container dimenticato dopo un redeploy manuale**.

---

## 2. RACCOMANDAZIONE - Cosa Fare Ora

### 2.1 Azione IMMEDIATA (5 minuti)

```bash
# SSH sulla VM
ssh miracollo-cervella

# 1. VERIFICA: backend-12 risponde a nginx
curl -H "Host: api.miracollo.com" http://localhost:80/api/health
# Aspettati: 200 OK

# 2. VERIFICA: backend-12 logga le richieste
docker logs -f miracollo-backend-12 --tail 20
# In altro terminale: curl https://api.miracollo.com/api/health
# Aspettati: log della richiesta in backend-12

# 3. SE VERIFICHE OK: Rimuovi backend-35
docker stop miracollo-backend-35
docker rm miracollo-backend-35
```

### 2.2 Perche Rimuovere backend-35

| Motivo | Dettaglio |
|--------|-----------|
| **Spreco risorse** | RAM e CPU usati per niente |
| **Sicurezza** | Porta 8001 esposta = superficie attacco |
| **Confusione** | 2 container = dubbi su quale usare |
| **Codice vecchio** | Potrebbe creare problemi se qualcuno lo usa |
| **Non in rete** | Non puo comunicare con nginx/altri servizi |

### 2.3 NON Rimuovere SE

```
STOP! Non rimuovere backend-35 se:

1. Qualcuno usa attivamente porta 8001 (es. debug, webhook)
   → Verificare: lsof -i :8001

2. C'e un motivo documentato (che non ho trovato)
   → Chiedere a Rafa: "Perche era esposta la 8001?"

3. Vuoi tenerlo come backup temporaneo
   → OK, ma fermalo: docker stop miracollo-backend-35
```

---

## 3. WORKFLOW FUTURO - Come Lavorare

### 3.1 Filosofia (da Protocollo Ibrido Sessione 168)

```
LOCALE  = Sviluppo MODULI COMPLETI (blocchi interi)
LAB     = Test volatile (Docker, reset facile)
PROD    = Produzione SACRA (solo plug-in, mai sostituire)

FILOSOFIA: Aggiungere, MAI sostituire
```

### 3.2 Struttura Docker Consigliata

```yaml
# docker-compose.prod.yml (DA CREARE sulla VM)

version: '3.8'

networks:
  miracollo-net:
    driver: bridge

services:
  nginx:
    container_name: miracollo-nginx
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/conf.d:/etc/nginx/conf.d:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
      - ./frontend/dist:/usr/share/nginx/html:ro
    networks:
      - miracollo-net
    depends_on:
      - backend
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "nginx", "-t"]
      interval: 30s
      timeout: 10s
      retries: 3

  backend:
    container_name: miracollo-backend
    build: ./backend
    env_file:
      - .env.production
    volumes:
      - ./backend/data:/app/data
    networks:
      - miracollo-net
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3

# NOTA: NO ports per backend!
# Nginx fa proxy interno via miracollo-net
```

### 3.3 Workflow Deploy (NUOVO)

```bash
# === DEPLOY NORMALE ===

# 1. Pull codice aggiornato
cd /app/miracollo
git pull origin main

# 2. Rebuild e restart (zero-downtime se healthcheck passa)
docker-compose -f docker-compose.prod.yml up -d --build

# 3. Verifica
docker-compose ps
curl https://api.miracollo.com/api/health

# === ROLLBACK SE PROBLEMI ===

# 1. Rollback git
git checkout HEAD~1

# 2. Rebuild
docker-compose -f docker-compose.prod.yml up -d --build
```

### 3.4 Workflow Deploy (VECCHIO - Evitare!)

```bash
# SBAGLIATO! Non fare piu cosi:

docker stop miracollo-backend-vecchio
docker run -d --name miracollo-backend-nuovo -p 8001:8001 ...

# Problemi:
# - Nomi cambiano ogni volta
# - Port mapping inconsistente
# - Network non gestita
# - Facile dimenticare container vecchi
```

---

## 4. CHECKLIST DEPLOY SICURI

### Pre-Deploy

```
[ ] Codice testato (locale o lab)
[ ] Commit pushato su GitHub
[ ] Backup database fatto (automatico ogni 6h, ma verificare)
[ ] docker-compose.prod.yml aggiornato se necessario
```

### Deploy

```
[ ] ssh miracollo-cervella
[ ] cd /app/miracollo
[ ] git pull origin main
[ ] docker-compose -f docker-compose.prod.yml up -d --build
[ ] docker-compose ps (tutti healthy?)
[ ] curl https://api.miracollo.com/api/health
```

### Post-Deploy

```
[ ] Monitorare logs 10 minuti: docker-compose logs -f
[ ] Testare funzionalita critiche (suggestions, properties)
[ ] Verificare nessun container orfano: docker ps -a
```

### Rollback (se problemi)

```
[ ] git checkout HEAD~1 (o commit specifico)
[ ] docker-compose -f docker-compose.prod.yml up -d --build
[ ] Verificare ritorno a stato precedente
[ ] Documentare cosa e andato storto in .sncp/
```

---

## 5. SERVE UN LAB LOCALE?

### Risposta: SI, ma OPZIONALE

**Per moduli nuovi (come Room Manager):**
- Sviluppo LOCALE con DB fake
- Test su LAB Docker (VM o locale)
- Deploy su PROD

**Per fix piccoli (bug, hotfix):**
- Fix diretto su VM (con attenzione)
- Test immediato
- Commit

### Setup Lab (da fare quando serve)

```bash
# OPZIONE A: Lab su VM (consigliato)
/app/miracollo-lab/          # Directory separata
docker-compose.lab.yml       # Porta 8001, DB lab

# OPZIONE B: Lab locale (per sviluppo pesante)
~/Developer/miracollogeminifocus-lab/
docker-compose -f docker-compose.lab.yml up -d
```

### Quando Usare Lab

| Situazione | Lab Necessario? |
|------------|-----------------|
| Bug fix piccolo | NO - testa su prod |
| Modulo nuovo | SI - sviluppa su lab |
| Migrazione database | SI - testa prima su lab |
| Refactoring grosso | SI - testa su lab |
| Hotfix urgente | NO - fix diretto con backup |

---

## 6. BEST PRACTICES

### 6.1 Container Naming

```
SCHEMA: {app}-{service}

Esempi:
  miracollo-backend    (NO numeri!)
  miracollo-nginx
  miracollo-frontend
  cervella-ai
```

**EVITARE:**
- miracollo-backend-12 (numero = segno di duplicati)
- miracollo-backend-new (confusione futura)
- backend-prod-test-v2 (troppo lungo)

### 6.2 Network Isolation

```
SEMPRE usare network dedicata:

docker network create miracollo-net

Benefici:
- Container comunicano via nome (es. http://backend:8000)
- Isolati da altri container
- No port exposure necessaria per comunicazione interna
```

### 6.3 Port Exposure

```
REGOLA: Esponi SOLO quello che serve

CORRETTO:
  nginx: 80, 443 (serve per utenti)
  backend: NESSUNA (nginx fa proxy)

SBAGLIATO:
  nginx: 80, 443
  backend: 8001 (perche? utenti non accedono direttamente)
```

### 6.4 Zero-Downtime Deploy

```bash
# Con docker-compose e healthcheck:

docker-compose up -d --build

# Compose:
# 1. Builda nuova immagine
# 2. Crea nuovo container
# 3. Aspetta healthcheck pass
# 4. Switcha traffico
# 5. Rimuove vecchio container

# Risultato: zero-downtime!
```

---

## 7. AZIONI RACCOMANDATE

### IMMEDIATO (Oggi)

| # | Azione | Tempo | Owner |
|---|--------|-------|-------|
| 1 | Verificare backend-12 risponde | 5 min | Rafa/Regina |
| 2 | Rimuovere backend-35 | 2 min | Rafa/Regina |
| 3 | Verificare sistema funziona | 5 min | Rafa/Regina |

### QUESTA SETTIMANA

| # | Azione | Tempo | Owner |
|---|--------|-------|-------|
| 4 | Creare docker-compose.prod.yml | 1 ora | cervella-devops |
| 5 | Testare deploy con compose | 30 min | cervella-devops |
| 6 | Migrare da container manuali a compose | 30 min | cervella-devops |
| 7 | Documentare workflow in CLAUDE.md VM | 15 min | Regina |

### QUESTO MESE

| # | Azione | Tempo | Owner |
|---|--------|-------|-------|
| 8 | Setup Lab su VM | 2 ore | cervella-devops |
| 9 | Script deploy automatico | 1 ora | cervella-devops |
| 10 | CI/CD pipeline (opzionale) | 4 ore | cervella-devops |

---

## 8. RISPOSTA ALLE DOMANDE

### 1. Perche ci sono 2 container backend?

**Risposta:** Deploy manuali senza cleanup.
Qualcuno ha creato backend-35, poi backend-12 in una rete diversa, senza rimuovere il primo.
NON e intenzionale (blue-green), e un errore operativo.

### 2. Quale workflow e corretto?

**Risposta:** docker-compose up (crea container automaticamente).
- Nomi fissi (miracollo-backend, non backend-N)
- Rete gestita automaticamente
- Nessun rischio duplicati

### 3. Serve un lab locale?

**Risposta:** SI, ma solo per moduli nuovi.
Per fix piccoli, lavorare direttamente su VM con backup.

### 4. Qual e la best practice?

**Deploy:**
```bash
cd /app/miracollo
git pull origin main
docker-compose -f docker-compose.prod.yml up -d --build
```

**Testing:**
- Moduli nuovi: lab prima, prod dopo
- Fix piccoli: prod diretta con backup

**Manutenzione:**
- Logs: docker-compose logs -f
- Restart: docker-compose restart backend
- Status: docker-compose ps

---

## 9. VERDETTO GUARDIANA OPS

```
+==================================================================+
|                                                                  |
|   VERDICT: APPROVATO CON AZIONI                                  |
|                                                                  |
|   SECURITY:     OK (backend-35 rimozione migliora sicurezza)     |
|   PERFORMANCE:  OK (meno risorse sprecate)                       |
|   RELIABILITY:  MIGLIORA (docker-compose = riproducibilita)      |
|   DEPLOY-READY: SI (dopo implementare compose)                   |
|                                                                  |
|   RISCHIO ATTUALE: MEDIO (container orfani = confusione)         |
|   RISCHIO DOPO FIX: BASSO (compose = deploy sicuri)              |
|                                                                  |
+==================================================================+
```

### Priorita Fix

1. **P0 (ORA):** Rimuovere backend-35
2. **P1 (Settimana):** Creare docker-compose.prod.yml
3. **P2 (Mese):** Setup Lab + Script deploy

---

## 10. COMANDI RAPIDI

### Cleanup Immediato

```bash
# Rimuovi container orfano
docker stop miracollo-backend-35 && docker rm miracollo-backend-35

# Verifica stato
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

### Deploy con Compose (dopo averlo creato)

```bash
# Deploy
docker-compose -f docker-compose.prod.yml up -d --build

# Logs
docker-compose -f docker-compose.prod.yml logs -f

# Restart singolo servizio
docker-compose -f docker-compose.prod.yml restart backend

# Status
docker-compose -f docker-compose.prod.yml ps
```

### Backup Before Changes

```bash
# Backup database
cp /app/miracollo/backend/data/miracollo.db \
   /home/rafapra/backups/miracollo_$(date +%Y%m%d_%H%M%S).db
```

---

*Report completato da Cervella Guardiana Ops*
*12 Gennaio 2026*

*"Una verifica approfondita ora = zero disastri dopo."*
*"La sicurezza non e negoziabile. Mai."*

---

## APPENDICE: Riferimenti

| Documento | Path |
|-----------|------|
| Audit VM | `.sncp/reports/AUDIT_MIRACOLLO_VM_20260112.md` |
| Protocollo Ibrido | `.sncp/idee/20260111_PROTOCOLLO_IBRIDO_DEFINITIVO.md` |
| Workflow Solo VM | `.sncp/idee/WORKFLOW_MIRACOLLO_SOLO_VM.md` |
| Questo Report | `.sncp/idee/20260112_STRATEGIA_CONTAINER_MIRACOLLO.md` |
