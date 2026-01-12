# AUDIT MIRACOLLO VM - 12 Gennaio 2026

> **Cervella Ingegnera - Audit Completo Infrastruttura**
> 
> **VM:** miracollo-cervella (34.27.179.164)
> **Data:** 2026-01-12 04:00 UTC
> **Durata Audit:** 15 minuti
> **Problemi Trovati:** 18 (5 CRITICI, 7 ALTO, 4 MEDIO, 2 BASSO)

---

## EXECUTIVE SUMMARY

**Health Score VM: 4/10** ⚠️ ATTENZIONE RICHIESTA

```
Infrastruttura:  🟡 Accettabile (VM stabile, backup ok)
Git & Deploy:    🔴 CRITICO (no repository, no CI/CD)
Database:        🔴 CRITICO (tabella mancante, errori runtime)
Docker:          🟡 Issues (container duplicati, no compose)
Sicurezza:       🔴 CRITICO (secrets esposti, no SSL gestito)
Organizzazione:  🔴 ALTO (file sparsi, nessuna struttura)
Applicazione:    🟡 Funzionante ma con errori
```

### Top 3 Problemi SHOW-STOPPER

1. **NO GIT REPOSITORY** - Impossibile tracciare modifiche, fare rollback, collaborare
2. **TABELLA DATABASE MANCANTE** - `suggestion_applications` causa errori ogni 2 minuti
3. **FILE SPARSI OVUNQUE** - 19 file Python in HOME, codice duplicato, zero organizzazione

---

## PROBLEMI TROVATI (per Priorità)

### 🔥 CRITICI (Fix Immediato!)

#### 1. NO GIT REPOSITORY
**Severità:** CRITICO
**Impact:** Deploy manuale, no rollback, no versioning, collaborazione impossibile

**Stato:**
```bash
/home/rafapra/app:           NOT a git repository
/home/rafapra/cervella-ai:   NOT a git repository
```

**Conseguenze:**
- Impossibile fare rollback se qualcosa si rompe
- Nessun tracking di chi/cosa/quando cambia
- Deploy manuale = alto rischio errori
- Collaborazione impossibile
- No CI/CD pipeline

**Come Fixare:**
```bash
# 1. Verificare quale repo è corretto (locale o GitHub)
# 2. Fare git clone su VM
# 3. Configurare credenziali
# 4. Configurare deploy automatico

Tempo: 30 minuti
```

**Effort:** MEDIO
**Priority:** P0 (blocca tutto il resto)

---

#### 2. DATABASE - TABELLA MANCANTE
**Severità:** CRITICO
**Impact:** Errori runtime ogni 2 minuti, notification worker ROTTO

**Errore:**
```
2026-01-12 04:00:00 ERROR - no such table: suggestion_applications
```

**Diagnosi:**
- Worker cerca tabella che non esiste
- Probabilmente migrazione Alembic mai applicata
- MA: `/app/backend/migrations/versions/*.py` NON ESISTE!
- Alembic NON configurato sulla VM

**Come Fixare:**
```bash
# OPZIONE A: Se migrations esistono nel repo
cd /home/rafapra/app/backend
alembic upgrade head

# OPZIONE B: Creare migration mancante
# (serve verificare schema atteso)

# OPZIONE C: Disabilitare worker temporaneamente
# (non risolve, ma ferma errori)

Tempo: 1-2 ore (dipende se migrations esistono)
```

**Effort:** ALTO
**Priority:** P0 (errori continui in produzione)

---

#### 3. GIT CREDENTIALS NON CONFIGURATE
**Severità:** CRITICO
**Impact:** Impossibile push/pull da GitHub

**Stato:**
```bash
git config --global --list
# fatal: unable to read config file '/home/rafapra/.gitconfig': No such file or directory
```

**Mancante:**
- `user.name`
- `user.email`
- Credenziali GitHub (token o SSH)

**Come Fixare:**
```bash
# 1. Configurare git globale
git config --global user.name "Rafa"
git config --global user.email "email@miracollo.com"

# 2. Aggiungere GitHub SSH key
ssh-keygen -t ed25519 -C "miracollo-vm"
# (key già esiste: ~/.ssh/id_ed25519)
# Aggiungere pub key a GitHub

# 3. Testare connessione
ssh -T git@github.com

Tempo: 15 minuti
```

**Effort:** BASSO
**Priority:** P0 (prerequisito per #1)

---

#### 4. SSL CERTIFICATES NON VERIFICABILI
**Severità:** CRITICO
**Impact:** Se scadono, tutto down. Non possiamo verificare stato.

**Problema:**
```bash
ls /etc/letsencrypt/live/*/fullchain.pem
# No such file or directory (dentro container nginx!)

crontab -l
# command not found (cron NON installato!)
```

**Diagnosi:**
- Certificati probabilmente gestiti FUORI container
- Nessun auto-renewal configurato visibile
- Impossibile verificare scadenza
- RISCHIO: Certificati scadono → sito down

**Come Fixare:**
```bash
# 1. Verificare dove sono i certificati REALI
find /etc -name "*miracollo.com*" 2>/dev/null

# 2. Verificare se certbot è installato
which certbot

# 3. Configurare auto-renewal
sudo certbot renew --dry-run

# 4. Testare scadenza
openssl s_client -connect api.miracollo.com:443 -servername api.miracollo.com \
  | openssl x509 -noout -dates

Tempo: 1 ora (investigation + setup)
```

**Effort:** MEDIO
**Priority:** P1 (può causare downtime futuro)

---

#### 5. SECRETS ESPOSTI IN DOCKER INSPECT
**Severità:** CRITICO (Sicurezza)
**Impact:** Chiunque con accesso Docker vede tutte le API keys

**Problema:**
```bash
docker inspect miracollo-backend-35 --format='{{range .Config.Env}}{{println .}}{{end}}'
# SECRET_KEY=tbfmXf0AbSrXIpbAgmHICOEcj8XDHjHAl-MwbHnCdhs
# GEMINI_API_KEY=...
# META_WHATSAPP_ACCESS_TOKEN=...
# (TUTTI I SECRETS VISIBILI!)
```

**Conseguenze:**
- Chiunque con accesso SSH può leggere secrets
- `docker inspect` mostra tutto in chiaro
- Log Docker potrebbero contenere secrets
- Nessun secret rotation possibile

**Come Fixare:**
```bash
# OPZIONE A: Docker Secrets (richiede swarm mode)
# OPZIONE B: Mount .env come volume read-only
docker run -v /secure/.env:/app/.env:ro ...

# OPZIONE C: HashiCorp Vault (overkill)
# OPZIONE D: Google Secret Manager (già su GCP)

Raccomandazione: Google Secret Manager + env injection

Tempo: 2-3 ore
```

**Effort:** ALTO
**Priority:** P1 (sicurezza, ma non immediato se VM privata)

---

### 🟠 ALTO (Fix Urgente)

#### 6. FILE PYTHON SPARSI IN HOME DIRECTORY
**Severità:** ALTO
**Impact:** Confusione, rischio di usare file sbagliati, zero organizzazione

**Trovati in `/home/rafapra`:**
```
bucchi_engine.py
current_main.py (11KB)
current_routers_init.py
main.py (12KB)
main_backup.py (11KB)
main_final.py (11KB)
main_no_revenue.py (11KB)
main_pricing_added.py (11KB)
research_orchestrator.py
revenue_bucchi.py
revenue_research.py
revenue_suggestions.py
routers_init.py
routers_init_current.py
routers_init_minimal.py (VUOTO!)
routers_init_no_revenue.py
suggerimenti_actions.py (17KB)
suggerimenti_engine.py (12KB)

deploy_pricing_tracking_20260110_174159.log
```

**Problema:**
- 19 file fuori posto
- 6 versioni di `main.py` (quale è quella vera?!)
- File vuoti (`routers_init_minimal.py`)
- Log file non ruotati

**Come Fixare:**
```bash
# 1. VERIFICARE quale main.py è in uso
docker exec miracollo-backend-35 cat /app/main.py | md5sum
md5sum ~/app/backend/main.py
md5sum ~/main.py
# → Confrontare hash

# 2. ARCHIVIARE (non cancellare subito!)
mkdir -p ~/archive_cleanup_20260112
mv ~/*.py ~/archive_cleanup_20260112/
mv ~/*.log ~/archive_cleanup_20260112/

# 3. DOCUMENTARE cosa erano
ls -lh ~/archive_cleanup_20260112/ > ~/CLEANUP_INVENTORY.txt

# 4. Dopo 1 settimana senza problemi: cancellare

Tempo: 30 minuti
```

**Effort:** BASSO
**Priority:** P1 (rischio confusione alto)

---

#### 7. CONTAINER BACKEND DUPLICATI
**Severità:** ALTO
**Impact:** Confusione, spreco risorse, quale serve alle requests?

**Stato:**
```
miracollo-backend-12   Up 7 hours   (NO port mapping!)
miracollo-backend-35   Up 7 hours   0.0.0.0:8001->8001/tcp (ACTIVE)
```

**Problema:**
- 2 container backend running
- Solo backend-35 è esposto (porta 8001)
- backend-12 NON ha porte mappate → INUTILE
- Creato 8h dopo backend-35

**Perché Successo:**
Probabilmente deploy manuale:
```bash
# Sessione 1: Deploy iniziale
docker run ... --name miracollo-backend-35

# Sessione 2: "Rifaccio deploy" (dimenticando di fermare)
docker run ... --name miracollo-backend-12
```

**Come Fixare:**
```bash
# 1. Verificare quale serve requests
docker logs -f miracollo-backend-12 &
docker logs -f miracollo-backend-35 &
# → Fare request a http://vm:8001/health
# → Vedere quale logga

# 2. Fermare inutile (probabilmente backend-12)
docker stop miracollo-backend-12
docker rm miracollo-backend-12

# 3. Implementare deploy script
# (così non succede più)

Tempo: 15 minuti
```

**Effort:** BASSO
**Priority:** P1 (spreco risorse)

---

#### 8. NO DOCKER COMPOSE FILE
**Severità:** ALTO
**Impact:** Deploy manuale, configurazione sparsa, riproducibilità zero

**Stato:**
```bash
find /home/rafapra -name 'docker-compose*.yml'
# (nessun risultato)

docker inspect miracollo-backend-35 --format='{{.Config.Labels}}'
# map[] (nessun label compose)
```

**Conseguenze:**
- Container avviati manualmente con `docker run`
- Configurazione non documentata
- Impossibile ricreare setup identico
- Network, volumi, dipendenze = tutti manuali
- Restart dopo reboot = manuale

**Come Fixare:**
```bash
# 1. RICOSTRUIRE docker-compose.yml da container running
# (cervella-backend può farlo!)

# 2. Testare in locale
docker-compose up -d

# 3. Migrare VM a docker-compose
docker stop miracollo-backend-35
docker-compose -f docker-compose.prod.yml up -d

Tempo: 2 ore
```

**Effort:** MEDIO
**Priority:** P1 (prerequisito per automation)

---

#### 9. NO FRONTEND BUILD
**Severità:** ALTO
**Impact:** Frontend probabilmente servito da dove? Come è deployato?

**Problema:**
```bash
ls /home/rafapra/app/frontend/dist
# No such file or directory
```

**Domande:**
- Il frontend è buildato?
- Dove sono i file statici?
- Come li serve nginx?
- Chi fa il build? Quando?

**Ipotesi:**
- Frontend build è DENTRO container nginx
- Oppure servito da CDN
- Oppure NON deployato (solo backend API)

**Come Verificare:**
```bash
# 1. Check nginx container
docker exec miracollo-nginx ls /usr/share/nginx/html

# 2. Check nginx config
docker exec miracollo-nginx cat /etc/nginx/conf.d/default.conf

# 3. Verificare se frontend funziona
curl -I https://api.miracollo.com/

Tempo: 30 minuti investigation
```

**Effort:** BASSO (investigation)
**Priority:** P2 (se frontend funziona, non urgente)

---

#### 10. ALEMBIC MIGRATIONS NON CONFIGURATE
**Severità:** ALTO
**Impact:** Impossibile gestire schema database, migrazioni manuali = caos

**Problema:**
```bash
ls /home/rafapra/app/backend/migrations/versions/*.py
# No such file or directory

find /home/rafapra/app/backend -name 'alembic.ini'
# (nessun file trovato)
```

**Conseguenze:**
- Nessuna migrazione database tracciata
- Schema modificato manualmente
- Impossibile replicare database
- Impossibile rollback schema
- Collaboration impossibile

**Come Fixare:**
```bash
# 1. Verificare se migrations esistono nel repo
# (dopo aver risolto #1 - Git)

# 2. Inizializzare Alembic
cd /home/rafapra/app/backend
alembic init migrations

# 3. Generare migrazione da schema attuale
alembic revision --autogenerate -m "Initial schema"

# 4. Applicare
alembic upgrade head

Tempo: 1 ora (se schema stabile)
```

**Effort:** MEDIO
**Priority:** P1 (collegato a #2)

---

#### 11. TAR ARCHIVES VECCHI IN APP/
**Severità:** ALTO (Disk Space)
**Impact:** 4.1MB sprecati, confusione

**Trovati:**
```
app/backend.tar.gz       1.9MB (4 Jan)
app/miracollo_full.tar.gz 2.2MB (4 Jan)
```

**Problema:**
- Archive vecchi (8 giorni)
- Mai usati (probabilmente backup manuali)
- Occupano spazio
- Confusione su cosa contengono

**Come Fixare:**
```bash
# 1. Verificare contenuto
tar -tzf app/backend.tar.gz | head -20
tar -tzf app/miracollo_full.tar.gz | head -20

# 2. Se sono backup: spostare in ~/backups/
mv app/*.tar.gz ~/backups/manual/

# 3. Se inutili: eliminare
rm app/*.tar.gz

Tempo: 5 minuti
```

**Effort:** BASSO
**Priority:** P2 (cleanup)

---

### 🟡 MEDIO (Fix Consigliato)

#### 12. LOG ROTATION NON CONFIGURATO
**Severità:** MEDIO
**Impact:** Log Docker crescono all'infinito → disk full futuro

**Problema:**
```bash
ls /etc/logrotate.d/docker*
# No such file or directory
```

**Conseguenze:**
- Log Docker non ruotati
- `/var/lib/docker/containers/*/logs` crescono
- Rischio disk full tra mesi

**Come Fixare:**
```bash
# 1. Configurare Docker log rotation globale
cat > /etc/docker/daemon.json << 'EOF'
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
EOF

# 2. Restart Docker
sudo systemctl restart docker

# 3. Verificare
docker info | grep -A 5 "Logging Driver"

Tempo: 15 minuti
```

**Effort:** BASSO
**Priority:** P2 (preventivo)

---

#### 13. CRON NON INSTALLATO
**Severità:** MEDIO
**Impact:** Nessun task schedulato possibile, backup manuali

**Problema:**
```bash
crontab -l
# command not found
```

**Ma:**
- Backup automatici FUNZIONANO (ogni 6h!)
- Come? Probabilmente systemd timers o Docker healthcheck

**Investigation Needed:**
```bash
# Verificare come funzionano backup
systemctl list-timers
docker inspect miracollo-backend-35 | grep -i health
```

**Come Fixare (se serve cron):**
```bash
sudo apt update
sudo apt install -y cron
sudo systemctl enable --now cron

Tempo: 5 minuti
```

**Effort:** BASSO
**Priority:** P3 (nice to have)

---

#### 14. CERVELLA-AI DEPRECATION WARNING
**Severità:** MEDIO
**Impact:** Breaking change futuro LangChain

**Warning:**
```
LangChainDeprecationWarning: The class `HuggingFaceEmbeddings` was deprecated 
in LangChain 0.2.2 and will be removed in 1.0.
Use: from langchain_huggingface import HuggingFaceEmbeddings
```

**Come Fixare:**
```bash
# 1. Update cervella-ai/requirements.txt
pip install langchain-huggingface

# 2. Update import in retriever.py
# OLD: from langchain.embeddings import HuggingFaceEmbeddings
# NEW: from langchain_huggingface import HuggingFaceEmbeddings

# 3. Rebuild container
docker build -t cervella-ai:latest .
docker restart cervella-ai

Tempo: 20 minuti
```

**Effort:** BASSO
**Priority:** P3 (non urgente, ma da fare)

---

#### 15. DOCKER VOLUMES ANONIMI
**Severità:** MEDIO
**Impact:** Impossibile capire cosa contengono, cleanup difficile

**Trovati:**
```
3cde8f1cee791275993bc8d36946b6d5b96375b130f831cb35392a2be85d1431
276b3a61ab5ec2a8b07547418fc1ea209c1f5790173d48a5acc26e457a8eb701
94663c6e06175200231d9dd8ef73f4d061052282613b918f4fd4928463bce915
```

**Problema:**
- 3 volumi con nomi hash
- Impossibile sapere contenuto
- Impossibile sapere quale container li usa
- Cleanup pericoloso

**Come Verificare:**
```bash
# Vedere quale container usa quali volumi
docker ps -a --format '{{.Names}}' | while read container; do
  echo "=== $container ==="
  docker inspect $container --format '{{range .Mounts}}{{.Name}} → {{.Destination}}{{println}}{{end}}'
done

# Verificare size
docker system df -v | grep -A 10 "Local Volumes"
```

**Come Fixare:**
```bash
# Se volume non usato: rimuovere
docker volume rm <volume_id>

# Se usato: rinominare logicamente (richiede recreate container)
docker volume create miracollo_data
# ... migrate data ...

Tempo: 1 ora (investigation + cleanup)
```

**Effort:** MEDIO
**Priority:** P3 (organizzazione)

---

### 🔵 BASSO (Nice to Have)

#### 16. NGINX CONFIG NON ACCESSIBILE
**Severità:** BASSO
**Impact:** Difficile debugging, configurazione nascosta

**Problema:**
```bash
docker exec miracollo-nginx ls /etc/nginx/conf.d/*.conf
# No such file or directory
```

**Probabile:**
- Config in `/etc/nginx/nginx.conf` (default)
- Oppure montato da volume esterno

**Come Verificare:**
```bash
docker exec miracollo-nginx cat /etc/nginx/nginx.conf
docker inspect miracollo-nginx --format='{{range .Mounts}}{{.Source}} → {{.Destination}}{{println}}{{end}}'
```

**Effort:** BASSO
**Priority:** P4 (investigation)

---

#### 17. SSH KEY CREATO MA NON USATO?
**Severità:** BASSO
**Impact:** Key creato oggi ma Git non configurato

**File:**
```
-rw------- 1 rafapra rafapra 411 Jan 12 03:55 id_ed25519
-rw-r--r-- 1 rafapra rafapra 103 Jan 12 03:55 id_ed25519.pub
```

**Domanda:**
- Key creato 2h fa (04:02 - 03:55 = ~7 min prima audit)
- Da chi? Rafa? Script automatico?
- Non aggiunto a GitHub (Git ancora non funziona)

**Action:**
- Aggiungere pub key a GitHub
- Testare connessione

**Effort:** 5 minuti
**Priority:** P4 (parte di #3)

---

#### 18. ENV FILES MULTIPLI
**Severità:** BASSO
**Impact:** Confusione, quale è usato?

**Trovati in `/home/rafapra/app`:**
```
.env (43 bytes) 
.env.production (4923 bytes)
```

**Problema:**
- `.env` troppo piccolo (43 bytes = quasi vuoto)
- `.env.production` ha tutti i secrets
- Quale usa il container?

**Come Verificare:**
```bash
docker exec miracollo-backend-35 env | grep DATABASE_URL
# Confrontare con .env vs .env.production
```

**Raccomandazione:**
- Usare SOLO `.env.production`
- Eliminare `.env` se vuoto
- Documentare quale file serve a cosa

**Effort:** 5 minuti
**Priority:** P4 (cleanup)

---

## INFRASTRUTTURA VM (Stato Generale)

### ✅ Cose Che Funzionano Bene

**VM Health:**
```
Hostname:     miracollo-cervella ✅
Uptime:       11 giorni, 2 ore ✅
Disk:         22GB/39GB (56% used) ✅
Memory:       1.7GB/3.8GB (49.6% used) ✅
Load:         0.08 (molto basso) ✅
```

**Docker Containers:**
```
miracollo-nginx      HEALTHY, 33h uptime ✅
miracollo-backend-35 HEALTHY, 7h uptime ✅
cervella-ai          HEALTHY, 38h uptime ✅
```

**Restart Policies:**
```
nginx:   unless-stopped ✅
backend: unless-stopped ✅
```

**Backup Database:**
```
Frequenza: Ogni 6 ore ✅
Ultimo:    12 Jan 00:00 (4h fa) ✅
Retention: ~5 giorni visibili ✅
Size:      992KB costante ✅
```

**API Health:**
```
Status:    healthy ✅
Version:   1.7.0 ✅
Database:  connected ✅
Uptime:    56 anni (bug timestamp, ma connesso) ✅
```

---

## RACCOMANDAZIONI PRIORITARIE

### Sprint 1: Git & Deploy (URGENTE)

**Obiettivo:** Ripristinare version control e deploy sicuro

**Checklist:**
- [ ] Configurare Git globale (user.name, user.email)
- [ ] Aggiungere SSH key a GitHub
- [ ] Clonare repository corretto
- [ ] Verificare branch (main? production?)
- [ ] Testare push/pull
- [ ] Creare script deploy automatico
- [ ] Documentare workflow deploy

**Tempo Stimato:** 2 ore
**Owner:** cervella-backend + Rafa (decisioni repo)

---

### Sprint 2: Database Fix (CRITICO)

**Obiettivo:** Eliminare errori runtime notification worker

**Checklist:**
- [ ] Trovare migration mancante (local repo)
- [ ] Applicare migration su VM
- [ ] Verificare tabella `suggestion_applications` esiste
- [ ] Restart notification worker
- [ ] Monitorare logs (no more errors)

**Tempo Stimato:** 1-2 ore
**Owner:** cervella-backend

---

### Sprint 3: Cleanup & Organization (ALTO)

**Obiettivo:** Eliminare caos file system

**Checklist:**
- [ ] Archiviare 19 file .py da HOME
- [ ] Rimuovere container backend-12 inutile
- [ ] Spostare tar.gz in backups/
- [ ] Creare docker-compose.yml
- [ ] Testare restart con compose
- [ ] Documentare struttura directory

**Tempo Stimato:** 2 ore
**Owner:** cervella-backend

---

### Sprint 4: Security Hardening (MEDIO)

**Obiettivo:** Proteggere secrets e verificare SSL

**Checklist:**
- [ ] Migrare secrets a Google Secret Manager
- [ ] Verificare certificati SSL
- [ ] Configurare auto-renewal SSL
- [ ] Configurare log rotation Docker
- [ ] Audit permessi file
- [ ] Rotate SECRET_KEY (se possibile)

**Tempo Stimato:** 3 ore
**Owner:** cervella-backend + infra

---

### Sprint 5: Alembic & Migrations (MEDIO)

**Obiettivo:** Gestione schema database professionale

**Checklist:**
- [ ] Setup Alembic nel repo
- [ ] Generare initial migration da schema attuale
- [ ] Testare migration su VM staging
- [ ] Applicare su produzione
- [ ] Documentare workflow migrations

**Tempo Stimato:** 2 ore
**Owner:** cervella-backend

---

## METRICHE FINALI

### Issues per Categoria

| Categoria | CRITICI | ALTO | MEDIO | BASSO | TOTALE |
|-----------|---------|------|-------|-------|--------|
| Git & Deploy | 2 | 0 | 0 | 1 | 3 |
| Database | 1 | 1 | 0 | 0 | 2 |
| Docker | 0 | 2 | 1 | 0 | 3 |
| Sicurezza | 2 | 0 | 0 | 0 | 2 |
| Organizzazione | 0 | 3 | 1 | 2 | 6 |
| Applicazione | 0 | 1 | 2 | 0 | 3 |
| **TOTALE** | **5** | **7** | **4** | **3** | **19** |

### Effort Totale Stimato

```
CRITICI:  5 issues × 1.5h avg = 7.5 ore
ALTO:     7 issues × 1.0h avg = 7.0 ore
MEDIO:    4 issues × 0.5h avg = 2.0 ore
BASSO:    3 issues × 0.2h avg = 0.6 ore
-------------------------------------------
TOTALE:                        17.1 ore ≈ 2.5 giorni
```

### Risk Score

```
Infrastruttura:   BASSO (VM stabile)
Deploy:           ALTO (no git, no automation)
Data Loss:        MEDIO (backup ok, ma no migrations)
Security:         ALTO (secrets esposti)
Maintainability:  CRITICO (caos organizzazione)

OVERALL RISK: ALTO ⚠️
```

---

## NEXT ACTIONS

### Immediate (Oggi)

1. **Configurare Git** (15 min)
   - `git config --global user.name "Rafa"`
   - `git config --global user.email "..."`
   - Aggiungere SSH key a GitHub

2. **Verificare quale repo clonare** (Rafa decide)
   - Locale CervellaSwarm o GitHub?
   - Quale branch? (main? production?)

3. **Archiviare file sparsi** (15 min)
   - `mkdir ~/archive_cleanup_20260112`
   - `mv ~/*.py ~/*.log ~/archive_cleanup_20260112/`

### This Week

4. **Clonare repo e deploy** (2h)
5. **Fixare database table** (1-2h)
6. **Creare docker-compose.yml** (1h)
7. **Rimuovere container duplicato** (15 min)

### This Month

8. **Setup Alembic migrations** (2h)
9. **Migrare secrets a Secret Manager** (3h)
10. **Audit completo sicurezza** (4h)

---

## CONCLUSIONI

**La VM funziona**, ma è in uno stato **"funziona per miracolo"**:
- Nessun version control
- Deploy manuali
- File sparsi ovunque
- Container duplicati
- Database con errori
- Secrets esposti

**È PRODUCTION-READY?** 🟡 Sì, ma fragile

**È MAINTAINABLE?** 🔴 No

**Priority assoluta:** Git + Deploy automation

Senza Git, OGNI altra modifica è pericolosa perché:
- Non possiamo fare rollback
- Non possiamo tracciare cambiamenti
- Non possiamo collaborare
- Non possiamo automatizzare

**Raccomandazione:** STOP nuove feature, START cleanup infrastrutturale.

---

*Audit completato da Cervella Ingegnera*
*12 Gennaio 2026 - 04:15 UTC*

*"Il codice pulito è un regalo per il te stesso di domani!"*
